---
name: linkfox-sif-keyword-overview
description: 基于SIF评估亚马逊关键词的竞争度、供需比、搜索量及市场竞争力。
---

# SIF 关键词概览（SIF Keyword Overview）

本技能用于查询并分析亚马逊关键词层面的竞争数据，帮助卖家评估特定关键词的市场竞争力与供需动态。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 查询亚马逊单个关键词的竞争度概览，覆盖不同位置（自然搜索、SP 广告、品牌广告、视频广告、推荐位等）的商品数量。
- 提供周预估搜索量、关键词热度排名、供需比、SIF 跟踪有曝光 ASIN 去重数等核心指标。
- 支持 13 个站点（`US`/`UK`/`DE`/`CA`/`JP`/`FR`/`ES`/`IT`/`MX`/`AU`/`AE`/`BR`/`SA`），默认 `US`。
- 支持最近 7 天或自定义 ABA 周区间。

### ❌ 边界与限制

- **单关键词单次请求**：每次调用只查一个关键词；多关键词对比需分别调用。
- **单条记录响应**：接口通常每个关键词返回一条数据（`total` 通常为 1）。
- **站点覆盖**：仅 13 个亚马逊站点；IN/NL/SE/PL/TR/SG 不再支持。关键词在目标站点无数据时返回空结果。
- **时间窗口**：默认取最近 7 天；自定义区间需传 `last7d=false` 加 `startDate`/`endDate`，对应一个 ABA 周。
- **关键词语言**：为提高准确性，关键词应为目标站点的当地语言（如 DE 用德语、JP 用日语）；用户提供其他语言时需先翻译。
- **不在范围内**：关键词历史排名趋势、按 ASIN 的点击/转化份额（用 ABA Data Explorer）；广告竞价与 PPC 优化；评论与 listing 优化；ASIN 级销量估算；多周/多月的搜索趋势详细分析。

## 核心概念

SIF 关键词概览为指定关键词返回竞争度快照，包含各位置商品数、周预估搜索量、关键词热度排名与供需比。

- **供需比（`supplyDemandRatio`）**：计算公式为 `搜索结果商品数 / 月搜索量`。数值越小，竞争越小、机会越大，是识别蓝海关键词的关键指标。<1 通常表示需求大于供应（机会），>5 通常表示市场饱和。
- **关键词热度排名（`keywordPopularityRank`）**：该关键词月搜索量在站点所有关键词中的排名，数值越小越热门（排名第 1 最热门）。用户说"排名上升"指数值减小，"排名下降"指数值增大。

完整字段说明见 [references/api.md](references/api.md)。

## 调用方式

- **API 端点**：`POST /sif/keywordOverview`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/sif_keyword_overview.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-sif-keyword-overview-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 基础关键词竞争度查询**
> "无线充电器这个关键词在亚马逊美国竞争有多激烈？"
```json
{"keyword": "wireless charger", "country": "US"}
```

**2. 非美国站点竞争度**
> "德国站 'Handyhulle' 有多少竞品？"
```json
{"keyword": "Handyhulle", "country": "DE"}
```

**3. 供需分析**
> "美国站 'yoga mat' 的供需比是多少？"
```json
{"keyword": "yoga mat", "country": "US"}
```

**4. 广告竞争评估**
> "英国站 'dog leash' 有多少卖家在投广告？"
```json
{"keyword": "dog leash", "country": "UK"}
```

**5. 多站点对比（多次调用）**
> "对比 'bluetooth speaker' 在 US、UK、DE 的竞争度"
- 调用 1：`{"keyword": "bluetooth speaker", "country": "US"}`
- 调用 2：`{"keyword": "bluetooth speaker", "country": "UK"}`
- 调用 3：`{"keyword": "Bluetooth Lautsprecher", "country": "DE"}`

**6. 指定日期区间**
> "'yoga mat' 在 2026-03-08 到 2026-03-14 的竞争度"
```json
{"keyword": "yoga mat", "country": "US", "last7d": false, "startDate": "2026-03-08", "endDate": "2026-03-14"}
```

## 展示规则

1. **清晰呈现数据**：以结构化表格展示用户关注的所有相关指标。
2. **突出关键指标**：重点展示供需比、关键词热度排名、搜索结果商品总数，这是最具行动价值的指标。
3. **排名口径说明**：展示关键词热度排名时提醒用户，数值越小表示搜索热度越高。
4. **供需比解读**：展示供需比时提供语境——<1 通常表示需求大于供应（机会），>5 通常表示市场饱和。
5. **广告竞争拆解**：用户询问广告竞争时，把 PPC 广告总数拆解为 SP、品牌广告、视频广告等组成部分。
6. **数据时效与周期**：始终展示 `keywordDataUpdateTime`（最近刷新时间）以及 `dataPeriodStartDate` ~ `dataPeriodEndDate`（数据对应的 ABA 周）；不要在未说明周期的情况下展示商品数。
7. **错误处理**：查询失败时根据 `msg` 字段说明原因，并建议调整参数（如检查关键词拼写、换站点）。
8. **不做主观建议**：客观呈现数据，除非用户明确要求，否则不做商业建议。

## 用户表达与场景速查

**适用** —— 关键词层面的竞争度与市场评估：

