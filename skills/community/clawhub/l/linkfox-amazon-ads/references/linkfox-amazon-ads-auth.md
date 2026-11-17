---
name: linkfox-amazon-ads-auth
description: 提供亚马逊广告店铺的授权与管理，支持单次授权自动绑定同账号下所有站点的广告 profile 并进行令牌管理。
---


# Amazon Ads 授权与广告账户管理

亚马逊广告（Amazon Ads）的授权（LWA OAuth）、profile 发现与访问令牌管理。是下游 skill 的前置依赖：下游为 `linkfox-amazon-ads-manager`（广告管理）、`linkfox-amazon-ads-report`（报告）。参数与字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 为亚马逊广告账号生成 LWA OAuth 授权链接，一次授权自动发现并绑定同账号下所有可用站点的广告 profile（每个站点对应一个 profileId）。
- 查询已授权账号与站点列表、profile 列表，读取与刷新访问令牌。
- 支持 `NA`（美加墨巴）/ `EU`（英德法意西荷印度中东等）/ `FE`（日澳新）三大区域，默认 `NA`。

### ❌ 边界与限制

- **accountName 必填**：调 `authorize_url.py` 前必须先向用户确认一个非空账号名。
- **令牌时效**：accessToken 有效期 1 小时，过期后下游返回 HTTP 401，需用 `refresh_token.py` 续签。
- **不修改广告**：本系列为只读授权与令牌管理，不创建/修改/删除广告。
- **不在范围内**：查广告活动/组/关键词/商品广告/定向 → `linkfox-amazon-ads-manager`；拉广告报告（含指标） → `linkfox-amazon-ads-report`；店铺订单/库存/财务 → `linkfox-amazon-store-*`。

## 执行流程

### 步骤 1：新账号授权

- 【输入】`accountName`（非空账号名，用于识别）、`region`（`NA`/`EU`/`FE`，默认 `NA`）
- 【动作】先向用户确认 `accountName`；调 `authorize_url.py` 生成授权 URL，提示用户在日常运营该店铺的安全网络环境（建议紫鸟浏览器等防关联浏览器）中打开链接完成 OAuth 授权
- 【输出】`authorizeUrl`；授权完成后系统自动存 token + 同步 profile

### 步骤 2：确认授权结果

- 【输入】无（取当前用户上下文）
- 【动作】调 `authorized_stores.py` 列出已授权账号 × 站点
- 【输出】`profileId` / `accountInfoName` / `countryCode` / `region` 列表

### 步骤 3：为下游解析 profileId

- 【输入】用户的自然语言站点描述（如「美国站」「我的店铺」）
- 【动作】单账号按 `countryCode` 直接定位；多账号按 `accountName` 向用户澄清；映射成功不播报 profileId 数值
- 【输出】`profileId`，静默传递给下游 skill

### 步骤 4：刷新过期令牌

- 【输入】`profileId` 或 `authRecordId`
- 【动作】下游返回 HTTP 401 或错误体含 `expired`/`unauthorized`/`access token` 时，调 `refresh_token.py`
- 【输出】新的 `accessToken`（有效期 1 小时）

## 核心概念

- **授权流程**：生成 URL → 用户浏览器授权 → 系统存 token + 同步 profile
- **一次授权多 profile**：每个 marketplace（US/UK/JP…）一个 profileId；下游调用必须带 profileId
- **accessToken 1 小时有效**；过期后下游返回 HTTP 401，可用 `refresh_token.py` 续签

## 可用脚本

| 脚本 | 作用 |
|------|------|
| `authorize_url.py` | 为新账号生成授权 URL（`accountName` 必填） |
| `authorized_stores.py` | 列出已授权的账号 × 站点（按 profileId 聚合） |
| `profiles.py` | 列 profile 列表（`refresh=true` 穿透上游刷新） |
| `refresh_token.py` | 刷新 accessToken |
| `store_tokens.py` | 查 token（供下游使用） |

入参、响应字段、错误码见 [references/api.md](references/api.md)。

## 调用方式

- **API 端点**：`POST /amazonAds/{authorizeUrl|storeTokens|authorizedStores|refreshToken}`（完整参数/响应/错误码见 [references/api.md](references/api.md)）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见上文）
- **成本约束**：本工具会消耗积分；失败/空结果不得自动连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- 始终将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/<skill-name>-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录；`<session>` 取自环境变量 `SESSION_ID`；禁止写入 /tmp，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 新授权账号**
> "帮我授权亚马逊美国广告账号"
- 先问用户要 `accountName` → 调 `authorize_url.py` 拿 URL → 给用户在浏览器打开 → 授权完成后系统自动存 token + 同步 profile → 可选调 `authorized_stores.py` 确认

