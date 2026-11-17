---
name: linkfox-amazon-product-selection
display_name: Linkfox 亚马逊选品
display_name_en: LinkFox Amazon Product Selection
description: 亚马逊选品一站式 AI 工具集，整合 竞品查询/ABA/前台/Keepa/Sorftime/Jungle Scout/卖家精灵/SIF/极目/商业洞察等 12 类工具 33 项子能力，覆盖选品、关键词、竞品、评论、利基与趋势。
description_zh: 亚马逊选品一站式 AI 工具集，整合 竞品查询、ABA 搜索词分析、亚马逊前台搜索/以图搜图/商品详情/评论/Alexa 导购、商业洞察六维报告、Keepa/Sorftime 历史时序、Jungle Scout/卖家精灵/SIF/极目关键词与利基市场等 12 类底层工具、33 项子能力。覆盖美国、英国、德国、日本等 15+ 站点，支持关键词挖掘、流量反查、竞品深挖、销量与价格趋势、利基竞争格局、评论痛点、AI 市场机会报告与反向赛道筛选。当用户需要亚马逊选品、市场调研、竞品分析、关键词分析、评论挖掘、历史趋势追踪或反向找赛道时触发。各子能力完整参数见 references/ 对应文件，脚本见 scripts/。
description_en: One-stop Amazon product-selection AI toolkit integrating 33 sub-capabilities across 12 tool families — competitor lookup, ABA search-term analysis, Amazon frontend search/image-search/product-detail/reviews/Alexa, business-insight six-dimension reports and reverse selection, Keepa/Sorftime historical time series, and Jungle Scout/SellerSprite/SIF/Jiimore keyword and niche analysis. Covers 15+ marketplaces (US/UK/DE/JP…) for keyword mining, traffic reverse lookup, competitor deep-dive, sales/price trends, niche competition, review pain points, AI opportunity reports and reverse niche screening. Triggered when the user needs Amazon product selection, market research, competitor analysis, keyword analysis, review mining, historical trend tracking or reverse niche discovery. Full params per sub-capability are in references/, executable scripts in scripts/.
category: e-commerce
version: 1.0.0
author: LinkFox
---

# Linkfox 亚马逊选品（Amazon Product Selection）

亚马逊选品一站式 AI 工具集，整合 **12 类底层工具、33 项子能力**，覆盖前台实时、历史时序、关键词与流量、利基市场、商业洞察与评论挖掘。各子能力完整参数、响应字段与错误码见 `references/` 下对应文件，可执行脚本见 `scripts/`。

## 能力边界

### ✅ 能力范围
- **前台实时数据**：关键词搜索排名与 SERP、以图搜图（`amazon_search`）、商品详情/五点/A+/变体（`amazon_product_detail`）、按星级筛选评论（`amazon_reviews`）、Alexa 自然语言导购（`amazon_alexa_assistant`）。
- **竞品搜索**：卖家精灵竞品查询（按关键词/ASIN/卖家/品牌/类目反查竞品，含销量、BSR、定价、评分与增长趋势，`sellersprite` 竞品查询）、极目按 ASIN 挖同细分市场竞品并按转化率/销量/价格/利润多维筛选（`jiimore` page-asins-by-asin）。
- **历史时序与趋势**：Keepa 商品详情/搜索/历史曲线（`keepa`，价格/BSR/月销/卖家数）、Sorftime 详情/搜索与趋势回看（`sorftime`，含 FBA 利润、Deal 历史、历史快照）。
- **关键词与流量分析**：ABA 搜索词挖掘（`amazon_aba_search_term`）、Jungle Scout 反查/拓展/历史/声量份额（`jungle_scout`）、SIF ASIN 关键词反查/ASIN 流量结构/关键词竞争概览/关键词下竞品流量来源拆解（`sif_search_intelligence`）、卖家精灵流量词反查（`sellersprite` 流量关键词）。
- **利基与市场分析**：极目细分市场指标/评论/竞品/潜力爆品（`jiimore`）、卖家精灵商品搜索选品、选市场列表与统计看板（`sellersprite`）、Jungle Scout 商品库与销量预估（`jungle_scout`）。
- **商业洞察与反向选品**：按关键词生成市场潜力/产品特征/评论/客户画像/搜索趋势/定价六维 AI 报告，按 30+ 商业维度反向筛选蓝海赛道（`amazon_business_insight`）。
- 覆盖美国、英国、德国、法国、日本、加拿大、意大利、西班牙、印度、墨西哥、巴西等 15+ 站点（站点集合随工具略有差异，详见各 references）。

