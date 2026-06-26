# Resource Modeling

## 资源建模概述

资源建模是 API 设计的第一步，将业务实体抽象为可操作的资源。

---

## 资源识别

### 什么是资源？

资源是：
- **名词** — 用户、产品、订单
- **可寻址** — 通过 URL 访问
- **有状态** — 可以创建、读取、更新、删除
- **表示业务实体** — 订单包含多个订单项

### 资源 vs 非资源

| 资源 ✅ | 非资源 ❌ |
|---------|-----------|
| users | getUsers |
| products | login |
| orders | calculate |
| payments | sendEmail |
| reviews | processOrder |

---

## 资源层级结构

### 典型层级

```
用户 (users)
├── 地址 (addresses)
├── 订单 (orders)
│   └── 订单项 (items)
├── 评论 (reviews)
└── 收藏 (favorites)
```

### URL 对应

```
/users                      # 用户列表
/users/123                  # 单个用户
/users/123/addresses         # 用户地址列表
/users/123/orders           # 用户订单列表
/users/123/orders/456       # 用户订单详情
/users/123/orders/456/items # 订单项列表
```

### 层级深度建议

**最多 3 层嵌套**，避免过深的关系。

```
✅ Good: /users/123/orders/456
❌ Too Deep: /orgs/1/depts/2/teams/3/members/4
```

---

## 资源关系类型

### 1. 拥有关系 (Ownership)

子资源属于父资源。

```bash
/users/123/orders        # 用户的订单
/users/123/addresses     # 用户的地址
```

### 2. 关联关系 (Association)

资源之间有关联但不拥有。

```bash
# 方式一：通过关联资源
/users/123/friends/456

# 方式二：通过查询参数（推荐）
/users/123?friends=true

# 方式三：通过独立端点
/friendships?user_id=123
```

### 3. 聚合关系 (Aggregation)

一个资源由多个子资源组成。

```bash
/orders/456/items        # 订单的所有项
/products/123/reviews     # 产品的所有评论
```

---

## 资源操作映射

### 基本 CRUD

| 操作 | HTTP Method | URL 示例 | 说明 |
|------|-------------|----------|------|
| Create | POST | POST /users | 创建用户 |
| Read | GET | GET /users/123 | 获取用户 |
| Update(Full) | PUT | PUT /users/123 | 全量更新用户 |
| Update(Partial) | PATCH | PATCH /users/123 | 部分更新用户 |
| Delete | DELETE | DELETE /users/123 | 删除用户 |
| List | GET | GET /users | 获取用户列表 |

### 非 CRUD 操作

使用 **动词作为资源名**：

```bash
# 激活用户
POST /users/123/activate

# 重置密码
POST /users/123/reset-password

# 取消订单
POST /orders/456/cancel

# 批量操作
POST /users/batch-delete
```

---

## 资源建模示例

### 电商系统

```
/products                    # 产品列表
/products/{productId}        # 产品详情
/products/{productId}/reviews # 产品评论

/categories                  # 分类列表
/categories/{categoryId}    # 分类详情

/users                       # 用户列表
/users/{userId}             # 用户详情
/users/{userId}/addresses   # 用户地址
/users/{userId}/wishlists   # 用户心愿单

/orders                      # 订单列表
/orders/{orderId}           # 订单详情
/orders/{orderId}/items     # 订单项

/carts                       # 购物车
/carts/{cartId}/items       # 购物车项

/payments                    # 支付记录
/payments/{paymentId}       # 支付详情

/reviews                     # 所有评论
/reviews?product_id=123     # 按产品筛选评论
```

### 博客系统

```
/articles                    # 文章列表
/articles/{articleId}       # 文章详情
/articles/{articleId}/comments # 文章评论

/users                       # 用户列表
/users/{userId}             # 用户详情
/users/{userId}/articles    # 用户的文章

/tags                        # 标签列表
/tags/{tagId}/articles      # 标签下的文章

/categories                  # 分类列表
/categories/{categoryId}    # 分类详情
```

---

## 资源粒度选择

### 粗粒度 vs 细粒度

| 类型 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 粗粒度 | 减少请求数 | 可能返回不需要的数据 | 移动端、高延迟网络 |
| 细粒度 | 按需获取 | 请求数多 | 复杂后台系统 |

### 建议

1. **默认粗粒度** — 一次请求返回完整资源
2. **提供字段过滤** — 允许客户端选择字段
   ```
   GET /users/123?fields=id,name,email
   ```
3. **提供关联资源** — 必要时可获取嵌套资源

---

## 影子资源 (Subtle Resources)

### 避免创建影子资源

影子资源是可以通过其他资源推导出来的资源。

```
❌ Bad
/users/123/friends-count      # 朋友数量
/users/123/is-following/456   # 是否关注某个用户

✅ Good
GET /users/123/friends        # 获取朋友列表
GET /users/123?fields=friendsCount  # 请求时指定字段
```

### 特殊情况

某些计算属性可以作为资源（如果计算成本高）：

```
✅ Acceptable
/reports/sales-summary        # 销售汇总（计算成本高）
/analytics/user-activity      # 用户活动分析
```

---

## 资源命名检查清单

- [ ] 使用复数名词（users, products）
- [ ] 使用小写字母和连字符（user-profiles）
- [ ] 避免缩写（使用 `products` 而非 `prods`）
- [ ] 层级不超过 3 层
- [ ] 每个资源有唯一 ID
- [ ] 操作使用 HTTP 方法而非 URL 动词