**2. 列已授权账号**
> "我绑定了哪些亚马逊广告账号？"
- 调 `authorized_stores.py`，展示 `profileId / accountInfoName / countryCode / region`

**3. 刷新过期令牌**
> "广告接口报 401 了"
- 调 `refresh_token.py`（传 `profileId` 或 `authRecordId`）

**4. 给下游解析 profileId**
> "查下我美国站的广告"
- 单账号直接定位；多账号按 `accountName` 澄清；不让用户报 profileId 数字

## 展示规则

1. **令牌掩码**：不输出完整 `accessToken` / `refreshToken`；脚本已做掩码，不要在摘要里还原。
2. **账号列表呈现**：以结构化表格展示 `profileId / accountInfoName / countryCode / region`，便于用户识别账号与站点。
3. **授权链接安全提示**：给出授权 URL 时同步提示在安全网络环境（建议防关联浏览器）中打开。
4. **错误处理**：授权/刷新失败按错误码解释原因，不擅自重试；建议调整措施（如重新授权、核对 profileId）。

## 用户表达与场景速查

**适用** —— 亚马逊广告授权与令牌管理：

| 用户说 | 场景 |
|--------|------|
| "授权亚马逊广告"、"绑定广告账户" | 新账号授权 |
| "我绑定了哪些广告账号" | 列已授权账号 |
| "广告报 401"、"令牌过期" | 刷新令牌 |
| "查我的 profile"、"美国站 profile" | profileId 解析 / profile 列表 |
| "Amazon Ads 授权"、"Ads token refresh" | 授权与令牌管理 |

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

## 常见问题

### 授权链接打开报 400，client_id 看起来被污染

现象：URL 里 `client_id` 中间出现空格 / `+`，Amazon 报 `StegoRuntimeOAuth2ClientManager:getClientDefinition`。
原因：授权链接 ~270 字符，从终端 / 聊天窗口复制时被软换行插入空格。
解决：`authorize_url.py` 成功后会同步写到剪贴板 + `~/.cache/linkfox/last_authorize_url.txt`，**从这两处复制**；浏览器地址栏 Ctrl+V 即可。建议无痕窗口打开。

### 授权回调页显示 `profile_sync_failed`

