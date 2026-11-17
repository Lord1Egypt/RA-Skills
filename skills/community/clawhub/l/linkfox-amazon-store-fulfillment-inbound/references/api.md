# Fulfillment Inbound API 参考

本 Skill 通过 LinkFox `POST /spApi/developerProxy` 调用 Amazon Fulfillment Inbound API，覆盖：

- Fulfillment Inbound `v2024-03-20`：45 个 operation。
- Fulfillment Inbound `v0`：6 个 Amazon 仍保留的查询和文档 operation。
- 总计 51 个 operation：28 GET、16 POST、7 PUT。

官方基线：

- [Fulfillment Inbound API 概述](https://developer-docs.amazon.com/sp-api/docs/fulfillment-inbound-api)
- [v2024-03-20 Reference](https://developer-docs.amazon.com/sp-api/reference/fulfillment-inbound-v2024-03-20)
- [v2024-03-20 OpenAPI 模型](https://github.com/amzn/selling-partner-api-models/blob/main/models/fulfillment-inbound-api-model/fulfillmentInbound_2024-03-20.json)
- [v0 OpenAPI 模型](https://github.com/amzn/selling-partner-api-models/blob/main/models/fulfillment-inbound-api-model/fulfillmentInboundV0.json)

## 调用契约

调用规范：

- 请求地址：`${LINKFOX_TOOL_GATEWAY}/spApi/developerProxy`，未设置 `LINKFOX_TOOL_GATEWAY` 时回退 `https://tool-gateway.linkfox.com`。
- 认证：优先读取 `LINKFOX_AGENT_API_KEY`，回退 `LINKFOXAGENT_API_KEY`。
- 请求头：`Authorization: <api_key>`、`Content-Type: application/json`、`User-Agent: LinkFox-Skill/2.0`，并透传 `SESSION_ID`、`MODE_ID`、`APP_NAME`。
- HTTP 方法：对 LinkFox 网关固定使用 POST；网关 payload 中的 `method` 才是 Amazon operation 的 GET/POST/PUT。
- 超时：150 秒。

所有入口脚本接收一个 JSON 字符串。公共字段：

| 字段 | 必填 | 说明 |
|---|---|---|
| `sellerId` | 是 | 已授权的 Amazon Seller ID |
| `region` | 是 | `NA` / `EU` / `FE` |
| `requestBody` | 条件 | Amazon operation 的 JSON request body；不将本地控制字段混入其中 |
| `confirmWrite` | 提交类操作 | 用户明确确认后传布尔值 `true` |
| `skipDepCheck` | 否 | 仅调试时跳过本地 auth skill 探测 |

脚本根据 operation 固定 Amazon `method` 和 `path`；调用方不应传原始 `method`、`path`、`queryString` 或 token。`developerProxy` 使用 `sellerId + region` 在服务端解析授权。

默认仅缓存成功的读/生成结果，按 `SESSION_ID` 隔离 24 小时；写或生成新方案成功后清理当前会话旧缓存，再仅保留当次成功 generate 结果。需要明确刷新时在公开 wrapper 后加 `--no-cache`。

网关原始响应保留在 `developerProxy`，常见字段为 `errcode`、`httpStatus`、`contentType`、`body`。脚本同时将成功 JSON body 解析为 operation 结果字段。

## operation 索引

| 分组 | 数量 | 参考 |
|---|---:|---|
| Inbound Plans | 7 | [inbound-plans.md](apis/inbound-plans.md) |
| Packing | 7 | [packing.md](apis/packing.md) |
| Placement | 3 | [placement.md](apis/placement.md) |
| Shipments | 7 | [shipments.md](apis/shipments.md) |
| Shipment Content Updates | 4 | [shipment-content-updates.md](apis/shipment-content-updates.md) |
| Delivery Windows / Documents | 4 | [delivery-windows-and-documents.md](apis/delivery-windows-and-documents.md) |
| Self-Ship Appointments | 4 | [self-ship-appointments.md](apis/self-ship-appointments.md) |
| Transportation | 3 | [transportation.md](apis/transportation.md) |
| Prep / Compliance / Labels | 5 | [prep-compliance-labels.md](apis/prep-compliance-labels.md) |
| Asynchronous Operations | 1 | [asynchronous-operations.md](apis/asynchronous-operations.md) |
| 保留 v0 | 6 | [legacy-v0.md](apis/legacy-v0.md) |

## 异步操作

19 个 operation 会发起异步处理：18 个返回 HTTP 202，`generateSelfShipAppointmentSlots` 返回 HTTP 201。响应中的 `operationId` 只用于：

```text
getInboundOperationStatus(operationId)
  ├─ IN_PROGRESS → 稍后由调用方再查
  ├─ SUCCESS     → 再进入下一个工作流步骤
  └─ FAILED      → 输出 operationProblems，停止下游写操作
```

HTTP 201/202 不代表业务已完成。脚本单次运行不隐式轮询、不自动执行下一步。

## request body 语义

- 有必填字段的 body：传 `requestBody` 对象并在本地校验必填键。
- OpenAPI 要求 body 但没有必填属性：允许 `requestBody: {}`，例如 `generatePlacementOptions`。
- OpenAPI 无 body：不向上游发送 body，例如 `generatePackingOptions`。
- HTTP 204：`updateInboundPlanName` 和 `updateShipmentName` 成功时 body 为空，不当作 JSON 解析错误。

## 分页

v2024 的分页接口从响应 `pagination.nextToken` 取值，下一次请求传 `paginationToken`。必须保留首页的所有过滤字段；不自动拉取全部页。

v0 的 Amazon wire 使用 `NextToken` 等 PascalCase 名称；脚本 CLI 统一接收 `nextToken` 等 lowerCamelCase 名称并自动映射。

## 错误处理

- `errcode != 200`：保留网关错误，不尝试解析为 Amazon 成功响应。
- Amazon HTTP 400/403/404/409/413/415/422：修正请求或工作流状态后再调用。
- HTTP 429/500/503：由调用方决定延迟重试；确认、取消、预约以及其他 POST/PUT 在响应不确定时不得由脚本自动重放。现有网关仅对识别到的 token 过期执行一次刷新后透明重试。
- auth / billing 错误：按 [onboarding.md](onboarding.md) 处理。
- 上报问题时使用 `skillName: linkfox-amazon-store-fulfillment-inbound`，保留脱敏后的 `developerProxy`、operation 和关联 ID。

## curl 示例

```bash
curl --request POST "${LINKFOX_TOOL_GATEWAY}/spApi/developerProxy" \
  --header "Authorization: ${LINKFOX_AGENT_API_KEY}" \
  --header "Content-Type: application/json" \
  --header "User-Agent: LinkFox-Skill/2.0" \
  --data '{"sellerId":"A1SELLER","region":"NA","method":"GET","path":"inbound/fba/2024-03-20/inboundPlans/PLAN_ID"}'
```

公开脚本会固定并校验 `method`、`path`、query 和 body；面向用户调用时应使用对应 operation 脚本，而不是自行拼接上述网关 payload。

## Feedback

问题反馈地址：`https://skill-api.linkfox.com/api/v1/public/feedback`。自动检测到持续的授权错误、白名单拒绝、契约不一致或 Amazon 响应结构变化时，附带 `skillName`、operation、脱敏后的关联 ID 与响应摘要。
