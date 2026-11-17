# Array

## Overview

Array and collection related functions

## of

Converts multiple elements into an array

```javascript
Array.of(...item);
```

| Parameter | Type | Description |
|------|----------|----|
| item | `Object` | Object |

**Return Value**

Type `Array<Object>`
Returns an array

**Example**

```javascript
Array.of(); //[]
Array.of('x', 2, 3, 4); //["x",2,3,4]
Array.of('x', null, 3, 4); //["x",null,3,4]
```

## toList

Converts elements into an array

```javascript
Array.toList(item);
```

| Parameter | Type | Description |
|------|----------|------------------------|
| item | `Object` | Object, if item is an array then returns a clone |

**Return Value**

Type `Array<Object>` Returns an array

**Example**

```javascript
Array.toList(); //null
Array.toList('x', 2, 3, 4); //["x",2,3,4]
Array.toList(['x', 2, 3, 4]); //["x",2,3,4]
Array.toList('x', null, 3, 4); //["x",null,3,4]
Array.toList('x'); //["x"]
Array.toList(null); //[null]
```

## join

Joins the contents of array using separator

```javascript
Array.join(array, separator);
```

| Parameter | Type | Description |
|-----------|----------|---------|
| array     | `Array`  | Array to join |
| separator | `String` | Separator |

**Return Value**

Type `String`
Returns the joined string

**Example**

```javascript
Array.join([1, 2, 3, 4], '-'); //"1-2-3-4"
Array.join([1, 2, 3, 4], null); //"1234"
Array.join([1, null, 3, 4], null); //"134"
Array.join([null, null, null, null], null); //""
Array.join(null, '-'); //null
Array.join(null, null); //null
```

## length

Returns the number of elements in list

```javascript
Array.length(list);
```

| Parameter | Type | Description |
|------|---------|-----------|
| list | `Array` | Array to get length of |

**Return Value**

Type `Integer`
Returns the length of the array, returns 0 if the array is null

**Example**

```javascript
Array.length([1, 2, 3, 4]); //4
Array.length([1, null, 3, 4]); //4
Array.length(null); //0
```

## get

Gets an element from the collection

If it is a List collection, key is an integer index from 0~(len - 1) and returns the value at that position. Accessing out of range will throw an exception. If it is a Map collection, key is the key of the key-value pair and returns the corresponding value.

```javascript
Array.get(list, key);
```

| Parameter | Type | Description |
|------|-----------------------|------------|
| list | `Array` or `Map`      | Collection to get element from |
| key  | `Integer` or `String` | Index or key of the element |

**Return Value**

Type `Object`
Returns the element in the collection, returns null if the element does not exist

**Example**

```javascript
Array.get([{ 'name': '张三' }, { 'name': '李四' }, { 'name': '王五' }], 1); //{name=李四}
Array.get([{ 'name': '张三' }, { 'name': '李四' }, { 'name': '王五' }], -1); //null
Array.get([{ 'name': '张三' }, { 'name': '李四' }, { 'name': '王五' }], 3); //null
Array.get([{ 'name': '张三' }, null, { 'name': '王五' }], 2); //{name=王五}
Array.get({ 'name': '张三' }, 'name'); //张三
Array.get({ 'name': '张三' }, 'age'); //null
Array.get(null, 3); //null
```

## set

Sets the value of an element in the collection. If it is a List collection, replaces the item at key with value. If it is a Map collection, key is the key of the key-value pair.

```javascript
Array.set(list, key, value);
```

| Parameter | Type | Description |
|-------|--------------------|-----------|
| list  | `Array` or `Map`   | Collection to set element in |
| key   | `String\| Integer` | Property value or index |
| value | `Object`           | Value to set |

**Return Value**

Type ``Array``|``Map``
Returns the modified collection

**Example**

```javascript
Array.set({ 'name': '张三' }, 'name', '张三三'); //{"name":"张三三"}
Array.set([{ 'name': '张三', "age": 18 }, { 'name': '张三', "age": 24 }], 'age', 20); //[{ 'name': '张三', "age": 20 }, { 'name': '张三', "age": 20 }]
Array.set([{ 'name': '张三', "age": 18 }, { 'name': '张三', "age": 24 }], 1, 20); //[{ 'name': '张三', "age": 20 }, 20]
```

