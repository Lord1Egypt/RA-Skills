---
name: linkfox-amazon-store-report
description: 亚马逊店铺报告自动化获取。支持库存、订单、销售流量、财务结算等95+种报告的请求、下载、解压及本地下载服务。
---

# 亚马逊店铺报告获取（Amazon Store Report）

本技能提供亚马逊卖家后台报告的端到端自动化获取：请求 → 轮询 → 下载 → 解压 → 预览，支持 95+ 种报告类型。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 获取亚马逊卖家后台结构化报告：库存、订单、销售流量、财务结算、FBA、退货、Brand Analytics、ABA 搜索词等 95+ 种报告类型。
- 全流程自动化：请求报告 → 轮询 `processingStatus` → 下载（多为 gzip TSV）→ 解压 → 输出本地路径与本机限时 HTTP 下载链接。
- 支持自定义时间范围、轮询间隔、最大轮询次数等参数。

### ❌ 边界与限制

- **依赖 `linkfox-amazon-store-auth`**：授权、选店铺、令牌刷新属于依赖 skill，未安装则必须先安装，不得绕过依赖直接调 `/spApi/authorizeUrl`、`/spApi/storeTokens`、`/spApi/authorizedStores`。
- **令牌时效**：`accessToken` 1 小时过期，脚本内部自动取最新令牌。
- **速率限制**：Reports API 约 0.0222 req/s，默认 30s 轮询为安全间隔。
- **报告时效**：部分财务报告可能需要 10–30 分钟，需按需调大 `maxAttempts`。
- **路径白名单**：后端 `sp-api.developer-proxy.allowed-path-prefixes` 必须允许 `reports/2021-06-30/reports`。
- **报告失败不自动替代**：用户指定报告类型失败（`FATAL`、403 等）时，立即停止并告知用户，不得自动改拉其他报告类型。
- **不在范围内**：授权新店铺、列已授权店铺、刷新/查询令牌（用 `linkfox-amazon-store-auth`）；商品 listing 管理、订单处理、广告投放（由其他 skill 负责）。

## 执行流程

每次进入本技能都按以下步骤顺序执行。

### 步骤 1：依赖检查

