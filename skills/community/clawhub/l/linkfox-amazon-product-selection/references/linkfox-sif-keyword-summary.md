---
name: linkfox-sif-keyword-summary
description: 拆解特定关键词下各竞品ASIN的流量来源，分析自然、广告及各种推荐位的曝光占比。
---

# SIF 关键词流量来源分析（SIF Keyword Traffic Source Summary）

本技能用于查询并分析 Amazon 关键词的流量来源数据，帮助卖家理解关键词背后的流量结构——包括自然搜索、Sponsored Products（SP）广告、品牌广告、视频广告以及各类亚马逊推荐位。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 针对单个关键词，返回该关键词下出现的 ASIN 列表，及其在该关键词上的曝光分布与商品级跨渠道流量构成。
- 覆盖自然搜索、SP 广告、SB 品牌广告、SBV 视频广告、SP 推荐位、Amazon's Choice（AC）、编辑推荐（ER）、Top Rated（TR）等流量来源。
- 支持按 ASIN 过滤、指定日期区间、新进流量词、单条件筛选（如仅看自然词、仅看 SP 广告词等）。
- 支持 13 个国家站点（US/UK/DE/CA/JP/FR/ES/IT/MX/AU/AE/BR/SA）。

### ❌ 边界与限制

- **单条件筛选**：每次请求最多传一个 `condition` 值；需对比多个流量来源时须分别请求。
- **关键词语言**：`searchKeyword` 应使用目标站点对应语言以获得最佳结果。
- **结果上限**：每页最多返回 100 条记录。
- **站点覆盖**：仅支持上述 13 个站点；IN / NL / SE / PL / TR / SG 等已不可用。
- **数据范围**：聚焦关键词维度的 ASIN 流量；不返回整 ASIN 元数据、跨渠道关键词计数或变体聚合（如需请使用 `sif/asinSummary` 接口）。
- **不在范围内**：历史关键词排名趋势（用 ABA 工具）；广告出价/预算优化；评论与 Listing 内容分析；销量估算；整 ASIN 跨所有关键词的流量结构（用 SIF ASIN 流量来源工具）。

## 核心概念

SIF 关键词流量分析接口针对一个给定关键词，返回该关键词下出现的 ASIN 及其在该关键词上的曝光分布、商品级跨渠道流量构成。它回答：**这个关键词下谁在抢流量，通过哪些渠道？**

**分析的流量渠道**：

- **自然搜索**——自然搜索结果位
- **SP 广告（Sponsored Products）**——付费商品广告位（常规槽位）
- **品牌广告（SB）**——搜索页顶部与底部品牌广告位
- **视频广告（SBV）**——Sponsored Brands Video 位
- **SP 推荐位**——Trending now / Seen on social media / Customers frequently viewed / 4 stars and above
- **Amazon's Choice（AC）**——AC 徽章推荐位
- **编辑推荐（ER）**——编辑/精选推荐位
- **Top Rated（TR）**——高评分推荐位

**两套得分体系（重要，勿混用）**：

1. **商品级**字段（无前缀，如 `naturalSearchExposureScore`）：该 ASIN 在所有关键词上的整体曝光。
2. **关键词级**字段（`keyword…` 前缀，如 `keywordNaturalExposureScore`）：该 ASIN 仅在本次查询关键词上的曝光。

## 调用方式

- **API 端点**：`POST /sif/keywordSummary`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/sif_keyword_traffic.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-sif-keyword-summary-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 关键词流量概览**
查询某关键词在 US 站点的流量来源分布：
```
searchKeyword: "wireless charger", country: "US"
```

**2. 仅看自然搜索流量**
只看某关键词下出现在自然搜索结果中的 ASIN：
```
searchKeyword: "wireless charger", country: "US", condition: "nfPosition"
```

**3. 分析 SP 广告竞争**
查看某关键词下哪些 ASIN 在投 SP 广告：
```
searchKeyword: "wireless charger", country: "US", condition: "isSpAd"
```

**4. SP 推荐位**
查看出现在 SP 推荐位（Trending now、Customers frequently viewed 等）的 ASIN：
```
searchKeyword: "wireless charger", country: "US", condition: "acAd"
```

