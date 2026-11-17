# Placement（3 operations）

路径版本：`/inbound/fba/2024-03-20`。

| Operation / 脚本 | HTTP / 成功 | Amazon path | 必要输入与语义 |
|---|---|---|---|
| `listPlacementOptions`<br>`list_placement_options.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/placementOptions` | 必填 `inboundPlanId`；可选 `pageSize` 1–20、`paginationToken`；返回 `placementOptions` |
| `generatePlacementOptions`<br>`generate_placement_options.py` | POST / 202<br>异步 | `/inboundPlans/{inboundPlanId}/placementOptions` | body 必须存在但允许 `{}`；India 可传 `customPlacement`；返回 `operationId` |
| `confirmPlacementOption`<br>`confirm_placement_option.py` | POST / 202<br>异步・确认 | `/inboundPlans/{inboundPlanId}/placementOptions/{placementOptionId}/confirmation` | 必填 `inboundPlanId`、`placementOptionId`；无 body；返回 `operationId` |

## 选择规则

- 一个 inbound plan 只确认一个 placement option。
- 每个 option 可能产生一个或多个 `shipmentId`，并包含 placement fee 或 discount。
- 确认前展示 `placementOptionId`、所有 shipment 划分、费用/折扣和有效期。
- 修改 packing information 后必须重新生成 placement options。
- India `customPlacement` 是数组，每项必填 `warehouseId` 和 `items`；不用于其他 marketplace。

`confirmPlacementOption` 是高影响操作。其成功后通过 `getShipment` 取得 `shipmentConfirmationId`，该值才是 v0 labels/BOL 应使用的标签 shipment ID。
