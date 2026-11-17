# informat.app Application Related Functions

## Overview

Use the `informat.app` object to perform global operations related to the application.

## abort

Terminate the current script execution

```javascript
informat.app.abort(message)
informat.app.abort(message, code)
```

**Parameters**

| Parameter | Type   | Description   |
|-----------|--------|---------------|
| message   | String | Alert message |
| code      | int    | Error code    |

**Return Value**

None

**Example**

```javascript
informat.app.abort('The project has already been initiated')
informat.app.abort('The project has already been initiated', 270001)
```

## appId

Query the current application ID

```javascript
informat.app.appId()
```

**Return Value**

Type is `String`, returns the current application ID

**Example**

::: code-group

```javascript [Call]
const appId = informat.app.appId();
console.log(appId);
```

```text [Return Value]
y2jtobhqycwxb
```

:::

## getAppIdByKey

Query the application ID under the team by application identifier

```javascript
informat.app.getAppIdByKey(key)
```

**Parameters**

| Parameter | Type   | Description          |
|-----------|--------|----------------------|
| key       | String | Application identifier |

**Return Value**

Type is `String`, returns the application ID

**Example**

::: code-group

```javascript [Call]
const appId = informat.app.getAppIdByKey('informat.example');
console.log(appId);
```

```text [Return Value]
y2jtobhqycwxb
```

:::

## getModuleIdByKey

Query the module ID by module identifier

```javascript
informat.app.getModuleIdByKey(key)
```

**Parameters**

| Parameter | Type   | Description       |
|-----------|--------|-------------------|
| key       | String | Module identifier |

**Return Value**

Type is `String`, returns the module ID

**Example**

::: code-group

```javascript [Call]
const moduleId = informat.app.getModuleIdByKey('dataModelBasics');
console.log(moduleId);
```

```text [Return Value]
ww0wfsota14xm
```

:::

## getModuleKeyById

Query the module identifier by module ID

```javascript
informat.app.getModuleKeyById(id)
```

**Parameters**

| Parameter | Type   | Description |
|-----------|--------|-------------|
| id        | String | Module ID   |

**Return Value**

Type is `String`, returns the module identifier

**Example**

::: code-group

```javascript [Call]
const moduleId = informat.app.getModuleKeyById('ww0wfsota14xm');
console.log(moduleId);
```

```text [Return Value]
dataModelBasics
```

:::

## userId

Query the current operating user ID

```javascript
informat.app.userId()
```

**Return Value**

Type is `String`, returns the current user ID

**Example**

::: code-group

```javascript [Call]
const userId = informat.app.userId();
console.log(userId);
```

```text [Return Value]
zhangsan
```

:::

## appDefine

Get the configuration information of the current application

```javascript
informat.app.appDefine()
```

**Return Value**

