---
name: linkfox-amazon-store-auth
description: 亚马逊店铺授权与管理。提供完整的店铺授权流程、令牌刷新、已授权店铺查询及访问令牌获取能力。
---

# 亚马逊店铺授权与管理（Amazon Store Auth）

本 skill 负责亚马逊卖家店铺的 OAuth 授权、已授权店铺列表、访问令牌获取与刷新，是拉取报告、查询库存、同步订单等所有下游操作的前置依赖。请求参数与响应字段详见 [references/api.md](references/api.md)，完整授权流程见 [references/authorization-flow.md](references/authorization-flow.md)，快速上手见 [references/quick-start.md](references/quick-start.md)。

> 相关 skill：若用户需要拉取亚马逊店铺报告（库存/订单/销售/财务报告等），请切换到 `linkfox-amazon-store-report`，该 skill 依赖本 skill 提供的授权与令牌能力。

## 能力边界

### ✅ 能力范围

- 生成亚马逊卖家授权链接，引导用户完成 OAuth 授权。
- 查询当前用户已授权的亚马逊店铺列表（sellerName / sellerId / region）。
- 获取指定店铺的访问令牌（accessToken / refreshToken / expiresIn）。
- 刷新过期令牌，续签新的 accessToken。
- 作为下游 skill 的前置依赖，负责"选店 → 取令牌"标准流程。

### ❌ 边界与限制

- **sellerName 必填**：调用 `/spApi/authorizeUrl` 前必须向用户询问并传入非空 `sellerName`，用于在已授权店铺列表中区分账号；不允许带空值调用。
- **令牌有效期**：`accessToken` 通常 1 小时过期，使用前需检查并按需刷新；`refreshToken` 失效后需重新授权。
- **区域专属**：每次店铺授权都与具体区域（NA/EU/FE）绑定，同一卖家在不同区域需分别授权。
- **用户隔离**：用户只能查看/管理自己授权的店铺。
- **回调白名单**：系统回调 URL 必须在授权方（紫鸟）处加白名单。
- **不在范围内**：拉取亚马逊报告（用 `linkfox-amazon-store-report`）；产品 listing 管理、订单处理、库存管理、广告投放由其他 skill 负责。

## 执行流程

### 流程一：新店铺授权

**步骤 1：获取授权链接**
- 【输入】`region`（默认 NA）、`sellerName`（必填，向用户询问非空店铺名）
- 【动作】调用 `POST /spApi/authorizeUrl`，传入 `region` 与 `sellerName`
- 【输出】`authorizeUrl`（Amazon 授权链接）

**步骤 2：用户浏览器授权**
- 【输入】`authorizeUrl`
- 【动作】把链接给用户，让其在浏览器打开并完成 Amazon 授权同意
- 【输出】Amazon 回调系统服务端，系统自动保存授权记录与令牌

**步骤 3：验证授权成功**
- 【输入】无
- 【动作】调用 `POST /spApi/authorizedStores`
- 【输出】已授权店铺列表，确认新店铺已出现（sellerName / sellerId / region）

### 流程二：为下游操作准备令牌（标准前置流程）

当用户提出任何涉及卖家后台数据的请求（拉报告、查库存、看订单等），本 skill 负责前置的"选店 → 取令牌"流程，具体业务由下游 skill 接手。

**步骤 1：列出已授权店铺**
- 【输入】无
- 【动作】调用 `POST /spApi/authorizedStores`
- 【输出】店铺列表（sellerName / sellerId / region）

**步骤 2：选择店铺**
- 【输入】店铺列表
- 【动作】若有多家店铺，请用户明确选哪一家
- 【输出】确定的 `sellerId` 与 `region`

**步骤 3：获取该店铺令牌**
- 【输入】`sellerId`、`region`
- 【动作】调用 `POST /spApi/storeTokens`；若 `expiresIn` 过短或令牌已过期，先调用 `POST /spApi/refreshToken` 续签
- 【输出】`accessToken`（及 `refreshToken` / `expiresIn`）

**步骤 4：交付下游 skill**
- 【输入】`accessToken`
- 【动作】把 `accessToken` 交给下游 skill（如 `linkfox-amazon-store-report`）
- 【输出】下游 skill 使用令牌执行具体业务

## 核心概念

Selling Partner API 是亚马逊为卖家提供的官方接口。本 skill 负责 OAuth 2.0 授权流程与令牌生命周期管理：