## add

Adds element item to the end of collection list

```javascript
Array.add(list, item);
```

| Parameter | Type | Description |
|------|----------|-----------|
| list | `Array`  | Collection to add element to |
| item | `Object` | Element to add |

**Return Value**

Type `Array`
Returns the collection with the added element

**Example**

```javascript
Array.add([1, 2, 3, 4, 5, 6], { 'name': '李四' }); //[1,2,3,4,5,6,{"name":"李四"}]
Array.add([1, 2, 3, 4, 5, 6], 12); //[1,2,3,4,5,6,12]
Array.add(null, { 'name': '李四' }); //null
```

## remove

Removes an element from the collection. If the collection is a Map type, item is the key.

```javascript
Array.remove(list, item);
```

| Parameter | Type | Description |
|------|---------------------|----------------|
| list | `Array` or `Map`     | Collection to remove element from |
| item | `Object` or `String` | Element to remove, or key of element |

**Return Value**

Type `Array` or `Map`
Returns the collection with the element removed

**Example**

```javascript
Array.remove([1, 2, 3, 4, 5, 6], { 'name': '李四' }); //[1,2,3,4,5,6]
Array.remove([1, 2, 3, 4, 5, 6], 5); //[1,2,3,4,6]
Array.remove({ 'name': '李四', 'age': 30 }, 'name'); //{"age":30}
Array.remove({ 'name': '李四', 'age': 30 }, 'sex'); //{"name":"李四","age":30}
Array.remove(null, { 'name': '李四' }); //null
Array.remove([null,1,2,3,null], null); //[1,2,3,null]
```

:::warning Notes
If **list** is of `Array` type, remove will only delete the `first matching` element
:::

## removeAll

Removes elements from the collection. If the collection is a Map type, item is the key.

```javascript
Array.removeAll(list, item);
```

| Parameter | Type | Description |
|------|-----------------------------|---------------------|
| list | `Array` or `Map`             | Collection to remove elements from |
| item | `Object` or `String` or `Array` | Element to remove, key of element, or array of elements |

**Return Value**

Type `Array` or `Map`
Returns the collection with elements removed

**Example**

```javascript
Array.removeAll([1, 2, 3, 4, 5, 6], { 'name': '李四' }); //[1,2,3,4,5,6]
Array.removeAll([1, 2, 3, 4, 5, 6], [1,5]); //[2,3,4,6]
Array.removeAll({ 'name': '李四', 'age': 30 }, 'name'); //{"age":30}
Array.removeAll({ 'name': '李四', 'age': 30 }, 'sex'); //{"name":"李四","age":30}
Array.removeAll(null, { 'name': '李四' }); //null
Array.removeAll([null,1,2,3,null], null); //[1,2,3]
Array.removeAll([null,1,2,3,null], [null,1]); //[2,3]
```

:::warning Notes
If **list** is of `Array` type, remove will only delete the `first matching` element
:::

## isEmpty

Determines whether list is an empty collection; returns true if list is `null` or has length 0, otherwise returns false

```javascript
Array.isEmpty(list);
```

| Parameter | Type | Description |
|------|-----------------|-----------|
| list | `Array` or `Map` | Collection to check length of |

**Return Value**

Type `Boolean` Whether the collection is empty

**Example**

```javascript
Array.isEmpty([1, 2, 3, 4, 5, 6]); //false
Array.isEmpty(0); //false
Array.isEmpty(1); //false
Array.isEmpty(0.0); //false
Array.isEmpty(1.0); //false
Array.isEmpty(null); //true
Array.isEmpty({ 'name': '李四', 'age': 30 }); //false
Array.isEmpty({}); //true
Array.isEmpty(''); //true
```

## isNotEmpty

Determines whether list is not an empty collection; returns false if list is `null` or has length 0, otherwise returns true

```javascript
Array.isNotEmpty(list);
```

| Parameter | Type | Description |
|------|-----------------|-----------|
| list | `Array` or `Map` | Collection to check length of |

**Return Value**

Type `Boolean` Whether the collection is not empty

**Example**

