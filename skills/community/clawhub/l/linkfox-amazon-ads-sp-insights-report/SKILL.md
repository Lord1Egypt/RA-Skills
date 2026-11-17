---
name: linkfox-amazon-ads-sp-insights-report
description: 亚马逊广告 Sponsored Products（SP）洞察报告技能，统一获取 Audience 受众细分表现和 Search Term Impression Share/Rank 搜索词展示份额/排名两类 Amazon Ads Reporting API v1 beta 报告。自动完成 profile 到 advertiser account 映射、报告创建、状态轮询、多分片 CSV 下载和落盘。只有用户明确要求 SP 受众报告、SP 搜索词展示份额或展示份额排名时触发；普通 SP 搜索词表现报告、SB/SD/DSP 报告不得触发。本技能依赖 linkfox-amazon-ads-auth。
---

# Amazon Ads SP 洞察报告获取

两类 Sponsored Products 专项报告一站式获取：脚本经 `developerProxy` 传 `profileId`（服务端解析 token），自动完成 advertiser account 映射、报告创建、等待（通常约 2–10 分钟）、多分片 CSV 下载和落盘。
脚本使用 Amazon Reporting API v1 beta 允许的固定字段组合，不接受调用方自由拼接字段。Audience 与 Search Term Impression Share/Rank 的完整字段依据分别见 `references/sp-audience-reporting-v1.md` 和 `references/sp-search-impression-share-v1.md`。

**依赖 `linkfox-amazon-ads-auth`**（脚本启动自动检查；未安装时 exit 42，stderr 打 `DEPENDENCY_MISSING`）。

### ⚠️ 多账号场景：调用前必须解析好 profileId

用户经常只说自然语言（“美国站”“日本站”“我的店铺”），本 Skill 的所有入口都必须拿到数字 `profileId` 才能调用。按下列顺序处理，**不要跳过**：

1. 先调 `linkfox-amazon-ads-auth` 的 `authorized_stores.py`，拉出用户已授权的账号 × 站点清单。
2. 根据用户提到的站点匹配 `countryCode`：
   - **只有 1 个候选** → 静默使用对应 `profileId`；不要向用户播报该数字。
   - **≥ 2 个候选** → 必须用 `accountName` 向用户确认，禁止默认选择第一个。
   - **0 个候选** → 告知用户该站点未授权，引导使用 `linkfox-amazon-ads-auth` 完成授权。
3. **严禁**要求用户直接提供 `profileId` 数字。
4. **严禁**在账号有歧义时自行选择默认账号。

完整决策表见 `linkfox-amazon-ads-auth` SKILL.md 的多账号场景说明。

## 调用方式

- **API 端点**：`POST /amazonAds/developerProxy`（脚本内部按顺序调用三个 Ads v1 路径；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline] [--no-cache]`（可用脚本见下文）
- **成本约束**：本工具不消耗算力；同一会话、同一报告类型和同一参数组合默认只调用一次，成功结果缓存 24 小时。失败、未完成或空报告不得自动换日期、切换账号或连续试探。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-ads-sp-insights-report-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录；`<session>` 取自环境变量 `SESSION_ID`；禁止写入 `/tmp`，当前目录不可写则报错）
- 报告 CSV 分片写入同一会话的 `data/`；最终响应不暴露 Amazon 预签名 URL
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要
- 加 `--inline` 强制全量打印到 stdout（同样落盘）；加 `--no-cache` 强制重新获取

**读数据建议**：先看摘要和 `preview`；响应 JSON 用 `jq` / `ConvertFrom-Json` 按需抽取，完整报告行从 `dataFiles[].path` 指向的文件用 CSV 工具或 `Import-Csv` 读取，避免整份报告进入上下文。

## 解决认证和算力问题

发生以下情况时，按 `references/onboarding.md` 引导解决：

### 异常情况
- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`
- **响应 401 或 402 状态码**
- **响应提示算力、余额、套餐或额度不足**

## Core Concepts

- **覆盖范围**：只覆盖 Sponsored Products Audience 和 Search Term Impression Share/Rank 两类 Reporting API v1 beta 报告
- **一站式**：自动完成 advertiser account 映射 → 创建报告 → 等待生成 → 下载全部 CSV/gzip 分片 → 返回预览与文件路径
- **双入口、共享流程**：两个公开入口分别固定报告类型，共用 `reporting_v1_workflow.py`；不要直接执行共享模块
- **固定字段**：Agent 不选择 `fields`、`groupBy` 或自由过滤条件；脚本按对应 reference 构造 Amazon 官方兼容字段组合
- **账号标识分工**：`profileId` 用于后端选择当前用户授权；`advertiserAccountId` 默认由脚本查询并映射
- **v1 与 v3 边界**：普通曝光、点击、花费、转化类 SP 搜索词报告使用 `linkfox-amazon-ads-report` 的 `spSearchTerm`，不是本 Skill
- **Beta 约束**：Amazon 当前将 Reporting API v1 标为 open beta；账号开放范围、字段和限流可能变化

## 可用脚本

