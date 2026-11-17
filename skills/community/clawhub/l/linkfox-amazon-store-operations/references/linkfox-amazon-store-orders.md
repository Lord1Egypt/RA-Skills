---
name: linkfox-amazon-store-orders
description: 亚马逊店铺订单管理。支持订单列表与详情查询、买家信息、收货地址、订单行获取、发货确认及管制订单核验。
---

# 亚马逊店铺订单（Amazon Store Orders）

本 skill 用于查询与管理亚马逊店铺订单，覆盖订单列表、详情、买家信息、收货地址、订单行、发货确认及管制订单核验。与 **`linkfox-amazon-store-auth`**、**`linkfox-amazon-store-report`**、**`linkfox-amazon-store-listings`**、**`linkfox-amazon-store-pricing`** 同系列。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 调用 SP-API Orders：v2026-01-01 的 `searchOrders`、`getOrder`；v0 的 `getOrderBuyerInfo`、`getOrderAddress`、`getOrderItems`、`getOrderItemsBuyerInfo`、`updateShipmentStatus`、`getOrderRegulatedInfo`、`updateVerificationStatus`、`confirmShipment`。
- 支持订单检索与分页（`paginationToken`）、按时间/履约状态/履约方筛选。
- 支持发货状态更新、发货确认、管制订单核验状态更新等写操作。

### ❌ 边界与限制

- **依赖**：必须先安装 **`linkfox-amazon-store-auth`** 并取得 `accessToken`，本 skill 不实现授权或令牌逻辑。
- **权限**：需 **Orders** 及相关角色；部分受限 PII 读取可能需 **Restricted Data Token（RDT）**，不在本 skill 内实现。
- **v0 接口**：`getOrderBuyerInfo` / `getOrderAddress` / `getOrderItems` / `getOrderItemsBuyerInfo` 在官方文档中为 **deprecated**，新集成优先用 v2026-01-01 的 `searchOrders` / `getOrder` 配合 `includedData`。
- **路径白名单**：网关若返回 **1005** 等拒绝转发，需后端放行 `orders/v0/...` 与 `orders/2026-01-01/...` 前缀。
- **速率**：`searchOrders` 默认速率较低（约 0.0056 req/s），注意 **429**。
- **成本**：本工具消耗积分；失败/空结果不得自动换关键词、翻页或连续试探。

## 执行流程

### 步骤 1：依赖检查

- 【输入】无
- 【动作】运行 `python scripts/check_auth_dependency.py`；若 exit code **42** 且 stderr 含 `DEPENDENCY_MISSING:`，先安装 **`linkfox-amazon-store-auth`**。
- 【输出】确认依赖就绪，可继续后续调用。

### 步骤 2：获取访问令牌

- 【输入】`sellerId`、`region`（NA / EU / FE 等，与 auth 一致）
- 【动作】`POST ${LINKFOX_TOOL_GATEWAY}/spApi/storeTokens`，Body：`{"sellerId":"<卖家ID>","region":"NA|EU|FE|..."}`。
- 【输出】响应中的 **`accessToken`**（供下一步 developerProxy 使用）。

### 步骤 3：转发 SP-API 订单操作

- 【输入】`accessToken`、`region`、目标 `path`、`method`（GET/POST/PATCH）、可选 `queryString` / `body`
- 【动作】`POST ${LINKFOX_TOOL_GATEWAY}/spApi/developerProxy`，按脚本一览选择对应脚本与 path。
- 【输出】网关响应 JSON（`developerProxy.errcode` / `httpStatus` / `body`）及脚本解析字段（如 `searchOrders`、`order`、`orderItems` 等）。完整响应落盘至 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-orders-<timestamp>.json`。

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（不同 SP-API 操作通过 path/method 区分；完整参数/响应/错误码见 [references/api.md](references/api.md)）。
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（脚本见下方「脚本一览」）。
- **成本约束**：需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-orders-<timestamp>.json`（`<session>` 取自环境变量 `SESSION_ID`；**禁止写入 /tmp**，当前目录不可写则报错）。
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout。
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）。
- 加 `--inline` 强制全量打印到 stdout（同样落盘）。

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取。

