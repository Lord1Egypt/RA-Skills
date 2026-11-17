---
name: linkfox-amazon-ads-report
description: 一站式获取亚马逊 SP、SB、SD 的全量广告报告，自动完成报告的创建、下载和解压，直接返回结构化数据。
---


# Amazon Ads 报告获取

报告一站式获取：脚本自动完成报告的创建、等待（约 2–10 分钟）、下载和解压，直接返回结构化数据。脚本不做"选哪些列 / 怎么分组"的业务判断，由 agent 先查 `references/report-types/` 下对应的 `.md`，再显式传给脚本。完整参数、响应、错误码见 [references/api.md](references/api.md)。**依赖 `linkfox-amazon-ads-auth`**（未安装时 exit 42，stderr 打 `DEPENDENCY_MISSING`）。

## 能力边界

### ✅ 能力范围

- 覆盖 Sponsored Products (SP) / Sponsored Brands (SB) / Sponsored Display (SD) 全部报告类型（以 `references/report-types/` 下存在的 `.md` 为准）。
- 一站式：脚本内部完成报告创建 → 等待生成 → 下载 → 解压，调用方只需等最终结果。
- 支持全链路模式（创建+轮询+下载）与仅轮询模式（用 `reportId` 救回上次超时）。

### ❌ 边界与限制

- **未覆盖**：Sponsored Television (ST) / Amazon DSP；Brand Analytics / Retail Analytics / Attribution 报告；报告删除/修改/定时任务；授权与 token（用 `linkfox-amazon-ads-auth`）；实体元数据管理（用 `linkfox-amazon-ads-manager`）。
- **多账号必须澄清**：所有脚本都要数字 `profileId`。先调 `linkfox-amazon-ads-auth` 的 `authorized_stores.py` 拉授权账号清单，按站点（美国→`US`）匹配候选 profile：只有 1 个候选静默取用；≥2 个候选**必须向用户澄清**用哪个账号；0 个候选引导去授权。严禁让用户直接报 profileId 数字，严禁歧义下挑第一个。完整决策表见 `linkfox-amazon-ads-auth` SKILL.md 的 Usage Scenarios 第 4 节。
- **成本约束**：失败/空结果不得自动换关键词、翻页或连续试探；需继续检索时先向用户说明会产生额外消耗。
- **日期上限**：多数报告 31 天；`sbPurchasedProduct` 731 天；GrossAndInvalids 系列 365 天（以 frontmatter `dateRange.maxSpanDays` 为准）。回溯窗口 SP 默认 95 天、SB 60 天、GrossAndInvalids 365 天（以 `dateRange.dataRetentionDays` 为准）。
- **数据延迟约 12 小时**；`endDate >= 今天` 脚本 stderr 警告但不拦截。

## 执行流程

### 步骤 1：解析 profileId

- 【输入】用户自然语言（如"美国站""日本站"）。
- 【动作】调 `linkfox-amazon-ads-auth` 的 `authorized_stores.py` 拉授权账号清单，按 `countryCode` 匹配候选 profile；1 个静默取用，≥2 个向用户澄清，0 个引导授权。
- 【输出】确定的 `profileId`（不向用户播报数字）与 `region`（`NA`/`EU`/`FE`）。

### 步骤 2：选 reportTypeId 并查 reference

- 【输入】用户意图（如"上周花费""哪个商品卖得好""用户搜什么词找到我"）。
- 【动作】按意图选 `reportTypeId`（如 `spCampaigns`/`spAdvertisedProduct`/`spSearchTerm`），打开 `references/report-types/<adProduct-dir>/<reportTypeId>.md`，从 frontmatter 取 `adProduct`/`groupBy`/`timeUnit`/`format`/`dateRange`/`filters`，从 Base metrics 表取允许的全部列名。
- 【输出】`adProduct` / `groupBy` / 可用 `columns` / `timeUnit` 可选值 / 日期约束。

### 步骤 3：咨询可定制条件

- 【输入】步骤 2 的元数据。
- 【动作】向用户询问 `timeUnit`（DAILY/SUMMARY）、`columns` 扩展（归因列、视频指标、newToBrand 等）、`filters`（campaignStatus/keywordType/adStatus 等）。用户答"默认/随便"则跳过，用默认规则。
- 【输出】用户确认的 `timeUnit`/`columns`/`filters`，或"使用默认"信号。

