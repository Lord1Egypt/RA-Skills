# informat.system System Global Operations

## Overview

Use the `informat.system` object to perform system global operations. Global operations require the `System Function Call` module in the license.

## serverId

Query the server node ID

```javascript
informat.system.serverId()
```

**Return Value**
Type is String, returns the server node ID.

> The server node ID value comes from the spring > application > serverId configuration in the **informat-next/instance/informat-xxxx/application.yml** file

**Example**

```javascript
informat.system.serverId(); // informat2-biz-prd
```

## host

Return the system's home page URL

```javascript
informat.system.host()
```

**Return Value**
Type is String, returns the system's home page URL.

**Example**

```javascript
informat.system.host();
// Returns
https://next.informat.cn/ 
```

## getAccount

Query account information

```javascript
informat.system.getAccount(id)
```

| Parameter | Type     | Description   |
|----|--------|------|
| id | String | Account ID |

**Return Value** Type is [Account](/guide/script/model.md#account)

Returns user information. Returns `null` if the user does not exist.

**Example**

Assuming an account with ID **lwfwqr67xsvup** exists in the system for user Zhang San

```javascript
informat.system.getAccount('lwfwqr67xsvup');
```

Return value

```json
{
  "avatar": "pic16.png",
  "companyId": "g09aj7cus3d8s",
  "createTime": 1664200514136,
  "email": "zhangsan@example.com",
  "id": "lwfwqr67xsvup",
  "isValid": true,
  "mobileNo": "13012345678",
  "name": "张三",
  "oid": "zhangsan",
  "updateTime": 1683598262000,
  "userName": "zhangsan",
  "valid": true
}
```

## getAccountByUserName

Query account information by username

```javascript
informat.system.getAccountByUserName(userName)
```

| Parameter       | Type     | Description  |
|----------|--------|-----|
| userName | String | Username |

**Return Value** Type is [Account](/guide/script/model.md#account)

Returns user information. Returns `null` if the user does not exist.

**Example**

Assuming a user with username **zhangsan** exists in the system

```javascript
informat.system.getAccountByUserName('zhangsan');
```

Return value

```json
{
  "avatar": "pic16.png",
  "companyId": "g09aj7cus3d8s",
  "createTime": 1664200514136,
  "email": "zhangsan@example.com",
  "id": "lwfwqr67xsvup",
  "isValid": true,
  "mobileNo": "13012345678",
  "name": "张三",
  "oid": "zhangsan",
  "updateTime": 1683598262000,
  "userName": "zhangsan",
  "valid": true
}
```

## getAccountByMobileNo

Query account information by mobile number

```javascript
informat.system.getAccountByMobileNo(mobileNo)
```

| Parameter       | Type     | Description  |
|----------|--------|-----|
| mobileNo | String | Mobile number |

**Return Value** Type is [Account](/guide/script/model.md#account)

Returns user information. Returns `null` if the user does not exist.

**Example**

Assuming a user with mobile number **13012345678** exists in the system

```javascript
informat.system.getAccountByMobileNo('13012345678');
```

Return value

```json
{
  "avatar": "pic16.png",
  "companyId": "g09aj7cus3d8s",
  "createTime": 1664200514136,
  "email": "zhangsan@example.com",
  "id": "lwfwqr67xsvup",
  "isValid": true,
  "mobileNo": "13012345678",
  "name": "张三",
  "oid": "zhangsan",
  "updateTime": 1683598262000,
  "userName": "zhangsan",
  "valid": true
}
```

## getAccountByEmail

Query account information by email

```javascript
informat.system.getAccountByEmail(mobileNo)
```

| Parameter    | Type     | Description |
|-------|--------|----|
| email | String | Email |

**Return Value** Type is [Account](/guide/script/model.md#account)

Returns user information. Returns `null` if the user does not exist.

**Example**

Assuming a user with email **zhangsan@example.com** exists in the system

```javascript
informat.system.getAccountByEmail('zhangsan@example.com');
```

Return value

```json
{
  "avatar": "pic16.png",
  "companyId": "g09aj7cus3d8s",
  "createTime": 1664200514136,
  "email": "zhangsan@example.com",
  "id": "lwfwqr67xsvup",
  "isValid": true,
  "mobileNo": "13012345678",
  "name": "张三",
  "oid": "zhangsan",
  "updateTime": 1683598262000,
  "userName": "zhangsan",
  "valid": true
}
```

## queryAccountList

Query account list

```javascript
informat.system.queryAccountList(query)
```

| Parameter    | Type                                    | Description     |
|-------|---------------------------------------|--------|
| query | [Query](/guide/script/model.md#query) | Account query criteria |

Fields available in the filter

| Field       | Type     | Description    |
|----------|--------|-------|
| id       | String | Account ID  |
| name     | String | Name    |
| userName | String | Username   |
| mobileNo | String | Mobile number   |
| email    | String | Email    |
| oid      | String | Third-party ID |

**Return Value**
Returns an account list, type is Array<[Account](/guide/script/model.md#account)>

**Example**

```javascript
informat.system.queryAccountList({
    pageIndex: 1,
    pageSize: 10,
    filter: {
        conditionList: [
            {
                fieldId: 'userName',
                opt: 'contains',
                value: 'zhang'
            }
        ]
    }
});
```

Return value

```json
[
  {
    "avatar": "pic16.png",
    "companyId": "g09aj7cus3d8s",
    "createTime": 1664200514136,
    "email": "zhangsan@example.com",
    "id": "lwfwqr67xsvup",
    "isValid": true,
    "mobileNo": "13012345678",
    "name": "张三",
    "oid": "zhangsan",
    "updateTime": 1683598262000,
    "userName": "zhangsan",
    "valid": true
  },
  {
    "avatar": "pic23.png",
    "createTime": 1675836165076,
    "id": "x3q3npo3xsait",
    "isValid": true,
    "mobileNo": "18291909205",
    "name": "张荣立",
    "updateTime": 1683594979000,
    "userName": "zhangrongli",
    "valid": true
  },
  {
    "avatar": "pic13.png",
    "createTime": 1682307631474,
    "email": "zhangrongfu@itit.io",
    "id": "wlt9cgr70o0yi",
    "isValid": true,
    "mobileNo": "15989268009",
    "name": "张荣富",
    "updateTime": 1683335991000,
    "userName": "zhangrongfu",
    "valid": true
  }
] 
```

## queryAccountListCount

Query total account count

```javascript
informat.system.queryAccountListCount(filter)
```

| Parameter     | Type                                      | Description   |
|--------|-----------------------------------------|------|
| filter | [Filter](/guide/script/model.md#filter) | Query criteria |

**Return Value**

Returns the total account count, type is `Integer`

**Example**

```javascript
informat.system.queryAccountListCount({
    conditionList: [
        {
            fieldId: 'userName',
            opt: 'contains',
            value: 'zhang'
        }
    ]
}); // Returns 3
```

## addAccount

Add a new account

```javascript
informat.system.addAccount(account)
```

| Parameter      | Type                                        | Description               |
|---------|-------------------------------------------|------------------|
| account | [AccountAddForm](/guide/script/model.md#accountaddform) | Account information. ID and creation time do not need to be provided |

**Return Value**
Returns the newly created account ID, type is String

**Example 1 - Add an account**

:::code-group

```js[Call]
informat.system.addAccount({
    name: 'test',
    avatar: 'pic15.png',
    userName: 'test',
    mobileNo: '13800000000',
    email: 'test@informat.cn',
    password: '<account-password>'
});
```

```json[Return Value]
"ap1cew2up9ehq"
```

:::
**Example 2 - Add an account with a specified ID**
:::code-group

```js[Call]
informat.system.addAccount({
	id: 'zhangsan',
    name: 'test',
    avatar: 'pic15.png',
    userName: 'zhangsan',
    mobileNo: '13800000000',
    email: 'zhangsan@informat.cn',
    password: '<account-password>'
});
```

```json[Return Value]
"zhangsan"
```

:::

## updateAccount

Update account information

```javascript
informat.system.updateAccount(account)
```

| Parameter      | Type                                        | Description   |
|---------|-------------------------------------------|------|
| account | [Account](/guide/script/model.md#account) | Account information |

Fields that can be updated

| Field                 | Type      | Description          |
|--------------------|---------|-------------|
| oid                | String  | Identifier         |
| name               | String  | Name          |
| userName           | String  | Username         |
| mobileNo           | String  | Mobile number         |
| email              | String  | Email          |
| avatar             | String  | Avatar          |
| language           | String  | Language          |
| needUpdatePassword | Boolean | Whether to force password change |

**Return Value**
Returns the number of updated accounts, type is `Integer`

**Example**

:::code-group

```js[Call]
informat.system.updateAccount({
    id: 'ap1cew2up9ehq',
    name: 'test2',
    avatar: 'pic16.png',
    userName: 'test2',
    mobileNo: '13700000000',
    email: 'test2@informat.cn'
});
```

```json[Return Value]
1
```

:::

## updateAccountList

Update account list

```javascript
informat.system.updateAccountList(account, filter)
```

| Parameter      | Type                                        | Description   |
|---------|-------------------------------------------|------|
| account | [Account](/guide/script/model.md#account) | Account information |
| filter  | [Filter](/guide/script/model.md#filter)   | Query criteria |

Fields that can be updated

| Field                 | Type      | Description          |
|--------------------|---------|-------------|
| oid                | String  | Identifier         |
| name               | String  | Name          |
| userName           | String  | Username         |
| mobileNo           | String  | Mobile number         |
| email              | String  | Email          |
| avatar             | String  | Avatar          |
| language           | String  | Language          |
| needUpdatePassword | Boolean | Whether to force password change |

**Return Value**
Returns the number of updated accounts, type is `Integer`

**Example**

```javascript
informat.system.updateAccountList(
    {
        name: 'test2',
        avatar: 'pic15.png',
        userName: 'test2',
        mobileNo: '13900000000',
        email: 'test2@informat.cn'
    },
    {
        conditionList: [
            { 'fieldId': 'id', 'opt': 'eq', 'value': 'ap1cew2up9ehq' }
        ]
    }
); 
```

## changePassword

Change account password

```javascript
informat.system.changePassword(accountId, pwd)
```

| Parameter        | Type     | Description   |
|-----------|--------|------|
| accountId | String | Account ID |
| pwd       | String | Password   |

## createToken

Create a login token for an account

```javascript
informat.system.createToken(accountId, type)
```

| Parameter        | Type     | Description                                                                                                                            |
|-----------|--------|-------------------------------------------------------------------------------------------------------------------------------|
| accountId | String | Account ID                                                                                                                          |
| type      | String | Token type<br/>`PC index`<br/>`Mobile mobile`<br/>`Survey mobile survey` <br/>`Survey PC surveyweb` <br/>In addition to built-in system types, custom types are also supported (e.g., app, wechat, wemp, etc.) |

**Return Value**
Returns the authorized TOKEN, type is `String`

**Example**

:::code-group

```javascript
informat.system.createToken('wlt9cgr70o0yi', 'index');
```

```json[Return Value]
"581aa91125e74a74a07747ef6862ba41"
```

:::

## getAccountByToken

Find account information by TOKEN

```javascript
informat.system.getAccountByToken(token)
```

| Parameter    | Type     | Description    |
|-------|--------|-------|
| token | String | TOKEN |

**Return Value**

Returns account information. Returns null if the TOKEN does not exist. Type is [Account](/guide/script/model.md#account)

:::code-group

```js[Call]
informat.system.getAccountByToken("581aa91125e74a74a07747ef6862ba41");
```

```json[Return Value]
{
    "avatar": "pic16.png",
    "companyId": "g09aj7cus3d8s",
    "createTime": 1664200514136,
    "email": "zhangsan@example.com",
    "id": "lwfwqr67xsvup",
    "isValid": true,
    "mobileNo": "13012345678",
    "name": "张三",
    "oid": "zhangsan",
    "updateTime": 1683598262000,
    "userName": "zhangsan",
    "valid": true
}
```

:::

## login

Log in to the system

```javascript
informat.system.login(loginForm)
```

| Parameter        | Type            | Description          |
|-----------|---------------|-------------|
| loginForm | [LoginForm](/guide/script/model.md#loginform) | Username or mobile number, email |

**Return Value**

Returns the login result, type is `LoginResult`

:::code-group

```js[Call]
informat.system.login({
	userName:'zhangsan',
	password:'<account-password>',
	type:'mobile',
	ip:'183.46.24.11'
})
```

```json[Return Value]
{
"accountId":"zhangsan",
"companyId":"g09aj7cus3d8s",
"errorCode":0,
"token":"2f7536034b3748c9ba7db15759d01f26"
}
```

:::

## validateAccount

Validate username and password

```javascript
informat.system.validateAccount(user, pwd)
```

| Parameter   | Type     | Description       |
|------|--------|----------|
| user | String | Username or mobile number |
| pwd  | String | Password       |

**Return Value**

Returns `true` if the username and password are correct, otherwise returns `false`. Type is `Boolean`

```javascript
informat.system.validateAccount('zhangsan', '<account-password>')// false
```

## setAccountValid

Enable/disable an account

```javascript
informat.system.setAccountValid(accountId, isValid)
```

| Parameter        | Type      | Description    |
|-----------|---------|-------|
| accountId | String  | Account ID  |
| isValid   | Boolean | Enable or disable |

**Example**

```javascript
// Disable Zhang San's account
informat.system.setAccountValid('lwfwqr67xsvup', false);
// Enable Zhang San's account
informat.system.setAccountValid('lwfwqr67xsvup', true);
```

## invokeLibrary

Call a function in an extension library

> For detailed information about extension libraries, see [Extension Library](/guide/app/library.md)

```javascript
informat.system.invokeLibrary(libraryId, className, method, args)
```

| Parameter        | Type     | Description                                         |
|-----------|--------|--------------------------------------------|
| libraryId | String | Extension library identifier                                     |
| className | String | Full class path of the class in the extension library, e.g., `com.mycompany.MyLibaray` |
| method    | String | Method to call in the extension library. This method must be static                    |
| args      | Parameter array   | Parameters to pass to the method. Pass null if there are no parameters                     |

**Return Value**

Return value of the method in the extension library, type is `Object`

Here is an example

```javascript
informat.system.invokeLibrary('mylibrary', 'com.mycompany.MyLibaray', 'add', [1, 2])
```

If the extension library function has no parameters

```javascript
informat.system.invokeLibrary('mylibrary', 'com.mycompany.MyLibaray', 'test', null);
informat.system.invokeLibrary('mylibrary', 'com.mycompany.MyLibaray', 'test');
```

For more detailed information, see [Extension Library](/guide/app/library.md)

## runProcess

Start a new process

```javascript
informat.system.runProcess(args)
```

| Parameter   | Type                                                      | Description   |
|------|---------------------------------------------------------|------|
| args | [ProcessRunArgs](/guide/script/model.md#processrunargs) | Execution parameters |

ProcessRunArgs structure

| Property      | Type                  | Description               |
|---------|---------------------|------------------|
| cmds    | Array&lt;String&gt; | Commands to execute            |
| timeout | Integer             | Timeout in milliseconds. 0 means no timeout |

**Return Value**

Type is [ProcessRunResult](/guide/script/model.md#processrunresult), structure:

| Property        | Type      | Description   |
|-----------|---------|------|
| exitValue | Integer | Exit code  |
| out       | String  | Standard output |
| err       | String  | Error output |

Here is an example

```javascript
const result = informat.system.runProcess({
    cmds: ['java', '-version'],
    timeout: 0
});
console.log(result.out); // java version "11.0.5" 2019-10-15 LTS
```

## runNodeJS

Start a new process to run NodeJS. Parameters are passed via command line arguments (cmdline) and standard input (stdin). The NodeJS process uses standard output and error output as return values.

```javascript
informat.system.runNodeJS(args)
```

| Parameter   | Type                                                    | Description   |
|------|-------------------------------------------------------|------|
| args | [RunNodeJSArgs](/guide/script/model.md#runnodejsargs) | Execution parameters |

RunNodeJSArgs structure

| Property      | Type                  | Description                                                    |
|---------|---------------------|-------------------------------------------------------|
| script  | String              | Script file to execute, e.g., test/helloworld.js                         |
| cmdline | Array&lt;String&gt; | The OS has a command line argument length limit. On Linux the maximum is 131071. Use stdin for passing large amounts of data |
| stdin   | String              | Standard input                                                  |
| env     | Object              | Environment variables                                                  |

**Return Value**

Type is [ProcessRunResult](/guide/script/model.md#processrunresult), structure:

| Property        | Type      | Description   |
|-----------|---------|------|
| exitValue | Integer | Exit code  |
| out       | String  | Standard output |
| err       | String  | Error output |

Here is an example

Test script file nodejs/md5test.js with the following content:

```javascript
/**
 * Use the md5 library to compute the md5 value of the input string. Input parameters are passed via command line
 */
var arguments = process.argv;
//Get input parameter
let input = arguments[2];
var md5 = require('md5');
//Use standard output to pass the result
console.log(md5(input));
```

Code to call NodeJS:

```javascript
var result = informat.system.runNodeJS({
    'script': 'nodejs/md5test.js',
    'cmdline': ['123456']
});
console.log('md5 value:', result.out);
```

## queryCompanyList

Query team list

```javascript
informat.system.queryCompanyList(query)
```

| Parameter    | Type                                    | Description   |
|-------|---------------------------------------|------|
| query | [Query](/guide/script/model.md#query) | Query criteria |

Fields available in the filter

| Field   | Type     | Description   |
|------|--------|------|
| id   | String | Account ID |
| name | String | Name   |

**Return Value**
Returns a team list, type is Array<[Company](/guide/script/model.md#company)>

**Example**

:::code-group

```js[Call]
informat.system.queryCompanyList({
    pageIndex: 1,
    pageSize: 10,
    filter: {
        conditionList: [
            {
                fieldId: 'name',
                opt: 'contains',
                value: '测试'
            }
        ]
    }
});
```

```json[Return Value]
[
  {
    "createAccountId":"zhangsan",
    "createTime":1665404532125,
    "dbIndex":0,
    "id":"ukswiyvmqlq5n",
    "maxApplicationNum":0,
    "maxUserNum":0,
    "name":"测试创建团队",
    "updateTime":1704353335727,
    "version":"free"
  },
  {
    "createAccountId":"zhangsan",
    "createTime":1669306766288,
    "dbIndex":0,
    "id":"kkoixbg8ew3ks",
    "maxApplicationNum":0,
    "maxUserNum":0,
    "name":"测试团队",
    "updateTime":1713920870106,
    "version":"enterprise"
  }
]
```

:::

## queryCompanyListCount

Query total team count

```javascript
informat.system.queryCompanyListCount(filter)
```

| Parameter    | Type                                      | Description    |
|-------|-----------------------------------------|-------|
| query | [Filter](/guide/script/model.md#filter) | Query filter |

Fields available in the filter

| Field   | Type     | Description   |
|------|--------|------|
| id   | String | Account ID |
| name | String | Name   |

**Return Value**
Returns the total team count, type is int

**Example**

:::code-group

```js[Call]
informat.system.queryCompanyListCount({
    conditionList: [
        {
            fieldId: 'name',
            opt: 'contains',
            value: '测试'
        }
    ]
});
```

```json[Return Value]
2
```

:::

## addCompanyMember

Add a team member

```javascript
informat.system.addCompanyMember(companyId, accountId, departmentList, roleList)
```

| Parameter             | Type              | Description    |
|----------------|-----------------|-------|
| companyId      | String          | Team ID |
| accountId      | String          | Account ID |
| departmentList | `Array<String>` | Department list  |
| roleList       | `Array<String>` | Role list  |

**Example**

```javascript
informat.system.addCompanyMember('g09aj7cus3d8s', 'skydu2', ['dev'], ['member']);
```

## queryCompanyDeptList

Query department list

```javascript
informat.system.queryCompanyDeptList(companyId, query)
```

| Parameter        | Type                                    | Description   |
|-----------|---------------------------------------|------|
| companyId | String                                | Team ID |
| query     | [Query](/guide/script/model.md#query) | Query criteria |

Fields available in the filter

| Field         | Type     | Description     |
|------------|--------|--------|
| id         | String | Department identifier  |
| parentId   | String | Parent department identifier |
| name       | String | Department name   |
| createTime | Date   | Creation time   |

**Return Value**
Type is Array<[Department](/guide/script/model.md#department)>
Returns the department list

***Example 1 - Query departments with names containing "R&D"***

:::code-group

```js[Call]
informat.system.queryCompanyDeptList(
	'g09aj7cus3d8s',{
    pageSize:-1,
    filter:{
        conditionList:[
            {"fieldId":"name","opt":"contains","value":"研发"}
        ]
    }
});
```

```json[Return Value]
[
  {
    "id": "yanfabu",
    "name": "研发部",
    "parentId": "root",
    "remark": "负责研究和开发新产品、技术或服务的部门",
    "rowNumber": 2,
    "shortName": "研发部"
  }
]
```

:::

## getCompanyAllRoles

Query all roles of a team

```javascript
informat.system.getCompanyAllRoles(companyId)
```

| Parameter        | Type     | Description   |
|-----------|--------|------|
| companyId | String | Team ID |

**Return Value**

Type is Array<[CompanyRole](/guide/script/model.md#companyrole)>, returns all roles

Example:

:::code-group

```js[Call]
informat.system.getCompanyAllRoles('g09aj7cus3d8s')
```

```json[Return Value]
[
  {
    "admin": true,
    "createTime": 1664196760903,
    "id": "admin",
    "isAdmin": true,
    "name": "管理员",
    "permissionIds": [
      
    ]
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
  }
]
```

:::

## addOptLog

Add a system log

```js
informat.system.addOptLog(optLog)
```

**Parameters**

| Parameter     | Type                                      | Description      |
|--------|-----------------------------------------|---------|
| optLog | [OptLog](/guide/script/model.md#optlog) | Operation log to add |

`OptLog` structure:
``
| Field | Type | Description |
|--------------|----------|--------------|
| id | `String` | Operation record ID |
| type | `String` | Operation type |
| accountId | `String` | Operator ID |
| companyId | `String` | Team ID |
| associatedId | `String` | Associated ID |
| remark | `String` | Remark, appended after operation details |

Available operation types:

| Operation Type                          | Description         |
|-------------------------------|------------|
| CreateAccount                 | Create account       |
| UpdateAccount                 | Update account       |
| Register                      | Register         |
| PasswordLogin                 | Password login     |
| WechatLogin                   | WeChat QR code login     |
| MobileNoLogin                 | Mobile verification code login    |
| DingTalkLogin                 | DingTalk auto-login      |
| WeWorkLogin                   | WeCom auto-login    |
| ssoLogin                      | SSO login      |
| Logout                        | Logout         |
| UpdateUserName                | Change login name      |
| UpdateNickName                | Change nickname       |
| UpdateMobileNo                | Change mobile number      |
| UpdateEmail                   | Change email       |
| SwitchCompany                 | Switch team       |
| InviteMember                  | Invite member       |
| DeleteMember                  | Remove member       |
| CreateDepartment              | Create department       |
| UpdateDepartment              | Edit department       |
| DeleteDepartment              | Delete department       |
| CreateRole                    | Create role       |
| UpdateRole                    | Edit role       |
| DeleteRole                    | Delete role       |
| CreateCompany                 | Create team       |
| CompanySetPro                 | Set trial       |
| CompanySetModule              | Set module       |
| CreateApp                     | Create application       |
| UpdateApp                     | Edit application       |
| DeleteApp                     | Delete application       |
| ArchiveApp                    | Archive application       |
| CreateAppMember               | Add application member     |
| UpdateAppMember               | Edit application member     |
| DeleteAppMember               | Delete application member     |
| UpdateAppMemberAccessPassword | Edit application member access password |
| CreateAppModule               | Add application module     |
| DeleteAppModule               | Delete application module     |
| DeleteRecycleBin              | Delete recycle bin data    |

**Example**

```js
let optlog = {
    accountId: informat.app.userId(),
    type: 'CreateAccount',
    companyId: informat.company.getCompany().id,
    remark: '（手动）'
}
informat.system.addOptLog(optlog)
```

## queryOptLogList

Query operation log list

```js
informat.system.queryOptLogList(query)
```

**Parameters**

| Parameter    | Type                                    | Description   |
|-------|---------------------------------------|------|
| query | [Query](/guide/script/model.md#query) | Query criteria |

Fields available in the filter

| Field         | Type       | Description   |
|------------|----------|------|
| type       | `String` | Operation type |
| accountId  | `String` | Operator |
| remark     | `String` | Remark   |
| createTime | `String` | Creation time |
| updateTime | `String` | Update time |

Available operation types:

| Operation Type                          | Description         |
|-------------------------------|------------|
| CreateAccount                 | Create account       |
| UpdateAccount                 | Update account       |
| Register                      | Register         |
| PasswordLogin                 | Password login     |
| WechatLogin                   | WeChat QR code login     |
| MobileNoLogin                 | Mobile verification code login    |
| DingTalkLogin                 | DingTalk auto-login      |
| WeWorkLogin                   | WeCom auto-login    |
| ssoLogin                      | SSO login      |
| Logout                        | Logout         |
| UpdateUserName                | Change login name      |
| UpdateNickName                | Change nickname       |
| UpdateMobileNo                | Change mobile number      |
| UpdateEmail                   | Change email       |
| SwitchCompany                 | Switch team       |
| InviteMember                  | Invite member       |
| DeleteMember                  | Remove member       |
| CreateDepartment              | Create department       |
| UpdateDepartment              | Edit department       |
| DeleteDepartment              | Delete department       |
| CreateRole                    | Create role       |
| UpdateRole                    | Edit role       |
| DeleteRole                    | Delete role       |
| CreateCompany                 | Create team       |
| CompanySetPro                 | Set trial       |
| CompanySetModule              | Set module       |
| CreateApp                     | Create application       |
| UpdateApp                     | Edit application       |
| DeleteApp                     | Delete application       |
| ArchiveApp                    | Archive application       |
| CreateAppMember               | Add application member     |
| UpdateAppMember               | Edit application member     |
| DeleteAppMember               | Delete application member     |
| UpdateAppMemberAccessPassword | Edit application member access password |
| CreateAppModule               | Add application module     |
| DeleteAppModule               | Delete application module     |
| DeleteRecycleBin              | Delete recycle bin data    |

**Return Value**

Type is Array<[OptLog](/guide/script/model.md#optlog)>, operation log list

**Example**
:::code-group

```js[Call]
let query = {
    pageSize:-1,
    filter: {
        conditionList:[
            {fieldId:'type', opt: 'eq', value: 'CreateAccount'}
        ]
    }
}
informat.system.queryOptLogList(query)
```

```json[Return Value]
[
  {
    "accountAvatar": "2e6e1b0512aa4d4c8c36221cde76027b.jpg",
    "accountId": "lisi",
    "accountName": "李四",
    "associatedId": "zhangsan",
    "companyId": "g09asd3qs3d8s",
    "companyName": "测试团队",
    "createTime": 1709863371382,
    "id": "cv7q7u8rnuksb",
    "remark": "创建账号:张三",
    "type": "CreateAccount",
    "updateTime": 1709863371382
  }
]
```

:::

## queryOptLogListCount

Query operation log count

```js
informat.system.queryOptLogListCount(filter)
```

**Parameters**

| Parameter     | Type                                      | Description   |
|--------|-----------------------------------------|------|
| filter | [Filter](/guide/script/model.md#filter) | Filter criteria |

Fields available in the filter

| Field        | Type       | Description   |
|-----------|----------|------|
| type      | `String` | Operation type |
| accountId | `String` | Operator |
| remark    | `String` | Remark   |

Available operation types:

| Operation Type                          | Description         |
|-------------------------------|------------|
| CreateAccount                 | Create account       |
| UpdateAccount                 | Update account       |
| Register                      | Register         |
| PasswordLogin                 | Password login     |
| WechatLogin                   | WeChat QR code login     |
| MobileNoLogin                 | Mobile verification code login    |
| DingTalkLogin                 | DingTalk auto-login      |
| WeWorkLogin                   | WeCom auto-login    |
| ssoLogin                      | SSO login      |
| Logout                        | Logout         |
| UpdateUserName                | Change login name      |
| UpdateNickName                | Change nickname       |
| UpdateMobileNo                | Change mobile number      |
| UpdateEmail                   | Change email       |
| SwitchCompany                 | Switch team       |
| InviteMember                  | Invite member       |
| DeleteMember                  | Remove member       |
| CreateDepartment              | Create department       |
| UpdateDepartment              | Edit department       |
| DeleteDepartment              | Delete department       |
| CreateRole                    | Create role       |
| UpdateRole                    | Edit role       |
| DeleteRole                    | Delete role       |
| CreateCompany                 | Create team       |
| CompanySetPro                 | Set trial       |
| CompanySetModule              | Set module       |
| CreateApp                     | Create application       |
| UpdateApp                     | Edit application       |
| DeleteApp                     | Delete application       |
| ArchiveApp                    | Archive application       |
| CreateAppMember               | Add application member     |
| UpdateAppMember               | Edit application member     |
| DeleteAppMember               | Delete application member     |
| UpdateAppMemberAccessPassword | Edit application member access password |
| CreateAppModule               | Add application module     |
| DeleteAppModule               | Delete application module     |
| DeleteRecycleBin              | Delete recycle bin data    |

**Return Value**

Type is `Integer`, operation log count

**Example**
:::code-group

```js [Call]
let filter = {
    conditionList: [
        { fieldId: 'type', opt: 'eq', value: 'CreateAccount' }
    ]
};
informat.system.queryOptLogListCount(filter);
```

```js[Return Value]
6
```

:::

## deleteOptLogList

Batch delete system logs

```js
informat.system.deleteOptLogList(filter)
```

**Parameters**

| Parameter     | Type                                      | Description   |
|--------|-----------------------------------------|------|
| filter | [Filter](/guide/script/model.md#filter) | Filter criteria |

Fields available in the filter

| Field         | Type       | Description   |
|------------|----------|------|
| type       | `String` | Operation type |
| accountId  | `String` | Operator |
| remark     | `String` | Remark   |
| createTime | `String` | Creation time |
| updateTime | `String` | Update time |

**Return Value**

Type is `Integer`, number of operation records deleted

**Example**
:::code-group

```js[Call]
let filter = {
    conditionList:[
        {fieldId:'type', opt: 'eq', value: 'CreateAccount'}
    ]
}
informat.system.deleteOptLogList(filter)
```

```js[Return Value]
6
```

:::

## runWithContext

Execute a script function across teams and applications

```js
informat.system.runWithContext(context, func)
```

**Parameters**

| Parameter      | Type                 | Description    |
|---------|--------------------|-------|
| context | [RunWithContext](/guide/script/model.md#runwithcontext) | Context configuration |
| func    | `Function`         | Function to execute |

`RunWithContext` structure:

| Parameter          | Type       | Description              |
|-------------|----------|-----------------|
| companyId   | `String` | Team ID. Defaults to the current team if not provided  |
| appDefineId | `String` | Application identifier. Defaults to the current application if not provided |

**Return Value**

Return value of the executed function

**Example**
:::code-group

```js[Call]
const addMember = () => {
    informat.user.addUser(informat.app.userId(), ['admin'])
    return true
}

let context = {
    companyId: 'xxxxxxxxxx',
    appDefineId: 'com.myApp'
}

informat.system.runWithContext(context, addMember)
```

```js[Return Value]
true
```

:::

## uploadFile

Upload a local file to shared storage. **Note: If a file with the same name exists, it will be overwritten**

```javascript
informat.system.uploadFile(localPath, remotePath)
```

**Parameters**

| Parameter         | Type     | Description     |
|------------|--------|--------|
| localPath  | String | Local file path |
| remotePath | String | Shared storage path |

**Return Value**

None

**Example**

```javascript
// Upload an avatar file. Avatar files need to be uploaded to the public directory
const localPath = 'local.png';
const remotePath = 'public/newAvatar.png';
informat.system.uploadFile(localPath, remotePath);
// Update user avatar
informat.system.updateAccount({
    id: 'ap1cew2up9ehq',
    avatar: 'newAvatar.png'
});
```

## setPasswordRule

Set password rules

```javascript
informat.system.setPasswordRule(reg)
```

**Parameters**

| Parameter  | Type     | Description          |
|-----|--------|-------------|
| reg | String | Password rule (regular expression) |

**Return Value**

None

**Example**

```javascript
// Password must be 7-20 characters combining numbers, letters, and special characters
informat.system.setPasswordRule('^w{7,20}$')
```

## executeAsync

Start a new thread to execute a task (asynchronous task execution)

```javascript
informat.system.executeAsync(func, arg)
```

**Parameters**

| Parameter              | Type       | Description            |
|-----------------|----------|---------------|
| func            | Function | Lambda function, cannot be null |
| arg             | Object   | Input parameter            |
| successCallback | Function | Success callback function, can be null |
| failedCallback  | Function | Failure callback function, can be null |

**Return Value**
None

**Example**

```javascript
function asyncTask(input) {
    console.log("asyncTask start: " + input);
    return informat.table.insert('dataModelBasics', {
        'singleText': input
    })
}

function successCallback(result) {
    console.log("asyncTask result: " + result);
    return informat.table.insert('dataModelBasics', {
        'singleText': 'success'
    })
}

function failedCallback(exception) {
    console.log("asyncTask exception: " + exception);
    return informat.table.insert('dataModelBasics', {
        'singleText': 'failed'
    })
}

informat.system.executeAsync(asyncTask, '123', successCallback, failedCallback)
```

## getTokenByAccount

Query login token by account ID and type

```javascript
informat.system.getTokenByAccount(accountId, type)
```

**Parameters**

| Parameter        | Type     | Description                     |
|-----------|--------|------------------------|
| accountId | String | Account ID                   |
| type      | String | Type. Available values: index, mobile |

**Return Value** [AccountToken](/guide/script/model.md#accounttoken)

**Example**

:::code-group

```javascript[Call]
let token = informat.system.getTokenByAccount('zhangsan', 'index');
console.log(token)
```

```json [Return Value]
{
  "accountId": "zhangsan",
  "companyId": "g09aj7cus3d8s",
  "createTime": 1744809507322,
  "dbIndex": 0,
  "expireTime": 1744827749095,
  "token": "b4b5013a483844c7b290808194f58418",
  "type": "index"
}
```

:::

## updateTokenExpireTime

Update the expiration time of an account login token

```javascript
informat.system.updateTokenExpireTime(token, expireTime)
```

**Parameters**

| Parameter         | Type     | Description   |
|------------|--------|------|
| token      | String | Login token |
| expireTime | Date   | Expiration time |

**Return Value**
None



## queryCompanySecurityApplyList

Query strict authorization control application record list

```js
informat.system.queryCompanySecurityApplyList(query)
```

**Parameters**

| Parameter    | Type                                    | Description   |
|-------|---------------------------------------|------|
| query | [Query](/guide/script/model.md#query) | Query criteria |

Fields available in the filter

| Field         | Type       | Description   |
|------------|----------|------|
| title  | `String` | Title |
| applyAccountId     | `String` | Applicant ID   |
| approveAccountId | `String` | Approver ID |
| status | `String` | Status (`applying` Pending; `agree` Approved; `refuse` Rejected; `cancel` Cancelled) |


**Return Value**

Type is Array<[CompanySecurityApply](/guide/script/model.md#companysecurityapply)>, strict authorization control application record list


## queryCompanySecurityApplyListCount

Query strict authorization control application record list count

```js
informat.system.queryCompanySecurityApplyListCount(filter)
```

**Parameters**

| Parameter     | Type                                      | Description   |
|--------|-----------------------------------------|------|
| filter | [Filter](/guide/script/model.md#filter) | Filter criteria |

Fields available in the filter

| Field         | Type       | Description   |
|------------|----------|------|
| title  | `String` | Title |
| applyAccountId     | `String` | Applicant ID   |
| approveAccountId | `String` | Approver ID |
| status | `String` | Status (`applying` Pending; `agree` Approved; `refuse` Rejected; `cancel` Cancelled) |



**Return Value**

Type is `Integer`, count