**5. 非美国站点分析**
分析日本站点的流量来源（使用当地语言关键词）：
```
searchKeyword: "ワイヤレス充電器", country: "JP"
```

**6. 聚焦特定竞品 ASIN**
限定返回少量竞品 ASIN：
```
searchKeyword: "wireless charger", country: "US", asins: "B01NBNDC1T,B09VLJJPL6"
```

**7. 自定义日期区间**
```
searchKeyword: "wireless charger", country: "US", last7d: false, startDate: "2026-04-05", endDate: "2026-04-11"
```

**8. 按整体 SP 曝光排序**
```
searchKeyword: "wireless charger", country: "US", sortBy: "totalSpSocre", desc: true
```

**9. 本期新进流量词**
```
searchKeyword: "wireless charger", country: "US", condition: "totalPeriod.in"
```

## 展示规则

1. **清晰呈现数据**：以结构化表格展示查询结果，按流量渠道曝光占比分组以便对比。
2. **区分商品级与关键词级得分**：勿混用 `naturalSearchExposureScore`（商品级）与 `keywordNaturalExposureScore`（仅本关键词）。标注列以使用户清楚所读口径。
3. **突出关键比例**：展示时强调自然搜索曝光占比与付费广告曝光占比，帮助快速判断自然/付费平衡。
4. **字段名友好化**：以用户友好语言呈现字段名，而非原始 API 字段名（如用「自然搜索曝光占比」代替 `naturalSearchExposureRatio`）。
5. **量大提示**：结果较多时展示核心数据并提示可翻页查看更多。
6. **周期标注**：对比曝光/计数时，标注解析出的时间窗口——默认 `last7d`，或自定义时为 `startDate ~ endDate`，并在每行标注 `dataPeriodStartDate`。
7. **错误处理**：查询失败时依据 `msg` 字段说明原因，并建议调整参数（如检查关键词拼写或站点代码）。
8. **百分比格式**：曝光占比以百分比展示（如 0.45 显示为「45%」）。
9. **流量来源小结**：展示单个 ASIN 数据时，提供简明流量构成小结（如「该商品 60% 曝光来自自然搜索，25% 来自 SP 广告，15% 来自品牌广告」）；用户专门询问本关键词时优先用关键词级字段。

## 用户表达与场景速查

**适用** —— Amazon 关键词流量来源与竞争结构分析：

| 用户说 | 场景 |
|--------|------|
| "这个关键词的流量从哪来" | 流量来源拆解 |
| "自然流量和付费流量各占多少" | 自然/付费占比分析 |
| "这个关键词谁在投 SP 广告" | SP 广告竞争分析（`condition=isSpAd`） |
| "哪些商品在 SP 推荐位" | SP 推荐位查询（`condition=acAd`） |
| "哪些商品有 Amazon's Choice" | AC 徽章分析（通过 `amazonsChoiceExposureScore`） |
| "这个关键词是不是被广告主导" | 广告饱和度评估 |
| "看下品牌广告竞争格局" | 品牌广告格局分析 |
| "竞品关键词的流量结构" | 竞争流量分析 |
| "哪些商品有编辑推荐" | ER 推荐位分析 |
| "对比这两个 ASIN 在本关键词下" | ASIN 过滤（`asins="B0A,B0B"`） |
| "3 月 8 日那周本关键词下的流量" | 自定义 `startDate`/`endDate` 窗口 |
| "本期新进流量词" | 新进筛选（`condition=totalPeriod.in`） |

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

