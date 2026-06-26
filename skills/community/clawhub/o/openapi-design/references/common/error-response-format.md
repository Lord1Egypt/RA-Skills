# Error Response Format

## 统一错误响应结构

### 标准错误格式

```json
{
  "error": {
    "code": "AUTH_001",
    "message": "Authentication required",
    "details": []
  },
  "meta": {
    "requestId": "req_abc123xyz",
    "timestamp": "2024-01-15T10:30:00Z",
    "apiVersion": "v1"
  }
}
```

### 字段说明

| 字段 | 必需 | 类型 | 描述 |
|------|------|------|------|
| `error.code` | ✅ | string | 错误码，格式 `{DOMAIN}_{NUMBER}` |
| `error.message` | ✅ | string | 用户可读的错误描述 |
| `error.details` | ⚠️ | array | 可选，详细错误信息列表 |
| `meta.requestId` | ✅ | string | 请求追踪 ID |
| `meta.timestamp` | ✅ | string | 错误发生时间（ISO 8601） |
| `meta.apiVersion` | ⚠️ | string | API 版本（可选） |

---

## 错误详情格式 (details)

### 参数验证错误

```json
{
  "error": {
    "code": "VAL_001",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "rejectedValue": "user@@example"
      },
      {
        "field": "age",
        "message": "Must be between 1 and 150",
        "rejectedValue": -5
      },
      {
        "field": "password",
        "message": "Must be at least 8 characters",
        "rejectedValue": "****"
      }
    ]
  }
}
```

### 业务逻辑错误

```json
{
  "error": {
    "code": "ORDER_003",
    "message": "Insufficient inventory",
    "details": [
      {
        "productId": "PROD_001",
        "requested": 10,
        "available": 3
      }
    ]
  }
}
```

---

## 错误码规范

### 错误码格式
```
{DOMAIN}_{NUMBER}
```

### 错误域划分

| 域 | 范围 | 说明 |
|----|------|------|
| `AUTH` | 001-099 | 认证错误 |
| `PERM` | 001-099 | 权限/授权错误 |
| `VAL` | 001-099 | 参数验证错误 |
| `RES` | 001-099 | 资源相关错误 |
| `BIZ` | 001-099 | 业务逻辑错误 |
| `RATE` | 001-099 | 频率限制错误 |
| `SYS` | 001-099 | 系统内部错误 |

### 常见错误码参考

| 错误码 | HTTP Status | 描述 |
|--------|-------------|------|
| AUTH_001 | 401 | 缺少认证信息 |
| AUTH_002 | 401 | Token 无效或已过期 |
| AUTH_003 | 401 | Token 格式错误 |
| PERM_001 | 403 | 权限不足 |
| PERM_002 | 403 | 操作被禁止 |
| VAL_001 | 400 | 参数验证失败 |
| VAL_002 | 400 | 缺少必需参数 |
| VAL_003 | 400 | 参数类型错误 |
| RES_001 | 404 | 资源不存在 |
| RES_002 | 404 | 资源已删除 |
| RES_003 | 409 | 资源已存在 |
| RES_004 | 409 | 资源版本冲突 |
| BIZ_001 | 422 | 业务规则违反 |
| BIZ_002 | 422 | 状态不允许此操作 |
| RATE_001 | 429 | 请求频率超限 |
| SYS_001 | 500 | 系统内部错误 |
| SYS_002 | 503 | 服务暂不可用 |

---

## 错误消息编写规范

### 原则

1. **用户可读** — 面向开发者或 API 调用者
2. **简洁明确** — 一句话说清问题
3. **不暴露内部细节** — 不包含 SQL、堆栈等信息
4. **提供解决线索** — 必要时给出建议

### ✅ Good Examples

```json
{
  "error": {
    "code": "AUTH_002",
    "message": "Access token has expired. Please refresh your token."
  }
}

{
  "error": {
    "code": "VAL_002",
    "message": "Missing required parameter: 'email'"
  }
}

{
  "error": {
    "code": "RES_001",
    "message": "User with ID 123 not found"
  }
}
```

### ❌ Bad Examples

```json
{
  "error": {
    "code": "SYS_001",
    "message": "java.lang.NullPointerException at UserService.java:42"
  }
}

{
  "error": {
    "code": "RES_001",
    "message": "Error"
  }
}

{
  "error": {
    "code": "VAL_001",
    "message": "Invalid"
  }
}
```

---

## 嵌套错误 (Nested Errors)

对于批量操作或复杂验证场景：

```json
{
  "error": {
    "code": "VAL_001",
    "message": "Multiple validation errors",
    "details": [
      {
        "field": "items[0].quantity",
        "message": "Must be positive",
        "rejectedValue": -1
      },
      {
        "field": "items[1].productId",
        "message": "Product not found",
        "rejectedValue": "INVALID_ID"
      }
    ]
  }
}
```

---

## 开发与生产环境差异

### 开发环境
可以包含更多调试信息（但仍不暴露敏感数据）：

```json
{
  "error": {
    "code": "VAL_001",
    "message": "Validation failed",
    "details": [...],
    "debug": {
      "stackTrace": "...",
      "requestPath": "/v1/users",
      "requestMethod": "POST"
    }
  }
}
```

### 生产环境
只返回安全的错误信息：

```json
{
  "error": {
    "code": "VAL_001",
    "message": "Validation failed",
    "details": [...]
  }
}
```
