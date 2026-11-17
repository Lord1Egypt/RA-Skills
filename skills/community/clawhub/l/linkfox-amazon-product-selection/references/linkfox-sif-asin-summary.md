---
name: linkfox-sif-asin-summary
description: 利用SIF数据分析ASIN的流量构成与曝光渠道（如自然、广告、推荐位），支持跨周期对比。
---

# SIF-ASIN流量概览（SIF ASIN Summary）

本技能用于查询并分析 Amazon ASIN 级别的流量来源数据，帮助卖家了解任意商品在各渠道的曝光与流量结构。请求参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 查询 ASIN 的流量来源构成与曝光分布，覆盖自然搜索、SP 广告、品牌广告、视频广告、Amazon's Choice、Editorial Recommendations、Top Rated 推荐位等渠道。
- 支持本期 / 上期 / 新进 / 退出跨周期对比（`*Prev` / `*In` / `*Out` 字段）。
- 支持单 ASIN 深度拆解与多 ASIN（最多 10 个）竞品对比。
- 支持按渠道筛选（`conditions`）与按曝光得分排序（`sortBy`）。

### ❌ 边界与限制

- **ASIN 上限**：单次请求最多 10 个 ASIN。
- **分页上限**：每页最多 10000 条。
- **站点覆盖**：仅支持 13 个站点（US、UK、DE、CA、JP、FR、ES、IT、MX、AU、AE、BR、SA）；IN / NL / SE / PL / TR / SG 已不可用。
- **时间窗口**：默认取最近 7 天（`last7d=true`）；查询其他窗口需设 `last7d=false` 并传 `startDate`/`endDate`。
- **曝光得分为相对值**：可用于跨渠道、跨 ASIN 对比，但非绝对流量体积。
- **不在范围内**：多周历史趋势曲线（仅本期+上期，长趋势用 ABA 数据）；关键词级搜索量或排名（用 ABA 或 ASIN-keywords 工具）；销量预估与收入分析；Listing 优化与文案；广告出价或预算建议。

## 核心概念

SIF（Search Intelligence Framework，搜索情报框架）ASIN Summary 提供 ASIN 在 Amazon 上流量来源的全景拆解，揭示商品总曝光如何分布于自然搜索、SP 广告、品牌广告、视频广告、Amazon's Choice、Editorial Recommendations、Top Rated 推荐等渠道，适用于竞品分析与流量策略优化。

- **曝光得分（Exposure Score）**：综合反映商品在某渠道所有关键词下整体可见度的复合指标，得分越高曝光越大。**曝光占比（Exposure Ratio）** 字段表示该渠道占总曝光的百分比。
- **流量关键词数（Traffic Keyword Count）**：商品被发现的流量词总数，按渠道拆分（自然搜索、SP 广告、品牌广告、视频广告等）。
- **字段后缀约定**：`*Prev` = 上一周期数值；`*In` / `*Out` = 本周期相对上期新进 / 退出数量，用于跨周对比。

完整字段说明见 [references/api.md](references/api.md)。

## 调用方式

- **API 端点**：`POST /sif/asinSummary`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/sif_asin_summary.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-sif-asin-summary-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 单 ASIN 流量拆解**
> "看一下 B09V3KXJPB 在美国站的流量来源"

查询 `searchValue = "B09V3KXJPB"`、`country = "US"`。

**2. 多 ASIN 竞品对比**
> "对比 B09V3KXJPB 和 B0BN1K7WJP 在美国站的流量结构"

查询 `searchValue = "B09V3KXJPB,B0BN1K7WJP"`、`country = "US"`。

**3. 指定站点查询**
> "分析 B07XJ8C8F5 在日本站的流量来源"

查询 `searchValue = "B07XJ8C8F5"`、`country = "JP"`。

**4. 自然流量 vs 付费流量**
> "B09V3KXJPB 的曝光里自然搜索和广告各占多少？"

查询该 ASIN，对比 `naturalSearchExposureRatio` 与 `sponsoredProductsExposureRatio`、`brandAdExposureRatio`、`videoAdExposureRatio`。

**5. 广告渠道深挖**
> "B0BN1K7WJP 在 SP、品牌广告、视频广告上各投了多少词？"

