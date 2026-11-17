---
name: linkfox-1688-procurement
description: 协助当前用户完成已授权的 1688 采购履约流程，包括授权检查、SKU/地址查询、订单预览、下单、支付、订单和物流跟踪等。

# 1688采购全流程（1688 Procurement Workflow）

本技能帮助 LinkFox 用户完成已授权的 1688 采购履约：OAuth 授权检查、SKU 与收货地址查询、下单预览、受保护的下单、支付链接获取、订单与物流跟踪、取消订单、确认收货。图搜找货使用 `linkfox-1688-search-by-image`，本技能不含图搜。端点与字段详见 [references/api.md](references/api.md)，多步采购前先读 [references/workflow.md](references/workflow.md)。

## 能力边界

### ✅ 能力范围

- 查询当前 LinkFox 用户的 1688 OAuth 授权状态、发起授权链接。
- 查询商品 SKU/规格、收货地址，进行下单预览（价格、运费、库存、地址）。
- 在用户单独中文确认后执行高风险写操作：创建订单、获取支付链接、取消订单、确认收货。
- 查询订单状态、物流概览与物流轨迹。

### ❌ 边界与限制

- **图搜不在范围**：以图搜图使用 `linkfox-1688-search-by-image`，本技能不包含图搜脚本。
- **授权前置**：除 `authorize_url.py` 和 `authorized_stores.py` 外，每个采购操作调用目标 endpoint 前都会先检查当前用户 ACTIVE 且未过期的 1688 授权；无授权时不调用目标 endpoint。
- **非自动化闭环**：视作流程地图而非全自动执行；不因"继续""可以"等前文措辞自动创建订单、获取支付链接、取消订单或确认收货。
- **回调端点不暴露**：`/alibaba1688/proxy/callback`、`/alibaba1688/authorizeCallback`、浏览器 OAuth 回调 URL 不作为 Skill 能力。
- **不索要凭据**：不向用户索要 1688 token、refresh token、callback code、app secret；token 闭环由 MyERP/ecom-plat 后端完成。
- **不查后端库**：不查后端库判断授权状态，使用 `authorizedStores`。
- **不自动重试**：高风险写操作失败不自动重试；不使用 `_dataQuery_executeDynamicQuery` 获取实时采购响应。
- **MCP 与 HTTP 分离**：MCP 启停只控制 MCP 暴露；脚本直连 tool-gateway HTTP route，彻底停用需关 route 或后端能力。
- **成本约束**：调用消耗积分；失败、空结果、参数不全或授权不足时不自动连续试探或轮询，继续查询前先向用户说明会产生额外消耗。

## 执行流程

采购流程按步骤协助用户完成，不能一次性自动执行完整下单闭环。每一步均不可跳过授权前置与高风险确认。

### 步骤 1：授权检查

