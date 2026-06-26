# 订单列表查询 V2 — `bg.order.list.v2.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_order_list_v2_get.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9（按 `type` 在 Partner EU 后台打开） |
| **网关** | `POST /temu/proxy`，`type`=`bg.order.list.v2.get`，业务载荷放在 Body 的 `params` |

**Description:** The `bg.order.list.v2.get` interface is designed to support batch return of corresponding order lists based on filtering criteria（按筛选条件批量返回订单列表）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    ├── pageNumber
    ├── pageSize
    ├── parentOrderStatus
    ├── parentOrderSnList[]
    ├── createAfter / createBefore
    ├── expectShipLatestTimeStart / expectShipLatestTimeEnd
    ├── updateAtStart / updateAtEnd
    ├── parentConfirmTimeStart / parentConfirmTimeEnd
    ├── regionId
    ├── fulfillmentTypeList[]
    ├── parentOrderLabel[]
    ├── packageAbnormalTypeList[]
    ├── sortby
    ├── hasPreSaleOrder
    ├── hasQualificationRequiredOrder
    └── skuId
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageNumber | INTEGER | 否 | Page number for pagination（页码），**默认 1** |
| pageSize | INTEGER | 否 | Page size for pagination（每页条数），**默认 10**，**最大 100** |
| parentOrderStatus | INTEGER | 否 | Parent order status（父订单状态）；**默认查询全部** |
| parentOrderSnList | STRING[] | 否 | List of parent order numbers（父订单号列表），**单次最多 20 条** |
| createAfter | INTEGER | 否 | Start time for querying parent order creation, in seconds (timestamp)；**须与 `createBefore` 成对使用** |
| createBefore | INTEGER | 否 | End time for querying parent order creation, in seconds (timestamp)，**闭区间**；**须与 `createAfter` 成对使用** |
| expectShipLatestTimeStart | INTEGER | 否 | Start time for querying expected latest shipment, in seconds |
| expectShipLatestTimeEnd | INTEGER | 否 | End time for querying expected latest shipment, in seconds |
| updateAtStart | INTEGER | 否 | Start time for querying order update / status change, in seconds (timestamp)；**须与 `updateAtEnd` 成对使用** |
| updateAtEnd | INTEGER | 否 | End time for querying order update / status change, in seconds (timestamp)，**闭区间**；**须与 `updateAtStart` 成对使用** |
| parentConfirmTimeStart | INTEGER | 否 | 父订单确认开始时间（秒级时间戳）；**须与 `parentConfirmTimeEnd` 成对使用** |
| parentConfirmTimeEnd | INTEGER | 否 | 父订单确认结束时间（秒级时间戳）；**须与 `parentConfirmTimeStart` 成对使用** |
| regionId | LONG | 否 | Region ID（区域 ID），例如 USA - **211** |
| fulfillmentTypeList | STRING[] | 否 | 订单履约类型列表，见下表 |
| parentOrderLabel | STRING[] | 否 | PO 订单状态标签筛选，见下表 |
| packageAbnormalTypeList | STRING[] | 否 | 发货后物流异常类型筛选，见下表 |
| sortby | STRING | 否 | Sort by（排序字段），**默认按订单创建时间**；输出为**倒序** |
| hasPreSaleOrder | BOOLEAN | 否 | Whether the parent order contains presale orders for inventory in transit（父订单是否含在途预售子单） |
| hasQualificationRequiredOrder | BOOLEAN | 否 | Whether the parent order contains orders that require qualification upload（是否含需上传资质子单） |
| skuId | LONG | 否 | SKU ID |

#### `parentOrderStatus`（入参筛选）

| 值 | 说明 |
|----|------|
| `0` | All（全部） |
| `1` | PENDING（待处理） |
| `2` | UN_SHIPPING（待发货） |
| `3` | CANCELED（已取消） |
| `4` | SHIPPED（已发货） |
| `5` | RECEIPTED（已签收） |
| `41` | Partially shipped（部分发货，仅 local mall） |
| `51` | Partially received（部分签收，仅 local mall） |

