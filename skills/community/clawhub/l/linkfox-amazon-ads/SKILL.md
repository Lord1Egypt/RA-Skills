---
name: linkfox-amazon-ads
display_name: Linkfox 亚马逊广告
display_name_en: LinkFox Amazon Ads
description: 亚马逊广告（Amazon Ads）全链路一站式 AI 工具集，整合授权与令牌管理、SP/SB/SD 广告查询与创建修改、广告报告一站式获取 3 项子能力，覆盖授权→管理→报表全链路。
description_zh: 亚马逊广告全链路工具集，含 3 项子能力：①广告授权与令牌管理（linkfox-amazon-ads-auth）：OAuth 授权、一次绑定同账号所有站点 profile、令牌读写刷新；②广告管理（linkfox-amazon-ads-manager）：SP/SB/SD 查询与创建修改写操作，含活动/广告组/关键词/定向/创意/预算规则；③广告报告（linkfox-amazon-ads-report）：SP/SB/SD 全量报告一站式获取（自动创建下载解压）。manager/report 依赖 auth。需广告授权、查询/修改/调价或拉取报告时触发。
description_en: One-stop Amazon Ads AI toolkit integrating 3 sub-capabilities across the full authorization → management → reporting chain: ① Ads authorization & token management (linkfox-amazon-ads-auth) — LWA OAuth authorization, single authorization binding all marketplace profiles under one account, authorized-account/profile queries, accessToken read & refresh; ② Ads management (linkfox-amazon-ads-manager) — list queries and create/update operations across the SP/SB/SD product lines, covering campaigns/ad groups/keywords/negative keywords/product ads/targeting/creatives/budget rules, including bid adjustment, budget modification and status changes; ③ Ads reports (linkfox-amazon-ads-report) — end-to-end fetch of all SP/SB/SD report types (create → poll → download → extract → structured return). Both manager and report depend on auth. Triggered when the user needs Amazon Ads authorization, querying/creating/modifying/adjusting bids on ads, or pulling ad reports. Full params per sub-capability are in references/, executable scripts in scripts/.
category: e-commerce
version: 1.0.0
author: LinkFox
---

# Linkfox 亚马逊广告（Amazon Ads）

亚马逊广告（Amazon Ads）全链路一站式 AI 工具集，整合 **3 项子能力**，覆盖授权与令牌、SP/SB/SD 广告查询与写操作、广告报告一站式获取。三条子能力构成「授权 → 管理 → 报表」链路：`linkfox-amazon-ads-auth` 是前置依赖（产出 `profileId` + 访问令牌），`linkfox-amazon-ads-manager`（实体元数据）与 `linkfox-amazon-ads-report`（指标报表）均依赖它。各子能力完整参数、响应字段与错误码见 `references/` 下对应文件，可执行脚本见 `scripts/<auth|manager|report>/`。

## 能力边界

### ✅ 能力范围

- **授权与令牌管理**（子能力 `linkfox-amazon-ads-auth`，tool_key `amazon_ads`）：为新账号生成 LWA OAuth 授权链接，一次授权自动发现并绑定同账号下所有可用站点的广告 profile（每站点一个 `profileId`）；查询已授权账号 × 站点列表与 profile 列表；读取与刷新访问令牌（`accessToken` 1 小时有效）；为下游解析 `profileId`。支持 `NA`（美加墨巴）/ `EU`（英德法意西荷印等）/ `FE`（日澳新）三大区域，默认 `NA`。
- **广告管理**（子能力 `linkfox-amazon-ads-manager`，tool_key `amazon_ads`）：查询（list）与创建/修改（create/update）SP/SB/SD 三条产品线的广告活动、广告组、关键词、否定关键词、商品广告、定向、否定定向、创意、预算规则等实体元数据；含出价调整、预算修改、状态变更、Budget Rules；自动分页、过滤器结构规范化、多账号 `profileId` 解析。写操作遵循财务安全指引（先确认再执行、执行后输出回执）。
- **广告报告**（子能力 `linkfox-amazon-ads-report`，tool_key `amazon_ads`）：一站式获取 SP/SB/SD 全量广告报告，脚本内部完成报告创建 → 等待生成 → 下载 → 解压，直接返回结构化数据；支持全链路模式与仅轮询模式（用 `reportId` 救回上次超时）。每个 `reportTypeId` 的可用 `columns`/`groupBy`/`filters`/`timeUnit`/日期约束以 `references/report-types/<adProduct-dir>/<reportTypeId>.md` 为单一真相源。
- **链路依赖**：manager 与 report 调用前必须先经 auth 拿到 `profileId`（数字，内部传递不播报）；令牌过期（下游 HTTP 401）时回 auth 用 `refresh_token.py` 续签。多账号场景按 `countryCode`/`accountName` 澄清，严禁让用户直接报 `profileId` 数字、严禁歧义下挑第一个。

