# 更新发货/重试购标 — `bg.logistics.shipment.update`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_buy_shipping_logistics_shipment_update.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.logistics.shipment.update`，业务载荷放在 Body 的 `params` |

**Description:** The `bg.logistics.shipment.update` interface is for sellers to create shipment logistics orders later, and to re-order online if the order fails.（卖家延后创建物流单，或在购标/下单失败后对包裹重新在线下单。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。  
> **典型场景：**  
> 1. 仅更新 **`shipLaterLimitTime`**（须由 **`bg.logistics.shipment.create`** 且 **`shipLater=true`** 创建）。  
> 2. **`retrySendPackageRequestList`**：对 **失败状态** 的包裹（`packageSn`）调整仓库/尺寸重量/渠道后重试购标。  
> **前置：** `packageSn` 来自 **`bg.logistics.shipment.result.get`**；渠道参数来自 **`bg.logistics.shippingservices.get`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── retrySendPackageRequestList[]     ← 选填；失败包裹重试购标
    │   ├── packageSn                     ← 失败包裹号
    │   ├── splitSubPackage
    │   ├── warehouseId
    │   ├── weight / weightUnit / extendWeight / extendWeightUnit
    │   ├── length / width / height / dimensionUnit
    │   ├── shipCompanyId / channelId / shipLogisticsType / signServiceId
    │   ├── pickupStartTime / pickupEndTime
    │   ├── confirmAcceptance[]
    │   ├── uspsMailingDateOffset
    │   ├── autoConfirmAfterPickup
    │   ├── cooperativeWarehouseShipment
    │   ├── interlineShipCompanyList[]
    │   ├── orderSendInfoList[]
    │   └── retrySendSubRequestList[]     ← 子包裹重试（拆包场景）
    └── shipLaterLimitTime                ← 选填；延后发货截止时间
