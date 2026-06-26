# 订单详情查询 V2 — `bg.order.detail.v2.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_order_detail_v2_get.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation（`menu_code` / `sub_menu_code` 以 Partner 后台该接口页为准） |
| **网关** | `POST /temu/proxy`，`type`=`bg.order.detail.v2.get`，业务载荷放在 Body 的 `params` |

**Description:** The `bg.order.detail.v2.get` interface is designed for merchants to retrieve detailed information about a specific order within their respective stores. This functionality provides merchants with access to comprehensive order details, enabling them to process, fulfill, and manage individual orders with precision.

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    ├── parentOrderSn (STRING, 必填)
    └── fulfillmentTypeList[] (STRING[], 否)
```

### `request`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | **是** | Parent order number（父订单号） |
| fulfillmentTypeList | STRING[] | 否 | The type of order fulfillment（订单履约类型），见下表 |

#### `fulfillmentTypeList[]`

| 值 | 说明 |
|----|------|
| `fulfillBySeller` | fulfill by seller（卖家履约） |
| `fulfillByCooperativeWarehouse` | fulfill by Cooperative Warehouse（合作仓履约） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-123456789",
    "fulfillmentTypeList": ["fulfillBySeller"]
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
    │   ├── parentOrderStatus
    │   ├── parentOrderTime
    │   ├── expectShipLatestTime
    │   ├── parentOrderPendingFinishTime
    │   ├── latestDeliveryTime
    │   ├── parentShippingTime
    │   ├── siteId
    │   ├── regionId
    │   ├── parentOrderLabel[]
    │   │   ├── name
    │   │   └── value
    │   ├── fulfillmentWarning[]
    │   ├── hasShippingFee
    │   ├── regionName1 / regionName2 / regionName3
    │   ├── orderPaymentType
    │   ├── batchOrderNumberList[]
    │   ├── shippingMethod
    │   ├── isShipmentConsolidatedByMainMall
    │   └── parentConfirmTime
    └── orderList[]
        ├── orderSn
        ├── quantity
        ├── canceledQuantityBeforeShipment
        ├── originalOrderQuantity
        ├── goodsId
        ├── packageSnInfo[]
        │   ├── packageSn
        │   ├── packageDeliveryType
        │   └── callSuccess
        ├── packageAbnormalTypeList[]
        ├── skuId
        ├── spec
        ├── originalSpecName
        ├── thumbUrl
        ├── goodsName
        ├── originalGoodsName
        ├── orderStatus
        ├── productList[]
        │   ├── productId
        │   ├── productSkuId
        │   ├── soldFactor
        │   └── extCode
        ├── orderLabel[]
        │   ├── name
        │   └── value
        ├── fulfillmentWarning[]
        ├── fulfillmentType
        ├── inventoryDeductionWarehouseId
        ├── inventoryDeductionWarehouseName
        ├── orderPaymentType
        ├── isCancelledDuringPending
        ├── earliestTimeBuyShippingLabel
        ├── earliestTimeGetShippingDocument
        ├── orderShippingTime
        ├── isShipmentConsolidatedByMainMall
        ├── orderCreateTime
        ├── qualificationUploadEndTime
        └── hasUploadedEvidence
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | result |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| parentOrderMap | OBJECT | Parent order information（父订单信息） |
| orderList | OBJECT[] | Order information（子订单列表） |

### `parentOrderMap`

| 参数 | 类型 | 说明 |
|------|------|------|
| parentOrderSn | STRING | Parent order number（父订单号） |
| parentOrderStatus | INTEGER | Status of the parent order：`1` PENDING；`2` UN_SHIPPING；`3` CANCELED；`4` SHIPPED；`41` PARTIALLY_SHIPPED；`5` DELIVERED；`51` PARTIALLY_DELIVERED |
| parentOrderTime | INTEGER | Time when the parent order was placed（下单时间，秒） |
| expectShipLatestTime | INTEGER | Latest shipment time（最晚发货时间，秒） |
| parentOrderPendingFinishTime | INTEGER | Time when the parent order finish pending（待处理完成时间，秒） |
| latestDeliveryTime | INTEGER | Latest delivery time（最晚送达时间，秒） |
| parentShippingTime | INTEGER | Time when the parent order was shipped（父订单发货时间，秒） |
| siteId | LONG | Site ID |
| regionId | LONG | Region ID，e.g. USA - **211** |
| parentOrderLabel | OBJECT[] | List of PO order status labels（父订单状态标签） |
| fulfillmentWarning | STRING[] | Fulfillment Prompt（履约提示），见下表 |
| hasShippingFee | BOOLEAN | 用户实付运费是否为零：`true` 为零，`false` 非零（**only for local mall**） |
| regionName1 | STRING | Address region 1（地址区域 1） |
| regionName2 | STRING | Address region 2 |
| regionName3 | STRING | Address region 3 |
| orderPaymentType | STRING | Order payment type：`COD`、`PPD` |
| batchOrderNumberList | STRING[] | batchOrderNumberList；**仅合作仓履约**有值，否则为空 |
| shippingMethod | INTEGER | delivery channel type：`1` Standard Shipping，`2` Store Delivery，`3` Customer Pickup |
| isShipmentConsolidatedByMainMall | BOOLEAN | 为 `true` 表示 PO 已由主站合并发货，需在主站侧确认发货/面单 |
| parentConfirmTime | INTEGER | Confirmation time of parent order in seconds (timestamp) |

#### `parentOrderMap.parentOrderLabel[]` — `name` 常见值

| name | 说明 |
|------|------|
| `soon_to_be_overdue` | 即将逾期 |
| `past_due` | 已逾期 |
| `pending_buyer_cancellation` | 买家取消待处理 |
| `pending_buyer_address_change` | 买家改地址待处理 |
| `pending_risk_control_alert` | 风控预警待处理 |
| `signature_required_on_delivery` | 需要签收 |

| 参数 | 类型 | 说明 |
|------|------|------|
| name | STRING | Label name |
| value | INTEGER | Whether the label exists：`0` = no label，`1` = label exists |

#### `parentOrderMap.fulfillmentWarning[]`

| 值 | 说明 |
|----|------|
| `SUGGEST_SIGNATURE_ON_DELIVERY` | It is recommended to purchase signature service for this order to ensure fulfillment |
| `CONFIRMED_CHANGED_ADDRESS` | Address has been changed and confirmed; pull the order again for the latest address |
| `RESTRICT_FEDEX_SELF_SHIPPING` | Restricted from confirming shipment by FedEx tracking number |
| `RESTRICT_USPS_SELF_SHIPPING` | Restricted from confirming shipment by USPS tracking number |
| `RESTRICT_SELF_SHIPPING` | Restricted from confirming shipment by tracking number |
| `BLOCK_LOGISTICS_PROVIDERS_{Name1,Name2,...}` | Consumer blocked some logistics providers (names in response) |
| `REQUIRES_CUSTOMER_PICKUP` | This order can only be fulfilled via customer pickup |

### `orderList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| orderSn | STRING | Order number (sub-order number)（子订单号） |
| quantity | INTEGER | The quantity seller needs to fulfill：`quantity = originalOrderQuantity - canceledQuantityBeforeShipment` |
| canceledQuantityBeforeShipment | INTEGER | The quantity of canceled before shipment |
| originalOrderQuantity | INTEGER | originalOrderQuantity |
| goodsId | LONG | Goods ID |
| packageSnInfo | OBJECT[] | package information（包裹信息） |
| packageAbnormalTypeList | STRING[] | Logistics anomalies after shipment，见下表 |
| skuId | LONG | Sku id；**It is only valid for LOCAL sellers not SEMI sellers** |
| spec | STRING | Product specification description for customer |
| originalSpecName | STRING | Product specification for seller；**Only for orders whose confirmation time is within no more than six months** |
| thumbUrl | STRING | Thumbnail image URL |
| goodsName | STRING | Product name for customer |
| originalGoodsName | STRING | Product name for seller；**Only for orders whose confirmation time is within no more than six months** |
| orderStatus | INTEGER | Status of the order：`1` PENDING；`2` UN_SHIPPING；`3` CANCELED；`4` SHIPPED；`41` PARTIALLY_SHIPPED；`5` DELIVERED；`51` PARTIALLY_DELIVERED |
| productList | OBJECT[] | Product information；**仅 SEMI 卖家有效，非 LOCAL** |
| orderLabel | OBJECT[] | The label of order（子订单标签） |
| fulfillmentWarning | STRING[] | Fulfillment Prompt（子订单履约提示），见下表 |
| fulfillmentType | STRING | `fulfillBySeller` / `fulfillByCooperativeWarehouse` |
| inventoryDeductionWarehouseId | STRING | The id of inventory deduction warehouse |
| inventoryDeductionWarehouseName | STRING | The name of inventory deduction warehouse |
| orderPaymentType | STRING | Order payment type：`COD`、`PPD` |
| isCancelledDuringPending | BOOLEAN | Whether the order is completely cancelled during the pending period |
| earliestTimeBuyShippingLabel | INTEGER | Order can only buy shipping label after this time |
| earliestTimeGetShippingDocument | INTEGER | Order can only get shipping document after this time |
| orderShippingTime | INTEGER | Time when the order was shipped；若含未发货或延迟包裹，返回 **null** |
| isShipmentConsolidatedByMainMall | BOOLEAN | 主站合并发货标记 |
| orderCreateTime | INTEGER | The time when the order was created |
| qualificationUploadEndTime | LONG | Deadline for uploading order qualification documents |
| hasUploadedEvidence | BOOLEAN | Whether the merchant has uploaded verification information such as SN, IMEI, and appraisal report |