```javascript
Array.isNotEmpty([1, 2, 3, 4, 5, 6]); //true
Array.isNotEmpty(0); //true
Array.isNotEmpty(1); //true
Array.isNotEmpty(0.0); //true
Array.isNotEmpty(1.0); //true
Array.isNotEmpty(null); //false
Array.isNotEmpty({ 'name': '李四', 'age': 30 }); //true
Array.isNotEmpty({}); //false
Array.isNotEmpty(''); //false
```

## contains

Determines whether list contains item

```javascript
Array.contains(list, item);
```

| Parameter | Type | Description |
|------|-----------------|----|
| list | `Array` or `Map` | Collection |
| item | `Object`        | Element |

**Return Value**

Type `Boolean` Whether the Array or Map collection contains item

**Example**

```javascript
Array.contains([1, 2, 3, 4, 5, 6], 1); //true
Array.contains([2, 3, 4, 5, 6], 1); //false
Array.contains(['1', 2, 3, 4, 5, 6], 1); //false
Array.contains([{ 'name': '张三' }, { 'name': '李四' }], { 'name': '张三' }); //true
Array.contains(null, '1'); //false
```

## containsAny

Determines whether list1 contains any element from list2

When list1 is null, always returns `false`. When list2 is empty, always returns `true`

```javascript
Array.containsAny(list1, list2);
```

| Parameter | Type | Description |
|-------|---------|------|
| list1 | `Array` | Collection 1 |
| list2 | `Array` | Collection 2 |

**Return Value**

Type `Boolean` Whether list1 contains any element from list2

**Example**

```javascript
Array.containsAny([1, 2, 3, 4, 5, 6], [1]); //true
Array.containsAny([1, 2, 3, 4, 5, 6], [8]); //false
Array.containsAny([1, 2, 3, 4, 5, 6], ['1']); //false
Array.containsAny([1, 2, 3, 4, 5, 6], null); //true
Array.containsAny(null, ['1']); //false
Array.containsAny(null, null); //false
```

## containsAll

Determines whether list1 contains all elements from list2

When list1 or list2 is empty, always returns `false`

```javascript
Array.containsAll(list1, list2);
```

| Parameter | Type | Description |
|-------|---------|------|
| list1 | `Array` | Collection 1 |
| list2 | `Array` | Collection 2 |

**Return Value**

Type `Boolean` Whether list1 contains all elements from list2

**Example**

```javascript
Array.containsAll([1, 2, 3], [2, 3]); //true
Array.containsAll([1, 2, 3], [2, 3, 4]); //false
Array.containsAll([1, 2, 3], ['1', 2]); //false
Array.containsAll([1, 2, 3], [1, 2, 3, 4]); //false
Array.containsAll(null, ['1']); //false
Array.containsAll(null, null); //false
```

## map

Returns a list of the key property values from list

```javascript
Array.map(list, key);
```

| Parameter | Type | Description |
|------|----------|---------|
| list | `Array`  | Collection 1 |
| key  | `String` | Property key |

**Return Value**

Type `Array` List of key property values from each element in list

**Example**

```javascript
Array.map([{ 'name': '张三' }, { 'name': '李四' }, { 'name': '王五' }], 'name'); //["张三","李四","王五"]
Array.map([{ 'name': '张三' }, { 'name': '李四' }, { 'name': '王五' }], 'age'); //[null,null,null]
Array.map([{ 'name': '张三' }, { 'name': '李四' }, { 'name': '王五' }], null); //[]
Array.map([null, null, { 'name': '张三' }], 'name'); //[null,null,"张三"]
Array.map(null, 'name'); //[]
```

## props

Returns a new list of objects composed of the props list from elements in list

```javascript
Array.props(list, props);
```

| Parameter | Type | Description |
|-------|-----------------|------------------------------|
| list  | `Array`         | Collection 1 |
| props | `Array<String>` | Property key list, throws exception if props is null |

**Return Value**

Type `Array` New list built from the props list properties of each element in list

**Example**

