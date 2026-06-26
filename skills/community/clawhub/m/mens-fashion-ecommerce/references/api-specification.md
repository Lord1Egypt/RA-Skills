# API接口规范

## API设计原则

### 1. RESTful 设计规范
- 使用名词复数表示资源
- 使用HTTP方法表示操作类型
- 使用状态码表示操作结果
- 使用查询参数进行过滤、排序、分页

### 2. 统一响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": 1640995200000
}
```

### 3. 错误码规范
- 200: 成功
- 400: 请求参数错误
- 401: 未授权
- 403: 权限不足
- 404: 资源不存在
- 500: 服务器内部错误

### 4. 版本管理
API版本通过URL路径管理：`/api/v1/`

## 认证接口

### 1. 用户注册
**POST** `/api/v1/auth/register`

**请求参数：**
```json
{
  "username": "string, required, 用户名",
  "password": "string, required, 密码",
  "email": "string, optional, 邮箱",
  "phone": "string, optional, 手机号",
  "captcha": "string, optional, 验证码"
}
```

**响应：**
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "userId": 1,
    "username": "testuser",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "timestamp": 1640995200000
}
```

### 2. 用户登录
**POST** `/api/v1/auth/login`

**请求参数：**
```json
{
  "username": "string, required, 用户名/邮箱/手机号",
  "password": "string, required, 密码",
  "rememberMe": "boolean, optional, 记住我"
}
```

**响应：**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "userId": 1,
    "username": "testuser",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 7200
  },
  "timestamp": 1640995200000
}
```

### 3. 获取用户信息
**GET** `/api/v1/auth/userinfo`

**请求头：**
```
Authorization: Bearer {token}
```

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "userId": 1,
    "username": "testuser",
    "email": "test@example.com",
    "phone": "13800138000",
    "avatar": "/images/avatar/default.jpg",
    "gender": 1,
    "birthday": "1990-01-01",
    "roles": ["user"],
    "permissions": ["user:read", "user:write"]
  },
  "timestamp": 1640995200000
}
```

### 4. 刷新Token
**POST** `/api/v1/auth/refresh`

**请求头：**
```
Authorization: Bearer {token}
```

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 7200
  },
  "timestamp": 1640995200000
}
```

## 用户管理接口

### 1. 获取用户列表
**GET** `/api/v1/users`

**查询参数：**
- `page`: 页码，默认1
- `size`: 每页大小，默认10
- `username`: 用户名模糊查询
- `email`: 邮箱模糊查询
- `phone`: 手机号模糊查询
- `status`: 状态过滤
- `sort`: 排序字段，如`createTime,desc`

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "page": 1,
    "size": 10,
    "total": 100,
    "pages": 10,
    "records": [
      {
        "userId": 1,
        "username": "testuser",
        "email": "test@example.com",
        "phone": "13800138000",
        "status": 1,
        "createTime": "2024-01-01 10:00:00"
      }
    ]
  },
  "timestamp": 1640995200000
}
```

