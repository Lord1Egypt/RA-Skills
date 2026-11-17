# informat.redis Redis

## Overview

Use the `informat.redis` object to perform Redis-related operations

## opsForValue

Get the value operations object

```javascript
const ops = informat.redis.opsForValue();
```

**Return Value**

Returns a value operations object.

**Example**
```javascript
const ops = informat.redis.opsForValue();
```

::: tip Note:
- This method requires no parameters and returns an object that can perform value operations.
:::

## opsForList

Get the list operations object

```javascript
const ops = informat.redis.opsForList();
```

**Return Value**

Returns a list operations object.

**Example**
```javascript
const ops = informat.redis.opsForList();
```

## opsForGeo

Get the geo operations object

```javascript
const ops = informat.redis.opsForGeo();
```

**Return Value**

Returns a geo operations object.

**Example**
```javascript
const ops = informat.redis.opsForGeo();
```

## redisTemplate

Get the Redis operation template

```javascript
const redisTemplate = informat.redis.redisTemplate();
```

**Return Value**

Returns a Redis operation template object.

**Example**
```javascript
const redisTemplate = informat.redis.redisTemplate();
```


## delete

Delete the value of a specified key

```javascript
informat.redis.delete(key)
```

| Parameter | Type     | Description        |
|-----------|----------|--------------------|
| key       | `String` | The key to delete  |

**Return Value**

Returns the result of the delete operation: true on success, false on failure.

**Example**
```javascript
informat.redis.delete('key1');
```

::: tip Note:
- The key parameter must be of string type. This method is suitable for deleting a single key.
:::


## deleteAll

Delete all values of a specified key group

```javascript
informat.redis.deleteAll(keys)
```

| Parameter | Type             | Description             |
|-----------|------------------|-------------------------|
| keys      | `Array<String>`  | The key group to delete |

**Return Value**

Returns the number of deleted keys, type `Number`

**Example**
```javascript
informat.redis.deleteAll(['key1', 'key2', 'key3']);
```

::: tip Note:
- The keys parameter must be an array type, and the array elements must be of string type. This method is suitable for batch deleting keys.
:::


## set

Set the value of a specified key

```javascript
ops.set(key, value, timeout, redisTimeoutUnit)
```

| Parameter        | Type               | Description                |
|------------------|--------------------|----------------------------|
| key              | `String`           | The key to set             |
| value            | `String`           | The value to set           |
| timeout          | `Integer`          | Optional, expiration time  |
| redisTimeoutUnit | `RedisTimeoutUnit` | Optional, time unit        |

:::info RedisTimeoutUnit options
- NANOSECONDS nanoseconds
- MICROSECONDS microseconds
- MILLISECONDS milliseconds
- SECONDS seconds
- MINUTES minutes
- HOURS hours
- DAYS days
:::

**Return Value**

No return value.

**Example**
```javascript
const ops = informat.redis.opsForValue();
ops.set('key1', 'value1', 5, 'MINUTES');
```

::: tip Note:
- Both key and value parameters must be of string type. This method is suitable for setting a single key-value pair, and can be used for caching or persisting data.
:::



## setIfAbsent

Set the value of a specified key only when the key does not exist

```javascript
ops.setIfAbsent(key, value, timeout, redisTimeoutUnit)
```

| Parameter        | Type               | Description                |
|------------------|--------------------|----------------------------|
| key              | `String`           | The key to set             |
| value            | `String`           | The value to set           |
| timeout          | `Integer`          | Optional, expiration time  |
| redisTimeoutUnit | `RedisTimeoutUnit` | Optional, time unit        |

**Return Value**

Returns a boolean indicating whether the value was successfully set.

**Example**
```javascript
const ops = informat.redis.opsForValue();
const success = ops.setIfAbsent('key1', 'value1', 5, 'MINUTES');
```

::: tip Note:
- Both key and value parameters must be of string type. This method is suitable for setting a value only when the key does not exist, and can be used to implement distributed locks.
:::



## setIfPresent

Set the value of a specified key only when the key exists

```javascript
ops.setIfPresent(key, value, timeout, redisTimeoutUnit)
```

| Parameter        | Type               | Description                |
|------------------|--------------------|----------------------------|
| key              | `String`           | The key to set             |
| value            | `String`           | The value to set           |
| timeout          | `Integer`          | Optional, expiration time  |
| redisTimeoutUnit | `RedisTimeoutUnit` | Optional, time unit        |

**Return Value**

