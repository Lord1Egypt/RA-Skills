---
name: linkfox-shopee-store-auth
description: Shopee（虾皮）店铺授权与管理技能，支持 ERP 与广告（AD）双应用分开授权。提供授权流程、已授权店铺查询以及授权状态读取。授权时可填写店铺名 shopName，region 支持 cn / global / br，appType 支持 erp / ad。当用户提到 Shopee 店铺授权、虾皮店铺绑定、ERP 授权、广告授权、appType、查询已授权 Shopee 店铺、Shopee seller authorization, bind Shopee shop, Shopee Ads authorization 时触发。即使未明确提及"Shopee"或"授权"，只要涉及虾皮卖家账号绑定、ERP/广告应用授权或店铺列表查询，也应触发。
---

# Shopee 店铺授权与管理

Shopee Open Platform 的 OAuth 授权、已授权店铺列表、授权状态读取。**下游业务的前置依赖**（经 `/shopee/developerProxy` 调用开放接口）。

Shopee **ERP** 与 **广告（AD）** 使用不同应用与 Token，必须按能力分开授权。

## Core Concepts

- **双应用**：`appType=erp`（商品/订单/物流等，默认）与 `appType=ad`（站内广告）彼此独立；同店可同时有两条授权
- **授权流程**：生成 URL → 用户浏览器授权 → Shopee 推送 Token → 系统按 `state` 落库
- **店铺标识**：`shopId` 与 `merchantId` 二选一即可定位；判断是否已授权须同时匹配 **`shopId/merchantId + appType`**
- **shopName 建议填写**：调 `authorize_url.py` 前建议问用户要一个便于识别的店铺名（API 非必填）
- **授权 URL 1 小时有效**：每次授权重新调用 `authorize_url.py`，不要缓存旧地址
- **下游选店**：业务 skill 经 `developerProxy` 只传 **`shopId`/`merchantId` + path**；**勿**传 `accessToken`，也**勿**在 proxy 里传 `appType`（服务端按 path 自动路由：`api/v2/ads/**` → AD，其它 `api/v2/**` → ERP）
- **accessToken 约 4 小时有效**（`expireIn` 通常 14400）；过期需按对应 `appType` 重新授权

## Shopee authorization routing

- Use `appType=erp` for product, order, logistics, and other ERP authorization.
- Use `appType=ad` for Shopee Ads authorization.
- Treat a missing or blank `appType` as `erp`.
- Check authorization by both store identity and `appType`; one store may have separate ERP and AD records.
- If the user needs both capabilities, obtain two fresh authorization URLs and explain that both authorizations must be completed.
- Authorization URLs expire after one hour, so obtain a new URL for every authorization attempt.

When calling `developerProxy`, pass the Shopee API path plus `shopId` or `merchantId`. Do not pass `appType` or an access token. The service routes `api/v2/ads/**` through the AD application and all other `api/v2/**` paths through the ERP application.

## 可用脚本

| 脚本 | 作用 |
|------|------|
| `authorize_url.py` | 生成授权 URL（可选 `shopName` / `region` / **`appType`**） |
| `authorized_stores.py` | 列出已授权店铺（含 **`appType`**；同店可能两条） |
| `store_tokens.py` | 查指定应用的授权/令牌**状态**（非下游 token 来源；须带 `appType` 区分） |

入参、响应字段、错误码见 `references/api.md`。

## 调用方式

- **API 端点**：`POST /shopee/{authorizeUrl|storeTokens|authorizedStores}`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见上文）
- **成本约束**：本工具会消耗积分；失败/空结果不得自动连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/<skill-name>-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和积分问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## 支持区域

`cn`（中国跨境，默认） / `global`（全球授权页） / `br`（巴西）。默认 `cn`。

## Usage Scenarios

### 1. 新授权店铺（ERP，默认）

1. 建议问用户要 `shopName`（便于后续识别；API 非必填）
2. 确认 `region`（默认 `cn`；全球站 `global`，巴西 `br`）
3. 调 `authorize_url.py`，传 **`appType=erp`**（或不传，服务端默认 erp）→ 给用户在浏览器打开（安全警告：为保障店铺安全，请务必在日常运营该店铺的安全网络环境中打开此链接。强烈建议使用紫鸟浏览器等专业的防关联浏览器进行授权，切勿在陌生或公共网络下操作。）
4. 授权完成后系统自动存 token；浏览器跳转成功/失败页
5. 调 `authorized_stores.py`，确认存在 **`appType=erp`**（或空，历史记录视为 erp）的记录

### 2. 广告应用授权（AD）

1. 调 `authorized_stores.py`，检查目标店是否已有 **`appType=ad`**
2. 未授权时调 `authorize_url.py`，传 **`appType=ad`**，并明确告知用户这是**广告应用**授权（与 ERP 无关）
3. 授权完成后再次检查 `appType=ad`
4. **禁止**用 ERP 授权代替广告授权

### 3. 同时需要 ERP 与广告

1. 分别检查 `appType=erp` 与 `appType=ad`
2. 仅为缺失的应用生成授权地址；两项都缺则生成**两个** URL，并标注用途
3. 提示用户需分别打开并完成两次授权；一次授权不会覆盖另一项能力

### 4. 列已授权店铺

