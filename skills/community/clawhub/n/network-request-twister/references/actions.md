# 动作参考手册

## 目录

- [通用规则](#通用规则)
- [请求阶段动作 (request)](#请求阶段动作-request)
  - [block](#block)
  - [setHeader](#setheader)
  - [removeHeader](#removeheader)
  - [setUrl](#seturl)
  - [setMethod](#setmethod)
  - [setQueryParam](#setqueryparam)
  - [removeQueryParam](#removequeryparam)
  - [setCookie](#setcookie)
  - [removeCookie](#removecookie)
  - [setFormField](#setformfield)
  - [removeFormField](#removeformfield)
  - [setBody（请求阶段）](#setbody请求阶段)
  - [appendBody（请求阶段）](#appendbody请求阶段)
  - [replaceBodyText（请求阶段）](#replacebodytext请求阶段)
  - [patchBodyJson（请求阶段）](#patchbodyjson请求阶段)
- [响应阶段动作 (response)](#响应阶段动作-response)
  - [setStatus](#setstatus)
  - [setBody（响应阶段）](#setbody响应阶段)
  - [appendBody（响应阶段）](#appendbody响应阶段)
  - [replaceBodyText（响应阶段）](#replacebodytext响应阶段)
  - [patchBodyJson（响应阶段）](#patchbodyjson响应阶段)
  - [replaceElement](#replaceelement)
  - [setCookie（响应阶段）](#setcookie响应阶段)
  - [removeCookie（响应阶段）](#removecookie响应阶段)
- [跨阶段动作](#跨阶段动作)
- [JSON Patch 操作速查](#json-patch-操作速查)

## 通用规则

- 动作按数组顺序依次执行
- 如果某个动作返回 `handled = true`（如 `block`、`setUrl` 等直接完成请求的动作），后续动作不再执行
- 动作执行失败不会导致整个规则失败，会记录错误日志并继续执行后续动作
- `stage` 决定动作在哪个阶段生效：`request` 阶段的动作修改发往服务器的内容，`response` 阶段的动作修改返回给浏览器的内容

---

## 请求阶段动作 (request)

### block
拦截请求，返回自定义响应。**这是唯一真正阻止请求发送到服务器的动作。**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `statusCode` | int | 200 | 返回的状态码 |
| `headers` | object | {} | 返回的响应头 |
| `body` | string | "" | 返回的响应体 |
| `bodyEncoding` | string | "text" | 编码方式（"text" 或 "base64"） |

```json
// 静默拦截
{"type": "block", "statusCode": 204}

// 返回自定义响应
{
  "type": "block",
  "statusCode": 200,
  "headers": {"Content-Type": "application/json"},
  "body": "{\"blocked\": true}"
}
```

block 动作使用 CDP `Fetch.fulfillRequest`，请求不会发送到服务器。

### setHeader
设置或覆盖请求头。如果 Header 已存在，覆盖其值；如果不存在，添加。

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | Header 名称 |
| `value` | string | Header 值 |

```json
{"type": "setHeader", "name": "Authorization", "value": "Bearer fake-token"}
{"type": "setHeader", "name": "X-Custom-Header", "value": "custom-value"}
```

### removeHeader
删除请求头。

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | 要删除的 Header 名称 |

```json
{"type": "removeHeader", "name": "Referer"}
{"type": "removeHeader", "name": "X-Tracking-ID"}
```

### setUrl
修改请求 URL。

| 参数 | 类型 | 说明 |
|------|------|------|
| `value` | string | 新的完整 URL |

```json
{"type": "setUrl", "value": "https://other-server.com/api/endpoint"}
```

### setMethod
修改 HTTP 方法。

| 参数 | 类型 | 说明 |
|------|------|------|
| `value` | string | 新方法（GET、POST、PUT、DELETE 等） |

```json
{"type": "setMethod", "value": "POST"}
```

### setQueryParam
设置或覆盖 URL Query 参数。

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | 参数名 |
| `value` | string | 参数值 |

```json
{"type": "setQueryParam", "name": "page", "value": "1"}
{"type": "setQueryParam", "name": "token", "value": "abc123"}
```

### removeQueryParam
删除 URL Query 参数。

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | 参数名 |

```json
{"type": "removeQueryParam", "name": "utm_source"}
{"type": "removeQueryParam", "name": "debug"}
```

### setCookie
设置或覆盖请求 Cookie（修改 Cookie 请求头）。

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | Cookie 名称 |
| `value` | string | Cookie 值 |

```json
{"type": "setCookie", "name": "session", "value": "fake-session-id"}
```

### removeCookie
删除请求 Cookie。

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | Cookie 名称 |

```json
{"type": "removeCookie", "name": "tracking_id"}
```

### setFormField
设置或覆盖表单字段（支持 application/x-www-form-urlencoded 和 multipart/form-data）。

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | 字段名 |
| `value` | string | 字段值 |

```json
{"type": "setFormField", "name": "username", "value": "admin"}
```

### removeFormField
删除表单字段。

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | 字段名 |

```json
{"type": "removeFormField", "name": "csrf_token"}
```

### setBody（请求阶段）
替换请求体。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `value` | string | 必填 | 新的请求体内容 |
| `body` | string | "" | 同上（优先级更高） |
| `encoding` | string | "text" | 编码方式 |

```json
{"type": "setBody", "value": "{\"username\":\"test\",\"password\":\"123\"}"}
```

如果 `value` 以 `{` 或 `[` 开头且原请求没有 `Content-Type: ...json`，会自动添加 `Content-Type: application/json`。

### appendBody（请求阶段）
在请求体末尾追加内容。

| 参数 | 类型 | 说明 |
|------|------|------|
| `value` | string | 追加的内容 |

```json
{"type": "appendBody", "value": "&extra_param=1"}
```

### replaceBodyText（请求阶段）
在请求体中查找替换文本。默认只替换第一次出现。

| 参数 | 类型 | 说明 |
|------|------|------|
| `search` | string | 查找的文本 |
| `replace` | string | 替换为的文本 |
| `replaceAll` | bool | 是否替换所有出现（默认 false） |

```json
{"type": "replaceBodyText", "search": "old_value", "replace": "new_value"}
{"type": "replaceBodyText", "search": "http://", "replace": "https://", "replaceAll": true}
```

### patchBodyJson（请求阶段）
对 JSON 请求体执行 RFC 6902 JSON Patch 操作。

| 参数 | 类型 | 说明 |
|------|------|------|
| `patches` | array | JSON Patch 操作数组 |

```json
{
  "type": "patchBodyJson",
  "patches": [
    {"op": "replace", "path": "/user/name", "value": "admin"},
    {"op": "add", "path": "/user/role", "value": "superuser"},
    {"op": "remove", "path": "/metadata"}
  ]
}
```

---

## 响应阶段动作 (response)

### setStatus
修改响应状态码。**仅在 response 阶段有效。**

| 参数 | 类型 | 说明 |
|------|------|------|
| `statusCode` | int | 新的状态码 |

```json
{"type": "setStatus", "statusCode": 500}
{"type": "setStatus", "statusCode": 404}
```

**注意：** 此动作会使用 `Fetch.fulfillRequest` 返回新响应，原响应体会丢失。如需保留响应体，改用 `setBody`。

### setBody（响应阶段）
替换响应体。

```json
{"type": "setBody", "value": "{\"mocked\": true, \"data\": []}"}
```

### appendBody（响应阶段）
在响应体末尾追加内容。

```json
{"type": "appendBody", "value": "<script>console.log('injected')</script>"}
```

### replaceBodyText（响应阶段）
在响应体中查找替换文本。

```json
{"type": "replaceBodyText", "search": "http://", "replace": "https://", "replaceAll": true}
{"type": "replaceBodyText", "search": "旧文案", "replace": "新文案"}
```

### patchBodyJson（响应阶段）
对 JSON 响应体执行 JSON Patch 操作。

```json
{
  "type": "patchBodyJson",
  "patches": [
    {"op": "replace", "path": "/status", "value": "ok"},
    {"op": "add", "path": "/injected", "value": true}
  ]
}
```

### replaceElement
使用 CSS 选择器替换 HTML 响应中的元素。**仅在 response 阶段有效。**

| 参数 | 类型 | 说明 |
|------|------|------|
| `selector` | string | CSS 选择器（支持所有 CSS3 选择器） |
| `value` | string | 替换的 HTML 内容 |

```json
// 替换 id 为 "header" 的元素
{"type": "replaceElement", "selector": "#header", "value": "<nav>新导航</nav>"}

// 替换所有 .ad-banner 元素为空
{"type": "replaceElement", "selector": ".ad-banner", "value": ""}

// 在 <head> 中注入脚本
{"type": "replaceElement", "selector": "head", "value": "<script>alert('injected')</script>"}
```

**CSS 选择器示例：**
- `div` — 标签选择器
- `.class-name` — 类选择器
- `#id-name` — ID 选择器
- `input[name="email"]` — 属性选择器
- `div > p` — 子代选择器
- `ul li:first-child` — 伪类选择器

### setCookie（响应阶段）
在响应中添加或覆盖 Set-Cookie 头。

```json
{"type": "setCookie", "name": "session", "value": "new-session-id"}
```

### removeCookie（响应阶段）
从响应中删除 Set-Cookie 头。

```json
{"type": "removeCookie", "name": "tracking_cookie"}
```

---

## 跨阶段动作

以下动作在 request 和 response 阶段均可用，行为因阶段而异：

| 动作 | request 阶段 | response 阶段 |
|------|-------------|---------------|
| `setCookie` | 修改请求 Cookie 头 | 修改响应 Set-Cookie 头 |
| `removeCookie` | 删除请求 Cookie 头 | 删除响应 Set-Cookie 头 |
| `setBody` | 替换请求体 | 替换响应体 |
| `appendBody` | 追加到请求体 | 追加到响应体 |
| `replaceBodyText` | 替换请求体中文本 | 替换响应体中文本 |
| `patchBodyJson` | JSON Patch 请求体 | JSON Patch 响应体 |

---

## JSON Patch 操作速查

全部 6 种 RFC 6902 操作均支持：

| 操作 | 说明 | 必填字段 |
|------|------|----------|
| `add` | 添加值到指定路径 | op, path, value |
| `remove` | 删除指定路径的值 | op, path |
| `replace` | 替换指定路径的值 | op, path, value |
| `move` | 移动值到新路径 | op, from, path |
| `copy` | 复制值到新路径 | op, from, path |
| `test` | 测试值是否匹配，不匹配则抛出异常 | op, path, value |

路径格式：`/` 分隔，数组用数字索引。例如 `/users/0/name`。