### ❌ 边界与限制
- **API Key 必需**：所有工具均需环境变量 `LINKFOX_AGENT_API_KEY`（或 `LINKFOXAGENT_API_KEY`）；各工具独立计费、独立限频，数据时效与站点覆盖随数据源而异。
- **计费约束**：同一会话同一参数组合默认只调用一次（脚本带 24h 本地缓存）；失败或空结果不得自动换关键词、翻页或改邮编连续试探；需继续检索时先向用户说明会产生额外消耗（各工具计费规则见 `skills-version.json` 对应条目与 references 内 api.md 的 `costToken` 字段）。
- **不在范围内**：店铺运营（Listing 刊登/订单/库存，用 SP-API 系列）、广告投放与管理（用 Amazon Ads 系列）、物流与供应链规划、1688 找货源、TikTok/沃尔玛等其他平台选品、非电商任务、与平台或卖家的直接沟通、实时库存与订单处理。
- **数据时效**：前台类工具为实时抓取（含 SERP 排名、评论、Alexa）；历史类（Keepa/Sorftime/ABA）为各自数据源的更新周期，`lastUpdate`/`costToken` 等字段标识刷新与消耗。

## 工具选择指南

按需求在下表定到子能力，再跳到【业务需求路由速查】查端点/脚本/references 取参执行。

| 需求 / 用户说 | 默认推荐（子能力） | 何时换用其他 |
|---|---|---|
| ASIN 商品数据 / 价格销量趋势（"这个 ASIN 卖得怎么样"） | `linkfox-keepa-product-request`（字段最全） | 要 FBA 利润+趋势回看用 `linkfox-sorftime-amazon-product-detail`；要 A+/变体/实时价用 `linkfox-amazon-product-detail` |
| ASIN 流量词反查（"ASIN 的流量词有哪些"） | `linkfox-sif-asin-keywords`（流量词+排名+搜索量） | 要 PPC 竞价+排名难度用 `linkfox-junglescout-keyword-by-asin`；要转化类型+历史月份用 `linkfox-sellersprite-traffic-keyword` |
| 关键词拓展 / 相关流量词（"这个词有哪些相关词/长尾词"） | `linkfox-junglescout-keyword-by-keyword`（种子词拓展，含搜索量/趋势/PPC 竞价） | 要按 ASIN 反查其流量词用 `linkfox-sif-asin-keywords`；要官方搜索词排名（非拓展）用 `linkfox-aba-intelligent-query` |
| 关键词搜索量趋势（"这个词的搜索量/排名"） | `linkfox-junglescout-keyword-history`（精确搜索量） | 要官方搜索排名（非搜索量）用 `linkfox-aba-intelligent-query` |
| 商品搜索 / 选品筛选（"帮我选品 / 什么好卖"） | `linkfox-keepa-product-search`（多维+历史） | 要历史快照回看用 `linkfox-sorftime-amazon-product-query`；要毛利筛选用 `linkfox-sellersprite-product-search`；要实时 SERP 用 `linkfox-amazon-search` |
| 关键词竞争度（"这个词竞争大不大"） | `linkfox-sif-keyword-overview`（供需比+搜索量） | 要品牌声量份额用 `linkfox-junglescout-keyword-share-of-voice` |
| 利基 / 细分市场评估（"细分市场能不能进"） | `linkfox-jiimore-get-niche-info-by-keyword`（垄断/品牌/新品成功率） | 要类目维度看板用 `linkfox-sellersprite-market-research` / `-market-statistics`；要多条件筛选商品库用 `linkfox-junglescout-product-database` |
| ASIN 销量预估 | `linkfox-junglescout-sales-estimates`（日维度） | 要 12 月月销趋势用 `linkfox-keepa-product-request` |
| 利基评论 / 痛点（"评论痛点 / 差评"） | `linkfox-jiimore-get-niche-review-from-keyword`（细分市场级） | 要单 ASIN 评论用 `linkfox-amazon-reviews-list` |
| ASIN 流量结构 / 竞品分析 | `linkfox-sif-asin-summary`（ASIN 流量构成） | 要关键词下竞品流量拆解用 `linkfox-sif-keyword-summary` |
| 竞品反查（关键词/ASIN/卖家/品牌） | `linkfox-sellersprite-competitor-lookup` | 要按 ASIN 挖同细分竞品用 `linkfox-jiimore-page-asins-by-asin` |
| 六维 AI 市场报告（"AI 市场报告"） | `linkfox-amazon-opportunity-report-by-keyword` | — |
| 反向按指标找赛道（"按条件反找赛道"） | `linkfox-amazon-opportunity-search-by-metrics` | — |
| 前台实时搜索 / 以图搜图（"前台搜一下这个词"） | `linkfox-amazon-search` / `linkfox-amazon-search-by-image` | — |
| 自然语言导购（"用自然语言问亚马逊推荐"） | `linkfox-amazon-alexa-search` | — |