- **授权流程**：生成授权 URL → 用户在 Amazon 完成授权 → Amazon 回调并附带授权码 → 系统用授权码换取令牌 → 令牌安全保存。
- **店铺名（`sellerName`）必填**：调用 `/spApi/authorizeUrl` 前必须向用户询问并获取一个清晰、非空的店铺名，用于在已授权店铺列表中标记该账号；不要留空或使用空白字符串。
- **令牌生命周期**：`accessToken` 通常 1 小时过期；`refreshToken` 用于在不重新授权的前提下续签新的 `accessToken`。

**支持区域**：

| 代码 | 名称 | 覆盖市场 |
|------|------|----------|
| NA | 北美 | 美国、加拿大、墨西哥 |
| EU | 欧洲 | 英国、德国、法国、意大利、西班牙、荷兰等 |
| FE | 远东 | 日本、澳大利亚、新加坡、印度 |

默认区域为 NA，用户未指定时使用 NA。

## 调用方式

- **API 端点**：`POST /spApi/{authorizeUrl|storeTokens|authorizedStores|refreshToken}`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；失败/空结果不得自动连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- 始终将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/<skill-name>-<timestamp>.json`（`<session>` 取自环境变量 `SESSION_ID`；禁止写入 /tmp，当前目录不可写则报错）。
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout。
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数、最大列表字段的长度 + 前 3 条样本）。
- 加 `--inline` 强制全量打印到 stdout（同样落盘）。

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

### 示例 1：授权新店铺
> 「我要授权我的亚马逊北美站点」

1. 询问店铺名 `sellerName`（若用户未提供），说明这只是在 LinkFox 里识别店铺的标签，建议与 Seller Central 后台名字保持一致。
2. 调用 `/spApi/authorizeUrl`，传入 `region` 与 `sellerName`。
3. 把返回的 `authorizeUrl` 给用户，让其在浏览器中打开。
4. 用户在 Amazon 完成授权 → Amazon 回调系统 → 系统自动保存授权。
5. 可选：调用 `/spApi/authorizedStores` 确认授权成功。

### 示例 2：查看已授权店铺
> 「列一下我已授权的亚马逊店铺」

1. 调用 `/spApi/authorizedStores`。
2. 展示店铺列表（sellerName / sellerId / region），按 sellerId、region 排序。

### 示例 3：刷新过期令牌
> 「我店铺的令牌过期了，帮我刷新」

1. 调用 `/spApi/refreshToken`，传入 `sellerId`（可选 `region`）。
2. 返回新的 `accessToken` / `refreshToken`，数据库自动更新。

### 示例 4：查询店铺令牌
> 「获取北美站点 A123 店铺的访问令牌」

1. 调用 `/spApi/storeTokens`，传入 `sellerId` 与 `region`。
2. 返回全部令牌信息，供下游业务调用。

## 展示规则

1. **先有店铺名再生成授权链接**：若用户未提供 `sellerName`，必须先问，不允许带空值调用 `/spApi/authorizeUrl`。
2. **只呈现数据**：展示授权结果、店铺列表、令牌信息即可，不做业务建议。
3. **安全意识**：不要明文显示完整的 `accessToken`/`refreshToken`，只展示前 10 个字符等掩码形式。
4. **清晰引导**：返回授权链接时，明确告知用户在浏览器中打开并完成授权。
5. **错误说明**：授权失败时，基于错误码解释原因并给出建议。
6. **成功确认**：授权完成后与用户确认，可选择展示该店铺基本信息。

## 用户表达与场景速查

**适用** —— 授权与令牌管理场景：

| 用户说 | 场景 |
|--------|------|
| "授权我的亚马逊店铺" / "Authorize my Amazon store" | 新店铺授权 |
| "看看已授权的亚马逊店铺" / "Show my authorized stores" | 列出已授权店铺 |
| "令牌过期了" / "My token expired" | 刷新令牌 |
| "获取 XXX 店铺的访问令牌" / "Get access token for store" | 查询店铺令牌 |
| "绑定我的亚马逊账号" / "Connect my Amazon seller account" | 新店铺授权 |

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

# 亚马逊店铺授权 API 参考

本文档描述授权与店铺/令牌管理相关的 API。若需经网关代理拉取报告或 Listing 单条查询等，请参考 `linkfox-amazon-store-report`、`linkfox-amazon-store-listings` skill。

## 调用规范

- **Base URL**：`${LINKFOX_TOOL_GATEWAY}`（默认 `https://tool-gateway.linkfox.com`；可用 `LINKFOX_TOOL_GATEWAY` 覆盖，兼容旧名 `STORE_API_BASE_URL` / `SPAPI_BASE_URL`）
- **请求方式**：所有接口均为 POST
- **Content-Type**：`application/json`
- **认证方式**：Header `Authorization: <api_key>`，API key 优先读取环境变量 `LINKFOX_AGENT_API_KEY`，未设置时回退到兼容旧名 `LINKFOXAGENT_API_KEY`（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 接口列表