```javascript
Array.props([{ 'name': '张三', 'age': 1 }, { 'name': '李四', 'age': 2 }, { 'name': '王五', 'age': 3 }], 'name'); //[{'name':'张三'},{'name':'李四'},{'name':'王五'}]
Array.props([{ 'name': '张三' }, { 'name': '李四' }, { 'name': '王五' }], 'age'); //[{'age':null},{'age':null},{'age':null}]
Array.props([{ 'name': '张三' }, { 'name': '李四' }, { 'name': '王五' }], null); //exception
Array.props([null, null, { 'name': '张三' }], 'name'); //[{'name':'张三'}]
Array.props(null, 'name'); //[]
```

## transform

Returns a new list of objects composed by mapping elements in list according to the mapping

```javascript
Array.transform(list, mapping);
```

| Parameter | Type | Description |
|---------|----------------------|---------|
| list    | `Array`              | Collection 1 |
| mapping | `Map<String,String>` | Property mapping object |

**Return Value**

Returns a new list of objects composed by mapping elements in list

**Example**

```javascript
Array.transform([{ 'name': '张三', 'age': 1 }, { 'name': '李四', 'age': 2 }, { 'name': '王五', 'age': 3 }], { 'name': 'userName', 'age': 'userAge' }); //[{'userName':'张三','userAge':1},{'userName':'李四','userAge':2},{'userName':'王五','userAge':3}]
Array.transform([{ 'name': '张三', 'age': 1 }, { 'name': '李四', 'age': 2 }, { 'name': '王五', 'age': 3 }], { 'name': 'userName', 'sex': 'userSex' }); //[{'userName':'张三','userSex':null},{'userName':'李四','userSex':null},{'userName':'王五','userSex':null}]
Array.transform([{ 'name': '张三', 'age': 1 }, { 'name': '李四', 'age': 2 }, null], { 'name': 'userName', 'age': 'userAge' }); //[{'userName':'张三','userAge':1},{'userName':'李四','userAge':2}]
Array.transform([{ 'name': '张三', 'age': 1 }, { 'name': '李四', 'age': 2 }], null); //[]
```

## concat

Returns list1 and list2 concatenated together

```javascript
Array.concat(list1, list2);
```

| Parameter | Type | Description |
|-------|---------|------|
| list1 | `Array` | Collection 1 |
| list2 | `Array` | Collection 2 |

**Return Value**

Type `Array` The concatenated collection of list1 and list2

**Example**

```javascript
Array.concat([1, 2, 3], [2, 3]); //[1,2,3,2,3]
Array.concat([1, 2, 3], [2, 3, 4]); //[1,2,3,2,3,4]
Array.concat([1, 2, 3], ['1', 2]); //[1,2,3,"1",2]
Array.concat([1, 2, 3], [1, 2, 3, 4]); //[1,2,3,1,2,3,4]
Array.concat([1, 2, 3], null); //[1,2,3]
Array.concat(null, ['1']); //["1"]
Array.concat(null, null); //[]
```

## sort

Sorts list by the key property

```javascript
Array.sort(list, key);
```

| Parameter | Type | Description |
|------|----------|-------|
| list | `Array`  | Collection |
| key  | `String` | Sort property |

**Return Value**

Type `Array` The sorted collection

**Example**

```javascript
Array.sort([
    { 'name': 'a', 'age': 20 },
    { 'name': 'b', 'age': 18 },
    { 'name': 'c', 'age': 32 },
    { 'name': 'c', 'age': 24 }
], 'age'); //[{"name":"a","age":20},{"name":"b","age":18},{"name":"c","age":32},{"name":"c","age":24}]
Array.sort([{ 'male': true, 'age': 20 }, { 'male': false, 'age': 18 }, { 'male': true, 'age': 32 }], 'male'); //[{"male":true,"age":20},{"male":false,"age":18},{"male":true,"age":32}]
Array.sort([{ 'male': true, 'age': 20 }, { 'male': false, 'age': 18 }], null); //[{"male":true,"age":20},{"male":false,"age":18}]
Array.sort(null, 'age'); //null
Array.sort([5, 4, 9, 20, 32, 1, 244]); //[1,4,5,9,20,32,244]
Array.sort(null, null); //null
```

## distinct

Removes duplicate items from list and returns the result

```javascript
Array.distinct(list);
```

| Parameter | Type | Description |
|------|---------|----|
| list | `Array` | Collection |

**Return Value**

Type `Array` The deduplicated collection

**Example**

