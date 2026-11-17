# Self-Ship Appointments（4 operations）

路径版本：`/inbound/fba/2024-03-20`。仅适用于 `MX`、`BR`、`EG`、`SA`、`AE`、`IN` marketplaces。

| Operation / 脚本 | HTTP / 成功 | Amazon path | 必要输入与语义 |
|---|---|---|---|
| `cancelSelfShipAppointment`<br>`cancel_self_ship_appointment.py` | PUT / 202<br>异步・取消 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/selfShipAppointmentCancellation` | 必填 plan/shipment ID；body 必须存在，可为 `{}` 或包含 `reasonComment`；返回 `operationId` |
| `getSelfShipAppointmentSlots`<br>`get_self_ship_appointment_slots.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/selfShipAppointmentSlots` | 必填 plan/shipment ID；可选 `pageSize` 1–100、`paginationToken`；返回 `selfShipAppointmentSlotsAvailability` |
| `generateSelfShipAppointmentSlots`<br>`generate_self_ship_appointment_slots.py` | POST / 201<br>异步 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/selfShipAppointmentSlots` | body 必须存在，可为 `{}`；可选 `desiredStartDate`、`desiredEndDate`；返回 `operationId` |
| `scheduleSelfShipAppointment`<br>`schedule_self_ship_appointment.py` | POST / 200<br>预约/改期 | `/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/selfShipAppointmentSlots/{slotId}/schedule` | 必填 plan/shipment/slot ID；body 必须存在，可为 `{}`；改期时必填 `reasonComment`；同步返回 `selfShipAppointmentDetails` |

## 执行顺序

```text
getShipment → 确认 amazonReferenceId 存在
generateSelfShipAppointmentSlots → getInboundOperationStatus == SUCCESS
getSelfShipAppointmentSlots → 展示 slot/date/expiration
用户明确确认
scheduleSelfShipAppointment
```

不传期望日期时，Amazon 默认提供未来 42 天的可用 slot。`slotId` 与当前 plan + shipment 绑定；生成新 slots 后不复用旧 ID。

`scheduleSelfShipAppointment` 和 `cancelSelfShipAppointment` 均是高影响操作。执行前显示 FC、shipment、日期时间、slot ID 和当前 appointment，并取得用户明确确认。