### ❌ 边界与限制

- **API Key 必需**：所有工具均需环境变量 `LINKFOX_AGENT_API_KEY`（或 `LINKFOXAGENT_API_KEY`）；各子能力独立计费、独立限频。
- **accountName 必填**：调 `authorize_url.py` 前必须先向用户确认一个非空账号名。
- **令牌时效**：`accessToken` 有效期 1 小时，过期后下游返回 HTTP 401，需用 `refresh_token.py` 续签。
- **manager 只给元数据，不含指标**：返回实体字段（id/名称/状态/匹配类型等）；曝光/点击/花费/转化等指标交给 report，按 id join。
- **manager 不支持 DELETE**：可通过 update `state=ARCHIVED` 归档，但不可逆；SB keywords/targets 等无 list all（Amazon 官方未提供，需按 id 单查，不在本 skill）；SD 非基础实体接口（brandSafety/recommendations/forecasts/optimizationRules/locations 等）不在范围。
- **report 日期约束**：多数报告跨度上限 31 天，`sbPurchasedProduct` 731 天，GrossAndInvalids 系列 365 天（以 frontmatter `dateRange.maxSpanDays` 为准）；回溯窗口 SP 默认 95 天、SB 60 天、GrossAndInvalids 365 天（以 `dateRange.dataRetentionDays` 为准）；数据延迟约 12 小时。
- **未覆盖**：Sponsored Television (ST) / Amazon DSP；Brand Analytics / Retail Analytics / Attribution 报告；报告删除/修改/定时任务。
- **计费约束**：同一会话同一参数组合默认只调用一次；失败或空结果不得自动换关键词、翻页或连续试探；需继续检索时先向用户说明会产生额外消耗（各子能力计费规则见 `skills-version.json` 对应条目与 references 内 api.md 的 `costToken` 字段）。
- **不在范围内**：店铺运营（Listing 刊登/订单/库存，用 SP-API 系列）、选品调研（用亚马逊选品系列）、1688 找货源、TikTok/沃尔玛等其他平台、与平台或卖家的直接沟通。

## 工具选择指南

按需求在下表定到子能力，再跳到【业务需求路由速查】查端点/脚本/references 取参执行。**核心区分：实体元数据（manager）vs 指标报表（report）——按 id join。**

