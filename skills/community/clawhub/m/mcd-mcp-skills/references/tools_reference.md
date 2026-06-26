# 麦当劳MCP工具参数参考

本文档详细说明麦当劳MCP Server所有工具的参数要求和使用方法。

## 目录
- [餐品信息查询](#餐品信息查询)
- [配送地址管理](#配送地址管理)
- [外送点餐流程](#外送点餐流程)
- [优惠券管理](#优惠券管理)
- [积分账户管理](#积分账户管理)
- [积分商城兑换](#积分商城兑换)
- [营销活动](#营销活动)
- [工具辅助](#工具辅助)

---

## 餐品信息查询

### list-nutrition-foods - 餐品营养信息列表

**功能说明：**
获取麦当劳常见餐品的营养成分数据，包括能量、蛋白质、脂肪、碳水化合物、钠、钙等信息。

**适用场景：**
- 用户咨询麦当劳餐品的热量或营养成分
- 帮助用户搭配指定热量的套餐

**参数：**
无

**返回数据示例：**
```json
[
  {
    "foodName": "巨无霸",
    "energy": 2573,
    "protein": 27.2,
    "fat": 26.3,
    "carbohydrate": 49.5,
    "sodium": 1093,
    "calcium": 180
  }
]
```

---

### query-meals - 查询当前门店可售卖的餐品列表

**功能说明：**
查询指定门店可售卖的餐品菜单，返回分类、餐品编码、标签等信息。

**适用场景：**
- 用户浏览某个门店的餐品菜单
- 获取餐品编码用于后续下单

**参数：**

| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| storeCode | string | 是 | 门店编码，从配送地址查询获取 |
| beCode | string | 是 | BE编码，从配送地址查询获取 |

**返回数据示例：**
```json
{
  "categories": [
    {
      "categoryId": "1",
      "categoryName": "超值套餐",
      "products": [
        {
          "mealCode": "M001",
          "mealName": "巨无霸套餐",
          "price": 31.0,
          "tags": ["热销", "经典"]
        }
      ]
    }
  ]
}
```

---

### query-meal-detail - 查询餐品详情

**功能说明：**
根据餐品编码查询餐品详情，包括套餐组成、默认选择等。

**适用场景：**
- 查看套餐包含的具体内容
- 了解餐品的组成部分和可选配置

**参数：**

| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| mealCode | string | 是 | 餐品编码，从餐品列表查询获取 |

**返回数据示例：**
```json
{
  "mealCode": "M001",
  "mealName": "巨无霸套餐",
  "description": "巨无霸+中薯条+中可乐",
  "components": [
    {
      "name": "巨无霸",
      "quantity": 1,
      "required": true
    },
    {
      "name": "中薯条",
      "quantity": 1,
      "required": true
    },
    {
      "name": "中可乐",
      "quantity": 1,
      "required": true,
      "customizable": true,
      "options": ["中可乐", "中雪碧", "中芬达"]
    }
  ]
}
```

---

## 配送地址管理

### delivery-query-addresses - 获取用户可配送地址列表

**功能说明：**
查询用户已创建的配送地址列表，返回地址信息及对应门店信息。

**适用场景：**
- 用户选择配送地址
- 获取门店编码和BE编码用于点餐

**参数：**
无

**返回数据示例：**
```json
{
  "addresses": [
    {
      "addressId": "ADR001",
      "address": "北京市朝阳区XXX街道XXX号",
      "contact": "张三",
      "phone": "13800138000",
      "storeCode": "S001",
      "beCode": "BE001",
      "storeName": "麦当劳XXX餐厅"
    }
  ]
}
```

**重要字段说明：**
- `addressId`: 地址ID，创建订单时使用
- `storeCode`: 门店编码，查询餐品和优惠券时使用
- `beCode`: BE编码，查询餐品和下单时使用

---

### delivery-create-address - 新增配送地址

**功能说明：**
创建新的可配送地址。

**适用场景：**
- 用户无可配送地址
- 用户需要添加新的收货地址

**参数：**

| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| address | string | 是 | 详细地址 |
| lat | string | 是 | 纬度 |
| lng | string | 是 | 经度 |
| contact | string | 是 | 联系人姓名 |
| phone | string | 是 | 联系电话 |

**返回数据示例：**
```json
{
  "addressId": "ADR002",
  "message": "地址创建成功"
}
```

---

## 外送点餐流程

### query-store-coupons - 查询用户在当前门店可用券

**功能说明：**
查询用户在当前门店下可使用的优惠券列表。

**适用场景：**
- 用户点餐前查看可用优惠
- 选择优惠进行价格计算

**参数：**

| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| storeCode | string | 是 | 门店编码 |

**返回数据示例：**
```json
{
  "coupons": [
    {
      "couponId": "CPN001",
      "couponName": "满50减10",
      "discountType": "满减",
      "discountValue": 10,
      "minAmount": 50,
      "validFrom": "2024-01-01",
      "validTo": "2024-12-31"
    }
  ]
}
```

---

### calculate-price - 商品价格计算

**功能说明：**
根据用户选购商品列表（可含优惠券）计算商品金额、配送费、优惠金额及应付总价。

**适用场景：**
- 订单创建前计算价格
- 使用优惠券时计算优惠后价格

**参数：**

| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| storeCode | string | 是 | 门店编码 |
| beCode | string | 是 | BE编码 |
| items | array | 是 | 商品列表（JSON格式） |
| coupons | array | 否 | 优惠券ID列表（JSON格式） |

**items参数格式：**
```json
[
  {
    "mealCode": "M001",
    "quantity": 1
  },
  {
    "mealCode": "M002",
    "quantity": 2
  }
]
```

**返回数据示例：**
```json
{
  "subtotal": 62.0,
  "deliveryFee": 9.0,
  "discount": 10.0,
  "total": 61.0,
  "couponDetails": [
    {
      "couponId": "CPN001",
      "couponName": "满50减10",
      "discount": 10.0
    }
  ]
}
```

---

### create-order - 创建外送订单

**功能说明：**
根据门店信息、配送地址、商品列表创建外送订单，返回订单详情与支付链接。

**适用场景：**
- 用户确认下单

**参数：**

| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| storeCode | string | 是 | 门店编码 |
| beCode | string | 是 | BE编码 |
| addressId | string | 是 | 配送地址ID |
| items | array | 是 | 商品列表（JSON格式） |
| coupons | array | 否 | 优惠券ID列表（JSON格式） |

**返回数据示例：**
```json
{
  "orderId": "ORD202401010001",
  "status": "待支付",
  "total": 61.0,
  "paymentUrl": "https://pay.mcd.cn/xxx",
  "estimatedDeliveryTime": "2024-01-01 12:30:00",
  "items": [
    {
      "mealCode": "M001",
      "mealName": "巨无霸套餐",
      "quantity": 1,
      "price": 31.0
    }
  ]
}
```

---

### query-order - 查询订单详情

**功能说明：**
查询订单状态、订单内容、配送信息等。

**适用场景：**
- 查看订单进度
- 确认订单信息

**参数：**

| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| orderId | string | 是 | 订单ID |

**返回数据示例：**
```json
{
  "orderId": "ORD202401010001",
  "status": "配送中",
  "total": 61.0,
  "deliveryAddress": "北京市朝阳区XXX街道XXX号",
  "riderName": "李四",
  "riderPhone": "13900139000",
  "estimatedArrivalTime": "2024-01-01 12:30:00",
  "items": [...]
}
```

---

## 优惠券管理

### available-coupons - 麦麦省券列表查询

**功能说明：**
查询麦麦省当前可领取的优惠券列表。

**适用场景：**
- 用户查看可领取的优惠券

**参数：**
无

**返回数据示例：**
```json
{
  "coupons": [
    {
      "couponId": "CPN001",
      "couponName": "满50减10",
      "description": "订单满50元立减10元",
      "validDays": 30
    }
  ]
}
```

---

### auto-bind-coupons - 麦麦省一键领券

**功能说明：**
自动领取麦麦省所有当前可用的麦当劳优惠券。

**适用场景：**
- 用户想一次性领取所有可用优惠券

**参数：**
无

**返回数据示例：**
```json
{
  "success": true,
  "claimedCount": 5,
  "coupons": [
    {
      "couponId": "CPN001",
      "couponName": "满50减10",
      "validTo": "2024-12-31"
    }
  ]
}
```

---

### query-my-coupons - 我的优惠券查询

**功能说明：**
查询用户可用的优惠券列表。

**适用场景：**
- 查看"我的优惠券"
- 了解可用于点餐的优惠券

**参数：**
无

**返回数据示例：**
```json
{
  "coupons": [
    {
      "couponId": "CPN001",
      "couponName": "满50减10",
      "status": "可用",
      "validTo": "2024-12-31"
    }
  ]
}
```

---

## 积分账户管理

### query-my-account - 我的积分查询

**功能说明：**
查询用户积分账户信息，包括可用积分、累计积分、冻结积分、即将过期积分等。

**适用场景：**
- 用户查询积分余额
- 了解积分状态和有效期

**参数：**
无

**返回数据示例：**
```json
{
  "availablePoints": 1250,
  "totalPoints": 5000,
  "frozenPoints": 100,
  "expiringPoints": 200,
  "expiringDate": "2024-03-31"
}
```

---

## 积分商城兑换

### mall-points-products - 积分兑换商品列表

**功能说明：**
查询麦麦商城内可以用积分兑换的餐品券。

**适用场景：**
- 用户浏览可兑换商品
- 选择积分兑换商品

**参数：**
无

**返回数据示例：**
```json
{
  "products": [
    {
      "productId": "PRD001",
      "productName": "麦辣鸡腿堡兑换券",
      "points": 500,
      "image": "https://xxx.jpg",
      "validDays": 30
    }
  ]
}
```

---

### mall-product-detail - 积分兑换商品详情

**功能说明：**
查询指定积分兑换商品券的详细信息。

**适用场景：**
- 查看商品兑换详情
- 确认兑换前了解商品信息

**参数：**

| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| productId | string | 是 | 商品ID |

**返回数据示例：**
```json
{
  "productId": "PRD001",
  "productName": "麦辣鸡腿堡兑换券",
  "points": 500,
  "description": "可兑换任意门店麦辣鸡腿堡一个",
  "validDays": 30,
  "usageInstructions": "到店出示券码即可使用",
  "image": "https://xxx.jpg"
}
```

---

### mall-create-order - 积分兑换商品下单

**功能说明：**
使用积分兑换指定餐品券，完成积分扣减并发放券码。

**适用场景：**
- 用户确认兑换商品

**参数：**

| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| productId | string | 是 | 商品ID |

**返回数据示例：**
```json
{
  "orderId": "MALL202401010001",
  "productId": "PRD001",
  "pointsDeducted": 500,
  "voucherCode": "MCD123456789",
  "validTo": "2024-12-31"
}
```

---

## 营销活动

### campaign-calendar - 活动日历查询

**功能说明：**
查询麦当劳中国当月的营销活动日历。

**适用场景：**
- 了解麦当劳优惠活动
- 查看即将开始的活动

**参数：**
无

**返回数据示例：**
```json
{
  "currentMonth": "2024年1月",
  "campaigns": [
    {
      "campaignId": "CAMP001",
      "campaignName": "春节特惠",
      "status": "进行中",
      "startDate": "2024-01-15",
      "endDate": "2024-02-15",
      "description": "春节套餐8折优惠"
    }
  ]
}
```

---

## 工具辅助

### now-time-info - 获取当前时间信息

**功能说明：**
返回当前的完整时间信息。

**适用场景：**
- 确定活动有效期
- 了解订单时间
- 判断营业时间

**参数：**
无

**返回数据示例：**
```json
{
  "timestamp": 1704067200,
  "datetime": "2024-01-01 12:00:00",
  "date": "2024-01-01",
  "time": "12:00:00",
  "weekday": "星期一",
  "timezone": "Asia/Shanghai"
}
```

---

## 常见问题

### Q1: 如何获取门店编码（storeCode）和BE编码（beCode）？

A: 调用 `delivery-query-addresses` 接口，从返回的配送地址列表中获取。

### Q2: 如何获取餐品编码（mealCode）？

A: 先获取门店编码和BE编码，然后调用 `query-meals` 接口查询餐品列表。

### Q3: JSON参数如何传递？

A: 在命令行中使用单引号包裹JSON字符串，例如：
```bash
--items '[{"mealCode":"M001","quantity":1}]'
```

### Q4: 订单创建流程是什么？

A: 标准流程如下：
1. 查询配送地址 → 获取 storeCode、beCode、addressId
2. 查询餐品列表 → 获取 mealCode
3. 查询可用优惠券 → 获取 couponId
4. 计算价格 → 确认总价
5. 创建订单 → 获取支付链接

### Q5: 积分兑换需要注意什么？

A: 
- 兑换前建议查询积分余额
- 兑换会立即扣减积分，请提示用户确认
- 兑换成功后会生成券码，可用于到店消费