| 用户说 | 场景 |
|--------|------|
| "XX 关键词竞争有多激烈" | 竞争强度判断 |
| "XX 下有多少商品" | 搜索结果商品数 |
| "XX 的供需比是多少" | 供需分析 |
| "XX 有多少卖家在投广告" | 广告竞争评估 |
| "XX 关键词是不是蓝海" | 市场机会评估 |
| "XX 关键词的搜索量" | 搜索热度估算 |
| "XX 在亚马逊有多火" | 关键词热度排名 |
| "对比各站点竞争度" | 多站点竞争对比 |
| "这个关键词下有多少 SIF 跟踪的 ASIN" | 去重跟踪 ASIN 数（`trackedAsinTotalCount`） |
| "某一周这个关键词的竞争度" | 通过 `startDate`/`endDate` 自定义区间 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题
发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用skill内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个skill并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个skill。

---

# SIF-关键词概览 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/sif/keywordOverview`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 是 | 关键词，尽量翻译成对应国家站点的语言。最大长度：1000 字符 |
| country | string | 否 | 国家站点，默认 `US`。可选值（共 13 个）：`US`、`UK`、`DE`、`CA`、`JP`、`FR`、`ES`、`IT`、`MX`、`AU`、`AE`、`BR`、`SA` |
| last7d | boolean | 否 | 是否取最近 7 天数据，默认 `true`。传 `false` 时使用 `startDate`/`endDate` 区间 |
| startDate | string | 否 | 开始日期 `yyyy-MM-dd`（`last7d=false` 时生效） |
| endDate | string | 否 | 结束日期 `yyyy-MM-dd`（与 `startDate` 配套） |


## 响应结构

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| msg | string | 消息 |
| total | integer | 数据总量。注意：本接口通常只返回单条数据，total 通常为1 |
| code | string | 返回码 |
| data | array | 返回数据（详见下方数据字段） |
| costTime | integer | 耗时（ms） |
| costToken | integer | 消耗token |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| title | string | 标题 |

### 数据字段（`data` 数组中的每个对象）

| 字段 | 类型 | 说明 |
|------|------|------|
| keyword | string | 关键词。搜索查询的关键词文本 |
| keywordPopularityRank | integer | 关键词热度排名。该关键词的月搜索量在亚马逊所有关键词中的排名，数值越小表示搜索量越大 |
| estimatedWeeklySearchVolume | integer | 周预估搜索量。该关键词在亚马逊上每周的预估搜索次数，反映该词的搜索热度 |
| supplyDemandRatio | number | 供需比率。供应与需求的比率，计算公式：搜索结果商品数 / 月搜索量，数值越小表示竞争越小、机会越大 |
| totalSearchResultProductCount | integer | 搜索结果商品总数。在该关键词下显示的所有商品总数（包括自然搜索、广告位、推荐位等） |
| naturalSearchProductCount | integer | 自然搜索商品数量。在该关键词的自然搜索结果中展示的商品数量（不包括广告位） |
| sponsoredProductsCount | integer | SP广告商品数量。在该关键词下投放Sponsored Products（赞助商品）广告的商品数量 |
| brandAdProductCount | integer | 品牌广告商品数量。在该关键词下投放品牌广告（Brand Ads）的商品数量 |
| videoAdProductCount | integer | 视频广告商品数量。在该关键词下投放视频广告（Video Ads）的商品数量 |
| paidAdvertisingProductCount | integer | PPC广告商品总数。在该关键词下所有PPC付费广告（包括SP、品牌广告、视频广告等）的商品总数 |
| amazonChoiceProductCount | integer | Amazon's Choice商品数量。在该关键词下获得Amazon's Choice推荐标志的商品数量 |
| topRatedProductCount | integer | Top Rated推荐商品数量。在该关键词下出现在Top Rated（高评分）推荐位的商品数量 |
| searchRecommendationProductCount | integer | 搜索推荐商品数量。在该关键词搜索时亚马逊推荐的商品数量 |
| editorialRecommendationsProductCount | integer | Editorial Recommendations商品数量。在该关键词下出现在编辑推荐位的商品数量 |
| recNonadProductCount | integer | 推荐位非广告商品数量。在该关键词下推荐位中属于非广告（自然）的商品数量 |
| recAdProductCount | integer | 推荐位广告商品数量。在该关键词下推荐位中属于广告的商品数量 |
| trackedAsinTotalCount | integer | SIF 跟踪的有曝光 ASIN 去重总数。该关键词下所有位置（自然/广告/推荐）中，SIF 系统追踪到有曝光得分的 ASIN 去重数量（上游字段：`totalAsinNum`） |
| totalMarketplaceKeywordCount | integer | 站点关键词总量。该站点所有关键词的总数量，用于了解市场整体规模 |
| dataPeriodStartDate | string | 数据周期起始日期。本次返回数据对应的 ABA 周起始日期（`yyyy-MM-dd`） |
| dataPeriodEndDate | string | 数据周期结束日期。本次返回数据对应的 ABA 周结束日期（`yyyy-MM-dd`） |
| keywordDataUpdateTime | string | 关键词数据更新时间 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 余额不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/sif/keywordOverview \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "wireless charger", "country": "US"}'
```

### 指定日期区间

```bash
curl -X POST https://tool-gateway.linkfox.com/sif/keywordOverview \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "yoga mat", "country": "US", "last7d": false, "startDate": "2026-03-08", "endDate": "2026-03-14"}'
```
