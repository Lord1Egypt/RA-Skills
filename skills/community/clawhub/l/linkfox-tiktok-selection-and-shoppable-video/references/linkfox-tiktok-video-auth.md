---
name: linkfox-tiktok-video-auth
description: 提供 TikTok 视频号达人 OAuth 授权、已授权账号列表、令牌查询与 access_token 刷新能力。
---

# TikTok 视频号授权与令牌管理

本 skill 负责 TikTok 视频上传模块（`/tiktokVideo`）的达人 OAuth 授权、已授权账号列表、令牌查询与刷新，是后续通过 `/tiktokVideo/developerProxy` 调用视频上传等开放接口的前置依赖。底层经 LinkFox 网关对接紫鸟开放平台，固定 `appType=creator`（达人端带货 / 视频上传）。接口参数、响应字段与错误码详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 生成 TikTok 达人/视频号 OAuth 授权链接，引导用户在浏览器完成授权。
- 列出当前用户已授权的视频号账号。
- 按 `openId` 查询已入库的访问令牌（供下游 `/tiktokVideo/developerProxy` 作为 `ttsAccessToken` 使用）。
- 用 `refreshToken` 刷新过期的 `accessToken` 并回写数据库。

### ❌ 边界与限制

- **模块独立**：本 skill 令牌仅适用于 `/tiktokVideo/*`，不可用于 `/tiktokShop/developerProxy`。TikTok Shop 卖家授权（`erp` / `affiliate`）请用 `linkfox-tiktok-shop-auth`，两者授权数据**不互通**。
- **令牌有效期**：`accessToken` 较短，过期需用 `refreshToken` 续签；`refreshToken` 过期须重新走授权流程。
- **授权链接时效**：`authorizeUrl` 有效期约 1 小时，过期需重新获取。
- **用户隔离**：用户只能查看/管理自己授权的账号。
- **回调白名单**：系统回调 URL 与调用 IP 必须在授权方（紫鸟）处加白名单。
- **不在范围内**：TikTok 视频上传等具体业务（用 `linkfox-tiktok-video` 经 `/tiktokVideo/developerProxy`）；TikTok Shop 可购物视频 / affiliate_creator 达人接口（用 `linkfox-tiktok-creator`，授权仍走本 skill）；TikTok 选品 / 达人带货数据分析（由 EchoTik 等其他 skill 负责）。

## 执行流程

### 步骤 1：生成授权链接
- 【输入】`region`（可选，默认 `global`，美国站用 `us`）；可选 `displayName` 作为展示标签。
- 【动作】调用 `/tiktokVideo/authorizeUrl`。
- 【输出】返回 `authorizeUrl`，交给用户在浏览器打开完成达人授权（链接约 1 小时失效）。

### 步骤 2：等待回调落库（系统自动）
- 【输入】用户在浏览器完成授权。
- 【动作】紫鸟将 Token POST 到 `/tiktokVideo/oauth/tokenCallback`（messageType=251），系统按 `state` 落库。
- 【输出】授权记录写入数据库，账号以 `openId` 标记。

### 步骤 3：列出已授权账号
- 【输入】当前用户上下文（无需传参）。
- 【动作】调用 `/tiktokVideo/authorizedAccounts`。
- 【输出】`accounts[]`（含 `openId` / `displayName` / `region` / `userType`）。

### 步骤 4：查询账号令牌
- 【输入】`openId`。
- 【动作】调用 `/tiktokVideo/accountTokens`（仅读取在库令牌，不触发上游刷新）。
- 【输出】`accessToken` / `refreshToken` / `accessTokenExpireIn` / `refreshTokenExpireIn` 等，供下游 `/tiktokVideo/developerProxy` 作为 `ttsAccessToken` 使用。

### 步骤 5：刷新令牌（按需）
- 【输入】`openId`。
- 【动作】调用 `/tiktokVideo/refreshToken`，由库中 `refreshToken` 调紫鸟续签并回写数据库。
- 【输出】新的 `accessToken` / `refreshToken` 与新过期时间戳；若 `refreshToken` 已过期，回到步骤 1 重新授权。

## 核心概念