### `packageSnInfo[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| packageSn | STRING | package number of this order |
| packageDeliveryType | INTEGER | Package delivery type：`1` Seller non-integrated；`2` Seller Temu-integrated；`3` Cooperative warehouse non-integrated；`4` Cooperative warehouse Temu-integrated |
| callSuccess | BOOLEAN | Whether the latest request `bg.logistics.shipment.create` is successful；与 Temu 非集成物流无关 |

#### `orderList[].packageAbnormalTypeList[]`

| 值 | 说明 |
|----|------|
| `WRONG_SHIPPING_ADDRESS` | Wrong shipping address |
| `SUSPECTED_ERROR_PROVIDER` | Suspected error provider |
| `NO_TRACK` | No track |
| `TRACK_TOO_EARLY` | Track too early |
| `OVERTIME_COLLECTION` | Overtime collection |
| `TRACK_COLLECT_FAIL` | Track collect fail |
| `SIGNED_BUT_UNRECEIVED_TASK` | Signed but unreceived task |

#### `productList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| productId | LONG | Product Id |
| productSkuId | LONG | Product sku id；**It is only valid for SEMI sellers not LOCAL sellers** |
| soldFactor | LONG | Conversion factor between product quantity and item quantity |
| extCode | STRING | Item code |

#### `orderList[].orderLabel[]` — `name` 常见值

