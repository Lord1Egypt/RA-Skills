# TikTok Shop ERP 授权 API Reference

本文档描述 **TikTok Shop ERP（小店，`appType=erp`）** 授权与店铺/令牌管理 API（`/tiktokShop`）。本 skill **仅支持 erp**；不处理 `affiliate` / `creator`。

业务数据（商品/订单/履约/财务等）由按功能拆分的 `linkfox-tiktok-shop-*` skill 经 `/tiktokShop/developerProxy`（`appType=erp`）调用，不在本 skill 范围。

> ⚠️ **达人/视频号授权**请用 **`linkfox-tiktok-video-auth`**（`/tiktokVideo`）。本 skill 脚本若收到非 `erp` 的 `appType` 将直接报错退出。

## Calling Conventions

- **Base URL**: `${LINKFOX_TOOL_GATEWAY}`（可用 `LINKFOX_TOOL_GATEWAY` 覆盖；未设置时回退 `TIKTOK_SHOP_API_BASE_URL`，再回退 `https://tool-gateway.linkfox.com`）
- **Request Method**: 全部 POST
- **Content-Type**: `application/json`
- **Authentication**: Header `Authorization: <api_key>`（`LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY`）
- **User-Agent**: `LinkFox-Skill/1.0`
- **超时**: 150s
- **appType**: 本 skill **固定 `erp`**

## API Endpoints

### 1. Get Authorization URL

**Endpoint**: `/tiktokShop/authorizeUrl`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| shopName | string | No | - | 店铺名称（展示用，最长 256） |
| region | string | No | `global` | `global` / `us` |
| appType | string | No | **`erp`（强制）** | 本 skill 始终传 `erp`；勿传 affiliate/creator |

**Response**:

```json
{
  "authorizeUrl": "https://services.tiktokshop.com/open/authorize?service_id=xxx&state=abc123"
}
```

> 授权 URL 约 1 小时有效；完成后 Token 由系统回调落库。

---

### 2. List Authorized Stores

**Endpoint**: `/tiktokShop/authorizedStores`

**Request**: 无（当前用户上下文）。

网关可能返回多种 `appType`；**本 skill 脚本只保留 `appType=erp`** 并重算 `total`。

**Response（脚本过滤后）**:

```json
{
  "stores": [
    {
      "openId": "7010736057180325637",
      "sellerName": "Test Shop",
      "sellerBaseRegion": "ID",
      "appType": "erp",
      "region": "global"
    }
  ],
  "total": 1
}
```

---

### 3. Query Store Tokens（可选 / 调试）

**Endpoint**: `/tiktokShop/storeTokens`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| openId | string | **Yes** | - | 卖家 open_id |
| appType | string | No | **`erp`（强制）** | 本 skill 始终传 `erp` |

**Response**:

```json
{
  "authRecordId": 1,
  "openId": "7010736057180325637",
  "appType": "erp",
  "accessToken": "TTP_Fw8rBwAAAA...",
  "refreshToken": "TTP_NTUxZTNh...",
  "accessTokenExpireIn": 1660556783,
  "refreshTokenExpireIn": 1691487031
}
```

> 只读库中令牌，**不**校验 `accessTokenExpireIn`，也**不**触发刷新。  
> ERP 业务 skill 调用 `/tiktokShop/developerProxy` 时只需传 `openId`，**不必**先调本接口。

---

### 4. Refresh Token（可选手动）

**Endpoint**: `/tiktokShop/refreshToken`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| openId | string | **Yes** | - | 卖家 open_id |
| appType | string | No | **`erp`（强制）** | 本 skill 始终传 `erp` |

**Response**:

```json
{
  "authRecordId": 1,
  "accessToken": "TTP_Fw8rBwAAAA...",
  "refreshToken": "TTP_NTUxZTNh...",
  "accessTokenExpireIn": 1660556783,
  "refreshTokenExpireIn": 1691487031,
  "message": "刷新成功并已更新数据库"
}
```

> **日常业务不要先手动刷新**。`developerProxy` 在上游 HTTP 401 或 token expired/invalid 时会自动调用刷新逻辑、回写数据库并重试一次。  
> 无按过期时间提前刷新、无定时任务。本接口仅供排查或用户明确要求。  
> `refresh_token` 过期后须重新走 authorizeUrl。

---

## ACCESS_TOKEN 后台化（业务 Agent 必读）

```
业务 skill  →  POST /tiktokShop/developerProxy { openId, appType=erp, path, method, ... }
网关        →  按 openId+appType 从库取 accessToken（忽略 ttsAccessToken）
           →  转发上游；若 401 / token expired|invalid → refresh 一次并重试
           →  刷新成功则更新库中 accessToken / refreshToken / 过期时间
```

业务 skill **禁止**在每次调用前执行：`storeTokens` → 判断过期 → `refreshToken`。

---

## Error Codes

| errcode | 含义 | 建议动作 |
|---------|------|----------|
| 1002 | 参数校验失败 / 未登录 | 检查必填参数与认证 |
| 1003 | 上游异常 | 稍后重试 |
| 1004 | 授权记录不存在 / 无 refresh_token | 核对 openId 或重新授权 |
| 1005 | developerProxy path 未白名单 | 联系运维放行（业务 skill） |

脚本本地拒绝非 erp 的 `appType` 时直接 stderr 报错并 exit 1（不发网关请求）。

---

## curl Examples

```bash
# ERP 授权链接
curl -X POST https://tool-gateway.linkfox.com/tiktokShop/authorizeUrl \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"shopName": "My Shop", "region": "us", "appType": "erp"}'

# 列店铺（脚本侧会过滤为 erp）
curl -X POST https://tool-gateway.linkfox.com/tiktokShop/authorizedStores \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'

# 查 ERP 令牌
curl -X POST https://tool-gateway.linkfox.com/tiktokShop/storeTokens \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"openId": "7010736057180325637", "appType": "erp"}'

# 刷新 ERP 令牌
curl -X POST https://tool-gateway.linkfox.com/tiktokShop/refreshToken \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"openId": "7010736057180325637", "appType": "erp"}'
```

---

## Feedback API

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`

```json
{
  "skillName": "linkfox-tiktok-shop-auth",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "ERP authorization flow worked smoothly."
}
```

---

## Important Notes

1. **仅 ERP**：`appType` 固定 `erp`。
2. **Token 安全**：输出掩码，勿打印完整 token。
3. **过期字段**：`*ExpireIn` 为绝对 Unix 时间戳（展示用）；`/storeTokens` 不据此自动刷新。
4. **下游**：业务走 `linkfox-tiktok-shop-*` + `developerProxy(openId)`；token 后台化 + 401 自动刷新。
5. **达人分流**：creator → `linkfox-tiktok-video-auth`。
6. **手动 refresh**：仅排查或用户明确要求；勿作为业务前置步骤。