**授权流程**：调用 `/tiktokVideo/authorizeUrl` 生成授权 URL → 用户在浏览器完成达人授权 → 紫鸟 POST Token 到 `/tiktokVideo/oauth/tokenCallback`（messageType=251）→ 系统按 `state` 落库。授权 URL 有效期约 1 小时，每次授权须重新获取。

**账号标识（`openId`）**：授权后以创作者唯一标识 `openId` 标记账号。查询令牌、刷新令牌均只需 `openId`（无需 `appType`）。

**令牌生命周期**：`accessToken` 与 `refreshToken` 均带绝对过期时间（Unix 时间戳）。`accessToken` 过期用 `refreshToken` 续签；`refreshToken` 过期须重新走授权流程。

**支持的 region**：`global`（全球，默认）/ `us`（美国站）。

## 调用方式

本 skill 经 LinkFox 网关调用 TikTok 视频上传授权相关接口，所有接口均为 POST，Header `Authorization: <api_key>`（读取环境变量 `LINKFOXAGENT_API_KEY`）。可用脚本：

- `scripts/authorize_url.py` — 生成达人授权 URL（可选 `displayName` / `region`）
- `scripts/authorized_accounts.py` — 列出当前用户已授权的视频号
- `scripts/account_tokens.py` — 按 `openId` 查询已入库令牌
- `scripts/refresh_token.py` — 刷新某账号的 access_token

## 使用示例

### 场景 1：授权新视频号
> 「我要授权 TikTok 视频上传 / 绑定视频号用于上传视频」
1. 确认 `region`（美国站用 `us`，否则默认 `global`），可选询问 `displayName`。
2. 调用 `/tiktokVideo/authorizeUrl`，得到 `authorizeUrl`。
3. 把 `authorizeUrl` 给用户，让其在浏览器中打开并完成授权（约 1 小时失效）。
4. 用户完成授权 → 紫鸟回调推送 Token → 系统自动落库。
5. 可选：调用 `/tiktokVideo/authorizedAccounts` 确认授权成功。

### 场景 2：查看已授权账号
> 「列一下我已授权的 TikTok 视频号」
1. 调用 `/tiktokVideo/authorizedAccounts`。
2. 展示账号列表（`displayName` / `openId` / `region` / `userType`）。

### 场景 3：刷新过期令牌
> 「我 TikTok 视频上传的令牌过期了，帮我刷新」
1. 调用 `/tiktokVideo/refreshToken`，传入 `openId`。
2. 返回新的 `accessToken` / `refreshToken` 并回写数据库。
3. 若 `refreshToken` 已过期，引导用户重新走场景 1 授权。

### 场景 4：查询账号令牌
> 「获取某 TikTok 视频号的访问令牌」
1. 调用 `/tiktokVideo/accountTokens`，传入 `openId`。
2. 返回令牌信息（供下游 `/tiktokVideo/developerProxy` 使用）。

### 场景 5：为视频上传准备令牌（标准前置流程）
当用户提出涉及 TikTok 视频上传的请求，本 skill 负责「选号 → 取令牌」前置流程，业务由 `/tiktokVideo/developerProxy` 接手：
1. 调用 `/tiktokVideo/authorizedAccounts` 列出已授权账号。
2. 多个视频号时请用户明确选择。
3. 调用 `/tiktokVideo/accountTokens` 传入 `openId` 获取令牌。
4. 把 `accessToken` 作为 `ttsAccessToken` 交给 `/tiktokVideo/developerProxy` 执行业务。

## 展示规则

1. **只呈现数据**：展示授权结果、账号列表、令牌信息即可，不做业务建议。
2. **安全意识**：不要明文显示完整 `accessToken` / `refreshToken`，仅展示前 10 字符等掩码形式。
3. **清晰引导**：返回授权链接时，明确告知用户在浏览器中打开并完成授权，且链接约 1 小时失效。
4. **过期解读**：`accessTokenExpireIn` / `refreshTokenExpireIn` 为绝对 Unix 时间戳，需与当前时间比较判断是否过期。
5. **错误说明**：授权或刷新失败时，基于错误码解释原因并给出建议。

## 用户表达与场景速查

**适用** —— 授权与令牌管理场景：

