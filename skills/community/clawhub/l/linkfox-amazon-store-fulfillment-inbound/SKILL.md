---
name: linkfox-amazon-store-fulfillment-inbound
description: 亚马逊 FBA 入仓与 Fulfillment Inbound 全流程管理。用于创建和管理 inbound plan，处理装箱、placement、shipment、货件内容更新、送达窗口、自配送预约、运输方案、商品合规、预处理、箱唛标签、提单及异步操作状态。用户提到 FBA 入库计划、Send to Amazon、创建入仓计划、packing option、placement option、transportation option、货件箱唛、入仓标签、送仓预约、shipmentConfirmationId、createInboundPlan、Fulfillment Inbound API、v2024-03-20 或 v0 入仓接口时触发。即使未明确说“Fulfillment Inbound”，只要希望把库存发往亚马逊运营中心并完成建仓、装箱、分仓、运输或交仓步骤，也应触发此技能。
---

# Amazon 店铺 Fulfillment Inbound

本 Skill 覆盖 Amazon Fulfillment Inbound `v2024-03-20` 的 45 个 operation，以及仍需配合新流程使用的 6 个 `v0` 查询/文档 operation。所有请求继续使用 Amazon Store 系列的生产链路：`POST /spApi/developerProxy`，由服务端通过 `sellerId + region` 解析授权。

## Prerequisites（必须先读）

1. 本 Skill 依赖 **`linkfox-amazon-store-auth`**。先运行 `python scripts/check_auth_dependency.py`；若 exit code 为 `42` 且 stderr 含 `DEPENDENCY_MISSING:`，先安装或加载该依赖。
2. 通过 auth Skill 选定店铺，取得 `sellerId` 与 `region`。`region` 仅允许 `NA`、`EU`、`FE`。
3. 不接收、存储或透传 `amzAccessToken`、`accessToken`、`refreshToken`。不要让调用方覆盖 Amazon `path`、`method` 或网关 `queryString`。
4. 先读与任务匹配的分组文档；完整契约入口见 [references/api.md](references/api.md)。

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<operation_script>.py '<JSON 参数>' [--inline] [--no-cache]`
- **调用约束**：本工具沿用 Amazon Store Skill 的统一免费配置；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换参数、翻页或连续试探；需要继续调用时先征得用户同意。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-fulfillment-inbound-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，`<session>` 取自环境变量 `SESSION_ID`；禁止写入 `/tmp`，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数、最大列表字段长度及前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）
- 加 `--no-cache` 强制本次读/生成操作访问网关；只在用户要求刷新或已确认外部状态变化时使用

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 JSON 文件按需抽取，避免整份 JSON 进入上下文。

## 工作方式

每个公开脚本只代表一个固定 operation，并且一次执行最多调用一次网关。统一执行器负责：

- 校验公共字段、path/query/body、枚举、分页上限和关键嵌套约束；
- 对 path segment 与 query 参数进行百分号编码；
- 将 v0 CLI 的 lowerCamelCase 参数映射为 Amazon 要求的 PascalCase wire 名称；
- 识别 200/201/202/204 成功响应并解析 JSON；
- 对异步响应返回显式 `nextAction`，但不自动轮询；
- 保存完整响应，大响应只在 stdout 展示摘要。

调用格式：

```bash
python scripts/<operation_script>.py '<JSON parameters>' [--inline] [--no-cache]
```

公共参数：

| 参数 | 必填 | 说明 |
|---|---|---|
| `sellerId` | 是 | 已授权 Seller ID |
| `region` | 是 | `NA` / `EU` / `FE` |
| path/query 参数 | 条件 | 使用各 operation 文档中的 lowerCamelCase 名称 |
| `requestBody` | 条件 | Amazon JSON body；推荐显式传此对象，也兼容将 body 字段放在顶层 |
| `confirmWrite` | 提交类操作必填 | 用户明确确认目标和选择后传布尔值 `true`；8 个确定性提交操作缺少该值时脚本会在网关调用前拒绝 |
| `skipDepCheck` | 否 | 仅本地调试使用 |

示例：

```bash
python scripts/get_inbound_plan.py '{"sellerId":"A1...","region":"NA","inboundPlanId":"wf12345678-1234-1234-1234-123456789012"}'

python scripts/create_inbound_plan.py '{"sellerId":"A1...","region":"NA","requestBody":{"destinationMarketplaces":["ATVPDKIKX0DER"],"items":[{"labelOwner":"AMAZON","msku":"SKU-1","prepOwner":"SELLER","quantity":10}],"sourceAddress":{"name":"Warehouse","addressLine1":"1 Main St","city":"Seattle","countryCode":"US","phoneNumber":"+1-206-555-0100","postalCode":"98101","stateOrProvinceCode":"WA"}}}'