查询该 ASIN，呈现 `sponsoredProductsKeywordCount`、`brandAdKeywordCount`、`topBrandAdKeywordCount`、`bottomBrandAdKeywordCount`、`videoAdKeywordCount`。

**6. 跨周期对比**
> "这个 ASIN 的总词数相比上周变化如何？"

查询该 ASIN，呈现 `totalTrafficKeywordCount`（本期）、`totalTrafficKeywordCountPrev`（上期）、`totalTrafficKeywordCountIn`（本周期新进）、`totalTrafficKeywordCountOut`（本周期退出）。自然搜索同理用 `naturalSearchKeywordCount*` 系列。

**7. 自定义日期区间**
> "B0XXX 在 2026-03-08 到 2026-03-14 的流量结构"

```
searchValue: "B0XXX", country: "US", last7d: false, startDate: "2026-03-08", endDate: "2026-03-14"
```

**8. 按渠道筛选并按 SP 曝光排序**
> "我 10 个商品里 SP 投放最强的 ASIN，按 SP 曝光排序"

```
searchValue: "B0A,B0B,...,B0J", conditions: "sp", sortBy: "totalSpSocre", desc: true
```

## 展示规则

1. **清晰呈现数据**：以结构化表格展示查询结果，将商品元信息、本期得分、关键词数、跨周期对比分列分组，便于阅读。
2. **百分比格式**：展示曝光占比时格式化为百分比（如 0.45 显示为 45.0%），更易理解。
3. **流量结构总览**：单 ASIN 查询时主动概括流量结构（如"自然 65%、SP 广告 25%、品牌广告 10%"），给出一眼可见的全景。
4. **周期标注**：展示 `*In` / `*Out` / `*Prev` 字段时须明确标注对比周期（如"对比上一个 7 天"或解析后的 `startDate ~ endDate` 区间），不要在没有说明对比窗口的情况下呈现周期差异。
5. **竞品对比布局**：多 ASIN 查询时使用并排对比表，让差异一目了然。
6. **错误处理**：查询失败时依据 `msg` 字段说明原因，并建议检查 ASIN 有效性或站点选择。
7. **变体感知**：若 `isVariantProduct` 为 true，提示该 ASIN 是变体，用户可能还需查看父 ASIN 以获取完整画像。

## 用户表达与场景速查

**适用** —— Amazon ASIN 流量来源与曝光分析：

| 用户说 | 场景 |
|--------|------|
| "这个 ASIN 的流量从哪来" | 流量来源拆解 |
| "这个商品有多少自然流量" | 自然搜索曝光分析 |
| "这个竞品是不是投了很多广告" | SP/品牌/视频广告曝光检查 |
| "对比这几个 ASIN 的流量结构" | 多 ASIN 竞品对比 |
| "这个商品有没有 Amazon's Choice" | AC/ER/TR 推荐检查 |
| "这个 ASIN 用了哪些广告渠道" | PPC 流量来源识别 |
| "这个 ASIN 排了多少个词" | 流量关键词数分析 |
| "这个商品靠付费还是自然流量" | 自然 vs 付费流量拆分 |
| "词数相比上周变化如何" | 跨周期对比（In/Out/Prev） |
| "这个 ASIN 新增了多少自然词" | 新进关键词数（`naturalSearchKeywordCountIn`） |
| "拉一下指定日期区间的数据" | 通过 `startDate`/`endDate` 自定义窗口 |
| "10 个 ASIN 按 SP 曝光排名" | 批量 `sortBy=totalSpSocre` |

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

