# Fulfillment Outbound API v2026-07-04 参考

## 调用规范

- 请求地址：`${LINKFOX_TOOL_GATEWAY}/spApi/developerProxy`；未设置网关变量时回退 `https://tool-gateway.linkfox.com`。
- 认证：优先 `LINKFOX_AGENT_API_KEY`，回退 `LINKFOXAGENT_API_KEY`。
- 请求头：`Authorization: <api_key>`、`Content-Type: application/json`、`User-Agent: LinkFox-Skill/2.0`，并透传 `SESSION_ID`、`MODE_ID`、`APP_NAME`。
- 超时：150 秒。
- 对 LinkFox 网关固定使用 POST；payload 中的 `method` 才是 Amazon GET/POST/PUT。
- 公共 CLI 参数：`sellerId`、`region`；有 body 的 operation 使用 `requestBody`。Amazon 分配多租户服务标识时，可额外传顶层 `fulfillmentServiceId`（1–40 字符），服务端仅将它映射为 `x-amzn-fulfillment-service-id`。
- `createOrder` / `updateOrder` / `cancelOrder` 需用户明确确认后传布尔值 `confirmWrite: true`。
- 禁止传入 token、原始 `path`、`method`、`queryString` 或 `body` 覆盖固定契约；禁止直接传原始 `x-amzn-fulfillment-service-id` 或把服务标识放入 query/body。

默认仅缓存成功的读/预览结果，按 `SESSION_ID` 隔离 24 小时；写操作成功后清理当前会话缓存。需要明确刷新时在公开 wrapper 后加 `--no-cache`。

官方基线：