- 【输入】无
- 【动作】检测 `linkfox-amazon-store-auth` 是否已安装：读取其 `SKILL.md`（仓库扁平目录 / `~/.claude/skills/` / `~/.cursor/skills/` / OpenClaw / Hermes 等路径），或运行 `python scripts/check_auth_dependency.py`（缺失时以 exit code `42` 退出，stderr 输出 `DEPENDENCY_MISSING:` 开头提示）。
- 【输出】依赖是否满足。未满足时优先尝试自动安装，否则引导用户前往 [LinkFox Skills](https://skill.linkfox.com/) 安装，**不得静默降级**。

### 步骤 2：选店铺与取令牌（委托依赖 skill）

- 【输入】已授权店铺列表
- 【动作】委托 `linkfox-amazon-store-auth`：调 `/spApi/authorizedStores` 让用户选店铺，调 `/spApi/storeTokens` 获取 `accessToken`（`scripts/get_report.py` 会自动完成取令牌）。
- 【输出】`accessToken`（与 `region` 匹配的店铺令牌）

### 步骤 3：识别报告类型

- 【输入】用户诉求（库存 / 订单 / 销售流量 / 财务 / FBA / Brand Analytics 等）与可选时间范围
- 【动作】匹配 `reportType` 枚举（完整清单见 [references/report-types.md](references/report-types.md)），确定 `marketplaceIds` 与可选 `reportOptions`。
- 【输出】`reportType` + `marketplaceIds` + 可选 `dataStartTime`/`dataEndTime`/`reportOptions`

### 步骤 4：请求与轮询报告

- 【输入】`sellerId`、`region`、`reportType`、`marketplaceIds` 等
- 【动作】运行 `scripts/get_report.py`：`POST /spApi/developerProxy`（`path=reports/2021-06-30/reports`，`method=POST`）创建报告 → 轮询 `processingStatus`（`IN_QUEUE` / `IN_PROGRESS` / `DONE` / `FATAL` / `CANCELLED`，默认 30s 间隔、20 次）。
- 【输出】`reportId` → `reportDocumentId`

### 步骤 5：下载与解压

- 【输入】`reportDocumentId`（来自步骤 4）
- 【动作】`POST /spApi/developerProxy`（`path=reports/2021-06-30/documents/{reportDocumentId}`，`method=GET`）取下载 URL → 下载（多为 gzip TSV）→ 解压。
- 【输出】`downloadPath`（本地绝对路径，已解压含文件名）、`fileName`、`localFileUri`（本机 `file://` URI）

### 步骤 6：本机下载服务

- 【输入】`downloadPath`（已解压文件本地路径，来自步骤 5）
- 【动作】默认启动短时本机 HTTP 服务（`serveExtractedFileHttpUrl` 开启），在 `serveSeconds` 计时结束后关闭。
- 【输出】`extractedFileHttpUrl`（本机限时 HTTP 直链，仅同机浏览器可下载已解压文件）、`extractedFileHttpServeSeconds`（默认 300，最少 10）

## 核心概念

- **Report Type（报告类型）**：亚马逊官方报告类型枚举，如 `GET_MERCHANT_LISTINGS_ALL_DATA`、`GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL`。完整列表见 [references/report-types.md](references/report-types.md)。
- **Marketplace ID**：区域内具体站点 ID，如 US = `ATVPDKIKX0DER`。
- **Report lifecycle**：请求报告 → 轮询 `processingStatus` → `DONE` 后拿到 `reportDocumentId` → 取下载 URL → 下载 → 解压。
- **Rate limits**：Reports API 约 0.0222 req/s；轮询需保留间隔（默认 30s）。

报告请求输入参数与输出字段详见 [references/api.md](references/api.md)（createReport 请求体字段、developerProxy 参数、错误码）。

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 [references/api.md](references/api.md)）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：

- 始终将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/<skill-name>-<timestamp>.json`（`<session>` 取自环境变量 `SESSION_ID`；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

### 脚本一览

- `scripts/get_report.py` ⭐ — 端到端自动化报告获取（**推荐**）
- `scripts/check_auth_dependency.py` — 检测依赖 skill `linkfox-amazon-store-auth` 是否已安装

## 使用示例

**1. 拉库存报告（推荐自动化流程）**

> "我要拉库存报告" / "pull inventory report"

```bash
python scripts/get_report.py '{
  "sellerId": "A1EC6SZ7XAMURH",
  "region": "NA",
  "reportType": "GET_MERCHANT_LISTINGS_ALL_DATA",
  "marketplaceIds": ["ATVPDKIKX0DER"]
}'
```

脚本自动完成取令牌 → 请求 → 轮询 → 下载 → 解压 → 输出 JSON，完成后给出 `extractedFileHttpUrl`、`downloadPath`、`fileName`、`localFileUri`。

**2. 自定义时间范围与轮询**

> "拉 2024-01-01 到 2024-01-31 的订单报告"

```bash
python scripts/get_report.py '{
  "sellerId": "A1EC6SZ7XAMURH",
  "region": "NA",
  "reportType": "GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL",
  "marketplaceIds": ["ATVPDKIKX0DER"],
  "dataStartTime": "2024-01-01T00:00:00Z",
  "dataEndTime": "2024-01-31T23:59:59Z",
  "pollInterval": 15,
  "maxAttempts": 40
}'
```

**3. 手工驱动（精细控制）**

通过 `/spApi/developerProxy` 手工驱动：`GET reports/2021-06-30/reports` 取现有报告；`POST` 创建新报告；`GET reports/2021-06-30/reports/{reportId}` 查状态；`GET reports/2021-06-30/documents/{reportDocumentId}` 取下载链接。详见 [references/api.md](references/api.md)。

## Marketplace ID 速查

| Region | Country | Marketplace ID |
|--------|---------|----------------|
| NA | United States | ATVPDKIKX0DER |
| NA | Canada | A2EUQ1WTGCTBG2 |
| NA | Mexico | A1AM78C64UM0Y8 |
| EU | United Kingdom | A1F83G8C2ARO7P |
| EU | Germany | A1PA6795UKMFR9 |
| FE | Japan | A1VC38T7YXB528 |

更多 marketplace ID 详见 [references/report-types.md](references/report-types.md)。

## 展示规则

1. **先依赖后业务**：依赖检查未通过前，不得开始任何报告相关调用。
2. **只呈现数据**：展示报告获取进度、下载路径、前几行预览；不做业务解读，不做主观商业建议。
3. **尊重用户选择的报告类型**：用户指定了报告类型就只拉那一种，不得擅自换其他类型。
4. **错误清晰**：报告失败（`FATAL` / 403 等）时，解释原因并把决定权交还用户；常见原因：`403 Unauthorized`（缺少 API 权限或未加入 Amazon Brand Registry）、`FATAL`（该店铺不支持此报告类型或数据不足）、Brand Analytics 类报告需品牌备案、Vendor 类报告仅限 Vendor 账号。
5. **安全**：日志中 accessToken 掩码展示。
6. **完成后展示地址与本机下载链接**：脚本成功结束后，必须把 `extractedFileHttpUrl`（已解压文件的本机 HTTP 下载，限时）、`downloadPath`（本地绝对路径）、`fileName` 与 `localFileUri` 告知用户；并说明「仅在运行脚本的同一台电脑、在服务保持时间内可用」。不要默认把 Amazon 源 URL 当作用户下载入口；仅在用户明确要求或排障需要时使用 `includeAmazonSourceUrl`。

## 用户表达与场景速查

**适用** — 亚马逊报告获取场景：

| 用户说 | 场景 |
|--------|------|
| "拉亚马逊库存报告" / "pull inventory report" | 库存报告 |
| "下载订单数据" / "download orders report" | 订单报告 |
| "获取销售流量报告" / "sales and traffic report" | 销售流量报告 |
| "拉财务结算报告" / "settlement report" | 财务结算报告 |
| "查 FBA 库存" / "FBA inventory report" | FBA 报告 |
| "拉某时间段的订单报告" / "orders from 2024-01-01 to ..." | 自定义时间范围 |
| "Brand Analytics 报告" / "ABA 搜索词报告" | 品牌分析报告 |

不适用场景见上方【能力边界】。

**边界判断**：本技能只负责「依赖检查 + 报告获取业务」，授权/令牌属于依赖 skill `linkfox-amazon-store-auth`；任何进入本技能的调用都要先跑执行流程步骤 1。

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

# Amazon 店铺报告 API 参考

本文档描述 **报告获取** 相关的 API。授权与令牌相关接口（`/spApi/authorizeUrl`、`/spApi/storeTokens`、`/spApi/refreshToken` 等）属于 **依赖 skill** `linkfox-amazon-store-auth`，请参考该 skill 的 `references/api.md`。

> ⚠️ **依赖提示**：在调用本 skill 接口前，请先确认 `linkfox-amazon-store-auth` 已安装（参见本 skill 的 `SKILL.md` 顶部 Prerequisites）。

## 调用约定

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}`（默认 `https://tool-gateway.linkfox.com`；可用 `STORE_API_BASE_URL` 或兼容旧名 `SPAPI_BASE_URL` 覆盖）
- **请求方式**：POST
- **Content-Type**：`application/json`
- **认证方式**：Header `Authorization: <api_key>`，读取环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY`（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## API 端点

### 1. Developer Proxy（转发亚马逊开放接口）

**Endpoint**: `/spApi/developerProxy`

报告相关的上游调用（列表 / 请求 / 查状态 / 取下载链接）都通过该代理接口转发。

**请求参数**（JSON）：

| 参数 | 类型 | 必填 | 说明 | 示例 |
|-----------|------|----------|-------------|---------|
| region | string | Yes | 区域代码：NA/EU/FE | "NA" |
| path | string | Yes | 上游 Reports 等 API 路径（不含域名与 developer-proxy/{region}/ 前缀） | "reports/2021-06-30/reports" |
| method | string | Yes | HTTP 方法：GET/POST/PUT/DELETE | "GET" |
| amzAccessToken | string | Yes | 访问令牌（来自 `/spApi/storeTokens`） | "Atza\|IwEBI..." |
| queryString | string | No | Query 参数（无 `?`） | "marketplaceIds=ATVPDKIKX0DER" |
| body | string | No | POST/PUT 请求体（JSON 字符串） | `"{\"reportType\":\"...\"}"` |
| contentType | string | No | Content-Type 头（默认 application/json） | "application/json" |

**响应**：

```json
{
  "errcode": 200,
  "errmsg": "ok",
  "httpStatus": 200,
  "contentType": "application/json",
  "body": "{\"reports\":[...]}"
}
```

**重要说明**：
- `path` 必须在白名单内（后端 `sp-api.developer-proxy.allowed-path-prefixes`）
- 默认白名单含 `reports/2021-06-30/reports`
- `amzAccessToken` 必须与 `region` 匹配的店铺令牌一致
- 速率限制按上游亚马逊接口端点执行

---

## createReport 请求体（`POST reports/2021-06-30/reports`）

`developerProxy` 的 `body` 为 **JSON 字符串**，反序列化后与 Amazon **CreateReport** 请求体一致。

### 通用字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| reportType | string | 是 | 报告类型枚举，见 `references/report-types.md` |
| marketplaceIds | array[string] | 是 | 站点 ID 列表（多数报告至少一个） |
| dataStartTime | string | 视报告 | ISO 8601；部分 schema 仅使用日期部分 `YYYY-MM-DD` |
| dataEndTime | string | 视报告 | 同上 |
| lastUpdatedDate | string | 视报告 | 部分 Vendor 报告要求，与日期字段组合以官方 schema 为准 |
| reportOptions | object | 视报告 | **Brand Analytics、销售流量、促销/优惠券、部分 Vendor** 等必填；键与枚举见各报告专页 |

### 与官方 JSON Schema 的对应关系

Amazon 在仓库 [amzn/selling-partner-api-models/schemas/reports](https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports) 中为 **带 JSON 结果包裹** 的报告提供了 Schema（含 `reportSpecification` 示例与结果字段定义）。

本 skill 在 `references/report-requests/` 下为 **每个 `*.json` 维护一份同名 `*.md`**，内容包括：

- 上游 Raw 链接与摘要说明  
- 从 schema 提取的 **`reportType`** 与 **`reportSpecification` 官方示例**（可直接作为 `body` 模板）  
- **`reportOptions`** 键表（若有）  
- 结果文档结构说明要点  

**入口索引**：[report-requests/README.md](./report-requests/README.md)  
**按 `reportType` 全覆盖（109 个）**：[report-requests/types/README.md](./report-requests/types/README.md)

> 大量 **Flat File**（订单、库存等 TSV）报告在官方仓库中**无**独立 `schemas/reports/*.json` 时，请求体通常为 `reportType` + `marketplaceIds` + 可选 `dataStartTime`/`dataEndTime`，详见 [Report type values](https://developer-docs.amazon.com/sp-api/docs/report-type-values)。

### 脚本参数映射（`scripts/get_report.py`）

| JSON 参数 | 写入 createReport 体 |
|-----------|------------------------|
| reportType | reportType |
| marketplaceIds | marketplaceIds |
| dataStartTime | dataStartTime |
| dataEndTime | dataEndTime |
| lastUpdatedDate | lastUpdatedDate |
| reportOptions | reportOptions（对象原样合并） |

---

## 与依赖 skill 的接力关系

下面是典型调用序列（本 skill + `linkfox-amazon-store-auth`）：

```
linkfox-amazon-store-auth/scripts/store_tokens.py    # 取 accessToken
           │
           ▼
linkfox-amazon-store-report/scripts/get_report.py    # 用 accessToken 拉报告
  1. POST /spApi/developerProxy (method=POST,  path=reports/2021-06-30/reports)
  2. POST /spApi/developerProxy (method=GET,   path=reports/2021-06-30/reports/{reportId})  # 轮询
  3. POST /spApi/developerProxy (method=GET,   path=reports/2021-06-30/documents/{reportDocumentId})
  4. 直接下载返回的 url 并解压
```

## 错误码

| errcode | 含义 | 建议动作 |
|---------|------|----------|
| 200 | 代理调用成功（还需看 `httpStatus`） | 继续解析 `body` |
| 1002 | 缺参数或认证失败 | 检查必填参数与 API key |
| 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 1003 | 第三方服务调用失败 | 稍后重试 |
| 1005 | path 不在白名单 | 联系后端加白名单 |

### Developer Proxy 上游状态码

调用成功（`errcode=200`）后必须再检查 `httpStatus`：

| httpStatus | 含义 | 建议动作 |
|------------|------|----------|
| 200 | 成功 | 正常解析 `body` |
| 202 | 已接受（创建报告后返回） | 拿到 reportId 进入轮询 |
| 400 | 参数错误 | 检查 reportType / marketplaceIds |
| 403 | 未授权 | 检查 accessToken、店铺权限、品牌备案 |
| 404 | 资源不存在 | 核对 reportId/reportDocumentId |
| 429 | 请求过快 | 指数退避重试 |
| 500 | 上游错误 | 延时重试 |

---

## curl 示例

### 列出现有报告

```bash
curl -X POST https://tool-gateway.linkfox.com/spApi/developerProxy \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "region": "NA",
    "path": "reports/2021-06-30/reports",
    "method": "GET",
    "amzAccessToken": "Atza|IwEBI...",
    "queryString": "reportTypes=GET_MERCHANT_LISTINGS_ALL_DATA&marketplaceIds=ATVPDKIKX0DER"
  }'
```

### 请求新报告

```bash
curl -X POST https://tool-gateway.linkfox.com/spApi/developerProxy \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "region": "NA",
    "path": "reports/2021-06-30/reports",
    "method": "POST",
    "amzAccessToken": "Atza|IwEBI...",
    "body": "{\"reportType\":\"GET_MERCHANT_LISTINGS_ALL_DATA\",\"marketplaceIds\":[\"ATVPDKIKX0DER\"]}",
    "contentType": "application/json"
  }'
```

### 查询报告状态

```bash
curl -X POST https://tool-gateway.linkfox.com/spApi/developerProxy \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "region": "NA",
    "path": "reports/2021-06-30/reports/<reportId>",
    "method": "GET",
    "amzAccessToken": "Atza|IwEBI..."
  }'
```

### 获取下载链接

```bash
curl -X POST https://tool-gateway.linkfox.com/spApi/developerProxy \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "region": "NA",
    "path": "reports/2021-06-30/documents/<reportDocumentId>",
    "method": "GET",
    "amzAccessToken": "Atza|IwEBI..."
  }'
```

---

## 报告类型索引

完整列表见 `references/report-types.md`（95+ 种）。精简摘要见 `references/report-types-basic.md`。

**带 schema 的请求/结果格式**：`references/report-requests/README.md`（与 [GitHub schemas/reports](https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports) 一一对应）。