### 2. 获取用户详情
**GET** `/api/v1/users/{userId}`

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "userId": 1,
    "username": "testuser",
    "email": "test@example.com",
    "phone": "13800138000",
    "avatar": "/images/avatar/default.jpg",
    "gender": 1,
    "birthday": "1990-01-01",
    "status": 1,
    "lastLoginTime": "2024-01-01 10:00:00",
    "createTime": "2024-01-01 10:00:00",
    "updateTime": "2024-01-01 10:00:00"
  },
  "timestamp": 1640995200000
}
```

### 3. 更新用户信息
**PUT** `/api/v1/users/{userId}`

**请求参数：**
```json
{
  "email": "string, optional, 邮箱",
  "phone": "string, optional, 手机号",
  "avatar": "string, optional, 头像",
  "gender": "number, optional, 性别",
  "birthday": "string, optional, 生日"
}
```

**响应：**
```json
{
  "code": 200,
  "message": "更新成功",
  "data": null,
  "timestamp": 1640995200000
}
```

### 4. 修改密码
**PUT** `/api/v1/users/{userId}/password`

**请求参数：**
```json
{
  "oldPassword": "string, required, 旧密码",
  "newPassword": "string, required, 新密码"
}
```

**响应：**
```json
{
  "code": 200,
  "message": "密码修改成功",
  "data": null,
  "timestamp": 1640995200000
}
```

## 商品管理接口

### 1. 获取商品列表
**GET** `/api/v1/products`

**查询参数：**
- `page`: 页码，默认1
- `size`: 每页大小，默认12
- `categoryId`: 分类ID过滤
- `keyword`: 关键词搜索
- `minPrice`: 最低价格
- `maxPrice`: 最高价格
- `isHot`: 是否热销
- `isNew`: 是否新品
- `isRecommend`: 是否推荐
- `status`: 状态过滤
- `sort`: 排序字段，如`price,asc`, `sales,desc`, `createTime,desc`

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "page": 1,
    "size": 12,
    "total": 1000,
    "pages": 84,
    "records": [
      {
        "productId": 1,
        "categoryId": 1,
        "name": "男士纯棉T恤",
        "subtitle": "舒适透气，夏季必备",
        "mainImage": "/images/products/1/main.jpg",
        "price": 99.00,
        "originalPrice": 129.00,
        "stock": 100,
        "sales": 500,
        "isHot": true,
        "isNew": true,
        "status": 1,
        "createTime": "2024-01-01 10:00:00"
      }
    ]
  },
  "timestamp": 1640995200000
}
```

### 2. 获取商品详情
**GET** `/api/v1/products/{productId}`

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "productId": 1,
    "categoryId": 1,
    "name": "男士纯棉T恤",
    "subtitle": "舒适透气，夏季必备",
    "mainImage": "/images/products/1/main.jpg",
    "subImages": [
      "/images/products/1/sub1.jpg",
      "/images/products/1/sub2.jpg",
      "/images/products/1/sub3.jpg"
    ],
    "detail": "<p>商品详情HTML内容</p>",
    "price": 99.00,
    "originalPrice": 129.00,
    "stock": 100,
    "sales": 500,
    "isHot": true,
    "isNew": true,
    "isRecommend": false,
    "status": 1,
    "createTime": "2024-01-01 10:00:00",
    "updateTime": "2024-01-01 10:00:00",
    "skus": [
      {
        "skuId": 1,
        "skuCode": "T001-S-M",
        "attributes": {
          "color": "白色",
          "size": "M"
        },
        "price": 99.00,
        "stock": 50,
        "image": "/images/products/1/sku1.jpg"
      }
    ]
  },
  "timestamp": 1640995200000
}
```

### 3. 创建商品
**POST** `/api/v1/products`

**请求参数：**
```json
{
  "categoryId": "number, required, 分类ID",
  "name": "string, required, 商品名称",
  "subtitle": "string, optional, 商品副标题",
  "mainImage": "string, required, 主图",
  "subImages": "array, optional, 子图数组",
  "detail": "string, optional, 商品详情",
  "price": "number, required, 价格",
  "originalPrice": "number, optional, 原价",
  "stock": "number, required, 库存",
  "isHot": "boolean, optional, 是否热销",
  "isNew": "boolean, optional, 是否新品",
  "isRecommend": "boolean, optional, 是否推荐",
  "sortOrder": "number, optional, 排序",
  "skus": [
    {
      "skuCode": "string, required, SKU编码",
      "attributes": "object, required, 属性",
      "price": "number, required, 价格",
      "stock": "number, required, 库存",
      "image": "string, optional, SKU图片"
    }
  ]
}
```

**响应：**
```json
{
  "code": 200,
  "message": "创建成功",
  "data": {
    "productId": 1
  },
  "timestamp": 1640995200000
}
```

### 4. 更新商品
**PUT** `/api/v1/products/{productId}`

**请求参数：** 同创建商品

**响应：**
```json
{
  "code": 200,
  "message": "更新成功",
  "data": null,
  "timestamp": 1640995200000
}
```

### 5. 删除商品
**DELETE** `/api/v1/products/{productId}`

**响应：**
```json
{
  "code": 200,
  "message": "删除成功",
  "data": null,
  "timestamp": 1640995200000
}
```

## 购物车接口

### 1. 获取购物车列表
**GET** `/api/v1/cart`

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "totalItems": 3,
    "totalPrice": 297.00,
    "items": [
      {
        "cartId": 1,
        "productId": 1,
        "productName": "男士纯棉T恤",
        "productImage": "/images/products/1/main.jpg",
        "skuId": 1,
        "skuAttributes": {
          "color": "白色",
          "size": "M"
        },
        "price": 99.00,
        "quantity": 2,
        "totalPrice": 198.00,
        "selected": true,
        "stock": 50
      },
      {
        "cartId": 2,
        "productId": 2,
        "productName": "男士牛仔裤",
        "productImage": "/images/products/2/main.jpg",
        "skuId": null,
        "skuAttributes": null,
        "price": 199.00,
        "quantity": 1,
        "totalPrice": 199.00,
        "selected": true,
        "stock": 100
      }
    ]
  },
  "timestamp": 1640995200000
}
```

