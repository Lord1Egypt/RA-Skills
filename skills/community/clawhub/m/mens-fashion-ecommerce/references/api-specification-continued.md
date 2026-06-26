Price": 297.00,
    "discountPrice": 10.00,
    "shippingPrice": 0.00,
    "actualPrice": 287.00,
    "status": 2,
    "statusText": "待发货",
    "paymentType": 1,
    "paymentTypeText": "支付宝",
    "paymentNo": "202401010001001",
    "paymentTime": "2024-01-01 10:05:00",
    "shippingCode": "SF123456789",
    "shippingCompany": "顺丰速运",
    "shippingTime": null,
    "receiveTime": null,
    "closeTime": null,
    "address": {
      "addressId": 1,
      "receiverName": "张三",
      "receiverPhone": "13800138000",
      "province": "北京市",
      "city": "北京市",
      "district": "朝阳区",
      "detailAddress": "某某街道123号",
      "postalCode": "100000"
    },
    "items": [
      {
        "itemId": 1,
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
        "totalPrice": 198.00
      },
      {
        "itemId": 2,
        "productId": 2,
        "productName": "男士牛仔裤",
        "productImage": "/images/products/2/main.jpg",
        "skuId": null,
        "skuAttributes": null,
        "price": 199.00,
        "quantity": 1,
        "totalPrice": 199.00
      }
    ],
    "createTime": "2024-01-01 10:00:00",
    "updateTime": "2024-01-01 10:05:00"
  },
  "timestamp": 1640995200000
}
```

### 4. 取消订单
**PUT** `/api/v1/orders/{orderId}/cancel`

**响应：**
```json
{
  "code": 200,
  "message": "取消成功",
  "data": null,
  "timestamp": 1640995200000
}
```

### 5. 确认收货
**PUT** `/api/v1/orders/{orderId}/confirm`

**响应：**
```json
{
  "code": 200,
  "message": "确认成功",
  "data": null,
  "timestamp": 1640995200000
}
```

### 6. 删除订单
**DELETE** `/api/v1/orders/{orderId}`

**响应：**
```json
{
  "code": 200,
  "message": "删除成功",
  "data": null,
  "timestamp": 1640995200000
}
```

## 支付接口

### 1. 获取支付信息
**GET** `/api/v1/orders/{orderId}/payment`

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "orderId": 1,
    "orderNo": "202401010001",
    "amount": 287.00,
    "subject": "男装电商订单",
    "body": "男士纯棉T恤等3件商品",
    "timeoutExpress": "30m",
    "paymentMethods": [
      {
        "type": 1,
        "name": "支付宝",
        "icon": "/images/payment/alipay.png"
      },
      {
        "type": 2,
        "name": "微信支付",
        "icon": "/images/payment/wechat.png"
      }
    ]
  },
  "timestamp": 1640995200000
}
```

### 2. 发起支付
**POST** `/api/v1/orders/{orderId}/pay`

**请求参数：**
```json
{
  "paymentType": "number, required, 支付方式：1-支付宝，2-微信"
}
```

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "paymentId": 1,
    "paymentNo": "202401010001001",
    "paymentType": 1,
    "amount": 287.00,
    // 支付宝支付返回
    "alipay": {
      "tradeNo": "202401010001001",
      "qrCode": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUg...",
      "formData": "<form action=\"https://openapi.alipay.com/gateway.do\" method=\"POST\">...</form>"
    },
    // 微信支付返回
    "wechat": {
      "appId": "wx1234567890",
      "timeStamp": "1640995200",
      "nonceStr": "5K8264ILTKCH16CQ",
      "package": "prepay_id=wx201410272009395522657a690389285100",
      "signType": "MD5",
      "paySign": "C380BEC2BFD727A4B6845133519F3AD6",
      "qrCode": "weixin://wxpay/bizpayurl?pr=abcdefg"
    }
  },
  "timestamp": 1640995200000
}
```

### 3. 查询支付状态
**GET** `/api/v1/payments/{paymentNo}/status`

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "paymentId": 1,
    "paymentNo": "202401010001001",
    "orderId": 1,
    "orderNo": "202401010001",
    "paymentType": 1,
    "amount": 287.00,
    "status": 2,
    "statusText": "支付成功",
    "paymentTime": "2024-01-01 10:05:00",
    "createTime": "2024-01-01 10:00:00"
  },
  "timestamp": 1640995200000
}
```