```javascript
Array.distinct([{ 'name': 'a', 'age': 20 }, { 'name': 'a', 'age': 20 }, { 'name': 'c', 'age': 32 }]); //[{"name":"a","age":20},{"name":"c","age":32}]
Array.distinct([1, 2, 2, 3, 4, 5, 67, 9]); //[1,2,3,4,5,67,9]
Array.distinct([1, 2, null, 3, 4, 5, null, 9]); //[1,2,null,3,4,5,9]
Array.distinct(null); //null
```

## reverse

Reverses list and returns the result

```javascript
Array.reverse(list);
```

| Parameter | Type | Description |
|------|---------|----|
| list | `Array` | Collection |

**Return Value**

Type `Array` The reversed collection

**Example**

```javascript
Array.reverse([{ 'name': 'a', 'age': 20 }, { 'name': 'c', 'age': 32 }]); //[{"name":"c","age":32},{"name":"a","age":20}]
Array.reverse([1, 2, 3, 4, 5, 6, 7, 9]); //[9,7,6,5,4,3,2,1]
Array.reverse([1, 2, null, 3, 4, 5, null, 9]); //[9,null,5,4,3,null,2,1]
Array.reverse(null); //null
```

## repeat

Generates an array where each item is element and the length is count

```javascript
Array.repeat(count, element);
```

| Parameter | Type | Description |
|---------|-----------|-------|
| count   | `Integer` | Number of repetitions |
| element | `Object`  | Element to repeat |

**Return Value**

Type `Array` The generated array

**Example**

```javascript
Array.repeat(4, { 'name': 'a' }); //[{"name":"a"},{"name":"a"},{"name":"a"},{"name":"a"}]
Array.repeat(4, 1); //[1,1,1,1]
Array.repeat(3, 'a'); //["a","a","a"]
Array.repeat(3, null); //[null,null,null]
```

## sublist

Returns the portion of list from fromIndex to toIndex

```javascript
Array.sublist(list, fromIndex, toIndex);
```

| Parameter | Type | Description |
|-----------|-----------|----------------------------------|
| list      | `Array`   | Collection |
| fromIndex | `Integer` | Start index, defaults to 0 if null |
| endIndex  | `Integer` | End index, defaults to the last element position if null |

**Return Value**

Type `Array` The generated array, returns null if list is empty

**Example**

```javascript
Array.sublist([1, 2, 3, 4], 0, 1); //[1,2]
Array.sublist([1, 2, 3, 4], 0, 100); //[1,2,3,4]
Array.sublist([1, 2, 3, 4], 1, 1); //[2]
Array.sublist([1, 2, 3, 4], null, null); //[]
Array.sublist([1, 2, 3, 4], null, 2); //[1,2,3]
Array.sublist([1, 2, 3, 4], 1, null); //[2,3,4]
Array.sublist(null, 0, 1); //null
```

## filter

Filters items from list where the property key equals value

```javascript
Array.filter(list, key, value);
```

| Parameter | Type | Description |
|-------|----------|-----------|
| list  | `Array`  | Collection |
| key   | `String` | Property key to compare |
| value | `Object` | Property value to compare |

**Return Value**

Type `Array` Array of items satisfying the condition

**Example**

```javascript
Array.filter([{ a: 1 }, { a: 2 }, { a: 2 }], "a", 2); //[{"a":2},{"a":2}]
Array.filter(null, "a", 2); //[]
Array.filter([{ a: 1 }, { a: 2 }, { a: 2 }], null, 2); //[]
```

## shift

Removes the first element from list and returns the removed element

```javascript
Array.shift(list);
```

| Parameter | Type | Description |
|------|---------|----|
| list | `Array` | Collection |

**Return Value**

Type `Object` The first element

**Example**

```javascript
Array.shift([1, 2, 3]); //1
Array.shift([]); //null
Array.shift(null); //null
```

## pop

Removes the last element from list and returns the removed element

```javascript
Array.pop(list);
```

| Parameter | Type | Description |
|------|---------|----|
| list | `Array` | Collection |

**Return Value**

Type `Object` The last element

**Example**

```javascript
Array.pop([1, 2, 3]); //3
Array.pop([]); //null
Array.pop(null); //null
```

## sum

Calculates the sum of a list with numeric elements