```

### `request` 内字段

> Partner **Request** 表将 **`request`**、**`retrySendPackageRequestList`**、**`shipLaterLimitTime`** 均标为选填（False）；下列说明列内容来自 Partner 导出页 **Required** 列（该页将长说明写在 Required 列而非 Description 列）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| retrySendPackageRequestList | OBJECT[] | 否 | retry Package List Information（失败包裹重试列表；每项对应一个待重试的 **`packageSn`** 及新的物流/尺寸参数） |
| shipLaterLimitTime | STRING | 否 | **Usage Rules:** shipLaterLimitTime can be updated only if the order was created with **shipLater=true** via **`bg.logistics.shipment.create`**. **Available Options by Order Label:** For orders **without** the **`Y2_advance_sale`** label, available options are: **24, 48, 72, 96, 120** hours. For orders **with** the **`Y2_advance_sale`** label, available options are: **144, 168, 192, 216, 240, 264, 288, 312, 336, 360** hours.（仅 **`shipLater=true`** 创建的订单可更新；无效值见错误码 **`120015532`**、**`120018078`**） |

#### `shipLaterLimitTime` 可选值（Partner 原文）

| 订单标签 | 可选小时（字符串） |
|----------|-------------------|
| 无 **`Y2_advance_sale`** 标签 | `24`、`48`、`72`、`96`、`120` |
| 有 **`Y2_advance_sale`** 标签 | `144`、`168`、`192`、`216`、`240`、`264`、`288`、`312`、`336`、`360` |

> 与 **`bg.logistics.shipment.create`** 入参 **`shipLaterLimitTime`** 规则一致；无效值见错误码 `120015532`。

#### `retrySendPackageRequestList[]` 元素字段

> Partner Request 表中 `retrySendPackageRequestList` 子行在导出 HTML 中为折叠状态；下列字段与类型来自 **Request Example**，说明结合 Partner 错误码、**`bg.logistics.shipment.create`** 的 **`sendRequestList[]`** 同名字段及 Buy-Shipping 流程整理。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| packageSn | STRING | **是**（重试时） | Package SN（包裹号；须为 **购标失败** 状态的包裹，见错误码 `120018002`、`120018027`） |
| splitSubPackage | BOOLEAN | 否 | 是否拆分子包裹发货。为 **true** 时 **`orderSendInfoList[].quantity`** 须为 **1**（`120011045`）；跨国拆包等限制见错误码 `120012029`、`120018084` |
| warehouseId | STRING | **是**（重试时） | Warehouse ID（发货仓库；来自 **`bg.logistics.warehouse.list.get`**，错误码 `120011006`） |
| weight | STRING | **是**（重试时） | 包裹重量。美国本地订单填**整数**（lb），小数用 **`extendWeight`**（oz）；非美国本地默认两位小数（`120015521`） |
| weightUnit | STRING | **是**（重试时） | 重量单位：美国 **`lb`**，其他 **`kg`** |
| extendWeight | STRING | 否 | 扩展重量（美国本地 oz 部分） |
| extendWeightUnit | STRING | 否 | 扩展重量单位：美国本地 **`oz`** |
| length | STRING | **是**（重试时） | 长度（两位小数） |
| width | STRING | **是**（重试时） | 宽度（两位小数） |
| height | STRING | **是**（重试时） | 高度（两位小数） |
| dimensionUnit | STRING | **是**（重试时） | 尺寸单位：美国 **`in`**，其他 **`cm`** |
| shipCompanyId | INTEGER | 否 | Shipping company ID（物流公司 ID；与 **`channelId`** / **`shipLogisticsType`** 配合，二选一方式见 `120015032`） |
| channelId | INTEGER | 否 | Channel ID（物流渠道 ID；来自 **`bg.logistics.shippingservices.get`** 的 **`onlineChannelDtoList`**） |
| shipLogisticsType | STRING | 否 | Ship logistics type（物流类型标识；与 **`channelId`** 二选一，见 `120015032`） |
| signServiceId | INTEGER | 否 | Signature service ID（签收服务 ID；订单带 **`signature_required_on_delivery`** 时须从推荐渠道选取，见 `120015545`） |
| pickupStartTime | INTEGER | 否 | Pickup window start time（预约揽收开始时间；须满足 `120019019` 等时间窗规则） |
| pickupEndTime | INTEGER | 否 | Pickup window end time（预约揽收结束时间；**pickupStartTime** 须早于 **pickupEndTime**） |
| confirmAcceptance | STRING[] | 否 | Confirmation matters for this shipment（发货前需确认的异常事项，如拒绝取消/改址/风控预警），枚举同 **`linkfox-temu-fulfillment-global`** 的 `DENY_CANCELLATION`、`DENY_ADDRESS_CHANGE`、`DENY_PARENT_RISK_WARNING` |
| uspsMailingDateOffset | INTEGER | 否 | USPS mailing date offset（USPS 邮寄日偏移；部分渠道禁止为 **0**，见 `120018086`） |
| autoConfirmAfterPickup | BOOLEAN | 否 | Auto confirm shipment after pickup（揽收后是否自动确认发货） |
| cooperativeWarehouseShipment | BOOLEAN | 否 | 是否合作仓发货（合作仓模式限制见 `120018074`、`120018079`、`120011030` 等） |
| interlineShipCompanyList | OBJECT[] | 否 | Interline / multi-leg shipping company list（联运各段承运信息） |
| orderSendInfoList | OBJECT[] | 否 | Product lines in this package（本包裹商品行；重试时若调整订单行须传） |
| retrySendSubRequestList | OBJECT[] | 否 | Retry sub-package list（子包裹重试参数；结构与子包裹物流字段类似 **`sendSubRequestList`**，见 `120011043`） |

##### `retrySendPackageRequestList[].orderSendInfoList[]` 元素字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | **是** | Parent Order Number（父订单号） |
| orderSn | STRING | **是** | Order Number（子订单号） |
| quantity | INTEGER | **是** | Quantity（本行数量；**splitSubPackage=true** 时须为 **1**） |
| goodsId | LONG | 否 | Goods ID（商品 ID） |
| skuId | LONG | 否 | SKU ID |

##### `retrySendPackageRequestList[].interlineShipCompanyList[]` 元素字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| shipLogisticsType | STRING | **是** | Logistics type for this leg（该段物流类型） |
| shipStageType | STRING | **是** | Shipping stage type（运输段类型，如首程/末程） |
| shipCompanyId | INTEGER | **是** | Shipping company ID（该段物流公司 ID） |
| channelId | INTEGER | **是** | Channel ID（该段渠道 ID） |

##### `retrySendPackageRequestList[].retrySendSubRequestList[]` 元素字段

> 子包裹重试对象**不含** `orderSendInfoList`（见 Request Example）；物流/渠道/尺寸字段与父级包裹项类似。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| packageSn | STRING | **是** | Sub-package SN（子包裹号） |
| warehouseId | STRING | **是** | Warehouse ID |
| weight | STRING | **是** | 重量 |
| weightUnit | STRING | **是** | 重量单位 |
| extendWeight | STRING | 否 | 扩展重量 |
| extendWeightUnit | STRING | 否 | 扩展重量单位 |
| length | STRING | **是** | 长度 |
| width | STRING | **是** | 宽度 |
| height | STRING | **是** | 高度 |
| dimensionUnit | STRING | **是** | 尺寸单位 |
| shipCompanyId | INTEGER | 否 | 物流公司 ID |
| channelId | INTEGER | 否 | 渠道 ID |
| shipLogisticsType | STRING | 否 | 物流类型 |
| signServiceId | INTEGER | 否 | 签收服务 ID |
| pickupStartTime | INTEGER | 否 | 揽收开始时间 |
| pickupEndTime | INTEGER | 否 | 揽收结束时间 |
| confirmAcceptance | STRING[] | 否 | 发货确认事项 |
| uspsMailingDateOffset | INTEGER | 否 | USPS 邮寄日偏移 |
| interlineShipCompanyList | OBJECT[] | 否 | 联运段列表（结构同上） |

> **调整范围（错误码 `120018004`）：** 一般仅允许修改 **`warehouseId`**、重量尺寸、物流公司/渠道等；不可随意变更业务不允许的字段。  
> **重试限制：** 同一包裹不支持重复重试两次（`120018017`）、部分包裹类型不支持重试（`120018013`）。包裹须处于 **失败** 状态（`120018002`）。

### 网关 `params` 写法

**仅更新延后发货时限：**

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "shipLaterLimitTime": "48"
  }
}
```