| 需求 / 用户说 | 默认推荐（子能力·脚本） | 何时换用其他 |
|---|---|---|
| 授权/绑定亚马逊广告账户（"授权亚马逊广告""绑定广告账户"） | `linkfox-amazon-ads-auth`·`scripts/auth/authorize_url.py` | — |
| 列已授权账号/站点（"我绑了哪些广告账号"） | `linkfox-amazon-ads-auth`·`scripts/auth/authorized_stores.py` | 要含货币/时区/日预算等业务字段用 `scripts/auth/profiles.py` |
| 广告接口报 401 / 令牌过期（"广告报 401"） | `linkfox-amazon-ads-auth`·`scripts/auth/refresh_token.py` | — |
| 查广告活动/广告组/关键词/商品广告/定向（"看下我的 SP 广告活动""某 campaign 下的广告组"） | `linkfox-amazon-ads-manager`·`scripts/manager/sp/list_*.py`（SB 用 `sb/`、SD 用 `sd/`） | 要曝光/点击/花费/转化指标用 report；要按 ASIN 反查投放用 `sp/list_product_ads.py` 客户端过滤 |
| 创建/修改/调价/改预算/暂停广告（"把出价调到 $1.5""预算改 $100""暂停某广告组"） | `linkfox-amazon-ads-manager`·`scripts/manager/<sp\|sb\|sd>/create_*.py` 或 `update_*.py` | — |
| 预算规则（"给某活动加预算规则"） | `linkfox-amazon-ads-manager`·`scripts/manager/<sp\|sb\|sd>/create_budget_rules.py` 等 | — |
| 广告效果/花费/指标（"上周广告花费""广告活动效果"） | `linkfox-amazon-ads-report`·`scripts/report/get_report.py`（reportTypeId `spCampaigns`/`sbCampaigns`/`sdCampaigns`） | 实体 id/名称/状态用 manager |
| 搜索词/投放商品/购买商品报告（"用户搜什么词找到我""哪个投放商品卖得好"） | `linkfox-amazon-ads-report`·`scripts/report/get_report.py`（`spSearchTerm`/`spAdvertisedProduct`/`spPurchasedProduct`） | — |
| 关键词表现/定向报告 | `linkfox-amazon-ads-report`·`scripts/report/get_report.py`（`spTargeting`） | 关键词实体元数据用 manager 的 `sp/list_keywords.py` |
| 流量异常/无效流量 | `linkfox-amazon-ads-report`·`scripts/report/get_report.py`（GrossAndInvalids 系列） | — |
| 继续等上次超时的报告 | `linkfox-amazon-ads-report`·`scripts/report/get_report.py`（仅轮询模式，传 `reportId`） | — |
| 多账号选哪个 profile（"查我美国站的广告"） | `linkfox-amazon-ads-auth`·`scripts/auth/authorized_stores.py` 解析 `profileId` | — |

### 工具选择思路
- **重要**：多个子能力满足需求时，要依据需求深入分析子能力的功能、用途、出入参，从中调研出最合适的子能力并推荐用户，让用户自己决定。
- 满足程度同等的前提下，向用户推荐"默认推荐子能力"。实体元数据与指标报表的关键分界：要 id/名称/状态/结构 → manager；要曝光/点击/花费/转化 → report，两者按 id join。

## 业务需求路由速查

按【工具选择指南】定到子能力后，下表查端点、脚本与 references 文件取参执行。脚本位于 `scripts/<auth|manager|report>/` 下。

### 子能力 ↔ references 文件 ↔ 端点 ↔ 脚本（3 项）

**linkfox-amazon-ads-auth**（端点各异，均 `POST /amazonAds/<op>`）
| 用途 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| 生成授权 URL | references/linkfox-amazon-ads-auth.md | POST /amazonAds/authorizeUrl | scripts/auth/authorize_url.py |
| 列已授权账号×站点 | references/linkfox-amazon-ads-auth.md | POST /amazonAds/authorizedStores | scripts/auth/authorized_stores.py |
| 列 profile（含货币/时区/日预算） | references/linkfox-amazon-ads-auth.md | POST /amazonAds/profiles | scripts/auth/profiles.py |
| 刷新令牌 | references/linkfox-amazon-ads-auth.md | POST /amazonAds/refreshToken | scripts/auth/refresh_token.py |
| 查令牌（不触发刷新） | references/linkfox-amazon-ads-auth.md | POST /amazonAds/storeTokens | scripts/auth/store_tokens.py |

**linkfox-amazon-ads-manager**（统一端点 `POST /amazonAds/developerProxy`，操作由请求体区分；共用参数、过滤器结构、枚举值见 references/linkfox-amazon-ads-manager.md 与 references/api/{sp,sb,sd}.md）

SP（Sponsored Products v3）—— `scripts/manager/sp/`
| 实体 | 查询 | 创建 | 修改 |
|------|------|------|------|
| 广告活动 | `sp/list_campaigns.py` | `sp/create_campaigns.py` | `sp/update_campaigns.py` |
| 广告组 | `sp/list_ad_groups.py` | `sp/create_ad_groups.py` | `sp/update_ad_groups.py` |
| 关键词 | `sp/list_keywords.py` | `sp/create_keywords.py` | `sp/update_keywords.py` |
| 否定关键词 | `sp/list_negative_keywords.py` | `sp/create_negative_keywords.py` | `sp/update_negative_keywords.py` |
| 商品广告 | `sp/list_product_ads.py` | `sp/create_product_ads.py` | `sp/update_product_ads.py` |
| 商品定向 | `sp/list_targets.py` | `sp/create_targets.py` | `sp/update_targets.py` |

