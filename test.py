from math import sqrt
import numpy as np
from random import randint
import datetime


##生成kd树
def createTree(dataSet, layer=0):
    #Calculate the length of the data, which may be zero during the iteration
    length = len(dataSet)
    if(length == 0):
        return
    #Calculate the variance of each dimension, with the large variance as the partition
    variance = []
    for i in range(np.array(dataSet).shape[1]):
        variance.append(np.std(np.array(dataSet)[:, i]))
    #Record the subscript of feature with large variance
    featureindex= np.argmax(variance)
    #deep copy
    dataSetCopy = dataSet[:]
    #Sort to find the median for the next step
    dataSetCopy.sort(key=lambda x: x[featureindex])
    layer += 1
    #when length of data only one
    if length == 1:
        return {'Value': dataSet[0], 'Layer': layer, 'feature': featureindex, 'Left': None, 'Right': None}
    #when length more than one
    elif length != 1:
        #median index
        midNum = length // 2
        #seprate left and right generate tree
        dataSetLeft = dataSetCopy[:midNum]
        dataSetRight = dataSetCopy[midNum + 1:]
        return {'Value': dataSetCopy[midNum], 'Layer': layer, 'feature': featureindex,
                'Left': createTree(dataSetLeft, layer)
            , 'Right': createTree(dataSetRight, layer)}


# conpute educis distance
def calDistance(sourcePoint, targetPoint):
    length = len(targetPoint)
    sum = 0.0
    for i in range(length):
        sum += (sourcePoint[i] - targetPoint[i]) ** 2
    sum = sqrt(sum)
    return sum


# DFS algorithm
def dfs(kdTree, target, tracklist=[]):
    #when  iteration need to iteration ro generate
    tracklistCopy = tracklist[:]
    #the mark of iteration's end
    if not kdTree:
        return None, tracklistCopy
    #DFS algorithm sequence of search is left to right
    elif not kdTree['Left']:
        tracklistCopy.append(kdTree['Value'])
        return kdTree['Value'], tracklistCopy
    #when left continue to iteration
    elif kdTree['Left']:
        pointValue = kdTree['Value']
        feature = kdTree['feature']
        tracklistCopy.append(pointValue)
        # return kdTree['Value'], tracklistCopy
        if target[feature] <= pointValue[feature]:
            return dfs(kdTree['Left'], target, tracklistCopy)
        elif target[feature] > pointValue[feature]:
            return dfs(kdTree['Right'], target, tracklistCopy)


# A function use to find a point in KDtree
def findPoint(Tree, value):
    #find generate tree
    if Tree != None and Tree['Value'] == value:
        return Tree
    #Tree is None
    else:
        if Tree == None:
            return
        if Tree['Left'] != None:
            return findPoint(Tree['Left'], value) or findPoint(Tree['Right'], value)


# KDtree search algorithm
def kdTreeSearch(tracklist, target, usedPoint=[], minDistance=float('inf'), minDistancePoint=None):
    #deep copy
    tracklistCopy = tracklist[:]
    usedPointCopy = usedPoint[:]

    #from tree node to compute
    minDistancePoint = tracklistCopy[-1]

    #only one element
    if len(tracklistCopy) == 1:
        return minDistancePoint
    #start to iteration
    else:
        #find track's tree
        point = findPoint(kdTree, tracklist[-1])
        #define anotherPoint to search
        anotherPoint=None
        #if Distance smaller than minDistance
        if calDistance(point['Value'], target) < minDistance:
            minDistance = calDistance(point['Value'], target)
            minDistancePoint = point['Value']
        #find fatherpoint
        fatherPoint = findPoint(kdTree, tracklistCopy[-2])
        fatherPointval = fatherPoint['Value']
        fatherPointfea = fatherPoint['feature']

        #judge fatherpoint wheather the smallest
        if calDistance(fatherPoint['Value'], target) < minDistance:
            minDistance = calDistance(fatherPoint['Value'], target)
            minDistancePoint = fatherPoint['Value']

        #find another Point
        if point == fatherPoint['Left']:
            anotherPoint = fatherPoint['Right']
        elif point == fatherPoint['Right']:
            anotherPoint = fatherPoint['Left']
        #judge another point
        if (anotherPoint == None or anotherPoint['Value'] in usedPointCopy or
        #if fatherPointval[fatherPointfea] - target[fatherPointfea]) > minDistance means it must bigger than minpoint
                abs(fatherPointval[fatherPointfea] - target[fatherPointfea]) > minDistance):
            #delete it from track
            usedPoint = tracklistCopy.pop()
            #add it to usedpoint
            usedPointCopy.append(usedPoint)
            return kdTreeSearch(tracklistCopy, target, usedPointCopy, minDistance, minDistancePoint)
        else:
            # delete it from track
            usedPoint = tracklistCopy.pop()
            # add it to usedpoint
            usedPointCopy.append(usedPoint)
            #find another point's track to help traverse
            subvalue, subtrackList = dfs(anotherPoint, target)
            #add track
            tracklistCopy.extend(subtrackList)
            return kdTreeSearch(tracklistCopy, target, usedPointCopy, minDistance, minDistancePoint)



my_data = np.loadtxt('real.txt').astype('float')
trainingSet = my_data[:,my_data.shape[1]-2:my_data.shape[1]]
trainingSet = [tuple(i) for i in trainingSet]
print(trainingSet)
kdTree = createTree(trainingSet)
print(kdTree)
target = eval(input('Input target point:'))
value, trackList = dfs(kdTree, target)
print(value,trackList)
start = datetime.datetime.now()
nnPoint = kdTreeSearch(trackList, target)
end = datetime.datetime.now()
print(end-start)
print(nnPoint)

