# 父售后单详情 — `temu.aftersales.parentaftersales.detail.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_returns_refunds_aftersales_parentaftersales_detail_get.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.aftersales.parentaftersales.detail.get`，业务载荷放在 Body 的 `params` |

**Description:** Query parent after-sales order detail.

> **`parentOrderSn`** 与 **`parentAfterSalesSn`** 均为必填。
> **`refundSummary`** 与 **`afterSalesList`** 在 Partner 导出 HTML 的 Response 表中为折叠行，下列层级按 **Response Example** 全量展开。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── parentOrderSn (STRING, 必填)
    └── parentAfterSalesSn (STRING, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | **是** | Order Number |
| parentAfterSalesSn | STRING | **是** | Parent After-Sales Order Number |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。Partner **Request Example** CURL 将业务字段写在 JSON 顶层；经 LinkFox 网关时建议放在 **`params.request`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-001",
    "parentAfterSalesSn": "PAS-001"
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；嵌套子行在导出 HTML 中多为折叠状态，下列层级按 **Response 表 + Response Example** 全部展开。

```text
response
├── success / errorCode / errorMsg
└── result
    ├── parentAfterSalesSn (STRING)
    ├── availableOperateList[] (INTEGER)
    ├── createAtMillis (LONG)
    ├── parentAfterSalesStatus (INTEGER)
    ├── refundSummary (OBJECT)
    │   ├── discountFromSellerRefund (OBJECT) → currency, amount
    │   ├── discountFromTEMURefund (OBJECT) → currency, amount
    │   ├── buyerTotalRefund (OBJECT) → currency, amount
    │   ├── shippingAmountRefundTaxExcl (OBJECT) → currency, amount
    │   ├── taxTotalRefund (OBJECT) → currency, amount
    │   └── retailPriceRefundTaxExcl (OBJECT) → currency, amount
    ├── parentOrderSn (STRING)
    ├── lastUpdateAtMillis (LONG)
    ├── afterSalesType (INTEGER)
    └── afterSalesList[]
        ├── applyAfterSalesGoodsNumber (INTEGER)
        ├── afterSalesSn (STRING)
        ├── orderSn (STRING)
        ├── applyRefundAmount (OBJECT) → currency, amount
        ├── afterSalesReasonDesc (STRING)
        ├── afterSalesGoodsInfo (OBJECT)
        │   ├── productSkuId, goodsId, skuId
        │   └── productList[] → productSkuId, extCode
        ├── afterSalesReasonCode (INTEGER)
        ├── buyerComment (STRING)
        └── afterSalesStatus (INTEGER)
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | 业务结果对象（见下表） |

### `result` 业务字段

| 参数 | 类型 | 说明 |
|------|------|------|
| parentAfterSalesSn | STRING | Parent after-sales order number（父售后单号） |
| availableOperateList | INTEGER[] | Available operations for the seller（卖家可执行操作码列表） |
| createAtMillis | LONG | Creation time in milliseconds（创建时间，毫秒） |
| parentAfterSalesStatus | INTEGER | Parent after-sales status（父售后单状态码） |
| refundSummary | OBJECT | Refund amount summary（退款金额汇总） |
| parentOrderSn | STRING | Parent order number（父订单号） |
| lastUpdateAtMillis | LONG | Last update time in milliseconds（最后更新时间，毫秒） |
| afterSalesType | INTEGER | After-sales type（售后类型） |
| afterSalesList | OBJECT[] | Child after-sales line list（子售后行列表） |

### `refundSummary` 内金额对象（`discountFromSellerRefund` 等）

各子字段均为 **OBJECT**，结构相同：

| 参数 | 类型 | 说明 |
|------|------|------|
| currency | STRING | Currency code（币种） |
| amount | NUMBER | Amount（金额） |

| 子字段 | 说明 |
|--------|------|
| discountFromSellerRefund | Discount refunded from seller（卖家侧优惠退款） |
| discountFromTEMURefund | Discount refunded from TEMU（平台侧优惠退款） |
| buyerTotalRefund | Total refund to buyer（买家总退款） |
| shippingAmountRefundTaxExcl | Shipping amount refund excluding tax（运费退款，不含税） |
| taxTotalRefund | Total tax refund（税费退款合计） |
| retailPriceRefundTaxExcl | Retail price refund excluding tax（零售价退款，不含税） |

### `afterSalesList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| applyAfterSalesGoodsNumber | INTEGER | Applied after-sales goods quantity（申请售后商品数量） |
| afterSalesSn | STRING | After-sales order number（子售后单号） |
| orderSn | STRING | Order number（子订单号） |
| applyRefundAmount | OBJECT | Applied refund amount（申请退款金额，`currency` + `amount`） |
| afterSalesReasonDesc | STRING | After-sales reason description（售后原因描述） |
| afterSalesGoodsInfo | OBJECT | After-sales goods information（售后商品信息） |
| afterSalesReasonCode | INTEGER | After-sales reason code（售后原因码） |
| buyerComment | STRING | Buyer comment（买家留言） |
| afterSalesStatus | INTEGER | After-sales status（子售后状态码） |

#### `afterSalesGoodsInfo`

| 参数 | 类型 | 说明 |
|------|------|------|
| productSkuId | LONG | Product SKU ID |
| goodsId | LONG | Goods ID |
| skuId | LONG | SKU ID |
| productList | OBJECT[] | Product list（`productSkuId`、`extCode`） |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 130010000 | system error | 见 Partner 文档；修正入参或售后状态后重试 |
| 130010005 | operate forbid | 见 Partner 文档；修正入参或售后状态后重试 |
| 130010001 | The parameter is illegal. Please check if the input parameter meets the regulations. | 见 Partner 文档；修正入参或售后状态后重试 |
| 130010002 | The order has been fully shipped. | 见 Partner 文档；修正入参或售后状态后重试 |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_returns_refunds_aftersales_parentaftersales_detail_get.py '{"accessToken": "TOKEN", "tokenPurpose": "order-shipping", "request": {"parentOrderSn": "PO-001", "parentAfterSalesSn": "PAS-001"}}'
```

**典型流程：** 用列表接口得到的 **`parentAfterSalesSn`** + **`parentOrderSn`** 拉取退款汇总与子售后明细，再决定上传面单/查地址等后续操作。
