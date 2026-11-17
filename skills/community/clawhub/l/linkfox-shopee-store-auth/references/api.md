# linkfox-shopee-store-auth — 参数与字段参考

Shopee 授权、已授权店铺列表、授权状态读取。支持 **ERP / AD** 双应用。

业务 API 转发见 `/shopee/developerProxy`（path 须以 `api/v2` 开头；**勿**传 `accessToken` / `appType`）。

## 通用约定

- **Base URL**：`${LINKFOX_TOOL_GATEWAY}`
- **Method**：POST，`Content-Type: application/json`
- **Auth**：Header `Authorization: <api_key>`（读环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY`；如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 关键 ID 与应用类型

```
  一次 OAuth 授权（指定 appType）
        ▼
  authRecordId (1 条)  ← 与该应用的 access/refresh token 绑定
        │
        ├──► shopId      ─┐
        ├──► merchantId  ─┘  查询时二选一即可
        └──► appType: erp | ad
```

- `authRecordId`：授权记录 ID；同一店铺可因 `appType` 不同有多条
- `shopId`：店铺 ID，转发 Shopee API 时写为 `shop_id`
- `merchantId`：商户 ID，与 `shopId` 二选一；转发时写为 `merchant_id`
- `appType`：`erp`（默认）或 `ad`；空/`null` 在展示与 ERP 查找时视为 `erp`
- `shopIdList` / `merchantIdList`：JSON 字符串，含本次授权绑定的全部 ID

判断是否已授权须同时匹配：**店铺标识 + appType**。

## 接口

### 1. 生成授权 URL — `/shopee/authorizeUrl`

服务端自动组装 `state`、`callbackUrl`、`redirectUrl`。授权地址约 **1 小时**有效，每次重新获取。

**Request**：
| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| `shopName` | string | 否 | - | 店铺展示名，便于在列表识别 |
| `region` | string | 否 | `cn` | `cn` / `global` / `br` |
| `appType` | string | 否 | `erp` | 只允许 `erp` 或 `ad` |

**Response**：
```json
{"sourceType": "shopee", "authorizeUrl": "https://open.shopee.cn/auth?...&state=abc123"}
```

授权完成后 Token 由 Shopee POST 到 `/shopee/oauth/tokenCallback`（系统内部）；浏览器跳转 `/shopee/oauth/redirect`，不作为公开接口。

ERP 示例：
```json
{"shopName": "Example Shop", "region": "cn", "appType": "erp"}
```

广告示例：
```json
{"shopName": "Example Shop", "region": "cn", "appType": "ad"}
```

---

### 2. 列已授权店铺 — `/shopee/authorizedStores`

**Request**：无（用当前用户上下文）

**Response**：
```json
{
  "total": 2,
  "stores": [
    {
      "authRecordId": 1,
      "shopId": "67890",
      "merchantId": "12345",
      "shopIdList": "[67890]",
      "merchantIdList": "[12345]",
      "shopName": "Test Shopee Shop",
      "region": "cn",
      "appType": "erp"
    },
    {
      "authRecordId": 2,
      "shopId": "67890",
      "merchantId": "12345",
      "shopName": "Test Shopee Shop",
      "region": "cn",
      "appType": "ad"
    }
  ]
}
```

同一个店铺可能返回 ERP、AD 两条。缺 `appType` 的历史记录按 **erp** 理解。

---

### 3. 查询授权状态 — `/shopee/storeTokens`

只返回授权状态/元数据，**不返回**原始 access token 或 refresh token（脚本侧也会剥离）。

**Request**（`shopId` 与 `merchantId` 二选一）：
| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| `shopId` | string | 与 merchantId 二选一 | - | 店铺 ID |
| `merchantId` | string | 与 shopId 二选一 | - | 商户 ID |
| `appType` | string | 否 | `erp` | `erp` 或 `ad` |

**Response（状态示例）**：
```json
{
  "authRecordId": 1,
  "shopId": "67890",
  "merchantId": "12345",
  "appType": "ad",
  "tokenType": "Bearer",
  "expireIn": 14400,
  "status": "ok"
}
```

本接口**不触发刷新**，仅读 DB。`expireIn` 为 access_token 剩余有效秒数（通常 14400）。

**不要**用本接口取 token 再传给 `/shopee/developerProxy`；proxy 由服务端按 path 注入对应应用 Token。

---

### 4. 业务转发（下游，非本 skill 脚本）— `/shopee/developerProxy`

```json
{
  "path": "api/v2/product/get_item_list",
  "method": "GET",
  "shopId": "67890",
  "queryString": "offset=0&page_size=20&item_status=NORMAL"
}
```

广告路径示例（自动走 AD Token）：
```json
{
  "path": "api/v2/ads/get_total_balance",
  "method": "GET",
  "shopId": "67890"
}
```

- `path` 必须以 `api/v2` 开头
- `shopId` 与 `merchantId` 至少传一个
- `accessToken` 已废弃，传入也会被忽略
- **不要**传 `appType`；`api/v2/ads/**` → AD，其它 → ERP

---

## 错误码

| errcode | 含义 | 建议 |
|---------|------|------|
| 200 | 成功 | — |
| 1002 | 参数错误、`appType` 非 erp/ad、未登录 | 修正参数，不要重试相同请求 |
| 1003 | 授权服务异常或网络失败 | 稍后重试；授权时重新获取 URL |
| 1004 | 找不到目标应用的店铺授权 | 按能力发起 ERP 或 AD 授权 |
| 1005 | Token 失效或转发路径未白名单 | Token 失效则重新授权；path 须以 `api/v2` 开头 |

错误响应：
```json
{"errcode": 1004, "errmsg": "未找到授权记录"}
```

---

## curl 示例

```bash
export KEY=$LINKFOXAGENT_API_KEY
BASE=https://tool-gateway.linkfox.com

# 1. ERP 授权 URL
curl -X POST $BASE/shopee/authorizeUrl -H "Authorization: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"shopName":"我的虾皮店铺","region":"cn","appType":"erp"}'

# 1b. 广告授权 URL
curl -X POST $BASE/shopee/authorizeUrl -H "Authorization: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"shopName":"我的虾皮店铺","region":"cn","appType":"ad"}'

# 2. 列已授权（含 appType）
curl -X POST $BASE/shopee/authorizedStores -H "Authorization: $KEY" \
  -H "Content-Type: application/json" -d '{}'

# 3. 查 AD 授权状态
curl -X POST $BASE/shopee/storeTokens -H "Authorization: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"shopId":"67890","appType":"ad"}'
```

---

## Feedback API

与上面的工具 API **base URL 不同**：

```bash
curl -X POST https://skill-api.linkfox.com/api/v1/public/feedback \
  -H "Content-Type: application/json" \
  -d '{"skillName":"linkfox-shopee-store-auth","sentiment":"POSITIVE",
       "category":"OTHER","content":"授权流程顺畅"}'
```

- `sentiment`: `POSITIVE` / `NEUTRAL` / `NEGATIVE`
- `category`: `BUG` / `COMPLAINT` / `SUGGESTION` / `OTHER`
