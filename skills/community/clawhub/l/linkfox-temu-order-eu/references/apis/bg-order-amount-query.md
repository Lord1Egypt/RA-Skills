# 订单金额/供货价查询 — `bg.order.amount.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_order_amount_query.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9（按 `type` 在 Partner EU 后台打开） |
| **网关** | `POST /temu/proxy`，`type`=`bg.order.amount.query`，业务载荷放在 Body 的 `params` |

**Description:** Provide the supply price information corresponding to the orders for the self-developed ERP（为自研 ERP 提供订单对应的供货价/金额信息）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    └── parentOrderSn (STRING, 必填)
```

### `request`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | **是** | Parent order number（父订单号） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-123456789"
  }
}
```

---

## Response（Temu `body` 解析后）

```text
response
├── success
├── errorCode
├── errorMsg
└── result
    ├── parentOrderMap
    │   ├── parentOrderSn
    │   ├── basePriceTotal
    │   ├── shippingAmountTotal
    │   ├── taxTotal
    │   ├── discountFromSeller
    │   ├── discountFromTEMU
    │   ├── refundsTotal
    │   ├── estimatedRevenueDeduction
    │   ├── estimatedRevenue
    │   ├── retailPriceTotal
    │   ├── customerPaid
    │   ├── totalDiscount
    │   └── signOnDelivery
    ├── orderList[]
    │   ├── orderSn
    │   ├── basePrice
    │   ├── unitBasePrice
    │   ├── quantity
    │   ├── unitRetailPrice
    │   ├── discountFromSeller
    │   ├── discountFromTEMU
    │   └── shipAmountTotal
    └── warning[]
```

> 下列带 **`currency` + `amount`** 的金额块结构相同，见 [金额块（MoneyAmount）](#金额块moneyamount)。

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | 订单金额结果 |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| parentOrderMap | OBJECT | Parent order information（父订单金额汇总） |
| orderList | OBJECT[] | Order information（子订单金额明细） |
| warning | STRING[] | warning message（告警信息） |

### `parentOrderMap`

| 参数 | 类型 | 说明 |
|------|------|------|
| parentOrderSn | STRING | Parent order number（父订单号） |
| basePriceTotal | OBJECT | Base price total（基础价/供货价合计） |
| shippingAmountTotal | OBJECT | Shipping total（运费合计） |
| taxTotal | OBJECT | Consumer's paid tax: Calculated on realPrice（消费者已付税费，按 realPrice 计算） |
| discountFromSeller | OBJECT | Discount from seller（卖家折扣） |
| discountFromTEMU | OBJECT | Discount from Temu（平台折扣） |
| refundsTotal | OBJECT | Refunds total（退款合计） |
| estimatedRevenueDeduction | OBJECT | Estimated revenue deduction（预估收入扣减） |
| estimatedRevenue | OBJECT | Estimated revenue（预估收入） |
| retailPriceTotal | OBJECT | Retail price total — Total promotional sale price of the products（零售价/促销售价合计） |
| customerPaid | OBJECT | Total paid — payment of the order from the customer（消费者实付合计） |
| totalDiscount | OBJECT | the amount of discount（折扣合计） |
| signOnDelivery | OBJECT | amount of signature on delivery（签收服务费） |

#### `parentOrderMap` 金额字段公式（官方说明）

| 字段 | 公式 / 说明 |
|------|-------------|
| estimatedRevenue | `estimatedRevenue = basePriceTotal + shippingAmountTotal - estimatedRevenueDeduction + signOnDelivery` |
| customerPaid | `customerPaid = retailPriceTotal + shippingAmountTotal + taxTotal - refundsTotal + signOnDelivery - totalDiscount` |
| totalDiscount | `totalDiscount = discountFromTEMU + discountFromSeller` |
| signOnDelivery | 消费者未购买该服务时返回 **NULL**；签收服务费已退款时返回 **0** |

### `orderList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| orderSn | STRING | Order number (sub-order number)（子订单号） |
| basePrice | OBJECT | Base price（子单基础价/供货价） |
| unitBasePrice | OBJECT | Base price subtotal — unit base price（单位基础价小计） |
| quantity | INTEGER | The quantity of original single items in order（订单原始单品数量） |
| unitRetailPrice | OBJECT | Unit retail price（单位零售价） |
| discountFromSeller | OBJECT | Discount from seller for this product（该商品卖家折扣） |
| discountFromTEMU | OBJECT | Discount from TEMU for this product（该商品平台折扣） |
| shipAmountTotal | OBJECT | shipping cost — Total shipping fee of this product（该商品运费合计） |

---

## 金额块（MoneyAmount）

以下字段均为 **OBJECT**，结构一致：

| 参数 | 类型 | 说明 |
|------|------|------|
| currency | STRING | currency（币种代码） |
| amount | LONG | The minimum currency unit of the local currency（本地货币**最小单位**金额）。例如美国：**Cents（分）** |

适用字段：`basePriceTotal`、`shippingAmountTotal`、`taxTotal`、`discountFromSeller`、`discountFromTEMU`、`refundsTotal`、`estimatedRevenueDeduction`、`estimatedRevenue`、`retailPriceTotal`、`customerPaid`、`totalDiscount`、`signOnDelivery`，以及 `orderList[]` 中的 `basePrice`、`unitBasePrice`、`unitRetailPrice`、`discountFromSeller`、`discountFromTEMU`、`shipAmountTotal`。

> 展示为美元等主币种时，需将 `amount` 除以 100（欧洲站）。

---

## 示例

```bash
python scripts/eu_order_amount_query.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-123456789"
  }
}'
```

ERP 对账时可与 `bg.order.detail.v2.get` 的子单 `orderSn` 对齐查看 `orderList[]` 各行金额。