### 步骤 4：构造入参

- 【输入】步骤 2 元数据 + 步骤 3 用户选择 + 日期范围。
- 【动作】按默认规则补全：日期跨度 ≤ 7 天用 `DAILY`（必含 `date`），> 7 天用 `SUMMARY`（必含 `startDate`+`endDate`）；追加报告主键字段（参考 groupBy 主键，如 campaignId+campaignName / advertisedAsin+advertisedSku / searchTerm）；基础指标 `impressions`/`clicks`/`cost`；仅当用户提到销售/转化/ROI/ACOS 时追加归因列（`sales7d`/`purchases7d`/`acosClicks7d`/`roasClicks7d`，以 Base metrics 存在者为准）；`groupBy` 取 frontmatter 第一个值；`filters` 默认不加。
- 【输出】完整的脚本入参 JSON（含 `adProduct`/`groupBy`/`columns` 三个必填字段）。

### 步骤 5：调脚本并处理结果

- 【输入】步骤 4 的入参 JSON + `profileId`/`region`。
- 【动作】运行 `python scripts/get_report.py '<JSON>'`；脚本完成创建→轮询→下载→解压。
- 【输出】成功返回 `reportId`、本地 `downloadPath` 与 `extractedFileHttpUrl`（约 5 分钟有效）；超时返回 `status=STILL_PROCESSING`（exit 2）含 `resumeHint.params`，询问用户是否继续等；失败返回 `error` 与 `httpStatus`。

## 核心概念

- **元数据 vs. 运行参数**：每个报告类型的可用字段（timeUnit/groupBy/filters/列名）集中在 `references/report-types/<adProduct-dir>/<reportTypeId>.md`；脚本运行参数（等待间隔、访问链接时效等）见本文件与 [references/api.md](references/api.md)。
- **单脚本 `get_report.py`**：覆盖 SP / SB / SD 全部 adProduct；传入 `reportId` 即跳过创建，仅轮询下载，救回上次超时。

## 可用脚本

| 脚本 | 职责 |
|------|------|
| `get_report.py` ⭐ | 一站式执行。必填 `adProduct`/`groupBy`/`columns`，由 agent 从 report-types/ 提取后传入 |
| `check_auth_dependency.py` | 检测 linkfox-amazon-ads-auth 是否安装 |

## 调用方式

- **API 端点**：`POST /amazonAds/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 [references/api.md](references/api.md)）。
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`。
- **超时即未完成**：`status=STILL_PROCESSING`（exit 2）时必须询问用户是否继续等（A. 再等 ~20 分钟 maxAttempts=60 / B. ~1 小时 maxAttempts=120 / C. 先停），用 `resumeHint.params` 切到仅轮询模式续跑。
- **自动恢复**：Amazon 对同参数请求返回 HTTP 425 `duplicate of <uuid>` 时，脚本自动解析老 reportId 并转为轮询，无需重试。

## 大响应处理

- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/<skill-name>-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录；`<session>` 取自 `SESSION_ID`；禁止写入 /tmp，不可写则报错）。
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout；> 8 KB：落盘后 stdout 只输出摘要（顶层字段、计数如 `total`/`costToken`、最大列表长度 + 前 3 条样本）。
- 加 `--inline` 强制全量打印到 stdout（同样落盘）。需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 JSON 按需抽取，避免整份 JSON 进入上下文。

## 使用示例

### 1. SP 广告活动报告（最常见）

```bash
python scripts/get_report.py '{
  "profileId": 1234567890, "region": "NA",
  "reportTypeId": "spCampaigns",
  "adProduct": "SPONSORED_PRODUCTS",
  "groupBy": ["campaign"],
  "columns": ["date","campaignId","campaignName","impressions","clicks","cost"],
  "startDate": "2026-04-27","endDate": "2026-05-03",
  "timeUnit": "DAILY"
}'
```

### 2. SP 搜索词报告（含归因）

