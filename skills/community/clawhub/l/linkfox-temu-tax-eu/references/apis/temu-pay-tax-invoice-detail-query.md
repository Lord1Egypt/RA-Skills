# 发票明细查询 — `temu.pay.tax.invoice.detail.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_tax_invoice_detail_query.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=3985fe93bff5437c87863a22112b72db |
| **网关** | `POST /temu/proxy`，`type`=`temu.pay.tax.invoice.detail.query`，业务载荷放在 Body 的 `params` |

**Description:** Query invoice detail information by parent order.

> **网关鉴权字段**由本 skill 处理；业务参数见下方 **`request`**。默认 **`site=eu`**、**`tokenPurpose=product-inventory`**。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT)
    └── parentOrderSn (STRING **必填**)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | **是** | parent order number |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "site": "eu",
  "request": {}
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 嵌套子行在导出 HTML 中多为折叠状态；下列层级按 **Response 表 + Response Example** 全部展开。

```text
response
├── success (BOOLEAN)
├── errorCode (INTEGER)
├── errorMsg (STRING)
└── result (OBJECT)
    ├── invoiceDetailInfoList[] (OBJECT[])
    ├── invoiceDetailInfoList[].orderMetaInfo (OBJECT)
    ├── invoiceDetailInfoList[].orderMetaInfo.isCustomerServiceChargeOrder (BOOLEAN)
    ├── invoiceDetailInfoList[].orderMetaInfo.parentAppealOrderSn (STRING)
    ├── invoiceDetailInfoList[].orderMetaInfo.originParentOrderTimeMillis (INTEGER)
    ├── invoiceDetailInfoList[].orderMetaInfo.orderTimeMillis (INTEGER)
    ├── invoiceDetailInfoList[].orderMetaInfo.tradeTransactionSn (STRING)
    ├── invoiceDetailInfoList[].orderMetaInfo.parentOrderSn (STRING)
    ├── invoiceDetailInfoList[].orderMetaInfo.parentShippingTimeMillis (INTEGER)
    ├── invoiceDetailInfoList[].orderMetaInfo.refundTimeMillis (INTEGER)
    ├── invoiceDetailInfoList[].orderMetaInfo.originParentOrderSn (STRING)
    ├── invoiceDetailInfoList[].orderMetaInfo.financeParentOrderSn (STRING)
    ├── invoiceDetailInfoList[].platformInfo (OBJECT)
    ├── invoiceDetailInfoList[].platformInfo.platformName (STRING)
    ├── invoiceDetailInfoList[].platformInfo.platformAddress (STRING)
    ├── invoiceDetailInfoList[].shippingFee (OBJECT)
    ├── invoiceDetailInfoList[].shippingFee.shippingAmountWithTax (INTEGER)
    ├── invoiceDetailInfoList[].shippingFee.shippingAmountExcludeTax (INTEGER)
    ├── invoiceDetailInfoList[].goodsInfoList[] (OBJECT[])
    ├── invoiceDetailInfoList[].goodsInfoList[].unitPriceWithVAT (INTEGER)
    ├── invoiceDetailInfoList[].goodsInfoList[].skuSpec (STRING)
    ├── invoiceDetailInfoList[].goodsInfoList[].quantity (INTEGER)
    ├── invoiceDetailInfoList[].goodsInfoList[].vatRateBase (INTEGER)
    ├── invoiceDetailInfoList[].goodsInfoList[].orderSn (STRING)
    ├── invoiceDetailInfoList[].goodsInfoList[].vatRate (INTEGER)
    ├── invoiceDetailInfoList[].goodsInfoList[].description (STRING)
    ├── invoiceDetailInfoList[].goodsInfoList[].unitPriceExcludeVAT (INTEGER)
    ├── invoiceDetailInfoList[].goodsInfoList[].totalGoodsAmount (INTEGER)
    ├── invoiceDetailInfoList[].invoiceDetailType (INTEGER)
    ├── invoiceDetailInfoList[].shippingInfoList[] (OBJECT[])
    ├── invoiceDetailInfoList[].shippingInfoList[].unitPriceWithVAT (INTEGER)
    ├── invoiceDetailInfoList[].shippingInfoList[].skuSpec (STRING)
    ├── invoiceDetailInfoList[].shippingInfoList[].quantity (INTEGER)
    ├── invoiceDetailInfoList[].shippingInfoList[].vatRateBase (INTEGER)
    ├── invoiceDetailInfoList[].shippingInfoList[].orderSn (STRING)
    ├── invoiceDetailInfoList[].shippingInfoList[].vatRate (INTEGER)
    ├── invoiceDetailInfoList[].shippingInfoList[].description (STRING)
    ├── invoiceDetailInfoList[].shippingInfoList[].unitPriceExcludeVAT (INTEGER)
    ├── invoiceDetailInfoList[].shippingInfoList[].totalGoodsAmount (INTEGER)
    ├── invoiceDetailInfoList[].invoiceType (INTEGER)
    ├── invoiceDetailInfoList[].currency (STRING)
    ├── invoiceDetailInfoList[].promotionInfo (OBJECT)
    ├── invoiceDetailInfoList[].promotionInfo.promotionAmountExcludeTax (INTEGER)
    ├── invoiceDetailInfoList[].promotionInfo.promotionAmountWithTax (INTEGER)
    ├── invoiceDetailInfoList[].addOrderInfoList[] (OBJECT[])
    ├── invoiceDetailInfoList[].addOrderInfoList[].amountWithTax (INTEGER)
    ├── invoiceDetailInfoList[].addOrderInfoList[].amountExcludeTax (INTEGER)
    ├── invoiceDetailInfoList[].addOrderInfoList[].addOrderDetailType (INTEGER)
```