- 【输入】当前 LinkFox 用户身份（来自 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY`）。
- 【动作】运行 `authorized_stores.py`，检查是否存在 `status=ACTIVE` 且 `expired=false` 的 1688 授权。
- 【输出】有 ACTIVE 授权 → 可继续采购；无 ACTIVE 授权 → 进入步骤 2。浏览器跳到 MyERP 登录页不等于授权失败，以脚本返回为准。

### 步骤 2：发起授权（仅未授权时）

- 【输入】当前用户身份。
- 【动作】运行 `authorize_url.py` 获取 1688 授权链接，让用户在浏览器完成 OAuth；完成后重新运行 `authorized_stores.py` 验证。
- 【输出】ACTIVE 授权账号出现 → 回到步骤 1 确认后继续。不要让用户提供 token、refresh token 或 callback code。

### 步骤 3：SKU 与收货地址查询

- 【输入】`offerId`（用户提供，或从 `linkfox-1688-search-by-image` 结果获得）。
- 【动作】运行 `sku.py` 查 SKU/规格、价格、起订量、库存；运行 `receive_address_list.py` 查当前用户 1688 收货地址。
- 【输出】SKU、规格、价格、起订量、库存；收货人、手机/电话、省市区详细地址、`addressId`。多地址时让用户明确选择，不猜测默认地址。

### 步骤 4：下单预览

- 【输入】`offerId`、SKU/规格、数量、收货地址、schema 要求的其他交易字段。
- 【动作】运行 `order_preview.py`。
- 【输出】商品/offerId、SKU/规格、数量、单价与商品总价、运费、收货地址、订单总额、买家留言、异常/库存/价格变化提示。预览失败 → 停止，不进入创建订单，向用户说明并重新确认参数。

### 步骤 5：创建订单（高风险）

- 【输入】预览通过的下单参数、用户对本次订单的单独中文确认（如"确认创建这个订单"）。
- 【动作】用户单独确认后，Agent 在 payload 中自动加入 JSON boolean `confirmCreateOrder=true`，运行 `create_order.py`。
- 【输出】订单号与下单结果。`create_order.py` 会本地拒绝缺少 `confirmCreateOrder=true` 的请求。失败不自动重试。

### 步骤 6：获取支付链接（高风险）

- 【输入】订单号、用户对获取该订单支付链接的单独中文确认（如"确认获取支付链接"）。
- 【动作】Agent 在 payload 中自动加入 `confirmGetPaymentUrl=true`，运行 `payment_url.py`。
- 【输出】支付链接。创建订单成功不等于用户同意获取支付链接，必须独立确认。失败不自动重试。

### 步骤 7：订单状态与物流跟踪

- 【输入】订单号（物流轨迹另需物流标识，以 schema 为准）。
- 【动作】按用户请求运行 `order_status.py`、`logistics.py`、`logistics_trace.py`。
- 【输出】订单状态、物流概览、物流轨迹。仍消耗积分，无用户要求时不连续轮询。

### 步骤 8：取消订单（高风险）

- 【输入】`orderId`、取消原因（如 schema 要求）、用户对该订单的单独中文确认（如"确认取消这个订单"）。
- 【动作】先展示 `orderId`、当前订单状态、取消原因、可能的履约或退款影响；用户单独确认后，Agent 在 payload 加入 `confirmCancel=true`，运行 `cancel_order.py`。
- 【输出】取消结果。失败不自动重试，避免重复取消。

### 步骤 9：确认收货（高风险）

- 【输入】`orderId`、用户对确认收货的单独中文确认（如"确认收货"）。
- 【动作】用户查询物流、看到已签收、或问"状态怎么样"都不等于确认收货；用户明确确认后，Agent 在 payload 加入 `confirmReceive=true`，运行 `confirm_receive.py`。
- 【输出】确认收货结果。失败不自动重试，避免重复确认。

## 高风险确认字段

用户侧只需用中文自然语言做单独明确确认，不要要求用户输入英文参数名或 `=true`。Agent 收到中文确认后调用脚本时自动加入对应 JSON boolean 安全字段（必须为 boolean `true`，字符串 `"true"`、数字 `1` 均被本地拒绝）。

| 操作 | 必填字段 |
|---|---|
| `createOrder` | `confirmCreateOrder=true` |
| `paymentUrl` | `confirmGetPaymentUrl=true` |
| `confirmReceive` | `confirmReceive=true` |
| `cancelOrder` | `confirmCancel=true` |

## 调用方式

- **API 端点**：`POST /alibaba1688/{authorizeUrl|authorizedStores|receiveAddressList|sku|orderPreview|createOrder|paymentUrl|orderStatus|logistics|logisticsTrace|confirmReceive|cancelOrder}`（完整参数、响应与错误处理见 [references/api.md](references/api.md)）。
- **Python 脚本**：`python scripts/<script_name>.py '<JSON 参数>' [--inline] [--save] [--no-save]`。
- **Windows 推荐**：`$env:PAYLOAD = '<JSON 参数>'` 后运行 `python scripts/<script_name>.py --payload-env PAYLOAD [--inline] [--save]`。

```powershell
$env:PAYLOAD = "{}"
python scripts/authorized_stores.py --payload-env PAYLOAD --inline
```

**脚本入参方式**：直接传 JSON 字符串、`--payload-env PAYLOAD`、`--payload-file payload.json`；`--inline` 强制全量打印到 stdout；`--save` 强制保存脱敏完整响应；`--no-save` 禁止保存。

**输出策略**：响应体 ≤ 8 KB 默认不落盘，直接把完整脱敏 JSON 打印到 stdout；> 8 KB 默认写入 `<writable-root>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-1688-procurement-<operation>-<timestamp>.json`，stdout 只输出摘要。`<writable-root>` 优先取 `ACPX_WORKSPACES` 第一个工作区，其次当前目录，最后用户目录；`<session>` 取自 `SESSION_ID`，未提供时自动生成；禁止写入 `/tmp`。加 `--save` 或 `LINKFOX_SKILL_SAVE_RESPONSE=1` 强制保存；`--no-save` 或 `LINKFOX_SKILL_NO_SAVE=1` 禁止保存。

**读数据建议**：先看 stdout 摘要判断是否足够；需要完整响应再加 `--save`，之后用 `jq` 或 `ConvertFrom-Json` 从保存的 JSON 按需抽取，避免整份 JSON 进入上下文。

## 展示规则

1. 采购依赖 OAuth 时先展示授权状态；不单凭浏览器跳转判断授权。
2. `authorizedStores` 输出是当前 LinkFox 用户的 1688 授权状态，不要描述成数据库全库账号列表。
3. 永不展示完整 API key、JWT、access token、refresh token、callback code、app secret、session key、Authorization header。
4. 清晰展示下单预览：商品/offerId、SKU/规格、数量、单价、商品总价、运费、收货地址、订单总额、买家留言、警告。
5. 高风险调用前复述精确操作、关键 ID、金额/状态（如可得），请用户中文确认；不要求用户输入内部 boolean 字段。
6. 收货地址展示到足以安全选择即可，避免不必要地重复完整手机号或敏感地址细节。
7. 返回 `costToken` 或等价成本字段时如实展示。

## 用户表达与场景速查

**适用** —— 1688 已授权采购履约：

| 用户说 | 场景 |
|--------|------|
| "查询我的1688授权店铺" / "show my authorized 1688 stores" | 授权检查 |
| "生成1688授权链接" / "authorize my 1688 account" | 发起新授权 |
| "查这个 offerId 的 SKU" | SKU 查询 |
| "查1688收货地址" | 收货地址查询 |
| "帮我预览1688订单" | 下单预览 |
| "确认下单" | 高风险创建订单门 |
| "获取支付链接" | 高风险支付链接门 |
| "查1688订单状态/物流" | 订单跟踪 |
| "取消这个1688订单" | 高风险取消门 |
| "确认收货" | 高风险确认收货门 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题

发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用skill内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个skill并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个skill。

---

# 1688采购流程 API 参考

本文记录 `linkfox-1688-procurement` 的 tool-gateway 调用规范、脚本入口、风险等级和关键字段。具体入参以网关当前 MCP schema 为准。

## 调用规范

- 请求地址：`${LINKFOX_TOOL_GATEWAY}<path>`，默认网关为 `https://tool-gateway.linkfox.com`
- 请求方式：`POST`
- Content-Type：`application/json; charset=utf-8`
- 认证方式：Header `Authorization: <api_key>`
- API key 读取顺序：`LINKFOX_AGENT_API_KEY`，然后 `LINKFOXAGENT_API_KEY`（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）
- User-Agent：`LinkFox-Skill/2.0`
- 透传 Header：`SESSION_ID`、`MODE_ID`、`APP_NAME`
- 超时：150s
- 输出保存：小响应默认不落盘；大响应、`--save` 或 `LINKFOX_SKILL_SAVE_RESPONSE=1` 时保存脱敏完整响应；`--no-save` 或 `LINKFOX_SKILL_NO_SAVE=1` 可禁止保存
- 缓存策略：不做 24h 响应缓存。授权、价格、库存、订单状态和物流以实时返回为准，高风险写操作不得缓存或自动重放。