### 工具选择思路
- **重要**：多个子能力满足需求时，要依据需求深入分析子能力的功能、用途、出入参、从中调研出最合适的子能力，并推荐用户，让用户自己决定。
- 满足程度同等的前提下，向用户推荐“默认推荐子能力”。

## 业务需求路由速查

按【工具选择指南】定到子能力 后，下表查端点、脚本与 references 文件取参执行：

### 子能力 ↔ references 文件 ↔ 端点 ↔ 脚本（33 项）

**amazon_aba_search_term**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-aba-intelligent-query | references/linkfox-aba-intelligent-query.md | POST /aba/intelligentQuery | aba_query.py |

**amazon_alexa_assistant**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-amazon-alexa-search | references/linkfox-amazon-alexa-search.md | POST /amazon/alexaSearch | amazon_alexa_search.py |

**amazon_business_insight**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-amazon-opportunity-report-by-keyword | references/linkfox-amazon-opportunity-report-by-keyword.md | POST /amazon/opportunity/reportByKeyword | amazon_opportunity_report.py |
| linkfox-amazon-opportunity-search-by-metrics | references/linkfox-amazon-opportunity-search-by-metrics.md | POST /amazon/opportunity/searchByMetrics | amazon_opportunity_screener.py |

**amazon_search**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-amazon-search | references/linkfox-amazon-search.md | POST /amazon/search | amazon_search.py |
| linkfox-amazon-search-by-image | references/linkfox-amazon-search-by-image.md | POST /amazon/searchByImage | amazon_search_by_image.py、upload_image.py |

**amazon_product_detail**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-amazon-product-detail | references/linkfox-amazon-product-detail.md | POST /amazon/product/detail | amazon_product_detail.py |

**amazon_reviews**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-amazon-reviews-list | references/linkfox-amazon-reviews-list.md | POST /amazon/reviews/list | amazon_reviews.py |

**jiimore**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-jiimore-get-niche-info-by-keyword | references/linkfox-jiimore-get-niche-info-by-keyword.md | POST /jiimore/getNicheInfoByKeyword | jiimore_get_niche_info_by_keyword.py |
| linkfox-jiimore-get-niche-info | references/linkfox-jiimore-get-niche-info.md | POST /jiimore/getNicheInfo | jiimore_get_niche_info.py |
| linkfox-jiimore-get-niche-review-from-keyword | references/linkfox-jiimore-get-niche-review-from-keyword.md | POST /jiimore/getNicheReviewFromKeyword | jiimore_get_niche_review.py |
| linkfox-jiimore-product-discovery | references/linkfox-jiimore-product-discovery.md | POST /jiimore/productDiscovery | jiimore_product_discovery.py |
| linkfox-jiimore-page-asins-by-asin | references/linkfox-jiimore-page-asins-by-asin.md | POST /jiimore/pageAsinsByAsin | jiimore_page_asins_by_asin.py |