## 脚本一览

| 能力 | developerProxy `path`（要点） | 脚本 |
|------|------------------------------|------|
| searchOrders | `orders/2026-01-01/orders` + Query | `search_orders.py` |
| getOrder | `orders/2026-01-01/orders/{orderId}` + Query | `get_order.py` |
| getOrderBuyerInfo | `orders/v0/orders/{orderId}/buyerInfo` | `get_order_buyer_info.py` |
| getOrderAddress | `orders/v0/orders/{orderId}/address` | `get_order_address.py` |
| getOrderItems | `orders/v0/orders/{orderId}/orderItems` + NextToken | `get_order_items.py` |
| getOrderItemsBuyerInfo | `orders/v0/orders/{orderId}/orderItems/buyerInfo` | `get_order_items_buyer_info.py` |
| updateShipmentStatus | `orders/v0/orders/{orderId}/shipment`，POST JSON | `update_shipment_status.py` |
| getOrderRegulatedInfo | `orders/v0/orders/{orderId}/regulatedInfo` | `get_order_regulated_info.py` |
| updateVerificationStatus | `orders/v0/orders/{orderId}/regulatedInfo`，PATCH JSON | `update_verification_status.py` |
| confirmShipment | `orders/v0/orders/{orderId}/shipmentConfirmation`，POST JSON | `confirm_shipment.py` |

共享逻辑见 `scripts/_spapi_orders_common.py`（仅供同目录脚本 import，非独立 CLI）。

## 使用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/search_orders.py '{"sellerId":"A1...","region":"NA","marketplaceIds":["ATVPDKIKX0DER"],"lastUpdatedAfter":"2026-05-01T00:00:00Z"}'