| 用户说 | 场景 |
|--------|------|
| "授权 TikTok 视频上传" / "Authorize TikTok video upload account" | 新视频号授权 |
| "绑定 TikTok 视频号用于上传视频" | 新视频号授权 |
| "看看已授权的 TikTok 视频号" / "Show my authorized TikTok video accounts" | 列出已授权账号 |
| "TikTok 视频上传令牌过期了" / "My TikTok video token expired" | 刷新令牌 |
| "获取 TikTok 视频号的访问令牌" / "Get TikTok video account access token" | 查询账号令牌 |

不适用场景见上方【能力边界】。

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

# TikTok 视频上传 API — 授权与令牌管理 API 参考

本文档描述 **TikTok 视频上传模块（`/tiktokVideo`）** 的授权与令牌管理接口。底层经 LinkFox 网关转发至紫鸟开放平台 `tiktok-auth/auth/creator-url` 与 `tiktok-auth/auth/refresh?appType=creator`。业务调用（视频上传等）通过 `/tiktokVideo/developerProxy` 完成，不在本 skill 范围内。

> **与 TikTok Shop 模块的区别**：本模块使用独立路由前缀 `/tiktokVideo`、独立数据表，固定 `appType=creator`（达人端），无需传 `appType` 参数。TikTok Shop 授权（`/tiktokShop/*`，含 `appType=erp/creator/affiliate`）由 `linkfox-tiktok-shop-auth` 负责，两者数据不互通。

## 调用规范

- **请求地址**：`https://tool-gateway.linkfox.com`（默认；可用环境变量 `LINKFOX_TOOL_GATEWAY` 覆盖）
- **请求方式**：所有接口均为 POST
- **Content-Type**：`application/json`
- **认证方式**：Header `Authorization: <api_key>`，API key 读取环境变量 `LINKFOXAGENT_API_KEY`（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）
- **User-Agent**：`LinkFox-Skill/1.0`
- **超时**：150s
- **用户鉴权**：以下接口均需 LinkFox 用户 Token；OAuth 回调端点不在本 skill 内

## 接口列表

### 1. 获取授权链接

**接口地址**：`/tiktokVideo/authorizeUrl`

调用紫鸟 `GET tiktok-auth/auth/creator-url`，获取达人（Creator）授权跳转地址。

**请求参数**（JSON）：

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| displayName | string | 否 | - | 视频号展示名称（可选，最长 256） |
| region | string | 否 | `global` | 地区：`global`（全球，默认）/ `us`（美国站） |

**响应**：

