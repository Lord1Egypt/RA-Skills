# 订单金额查询 V2 — `temu.order.amount.v2.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_order_amount_v2_query.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9&sub_menu_code=2ae82004ae7644c5a072e9dc1e33eaec |
| **网关** | `POST /temu/proxy`，`type`=`temu.order.amount.v2.query`，业务载荷放在 Body 的 `params` |

**Description:** Query order amount information (V2) with detailed tax-exclusive / tax-inclusive breakdown at parent and sub-order level（订单金额查询 V2：父单与子单维度提供更细的税费拆分字段）。

> **与 V1 区别：** 旧版 [`bg.order.amount.query`](./bg-order-amount-query.md) 字段结构较简；**V2** 使用 **`salesProceeds`** / **`customerPaid`** 分组及更多 `TaxExcl`/`TaxIncl` 明细。  
> 默认 **`site=global`**、**`tokenPurpose=order-shipping`**。

---

## Request 结构（Partner Request 表）

```text
params
└── request (OBJECT)
    └── parentOrderSn (STRING, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | **是** | Parent order number.（父订单号） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "site": "global",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-123456789"
  }
}
```

> Partner **Request Example** CURL 可能将 `parentOrderSn` 写在顶层；经 LinkFox 网关请放在 **`params.request`**。

---

## Response（Partner Response 表，全量展开）

Partner **Response** 表在浏览器另存为 HTML 时仅导出顶层 4 行；下列先列出 **HTML 可见行**，再将 **`result` 下级按 Response 表全部展开**（与 Partner 后台展开一致）。

### Partner Response 表（HTML 导出可见行）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | Order amount result（V2） |

### 结构树（`result` 及下级全部展开）

```text
response
├── success (BOOLEAN)
├── errorCode (INTEGER)
├── errorMsg (STRING)
└── result (OBJECT)
    ├── parentOrderMap (OBJECT)
    │   ├── parentOrderSn (STRING)
    │   ├── salesProceeds (OBJECT)
    │   │   └── …（各金额字段均为 MoneyAmount：currency + amount）
    │   └── customerPaid (OBJECT)
    │       └── …（各金额字段均为 MoneyAmount）
    ├── orderList[] (OBJECT[])
    │   ├── orderSn, quantity, productTaxRate, shipTaxRate
    │   └── …（各金额字段均为 MoneyAmount）
    └── warning[] (STRING[])
```

### 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | Order amount result（V2） |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| parentOrderMap | OBJECT | Parent order amount summary（父订单金额汇总，含 `salesProceeds` 与 `customerPaid`） |
| orderList | OBJECT[] | Sub-order amount details（子订单金额明细列表） |
| warning | STRING[] | Warning messages（告警信息，如部分金额仍在系统计算中） |

### `parentOrderMap`

| 参数 | 类型 | 说明 |
|------|------|------|
| parentOrderSn | STRING | Parent order number（父订单号） |
| salesProceeds | OBJECT | Seller sales proceeds breakdown（卖家侧销售收入/结算相关金额） |
| customerPaid | OBJECT | Customer paid amount breakdown（消费者支付相关金额） |

#### `parentOrderMap.salesProceeds`

| 参数 | 类型 | 说明 |
|------|------|------|
| productTax | MoneyAmount | Product tax（商品税） |
| productTaxCustomerDiscounted | MoneyAmount | Product tax after customer discount |
| shippingTaxCustomerDiscounted | MoneyAmount | Shipping tax after customer discount |
| basePriceSellerDiscount | MoneyAmount | Base price seller discount（卖家基础价折扣） |
| shippingTotalTaxExcl | MoneyAmount | Shipping total tax exclusive（运费合计，不含税） |
| basePriceOff | MoneyAmount | Base price off（基础价减免） |
| basePriceDiscountedTotal | MoneyAmount | Base price discounted total（折后基础价合计） |
| estimatedSettlementTotal | MoneyAmount | Estimated settlement total（预估结算合计） |
| shippingTax | MoneyAmount | Shipping tax |
| productTaxTemu | MoneyAmount | Product tax (Temu portion) |
| shippingTaxTemu | MoneyAmount | Shipping tax (Temu portion) |
| shippingCustomerTotalTaxExcl | MoneyAmount | Customer shipping total tax exclusive |
| estimatedDeduction | MoneyAmount | Estimated deduction（预估扣减） |
| basePriceTotal | MoneyAmount | Base price total（基础价/供货价合计） |
| shippingTemuDiscountTotalTaxExcl | MoneyAmount | Temu shipping discount total tax exclusive |

#### `parentOrderMap.customerPaid`