### 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | Business result |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| invoiceDetailInfoList[] | OBJECT[] | invoiceDetailInfoList（OBJECT[]） |
| invoiceDetailInfoList[].orderMetaInfo | OBJECT | orderMetaInfo（OBJECT） |
| invoiceDetailInfoList[].orderMetaInfo.isCustomerServiceChargeOrder | BOOLEAN | isCustomerServiceChargeOrder（BOOLEAN） |
| invoiceDetailInfoList[].orderMetaInfo.parentAppealOrderSn | STRING | parentAppealOrderSn（STRING） |
| invoiceDetailInfoList[].orderMetaInfo.originParentOrderTimeMillis | INTEGER | originParentOrderTimeMillis（INTEGER） |
| invoiceDetailInfoList[].orderMetaInfo.orderTimeMillis | INTEGER | orderTimeMillis（INTEGER） |
| invoiceDetailInfoList[].orderMetaInfo.tradeTransactionSn | STRING | tradeTransactionSn（STRING） |
| invoiceDetailInfoList[].orderMetaInfo.parentOrderSn | STRING | parentOrderSn（STRING） |
| invoiceDetailInfoList[].orderMetaInfo.parentShippingTimeMillis | INTEGER | parentShippingTimeMillis（INTEGER） |
| invoiceDetailInfoList[].orderMetaInfo.refundTimeMillis | INTEGER | refundTimeMillis（INTEGER） |
| invoiceDetailInfoList[].orderMetaInfo.originParentOrderSn | STRING | originParentOrderSn（STRING） |
| invoiceDetailInfoList[].orderMetaInfo.financeParentOrderSn | STRING | financeParentOrderSn（STRING） |
| invoiceDetailInfoList[].platformInfo | OBJECT | platformInfo（OBJECT） |
| invoiceDetailInfoList[].platformInfo.platformName | STRING | platformName（STRING） |
| invoiceDetailInfoList[].platformInfo.platformAddress | STRING | platformAddress（STRING） |
| invoiceDetailInfoList[].shippingFee | OBJECT | shippingFee（OBJECT） |
| invoiceDetailInfoList[].shippingFee.shippingAmountWithTax | INTEGER | shippingAmountWithTax（INTEGER） |
| invoiceDetailInfoList[].shippingFee.shippingAmountExcludeTax | INTEGER | shippingAmountExcludeTax（INTEGER） |
| invoiceDetailInfoList[].goodsInfoList[] | OBJECT[] | goodsInfoList（OBJECT[]） |
| invoiceDetailInfoList[].goodsInfoList[].unitPriceWithVAT | INTEGER | unitPriceWithVAT（INTEGER） |
| invoiceDetailInfoList[].goodsInfoList[].skuSpec | STRING | skuSpec（STRING） |
| invoiceDetailInfoList[].goodsInfoList[].quantity | INTEGER | quantity（INTEGER） |
| invoiceDetailInfoList[].goodsInfoList[].vatRateBase | INTEGER | vatRateBase（INTEGER） |
| invoiceDetailInfoList[].goodsInfoList[].orderSn | STRING | orderSn（STRING） |
| invoiceDetailInfoList[].goodsInfoList[].vatRate | INTEGER | vatRate（INTEGER） |
| invoiceDetailInfoList[].goodsInfoList[].description | STRING | description（STRING） |
| invoiceDetailInfoList[].goodsInfoList[].unitPriceExcludeVAT | INTEGER | unitPriceExcludeVAT（INTEGER） |
| invoiceDetailInfoList[].goodsInfoList[].totalGoodsAmount | INTEGER | totalGoodsAmount（INTEGER） |
| invoiceDetailInfoList[].invoiceDetailType | INTEGER | invoiceDetailType（INTEGER） |
| invoiceDetailInfoList[].shippingInfoList[] | OBJECT[] | shippingInfoList（OBJECT[]） |
| invoiceDetailInfoList[].shippingInfoList[].unitPriceWithVAT | INTEGER | unitPriceWithVAT（INTEGER） |
| invoiceDetailInfoList[].shippingInfoList[].skuSpec | STRING | skuSpec（STRING） |
| invoiceDetailInfoList[].shippingInfoList[].quantity | INTEGER | quantity（INTEGER） |
| invoiceDetailInfoList[].shippingInfoList[].vatRateBase | INTEGER | vatRateBase（INTEGER） |
| invoiceDetailInfoList[].shippingInfoList[].orderSn | STRING | orderSn（STRING） |
| invoiceDetailInfoList[].shippingInfoList[].vatRate | INTEGER | vatRate（INTEGER） |
| invoiceDetailInfoList[].shippingInfoList[].description | STRING | description（STRING） |
| invoiceDetailInfoList[].shippingInfoList[].unitPriceExcludeVAT | INTEGER | unitPriceExcludeVAT（INTEGER） |
| invoiceDetailInfoList[].shippingInfoList[].totalGoodsAmount | INTEGER | totalGoodsAmount（INTEGER） |
| invoiceDetailInfoList[].invoiceType | INTEGER | invoiceType（INTEGER） |
| invoiceDetailInfoList[].currency | STRING | currency（STRING） |
| invoiceDetailInfoList[].promotionInfo | OBJECT | promotionInfo（OBJECT） |
| invoiceDetailInfoList[].promotionInfo.promotionAmountExcludeTax | INTEGER | promotionAmountExcludeTax（INTEGER） |
| invoiceDetailInfoList[].promotionInfo.promotionAmountWithTax | INTEGER | promotionAmountWithTax（INTEGER） |
| invoiceDetailInfoList[].addOrderInfoList[] | OBJECT[] | addOrderInfoList（OBJECT[]） |
| invoiceDetailInfoList[].addOrderInfoList[].amountWithTax | INTEGER | amountWithTax（INTEGER） |
| invoiceDetailInfoList[].addOrderInfoList[].amountExcludeTax | INTEGER | amountExcludeTax（INTEGER） |
| invoiceDetailInfoList[].addOrderInfoList[].addOrderDetailType | INTEGER | addOrderDetailType（INTEGER） |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_tax_invoice_detail_query.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "site": "eu",
  "request": {}
}'
```