# SIF-关键词流量来源 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/sif/keywordSummary`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKeyword | string | 是 | 搜索关键词，尽量翻译成对应国家站点的语言。最大长度 1000 字符 |
| country | string | 否 | 国家站点，默认 `US`。可选值（共 13 个）：`US`、`UK`、`DE`、`CA`、`JP`、`FR`、`ES`、`IT`、`MX`、`AU`、`AE`、`BR`、`SA` |
| asins | string | 否 | ASIN 过滤列表，多个用英文逗号分隔；不传则返回该关键词下所有 ASIN。最大长度 1000 字符 |
| condition | string | 否 | 条件筛选，每次只能传一个。<br>**标志类**：`nfPosition`（自然流量词）、`isSpAd`（SP广告词）、`isVedioAd`（视频广告词）、`isBrandAd`（品牌广告词）、`isPPCAd`（PPC广告词）、`isSearchRecommend`（搜索推荐词）、`acAd`（SP 推荐）<br>**周期计数类**：`totalPeriod.in`（新进全部流量词）、`nfKeywordCnt.total` / `.in`、`adKeywordCnt.total` / `.in`、`allSpKeywordCnt.total` / `.in`、`spKeywordCnt.total` / `.in`、`recSpKeywordCnt.total` / `.in`、`allSbKeywordCnt.total` / `.in`、`sbKeywordCnt.total` / `.in`、`sbvKeywordCnt.total` / `.in` |
| last7d | boolean | 否 | 是否取最近 7 天数据，默认 `true`。传 `false` 时使用 `startDate`/`endDate` 区间 |
| startDate | string | 否 | 开始日期 `yyyy-MM-dd`（`last7d=false` 时生效；不填取系统最新整周） |
| endDate | string | 否 | 结束日期 `yyyy-MM-dd`（与 `startDate` 配套） |
| sortBy | string | 否 | 排序字段。可选值：`totalKeywordNum`（全部流量词）、`naturalKeywordNum`（自然流量词）、`brandKeywordNum`（品牌广告词）、`vedioKeywordNum`（视频广告词）、`acKeywordNum`（AC推荐词）、`erKeywordNum`（ER推荐词）、`trKeywordNum`（TR推荐词）、`sumScore`（所有关键词曝光总得分）、`totalNfScore`、`totalSpSocre`（注意拼写）、`totalBrandScore`、`totalVedioScore`、`totalAcScore`、`totalTrScore`、`totalErScore` |
| pageNum | integer | 否 | 页码，默认 `1` |
| pageSize | integer | 否 | 每页数量，最小 10，最大 100，默认 `100` |
| desc | boolean | 否 | 是否降序，默认 `true` |


## 响应结构

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| code | string | 返回码 |
| msg | string | 消息 |
| total | integer | 本次实际返回的数据数量 |
| data | array | 返回数据，商品关键词流量数据对象数组 |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| title | string | 标题 |
| costTime | integer | 耗时（ms） |
| costToken | integer | 消耗token |

> 本接口不返回 `isParentAsin`、`variantsNum`、`noKeywordVariantsNum`；如需这些字段请使用 `sif/asinSummary` 接口。

### 数据项字段（`data` 数组中的每个对象）

