# 匹配条件参考手册

## 条件结构

每个条件是一个 JSON 对象，至少包含 `type` 字段：

```json
{"type": "条件类型", "name": "...", "value": "...", "values": [...], "pattern": "...", "path": "..."}
```

不同条件类型需要不同的字段组合，详见下文。

## URL 条件 (5 种)

### urlEquals
URL 完全相等匹配。

```json
{"type": "urlEquals", "value": "https://example.com/api/users"}
```

### urlPrefix
URL 前缀匹配。

```json
{"type": "urlPrefix", "value": "https://api.example.com/"}
```

### urlSuffix
URL 后缀匹配。

```json
{"type": "urlSuffix", "value": ".png"}
```

### urlContains
URL 包含子串匹配。

```json
{"type": "urlContains", "value": "analytics"}
```

### urlRegex
URL 正则匹配。

```json
{"type": "urlRegex", "pattern": "^https://.*\\.example\\.com/api/.*$"}
```

## 请求元数据条件 (2 种)

### method
HTTP 方法匹配。`values` 不区分大小写。

```json
{"type": "method", "values": ["GET", "POST"]}
```

### resourceType
资源类型匹配。`values` 不区分大小写。

常用类型：`Document`、`XHR`、`Fetch`、`Script`、`Stylesheet`、`Image`、`Font`、`Media`、`WebSocket`

```json
{"type": "resourceType", "values": ["XHR", "Fetch"]}
```

## Header 条件 (5 种)

所有 Header 名称匹配**不区分大小写**。

### headerExists
Header 存在。

```json
{"type": "headerExists", "name": "Authorization"}
```

### headerNotExists
Header 不存在。

```json
{"type": "headerNotExists", "name": "X-Custom-Token"}
```

### headerEquals
Header 值完全相等。

```json
{"type": "headerEquals", "name": "Content-Type", "value": "application/json"}
```

### headerContains
Header 值包含子串。

```json
{"type": "headerContains", "name": "Accept", "value": "json"}
```

### headerRegex
Header 值正则匹配。

```json
{"type": "headerRegex", "name": "Authorization", "pattern": "^Bearer\\s+.+"}
```

## Query 参数条件 (5 种)

### queryExists
URL 中存在指定 Query 参数。

```json
{"type": "queryExists", "name": "page"}
```

### queryNotExists
URL 中不存在指定 Query 参数。

```json
{"type": "queryNotExists", "name": "debug"}
```

### queryEquals
Query 参数值完全相等。

```json
{"type": "queryEquals", "name": "page", "value": "1"}
```

### queryContains
Query 参数值包含子串。

```json
{"type": "queryContains", "name": "q", "value": "搜索词"}
```

### queryRegex
Query 参数值正则匹配。

```json
{"type": "queryRegex", "name": "id", "pattern": "^\\d+$"}
```

## Cookie 条件 (5 种)

从请求 Header 中的 `Cookie` 字段解析。

### cookieExists
Cookie 名称存在。

```json
{"type": "cookieExists", "name": "session"}
```

### cookieNotExists
Cookie 名称不存在。

```json
{"type": "cookieNotExists", "name": "tracking_id"}
```

### cookieEquals
Cookie 值完全相等。

```json
{"type": "cookieEquals", "name": "session", "value": "abc123"}
```

### cookieContains
Cookie 值包含子串。（注意：Cookie 值是区分大小写的）

```json
{"type": "cookieContains", "name": "token", "value": "eyJ"}
```

### cookieRegex
Cookie 值正则匹配。

```json
{"type": "cookieRegex", "name": "token", "pattern": "^[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+$"}
```

## Body 条件 (3 种)

仅适用于有请求体 (POST/PUT/PATCH) 的请求。

### bodyContains
请求体包含子串。

```json
{"type": "bodyContains", "value": "password"}
```

### bodyRegex
请求体正则匹配。

```json
{"type": "bodyRegex", "pattern": "\"username\":\\s*\"[^\"]+\""}
```

### bodyJsonPath
请求体 JSON 路径匹配。路径格式为 `/` 分隔的简单路径（非标准 JSONPath）。
- `/key` — 对象属性
- `/key/sub` — 嵌套对象
- `/array/0` — 数组索引
- `""` — 整个 JSON 根对象

值比较使用字符串相等。布尔值写作 `"true"`/`"false"`，null 写作 `"null"`。

```json
{"type": "bodyJsonPath", "path": "/user/name", "value": "admin"}
{"type": "bodyJsonPath", "path": "/data/items/0/id", "value": "42"}
{"type": "bodyJsonPath", "path": "/ok", "value": "true"}
```

## 逻辑组合

### allOf（AND 逻辑）
所有条件都满足才匹配。

```json
{
  "allOf": [
    {"type": "urlContains", "value": "/api/"},
    {"type": "method", "values": ["POST"]},
    {"type": "headerExists", "name": "Authorization"}
  ]
}
```

### anyOf（OR 逻辑）
任意一个条件满足即匹配。

```json
{
  "anyOf": [
    {"type": "urlContains", "value": "analytics"},
    {"type": "urlContains", "value": "tracking"}
  ]
}
```

### 同时使用
allOf 和 anyOf 可同时指定。allOf 和 anyOf 都必须满足（即 allOf 的 AND 结果和 anyOf 的 OR 结果取 AND）。

```json
{
  "allOf": [
    {"type": "resourceType", "values": ["XHR"]}
  ],
  "anyOf": [
    {"type": "urlContains", "value": "/api/v1/"},
    {"type": "urlContains", "value": "/api/v2/"}
  ]
}
```
以上规则匹配：资源类型为 XHR **并且** URL 包含 `/api/v1/` 或 `/api/v2/` 的请求。

### 空匹配
如果 `allOf` 和 `anyOf` 都为空数组，则匹配**所有**请求。