Type is [AppDefine](/guide/script/model.md#appdefine), returns the current application configuration

**Example**

::: code-group

```javascript [Call]
const appDefine = informat.app.appDefine();
console.log(appDefine);
```

```json [Return Value]
{
  "apiList": [
  ],
  "automaticList": [
    {
      "directory": false,
      "expand": false,
      "id": "kg93tarx7z0ni",
      "isDirectory": false,
      "key": "kg93tarx7z0ni",
      "name": "Excel转换为Pdf",
      "type": "default"
    },
    {
      "directory": false,
      "expand": false,
      "id": "pk7azjbk73fm3",
      "isDirectory": false,
      "key": "pk7azjbk73fm3",
      "name": "发布应用事件",
      "type": "default"
    },
    {
      "directory": false,
      "expand": false,
      "id": "a1ns3a7wu1nw7",
      "isDirectory": false,
      "name": "发布应能用时间",
      "type": "default"
    }
  ],
  "color": "c1",
  "eventList": [
    {
      "id": "gzginycn5nk4",
      "key": "shijian",
      "name": "发布事件"
    }
  ],
  "id": "excel2pdf",
  "moduleList": [
    {
      "directory": false,
      "expand": false,
      "icon": "table",
      "id": "v10lxegyp7q9x",
      "isDirectory": false,
      "key": "tab",
      "name": "数据表",
      "type": "Table"
    }
  ],
  "name": "分区示例",
  "roleList": [
    {
      "directory": false,
      "expand": false,
      "id": "lzlq4xtzj7wa0",
      "isDirectory": false,
      "key": "admin",
      "name": "管理员"
    }
  ],
  "scheduleList": [
  ],
  "scriptList": [
  ],
  "versionList": [
  ]
}
```

:::

## moduleTree

Get the module tree

```javascript
informat.app.moduleTree()
```

**Return Value**

Type is Array<[ObjectRef](/guide/script/model.md#objectref)>, returns the module list

**Example**

::: code-group

```javascript [Call]
const moduleTree = informat.app.moduleTree();
console.log(moduleTree);
```

```json [Return Value]
[
  {
    "directory": false,
    "expand": false,
    "icon": "table",
    "id": "ww0wfsota14xm",
    "isDirectory": false,
    "key": "dataModelBasics",
    "name": "基础数据表模型",
    "type": "Table"
  },
  {
    "children": [
      {
        "children": [
          {
            "directory": false,
            "expand": false,
            "icon": "table",
            "id": "fq8npovpr6xwq",
            "isDirectory": false,
            "key": "fq8npovpr6xwq",
            "name": "数据表xx",
            "type": "Table"
          }
        ],
        "directory": true,
        "expand": false,
        "icon": "arrow-up-circle",
        "id": "bo6uz2zshv8u",
        "isDirectory": true,
        "name": "分组11",
        "type": "Group"
      }
    ],
    "directory": true,
    "expand": false,
    "icon": "corner-down-right",
    "id": "d6l87tqgh3s9",
    "isDirectory": true,
    "name": "分组1",
    "type": "Group"
  }
]
```

:::

## weworkAccessToken

Get the WeCom (Enterprise WeChat) AccessToken

```javascript
informat.app.weworkAccessToken()
```

**Return Value**

Type `String`, WeCom AccessToken

**Example**

::: code-group

```javascript [Call]
const accessToken = informat.app.weworkAccessToken();
console.log(accessToken);
```

```text [Return Value]
<wework-access-token>
```

:::

## dingtalkAccessToken

Get the DingTalk AccessToken

```javascript
informat.app.dingtalkAccessToken()
```

**Return Value**

Type `String`, DingTalk AccessToken

**Example**

::: code-group

```javascript [Call]
const accessToken = informat.app.dingtalkAccessToken();
console.log(accessToken);
```

```text [Return Value]
<dingtalk-access-token>
```

:::

## feishuAccessToken

Get the Feishu (Lark) application AccessToken

```javascript
informat.app.feishuAccessToken()
```

**Return Value**

Type `String`, Feishu application AccessToken

**Example**

::: code-group

```javascript [Call]
const accessToken = informat.app.feishuAccessToken();
console.log(accessToken);
```

```text [Return Value]
<feishu-app-access-token>
```

:::

## feishuTenantAccessToken

Get the Feishu (Lark) tenant AccessToken

```javascript
informat.app.feishuTenantAccessToken()
```

**Return Value**

Type `String`, Feishu tenant AccessToken

**Example**

::: code-group

```javascript [Call]
const accessToken = informat.app.feishuTenantAccessToken();
console.log(accessToken);
```

```text [Return Value]
<feishu-tenant-access-token>
```

:::

## appEnvProp

Get an environment variable value

```javascript
informat.app.appEnvProp(id)
```

**Parameters**

| Parameter | Type   | Description           |
|-----------|--------|-----------------------|
| id        | String | Environment variable ID |

**Return Value**

Type `String`, environment variable value

::: code-group

```javascript [Call]
informat.app.appEnvProp('host');
```

```text [Return Value]
<app-env-host-url>
```

:::

## showModuleAlert

Set the module alert message

```javascript
informat.app.showModuleAlert(moduleAlert)
```

::: tip Note
The module alert message is displayed at the top of the module page to show descriptive text. For example, displaying the current import progress during data import.
:::

**Parameters**

| Parameter   | Type                                              | Description   |
|-------------|---------------------------------------------------|---------------|
| moduleAlert | [ModuleAlert](/guide/script/model.md#modulealert) | Alert message |

**Example**

```javascript
informat.app.showModuleAlert({
    moduleId: 'task',
    title: 'Data is being imported',
    description: 'Currently importing 40/100',
    type: 'info'
})
```

## hideModuleAlert

Hide the module alert message

```javascript
informat.app.hideModuleAlert(moduleId)
```

**Parameters**

| Parameter | Type     | Description       |
|-----------|----------|-------------------|
| moduleId  | `String` | Module identifier |

**Example**

```js
informat.app.hideModuleAlert('task')
```

## invokeAutomatic

Invoke an automation program

```javascript
informat.app.invokeAutomatic(automaticId, args)
```

::: tip Note

- An exception will be thrown if the automation program does not exist
- Returns `null` if the automation program has no return value
  :::

**Parameters**

| Parameter   | Type            | Description                     |
|-------------|-----------------|----------------------------------|
| automaticId | `String`        | Automation program identifier   |
| args        | `Array<Object>` | Parameter list                  |

**Return Value**

Type `Object`, the return value of the automation program

**Example**

::: code-group

```javascript [Call]
informat.app.invokeAutomatic('addAutomatic', [1, 2])
```

```text [Return Value]
3
```

:::

## pushEvent

Push an event to the client

```javascript
informat.app.pushEvent(event)
```

**Parameters**

| Parameter | Type                                          | Description |
|-----------|-----------------------------------------------|-------------|
| event     | [PushEvent](/guide/script/model.md#pushevent) | Event data  |

**Example**

::: code-group

```javascript [Refresh Module]
informat.app.pushEvent({
    eventId: 'ModuleRefresh',
    moduleRefreshModuleId: 'task'
});
```

```javascript [Show Toast Message]
informat.app.pushEvent({
    eventId: 'Toast',
    toastMessage: 'Zhang San deleted record test'
});
```

```javascript [Refresh Record Form]
informat.app.pushEvent({
    eventId: 'RecordFormRefresh',
    recordFormRefreshTableId: 'task',
    recordFormRefreshRecordId: 'sf2lk7c7ctzyq'
});
```

:::

## publishAppEvent

Publish an application event

```javascript
informat.app.publishAppEvent(event)
```

::: tip

- Other applications in the team can receive event messages through listeners
  :::

**Parameters**

| Parameter | Type | Description       |
|-----------|------|-------------------|
| event     | [AppEvent](/guide/script/model.md#appevent) | Application event |

**Example**

```javascript
informat.app.publishAppEvent({
    id: 'publishFromSript',
    content: {
        user: 'Zhang San'
    }
});
```

## queryCustomRoleList

Query the custom role list

```javascript
informat.app.queryCustomRoleList(query)
```

**Parameters**

| Parameter | Type                               | Description     |
|-----------|----------------------------------|-----------------|
| query     | [Query](/guide/script/model.md#query) | Query condition |

Fields available in the filter

| Parameter | Type     | Description |
|-----------|----------|-------------|
| name      | `String` | Name        |

**Example**

Query custom roles whose name contains `General Manager`

::: code-group

```javascript [Call]
informat.app.queryCustomRoleList({
    pageIndex: 1,
    pageSize: 100,
    filter: {
        conditionList: [
            {
                fieldId: 'name',
                opt: 'contains',
                value: '总经理'
            }
        ]
    }
});
```
```json [Return Value]
[
  {
    "createTime": 1709884168637,
    "id": "ceo",
    "name": "总经理",
    "permissionList": [
      "AppAccess",
      "AppMember",
      "...",
      "zu2whl8gk09j9_ExternalAccess",
      "printDesigner_DashboardAccess"
    ],
    "updateTime": 1717065850763
  }
]
```
:::

## queryCustomRoleListCount

Query the total count of custom roles

```javascript
informat.app.queryCustomRoleListCount(filter)
```

**Parameters**

| Parameter | Type                                    | Description     |
|----------|-----------------------------------------|-----------------|
| filter   | [Filter](/guide/script/model.md#filter) | Query condition |

**Example**

Query the total count of custom roles whose name contains `General Manager`

::: code-group

```javascript [Call]
informat.app.queryCustomRoleListCount({
    conditionList: [
        {
            fieldId: 'name',
            opt: 'contains',
            value: '总经理'
        }
    ]
});
```
```text [Return Value]
1
```
:::

## addCustomRole

Add a custom role

```javascript
informat.app.addCustomRole(role)
```

| Parameter | Type                                          | Description |
|-----------|-----------------------------------------------|-------------|
| role      | [CustomRole](/guide/script/model.md#customrole) | Custom role |

**Example**

```javascript
informat.app.addCustomRole({
    id: 'supplier',
    name: 'Supplier',
    remark: 'Directly provides goods and related services to retailers',
    permissionList: ['AppAccess', 'user_TableAccess']
});
```

## updateCustomRole

Update a custom role

```javascript
informat.app.updateCustomRole(role)
```

**Parameters**

| Parameter | Type         | Description |
|-----------|--------------|-------------|
| role      | [CustomRole](/guide/script/model.md#customrole) | Custom role |

**Return Value**

Type `Integer`
Number of updated records

**Example**

::: code-group

```javascript [Call]
informat.app.updateCustomRole({
    id: 'supplier',
    name: 'Primary Supplier',
    remark: 'Directly provides goods and related services to retailers',
    permissionList: ['AppAccess', 'user_TableAccess', 'user_TableInsert']
});
```
```text [Return Value]
1
```

:::

## deleteCustomRole

Delete a custom role

```javascript
informat.app.deleteCustomRole(id)
```

| Parameter | Type     | Description            |
|-----------|----------|------------------------|
| id        | `String` | Custom role identifier |

**Return Value**

Type `Integer`
Number of deleted records

**Example**

::: code-group

```javascript [Call]
informat.app.deleteCustomRole('supplier');
```
```text [Return Value]
1
```
:::

## setAppBadge

Set the application badge

```javascript
informat.app.setAppBadge(content)
```

**Parameters**

| Parameter | Type     | Description       |
|-----------|----------|-------------------|
| content   | `String` | Badge content     |

**Example**

```javascript
informat.app.setAppBadge('Important');
```

## favoriteModule

Favorite a module

```javascript
informat.app.favoriteModule(moduleList)
```

| Parameter  | Type            | Description            |
|------------|-----------------|------------------------|
| moduleList | `Array<String>` | Module identifier list |

**Return Value**

Type `Array<String>`
Favorite record ID list

**Example**
::: code-group

```javascript [Call]
informat.app.favoriteModule(['scriptTableA', 'scriptTableB']);
```
```json [Return Value]
[
  "gh2lsh2sgnnms",
  "f52xscr7c77u0"
]
```
:::

## cancelFavoriteModule

Cancel favoriting a module

```javascript
informat.app.cancelFavoriteModule(moduleList)
```

| Parameter  | Type            | Description            |
|------------|-----------------|------------------------|
| moduleList | `Array<String>` | Module identifier list |

**Return Value**

Type `Integer`
Number of records affected by unfavoriting

**Example**

::: code-group

```javascript [Call]
informat.app.cancelFavoriteModule(['scriptTableA', 'scriptTableB']);
```
```text [Return Value]
2
```

:::

## queryFavoriteModuleList

Query my favorited module list (modules within this application)

```javascript
informat.app.queryFavoriteModuleList(query)
```

| Parameter | Type    | Description     |
|-----------|---------|-----------------|
| query     | [Query](/guide/script/model.md#query) | Query condition |

Fields available in the filter

| Parameter  | Type     | Description |
|------------|----------|-------------|
| moduleName | `String` | Module name |

**Return Value**

Type Array<[ModuleFavorite](/guide/script/model.md#modulefavorite)>, my favorited module list

**Example**

Query favorited modules whose name contains `Task`

::: code-group

```javascript [Call]
informat.app.queryFavoriteModuleList({
    pageIndex: 1,
    pageSize: 100,
    filter: {
        conditionList: [
            {
                fieldId: 'moduleName',
                opt: 'contains',
                value: '任务'
            }
        ]
    }
});
```
```json [Return Value]
[
  {
    "accountId": "yvkc2kwpy3xzr",
    "applicationId": "i1mwqy35y88hl",
    "id": "n9m98qmomke3g",
    "moduleIcon": "noto-slightly-smiling-face",
    "moduleId": "vylzhve0zrehp",
    "moduleName": "欢迎",
    "moduleType": "Dashboard"
  }
]
```

:::

## queryFavoriteModuleListCount

Query the total count of my favorited modules (modules within this application)

```javascript
informat.app.queryFavoriteModuleListCount(filter)
```

| Parameter | Type                                    | Description     |
|----------|-----------------------------------------|-----------------|
| filter   | [Filter](/guide/script/model.md#filter) | Query condition |

**Return Value**

Type `Integer`, total count of my favorited modules

**Example**

Query the total count of favorited modules whose name contains `Task`

::: code-group

```javascript [Call]
informat.app.queryFavoriteModuleListCount({
    conditionList: [
        {
            fieldId: 'moduleName',
            opt: 'contains',
            value: '任务'
        }
    ]
});
```

```text [Return Value]
1
```

:::

## eval

Run a script

```javascript
informat.app.eval(script)
```

| Parameter | Type     | Description       |
|-----------|----------|-------------------|
| script    | `String` | JS script content |

**Return Value**

Type `Object`, script execution result

**Example**


::: code-group

```javascript [Call]
informat.app.eval(`
        let date = new Date()
        console.log(date);`
);
```

```text [Return Value]
Fri May 31 10:11:55 CST 2024
```

:::

## appInfo

App runtime information

```javascript
informat.app.appInfo()
```

**Return Value**

Type [Application](/guide/script/model.md#app), app runtime information

**Example**

::: code-group

```javascript [Call]
informat.app.appInfo();
```

```json [Return Value]
{
  "appDefineBuild": 863,
  "appDefineEditable": true,
  "appDefineVersion": "17",
  "appDefineId": "com.mycompany",
  "color": "c7",
  "createAccountId": "zhangsan",
  "createTime": 1680006873433,
  "icon": "home",
  "id": "ftegr30w93jya",
  "enableAppJsonLog": false,
  "enableAppLog": false,
  "env": "dev",
  "name": "测试一下",
  "updateAccountId": "zhangsan",
  "updateTime": 1696919628896
}
```

:::

## runSchedule

Run a scheduled task

```javascript
informat.app.runSchedule(key)
```

::: tip Note
A successful run will affect the next scheduled execution time. For example, if a scheduled task runs every hour and the last execution was at 19:30, the next execution would be at 20:30. If the user calls this API to run the task at 20:10, the next execution time will be 21:10, not 20:30.
:::

| Parameter | Type     | Description              |
|-----------|----------|--------------------------|
| key       | `String` | Scheduled task identifier |

**Return Value**

None

**Example**

```javascript
informat.app.runSchedule('ao8ymduy4jt2p');
```

## getPerformanceStatistics

Returns the performance statistics list for the current app

```javascript
informat.app.getPerformanceStatistics()
```

**Return Value**

Type Array<[ApplicationProcess](/guide/script/model.md#applicationprocess)>
Performance statistics list for the current app

**Example**

::: code-group

```javascript [Call]
informat.app.getPerformanceStatistics();
```

```json [Return Value]
[
  {
    "associatedId": "xxx_eval_lan5wqq9au2ls",
    "associatedKey": "xxx_eval_lan5wqq9au2ls",
    "associatedName": "xxx_eval_lan5wqq9au2ls",
    "id": "biy9wnye6i4bd",
    "serverId": "informat-biz2-prd",
    "startTime": 1717068263865,
    "status": "running",
    "type": "script"
  },
  {
    "associatedId": "xxxx_eval_s67wnu06xntlc",
    "associatedKey": "xxx_eval_s67wnu06xntlc",
    "associatedName": "xxx_eval_s67wnu06xntlc",
    "endTime": 1717068247296,
    "id": "oaqm8xgyz7m3z",
    "serverId": "informat-biz2-prd",
    "startTime": 1717068247294,
    "status": "success",
    "type": "script"
  }
]
```

:::

## queryAppChangeLogList

Query the application operation log list

```javascript
informat.app.queryAppChangeLogList(query)
```

**Parameters**

| Parameter | Type    | Description     |
|-----------|---------|-----------------|
| query     | [Query](/guide/script/model.md#query) | Query condition |

Fields available in the filter

| Parameter       | Type     | Description    |
|-----------------|----------|----------------|
| type            | `String` | Type           |
| createAccountId | `String` | Creator ID     |

**Example**

Query application operation logs of type `MemberUpdate`

::: code-group

```javascript [Call]
informat.app.queryAppChangeLogList({
    pageIndex: 1,
    pageSize: 100,
    filter: {
        conditionList: [
            {
                fieldId: 'type',
                opt: 'eq',
                value: 'MemberUpdate'
            }
        ]
    }
});
```
```json [Return Value]
[
  {
    "content": "{\"avatar\":\"bc57a52b30c648c6bdba32c41b2f5371.jpg\",\"id\":\"skydu\",\"name\":\"张三\",\"newRoleList\":[\"管理员\"],\"oldRoleList\":[\"管理员\",\"成员\"]}",
    "createAccountAvatar": "bc57a52b30c648c6bdba32c41b2f5371.jpg",
    "createAccountId": "zhangsan",
    "createAccountName": "张三",
    "createTime": 1719212372446,
    "id": "uvxmqtn5337cv",
    "type": "MemberUpdate"
  }
]
```

:::

## queryAppChangeLogListCount

Query the total count of application operation logs

```javascript
informat.app.queryAppChangeLogListCount(filter)
```

**Parameters**

| Parameter | Type     | Description     |
|-----------|----------|-----------------|
| filter    | [Filter](/guide/script/model.md#filter) | Query condition |

**Example**

Query the total count of application operation logs of type `MemberUpdate`

::: code-group

```javascript [Call]
informat.app.queryAppChangeLogListCount({
    conditionList: [
        {
            fieldId: 'type',
            opt: 'eq',
            value: 'MemberUpdate'
        }
    ]
});
```

```text [Return Value]
1
```

:::

## addAppChangeLog

Create an application change log

```javascript
informat.app.addAppChangeLog(content)
```

**Parameters**

| Parameter | Type     | Description    |
|-----------|----------|----------------|
| content   | `String` | Change content |

**Example**

```javascript
informat.app.addAppChangeLog('Create record');
```

## deleteAppChangeLog

Delete an application change log

```javascript
informat.app.deleteAppChangeLog(id)
```

**Parameters**

| Parameter | Type     | Description    |
|-----------|----------|----------------|
| id        | `String` | App log ID     |

**Example**

```javascript
informat.app.deleteAppChangeLog('nf6k7cf5u80ca');
```

## addDesignerUserList

Add application designer member list

```js
informat.app.addDesignerUserList(type, userIdList)
```

**Parameters**

| Parameter  | Type            | Description                   |
|------------|-----------------|-------------------------------|
| type       | `String`        | Application design permission type |
| userIdList | `Array<String>` | Account ID array              |

Application design permission types:

| Parameter | Description                            |
|-----------|----------------------------------------|
| access    | Can enter the application design page  |
| edit      | Can perform application design         |
| publish   | Can publish the application            |

**Example**

```js
informat.app.addDesignerUserList('access', [informat.app.userId()])
informat.app.addDesignerUserList('edit', [informat.app.userId()])
informat.app.addDesignerUserList('publish', [informat.app.userId()])
```

:::tip Note

- The application design edit members and publish members are empty by default, and when empty, all members have edit and publish permissions by default. In this case, calling `addDesignerUserList` and `removeDesignerUserList` may produce unexpected results.

- To manage member edit and publish permissions, you should first configure the corresponding edit and publish members.
  
:::

## getDesignerUserList

Query the application designer member list

```js
informat.app.getDesignerUserList(type)
```

**Parameters**

| Parameter | Type     | Description                   |
|-----------|----------|-------------------------------|
| type      | `String` | Application design permission type |

Application design permission types:

| Parameter | Description                            |
|-----------|----------------------------------------|
| access    | Can enter the application design page  |
| edit      | Can perform application design         |
| publish   | Can publish the application            |

**Example**

::: code-group

```javascript [Call]
informat.app.getDesignerUserList('access')
```

```json [Return Value]
[
  "lwfwqr67xsvup",
  "uc4qsqmm64nep",
  "zhansan",
  "lisi"
]
```

:::

## removeDesignerUserList

Remove application designer member list

```js
informat.app.removeDesignerUserList(type, userIdList)
```

**Parameters**

| Parameter  | Type            | Description                   |
|------------|-----------------|-------------------------------|
| type       | `String`        | Application design permission type |
| userIdList | `Array<String>` | Account ID array              |

Application design permission types:

| Parameter | Description                            |
|-----------|----------------------------------------|
| access    | Can enter the application design page  |
| edit      | Can perform application design         |
| publish   | Can publish the application            |

**Example**

```js
informat.app.removeDesignerUserList('access', [informat.app.userId()])
informat.app.removeDesignerUserList('edit', [informat.app.userId()])
informat.app.removeDesignerUserList('publish', [informat.app.userId()])
```

## userLoginType

Query the current user's login type

```js
informat.app.userLoginType()
```

**Return Value**

Type is `String`, returns the current user's login type

::: code-group

```javascript [Call]
const userLoginType = informat.app.userLoginType();
console.log(userLoginType);
```

```text [Return Value]
index
```

:::