> 两类得分：无前缀字段（如 `naturalSearchExposureScore`）为该 ASIN 在所有关键词上的商品级整体指标；`keyword*` 前缀字段（如 `keywordNaturalExposureScore`）为该 ASIN 仅在本次查询的关键词上的指标。

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN 编码 |
| productTitle | string | 商品标题 |
| productImageUrl | string | 商品主图 URL |
| productPrice | number | 商品售价 |
| customerRatingCount | integer | 客户评分总数 |
| productStarRating | number | 商品星级（0–5 星） |
| productRatingScore | number | 商品评分数值 |
| productUpdateTime | string | 产品更新时间（`yyyy-MM-dd HH:mm:ss`） |
| dataPeriodStartDate | string | 数据周期起始日期（`yyyy-MM-dd`） |
| totalExposureScore | number | 总曝光分数 |
| totalExposureRatio | number | 总流量份额 |
| naturalSearchExposureScore | number | 自然搜索曝光总分 |
| naturalSearchExposureRatio | number | 自然搜索曝光占比 |
| sponsoredProductsExposureScore | number | SP 广告曝光总分 |
| sponsoredProductsExposureRatio | number | SP 广告曝光占比 |
| brandAdExposureScore | number | 品牌广告曝光总分 |
| brandAdExposureRatio | number | 品牌广告曝光占比 |
| videoAdExposureScore | number | 视频广告曝光总分 |
| videoAdExposureRatio | number | 视频广告曝光占比 |
| amazonsChoiceExposureScore | number | AC 曝光总分 |
| amazonsChoiceExposureRatio | number | AC 曝光占比 |
| editorialRecommendationsExposureScore | number | ER 曝光总分 |
| editorialRecommendationsExposureRatio | number | ER 曝光占比 |
| topRatedExposureScore | number | TR 曝光总分 |
| topRatedExposureRatio | number | TR 曝光占比 |
| recommendPositionExposureScore | number | 推荐位曝光总分 |
| recommendAdExposureScore | number | 推荐位广告曝光分数 |
| recommendAdExposureRatio | number | 推荐位广告流量份额 |
| recommendNonadExposureScore | number | 推荐位非广告曝光分数 |
| recommendNonadExposureRatio | number | 推荐位非广告流量份额 |
| comprehensiveNaturalExposureScore | number | 综合自然流量得分（自然搜索 + 推荐位非广告） |
| comprehensiveNaturalExposureRatio | number | 综合自然流量份额 |
| keywordTotalExposureScore | number | 关键词总得分 |
| keywordNaturalExposureScore | number | 关键词自然得分 |
| keywordSponsoredProductsExposureScore | number | 关键词 SP 广告得分 |
| keywordBrandAdExposureScore | number | 关键词品牌广告得分 |
| keywordVideoAdExposureScore | number | 关键词视频广告得分 |
| keywordAmazonsChoiceExposureScore | number | 关键词 AC 得分 |
| keywordRecommendExposureScore | number | 关键词推荐位得分 |
| keywordRecommendAdExposureScore | number | 关键词推荐位广告得分 |
| keywordRecommendNonadExposureScore | number | 关键词推荐位非广告得分 |
| keywordComprehensiveNaturalExposureScore | number | 关键词综合自然得分（自然 + 推荐位非广告） |
| ppcTrafficSources | array | PPC 付费广告流量来源标记。包含：SP 广告、头部品牌广告、底部品牌广告、视频广告 |
| naturalSearchTrafficSources | array | 自然搜索流量来源标记 |
| amazonRecommendationSources | array | 亚马逊推荐流量来源标记。包含：Best Seller、AC、ER、TR、TRFOB 等 |
| promotionalDealSources | array | 促销活动流量来源标记。包含：Coupon、Limited Time Deal、Lowest Price in 30 Days 等 |

> 本接口不返回以下字段：`productCategory`、`productFeatures`、`isVariantProduct`、`isMonitored`、`monitoringStartTime`，以及 per-ASIN 的 `totalTrafficKeywordCount`、`naturalSearchKeywordCount`、`sponsoredProductsKeywordCount`、`brandAdKeywordCount`、`topBrandAdKeywordCount`、`bottomBrandAdKeywordCount`、`videoAdKeywordCount`、`amazonsChoiceKeywordCount`、`editorialRecommendationsKeywordCount`、`topRatedKeywordCount`、`frequentlyBoughtKeywordCount`。如需这些字段，请使用 `sif/asinSummary` 接口。

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
curl -X POST https://tool-gateway.linkfox.com/sif/keywordSummary \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"searchKeyword": "wireless charger", "country": "US"}'
```

### 带条件筛选（仅SP广告词）：

```bash
curl -X POST https://tool-gateway.linkfox.com/sif/keywordSummary \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"searchKeyword": "wireless charger", "country": "US", "condition": "isSpAd"}'
```

### 按 ASIN 过滤 + 指定日期区间：

```bash
curl -X POST https://tool-gateway.linkfox.com/sif/keywordSummary \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"searchKeyword": "wireless charger", "country": "US", "asins": "B01NBNDC1T,B09VLJJPL6", "last7d": false, "startDate": "2026-04-05", "endDate": "2026-04-11"}'
```

### 按 SP 曝光得分排序：

```bash
curl -X POST https://tool-gateway.linkfox.com/sif/keywordSummary \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"searchKeyword": "wireless charger", "country": "US", "sortBy": "totalSpSocre", "desc": true}'
```

### 带分页参数：

```bash
curl -X POST https://tool-gateway.linkfox.com/sif/keywordSummary \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"searchKeyword": "phone case", "country": "US", "pageNum": 2, "pageSize": 50}'
```