```javascript
Array.sum(list);
```

| Parameter | Type | Description |
|------|---------|----|
| list | `Array` | Collection |

**Return Value**

Type `Double` The sum result

**Example**

```javascript
Array.sum([1, 2, 3]); //6.0
Array.sum([]); //0.0
Array.sum([null, null, null]); //0.0
Array.sum([1, null, 2]); //3.0
Array.sum(null); //0.0
Array.sum(["1", "2", "3"]); //6.0 If array element type is string, the system will convert to decimal; returns 0 if conversion fails
Array.sum(["1", "2", "s"]); //3.0 If array element type is string, treats as 0 if conversion fails
```

## avg

Calculates the average of a list with numeric elements

```javascript
Array.avg(list);
```

| Parameter | Type | Description |
|------|---------|----|
| list | `Array` | Collection |

**Return Value**

Type `Double` The average result

**Example**

```javascript
Array.avg([1, 2, 3]); //2.0
Array.avg([]); //0.0
Array.avg([null, null, null]); //0.0
Array.avg([1, null, 2]); //1.0
Array.avg(null); //0.0
Array.avg(["1", "2", "3"]); //2.0 If array element type is string, the system will convert to decimal; returns 0 if conversion fails
Array.avg(["1", "2", "s"]); //1.0 If array element type is string, treats as 0 if conversion fails
```

## max

Calculates the maximum value of a list with numeric elements

```javascript
Array.max(list);
```

| Parameter | Type | Description |
|------|---------|----|
| list | `Array` | Collection |

**Return Value**

Type `Double` The maximum value in list

**Example**

```javascript
Array.max([1, 2, 3]); //3.0
Array.max([]); //null
Array.max([null, null, null]); //null
Array.max([1, null, 2]); //2.0
Array.max(null); //null
Array.max(["1", "2", "3"]); //3.0 If array element type is string, the system will convert to decimal; if conversion fails
Array.max(["1", "2", "s"]); //2.0 If array element type is string, treats as 0 if conversion fails
```

## min

Calculates the minimum value of a list with numeric elements

```javascript
Array.min(list);
```

| Parameter | Type | Description |
|------|---------|----|
| list | `Array` | Collection |

**Return Value**

Type `Double` The minimum value in list

**Example**

```javascript
Array.min([1, 2, 3]); //1.0
Array.min([]); //null
Array.min([null, null, null]); //null
Array.min([1, null, 2]); //1.0
Array.min(null); //null
Array.min(["1", "2", "3"]); //1.0 If array element type is string, the system will convert to decimal; returns 0 if conversion fails
Array.min(["1", "2", "s"]); //1.0 If array element type is string, ignores if conversion fails
```

## first

Returns the first element in list

```javascript
Array.first(list);
```

| Parameter | Type | Description |
|------|---------|----|
| list | `Array` | Collection |

**Return Value**

Type `Object` The first element in list

**Example**

```javascript
Array.first([1, 2, 3]); //1
Array.first([]); //null
Array.first(null); //null
```

## last

Returns the last element in list

```javascript
Array.last(list);
```

| Parameter | Type | Description |
|------|---------|----|
| list | `Array` | Collection |

**Return Value**

Type `Object` The last element in list

**Example**

```javascript
Array.last([1, 2, 3]); //3
Array.last([]); //null
Array.last(null); //null
```

## stream

Creates an array stream for chaining array operations

```javascript
Array.stream(array)
```

| Parameter | Type | Description |
|-------|----------|---------|
| array | `Array`  | Array or collection |

**Return Value**

Type `ArrayStream`
Returns an array stream object that can chain array operation methods.

**Example**

```javascript
Array.stream([1, 2, 3, 4, 5])
  .filter('value', '>', 2)
  .sort()
  .get()
```

### ArrayStream Methods

ArrayStream objects provide the following chainable methods:

#### get

Returns the current array

```javascript
stream.get()
```

**Return Value**

Type `Array` Current array

#### length

Returns the array length

```javascript
stream.length()
```

**Return Value**

Type `Number` Array length

#### add

Adds an element to the array

```javascript
stream.add(item)
```

| Parameter | Type | Description |
|------|----------|------|
| item | `Object` | Element to add |

**Return Value** `ArrayStream` itself, for chaining.

