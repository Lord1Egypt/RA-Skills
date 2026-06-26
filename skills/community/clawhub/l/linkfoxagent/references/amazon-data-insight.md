# 亚马逊数据洞察

共 3 个工具。使用 `@工具中文名` 语法在任务提示词中调用。

本分组聚合了 LinkFox 在亚马逊侧沉淀的数据洞察能力：

- **@ABA-数据挖掘**：基于 ABA 多站点搜索词数据库做 SQL 级统计与发现，覆盖关键词热度、长尾、季节性、点击/转化占比等维度。
- **@亚马逊-商业洞察报告**：按关键词正向生成综合商业洞察报告（Markdown），覆盖市场潜力、产品特征、用户评论、客户画像、搜索趋势、定价分析六大维度。
- **@亚马逊-商业洞察(反向)**：基于历史商业洞察报告沉淀的指标池，按 30+ 项商业维度反向筛选符合条件的赛道与关键词候选。

---

### @ABA-数据挖掘

降本增效，洞察先机

工具中文名：ABA-数据挖掘
功能说明：支持亚马逊多站点的ABA进行SQL统计和数据发现，返回值的rank越小则表示排名越好。

**Prompt 模板：**

> 筛选{{美国站}}，关键词包含“{{gift}}”，{{2025年Q1}}和{{全年}}的平均搜索排名都大于{{50万}}，但最新排名冲进{{5万}}-{{10万}}的搜索词。获取搜索词、最新排名、全年平均排名、Q1平均排名、最新Top 1的ASIN。请提供下载链接。

`{{}}` 中的内容为需要替换的参数。

**参数约束：**

- **需要查询或分析的具体内容。应客观反映用户意图，不能曲解用户需求。**: 必填, `筛选美国站，关键词“gift”在过去12周的搜索热度排名。`=搜索词的热度排名趋势分析, `筛选美国站，关键词包含“gift”，2025年Q1和全年的平均搜索排名都大于50万，但最新排名冲进5万-10万的搜索词。`=潜力爆款挖掘/黑马词挖掘, `筛选美国站，最新排名在20万以内，且4周前的排名比8周前提升30%，本周的排名比4周前提升30%的搜索词。`=持续增长趋势挖掘, `筛选美国站，筛选当前搜索排名在20000以内，近三个月点击占比Top 1的Asin的转化率占比低于5%的搜索词。相同搜索词相同Asin值保留最新的一个。`=市场机会挖掘/高搜索量低垄断, `筛选美国站，包含“cup”的关键词中，去年（2024年）1-9月份排名未进入50万，10-11月份连续进入20万的词。`=节日/季节性礼物词定位, `筛选筛选美国站关键词包含“hat”的，最新搜索排名在5万-20万之间，且近3个月来点击占比大于20%，转化占比小于10%的ASIN。相同搜索词和ASIN仅保留点击占比和转化占比的比例最小数据。`=高点击低转化ASIN挖掘, `筛选美国站，关键词包含“charger”的，当前排名在20万开外的，近2个月的平均转化占比大于平均转化占比1.5倍的关键词，以及相应的ASIN。`=高ROAS长尾蓝海词库构建, `找到美国站“charger”的长尾词中，近一个月才进入排名榜单，且当前排名在50万以内的所有词。`=市场新词与新需求侦测, `筛选美国站中“table”的长尾词中，排名在10万-30万之间，且近4周的搜索排名增长50%以上的搜索词。`=捕捉细分趋势/变体增长
- **是否生成下载链接。当用户要求下载、导出、或生成下载链接时，设置为true。**: `true`=生成下载链接，可下载全量的查询结果（但不超过10000条）。, `false`=不生成下载链接。
- **调用顺序**
- **亚马逊市场（站点）**: `DE`=亚马逊-德国站, `BR`=亚马逊-巴西站, `US`=亚马逊-美国站, `CA`=亚马逊-加拿大站, `AU`=亚马逊-澳大利亚站, `JP`=亚马逊-日本站, `AE`=亚马逊-阿联酋站, `ES`=亚马逊-西班牙站, `FR`=亚马逊-法国站, `IT`=亚马逊-意大利站, `SA`=亚马逊-沙特站, `TR`=亚马逊-土耳其站, `MX`=亚马逊-墨西哥站, `SE`=亚马逊-瑞典站, `NL`=亚马逊-荷兰站

---

### @亚马逊-商业洞察报告

AI 综合商业洞察

工具中文名：亚马逊-商业洞察报告
功能说明：按亚马逊站点和关键词精准查询亚马逊站内六大核心维度（市场潜力、产品特征、用户评论、客户画像、搜索趋势、定价分析）的原始报告数据，利用 AI 进行多维交叉分析与提炼，最终生成一份综合性商业洞察报告（Markdown 格式）。