### 1. 获取授权链接

**端点**：`/spApi/authorizeUrl`

**请求参数**（JSON）：

| 参数 | 类型 | 必填 | 说明 | 示例 |
|-----------|------|----------|-------------|---------|
| region | string | 是 | 区域代码：NA / EU / FE | "NA" |
| sellerName | string | **是** | 店铺展示名（店铺名）— **必填，非空**；用于在已授权店铺列表中识别账号 | "My Store" |

**响应**：

```json
{
  "authorizeUrl": "https://sellercentral.amazon.com/apps/authorize/consent?..."
}
```

> 说明：授权完成后的回调由 Amazon 直接回调服务端内部接口处理，属于系统内部流程，不作为本 skill 的用户调用接口。

---

### 2. 查询已授权店铺列表

**端点**：`/spApi/authorizedStores`

**请求参数**：无（使用当前用户上下文）

**响应**：

```json
{
  "stores": [
    {
      "sellerName": "My Store",
      "sellerId": "A1234567890",
      "region": "NA"
    }
  ],
  "total": 1
}
```

---

### 3. 刷新令牌

**端点**：`/spApi/refreshToken`

**请求参数**（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|-----------|------|----------|-------------|
| sellerId | string | 是 | Seller ID |
| region | string | 否 | 区域代码（精确匹配可选） |

**响应**：

```json
{
  "authRecordId": 123,
  "accessToken": "Atza|IwEBIA...",
  "refreshToken": "Atzr|IwEBIJ...",
  "tokenType": "bearer",
  "expiresIn": "3600",
  "message": "Token refreshed and updated"
}
```

---

### 4. 查询店铺令牌

**端点**：`/spApi/storeTokens`

**请求参数**（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|-----------|------|----------|-------------|
| sellerId | string | 是 | Seller ID |
| region | string | 是 | 区域代码 |

**响应**：

```json
{
  "sellerId": "A1234567890",
  "region": "NA",
  "authRecordId": 123,
  "accessToken": "Atza|IwEBIA...",
  "refreshToken": "Atzr|IwEBIJ...",
  "tokenType": "bearer",
  "expiresIn": "3600"
}
```

返回的 `accessToken` 可交给下游 skill（如 `linkfox-amazon-store-report`）用于调用亚马逊开放接口。

---

## 错误码

| errcode | 含义 | 建议动作 |
|---------|------|----------|
| 200 | 成功 | 正常解析 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 1002 | 缺参数或认证失败 | 检查必填参数与认证 |
| 1003 | 第三方服务调用失败 | 稍后重试，检查网络与白名单 |
| 1004 | 授权记录不存在或不属于当前用户 | 核对 sellerId/region 或重新授权 |

**错误响应示例**：

```json
{
  "errcode": 1002,
  "errmsg": "Missing required parameter: region"
}
```

---

## curl 示例

### 获取授权链接

```bash
curl -X POST https://tool-gateway.linkfox.com/spApi/authorizeUrl \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"region": "NA", "sellerName": "My Store"}'
```

### 查询已授权店铺列表

```bash
curl -X POST https://tool-gateway.linkfox.com/spApi/authorizedStores \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json"
```

### 刷新令牌

```bash
curl -X POST https://tool-gateway.linkfox.com/spApi/refreshToken \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sellerId": "A1234567890", "region": "NA"}'
```

### 查询店铺令牌

```bash
curl -X POST https://tool-gateway.linkfox.com/spApi/storeTokens \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sellerId": "A1234567890", "region": "NA"}'
```

---

## 重要事项

1. **令牌安全**：不要打印完整 accessToken/refreshToken，仅展示前 10 字符掩码。
2. **令牌生命周期**：accessToken 1 小时过期，使用前检查并按需刷新。
3. **区域专属**：同一卖家在不同区域需要分别授权。
4. **用户隔离**：所有 API 都强制用户级访问控制。
5. **回调白名单**：系统回调 URL 必须在授权提供方（紫鸟）处加白名单。

完整授权流程与实现细节：见 `authorization-flow.md`。