```bash
python scripts/get_report.py '{
  "profileId": 1234567890, "region": "NA",
  "reportTypeId": "spSearchTerm",
  "adProduct": "SPONSORED_PRODUCTS",
  "groupBy": ["searchTerm"],
  "columns": ["searchTerm","keyword","matchType","impressions","clicks","cost",
              "sales7d","sales14d","purchases7d","acosClicks14d","roasClicks14d",
              "startDate","endDate"],
  "startDate": "2026-04-01","endDate": "2026-04-30",
  "timeUnit": "SUMMARY",
  "filters": [{"field":"keywordType","values":["BROAD","PHRASE","EXACT"]}]
}'
```

### 3. SD 广告活动报告

```bash
python scripts/get_report.py '{
  "profileId": 1234567890, "region": "NA",
  "reportTypeId": "sdCampaigns",
  "adProduct": "SPONSORED_DISPLAY",
  "groupBy": ["campaign"],
  "columns": ["date","campaignId","campaignName","impressions","clicks","cost","purchases","sales"],
  "startDate": "2026-04-27","endDate": "2026-05-03",
  "timeUnit": "DAILY"
}'
```

### 4. 轮询已有 reportId（救回超时）

```bash
python scripts/get_report.py '{
  "profileId": 1234567890, "region": "NA",
  "reportId": "7df1ef5d-45ba-40cc-b607-ff2148cf4f5e",
  "maxAttempts": 60, "pollInterval": 30
}'
```

## 展示规则

1. **如实呈现数据**：以结构化表格展示报告行（campaign/asin/searchTerm 等主键 + impressions/clicks/cost/sales 等指标），不做主观商业建议。
2. **提供文件路径与链接**：成功后把 `downloadPath` 与 `extractedFileHttpUrl` 完整展示，并提醒访问链接约 5 分钟内有效，过期需重新拉取。
3. **不盲目重试**：报告失败（非 2xx 或 `status=FAILED`）时如实告知错误原因；超时（`STILL_PROCESSING`）不是失败，须询问用户是否继续等。
4. **空数据不等于报错**：账号当期无投放时报告会成功生成，JSON 可能为 `[]` 或指标全 0，需说明。
5. **不擅自替换 reportTypeId**：用户指定了就只拉那一种。

## 用户表达与场景速查

**适用** —— 亚马逊广告报告拉取：

| 用户说 | 场景 / reportTypeId |
|--------|------|
| "上周广告花费"、"广告活动效果" | 广告活动级 `spCampaigns`/`sbCampaigns`/`sdCampaigns` |
| "哪个投放商品卖得好" | 投放商品 `spAdvertisedProduct` |
| "用户搜什么词找到我" | 搜索词 `spSearchTerm` |
| "关键词表现" | 定向/关键词 `spTargeting` |
| "购买了我的商品" | 购买商品 `spPurchasedProduct`/`sbPurchasedProduct` |
| "广告组数据" | 广告组 `sbAdGroup` |
| "流量异常 / 无效流量" | GrossAndInvalids 系列 |
| "Prompt 扩展报告" | `spPromptAdExtension`/`sbPromptAdExtension` |
| "继续等上次那个报告" | 仅轮询模式（传 `reportId`） |

不适用场景见上方【能力边界】。

## 常见错误

| 状态 | 含义 | 建议 |
|------|------|------|
| `Missing required parameters: adProduct/groupBy/columns` | 未显式传入三必填 | 回到执行流程步骤 2，从 `.md` 读出并补上 |
| `HTTP 401` | accessToken 过期 | 调 ads-auth 的 `refresh_token.py` 后重试 |
| `HTTP 403` | 未关联广告账户或权限不足 | 到 Amazon Ads 后台检查经理账户/广告账户关联 |
| `HTTP 400 "must not exceed maximum range"` | 日期跨度超限 | 拆分拉取后本地合并；上限看 frontmatter `dateRange.maxSpanDays` |
| `HTTP 400` 含 `columns`/`groupBy` 校验错 | 列名拼写错/不匹配 | 对照 `.md` Base metrics 表核对 |
| `status=FAILED` 含 `failureReason` | 上游生成失败 | 多为日期窗口或权限问题，按 failureReason 处理 |
| `status=STILL_PROCESSING` (exit 2) | 轮询窗口耗尽但报告仍在生成 | 非失败。用 `resumeHint.params` 切到仅轮询模式续跑 |
| `HTTP 425 "duplicate of"` | 同参数已有在跑的报告 | 脚本自动转为轮询该老 reportId，无需干预 |
| exit 42 | 依赖 skill 未安装 | 先装 `linkfox-amazon-ads-auth` |

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