### 4. 支付回调
**POST** `/api/v1/payments/callback/{paymentType}`

**请求参数：** 支付平台回调参数

**响应：**
```text
success 或 fail
```

## 地址管理接口

### 1. 获取地址列表
**GET** `/api/v1/addresses`

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "addressId": 1,
      "receiverName": "张三",
      "receiverPhone": "13800138000",
      "province": "北京市",
      "city": "北京市",
      "district": "朝阳区",
      "detailAddress": "某某街道123号",
      "postalCode": "100000",
      "isDefault": true,
      "createTime": "2024-01-01 10:00:00"
    }
  ],
  "timestamp": 1640995200000
}
```

### 2. 添加地址
**POST** `/api/v1/addresses`

**请求参数：**
```json
{
  "receiverName": "string, required, 收货人姓名",
  "receiverPhone": "string, required, 收货人电话",
  "province": "string, required, 省份",
  "city": "string, required, 城市",
  "district": "string, required, 区县",
  "detailAddress": "string, required, 详细地址",
  "postalCode": "string, optional, 邮政编码",
  "isDefault": "boolean, optional, 是否默认"
}
```

**响应：**
```json
{
  "code": 200,
  "message": "添加成功",
  "data": {
    "addressId": 1
  },
  "timestamp": 1640995200000
}
```

### 3. 更新地址
**PUT** `/api/v1/addresses/{addressId}`

**请求参数：** 同添加地址

**响应：**
```json
{
  "code": 200,
  "message": "更新成功",
  "data": null,
  "timestamp": 1640995200000
}
```

### 4. 删除地址
**DELETE** `/api/v1/addresses/{addressId}`

**响应：**
```json
{
  "code": 200,
  "message": "删除成功",
  "data": null,
  "timestamp": 1640995200000
}
```

### 5. 设置默认地址
**PUT** `/api/v1/addresses/{addressId}/default`

**响应：**
```json
{
  "code": 200,
  "message": "设置成功",
  "data": null,
  "timestamp": 1640995200000
}
```

## 商品分类接口

### 1. 获取分类树
**GET** `/api/v1/categories/tree`

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "categoryId": 1,
      "parentId": 0,
      "name": "上衣",
      "icon": "icon-shirt",
      "image": "/images/categories/shirt.jpg",
      "level": 1,
      "sortOrder": 1,
      "status": 1,
      "children": [
        {
          "categoryId": 2,
          "parentId": 1,
          "name": "T恤",
          "icon": null,
          "image": null,
          "level": 2,
          "sortOrder": 1,
          "status": 1,
          "children": []
        }
      ]
    }
  ],
  "timestamp": 1640995200000
}
```

### 2. 获取热门分类
**GET** `/api/v1/categories/hot`

**查询参数：**
- `limit`: 限制数量，默认6

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "categoryId": 2,
      "name": "T恤",
      "image": "/images/categories/t-shirt.jpg",
      "productCount": 150
    }
  ],
  "timestamp": 1640995200000
}
```

## 商品评价接口

### 1. 获取商品评价列表
**GET** `/api/v1/products/{productId}/reviews`

**查询参数：**
- `page`: 页码，默认1
- `size`: 每页大小，默认10
- `rating`: 评分过滤
- `hasImage`: 是否有图片
- `sort`: 排序字段，如`createTime,desc`, `likeCount,desc`

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
        "reviewId": 1,
        "userId": 1,
        "username": "testuser",
        "avatar": "/images/avatar/default.jpg",
        "rating": 5,
        "content": "衣服质量很好，穿着很舒服",
        "images": [
          "/images/reviews/1/1.jpg",
          "/images/reviews/1/2.jpg"
        ],
        "isAnonymous": false,
        "likeCount": 10,
        "replyCount": 2,
        "createTime": "2024-01-01 10:00:00",
        "replies": [
          {
            "replyId": 1,
            "content": "感谢您的评价！",
            "isSeller": true,
            "createTime": "2024-01-01 10:05:00"
          }
        ]
      }
    ],
    "summary": {
      "totalCount": 50,
      "averageRating": 4.8,
      "ratingDistribution": {
        "5": 40,
        "4": 8,
        "3": 1,
        "2": 1,
        "1": 0
      },
      "hasImageCount": 30
    }
  },
  "timestamp": 1640995200000
}
```

