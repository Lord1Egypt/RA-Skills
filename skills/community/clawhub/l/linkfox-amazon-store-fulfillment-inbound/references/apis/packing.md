# Packing（7 operations）

路径版本：`/inbound/fba/2024-03-20`。

| Operation / 脚本 | HTTP / 成功 | Amazon path | 必要输入与语义 |
|---|---|---|---|
| `listPackingGroupBoxes`<br>`list_packing_group_boxes.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/packingGroups/{packingGroupId}/boxes` | 必填 `inboundPlanId`、`packingGroupId`；可选 `pageSize` 1–100、`paginationToken` |
| `listPackingGroupItems`<br>`list_packing_group_items.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/packingGroups/{packingGroupId}/items` | 必填 `inboundPlanId`、`packingGroupId`；可选 `pageSize` 1–100、`paginationToken` |
| `setPackingInformation`<br>`set_packing_information.py` | POST / 202<br>异步 | `/inboundPlans/{inboundPlanId}/packingInformation` | body 必填 `packageGroupings`；每项必填 `boxes`，并在 `packingGroupId` / `shipmentId` 中二选一；返回 `operationId` |
| `listPackingOptions`<br>`list_packing_options.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/packingOptions` | 必填 `inboundPlanId`；可选 `pageSize` 1–20、`paginationToken`；返回 `packingOptions` |
| `generatePackingOptions`<br>`generate_packing_options.py` | POST / 202<br>异步 | `/inboundPlans/{inboundPlanId}/packingOptions` | 必填 `inboundPlanId`；无 body；返回 `operationId` |
| `confirmPackingOption`<br>`confirm_packing_option.py` | POST / 202<br>异步・确认 | `/inboundPlans/{inboundPlanId}/packingOptions/{packingOptionId}/confirmation` | 必填 `inboundPlanId`、`packingOptionId`；无 body；返回 `operationId` |
| `listInboundPlanPallets`<br>`list_inbound_plan_pallets.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/pallets` | 必填 `inboundPlanId`；可选 `pageSize` 1–1000、`paginationToken` |

## `setPackingInformation` 规则

- 已知箱规且 placement 尚未确认：每个 grouping 传已确认 packing option 中的 `packingGroupId`，省略 `shipmentId`。
- Pack Later 且 placement 已确认：每个 grouping 传已确认 placement 中的 `shipmentId`，省略 `packingGroupId`。
- India custom-placement 是特例：官方 India 用例要求先为选定 placement 的所有 `shipmentId` 设置 packing information，然后才 `confirmPlacementOption`。
- `boxes` 每个 grouping 1–5000。一般包含 `contentInformationSource`、dimensions、weight、quantity 和 items。
- `contentInformationSource` 为 `BARCODE_2D` 或 `MANUAL_PROCESS` 时，`items` 应保留为 `null`，不能在清理 JSON 时擅自删除。
- 重新设置箱规后，之前生成的 placement options 失效，要重新 generate/list。

`confirmPackingOption` 前先展示 packing groups、supported configurations 和可能的 incentive；不按列表序号隐式确认。