python scripts/get_order.py '{"sellerId":"A1...","region":"NA","orderId":"123-1234567-1234567","includedData":["FULFILLMENT","PACKAGES"]}'
```

## 展示规则

1. 先看网关 **`developerProxy.errcode`** / **`httpStatus`**，再解析各脚本附加字段（如 `searchOrders`、`order`）。
2. **POST/PATCH** 脚本：`stdout` 中含 **`requestBody`**（组装后的 Amazon 请求体），便于排查。
3. **v0** 买家/地址/行项目接口为 deprecated；新集成优先用 **v2026-01-01** 的 `searchOrders` / `getOrder` 与 `includedData` 拉齐业务字段。
4. `searchOrders` 默认速率较低，注意 **429**。
5. 受限 PII / RDT 以 Amazon 数据保护政策为准；详见 [references/api.md](references/api.md)。

## 用户表达与场景速查

**适用** —— 亚马逊店铺订单查询与管理：

| 用户说 | 场景 |
|--------|------|
| "查一下亚马逊订单"、"最近订单列表" | 订单检索（searchOrders） |
| "看下这个订单详情" | 单笔订单（getOrder） |
| "买家信息"、"收货地址" | 买家/地址（getOrderBuyerInfo / getOrderAddress） |
| "订单行项目"、"订单里的商品" | 订单行（getOrderItems） |
| "确认发货"、"标记已发货" | 发货确认（confirmShipment / updateShipmentStatus） |
| "管制订单"、"核验状态" | 管制订单核验（getOrderRegulatedInfo / updateVerificationStatus） |
| "SP-API 订单"、"Orders API" | 通用订单接口调用 |

不适用场景见上方【能力边界】。

## 官方参考索引

| 能力 | 文档 |
|------|------|
| searchOrders | [searchOrders](https://developer-docs.amazon.com/sp-api/reference/searchorders) |
| getOrder (v2026-01-01) | [getOrder](https://developer-docs.amazon.com/sp-api/reference/getorder-3) |
| getOrderBuyerInfo (deprecated) | [getOrderBuyerInfo](https://developer-docs.amazon.com/sp-api/reference/getorderbuyerinfo) |
| getOrderAddress (deprecated) | [getOrderAddress](https://developer-docs.amazon.com/sp-api/reference/getorderaddress) |
| getOrderItems (deprecated) | [getOrderItems](https://developer-docs.amazon.com/sp-api/reference/getorderitems) |
| getOrderItemsBuyerInfo (deprecated) | [getOrderItemsBuyerInfo](https://developer-docs.amazon.com/sp-api/reference/getorderitemsbuyerinfo) |
| updateShipmentStatus | [updateShipmentStatus](https://developer-docs.amazon.com/sp-api/reference/updateshipmentstatus) |
| getOrderRegulatedInfo | [getOrderRegulatedInfo](https://developer-docs.amazon.com/sp-api/reference/getorderregulatedinfo) |
| updateVerificationStatus | [updateVerificationStatus](https://developer-docs.amazon.com/sp-api/reference/updateverificationstatus) |
| confirmShipment | [confirmShipment](https://developer-docs.amazon.com/sp-api/reference/confirmshipment) |

## 解决认证和积分问题

发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用 skill 内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个 skill 并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个 skill。

---

# linkfox-amazon-store-orders — API 与网关调用说明

## 1. 调用链

1. **`POST ${LINKFOX_TOOL_GATEWAY}/spApi/storeTokens`**  
   Body: `{"sellerId":"<卖家ID>","region":"NA|EU|FE|..."}`  
   响应需含 **`accessToken`**。

2. **`POST ${LINKFOX_TOOL_GATEWAY}/spApi/developerProxy`**  
   Body 字段（与 listings / pricing 系列一致）：
   - **`region`**：与 storeTokens 相同。
   - **`path`**：Amazon SP-API 相对 path，**无**前导 `/`。
   - **`method`**：`GET` | `POST` | `PATCH`。
   - **`amzAccessToken`**：上一步的 access token。
   - **`queryString`**（可选）：URL 查询串，不含 `?`。
   - **`body`**（POST/PATCH）：JSON 字符串。
   - **`contentType`**：如 `application/json`。

环境变量：

- **`LINKFOX_AGENT_API_KEY`**（或 **`LINKFOXAGENT_API_KEY`**，必填）：网关鉴权。（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）
- **`LINKFOX_TOOL_GATEWAY`**（或 `STORE_API_BASE_URL` / `SPAPI_BASE_URL`，可选）：默认 `https://tool-gateway.linkfox.com`。

---

## 2. 脚本与 path / method 对照

| 脚本 | method | path 模板 |
|------|--------|-----------|
| `search_orders.py` | GET | `orders/2026-01-01/orders` |
| `get_order.py` | GET | `orders/2026-01-01/orders/{orderId}` |
| `get_order_buyer_info.py` | GET | `orders/v0/orders/{orderId}/buyerInfo` |
| `get_order_address.py` | GET | `orders/v0/orders/{orderId}/address` |
| `get_order_items.py` | GET | `orders/v0/orders/{orderId}/orderItems` |
| `get_order_items_buyer_info.py` | GET | `orders/v0/orders/{orderId}/orderItems/buyerInfo` |
| `update_shipment_status.py` | POST | `orders/v0/orders/{orderId}/shipment` |
| `get_order_regulated_info.py` | GET | `orders/v0/orders/{orderId}/regulatedInfo` |
| `update_verification_status.py` | PATCH | `orders/v0/orders/{orderId}/regulatedInfo` |
| `confirm_shipment.py` | POST | `orders/v0/orders/{orderId}/shipmentConfirmation` |

`orderId` 在 path 中经 **percent-encoding**（与 listings SKU 处理一致）。

---

## 3. 各脚本 JSON 入参

### 3.1 公共字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sellerId | string | 是 | 卖家 ID |
| region | string | 是 | NA / EU / FE 等与 auth 一致 |
| skipDepCheck | boolean | 否 | 为 true 时跳过本地依赖探测 |

