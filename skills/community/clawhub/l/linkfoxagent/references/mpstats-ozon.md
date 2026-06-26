# Mpstats-Ozon

共 6 个工具。使用 `@工具中文名` 语法在任务提示词中调用。覆盖 Ozon 俄罗斯站选品、店铺/类目/品牌下钻、商品详情批量查询与单 SKU 分日趋势。

### @Mpstats-Ozon-商品搜索

选品起点、关键词搜索

工具中文名：Mpstats-Ozon-商品搜索
功能说明：按俄语关键词、SKU 搜索 Ozon 俄罗斯站商品，返回 SKU ID、商品名称、品牌、卖家、商品页/主图链接等基础身份字段，是 Ozon 选品链路的起点。后续价格、销量、库存等业务指标请走 `@Mpstats-Ozon-商品详情`。

**Prompt 模板：**

> @Mpstats-Ozon-商品搜索 查询关键词为"{{кроссовки}}"的 Ozon 商品，统计窗口 {{2025-01-01}} 至 {{2025-01-31}}

`{{}}` 中的内容为需要替换的参数。

**参数约束：**

- **keyword**: 搜索关键词（俄语），例如 `кроссовки`(跑鞋)、`наушники`(耳机)。与 productIds 至少传一个，maxLength 1000
- **productIds**: SKU 列表（整数数组），单次最多 1000 个，例如 `[35995104, 153525562, 142257239]`
- **startDate**: 统计起始日期，格式 `YYYY-MM-DD`；留空时按一年前；最晚可选昨日
- **endDate**: 统计结束日期，格式 `YYYY-MM-DD`；留空时按昨天；最晚可选昨日

> 注：本接口单次最多返回约 36 条记录（官方上限），不暴露分页/排序/筛选入参；如需更精确结果请收窄 keyword/SKU 或日期窗口。

---

### @Mpstats-Ozon-卖家商品

卖家下钻、店铺洞察

工具中文名：Mpstats-Ozon-卖家商品
功能说明：按卖家 ID 下钻 Ozon 商品列表，返回该卖家下所有商品的销量、销售额、价格、评分、库存、周转、损失销售额、营收占比等指标。用于店铺结构分析、爆款拆解与卖家对标。

**Prompt 模板：**

> @Mpstats-Ozon-卖家商品 查询卖家 ID 为 `{{3628678}}` 的全部商品，统计期 {{2025-01-01}} 至 {{2025-01-31}}，按月销量(sales)降序，返回前 {{100}} 条

`{{}}` 中的内容为需要替换的参数。

**参数约束：**

- **sellerId**: 必填，卖家 ID（纯数字字符串），如 `3628678`，与商品列表 / 卖家榜中的卖家标识一致
- **startDate**: 统计起始日期，格式 `YYYY-MM-DD`；最晚可选昨日
- **endDate**: 统计结束日期，格式 `YYYY-MM-DD`；不得早于 startDate；最晚可选昨日
- **filters**: 数值筛选列表，每项 `{field, op, value, value2?}`，多列间 AND
  - 常用 `field`（snake_case）：`sales`(月销量)、`final_price`(售价 RUB)、`rating`(评分 0-5)、`comments`(评论数)、`balance`(库存件)、`revenue`(销售额 RUB)、`days_in_stock`(有货天数)、`turnover_days`(周转天数)、`lost_profit`(损失销售额 RUB)、`category_position`(类目排名)
  - `op`：`GTE` / `LTE` / `GT` / `LT` / `EQ` / `NOT_EQ` / `BETWEEN`（BETWEEN 需配 `value2` 作为闭区间上界）
  - 示例：`[{"field":"sales","op":"GTE","value":50},{"field":"rating","op":"GTE","value":4.5}]`
- **sortField**: 排序列名，snake_case 格式，如 `sales`/`revenue`/`final_price`/`balance`/`rating`
- **sortDirection**: `asc` 升序 / `desc` 降序
- **page**: 页码，从 1 开始
- **pageSize**: 每页行数，默认 100，取值范围 1-100
- **currency**: 金额换算货币代码，默认 `RUB`，可传 `USD`/`EUR` 等
- **currencyRate**: 自定义汇率（仅当使用非默认货币时配合 currency 使用）
- **includeFbs**: 是否纳入 FBS（卖家自发货）数据，`true`=纳入，`false`=仅 FBO

---

### @Mpstats-Ozon-类目商品

类目下钻、爆款挖掘

工具中文名：Mpstats-Ozon-类目商品
功能说明：按俄语类目全路径下钻 Ozon 商品列表，返回该类目下所有商品及其销量、销售额、价格、评分、库存、周转天数、损失销售额、营收占比、类目排名等完整指标。支持多条件筛选与排序，适用于类目爆款挖掘与蓝海洞察。

**Prompt 模板：**

> @Mpstats-Ozon-类目商品 查询类目 `{{Одежда/Женская одежда/Футболки и топы женские/Футболки и поло женские}}`，筛选 `{{月销 ≥ 50 且评分 ≥ 4.5}}` 的商品，按销售额降序返回前 {{50}} 条

`{{}}` 中的内容为需要替换的参数。

**参数约束：**

