# informat.table Data Table Operations

## Overview

Use the `informat.table` object to perform data table related operations.
:::tip Note
Update, insert, and delete operations on data tables in scripts will not trigger listeners.
:::

## Query Usage Example

```javascript
const query = {
  // Page number, starting from 1. Default is 1
  pageIndex: 1,
  // Number of records per page. Default is 100, -1 means query all data
  pageSize: 10,
  // Filter - TableRecordFilter
  filter: {
    // Filter conditions - TableRecordCondition
    conditionList: [
      {
        // Field identifier to query
        fieldId: "name",
        /**
         * Comparison method - TableRecordConditionOpt, values are:
         * eq                Equals
         * ne                Not equals
         * gt                Greater than
         * ge                Greater than or equals
         * lt                Less than
         * le                Less than or equals
         * contains          Contains
         * notcontains       Does not contain
         * startswith        Starts with
         * endswith          Ends with
         * isnull            Is null
         * isnotnull         Is not null
         * in                In list
         * notin             Not in list
         * between           In range
         * notbetween        Not in range
         * parenteq          Parent object equals
         * parentrooteq      Root node equals
         * parentcontains    Parent object contains
         * multipleandquery  Multiple value AND fuzzy query
         * multipleorquery   Multiple value OR fuzzy query
         * intree            In tree
         */
        opt: "eq",
        /**
         * Processing function for data values - TableRecordConditionFunc
         * For date type fields:
         * week                 Day of the week (Monday=1, Tuesday=2, ..., Sunday=7)
         * month                Month of the year
         * quarter              Quarter of the year
         * year                 Year
         * dayofyear            Day of the year
         * weekofyear           Week of the year
         * dayofmonth           Day of the month
         * daytonow             Days from today (yesterday=1, today=0, tomorrow=-1)
         * weektonow            Weeks from today (last week=1, this week=0, next week=-1)
         * monthtonow           Months from today (last month=1, this month=0, next month=-1)
         * quartertonow         Quarters from today (last quarter=1, this quarter=0, next quarter=-1)
         * yeartonow            Years from today (last year=1, this year=0, next year=-1)
         * fmtday               Year-Month-Day format: 2021-01-01
         * fmtweek              Year-Week format: 2021-1
         * fmtmonth             Year-Month format: 2021-01
         * fmtquarter           Year-Quarter format: 2021-1
         * For member type fields:
         * nameOfAccount        Name
         */
        func: null,
        // Comparison value
        value: "张三",
      },getTableInfo
    ],
    // Nested sub-filters, value is an array of TableRecordFilter, supports layered nesting
    children: [],
    /**
     * Combination method of sub-filters with parent filter
     * Values:
     * and      Match all
     * or       Match any
     */
    opt: "and",
  },
  // Field identifier list to include in return values. Returns all fields when not provided or empty array
  includeFields: ["id", "name", "age"],
  // Group by field identifier list
  groupByList: [],
  // Aggregation query list - TableRecordAggregationQuery
  aggregationQueryList: [
    {
      // Field to aggregate
      fieldId: "sex",
      /**
       * Aggregation method
       * Values:
       * count        Count
       * avg          Average (number, date types)
       * sum          Sum (number, date types)
       * max          Maximum (number, date types)
       * min          Minimum (number, date types)
       */
      func: "count",
      // Whether to deduplicate
      distinct: false,
    },
  ],
  // Sort order array - OrderBy
  orderByList: [
    {
      // Field identifier to sort by
      field: "name",
      /**
       * Sort direction values:
       * asc      Ascending
       * desc     Descending
       */
      type: "desc",
    },
  ],
  // Distinct field identifier list
  distinctFieldList: [],
  // Field identifier list to exclude from return values. Returns all fields when not provided or empty array
  excludeFields: [],
  // Whether to return option names. Returns option names for `List Selection`, `Cascade Selection`, `Tree Selection` fields
  returnOptionName: false,
};
```

:::warning Important Notes

**Difference between contains and in in TableRecordConditionOpt**

For example: A task table has an owner field (identifier: owner, type: User Selection, multiple), with the following records:

| ID  | Owner    |
| --- | --------- |
| 1   | Zhang San, Li Si |
| 2   | Zhang San      |
| 3   | Wang Wu      |

- Contains: The right-side member list contains any one of the left-side members

  - { fieldId: 'owner', opt: 'contains', value: ['张三'] }
    Records 1 and 2 satisfy the condition

- In list: The right-side member list contains all of the left-side members
  - { fieldId: 'owner', opt: 'in', value: ['张三'] }
    Only record 2 satisfies the condition
  - { fieldId: 'owner', opt: 'in', value: ['张三','李四'] }
    Records 1 and 2 satisfy the condition

:::

## queryList

Query multiple records by condition

```javascript
informat.table.queryList(tableId, query);
```