### 3.2 `search_orders.py`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| marketplaceIds | string[] | 是 | 站点 ID 列表，长度 ≤ 50（以 Amazon 为准） |
| createdAfter | string | 条件 | ISO 8601；与 `lastUpdatedAfter` **二选一** |
| createdBefore | string | 否 | 与 `createdAfter` 同组使用 |
| lastUpdatedAfter | string | 条件 | ISO 8601；与 `createdAfter` **二选一** |
| lastUpdatedBefore | string | 否 | 与 `lastUpdatedAfter` 同组使用 |
| fulfillmentStatuses | string[] | 否 | 如 PENDING、UNSHIPPED、SHIPPED、CANCELLED 等 |
| fulfilledBy | string[] | 否 | MERCHANT、AMAZON |
| maxResultsPerPage | number | 否 | 1～100，默认 100 |
| paginationToken | string | 否 | 上一页响应 **`nextToken`** |
| includedData | string[] | 否 | BUYER、RECIPIENT、PROCEEDS、FULFILLMENT、PACKAGES 等（见 [searchOrders](https://developer-docs.amazon.com/sp-api/reference/searchorders)） |

脚本会在 stdout 的 JSON 中解析 **`searchOrders`**（当 `developerProxy.errcode==200` 且 `httpStatus==200` 时由 `body` JSON 解析）。

### 3.3 `get_order.py`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderId | string | 是 | 亚马逊订单号 |
| includedData | string[] | 否 | 同官方 `includedData` |

解析字段：**`order`**。

### 3.4 `get_order_buyer_info.py` / `get_order_address.py`

| 字段 | 类型 | 必填 |
|------|------|------|
| orderId | string | 是 |

解析字段：**`buyerInfo`** / **`shippingAddress`**（以实际 JSON 为准）。

### 3.5 `get_order_items.py` / `get_order_items_buyer_info.py`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderId | string | 是 | |
| nextToken | string | 否 | 映射为查询参数 **`NextToken`** |

解析字段：**`orderItems`** / **`orderItemsBuyerInfo`**。

### 3.6 `update_shipment_status.py`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderId | string | 是 | |
| marketplaceId | string | 是 | |
| shipmentStatus | string | 是 | ReadyForPickup、PickedUp、RefusedPickup |
| orderItems | object[] | 否 | 部分更新时的行项目 |

成功时 Amazon 常返回 **HTTP 204**，stdout 中 **`developerProxy`** 含状态即可，未必有 JSON body。

### 3.7 `get_order_regulated_info.py`

仅需 **`orderId`**。解析字段：**`regulatedOrder`**。

### 3.8 `update_verification_status.py`

| 方式 | 说明 |
|------|------|
| `regulatedOrderVerificationStatus` | 对象，脚本包装为 `{ "regulatedOrderVerificationStatus": ... }` |
| `requestBody` | 整包 PATCH body 对象 |

成功可能为 **204**。

### 3.9 `confirm_shipment.py`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| requestBody | object | 是 | 与官方 **confirmShipment** schema 一致 |

成功可能为 **204**。

---

## 4. 响应与错误

- 脚本统一输出 JSON：`developerProxy` 为网关原样；部分脚本增加 **`resolvedPath`**、**`queryString`**、**`requestBody`**。
- 优先阅读 **`developerProxy.errcode`**、**`developerProxy.httpStatus`**，再读 **`developerProxy.body`**（常为 Amazon 错误 JSON）。
- **429**：需降频重试；searchOrders 默认速率较低。
- HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。
- HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。

---

## 5. 受限数据与 deprecated

- **getOrderBuyerInfo / getOrderAddress / getOrderItems / getOrderItemsBuyerInfo** 在官方文档中标记为 **deprecated**；敏感数据需 **RDT** 与数据保护策略，见 [Tokens API](https://developer-docs.amazon.com/sp-api/reference/createrestricteddatatoken) 与 Orders 文档说明。
- **getOrderRegulatedInfo** 的 `Accept` 等头若需特化，取决于网关是否支持透传；当前脚本未附加额外 Amazon 请求头。