额外：活动级否定关键词 `sp/create|update_campaign_negative_keywords.py`、活动级否定定向 `sp/create|update_campaign_negative_targets.py`、广告组级否定定向 `sp/create|update_negative_targets.py`、预算规则 `sp/list|create|update_budget_rules.py`、预算规则关联 `sp/create_budget_rules_association.py`。

SB（Sponsored Brands v4）—— `scripts/manager/sb/`
| 实体 | 查询 | 创建 | 修改 |
|------|------|------|------|
| 广告活动 | `sb/list_campaigns.py` | `sb/create_campaigns.py` | `sb/update_campaigns.py` |
| 广告组 | `sb/list_ad_groups.py` | `sb/create_ad_groups.py` | `sb/update_ad_groups.py` |
| 广告创意 | `sb/list_ads.py` | `sb/create_ads.py` | `sb/update_ads.py` |

额外：预算规则 `sb/list|create|update_budget_rules.py`。

SD（Sponsored Display v3）—— `scripts/manager/sd/`
| 实体 | 查询 | 创建 | 修改 |
|------|------|------|------|
| 广告活动 | `sd/list_campaigns.py` | `sd/create_campaigns.py` | `sd/update_campaigns.py` |
| 广告组 | `sd/list_ad_groups.py` | `sd/create_ad_groups.py` | `sd/update_ad_groups.py` |
| 商品广告 | `sd/list_product_ads.py` | `sd/create_product_ads.py` | `sd/update_product_ads.py` |
| 定向子句 | `sd/list_targets.py` | `sd/create_targets.py` | `sd/update_targets.py` |
| 否定定向子句 | `sd/list_negative_targets.py` | `sd/create_negative_targets.py` | `sd/update_negative_targets.py` |
| 创意素材 | `sd/list_creatives.py` | `sd/create_creatives.py` | `sd/update_creatives.py` |

额外：预算规则 `sd/list|create|update_budget_rules.py`。详细过滤器、枚举值、返回字段见 references/api/sp.md / sb.md / sd.md。

**linkfox-amazon-ads-report**（统一端点 `POST /amazonAds/developerProxy`，全链路/仅轮询模式见 references/linkfox-amazon-ads-report.md）
| 用途 | references 文件 | 脚本 | reportTypeId（详见 references/report-types/） |
|---|---|---|---|
| SP/SB/SD 全量报告一站式获取 | references/linkfox-amazon-ads-report.md | scripts/report/get_report.py | `spCampaigns`/`spAdvertisedProduct`/`spSearchTerm`/`spTargeting`/`spPurchasedProduct`/`spGrossAndInvalids`/`spPromptAdExtension`、`sbCampaigns`/`sbAdGroup`/`sbAds`/`sbSearchTerm`/`sbTargeting`/`sbPurchasedProduct`/`sbCampaignPlacement`/`sbGrossAndInvalids`/`sbPromptAdExtension`、`sdCampaigns`/`sdAdGroup`/`sdAdvertisedProduct`/`sdTargeting`/`sdPurchasedProduct`/`sdGrossAndInvalids` |
| 检测 auth 依赖 | references/linkfox-amazon-ads-report.md | scripts/report/check_auth_dependency.py | — |

> manager 与 report 各自带 `check_auth_dependency.py`（检测 `linkfox-amazon-ads-auth` 是否安装，缺失时 exit 42、stderr 打 `DEPENDENCY_MISSING`）；manager 的 sp/sb/sd 脚本依赖同目录 `_common.py`，report 的 `get_report.py` 自包含。报告类型的完整列清单/groupBy/filters 以 `references/report-types/<sp|sb|sd>/<reportTypeId>.md` 为单一真相源。

## 调用方式

