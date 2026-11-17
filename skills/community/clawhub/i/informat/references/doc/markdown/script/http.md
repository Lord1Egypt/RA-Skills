# informat.http HTTP Request

## Overview

Use the `informat.http` object to make HTTP network requests. After making a unified informat.http.request call, you get a response object.

::: info

- Since network fluctuations or service exceptions on the called party's side may cause request failures, such as common HTTP status codes like 404, 502, etc.,
  please first check the corresponding status code before proceeding with subsequent business logic.
- Some services may redirect to another URL after being called. In such cases, you can set the followRedirect property in the request object to true to automatically redirect to the actual URL, or handle the redirect in your business code.
  :::

## request

Send a request

```javascript
informat.http.request(request)
```

| Parameter | Type                                           | Description    |
|-----------|--------------------------------------------|----------------|
| request   | [HttpRequest](/guide/script/model.md#httprequest) | Request object |

**Return Value**
Type [HttpResponse](/guide/script/http.md#response)
Returns the content of the HTTP request

**Example**

```js
const req = {
    url: 'https://demo.api.com/api',
    method: 'POST',
    timeout: 1000,
    form: {
        'p1': 1,
        'p2': 'str'
    }
}
informat.http.request(req)
```

## Response

### statusCode

HTTP status code

```js
response.statusCode()
```

**Return Value**

Type `Integer`

### body

Content

```js
response.body()
```

**Return Value**

Type `String`

### headers

Get HTTP response headers

```js
response.headers()
```

**Return Value**

Type `Object<String,String>`

### contentEncoding

Content encoding of the response

```js
response.contentEncoding()
```

**Return Value**

Type `String`

### contentLength

Content length of the response

```js
response.contentLength()
```

**Return Value**

Type `Integer`

### saveBodyAsFile

Save file to local storage

```js
response.saveBodyAsFile(path)
```

| Parameter | Type     | Description  |
|-----------|----------|--------------|
| path      | `String` | Storage path |

### saveBodyAsStorage

Save file to shared storage

```js
response.saveBodyAsStorage(path)
```

| Parameter | Type     | Description  |
|-----------|----------|--------------|
| path      | `String` | Storage path |

### saveBodyAsAttachment

Save as attachment object

```js
response.saveBodyAsAttachment(tableKey, fieldKey, fileName)
```

| Parameter | Type     | Description          |
|-----------|----------|----------------------|
| tableKey  | `String` | Data table identifier |
| fieldKey  | `String` | Field identifier      |
| fileName  | `String` | File name             |

## Examples

### Example 1: Making a POST request

```js
const req = {
    url: 'https://demo.api.com/api',
    method: 'POST',
    timeout: 1000,
    form: {
        'p1': 1,
        'p2': 'str'
    }
}
const rsp = informat.http.request(req);
console.log(rsp.body());// Request result
```

### Example 2: Making a GET request

::: code-group

```javascript [Call Example 1]
const req = {
    url: 'https://demo.api.com/api?a=zhangsan&b=lisi',
    method: 'GET',
    timeout: 1000,
}
const ctx = informat.http.request(req)
console.log(ctx.body(), '....') // Request result
```

```javascript [Call Example 2]
const req = {
    url: 'https://demo.api.com/api',
    method: 'GET',
    timeout: 1000,
    form: {
        a: 'zhangsan',
        b: 'lisi'
    }
}
const ctx = informat.http.request(req)
console.log(ctx.body(), '....') // Request result
```

:::

### Example 3: Download a remote file and save to the local sandbox environment

```js
const req = {
    url: 'https://next.informat.cn/logo.png',
    followRedirect: true,
    maxRedirectCount: 10,
}
const rsp = informat.http.request(req);
rsp.saveBodyAsFile('logo.png');
```

### Example 4: Download a remote file and save to S3 shared storage

```js
const req = {
    url: 'https://next.informat.cn/logo.png',
    followRedirect: true,
    maxRedirectCount: 10,
}
const rsp = informat.http.request(req);
rsp.saveBodyAsStorage('logo.png');
```

### Example 5: Call a request, upload the file to shared storage, and save as an attachment object

```js
let req = {
    url: 'https://demo.api.com/api',
    followRedirect: true,
    maxRedirectCount: 10,
};
let rsp = informat.http.request(req);
const attachment = rsp.saveBodyAsAttachment('tableKey', 'fieldKey', 'demo.png');
// After saving as attachment, you can perform operations such as update data, insert data, etc. (tableKey and fieldKey must be consistent)
const insertBean = {
    name: 'demo name',
    attachment: attachment,  // If multi-select, wrap with [] e.g.: attachment: [attachment]
};
// Call the insert data API
informat.table.insert('tableKey', insertBean);
```

### Example 6: Upload a sandbox environment file to a third-party API

```js
const req = {
    url: 'https://demo.api.com/api',
    method: 'POST',
    timeout: 5000,
    files: {
        file: 'demo.jpg'
    }
}
const resp = informat.http.request(req);
console.log(resp.statusCode());
console.log(resp.body());
```

### Example 7: Upload a shared storage file to a third-party API

```js
const req = {
    url: 'https://demo.api.com/api',
    method: 'POST',
    timeout: 5000,
    storages: {
        file: 'demo.jpg'
    }
}
const resp = informat.http.request(req);
console.log(resp.statusCode());
console.log(resp.body());
```
