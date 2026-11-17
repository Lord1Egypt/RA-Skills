# User

## Overview

User-related operation functions in the current system

## usersWithRole

Returns a list of users who have any one of the roles in roleIdList

```javascript
User.usersWithRole(roleIdList)
```

| Parameter | Type | Description |
|------------|-----------------|----------|
| roleIdList | `Array<String>` | Array of role identifiers |

**Return Value**

Type `Array<String>`
Array of user IDs who have any one of the roles in roleIdList

**Example**

```javascript
User.usersWithRole(['admin'])//[user1, user2, user3] 
```

## usersWithDepartment

Returns a list of users belonging to the departments in departmentIdList

```javascript
User.usersWithDepartment(departmentIdList)
```

| Parameter | Type | Description |
|------------|-----------------|---------|
| departmentIdList | `Array<String>` | Array of department identifiers |

**Return Value**

Type `Array<String>`
Returns a list of users belonging to the departments in departmentIdList

**Example**

```javascript
User.usersWithDepartment(['yanfabu'])
```

## superiorUsers

Returns the list of superiors for userId

```javascript
User.superiorUsers(userId)
```

| Parameter | Type | Description |
|--------|--------|------------|
| userId | `String` | User ID to query superiors for |

**Return Value**

Type `Array<String>`
List of IDs of the user's superiors

**Example**

```javascript
User.superiorUsers('user1')//[user2,user3] 
```

## superiorUsersWithLevel

Returns the list of consecutive superiors for userId

```javascript
User.superiorUsersWithLevel(userId,level)
```

| Parameter | Type | Description |
|--------|-----------|------------|
| userId | `String`  | User ID to query superiors for |
| level | `Integer` | Number of superior levels to query |

**Return Value**

Type `Array<String>`
List of IDs of the user's superiors

**Example**

```javascript
User.superiorUsersWithLevel(Context.userId(),1)
```

## subordinateUsers

Returns the list of subordinates for userId

```javascript
User.subordinateUsers(userId)
```

| Parameter | Type | Description |
|--------|--------|------------|
| userId | `String` | User ID to query subordinates for |

**Return Value**

Type `Array<String>`
List of IDs of the user's subordinates

**Example**

```javascript
User.subordinateUsers('user1')//[user2,user3] 
```

## subordinateUsersWithLevel

Returns the list of consecutive subordinates for userId

```javascript
User.subordinateUsersWithLevel(userId, level)
```

| Parameter | Type | Description |
|--------|--------|------------|
| userId | `String` | User ID to query subordinates for |
| level | `Integer` | Number of levels |

**Return Value**

Type `Array<String>`
List of IDs of the user's subordinates

**Example**

```javascript
User.subordinateUsersWithLevel('user1',2)//[user2,user3] 
```

## leaderOfDept

Returns the list of leaders for a single department

```javascript
User.leaderOfDept(departmentId)
```

| Parameter | Type | Description |
|--------------|--------|------|
| departmentId | `String` | Department ID |

**Return Value**

Type `Array<String>`
List of user IDs of department leaders

**Example**

```javascript
User.leaderOfDept('dept1')//[user2,user3] 
```

## leaderOfDeptWithLevel

Returns the list of leaders of consecutive parent departments

```javascript
User.leaderOfDeptWithLevel(departmentId,level)
```

| Parameter | Type | Description |
|--------------|--------|------|
| departmentId | `String` | Department ID |
| level | `Integer` | Number of parent levels to query |

**Return Value**

Type `Array<String>`
Returns the list of leaders of consecutive parent departments

**Example**

```javascript
User.leaderOfDeptWithLevel('yanfabu',1)
```

## leaderOfDeptList

Returns the list of leaders for multiple departments

```javascript
User.leaderOfDeptList(departmentIdList)
```

| Parameter | Type | Description |
|------------------|---------------|--------|
| departmentIdList | `Array<String>` | List of department IDs |

**Return Value**

Type `Array<String>`
List of user IDs of department leaders

**Example**

```javascript
User.leaderOfDeptList(['dept1', 'dept2'])//[user2,user3,user4] 
```



## parentOfDept

Returns the parent department ID of a department

```javascript
User.parentOfDept(departmentId)
```