- **网关**：`${LINKFOX_TOOL_GATEWAY}/<端点>`，请求方式 POST、Content-Type `application/json`，认证 Header `Authorization: <api_key>`（api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取；未配置按下方【解决认证和积分问题】处理）。auth 端点为 `/amazonAds/{authorizeUrl|storeTokens|authorizedStores|refreshToken|profiles}`；manager 与 report 统一走 `POST /amazonAds/developerProxy`，操作由请求体区分。各端点路径见上方【业务需求路由速查】与对应 references 文件。
- **Python 脚本**：每项子能力对应 `scripts/<auth|manager|report>/<脚本名>.py '<JSON 参数>' [--inline]`（脚本名与端点见路由速查表；manager 脚本路径形如 `scripts/manager/sp/list_campaigns.py`）。脚本内部完成网关调用、鉴权与落盘；manager/report 脚本启动时自动检查 `linkfox-amazon-ads-auth` 依赖（可传 `skipDepCheck:true` 跳过）。
- **输出策略（脚本默认行为）**：始终将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/<skill>-<timestamp>.json`（`<cwd>` 为脚本执行时工作目录；`<session>` 取自环境变量 `SESSION_ID`；禁止写入 /tmp，当前目录不可写则报错）；响应体 ≤ 8 KB 落盘后完整打印到 stdout，> 8 KB 仅打印摘要（顶层字段、常见计数、最大列表长度 + 前 3 条样本）；加 `--inline` 强制全量打印（同样落盘）。report 的 `get_report.py` 还会通过本机 `127.0.0.1` 临时 HTTP 服务暴露解压后的 JSON（`serveSeconds` 后自动关闭）。
- **读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 PowerShell `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。
- **完整参数**：每个子能力的请求参数、响应字段、错误码、curl 示例见 `references/linkfox-amazon-ads-<auth|manager|report>.md`（文件内含该子能力 SKILL.md 正文与 api.md 全文）；manager 的 SP/SB/SD 过滤器/枚举/字段见 `references/api/{sp,sb,sd}.md`，report 的报告类型规格见 `references/report-types/<sp|sb|sd>/<reportTypeId>.md`。

## 使用示例

以下按子能力给出代表性出入参示例；其余参数见对应 references 文件。`profileId` 为数字（从 auth 获取，内部传递不播报），`region` 为 `NA`/`EU`/`FE`。

### 授权与令牌（auth）

**1. 生成授权 URL（authorize_url.py）**
```json
{"region": "NA", "accountName": "我的美国广告账号"}
```
出参：`authorizeUrl`（约 270 字符，从剪贴板/`~/.cache/linkfox/last_authorize_url.txt` 复制，建议无痕窗口在安全网络环境打开）、`sourceType`。

**2. 列已授权账号×站点（authorized_stores.py）**
```json
{}
```
出参：`total`、`stores[]`（profileId/accountInfoId/accountInfoName/accountType/countryCode/marketplaceStringId/region/authRecordId/accountName）。

**3. 刷新令牌（refresh_token.py）**
```json
{"profileId": 1111111111}
```
出参：`authRecordId`、`accessToken`/`refreshToken`（脚本已掩码）、`tokenType`、`expiresIn`（"3600"）、`message`。`accessToken` 1 小时有效。

### 广告管理（manager）

**4. 列活跃 SP 广告活动（manager/sp/list_campaigns.py）**
```json
{"profileId": 1234567890, "region": "NA", "stateFilter": {"include": ["ENABLED"]}}
```
出参：`success`、`campaigns[]`（id/name/state/biddingStrategy/dailyBudget/startDate…）、`total`、`pagesFetched`、`truncated`。自动分页（`fetchAll` 默认 true，跟 `nextToken`，`maxPages=50` 兜底）。

**5. 看某 SP campaign 下的广告组（manager/sp/list_ad_groups.py）**
```json
{"profileId": 1234567890, "region": "NA", "campaignIdFilter": {"include": ["998877665544"]}}
```
出参：`adGroups[]`（id/name/state/defaultBid/campaignId…）、`total`、`truncated`。

**6. 按 ASIN 反查 SP 投放（manager/sp/list_product_ads.py，客户端过滤）**
```json
{"profileId": 1234567890, "region": "NA", "asinFilter": {"include": ["B01ABCDEFG"]}, "campaignIdFilter": {"include": ["998877665544"]}}
```
出参：`productAds[]`（asin/sku/campaignId/adGroupId/state…）、`serverTotalBeforeClientFilter`、`clientSideFilters`。

**7. 修改出价/预算（manager/sp/update_keywords.py，写操作先确认）**
```json
{"profileId": 1234567890, "region": "NA", "updates": [{"keywordId": "123456789012", "bid": 1.5}]}
```
出参：`success`、`keywords.updateSuccessResults`/`updateErrorResults`（含错误码与原因）。写操作执行前须输出确认摘要，执行后须输出操作回执（见展示规则）。

