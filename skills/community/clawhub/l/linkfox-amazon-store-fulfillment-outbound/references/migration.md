# 从 Fulfillment Outbound v2020-07-01 迁移

| v2020-07-01 | v2026-07-04 |
|---|---|
| `getFulfillmentPreview` | `getOrderPreview` |
| `deliveryOffers` | `getOffers` |
| `createFulfillmentOrder` | `createOrder` |
| `listAllFulfillmentOrders` | `listOrders` |
| `getFulfillmentOrder` | `getOrder` |
| `updateFulfillmentOrder` | `updateOrder` |
| `cancelFulfillmentOrder` | `cancelOrder` |
| `submitFulfillmentOrderStatusUpdate` | `updateOrderStatus`（沙箱专用） |

基础路径从 `/fba/outbound/2020-07-01` 改为 `/fulfillment/outbound/2026-07-04`。请求和响应字段也发生重构，例如 `sellerFulfillmentOrderId` 改为 `orderId`，商品标识使用 `amazonSku`，items/quantity 结构改为 lineItems/amount。

以下旧操作没有当前版本的一一替代：`getFeatures`、`getFeatureSKU`、`getFeatureInventory`、`createFulfillmentReturn`、`listReturnReasonCodes`。`getPackageTrackingDetails` 已迁移到 Amazon Shipment Tracking API。不要为了兼容旧调用而把这些 operation 注册到新路径。

官方迁移指南：[Fulfillment Outbound migration guide](https://developer-docs.amazon.com/sp-api/docs/fulfillment-outbound-migration-guide)。
