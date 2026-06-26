# API Design Principles

## RESTful Design Fundamentals

### 1. 资源导向 (Resource-Oriented)

API 应该围绕**资源**而非**动作**设计。

| ❌ Wrong | ✅ Correct |
|----------|------------|
| `POST /createUser` | `POST /users` |
| `GET /getUserById/123` | `GET /users/123` |
| `POST /updateUser` | `PATCH /users/123` |
| `DELETE /deleteUser/123` | `DELETE /users/123` |

### 2. 使用正确的 HTTP 方法

| Method | Purpose | Idempotent | Safe |
|--------|---------|-------------|------|
| GET | 查询资源 | Yes | Yes |
| POST | 创建资源 | No | No |
| PUT | 完整替换资源 | Yes | No |
| PATCH | 部分更新资源 | No | No |
| DELETE | 删除资源 | Yes | No |

### 3. 层级结构 (Hierarchical)

使用嵌套路径表示资源层级，但**避免过深嵌套**（建议最多 2-3 层）。

```
✅ Good: /users/123/orders
✅ Good: /users/123/orders/456
❌ Too Deep: /users/123/orders/456/items/789
```

### 4. 使用复数名词

```bash
✅ /users
✅ /products
✅ /orders
❌ /user
❌ /product
```

### 5. 查询参数用于过滤/分页

```
GET /users?status=active&page=1&limit=20
GET /products?category=electronics&sort=price:desc
GET /orders?created_after=2024-01-01
```

---

## URL 设计规范

### 规则

1. **小写字母** + **连字符分隔**
   ```
   ✅ /user-profiles
   ❌ /userProfiles
   ❌ /user_profiles
   ```

2. **不使用动词**，用 HTTP 方法表达动作
   ```
   ✅ GET /users/123
   ❌ GET /getUser/123
   ```

3. **文件扩展名不推荐**
   ```
   ❌ /users/123.json
   ✅ /users/123 (通过 Accept header 指定格式)
   ```

4. **版本控制**
   ```
   /v1/users
   /v2/users
   ```

---

## 数据格式

### 请求格式
- JSON 作为默认数据格式
- 设置 `Content-Type: application/json`

### 响应格式
- JSON 响应体
- 使用 `camelCase` 命名
- ISO 8601 日期格式

```json
{
  "data": {
    "userId": 123,
    "userName": "John",
    "createdAt": "2024-01-15T10:30:00Z"
  },
  "meta": {
    "requestId": "req_abc123"
  }
}
```

---

## 分页规范

使用 **Cursor-based** 或 **Offset-based** 分页：

### Offset-based
```
GET /users?page=1&limit=20
```

### Cursor-based
```
GET /users?after=cursor_xyz&limit=20
```

### 分页响应
```json
{
  "data": [...],
  "pagination": {
    "total": 150,
    "page": 1,
    "limit": 20,
    "hasMore": true
  }
}
```

---

## 认证与授权

1. 使用标准认证协议（OAuth 2.0 / JWT）
2. 通过 `Authorization` header 传递 token
3. 不要在 URL 中包含敏感信息

```
✅ Authorization: Bearer eyJhbGciOiJIUzI1NiIsIn...
❌ GET /users/123?token=eyJhbGciOiJIUzI1NiIs...
```
