# Transportation（3 operations）

路径版本：`/inbound/fba/2024-03-20`。

| Operation / 脚本 | HTTP / 成功 | Amazon path | 必要输入与语义 |
|---|---|---|---|
| `listTransportationOptions`<br>`list_transportation_options.py` | GET / 200 | `/inboundPlans/{inboundPlanId}/transportationOptions` | 必填 `inboundPlanId`；可选 `pageSize` 1–20、`paginationToken`、`placementOptionId`、`shipmentId`；返回 `transportationOptions` |
| `generateTransportationOptions`<br>`generate_transportation_options.py` | POST / 202<br>异步 | `/inboundPlans/{inboundPlanId}/transportationOptions` | body 必填 `placementOptionId`、`shipmentTransportationConfigurations`；返回 `operationId` |
| `confirmTransportationOptions`<br>`confirm_transportation_options.py` | POST / 202<br>异步・确认 | `/inboundPlans/{inboundPlanId}/transportationOptions/confirmation` | body 必填 `transportationSelections`，每项至少绑定 `shipmentId` + `transportationOptionId`；返回 `operationId` |

## Generate/list

- `shipmentTransportationConfigurations` 覆盖候选 placement 中的所有 shipments，按 mode 提供 ready-to-ship window、freight 和 pallet 信息。
- 不同 placement option 的 transportation 费用可能不同。在 placement 确认前，可按候选 `placementOptionId` 生成/列出 transportation options 供用户比较。
- 分页时保留 `placementOptionId` 和 `shipmentId` 过滤条件。
- 展示每个 option 的 shipment、carrier、`shippingMode`、`shippingSolution`、cost、void window、expiration 和 preconditions。

## Confirm

- 必须先确认 placement option。
- 每个 shipment 选择一个与之匹配的 transportation option。
- 自有承运人在 preconditions 要求时，先确认对应 delivery window。
- Amazon Partnered 确认意味着同意运费估算和 Amazon 扣费。
- 确认后不能再为该 plan 生成或确认新 transportation options。

`confirmTransportationOptions` 是高影响操作，不能从“列出方案”或“推荐便宜方案”自动进入确认。