# SIF-ASIN流量来源 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/sif/asinSummary`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchValue | string | 是 | 搜索值，ASIN码，多个用逗号分隔，最多10个ASIN，最大长度1000字符 |
| country | string | 否 | 国家站点，默认 `US`。可选值（共 13 个）：`US`、`UK`、`DE`、`CA`、`JP`、`FR`、`ES`、`IT`、`MX`、`AU`、`AE`、`BR`、`SA` |
| last7d | boolean | 否 | 是否取最近 7 天数据，默认 `true`。传 `false` 时使用 `startDate`/`endDate` 区间 |
| startDate | string | 否 | 开始日期 `yyyy-MM-dd`（`last7d=false` 时生效；不填取系统最新周） |
| endDate | string | 否 | 结束日期 `yyyy-MM-dd`（与 `startDate` 配套） |
| conditions | string | 否 | 条件筛选，多个以英文逗号隔开。可选值：`nf`（自然流量）、`sp`（SP广告）、`sb`（SB常规）、`sbv`（视频广告）、`ad`（广告流量）、`acAd`（SP推荐）、`totalPeriod.in`（新进全部流量词） |
| sortBy | string | 否 | 排序字段，可选值：`totalKeywordNum`（全部流量词）、`naturalKeywordNum`（自然流量词）、`brandKeywordNum`（品牌广告词）、`vedioKeywordNum`（视频广告词）、`acKeywordNum`（AC推荐词）、`erKeywordNum`（ER推荐词）、`trKeywordNum`（TR推荐词）、`sumScore`（所有关键词曝光总得分）、`totalNfScore`（所有自然排名曝光总得分）、`totalSpSocre`（所有SP广告曝光总得分，注意拼写）、`totalBrandScore`（所有品牌广告曝光总得分）、`totalVedioScore`（所有视频广告曝光总得分）、`totalAcScore`（所有AC推荐曝光总得分）、`totalTrScore`（所有TR推荐曝光总得分）、`totalErScore`（所有ER推荐曝光总得分） |
| pageNum | integer | 否 | 页码，默认 `1` |
| pageSize | integer | 否 | 每页数量，最小10，最大 **10000**，默认 `10000` |
| desc | boolean | 否 | 是否降序，默认 `true` |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| code | string | 返回码 |
| msg | string | 消息 |
| total | integer | 本次实际返回的数据数量 |
| data | array | 返回数据，ASIN汇总对象数组（详见下方） |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| title | string | 标题 |
| isParentAsin | boolean | 搜索的是否是父ASIN |
| variantsNum | integer | 有关键词的变体商品数量 |
| noKeywordVariantsNum | integer | 无关键词的变体商品数量 |
| costTime | integer | 耗时（ms） |
| costToken | integer | 消耗token |

### data 数组元素字段

