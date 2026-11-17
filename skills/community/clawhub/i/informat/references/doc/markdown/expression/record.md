# Record

## Overview

Data table related functions

## getById

Returns the queried data table record information

```javascript
Record.getById(tableId, recordId)
```

| Parameter | Type | Description |
|----------|--------|---------|
| tableId  | `String` | Data table identifier |
| recordId | `String` | Record ID |

**Return Value**

Type `Object`
Data table record information, returns `null` if it does not exist

**Example**

```javascript
Record.getById('order', 'z2koxrkxtp854')//{amount=11, name=测试采购单, id=z2koxrkxtp854} 
```



## getFieldValue

Returns the field value of a data table record

```javascript
Record.getFieldValue(tableId, recordId, fieldId)
```

| Parameter | Type | Description |
|----------|--------|---------|
| tableId  | `String` | Data table identifier |
| recordId | `String` | Record ID |
| fieldId  | `String` | Field identifier |


**Return Value** 

Type `Object`
The field value of the data table record. Returns `null` if the record does not exist, returns `null` if the property does not exist.
Throws an exception if the data table does not exist

**Example**

```javascript
//{amount=11, name=测试采购单, id=z2koxrkxtp854} 
Record.getFieldValue('order','z2koxrkxtp854','amount')//11
```



## getByField

Filters data table records by a single field

```javascript
Record.getByField(tableId, fieldId, opt, value)
```

| Parameter | Type | Description |
|---------|--------|----------------------------------------------|
| tableId | `String` | Data table identifier |
| fieldId | `String` | Field to filter by |
| opt     | `String` | Operator, see `ConditionOpt` for operators |
| value   | `Object` | Filter condition value |

**Return Value**

Type `Array<Record>`
Returns a list of records matching the condition, up to 10000 records maximum. Returns an empty array if no data matches.
Throws an exception if the data table does not exist
 
**Example**

```javascript
//{amount=11, name=测试采购单, id=z2koxrkxtp854} 
Record.getByField('order', 'amount', 'eq', 11)//[{amount=11, name=测试采购单, id=z2koxrkxtp854}]
```



## getByFields

Filters data table records by multiple fields

```javascript
Record.getByFields(tableId, conditions)
```

