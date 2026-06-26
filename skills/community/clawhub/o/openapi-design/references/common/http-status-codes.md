# HTTP Status Codes

## 2xx Success

| Code | 含义 | 使用场景 |
|------|------|----------|
| **200** | OK | 成功查询（GET）、更新（PUT/PATCH） |
| **201** | Created | 成功创建资源（POST） |
| **202** | Accepted | 异步请求已接受（不立即完成） |
| **204** | No Content | 成功删除（DELETE），无返回体 |

### 典型响应

```json
// 200 OK - 查询成功
{
  "data": { "userId": 123, "userName": "John" }
}

// 201 Created - 创建成功
{
  "data": { "userId": 456, "userName": "Jane" },
  "message": "User created successfully"
}

// 204 No Content - 删除成功
// (无响应体)
```

---

## 3xx Redirection

| Code | 含义 | 使用场景 |
|------|------|----------|
| **301** | Moved Permanently | 资源永久移动到新地址 |
| **302** | Found | 临时重定向（非 POST 请求） |
| **303** | See Other | POST 后重定向到 GET |
| **304** | Not Modified | 缓存未变更（配合 ETag） |

**注意**：API 尽量避免使用 3xx，客户端应直接访问正确地址。

---

## 4xx Client Error

| Code | 含义 | 使用场景 |
|------|------|----------|
| **400** | Bad Request | 请求格式错误、参数验证失败 |
| **401** | Unauthorized | 未认证（未提供或无效 token） |
| **403** | Forbidden | 已认证但无权限 |
| **404** | Not Found | 资源不存在 |
| **405** | Method Not Allowed | HTTP 方法不支持 |
| **409** | Conflict | 资源冲突（如重复创建） |
| **410** | Gone | 资源已永久删除 |
| **422** | Unprocessable Entity | 请求格式正确但语义错误 |
| **429** | Too Many Requests | 请求频率超限 |

### 典型响应

```json
// 400 Bad Request
{
  "error": {
    "code": "VAL_001",
    "message": "Validation failed",
    "details": [
      { "field": "email", "message": "Invalid email format" },
      { "field": "age", "message": "Must be a positive integer" }
    ]
  }
}

// 401 Unauthorized
{
  "error": {
    "code": "AUTH_001",
    "message": "Authentication required"
  }
}

// 403 Forbidden
{
  "error": {
    "code": "PERM_001",
    "message": "Insufficient permissions"
  }
}

// 404 Not Found
{
  "error": {
    "code": "RES_001",
    "message": "User not found"
  }
}

// 429 Too Many Requests
{
  "error": {
    "code": "RATE_001",
    "message": "Rate limit exceeded"
  },
  "headers": {
    "X-RateLimit-Limit": "100",
    "X-RateLimit-Remaining": "0",
    "X-RateLimit-Reset": "1704009600"
  }
}
```

---

## 5xx Server Error

| Code | 含义 | 使用场景 |
|------|------|----------|
| **500** | Internal Server Error | 服务器内部错误（不暴露细节） |
| **502** | Bad Gateway | 上游服务错误 |
| **503** | Service Unavailable | 服务暂时不可用 |
| **504** | Gateway Timeout | 上游服务超时 |

### 典型响应

```json
// 500 Internal Server Error
{
  "error": {
    "code": "SYS_001",
    "message": "An internal error occurred",
    "requestId": "req_abc123"
  }
}
```

---

## 状态码选择指南

### 创建资源
- **201** — 成功创建
- **400** — 请求参数错误
- **401** — 未认证
- **409** — 资源已存在冲突

### 查询资源
- **200** — 成功
- **401** — 未认证
- **404** — 资源不存在

### 更新资源
- **200** — 成功更新
- **400** — 请求参数错误
- **401** — 未认证
- **403** — 无权限
- **404** — 资源不存在
- **409** — 版本冲突

### 删除资源
- **204** — 成功删除（无返回体）
- **200** — 成功删除（返回删除的资源）
- **401** — 未认证
- **403** — 无权限
- **404** — 资源不存在

---

## Rate Limit 相关 Header

| Header | 含义 |
|--------|------|
| `X-RateLimit-Limit` | 请求速率上限 |
| `X-RateLimit-Remaining` | 剩余请求次数 |
| `X-RateLimit-Reset` | 速率限制重置时间（Unix timestamp） |
| `Retry-After` | 距离下次可请求的秒数（429 时返回） |