> 字段后缀约定：`*Prev` 为上一周期数值；`*In` / `*Out` 为本周期相对上期新进 / 退出数量，用于跨周对比。

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN 编码。亚马逊商品标准识别码 |
| productTitle | string | 商品标题 |
| productCategory | string | 商品类目 |
| productPrice | number | 商品售价 |
| productImageUrl | string | 商品主图 URL |
| productFeatures | array | 商品特征列表 |
| customerRatingCount | integer | 客户评分总数 |
| productStarRating | number | 商品星级（0–5 星） |
| productRatingScore | number | 商品评分数值（0–5，亚马逊页面显示数值） |
| isVariantProduct | boolean | 是否为变体 |
| recentMonthlySalesBucket | string | 近一月销量桶（仅 keywordSummary 路径有值，形如 `"300+"` 或 `"1,000+"`） |
| isMonitored | boolean | 是否已监控 |
| monitoringStartTime | string | 商品关注时间 |
| dataPeriodStartDate | string | 数据周期起始日期（`yyyy-MM-dd`） |
| totalExposureScore | number | 总曝光分数。该商品在所有关键词下的曝光量综合评分 |
| totalExposureScorePrev | number | 上周期总曝光分数 |
| totalTrafficKeywordCount | integer | 流量关键词总数 |
| totalTrafficKeywordCountIn | integer | 本周期新进流量关键词数量 |
| totalTrafficKeywordCountOut | integer | 本周期退出流量关键词数量 |
| totalTrafficKeywordCountPrev | integer | 上周期流量关键词总数 |
| naturalSearchExposureScore | number | 自然搜索曝光总分 |
| naturalSearchExposureRatio | number | 自然搜索曝光占比 |
| naturalSearchExposureScorePrev | number | 上周期自然搜索曝光分数 |
| naturalSearchKeywordCount | integer | 自然搜索关键词数量 |
| naturalSearchKeywordCountIn | integer | 本周期新进自然搜索关键词数量 |
| naturalSearchKeywordCountOut | integer | 本周期退出自然搜索关键词数量 |
| naturalSearchKeywordCountPrev | integer | 上周期自然搜索关键词数量 |
| sponsoredProductsExposureScore | number | SP 广告曝光总分 |
| sponsoredProductsExposureRatio | number | SP 广告曝光占比 |
| sponsoredProductsExposureScorePrev | number | 上周期 SP 广告曝光分数 |
| sponsoredProductsKeywordCount | integer | SP 广告关键词数量 |
| brandAdExposureScore | number | 品牌广告曝光总分 |
| brandAdExposureRatio | number | 品牌广告曝光占比 |
| brandAdExposureScorePrev | number | 上周期品牌广告曝光分数 |
| brandAdKeywordCount | integer | 品牌广告关键词总数 |
| topBrandAdKeywordCount | integer | 页面顶部品牌广告关键词数量 |
| bottomBrandAdKeywordCount | integer | 页面底部品牌广告关键词数量 |
| videoAdExposureScore | number | 视频广告曝光总分 |
| videoAdExposureRatio | number | 视频广告曝光占比 |
| videoAdExposureScorePrev | number | 上周期视频广告曝光分数 |
| videoAdKeywordCount | integer | 视频广告关键词数量 |
| amazonsChoiceExposureScore | number | Amazon's Choice 曝光总分 |
| amazonsChoiceExposureRatio | number | Amazon's Choice 曝光占比 |
| amazonsChoiceExposureScorePrev | number | 上周期 AC 曝光分数 |
| amazonsChoiceKeywordCount | integer | Amazon's Choice 关键词数量 |
| amazonsChoiceKeywordCountIn | integer | 本周期新进 AC 关键词数量 |
| amazonsChoiceKeywordCountOut | integer | 本周期退出 AC 关键词数量 |
| editorialRecommendationsExposureScore | number | Editorial Recommendations 曝光总分 |
| editorialRecommendationsExposureRatio | number | Editorial Recommendations 曝光占比 |
| editorialRecommendationsKeywordCount | integer | Editorial Recommendations 关键词数量 |
| topRatedExposureScore | number | Top Rated 推荐曝光总分 |
| topRatedExposureRatio | number | Top Rated 推荐曝光占比 |
| topRatedKeywordCount | integer | Top Rated 推荐关键词数量 |
| frequentlyBoughtKeywordCount | integer | 高频购买推荐关键词数量（Top Rated Frequently Bought） |
| recommendPositionExposureScore | number | 推荐位曝光总分 |
| recommendAdExposureScore | number | 推荐位广告曝光分数 |
| recommendNonadExposureScore | number | 推荐位非广告曝光分数 |
| nonAcRecommendExposureScore | number | 非 AC 推荐位曝光分数 |
| recommendKeywordCount | integer | 推荐位关键词总数 |
| recommendAdKeywordCount | integer | 推荐位广告关键词数量 |
| recommendNonadKeywordCount | integer | 推荐位非广告关键词数量 |
| ppcTrafficSources | array | PPC 付费广告流量来源标记。包含：SP 广告、头部品牌广告、底部品牌广告、视频广告 |
| naturalSearchTrafficSources | array | 自然搜索流量来源标记 |
| amazonRecommendationSources | array | 亚马逊推荐流量来源标记。包含：Best Seller、AC、ER、TR、TRFOB 等 |
| promotionalDealSources | array | 促销活动流量来源标记。包含：Coupon、Limited Time Deal、Lowest Price in 30 Days 等 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
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
curl -X POST https://tool-gateway.linkfox.com/sif/asinSummary \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"searchValue": "B09V3KXJPB", "country": "US"}'
```

### 多ASIN查询

```bash
curl -X POST https://tool-gateway.linkfox.com/sif/asinSummary \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"searchValue": "B09V3KXJPB,B0BN1K7WJP", "country": "US", "pageSize": 10000, "pageNum": 1, "desc": true}'
```

### 指定日期区间 + 仅查广告流量

```bash
curl -X POST https://tool-gateway.linkfox.com/sif/asinSummary \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"searchValue": "B09V3KXJPB", "country": "US", "last7d": false, "startDate": "2026-03-08", "endDate": "2026-03-14", "conditions": "ad", "sortBy": "totalSpSocre"}'
```