**jungle_scout**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-junglescout-keyword-by-asin | references/linkfox-junglescout-keyword-by-asin.md | POST /tool-jungle-scout/keywords/by-asin | junglescout_keyword_by_asin.py |
| linkfox-junglescout-keyword-by-keyword | references/linkfox-junglescout-keyword-by-keyword.md | POST /tool-jungle-scout/keywords/by-keyword | junglescout_keyword_by_keyword.py |
| linkfox-junglescout-keyword-history | references/linkfox-junglescout-keyword-history.md | POST /tool-jungle-scout/keywords/historical-search-volume | junglescout_keyword_history.py |
| linkfox-junglescout-keyword-share-of-voice | references/linkfox-junglescout-keyword-share-of-voice.md | POST /tool-jungle-scout/keywords/share-of-voice | junglescout_keyword_sov.py |
| linkfox-junglescout-product-database | references/linkfox-junglescout-product-database.md | POST /tool-jungle-scout/product-database/query | junglescout_product_database.py |
| linkfox-junglescout-sales-estimates | references/linkfox-junglescout-sales-estimates.md | POST /tool-jungle-scout/sales-estimates/query | junglescout_sales_estimates.py |

**keepa**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-keepa-product-request | references/linkfox-keepa-product-request.md | POST /keepa/productRequest | keepa_product_detail.py |
| linkfox-keepa-product-search | references/linkfox-keepa-product-search.md | POST /keepa/productSearch | keepa_product_search.py |
| linkfox-keepa-product-series | references/linkfox-keepa-product-series.md | POST /keepa/productSeries | keepa_product_history.py |

**sellersprite**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-sellersprite-competitor-lookup | references/linkfox-sellersprite-competitor-lookup.md | POST /sellersprite/competitor-lookup | sellersprite_competitor_lookup.py |
| linkfox-sellersprite-product-search | references/linkfox-sellersprite-product-search.md | POST /sellersprite/productSearch | sellersprite_product_search.py |
| linkfox-sellersprite-market-research | references/linkfox-sellersprite-market-research.md | POST /sellersprite/market/research | sellersprite_market_research.py |
| linkfox-sellersprite-market-statistics | references/linkfox-sellersprite-market-statistics.md | POST /sellersprite/market/statistics | sellersprite_market_statistics.py |
| linkfox-sellersprite-traffic-keyword | references/linkfox-sellersprite-traffic-keyword.md | POST /sellersprite/traffic/keyword | sellersprite_traffic_keyword.py |

**sif_search_intelligence**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-sif-asin-keywords | references/linkfox-sif-asin-keywords.md | POST /sif/asinKeywords | sif_asin_keywords.py |
| linkfox-sif-asin-summary | references/linkfox-sif-asin-summary.md | POST /sif/asinSummary | sif_asin_summary.py |
| linkfox-sif-keyword-overview | references/linkfox-sif-keyword-overview.md | POST /sif/keywordOverview | sif_keyword_overview.py |
| linkfox-sif-keyword-summary | references/linkfox-sif-keyword-summary.md | POST /sif/keywordSummary | sif_keyword_traffic.py |

**sorftime**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-sorftime-amazon-product-detail | references/linkfox-sorftime-amazon-product-detail.md | POST /sorftime/amazon/productDetail | sorftime_product_detail.py |
| linkfox-sorftime-amazon-product-query | references/linkfox-sorftime-amazon-product-query.md | POST /sorftime/amazon/productQuery | sorftime_product_search.py |

## 调用方式

