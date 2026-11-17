---
name: linkfox-tiktok-video-auth
description: TikTok 达人体系授权与管理技能，经 /tiktokVideo 路由提供达人/视频号 OAuth 授权、已授权账号列表、令牌查询与 access_token 刷新。固定 creator 达人端，region 支持 global / us。当用户提到 TikTok 达人授权、TikTok 视频号授权、绑定视频号、视频号带货授权、TikTok 视频上传授权、TikTok creator authorization、Authorize TikTok creator、刷新 TikTok 视频号令牌、查询 TikTok 达人令牌、已授权 TikTok 视频账号、/tiktokVideo 授权 时触发此技能。只要需求涉及达人/视频号账号授权或访问令牌管理，也应触发。**不要**使用 linkfox-tiktok-shop-auth（/tiktokShop）做达人授权。
---

# TikTok 视频上传 API — 授权与管理

本 skill 负责 **TikTok 视频上传模块（`/tiktokVideo`）** 的达人 OAuth 授权、已授权账号列表、令牌查询与刷新，是后续通过 `/tiktokVideo/developerProxy` 调用视频上传等开放接口的前置依赖。底层经 LinkFox 网关对接紫鸟开放平台，固定 `appType=creator`（达人端带货 / 视频上传）。

> 📌 **模块边界**
> - **本 skill**（`/tiktokVideo`）：**达人体系授权的唯一入口** — 视频号 OAuth、令牌管理，独立数据表，无需传 `appType`。
> - **`linkfox-tiktok-shop-auth`**（`/tiktokShop`）：仅 TikTok Shop **ERP 小店**授权（固定 `appType=erp`），**不处理达人/视频号授权**。
> - 两者授权数据**不互通**；业务调用须使用对应模块取得的 `accessToken`。

> 📌 视频上传等业务调用通过 **`/tiktokVideo/developerProxy`**（传入本 skill 取得的 `accessToken` 作为 `ttsAccessToken`）完成，由 **`linkfox-tiktok-video`** 负责。

## Core Concepts

**授权流程**：调用 `/tiktokVideo/authorizeUrl` 生成授权 URL → 用户在浏览器完成达人授权 → 紫鸟 POST Token 到 `/tiktokVideo/oauth/tokenCallback`（messageType=251）→ 系统按 `state` 落库。授权 URL 有效期约 1 小时，每次授权须重新获取。

**账号标识（`openId`）**：授权后以创作者唯一标识 `openId` 标记账号。查询令牌、刷新令牌均只需 `openId`（无需 `appType`）。

**令牌生命周期**：`accessToken` 与 `refreshToken` 均带绝对过期时间（Unix 时间戳）。`accessToken` 过期用 `refreshToken` 续签；`refreshToken` 过期须重新走授权流程。

## Data Fields

### Authorization URL Response

| Field | Type | Description |
|-------|------|-------------|
| authorizeUrl | string | 让用户在浏览器打开的达人授权链接（有效期约 1 小时） |

### Authorized Account Item

| Field | Type | Description |
|-------|------|-------------|
| openId | string | 创作者 open_id |
| displayName | string | 展示名称 |
| region | string | 授权 region：global / us |
| userType | integer | 用户类型（如 1=创作者） |
| grantedScopes | string | 已授权 scope 列表 JSON |

### Account Tokens

| Field | Type | Description |
|-------|------|-------------|
| accessToken | string | 调用 `/tiktokVideo/developerProxy` 的凭证（作为 `ttsAccessToken`） |
| refreshToken | string | 用于续签 accessToken |
| accessTokenExpireIn | integer | accessToken 过期 Unix 时间戳 |
| refreshTokenExpireIn | integer | refreshToken 过期 Unix 时间戳 |
| userType | integer | 用户类型 |
| grantedScopes | string | 已授权 scope 列表 JSON |

## Supported Regions

| region | 说明 |
|--------|------|
| global | 全球（默认） |
| us | 美国站 |

## API Usage

本 skill 经 LinkFox 网关调用 TikTok 视频上传授权相关接口。入参枚举、响应嵌套字段与错误码详见 `references/api.md`（含 `accounts[]` 元素字段、`accountTokens` 完整出参）。