- **categoryPath**: 必填，Ozon 类目全路径，必须为俄语、与平台类目树一致，层级用 `/` 分隔。例：`Одежда/Женская одежда/Футболки и топы женские/Футболки и поло женские`、`Бытовая техника/Техника для кухни/Печи и грили/Аэрогрили`
- **startDate** / **endDate**: 统计期，格式 `YYYY-MM-DD`；endDate 不得早于 startDate；最晚可选昨日
- **filters**: 数值筛选条件列表，结构与字段同 `@Mpstats-Ozon-卖家商品`（`sales` / `final_price` / `rating` / `comments` / `balance` / `revenue` / `days_in_stock` / `turnover_days` / `lost_profit` / `category_position`；op 支持 `GTE`/`LTE`/`GT`/`LT`/`EQ`/`NOT_EQ`/`BETWEEN`）
- **sortField** / **sortDirection**: 排序列与方向，snake_case；常用 `sales`/`revenue`/`final_price`/`balance`/`rating`
- **page** / **pageSize**: 分页，默认 100/页，取值 1-100
- **currency**: 金额换算货币，默认 `RUB`，可传 `USD`/`EUR`/`CNY` 等
- **currencyRate**: 自定义汇率（配合 `currency` 使用）
- **includeFbs**: 是否纳入 FBS 数据

---

### @Mpstats-Ozon-品牌商品

品牌下钻、竞品分析

工具中文名：Mpstats-Ozon-品牌商品
功能说明：按品牌名下钻 Ozon 商品列表，返回该品牌下所有商品的销量、销售额、价格、评分、库存等指标。用于品牌对标、竞品分析与品牌商品结构研究。

**Prompt 模板：**

> @Mpstats-Ozon-品牌商品 查询品牌 `{{adidas}}` 在 {{2025-01-01}} 至 {{2025-01-31}} 的商品，按销量降序返回前 {{50}} 条

`{{}}` 中的内容为需要替换的参数。

**参数约束：**

- **brandName**: 必填，Ozon 品牌展示名称，与平台品牌字段一致（俄语或拉丁拼写），如 `adidas`、`Xiaomi`；勿填类目路径或卖家 ID
- **startDate** / **endDate**: 统计期，格式 `YYYY-MM-DD`；endDate 不得早于 startDate；最晚可选昨日
- **filters**: 数值筛选条件列表，结构与字段同 `@Mpstats-Ozon-卖家商品`
- **sortField** / **sortDirection**: 排序列与方向，snake_case
- **page** / **pageSize**: 分页，默认 100/页，取值 1-100
- **currency**: 金额换算货币，默认 `RUB`
- **currencyRate**: 自定义汇率
- **includeFbs**: 是否纳入 FBS 数据

---

### @Mpstats-Ozon-商品详情

基础数据、批量查询

工具中文名：Mpstats-Ozon-商品详情
功能说明：按 SKU 列表一次性获取一个或多个 Ozon 商品的全量详情，覆盖价格、折扣、Ozon Card 价、评分、评论数、库存、销量、销售额、有货日均销量/销售额、损失销售额、潜在销售额、上一周期对比、商品图片、上架日期、配送方案（FBO/FBS）等字段。服务端并发请求，单条失败自动重试一次，支持部分成功（含 `failures` 清单）。

**Prompt 模板：**

> @Mpstats-Ozon-商品详情 批量获取商品 `{{1786874757}}`、`{{151623766}}`、`{{142257239}}` 在 {{2025-01-01}} 至 {{2025-01-31}} 期间的全量商品详情

`{{}}` 中的内容为需要替换的参数。

**参数约束：**

- **productIds**: 必填，Ozon 商品 ID（SKU）列表（整数数组），单次最多 100 个；超过请分批调用。例：`[1786874757, 151623766]`
- **startDate** / **endDate**: 统计起止日期（整批共享），格式 `YYYY-MM-DD`；最晚可选昨日
- **includeFbs**: 是否包含 FBS 数据（整批共享）
- 单 SKU 场景也走此接口（productIds 传单元素数组）

---

### @Mpstats-Ozon-商品趋势

趋势验证、时间序列

工具中文名：Mpstats-Ozon-商品趋势
功能说明：按日期粒度返回单个 Ozon 商品的时间序列表现，包含每日销量、价格、Ozon Card 价、库存、评分、评论数、折扣、是否新品/畅销标识等，可选附带搜索位次/可见性数据。用于验证商品的增长趋势、季节性与异常波动。
限制：本工具返回的是日级时间序列数据，不支持 @智能数据查询 进行二次分析；单次查询一个 SKU；数据延迟 T-1，最晚可选昨日；`includeSearchStats` 部分赛道可能不支持。

**Prompt 模板：**

> @Mpstats-Ozon-商品趋势 查询商品 `{{1786874757}}` 在 {{2025-03-01}} 至 {{2025-03-31}} 期间的分日销量与价格趋势

`{{}}` 中的内容为需要替换的参数。

**参数约束：**

- **productId**: 必填，Ozon 商品 ID（SKU），整数，如 `1786874757`
- **startDate** / **endDate**: 必填，统计起止日 `YYYY-MM-DD`；趋势数据延迟 T-1，最晚可选昨日，不能选当日或未来
- **includeFbs**: 是否包含 FBS 数据
- **includeSearchStats**: 是否附带搜索位次 / 可见性数据，部分赛道可能不支持

---