- [Fulfillment Outbound API](https://developer-docs.amazon.com/sp-api/docs/fulfillment-outbound-api)
- [v2026-07-04 Reference](https://developer-docs.amazon.com/sp-api/reference/fulfillment-outbound-v2026-07-04)
- [v2026-07-04 OpenAPI Model](https://github.com/amzn/selling-partner-api-models/blob/main/models/fulfillment-outbound-api-model/fulfillmentOutbound_2026-07-04.json)

## Operation 契约

| Operation | Amazon method/path | 输入 | 成功状态 |
|---|---|---|---|
| `getOrderPreview` | POST `/fulfillment/outbound/2026-07-04/previews` | body | 200 |
| `getOffers` | POST `/fulfillment/outbound/2026-07-04/offers` | body | 200 |
| `createOrder` | POST `/fulfillment/outbound/2026-07-04/orders` | body | 200/202 |
| `listOrders` | GET `/fulfillment/outbound/2026-07-04/orders` | query | 200 |
| `getOrder` | GET `/fulfillment/outbound/2026-07-04/orders/{orderId}` | path/query | 200 |
| `updateOrder` | PUT `/fulfillment/outbound/2026-07-04/orders/{orderId}` | path/body | 202 |
| `cancelOrder` | PUT `/fulfillment/outbound/2026-07-04/orders/{orderId}/cancel` | path | 202 |
| `updateOrderStatus` | PUT `/fulfillment/outbound/2026-07-04/orders/{orderId}/status` | path/body | 204，沙箱专用 |
| `updatePackage` | PUT `/fulfillment/outbound/2026-07-04/orders/{orderId}/packages/{packageId}` | path/body | 204，沙箱专用 |
| `getInvoiceHeaders` | GET `/finances/invoices/2026-06-25/invoices` | query | 200，关联的 Invoices API operation |

### getOrderPreview

必填 body：

- `destination.deliveryAddress`：地址至少包含 `name`、`addressLine1`、`postalCode`、两位大写 `countryCode`。
- `lineItems[]`：每项包含 `product.productIdentifier.amazonSku` 和 `amount.value`；`amount.unit` 如提供应为 `EACHES`。

可选：`channel`、`fulfillmentConfiguration`、`origin`、`excludeEstimatedFees`、`includePaymentOnDelivery`。响应关键字段：`plannedShipments[]`、`constraints[]`。

### getOffers

必填 body：

- `origin.countryCode`
- `items[].productIdentifier.amazonSku`

Amazon 当前 schema 没有将 `OfferItem.productIdentifier` 标为 required，但空 item 无法定位 SKU；本 Skill 为避免消耗一次无效付费调用，在本地要求每个 item 提供 `productIdentifier.amazonSku`。预览、创建和报价的数组也要求至少一项。

可选 `destination` 和 `fulfillmentConfiguration`。响应关键字段为 `offerResults[]`，每项包含输入 item、`offers[]`、可能的 `constraints[]`。

### createOrder

必填 body：

- `orderId`：卖家生成的唯一订单标识。
- `destination.deliveryAddress`
- `lineItems[]`：每项包含唯一 `lineItemId`、`product.productIdentifier.amazonSku`、`amount.value`。

可选：`channel`、`origin`、`fulfillmentConfiguration`、`paymentInformation`。`fulfillmentConfiguration.action` 常见为 `SHIP` 或 `HOLD`；policy 可为 `FILL_OR_KILL`、`FILL_ALL`、`FILL_ALL_AVAILABLE`。

HTTP 200 返回 `order`；HTTP 202 返回至少 `orderId` 和 `status`。202 后通过 `getOrder` 恢复状态。

### listOrders

query 参数：

- `updatedAfter`：ISO 8601 date-time。
- `pageToken`：从上一页 `pagination.nextToken` 获取。
- `shipments`：`INCLUDE` / `EXCLUDE`。

响应关键字段：`orders[]`、`pagination.nextToken`。脚本不自动翻页。

### getOrder

- path：`orderId`，1–40 字符。
- query：可选 `shipments=INCLUDE|EXCLUDE`。
- 响应：`order`；包含状态、配置、地址、line items，选择 INCLUDE 时可包含 shipments、packages 与 tracking。

`getOrder` 的当前响应模型已承载多个旧版独立查询场景，不需要在 v2026 路径上虚构额外 operation：

- `shipments[].packages[].tracking.carrier|amazon`：承运商/Amazon 跟踪号和 URL；
- `tracking.proofOfDelivery.deliveryPhotoUrl|receivedBy`：投递照片或签收人；
- `tracking.dropOffLocation`：包括日本 locker/delivery box 等投放位置；
- `shipments[].items[].unitIdentifiers`：商品实例/序列号标识；
- 多个 `shipments` / `packages` 以及 line item 的 `cancelledAmount` / `unfulfillableAmount`：用于拆包和部分履约状态。

这些字段均由 wrapper 保留在完整响应中；仅在用户需要包裹/跟踪明细时传 `shipments: "INCLUDE"`。

### updateOrder

- path：`orderId`。
- body：`fulfillmentConfiguration`；当前模型只允许更新 action。通常用 `{"fulfillmentConfiguration":{"action":"SHIP"}}` 释放 HOLD。
- HTTP 202 表示已接受，不代表更新完成；后续用 `getOrder` 核实。

### cancelOrder

- path：`orderId`。
- 无 request body。
- HTTP 202 表示取消请求已接受；后续用 `getOrder` 核实最终状态。

### 动态沙箱操作

- `updateOrderStatus` body：`status`，允许 `PROCESSING`、`COMPLETE`、`COMPLETE_PARTIAL`、`CANCELLED`、`UNFULFILLABLE`、`INVALID`。
- `updatePackage` body：必填 `status`，可选 `deliveryTime`、`tracking`。路径直接结束于 `{packageId}`，没有额外 `/status` 段。

Amazon OpenAPI 对这两个路径显式设置 `x-amzn-api-sandbox-only: true`。按照现有 FBA Skill 的统一调用方式，wrapper 仍使用标准 `/spApi/developerProxy` 请求结构，不接收也不发送单独的 `sandbox` 控制字段，不需要 Skill 专属 sandbox 配置。只能用于 sandbox 测试数据，路径是否可用由统一网关及其上游路由决定。两项写操作同样要求 `confirmWrite: true`。

### 关联的 `getInvoiceHeaders`

Amazon Outbound 概述页的“Roles for v2026-07-04”列表展示 `getInvoiceHeaders`，实际 Reference 路径为 `GET /finances/invoices/2026-06-25/invoices`，属于 **Invoices API v2026-06-25**，且不在 `fulfillmentOutbound_2026-07-04.json` 的 9 个 operation 中。本 Skill 仍按概述页提供 `get_invoice_headers.py`，但保留真实 API 归属和路径，不把它拼接到 Outbound 路径。

query：

- `marketplaceId`：必填。
- `nextToken`：分页 token；脚本不自动翻页，Amazon 可能返回空页。
- `fromIssueDate` / `toIssueDate`：必须同时提供或同时省略，ISO 8601 date-time，范围不得超过 90 天。
- `invoicesModifiedAfter`：可选 ISO 8601 date-time。

响应关键字段为 `invoices[]`、`numOfRecords`、`nextToken`。该 operation 不定义 `x-amzn-fulfillment-service-id`，因此禁止传 `fulfillmentServiceId`。

## 响应与错误

公开脚本保留以下外层结构：

- `operationId`、`method`、`resolvedPath`
- `queryString` / `requestBody`（存在时）
- `developerProxy.errcode`、`developerProxy.httpStatus`、`developerProxy.contentType`、`developerProxy.body`
- 解析后的 operation 结果字段
- 202 时可能有 `nextAction`，但不会自动轮询

判定顺序：先检查 `errcode == 200`，再检查 Amazon `httpStatus`，最后读取解析结果。400/403/404/413/415 修正请求；429/500/503 或超时不自动重放写操作。

## curl 示例

```bash
curl --request POST "${LINKFOX_TOOL_GATEWAY}/spApi/developerProxy" \
  --header "Authorization: ${LINKFOX_AGENT_API_KEY}" \
  --header "Content-Type: application/json" \
  --header "User-Agent: LinkFox-Skill/2.0" \
  --data '{"sellerId":"A1SELLER","region":"NA","method":"GET","path":"fulfillment/outbound/2026-07-04/orders/ORDER-1","queryString":"shipments=INCLUDE","fulfillmentServiceId":"tenant-1"}'
```

面向用户应调用固定 operation 脚本，不应直接允许其覆盖上述 method/path。

## Feedback

问题反馈地址：`https://skill-api.linkfox.com/api/v1/public/feedback`。附 `skillName: linkfox-amazon-store-fulfillment-outbound`、operation、脱敏 ID、resolved path、HTTP 状态与响应摘要。