### 2. 添加商品到购物车
**POST** `/api/v1/cart`

**请求参数：**
```json
{
  "productId": "number, required, 商品ID",
  "skuId": "number, optional, SKU ID",
  "quantity": "number, required, 数量，默认1"
}
```

**响应：**
```json
{
  "code": 200,
  "message": "添加成功",
  "data": {
    "cartId": 1
  },
  "timestamp": 1640995200000
}
```

### 3. 更新购物车商品数量
**PUT** `/api/v1/cart/{cartId}`

**请求参数：**
```json
{
  "quantity": "number, required, 数量"
}
```

**响应：**
```json
{
  "code": 200,
  "message": "更新成功",
  "data": null,
  "timestamp": 1640995200000
}
```

### 4. 选择/取消选择商品
**PUT** `/api/v1/cart/{cartId}/select`

**请求参数：**
```json
{
  "selected": "boolean, required, 是否选择"
}
```

**响应：**
```json
{
  "code": 200,
  "message": "操作成功",
  "data": null,
  "timestamp": 1640995200000
}
```

### 5. 批量选择/取消选择
**PUT** `/api/v1/cart/batch-select`

**请求参数：**
```json
{
  "selected": "boolean, required, 是否选择",
  "cartIds": "array, optional, 购物车ID数组，为空表示全部"
}
```

**响应：**
```json
{
  "code": 200,
  "message": "操作成功",
  "data": null,
  "timestamp": 1640995200000
}
```

### 6. 删除购物车商品
**DELETE** `/api/v1/cart/{cartId}`

**响应：**
```json
{
  "code": 200,
  "message": "删除成功",
  "data": null,
  "timestamp": 1640995200000
}
```

### 7. 清空购物车
**DELETE** `/api/v1/cart/clear`

**响应：**
```json
{
  "code": 200,
  "message": "清空成功",
  "data": null,
  "timestamp": 1640995200000
}
```

## 订单接口

### 1. 创建订单
**POST** `/api/v1/orders`

**请求参数：**
```json
{
  "addressId": "number, required, 地址ID",
  "cartIds": "array, optional, 购物车ID数组，为空表示使用选中的购物车商品",
  "couponId": "number, optional, 优惠券ID",
  "remark": "string, optional, 订单备注"
}
```

**响应：**
```json
{
  "code": 200,
  "message": "创建成功",
  "data": {
    "orderId": 1,
    "orderNo": "202401010001",
    "totalPrice": 297.00,
    "actualPrice": 287.00
  },
  "timestamp": 1640995200000
}
```

### 2. 获取订单列表
**GET** `/api/v1/orders`

**查询参数：**
- `page`: 页码，默认1
- `size`: 每页大小，默认10
- `status`: 状态过滤
- `startTime`: 开始时间
- `endTime`: 结束时间
- `sort`: 排序字段，如`createTime,desc`

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "page": 1,
    "size": 10,
    "total": 50,
    "pages": 5,
    "records": [
      {
        "orderId": 1,
        "orderNo": "202401010001",
        "totalPrice": 297.00,
        "actualPrice": 287.00,
        "status": 2,
        "statusText": "待发货",
        "itemCount": 3,
        "createTime": "2024-01-01 10:00:00"
      }
    ]
  },
  "timestamp": 1640995200000
}
```

### 3. 获取订单详情
**GET** `/api/v1/orders/{orderId}`

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "orderId": 1,
    "orderNo": "202401010001",
    "userId": 1,
    "total