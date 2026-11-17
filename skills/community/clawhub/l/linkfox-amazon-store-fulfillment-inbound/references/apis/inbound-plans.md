# Inbound Plans（7 operations）

路径版本：`/inbound/fba/2024-03-20`。

| Operation / 脚本 | HTTP / 成功 | Amazon path | 必要输入与语义 |
|---|---|---|---|
| `listInboundPlans`<br>`list_inbound_plans.py` | GET / 200 | `/inboundPlans` | 可选 `pageSize` 1–30、`paginationToken`、`status` (`ACTIVE/VOIDED/SHIPPED`)、`sortBy` (`LAST_UPDATED_TIME/CREATION_TIME`)、`sortOrder` (`ASC/DESC`)；返回 `inboundPlans` + `pagination` |
| `createInboundPlan`<br>`create_inbound_plan.py` | POST / 202<br>异步 | `/inboundPlans` | body 必填 `destinationMarketplaces`、`items`、`sourceAddress`，可选 `name`；返回 `inboundPlanId` + `operationId` |
| `getInboundPlan`<br>`get_inbound_plan.py` | GET / 200 | `/inboundPlans/{inboundPlanId}` | 必填 `inboundPlanId`；返回 plan 状态、marketplaces、packing/placement options 和 shipments 摘要 |
| `listInboundPlanBoxes`<br>`list_inbound_plan_boxes.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/boxes` | 必填 `inboundPlanId`；可选 `pageSize` 1–1000、`paginationToken` |
| `cancelInboundPlan`<br>`cancel_inbound_plan.py` | PUT / 202<br>异步・取消 | `/inboundPlans/{inboundPlanId}/cancellation` | 必填 `inboundPlanId`；无 body；返回 `operationId` |
| `listInboundPlanItems`<br>`list_inbound_plan_items.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/items` | 必填 `inboundPlanId`；可选 `pageSize` 1–1000、`paginationToken` |
| `updateInboundPlanName`<br>`update_inbound_plan_name.py` | PUT / 204 | `/inboundPlans/{inboundPlanId}/name` | 必填 `inboundPlanId`；body 必填 `name`；成功响应无 body |

## Create 要点

- `destinationMarketplaces` 当前每个 plan 只传一个 marketplace ID。
- `items` 中每项的关键字段是 `msku`、`quantity`、`prepOwner`、`labelOwner`；按商品需要增加 `expiration` 或 `manufacturingLotCode`。
- `sourceAddress` 至少包含 `name`、`addressLine1`、`city`、两位大写 `countryCode`、`phoneNumber`、`postalCode`。创建后如需修改单个 shipment 的发货地址，使用 `updateShipmentSourceAddress`。
- 保留 `createInboundPlan` 返回的两个 ID：`operationId` 用于查状态，`inboundPlanId` 用于后续全部 plan operation。

`cancelInboundPlan` 是不可隐式执行的高影响操作；执行前展示 plan ID 和当前状态并取得用户明确确认。
