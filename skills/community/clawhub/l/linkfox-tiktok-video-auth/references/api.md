# TikTok 视频上传 API — 授权与令牌管理 API Reference

本文档描述 **TikTok 视频上传模块（`/tiktokVideo`）** 的授权与令牌管理接口。底层经 LinkFox 网关转发至紫鸟开放平台 `tiktok-auth/auth/creator-url` 与 `tiktok-auth/auth/refresh?appType=creator`。业务调用（视频上传等）通过 `/tiktokVideo/developerProxy` 完成，不在本 skill 范围内。

> **与 TikTok Shop 模块的区别**：本模块使用独立路由前缀 `/tiktokVideo`、独立数据表，固定 `appType=creator`（达人端），无需传 `appType` 参数。TikTok Shop 授权（`/tiktokShop/*`，含 `appType=erp/creator/affiliate`）由 `linkfox-tiktok-shop-auth` 负责，两者数据不互通。

## Calling Conventions

- **Base URL**: `https://tool-gateway.linkfox.com`（默认；可用环境变量 `TIKTOK_VIDEO_API_BASE_URL` 覆盖）
- **Request Method**: 所有接口均为 POST
- **Content-Type**: `application/json`
- **Authentication**: Header `Authorization: <api_key>`，API key 读取环境变量 `LINKFOXAGENT_API_KEY`
- **User-Agent**: `LinkFox-Skill/1.0`
- **超时**: 150s
- **用户鉴权**: 以下接口均需 LinkFox 用户 Token；OAuth 回调端点不在本 skill 内

## API Endpoints

### 1. Get Authorization URL

**Endpoint**: `/tiktokVideo/authorizeUrl`

调用紫鸟 `GET tiktok-auth/auth/creator-url`，获取达人（Creator）授权跳转地址。

**Request Parameters** (JSON):

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| displayName | string | No | - | 视频号展示名称（可选，最长 256） |
| region | string | No | `global` | 地区：`global`（全球，默认）/ `us`（美国站） |

**Response**:

```json
{
  "authorizeUrl": "https://services.tiktokshop.com/open/authorize?service_id=xxx&state=abc123"
}
```

| Field | Type | Description |
|-------|------|-------------|
| authorizeUrl | string | 用户在浏览器中打开的授权链接（有效期约 1 小时） |

> 授权 URL 每次须重新获取。用户完成授权后，紫鸟将 Token **POST** 到 `{gateway.url}/tiktokVideo/oauth/tokenCallback`（messageType=251），浏览器同时重定向到 `{gateway.url}/tiktokVideo/oauth/redirect`。

---

### 2. List Authorized Accounts

**Endpoint**: `/tiktokVideo/authorizedAccounts`

**Request Parameters**: 无（使用当前用户上下文）。

**Response**:

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

| Field | Type | Description |
|-------|------|-------------|
| openId | string | 创作者 open_id |
| displayName | string | 展示名称 |
| region | string | 授权 region（global / us） |
| userType | integer | 用户类型（如 1=创作者） |
| grantedScopes | string | 已授权 scope 列表 JSON 字符串 |

---

### 3. Query Account Tokens

**Endpoint**: `/tiktokVideo/accountTokens`

按 `openId` 读取当前用户已绑定授权在库中的令牌，**不调用**紫鸟刷新接口。

**Request Parameters** (JSON):

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| openId | string | **Yes** | 创作者 open_id（最长 128） |

**Response**:

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

| Field | Type | Description |
|-------|------|-------------|
| authRecordId | integer | 授权主表 ID |
| openId | string | 创作者 open_id |
| accessToken | string | access_token（供 `/tiktokVideo/developerProxy` 的 `ttsAccessToken` 使用） |
| refreshToken | string | refresh_token |
| accessTokenExpireIn | integer | access_token 过期 Unix 时间戳 |
| refreshTokenExpireIn | integer | refresh_token 过期 Unix 时间戳 |
| userType | integer | 用户类型 |
| grantedScopes | string | 已授权 scope 列表 JSON |