| Parameter | Type | Description |
|--------------|--------|------|
| departmentId | `String` | Department ID |

**Return Value**

Type `String`
Parent department ID

**Example**

```javascript
User.parentOfDept('dept1')//dept2 
```

## parentOfDeptList

Returns the list of parent department IDs

```javascript
User.parentOfDeptList(departmentId)
```

| Parameter | Type | Description |
|--------------|--------|------|
| departmentId | `String` | Department ID |

**Return Value**

Type `Array<String>`
List of parent department IDs

**Example**

```javascript
User.parentOfDept('dept1')//['dept2','dept3'] 
```



## childrenOfDept

Returns the list of all sub-departments of a single department

The department structure is tree-shaped. This API will recursively return all child nodes in the tree structure under the specified department.

```javascript
User.childrenOfDept(departmentId)
```

| Parameter | Type | Description |
|--------------|--------|------|
| departmentId | `String` | Department ID |

**Return Value**

Type `Array<String>`
List of child department IDs

**Example**

```javascript
User.childrenOfDept('dept1')//[dept2,dept3] 
```



## childrenOfDeptList

Returns the list of all sub-departments for multiple departments

```javascript
User.childrenOfDeptList(departmentList)
```

| Parameter | Type | Description |
|----------------|---------------|--------|
| departmentList | `Array<String>` | List of department IDs |

**Return Value**

Type `Array<String>`
List of child department IDs

**Example**

```javascript
User.childrenOfDeptList(['dept1', 'dept2'])//[dept2,dept3] 
```



## directChildrenOfDept

Returns the list of direct child departments

```javascript
User.directChildrenOfDept(departmentId)
```

| Parameter | Type | Description |
|--------------|--------|------|
| departmentId | `String` | Department ID |

**Return Value**

Type `Array<String>`
List of child department IDs

**Example**

```javascript
User.directChildrenOfDept('dept1')//[dept2] 
```



## user

Returns user information

```javascript
User.user(userId)
```

| Parameter | Type | Description |
|--------|--------|------|
| userId | `String` | User ID |

**Return Value**

Type [`User`](../script/model.html#user)

**Example**

:::: tabs
::: tab Call
```javascript
User.user(Context.userId())
```
:::

::: tab Return Value
```json
{
  "avatar": "pic10.png",
  "companyRoleList": [
    "designer",
    "admin"
  ],
  "departmentList": [
    "dev"
  ],
  "id": "zhangsan",
  "leaderList": [],
  "name": "张三",
  "roleList": [
    "admin"
  ],
  "userName": "zhangsan"
}
```
:::

::::


## userInfo

Returns user information

```javascript
User.userInfo(userId)
```

| Parameter | Type | Description |
|--------|--------|------|
| userId | `String` | User ID |

**Return Value**

Type [`UserInfo`](../script/model.html#userInfo)

**Example**
:::: tabs
::: tab Call
```javascript
User.userInfo(Context.userId())
```
:::

::: tab Return Value
```json
{
  "avatar": "pic10.png",
  "companyRoleList": [
    "designer",
    "admin"
  ],
  "departmentList": [
    "dev"
  ],
  "id": "zhangsan",
  "leaderList": [],
  "name": "张三",
  "roleList": [
    "admin"
  ],
  "userName": "zhangsan"
}
```
:::

::::




## userList

Returns a list of user information in batch

```javascript
User.userList(idList)
```

| Parameter | Type | Description |
|--------|-----------------|----------|
| idList | `Array<String>` | Array of user IDs |

**Return Value**

Type `Array<UserInfo>`

**Example**

```javascript
User.userList(['user1', 'user2'])
```

## deptList

Returns department information list for the departments in departmentIdList

```javascript
User.deptList(departmentIdList)
```

| Parameter | Type | Description |
|------------------|-----------------|--------|
| departmentIdList | `Array<String>` | List of department IDs |

**Return Value**

Type `Array<Dept>`

**Example**

```javascript
User.deptList(['dept1', 'dept2'])
```



## dept

Returns department information

```javascript
User.dept(deptId)
```

| Parameter | Type | Description |
|--------|--------|------|
| deptId | `String` | Department ID |

**Return Value**

Type `Dept`

**Example**

```javascript
User.dept('dept1')
```