原因：当前 Amazon 账号未在广告后台创建"经理账户（Manager Account）"并关联广告账户。
解决：登录 [Amazon Ads 控制台](https://advertising.amazon.com/) → Manager accounts → 关联账户，重新授权。

---

# linkfox-amazon-ads-auth — 参数与字段参考

Amazon Ads 授权、已授权账号列表、profile 管理、令牌读取与刷新。

下游实体查询见 `linkfox-amazon-ads-manager`；SP 报告见 `linkfox-amazon-ads-report`。

## 通用约定

- **基础地址**：`${LINKFOX_TOOL_GATEWAY}`
- **请求方式**：POST，`Content-Type: application/json`
- **认证方式**：Header `Authorization: <api_key>`（读环境变量 `LINKFOX_AGENT_API_KEY`（优先）或 `LINKFOXAGENT_API_KEY`；如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 关键 ID 关系

```
  一次 OAuth 授权
        ▼
  authRecordId (1 条)  ← 与 accessToken/refreshToken 绑定
        │
        ├──► profileId A (US)    ─┐
        ├──► profileId B (CA)    ├── 一次授权 → 多个 profile（每个 marketplace 一个）
        └──► profileId C (MX)    ─┘
```

- `authRecordId`：授权记录 ID，一次 LWA OAuth 对应一个
- `profileId`：业务操作单位；下游 skill 调用的核心参数
- `accountInfoId`：广告主 entity 级标识，跨 marketplace 稳定

## 接口

### 1. 生成授权 URL — `/amazonAds/authorizeUrl`

**请求**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `region` | string | 是 | `NA` / `EU` / `FE` |
| `accountName` | string | **是** | 非空字符串，用于在已授权列表识别 |

**响应**：
```json
{"authorizeUrl": "https://sellercentral.amazon.com/ap/oa?...", "sourceType": "amazon_ads"}
```

授权完成后 OAuth 回调由系统内部处理（存 token + 同步 profile），不作为公开接口。

---

### 2. 列已授权账号 — `/amazonAds/authorizedStores`

**请求**：无（用当前用户上下文）

**响应**：
```json
{
  "total": 3,
  "stores": [
    {
      "profileId": 1111111111,
      "accountInfoId": "ENTITY1ABC",
      "accountInfoName": "店铺 A",
      "accountType": "seller",
      "countryCode": "US",
      "marketplaceStringId": "ATVPDKIKX0DER",
      "region": "NA",
      "authRecordId": 1001,
      "accountName": "我的美国广告账号"
    }
  ]
}
```

按 profileId 聚合（每个账号 × marketplace 一条）。
`accountType` ∈ `seller` / `vendor` / `agency`。

---

### 3. 列 profile — `/amazonAds/profiles`

**请求**：
| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| `refresh` | boolean | 否 | false | true=穿透上游重新拉取并落库；false=读本地快照 |

**响应**：
```json
{
  "total": 3, "refreshed": false,
  "profiles": [{
    "profileId": 1111111111, "region": "NA", "countryCode": "US",
    "currencyCode": "USD", "dailyBudget": "100.00",
    "timezone": "America/Los_Angeles",
    "accountInfoId": "ENTITY1ABC", "accountInfoType": "seller",
    "accountInfoName": "店铺 A",
    "marketplaceStringId": "ATVPDKIKX0DER",
    "authRecordId": 1001
  }]
}
```

与 `authorizedStores` 区别：前者面向"选账号 × 站点"粗粒度；本接口含货币、时区、日预算等业务字段。

---

### 4. 刷新令牌 — `/amazonAds/refreshToken`

`accessToken` 1 小时有效；过期后下游返回 HTTP 401 或错误体含 `expired` / `unauthorized` / `access token`。

**请求**（`authRecordId` 和 `profileId` 二选一）：
| 参数 | 类型 | 说明 |
|------|------|------|
| `authRecordId` | number | 授权主表 ID |
| `profileId` | number | 系统会反查到所属授权 |

**响应**：
```json
{
  "authRecordId": 1001,
  "accessToken": "Atza|IwEBI...", "refreshToken": "Atzr|IwEBI...",
  "tokenType": "bearer", "expiresIn": "3600",
  "message": "刷新成功"
}
```

---

### 5. 查询令牌 — `/amazonAds/storeTokens`

**请求**（二选一，同上）：`authRecordId` 或 `profileId`。

**响应**：同 §4，少了 `message` 字段。

本接口**不触发刷新**，仅读 DB。

---

## 错误码

| errcode | 含义 | 建议 |
|---------|------|------|
| 200 | 成功 | — |
| 402 | 计费/积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 1002 | 缺参数或认证失败 | 检查必填参数与 API Key |
| 1003 | 上游 Amazon Ads 调用失败 | 稍后重试 |
| 1004 | 授权记录不存在或不属于当前用户 | 核对 profileId / authRecordId |
| 1005 | profileId 权限校验失败 | 核对 profileId 归属 |

错误响应：
```json
{"errcode": 1002, "errmsg": "缺少 accountName（账户显示名，必填非空）"}
```

---

## curl 示例

```bash
export KEY=$LINKFOXAGENT_API_KEY
BASE=https://tool-gateway.linkfox.com

# 1. 生成授权 URL
curl -X POST $BASE/amazonAds/authorizeUrl -H "Authorization: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"region":"NA","accountName":"我的美国广告账号"}'

# 2. 列已授权
curl -X POST $BASE/amazonAds/authorizedStores -H "Authorization: $KEY" \
  -H "Content-Type: application/json" -d '{}'

# 3. 列 profile（refresh=true 穿透刷新）
curl -X POST $BASE/amazonAds/profiles -H "Authorization: $KEY" \
  -H "Content-Type: application/json" -d '{"refresh":true}'

# 4. 刷新令牌
curl -X POST $BASE/amazonAds/refreshToken -H "Authorization: $KEY" \
  -H "Content-Type: application/json" -d '{"profileId":1111111111}'

# 5. 查令牌
curl -X POST $BASE/amazonAds/storeTokens -H "Authorization: $KEY" \
  -H "Content-Type: application/json" -d '{"profileId":1111111111}'
```
