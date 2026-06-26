# 麦当劳 MCP 工具参考

## 🎫 优惠券相关

### available-coupons
查询麦麦省可领取的优惠券列表。

```bash
python3 scripts/mcp_call.py available-coupons
```

**返回示例：**
```json
{
  "data": [
    {
      "couponName": "10.9元麦辣鸡翅",
      "couponImage": "https://img.mcd.cn/...",
      "couponStatus": "HAVING_RECEIVE",
      "label": "已领取"
    }
  ]
}
```

### query-my-coupons
查询用户卡包中的优惠券资产。

**参数：**
- `page`: 页码，默认第1页，最多5页
- `pageSize`: 每页条数，默认200条

```bash
python3 scripts/mcp_call.py query-my-coupons '{"page":"1","pageSize":"50"}'
```

### query-store-coupons
查询指定门店可用的优惠券（需要先获取门店信息）。

**参数：**
- `storeCode`: 门店编码（从 delivery-query-addresses 获取）
- `beCode`: BE编码（从 delivery-query-addresses 获取）

### auto-bind-coupons
自动领取所有可领取的优惠券。

```bash
python3 scripts/mcp_call.py auto-bind-coupons
```

---

## 🍔 点餐相关

### query-meals
查询门店餐品菜单。

**参数：**
- `storeCode`: 门店编码（必填）
- `beCode`: BE编码（必填）

### query-meal-detail
查询餐品详情（套餐选配信息）。

**参数：**
- `code`: 餐品编码
- `storeCode`: 门店编码
- `beCode`: BE编码

### calculate-price
计算订单价格（下单前必须调用）。

**参数：**
- `storeCode`: 门店编码
- `beCode`: BE编码
- `items`: 商品列表
  - `productCode`: 商品编码
  - `quantity`: 数量
  - `couponId`: 优惠券ID（可选）
  - `couponCode`: 优惠券编码（可选）

**返回示例：**
```json
{
  "data": {
    "originalPrice": 5000,    // 原价（分）
    "price": 4500,            // 现价（分）
    "deliveryPrice": 900,     // 配送费（分）
    "packingPrice": 200,      // 打包费（分）
    "discount": 500           // 优惠（分）
  }
}
```

### create-order
创建外卖订单。

**参数：**
- `addressId`: 配送地址ID
- `storeCode`: 门店编码
- `beCode`: BE编码
- `items`: 商品列表

---

## 🚚 外卖配送

### delivery-query-addresses
查询用户配送地址列表（点外卖第一步）。

```bash
python3 scripts/mcp_call.py delivery-query-addresses
```

**返回关键字段：**
- `addressId`: 配送地址ID
- `storeCode`: 可配送门店编码
- `beCode`: BE编码
- `storeName`: 门店名称
- `fullAddress`: 完整地址

### delivery-create-address
创建新的配送地址。

**参数：**
- `city`: 城市名称
- `contactName`: 联系人姓名
- `gender`: 性别（先生/女士）
- `phone`: 手机号（11位）
- `address`: 配送地址
- `addressDetail`: 门牌号

---

## 📦 订单查询

### query-order
查询订单详情。

**参数：**
- `orderId`: 订单号（34位数字字符串）

---

## 🎁 积分商城

### query-my-account
查询积分账户详情。

```bash
python3 scripts/mcp_call.py query-my-account
```

**返回示例：**
```json
{
  "data": {
    "availablePoint": "5000",      // 可用积分
    "accumulativePoint": "50000",  // 累计积分
    "currentMouthExpirePoint": "100"  // 本月将过期
  }
}
```

### mall-points-products
查询可兑换商品列表。

```bash
python3 scripts/mcp_call.py mall-points-products
```

### mall-product-detail
查询商品详情。

**参数：**
- `spuId`: 商品ID

### mall-create-order
创建积分兑换订单。

**参数：**
- `skuId`: 商品SKU ID
- `count`: 兑换数量（默认1）

---

## 📅 其他工具

### campaign-calendar
查询营销活动日历。

**参数：**
- `specifiedDate`: 基准日期（可选，格式：yyyy-MM-dd）

### now-time-info
获取服务器当前时间。

### list-nutrition-foods
查询餐品营养成分数据。

```bash
python3 scripts/mcp_call.py list-nutrition-foods
```
