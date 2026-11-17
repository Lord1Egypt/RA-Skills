# Fulfillment Outbound 工作流

## 报价与可履约性

1. 选择 `sellerId + region`。
2. 用 `getOffers` 比较多个 SKU 的服务等级与到期时间，或用 `getOrderPreview` 获取 planned shipments、费用和 constraints。
3. 发现 constraints 时停止创建，向用户展示受影响 SKU 和 Amazon 原因。

## 创建订单

1. 固定唯一 `orderId` 和每行唯一 `lineItemId`。
2. 展示目的地址、SKU、数量、service tier、费用和 `SHIP`/`HOLD`。
3. 获得明确确认后只调用一次 `createOrder`。
4. HTTP 200 读取 `order`；HTTP 202 用 `getOrder` 后续查询，禁止自动轮询。

## HOLD 后发货

1. `getOrder` 确认订单仍可更新。
2. 展示将从 HOLD 改为 SHIP 的订单并确认。
3. 调用 `updateOrder`，body 为 `{"fulfillmentConfiguration":{"action":"SHIP"}}`。
4. 用 `getOrder` 核实状态。

## 查询、分页和跟踪

- `listOrders` 使用 `updatedAfter` 或 `pageToken`；不自动遍历全部页。
- 需要 shipments、packages、tracking 或 proof-of-delivery 数据时传 `shipments: "INCLUDE"`。
- v2026 返回的 tracking 已嵌入 order shipments；不要调用旧版 `getPackageTrackingDetails`。

`getOrder(shipments="INCLUDE")` 已覆盖当前文档中的多个用例，不是额外 operation：

- 配送跟踪：`shipments[].packages[].tracking.carrier/amazon` 的 `trackingNumber` 和 `trackingUrl`。
- 签收凭证：`tracking.proofOfDelivery.deliveryPhotoUrl` 和 `receivedBy`；这些字段只在 Amazon 实际返回时展示，不伪造图片或收件人。
- 收件/投递位置：`tracking.dropOffLocation.type/attributes`，可表示 locker、delivery box、neighbor 等。
- 分包与部分履约：按 `shipmentItemIds` 将 package 与 shipment item 对应，并分别展示 shipment/package status。
- 单件标识：`shipment.items[].unitIdentifiers` 保留 Amazon 返回的制造批号/单位标识；不将其误当成 `lineItemId`。

POD 图片 URL 和收件人信息可能涉及收件人隐私；只在用户确实请求签收凭证时展示，不记录到问题反馈中。

## 发票头查询

1. 使用 `getInvoiceHeaders`，必传 `marketplaceId`。
2. 需要按开票时间过滤时同时传 `fromIssueDate` 和 `toIssueDate`，范围不超过 90 天；需要增量同步时使用 `invoicesModifiedAfter`。
3. 展示 `invoices[]`、`numOfRecords` 和 `nextToken`；不得自动翻页。
4. 该 operation 属于 Invoices v2026-06-25，不传 `fulfillmentServiceId`，也不把路径改写到 Outbound 前缀。

## 动态沙箱

1. `updateOrderStatus` 和 `updatePackage` 只用于测试订单，先展示 sandbox 目标、order/package ID 和状态变化。
2. 用户确认后传 `confirmWrite: true`。
3. 与现有 FBA Skill 一致，wrapper 使用统一 `/spApi/developerProxy`，不传额外 `sandbox` 字段；测试环境沿用 Amazon Store Skill 的网关配置。

## 区域和特殊履约配置

- Japan 预约配送/时段：先用 `getOrderPreview` 确认 `fulfillmentConfiguration.serviceLevel.deliveryInterval`，再将 Amazon 接受的配置传给 `createOrder`。
- Japan 投递偏好：`destination.dropOffLocation` 可表达 neighbor、delivery box、locker 等类型；只传用户明确提供且当地支持的 attributes。
- India：`paymentInformation` 及 line-item payment-on-delivery 字段仅在 Amazon India 当前支持的业务中使用。
- Cross-border：同时展示并确认 `origin.countryCode`、destination country 和 `perUnitDeclaredValue`；以 preview constraints 为准。
- Unbranded / SIPP / Block AMZL：先通过 preview/offers 获取当前可用的 service 配置，然后把用户确认的 `fulfillmentConfiguration.services.packaging/additional` 原样传入 `createOrder`；不自行猜测区域可用值。
- 订单状态通知属于 Notifications API 的 `FULFILLMENT_ORDER_STATUS` 订阅，不是 Outbound 的第 10 个 operation。

## 取消

1. `getOrder` 恢复最新状态。
2. 展示可能无法取消已进入拣货/发运的部分，并取得确认。
3. 调用 `cancelOrder` 一次。
4. HTTP 202 后通过 `getOrder` 核实；不把接受请求等同于取消完成。
