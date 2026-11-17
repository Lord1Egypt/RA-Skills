# Delivery Windows 与 Documents（4 operations）

路径版本：`/inbound/fba/2024-03-20`。

| Operation / 脚本 | HTTP / 成功 | Amazon path | 必要输入与语义 |
|---|---|---|---|
| `getDeliveryChallanDocument`<br>`get_delivery_challan_document.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/deliveryChallanDocument` | 必填 plan/shipment ID；返回 `documentDownload`；仅 India PCP shipment |
| `listDeliveryWindowOptions`<br>`list_delivery_window_options.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/deliveryWindowOptions` | 必填 plan/shipment ID；可选 `pageSize` 1–100、`paginationToken`；返回 window IDs、dates、availability/validity |
| `generateDeliveryWindowOptions`<br>`generate_delivery_window_options.py` | POST / 202<br>异步 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/deliveryWindowOptions` | 必填 plan/shipment ID；无 body；返回 `operationId` |
| `confirmDeliveryWindowOptions`<br>`confirm_delivery_window_options.py` | POST / 202<br>异步・确认 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/deliveryWindowOptions/{deliveryWindowOptionId}/confirmation` | 必填 plan/shipment/window ID；无 body；返回 `operationId` |

## Delivery window 规则

- 自有承运人选项通常需要为 placement 中的每个 shipment 生成和确认 delivery window，以 transportation option `preconditions` 为准。
- 确认前展示 `startDate`、`endDate`、`availabilityType` 和 `validUntil`。
- 过期后重新 generate/list，不确认旧 ID。
- `confirmDeliveryWindowOptions` 是高影响操作，应取得用户明确确认。

## Challan 文档

`getDeliveryChallanDocument` 返回的 URI 可能有过期时间。如用户要下载，应使用当次 Amazon 响应的 HTTPS URI 立即下载；不接受用户传入的任意 URL。