#### `fulfillmentTypeList[]`

| 值 | 说明 |
|----|------|
| `fulfillBySeller` | fulfill by seller（卖家履约） |
| `fulfillByCooperativeWarehouse` | fulfill by Cooperative Warehouse（合作仓履约） |

#### `parentOrderLabel[]`（筛选）

| 值 | 说明 |
|----|------|
| `soon_to_be_overdue` | 即将逾期 |
| `past_due` | 已逾期 |
| `pending_buyer_cancellation` | 买家待取消 |
| `pending_buyer_address_change` | 买家待改地址 |
| `pending_risk_control_alert` | 风控预警待处理 |
| `signature_required_on_delivery` | 签收需签名 |

#### `packageAbnormalTypeList[]`（筛选）

| 值 | 说明 |
|----|------|
| `WRONG_SHIPPING_ADDRESS` | 收货地址错误 |
| `SUSPECTED_ERROR_PROVIDER` | 疑似承运商异常 |
| `NO_TRACK` | 无轨迹 |
| `TRACK_TOO_EARLY` | 轨迹过早 |
| `OVERTIME_COLLECTION` | 揽收超时 |
| `TRACK_COLLECT_FAIL` | 揽收失败 |

#### `sortby`

| 值 | 说明 |
|----|------|
| `createTime` | 按创建时间排序（**默认**） |
| `updateTime` | 按更新时间排序 |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pageNumber": 1,
    "pageSize": 20,
    "parentOrderStatus": 2
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "parentOrderSnList": ["PO-123456789"],
    "createAfter": 1700000000,
    "createBefore": 1700086400,
    "sortby": "updateTime"
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
    ├── pageItems[]
    │   ├── parentOrderMap
    │   │   ├── parentOrderSn
    │   │   ├── parentOrderStatus
    │   │   ├── parentOrderTime
    │   │   ├── expectShipLatestTime
    │   │   ├── parentOrderPendingFinishTime
    │   │   ├── latestDeliveryTime
    │   │   ├── parentShippingTime
    │   │   ├── siteId
    │   │   ├── regionId
    │   │   ├── parentOrderLabel[]
    │   │   │   ├── name
    │   │   │   └── value
    │   │   ├── fulfillmentWarning[]
    │   │   ├── hasShippingFee
    │   │   ├── updateTime
    │   │   ├── orderPaymentType
    │   │   ├── batchOrderNumberList[]
    │   │   ├── shippingMethod
    │   │   ├── isShipmentConsolidatedByMainMall
    │   │   └── parentConfirmTime
    │   └── orderList[]
    │       ├── orderSn
    │       ├── quantity
    │       ├── canceledQuantityBeforeShipment
    │       ├── originalOrderQuantity
    │       ├── goodsId
    │       ├── skuId
    │       ├── spec
    │       ├── originalSpecName
    │       ├── thumbUrl
    │       ├── goodsName
    │       ├── originalGoodsName
    │       ├── orderStatus
    │       ├── productList[]
    │       │   ├── productId
    │       │   ├── productSkuId
    │       │   ├── soldFactor
    │       │   └── extCode
    │       ├── packageAbnormalTypeList[]
    │       ├── orderLabel[]
    │       │   ├── name
    │       │   └── value
    │       ├── fulfillmentWarning[]
    │       ├── fulfillmentType
    │       ├── inventoryDeductionWarehouseId
    │       ├── inventoryDeductionWarehouseName
    │       ├── orderPaymentType
    │       ├── isCancelledDuringPending
    │       ├── earliestTimeBuyShippingLabel
    │       ├── earliestTimeGetShippingDocument
    │       ├── orderShippingTime
    │       ├── isShipmentConsolidatedByMainMall
    │       ├── orderCreateTime
    │       └── qualificationUploadEndTime
    └── totalItemNum
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | 业务结果 |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| pageItems | OBJECT[] | Page items（分页订单条目） |
| totalItemNum | INTEGER | Total number of matching records（匹配记录总数） |