| 脚本 | 职责 |
|------|------|
| `get_sp_audience_report.py` | 一站式获取 SP Audience 受众细分表现；支持 ACCOUNT / CAMPAIGN / AD_GROUP 粒度 |
| `get_sp_search_impression_share.py` | 一站式获取 SP 搜索词展示份额与展示份额排名 |
| `check_auth_dependency.py` | 检测 `linkfox-amazon-ads-auth` 是否安装 |

完整参数、内部调用链和响应结构见 `references/api.md`。选择 Audience 时读 `references/sp-audience-reporting-v1.md`；选择 Search Impression Share 时读 `references/sp-search-impression-share-v1.md`。

## Agent 调用流程

Agent 收到“SP 受众”或“SP 搜索词展示份额”需求时，**必须**按下列顺序：

1. **定报告类型**：Audience 使用 `get_sp_audience_report.py`；展示份额/排名使用 `get_sp_search_impression_share.py`。一次只调用一个入口。
2. **查 reference**：读取对应报告 reference，确认字段含义、限制和展示重点。
3. **解析账号**：通过 Ads Auth Skill 按站点得到唯一 `profileId` 和 `region`；多候选时先向用户确认账号。
4. **确认日期与粒度**：创建模式必须有 `startDate` / `endDate`。未指定 `timeUnit` 时使用 `DAILY`；Audience 未指定 `detailLevel` 时使用 `ACCOUNT`。
5. **告知等待时间并调用**：说明 Amazon 通常需要约 2–10 分钟，然后运行选定入口。脚本会自动映射账号、创建、轮询和下载，不要手工拆成三次业务调用。
6. **处理结果**：`success=true` 时展示报告类型、日期、总行数、预览和全部文件路径；`totalRows=0` 是合法空报告。
7. **处理未完成**：`status=STILL_PROCESSING` 不是失败。先向用户确认是否继续，再使用 `resumeHint.params` 和 `--no-cache` 轮询同一 `reportId`，禁止创建重复报告。

## 默认条件（用户未指定时使用）

| 条件 | 默认规则 |
|------|---------|
| 报告类型 | 根据用户意图二选一；不同时拉取两类报告 |
| `startDate` / `endDate` | 不擅自猜测；用户未给日期时先询问 |
| `timeUnit` | `DAILY` |
| Audience `detailLevel` | `ACCOUNT` |
| `advertiserAccountId` | 不传，由脚本根据 `profileId` 自动映射 |
| `pollInterval` | 60 秒 |
| `maxAttempts` | 10；形成约 10 分钟客户端等待窗口 |
| 字段与过滤 | 使用脚本固定的官方兼容组合，不接受自定义 |

## 请求示例

### 1. SP Audience 报告

```bash
python scripts/get_sp_audience_report.py '{
  "profileId": 1234567890, "region": "NA",
  "startDate": "2026-08-01", "endDate": "2026-08-07",
  "timeUnit": "DAILY", "detailLevel": "ACCOUNT"
}'
```

### 2. SP Search Term Impression Share/Rank 报告

```bash
python scripts/get_sp_search_impression_share.py '{
  "profileId": 1234567890, "region": "NA",
  "startDate": "2026-08-01", "endDate": "2026-08-07",
  "timeUnit": "DAILY"
}'
```

### 3. 轮询已有 reportId（救回上次未完成报告）

根据原报告类型继续使用原入口；仅传 `profileId`、`region`、`reportId` 和轮询参数：

```bash
python scripts/get_sp_search_impression_share.py '{
  "profileId": 1234567890, "region": "NA",
  "reportId": "REPORT_ID",
  "pollInterval": 60, "maxAttempts": 20
}' --no-cache
```

## 响应格式

成功：

```json
{
  "success": true,
  "status": "COMPLETED",
  "reportId": "report-id",
  "reportKind": "audience",
  "totalRows": 42,
  "dataFiles": [{"part": 1, "path": "C:/.../part-01.csv", "rowCount": 42}],
  "preview": [{"audienceSegment.name": "In-market ..."}],
  "pollAttempts": 2,
  "elapsedSeconds": 60.2
}
```

- **失败**：`success=false`，并包含 `error`、脱敏后的 `details` 和 `_cacheable=false`。
- **未完成**：`status=STILL_PROCESSING`，并包含原 `reportId`、`resumeHint.mode=poll-only`、`resumeHint.params` 和 `_cacheable=false`。

## 调用原则

- 用户明确指定报告类型时只调用该类型，不擅自替换或同时生成另一份报告
- Search Impression Share 不得追加 campaign、adGroup、target、keyword、groupBy 或自定义 fields
- 参数中不得出现 access token、refresh token、LWA 密钥或自定义 Amazon 请求头；脚本会在联网前递归拒绝
- 报告失败时如实展示 Amazon 错误，不盲目换参数重建
- 报告仍在生成时复用同一 `reportId`；禁止因为等待较久创建重复报告
- 成功后展示 CSV 文件路径和必要预览，不展示完整 Token、内部授权记录或 Amazon 预签名 URL
- 客观呈现报告数据；除非用户要求，不主动扩展成商业决策建议