| Parameter | Type | Description |
|------------|--------|----------------------------------------------|
| tableId    | `String` | Data table identifier |
| conditions | `Array`  | Filter conditions, see [Condition](../script/model.html#condition) for details |

**Return Value**

Type `Array<Record>`
Returns a list of records matching the conditions, up to 10000 records maximum. Returns an empty array if no data matches.
Throws an exception if the data table does not exist

**Example**

```javascript
//{amount=11, text=13, id=z2koxrkxtp854} 
Record.getByFields('tab', [{ "fieldId": 'text', "opt": "eq", "value": '13' }])//[{amount=11, text=13, id=z2koxrkxtp854}]
```



## getRecordOptionName

Returns the name of a single option value

```javascript
Record.getRecordOptionName(tableId, fieldId, value)
```

| Parameter | Type | Description |
|---------|--------|---------|
| tableId | `String` | Data table identifier |
| fieldId | `String` | Field identifier |
| value   | `String` | Option value |

**Return Value** 

Type `String`
Returns the name of the option value. If the option value does not exist in the option list, returns the passed-in option value.
Throws an exception if the data table does not exist

**Example**

```javascript
//Option value list: a:'选项1',b:'选项2'
//{amount=11, name=测试采购单, id=z2koxrkxtp854,type=a} 
Record.getRecordOptionName('order', 'type', 'a')//选项1
Record.getRecordOptionName('order', 'type', 'c')//c
```



## getRecordOptionNames

Returns the names of multiple option values joined together

```javascript
Record.getRecordOptionNames(tableId, fieldId, valueList, join)
```

| Parameter | Type | Description |
|-----------|-----------------|---------|
| tableId   | `String`          | Data table identifier |
| fieldId   | `String`          | Field identifier |
| valueList | `Array<String>` | Option value list |
| join      | `String`          | Join string |

**Return Value** 

Type `String`
Returns the joined option value names. If an option value does not exist in the option list, uses the option value for joining.
Throws an exception if the data table does not exist

**Example**

```javascript
//Option value list: a:'选项1',b:'选项2'
//{amount=11, name=测试采购单, id=z2koxrkxtp854,type=a} 
Record.getRecordOptionNames('order', 'type', ['a', 'b'], ',')//选项1,选项2
Record.getRecordOptionNames('order', 'type', ['a', 'b', 'c'], ',')//选项1,选项2,c
```



## getRecordOptions

Returns the option value list

```javascript
Record.getRecordOptions(tableId, fieldId)
```

| Parameter | Type | Description |
|---------|--------|---------|
| tableId | `String` | Data table identifier |
| fieldId | `String` | Field identifier |

**Return Value**

Type `Array<Option>`
Returns the option value list. Returns null if the field is not `List Select`, `Tree Select`, or `Cascade Select`.
Throws an exception if the data table does not exist

**Example**

```javascript
//Option value list: a:'选项1',b:'选项2'
Record.getRecordOptions('order', 'type')//[{id:'a',name:'选项1'},{id:'b',name:'选项2'}]
```



## getRelationList

Returns the value of a data table relation list field

```javascript
Record.getRelationList(tableId, fieldId, recordId)
```

| Parameter | Type | Description |
|----------|--------|---------|
| tableId  | `String` | Data table identifier |
| fieldId  | `String` | Field identifier |
| recordId | `String` | Record ID |

**Return Value** 

Type `Array<Record>`
Returns the relation list values. Returns an empty array if the field is not a `Relation List`.
Throws an exception if the data table does not exist

**Example**
```javascript
Record.getRelationList('order','orderDetail','z2koxrkxtp854')
```

## getCountByField

Gets the count of data table records filtered by a single field

```javascript
Record.getCountByField(tableId, fieldId, opt, value)
```

| Parameter | Type | Description |
|---------|--------|----------------------------------------------|
| tableId | `String` | Data table identifier |
| fieldId | `String` | Field to filter by |
| opt     | `String` | Operator, see `ConditionOpt` for operators |
| value   | `Object` | Filter condition value |

**Return Value**

Type `Number`
Returns the count of records matching the condition.
Throws an exception if the data table does not exist
 
**Example**

```javascript
//{amount=11, name=测试采购单, id=z2koxrkxtp854} 
Record.getCountByField('order', 'amount', 'eq', 11)//1
```

## getCountByFields

Gets the count of data table records filtered by multiple fields

```javascript
Record.getCountByFields(tableId, conditions)
```

| Parameter | Type | Description |
|------------|--------|----------------------------------------------|
| tableId    | `String` | Data table identifier |
| conditions | `Array`  | Filter conditions, see [Condition](../script/model.html#condition) for details |

**Return Value**

Type `Number`
Returns the count of records matching the conditions.
Throws an exception if the data table does not exist

**Example**

```javascript
//{amount=11, text=13, id=z2koxrkxtp854} 
Record.getCountByFields('tab', [{ "fieldId": 'text', "opt": "eq", "value": '13' }])//1
```

## count

Gets the count of data table records filtered by multiple fields (similar to getCountByFields)

```javascript
Record.count(tableId, conditions)
```

| Parameter | Type | Description |
|------------|--------|----------------------------------------------|
| tableId    | `String` | Data table identifier |
| conditions | `Array`  | Filter conditions, see [Condition](../script/model.html#condition) for details |

**Return Value**

Type `Number`
Returns the count of records matching the conditions.
Throws an exception if the data table does not exist

**Example**

```javascript
//{amount=11, text=13, id=z2koxrkxtp854} 
Record.count('tab', [{ "fieldId": 'text', "opt": "eq", "value": '13' }])//1
```

## stream

Creates a data table record stream for chaining filters and queries

```javascript
Record.stream(tableId)
```

| Parameter | Type | Description |
|---------|--------|---------|
| tableId | `String` | Data table identifier |

**Return Value**

Type `RecordStream`
Returns a record stream object that can chain filter conditions and execute queries.

**Example**

```javascript
Record.stream('order')
  .filter('amount', 'eq', 11)
  .limit(10)
  .list()
```

```javascript
// Using orderBy to sort by field
Record.stream('order')
  .filter('status', 'eq', 'completed')
  .orderBy('createdAt', 'desc')  // Sort by creation time descending
  .orderBy('amount', 'asc')      // Then sort by amount ascending
  .limit(20)
  .list()
```

### RecordStream Methods

RecordStream objects provide the following chainable methods:

#### limit

Sets the maximum number of records to return

```javascript
stream.limit(limit)
```

| Parameter | Type | Description |
|-------|--------|---------|
| limit | `Number` | Maximum number of records |

**Return Value** `RecordStream` itself, for chaining.

#### id

Filters records by ID

```javascript
stream.id(recordId)
```

| Parameter | Type | Description |
|----------|--------|------|
| recordId | `String` | Record ID |

**Return Value** `RecordStream` itself, for chaining.

#### filter

Adds a filter condition

```javascript
stream.filter(fieldId, opt, value)
stream.filter(fieldId, opt, value, func)
```

| Parameter | Type | Description |
|---------|--------|----------------------------------------------|
| fieldId | `String` | Field to filter by |
| opt     | `String` | Operator, see `ConditionOpt` for operators |
| value   | `Object` | Filter condition value |
| func    | `String` | Optional, function name, e.g. `date` for date functions |

**Return Value** `RecordStream` itself, for chaining.

#### orderBy

Adds a sort condition

```javascript
stream.orderBy(fieldId, type)
```

| Parameter | Type | Description |
|---------|--------|------------------------|
| fieldId | `String` | Sort field |
| type    | `String` | Sort type: `asc` or `desc` |

**Return Value** `RecordStream` itself, for chaining.

**Example**

```javascript
// Sort by creation time descending
stream.orderBy('createdAt', 'desc')

// Sort by amount ascending  
stream.orderBy('amount', 'asc')

// Chain multiple sort conditions
stream
  .orderBy('status', 'asc')
  .orderBy('createdAt', 'desc')
```

#### list

Executes the query and returns a list of records

```javascript
stream.list()
```

**Return Value**

Type `Array<Record>`
Returns a list of records matching the conditions, limited by the limit setting.

#### count

Executes the query and returns the record count

```javascript
stream.count()
```

**Return Value**

Type `Number`
Returns the count of records matching the conditions.

#### first

Executes the query and returns the first record

```javascript
stream.first()
```

**Return Value**

Type `Record`
Returns the first record, or `null` if no records match the conditions.

#### firstProp

Executes the query and returns the specified field value of the first record

```javascript
stream.firstProp(fieldId)
```

| Parameter | Type | Description |
|---------|--------|---------|
| fieldId | `String` | Field identifier |

**Return Value**

Type `Object`
Returns the specified field value of the first record, or `null` if no records match the conditions.
