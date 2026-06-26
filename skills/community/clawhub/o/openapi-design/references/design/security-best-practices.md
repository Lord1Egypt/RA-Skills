# Security Best Practices

## 认证与授权

### 1. 认证 (Authentication)

#### 使用标准认证协议

| 协议 | 适用场景 |
|------|----------|
| OAuth 2.0 | 第三方应用授权 |
| JWT | 自有应用的无状态认证 |
| API Key | 服务间通信 |

#### JWT Token 示例

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Token 安全要求

```json
{
  "alg": "RS256",  // 使用非对称算法
  "typ": "JWT",
  "exp": 1704009600,  // 必须有过期时间
  "iat": 1704006000
}
```

### 2. 授权 (Authorization)

#### 权限控制级别

| 级别 | 说明 |
|------|------|
| 资源级 | 用户只能访问自己的资源 |
| 字段级 | 用户只能看到部分字段 |
| 操作级 | 用户只能执行特定操作 |

#### 资源级授权示例

```bash
# 用户只能获取自己的订单
GET /users/123/orders

# 验证用户 ID 匹配
if (resource.userId !== currentUser.id) {
  return 403 Forbidden
}
```

---

## 输入验证

### 1. 参数验证

```json
// 验证规则示例
{
  "userId": {
    "type": "integer",
    "required": true,
    "min": 1
  },
  "email": {
    "type": "string",
    "required": true,
    "format": "email"
  },
  "status": {
    "type": "string",
    "enum": ["active", "inactive", "pending"]
  }
}
```

### 2. SQL 注入防护

```sql
-- ❌ 危险：拼接用户输入
SELECT * FROM users WHERE id = ' + userId + '

-- ✅ 安全：参数化查询
SELECT * FROM users WHERE id = $1
```

### 3. XSS 防护

```json
// 响应中转义 HTML 特殊字符
{
  "message": "User &lt;script&gt;alert(1)&lt;/script&gt; created"
}
```

---

## 数据保护

### 1. 敏感数据处理

```json
// ❌ 错误：返回敏感字段
{
  "user": {
    "id": 123,
    "name": "John",
    "password": "secret123",
    "ssn": "123-45-6789"
  }
}

// ✅ 正确：过滤敏感字段
{
  "user": {
    "id": 123,
    "name": "John"
  }
}
```

### 2. 信用卡号处理

```json
{
  "payment": {
    "id": "pay_123",
    "last4": "4242",
    "brand": "visa",
    "expMonth": 12,
    "expYear": 2025
    // 不返回完整卡号
  }
}
```

---

## 速率限制 (Rate Limiting)

### 实现方式

```http
# 请求限制 Header
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1704009600

# 超限响应
HTTP/1.1 429 Too Many Requests
Retry-After: 60
```

### 限制策略

| 限制类型 | 建议值 |
|----------|--------|
| 未认证请求 | 20-100 次/分钟 |
| 已认证请求 | 100-1000 次/分钟 |
| 写入操作 | 10-50 次/分钟 |
| 批量操作 | 5-20 次/分钟 |

---

## CORS 配置

### 安全配置

```http
# ❌ 危险：允许所有来源
Access-Control-Allow-Origin: *

# ✅ 安全：明确指定来源
Access-Control-Allow-Origin: https://app.example.com
```

### CORS Header

```http
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PATCH, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 86400
```

---

## 安全 Header

### 必需的安全 Header

```http
# 防止 XSS
X-Content-Type-Options: nosniff

# 防止点击劫持
X-Frame-Options: DENY

# HSTS（仅 HTTPS）
Strict-Transport-Security: max-age=31536000; includeSubDomains

# CSP
Content-Security-Policy: default-src 'self'

# 引用来源策略
Referrer-Policy: strict-origin-when-cross-origin
```

---

## 日志与监控

### 安全事件日志

| 事件 | 日志级别 |
|------|----------|
| 认证失败 | WARN |
| 权限不足 | WARN |
| 异常访问 | ERROR |
| 速率超限 | INFO |

### 日志内容

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "warn",
  "event": "auth_failed",
  "userId": "123",
  "ip": "203.0.113.50",
  "userAgent": "Mozilla/5.0...",
  "requestId": "req_abc123"
}
```

---

## HTTPS 要求

### 必须使用 HTTPS

```http
# ❌ 不安全
http://api.example.com/users

# ✅ 安全
https://api.example.com/users
```

### 强制重定向

```http
# HTTP 请求重定向到 HTTPS
HTTP/1.1 301 Moved Permanently
Location: https://api.example.com/users
```

---

## 错误处理安全

### 不暴露内部信息

```json
// ❌ 错误：暴露内部细节
{
  "error": {
    "code": "SYS_001",
    "message": "java.sql.SQLException: Connection refused at DB.java:42"
  }
}

// ✅ 正确：只返回安全信息
{
  "error": {
    "code": "SYS_001",
    "message": "Database connection error",
    "requestId": "req_abc123"
  }
}
```