---

### 4. Refresh Token

**Endpoint**: `/tiktokVideo/refreshToken`

从库中读取 `refresh_token`，调用紫鸟 `GET tiktok-auth/auth/refresh?appType=creator` 续签并回写数据库。

**Request Parameters** (JSON):

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| openId | string | **Yes** | 创作者 open_id |

**Response**:

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

| Field | Type | Description |
|-------|------|-------------|
| authRecordId | integer | 授权记录 ID |
| accessToken | string | 新的 access_token |
| refreshToken | string | 新的 refresh_token |
| accessTokenExpireIn | integer | access_token 过期 Unix 时间戳 |
| refreshTokenExpireIn | integer | refresh_token 过期 Unix 时间戳 |
| message | string | 说明信息 |

> `refresh_token` 过期后须重新走 **`/tiktokVideo/authorizeUrl`** 授权流程。

---

## Error Codes

| errcode | 含义 | 建议动作 |
|---------|------|----------|
| 1002 | 参数校验失败 / 未登录（如缺少 openId） | 检查必填参数与认证 |
| 1003 | 上游（紫鸟）服务或网络异常 / 未配置 gateway.url | 稍后重试，检查网络与白名单 |
| 1004 | 授权记录不存在或不属于当前用户、缺少 refresh_token | 核对 openId 或重新授权 |
| 1005 | 开发者代理 path 未在白名单（仅 developerProxy 相关） | 使用白名单内的 path 前缀 |

**Error Response Example**:

```json
{
  "errcode": 1002,
  "errmsg": "Missing required parameter: openId"
}
```

---

## curl Examples

### Get Authorization URL

```bash
curl -X POST https://tool-gateway.linkfox.com/tiktokVideo/authorizeUrl \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"displayName": "My Channel", "region": "global"}'
```

### List Authorized Accounts

```bash
curl -X POST https://tool-gateway.linkfox.com/tiktokVideo/authorizedAccounts \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Query Account Tokens

```bash
curl -X POST https://tool-gateway.linkfox.com/tiktokVideo/accountTokens \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"openId": "-7xYtQAAAABxLMG_EcfywQsTcT1aFR3GeQr_8HDLD21B4pJzd1zZcg"}'
```

### Refresh Token

```bash
curl -X POST https://tool-gateway.linkfox.com/tiktokVideo/refreshToken \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"openId": "-7xYtQAAAABxLMG_EcfywQsTcT1aFR3GeQr_8HDLD21B4pJzd1zZcg"}'
```

---

## Feedback API

> 本接口与上面的工具 API **是不同 base URL**，请勿混用。

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type**: `application/json`

```json
{
  "skillName": "linkfox-tiktok-video-auth",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Authorization flow worked smoothly, user was satisfied."
}
```

**Field rules**:
- `skillName`: 使用本 skill 的 YAML frontmatter `name`
- `sentiment`: `POSITIVE` / `NEUTRAL` / `NEGATIVE`
- `category`: `BUG` / `COMPLAINT` / `SUGGESTION` / `OTHER`
- `content`: 用户说的话、实际发生了什么、为什么是问题或赞赏

---

## Important Notes

1. **Token 安全**：不要向用户明文展示完整 accessToken/refreshToken，仅展示前 10 字符掩码。
2. **过期判断**：`accessTokenExpireIn` / `refreshTokenExpireIn` 为绝对 Unix 时间戳，与当前时间比较判断是否过期。
3. **用户隔离**：所有 API 都强制用户级访问控制。
4. **回调白名单**：系统回调 URL 与调用 IP 必须在授权提供方（紫鸟）处加白名单。
5. **独立模块**：本模块令牌仅适用于 `/tiktokVideo/developerProxy`，不可用于 `/tiktokShop/developerProxy`。
