# 订单金额查询 V3 — `temu.order.amount.v3.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_order_amount_v3_query.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9&sub_menu_code=3ffe9c4c79b9418285eb7ec09cf7b329 |
| **网关** | `POST /temu/proxy`，`type`=`temu.order.amount.v3.query`，业务载荷放在 Body 的 `params` |

**Description:** Query order amount information (V3) with tax-inclusive oriented amount fields（订单金额查询 V3：字段以含税价 TaxIncl 为主，结构相对 V2 精简）。

> **与 V2 区别：** [`temu.order.amount.v2.query`](./temu-order-amount-v2-query.md) 提供更细的税费拆分（含大量 `TaxExcl` 字段）；**V3** 侧重 **`TaxIncl`** 汇总字段。按店铺所在国/区域与 Partner 指引选择版本。

> **网关鉴权字段**由本 skill 处理；建议使用 **`tokenPurpose=order-shipping`**，**`site=eu`**。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    └── parentOrderSn (STRING, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | **是** | Parent order number（父订单号） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "site": "eu",
  "request": {
    "parentOrderSn": "PO-123456789"
  }
}
```

---

## Response（Temu `body` 解析后）

```text
response
├── success / errorCode / errorMsg
└── result
    ├── parentOrderMap (OBJECT)
    │   ├── parentOrderSn (STRING)
    │   ├── salesProceeds (OBJECT) → MoneyAmount 字段
    │   └── customerPaid (OBJECT) → MoneyAmount 字段
    ├── orderList[] (OBJECT[])
    └── warning[] (STRING[])
```

### 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | Order amount result（V3） |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| parentOrderMap | OBJECT | Parent order amount summary |
| orderList | OBJECT[] | Sub-order amount details |
| warning | STRING[] | Warning messages |

### `parentOrderMap`

| 参数 | 类型 | 说明 |
|------|------|------|
| parentOrderSn | STRING | Parent order number |
| salesProceeds | OBJECT | Seller sales proceeds（卖家侧金额） |
| customerPaid | OBJECT | Customer paid breakdown（消费者支付金额） |

#### `parentOrderMap.salesProceeds`

| 参数 | 类型 | 说明 |
|------|------|------|
| basePriceDiscountedTotal | MoneyAmount | Base price discounted total |
| estimatedSettlementTotal | MoneyAmount | Estimated settlement total |
| basePriceSellerDiscount | MoneyAmount | Base price seller discount |
| shippingCustomerTotalTaxIncl | MoneyAmount | Customer shipping total tax inclusive |
| shippingTemuDiscountTotalTaxIncl | MoneyAmount | Temu shipping discount total tax inclusive |
| estimatedDeduction | MoneyAmount | Estimated deduction |
| basePriceOff | MoneyAmount | Base price off |
| basePriceTotal | MoneyAmount | Base price total |
| shippingTotalTaxIncl | MoneyAmount | Shipping total tax inclusive |

#### `parentOrderMap.customerPaid`

| 参数 | 类型 | 说明 |
|------|------|------|
| retailPriceDiscountedTotalTaxIncl | MoneyAmount | Retail price discounted total tax inclusive |
| productRefundsTotal | MoneyAmount | Product refunds total |
| customerPaidTotal | MoneyAmount | Customer paid total |
| retailPriceTotalTaxIncl | MoneyAmount | Retail price total tax inclusive |
| retailPriceSellerDiscountTaxIncl | MoneyAmount | Retail price seller discount tax inclusive |
| shippingDiscountedTotalTaxIncl | MoneyAmount | Shipping discounted total tax inclusive |
| shippingTemuDiscountTotalTaxIncl | MoneyAmount | Temu shipping discount total tax inclusive |
| retailPriceTemuDiscountTaxIncl | MoneyAmount | Retail price Temu discount tax inclusive |
| shippingTotalTaxIncl | MoneyAmount | Shipping total tax inclusive |

### `orderList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| orderSn | STRING | Sub-order number |
| quantity | INTEGER | Quantity |
| retailPriceTotalTaxIncl | MoneyAmount | Retail price total tax inclusive |
| basePriceSellerDiscount | MoneyAmount | Base price seller discount |
| shippingTemuDiscountTotalTaxIncl | MoneyAmount | Shipping Temu discount total tax inclusive |
| unitRetailPriceTaxIncl | MoneyAmount | Unit retail price tax inclusive |
| basePriceOff | MoneyAmount | Base price off |
| basePriceDiscountedTotal | MoneyAmount | Base price discounted total |
| estimatedSettlementTotal | MoneyAmount | Estimated settlement total |
| retailPriceDiscountedTotalTaxIncl | MoneyAmount | Retail price discounted total tax inclusive |
| unitBasePrice | MoneyAmount | Unit base price |
| shippingCustomerTotalTaxIncl | MoneyAmount | Shipping customer total tax inclusive |
| estimatedDeduction | MoneyAmount | Estimated deduction |
| retailPriceTemuDiscountTaxIncl | MoneyAmount | Retail price Temu discount tax inclusive |
| basePriceTotal | MoneyAmount | Base price total |
| shippingTotalTaxIncl | MoneyAmount | Shipping total tax inclusive |

---

## 金额块（MoneyAmount）

结构同 [temu-order-amount-v2-query.md](./temu-order-amount-v2-query.md#金额块moneyamount)：`currency` + `amount`（本地最小货币单位）。

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 140020015 | This API is not applicable to the country or region where the current store is located. | 确认店铺区域；必要时改用 V2 或 `bg.order.amount.query` |
| 140020002 | Order not found | 核对 `parentOrderSn` |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_order_amount_v3_query.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "site": "eu",
  "request": {
    "parentOrderSn": "PO-123456789"
  }
}'
```

**典型流程：** 欧洲含税价对账优先 **V3**；需细粒度税费拆分时用 **V2**。