`customized_products`、`US_to_CA`、`is_US_to_CA_BBC`、`Y2_advance_sale`、`pre_sale_order`、`made_to_order`、`vacation_order`、`second_hand_collectible_order`、`second_hand_luxury_order`

| 参数 | 类型 | 说明 |
|------|------|------|
| name | STRING | Label name |
| value | INTEGER | Is there a label：`0` = no label，`1` = labeled；BBC orders need to judge combined with `is_US_to_CA_BBC` |

#### `orderList[].fulfillmentWarning[]`

| 值 | 说明 |
|----|------|
| `SAVE_SN_INFORMATION_FOR_RETURN` | It is recommended to save sn information for this order to identify the authenticity of the returned goods |
| `REQUIRES_AUTHENTICATION_REPORT_SUBMISSION` | Requires submission of an authentication report in Temu Seller Center；超时自动取消并可能处罚 |
| `REQUIRES_AGE_VERIFICATION` | It is recommended to purchase the age verification service for the signatory |
| `SPECIFIC_LOGISTICS_REQUIRED` | It is required to choose specific logistics to fulfill this order |
| `REQUIRES_CUSTOMER_PICKUP` | This order can only be fulfilled via customer pickup |

---

## 示例

```bash
python scripts/us_order_detail_v2_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-123456789"
  }
}'
```

可先通过 `bg.order.list.v2.get` 获取 `parentOrderSn`，再调用本接口拉取完整详情。