限制：当前仅支持美国站点（US）。本工具返回的数据是非结构化的 Markdown 报告，不支持 @智能数据查询 进行二次分析。

**Prompt 模板：**

> 帮我搜索{{美国站}}，关键词是{{men necklace silver}}的商业洞察报告

`{{}}` 中的内容为需要替换的参数。

**参数约束：**

- **亚马逊站点代码（当前仅支持 US）**: 必填, 默认 `US`
- **要查询洞察报告的搜索关键词**: 必填

---

### @亚马逊-商业洞察(反向)

按指标反向筛选赛道

工具中文名：亚马逊-商业洞察(反向)
功能说明：基于历史商业洞察报告沉淀的指标数据池，支持以选品视角反向筛选亚马逊赛道与关键词。能够将用户口语化的需求映射为具体的查询条件，支持通过 30+ 项商业维度（包含市场规模与增长势能、价格区间与档位份额、竞争密度与头部集中度、人群画像如年龄/性别/收入、评论卖点与痛点标签等）精准圈选细分市场。返回结构化的赛道指标对比表，辅助选品与商业决策。

限制：
1. 当前仅支持美国站点（入参固定 US）。
2. 不支持分页，默认按采集时间倒序返回最近 25 条（通过 limit 最大可至 200 条）。
3. 必须至少提供 keyword/nicheName 或任意一个指标过滤字段，禁止全量空参数。
4. 本工具返回值不落库，直接驱动前端 UI 渲染，不支持 @智能数据查询 进行二次加工。

**Prompt 模板：**

> 帮我在{{美国站}}反向筛选赛道：{{品牌数 ≤ 20，搜索量同比 ≥ 100%，新品平均评论量 ≤ 500}}，最多返回{{25}}条候选。

> 反查包含关键词“{{whoop band}}”的细分赛道，列出市场规模、增长率、品牌数、价格区间和好评/差评主题。

`{{}}` 中的内容为需要替换的参数。

**参数约束：**

> 所有参数均为可选，但必须至少传入一个文本筛选字段（keyword / nicheName）或任意指标过滤字段。完整字段、类型与取值范围以工具 inputSchema 与独立 skill `linkfox-amazon-opportunity-screener/references/api.md` 为准。

- **站点（amazonDomain）**: 闭枚举，当前仅 `US`，缺省视为美国站
- **返回条数（limit）**: 整数 1-200，默认 25
- **文本搜索**: `keyword`（关键词片段，LIKE）、`nicheName`（赛道归一名片段，snake_case，LIKE）
- **市场规模与增长**: `nicheRevenue360dMinUsdAtLeastGte/Lte`、`nicheRevenue360dMaxUsdAtLeastGte/Lte`、`nichePeakSearchVolumeAtLeastGte/Lte`、`nicheSearchVolumeYoyChangePctAtLeastGte/Lte`、`nichePeakMonthGte/Lte`（1-12）
- **竞争格局**: `nicheBrandCountGte/Lte`、`nicheBrandCountYoyChangePctAtLeastGte/Lte`、`nicheTop5ProductClickSharePctAtLeastGte/Lte`、`featureTop5BrandSharePctAtLeastGte/Lte`、`featureTopBrandsContains`（品牌名片段，区分大小写）
- **价格与档位**: `priceMinUsdGte/Lte`、`priceMaxUsdGte/Lte`、`priceSweetSpotMinUsdGte/Lte`、`priceSweetSpotMaxUsdGte/Lte`、`priceEntryClickSharePctAtLeastGte/Lte`、`priceMidClickSharePctAtLeastGte/Lte`、`priceHighClickSharePctAtLeastGte/Lte`（份额 0-100）
- **人群画像**: `demoPrimaryAgeMinGte/Lte`、`demoPrimaryAgeMaxGte/Lte`、`demoGenderDominant`（`female`/`male`/`mixed`/`unspecified`）、`demoPrimaryIncomeTier`（`low`/`middle_low`/`middle`/`middle_upper`/`upper_middle`/`high`）、`demoLifeStageTagsContains`（snake_case 片段）
- **产品特征**: `featureNewAvgReviewCountAtLeastGte/Lte`、`featureEstablishedAvgReviewCountAtLeastGte/Lte`、`featureEmergingTrendTagsContains`、`featureUncommonFeatureTagsContains`、`searchTopCategory1Label`（snake_case 片段）
- **评论卖点 / 痛点**: `reviewPositiveTop1Topic`、`reviewPositiveTop1PctAtLeastGte/Lte`、`reviewNegativeTop1Topic`、`reviewNegativeTop1PctAtLeastGte/Lte`、`reviewNegativeTop2Topic`、`reviewStrategicInsightTagsContains`（占比 0-100，标签为 snake_case 片段 LIKE）

---