Windows 推荐使用 `--payload-env` 或 `--payload-file`，避免 shell 转义破坏 JSON。

```powershell
$env:PAYLOAD = "{}"
python scripts/authorized_stores.py --payload-env PAYLOAD --inline
```

## 授权规则

`authorizedStores` 是当前 LinkFox 用户的 1688 OAuth 授权检查入口。它依赖 API key 中的 LinkFox 用户身份，后端应只返回当前用户的授权店铺。

脚本层规则：

- `authorizeUrl` 不做 1688 OAuth 前置检查，因为它用于发起授权。
- `authorizedStores` 不做 1688 OAuth 前置检查，因为它本身就是检查入口。
- 其他采购操作在调用目标 endpoint 前，脚本会先调用 `authorizedStores`。
- 没有 `status=ACTIVE` 且 `expired=false` 的店铺时，脚本返回 `authorization_required`，不会调用目标 endpoint。

这层检查不能替代后端鉴权；后端仍必须按 `Token.uid` 或等价用户身份过滤和校验授权。

## MCP 与 Skill 暴露关系

MCP 工具启停和 Skill HTTP 调用是两层能力：

| 层级 | 控制内容 | 对本 Skill 的影响 |
|---|---|---|
| MCP tool enabled | 是否出现在 MCP 工具列表或 Agent 工具调用面 | 不决定脚本是否能 HTTP 调用 |
| Gateway route enabled | tool-gateway 是否转发对应 HTTP path | 决定脚本是否可用 |
| Backend capability enabled | ecom-plat 是否处理业务 | 决定最终业务是否可用 |

