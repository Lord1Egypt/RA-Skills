# Naming Conventions

## 资源命名

### 基本规则

| 类型 | 规则 | 示例 |
|------|------|------|
| 集合（复数） | 全部小写，复数名词 | `users`, `products`, `orders` |
| 单个资源 | 复数 + ID | `users/123`, `orders/456` |
| 动作资源 | 动词名词 | `/users/123/activate` |

### 常见资源命名

```
✅ /users                    # 用户
✅ /products                 # 产品
✅ /orders                   # 订单
✅ /orders/123/items         # 订单项
✅ /users/123/profile        # 用户资料
✅ /users/123/addresses       # 用户地址
✅ /products/123/reviews      # 产品评论
✅ /users/123/orders          # 用户订单
```

### 避免的名称

```
❌ /UserList
❌ /getUser
❌ /create_order
❌ /USERS
❌ /userProfile (应分开)
```

---

## 字段命名

### JSON 字段命名

| 场景 | 规则 | 示例 |
|------|------|------|
| 一般 | camelCase | `userName`, `createdAt` |
| ID | `resourceId` 或 `{resource}_id` | `userId`, `orderId` |
| 时间 | ISO 8601 + `At` 结尾 | `createdAt`, `updatedAt`, `deletedAt` |
| 布尔 | `is`, `has`, `can` 前缀 | `isActive`, `hasPermission` |
| 枚举 | `status`, `type` 后缀 | `orderStatus`, `userType` |

### 避免的字段名

```
❌ user_name (应使用 userName)
❌ created_at (应使用 createdAt)
❌ IsActive (应使用 isActive)
❌ data (太模糊，应使用具体名称)
❌ info (太模糊)
❌ temp / tmp (临时字段)
```

---

## 参数命名

### Path 参数
```
GET /users/{userId}
GET /orders/{orderId}/items/{itemId}

✅ userId, orderId, itemId
❌ id, oid, uid
```

### Query 参数
```
GET /users?status=active&page=1&limit=20

规则：小写 + 下划线分隔（query 参数可用下划线）
✅ status, page_size, sort_by, filter_by
❌ statusFilter, pageSize, sortBy
```

### Header 参数
```
Content-Type: application/json
Authorization: Bearer {token}
X-Request-ID: {uuid}
X-Correlation-ID: {uuid}

规则：Kebab-case + 语义化前缀
✅ X-Request-ID, X-Correlation-ID
❌ requestId, correlation_id
```

---

## 错误代码命名

### 错误码格式

```
{DOMAIN}_{CODE}

示例：
- AUTH_001      # 认证错误
- USER_002      # 用户错误
- ORDER_003     # 订单错误
- VAL_004       # 验证错误
```

### 常见错误域

| 域 | 用途 |
|----|------|
| `AUTH` | 认证相关 |
| `PERM` | 授权/权限相关 |
| `VAL` | 参数验证相关 |
| `RES` | 资源相关（不存在等） |
| `SYS` | 系统内部错误 |

---

## 文件命名（OpenAPI）

```
{resource}-api.yaml
或
{resource}-openapi3.yaml

示例：
- users-api.yaml
- orders-api.yaml
- payments-api.yaml
```

---

## 版本命名

```
v1, v2, v3...

路径格式：/v1/users
Header格式：API-Version: 2024-01-01
```