### `result.pageItems[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| parentOrderMap | OBJECT | Parent order information（父订单信息） |
| orderList | OBJECT[] | Order information（子订单列表） |

### `parentOrderMap`

| 参数 | 类型 | 说明 |
|------|------|------|
| parentOrderSn | STRING | Parent order number（父订单号） |
| parentOrderStatus | INTEGER | Status of the parent order，见下表（**出参枚举**） |
| parentOrderTime | INTEGER | Time when the parent order was placed（下单时间，秒） |
| expectShipLatestTime | INTEGER | Latest shipment time（最晚发货时间，秒） |
| parentOrderPendingFinishTime | INTEGER | Time when the parent order finish pending（待处理完成时间，秒） |
| latestDeliveryTime | INTEGER | Latest delivery time（最晚送达时间，秒） |
| parentShippingTime | INTEGER | Time when the parent order was shipped（父订单发货时间，秒） |
| siteId | LONG | Site ID |
| regionId | LONG | Region ID，例如 USA - **211** |
| parentOrderLabel | OBJECT[] | List of PO order status labels（父订单标签列表） |
| fulfillmentWarning | STRING[] | Fulfillment Prompt（履约提示），见下表 |
| hasShippingFee | BOOLEAN | 用户实付运费是否为零：`true` 为零，`false` 非零（**仅 local mall**） |
| updateTime | LONG | Order update time, in seconds（订单更新时间，秒） |
| orderPaymentType | STRING | Order payment type：`COD`、`PPD` |
| batchOrderNumberList | STRING[] | 批次单号列表；**仅合作仓履约**有值，否则为空 |
| shippingMethod | INTEGER | delivery channel type：`1` Standard Shipping，`2` Store Delivery，`3` Customer Pickup |
| isShipmentConsolidatedByMainMall | BOOLEAN | 为 `true` 表示主站已合并发货，需在主站侧确认发货/面单 |
| parentConfirmTime | INTEGER | Confirmation time of parent order, in seconds (timestamp) |

#### `parentOrderStatus`（出参）

| 值 | 说明 |
|----|------|
| `1` | PENDING |
| `2` | UN_SHIPPING |
| `3` | CANCELED |
| `4` | SHIPPED |
| `41` | PARTIALLY_SHIPPED |
| `5` | DELIVERED |
| `51` | PARTIALLY_DELIVERED |

#### `parentOrderMap.parentOrderLabel[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| name | STRING | Label name（标签名） |
| value | INTEGER | Whether the label exists：`0` 无标签，`1` 有标签 |

#### `parentOrderMap.fulfillmentWarning[]`（父订单）

| 值 | 说明 |
|----|------|
| `SUGGEST_SIGNATURE_ON_DELIVERY` | 建议购买签收服务 |
| `CONFIRMED_CHANGED_ADDRESS` | 地址已变更并确认，建议重新拉单获取最新地址 |
| `RESTRICT_FEDEX_SELF_SHIPPING` | 限制使用 FedEx 运单号确认发货 |
| `RESTRICT_USPS_SELF_SHIPPING` | 限制使用 USPS 运单号确认发货 |
| `RESTRICT_SELF_SHIPPING` | 限制使用运单号确认发货 |
| `BLOCK_LOGISTICS_PROVIDERS_{Name1,Name2,...}` | 买家屏蔽部分物流商（名称在响应中展开） |
| `REQUIRES_CUSTOMER_PICKUP` | 仅支持买家自提履约 |