Returns a boolean indicating whether the value was successfully set.

**Example**
```javascript
const ops = informat.redis.opsForValue();
const success = ops.setIfPresent('key1', 'value1', '5', 'MINUTES');
```

::: tip Note:
- Both key and value parameters must be of string type. This method is suitable for setting a value only when the key exists, and can be used to update existing key-value pairs.
:::



## multiSet

Batch set values for specified keys

```javascript
ops.multiSet(keyValuePairs)
```

| Parameter     | Type     | Description                   |
|---------------|----------|-------------------------------|
| keyValuePairs | `Object` | Key-value pairs object to set |

**Return Value**

No return value.

**Example**
```javascript
const ops = informat.redis.opsForValue();
ops.multiSet({ 'key1': 'value1', 'key2': 'value2', 'key3': 'value3' });
```

::: tip Note:
- The keyValuePairs parameter must be an object type, and both keys and values of the object must be of string type. This method is suitable for batch setting data, which can reduce the number of communications with Redis and improve system performance.
:::

## multiSetIfAbsent

Batch set values for specified keys only when all keys do not exist

```javascript
ops.multiSetIfAbsent(keyValuePairs)
```

| Parameter     | Type     | Description                   |
|---------------|----------|-------------------------------|
| keyValuePairs | `Object` | Key-value pairs object to set |

**Return Value**

Returns a boolean indicating whether the values were successfully set.

**Example**
```javascript
const ops = informat.redis.opsForValue();
const success = ops.multiSetIfAbsent({ 'key1': 'value1', 'key2': 'value2', 'key3': 'value3' });
```

::: tip Note:
- The keyValuePairs parameter must be an object type, and both keys and values of the object must be of string type. This method is suitable for batch setting values only when all keys do not exist, and can be used to implement distributed locks.
:::



## setRange

Set a substring of the value of a specified key

```javascript
ops.setRange(key, value, offset)
```

| Parameter | Type      | Description                      |
|-----------|-----------|----------------------------------|
| key       | `String`  | The key to set                   |
| value     | `String`  | The substring value to set       |
| offset    | `Integer` | The starting position of the substring |

**Return Value**

No return value.

**Example**
```javascript
const ops = informat.redis.opsForValue();
ops.setRange('key1', 'value1', 2);
```

::: tip Note:
- The key and value parameters must be of string type, and offset must be of number type. This method is suitable for updating partial content of a string.
:::


Below are the development documentation examples for each method written according to the template format provided:



## get

Get the value of a specified key

```javascript
ops.get(key)
```

| Parameter | Type     | Description       |
|-----------|----------|-------------------|
| key       | `String` | The key to get    |

**Return Value**

Returns the value corresponding to the key, or null if the key does not exist.

**Example**
```javascript
const ops = informat.redis.opsForValue();
const value = ops.get('key1');
```

::: tip Note:
- The key parameter must be of string type. This method is suitable for getting a single key-value pair, and can be used to read cached or persisted data.
:::



## getAndExpire

Get the value of a specified key and set an expiration time

```javascript
ops.getAndExpire(key, timeout, redisTimeoutUnit)
```

| Parameter        | Type               | Description        |
|------------------|--------------------|--------------------|
| key              | `String`           | The key to get     |
| timeout          | `Integer`          | Expiration time    |
| redisTimeoutUnit | `RedisTimeoutUnit` | Time unit          |

**Return Value**

Returns the value corresponding to the key, or null if the key does not exist.

**Example**
```javascript
const ops = informat.redis.opsForValue();
const value = ops.getAndExpire('key1', 60, 'SECONDS'); // Get the value of key1 and set it to expire in 60 seconds
```

::: tip Note:
- The key parameter must be of string type, and timeout must be of number type. This method is suitable for scenarios where you need to get a value and set an expiration time at the same time.
:::



## getAndPersist

Get the value of a specified key and remove the expiration time

```javascript
ops.getAndPersist(key)
```

| Parameter | Type     | Description       |
|-----------|----------|-------------------|
| key       | `String` | The key to get    |

**Return Value**

Returns the value corresponding to the key, or null if the key does not exist.

**Example**
```javascript
const ops = informat.redis.opsForValue();
const value = ops.getAndPersist('key1'); // Get the value of key1 and remove its expiration time
```

::: tip Note:
- The key parameter must be of string type. This method is suitable for scenarios where you need to get a value and remove the expiration time at the same time.
:::



## getAndSet

Get the value of a specified key and set a new value