| 参数 | 类型 | 说明 |
|------|------|------|
| retailPriceDiscountedTotalTaxExcl | MoneyAmount | Retail price discounted total tax exclusive |
| productRefundsTotal | MoneyAmount | Product refunds total（商品退款合计） |
| retailPriceTemuDiscountTaxExcl | MoneyAmount | Retail price Temu discount tax exclusive |
| retailPriceSellerDiscountTaxExcl | MoneyAmount | Retail price seller discount tax exclusive |
| retailPriceTotalTaxIncl | MoneyAmount | Retail price total tax inclusive |
| shippingDiscountedTotalTaxExcl | MoneyAmount | Shipping discounted total tax exclusive |
| shippingTotalTaxExcl | MoneyAmount | Shipping total tax exclusive |
| shippingTaxTemuDiscount | MoneyAmount | Shipping tax Temu discount |
| shippingTax | MoneyAmount | Shipping tax |
| customerPaidTotal | MoneyAmount | Customer paid total（消费者实付合计） |
| retailPriceTotalTaxExcl | MoneyAmount | Retail price total tax exclusive |
| shippingTaxDiscounted | MoneyAmount | Shipping tax discounted |
| productTaxDiscounted | MoneyAmount | Product tax discounted |
| shippingTemuDiscountTotalTaxExcl | MoneyAmount | Temu shipping discount total tax exclusive |
| shippingTotalTaxIncl | MoneyAmount | Shipping total tax inclusive |

### `orderList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| orderSn | STRING | Order number (sub-order)（子订单号） |
| quantity | INTEGER | Quantity（数量） |
| productTaxRate | INTEGER/NUMBER | Product tax rate（商品税率） |
| shipTaxRate | INTEGER/NUMBER | Shipping tax rate（运费税率） |
| productTax | MoneyAmount | Product tax |
| productTaxCustomerDiscounted | MoneyAmount | Product tax customer discounted |
| shippingTaxCustomerDiscounted | MoneyAmount | Shipping tax customer discounted |
| retailPriceTotalTaxIncl | MoneyAmount | Retail price total tax inclusive |
| basePriceSellerDiscount | MoneyAmount | Base price seller discount |
| shippingTotalTaxExcl | MoneyAmount | Shipping total tax exclusive |
| basePriceOff | MoneyAmount | Base price off |
| estimatedSettlementTotal | MoneyAmount | Estimated settlement total |
| shippingTax | MoneyAmount | Shipping tax |
| productTaxTemu | MoneyAmount | Product tax Temu |
| shippingCustomerTotalTaxExcl | MoneyAmount | Shipping customer total tax exclusive |
| unitRetailPriceTaxExcl | MoneyAmount | Unit retail price tax exclusive |
| shippingTemuDiscountTotalTaxExcl | MoneyAmount | Shipping Temu discount total tax exclusive |
| shippingTotalTaxIncl | MoneyAmount | Shipping total tax inclusive |
| retailPriceDiscountedTotalTaxExcl | MoneyAmount | Retail price discounted total tax exclusive |
| retailPriceTemuDiscountTaxExcl | MoneyAmount | Retail price Temu discount tax exclusive |
| unitRetailPriceTaxIncl | MoneyAmount | Unit retail price tax inclusive |
| basePriceDiscountedTotal | MoneyAmount | Base price discounted total |
| unitBasePrice | MoneyAmount | Unit base price |
| shippingTaxTemu | MoneyAmount | Shipping tax Temu |
| retailPriceTotalTaxExcl | MoneyAmount | Retail price total tax exclusive |
| estimatedDeduction | MoneyAmount | Estimated deduction |
| basePriceTotal | MoneyAmount | Base price total |

---

## 金额块（MoneyAmount）

除 **`quantity`**、**`productTaxRate`**、**`shipTaxRate`**、**`orderSn`**、**`parentOrderSn`**、**`warning`** 外，上表中标为 **MoneyAmount** 的字段均为 **OBJECT**：

| 参数 | 类型 | 说明 |
|------|------|------|
| currency | STRING | Currency code（币种） |
| amount | LONG | Amount in local minimum currency unit（本地货币最小单位） |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 140020015 | This API is not applicable to the country or region where the current store is located. | 确认店铺区域与 `site=global`；换适用接口或站点 |
| 140020002 | Order not found | 核对 `parentOrderSn` |
| 140020008 | Some amount fields are still undergoing system calculation. Please try again later. | 稍后重试；关注 `result.warning` |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_order_amount_v2_query.py '{
  "accessToken": "TOKEN",
  "site": "global",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-123456789"
  }
}'
```

**典型流程：** `bg.order.list.v2.get` 取得 **`parentOrderSn`** → 本接口拉 V2 金额明细 → ERP 与 `orderList[].orderSn` 对账。
