# McDonald's China MCP API Reference

## Base URL
```
https://mcp.mcd.cn
```

## Authentication
```
Authorization: Bearer YOUR_MCP_TOKEN
```

## All Available Tools

### 1. Coupons

#### available-coupons
Query coupons available to claim.

**Parameters:** None

**Response:**
```
### 麦麦省优惠券列表：
- 优惠券标题：11.9元麦乐鸡
  状态：已领取
- 优惠券标题：9.9元薯你最甜
  状态：未领取
```

#### auto-bind-coupons
Automatically claim all available coupons.

**Parameters:** None

**Response:**
```
### 🎉 领券结果
**总计**: 1 张优惠券
**成功**: 1 张
**失败**: 0 张

#### ✅ 成功领取的优惠券：
- **9.9元薯你最甜**
  - couponId：8ED8D8BEBEBDEF26B615682E92EFAC86
  - couponCode：MCDD60T892ST5EV00N1090
```

#### query-my-coupons
Query user's claimed coupons.

**Parameters:** None

**Response:**
```
# 您的优惠券列表
共 1 张可用优惠券

## 9.9元薯你最甜
- **优惠**: ¥9.9 (用券价格)
- **有效期**: 2025-12-09 00:00-2026-02-12 23:59
- **领取时间**: 今日收到
- **标签**: 到店专用、外送专用
```

---

### 2. Points (麦麦商城)

#### query-my-account
Query user's points balance.

**Parameters:** None

**Response:**
```json
{
  "availablePoint": "7592",
  "accumulativePoint": "141760.94",
  "currency": "麦当劳积分",
  "frozenPoint": "30",
  "expiredPoint": "0"
}
```

#### mall-points-products
Query products redeemable with points.

**Parameters:** None

**Response:**
```json
[
  {
    "spuName": "中杯拿铁/美式500积分",
    "spuId": 542,
    "skuId": 10997,
    "spuImage": "https://...",
    "point": "500"
  }
]
```

#### mall-product-detail
Get details of a specific points product.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| spuId | Long | Yes | Product ID from mall-points-products |

#### mall-create-order
Redeem points for a product.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| skuId | Long | Yes | SKU ID from mall-points-products |
| count | Integer | No | Quantity (default: 1) |

---

### 3. Calendar (麦麦日历)

#### campaign-calendar
Query monthly marketing activities.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| specifiedDate | String | No | Date in yyyy-MM-dd format |

**Response:**
```
### 当前时间：2025-12-09 14:48:42 ###
活动列表：
#### 12月8日 往期回顾
- **活动标题**：小女警沙发！12月12日麦麦商城见！
...
```

---

### 4. Delivery (点餐)

#### delivery-query-addresses
Query user's saved delivery addresses.

**Parameters:** None

**Response:**
```json
{
  "addresses": [
    {
      "addressId": "1",
      "contactName": "张三",
      "phone": "152****6666",
      "fullAddress": "xx省xx市xxx小区 x栋x单元xxx室",
      "storeCode": "12345",
      "storeName": "xxx门店",
      "beCode": "12345"
    }
  ]
}
```

#### delivery-create-address
Add new delivery address.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| city | String | Yes | City name, e.g., 南京市 |
| contactName | String | Yes | Contact name, e.g., 李明 |
| gender | String | No | 先生 or 女士 |
| phone | String | Yes | 11-digit phone number |
| address | String | Yes | Delivery address |
| addressDetail | String | Yes | Detailed address (unit/room) |

#### query-store-coupons
Query coupons available for a specific store.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| storeCode | String | Yes | Store code |
| beCode | String | Yes | BE code |

#### query-meals
Query menu for a store.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| storeCode | String | Yes | Store code |
| beCode | String | Yes | BE code |

#### query-meal-detail
Get details of a specific meal.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| code | String | Yes | Meal code |
| storeCode | String | No | Store code |
| beCode | String | Yes | BE code |

#### calculate-price
Calculate order price.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| storeCode | String | Yes | Store code |
| beCode | String | Yes | BE code |
| items | Array | Yes | Product list |

**items structure:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| productCode | String | Yes | Product code |
| quantity | Integer | Yes | Quantity |
| couponId | String | No | Coupon ID |
| couponCode | String | No | Coupon code |

#### create-order
Create delivery order.

**Parameters:** Same as calculate-price

#### query-order
Query order status.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| orderId | String | Yes | Order ID |

---

### 5. Nutrition (餐品营养)

#### list-nutrition-foods
Get nutrition information for menu items.

**Parameters:** None

**Response:**
```json
{
  "productName": "猪柳麦满分",
  "nutritionDescription": "null",
  "energyKj": "1288",
  "energyKcal": "308",
  "protein": "16",
  "fat": "16",
  "carbohydrate": "24",
  "sodium": "781",
  "calcium": "213"
}
```

---

### 6. General

#### now-time-info
Get current server time.

**Parameters:** None

**Response:**
```json
{
  "timestamp": 1765447025424,
  "datetime": "2025-12-11T17:57:05.424",
  "formatted": "2025-12-11 17:57:05",
  "date": "2025-12-11",
  "year": 2025,
  "month": 12,
  "day": 11,
  "dayOfWeek": "THURSDAY",
  "timezone": "GMT+08:00",
  "offset": "+08:00",
  "utc": "2025-12-11T09:57:05.425Z"
}
```

---

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 401 | Token invalid or expired | Check your MCP Token |
| 429 | Rate limit exceeded | Wait and retry (600/min max) |