### Available Scripts

- `scripts/authorize_url.py` — 生成达人授权 URL（可选 `displayName` / `region`）
- `scripts/authorized_accounts.py` — 列出当前用户已授权的视频号
- `scripts/account_tokens.py` — 按 `openId` 查询已入库令牌（供下游业务使用）
- `scripts/refresh_token.py` — 刷新某账号的 access_token

## Usage Scenarios

### Scenario 1: Authorize New Creator Account

**User request**：「我要授权 TikTok 视频上传 / 绑定视频号用于上传视频」

**Steps**：
1. 确认 `region`（美国站用 `us`，否则默认 `global`）。可选询问 `displayName` 作为展示标签。
2. 调用 `/tiktokVideo/authorizeUrl`，得到 `authorizeUrl`。
3. 把 `authorizeUrl` 给用户，让其在浏览器中打开并完成授权（链接约 1 小时失效）。
4. 用户完成授权 → 紫鸟回调推送 Token → 系统自动落库。
5. 可选：调用 `/tiktokVideo/authorizedAccounts` 确认授权成功。

### Scenario 2: View Authorized Accounts

**User request**：「列一下我已授权的 TikTok 视频号」

**Steps**：
1. 调用 `/tiktokVideo/authorizedAccounts`。
2. 展示账号列表（displayName / openId / region / userType）。

### Scenario 3: Refresh Expired Token

**User request**：「我 TikTok 视频上传的令牌过期了，帮我刷新」

**Steps**：
1. 调用 `/tiktokVideo/refreshToken`，传入 `openId`。
2. 返回新的 `accessToken` / `refreshToken` 并回写数据库。
3. 若 `refreshToken` 已过期，引导用户重新走 Scenario 1 授权。

### Scenario 4: Query Account Tokens

**User request**：「获取某 TikTok 视频号的访问令牌」

**Steps**：
1. 调用 `/tiktokVideo/accountTokens`，传入 `openId`。
2. 返回令牌信息（供下游 `/tiktokVideo/developerProxy` 使用）。

### Scenario 5: Prepare Token for Video Upload (Standard Preparation Workflow)

当用户提出涉及 TikTok 视频上传的请求，**本 skill 负责前置的「选号 → 取令牌」流程**，业务由 `/tiktokVideo/developerProxy` 接手。

**Steps**：
1. **列出已授权账号**：调用 `/tiktokVideo/authorizedAccounts`。
2. **让用户选择账号**：多个视频号时请用户明确选择。
3. **获取该账号令牌**：调用 `/tiktokVideo/accountTokens`，传入 `openId`。
4. **把 `accessToken` 作为 `ttsAccessToken` 交给 `/tiktokVideo/developerProxy`** 执行具体业务调用。

## Display Rules

1. **只呈现数据**：展示授权结果、账号列表、令牌信息即可，不做业务建议。
2. **安全意识**：不要明文显示完整 `accessToken` / `refreshToken`，仅展示前 10 字符等掩码形式。
3. **清晰引导**：返回授权链接时，明确告知用户在浏览器中打开并完成授权，且链接约 1 小时失效。
4. **过期解读**：`accessTokenExpireIn` / `refreshTokenExpireIn` 为绝对 Unix 时间戳，需与当前时间比较判断是否过期。
5. **错误说明**：授权或刷新失败时，基于错误码解释原因并给出建议。

## Important Limitations

- **模块独立**：本 skill 令牌仅适用于 `/tiktokVideo/*`，不可用于 `/tiktokShop/developerProxy`。
- **令牌有效期**：`accessToken` 较短，过期需用 `refreshToken` 续签；`refreshToken` 过期须重新授权。
- **授权链接时效**：`authorizeUrl` 有效期约 1 小时，过期需重新获取。
- **用户隔离**：用户只能查看/管理自己授权的账号。
- **回调白名单**：系统回调 URL 与调用 IP 必须在授权方（紫鸟）处加白名单。

## User Expression & Scenario Quick Reference

