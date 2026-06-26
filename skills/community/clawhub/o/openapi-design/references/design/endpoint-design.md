# Endpoint Design

## 端点设计原则

### 1. 资源端点 vs 动作端点

#### 资源端点（首选）

```
GET    /users              # 列出用户
POST   /users              # 创建用户
GET    /users/123          # 获取用户
PATCH  /users/123          # 更新用户
DELETE /users/123          # 删除用户
```

#### 动作端点（特定场景）

当操作无法用 CRUD 表达时：

```bash
# 多步操作
POST /users/123/reset-password

# 批量操作
POST /users/batch-delete
POST /users/batch-update

# 复杂查询（超出标准 CRUD）
POST /users/search  # 复杂搜索条件
GET  /reports/daily-sales  # 生成报表
```

---

## 查询设计

### 过滤 (Filtering)

```
GET /users?status=active
GET /products?category=electronics&price_min=100&price_max=500
GET /orders?created_after=2024-01-01&status=completed
```

### 排序 (Sorting)

```
GET /products?sort=price:asc
GET /products?sort=created_at:desc
GET /products?sort=price:asc,name:asc  # 多字段排序
```

### 分页 (Pagination)

#### Offset-based
```
GET /users?page=1&limit=20
```

#### Cursor-based（推荐大数据量）
```
GET /users?after=user_abc123&limit=20
```

### 字段选择

```
GET /users?fields=id,name,email
GET /users/123?fields=id,name
```

### 响应分页元数据

```json
{
  "data": [...],
  "pagination": {
    "total": 150,
    "page": 1,
    "limit": 20,
    "hasMore": true,
    "nextCursor": "user_abc123"
  }
}
```

---

## 复杂查询端点

### 搜索端点

```bash
POST /users/search

Body:
{
  "query": {
    "name": "John",
    "status": "active"
  },
  "filters": {
    "created_after": "2024-01-01",
    "role": ["admin", "user"]
  },
  "sort": {
    "field": "created_at",
    "order": "desc"
  },
  "pagination": {
    "limit": 20,
    "offset": 0
  }
}
```

---

## 关联资源端点

### 获取关联资源

```bash
# 获取用户的所有订单
GET /users/123/orders

# 获取用户订单中的特定项
GET /users/123/orders/456
```

### 展开关联资源

```bash
# 获取用户并包含订单
GET /users/123?expand=orders

# 响应
{
  "data": {
    "id": 123,
    "name": "John",
    "orders": [
      { "id": 456, "status": "completed" }
    ]
  }
}
```

---

## 批量操作端点

### 批量创建

```bash
POST /users/batch

Body:
{
  "users": [
    { "name": "User 1", "email": "user1@example.com" },
    { "name": "User 2", "email": "user2@example.com" }
  ]
}

Response:
{
  "data": [
    { "id": 123, "name": "User 1", "status": "created" },
    { "id": 124, "name": "User 2", "status": "created" }
  ],
  "errors": []
}
```

### 批量更新

```bash
PATCH /users/batch

Body:
{
  "users": [
    { "id": 123, "status": "active" },
    { "id": 124, "status": "inactive" }
  ]
}
```

### 批量删除

```bash
DELETE /users/batch

Body:
{
  "ids": [123, 124, 125]
}

Response:
{
  "data": {
    "deleted": 3
  }
}
```

---

## 端点设计检查清单

- [ ] 使用复数名词作为资源名
- [ ] 使用正确的 HTTP 方法
- [ ] URL 层级不超过 3 层
- [ ] 查询参数用于过滤、排序、分页
- [ ] 使用标准状态码
- [ ] 错误响应格式统一
- [ ] 避免在 URL 中使用动词
- [ ] 使用小写字母和连字符