**失败包裹重试购标：**

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "retrySendPackageRequestList": [
      {
        "packageSn": "PKG-FAILED-001",
        "warehouseId": "WH-001",
        "weight": "2",
        "weightUnit": "lb",
        "extendWeight": "8",
        "extendWeightUnit": "oz",
        "length": "12.00",
        "width": "8.00",
        "height": "4.00",
        "dimensionUnit": "in",
        "channelId": 12345,
        "shipLogisticsType": "GROUND",
        "signServiceId": 0,
        "orderSendInfoList": [
          {
            "parentOrderSn": "PO-20260101001",
            "orderSn": "O-20260101001-1",
            "quantity": 1,
            "goodsId": 987654321,
            "skuId": 111222333
          }
        ]
      }
    ]
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
└── result (BOOLEAN)    ← 业务是否更新/重试受理成功
```

### 顶层字段

> Partner **Response** 表对上述字段 **Description** 列为空；下列说明结合 **Response Example**（`result: true/false`）与通用网关语义整理。

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | BOOLEAN | result（业务结果；更新/重试是否受理成功；Partner Response 表类型为 **BOOLEAN**，Response Example 为 `true`/`false`） |

> 调用成功时先判断 **`response.success === true`**，再读 **`result`**。异步购标结果仍须用 **`bg.logistics.shipment.result.get`** 查询包裹状态。

---

## 常见业务错误码（Partner Error Code）

| 错误码 | 错误信息（原文） | 处理建议 |
|--------|------------------|----------|
| 120018078 | Cannot set shipLaterLimitTime: order was created for immediate shipment. | 仅 **`shipLater=true`** 创建的订单可改 **`shipLaterLimitTime`** |
| 120018002 | The package is not in failed state, please check the package status. | 仅对失败包裹调用 **`retrySendPackageRequestList`** |
| 120018027 | The packageSn is invalid... | 核对 **`packageSn`** 与站点 |
| 120018017 | Does not support retrying twice | 勿对同一包裹重复重试 |
| 120018013 | Does not support this package retry | 该包裹类型不可重试 |
| 120018004 | Only allow adjustments to warehouseId, weight, dimensions, shipping company, etc. | 仅调整允许的物流参数字段 |
| 120018062 | COD orders do not allow updating shipping information. | COD 订单不可更新 |
| 120018049 | Failed to update shipping information. Please cancel the appointment for pickup first. | 先取消揽收预约 |
| 120015532 | shipLaterLimitTime is invalid... | 按订单是否 **Y2_advance_sale** 选合法小时数 |
| 120015507 | Wrong package {*} information. Try again. | 检查重量尺寸单位 |
| 120015032 | You should choose one fulfillment way and fulfill channelId or shipLogisticsType. | **`channelId`** 与 **`shipLogisticsType`** 择一传全 |
| 120011006 | The parameter warehouseId is invalid. | 使用有效 **`warehouseId`** |
| 120011043 | Missing required parameters for 'sendSubRequestList'. | 拆包子包裹时补全 **`retrySendSubRequestList`** |
| 120011045 | For splitSubPackage quantity needs to be 1. | 拆包时 **quantity=1** |
| 120011044 | Exceeded maximum allowed attached packages. Limit is 10. | 子包裹最多 10 个 |
| 120019019 | Invalid pickup time range... | 按 Partner 规则设置揽收时间段 |
| 120019009 | Invalid pickup reservation time. See pickupRules... | 参考 **`bg.logistics.shippingservices.get`** 返回的 **pickupRules** |
| 120018088 | Failed to buy-shipping on platform , reason :{*} | 查看平台返回原因后调整参数重试 |

<details>
<summary>完整错误码列表（68 条，Partner 原文）</summary>

| 错误码 | 错误信息 |
|--------|----------|
| 120015038 | Please note that the Buy Shipping service is not applicable to age-restricted product sales. |
| 120018074 | The cooperative warehouse mode does not support merging and shipping orders from multiple stores |
| 120018079 | The warehouseid has not completed the cooperative warehouse authorization |
| 120018080 | The current channel must be shipped later |
| 120018082 | This channel is not supported for shipping |
| 120018084 | Shipping from a cooperative warehouse and do not support unpacking sub packages |
| 120018085 | The channel used by {*} needs to be shipped through a cooperative warehouse |
| 120018086 | The current channel USPSMailingDateOffset prohibits the input of 0 |
| 120018088 | Failed to buy-shipping on platform , reason :{*} |
| 120011020 | Invalid request parameters |
| 120018078 | Cannot set shipLaterLimitTime: order was created for immediate shipment. |
| 120011018 | Orders with "signature_required_on_delivery" can only buy shipping label from the channel which provide signature service,please call "bg.logistics.shippingservices.get" to get the recommended channels. |
| 120015507 | Wrong package {*} information. Try again. |
| 120011017 | The input warehouse does not support the USPS Ground Advantage shipping service. It is recommended to use a warehouse where "supportsUspsGroundAdvantage" is true by calling the bg.logistics.warehouse.list.get API. |
| 120012044 | This channel requires passing the exam to gain access. |
| 120012061 | The current parent order has a pending risk control alert, It is not recommended to proceed with the performance. You can submit a cancellation request. |
| 120019009 | Invalid pickup reservation time. See pickupRules for valid options. |
| 120011015 | Incomplete warehouse details. Update in Seller Central to process shipment. |
| 120015040 | The parent order {*} can not be fulfilled by the selected logistics provider due to the customer's delivery preferences. Please change another logistics provider to fulfill again. |
| 120015545 | Orders with "signature_required_on_delivery" can only buy shipping label from the channel which provide signature service. Please call "bg.logistics.shippingservices.get" to get the recommended channel and request with the field "signServiceId". |
| 120015543 | The Order with label "signature_required_on_delivery" and other orders cannot be fulfilled at the same time. Please fulfill the order with label "signature_required_on_delivery" separately. |
| 120015037 | This logistics provider does not support this business scenario. |
| 120018063 | Your funds have been reserved, so you are temporarily unable to use the 'Buy shipping' function. |
| 120018010 | The packages {*} have been canceled. Please fulfill again by Temu non-integrated logistics or Temu integrated logistics. |
| 120018062 | COD orders do not allow updating shipping information. |
| 120011051 | COD orders do not allow adding sub-packages |
| 120012037 | Order can only buy shipping label after the "earliestTimeBuyShippingLabel". |
| 120019019 | Invalid pickup time range. Please ensure times are within the next 5 calendar days (8:00-17:00), on the same day, and can't be weekend, and pickupStartTime is before pickupEndTime |
| 120015032 | You should choose one fulfillment way and fulfill channelId or shipLogisticsType. |
| 120011030 | Cooperative warehouse order fulfillment restricted. |
| 120011089 | Purchasing shipping labels for Amazon FBA warehouses is not supported. |
| 120015531 | Only order with "Y2_advance_sale" label can be fulfilled by warehouse in "other" type. |
| 120015532 | shipLaterLimitTime is invalid, please check the valid value for orders with "Y2_advance_sale" label |
| 120015533 | The order with "Y2_advance_sale" label and the order without "Y2_advance_sale" label can't be fulfilled simultaneously. |
| 120015534 | Order with "Y2_advance_sale" label should set "shipLater=true" when you are fulfilled by Temu integrated logistics. |
| 120018049 | Failed to update shipping information. Please cancel the appointment for pickup first. |
| 120011082 | Failed to buy the shipping label. Please fill in the warehouse management type and warehouse brand in the Temu seller center first. |
| 120015518 | The order with "US-to-CA" Label and the order without "US-to-CA" Label can't be shipped together. |
| 120011043 | Missing required parameters for 'sendSubRequestList'. |
| 120011044 | Exceeded maximum allowed attached packages. Limit is 10. |
| 120011045 | For splitSubPackage quantity needs to be 1. |
| 120012029 | Warehouse and recipient in different countries splitSubPackage cannot enter "TRUE". |
| 120015520 | Call failed: Cannot convert subPackage to self-shipment. |
| 120012023 | Address change pending. Please process before shipping. |
| 120012030 | Order cancel pending. Please process before shipping. |
| 120019016 | Unexpected parameter pickupTime. |
| 120019017 | Miss required parameter pickupTime. |
| 120018017 | Does not support retrying twice |
| 120018013 | Does not support this package retry |
| 120015026 | A large items template has been used for the items in this package. Only specified logistics providers can be used for shipping. |
| 120013007 | Product sku sensitive query fail |
| 120013008 | Order lacks necessary sensitive attributes. |
| 120013009 | Order lacks necessary sensitive attributes. |
| 120018004 | Only allow adjustments to warehouseId, weight, dimensions, shipping company, etc. |
| 120011047 | Not support local mall |
| 120011048 | Usage channel does not match the confirmation scenario |
| 120012031 | The current parent order has a pending risk control alert. |
| 120018020 | The BBC order is not allowed. |
| 120015027 | A large items template has been used for the items in this package. Only special channels can be used for shipping. |
| 120018025 | Orders exist after-sales applications, please complete the processing before operation |
| 120012007 | The parentOrder or Order is invalid. Please check if the parentOrder matches the Order, the parentOrder or Order is nonexistent etc. |
| 120015521 | The parameter Weight should be integer. |
| 120011006 | The parameter warehouseId is invalid. |
| 120011072 | The request area is incorrect. Please check the request area and replace it with the correct request area. The request area for the United States is US, and the request area for other non-European countries is global. |
| 120012016 | The parentOrder or Order is invalid. Please check if the parentOrder matches the Order, the parentOrder or Order is nonexistent etc. |
| 120018027 | The packageSn is invalid. Please check the request area or if the packageSn is nonexistent etc. |
| 120015528 | O-orders of COD type exist in body, and COD type O-orders can only be shipped with Temu Label. |

</details>

---

## 典型用法

```text
1. bg.logistics.shipment.create（shipLater=true）→ 创建延后发货包裹
2. bg.logistics.shipment.update（shipLaterLimitTime）→ 调整最晚发货时限
--- 或 ---
1. bg.logistics.shipment.create / result.get     → 购标失败，取得 packageSn
2. bg.logistics.shippingservices.get             → 重新选 channelId / signServiceId
3. bg.logistics.shipment.update（retrySendPackageRequestList）→ 重试购标
4. bg.logistics.shipment.result.get              → 确认包裹状态
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/global_buy_shipping_logistics_shipment_update.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "shipLaterLimitTime": "72"
  }
}'
```

```bash
python scripts/global_buy_shipping_logistics_shipment_update.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "retrySendPackageRequestList": [
      {
        "packageSn": "PKG-FAILED-001",
        "warehouseId": "WH-001",
        "weight": "2",
        "weightUnit": "lb",
        "length": "12.00",
        "width": "8.00",
        "height": "4.00",
        "dimensionUnit": "in",
        "channelId": 12345
      }
    ]
  }
}'
```

```bash
python scripts/temu_global_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "bg.logistics.shipment.update",
  "params": {
    "request": {
      "shipLaterLimitTime": "48"
    }
  }
}'
```