- **网关**：`${LINKFOX_TOOL_GATEWAY}/<端点>`，请求方式 POST、Content-Type `application/json`，认证 Header `Authorization: <api_key>`（api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取；未配置按下方【解决认证和积分问题】处理）。各端点路径见下方【业务需求路由速查】与对应 references 文件。
- **Python 脚本**：每项子能力对应 `scripts/<脚本名>.py '<JSON 参数>' [--inline]`（脚本名与端点见路由速查表）。脚本内部完成网关调用、鉴权与落盘。
- **输出策略（脚本默认行为）**：始终将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/<skill>-<timestamp>.json`（`<cwd>` 为脚本执行时工作目录；`<session>` 取自环境变量 `SESSION_ID`；禁止写入 /tmp，当前目录不可写则报错）；响应体 ≤ 8 KB 落盘后完整打印到 stdout，> 8 KB 仅打印摘要（顶层字段、常见计数、最大列表长度 + 前 3 条样本）；加 `--inline` 强制全量打印（同样落盘）。
- **读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 PowerShell `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。
- **完整参数**：每个子能力的请求参数、响应字段、错误码、curl 示例见 `references/<源skill>.md`（文件内含该子能力 SKILL.md 正文与 api.md 全文）。

## 使用示例

以下按数据层给出代表性子能力的出入参示例；其余子能力参数见对应 references 文件。`domain` 为 Keepa 站点数字 ID（`1`=美/`2`=英/`3`=德/`5`=日…），`marketplace`/`amazonDomain`/`country`/`countryCode`/`region` 为各工具的站点代码，含义见 references。

### 前台实时层

**1. 关键词搜索排名（amazon_search → amazon_search.py）**
```json
{"keyword": "wireless earbuds", "amazonDomain": "amazon.com", "page": 1}
```
出参：`products[]`（asin/title/brand/price/rating/ratings/position/sponsored/imageUrl/asinUrl/delivery）、`total`、`costToken`。

**2. 以图搜图（amazon_search_by_image → amazon_search_by_image.py，需先 upload_image.py 上传）**
```json
{"imageUrl": "https://m.media-amazon.com/images/I/61pAlIX8SZL._AC_SY575_.jpg", "amazonDomain": "amazon.com", "sort": "default"}
```
出参：`products[]`（asin/title/price/oldPrice/rating/ratings/brand）；设 `aggregateByKeepaData:true` 可聚合 salesRank/monthlySalesUnits/fbaFees/profit。

**3. 商品详情（amazon_product_detail → amazon_product_detail.py）**
```json
{"asins": "B072MQ5BRX,B08N5WRWNW", "amazonDomain": "amazon.com"}
```
出参：`products[]`（asin/title/brand/price/oldPrice/rating/ratings/aboutItem/variants/customerReviews/productImageUrls）、`total`、`costToken`。

**4. 商品评论（amazon_reviews → amazon_reviews.py）**
```json
{"asin": "B08N5WRWNW", "domainCode": "com", "star1Num": 10, "star2Num": 10, "star3Num": 10, "star4Num": 10, "star5Num": 10, "sortBy": "recent"}
```
出参：`data[]`（reviewId/title/text/rating/date/userName/verified/vine/numberOfHelpful/imageUrlList/videoUrlList）、`total`、`costToken`。

**5. Alexa 导购问答（amazon_alexa_assistant → amazon_alexa_search.py）**
```json
{"prompts": ["best wireless earbuds for running"], "format": "json"}
```
出参：`data`（导购回答/推荐商品分组/ASIN 列表/可追问问题）、`resultsNum`、`costToken`。仅支持单条 prompt，追问需 agent 拼接上下文后发起新请求。

### 历史时序层

**6. Keepa 商品详情（keepa → keepa_product_detail.py）**
```json
{"asin": "B0088PUEPK", "domain": "1", "history": 1}
```
出参：`products[]`（asin/title/price/salesRank/salesRank30/90/180/monthlySalesUnits(含近12月)/monthlySalesRevenue/fbaFees/profit/rating/reviewCount/categoryTree/lastUpdate）、`costToken`。批量最多 5 个 ASIN。

**7. Sorftime 商品详情与趋势（sorftime → sorftime_product_detail.py）**
```json
{"asin": "B00FLYWNYQ", "marketplace": "us"}
```
出参：`products[]`（asin/title/price/profitRate/profitAmount/salesRank/monthlySalesUnits/rating/fbaFees/bsrRankTrend/priceTrend/rankTrend/dealTrend）、`costToken`。

### 关键词与流量层

