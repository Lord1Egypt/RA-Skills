# HTTP 网络请求

> 来源：华为开发者文档 - 使用HTTP访问网络（2026-04-20）
> https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/http-request

## 概述

HTTP 模块提供标准的 HTTP 网络服务能力，支持 GET/POST/HEAD/PUT/DELETE/TRACE/CONNECT/OPTIONS 方法。

从 API version 22 起支持 **HTTP 拦截器**，可在请求-响应生命周期中插入自定义逻辑。

## 基础请求

```typescript
import http from '@ohos.net.http';

// 创建 HTTP 请求任务
let httpRequest = http.createHttp();

// 发起请求
httpRequest.request(
  'https://api.example.com/data',
  {
    method: http.RequestMethod.GET,       // 默认 GET
    header: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer token'
    },
    connectTimeout: 60000,                  // 连接超时（ms）
    readTimeout: 60000,                   // 读取超时（ms）
    expectDataType: http.HttpDataType.STRING  // 响应数据类型
  },
  (err, data) => {
    if (err) {
      console.error(`请求失败: ${err.message}`);
      return;
    }
    if (data.responseCode === 200) {
      console.info(`响应: ${data.result}`);
    }
  }
);

// 请求完成销毁
httpRequest.destroy();
```

## 常用请求方法

```typescript
// GET 请求
async function fetchData() {
  let httpRequest = http.createHttp();
  const result = await httpRequest.request(
    'https://api.example.com/users/123',
    {
      method: http.RequestMethod.GET,
      header: { 'Accept': 'application/json' }
    }
  );
  console.info(`状态: ${result.responseCode}, 数据: ${result.result}`);
  httpRequest.destroy();
  return result;
}

// POST 请求（JSON body）
async function postData() {
  let httpRequest = http.createHttp();
  const result = await httpRequest.request(
    'https://api.example.com/users',
    {
      method: http.RequestMethod.POST,
      header: {
        'Content-Type': 'application/json'
      },
      extraData: JSON.stringify({ name: 'Alice', age: 30 })
    }
  );
  if (result.responseCode === 201) {
    console.info('创建成功');
  }
  httpRequest.destroy();
  return result;
}

// PUT 请求
async function updateData() {
  let httpRequest = http.createHttp();
  const result = await httpRequest.request(
    'https://api.example.com/users/123',
    {
      method: http.RequestMethod.PUT,
      header: { 'Content-Type': 'application/json' },
      extraData: JSON.stringify({ name: 'Bob' })
    }
  );
  httpRequest.destroy();
  return result;
}

// DELETE 请求
async function deleteData() {
  let httpRequest = http.createHttp();
  const result = await httpRequest.request(
    'https://api.example.com/users/123',
    { method: http.RequestMethod.DELETE }
  );
  httpRequest.destroy();
  return result;
}
```

## 请求选项（HttpRequestOptions）

| 选项 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| method | RequestMethod | 请求方法 | GET |
| header | Object | 请求头 | — |
| extraData | string/Object | 请求体数据 | — |
| connectTimeout | number | 连接超时（ms）| 60000 |
| readTimeout | number | 读取超时（ms）| 60000 |
| expectDataType | HttpDataType | 期望响应类型：STRING/OBJECT/ARRAY_BUFFER | STRING |
| usingProtocol | HttpProtocol | HTTP 协议版本 | HTTP_1_1 |

## 响应数据结构

```typescript
// HttpResponse 结果
{
  responseCode: number;       // HTTP 状态码（200/404/500 等）
  result: string | Object | ArrayBuffer;  // 响应体（类型由 expectDataType 决定）
  header: Object;             // 响应头
  message: string;            // 状态消息
  cookies: string;            // cookies
}

// 响应头示例
{
  'Content-Type': 'application/json',
  'Date': 'Wed, 22 Apr 2026 00:00:00 GMT',
  'Content-Length': '1234'
}
```

## HTTP 拦截器（API v22+）

拦截器可以在请求发送前和响应到达后插入自定义逻辑：

