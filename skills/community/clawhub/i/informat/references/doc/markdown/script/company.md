# informat.company Team

## Overview

Use the `informat.company` object to perform team-related operations.

## getCompany

Query current team information

```javascript
informat.company.getCompany();
```

**Return Value**

Type is [Company](/guide/script/model.md#company), returns the team

**Example**

::: code-group

```javascript [Call]
informat.company.getCompany();
```
```json [Return Value]
{
  "createAccountId": "wcueuhi1ib6ul",
  "createTime": 1664196760747,
  "dbIndex": 0,
  "favicon": "0238219de8614a6a8a27db74d2dfc82a.jpg",
  "id": "g09aj7cus3d8s",
  "maxApplicationNum": 0,
  "maxUserNum": 10000,
  "name": "深圳交付团队UAT",
  "updateTime": 1683595804684,
  "version": "enterprise"
}
```
:::

## queryRoleList

Query team role list

```javascript
informat.company.queryRoleList()
```

**Return Value**

Type is Array<[Role](/guide/script/model.md#role)>, returns all roles

**Example**

::: code-group

```javascript [Call]
informat.company.queryRoleList()
```
```json [Return Value]
[
  {
    "admin": true,
    "createTime": 1664196760903,
    "id": "admin",
    "isAdmin": true,
    "name": "管理员",
    "permissionIds": []
  },
  {
    "admin": false,
    "createTime": 1664196760907,
    "id": "member",
    "isAdmin": false,
    "name": "成员",
    "permissionIds": [
      "InviteMember"
    ]
  },
  {
    "admin": false,
    "createTime": 1670301261933,
    "id": "supplier",
    "isAdmin": false,
    "name": "供应商",
    "permissionIds": [
      "InviteMember"
    ]
  }
]
```
:::

## addCompanyMember

Add an account to the team member list

```javascript
informat.company.addCompanyMember(accountId, departmentList, roleList)
```

::: tip Note
Adding an account to team members is limited by the team member count in the license. If the team member count exceeds the license limit, the addition will fail.
:::

| Parameter             | Type              | Description                        |
|----------------|-----------------|---------------------------|
| accountId      | `String`        | Account ID                      |
| departmentList | `Array<String>` | Department ID list. If the list is empty, the user will be added to the root department |
| roleList       | `Array<String>` | Role ID list                    |

**Example**

```javascript
informat.company.addCompanyMember('zhangsan', ['yanfabu'], ['tester']);
```

## deleteCompanyMember

Remove an account from team members

```javascript
informat.company.deleteCompanyMember(accountId)
```

| Parameter        | Type       | Description   |
|-----------|----------|------|
| accountId | `String` | Account ID |

**Return Value**

Type is `Boolean`, returns whether the removal was successful

**Example**

::: code-group

```javascript [Call]
informat.company.deleteCompanyMember('zhangsan');
```
```text [Return Value]
true
```
:::

## updateCompanyMember

Update a team member

```javascript
informat.company.updateCompanyMember(member)
```

| Parameter     | Type                                       | Description   |
|--------|------------------------------------------|------|
| member | [CompanyMember](/guide/script/model.md#companymember) | Team member |

**Example**

```javascript
informat.company.updateCompanyMember({
    id: 'zhangsan',
    departmentList: ['yanfabu', 'yunyingbu'],
    roleList: ['tester', 'devopser'],
    leaderList: ['lisi'],
    dingtalkUserId: 'zhangsan',
    weworkUserId: 'eobg38987',
    feishuUserId: 'ecbg46933',
});
```

## queryCompanyMemberList

Query team member list

```javascript
informat.company.queryCompanyMemberList(query)
```

| Parameter    | Type                               | Description     |
|-------|----------------------------------|--------|
| query | [Query](/guide/script/model.md#query) | Team member query criteria |

**Return Value**
Type Array<[CompanyMember](/guide/script/model.md#companymember)>, team member list

**Example**

::: code-group

```javascript [Call]
informat.company.queryCompanyMemberList({
	pageIndex:1,
	pageSize:100,
	filter:{
		conditionList:[{
			"fieldId":"weworkUserId",
			"opt":"isnull"
		}]
	}
});
```
```json [Return Value]
[
  {
    "createTime": 1700628322740,
    "departmentKeyList": [
      "root"
    ],
    "departmentList": [
      "acocdpvd8d6a6"
    ],
    "id": "zhangsan",
    "name": "张三",
    "rowNumber": 5,
    "updateTime": 1700820250268
  }
]
```
:::

## queryCompanyMemberListCount

Query team member list count

```javascript
informat.company.queryCompanyMemberListCount(filter)
```

| Parameter    | Type                                       | Description     |
|-------|------------------------------------------|--------|
| filter | [Filter](/guides/script/model.md#filter) | Team member query filter |

**Return Value**

Type is `Integer`, returns the total count of matches

**Example**

::: code-group

```javascript [Call]
informat.company.queryCompanyMemberListCount(
	{
		conditionList:[{
			"fieldId":"weworkUserId",
			"opt":"isnull"
		}]
	}
);
```
```text [Return Value]
2
```
:::

## queryAppGroupById

Query an application group by ID

```javascript
informat.company.queryAppGroupById(id)
```

| Parameter    | Type              | Description     |
|-------|-----------------|--------|
| id | `String` | Application group ID |


**Return Value**

Type is [AppGroup](/guide/script/model.md#appgroup), returns the application group

**Example**


::: code-group

```javascript [Call]
informat.company.queryAppGroupById('ruh8zp94ke3p0');
```
```json [Return Value]
{
  "createTime": 1700628428167,
  "id": "qvwfhdf328lex",
  "name": "演示（gitee上有链接，供客户安装）",
  "rowNumber": 1,
  "updateTime": 1717149133338
}
```
:::

## queryAppGroupList

Query application group list

```javascript
informat.company.queryAppGroupList(query)
```

| Parameter    | Type              | Description     |
|-------|-----------------|--------|
| query | [Query](/guide/script/model.md#query) | Query criteria |

**Return Value**

Type is Array<[AppGroup](/guide/script/model.md#appgroup)>, returns the application group list

**Example**

::: code-group

```javascript [Call]
informat.company.queryAppGroupList({
	pageIndex:1,
	pageSize:100,
	filter:{
		conditionList:[{
			"fieldId": "name",
			"opt":"isnotnull"
		}]
	}
});
```
```json [Return Value]
[
  {
    "createTime": 1717146091865,
    "id": "sjppghi7ofsci",
    "name": "⚠️案例-项目管理",
    "rowNumber": 5,
    "updateTime": 1717660920434
  },
  {
    "createTime": 1717660867337,
    "id": "mjeb7d6mnrsi7",
    "name": "⚠️案例-生产制造2",
    "rowNumber": 8,
    "updateTime": 1717660937343
  }
]
```
:::

## queryAppGroupListCount

Query application group list count

```javascript
informat.company.queryAppGroupListCount(filter)
```

| Parameter    | Type                                | Description     |
|-------|-----------------------------------|--------|
| filter | [Filter](/guide/script/model.md#filter) | Query filter |

**Return Value**

Type is `Integer`, returns the total count of matches

**Example**

::: code-group

```javascript [Call]
informat.company.queryAppGroupListCount({
      conditionList:[{
        "fieldId":"name",
        "opt":"contains",
        "value":"案例"
      }]
    }
)
```
```text [Return Value]
4
```
:::

## addAppGroup

Create an application group

```javascript
informat.company.addAppGroup(group);
```

| Parameter     | Type     | Description             |
| -------- | -------- | ---------------- |
| group | [AppGroup](/guide/script/model.md#appgroup) | Application group |

**Return Value**

Type `String`, ID of the newly created application group

**Example**

::: code-group

```javascript [Call]
informat.company.addAppGroup({
	'name':'测试分组'
});
```
```text [Return Value]
qunzjrmed162w
```
:::

## updateAppGroup

Edit an application group

```javascript
informat.company.updateAppGroup(group);
```

| Parameter     | Type     | Description             |
| -------- | -------- | ---------------- |
| group | [AppGroup](/guide/script/model.md#appgroup)| Application group |

**Return Value**

Type `Integer`, number of groups successfully edited

::: code-group

```javascript [Call]
informat.company.updateAppGroup({
	'id':'qunzjrmed162w',
	'name':'测试分组2'
})
```
```text [Return Value]
1
```
:::

## deleteAppGroup

Delete an application group

```javascript
informat.company.deleteAppGroup(id);
```
::: warning
Cannot delete a group that contains applications
:::


| Parameter     | Type     | Description             |
| -------- | -------- | ---------------- |
| id | `String` | Application group ID |

**Return Value**

Type is `Integer`, number of groups successfully deleted

**Example**

::: code-group

```javascript [Call]
informat.company.deleteAppGroup('qunzjrmed162w');
```
```text [Return Value]
1
```
:::

## queryAppList

Query application list

```javascript
informat.company.queryAppList(query)
```

| Parameter    | Type              | Description     |
|-------|-----------------|--------|
| query | [Query](/guide/script/model.md#query) | Query criteria |

**Return Value** 

Type is Array<[Application](/guide/script/model.md#app)>, returns the application list

**Example**

::: code-group

```javascript [Call]
informat.company.queryAppList({
	pageIndex:1,
	pageSize:100,
	filter:{
		conditionList:[{
			"fieldId":"name",
			"opt":"contains",
			"value":"测试"
		}]
	}
});
```
```json [Return Value]
[
  {
    "appDefineId": "com.mycompany",
    "color": "c7",
    "createAccountId": "zhangsan",
    "createTime": 1680006873433,
    "icon": "home",
    "id": "ftegr30w93jya",
    "name": "测试一下",
    "updateAccountId": "zhangsan",
    "updateTime": 1696919628896
  },
  {
    "appDefineId": "cn.informat.test",
    "color": "c1",
    "createAccountId": "zhangsan",
    "createTime": 1664258560997,
    "icon": "community",
    "id": "btz5tka89273q",
    "name": "全字段测试",
    "updateAccountId": "zhangsan",
    "updateTime": 1696919628886
  }
]
```
:::

## queryAppListCount

Query application list count

```javascript
informat.company.queryAppListCount(filter)
```

| Parameter    | Type              | Description     |
|-------|-----------------|--------|
| filter | [Filter](/guide/script/model.md#filter) | Query filter |

**Return Value**

Type is `Integer`, returns the total count of matches

**Example**

::: code-group

```javascript [Call]
informat.company.queryAppListCount(
	{
		conditionList:[{
			"fieldId":"name",
			"opt":"contains",
			"value":"测试"
		}]
	}
);
```
```text [Return Value]
2
```
:::

## installApp

Install an application

```javascript
informat.company.installApp(req);
```

| Parameter     | Type                                           | Description             |
| -------- |----------------------------------------------| ---------------- |
| req | [InstallAppRequest](/guide/script/model.md#installapprequest) | Installation information |

**Return Value**

Type is `String`, ID of the newly installed application

**Example**

::: code-group

```javascript [Call]
let company = informat.company.getCompany();
informat.company.installApp({
	'groupId': company.id,
	'imrUrl':'https://next.inforamt.cn/test.imr'
});
```
```text [Return Value]
uzafvisn1whcq
```
:::

## uninstallApp

Uninstall an application

```javascript
informat.company.uninstallApp(appId);
```

| Parameter     | Type     | Description             |
| -------- | -------- | ---------------- |
| appId | `String` | Application ID |


**Example**

```javascript
informat.company.uninstallApp('uzafvisn1whcq');
```

## getUserAppList

Query the list of applications accessible to a user

```javascript
informat.company.getUserAppList(accountId)
```

| Parameter    | Type              | Description     |
|-------|-----------------|--------|
| accountId | `String` | Account ID |

**Return Value** 

Type is [UserAppList](/guide/script/model.md#userapplist), returns the application list

**Example**

::: code-group

```javascript [Call]
informat.company.getUserAppList('zhangsan');
```
```json [Return Value]
{
	"appGroupList":[
		{
			"createTime":1737464180983,
			"id":"nj4h8ci8kjpsu",
			"name":"演示应用",
			"rowNumber":1,
			"updateTime":1738810011210
		},
		{
			"createTime":1717142070955,
			"id":"qdjpyk2iw8zzt",
			"name":"开发迭代",
			"rowNumber":2,
			"updateTime":1738810011216
		}
	],
	"appList":[
		{
			"appDefineBuild":920,
			"appDefineEditable":true,
			"appDefineId":"com.demo.srm",
			"appDefineVersion":"1.0",
			"color":"c1",
			"createAccountId":"lwfwqr67xsvup",
			"createTime":1725441476365,
			"enableAppJsonLog":false,
			"enableAppLog":false,
			"icon":"instance-fill",
			"id":"dvl8ig0j3odwh",
			"logLevel":"DEBUG",
			"name":"功能演示-供应商管理",
			"groupId":"nj4h8ci8kjpsu",
			"updateTime":1739861044583
		},
		{
			"appDefineBuild":54,
			"appDefineEditable":true,
			"appDefineId":"demoApp.pm",
			"appDefineVersion":"1.0",
			"color":"c2",
			"createTime":1725503438313,
			"enableAppJsonLog":false,
			"enableAppLog":false,
			"icon":"task",
			"id":"m4mfdpi5plchm",
			"logLevel":"DEBUG",
			"name":"功能演示-项目管理",
			"groupId":"nj4h8ci8kjpsu",
			"updateTime":1740559881456
		}
	]
}
```
:::