# linkfox-amazon-ads-report — 参数与字段参考

Amazon Ads 报告自动化获取（SP / SB 覆盖；SD / ST / DSP 暂未覆盖）。授权见 `linkfox-amazon-ads-auth`；广告管理见 `linkfox-amazon-ads-manager`。

> **📌 报告类型的真相源**：每个 `reportTypeId` 的完整规格（可用 columns / groupBy / filters / timeUnit / 日期约束 / 官方示例）在 `references/report-types/<adProduct-dir>/<reportTypeId>.md`，**按 adProduct 分目录**：
> - `report-types/sp/`（Sponsored Products）
> - `report-types/sb/`（Sponsored Brands）
>
> 目录总览见 `report-types/index.md`。本文件仅给运行时脚本参数与通用规则。

## 支持的报告类型

完整列表见 `report-types/index.md` 及各 adProduct 子目录下的 `index.md`。常用快速索引：

| reportTypeId | 业务含义 | 文件 |
|--------------|---------|------|
| `spCampaigns` | 广告活动级（SP） | `report-types/sp/spCampaigns.md` |
| `spAdvertisedProduct` | 投放商品级（SP） | `report-types/sp/spAdvertisedProduct.md` |
| `spSearchTerm` | 搜索词级（SP） | `report-types/sp/spSearchTerm.md` |
| `spTargeting` | 定向/关键词级（SP） | `report-types/sp/spTargeting.md` |
| `sbCampaigns` / `sbAdGroup` / `sbAds` / ... | Sponsored Brands | `report-types/sb/*.md` |

## 输入参数

脚本支持两种模式：

- **全链路模式（默认）**：创建报告 → 轮询 → 下载。需要下表全部必填字段。
- **仅轮询模式**：入参中显式传入 `reportId`（见下方"可选流程参数"），跳过创建，只需 `profileId` / `region`，其余全部可省略。用于救回上次客户端超时但报告仍在跑的场景。

### 必填（全链路模式）

| 参数 | 类型 | 说明 |
|------|------|------|
| `profileId` | number | 从 ads-auth 获取 |
| `region` | string | `NA` / `EU` / `FE` |
| `reportTypeId` | string | 见 `report-types/index.md` 各 adProduct 子目录下的完整列表 |
| `adProduct` | string | 取自对应 `.md` 文件的 frontmatter（`SPONSORED_PRODUCTS` / `SPONSORED_BRANDS`）|
| `groupBy` | list | 取自对应 `.md` 文件的 frontmatter |
| `columns` | list | 取自对应 `.md` 文件 Base metrics 表的子集 |
| `startDate` | string | `YYYY-MM-DD`（含当天） |
| `endDate` | string | `YYYY-MM-DD`（含当天） |

### 可选业务参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `name` | `{reportTypeId}_{startDate}_{endDate}` | 报告显示名 |
| `timeUnit` | `SUMMARY` | `DAILY`（每天一行） / `SUMMARY`（整期一行） |
| `format` | `GZIP_JSON` | 响应文件格式 |
| `filters` | 空 | 过滤条件数组，字段与取值见对应 `.md` 文件 |

### 可选流程参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `reportId` | 无 | 若显式传入，脚本进入**仅轮询模式**：跳过创建步骤，直接对该 reportId 轮询与下载。此时只要 `profileId` / `region` + `reportId`，其他字段可省 |
| `pollInterval` | 30 | 轮询间隔秒 |
| `maxAttempts` | 20 | 最大轮询次数（默认 10 分钟上限） |
| `skipDepCheck` | false | 跳过依赖检查 |
| `serveExtractedFileHttp` | true | 是否启本机 HTTP 服务 |
| `serveHost` | `127.0.0.1` | 绑定地址（仅本机可访问） |
| `servePort` | 0 | 端口（0=系统分配） |
| `serveSeconds` | 300 | HTTP 服务存活秒 |
| `includeAmazonSourceUrl` | false | 响应中带预签名 URL |

