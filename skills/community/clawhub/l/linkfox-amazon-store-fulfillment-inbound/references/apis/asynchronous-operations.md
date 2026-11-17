# Asynchronous Operations（1 operation）

| Operation / 脚本 | HTTP / 成功 | Amazon path | 必要输入与语义 |
|---|---|---|---|
| `getInboundOperationStatus`<br>`get_inbound_operation_status.py` | GET / 200 | `/inbound/fba/2024-03-20/operations/{operationId}` | 必填 `operationId`；返回 `operation`、`operationId`、`operationStatus`、`operationProblems` |

`operationStatus` 只有：

| 状态 | 处理 |
|---|---|
| `IN_PROGRESS` | 记录 operation ID，稍后由调用方再次查询；不进入下游步骤 |
| `SUCCESS` | 只表示该一个 operation 完成；可通过下一个 list/get operation 读取结果 |
| `FAILED` | 展示 `operationProblems`，停止下游写操作；修正输入或工作流后由用户决定是否重新发起 |

## 异步发起 operation 清单（19）

- Plans：`createInboundPlan`、`cancelInboundPlan`
- Packing：`generatePackingOptions`、`confirmPackingOption`、`setPackingInformation`
- Placement：`generatePlacementOptions`、`confirmPlacementOption`
- Content updates：`generateShipmentContentUpdatePreviews`、`confirmShipmentContentUpdatePreview`
- Delivery windows：`generateDeliveryWindowOptions`、`confirmDeliveryWindowOptions`
- Self-ship：`cancelSelfShipAppointment`、`generateSelfShipAppointmentSlots`
- Shipment updates：`updateShipmentSourceAddress`、`updateShipmentTrackingDetails`
- Transportation：`generateTransportationOptions`、`confirmTransportationOptions`
- Item data：`updateItemComplianceDetails`、`setPrepDetails`

其中 `generateSelfShipAppointmentSlots` 返回 HTTP 201，其余 18 个返回 HTTP 202。两种 HTTP 状态都必须继续查 `operationStatus`。

本 Skill 不隐式轮询。只有用户或上层工作流显式请求查状态时，才再运行本脚本。
