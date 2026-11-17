# linkfox-amazon-store-fba — API 与网关说明

## 1. 调用链

`POST ${LINKFOX_TOOL_GATEWAY}/spApi/developerProxy`

| 字段 | 说明 |
|------|------|
| region | NA / EU / FE |
| path | SP-API 相对路径，无前导 `/` |
| method | GET / POST / PUT / DELETE / PATCH |
| sellerId | 店铺 ID（网关解析 token） |
| queryString | 可选 |
| body + contentType | 写操作 |

环境变量：`LINKFOX_AGENT_API_KEY`（或 `LINKFOXAGENT_API_KEY`）、可选 `LINKFOX_TOOL_GATEWAY`。

## 2. 通用 JSON 入参

| 字段 | 必填 | 说明 |
|------|------|------|
| sellerId / region | 是 | |
| api / operation | 用 `fba_api.py` 时必填 | Amazon operationId |
| requestBody | 写操作推荐 | 官方 body |
| query | 否 | 额外 query 对象 |
| queryString | 否 | 原始查询串（覆盖） |
| skipDepCheck | 否 | 跳过 auth skill 探测 |
| marketplaceId | 否 | 自动提升为 marketplaceIds |

路径模板参数（如 `inboundPlanId`、`shipmentId`、`sellerSku`）直接写在同级 JSON。

## 3. 模块索引

完整表见 [`capabilities.md`](capabilities.md)，机器可读见 [`operations.json`](operations.json)。

### 3.1 Eligibility

- `getItemEligibilityPreview`：`asin` + `program`；INBOUND 需 marketplaceIds

### 3.2 Inventory

- `getInventorySummaries`：granularityType + granularityId + marketplaceIds
- `createInventoryItem` / `addInventory`：marketplaceId + requestBody
- `deleteInventoryItem`：sellerSku + marketplaceId

### 3.3 Inbound v0

- prepInstructions / labels / billOfLading / shipments / shipmentItems

### 3.4 Inbound 2024-03-20

- InboundPlan CRUD 与状态机：packing → placement → transportation → shipment
- 异步：`getInboundOperationStatus`
- items：compliance / labels / prepDetails

### 3.5 Outbound 2020-07-01

- preview / deliveryOffers / fulfillmentOrders CRUD / return / tracking / features

## 4. 官方入口

- [getItemEligibilityPreview](https://developer-docs.amazon.com/sp-api/reference/getitemeligibilitypreview)
- [FBA Inventory v1](https://developer-docs.amazon.com/sp-api/reference/fba-inventory-v1)
- [Fulfillment Inbound v2024-03-20](https://developer-docs.amazon.com/sp-api/reference/fulfillment-inbound-v2024-03-20)
- [Fulfillment Inbound v0](https://developer-docs.amazon.com/sp-api/reference/fulfillment-inbound-v0)
- [Fulfillment Outbound 2020-07-01](https://developer-docs.amazon.com/sp-api/reference/fulfillment-outbound-2020-07-01)

## 5. 错误处理

| 现象 | 处理 |
|------|------|
| 401/402 / 算力 | onboarding.md |
| 1005 | 放行 `fba/`、`inbound/fba/` |
| 403 | 角色/权限 |
| 409/422 | 状态机或参数问题 |
| 429 | 降速，先征得用户同意 |

## 6. Feedback

`skillName`：`linkfox-amazon-store-fba`