```json
{
  "authorizeUrl": "https://services.tiktokshop.com/open/authorize?service_id=xxx&state=abc123"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| authorizeUrl | string | 用户在浏览器中打开的授权链接（有效期约 1 小时） |

> 授权 URL 每次须重新获取。用户完成授权后，紫鸟将 Token **POST** 到 `{gateway.url}/tiktokVideo/oauth/tokenCallback`（messageType=251），浏览器同时重定向到 `{gateway.url}/tiktokVideo/oauth/redirect`。

---

### 2. 列出已授权账号

**接口地址**：`/tiktokVideo/authorizedAccounts`

**请求参数**：无（使用当前用户上下文）。

**响应**：

```json
{
  "accounts": [
    {
      "openId": "-7xYtQAAAABxLMG_EcfywQsTcT1aFR3GeQr_8HDLD21B4pJzd1zZcg",
      "displayName": "My Channel",
      "region": "global",
      "userType": 1,
      "grantedScopes": "[\"creator.video.write\"]"
    }
  ],
  "total": 1
}
```

**accounts[] 字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| openId | string | 创作者 open_id |
| displayName | string | 展示名称 |
| region | string | 授权 region（global / us） |
| userType | integer | 用户类型（如 1=创作者） |
| grantedScopes | string | 已授权 scope 列表 JSON 字符串 |

---

### 3. 查询账号令牌

**接口地址**：`/tiktokVideo/accountTokens`

按 `openId` 读取当前用户已绑定授权在库中的令牌，**不调用**紫鸟刷新接口。

**请求参数**（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| openId | string | **是** | 创作者 open_id（最长 128） |

**响应**：

```json
{
  "authRecordId": 1,
  "openId": "-7xYtQAAAABxLMG_EcfywQsTcT1aFR3GeQr_8HDLD21B4pJzd1zZcg",
  "accessToken": "TTP_Fw8rBwAAAA...",
  "refreshToken": "TTP_NTUxZTNh...",
  "accessTokenExpireIn": 1781061564,
  "refreshTokenExpireIn": 1811992756,
  "userType": 1,
  "grantedScopes": "[\"creator.video.write\"]"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| authRecordId | integer | 授权主表 ID |
| openId | string | 创作者 open_id |
| accessToken | string | access_token（供 `/tiktokVideo/developerProxy` 的 `ttsAccessToken` 使用） |
| refreshToken | string | refresh_token |
| accessTokenExpireIn | integer | access_token 过期 Unix 时间戳 |
| refreshTokenExpireIn | integer | refresh_token 过期 Unix 时间戳 |
| userType | integer | 用户类型 |
| grantedScopes | string | 已授权 scope 列表 JSON |

---

### 4. 刷新令牌

**接口地址**：`/tiktokVideo/refreshToken`

从库中读取 `refresh_token`，调用紫鸟 `GET tiktok-auth/auth/refresh?appType=creator` 续签并回写数据库。

**请求参数**（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| openId | string | **是** | 创作者 open_id |

**响应**：

```json
{
  "authRecordId": 1,
  "accessToken": "TTP_Fw8rBwAAAA...",
  "refreshToken": "TTP_NTUxZTNh...",
  "accessTokenExpireIn": 1781061564,
  "refreshTokenExpireIn": 1811992756,
  "message": "刷新成功并已更新数据库"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| authRecordId | integer | 授权记录 ID |
| accessToken | string | 新的 access_token |
| refreshToken | string | 新的 refresh_token |
| accessTokenExpireIn | integer | access_token 过期 Unix 时间戳 |
| refreshTokenExpireIn | integer | refresh_token 过期 Unix 时间戳 |
| message | string | 说明信息 |

> `refresh_token` 过期后须重新走 **`/tiktokVideo/authorizeUrl`** 授权流程。

---

## 错误码

| errcode | 含义 | 建议动作 |
|---------|------|----------|
| 1002 | 参数校验失败 / 未登录（如缺少 openId） | 检查必填参数与认证 |
| 1003 | 上游（紫鸟）服务或网络异常 / 未配置 gateway.url | 稍后重试，检查网络与白名单 |
| 1004 | 授权记录不存在或不属于当前用户、缺少 refresh_token | 核对 openId 或重新授权 |
| 1005 | 开发者代理 path 未在白名单（仅 developerProxy 相关） | 使用白名单内的 path 前缀 |

**错误响应示例**：

```json
{
  "errcode": 1002,
  "errmsg": "Missing required parameter: openId"
}
```

---

## curl 示例

### 获取授权链接

```bash
curl -X POST https://tool-gateway.linkfox.com/tiktokVideo/authorizeUrl \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"displayName": "My Channel", "region": "global"}'
```

### 列出已授权账号

```bash
curl -X POST https://tool-gateway.linkfox.com/tiktokVideo/authorizedAccounts \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 查询账号令牌

```bash
curl -X POST https://tool-gateway.linkfox.com/tiktokVideo/accountTokens \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"openId": "-7xYtQAAAABxLMG_EcfywQsTcT1aFR3GeQr_8HDLD21B4pJzd1zZcg"}'
```

### 刷新令牌

```bash
curl -X POST https://tool-gateway.linkfox.com/tiktokVideo/refreshToken \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"openId": "-7xYtQAAAABxLMG_EcfywQsTcT1aFR3GeQr_8HDLD21B4pJzd1zZcg"}'
```

---

## 重要说明

1. **Token 安全**：不要向用户明文展示完整 accessToken/refreshToken，仅展示前 10 字符掩码。
2. **过期判断**：`accessTokenExpireIn` / `refreshTokenExpireIn` 为绝对 Unix 时间戳，与当前时间比较判断是否过期。
3. **用户隔离**：所有 API 都强制用户级访问控制。
4. **回调白名单**：系统回调 URL 与调用 IP 必须在授权提供方（紫鸟）处加白名单。
5. **独立模块**：本模块令牌仅适用于 `/tiktokVideo/developerProxy`，不可用于 `/tiktokShop/developerProxy`。
