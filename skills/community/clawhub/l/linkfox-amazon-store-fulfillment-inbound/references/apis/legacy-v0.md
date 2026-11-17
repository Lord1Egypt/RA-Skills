# 保留的 Fulfillment Inbound v0（6 operations）

Amazon 官方仍保留以下 6 个 v0 operation。本 Skill 不包含已废弃的 v0 创建、修改、运输估算或确认 operation。

| Operation / 脚本 | HTTP / 成功 | Amazon path | 必要输入与语义 |
|---|---|---|---|
| `getPrepInstructions`<br>`get_prep_instructions.py` | GET / 200 | `/fba/inbound/v0/prepInstructions` | CLI 必填 `shipToCountryCode`；通常传 `sellerSKUList` / `asinList` 至少一组，各最多 50；返回 prep instructions 和 invalid SKU/ASIN |
| `getLabels`<br>`get_labels.py` | GET / 200 | `/fba/inbound/v0/shipments/{shipmentId}/labels` | path 使用 `shipmentConfirmationId`；CLI 必填 `pageType`、`labelType`；按模式可传 packages/pallets/page 参数；返回 `payload.DownloadURL` |
| `getBillOfLading`<br>`get_bill_of_lading.py` | GET / 200 | `/fba/inbound/v0/shipments/{shipmentId}/billOfLading` | path 使用 `shipmentConfirmationId`；返回 `payload.DownloadURL` |
| `getShipments`<br>`get_shipments.py` | GET / 200 | `/fba/inbound/v0/shipments` | CLI 必填 `queryType`、`marketplaceId`；其他参数受 QueryType 约束；返回 `ShipmentData`、`NextToken` |
| `getShipmentItemsByShipmentId`<br>`get_shipment_items_by_shipment_id.py` | GET / 200 | `/fba/inbound/v0/shipments/{shipmentId}/items` | 必填 legacy `shipmentId`；`marketplaceId` 已废弃，不传；返回 `ItemData`、`NextToken` |
| `getShipmentItems`<br>`get_shipment_items.py` | GET / 200 | `/fba/inbound/v0/shipmentItems` | CLI 必填 `queryType`、`marketplaceId`；其他参数受 QueryType 约束；返回 `ItemData`、`NextToken` |

## v0 query 规则

v0 参数大小写是 Amazon wire 契约的一部分。脚本 CLI 只需传项目统一的 lowerCamelCase 名称，执行器自动映射：`marketplaceId → MarketplaceId`、`queryType → QueryType`、`nextToken → NextToken`。

`getShipments.queryType`：

- `SHIPMENT`：传 `shipmentStatusList` 和/或 `shipmentIdList`（最多 999）。
- `DATE_RANGE`：传 `lastUpdatedAfter` / `lastUpdatedBefore`。
- `NEXT_TOKEN`：传上一页的 `nextToken`，不混用新筛选条件。

`getShipmentItems.queryType`：

- `DATE_RANGE`：传 `lastUpdatedAfter` / `lastUpdatedBefore`。
- `NEXT_TOKEN`：传 `nextToken`，只继续上一页查询。

v0 数组 query 使用该 API 的 CSV wire 格式，不复用 v2024 `mskus` 的重复 key 规则。

## Labels 和 BOL

v2024 工作流中，先：

```text
getShipment(inboundPlanId, shipmentId)
  → shipmentConfirmationId
  → getLabels / getBillOfLading 的 v0 {shipmentId} path
```

- 不要将 v2024 38 字符 `shipmentId` 直接作为 label/BOL 路径值。
- CLI `packageLabelsToPrint` 要与 v2024 `listShipmentBoxes` 返回的 `boxId` 一致，否则 Amazon 可返回 `IncorrectPackageIdentifier`。
- CLI `labelType` 允许 `BARCODE_2D`、`UNIQUE`、`PALLET`；`pageType` 是 marketplace 相关枚举。
- Non-Partnered LTL labels 需要 `pageSize` 和 `pageStartIndex`，`pageSize` 最大 1000。
- `numberOfPallets` 为每个 pallet 返回四张相同标签。
- labels 和 BOL 的 `DownloadURL` 仅有效约 15 秒；如用户要文件，调用者应在同一任务中取得 URL 后立即下载。

下载时只使用 Amazon 当次响应的 HTTPS URL，不接受用户提供的任意 URL。