### 2. 添加商品评价
**POST** `/api/v1/orders/{orderId}/items/{itemId}/review`

**请求参数：**
```json
{
  "rating": "number, required, 评分1-5",
  "content": "string, required, 评价内容",
  "images": "array, optional, 图片数组",
  "isAnonymous": "boolean, optional, 是否匿名"
}
```

**响应：**
```json
{
  "code": 200,
  "message": "评价成功",
  "data": {
    "reviewId": 1
  },
  "timestamp": 1640995200000
}
```

### 3. 点赞评价
**POST** `/api/v1/reviews/{reviewId}/like`

**响应：**
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "likeCount": 11
  },
  "timestamp": 1640995200000
}
```

## 优惠券接口

### 1. 获取可用优惠券
**GET** `/api/v1/coupons/available`

**查询参数：**
- `amount`: 订单金额，用于筛选可用优惠券

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "couponId": 1,
      "name": "新人专享券",
      "type": 1,
      "typeText": "满减券",
      "amount": 10.00,
      "minAmount": 100.00,
      "description": "新人专享，满100减10",
      "validityType": 2,
      "validDays": 30,
      "expireTime": "2024-02-01 10:00:00"
    }
  ],
  "timestamp": 1640995200000
}
```

### 2. 领取优惠券
**POST** `/api/v1/coupons/{couponId}/receive`

**响应：**
```json
{
  "code": 200,
  "message": "领取成功",
  "data": {
    "userCouponId": 1
  },
  "timestamp": 1640995200000
}
```

### 3. 获取我的优惠券
**GET** `/api/v1/coupons/my`

**查询参数：**
- `status`: 状态过滤：1-未使用，2-已使用，3-已过期

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "userCouponId": 1,
      "couponId": 1,
      "name": "新人专享券",
      "type": 1,
      "amount": 10.00,
      "minAmount": 100.00,
      "status": 1,
      "statusText": "未使用",
      "receiveTime": "2024-01-01 10:00:00",
      "expireTime": "2024-02-01 10:00:00"
    }
  ],
  "timestamp": 1640995200000
}
```

## 文件上传接口

### 1. 上传文件
**POST** `/api/v1/upload`

**请求头：**
```
Content-Type: multipart/form-data
```

**请求参数：**
- `file`: 文件
- `type`: 文件类型：avatar-头像，product-商品，review-评价

**响应：**
```json
{
  "code": 200,
  "message": "上传成功",
  "data": {
    "url": "/uploads/2024/01/01/abcdefg.jpg",
    "filename": "abcdefg.jpg",
    "size": 102400,
    "mimeType": "image/jpeg"
  },
  "timestamp": 1640995200000
}
```

## 搜索接口

### 1. 商品搜索
**GET** `/api/v1/search/products`

**查询参数：**
- `q`: 搜索关键词
- `page`: 页码，默认1
- `size`: 每页大小，默认12
- `categoryId`: 分类ID
- `minPrice`: 最低价格
- `maxPrice`: 最高价格
- `sort`: 排序字段：relevance-相关度，sales-销量，price-价格，createTime-新品

**响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "page": 1,
    "size": 12,
    "total": 100,
    "pages": 9,
    "records": [
      {
        "productId": 1,
        "name": "男士纯棉T恤",
        "subtitle": "舒适透气，夏季必备",
        "mainImage": "/images/products/1/main.jpg",
        "price": 99.00,
        "originalPrice": 129.00,
        "sales": 500,
        "isHot": true,
        "isNew": true
      }
    ],
    "facets": {
      "categories": [
        {
          "categoryId": 1,
          "name": "上衣",
          "count": 60
        }
      ],
      "priceRanges": [
        {
          "min": 0,
          "max": 100,
          "count": 30
        }
      ]
    }
  },
  "timestamp": 1640995200000
}
```

### 2. 搜索建议
**GET** `/api/v1/search/suggest`

**查询参数：**
-