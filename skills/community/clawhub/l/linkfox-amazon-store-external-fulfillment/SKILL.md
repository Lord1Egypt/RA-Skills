---
name: linkfox-amazon-store-external-fulfillment
description: 亚马逊 External Fulfillment 外部履约管理。用于 Seller Flex、FBA Onsite、Easy Ship、Self Ship、MFN Self Delivery 等项目中的按 location 库存查询或更新、履约货件处理、包裹与状态更新、配送选项、面单、发票和退货查询。用户提到 External Fulfillment、SmartConnect、Seller Flex、FBA Onsite、Easy Ship、Self Ship、batchInventory、location 库存、外部履约 shipment、EF 面单、EF 发票或 EF 退货时触发。即使未明确说“External Fulfillment API”，只要需求围绕这些外部履约项目的库存、货件、包裹或退货，也应触发此技能；普通卖家订单使用 linkfox-amazon-store-orders，FBA/MCF 使用对应 fulfillment 技能。
---

# Amazon 店铺 External Fulfillment

本 skill 与 **`linkfox-amazon-store-auth`** 等同属 **Amazon Store** 系列：依赖 **`linkfox-amazon-store-auth`** 选店（`sellerId`+`region`）；直接 **`POST /spApi/developerProxy`** 传入 `sellerId`+`region`，由服务端解析 token（勿传 `amzAccessToken`，除非兼容旧调用）。转发上游 **`GET` / `POST` / `PUT` / `PATCH`**。