因此，MCP 停用但 gateway route 仍启用时，Skill 脚本可以继续使用。若要完全停用某能力，应关闭 gateway route 或后端能力。

## 禁止作为 Skill 能力的端点

以下是授权闭环或 MyERP/ecom-plat 后端回调路径，不是 MCP 工具，不应写成 Skill 脚本：

- `/alibaba1688/proxy/callback`
- `/alibaba1688/authorizeCallback`
- `/alibaba1688/oauth/callback`

## API 与脚本一览

| 能力 | MCP tool | Path | Script | 风险 | OAuth 前置检查 | 确认字段 |
|---|---|---|---|---|---|---|
| 生成授权链接 | `_alibaba1688_authorizeUrl` | `/alibaba1688/authorizeUrl` | `authorize_url.py` | 低 | 否 | - |
| 查询已授权账号 | `_alibaba1688_authorizedStores` | `/alibaba1688/authorizedStores` | `authorized_stores.py` | 低 | 否 | - |
| 查询收货地址 | `_alibaba1688_receiveAddressList` | `/alibaba1688/receiveAddressList` | `receive_address_list.py` | 低 | 是 | - |
| 查询 SKU | `_alibaba1688_sku` | `/alibaba1688/sku` | `sku.py` | 低 | 是 | - |
| 下单预览 | `_alibaba1688_orderPreview` | `/alibaba1688/orderPreview` | `order_preview.py` | 中 | 是 | - |
| 创建订单 | `_alibaba1688_createOrder` | `/alibaba1688/createOrder` | `create_order.py` | 高 | 是 | `confirmCreateOrder=true` |
| 获取支付链接 | `_alibaba1688_paymentUrl` | `/alibaba1688/paymentUrl` | `payment_url.py` | 高 | 是 | `confirmGetPaymentUrl=true` |
| 查询订单状态 | `_alibaba1688_orderStatus` | `/alibaba1688/orderStatus` | `order_status.py` | 低 | 是 | - |
| 查询物流 | `_alibaba1688_logistics` | `/alibaba1688/logistics` | `logistics.py` | 低 | 是 | - |
| 查询物流轨迹 | `_alibaba1688_logisticsTrace` | `/alibaba1688/logisticsTrace` | `logistics_trace.py` | 低 | 是 | - |
| 确认收货 | `_alibaba1688_confirmReceive` | `/alibaba1688/confirmReceive` | `confirm_receive.py` | 高 | 是 | `confirmReceive=true` |
| 取消订单 | `_alibaba1688_cancelOrder` | `/alibaba1688/cancelOrder` | `cancel_order.py` | 高 | 是 | `confirmCancel=true` |