## 常见错误

| 状态 | 含义 | 建议 |
|------|------|------|
| `Missing or invalid parameter` | 缺少 profile、region 或创建日期 | 补齐对应 reference 要求的参数后再调 |
| `Unsupported parameter(s)` | 传了本报告不支持的字段或维度 | 删除不支持参数；不要绕过脚本固定字段组合 |
| `HTTP 401` | LinkFox Key 或 Amazon Ads 授权失效 | LinkFox 401 走 onboarding；上游 401 使用 Ads Auth 刷新授权 |
| `HTTP 403` | 当前 Ads 应用或账号未开放 Reporting API v1 | 检查 Ads API 应用与授权账号权限；不得用 v3 数据伪造结果 |
| `HTTP 429` | Amazon Ads 上游限流 | 保持每分钟级轮询，不密集重试 |
| `status=FAILED` | Amazon 报告生成失败 | 透传失败详情，不自动更换参数重建 |
| `status=STILL_PROCESSING` | 客户端等待窗口结束，但报告仍在生成 | 不是失败；向用户确认后用 `resumeHint.params` 继续原 reportId |
| `totalRows=0` | 报告成功但当期无数据 | 合法空结果，不自动扩大日期或切换账号 |
| exit 42 | 依赖 Skill 未安装 | 先安装或加载 `linkfox-amazon-ads-auth` |

## 日期与数据

- 创建报告时 `startDate` / `endDate` 必须使用 `YYYY-MM-DD`，且 `startDate <= endDate`
- `endDate` 不得晚于今天；使用当天可能得到尚未完整的数据，优先选择昨天或更早日期
- `DAILY` 返回 `date.value`；`SUMMARY` 返回 `dateRange.value`
- Audience 重点展示受众名称/类型/来源、国家、曝光、点击、花费、购买、销售额和 ROAS，并保留币种字段
- Search Impression Share 重点展示 `searchTerm.value`、`metric.impressionShare` 和 `metric.impressionShareRank`
- 完成报告可能包含多个分片；必须保留并展示全部 `dataFiles`

## Not Applicable

- 普通 SP 搜索词表现报告（曝光、点击、花费、销售、转化）→ `linkfox-amazon-ads-report` 的 `spSearchTerm`
- SP / SB / SD 常规 v3 报告 → `linkfox-amazon-ads-report`
- 广告活动、广告组、关键词、投放和预算实体管理 → `linkfox-amazon-ads-manager`
- 授权、账号选择与 token 刷新 → `linkfox-amazon-ads-auth`
- Sponsored Brands、Sponsored Display、Sponsored Television、Amazon DSP、Brand Analytics、Retail Analytics → 不在本 Skill

## Amazon Ads API 接口保护与重试指引

同一广告账号/profile 连续收到 Amazon Ads API 的 400、403、404 或 429 时，网关会返回 450、453、454 或 459 并短暂冷却。这些自定义状态码不是 Amazon 原生状态，也不表示封号；目的是避免持续异常或高频调用扩大广告账号风险。

| 状态与 message | 范围 | 触发与冷却 | 处理 |
|---|---|---|---|
| `450`：`400，请求异常，请优化您的参数` | 广告账号/profile+接口 | 60 秒内超过 3 次：5 分钟；10 分钟内超过 4 次：20 分钟 | 停止原参数重试，检查 profileId、region、实体/报告 ID、日期和请求体 |
| `453`：`403，店铺未授权，请先授权` | 广告账号/profile 全部接口 | 60 秒内超过 2 次：5 分钟；10 分钟内超过 4 次：30 分钟 | 停止该广告账号调用，检查 Ads 授权、应用权限、profile 归属和区域 |
| `454`：`404，资源不存在，请优化您的参数` | 广告账号/profile+接口 | 60 秒内超过 3 次：5 分钟；10 分钟内超过 4 次：30 分钟 | 确认资源 ID、所属 profile/区域、资源状态和接口路径 |
| `459`：`429限流中，请降低频率` | 广告账号/profile+接口 | 首次：15 秒；2 分钟内超过 2 次：30 秒；3 分钟内超过 4 次：2 分钟 | 降低并发、分页和轮询频率并逐级退避 |

- 立即停止自动或并发重试，不得通过换脚本或重复创建任务绕过保护；优先遵循 `retryAfter`、`blockedUntil`，没有时按表中时长说明。
- 450/453/454 必须先修正参数、授权或资源标识，冷却后最多谨慎重试一次；再次触发则停止调用。453 期间停止该广告账号/profile 全部 Ads API。
- 保留已有 `reportId` 等任务 ID；写操作结果不确定时先查询状态，不直接重放。
- 向用户先说明广告账号保护，再给原因、处理和等待时间。可回复：“为保护您的亚马逊广告账号安全，检测到 Amazon Ads API 连续返回{原因}，当前已进入短暂保护。请先{处理动作}，预计{等待时间}后再试；这不代表封号，也不是套餐或积分限制。”不要只说“LinkFox 限流”或“服务器繁忙”。

## 算力消耗规则

不消耗算力。

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