### `orderList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| orderSn | STRING | Order number (sub-order number)（子订单号） |
| quantity | INTEGER | 卖家需履约数量：`quantity = originalOrderQuantity - canceledQuantityBeforeShipment` |
| canceledQuantityBeforeShipment | INTEGER | 发货前取消数量 |
| originalOrderQuantity | INTEGER | 原始下单数量 |
| goodsId | LONG | Goods ID |
| skuId | LONG | Sku id；**仅 LOCAL 卖家有效，非 SEMI** |
| spec | STRING | Product specification description for customer（买家可见规格描述） |
| originalSpecName | STRING | Product specification for seller；**确认时间在近 6 个月内**的订单建议填写 |
| thumbUrl | STRING | Thumbnail image URL |
| goodsName | STRING | Product name for customer |
| originalGoodsName | STRING | Product name for seller；**确认时间在近 6 个月内**的订单建议填写 |
| orderStatus | INTEGER | Status of the order：`1` PENDING；`2` UN_SHIPPING；`3` CANCELED；`4` SHIPPED；`41` PARTIALLY_SHIPPED；`5` DELIVERED；`51` PARTIALLY_DELIVERED |
| productList | OBJECT[] | Product SKU info；**仅 SEMI 卖家有效，非 LOCAL** |
| packageAbnormalTypeList | STRING[] | 发货后物流异常类型，见下表（含 `SIGNED_BUT_UNRECEIVED_TASK`） |
| orderLabel | OBJECT[] | The label of order（子订单标签） |
| fulfillmentWarning | STRING[] | Fulfillment Prompt（子订单履约提示），见下表 |
| fulfillmentType | STRING | `fulfillBySeller` / `fulfillByCooperativeWarehouse` |
| inventoryDeductionWarehouseId | STRING | The id of inventory deduction warehouse |
| inventoryDeductionWarehouseName | STRING | The name of inventory deduction warehouse |
| orderPaymentType | STRING | `COD`、`PPD` |
| isCancelledDuringPending | BOOLEAN | Whether the order is completely cancelled during the pending period |
| earliestTimeBuyShippingLabel | INTEGER | Order can only buy shipping label after this time |
| earliestTimeGetShippingDocument | INTEGER | Order can only get shipping document after this time |
| orderShippingTime | INTEGER | Time when the order was shipped；含未发货/延迟包裹时可能为 `null` |
| isShipmentConsolidatedByMainMall | BOOLEAN | 主站合并发货标记，同 `parentOrderMap` |
| orderCreateTime | INTEGER | The time when the order was created |
| qualificationUploadEndTime | LONG | Deadline for uploading order qualification documents |

#### `productList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| productId | LONG | productId |
| productSkuId | LONG | SKU ID of the product variation |
| soldFactor | LONG | 商品数量与件数换算因子 |
| extCode | STRING | Item code |

#### `orderList[].packageAbnormalTypeList[]`（出参，比入参多一项）

| 值 | 说明 |
|----|------|
| `WRONG_SHIPPING_ADDRESS` | 收货地址错误 |
| `SUSPECTED_ERROR_PROVIDER` | 疑似承运商异常 |
| `NO_TRACK` | 无轨迹 |
| `TRACK_TOO_EARLY` | 轨迹过早 |
| `OVERTIME_COLLECTION` | 揽收超时 |
| `TRACK_COLLECT_FAIL` | 揽收失败 |
| `SIGNED_BUT_UNRECEIVED_TASK` | 已签收但未收货任务 |

#### `orderList[].orderLabel[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| name | STRING | Label name，如 `customized_products`、`pre_sale_order`、`made_to_order` 等 |
| value | INTEGER | `0` 无标签，`1` 有标签；BBC 订单需结合 `is_US_to_CA_BBC` 判断 |

#### `orderList[].fulfillmentWarning[]`

| 值 | 说明 |
|----|------|
| `SAVE_SN_INFORMATION_FOR_RETURN` | 建议保存 SN 便于退货鉴真 |
| `REQUIRES_AUTHENTICATION_REPORT_SUBMISSION` | 须在卖家中心提交鉴定报告，超时自动取消并可能处罚 |
| `REQUIRES_AGE_VERIFICATION` | 建议购买签收人年龄验证服务 |
| `SPECIFIC_LOGISTICS_REQUIRED` | 须选择指定物流履约 |
| `REQUIRES_CUSTOMER_PICKUP` | 仅支持买家自提 |

---

## 示例

```bash
python scripts/eu_order_list_v2_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pageNumber": 1,
    "pageSize": 20,
    "parentOrderStatus": 2
  }
}'
```
