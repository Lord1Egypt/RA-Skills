# informat.user User Operations

## Overview

Use the `informat.user` object to perform user information operations

***

## getUser

Query user information with getUser

```javascript
informat.user.getUser(id)
```

| Parameter | Type     | Description |
|----|--------|------|
| id | String | User ID |

**Return Value**
Type is [User](/guide/script/model.md#user)
Returns user information, or `null` if the user does not exist

Example:

:::code-group

```js[Call]
informat.user.getUser('zhangsan');
```

```json[Return Value]
{
  "avatar": "pic10.png",
  "companyRoleList": [
    "admin",
    "tester"
  ],
  "departmentList": [
    "yanfabu",
    "yunyingbu"
  ],
  "id": "zhangsan",
  "leaderList": [
    "lisi"
  ],
  "name": "张三",
  "roleList": [
    "tester",
    "admin"
  ],
  "userInfo": {
    "age": 20
  }
}
```

:::

## getUserInfo

Query detailed user information

```javascript
informat.user.getUserInfo(id)
```

| Parameter | Type     | Description |
|----|--------|------|
| id | String | User ID |

**Return Value**
Type is [UserInfo](/guide/script/model.md#userinfo)
Returns user information, or `null` if the user does not exist

Example:

:::code-group

```js[Call]
informat.user.getUserInfo('zhangsan');
```

```json[Return Value]
{
  "avatar": "pic10.png",
  "companyRoleList": [
    "admin",
    "tester"
  ],
  "departmentList": [
    "yanfabu",
    "yunyingbu"
  ],
  "email": "zhangsan@informat.cn",
  "id": "zhangsan",
  "leaderList": [
    "lisi"
  ],
  "mobileNo": "19900000000",
  "name": "张三",
  "roleList": [
    "tester",
    "admin"
  ],
  "userInfo": {
    "age": 20
  },
  "userName": "zhangsan"
}
```

:::

## getUserList

Query user list by user ID list
:::tip
List queries do not return user extended information
:::

```javascript
informat.user.getUserList(idList)
```

| Parameter | Type              | Description |
|--------|-----------------|--------|
| idList | `Array<String>` | User ID list |

**Return Value**
Type is Array<[User](/guide/script/model.md#user)>
Returns user list

Example:

:::code-group

```js[Call]
informat.user.getUserList(['zhangsan','lisi']);
```

```json[Return Value]
[
  {
    "avatar": "pic10.png",
    "companyRoleList": [
      "admin",
      "tester"
    ],
    "departmentList": [
      "yanfabu",
      "yunyingbu"
    ],
    "id": "zhangsan",
    "leaderList": [
      "lisi"
    ],
    "name": "张三",
    "roleList": [
      "tester",
      "admin"
    ]
  }
]
```

:::

## getAppUserList

Query application member list
:::tip
Note that user extended information is not returned here
:::

```javascript
informat.user.getAppUserList()
```

**Return Value**
Type is Array<[User](/guide/script/model.md#user)>
Returns application member list

Example:

:::code-group

```js[Call]
informat.user.getAppUserList();
```

```json[Return Value]
[
  {
    "avatar": "pic10.png",
    "companyRoleList": [
      "admin",
      "tester"
    ],
    "departmentList": [
      "yanfabu",
      "yunyingbu"
    ],
    "id": "zhangsan",
    "leaderList": [
      "lisi"
    ],
    "name": "张三",
    "roleList": [
      "admin"
    ]
  }
]
```

:::

## getUserByRoleList

Query user list by application roles
:::tip
Note that user extended information is not returned here
:::

```javascript
informat.user.getUserByRoleList(['admin'])
```

| Parameter | Type              | Description |
|----------|-----------------|-----------|
| roleList | `Array<String>` | Application role identifier list |

**Return Value**
Type is Array<[User](/guide/script/model.md#user)>
Returns user list

Example:

:::code-group

```js[Call]
informat.user.getUserByRoleList('admin');
```

```json[Return Value]
[
  {
    "avatar": "pic10.png",
    "companyRoleList": [
      "admin",
      "tester"
    ],
    "departmentList": [
      "yanfabu",
      "yunyingbu"
    ],
    "id": "zhangsan",
    "leaderList": [
      "lisi"
    ],
    "name": "张三",
    "roleList": [
      "admin"
    ]
  },
  {
    "avatar": "pic22.png",
    "companyRoleList": [
      "admin",
      "tester"
    ],
    "departmentList": [
      "yanfabu",
      "yunyingbu"
    ],
    "id": "lisi",
    "leaderList": [],
    "name": "李四",
    "roleList": [
      "admin"
    ]
  }
]
```

:::

## getUserByDeptList

Query user list by department

```javascript
informat.user.getUserByDeptList(deptList)
```

| Parameter | Type              | Description |
|----------|-----------------|---------|
| deptList | `Array<String>` | Department identifier list |

**Return Value**
Type is Array<[User](/guide/script/model.md#user)>
Returns user list

Example:

:::code-group

```javascript
informat.user.getUserByDeptList(['yanfabu', 'yunyingbu']); 
```

```json[Return Value]
[
  {
    "avatar": "pic10.png",
    "companyRoleList": [
      "admin",
      "tester"
    ],
    "departmentList": [
      "yanfabu",
      "yunyingbu"
    ],
    "id": "zhangsan",
    "leaderList": [
      "lisi"
    ],
    "name": "张三",
    "roleList": [
      "admin"
    ]
  }
]
```

:::

## getSuperiorUsers

Query a user's direct superiors

```javascript
informat.user.getSuperiorUsers(userId)
```

| Parameter | Type     | Description |
|--------|--------|------|
| userId | String | User ID |

**Return Value**
Type is Array<[User](/guide/script/model.md#user)>
Returns the user's superior list

Example:

:::code-group

```js[Call]
informat.user.getSuperiorUsers('zhangsan');
```

```json[Return Value]
[
  {
    "avatar": "pic22.png",
    "companyRoleList": [
      "admin",
      "tester"
    ],
    "departmentList": [
      "yanfabu",
      "yunyingbu"
    ],
    "id": "lisi",
    "leaderList": [],
    "name": "李四",
    "roleList": [
      "admin"
    ]
  }
]
```

:::

## getSubordinateUsers

Query a user's direct subordinates

```javascript
informat.user.getSubordinateUsers(userId)
```

| Parameter | Type     | Description |
|--------|--------|------|
| userId | String | User ID |

**Return Value**
Type is Array<[User](/guide/script/model.md#user)>
Returns the user's subordinate list

Example:

:::code-group

```js[Call]
informat.user.getSubordinateUsers('lisi');
```

```json[Return Value]
[
  {
    "avatar": "pic10.png",
    "companyRoleList": [
      "admin",
      "tester"
    ],
    "departmentList": [
      "yanfabu",
      "yunyingbu"
    ],
    "id": "zhangsan",
    "leaderList": [
      "lisi"
    ],
    "name": "张三",
    "roleList": [
      "tester",
      "admin"
    ]
  }
]
```

:::

## getLeaderOfDeptList

Query department leaders

```javascript
informat.user.getLeaderOfDeptList(deptList)
```

| Parameter | Type              | Description |
|----------|-----------------|--------|
| deptList | `Array<String>` | Department ID list |

**Return Value**
Type is Array<[User](/guide/script/model.md#user)>
Returns department leader list

Example:

:::code-group

```js[Call]
informat.user.getLeaderOfDeptList(['yunyingbu']);
```

```json[Return Value]
[
  {
    "avatar": "pic14.png",
    "companyRoleList": [
      "admin"
    ],
    "departmentList": [
      "yunyingbu"
    ],
    "id": "l4cntsd6j16qv",
    "leaderList": [],
    "name": "大熊",
    "roleList": []
  }
]
```

:::

## getUserRoleList

Query application role list

```javascript
informat.user.getUserRoleList()
```

**Return Value**
Type is Array<[UserRole](/guide/script/model.md#userrole)>
Returns all application role list

Example:

:::code-group

```js[Call]
informat.user.getUserRoleList();
```

```json[Return Value]
[
  {
    "admin": true,
    "id": "admin",
    "isAdmin": true,
    "name": "管理员",
    "permissionList": []
  },
  {
    "admin": false,
    "id": "hrManager",
    "isAdmin": false,
    "name": "HR",
    "permissionList": [
      "AppAccess",
      "AppMember",
      "gkxv4nq60zdwm",
      "task_taskCustomPermission"
    ]
  }
]
```

:::

## addUser

Add a user to the application

```javascript
informat.user.addUser(userId, roleList)
```

| Parameter | Type              | Description |
|----------|-----------------|--------|
| userId   | String          | User ID |
| roleList | `Array<String>` | Application role list |

Example: Add user zhangsan to the application and assign the admin and tester roles

```javascript
informat.user.addUser('zhangsan', ['admin', 'tester']);
```

## updateUserRole

Update an application member's roles

```javascript
informat.user.updateUserRole(userId, roleList)
```

| Parameter | Type              | Description |
|----------|-----------------|--------|
| userId   | String          | User ID |
| roleList | `Array<String>` | Application role list |

Example: Change user zhangsan's application role to tester

```javascript
informat.user.updateUserRole('zhangsan', ['tester']);
```

## deleteUser

Remove a user from the application

```javascript
informat.user.deleteUser(userId)
```

| Parameter | Type     | Description |
|--------|--------|------|
| userId | String | User ID |

Example: Remove user zhangsan from the application

```javascript
informat.user.deleteUser('zhangsan');
```

## getUserPermissions

Query all application permissions for a user

```javascript
informat.user.getUserPermissions(userId)
```

| Parameter | Type       | Description |
|--------|----------|------|
| userId | `String` | User ID |

**Return Value**
Type is `Array<String>`
Returns all application permission list for the user

Example: Query all application permissions for user zhangsan

```javascript
informat.user.getUserPermissions('zhangsan');
```

## getAllPermissions

Query all application permission definitions

```javascript
informat.user.getAllPermissions()
```

**Return Value**
Type is `Array<String>`
Returns all application permission definitions

Example: Query all application permission definitions

```javascript
informat.user.getAllPermissions();
```