```javascript
ops.getAndSet(key, newValue)
```

| Parameter | Type     | Description       |
|-----------|----------|-------------------|
| key       | `String` | The key to get    |
| newValue  | `String` | The new value     |

**Return Value**

Returns the previous value corresponding to the key, or null if the key does not exist.

**Example**
```javascript
const ops = informat.redis.opsForValue();
const oldValue = ops.getAndSet('key1', 'newValue'); // Get the old value of key1 and set the new value to newValue
```

::: tip Note:
- Both key and newValue parameters must be of string type. This method is suitable for scenarios where you need to get the old value and set a new value.
:::



## multiGet

Batch get values of specified keys

```javascript
ops.multiGet(keys)
```

| Parameter | Type            | Description         |
|-----------|-----------------|---------------------|
| keys      | `Array<String>` | The key group to get |

**Return Value**

Returns an array of values corresponding to the keys, or null if a key does not exist.

**Example**
```javascript
const ops = informat.redis.opsForValue();
const values = ops.multiGet(['key1', 'key2', 'key3']);
```

::: tip Note:
- The keys parameter must be an array type, and the array elements must be of string type. This method is suitable for batch getting data, which can reduce the number of communications with Redis and improve system performance.
:::



## increment

Increment the value of a specified key by 1

```javascript
ops.increment(key)
```

| Parameter | Type     | Description            |
|-----------|----------|------------------------|
| key       | `String` | The key to increment   |

**Return Value**

Returns the incremented value.

**Example**
```javascript
const ops = informat.redis.opsForValue();
const newValue = ops.increment('key1'); // Increment the value of key1 by 1
```

::: tip Note:
- The key parameter must be of string type. This method is suitable for auto-increment operations on numeric key-value pairs.
:::



## decrement

Decrement the value of a specified key by 1

```javascript
ops.decrement(key)
```

| Parameter | Type     | Description            |
|-----------|----------|------------------------|
| key       | `String` | The key to decrement   |

**Return Value**

Returns the decremented value.

**Example**
```javascript
const ops = informat.redis.opsForValue();
const newValue = ops.decrement('key1'); // Decrement the value of key1 by 1
```

::: tip Note:
- The key parameter must be of string type. This method is suitable for auto-decrement operations on numeric key-value pairs.
:::



## append

Append a string to the value of a specified key

```javascript
ops.append(key, value)
```

| Parameter | Type     | Description              |
|-----------|----------|--------------------------|
| key       | `String` | The key to append to     |
| value     | `String` | The string to append     |

**Return Value**

Returns the length of the value after appending.

**Example**
```javascript
const ops = informat.redis.opsForValue();
const newLength = ops.append('key1', 'appendValue'); // Append the string appendValue to the value of key1
```

::: tip Note:
- Both key and value parameters must be of string type. This method is suitable for append operations on string type key-value pairs.
:::
  

## size

Get the size (in bytes) of the value of a specified key

```javascript
ops.size(key)
```

| Parameter | Type     | Description              |
|-----------|----------|--------------------------|
| key       | `String` | The key to get size of   |

**Return Value**

Returns the size (in bytes) of the value corresponding to the key, or 0 if the key does not exist.

**Example**
```javascript
const ops = informat.redis.opsForValue();
const size = ops.size('myKey');
```

::: tip Note:
- The key parameter must be of string type. This method is suitable for scenarios where you need to get the size of a stored value.
:::



## setBit

Set the value of a specific bit of a specified key

```javascript
ops.setBit(key, offset, value)
```

| Parameter | Type      | Description                              |
|-----------|-----------|------------------------------------------|
| key       | `String`  | The key to set the bit value for         |
| offset    | `Integer` | The bit offset to set (starting from 0)  |
| value     | `Integer` | The bit value to set (0 or 1)            |

**Return Value**

Returns the previous value of the bit before setting.

**Example**
```javascript
const ops = informat.redis.opsForValue();
const previousValue = ops.setBit('myKey', 5, 1);
```

::: tip Note:
- The key parameter must be of string type, offset must be of number type, and value must be 0 or 1. This method is suitable for bit operation scenarios.
:::



## getBit

Get the value of a specific bit of a specified key

```javascript
ops.getBit(key, offset)
```

| Parameter | Type      | Description                              |
|-----------|-----------|------------------------------------------|
| key       | `String`  | The key to get the bit value from        |
| offset    | `Integer` | The bit offset to get (starting from 0)  |

**Return Value**

