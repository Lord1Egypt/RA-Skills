# 数据工具字段参考手册

全流程使用 7 个数据工具，以下为每个工具的调用方式、返回字段及在全流程中的消费链路。

## 1. linkfox-amazon-product-detail

**用途**：拉取商品详情（S0 商品类型判定、S4 功能重合度对比）

**调用**：`python scripts/amazon_product_detail.py '<JSON>'`
**关键参数**：`asins`（逗号分隔，最多40个）、`amazonDomain`、`returnRelatedProducts`
**积分**：成功返回商品数 × 15

**返回字段**：

| 字段 | 类型 | 说明 | 消费步骤 |
|------|------|------|----------|
| asin | string | 商品ASIN | 全流程 |
| title | string | 商品标题 | S0/S4 |
| brand | string | 品牌名 | S0/S5 |
| price | number | 当前售价 | S3价格过滤 |
| oldPrice | number | 原价 | S0 |
| rating | number | 评分(0-5) | S0 |
| ratings | number | 评论总数 | S0基线/S5评分 |
| aboutItemFivePoint | array | 五点描述 | S0/S4功能对比 |
| itemSpecifications | dict | 规格表(key-value) | S0类型判定/S4功能对比 |
| variants | array | 变体列表(颜色/ASIN) | S0变体排除 |
| productImageUrls | array | 商品图片URL列表 | S2非标品路径 |
| thumbnail | string | 缩略图URL | S2以图搜图 |
| boughtLastMonthCount | number | 近月购买量 | S0基线 |
| badges | string | 标签(Amazon's Choice等) | S0 |
| stock | string | 库存状态 | S0 |
| productDescription | string | A+描述 | S4 |
| customerReviews | array | 评论样本 | S8 SWOT |
| reviewsSummary | string | 评论摘要 | S8 SWOT |

## 2. linkfox-amazon-search

**用途**：亚马逊前台搜索（S2 标品/混合路径候选池生成）

**调用**：`python scripts/amazon_search.py '<JSON>'`
**关键参数**：`keyword`、`amazonDomain`、`page`、`sort`
**积分**：~20/次

**返回字段**：

| 字段 | 类型 | 说明 | 消费步骤 |
|------|------|------|----------|
| asin | string | 商品ASIN | S2候选池 |
| title | string | 商品标题 | S2 |
| brand | string | 品牌名 | S2/S5 |
| price | number | 售价 | S3价格过滤 |
| rating | number | 评分 | S2 |
| ratings | number | 评论数 | S2/S5 |
| position | number | 搜索结果位置(从1开始) | S6首页判定 |
| sponsored | boolean | 是否广告位 | S6 |
| thumbnail | string | 缩略图URL | S2 |
| imageUrl | string | 主图URL | S2 |
| delivery | string | 配送信息 | S2 |
| primeEligible | boolean | Prime资格 | S2 |

## 3. linkfox-keepa-product-request

**用途**：Keepa历史数据（S3价格过滤+Keepa数据拉取、S5三模型评分）

**调用**：`python scripts/keepa_product_detail.py '<JSON>'`
**关键参数**：`asin`（逗号分隔，最多5个）、`domain`(数字)、`history`(0/1)
**积分**：~240/批(5个ASIN)

**返回字段**（history=1）：

| 字段 | 类型 | 说明 | 消费步骤 |
|------|------|------|----------|
| asin | string | 商品ASIN | 全流程 |
| title | string | 商品标题 | S2 |
| brand | string | 品牌名 | S5 |
| price | number | 当前售价 | S3价格过滤 |
| rating | number | 评分 | S5 |
| reviewCount | number | 评论总数 | S5评论差距评分 |
| salesRank | number | 当前BSR | S5 BSR差距评分 |
| salesRank30 | number | 30天BSR均值 | S5潜力股BSR改善 |
| salesRank90 | number | 90天BSR均值 | S8趋势分析 |
| salesRank180 | number | 180天BSR均值 | S5潜力股BSR改善 |
| monthlySalesUnits | number | 当月销量 | S5标杆销量规模 |
| monthlySalesUnits1-12MonthsAgo | number | 1-12月前月销量 | S5潜力股销量趋势 |
| monthlySalesRevenue | number | 月销售额 | S8 |
| fbaFees | number | FBA费用 | S8 |
| referralFeePercentage | number | 佣金比例 | S8 |
| profit | number | 单件利润 | S8 |
| packageWeight | number | 包装重量 | S8 |
| packageLength/Width/Height | number | 包装尺寸 | S8 |
| variationNum | number | 变体数量 | S5功能差异化 |
| sellerNum | number | 卖家数量 | S8 |
| fulfillment | string | 配送方式(FBA/FBM) | S8 |
| availableDate | string | 上架日期 | S5上架时间评分 |
| manufacturer | string | 制造商 | S8 |
| categoryTree | string | 类目树 | S0同类目验证 |

## 4. linkfox-sellersprite-traffic-keyword

**用途**：卖家精灵流量词反查（S3数据采集、S6首页词归因）

**调用**：`python scripts/sellersprite_traffic_keyword.py '<JSON>'`
**关键参数**：`marketplace`、`asin`、`page`、`size`(最大100)、`orderField`、`orderDesc`
**积分**：15/次（含翻页）
**翻页逻辑**：返回100条则继续翻页，<100条停止

**返回字段**：

| 字段 | 类型 | 说明 | 消费步骤 |
|------|------|------|----------|
| keyword | string | 搜索关键词 | S6首页词归因 |
| keywordCn | string | 关键词中文翻译 | S6报告 |
| trafficPercentage | number | 流量占比(0-1) | S6 |
| searches | number | 月搜索量 | S6战场排序 |
| calculatedWeeklySearches | number | 计算周搜索量 | S6 |
| searchesRank | number | 搜索热度排名 | S6 |
| rankPosition | object | 排名位置{page,position,index,pageSize} | S6首页判定(page==1) |
| badges | array | 标签[naturalSearching/amazonChoice/ads/sponsorBrand/sponsorVideo/highlyRated] | S6 AC词统计 |
| trafficKeywordType | string | 流量类型[primary/precise/preciseLongTail] | S6 |
| conversionKeywordType | string | 转化类型[excellent/stable/loss/invalid] | S6/S8 |
| naturalRatio | number | 自然流量占比(0-1) | S6 |
| adRatio | number | 广告流量占比(0-1) | S6 |
| bid | number | PPC建议竞价 | S8 |
| bidMin/bidMax | number | 竞价区间 | S8 |
| supplyDemandRatio | number | 供需比 | S8 |
| titleDensity | number | 标题密度 | S8 |
| monopolyClickRate | number | 垄断点击率 | S8 |
| top3ClickingRate | number | TOP3点击率 | S8 |
| top3ConversionRate | number | TOP3转化率 | S8 |
| clicks | number | 点击量 | S8 |
| impressions | number | 展示量 | S8 |
| purchases | number | 购买量 | S8 |
| purchaseRate | number | 购买率(0-1) | S8 |
| products | number | 竞争商品数 | S8 |
| latest1/7/30daysAds | number | 1/7/30天广告天数 | S8 |

## 5. linkfox-aba-intelligent-query

**用途**：ABA TOP3数据（S4数据采集、S7 ABA交叉对比）

**调用**：`python scripts/aba_query.py '<JSON>'`
**关键参数**：`analysisDescription`（自然语言查询描述）
**积分**：~6,500/次

**两种查询模式**：

**按关键词查**（查某个词的TOP3 ASIN）：
```
"筛选美国站最近一周搜索词为{keyword}的数据，返回clickedAsin、clickShareRank、clickShare、conversionShare"
```

**按ASIN反查**（查某个ASIN上了哪些词的TOP3）：
```
"筛选美国站最近一周被点击ASIN为{asin}的数据，返回searchTerm、clickShareRank、clickShare、conversionShare"
```

**返回字段**：

| 字段 | 类型 | 说明 | 消费步骤 |
|------|------|------|----------|
| searchTerm | string | 搜索词(按ASIN反查时) | S7 |
| clickedAsin | string | 被点击ASIN(按词查时) | S7 |
| clickedItemName | string | 商品名称(按词查时) | S7 |
| clickShareRank | string | 点击排名(1/2/3) | S7 ABA统治力 |
| clickShare | string | 点击占比(0-1) | S7 |
| conversionShare | string | 转化占比(0-1) | S7/S8 |

## 6. competitor_selector.py（评分脚本）

**用途**：三模型评分（S5 直接竞品+潜力股+标杆）

**调用**：`python competitor_selector.py --stdin < params.json`
**积分**：0（本地计算）

**输入字段**：

| 字段 | 来源 | 说明 |
|------|------|------|
| target.asin | S0 | 目标ASIN |
| target.bsr | S2 Keepa | 目标BSR |
| target.reviews | S2 Keepa | 目标评论数 |
| target.price | S2 Keepa | 目标价格 |
| target.conv_rate | S5 卖家精灵(purchaseRate加权聚合) | 目标转化率 |
| target.monthly_sales | S2 Keepa | 目标月销 |
| target.launch_date | S2 Keepa | 目标上架日期 |
| candidates[].asin | S3 | 候选ASIN |
| candidates[].bsr | S3 Keepa | 候选BSR |
| candidates[].reviews | S3 Keepa | 候选评论数 |
| candidates[].conv_rate | S3 卖家精灵(purchaseRate加权聚合) | 候选转化率 |
| candidates[].sales_history[6] | S3 Keepa | 6月月销历史 |
| candidates[].rank_30/rank_180 | S3 Keepa | BSR 30/180天均值 |
| candidates[].aba_kw_count | S4 ABA | ABA上榜词数 |
| overlap_scores{asin:ratio} | S4 AIGC | 功能/外观重合度 |

**输出字段**：

| 字段 | 说明 |
|------|------|
| direct_competitors[].score | 6维可达性总分 |
| direct_competitors[].scores.{bsr/reviews/conv/price/features/launch} | 各维度得分(1-5) |
| rising_stars[].score | 5维增长性总分 |
| rising_stars[].scores.{sales/reviews/bsr/conv/launch} | 各维度得分 |
| rising_stars[].sales_data.{history/slope/growth/recent_avg} | 销量趋势数据 |
| benchmarks[].score | 5维领先度总分 |
| benchmarks[].scores.{bsr/reviews/sales/aba/price} | 各维度得分 |
| benchmarks[].leads[] | 领先维度列表 |
| summary.{total/direct/rising/benchmark} | 各类数量统计 |

## 7. linkfox-report-generator

**用途**：HTML报告生成（S9 最终交付）

**调用**：`python scripts/inject_report.py --content-file <fragment.html> --language zh --title <slug>`
**积分**：0（本地渲染）

**输入**：HTML片段文件（按analysis-layouts.md组件库编写）
**输出**：完整HTML报告文件路径

**可用组件**：report-header / kpi-cards / content-section / chart-container / data-table / tags / quote-cards / tag-cloud / insight-list / comparison-grid / progress-bar / summary-box / swot-grid / footer / canvas-chart / data-source / evidence-image-grid

## 字段消费链路图

```
卖家精灵流量词(searches×trafficPercentage) ──→ S1核心词识别(加权TOP8)
                                ↓
Amazon前台搜索(position) ──→ S2候选池(多词共存≥2)
                                ↓
Keepa(price) ──→ S3价格过滤(±20%) + 变体排除
                                ↓
Amazon Detail(五点+规格) + AIGC ──→ S4重合度过滤(≥80%)
                                ↓
Keepa(BSR/reviews/sales_history/rank_30/rank_180) ──┐
卖家精灵(purchaseRate加权聚合) ──────────────────────→ S5三模型评分
ABA(aba_kw_count) ─────────────────────────────────┘
                                ↓
卖家精灵(rankPosition.page) ──→ S6首页词归因(唯一vs重复)
                                ↓
ABA(searchTerm/clickShareRank) ──→ S7 ABA交叉对比
                                ↓
全部数据 ──→ S8 SWOT研判(优势/劣势/机会/威胁)
                                ↓
全部数据 ──→ S9 HTML报告(9章节+图表)
```