| Parameter    | Type                                            | Description           |
| ------- | ----------------------------------------------- | -------------- |
| tableId | String                                          | Data table identifier |
| query   | [`Query`](/guide/script/table.md#query使用示例) | Query criteria       |

#### Return Value

Data record list, type is `Array<Object>`

:::: tabs

::: tab "Example 1 - Query"
Query the top 3 employees whose names contain Zhang or Li and age is greater than 20, sorted by age ascending

```js
informat.table.queryList("staffs", {
  pageIndex: 1,
  pageSize: 3,
  filter: {
    opt: "and",
    conditionList: [{ fieldId: "age", opt: "gt", value: "20" }],
    children: [
      {
        opt: "or",
        conditionList: [
          { fieldId: "name", opt: "startswith", value: "张" },
          { fieldId: "name", opt: "startswith", value: "李" },
        ],
      },
    ],
  },
  orderByList: [{ field: "age", type: "asc" }],
});
```

The above call is equivalent to SQL

```sql
where age>20 and (name like '张%' or name like '李%')
```

:::

::: tab "Example 2 - Cascade Selection"
Query employee list where the area is Nanshan District, Shenzhen City

```javascript
informat.table.queryList("staffs", {
  pageIndex: 1,
  pageSize: 3,
  filter: {
    opt: "and",
    conditionList: [{ fieldId: "area", opt: "eq", value: ["广东省", "深圳市", "南山区"] }],
  },
});
```

:::

::: tab "Example 3 - Child Object"

Child object - Query all sub-departments of the Technology department

```javascript
informat.table.queryList("scriptTableB", {
  pageSize: -1,
  filter: {
    opt: "and",
    conditionList: [{ fieldId: "children", opt: "parentrooteq", value: ["rpev2ztqnbu8o"] }],
  },
});
```

Return data:

```json
[
  {
    "children": "o32bbe3eqrrg0.zzzq65nxu0qv1",
    "id": "c91au1arsncd6"
  },
  {
    "children": "o32bbe3eqrrg0.zzzq65nxu0qv1",
    "id": "z00ei9fqymbra"
  },
  {
    "children": "o32bbe3eqrrg0.zzzq65nxu0qv1.z00ei9fqymbra",
    "id": "ci92j4ddenf9o"
  }
]
```

:::

::: tab "Example 4 - Return Specific Fields"

Paginated query of employee list, returning only name and sex fields, and returning option names for sex \*

```javascript
informat.table.queryList("staffs", {
  pageIndex: 1, //Starting from 1
  pageSize: 10,
  returnOptionName: true,
  includeFields: ["name", "sex"],
});
```

:::

::: tab "Example 5 - Return Data Excluding Specific Fields"

Paginated query of employee list, returning all fields except name and sex \*

```javascript
informat.table.queryList("staffs", {
  pageIndex: 1, //Starting from 1
  pageSize: 10,
  excludeFields: ["name", "sex"],
});
```

:::

::: tab "Example 6 - Aggregation Query"

Group by age aggregation query

```javascript
informat.table.queryList("staffs", {
  groupByList: ["age"],
  /*
   * Date aggregation query
   * groupByList usage example: groupByList: ['dataTime$year'],
   * dataTime: aggregation field
   * $ aggregation method separator
   * year: aggregation method. Year: year, Month of year: month, Day of week: week
   * See TableRecordQuery documentation
   */
  aggregationQueryList: [
    {
      func: "count",
      fieldId: "age",
    },
  ],
  orderByList: [{ field: "age", type: "asc" }],
});
```

Return data:

```json
[
  {
    "age": 23,
    "age_count": 2
  },
  {
    "age": 24,
    "age_count": 1
  },
  {
    "age": 25,
    "age_count": 1
  }
]
```

Group by birthday year aggregation query


```javascript
informat.table.queryList('staffs', {
    groupByList:["birthday$year"],
    aggregationQueryList: [
        {
            func: 'count'
        }
    ],
    orderByList: [{ field: 'birthday$year', type: 'asc' }]
});
```

Return data:

```json
[
  {
    "birthday$year":"1998",
    "count":2
  },
  {
    "birthday$year":"1999",
    "count":1
  },
  {
    "birthday$year":"2000",
    "count":1
  }
]
```

:::

::: tab "Example 7 - Query employees created in May 2025 (using fmtmonth)"

```javascript
informat.table.queryList("staffs", {
  pageSize: -1,
  filter: {
    conditionList: [{ fieldId: "createTime", opt: "eq", func:"fmtmonth", value: "2025-05" }],
  }
});
```

Return data:

```json
[
  {
    "createUser_name":"skydu",
    "recordId":"kq91s9fosqh2l",
    "id":"kq91s9fosqh2l",
    "seq":415,
    "rewardCount":0,
    "updateUser_name":"skydu",
    "seqno":415,
    "staffNo":"INFO-2025-00012",
    "sex":"male",
    "updateUser":"skydu",
    "updateTime":1746755574341,
    "totalLevelDays":0,
    "createTime":1746755574341,
    "grade":4,
    "name":"张三",
    "updateUser_avatar":"pic10.png",
    "createUser":"skydu",
    "createUser_avatar":"pic10.png",
    "age":28,
    "status":"onjob"
  }
]
```
:::


::::

## queryListCount

Query the count of records matching conditions

```javascript
informat.table.queryListCount(tableId, filter);
```

| Parameter    | Type                | Description           |
| ------- | ------------------- | -------------- |
| tableId | String              | Data table identifier |
| filter  | `TableRecordFilter` | Query criteria, required; pass `{}` when there is no filter; do not omit it |

#### Return Value

Count of records matching the conditions, type is `Integer`

**_Example_**

::: code-group

```js
informat.table.queryListCount("staffs", {
  conditionList: [{ fieldId: "name", opt: "contains", value: "张" }],
});
```

When there is no filter, still pass the second argument:

```js
informat.table.queryListCount("staffs", {});
```

```json
2
```

:::


## getTableInfo

Query data table information

```javascript
informat.table.getTableInfo(tableId);
```

| Parameter    | Type   | Description           |
| ------- | ------ | -------------- |
| tableId | String | Data table identifier |

#### Return Value

Type is [TableInfo](/guide/script/model.md#tableinfo), returns data table information

**_Example_**
::: code-group

```js
informat.table.getTableInfo("task");
```

```json
{
  "table": {
    "id": "cfg9ywr41G",
    "key": "task",
    "name": "任务"
  },
  "tableFieldList": [
    {
      "id": "id",
      "key": "id",
      "name": "id",
      "type": "UUID"
    },
    {
      "id": "mzqlwrDgOM",
      "key": "expectDate",
      "name": "期望完成时间",
      "type": "Date"
    },
    {
      "id": "tp0rfnbmcc3sd",
      "key": "updateTime",
      "name": "更新时间",
      "type": "LastModifyTime"
    },
    {
      "id": "u3qh6zf0lgwus",
      "key": "updateUser",
      "name": "更新人",
      "type": "LastModifyUser"
    },
    {
      "id": "Wfgb3bwKdf",
      "key": "name",
      "name": "名称",
      "type": "SingleText"
    }
  ]
}
```

:::


## getTableFieldInfo

Query data table field information

```javascript
informat.table.getTableFieldInfo(tableId, fieldId);
```

| Parameter    | Type   | Description               |
| ------- | ------ | ------------------ |
| tableId | String | Data table identifier     |
| fieldId | String | Data table field identifier |

#### Return Value

Type is [TableFieldInfo](/guide/script/model.md#tablefieldinfo), returns data table field information

**_Example_**

::: code-group

```js
informat.table.getTableFieldInfo("task", "name");
```

```json
{
  "changeLogAccessRoleList": [],
  "defaultValueRuleList": [],
  "displayWidth": 50,
  "enableChangeLog": true,
  "hidden": false,
  "icon": "text",
  "id": "Wfgb3bwKdf",
  "key": "name",
  "name": "名称",
  "readonly": false,
  "singleTextSetting": {
    "autoCompleteAutomaticVarList": [],
    "autoCompleteTriggerOnFocus": false,
    "buttonList": [],
    "enableAutoComplete": false,
    "format": "string",
    "max": 200,
    "min": 0,
    "nullable": true,
    "storageSize": 200
  },
  "tableId": "task",
  "type": "SingleText",
  "validateRuleList": []
}
```

:::

## queryById

Query a single record by ID

```javascript
informat.table.queryById(tableId, recordId);
```

| Parameter     | Type   | Description              |
| -------- | ------ | ----------------- |
| tableId  | String | Data table identifier    |
| recordId | String | ID of the record to query |

#### Return Value

The queried data record, type is `Object`

**_Example_**

::: code-group

```js
informat.table.queryById("task", "aorxux52i4t1z");
```

```json
{
  "id": "aorxux52i4t1z",
  "name": "任务1",
  "startDate": "2022-12-05 00:00:00.0"
}
```

:::

## queryOne

Query the first record matching the conditions

```javascript
informat.table.queryOne(tableId, query);
```

| Parameter    | Type                                                       | Description           |
| ------- | ---------------------------------------------------------- | -------------- |
| tableId | String                                                     | Data table identifier |
| query   | [`TableRecordQuery`](/guide/script/table.md#query使用示例) | Query criteria       |

#### Return Value

The queried data record, type is `Object`

**_Example_**

::: code-group

```js
informat.table.queryOne("task", {
  pageSize: 1,
  filter: {
    conditionList: [{ fieldId: "name", opt: "eq", value: "任务1" }],
  },
});
```

```json
{
  "id": "aorxux52i4t1z",
  "name": "任务1",
  "startDate": "2022-12-05 00:00:00.0"
}
```

:::

## query

Query a single record by ID and conditions

```javascript
informat.table.query(tableId, recordId, setting);
```

| Parameter     | Type                      | Description              |
| -------- | ------------------------- | ----------------- |
| tableId  | String                    | Data table identifier    |
| recordId | String                    | ID of the record to query |
| setting  | `TableRecordQuerySetting` | Query settings          |

`TableRecordQuerySetting` structure:

| Parameter             | Type            | Description                                                               |
| ---------------- | --------------- | ------------------------------------------------------------------ |
| forUpdate        | Boolean         | Whether to lock the row                                                         |
| returnOptionName | Boolean         | If there are `List Selection`, `Cascade Selection`, `Tree Selection` fields, also returns option value names |
| includeFields    | `Array<String>` | Field list to return. Returns all fields if empty                           |

#### Return Value

The queried data record, type is `Object`

**_Example: Query a record with row lock_**

::: code-group

```js
informat.table.query("task", "aorxux52i4t1z", {
  forUpdate: true,
});
```

```json
{
  "id": "aorxux52i4t1z",
  "name": "任务1",
  "startDate": "2022-12-05 00:00:00.0"
}
```

:::



## insert

Create a record

For `Creator`, `Creation Time`, `Last Modifier`, and `Last Modified Time` fields, if these are not provided in the record being created, the system will use the current time as `Creation Time`
and `Last Modified Time`, and the current operator as `Creator` and `Last Modifier`. If the record creation is triggered by a scheduled task, the current operator is `INFORMAT`.

```javascript
informat.table.insert(tableId, data);
```

| Parameter    | Type   | Description           |
| ------- | ------ | -------------- |
| tableId | String | Data table identifier |
| data    | Object | Record to create |

#### Return Value

Returns the created record ID

#### Example

::: code-group

```js
informat.table.insert("staffs", {
  name: "赵六",
  sex: "male",
  age: 30,
  grade: 5,
  area: ["广东省", "深圳市", "南山区"],
});
```

```json
"twmvau4ogujcc"
```

:::

For detailed formats, see: [**Record Type Conversion**](/guide/table/table_transform_record.md)

## insertEx

Create a record with configuration
Similar to `insert`, the only difference is the additional configuration parameter

```javascript
informat.table.insertEx(tableId, data, config);
```

| Parameter    | Type                 | Description           |
| ------- | -------------------- | -------------- |
| tableId | String               | Data table identifier |
| data    | Object               | Record to create |
| config  | `InsertRecordConfig` | Configuration       |

`InsertRecordConfig` structure:

| Parameter                        | Type    | Description                          |
| --------------------------- | ------- | ----------------------------- |
| disableCalculateRollupField | Boolean | Whether to skip rollup field calculation, default false |

When creating a new record, if the table is a sub-table of a main table and certain fields are rollup fields from lookup rollup or relation list rollup in the main table, the system will automatically calculate these rollup fields in the main table. For example, when creating a large number of sub-table records at once, there is actually no need to recalculate the main table's rollup fields each time a sub-table record is created, because rollup calculation takes considerable time. Therefore, you only need to recalculate the rollup after the last sub-table record is created.
To improve efficiency and reduce unnecessary calculations, you can set the `disableCalculateRollupField` configuration parameter in `InsertRecordConfig`
to `true`
in this case. This way, the system will not calculate rollup fields each time a sub-table record is created. After all sub-table records are created, call `informat.table.refreshRelationRollup`
and `informat.table.refreshLookupRollup` separately to calculate the rollups.

#### Return Value

Created record ID

::: code-group

```js
informat.table.insertEx(
  "staffs",
  {
    name: "赵六",
    sex: "male",
    age: 30,
    grade: 5,
    area: ["广东省", "深圳市", "南山区"],
  },
  {
    disableCalculateRollupField: true,
  }
);
```

```json
"ecxnsomw69dmn"
```

:::

## batchInsert

Batch create records

For `Creator`, `Creation Time`, `Last Modifier`, and `Last Modified Time` fields, if these are not provided in the records being created, the system will use the current time as `Creation Time`
and `Last Modified Time`, and the current operator as `Creator` and `Last Modifier`. If the record creation is triggered by a scheduled task, the current operator is `INFORMAT`.

```javascript
informat.table.batchInsert(tableId, dataList);
```

| Parameter     | Type   | Description               |
| -------- | ------ | ------------------ |
| tableId  | String | Data table identifier       |
| dataList | Array  | List of records to create |

#### Return Value

Number of created records

:::: tabs

::: tab "Example 1 - Batch Insert"

::: code-group

```js
informat.table.batchInsert("staffs", [
  { name: "赵六", sex: "male", age: 30, grade: 5, area: ["广东省", "深圳市", "南山区"] },
  { name: "孙七", sex: "female", age: 27, grade: 4, area: ["广东省", "深圳市", "宝安区"] },
]);
```

```json
2
```

:::

::: tab "Example 2 - Batch Insert with Custom Record IDs"

::: code-group

```js
informat.table.batchInsert("staffs", [
  { id: "1", name: "赵六", sex: "male", age: 30, grade: 5, area: ["广东省", "深圳市", "南山区"] },
  { id: "2", name: "孙七", sex: "female", age: 27, grade: 4, area: ["广东省", "深圳市", "宝安区"] },
]);
```

```json
2
```

:::
::::

:::warning Important Notes
Differences between batch insert and single record insert:

`Child Object Number`, `Number`, `Lookup Rollup`, and `Relation List Rollup` fields are not calculated during batch insert.
:::

## update

Update a record
For `Last Modifier` and `Last Modified Time` fields, if these are not provided in the update record, the system will use the current time as `Last Modified Time`
and the current operator as `Last Modifier`. If the update is triggered by a scheduled task, the current operator is `INFORMAT`.

```javascript
informat.table.update(tableId, data);
```

| Parameter    | Type   | Description           |
| ------- | ------ | -------------- |
| tableId | String | Data table identifier |
| data    | Object | Record to update |

#### Return Value

Number of successfully updated records

#### Example 1

::: code-group

```js
informat.table.update("staffs", {
  id: "1",
  name: "赵六2",
  sex: "male",
  age: 28,
  grade: 2,
  area: ["广东省", "深圳市", "福田区"],
});
```

```json
1
```

:::

For detailed formats, see: [**Record Type Conversion**](/guide/table/table_transform_field.md)

## updateEx

Update a record with configuration
Similar to `update`, the only difference is the additional update configuration parameter

```javascript
informat.table.updateEx(tableId, data, config);
```

| Parameter    | Type                 | Description           |
| ------- | -------------------- | -------------- |
| tableId | String               | Data table identifier |
| data    | Object               | Record to update |
| config  | `UpdateRecordConfig` | Update configuration   |

`UpdateRecordConfig` structure:

| Parameter                        | Type    | Description                          |
| --------------------------- | ------- | ----------------------------- |
| enableChangeLog             | Boolean | Whether to enable change log, default false   |
| disableCalculateRollupField | Boolean | Whether to skip rollup field calculation, default false |
| updateBpmnInstaceFormVar    | Boolean | Whether to sync update workflow instance form variables, default false |

When updating records, if the table is a sub-table of a main table and the updated fields are rollup fields from lookup rollup or relation list rollup in the main table, the system will automatically calculate these rollup fields in the main table. For example, when updating a large number of sub-table records at once, there is actually no need to recalculate the main table's rollup fields each time a sub-table record is updated, because rollup calculation takes considerable time. Therefore, you only need to recalculate the rollup after the last sub-table record is updated.
To improve efficiency and reduce unnecessary calculations, you can set the `disableCalculateRollupField` configuration parameter in `UpdateRecordConfig`
to `true`
in this case. This way, the system will not calculate rollup fields each time a sub-table record is updated. After all sub-table records are updated, call `informat.table.refreshRelationRollup`
and `informat.table.refreshLookupRollup` separately to calculate the rollups.

#### Example 1

::: code-group

```js
informat.table.updateEx(
  "staffs",
  {
    id: "1",
    name: "赵六2",
    sex: "male",
    age: 28,
    grade: 2,
    area: ["广东省", "深圳市", "福田区"],
  },
  {
    enableChangeLog: true,
    disableCalculateRollupField: true,
  }
);
```

```json
1
```

:::

#### Return Value

Number of successfully updated records

## batchUpdate

Batch update records
For `Last Modifier` and `Last Modified Time` fields, if these are not provided in the update records, the system will use the current time as `Last Modified Time`
and the current operator as `Last Modifier`. If the update is triggered by a scheduled task, the current operator is `INFORMAT`.
Note: All records in the update list must have the same set of updated fields. If a value is null, it will also be batch updated to null.

```javascript
informat.table.batchUpdate(tableId, dataList);
```

| Parameter     | Type   | Description               |
| -------- | ------ | ------------------ |
| tableId  | String | Data table identifier     |
| dataList | Object | List of records to update |

**Example**

::: code-group

```js
informat.table.batchUpdate("staffs", [
  { id: "1", name: "赵六2", sex: "male", age: 29, grade: 3, area: ["广东省", "深圳市", "南山区"] },
  { id: "2", name: "孙七2", sex: "female", age: 26, grade: 2, area: ["广东省", "深圳市", "宝安区"] },
]);
```

```json
3
```

:::

:::warning Important Notes
Differences between batch update and single record update:

`Child Object Number`, `Number`, `Lookup Rollup`, and `Relation List Rollup` fields are not calculated during batch update.
:::

## updateList

Update multiple records by condition

```javascript
informat.table.updateList(tableId, filter, data);
```

| Parameter    | Type     | Description           |
| ------- | -------- | -------------- |
| tableId | String   | Data table identifier |
| filter  | `Filter` | Filter criteria       |
| data    | Object   | Data to update |

#### Return Value

Number of successfully updated records

Example: Update the grade of all employees with last name Zhang to 4

::: code-group

```js
informat.table.updateList(
  "staffs",
  {
    conditionList: [{ fieldId: "name", opt: "contains", value: "张%" }],
  },
  { grade: 4 }
);
```

```json
2
```

:::

## updateListEx

Update multiple records by condition and configuration

```javascript
informat.table.updateListEx(tableId, filter, data, config);
```

| Parameter    | Type                 | Description           |
| ------- | -------------------- | -------------- |
| tableId | String               | Data table identifier |
| filter  | `Filter`             | Filter criteria       |
| data    | Object               | Data to update |
| config  | `UpdateRecordConfig` | Update configuration   |

`UpdateRecordConfig` structure:

| Parameter                        | Type    | Description                          |
| --------------------------- | ------- | ----------------------------- |
| enableChangeLog             | Boolean | Whether to enable change log, default false   |
| disableCalculateRollupField | Boolean | Whether to skip rollup field calculation, default false |
| updateBpmnInstaceFormVar    | Boolean | Whether to sync update workflow instance form variables, default false |

#### Return Value

Number of successfully updated records

Example:

::: code-group

```js
informat.table.updateListEx(
  "staffs",
  {
    conditionList: [{ fieldId: "name", opt: "contains", value: "张%" }],
  },
  { grade: 4 },
  { disableCalculateRollupField: true }
);
```

```json
2
```

:::

## delete

If the recycle bin is enabled, deleted records will be placed in the recycle bin.
Delete a single record

```javascript
informat.table.delete(tableId, recordId);
```

| Parameter     | Type   | Description              |
| -------- | ------ | ----------------- |
| tableId  | String | Data table identifier    |
| recordId | String | ID of the record to delete |

#### Return Value

Number of successfully deleted records

Example:

::: code-group

```js
informat.table.delete("staffs", "twmvau4ogujcc");
```

```json
1
```

:::

## deleteEx

Delete a record with configuration
Similar to `delete`, the only difference is the additional configuration parameter

```javascript
informat.table.deleteEx(tableId, recordId, config);
```

| Parameter     | Type                 | Description              |
| -------- | -------------------- | ----------------- |
| tableId  | String               | Data table identifier    |
| recordId | String               | ID of the record to delete |
| config   | `DeleteRecordConfig` | Configuration          |

`DeleteRecordConfig` structure:

| Parameter                        | Type    | Description                          |
| --------------------------- | ------- | ----------------------------- |
| disableCalculateRollupField | Boolean | Whether to skip rollup field calculation, default false |

When deleting records, if the table is a sub-table of a main table and certain fields are rollup fields from lookup rollup or relation list rollup in the main table, the system will automatically calculate these rollup fields in the main table. For example, when deleting a large number of sub-table records at once, there is actually no need to recalculate the main table's rollup fields each time a sub-table record is deleted, because rollup calculation takes considerable time. Therefore, you only need to recalculate the rollup after the last sub-table record is deleted.
To improve efficiency and reduce unnecessary calculations, you can set the `disableCalculateRollupField` configuration parameter in `DeleteRecordConfig`
to `true`
in this case. This way, the system will not calculate rollup fields each time a sub-table record is deleted. After all sub-table records are deleted, call `informat.table.refreshRelationRollup`
and `informat.table.refreshLookupRollup` separately to calculate the rollups.

#### Return Value

Number of successfully deleted records

## deleteList

If the recycle bin is enabled, deleted records will be placed in the recycle bin.
Delete multiple records by condition

```javascript
informat.table.deleteList(tableId, filter);
```

| Parameter    | Type     | Description           |
| ------- | -------- | -------------- |
| tableId | String   | Data table identifier |
| filter  | `Filter` | Filter criteria       |

#### Return Value

Number of successfully deleted records

Example: Delete employees who have resigned

::: code-group

```js
informat.table.deleteList("staffs", {
  conditionList: [{ fieldId: "status", opt: "ge", value: "dimission" }],
});
```

```json
2
```

:::

:::tip
The underlying implementation of `informat.table.deleteList`
first queries all records, then deletes them one by one. If a recycle bin is configured, deleted records are placed in the recycle bin, so it is not fast. When batch deleting a large number of records and seeking better performance, use
`informat.table.batchDelete`
:::

## deleteListEx

If the recycle bin is enabled, deleted records will be placed in the recycle bin.
Delete multiple records by condition and configuration

```javascript
informat.table.deleteListEx(tableId, filter, config);
```

| Parameter    | Type                 | Description           |
| ------- | -------------------- | -------------- |
| tableId | String               | Data table identifier |
| filter  | `Filter`             | Filter criteria       |
| config  | `DeleteRecordConfig` | Configuration       |

#### Return Value

Number of successfully deleted records

Example:

::: code-group

```js
informat.table.deleteListEx(
  "user",
  {
    conditionList: [{ fieldId: "id", opt: "in", value: ["k3oybvxo0lwxv", "htfesu6ghbcro"] }],
  },
  {
    disableCalculateRollupField: true,
  }
);
```

```json
2
```

:::

## batchDelete

Batch delete records
If the recycle bin is enabled, deleted records will NOT be placed in the recycle bin.

```javascript
informat.table.batchDelete(tableId, idList);
```

| Parameter    | Type   | Description         |
| ------- | ------ | ------------ |
| tableId | String | Data table identifier |
| idList  | Array  | Record ID list |

**_Example_**

::: code-group

```js
informat.table.batchDelete("staffs", ["uphuksrz88xij", "cyljta5v60mup"]);
```

```json
2
```

:::

## queryRelationList

Query the sub-table record list corresponding to a relation list field by main table record ID

```javascript
informat.table.queryRelationList(tableId, relationFieldId, recordId, query);
```

| Parameter            | Type    | Description            |
| --------------- | ------- | --------------- |
| tableId         | String  | Data table identifier  |
| relationFieldId | String  | Relation list field ID |
| recordId        | String  | Main table record ID   |
| query           | `Query` | Sub-table query criteria    |

#### Return Value

Data record list, type is `Array<Object>`

**_Example_**

```javascript
informat.table.queryRelationList("staffs", "rewardList", "yhg8b23ej2gt6", {
  pageIndex: 1,
  pageSize: 50,
  filter: {
    conditionList: [{ fieldId: "name", opt: "contains", value: "优秀员工" }],
  },
});
```

## addRelation

Add a relation list value

```javascript
informat.table.addRelation(tableId, relationFieldId, recordId, relationRecordId);
```

| Parameter             | Type   | Description              |
| ---------------- | ------ | ----------------- |
| tableId          | String | Data table identifier    |
| relationFieldId  | String | Relation list field      |
| recordId         | String | Main table record ID     |
| relationRecordId | String | Relation list record ID |

**_Example_**

```javascript
informat.table.addRelation("staffs", "rewardList", "yhg8b23ej2gt6", "rgf4fbbb543kj");
```

## deleteRelation

Delete a relation list value

```javascript
informat.table.deleteRelation(tableId, relationFieldId, recordId, relationRecordId);
```

| Parameter             | Type   | Description              |
| ---------------- | ------ | ----------------- |
| tableId          | String | Data table identifier    |
| relationFieldId  | String | Relation list field      |
| recordId         | String | Main table record ID     |
| relationRecordId | String | Relation list record ID |

**_Example_**

```javascript
informat.table.deleteRelation("staffs", "rewardList", "yhg8b23ej2gt6", "rgf4fbbb543kj");
```

## hasRelation

Check if records exist in a relation list
If the relation list contains any of the record IDs specified in relationRecordIdList, those record IDs are included in the returned array.

For example, if the relation list contains:

- record1
- record2
- record3

And relationRecordIdList is `record1` `record2` `record4`, the return value is `record1` `record2`

```javascript
informat.table.hasRelation(tableId, relationFieldId, recordId, relationRecordIdList);
```

| Parameter                 | Type                | Description                   |
| -------------------- | ------------------- | ---------------------- |
| tableId              | String              | Data table identifier         |
| relationFieldId      | String              | Relation list field           |
| recordId             | String              | Main table record ID          |
| relationRecordIdList | Array&lt;String&gt; | Relation record ID list |

#### Return Value

List of record IDs that exist in the relationFieldId relation list of recordId, type is `Array<String>`

**_Example_**

```javascript
informat.table.hasRelation("staffs", "rewardList", "yhg8b23ej2gt6", ["rgf4fbbb543kj", "ct82dszf20s2u"]);
// Return data:
["rgf4fbbb543kj"];
```

## getRelationRecordIdList

Query the list of records that have a specified record in their relation list
Query data in the **main table** that has a relation with a **record ID** in the target table linked by a **relation list** field. Returns the list of related main table record IDs.

For example, the data table contains:

| Main Table Record ID | Relation List          |
| ----------- | ----------------- |
| m1          | [record1,record2] |
| m2          | [record1,record3] |
| m3          | [record3,record4] |

If the specified record is `record3`, the return value is `m2` `m3`

```javascript
informat.table.getRelationRecordIdList(tableId, relationFieldId, recordId);
```

| Parameter            | Type   | Description                        |
| --------------- | ------ | --------------------------- |
| tableId         | String | Main table data table identifier          |
| relationFieldId | String | Main table relation list field ID |
| recordId        | String | Sub-table record ID               |

#### Return Value

List of record IDs where recordId exists in the relationFieldId relation list, type is `Array<String>`

**_Example_**

```javascript
informat.table.getRelationRecordIdList("staffs", "rewardList", "rgf4fbbb543kj");
// Return data:
["yhg8b23ej2gt6"];
```

## updateChildrenField

Update a child object field

Move a record under parentRecordId. If the current record has child nodes, the child nodes will be updated accordingly.

```javascript
informat.table.updateChildrenField(tableId, childrenFieldId, recordId, parentRecordId);
```

| Parameter            | Type   | Description                                                         |
| --------------- | ------ | ------------------------------------------------------------ |
| tableId         | String | Data table identifier                                               |
| childrenFieldId | String | Child object field                                                   |
| recordId        | String | Record ID to update                                              |
| parentRecordId  | String | Parent node to move to. If parent node is `null`, the record will be moved to the root |

**_Example_**

```javascript
informat.table.updateChildrenField("task", "children", "z00ei9fqymbra", "zzzq65nxu0qv1");
```

## queryChildrenList

Query the `child object` record list of a specified record by condition

```javascript
informat.table.queryChildrenList(tableId, childrenFieldId, recordId, query);
```

| Parameter            | Type    | Description           |
| --------------- | ------- | -------------- |
| tableId         | String  | Data table identifier |
| childrenFieldId | String  | Child object field     |
| recordId        | String  | Main table record ID  |
| query           | `Query` | Query criteria       |

**_Example_**

::: code-group

```js
informat.table.queryChildrenList("staffsDept", "children", "rpev2ztqnbu8o", {
  pageIndex: 1,
  pageSize: 50,
});
```

```json
[
  {
    "children": "rpev2ztqnbu8o",
    "createTime": 1717500998762,
    "name": "技术一组",
    "id": "pz9y1fse8hccw",
    "seq": 5
  },
  {
    "children": "rpev2ztqnbu8o",
    "createTime": 1717501030793,
    "name": "技术二组",
    "id": "l8w9u9raftp2a",
    "seq": 6
  }
]
```

:::

## cloneAttachment

Copy attachment field files to a target field
Copy files from a source data table's attachment field to a target table's attachment field.

:::tip
Note: attachment is an object, not an array. If the attachment field is multi-select, you need to use array index to select the corresponding attachment object.
:::

```javascript
informat.table.cloneAttachment(sourceTableId, sourceFieldId, targetTableId, targetFieldId, attachment);
```

| Parameter          | Type                                                      | Description               |
| ------------- | --------------------------------------------------------- | ------------------ |
| sourceTableId | String                                                    | Source data table identifier   |
| sourceFieldId | String                                                    | Source field identifier     |
| targetTableId | String                                                    | Target data table identifier |
| targetFieldId | String                                                    | Target field identifier   |
| attachment    | [TableAttachment](/guide/script/model.md#tableattachment) | Attachment object           |

#### Return Value

Attachment object after successful copy, type is [TableAttachment](/guide/script/model.md#tableattachment)

**_Example_**

::: code-group

```js
var record = informat.table.queryById("staffs", "yhg8b23ej2gt6");
console.log("record.attachment", record.attachment);
if (record.attachment == null) {
  return null;
}
var targetAttachments = [];
record.attachment.forEach((att) => {
  //Multi-select
  var targetAttachment = informat.table.cloneAttachment("staffs", "attachment", "staffsDept", "attachment", att);
  targetAttachments.push(targetAttachment);
});
console.log("targetAttachments", targetAttachments);
informat.table.update("staffsDept", {
  id: "pz9y1fse8hccw",
  attachment: targetAttachments,
});
```

```json
[
  {
    "id": "1d14a4c1080e4f5992052aeab13951df.jpg",
    "md5": "b394f37c3180e68090e2a0f1370f2aa9",
    "name": "测试.jpg",
    "path": "uljrmxosme2uw/dwbndumn3dc8k/1d14a4c1080e4f5992052aeab13951df.jpg",
    "size": 7757,
    "thumbnail": "c270728528b54876abf67fb7e9ec4f24.jpg"
  }
]
```

:::

## moveAttachment

Move attachment field files to a target attachment field
Move files from a source data table's attachment field to a target table's attachment field.

:::tip
Note: attachment is an object, not an array. If the attachment field is multi-select, you need to use array index to select the corresponding attachment object.
:::

```javascript
informat.table.moveAttachment(sourceTableId, sourceFieldId, targetTableId, targetFieldId, attachment);
```

| Parameter          | Type                                                      | Description               |
| ------------- | --------------------------------------------------------- | ------------------ |
| sourceTableId | String                                                    | Source data table identifier   |
| sourceFieldId | String                                                    | Source field identifier     |
| targetTableId | String                                                    | Target data table identifier |
| targetFieldId | String                                                    | Target field identifier   |
| attachment    | [TableAttachment](/guide/script/model.md#tableattachment) | Attachment object           |

#### Return Value

Attachment object after successful move, type is [TableAttachment](/guide/script/model.md#tableattachment)

**_Example_**

```javascript
var record = informat.table.queryById("task", "cyrzgschwivz1");
informat.table.moveAttachment("task", "attachment", "task2", "attachment", record.attachment);
```

## createAttachment

Create an attachment from a file in the local sandbox
Upload a file from the local sandbox to shared storage and generate a [TableAttachment](/guide/script/model.md#tableattachment) object. If the file is an image type, the system will automatically generate a thumbnail.
If there are watermark settings in the attachment configuration, the system will automatically generate a watermark.


```javascript
informat.table.createAttachment(tableId, fieldId, path);
```

| Parameter    | Type   | Description                 |
| ------- | ------ | -------------------- |
| tableId | String | Data table identifier       |
| fieldId | String | Attachment field identifier     |
| path    | String | File path in the local sandbox |

#### Return Value

Attachment field after successful creation, type is [TableAttachment](/guide/script/model.md#tableattachment)

**_Example_**

Download an image from a URL, save it to a local sandbox file, then create an attachment from the local sandbox file, and save it to the attachment field of a record in the staffs table

The staffs table has an attachment field

| Field Identifier | Type | Description |
| ---------- | ---- | ---- |
| attachment | Attachment | Multi-select |

```javascript
const req = {
  url: "https://www.informat.cn/favicon.ico",
};
const rsp = informat.http.request(req);
//Save to local sandbox
rsp.saveBodyAsFile("tmp/demo.png");
var attachment = informat.table.createAttachment("staffs", "attachment", "tmp/demo.png");
//Update the attachment field of the data table record
informat.table.update("staffs", {
  id: "yhg8b23ej2gt6",
  attachment: [attachment], //Because the attachment field is multi-select, use an array here; similarly, if not multi-select, no array is needed
});
//Delete the local file
informat.file.delete("tmp/demo.png");
```

## createAttachmentStorage

Create an attachment from a file in remote storage
Copy a file from remote storage as the value of an attachment field. If it is an image type, no thumbnail will be generated; the thumbnail value will be the same as the attachment value.
This operation will also not generate a watermark.

```javascript
informat.table.createAttachmentStorage(tableId, fieldId, path);
```

| Parameter    | Type   | Description                 |
| ------- | ------ | -------------------- |
| tableId | String | Data table identifier       |
| fieldId | String | Attachment field identifier     |
| path    | String | File path in remote storage |

#### Return Value

Attachment field after successful creation, type is [TableAttachment](/guide/script/model.md#tableattachment)

**_Example_**

Download an image from a URL, save it to shared storage, then create an attachment from the file in remote storage, and save it to the attachment field of a record in the staffs table

The staffs table has an attachment field

| Field Identifier | Type | Description |
| ---------- | ---- | ---- |
| attachment | Attachment | Multi-select |

```javascript
const req = {
  url: "https://www.informat.cn/favicon.ico",
};
const rsp = informat.http.request(req);
//Save to remote storage
rsp.saveBodyAsStorage("remote/demo.png");
var attachment = informat.table.createAttachmentStorage("staffs", "attachment", "remote/demo.png");
//Update the attachment field of the data table record
informat.table.update("staffs", {
  id: "lc44f3lfggnbb",
  attachment: [attachment], //Because the attachment field is multi-select, use an array here; similarly, if not multi-select, no array is needed
});
//Delete the local file
informat.file.delete("tmp/demo.png");
```

## cloneTableSignature

Copy handwritten signature field files to a target field
Copy files from a source data table's handwritten signature field to a target table's handwritten signature field.

```javascript
informat.table.cloneTableSignature(sourceTableId, sourceFieldId, targetTableId, targetFieldId, signature);
```

| Parameter          | Type                                                    | Description               |
| ------------- | ------------------------------------------------------- | ------------------ |
| sourceTableId | String                                                  | Source data table identifier   |
| sourceFieldId | String                                                  | Source field identifier     |
| targetTableId | String                                                  | Target data table identifier |
| targetFieldId | String                                                  | Target field identifier   |
| signature     | [TableSignature](/guide/script/model.md#tablesignature) | Handwritten signature object       |

#### Return Value

Handwritten signature after successful copy, type is [TableSignature](/guide/script/model.md#tablesignature)

**_Example_**

Upload a handwritten signature to a custom form via automation, then copy the handwritten signature attachment from the custom form to the handwritten signature field of a record in the staffs table.

Custom form data table identifier: $Automatic_b0qt6ci821n2m_nuxfjrga56kj
The custom form data table has a handwritten signature field (single-select)
The staffs table has a handwritten signature field (single-select)

| Field Identifier | Type | Description |
| ---------- | ---- | ---- |
| signature  | Signature | Single-select |

```javascript
let signature = informat.table.cloneTableSignature("$Automatic_b0qt6ci821n2m_nuxfjrga56kj", "signature", "staffs", "signature", form.signature);
informat.table.update("staffs", {
  id: "yhg8b23ej2gt6",
  signature: signature,
});
```

## refreshDataSource

Refresh materialized view data
When the data source is from a `Database View` and the materialized view option is enabled, this will refresh the materialized view data. In other cases, an exception will be thrown.

```javascript
informat.table.refreshDataSource(tableId);
```

| Parameter    | Type   | Description           |
| ------- | ------ | -------------- |
| tableId | String | Data table identifier |

**_Example_**

```javascript
informat.table.refreshDataSource("techStaffsView");
```

## refreshRelationRollup

Recalculate the value of a relation list rollup field

```javascript
informat.table.refreshRelationRollup(tableId, fieldId, recordIdList);
```

| Parameter         | Type   | Description                                        |
| ------------ | ------ | ------------------------------------------- |
| tableId      | String | Data table identifier                                |
| fieldId      | String | Relation list rollup field identifier                      |
| recordIdList | String | Main table record ID list. If empty, recalculates for the entire table |

**_Example_**

```javascript
informat.table.refreshRelationRollup("staffs", "rewardCount", null); //Recalculate all records
informat.table.refreshRelationRollup("staffs", "rewardCount", ["yhg8b23ej2gt6"]); //Only recalculate rollup data for yhg8b23ej2gt6
```

## refreshLookupRollup

Recalculate the value of a lookup rollup field

```javascript
informat.table.refreshLookupRollup(tableId, fieldId, recordIdList, subFilter);
```

| Parameter         | Type                                    | Description                                        |
| ------------ | --------------------------------------- | ------------------------------------------- |
| tableId      | String                                  | Data table identifier                                |
| fieldId      | String                                  | Lookup rollup field identifier                      |
| recordIdList | `Array<String>`                         | Main table record ID list. If empty, recalculates for the entire table |
| subFilter    | [Filter](/guide/script/model.md#filter) | Sub-table filter criteria, can be null                       |

**_Example_**

```javascript
informat.table.refreshLookupRollup("staffs", "totalLevelDays", null, null); //Recalculate all records
informat.table.refreshLookupRollup("staffs", "totalLevelDays", ["yhg8b23ej2gt6"], null); //Only recalculate yhg8b23ej2gt6
```

## queryChangeLogListCount

Get the total count of change logs

```javascript
informat.table.queryChangeLogListCount(tableId, filter);
```

| Parameter    | Type                                    | Description         |
| ------- | --------------------------------------- | ------------ |
| tableId | String                                  | Data table identifier |
| filter  | [Filter](/guide/script/model.md#filter) | Filter criteria     |

Fields available in the filter

| Field         | Type    | Description        |
| ------------ | ------- | ----------- |
| id           | Integer | Change log ID |
| fieldName    | String  | Field name    |
| recordId     | String  | Record ID     |
| createUserId | String  | Creator ID   |

**Return Value**
Type is `Integer`
Returns the change log count

**Example**

```javascript
const count = informat.table.queryChangeLogListCount("tableKey", {
  conditionList: [
    {
      fieldId: "recordId",
      opt: "eq",
      value: "gn43hedzzgztp",
    },
  ],
});
// Get the matching count
console.log("count:", count);
```

## queryChangeLogList

Get the change log list

```javascript
informat.table.queryChangeLogList(tableId, informatQuery);
```

| Parameter          | Type                                  | Description         |
| ------------- | ------------------------------------- | ------------ |
| tableId       | String                                | Data table identifier |
| informatQuery | [Query](/guide/script/model.md#query) | Query criteria     |

Fields available in the filter

| Field         | Type    | Description        |
| ------------ | ------- | ----------- |
| id           | Integer | Change log ID |
| fieldName    | String  | Field name    |
| recordId     | String  | Record ID     |
| createUserId | String  | Creator ID   |

**Return Value**
Type is Array<[TableChangeLog](/guide/script/model.md#tablechangelog)>
Returns the change log list

**Example**

:::code-group

```js
informat.table.queryChangeLogList("staffs", {
  pageIndex: 1,
  pageSize: 20,
  filter: {
    conditionList: [
      {
        fieldId: "recordId",
        opt: "eq",
        value: "yhg8b23ej2gt6",
      },
    ],
  },
});
```

```json
[
  {
    "afterValue": {
      "type": "RelationRecord",
      "value": "fh1snm1k18kqc",
      "multiple": false,
      "valueString": "销售部"
    },
    "beforeValue": {
      "type": "RelationRecord",
      "multiple": false
    },
    "fieldName": "所在部门",
    "id": "1",
    "recordId": "yhg8b23ej2gt6"
  }
]
```

:::

## queryCommentListCount

Get the total count of form comments

```javascript
informat.table.queryCommentListCount(tableId, filter);
```

| Parameter    | Type                                    | Description         |
| ------- | --------------------------------------- | ------------ |
| tableId | String                                  | Data table identifier |
| filter  | [Filter](/guide/script/model.md#filter) | Filter criteria     |

Fields available in the filter

| Field         | Type    | Description        |
| ------------ | ------- | ----------- |
| id           | int     | Comment ID     |
| comment      | String  | Comment content    |
| isDeleted    | Boolean | Whether deleted    |
| parentId     | Integer | Reply comment ID |
| recordId     | String  | Record ID     |
| createUserId | String  | Creator ID   |

**Return Value**
Type is `Intetger`
Returns the form comment count

**Example**
:::code-group

```js
informat.table.queryCommentListCount("staffs", {
  conditionList: [
    {
      fieldId: "recordId",
      opt: "eq",
      value: "yhg8b23ej2gt6",
    },
  ],
});
```

```json
1
```

:::

## queryCommentList

Get the form comment list

```javascript
informat.table.queryCommentList(tableId, query);
```

| Parameter    | Type                                  | Description         |
| ------- | ------------------------------------- | ------------ |
| tableId | String                                | Data table identifier |
| query   | [Query](/guide/script/model.md#query) | Query criteria     |

Fields available in the filter

| Field         | Type    | Description        |
| ------------ | ------- | ----------- |
| id           | int     | Comment ID     |
| comment      | String  | Comment content    |
| isDeleted    | Boolean | Whether deleted    |
| parentId     | Integer | Reply comment ID |
| recordId     | String  | Record ID     |
| createUserId | String  | Creator ID   |

**Return Value**
Type is Array<[TableComment](/guide/script/model.md#tablecomment)>
Returns the form comment list

**Example**

:::code-group

```js
informat.table.queryCommentList("staffs", {
  pageIndex: 1,
  pageSize: 20,
  filter: {
    conditionList: [
      {
        fieldId: "recordId",
        opt: "eq",
        value: "yhg8b23ej2gt6",
      },
    ],
  },
});
```

```json
[
  {
    "comment": "{\"type\":\"doc\",\"content\":[{\"type\":\"paragraph\",\"content\":[{\"text\":\"挺好的\",\"type\":\"text\"}]}]}",
    "createTime": 1717728322411,
    "createUserAvatar": "79a487eb7f384321bfaed16eb9e020d8.jpg",
    "createUserId": "skydu",
    "createUserName": "杜展扬",
    "delete": false,
    "id": 1,
    "isDelete": false,
    "parentId": 0,
    "recordId": "yhg8b23ej2gt6"
  }
]
```

:::

## addComment

Add a form comment

```javascript
informat.table.addComment(tableId, tableComment);
```

| Parameter         | Type                                                        | Description         |
| ------------ | ----------------------------------------------------------- | ------------ |
| tableId      | String                                                      | Data table identifier |
| tableComment | [TableCommentForm](/guide/script/model.md#tablecommentform) | Form comment     |

**Return Value**
Type is `Integer`
Returns the newly added ID

**Comment Example**

:::code-group

```js
informat.table.addComment("staffs", {
  recordId: "yhg8b23ej2gt6",
  content: "评论内容",
  createUserId: "skydu", //Optional
});
```

```json
2
```

:::

**Reply Comment Example**

:::code-group

```js
informat.table.addComment("staffs", {
  recordId: "yhg8b23ej2gt6",
  parentId: 2, // Optional
  content: "回复上一条评论",
  createUserId: "skydu", //Optional
});
```

```json
3
```

:::

## deleteComment

Delete a form comment
:::tip
If the comment has replies, it will be soft deleted; otherwise it will be physically deleted.
If the comment does not exist, a "comment not found" error will be thrown.
:::

```javascript
informat.table.deleteComment(tableId, commentId);
```

| Parameter      | Type    | Description         |
| --------- | ------- | ------------ |
| tableId   | String  | Data table identifier |
| commentId | Integer | Form comment ID  |

**Example**

```javascript
informat.table.deleteComment("staffs", 3);
```

## getIdFieldSeq

Query the current auto-increment sequence number of a number field

```javascript
informat.table.getIdFieldSeq(tableId, fieldId);
```

| Parameter    | Type   | Description           |
| ------- | ------ | -------------- |
| tableId | String | Data table identifier   |
| fieldId | String | Number field identifier |

**Return Value**
Type is `Integer`
Returns the current auto-increment sequence number

**Example**

:::code-group

```js
informat.table.getIdFieldSeq("task", "number");
```

```js[Return Value]
2
```

:::

## setIdFieldSeq

Set the auto-increment sequence number of a number field

```javascript
informat.table.setIdFieldSeq(tableId, fieldId, seq);
```

| Parameter    | Type    | Description           |
| ------- | ------- | -------------- |
| tableId | String  | Data table identifier   |
| fieldId | String  | Number field identifier |
| seq     | Integer | Auto-increment sequence number       |

**Example**

```javascript
informat.table.setIdFieldSeq("staffs", "staffNo", 10);
```

## updateRecordSeq

Update the sort sequence number of a data table record

```javascript
informat.table.updateRecordSeq(tableId, recordId, seq);
```

| Parameter     | Type    | Description          |
| -------- | ------- | ------------- |
| tableId  | String  | Data table identifier  |
| recordId | String  | Data table record ID |
| seq      | Integer | New sort sequence number  |

**Example**

```javascript
informat.table.updateRecordSeq("staffs", "yhg8b23ej2gt6", 101);
```

## moveRecord

Move a record
:::tip
After moving, seq will be recalculated in order
:::

```javascript
informat.table.moveRecord(tableId, recordId, targetRecordId, type);
```

| Parameter           | Type   | Description                                                                                           |
| -------------- | ------ | ---------------------------------------------------------------------------------------------- |
| tableId        | String | Data table identifier                                                                                   |
| recordId       | String | Record ID                                                                                        |
| targetRecordId | String | Target record ID                                                                                    |
| type           | String | Drag mode. Available values:<br />before: Move the record before the target record<br />after: Move the record after the target record |

**Example**

```javascript
informat.table.moveRecord("task", "ksrhoqarae7hj", "dvmdfh74m0s2w", "before");
```

## moveTreeViewRecord

Move a record in tree view

```javascript
informat.table.moveTreeViewRecord(tableId, childrenFieldId, recordId, parentRecordId, targetRecordId, type);
```

| Parameter            | Type   | Description                                                                                                                   |
| --------------- | ------ | ---------------------------------------------------------------------------------------------------------------------- |
| tableId         | String | Data table identifier                                                                                                           |
| childrenFieldId | String | Child object field                                                                                                             |
| recordId        | String | Record ID                                                                                                                |
| parentRecordId  | String | Parent object record ID. Not needed if moving within the same level                                                                           |
| targetRecordId  | String | Target record ID                                                                                                            |
| type            | String | Drag mode. Available values:<br />before: Move the record before the target record<br />after: Move the record after the target record<br />inner: Inside the parent object |

**Example 1 - Move a record within the same level**

```javascript
informat.table.moveTreeViewRecord("staffsDept", "children", "l8w9u9raftp2a", null, "pz9y1fse8hccw", "before");
```

**Example 2 - Drag a record to a new parent record**

```javascript
informat.table.moveTreeViewRecord("staffsDept", "children", "l8w9u9raftp2a", "fh1snm1k18kqc", "u3lma96ibq52h", "before");
```

## moveLookupFieldRecord

Move a record within a lookup list field

```javascript
informat.table.moveLookupFieldRecord(tableId, lookupFieldId, mainRecordId, recordId, targetRecordId, type);
```

| Parameter           | Type   | Description                                                                                           |
| -------------- | ------ | ---------------------------------------------------------------------------------------------- |
| tableId        | String | Data table identifier                                                                                   |
| lookupFieldId  | String | Lookup list field                                                                                   |
| mainRecordId   | String | Main table record ID                                                                                    |
| recordId       | String | Sub-table record ID                                                                                    |
| targetRecordId | String | Sub-table target record ID                                                                                |
| type           | String | Drag mode. Available values:<br />before: Move the record before the target record<br />after: Move the record after the target record |

**Example**

```javascript
informat.table.moveLookupFieldRecord("staffs", "leaveLogRel", "yhg8b23ej2gt6", "p54xumqba4kmm", "vdbt9kk1cugvy", "before");
```

## moveRelationFieldRecord

Move a record within a relation list field

```javascript
informat.table.moveRelationFieldRecord(tableId, relationFieldId, mainRecordId, recordId, targetRecordId, type);
```

| Parameter            | Type   | Description                                                                                           |
| --------------- | ------ | ---------------------------------------------------------------------------------------------- |
| tableId         | String | Data table identifier                                                                                   |
| relationFieldId | String | Relation list field                                                                                   |
| mainRecordId    | String | Main table record ID                                                                                    |
| recordId        | String | Sub-table record ID                                                                                    |
| targetRecordId  | String | Sub-table target record ID                                                                                |
| type            | String | Drag mode. Available values:<br />before: Move the record before the target record<br />after: Move the record after the target record |

**Example**

```javascript
informat.table.moveRelationFieldRecord("staffs", "rewardList", "yhg8b23ej2gt6", "vsf3lo6ryj6lc", "ct82dszf20s2u", "before");
```

## moveChildrenFieldRecord

Move a record within a child object field

```javascript
informat.table.moveChildrenFieldRecord(tableId, childrenFieldId, mainRecordId, recordId, targetRecordId, type);
```

| Parameter            | Type   | Description                                                                                           |
| --------------- | ------ | ---------------------------------------------------------------------------------------------- |
| tableId         | String | Data table identifier                                                                                   |
| childrenFieldId | String | Child object field                                                                                     |
| mainRecordId    | String | Main table record ID                                                                                    |
| recordId        | String | Sub-table record ID                                                                                    |
| targetRecordId  | String | Sub-table target record ID                                                                                |
| type            | String | Drag mode. Available values:<br />before: Move the record before the target record<br />after: Move the record after the target record |

**Example**

```javascript
informat.table.moveChildrenFieldRecord("staffsDept", "children", "rpev2ztqnbu8o", "l8w9u9raftp2a", "pz9y1fse8hccw", "before");
```

## moveLookupFieldTreeViewRecord

Move a record in tree view within a lookup list field

```javascript
informat.table.moveLookupFieldTreeViewRecord(tableId, lookupFieldId, childrenFieldId, mainRecordId, recordId, parentRecordId, targetRecordId, type);
```

| Parameter            | Type   | Description                                                                                                                   |
| --------------- | ------ | ---------------------------------------------------------------------------------------------------------------------- |
| tableId         | String | Data table identifier                                                                                                           |
| lookupFieldId   | String | Lookup list field                                                                                                           |
| childrenFieldId | String | Child object field                                                                                                             |
| mainRecordId    | String | Main table record ID                                                                                                            |
| recordId        | String | Sub-table record ID                                                                                                            |
| parentRecordId  | String | Parent object record ID                                                                                                          |
| targetRecordId  | String | Sub-table target record ID                                                                                                        |
| type            | String | Drag mode. Available values:<br />before: Move the record before the target record<br />after: Move the record after the target record<br />inner: Inside the parent object |

**Example**

```javascript
informat.table.moveLookupFieldTreeViewRecord("lookup", "lookup_children", "children", "ozyqa05tj4xs0", "xim3193k04lu0", null, "pjrpekzh9gc2j", "before");
```

## moveRelationFieldTreeViewRecord

Move a record in tree view within a relation list field

```javascript
informat.table.moveRelationFieldTreeViewRecord(tableId, relationFieldId, childrenFieldId, mainRecordId, recordId, parentRecordId, targetRecordId, type);
```

| Parameter            | Type   | Description                                                                                                                   |
| --------------- | ------ | ---------------------------------------------------------------------------------------------------------------------- |
| tableId         | String | Data table identifier                                                                                                           |
| relationFieldId | String | Relation list field                                                                                                           |
| childrenFieldId | String | Child object field                                                                                                             |
| mainRecordId    | String | Main table record ID                                                                                                            |
| recordId        | String | Sub-table record ID                                                                                                            |
| parentRecordId  | String | Parent object record ID                                                                                                          |
| targetRecordId  | String | Sub-table target record ID                                                                                                        |
| type            | String | Drag mode. Available values:<br />before: Move the record before the target record<br />after: Move the record after the target record<br />inner: Inside the parent object |

**Example**

```javascript
informat.table.moveRelationFieldTreeViewRecord("relation", "relation_children", "children", "xzyqa35tj4xsq", "kim3193k54lu8", null, "fjrpekzh9gc6h", "before");
```

## moveChildrenFieldTreeViewRecord

Move a record in tree view within a child object field

```javascript
informat.table.moveChildrenFieldTreeViewRecord(tableId, mainChildrenFieldId, childrenFieldId, mainRecordId, recordId, parentRecordId, targetRecordId, type);
```

| Parameter                | Type   | Description                                                                                                                   |
| ------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------- |
| tableId             | String | Data table identifier                                                                                                           |
| mainChildrenFieldId | String | Child object field                                                                                                             |
| childrenFieldId     | String | Child object field                                                                                                             |
| mainRecordId        | String | Main table record ID                                                                                                            |
| recordId            | String | Sub-table record ID                                                                                                            |
| parentRecordId      | String | Parent object record ID                                                                                                          |
| targetRecordId      | String | Sub-table target record ID                                                                                                        |
| type                | String | Drag mode. Available values:<br />before: Move the record before the target record<br />after: Move the record after the target record<br />inner: Inside the parent object |

**Example**

```javascript
informat.table.moveChildrenFieldTreeViewRecord("children", "children_children", "children", "izyqa25tj4xsp", "iim3103k54lup", null, "ilrpekzh3gc2p", "before");
```

## refreshIndexNumber

Recalculate child object number

```javascript
informat.table.refreshIndexNumber(tableId, fieldId, parentRecordId);
```

| Parameter           | Type   | Description                                               |
| -------------- | ------ | -------------------------------------------------- |
| tableId        | String | Data table identifier                                       |
| fieldId        | String | Child object number field                                     |
| parentRecordId | String | Parent object record ID. Can be empty; when empty, recalculates all |

**Example**

```javascript
informat.table.refreshIndexNumber("staffsDept", "indexNumber", "rpev2ztqnbu8o"); //Recalculate child record list of the parent record
informat.table.refreshIndexNumber("staffsDept", "indexNumber", null);
```

## validateForm

Execute field validation rules to validate form data

```javascript
informat.table.validateForm(tableId, record);
```

| Parameter           | Type   | Description                                               |
| -------------- | ------ | -------------------------------------------------- |
| tableId        | String | Data table identifier                                       |
| record        | Object | Form record                                     |

**Example**

```javascript
let result=informat.table.validateForm("staffs", {
	age:-1
}); 
console.log(result);
```
Output
```json
{
  "itemList":[
    {
      "errorCode":270001,
      "errorMessage":"年龄不能小于等于0",
      "fieldId":"urx7djdqnp7mf",
      "fieldKey":"age",
      "fieldName":"年龄"
    }
  ]
}
```

## validateFormBySetting

Validate form data based on configuration

```javascript
informat.table.validateFormBySetting(tableId, record, setting);
```

| Parameter           | Type   | Description                                               |
| -------------- | ------ | -------------------------------------------------- |
| tableId        | String | Data table identifier                                       |
| record        | Object | Form record                                     |
| setting        | ValidateFormSetting | Configuration options                                     |


### ValidateFormSetting
Validation configuration
```ts
interface ValidateFormSetting {
	nullable:boolean;//Required field validation
	optionValue:boolean;//Option value range validation
	range:boolean;//Single text, multi-line text length; decimal and integer range validation
	validateRule:boolean;//Field validation rule validation
}
```

**Example 1**

```javascript
let result=informat.table.validateFormBySetting('staff',{'age':'1'},{'nullable':true})
console.log(result);
```
Output
```json
{
  "itemList":[
    {
      "errorCode":210204,
      "errorMessage":"字段值不能为空",
      "fieldId":"n05f9w24mu2y3",
      "fieldKey":"name",
      "fieldName":"姓名"
    }
  ]
}
```

**Example 2**

```javascript
let result=informat.table.validateFormBySetting('staff',{'salary':'100000'},{'range':true})
console.log(result);
```
Output
```json
{
  "itemList":[
    {
      "errorCode":210202,
      "errorMessage":"数据表【员工】字段【薪资】取值不在限定范围内 100000/50000",
      "fieldId":"p6vou466dq0xy",
      "fieldKey":"salary",
      "fieldName":"薪资"
    }
  ]
}
```

**Example 3**

```javascript
let result=informat.table.validateFormBySetting('staff',{'sex':'test'},{'optionValue':true})
console.log(result);
```
Output
```json
{
  "itemList":[
    {
      "errorCode":210205,
      "errorMessage":"字段值不在选项范围内",
      "fieldId":"jxky9knv40ikm",
      "fieldKey":"sex",
      "fieldName":"性别"
    }
  ]
}
```