`_alibaba1688_imageSearch` 由 `linkfox-1688-search-by-image` 独立承担，本 Skill 不包含图搜脚本。

## 入参要点

| 能力 | 关键字段说明 |
|---|---|
| `authorizeUrl` | 按 schema 传授权展示字段；如需账号标签，优先使用 `accountName` |
| `authorizedStores` | 通常无需业务参数；用户身份来自 LinkFox API key |
| `receiveAddressList` | 依赖当前用户 ACTIVE 1688 授权 |
| `sku` | 通常需要 `offerId` |
| `orderPreview` | 通常需要 `offerId`、SKU/规格、数量、收货地址等下单参数 |
| `createOrder` | 下单参数与预览保持一致，并必须加 `confirmCreateOrder=true` |
| `paymentUrl` | 通常需要订单号，并必须加 `confirmGetPaymentUrl=true` |
| `orderStatus` | 通常需要订单号 |
| `logistics` | 通常需要订单号 |
| `logisticsTrace` | 通常需要订单号及物流标识，以 schema 为准 |
| `confirmReceive` | 订单号 + `confirmReceive=true` |
| `cancelOrder` | 订单号、取消原因（如 schema 要求）+ `confirmCancel=true` |

## 高风险校验

用户侧只需要用中文自然语言做单独明确确认，例如“确认创建这个订单”“确认获取这个订单的支付链接”“确认取消这个订单”“确认收货”。不要要求用户输入英文参数名或 `=true`。

Agent 在收到中文确认后，调用脚本时必须自动加入对应 JSON boolean 安全字段。高风险脚本会在本地先校验确认字段，确认字段不满足时不会联网：

| 脚本 | 本地拒绝条件 |
|---|---|
| `create_order.py` | 缺少 JSON boolean `confirmCreateOrder=true` |
| `payment_url.py` | 缺少 JSON boolean `confirmGetPaymentUrl=true` |
| `confirm_receive.py` | 缺少 JSON boolean `confirmReceive=true` |
| `cancel_order.py` | 缺少 JSON boolean `confirmCancel=true` |

字符串 `"true"`、数字 `1`、大小写变体都不算确认。

## 响应与错误处理

- HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。
- HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。
- `authorization_required`：没有当前用户 ACTIVE 1688 OAuth 授权；先运行 `authorize_url.py`，用户授权后再运行 `authorized_stores.py` 验证。
- 下单预览失败：停止，不要进入创建订单；向用户说明失败原因并重新确认参数。
- 高风险写操作失败：不要自动重试，避免重复下单、重复取消或重复确认收货。

## 敏感信息规则

脚本会对常见敏感字段做脱敏落盘。Agent 展示结果时仍需避免暴露：

- LinkFox API key / JWT
- 1688 access token / refresh token
- Authorization header
- OAuth callback `code`
- app secret / session key / refresh secret

---

# 1688采购流程地图

本文档是流程地图，不是自动化脚本。Agent 可以按步骤协助用户完成采购，但不能一次性自动执行完整下单闭环。

## 总原则

1. 采购业务先查授权，再查商品和地址，再预览，再让用户确认。
2. 图搜找货使用 `linkfox-1688-search-by-image`，本 Skill 只处理采购履约。
3. 除 `authorizeUrl` 和 `authorizedStores` 外，脚本会在每个采购 endpoint 前自动检查当前用户 ACTIVE 授权。
4. 下单、支付链接、取消订单、确认收货都是独立高风险动作，各自需要单独确认。
5. 用户前面说过"继续""可以""按上面来"，不能作为后续高风险动作的确认。

## 1. 授权检查

运行：

```powershell
$env:PAYLOAD = "{}"
python scripts/authorized_stores.py --payload-env PAYLOAD --inline
```

判断：

- 有 `status=ACTIVE` 且 `expired=false`：可以继续采购流程。
- 没有 ACTIVE 授权：进入授权步骤。
- 浏览器最后跳到 MyERP 登录页不等于授权失败；以 `authorized_stores.py` 返回为准。