调 `authorized_stores.py`，展示 `shopName / shopId / merchantId / region / **appType**`。同店可能出现 ERP、AD 两条。

### 5. 给下游准备店铺选店信息（高频）

用户只说自然语言（"我的虾皮店"、"67890 那家店"），**不要让用户报冗长 token**。

| 用户上下文 | Agent 动作 |
|---|---|
| 只授权 1 家店铺（且目标能力已授权） | 直接取该店铺 `shopId`（或 `merchantId`），不问 |
| 授权 ≥ 2 家 + 只说店名 | 按 `shopName` 向用户澄清 |
| 同时给出 shopName 或 shopId | 直接定位 |
| 显式给出 shopId / merchantId | 直接用 |
| 店铺在列表中存在但缺少目标 `appType` | 按能力发起对应授权，**不要**调用业务接口 |

**静默原则**：定位成功时只确认店铺标识与应用类型，不向用户索要 token。

**推荐流程**：`authorized_stores.py` 按 **`shopId + appType`** 确认已授权 → 下游 skill 直接 `POST /shopee/developerProxy` 传入 `shopId`（或 `merchantId`），由服务端按 path 解析对应应用 token。

`store_tokens.py` **仅用于**确认授权/令牌状态（须传 `appType`），**不要**为 proxy 调用先取 `accessToken`。

## 调用原则

- 授权前建议确认 `shopName`、`region`、**`appType`**
- 不假设 `storeTokens` 响应含 raw `accessToken`；展示状态与过期元数据即可
- 授权失败按错误码解释原因；不擅自重试
- 令牌过期须按对应 `appType` 重新走授权流程
- 历史空 `app_type` 视为 ERP，不是 AD

## 常见问题

### 授权完成但查不到店铺

原因：Token 推送回调（`/shopee/oauth/tokenCallback`）未成功落库，或 `state` 不匹配。
解决：查看服务日志；重新调 `authorize_url.py`（勿复用过期 URL）完成授权。

### 查令牌 / 业务调用返回 1004

原因：`shopId` / `merchantId` 错误，或**目标应用**未授权（例如只有 ERP、没有 AD）。
解决：先调 `authorized_stores.py` 核对 `shopId + appType`；缺则按能力重新授权。

### 店铺已授权但广告 API 失败

原因：有 ERP 记录 ≠ 有 AD 记录；广告不能使用 ERP Token。
解决：发起 `appType=ad` 授权后再调 `linkfox-shopee-store-ads`。

## Not Applicable

- **Shopee 订单查询与处理** → `linkfox-shopee-store-orders`
- **Shopee 店铺信息与设置** → `linkfox-shopee-store-shop`
- **Shopee 店铺商品 listing** → `linkfox-shopee-store-product`
- **Shopee 跨境全球商品 GlobalProduct** → `linkfox-shopee-store-global-product`
- **Shopee 跨境商户信息 Merchant** → `linkfox-shopee-store-merchant`
- **Shopee 物流发货 Logistics** → `linkfox-shopee-store-logistics`
- **Shopee 退货退款 Returns** → `linkfox-shopee-store-returns`
- **Shopee 站内广告 Ads** → `linkfox-shopee-store-ads`（业务调用；授权仍用本 skill 的 `appType=ad`）
- **Shopee 支付结算 Payment** → `linkfox-shopee-store-payment`
- **Shopee 联盟营销 AMS** → `linkfox-shopee-store-ams`
- **Shopee 店铺视频 Video** → `linkfox-shopee-store-video`
- **Shopee 媒体上传 MediaSpace** → `linkfox-shopee-store-media-space`
- **Shopee 媒体上传 Media** → `linkfox-shopee-store-media`（`api/v2/media/...`，module=130）
- **Shopee 头程物流 FirstMile** → `linkfox-shopee-store-first-mile`
- **Shopee 折扣促销 Discount** → `linkfox-shopee-store-discount`
- **Shopee 套装优惠 Bundle Deal** → `linkfox-shopee-store-bundle-deal`
- **Shopee 加购优惠 Add-On Deal** → `linkfox-shopee-store-add-on-deal`
- **Shopee 店铺优惠券 Voucher** → `linkfox-shopee-store-voucher`
- **Shopee 店铺秒杀 Shop Flash Sale** → `linkfox-shopee-store-shop-flash-sale`
- **Shopee 关注有礼 Follow Prize** → `linkfox-shopee-store-follow-prize`
- **Shopee 精选商品 Top Picks** → `linkfox-shopee-store-top-picks`
- **Shopee 店铺分类 Shop Category** → `linkfox-shopee-store-shop-category`
- **Shopee 账户健康 Account Health** → `linkfox-shopee-store-account-health`
- **Shopee Public 公共模块** → `linkfox-shopee-store-public`（`v2.public.*` 底层 OAuth / Partner 查询）
- **Shopee Push 推送机制** → `linkfox-shopee-store-push`
- **Shopee SBS 仓储服务** → `linkfox-shopee-store-sbs`
- **Shopee FBS 巴西仓储** → `linkfox-shopee-store-fbs`
- **Shopee 直播 Livestream** → `linkfox-shopee-store-livestream`
- Shopee 选品（友鹰） → `linkfox-youying-shopee-product-search`
- 商品 listing 管理 → 专用 product skill 或 `developerProxy` 商品 API

## 积分消耗规则

不消耗积分。

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
