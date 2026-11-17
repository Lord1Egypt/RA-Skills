# 亚马逊生态 skills

**28 个 skill**，覆盖亚马逊原生数据 + 分析工具（SellerSprite / Keepa / SIF / ABA / Alexa）+ Jiimore niche insight。

**归属 agent**：全部挂载在 `default`（主 agent），另 `linkfox-market-analysis-agent` / `linkfox-product-selection-agent` 也全部继承。数据查询类走 `default` 即可，不需要切专业 agent。

**不确定用哪个 agent？** → 用 `default`（`--model default` 或省略）。default 覆盖本桶所有 28 个 skill。

## Skills

| skill | 用途 | 入参（关键字段） | 返回摘要 |
|---|---|---|---|
| `linkfox-aba-intelligent-query` | 用自然语言查询 ABA 搜索词数据（15站近3年周维度） | `analysisDescription` (必填, 中文自然语言描述) | 搜索词列表 JSON，含 searchTerm/searchFrequencyRank/clickedAsin/clickShare/conversionShare；大结果给 downloadUrl |
| `linkfox-amazon-alexa-search` | 调用亚马逊前台 Alexa 助手做对话式选品 | `prompts` (必填, 仅1条), `url` (可选页面上下文), `format` (markdown/json) | 单轮 Q&A：Alexa 回答文本 + 推荐商品组（asin/title/price）+ followUpQuestions |
| `linkfox-amazon-category-lookup` | 查亚马逊类目节点（子节点下钻或名称模糊搜） | `--mode` (lookup/like), `nodeId` 或 `nodeLabel`, `marketId` (默认1=US) | 类目节点列表 JSON：nodeId/nodeLabel/商品数/父子关系 |
| `linkfox-amazon-opportunity-report-by-keyword` | 生成关键词六维亚马逊商业洞察报告（仅US） | `keyword` (必填), `site` (仅 US) | AI 综合 Markdown 报告：市场潜力/产品特征/评论/画像/趋势/定价 |
| `linkfox-amazon-opportunity-search-by-metrics` | 按30+商业指标反向筛选亚马逊赛道（仅US） | `keyword`/`nicheName` 或任一指标过滤器 (至少1项), `limit` | niche 列表 JSON：marketplace/keyword/市场规模/竞争/价格档/画像/评论主题 |
| `linkfox-amazon-product-detail` | 按 ASIN 拉亚马逊 listing 完整详情（22站，最多40个） | `asins` (必填, 逗号分隔), `amazonDomain` (默认 amazon.com), `deliveryZip` | listing JSON：标题/五点/A+/规格/主图与副图/价格/评分/变体/BSR |
| `linkfox-amazon-reviews-list` | 按 ASIN 拉真实评论（15站，按星级分桶抓取） | `asin` (必填), `star1Num`~`star5Num` (每档0-100), `domainCode`, `sortBy` | 评论列表 JSON：评论正文/星级/日期/verified/helpful 计数 |
| `linkfox-amazon-search` | 模拟前台搜索抓取 SERP（22站，实时排位） | `keyword`, `amazonDomain`, `sort`, `page`, `deliveryZip` | SERP 商品列表：位置/asin/标题/价格/评分/reviews/sponsored 标 |
| `linkfox-amazon-search-by-image` | 用图片URL在亚马逊做视觉相似搜（8站） | `imageUrl` (必填), `amazonDomain` (必填), `sort`, `aggregateByKeepaData` | 相似商品列表：asin/title/image/price/rating，可选 Keepa 销量/BSR 增强 |
| `linkfox-jiimore-get-niche-info` | Jiimore 按 nicheId 查细分市场详情（US/JP/DE） | `nicheId` (必填), `countryCode` (默认 US) | 单 niche 详情 JSON：市场规模/需求评分/竞争集中度/新品成功率/断货率/评论洞察 |
| `linkfox-jiimore-get-niche-info-by-keyword` | Jiimore 按关键词查所在细分市场画像列表 | `keyword` (必填, 站点语言), `countryCode`, 各类 min/max 指标过滤 | niche 列表 JSON：搜索量/销量/品牌数/头部集中度/CPC/demand 评分 |
| `linkfox-jiimore-get-niche-review-from-keyword` | Jiimore 按关键词做细分市场评论主题分析 | `keyword` (必填), `countryCode`, `sortField` | 评论主题列表：topic/type(pos/neg)/percentOfMentions/关联 niche |
| `linkfox-jiimore-page-asins-by-asin` | Jiimore 按参考 ASIN 挖同 niche 竞品列表 | `asin` (必填), `countryCode`, 价格/评论/点击/毛利等 min/max | 竞品 ASIN 列表：转化率/点击量/月销/评分/价格/FBA 费/毛利率 |
| `linkfox-jiimore-product-discovery` | Jiimore 按关键词+指标条件挖潜力商品 | `keyword` (必填), `clickConversionRateMin`, `salesVolumeT360Min` 等 | 商品列表 JSON：asin/价格/转化率/点击增长/月销/毛利率/评分 |
| `linkfox-keepa-product-request` | Keepa 按 ASIN 拉商品详情（可含12月销量与历史BSR） | `asin` (必填, 最多5个逗号分隔), `domain` (数字ID), `history` (0/1) | 详情 JSON：标题/主图/价格/尺寸/重量/BSR/月销量数组/FBA 费 |
| `linkfox-keepa-product-search` | Keepa 多维选品搜索（价格/BSR/月销/类目/关键词等） | `domain` (必填), `keyword`/`categoriesIncludeNames`, `currentSalesLte`, `monthlySoldGte` | 商品列表 JSON：asin/标题/价格/BSR/月销/上架日期/材质/近12月销量 |
| `linkfox-keepa-product-series` | Keepa 按 ASIN 拉时序历史曲线（价格/BSR/评分等） | `asin` (必填), `domain`, `showPrice`/`showBsrMain`/`showSellerCount` 等开关 | 时序 JSON：Buy Box/FBA/FBM/List/Deal 价、BSR、评分、月销量的 {time,value} 数组 |
| `linkfox-sellersprite-competitor-lookup` | 卖家精灵按 ASIN/关键词/品牌查竞品（12站，可历史月） | `marketplace`, `keyword` 或 `asinList` 或 `brand`, `dataSnapshotMonth` | 竞品列表 JSON：asin/月销量/月销售额/BSR/价格/评分/增长率 |
| `linkfox-sellersprite-market-research` | 卖家精灵按类目筛选可入市场（70+指标） | `marketplace` (必填), `nodeIdPath`/`departmentKeyword`, 各类集中度/新品占比 min/max | 类目市场列表 JSON：月均销量/销售额/集中度/FBA 占比/新品指标 |
| `linkfox-sellersprite-market-statistics` | 卖家精灵按类目节点出市场统计看板 | `marketplace` (必填), `nodeIdPath` (必填), `topN`, `newProduct` | 节点聚合统计：头部 Listing 均价/均评分/均 BSR/月销、新品数与占比 |
| `linkfox-sellersprite-product-search` | 卖家精灵商品数据库多维筛选（10站，可历史快照） | `keyword`/`nodeLabel`, `marketplace`, `minUnits`/`minProfit`/`minBsr` 等 | 商品列表 JSON：asin/价格/月销量/月营收/BSR/评分/毛利率/上架期 |
| `linkfox-sellersprite-traffic-keyword` | 卖家精灵按 ASIN 反查流量词（自然/广告位） | `marketplace` (必填), `asin` (必填), `month`, `trafficKeywordTypes` | 流量词列表：关键词/搜索量/自然排名/广告位/转化标签/流量占比类型 |
| `linkfox-sif-asin-keywords` | SIF 按 ASIN 反查关键词并给排名与流量得分（13站） | `asin` (必填), `marketplace`, 时间窗参数 | 关键词列表 JSON：keyword/自然排名/SP排名/周搜索量/自然与付费得分/转化标签 |
| `linkfox-sif-asin-summary` | SIF 拆解 ASIN 总曝光在各流量渠道的占比 | `asin` (必填), `marketplace`, 时间窗参数 | 曝光汇总 JSON：自然/SP/SB/SBV/AC/ER/TR 各渠道曝光得分与占比及新进/退出词 |
| `linkfox-sif-keyword-overview` | SIF 查关键词竞争度与供需比（13站） | `keyword` (必填, 站点语言), `country` (默认 US) | 关键词概览 JSON：周搜索量/热度排名/供需比/SP/SB/视频/AC 商品数 |
| `linkfox-sif-keyword-summary` | SIF 在给定关键词下拆解各竞品 ASIN 的流量来源 | `searchKeyword` (必填), `country`, `asins` 过滤, `condition` 过滤 | ASIN 列表 JSON：keyword级+产品级 自然/SP/SB/SBV/AC 曝光得分与关键词数 |
| `linkfox-sorftime-amazon-product-detail` | Sorftime 按 ASIN 拉详情+历史趋势（14站，2021至今） | `asin` (必填, 最多10个), `marketplace` (小写如 us/gb), `includeTrend`, 日期区间 | 详情 JSON：标题/图片/BSR/价格/月销/利润/FBA 拆解 + BSR/销量/价格时序 |
| `linkfox-sorftime-amazon-product-query` | Sorftime 多维产品搜索（14站，16种查询类型，可回看历史月） | `marketplace` (必填, 小写), `queryMode` (1/2), `queryType`, `queryValue`, `queryMonth` | 商品列表 JSON：asin/价格/月销量/月营收/BSR/评分/毛利/上架天数 |