Returns the value of the specific bit of the specified key (0 or 1).

**Example**
```javascript
const ops = informat.redis.opsForValue();
const bitValue = ops.getBit('myKey', 5);
```

::: tip Note:
- The key parameter must be of string type, and offset must be of number type. This method is suitable for bit operation scenarios.
:::
  

## opsForList

Provides a collection of methods for Redis list operations.

## range

Get elements within a specified range in a list.

```javascript
opsForList.range(key, start, end)
```

| Parameter | Type      | Description     |
|-----------|-----------|-----------------|
| key       | `String`  | The list key    |
| start     | `Integer` | Start position  |
| end       | `Integer` | End position    |

**Return Value**

Returns the list of elements within the specified range.

**Example**
```javascript
const ops = informat.redis.opsForList();
const elements = ops.range('myList', 0, -1);
```

::: tip Note:
- The `key` parameter must be of string type, and `start` and `end` must be of number type. `start` and `end` can be negative, indicating counting from the end of the list.
:::



## trim

Trim a list, keeping only elements within the specified range.

```javascript
opsForList.trim(key, start, end)
```

| Parameter | Type      | Description     |
|-----------|-----------|-----------------|
| key       | `String`  | The list key    |
| start     | `Integer` | Start position  |
| end       | `Integer` | End position    |

**Return Value**

No return value.

**Example**
```javascript
const ops = informat.redis.opsForList();
ops.trim('myList', 1, 3);
```

::: tip Note:
- The `key` parameter must be of string type, and `start` and `end` must be of number type. `start` and `end` can be negative, indicating counting from the end of the list.
:::



## size

Get the length of a list.

```javascript
opsForList.size(key)
```

| Parameter | Type     | Description     |
|-----------|----------|-----------------|
| key       | `String` | The list key    |

**Return Value**

Returns the length of the list.

**Example**
```javascript
const ops = informat.redis.opsForList();
const length = ops.size('myList');
```

::: tip Note:
- The `key` parameter must be of string type.
:::



## leftPush

Insert an element at the head of a list.

```javascript
opsForList.leftPush(key, value)
```

| Parameter | Type     | Description           |
|-----------|----------|-----------------------|
| key       | `String` | The list key          |
| value     | `Object` | The element to insert |

**Return Value**

Returns the length of the list after insertion.

**Example**
```javascript
const ops = informat.redis.opsForList();
const length = ops.leftPush('myList', 'element');
```

::: tip Note:
- The `key` parameter must be of string type, and `value` can be of any type.
:::



## leftPushAll

Insert multiple elements at the head of a list.

```javascript
opsForList.leftPushAll(key, values)
```

| Parameter | Type            | Description                 |
|-----------|-----------------|-----------------------------|
| key       | `String`        | The list key                |
| values    | `Array<Object>` | Array of elements to insert |

**Return Value**

Returns the length of the list after insertion.

**Example**
```javascript
const ops = informat.redis.opsForList();
const length = ops.leftPushAll('myList', ['element1', 'element2']);
```

::: tip Note:
- The `key` parameter must be of string type, and `values` must be an array type with elements of any type.
:::



## leftPushIfPresent

Insert an element at the head of a list, only when the list exists.

```javascript
opsForList.leftPushIfPresent(key, value)
```

| Parameter | Type     | Description           |
|-----------|----------|-----------------------|
| key       | `String` | The list key          |
| value     | `Object` | The element to insert |

**Return Value**

Returns the length of the list after insertion, or 0 if the list does not exist.

**Example**
```javascript
const ops = informat.redis.opsForList();
const length = ops.leftPushIfPresent('myList', 'element');
```

::: tip Note:
- The `key` parameter must be of string type, and `value` can be of any type.
:::



## rightPush

Insert an element at the tail of a list.

```javascript
opsForList.rightPush(key, value)
```

| Parameter | Type     | Description           |
|-----------|----------|-----------------------|
| key       | `String` | The list key          |
| value     | `Object` | The element to insert |

**Return Value**

Returns the length of the list after insertion.

**Example**
```javascript
const ops = informat.redis.opsForList();
const length = ops.rightPush('myList', 'element');
```

::: tip Note:
- The `key` parameter must be of string type, and `value` can be of any type.
:::

Below are the detailed documentation for the `opsForList` methods in Redis:



## rightPushAll

Insert all specified values at the tail of the list stored at key

```javascript
opsForList.rightPushAll(key, values)
```