```typescript
import http from '@ohos.net.http';

// 创建带拦截器的 HTTP 请求
let httpRequest = http.createHttp();

// 添加请求拦截器（在请求发送前调用）
httpRequest.on('requestIntercept', (request) => {
  // 修改请求
  request.header['Authorization'] = `Bearer ${getToken()}`;
  request.extraData = { ...request.extraData, ts: Date.now() };
  return request;  // 返回修改后的请求
});

// 添加响应拦截器（在响应到达后调用）
httpRequest.on('responseIntercept', (response) => {
  // 处理响应
  if (response.responseCode === 401) {
    // Token 过期，跳转登录
    router.pushUrl({ url: 'pages/Login' });
  }
  return response;  // 返回处理后的响应
});

// 发起请求
httpRequest.request(url, options, (err, data) => {
  // ...
});
```

## 文件上传下载

```typescript
// 大文件下载（流式传输）
async function downloadFile(url: string, filePath: string) {
  let httpRequest = http.createHttp();
  
  let file = fs.openSync(filePath, fs.OpenMode.WRITE_ONLY);
  
  httpRequest.requestInStream(url, {
    method: http.RequestMethod.GET,
  }, (err, data) => {
    if (err) {
      console.error(`下载失败: ${err.message}`);
    } else {
      // data 为分块数据，需要自己拼接
      // 使用 request + fs 实现完整下载
    }
    fs.closeSync(file);
    httpRequest.destroy();
  });
}

// 使用 request 下载文件
async function downloadFile2(url: string, savePath: string) {
  let httpRequest = http.createHttp();
  
  const response = await httpRequest.request(url, {
    method: http.RequestMethod.GET,
  });
  
  if (response.responseCode === 200) {
    let file = fs.openSync(savePath, fs.OpenMode.WRITE_ONLY | fs.OpenMode.CREATE);
    fs.writeSync(file.fd, response.result as ArrayBuffer);
    fs.closeSync(file);
  }
  
  httpRequest.destroy();
}
```

## 证书配置

```typescript
// TLS 客户端证书验证
httpRequest.request(url, {
  method: http.RequestMethod.GET,
  certificate: {
    certPath: '/path/to/cert.pem',       // 客户端证书路径
    certType: http.CertType.P12,          // 证书类型：P12 / PEM / etc
    keyPath: '/path/to/key.pem',         // 私钥路径（可选）
    keyPassword: 'password'               // 私钥密码（可选）
  }
});

// 证书锁定（Certificate Pinning）
// 通过设置 caPath 只信任特定 CA
httpRequest.request(url, {
  method: http.RequestMethod.GET,
  caPath: '/path/to/ca.pem'             // 受信任的 CA 证书路径
});
```

## WebSocket

```typescript
import webSocket from '@ohos.net.webSocket';

// 创建 WebSocket 连接
let ws = webSocket.createWebSocket();
ws.on('open', (err, value) => {
  console.info('WebSocket 连接已打开');
  ws.send('Hello Server');
});

ws.on('message', (err, value) => {
  console.info(`收到消息: ${value}`);
  if (value === 'close') {
    ws.close();
  }
});

ws.on('close', (err, value) => {
  console.info(`WebSocket 关闭: code=${value.code}, reason=${value.reason}`);
});

ws.on('error', (err) => {
  console.error(`WebSocket 错误: ${err.message}`);
});

// 建立连接
ws.connect('wss://echo.websocket.org', (err, value) => {
  if (err) {
    console.error(`连接失败: ${err.message}`);
  }
});

// 关闭连接
ws.close();
```

## Cookie 管理

```typescript
// 启用 Cookie
httpRequest.request(url, {
  method: http.RequestMethod.GET,
  usingCookie: true   // 启用 Cookie 自动管理
});
```

## DNS 解析

```typescript
import dns from '@ohos.net.connection';

// 获取域名 IP
dns.getAddressesByName('api.example.com', (err, addresses) => {
  if (err) {
    console.error(`DNS 解析失败: ${err.message}`);
    return;
  }
  console.info(`IP地址: ${JSON.stringify(addresses)}`);
});
```

## 常见错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 301/302 | 重定向 |
| 400 | 请求参数错误 |
| 401 | 未授权（Token 失效）|
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |
| 502 | 网关错误 |
| 504 | 网关超时 |
