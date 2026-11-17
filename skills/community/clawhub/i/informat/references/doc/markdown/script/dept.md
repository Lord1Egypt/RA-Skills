# informat.dept Department Organization Operations

## Overview

Use the `informat.dept` object to perform department-related operations

## queryDeptList

Query department list

```javascript
informat.dept.queryDeptList(query)
```

| Parameter | Type                                  | Description     |
|-----------|---------------------------------------|-----------------|
| query     | [Query](/guide/script/model.md#query) | Query condition |

**Return Value**

Type Array<[Department](/guide/script/model.md#department)>
Returns the department list

**Example 1: Query departments whose name contains "R&D"**

::: code-group

```javascript [Call]
informat.dept.queryDeptList({
    pageSize: -1,
    filter: {
        conditionList: [
            { "fieldId": "name", "opt": "contains", "value": "研发" }
        ]
    }
});
```

```json [Return Value]
[
  {
    "id": "yanfabu",
    "name": "研发部",
    "parentId": "root",
    "remark": "负责研究和开发新产品、技术或服务的部门",
    "rowNumber": 2,
    "shortName": "研发部"
  },
  {
    "id": "yanfa1zu",
    "name": "研发1组",
    "parentId": "yanfabu",
    "remark": "",
    "rowNumber": 1,
    "shortName": "研发1组"
  },
  {
    "id": "yanfa2zu",
    "name": "研发2组",
    "parentId": "yanfabu",
    "remark": "",
    "rowNumber": 2,
    "shortName": "研发2组"
  }
]
```

:::

**Example 2: Query sub-departments under the R&D department (non-recursive)**

::: code-group

```javascript [Call]
informat.dept.queryDeptList({
    pageSize: -1,
    filter: {
        conditionList: [
            { "fieldId": "parentId", "opt": "eq", "value": "yanfabu" }
        ]
    }
});
```

```json [Return Value]
[
  {
    "id": "yanfa1zu",
    "name": "研发1组",
    "parentId": "yanfabu",
    "remark": "",
    "rowNumber": 1,
    "shortName": "研发1组"
  },
  {
    "id": "yanfa2zu",
    "name": "研发2组",
    "parentId": "yanfabu",
    "remark": "",
    "rowNumber": 2,
    "shortName": "研发2组"
  }
]
```

:::

## queryDeptListCount

Query department list count

```javascript
informat.dept.queryDeptListCount(filter)
```

| Parameter | Type                                    | Description     |
|-----------|-----------------------------------------|-----------------|
| filter    | [Filter](/guide/script/model.md#filter) | Query condition |

**Return Value**

Type `Integer`
Returns the total count of departments

**Example**

::: code-group

```javascript [Call]
informat.dept.queryDeptListCount({
    conditionList: [
        { "fieldId": "name", "opt": "contains", "value": "研发" }
    ]
});
```

```text [Return Value]
1
```

:::

## getDept

Query department information

```javascript
informat.dept.getDept(id)
```

| Parameter | Type   | Description       |
|-----------|--------|-------------------|
| id        | String | Department identifier |

**Return Value**
Type [Department](/guide/script/model.md#department)
Returns department information, or `null` if the department does not exist

**Example**

::: code-group

```javascript [Call]
informat.dept.getDept('yanfabu');
```

```json [Return Value]
{
  "id": "yanfabu",
  "name": "研发部",
  "parentId": "root",
  "remark": "负责研究和开发新产品、技术或服务的部门",
  "rowNumber": 2,
  "shortName": "研发部"
}
```

:::

## getParentOfDept

Query all parent departments of a department

```javascript
informat.dept.getParentOfDept(deptId)
```

| Parameter | Type     | Description       |
|-----------|----------|-------------------|
| deptId    | `String` | Department identifier |

**Return Value**
Type Array<[Department](/guide/script/model.md#department)>
Returns the list of parent departments

**Example**

::: code-group

```javascript [Call]
informat.dept.getParentOfDept('yanfabu');
```

```json [Return Value]
[
  {
    "id": "root",
    "name": "INFORMAT",
    "rowNumber": 1
  }
]
```

:::

## getChildrenOfDept

Query all sub-departments

```javascript
informat.dept.getChildrenOfDept(deptId)
```

| Parameter | Type     | Description       |
|-----------|----------|-------------------|
| deptId    | `String` | Department identifier |

**Return Value**
Type Array<[Department](/guide/script/model.md#department)>
Returns all sub-departments

**Example**

::: code-group

```javascript [Call]
informat.dept.getChildrenOfDept('yanfabu');
```

```json [Return Value]
[
  {
    "id": "yanfa1",
    "name": "研发1组",
    "parentId": "yanfabu",
    "rowNumber": 1
  },
  {
    "id": "yanfa2",
    "name": "研发2组",
    "parentId": "yanfabu",
    "rowNumber": 2
  }
]
```

:::

## getDirectChildrenOfDept

Query direct sub-departments

```javascript
informat.dept.getDirectChildrenOfDept(deptId)
```

| Parameter | Type     | Description       |
|-----------|----------|-------------------|
| deptId    | `String` | Department identifier |

**Return Value**

Type Array<[Department](/guide/script/model.md#department)>
Returns direct sub-departments

**Example**

::: code-group

```javascript [Call]
informat.dept.getDirectChildrenOfDept('yanfabu');
```

```json [Return Value]
[
  {
    "id": "yanfa1",
    "name": "研发1组",
    "parentId": "yanfabu",
    "rowNumber": 1
  },
  {
    "id": "yanfa2",
    "name": "研发2组",
    "parentId": "yanfabu",
    "rowNumber": 2
  }
]
```

:::

## addDept

Add a department

```javascript
informat.dept.addDept(dept)
```

| Parameter | Type                                              | Description          |
|-----------|---------------------------------------------------|----------------------|
| dept      | [Department](/guide/script/model.md#department)   | Department information |

**Return Value**

Type `String`
Returns the identifier of the newly added department

**Example**

```javascript
informat.dept.addDept({
    'id': 'yanfabu',
    'name': '研究开发部',
    'shortName': '研发部',
    'parentId': 'root',
    'ownerList': ['zhangsan'],
    'remark': '负责研究和开发新产品、技术或服务的部门'
});
```

## updateDept

Update a department

```javascript
informat.dept.updateDept(dept)
```

| Parameter | Type                                              | Description |
|-----------|---------------------------------------------------|-------------|
| dept      | [Department](/guide/script/model.md#department)   | Department  |

**Example**

```javascript
informat.dept.updateDept({
    'id': 'yanfabu',
    'name': '研究开发部',
    'shortName': '研发部',
    'parentId': 'root',
    'ownerList': ['zhangsan', 'lisi'],
    'remark': '负责研究和开发新产品、技术或服务的部门'
});
```

## deleteDept

Delete a department

```javascript
informat.dept.deleteDept(deptId)
```

| Parameter | Type     | Description       |
|-----------|----------|-------------------|
| deptId    | `String` | Department identifier |

**Example**

```javascript
informat.dept.deleteDept('yanfabu');
```