**8. ABA 搜索词分析（amazon_aba_search_term → aba_query.py）**
```json
{"analysisDescription": "筛选美国站关键词gift在过去12周的搜索热度排名", "region": "US"}
```
出参：`tables`（搜索词/周开始日期/站点/搜索排名/点击ASIN/商品名/点击占比/转化占比）、`total`、`downloadUrl`（`createDownloadUrl:true` 时生成 CSV）、`costToken`。

**9. Jungle Scout 关键词拓展（jungle_scout → junglescout_keyword_by_keyword.py）**
```json
{"marketplace": "us", "searchTerms": "yoga mat", "needCount": 20}
```
出参：`keywordInfoList[]`（name/monthlySearchVolumeExact/monthlySearchVolumeBroad/monthlyTrend/dominantCategory/organicProductCount/ppcBidExact/ppcBidBroad/easeOfRankingScore）、`costToken`。

**10. SIF 关键词竞争概览（sif_search_intelligence → sif_keyword_overview.py）**
```json
{"keyword": "wireless charger", "country": "US"}
```
出参：`keyword`/keywordPopularityRank/estimatedWeeklySearchVolume/supplyDemandRatio/totalSearchResultProductCount/sponsoredProductsCount/paidAdvertisingProductCount/trackedAsinTotalCount。

### 利基与市场层

**11. 极目利基市场分析（jiimore → jiimore_get_niche_info_by_keyword.py）**
```json
{"keyword": "wireless earbuds", "countryCode": "US", "sortField": "demand", "sortType": "desc", "pageSize": 20}
```
出参：`data`（nicheId/nicheTitle/translationZh/demand/productCount/avgPrice/searchVolumeWeekly/unitsSoldWeekly/brandCount/top5BrandsClickShare/launchRateSemiannual/cpc）、`costToken`。

**12. 卖家精灵商品搜索选品（sellersprite → sellersprite_product_search.py）**
```json
{"keyword": "yoga mat", "marketplace": "US", "minUnits": 300, "minPrice": 10, "maxPrice": 50, "order": {"field": "total_units", "desc": "true"}, "page": 1, "size": 20}
```
出参：`products[]`（asin/title/price/月销量/月销售额/BSR/评分/毛利率/配送方式）、`total`、`costToken`。

### 商业洞察层

**13. 六维 AI 市场机会报告（amazon_business_insight → amazon_opportunity_report.py）**
```json
{"site": "US", "keyword": "ice bricks"}
```
出参：市场潜力/产品特征/用户评论/客户画像/搜索趋势/定价分析六维 AI 报告，`costTime`、`costToken`。当前仅支持 US 站。

**14. 反向选品赛道筛选（amazon_business_insight → amazon_opportunity_screener.py）**
```json
{"nicheBrandCountLte": 20, "nicheSearchVolumeYoyChangePctAtLeastGte": 100, "featureNewAvgReviewCountAtLeastLte": 500, "limit": 25}
```
出参：`data[]`（每条约 37 字段：keyword/nicheName/nicheRevenue360d/nicheBrandCount/priceMinUsd/demoGenderDominant/reviewNegativeTop1Topic…），至少一个过滤条件。计费按返回条数 N（即使 N=0 也按最低计费）。

## 展示规则

1. **客观呈现数据**：以清晰表格展示查询结果，不做主观商业建议（除非用户主动要求）；不同平台币种不同，展示价格/收入时务必提示币种（响应 `currency` 字段标明本地币种）。
2. **来源标注**：展示数据时说明来自哪个工具/数据源（Keepa/Sorftime/Jungle Scout/极目/SIF/卖家精灵/ABA/前台/商业洞察）。
3. **不可用数据**：值为 `0` 或 `-1` 的字段表示数据不可用，标注"N/A"或省略，不作实际值展示。
4. **错误处理与协同**：查询失败时根据响应 `errcode`/`errmsg` 说明原因并建议修正（ASIN 格式、站点不支持、参数越界等）；连续使用多工具时将各工具发现汇总为连贯分析，标注数据来源与时间窗。

## 解决认证和积分问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

**注意**：你是workbuddy，并且渠道是workbuddy，使用 onboarding 引导登录注册时 channel **必须**为 workbuddy。这非常重要！

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。