## 日期限制

- **跨度上限**：以对应 `.md` 文件 frontmatter 的 `dateRange.maxSpanDays` 为准（多数 31 天；`sbPurchasedProduct` 731 天；GrossAndInvalids 系列 365 天）。超出返回 HTTP 400 `"must not exceed maximum range"`。
- **回溯上限**：以 `dateRange.dataRetentionDays` 为准（SP 多为 95 天，SB 60 天）。
- **数据延迟**：~12 小时；`endDate >= 今天` 脚本会 stderr 警告但不拦截。建议 `endDate <= 昨天`。

## 各报告类型的列

每个 reportTypeId 的完整 Base metrics 列表、allowed groupBy、filters 枚举值，统一在 `report-types/<adProduct-dir>/<reportTypeId>.md` 中维护：

- `.md` 的 **frontmatter** 提供 `adProduct` / `groupBy` / `timeUnit`（可选值）/ `format` / `filters` / `dateRange`
- **Base metrics 表**列出此报告类型支持的**全部列名**；调用方按业务需要选子集

归因窗口后缀约定：`_1d` / `_7d` / `_14d` / `_30d` 表示 1/7/14/30 天归因窗口（点击或曝光归因的销售额、订单量、件数等）。具体每个字段支持哪些窗口，以对应 `.md` 文件的 Base metrics 表为准（不是所有字段都有全部 4 个窗口版本）。

## 工作流与输出

脚本流程：依赖检查 → 取 token → 创建报告 → 等待生成（每 `pollInterval` 秒查询一次状态）→ 下载 GZIP_JSON（Amazon 预签名 URL 约 1 小时有效）→ 解压为可读 JSON → 通过本机 `127.0.0.1` 上的临时 HTTP 服务对调用方暴露（`serveSeconds` 后自动关闭）→ 输出调用结果 JSON（含本地文件路径与访问链接）。

`status` 枚举：`PENDING` / `PROCESSING` / `COMPLETED` / `FAILED`。

### 成功响应

```json
{
  "success": true,
  "reportId": "4ee811a0-6aaa-4ceb-9d31-d3bcecf85430",
  "status": "COMPLETED",
  "reportTypeId": "spCampaigns",
  "startDate": "2026-04-28", "endDate": "2026-05-04",
  "pollAttempts": 13, "elapsedSeconds": 255,
  "downloadPath": "C:/.../tmp/report-xxx.json",
  "extractedFileHttpUrl": "http://127.0.0.1:51234/report-xxx.json",
  "serveExpiresAt": "2026-05-06T14:54:03+08:00"
}
```

### 失败响应

**a) 创建阶段非 2xx**：
```json
{"error":"Upstream HTTP 400","httpStatus":400,
 "body":"{\"code\":\"400\",\"detail\":\"startDate to endDate range (32 days) must not exceed maximum range (31 days)\"}"}
```

**b) 报告生成失败**（`failureReason` 从上游透传）：
```json
{"success":false,"error":"Report generation failed with status=FAILED",
 "reportId":"4ee811a0-...","status":"FAILED",
 "failureReason":"Requested columns are not supported for this report type.",
 "pollAttempts":3}
```

**c) 轮询超时**（报告未坏，仅客户端等待窗口耗尽 — **exit code = 2**）：
```json
{
  "success": false,
  "status": "STILL_PROCESSING",
  "reportId": "4ee811a0-...",
  "reportTypeId": "spCampaigns",
  "profileId": 1234567890,
  "lastStatus": "PROCESSING",
  "pollAttempts": 20,
  "elapsedSeconds": 600,
  "message": "客户端已等 ~600 秒（20 次轮询）报告仍在 Amazon 侧生成，并未失败。用 reportId 切换到仅轮询模式即可继续等待。",
  "resumeHint": {
    "mode": "poll-only",
    "note": "传入 reportId + 更大的 maxAttempts 继续轮询同一份报告",
    "params": {"profileId": 1234567890, "region": "NA", "reportId": "4ee811a0-...", "maxAttempts": 60, "pollInterval": 30}
  }
}
```