### 广告报告（report）

**8. SP 广告活动报告（report/get_report.py，DAILY 一周）**
```json
{"profileId": 1234567890, "region": "NA", "reportTypeId": "spCampaigns", "adProduct": "SPONSORED_PRODUCTS", "groupBy": ["campaign"], "columns": ["date","campaignId","campaignName","impressions","clicks","cost"], "startDate": "2026-04-27", "endDate": "2026-05-03", "timeUnit": "DAILY"}
```
出参：`success`、`reportId`、`status`（PENDING/PROCESSING/COMPLETED/FAILED）、`pollAttempts`、`elapsedSeconds`、`downloadPath`、`extractedFileHttpUrl`（约 5 分钟有效）、`serveExpiresAt`。脚本完成创建→轮询→下载→解压。

**9. SP 搜索词报告（report/get_report.py，SUMMARY + 归因 + 过滤）**
```json
{"profileId": 1234567890, "region": "NA", "reportTypeId": "spSearchTerm", "adProduct": "SPONSORED_PRODUCTS", "groupBy": ["searchTerm"], "columns": ["searchTerm","keyword","matchType","impressions","clicks","cost","sales7d","purchases7d","acosClicks14d","roasClicks14d","startDate","endDate"], "startDate": "2026-04-01", "endDate": "2026-04-30", "timeUnit": "SUMMARY", "filters": [{"field": "keywordType", "values": ["BROAD","PHRASE","EXACT"]}]}
```
出参：同 §8；归因窗口后缀 `_1d`/`_7d`/`_14d`/`_30d` 表示 1/7/14/30 天归因，具体字段支持哪些窗口以 `references/report-types/sp/spSearchTerm.md` 的 Base metrics 表为准。

**10. 仅轮询已有 reportId（report/get_report.py，救回超时）**
```json
{"profileId": 1234567890, "region": "NA", "reportId": "7df1ef5d-45ba-40cc-b607-ff2148cf4f5e", "maxAttempts": 60, "pollInterval": 30}
```
出参：同 §8。轮询窗口耗尽但报告仍在生成时返回 `status=STILL_PROCESSING`（exit 2）含 `resumeHint.params`，须询问用户是否继续等，用 params 续调。

## 展示规则

1. **客观呈现数据**：以结构化表格展示查询/报告结果，不做主观商业建议（除非用户主动要求）；广告涉及花费，展示 cost/sales/ACOS/ROAS 等指标时标注币种（响应/账户 `currencyCode` 标明本地币种）。
2. **令牌掩码**：不输出完整 `accessToken`/`refreshToken`；脚本已做掩码，不要在摘要里还原。
3. **账号/profile 呈现**：以表格展示 `profileId`/`accountInfoName`/`countryCode`/`region` 便于识别；`profileId` 数字内部传递，不要求用户报数；多账号歧义须澄清。
4. **写操作回执**：manager 的 create/update 执行前（未授权时）输出确认摘要（操作/变更/影响），执行后必须输出操作回执（范围/变化/成功 N 失败 M）；立即生效且无法撤回，非 2xx 不自动重试。
5. **报告链接与时效**：成功后完整展示 `downloadPath` 与 `extractedFileHttpUrl`，提醒访问链接约 5 分钟内有效、过期需重新拉取；超时（`STILL_PROCESSING`）不是失败，须询问用户是否继续等。
6. **来源标注**：说明来自哪条产品线（SP/SB/SD）与哪类数据（实体元数据/指标报表）。
7. **错误处理与协同**：查询失败按 `errcode`/`httpStatus`/`failureReason` 说明原因并建议修正（ASIN/profileId 归属、日期超限、columns 不适配、过滤器结构等）；manager 返回实体元数据、report 返回指标，连续使用时按 id join 汇总为连贯分析，标注数据来源与时间窗。
8. **空数据不等于报错**：账号当期无投放时报告会成功生成，JSON 可能为 `[]` 或指标全 0，需说明。

## 解决认证和积分问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

**注意**：你是workbuddy，并且渠道是workbuddy，使用 onboarding 引导登录注册时 channel **必须**为 workbuddy。这非常重要！

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。