适用渠道：Seller Flex / FBA Onsite、Multi Seller Flex、Easy Ship、Self Ship、MFN Self Delivery、Amazon Pharmacy 等（以商家 allowlist 与角色为准）。

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（完整参数/响应见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；失败/空结果不得自动翻页或连续试探；需要继续时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-external-fulfillment-<timestamp>.json`
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要
- 加 `--inline` 强制全量打印（同样落盘）

**读数据建议**：先看摘要；需要具体字段时用 `jq` / `ConvertFrom-Json` 从落盘文件抽取。

## 解决认证和算力问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或余额不足**：消息含"算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## 官方参考索引

| 模块 | 能力 | 文档 |
|------|------|------|
| Inventory | batchInventory | [batchInventory](https://developer-docs.amazon.com/sp-api/reference/batchinventory) |
| Shipping | getShipments | [getShipments](https://developer-docs.amazon.com/sp-api/reference/getshipments-1) |
| Shipping | getShipment | [getShipment](https://developer-docs.amazon.com/sp-api/reference/getshipment-1) |
| Shipping | processShipment | [processShipment](https://developer-docs.amazon.com/sp-api/reference/processshipment) |
| Shipping | createPackages | [createPackages](https://developer-docs.amazon.com/sp-api/reference/createpackages) |
| Shipping | updatePackage | [updatePackage](https://developer-docs.amazon.com/sp-api/reference/updatepackage) |
| Shipping | updatePackageStatus | [updatePackageStatus](https://developer-docs.amazon.com/sp-api/reference/updatepackagestatus) |
| Shipping | retrieveShippingOptions | [retrieveShippingOptions](https://developer-docs.amazon.com/sp-api/reference/retrieveshippingoptions) |
| Shipping | generateInvoice | [generateInvoice](https://developer-docs.amazon.com/sp-api/reference/generateinvoice) |
| Shipping | retrieveInvoice | [retrieveInvoice](https://developer-docs.amazon.com/sp-api/reference/retrieveinvoice) |
| Shipping | generateShipLabels | [generateShipLabels](https://developer-docs.amazon.com/sp-api/reference/generateshiplabels) |
| Returns | listReturns | [listReturns](https://developer-docs.amazon.com/sp-api/reference/listreturns) |
| Returns | getReturn | [getReturn](https://developer-docs.amazon.com/sp-api/reference/getreturn) |

---

## Prerequisites（必须先读）

本 skill **依赖** **`linkfox-amazon-store-auth`**。

1. 运行 `python scripts/check_auth_dependency.py`；若 exit code **42** 且 stderr 含 `DEPENDENCY_MISSING:`，请先安装 **`linkfox-amazon-store-auth`**。
2. **不要**在本 skill 内绕过依赖实现授权或令牌逻辑。
3. 商家需 **External Fulfillment allowlist**，应用需 **Direct-to-Consumer Shipping (Restricted)** 角色。

---

## Current Capabilities（脚本一览）

| 能力 | developerProxy `path`（要点） | 脚本 |
|------|------------------------------|------|
| batchInventory | `externalFulfillment/inventory/2024-09-11/inventories`，POST | `post_batch_inventory.py` |
| getShipments | `externalFulfillment/2024-09-11/shipments` + Query | `get_shipments.py` |
| getShipment | `.../shipments/{shipmentId}` | `get_shipment.py` |
| processShipment | `.../shipments/{shipmentId}?operation=`，POST | `process_shipment.py` |
| createPackages | `.../shipments/{shipmentId}/packages`，POST | `create_packages.py` |
| updatePackage | `.../shipments/{shipmentId}/packages/{packageId}`，PUT | `update_package.py` |
| updatePackageStatus | 同上 path，PATCH | `update_package_status.py` |
| retrieveShippingOptions | `.../shipments/{shipmentId}/shippingOptions` + packageId | `retrieve_shipping_options.py` |
| generateInvoice | `.../shipments/{shipmentId}/invoice`，POST | `generate_invoice.py` |
| retrieveInvoice | 同上 path，GET | `retrieve_invoice.py` |
| generateShipLabels | `.../shipments/{shipmentId}/shipLabels?operation=`，PUT | `generate_ship_labels.py` |
| listReturns | `externalFulfillment/2024-09-11/returns` + Query | `list_returns.py` |
| getReturn | `.../returns/{returnId}` | `get_return.py` |

共享逻辑见 **`scripts/_spapi_ef_common.py`**（仅供同目录脚本 import）。

---

## Quick Parameters（摘要）

- **batchInventory**：`requests` 1～10 条。简化项：`action`=`fetch`|`update`、`locationId`、`skuId`；update 必填 `quantity`。MFN 单仓常用 `locationId=DEFAULT`；Seller Flex 用 4 位仓码。高级：`useAmazonRequestShape:true` 直传官方 `requests`。
- **getShipments**：必填 `status`（如 `ACCEPTED`/`CREATED`）；可选 `locationId`、`marketplaceId`、`channelName`、`lastUpdatedAfter/Before`、`maxResults`、`paginationToken`。
- **processShipment**：`operation`=`CONFIRM`|`REJECT`；REJECT 时可传 `referenceId`/`lineItems` 或 `requestBody`。
- **createPackages / updatePackage**：包裹尺寸重量与 `packageLineItems` 按官方 schema 放在 `packages` 或 `requestBody`。
- **updatePackageStatus**：主要用于 Self Delivery；传 `status`/`subStatus`/`reason`。
- **generateShipLabels**：`operation`=`GENERATE`|`REGENERATE`；可选 `shippingOptionId`、`packageIds`。
- **listReturns**：可选 `status`（新退货常用 `CREATED`）、`returnLocationId`、时间窗、`nextToken`。

典型履约流程：`getShipments` → `processShipment(CONFIRM)` → `createPackages` → `retrieveShippingOptions` → `generateInvoice` → `generateShipLabels` →（Self Delivery）`updatePackageStatus`。

---

## Scripts

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/post_batch_inventory.py '{"sellerId":"A1...","region":"NA","requests":[{"action":"fetch","locationId":"DEFAULT","skuId":"SKU-1","marketplaceAttributes":{"marketplaceId":"ATVPDKIKX0DER","channelName":"MFN"}}]}'

python scripts/get_shipments.py '{"sellerId":"A1...","region":"NA","status":"ACCEPTED","locationId":"ABCD"}'

python scripts/process_shipment.py '{"sellerId":"A1...","region":"NA","shipmentId":"...","operation":"CONFIRM"}'
```

