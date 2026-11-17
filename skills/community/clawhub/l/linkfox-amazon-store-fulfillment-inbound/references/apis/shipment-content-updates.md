# Shipment Content Updates（4 operations）

路径版本：`/inbound/fba/2024-03-20`。

| Operation / 脚本 | HTTP / 成功 | Amazon path | 必要输入与语义 |
|---|---|---|---|
| `listShipmentContentUpdatePreviews`<br>`list_shipment_content_update_previews.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/contentUpdatePreviews` | 必填 plan/shipment ID；可选 `pageSize` 1–20、`paginationToken` |
| `generateShipmentContentUpdatePreviews`<br>`generate_shipment_content_update_previews.py` | POST / 202<br>异步 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/contentUpdatePreviews` | body 必填 `boxes`、`items`；返回 `operationId` |
| `getShipmentContentUpdatePreview`<br>`get_shipment_content_update_preview.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/contentUpdatePreviews/{contentUpdatePreviewId}` | 必填 plan/shipment/preview ID；返回 `requestedUpdates`、`transportationOption`、`expiration` |
| `confirmShipmentContentUpdatePreview`<br>`confirm_shipment_content_update_preview.py` | POST / 202<br>异步・确认 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/contentUpdatePreviews/{contentUpdatePreviewId}/confirmation` | 必填 plan/shipment/preview ID；无 body；返回 `operationId` |

这一组操作用于 transportation 已确认后的 shipment 内容调整。不要直接确认 list 中的第一项；先 get preview，向用户展示内容变更、新 transportation option/费用和 `expiration`。

只能在同一 plan + shipment 中使用 preview ID。已过期或重新生成后的旧 preview 不得确认。
