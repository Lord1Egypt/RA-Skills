# Shipments（7 operations）

路径版本：`/inbound/fba/2024-03-20`。

| Operation / 脚本 | HTTP / 成功 | Amazon path | 必要输入与语义 |
|---|---|---|---|
| `getShipment`<br>`get_shipment.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}` | 必填 `inboundPlanId`、`shipmentId`；返回 placement、destination、status，以及可用时的 `shipmentConfirmationId`、`amazonReferenceId`、transport/tracking |
| `listShipmentBoxes`<br>`list_shipment_boxes.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/boxes` | 必填 plan/shipment ID；可选 `pageSize` 1–1000、`paginationToken` |
| `listShipmentItems`<br>`list_shipment_items.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/items` | 必填 plan/shipment ID；可选 `pageSize` 1–1000、`paginationToken` |
| `listShipmentPallets`<br>`list_shipment_pallets.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/pallets` | 必填 plan/shipment ID；可选 `pageSize` 1–1000、`paginationToken` |
| `updateShipmentName`<br>`update_shipment_name.py` | PUT / 204 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/name` | 必填 plan/shipment ID；body 必填 `name`；成功响应无 body |
| `updateShipmentSourceAddress`<br>`update_shipment_source_address.py` | PUT / 202<br>异步 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/sourceAddress` | 必填 plan/shipment ID；body 必填 `address`，地址至少含 name/addressLine1/city/countryCode/phoneNumber/postalCode；返回 `operationId` |
| `updateShipmentTrackingDetails`<br>`update_shipment_tracking_details.py` | PUT / 202<br>异步 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/trackingDetails` | 必填 plan/shipment ID；body 必填 `trackingDetails`；返回 `operationId` |

## Tracking 输入

`trackingDetails` 按 shipment mode 二选一：

- SPD：`spdTrackingDetail` 中提供每个 `boxId` 对应的 `trackingId`。
- LTL/FTL：`ltlTrackingDetail` 中提供承运人给出的 freight bill/BOL 信息。

不在同一请求中同时提交 SPD 和 LTL tracking。更新前可以使用 `listShipmentBoxes` 取回真实 `boxId`。

## 跨版本提醒

`getShipment.shipmentId` 是 v2024 工作流 ID；`getShipment.shipmentConfirmationId` 是标签上的 ID。v0 `getLabels` 和 `getBillOfLading` 使用后者，见 [../identifiers.md](../identifiers.md)。