调用方收到此响应应视为"未完成"而非"失败"，询问用户是否继续等待，直接把 `resumeHint.params` 作为入参续调 `get_report.py`。

## 错误码

| httpStatus / exit | 含义 | 建议 |
|-------------------|------|------|
| 200 | 成功 | 消费 `extractedFileHttpUrl` 或 `downloadPath` |
| 400 | 入参错（日期超限 / reportTypeId 非法 / columns 不适配） | 按 `detail` 修正 |
| 401 | accessToken 过期 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 402 | 积分或余额不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 403 | profileId 无权限 | 核对 profileId |
| 404 | reportId 不存在或已过期 | 重新发起报告 |
| 422 | columns / groupBy 与 reportTypeId 不适配 | 对照 `report-types/<adProduct-dir>/<reportTypeId>.md` 的 Base metrics / frontmatter 核对 |
| 425 | 同参数已有在跑的报告，Amazon 做了去重；body 形如 `"The Request is a duplicate of : <reportId>"` | **脚本自动解析该 reportId 并无缝转为轮询该老报告**，正常情况下无需干预；若调用方自行处理，也可把 reportId 拿出来，下次改用仅轮询模式（`{..., "reportId":"<uuid>"}`） |
| 429 | 限流（~30 req/min/profile） | 间隔 30s 重试 |
| `status=FAILED` | 上游生成失败 | 看 `failureReason` |
| `status=STILL_PROCESSING` (exit 2) | 客户端轮询窗口耗尽但报告仍在 Amazon 侧生成 | **非失败**。stdout 已输出 `reportId` 与 `resumeHint.params`。询问用户是否继续等，用 params 切到仅轮询模式续跑（maxAttempts=60 约 30 分钟 / =120 约 1 小时） |
| exit 42 | 依赖 skill 未安装 | 先装 `linkfox-amazon-ads-auth` |

## 调用示例

```bash
# 1. SP 广告活动汇总（DAILY，一周）
python get_report.py '{"profileId":1111111111,"region":"NA",
  "reportTypeId":"spCampaigns",
  "adProduct":"SPONSORED_PRODUCTS",
  "groupBy":["campaign"],
  "columns":["date","campaignId","campaignName","impressions","clicks","cost"],
  "startDate":"2026-04-27","endDate":"2026-05-03",
  "timeUnit":"DAILY"}'

# 2. SP 搜索词 + 多归因窗口 + 过滤仅看关键词匹配
python get_report.py '{"profileId":1111111111,"region":"NA",
  "reportTypeId":"spSearchTerm",
  "adProduct":"SPONSORED_PRODUCTS",
  "groupBy":["searchTerm"],
  "columns":["searchTerm","keyword","matchType","impressions","clicks","cost",
             "sales7d","sales14d","sales30d",
             "purchases7d","purchases14d","purchases30d",
             "acosClicks14d","roasClicks14d","startDate","endDate"],
  "startDate":"2026-04-01","endDate":"2026-04-30",
  "timeUnit":"SUMMARY",
  "filters":[{"field":"keywordType","values":["BROAD","PHRASE","EXACT"]}]}'

# 3. SP 投放商品 + 长时间等待 + 不启本机 HTTP
python get_report.py '{"profileId":1111111111,"region":"NA",
  "reportTypeId":"spAdvertisedProduct",
  "adProduct":"SPONSORED_PRODUCTS",
  "groupBy":["advertiser"],
  "columns":["advertisedAsin","advertisedSku","impressions","clicks","cost",
             "sales7d","acosClicks7d","roasClicks7d","startDate","endDate"],
  "startDate":"2026-04-01","endDate":"2026-04-30",
  "timeUnit":"SUMMARY",
  "maxAttempts":60,"pollInterval":20,"serveExtractedFileHttp":false}'

# 4. 仅轮询一个已有 reportId（救回上次超时）
python get_report.py '{"profileId":1111111111,"region":"NA",
  "reportId":"7df1ef5d-45ba-40cc-b607-ff2148cf4f5e",
  "maxAttempts":60,"pollInterval":30}'
```