python scripts/get_labels.py '{"sellerId":"A1...","region":"NA","shipmentConfirmationId":"FBA...","pageType":"PackageLabel_Letter_2","labelType":"UNIQUE"}'
```

## 选择 operation

| 分组 | 用途 | 详细参数与脚本 |
|---|---|---|
| Inbound Plans | 创建、读取、取消、改名、查看 plan 内容 | [inbound-plans.md](references/apis/inbound-plans.md) |
| Packing | 生成/确认装箱方案、提交箱规、查看 packing group | [packing.md](references/apis/packing.md) |
| Placement | 生成、列出、确认分仓方案 | [placement.md](references/apis/placement.md) |
| Shipments | 读取货件、箱/件/托盘、名称和地址、tracking | [shipments.md](references/apis/shipments.md) |
| Content Updates | 预览并确认已建货件内容变更 | [shipment-content-updates.md](references/apis/shipment-content-updates.md) |
| Delivery | delivery window 与 delivery challan | [delivery-windows-and-documents.md](references/apis/delivery-windows-and-documents.md) |
| Self-Ship | India 自配送预约槽与预约 | [self-ship-appointments.md](references/apis/self-ship-appointments.md) |
| Transportation | 生成、比较、确认运输方案 | [transportation.md](references/apis/transportation.md) |
| Prep / Compliance / Labels | 预处理、合规和商品标签 | [prep-compliance-labels.md](references/apis/prep-compliance-labels.md) |
| Async Status | 查询 `operationId` 的执行状态 | [asynchronous-operations.md](references/apis/asynchronous-operations.md) |
| Retained v0 | prep instructions、箱唛、BOL、旧货件查询 | [legacy-v0.md](references/apis/legacy-v0.md) |

## 执行规则

1. 先确认当前工作流阶段及已有 ID；ID 的来源和跨版本映射见 [references/identifiers.md](references/identifiers.md)。已有 plan/shipment 时优先只读恢复，不重复创建。
2. 写操作前确认用户意图和目标店铺。以下 8 个确定性提交操作必须在执行前向用户展示关键选择并取得明确确认：`cancelInboundPlan`、`confirmPackingOption`、`confirmPlacementOption`、`confirmShipmentContentUpdatePreview`、`confirmDeliveryWindowOptions`、`cancelSelfShipAppointment`、`scheduleSelfShipAppointment`、`confirmTransportationOptions`。
3. `confirmTransportationOptions` 可能接受运输费用；确认前展示每个 shipment 的 option、费用、币种、时效与 expiration。不得替用户默认选择收费项。
4. 19 个异步发起 operation 返回 `operationId` 后，只调用 `get_inbound_operation_status.py` 查询。`IN_PROGRESS` 时停止并告知稍后再查；`FAILED` 时展示 `operationProblems`，不得进入下游写步骤；仅 `SUCCESS` 可继续。
5. 脚本层不自动翻页、轮询、换参数试探或重放 POST/PUT。现有网关仅在识别到 token 过期时会刷新 token 并透明重试一次；429/500/503 或超时造成结果不确定时，优先通过 status/read operation 恢复状态。
6. `updateInboundPlanName`、`updateShipmentName` 的 204 空 body 是成功，不当作解析失败。
7. `getLabels` / `getBillOfLading` 必须使用 `getShipment` 返回的 `shipmentConfirmationId`；脚本同时接受该别名。下载 URL 可能很快过期，应在取得后立即下载，不要长期保存 URL。

完整标准路径、Pack Later、India、自有承运人和 shipment content update 流程见 [references/workflows.md](references/workflows.md)。市场限制见 [references/marketplace-constraints.md](references/marketplace-constraints.md)。

## 输出与错误处理

- 完整响应保存到 `linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-fulfillment-inbound-<timestamp>.json`；stdout 会打印实际路径。
- 响应不超过 8 KB 时打印完整 JSON；更大时打印摘要；`--inline` 强制打印完整 JSON。
- 始终先判断 `developerProxy.errcode`，再判断 `httpStatus`，最后读取 operation 结果字段。
- 401/402、API Key、授权、算力或余额问题按 [references/onboarding.md](references/onboarding.md) 处理。
- Amazon 返回 400/403/404/409/413/415/422 时，修正输入或流程状态后由用户决定是否再次调用。

## 参考路由

- 字段、响应、分页、错误语义：读 [references/api.md](references/api.md)。
- 业务流程选择：读 [references/workflows.md](references/workflows.md)。
- ID 产生和 v2024/v0 映射：读 [references/identifiers.md](references/identifiers.md)。
- 国家/市场差异：读 [references/marketplace-constraints.md](references/marketplace-constraints.md)。
- 某个 operation 的 method/path/body/script：只读对应的 `references/apis/*.md` 分组文档。

问题反馈使用 `skillName: linkfox-amazon-store-fulfillment-inbound`，并附脱敏后的 operation、关联 ID 与 `developerProxy` 响应。

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

不消耗算力（以网关实际计费为准）。

---
*更多跨境 Skill：[LinkFox Skills](https://skill.linkfox.com/)*