`authorizedStores` 应只返回当前 LinkFox API key 对应用户的授权店铺。不要把它理解为后台全库账号列表。

## 2. 发起授权

运行 `authorize_url.py` 获取 1688 授权链接，并让用户在浏览器打开。

用户完成授权后，再运行 `authorized_stores.py` 验证是否出现 ACTIVE 账号。

不要让用户提供 1688 token、refresh token 或 callback code。授权 token 保存由 MyERP/ecom-plat 后端闭环完成。

## 3. 找货与 SKU

如果用户按图片找货：

1. 切换到 `linkfox-1688-search-by-image`。
2. 从图搜结果中选择目标 `offerId`。
3. 回到本 Skill，用 `sku.py` 查询 SKU/规格。

如果用户已提供 `offerId`：

1. 直接运行 `sku.py`。
2. 展示 SKU、规格、价格、起订量、库存等关键字段。
3. 让用户选择明确的 SKU 和数量。

## 4. 收货地址

运行 `receive_address_list.py` 查询当前用户可用的 1688 收货地址。

展示地址时应包含：

- 收货人
- 手机/电话（如返回）
- 省市区与详细地址
- `addressId` 或等价标识

不要猜测默认地址。多地址时让用户明确选择。

## 5. 下单预览

运行 `order_preview.py` 前确认已具备：

- `offerId`
- SKU/规格
- 数量
- 收货地址
- schema 要求的其他交易字段

预览结果必须先展示给用户：

- 商品/offerId
- SKU/规格
- 数量
- 单价与商品总价
- 运费
- 收货地址
- 订单总额
- 任何异常、库存或价格变化提示

预览失败时停止，不要进入创建订单。

## 6. 创建订单

创建订单是高风险动作。必须先询问用户是否确认创建该订单，并复述预览摘要。用户只需要中文自然语言确认，例如"确认创建这个订单"；不要要求用户输入 `confirmCreateOrder=true`。

只有用户针对本次订单明确确认后，Agent 才在脚本 payload 中自动加入：

```json
{
  "...": "order payload",
  "confirmCreateOrder": true
}
```

`create_order.py` 会拒绝缺少 `confirmCreateOrder=true` 的请求。

## 7. 获取支付链接

获取支付链接也是独立高风险动作。创建订单成功不等于用户同意获取支付链接。用户只需要中文自然语言确认，例如"确认获取支付链接"；不要要求用户输入 `confirmGetPaymentUrl=true`。

用户单独确认后，Agent 在脚本 payload 中自动加入：

```json
{
  "orderId": "...",
  "confirmGetPaymentUrl": true
}
```

## 8. 订单状态与物流

查询类动作可在用户请求时执行：

- `order_status.py`
- `logistics.py`
- `logistics_trace.py`

这些仍然会消耗积分。不要在没有用户要求的情况下连续轮询。

## 9. 取消订单

取消订单是高风险动作。执行前展示：

- `orderId`
- 当前订单状态
- 取消原因
- 可能的履约或退款影响（如响应中可判断）

只有用户针对该订单明确确认取消后，Agent 才运行 `cancel_order.py`，并在脚本 payload 中自动加入：

```json
{
  "orderId": "...",
  "confirmCancel": true
}
```

## 10. 确认收货

确认收货是高风险动作。用户查询物流、看到已签收、或问"状态怎么样"，都不等于确认收货。

只有用户明确确认收货后，Agent 才运行 `confirm_receive.py`，并在脚本 payload 中自动加入：

```json
{
  "orderId": "...",
  "confirmReceive": true
}
```

## MCP 与 Skill 分离

MCP 停用只表示该工具不再通过 MCP 工具列表暴露。只要 tool-gateway 对应 HTTP route 仍启用，本 Skill 的脚本仍可通过 HTTP 调用。

如果需要彻底禁用某个采购能力，需要关闭对应 gateway route 或后端能力，而不是只从 MCP 列表移除。
