# 确认发货 V2 — `bg.logistics.shipment.v2.confirm`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_self_fulfilled_logistics_shipment_v2_confirm.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=38e79b35d2cb463d85619c1c786dd303（`sub_menu_code` 以 Partner 后台该接口页为准） |
| **网关** | `POST /temu/proxy`，`type`=`bg.logistics.shipment.v2.confirm`，业务载荷放在 Body 的 `params` |

**Description:** The `bg.logistics.shipment.v2.confirm` interface is designed to synchronize and return order fulfillment information through this interface. Switch the order status from **pending shipment** to **shipped**（同步并回传订单履约/发货信息，将订单状态从待发货切换为已发货）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。  
> **前置依赖：** `carrierId` 与 `bg.logistics.companies.get` 返回的 **`logisticsServiceProviderId`** 相同；`selfShippingWarehouseId` 来自 **`linkfox-temu-fulfillment-us`** 的 **`bg.logistics.warehouse.list.get`**（`warehouseId`）。订单号来自 **`linkfox-temu-order-us`**（如 `bg.order.detail.v2.get`）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── sendType                    ← 必填
    └── sendRequestList[]           ← 必填（Shipment package details）
        ├── carrierId               ← 必填
        ├── trackingNumber          ← 必填
        ├── selfShippingWarehouseId ← 必填
        ├── orderSendInfoList[]     ← 必填（本包裹内商品行）
        │   ├── parentOrderSn       ← 必填
        │   ├── orderSn             ← 必填
        │   ├── goodsId             ← 选填
        │   ├── skuId               ← 选填
        │   └── quantity            ← 必填
        ├── confirmAcceptance[]     ← 选填
        └── subSendRequests[]       ← 选填（子包裹/子运单）
            ├── carrierId           ← 必填（当使用 subSendRequests 时）
            ├── trackingNumber      ← 必填
            └── selfShippingWarehouseId ← 必填
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sendType | INTEGER | **是** | SendType（发货方式），见下表 |
| sendRequestList | OBJECT[] | **是** | Shipment package details（发货包裹明细列表）；每个元素描述一个包裹及其运单、仓库、商品行 |

#### `sendType`

| 值 | 说明 |
|----|------|
| `0` | 同一 **父订单** 内全部商品，**一个包裹、一个运单号** 发货 |
| `1` | 同一 **父订单** 内**部分商品**分多个包裹、多个运单号发货；**该父订单下所有待发商品须在一次 API 调用中全部提交**（不可拆成多次 confirm 漏发） |
| `2` | **多个父订单** 的商品合并为 **一个包裹、一个运单号** 发货 |

#### `sendRequestList[]` 元素字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| carrierId | LONG | **是** | Carrier ID（承运商 ID），与 **`bg.logistics.companies.get`** 返回的 **`logisticsServiceProviderId`** 相同 |
| trackingNumber | STRING | **是** | Tracking Number（物流运单号 / 跟踪号） |
| selfShippingWarehouseId | STRING | **是** | The shipment warehouse ID（自发货仓库 ID），通过 **`linkfox-temu-fulfillment-us`** 的 **`bg.logistics.warehouse.list.get`** 返回的 **`warehouseId`** 获取 |
| orderSendInfoList | OBJECT[] | **是** | Product List in this package（本包裹内要发货的商品行列表） |
| confirmAcceptance | STRING[] | 否 | Confirmation matters for this shipment（本批发货需确认的异常/预警事项），见下表 |
| subSendRequests | OBJECT[] | 否 | Sub Send Requests（子发货请求；用于一单多包裹等场景下的子运单明细） |

##### `orderSendInfoList[]` 元素字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | **是** | Parent Order Number（父订单号） |
| orderSn | STRING | **是** | Order Number（子订单号 / 订单号） |
| goodsId | LONG | 否 | Goods ID（商品 ID） |
| skuId | LONG | 否 | SKU ID |
| quantity | INTEGER | **是** | Quantity of the product（本行发货数量） |

##### `confirmAcceptance[]` 枚举值

| 值 | 说明 |
|----|------|
| `DENY_CANCELLATION` | Reject the cancellation request for this order（拒绝该订单的取消申请后继续发货） |
| `DENY_ADDRESS_CHANGE` | Reject the address change request for this order（拒绝该订单的改地址申请后继续发货） |
| `DENY_PARENT_RISK_WARNING` | Reject the risk warning for this order（拒绝/确认父订单风险预警后继续发货） |