---

## Display Rules

1. 先看网关 **`developerProxy.errcode` / `httpStatus`**，再解析脚本附加字段（如 **`batchInventory`**、**`shipments`**、**`invoice`**）。
2. **batchInventory** 成功时常为 **207** Multi-Status；逐条看 `responses[].status`。
3. 多数写操作成功可能为 **204**（无 body）；stdout 会标 `success: true`。
4. 发票/面单文档多为 Base64 或预签名 URL，勿把整段大 base64 反复贴进上下文。
5. **路径白名单**：若返回 **1005**，需后端放行 **`externalFulfillment/`** 前缀。

---

## Important Limitations

- 权限：**Direct-to-Consumer Shipping (Restricted)**；商家需 allowlist。
- **写库存为绝对值发布**，非增量；只同步有变化的 SKU；SKU 特殊字符需 URL 编码（脚本已处理简化入参）。
- 与 **`linkfox-amazon-store-orders`**（普通 Orders）、**`linkfox-amazon-store-feeds`**（Feed 改库存）、**`linkfox-amazon-store-report`**（库存报告）边界不同，勿混用。
- Seller Flex 上 `retrieveShippingOptions` 常返回空；Easy Ship 全球多数站点可能不支持 `generateInvoice`（印度除外）。
- 返回结构以 Amazon schema 为准；详见 **`references/api.md`**。

## Amazon SP-API 接口保护与重试指引

同一店铺连续收到 Amazon SP-API 的 400、403、404 或 429 时，网关会返回 450、453、454 或 459 并短暂冷却。这些自定义状态码不是 Amazon 原生状态，也不表示封号；目的是避免持续异常或高频调用扩大店铺风险。

| 状态与 message | 范围 | 触发与冷却 | 处理 |
|---|---|---|---|
| `450`：`400，请求异常，请优化您的参数` | 店铺+接口 | 60 秒内超过 3 次：5 分钟；10 分钟内超过 4 次：20 分钟 | 停止原参数重试，检查必填字段、marketplace、ID、日期和请求体 |
| `453`：`403，店铺未授权，请先授权` | 店铺全部接口 | 60 秒内超过 2 次：5 分钟；10 分钟内超过 4 次：30 分钟 | 停止该店铺调用，检查授权、权限、店铺归属和区域 |
| `454`：`404，资源不存在，请优化您的参数` | 店铺+接口 | 60 秒内超过 3 次：5 分钟；10 分钟内超过 4 次：30 分钟 | 确认资源 ID、所属店铺/站点、资源状态和接口路径 |
| `459`：`429限流中，请降低频率` | 店铺+接口 | 首次：15 秒；2 分钟内超过 2 次：30 秒；3 分钟内超过 4 次：2 分钟 | 降低并发、分页和轮询频率并逐级退避 |

- 立即停止自动或并发重试，不得通过换脚本或重复创建任务绕过保护；优先遵循 `retryAfter`、`blockedUntil`，没有时按表中时长说明。
- 450/453/454 必须先修正参数、授权或资源标识，冷却后最多谨慎重试一次；再次触发则停止调用。453 期间停止该店铺全部 SP-API。
- 保留已有 `reportId`、`feedId` 等任务 ID；写操作结果不确定时先查询状态，不直接重放。
- 向用户先说明店铺保护，再给原因、处理和等待时间。可回复：“为保护您的亚马逊店铺安全，检测到 Amazon SP-API 连续返回{原因}，当前已进入短暂保护。请先{处理动作}，预计{等待时间}后再试；这不代表封号，也不是套餐或算力限制。”不要只说“LinkFox 限流”或“服务器繁忙”。

## 算力消耗规则

不消耗算力（以网关实际计费为准；若网关计费则按算力规则处理）。

**Feedback：** 见 `references/api.md`，`skillName`：`linkfox-amazon-store-external-fulfillment`。

---
*更多跨境 skill：[LinkFox Skills](https://skill.linkfox.com/)*