#### remove

Removes an element from the array

```javascript
stream.remove(item)
```

| Parameter | Type | Description |
|------|----------|------|
| item | `Object` | Element to remove |

**Return Value** `ArrayStream` itself, for chaining.

#### removeAll

Removes multiple elements from the array

```javascript
stream.removeAll(items)
```

| Parameter | Type | Description |
|-------|----------|----------|
| items | `Array`  | Array of elements to remove |

**Return Value** `ArrayStream` itself, for chaining.

#### sort

Sorts the array by specified property

```javascript
stream.sort(key)
```

| Parameter | Type | Description |
|------|----------|-------|
| key  | `String` | Sort property |

**Return Value** `ArrayStream` itself, for chaining.

#### map

Extracts the specified property from each element in the array

```javascript
stream.map(key)
```

| Parameter | Type | Description |
|------|----------|---------|
| key  | `String` | Property to extract |

**Return Value** `ArrayStream` itself, for chaining.

#### props

Extracts multiple properties from each element in the array

```javascript
stream.props(props)
stream.props(propArray)
```

| Parameter | Type | Description |
|-----------|-----------------|----------|
| props     | `Array<String>` | Property list |
| propArray | `String...`     | Property varargs |

**Return Value** `ArrayStream` itself, for chaining.

#### transform

Transforms property names of each element in the array

```javascript
stream.transform(mapping)
```

| Parameter | Type | Description |
|---------|----------------------|---------|
| mapping | `Map<String,String>` | Property mapping |

**Return Value** `ArrayStream` itself, for chaining.

#### repeat

Repeats array elements

```javascript
stream.repeat(count, item)
```

| Parameter | Type | Description |
|-------|-----------|-------|
| count | `Integer` | Number of repetitions |
| item  | `Object`  | Element to repeat |

**Return Value** `ArrayStream` itself, for chaining.

#### reverse

Reverses the array

```javascript
stream.reverse()
```

**Return Value** `ArrayStream` itself, for chaining.

#### distinct

Deduplicates the array

```javascript
stream.distinct()
```

**Return Value** `ArrayStream` itself, for chaining.

#### sublist

Gets a sub-array

```javascript
stream.sublist(from, end)
```

| Parameter | Type | Description |
|-------|-----------|--------|
| from  | `Integer` | Start index |
| end   | `Integer` | End index |

**Return Value** `ArrayStream` itself, for chaining.

#### shift

Removes the first element of the array

```javascript
stream.shift()
```

**Return Value** `ArrayStream` itself, for chaining.

#### pop

Removes the last element of the array

```javascript
stream.pop()
```

**Return Value** `ArrayStream` itself, for chaining.

#### concat

Concatenates another array

```javascript
stream.concat(list)
```

| Parameter | Type | Description |
|------|---------|--------|
| list | `Array` | Array to concatenate |

**Return Value** `ArrayStream` itself, for chaining.

#### filter

Filters array elements

```javascript
stream.filter(key, value)
```

| Parameter | Type | Description |
|-------|----------|-----------|
| key   | `String` | Property key to compare |
| value | `Object` | Property value to compare |

**Return Value** `ArrayStream` itself, for chaining.

#### set

Sets array element values

```javascript
stream.set(key, value)
```

| Parameter | Type | Description |
|-------|----------|-----------|
| key   | `Object` | Index or property name |
| value | `Object` | Value to set |

**Return Value** `ArrayStream` itself, for chaining.

#### sum

Calculates the sum of array elements

```javascript
stream.sum()
```

**Return Value**

Type `Number` Sum of array elements

#### avg

Calculates the average of array elements

```javascript
stream.avg()
```

**Return Value**

Type `Number` Average of array elements

#### max

Gets the maximum value of array elements

```javascript
stream.max()
```

**Return Value**

Type `Number` Maximum value of array elements

#### min

Gets the minimum value of array elements

```javascript
stream.min()
```

**Return Value**

Type `Number` Minimum value of array elements

#### first

Gets the first element of the array

```javascript
stream.first()
```

**Return Value**

Type `Object` First element of the array

#### last

Gets the last element of the array

```javascript
stream.last()
```

**Return Value**

Type `Object` Last element of the array