> 仅当订单存在对应待处理事项且商家选择「拒绝申请并继续发货」等场景时传入；无此类事项可省略。

##### `subSendRequests[]` 元素字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| carrierId | LONG | **是** | Logistics Company ID（子包裹承运商 ID） |
| trackingNumber | STRING | **是** | Waybill Number（子包裹运单号） |
| selfShippingWarehouseId | STRING | **是** | Self-Delivery Warehouse ID（子包裹自发货仓库 ID） |

> 使用 **`subSendRequests`** 时，父级 **`sendRequestList`** 元素仍须填写 **`orderSendInfoList`** 等；子项用于补充额外运单/仓库组合，具体与 **`sendType=1`** 等多包裹场景配合，以 Partner 文档与订单详情约束为准。

### 网关 `params` 写法（`sendType=0` 单包裹示例）

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "sendType": 0,
    "sendRequestList": [
      {
        "carrierId": 123456789,
        "trackingNumber": "1Z999AA10123456784",
        "selfShippingWarehouseId": "WH-001",
        "orderSendInfoList": [
          {
            "parentOrderSn": "PO-xxx",
            "orderSn": "O-xxx",
            "goodsId": 987654321,
            "skuId": 111222333,
            "quantity": 1
          }
        ]
      }
    ]
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "sendType": 1,
    "sendRequestList": [
      {
        "carrierId": 123456789,
        "trackingNumber": "TRACK-A",
        "selfShippingWarehouseId": "WH-001",
        "orderSendInfoList": [
          {
            "parentOrderSn": "PO-xxx",
            "orderSn": "O-xxx-a",
            "quantity": 1
          }
        ],
        "confirmAcceptance": ["DENY_CANCELLATION"],
        "subSendRequests": [
          {
            "carrierId": 123456789,
            "trackingNumber": "TRACK-B",
            "selfShippingWarehouseId": "WH-001"
          }
        ]
      }
    ]
  }
}
```

> 官方表将顶层 **`request`** 标为选填（False），但 **`sendType`**、**`sendRequestList`** 及其子字段多为必填；实际调用时**应传入完整 `request` 对象**。

---

## Response（Temu `body` 解析后）

```text
response
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)
    ├── assistantAgreementText
    └── warningMessage[]
```

### 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | result（业务结果对象） |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| assistantAgreementText | STRING | Enables intelligent trajectory assistant to detect and correct potential mistakes in carrier entries（智能轨迹助手相关提示文案，用于检测并纠正承运商录入错误） |
| warningMessage | STRING[] | Provides relevant prompts related to the current shipping request（与本次发货请求相关的提示/警告信息列表） |

> 调用成功时先判断 **`response.success === true`**，再查看 **`result.warningMessage`** 是否有需向用户展示的警告；发货是否最终在平台侧生效，建议再调 **`linkfox-temu-order-us`** 的 `bg.order.detail.v2.get` 核对订单状态。

---

## 典型流程

```text
1. linkfox-temu-order-us          → 待发货订单 / 订单详情（parentOrderSn、orderSn、数量）
2. bg.logistics.companies.get    → carrierId（= logisticsServiceProviderId）
3. linkfox-temu-fulfillment-us → bg.logistics.warehouse.list.get → warehouseId / selfShippingWarehouseId
4. bg.logistics.shipment.v2.confirm（本接口）→ 提交运单并确认发货
5. linkfox-temu-order-us          → 刷新订单状态（parentOrderStatus 等）
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/us_self_fulfilled_logistics_shipment_v2_confirm.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "sendType": 0,
    "sendRequestList": [
      {
        "carrierId": 123456789,
        "trackingNumber": "9400111899223344556677",
        "selfShippingWarehouseId": "YOUR_WAREHOUSE_ID",
        "orderSendInfoList": [
          {
            "parentOrderSn": "PO-20260101001",
            "orderSn": "O-20260101001-1",
            "skuId": 58224724203874,
            "quantity": 2
          }
        ]
      }
    ]
  }
}'
```

```bash
python scripts/temu_us_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "bg.logistics.shipment.v2.confirm",
  "params": {
    "request": {
      "sendType": 0,
      "sendRequestList": []
    }
  }
}'
```