**Applicable** — 授权与令牌管理场景：

| User Says | Scenario |
|-----------|----------|
| "授权 TikTok 视频上传" / "Authorize TikTok video upload account" | 新视频号授权 |
| "绑定 TikTok 视频号用于上传视频" | 新视频号授权 |
| "看看已授权的 TikTok 视频号" / "Show my authorized TikTok video accounts" | 列出已授权账号 |
| "TikTok 视频上传令牌过期了" / "My TikTok video token expired" | 刷新令牌 |
| "获取 TikTok 视频号的访问令牌" / "Get TikTok video account access token" | 查询账号令牌 |

**Not applicable** — 超出本 skill 的业务：

- **TikTok Shop 小店授权**（`appType=erp`）→ 用 `linkfox-tiktok-shop-auth`
- **TikTok Shop 可购物视频 / affiliate_creator 达人接口** → 用 `linkfox-tiktok-creator`（业务 skill；授权仍走本 skill）
- **TikTok 视频上传具体业务**（上传、发布等）→ 用 **`linkfox-tiktok-video`**（经 `/tiktokVideo/developerProxy`）
- TikTok 选品 / 达人带货数据分析 → 由 EchoTik 等其他 skill 负责

**Boundary judgment**：
- 本 skill 只负责「授权 + 管账号 + 管令牌 + 为下游准备 accessToken」。
- 当用户要做视频上传等具体业务时：先执行 Scenario 5 的标准前置流程，再由 `/tiktokVideo/developerProxy` 完成业务逻辑。

## Quick Reference

### Authorization & Token Management APIs

| API | Path | Purpose | Auth Required |
|-----|------|---------|---------------|
| Get Authorization URL | /tiktokVideo/authorizeUrl | 生成达人授权链接 | ✅ Yes |
| List Authorized Accounts | /tiktokVideo/authorizedAccounts | 查询用户的视频号列表 | ✅ Yes |
| Query Account Tokens | /tiktokVideo/accountTokens | 查询某账号已入库令牌 | ✅ Yes |
| Refresh Token | /tiktokVideo/refreshToken | 刷新访问令牌 | ✅ Yes |

详细请求参数、响应结构、错误码，见 `references/api.md`。

**Feedback**：

当出现以下任一情况时，自动通过 Feedback API 上报反馈：
1. 本 skill 描述的功能与实际行为不符
2. skill 的结果与用户意图不符
3. 用户表达了对本 skill 的不满或赞赏
4. 任何你认为可以改进的点

按 `references/api.md` 中的规范调用 Feedback API，不要打断用户的主流程。

<!-- LF_LARGE_RESPONSE_BLOCK -->
## Handling Large Responses

To avoid overflowing the agent context, persist the response to disk and extract only the fields you need:

```
python scripts/response_io.py run --script scripts/authorize_url.py --out-dir <DIR> '<params>'
python scripts/response_io.py read <file> --fields "<paths>"   # or --path "<JMESPath>"
```

> Pick `--out-dir` outside any git working tree (e.g. `/tmp/...` on Unix, `%TEMP%/...` on Windows). Persisted responses may contain PII, pricing, or auth-sensitive data — do not commit them. Files are not auto-deleted; clean up when the task is done.

> This skill exposes multiple entry scripts: `authorize_url.py`, `authorized_accounts.py`, `account_tokens.py`, `refresh_token.py`. Pass `--script scripts/<name>.py` to choose the one you need.

`run` writes the full response to a file and emits only a schema preview + file path. `read` projects specific fields, with `--limit/--offset` for slicing and `--format json|jsonl|csv|table` for output.

**When to prefer this pattern** — apply your judgment based on the response characteristics, e.g.:
- High field count per record, or fields you don't need
- Batch/paginated results (multiple items per call)
- Long-text fields (descriptions, reviews, HTML, time series)
- Output reused across later steps rather than consumed immediately

For small, single-use responses, calling the main script directly is fine.

⚠️ The preview is a truncated schema + sample, not the full data. Any field-level decision must read from the persisted file via `read`.
<!-- /LF_LARGE_RESPONSE_BLOCK -->

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