| Parameter | Type            | Description                    |
|-----------|-----------------|--------------------------------|
| key       | `String`        | The key corresponding to the list |
| values    | `Array<String>` | Array of values to insert      |

**Return Value**

Returns the length of the list after the insert operation.

**Example**
```javascript
const opsForList = informat.redis.opsForList();
const length = opsForList.rightPushAll('myList', ['value1', 'value2', 'value3']);
```

::: tip Note:
- The key parameter must be of string type, and values must be an array type with string type elements.
:::



## rightPushIfPresent

Insert a value at the tail of a list only when the list exists

```javascript
opsForList.rightPushIfPresent(key, value)
```

| Parameter | Type     | Description                    |
|-----------|----------|--------------------------------|
| key       | `String` | The key corresponding to the list |
| value     | `String` | The value to insert            |

**Return Value**

Returns the length of the list after the insert operation, or 0 if the list does not exist.

**Example**
```javascript
const opsForList = informat.redis.opsForList();
const length = opsForList.rightPushIfPresent('myList', 'value1');
```

::: tip Note:
- Both key and value parameters must be of string type.
:::



## set

Set the value of the element at the specified index in the list

```javascript
opsForList.set(key, index, value)
```

| Parameter | Type      | Description                    |
|-----------|-----------|--------------------------------|
| key       | `String`  | The key corresponding to the list |
| index     | `Integer` | The list index                 |
| value     | `String`  | The value to set               |

**Return Value**

No return value.

**Example**
```javascript
const opsForList = informat.redis.opsForList();
opsForList.set('myList', 1, 'newValue');
```

::: tip Note:
- The key parameter must be of string type, index must be of number type, and value must be of string type.
:::



## index

Get the value of the element at the specified index in the list

```javascript
opsForList.index(key, index)
```

| Parameter | Type      | Description                    |
|-----------|-----------|--------------------------------|
| key       | `String`  | The key corresponding to the list |
| index     | `Integer` | The list index                 |

**Return Value**

Returns the value of the element at the specified index in the list, or null if the index is out of range.

**Example**
```javascript
const opsForList = informat.redis.opsForList();
const value = opsForList.index('myList', 1);
```

::: tip Note:
- The key parameter must be of string type, and index must be of number type.
:::



## indexOf

Get the index of a specified value in the list

```javascript
opsForList.indexOf(key, value)
```

| Parameter | Type     | Description                    |
|-----------|----------|--------------------------------|
| key       | `String` | The key corresponding to the list |
| value     | `String` | The value to find              |

**Return Value**

Returns the index of the specified value in the list, or -1 if the value does not exist.

**Example**
```javascript
const opsForList = informat.redis.opsForList();
const index = opsForList.indexOf('myList', 'value1');
```

::: tip Note:
- Both key and value parameters must be of string type.
:::



## leftPop

Remove and return the head element of the list

```javascript
opsForList.leftPop(key)
```

| Parameter | Type     | Description                    |
|-----------|----------|--------------------------------|
| key       | `String` | The key corresponding to the list |

**Return Value**

Returns the head element of the list, or null if the list is empty.

**Example**
```javascript
const opsForList = informat.redis.opsForList();
const value = opsForList.leftPop('myList');
```

::: tip Note:
- The key parameter must be of string type.
:::



## rightPop

Remove and return the tail element of the list

```javascript
opsForList.rightPop(key)
```

| Parameter | Type     | Description                    |
|-----------|----------|--------------------------------|
| key       | `String` | The key corresponding to the list |

**Return Value**

Returns the tail element of the list, or null if the list is empty.

**Example**
```javascript
const opsForList = informat.redis.opsForList();
const value = opsForList.rightPop('myList');
```

::: tip Note:
- The key parameter must be of string type.
:::



## rightPopAndLeftPush

Pop a value from the tail of the source list and push it to the head of the destination list

```javascript
opsForList.rightPopAndLeftPush(sourceKey, destinationKey)
```

| Parameter      | Type     | Description                          |
|----------------|----------|--------------------------------------|
| sourceKey      | `String` | The key corresponding to the source list      |
| destinationKey | `String` | The key corresponding to the destination list |

**Return Value**

Returns the value popped from the source list, or null if the source list is empty.

**Example**
```javascript
const opsForList = informat.redis.opsForList();
const value = opsForList.rightPopAndLeftPush('sourceList', 'destinationList');
```

::: tip Note:
- Both sourceKey and destinationKey parameters must be of string type.
:::
  



