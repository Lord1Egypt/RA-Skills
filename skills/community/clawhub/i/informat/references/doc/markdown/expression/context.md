# Context

## Overview

Context-related functions. Context represents the environment parameters during execution.


## userId

Returns the user ID of the current operation

```javascript
Context.userId()
```

**Return Value**

Type `String`
The current operation user

**Example**

```javascript
Context.userId() //ek5veueb6c9zg
```

::: tip
The context user only has a value when the operation is initiated by a user. For example, during `scheduled task execution` or `API` access, the operation user is `null`
:::

## appId

Returns the current application ID

```javascript
Context.appId()
```

**Return Value**

Type `String`
Current application ID

**Example**

```javascript
Context.appId() 
```


## appEnvProp

Returns the environment variable of the current application

```javascript
Context.appEnvProp(propKey)
```

| Parameter | Type | Description |
|---------|--------|----------|
| propKey | `String` | Key of the environment variable |

**Return Value**

Type `String`
Value of the environment variable

**Example**

Assuming the application has the following environment variables configured:

| Environment | Variable Identifier | Variable Value |
|-----|--------|-------------------------|
| dev | payURL | http://dev-demo.com/pay |
| prd | payURL | http://prd-demo.com/pay |

```javascript
//When called in dev environment
Context.appEnvProp('payURL')//http://dev-demo.com/pay 
```

::: warning Notes
When used on the `client side`, only environment variables that are set to allow client access can be accessed. There is no such restriction on the `server side`.
:::

## httpHeaders

Returns the HTTP headers of the current operation

```javascript
Context.httpHeaders()
```


**Return Value**

Type `Object`
HTTP header values

**Example**
:::: tabs
::: tab "Call"
```javascript
Context.httpHeaders()
```
:::

::: tab "Return Value"
```json
{
    "host" : "uat2.informat.cn", 
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", 
    "sec-fetch-dest" : "empty"
} 
```
:::
::::

::: tip
If the operation is not triggered by a user (e.g., scheduled tasks, event handlers), httpHeaders returns `{}`
:::

## clipboardType

Returns the data type stored in the current application clipboard

```javascript
Context.clipboardType()
```

**Return Value**

Type `String`
Data type stored in the application clipboard

**Example**

```javascript
Context.clipboardType() //test
```

::: tip The application clipboard needs to be set through the following operations
- Automation step `Set Application Clipboard`
- Widget `Set Application Clipboard Data`
:::


## clipboardData

Returns the data stored in the current application clipboard

```javascript
Context.clipboardData()
```

**Return Value**

Type `Object`
Data stored in the application clipboard


## weworkAccessToken

Returns the WeCom AccessToken

```javascript
Context.weworkAccessToken()
```

**Return Value**

Type `String`
WeCom AccessToken

## dingtalkAccessToken

Returns the DingTalk AccessToken

```javascript
Context.dingtalkAccessToken()
```

**Return Value**

Type `String`
DingTalk AccessToken

## feishuAccessToken

Returns the Feishu App AccessToken

```javascript
Context.feishuAccessToken()
```

**Return Value**

Type `String`
Feishu App AccessToken

## feishuTenantAccessToken

Returns the Feishu Tenant AccessToken

```javascript
Context.feishuTenantAccessToken()
```

## requestIp

Returns the IP information of the current request

```javascript
Context.requestIp()
```

**Return Value**

Type `String`
IP information of the current request

## hasAppPerm

Determines whether the current user has the application permission with identifier permKey

```javascript
Context.hasAppPerm(permKey)
```

| Parameter | Type | Description |
|----|----------|--------------------------------------------------------|
|permKey| `String` | Permission identifier |

**Return Value**

Type `Boolean`
Whether the user has the application permission

## hasModulePerm

Determines whether the current user has the module permission with module identifier moduleKey and permission identifier permKey

```javascript
Context.hasModulePerm(moduleKey, permKey);
```

| Parameter | Type | Description |
|----|----------|--------------------------------------------------------|
|moduleKey| `String` | Module identifier |
|permKey| `String` | Permission identifier |


**Return Value**

Type `Boolean`
Whether the user has the module permission

## getModuleIdByKey

Gets the module ID by module identifier

```javascript
Context.getModuleIdByKey(moduleKey)
```

| Parameter | Type | Description |
|----------|----------|---------|
| moduleKey | `String` | Module identifier |

**Return Value**

Type `String`
Module ID, returns `null` if the module does not exist

**Example**

```javascript
Context.getModuleIdByKey('order') // "m1234567890"
```

## getModuleKeyById

Gets the module identifier by module ID

```javascript
Context.getModuleKeyById(moduleId)
```

| Parameter | Type | Description |
|----------|----------|-------|
| moduleId | `String` | Module ID |

**Return Value**

Type `String`
Module identifier, returns `null` if the module does not exist

**Example**

```javascript
Context.getModuleKeyById('m1234567890') // "order"
```
