# Prep、Compliance 与 Marketplace Labels（5 operations）

路径版本：`/inbound/fba/2024-03-20`。

| Operation / 脚本 | HTTP / 成功 | Amazon path | 必要输入与语义 |
|---|---|---|---|
| `listItemComplianceDetails`<br>`list_item_compliance_details.py` | GET / 200 | `/items/compliance` | query 必填 `mskus` 1–100 和 `marketplaceId`；返回 `complianceDetails`；India 专用 |
| `updateItemComplianceDetails`<br>`update_item_compliance_details.py` | PUT / 202<br>异步 | `/items/compliance` | query 必填 `marketplaceId`；body 必填 `msku`、`taxDetails`；返回 `operationId`；India 专用 |
| `createMarketplaceItemLabels`<br>`create_marketplace_item_labels.py` | POST / 200<br>文档 | `/items/labels` | body 必填 `labelType`、`marketplaceId`、`mskuQuantities` 1–100；可选 `pageType`、`localeCode`、width/height；返回 `documentDownloads` |
| `listPrepDetails`<br>`list_prep_details.py` | GET / 200 | `/items/prepDetails` | query 必填 `marketplaceId`、`mskus` 1–100；返回 `mskuPrepDetails` |
| `setPrepDetails`<br>`set_prep_details.py` | POST / 202<br>异步 | `/items/prepDetails` | body 必填 `marketplaceId`、`mskuPrepDetails`；返回 `operationId` |

## MSKU query 编码

`listItemComplianceDetails` 和 `listPrepDetails` 使用重复 key，不使用 CSV：

```text
mskus=SKU-1&mskus=SKU-2&marketplaceId=...
```

Amazon 要求 MSKU 中的下列字符在最终 URL 中双重 percent encode：

```text
% → %2525
+ → %252B
, → %252C
```

不能将过长 MSKU 列表静默截断。如 LinkFox `queryString` 超过限制，应报错并让调用方显式分批。

## Prep details 一致性

- 先 `setPrepDetails` 并等待异步成功，再 `listPrepDetails`。
- Seller Central 中设置的 prep details 不会由该 operation 返回。
- US marketplace 要求卖家在入库前完成商品 prep 和 label。

## Marketplace item label 文档

`documentDownloads[]` 包含 `downloadType`、`uri` 和可选 `expiration`。如用户需要文件，只使用当次响应的 HTTPS URI 立即下载，不接受任意 URL 作为输入。
