# 指数信息查询 — 接口字段权威参考（v3）

本文中的路径均为 JSON 路径，`$` 表示响应根节点。字段缺失、空值或结构异常时先检查真实响应，不把 ETF 或场外基金字段套到指数对象。

## 公共请求头与约定（v3）

- 请求头：`Authorization: Bearer <token>`、`X-Caller-Type: external`，由 `scripts/api_client.py` 与 `config.py` 处理。
- **GET 接口**参数走 URL query，数组参数用英文逗号拼接的字符串；**POST 接口**参数走 JSON body。
- 除 `search/index-advanced` 外，POST 接口不再有公共 `requestId` 参数；GET 接口一律无 `requestId`。
- 响应外层信封统一为 `{success, code(string "0000"), message, data}`，无 requestId/timestamp 外层（部分接口 data 内含 serverTime）。
- 指数代码通常使用 6 位交易代码；带后缀代码读取 `sinfoWindcode` / `sInfoWindcode`。
- 批量接口（index/detail、index/valuation、index/financial-indicators 等）不再返回 `availabilityStatus` 包装：代码无效或未找到时该项直接缺失或为 `null`（如 valuation 的数组内 null 项），取值前需判空，不要编造名称、行情、估值或成分股，用自然语言说明未找到的部分。
- 指数点位不是基金净值，指数成分股不是某只基金的实际持仓，指数收益也不是跟踪基金的实际收益。
- 所有 GET 接口的数组参数均以**英文逗号拼接的字符串**传递，不要传 JSON 数组。

## 回答口径说明模板（输出必守）

回答中涉及**数值/数据时，必须随数据给出完整口径**，否则判为口径说明缺失。逐项必守：

1. **凡涉及区间（收益、涨跌幅、分位、日均成交额、年化、回撤等），必须给出区间起止日期**，不得只说"近1年/近3年"：
   - 正确示例：`近1年（2025-09-17~2026-09-17）收益 +12.3%`、`近5年分位（2021-09-17~2026-09-17）`。
   - 区间由查询日回推时，写明"自查询日（2026-09-17）往前推 N 个月/年"。
2. **凡实时/盘中行情（最新点位、最新价、涨跌幅），必须给出行情时间戳**：
   - 接口返回精确时间（如 `quote/index/list` 的 `latestQuote` 内时间）→ 写出具体日期与时分秒；
   - 接口不返回时间戳 → 如实注明"接口返回的最新一笔，无具体时间戳"，**不得编造日期/时间**。
3. **快照类数据（权重、估值、股息率、财务指标、报告期）必须给出数据截止日/报告期**（如 `rptDate`、`positionDate`、估值 `date`），不得只写"最新报告期"。
4. **口径注与正文数据一一对应**：正文引用的每个数字在口径注中都能找到取数口径，正文未出现的数字不要出现在口径注中。
5. **多个相近数字并存时（如不同区间收益、不同报告期），必须说明各自区间起点/报告期差异**。
6. **单位换算必须标注**：倍/%/亿元/亿股，换算关系在首次出现时说明。
7. **排序/筛选说明**：若排序或分页在本地完成，须说明"按 X 字段本地排序/扫描范围"；如结论用"境内指数"概括但实际含港深指数，须说明查询范围口径。
8. **口径矛盾必须解释**（如报告期 06-30 与行情日 09-17 并存、快照与分钟数据日期不同），不得同时出现冲突口径不解释。
9. **历史序列类数据（`index/*/history`）必须给出三要素**：① 查询方式口径（不传日期=最新交易日/最新报告期、`endDate` as-of、或自定义区间，写出实际起止日期或报告期）；② 数据条数与排序（如"区间内 N 个交易日，按日期倒序"）；③ **截断提示**：`truncated=true` 时必须说明"区间记录超过 500 条，仅返回最近 500 个交易日"，不得把部分数据当全量。
10. **最新类接口为空时必须兜底**：`index/valuation`（最新估值）存在间歇性返回空数组的情况，若 `$.data` 为空须改调 `index/valuation/history`（不传日期）取最新并注明 `trdDt`，不得直接回答"无数据"。

## 能力与数据路径速查

| 接口 | 结果路径 | 主要用途 |
|---|---|---|
| `POST /skill/v3/search/index-advanced` | `$.data.data[]` | 指数关键词搜索与复杂筛选（v3 改名自 search/chinaIndex） |
| `POST /skill/v3/search/index-by-stock` | `$.data.list[]` | 按成分股反查指数 |
| `POST /skill/v3/search/index-by-risk` | `$.data.data[]` | 按风险指标筛选指数（v3 新增） |
| `GET /skill/v3/index/detail` | `$.data.data[0]`（单对象） | 指数完整画像（⚠️ 实际多包一层 data 数组） |
| `POST /skill/v3/index/holdings` | `$.data.data[]` | 前十大成分股（⚠️ 实际多包一层 data+serverTime） |
| `GET /skill/v3/index/return` | `$.data.data[]` | 历史区间收益（批量） |
| `GET /skill/v3/index/interval-return` | `$.data` | 单只区间收益（v3 新增） |
| `GET /skill/v3/index/valuation` | `$.data[]` | 当前估值与历史分位（批量） |
| `GET /skill/v3/index/valuation/history` | `$.data[]`（每指数一组 `items[]`） | 估值历史序列：指定交易日/区间的 PE/PB/PS/PCF 及分位（v3.2 新增） |
| `GET /skill/v3/index/financial-indicators` | `$.data[]` | 基本面汇总指标（批量） |
| `GET /skill/v3/index/financial-indicators/history` | `$.data[]`（每指数一组 `items[]`） | 基本面历史：按报告期/区间的营收、净利润、ROE 等（v3.2 新增） |
| `GET /skill/v3/index/dividend-ratio/{indexCode}` | 顶层数组 | 股息率历史（v3 新增，单指数全量） |
| `GET /skill/v3/index/dividend-ratio/history` | `$.data[]`（每指数一组 `items[]`） | 股息率历史：批量 + 指定交易日/区间（v3.2 新增） |
| `GET /skill/v3/quote/index/list` | `$.data.data[].list[]` + `$.data.data[].latestQuote{}` | 批量快照 + 最新点位与分钟（⚠️ 实际多包一层 data 数组） |
| `GET /skill/v3/quote/index/single` | `$.data.latestQuote{}` + `$.data.list[]` | 单只指数盘口 + 分钟（v3 新增） |
| `GET /skill/v3/quote/index/realtime` | `$.data.data[]` | 一屏实时：点位+估值+跟踪产品（v3 新增） |
| `POST /skill/v3/quote/index/kline` | `$.data.candle` + `$.data.<代码>` | 指数历史K线 |
| `GET /skill/v3/discovery/hot-search-recommend` | `$.data.indexList[]` | 指数热搜推荐 |
| `GET /skill/v3/discovery/index-hot-rank` | `$.data.list[]` | 指数热度榜（v3 新增） |
| `GET /skill/v3/discovery/index-surge-rank` | `$.data.list[]` | 指数飙升榜（v3 新增） |

> ⚠️ v3 变化：`search/chinaIndex` → `search/index-advanced`；`quote/index` → `quote/index/list`；指数分钟行情由 `quote/minite`（v2）改为 `quote/index/single`（单只）与 `quote/index/list`（批量随附分钟）；`discovery/hot-search` 已删除，改用 `hot-search-recommend`/`index-hot-rank`/`index-surge-rank`。

---

## `POST /skill/v3/search/index-advanced` — 搜索中国指数（v3 改名自 search/chinaIndex）

按关键词与复杂条件检索境内指数（regionType 固定 CHINA，只覆盖境内指数），返回含随附行情、表现、估值基本面和跟踪产品的指数列表。

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `keyword` | string | 否 | 指数代码、名称或简称 |
| `pageNum` | integer | 否 | 默认1 |
| `pageSize` | integer | 否 | 默认10 |
| `filters` | object | 否 | 复杂筛选条件 |
| `fundCodes` | array | 否 | 指定指数代码集合内筛选 |
| `regionType` | string | 否 | 地区：`CHINA`（境内，默认）/ `OVERSEAS`（境外） |
| `sortField` | string | 否 | 排序字段（`trackETFScale`、`pctChg1Y` 等） |
| `sortOrder` | string | 否 | `asc` / `desc` |
| `requestId` | string | 否 | 请求唯一标识 |

`filters` 支持（数值筛选均为 `{ "min": number, "max": number }`，边界包含，只传需限制的一侧）：

- `productType[]`：产品类型多选（一级-二级-三级，用 `-` 拼接，如 `股票-规模指数（宽基）-中国-市场类型-A股`）；
- 表现区间：`pctChg1D/1W/1M/3M/TY/1Y/3Y/5Y`（⚠️ 筛选项无 6M，响应字段里有 `pctChg6M`）；
- 估值：`PETtm/PETtm5Y`、`PBLf/PBLf5Y`、`PSTtm/PSTtm5Y`（倍数及近5年分位）；
- 基本面：`dividendYield`、`ROE`、`operatingRevenueYoy`、`parentComOwnerYoy`；
- 跟踪产品：`trackETFNetInFlow`（元）、`trackETFAmount`（元）、`trackETFCount`（只）、`trackETFScale`（**万元**）、`trackETFLinkedCount`（只）、`trackETFLinkedScale`（**万元**）；
- 年度表现：`lastYearYield`、`prevYearYield`。

分页字段：`$.data.pageNum`、`pageSize`、`totalNum`、`serverTime`。

> **筛选与分页规则**：筛选类条件（表现、估值、基本面、跟踪产品区间）必须优先用 `filters` 参数在服务端完成，禁止靠翻页逐条人工过滤。搜索响应已随附行情（`lastPrice`、`changeRate`）、表现（`pctChg*`）、估值基本面和跟踪产品等字段；排序和比较基于搜索结果完成，不为每只候选重复请求详情。`pageSize` 建议直接取大值一次取回候选；翻页仅为浏览候选，根据 `totalNum` 判断是否还有未覆盖结果，仅当已取页面确实无匹配候选时才翻页，最多翻页 5 页，仍覆盖不全时在回答中说明筛选条件、覆盖范围与排序口径，不得继续扫库。确需详情时，多指数必须用批量接口一次传入全部代码，禁止逐个单查。

`$.data.data[]` 关键字段：

- 标识分类：`trdCode`、`sinfoWindcode`、`indexName`、`indexSht`、`firstClass`、`indexType`、`indexTopType`/`indexBottomType`、`creatIndexOrg`、`regionType`、`realtimeQuoteType`、`authorizedIndex`。
- ⚠️ `sinfoWindcodeHighLight`、`indexShtHighLight` 含 HTML 高亮标签，对外展示必须用不带 HighLight 的字段。
- 随附行情：`lastPrice`（点）、`changeRate`（%）。
- 表现：`pctChg1D~Bgn`（含 6M）、`lastYearYield`、`prevYearYield`。
- 估值基本面：`PETtm/PBLf/PSTtm` 及 5Y/Bgn 分位、`ROE`、`dividendYield`、营收与利润增速（`trdDt` 为基本面披露日期）。
- 跟踪产品：`trackETFCount`、`trackETFScale`（元）、`trackETFAmount`（元）、`trackETFNetInFlow`（元）、`trackETFLinkedCount`、`trackETFLinkedScale`（元）。⚠️ 筛选口径与响应单位不一致：`filters.trackETFScale/trackETFLinkedScale` 按**万元**传区间，响应同名字段为**元**。
- 代表产品：`maxScaleFund`、`maxExcessReturnFund`、`minTrackErrorFund`（各自 fundScale 万元）。
- 产品列表：`relatedETF[]`（fundScale 万元）、`relatedOutIndex[]`（fundScale **元**，与详情接口口径一致）。

---

## `POST /skill/v3/search/index-by-stock` — 按成分股反查指数

根据股票代码列表搜索包含这些股票的指数，返回指数列表及成分股持仓占比。

**请求体**：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `stockCodes` | array | 是 | 股票代码列表（6位数字，不带交易所后缀），如 ["600519","000858"] |
| `onlyIncludeFullMatch` | string | 否 | `Y`=仅返回同时包含全部输入股票的指数，`N`=任意包含（默认） |
| `showOnlyMaxIndexScaleMatch` | string | 否 | `Y`=仅返回相同指数分类中跟踪规模最大的指数 |
| `pageNum` / `pageSize` | number | 否 | 默认 1/10 |

**最终数据路径**：`$.data.list[]`；分页信息在 `$.data.currentPage`、`totalPage`、`totalCount`；`$.data.maxHoldNavRat` 为最大持仓占比。

`$.data.list[]` 字段（⚠️ 实测 list 项**仅以下 7 个字段**，不要读取不存在的 matchedStocks/indexCode/weight/holdings/trackETFs 等）：

| 字段 | 说明 |
|---|---|
| `trdCode` | 指数代码 |
| `indexName` / `indexSht` | 指数名称、简称 |
| `indexType` | 指数分类 |
| `sInfoWindcode` | 指数万德代码（⚠️ 大写 S） |
| `totalRatio` | 查询股票的成分股权重合计（%） |
| `holdingsDetail` | 查询股票在指数中的权重明细（**仅** `stockCode`、`secuSht`、`holdNavRat` 三个子字段） |

辅助回显：`$.data.requestList[]`（回显请求股票：`stockCode`、`secuSht`、`holdNavRat`、`labelCode`、`labelName`）；分页在 `$.data.currentPage`、`totalPage`、`totalCount`；`$.data.maxHoldNavRat` 为最大持仓占比。⚠️ 实际响应**无** `matchedStocks` 字段。

---

## `POST /skill/v3/search/index-by-risk` — 按风险指标筛选指数（v3 新增）

按风险收益指标（夏普、最大回撤、年化波动、年化收益）区间筛选指数。适用于「低回撤高夏普的指数」类问题。

**请求体**（均为可选区间，只传需限制的一侧；`min`/`max` 边界包含）：

| 参数 | 类型 | 说明 |
|---|---|---|
| `keyword` | string | 关键词 |
| `indexCodes` | array | 指定代码集合内筛选 |
| `indexType` | string | 指数类型 |
| `timePeriod` | string | 统计周期（如 `1Y`/`3Y`/`5Y`） |
| `sharpRatioMin` / `sharpRatioMax` | number | 夏普比率区间 |
| `maxDownMin` / `maxDownMax` | number | 最大回撤区间（%，负值） |
| `annualizedVolMin` / `annualizedVolMax` | number | 年化波动率区间（%） |
| `annualizedReturnMin` / `annualizedReturnMax` | number | 年化收益率区间（%） |
| `sortField` / `sortOrder` | string | 排序字段 / asc/desc |
| `page` / `pageSize` | number | 分页 |
| `requestId` | string | 请求唯一标识 |

**最终数据路径**：`$.data.data[]`；分页在 `$.data.pageNum`、`pageSize`、`totalNum`、`serverTime`。

---

## `GET /skill/v3/index/detail` — 指数详情（v3 起单对象平铺）

查询单只指数的完整画像：分类、编制机构、跟踪产品、年化表现、波动、回撤、市值分布、行业分布、估值分位等。

**请求参数**（URL query）：`indexCodes`（string，指数代码，**逗号分隔，一次最多 20 个**，如 `000300,399006`）

**最终数据路径**：`$.data.data[0]`（⚠️ 实际响应为 `{serverTime, data:[单元素数组]}`，指数对象在 `data.data[0]`，不是单对象平铺；也不再按代码分组返回、无 availabilityStatus/detail 包装）

> ⚠️ 由于响应是 `data.data[0]` 单对象，如需多只指数详情请逐只调用本接口（每次传一只）或改用 `quote/index/realtime`/`search/index-advanced` 的组合字段；不要把数组期望套在单对象上。

`$.data.data[0]` 字段：

| 字段 | 说明 |
|---|---|
| `trdCode` / `sinfoWindcode` / `indexName` / `indexSht` | 指数代码、万德代码、名称、简称 |
| `indexType` / `firstClass` / `secondClass` / `thirdClassMarketType` / `thirdClassMarketValue` / `className` | 指数分类 |
| `relatedETF[]` / `relatedOutIndex[]` | 跟踪 ETF / 场外基金（`trdCode`、`fundSht`、`fundType`、`fundScale`） |
| `trackETFCount` / `trackETFScale` / `trackETFLinkedCount` / `trackETFLinkedScale` | 跟踪产品数量与规模（⚠️ `trackETFScale`/`trackETFLinkedScale` 为**万元**口径，÷1e4=亿；与 search/realtime 的元口径不同） |
| `maxScaleFund` / `maxExcessReturnFund` / `minTrackErrorFund` | 代表产品（`trdCode`、`fundSht`、`fundType`、`fundScale`） |
| `annualizedReturn1Y~Bgn` | 年化收益率（%） |
| `pctChg1Y~Bgn` | 涨跌幅（%） |
| `annualizedVol1Y~Bgn` / `volatility1Y~Bgn` | 年化波动率（%）/ 波动率（⚠️ `volatility1Y` 为日波动率，量级约 1；`annualizedVol1Y` 为年化值约 18，两者不同口径，勿混淆） |
| `maxDown1Y~Bgn` | 最大回撤（%） |
| `sharpRatio1Y~Bgn` | 夏普比率 |
| `marketCapDistTrdDt` / `largeCapStocks`（数量）/ `largeCapStocksProportion`（%）/ `midCapStocks` / `midCapStocksProportion` / `smallCapStocks` / `smallCapStocksProportion` | 市值分布：大/中/小盘股票**数量**与**占比**（%）——数量和占比是两个独立字段 |
| `industryDistribution[]` | 行业分布：`industryName`、`industryWeight`（%）、`industryWeightOrder` |
| `eodPriceJson` / `financialIndicatorJson` / `valuationPercentileJson` / `dividendRatioJson` | 数据文件路径，不当作内嵌 JSON 解析 |
| `pubDt` / `baseDt` / `lastYearYield` / `prevYearYield` | 数据日期与年度表现 |

---

## `POST /skill/v3/index/holdings` — 前十大成分股（v3 平铺列表）

批量查询指数前十大成分股。

**请求体**：`fundCodes`（array，指数代码列表，最多 **20** 个）、`date`（string，可选，yyyy-MM-dd，不传返回最新报告期）

**最终数据路径**：`$.data.data[]`（⚠️ 实际响应为 `{serverTime, data:[...]}`，列表在 `data.data` 下；v3 起为**平铺列表**，不再按指数分组，也无 fundCode/availabilityStatus/holdingItems 包装）

| 字段 | 说明 |
|---|---|
| `trdCode` | 指数代码 |
| `trdDt` | 报告期，yyyy-MM-dd |
| `stockCode` / `stockSht` | 股票代码、简称 |
| `weight` | 权重（%） |
| `rn` | 排名（1=第一大） |
| `swfirstClass` / `swsecondClass` / `swthirdClass` | 申万行业分类 |

> ⚠️ v3 平铺后：多指数结果混在一个数组里，回答"每只指数的前十大成分股"时必须按 `trdCode` 分组再展示。

---

## `GET /skill/v3/index/return` — 批量指数区间收益

批量查询多只指数在预设周期或自定义区间内的收益率（%）。

**请求参数**（URL query）：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `codes` | string | 是 | 指数代码，逗号分隔，最多 **20** 只 |
| `timeMode` | string | 是 | `PERIOD` / `RANGE` |
| `period` | string | PERIOD时必填 | `1M/3M/6M/1Y/3Y/5Y/10Y/TY/INCE` ⚠️ v3 无 1D/1W |
| `startDate` / `endDate` | string | RANGE时必填 | yyyy-MM-dd |
| `boundaryMatchMode` | string | 否 | `FLEXIBLE`（默认）/ `STRICT` |

> ⚠️ **默认使用 FLEXIBLE（可省略）**：边界非交易日时自动收缩到最近可交易日，返回实际区间与收益率。仅在用户**明确要求严格边界**时才用 STRICT；且 **STRICT 遇非交易日边界会直接报错**（success:false，提示建议前后交易日，如"开始日期 2025-01-01 不是交易日"），此时应如实转述接口错误信息，并建议改用 FLEXIBLE 重查后展示实际收缩的起止日期与收益率，不得凭空断言"无法返回数据"。

**最终数据路径**：`$.data.data[]`（⚠️ v3 多包一层 data）

| 字段 | 说明 |
|---|---|
| `code` | 指数代码 ⚠️ v3 字段是 `code`（v2 为 fundCode/trdCode） |
| `startDate` / `endDate` | 实际区间起止日期 |
| `returnRate` | 区间收益率（%，null 判空处理） |
| `availabilityStatus` | 有数据 / 历史查询无数据 / 不支持的期间 / 系统异常 等 |

> ⚠️ `availabilityStatus`≠有数据 时 `returnRate` 为 null，用 `.get('returnRate')` 取值，不把无数据当 0；展示以返回的 startDate/endDate 为准。
>
> ⚠️ 本接口无预设"今年以来"周期（period 无 YTD），查"今年以来"用 RANGE 模式（startDate=当年1月1日）。

---

## `GET /skill/v3/index/interval-return` — 单只指数区间收益（v3 新增）

查询**单只**指数的区间收益率（%）。与 `index/return` 区别：一次只查一只，返回单对象。

**请求参数**（URL query）：`code`（string，单只指数代码）、`timeMode`（`PERIOD`/`RANGE`）、`period`、`startDate`/`endDate`、`boundaryMatchMode`（同上）。

**最终数据路径**：`$.data`（单对象）

| 字段 | 说明 |
|---|---|
| `code` | 指数代码 |
| `startDate` / `endDate` | 实际区间起止日期 |
| `returnRate` | 区间收益率（%，null 判空处理） |
| `availabilityStatus` | 数据可用性状态 |
| `serverTime` | 服务器时间 |

---

## `GET /skill/v3/index/valuation` — 指数估值与历史分位

批量查询指数当前估值倍数及其历史分位。PE/PB/PS 的倍数与分位为主；⚠️ **实际返回还含 PCF 系列字段**（pCFTtm/pCFTtm1Y~10Y 等），与 v3 spec 声称"已删除 PCF"矛盾，以实际返回为准——需要 PCF 时可直接读。

**请求参数**（URL query）：`indexCodes`（string，指数代码，逗号分隔）

**最终数据路径**：`$.data[]`（数组，每项一只指数）

| 字段 | 说明 |
|---|---|
| `pETtm` / `pETtm1Y~10Y/Bgn/TY` | PE-TTM 倍数及历史分位（%）⚠️ v3 字段为**小写 p**开头（pETtm），不是 v2 的 PETtm；分位后缀含 `3M`（近3月）、`6M`、`1Y`、`2Y`、`3Y`、`5Y`、`10Y`、`Bgn`（成立以来）、`TY`（今年） |
| `pBLf` / `pBLf*` | PB-LF 倍数及分位 |
| `pSTtm` / `pSTtm*` | PS-TTM 倍数及分位 |
| `pCFTtm` / `pCFTtm*` | 现金流倍数及分位（⚠️ 实际返回仍有，与 spec 声称"v3 删除"矛盾） |
| `trdCode` | 指数代码 |
| `trdDt` | 估值数据日期 |

> ⚠️ 倍数与分位单位不同：`pETtm` 等为倍数（倍），`pETtm5Y` 等为分位百分比（%），展示时必须区分并注明 trdDt。
>
> 🔴 **回答要求（必守）：估值倍数必须与历史分位成对给出。** 用本接口回答 PE/PB/PS（或"估值/贵不贵/处于什么位置"）类问题时，**只给倍数视为不合格**：须同时给出对应分位（默认取 `pETtm5Y`/`pBLf5Y`/`pSTtm5Y` 近5年分位；用户指定窗口则用其窗口，如 `*3Y`、`*Bgn`），并注明分位窗口（含起止日期）与数据日期 `trdDt`；分位缺失时须说明原因（接口未返回、指数成立时间不足等），不得省略或编造。
>
> ⚠️ **实测（2026-09）**：接口正常返回数据（此前一度返回空数组，已恢复）。无效指数代码（如 H30374）时数组内该项为 `null`，取值前需判空（`item and item.get('pETtm')`），不把 null 当作 0 或跳过其他正常项。
>
> ⚠️ **实测（2026-10-08）**：本接口**再次持续返回空数组**（`data: []`，连续 6/6 次，000300/000905/399006/000852 均空），而同期 `index/financial-indicators`、`index/dividend-ratio/{indexCode}` 正常。属**间歇性空数组**问题。
> **兜底规则（必守）**：调用本接口后若 `$.data` 为空数组，**必须改调 `index/valuation/history`（不传日期即可取最新交易日）**，用其 `items[0]` 作为最新估值取值，并在回答中注明数据日期 `trdDt`；不得因本接口为空就回答"无估值数据"。

---

## `GET /skill/v3/index/valuation/history` — 指数估值历史序列（v3.2 新增）

批量获取**多个指数指定交易日/日期区间的估值历史明细**（PE-TTM、PB-LF、PS-TTM、**PCF-TTM** 及各自 `3M/6M/1Y/2Y/3Y/5Y/10Y/TY/Bgn` 百分位）。用于"估值历史走势/某日估值/分位变化"类问题；查"当前最新估值"优先用 `index/valuation`（为空时用本接口兜底）。

**请求参数**（URL query）：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `indexCodes` | string | 是 | 指数代码，多个用**英文逗号**拼接，**最多 20 个**（超限报错「单次请求数量不能超过20个」） |
| `beginDate` | string | 否 | 交易日开始日期 `yyyy-MM-dd`，需与 `endDate` 配合 |
| `endDate` | string | 否 | 单传=截至该日最近交易日（**as-of，自动吸收周末/节假日**，如传周日返回上周五）；配合 `beginDate`=日期区间 |

**日期语义**：不传日期=最新交易日（返回 1 条）；只传 `endDate`=as-of 单日；`beginDate`+`endDate`=区间（`items` 按 `trdDt` **倒序**）。`beginDate` 晚于 `endDate` 会报错「开始日期不能晚于结束日期」。

**最终数据路径**：`$.data[]`（数组，每指数一组）

| 字段 | 说明 |
|---|---|
| `trdCode` | 指数代码 |
| `availabilityStatus` | `有数据` / `无符合条件的数据`（如区间内全为非交易日） |
| `truncated` | 区间内交易日记录 >**500** 行时为 `true`，`items` 仅保留**最近 500 条** |
| `items[]` | 交易日记录（倒序），每项含 `trdDt` + 41 个估值字段 |

**`items[]` 字段（共 41 个）**：`trdDt`；`pETtm`/`pBLf`/`pSTtm`/`pCFTtm`（倍数）及其各自 `3M`/`6M`/`1Y`/`2Y`/`3Y`/`5Y`/`10Y`/`TY`/`Bgn` 分位（%）。⚠️ 字段为**小写 p 开头**；倍数与分位单位不同，展示必须区分。

> 🔴 **回答要求（必守）：倍数与分位成对给出。** 用本接口回答"某日/某区间估值"时，除 PE/PB/PS 倍数外必须同时给出对应分位（该交易日记录内自带各窗口分位，直接取用），并注明该分位对应的窗口与 `trdDt`；不得只回答倍数。

> ⚠️ **实测（2026-10-08 验证）**：无日期→1 条（`trdDt=2026-09-29`）；区间 `2026-08-01~2026-09-30`→41 条倒序；长区间（约 900 交易日）→`truncated=true`、`items=500`、范围收敛为最近 500 个交易日。**PCF 系列（`pCFTtm*`）实际存在**，与 spec 声称"删除 PCF"矛盾，以实际返回为准。
> ⚠️ 无效代码（如 `999999`）→ `data=[]` 且 `message` 提示「查询完成，但以下代码不是有效指数类型: …」，**不会**返回 `availabilityStatus="未找到该指数"` 的占位项；混合传入时只返回有效组。
>
> 💡 **长区间取数技巧（先判 `truncated`）**：需要超过 500 个交易日的历史时，先看返回的 `truncated`——
> - `truncated=false`：数据完整，直接使用；
> - `truncated=true`：单次只拿到**最近 500 个交易日**。此时可**分段查询**（如按年切分为多个区间分别调用）再按 `trdDt` 拼接，得到完整序列；
> - 采用分段拼接时，回答中必须说明**分段方式、合计条数与实际覆盖的起止日期**，不得表述为"接口一次性返回全部"；若未分段，则必须说明"区间超过 500 条，仅覆盖最近 500 个交易日"。
>
> 同类口径同样适用于 `index/dividend-ratio/history`（两者都有 `truncated` 字段）。

---

## `GET /skill/v3/index/financial-indicators` — 基本面汇总指标

批量查询指数的 ROE、股息率、营收与利润增速等基本面指标。

**请求参数**（URL query）：`indexCodes`（string，指数代码，逗号分隔）

**最终数据路径**：`$.data[]`

| 字段 | 说明 |
|---|---|
| `rOE` | 净资产收益率 ROE（%）⚠️ 注意大小写 rOE |
| `dividendYield` | 股息率（%） |
| `operatingIncome` / `parentComOwners` | 营业收入 / 归母净利润（**万元**，÷1e4=亿） |
| `operatingRevenueYoy` / `parentComOwnerYoy` | 营收同比 / 归母净利润同比（%） |
| `trdCode` / `trdDt` | 指数代码 / 披露日期 |

---

## `GET /skill/v3/index/financial-indicators/history` — 指数基本面历史序列（v3.2 新增）

批量获取**多个指数指定报告期/日期区间的基本面历史指标**（营业收入、归母净利润、ROE、同比等），用于"历史营收/净利润趋势、多期对比"类问题；查最新一期用 `index/financial-indicators`。

**请求参数**（URL query）：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `indexCodes` | string | 是 | 指数代码，逗号拼接，**最多 20 个** |
| `beginDate` | string | 否 | 报告期开始日期 `yyyy-MM-dd`，需与 `endDate` 配合 |
| `endDate` | string | 否 | 单传=**指定报告期**（填季度末，如 `2025-09-30` 表示 2025 年三季度）；配合 `beginDate`=报告期区间 |

**日期语义**：不传日期=最新报告期；`items` 按报告期（`trdDt`）**倒序**。报告期数量天然有限（实测 2015 年至今约 46 期），**本接口无 `truncated` 字段**。

**最终数据路径**：`$.data[]`（数组，每指数一组）

| 字段 | 说明 |
|---|---|
| `trdCode` / `availabilityStatus` | 指数代码 / 数据可用性 |
| `items[]` | 报告期记录（倒序） |

**`items[]` 字段**：`trdDt`（报告期，季度末）、`operatingIncome`（营业收入，**万元**）、`operatingRevenueYoy`（营收同比 %）、`parentComOwners`（归母净利润，**万元**）、`parentComOwnerYoy`（归母净利润同比 %）、`netProfitYoy`（净利润同比 %）、`rOE`（ROE %）、`calcNc` / `indexNc`（计算用/指数成分数量）。

> ⚠️ **实测（2026-10-08 验证）**：不传日期→`trdDt=2026-06-30`；`endDate=2025-09-30`→恰为 2025Q3；区间 `2024-01-01~2025-12-31`→8 个报告期倒序。**金额单位（万元）与 `index/financial-indicators` 完全一致**（同报告期 `operatingIncome`、`rOE` 数值相同），无需换算差异。
> ⚠️ **金额为年内累计口径**：`trdDt=03-31` 为一季度、`06-30` 为半年报、`09-30` 为三季报、`12-31` 为**全年**（实测 000905：2026-06-30 营收 54963 亿 vs 2025-12-31 全年 110035 亿）。**跨报告期比较时必须说明各自累计区间**（半年报对半年报、年报对年报），不得把"半年报 vs 年报"直接当作环比。

---

## `GET /skill/v3/index/dividend-ratio/{indexCode}` — 股息率历史（v3 新增）

查询指数历史股息率序列。⚠️ 注意：该接口路径带路径参数，且**响应是顶层数组**（不在 `$.data` 下）。

**请求参数**（URL query）：`indexCode`（string，指数代码）

**最终数据路径**：响应顶层数组（⚠️ 不是 `$.data`，直接是 `[{...}]`）

| 字段 | 说明 |
|---|---|
| `trdCode` | 指数代码 |
| `trdDt` | 数据日期 |
| `dividendYield` | 股息率（%） |

> 本接口返回**单指数全量历史**（实测 000300 返回 5220 条，自 2005-04-08 起）；需要**批量**或**指定日期/区间**时用下方的 `index/dividend-ratio/history`。

---

## `GET /skill/v3/index/dividend-ratio/history` — 指数股息率历史（批量/区间，v3.2 新增）

批量获取**多个指数指定交易日/日期区间的股息率历史明细**，用于"股息率历史走势、某日股息率、多指数股息率对比"类问题。

**请求参数**（URL query）：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `indexCodes` | string | 是 | 指数代码，逗号拼接，**最多 20 个** |
| `beginDate` | string | 否 | 交易日开始日期 `yyyy-MM-dd` |
| `endDate` | string | 否 | 单传=截至该日最近交易日（**as-of**，自动吸收周末/节假日）；配合 `beginDate`=日期区间 |

**最终数据路径**：`$.data[]`（数组，每指数一组）

| 字段 | 说明 |
|---|---|
| `trdCode` / `availabilityStatus` | 指数代码 / 数据可用性 |
| `truncated` | 区间内交易日记录 >**500** 行时为 `true`，仅保留**最近 500 条** |
| `items[]` | 交易日记录（倒序）：`trdDt`（数据日期）、`dividendYield`（股息率 %） |

> ⚠️ **实测（2026-10-08 验证）**：不传日期→1 条最新（`trdDt=2026-09-29`）；`endDate=2025-06-29`（周日）→返回 `2025-06-27`（周五，as-of 生效）；区间 `2026-09-01~2026-09-30`→20 条倒序；长区间（2015 年至今）→`truncated=true`、`items=500`，范围收敛为最近 500 个交易日。
> ⚠️ 无效代码 → `data=[]` + `message` 提示「不是有效指数类型」；`beginDate` 晚于 `endDate` → 报错「开始日期不能晚于结束日期」。

---

## `GET /skill/v3/quote/index/list` — 批量指数行情（v3 改名自 quote/index）

> **调用前检查**：`search/index-advanced` 的响应**已随附**行情（`lastPrice`、`changeRate`）、表现（`pctChg*`）、估值与基本面（`PETtm`/`PETtm5Y`/`PBLf`/`PBLf5Y`/`ROE`/`dividendYield`）及跟踪产品（`trackETFScale` 等）字段，**禁止为这些字段重复调用本接口**；本接口用于需要批量精简行情+当日分钟快照、或搜索未覆盖的代码集合的场景。

批量获取多个指数的最新点位、涨跌、成交与当日分钟序列。

**请求参数**（URL query）：`indexCodes`（string，指数代码，逗号分隔）

**最终数据路径**：`$.data.data[].{latestQuote, yesterdayClosePrice, serverTime, list}`（⚠️ 实际响应为 `{serverTime, data:[每只指数一项]}`，行情对象在 `data.data[]` 下，不是 `$.data.list[]`）。

| 字段 | 说明 |
|---|---|
| `latestQuote{}` | 最新行情快照：`date`（yyyyMMdd 整数）+ `timeStamp`（HHmmss 整数）精确行情时间、`symbol`、`lastPrice`（点）、`dealVolume`、`dealBalance`、`iopv`、`changeRate`（%）、`turnoverRatio`、`yesterdayClosePrice`、`changeValue`（涨跌额，点） |
| `list[]` | 当日分钟序列：`minute`（分钟时间戳，如 930）、`lastPrice`、`changeRate` |
| `yesterdayClosePrice` | 昨收（点） |

> `date + timeStamp` 是行情数据时间，`serverTime` 是服务器时间；非交易时段表述为"接口返回的最新一笔行情"。

---

## `GET /skill/v3/quote/index/single` — 单只指数盘口+分钟（v3 新增，承接原 quote/minite 的指数分钟）

查询**单只**指数的完整盘口快照与当日分钟序列。v3 起指数分钟行情可通过本接口（单只）或 `quote/index/list`（批量随附，实测每只同样返回当日每分钟）获取；只需单只时用本接口，需要多只时用批量接口一次取回。

**请求参数**（URL query）：`symbol`（string，单只指数代码）

**最终数据路径**：`$.data.latestQuote{}` + `$.data.list[]`；`$.data.serverTime` 为服务器时间。

`latestQuote{}` 字段：`date` + `timeStamp`（精确行情时间）、`symbol`、`lastPrice`（点）、`dealVolume`、`dealBalance`、`iopv`、`changeRate`（%）、`turnoverRatio`、`yesterdayClosePrice`、`changeValue`（涨跌额，点）。

`list[]` 字段：`minute`（分钟时间戳，如 930 表示 9:30）、`lastPrice`、`changeRate`。

> "上午走势/分时"类问题读取 `list[]`，最新一笔以 `latestQuote` 为准并注明精确行情时间。

---

## `GET /skill/v3/quote/index/realtime` — 指数一屏实时（v3 新增）

> **一屏能力**：本接口同时返回最新点位与涨跌（`lastPrice`/`changeRate`）、估值及历史分位（`PETtm`/`PETtm5Y`/`PBLf`/`PBLf5Y`/`PSTtm`）、基本面（`ROE`、`dividendYield`）与跟踪产品规模（`trackETFScale` 等），"一屏看收盘/估值/基本面"类问题用本接口一次即可，无需再叠加 `quote/index/list` 或 `index/valuation`。

批量获取指数的"一屏"数据：实时点位涨跌 + 估值（PE/PB/PS 及分位）+ 表现（各周期涨跌幅）+ 跟踪产品规模。适用于「一屏看多只指数的点位、估值、规模」类问题。

**请求参数**（URL query）：`indexCodes`（string，指数代码，逗号分隔）

**最终数据路径**：`$.data.data[]`（⚠️ 多包一层 data；`$.data.serverTime` 为服务器时间）

`$.data.data[]` 字段（每项一只指数）：

| 字段 | 说明 |
|---|---|
| `indexName` / `indexSht` / `indexCode` / `indexType` / `sinfoWindcode` / `firstClass` / `indexTopType` / `indexBottomType` | 标识与分类 |
| `lastPrice` / `changeRate` | 最新点位 / 涨跌幅（%） |
| `pctChg1D~Bgn` | 各周期涨跌幅（%） |
| `PETtm` / `PETtm5Y` / `PBLf` / `PBLf5Y` / `PSTtm` / `PSTtm5Y` | 估值倍数与近5年分位 ⚠️ 此处为大写（与 index/valuation 的小写 p 不同） |
| `ROE` / `dividendYield` / `operatingRevenueYoy` / `parentComOwnerYoy` | 基本面 |
| `trackETFCount` / `trackETFScale` / `trackETFAmount` / `trackETFNetInFlow` / `trackETFLinkedCount` / `trackETFLinkedScale` | 跟踪产品 |
| `maxScaleFund` / `maxExcessReturnFund` / `minTrackErrorFund` | 代表产品（fundSht/trdCode/fundType/fundScale） |
| `relatedETF[]` / `relatedOutIndex[]` | 跟踪 ETF / 场外基金 |

> 🔴 **回答要求（必守）**：用本接口回答估值时，`PETtm`/`PBLf`/`PSTtm` 等倍数必须与 `PETtm5Y`/`PBLf5Y`/`PSTtm5Y` 近5年分位**成对给出**，不得只报倍数。

---

## `POST /skill/v3/quote/index/kline` — 指数历史K线

查询指数历史 K 线（日K/周K/月K/分钟K）。

**请求体**：`symbol`（string，指数代码，单只）、`candlePeriod`（`DAY`/`WEEK`/`MONTH`/`MINUTE_1`/`MINUTE_5`/`MINUTE_15`）、`dateRange`（yyyyMMdd~yyyyMMdd）、`needFillKLine`（integer，0/1）。

**查询范围限制**：日K 最多 500 天，周K/月K 最多 10 年，分钟K 最多 7 天，超出返回错误提示（成立以来超出限制时改为近10年区间重查并如实说明截断）。

**最终数据路径**：`$.data.candle`（列名数组）+ `$.data.<代码>`（与列名逐列对齐的二维数组）。⚠️ 无 `lastUpdateTime` 字段（实际 data 只有 `candle` 与代码两个 key）。

> 列名固定为 `["date", "min_time", "open_px", "high_px", "low_px", "close_px", "deal_volume", "deal_amount"]`；`min_time` 分钟K 为 HHmm 整数、日/周/月K 为 0；按列名对齐解析，不预测后续走势。
>
> ⚠️ **回答呈现要求**：展示K线数据时应**完整呈现全部列**（日期/开/高/低/收/成交量/成交额），成交量（deal_volume）与成交额（deal_amount）**不可省略**；单位按数据口径说明（指数K线成交量/成交额为成分股口径，量额列若为原始值需注明单位）。
>
> ⚠️ **实测（2026-09）**：全周期（DAY/WEEK/MONTH/MINUTE_15）全历史数据均正常返回（此前曾一度仅返回近期数据，已恢复）；仍受文档范围限制（日K 最多 500 天、周/月K 最多 10 年、分钟K 最多 7 天），超出会返回错误提示，如实说明即可。

---

## `GET /skill/v3/discovery/hot-search-recommend` — 指数热搜推荐（v3 结构变化）

返回热搜 ETF、热搜场外基金、热搜指数三组推荐。⚠️ v3 起无 `type` 参数，一次返回全部三组，响应结构改为 `$.data.{etfList, otcList, indexList}`。

**无请求参数**

**最终数据路径**：`$.data.indexList[]`（本技能读取）→ `code`（指数代码）、`name`（指数名称）。`navPctChg1Y` 仅场外基金类型返回，指数类型为空属正常，不补造涨跌幅。

> ⚠️ 口径：本接口返回"热搜推荐"（推荐列表），**不是按搜索次数统计的关键词热榜**，无热度值/搜索次数字段，不得表述为"按搜索热度排序"；热门指数类问题优先用 `discovery/index-hot-rank`（含涨跌幅与点位）。

---

## `GET /skill/v3/discovery/index-hot-rank` — 指数热度榜（v3 新增）

查询指数热搜热度榜。适用于「大家都在关注哪些指数」类问题。

**请求参数**（URL query）：`timeType`（string，必填）：`last`（最新）/ `week`（周）/ `month`（月）

**最终数据路径**：`$.data.list[]`；`$.data.lastSyncTime`、`startDay`、`endDay` 为榜单同步时间与统计区间。

| 字段 | 说明 |
|---|---|
| `indexCode` / `indexName` | 指数代码、名称 |
| `hotValue` / `rank` | 热度值（⚠️ 实测当前返回全为 null，不要依赖）/ 排名 |
| `changeRate` / `lastPrice` / `lastPriceDate` | 最新涨跌幅（%）、点位、行情日期 |

---

## `GET /skill/v3/discovery/index-surge-rank` — 指数飙升榜（v3 新增）

查询指数热度飙升榜（热度排名上升最快）。

**请求参数**（URL query）：`timeType`（string，必填）：`week`（周）/ `month`（月）

**最终数据路径**：`$.data.list[]`；`$.data.lastSyncTime`、`startDay`、`endDay`。

| 字段 | 说明 |
|---|---|
| `indexCode` / `indexName` | 指数代码、名称 |
| `hotValue` / `rank` | 热度值（⚠️ 实测当前返回全为 null，不要依赖）/ 排名 |
| `changeRate` / `surgeRate` / `lastPrice` | 涨跌幅（%）/ 飙升幅度（⚠️ 实测为**字符串**，如 "33"，使用前转数字）/ 点位 |

---


## `POST /skill/v3/quote/stock/list` — 批量股票实时行情（补充能力）

按代码批量查询个股最新价、涨跌幅、行情时间。用于回答涉及**个股**行情的补充问题（如指数成分股当日表现）。

**请求参数**（body）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| builders | array | 是 | `[{"symbol":"300750","exchange":"2"}, ...]`；`symbol`=6位股票代码，`exchange`=`1`（上交所）/`2`（深交所）/`HK`（香港） |

**最终数据路径**：`$.data.dataInfo[]`；`$.data.serverTime` 为服务器时间。

| 字段 | 说明 |
|------|------|
| symbol / exchange | 股票代码 / 交易所 |
| lastPrice / changeRate | 最新价（元）/ 涨跌幅（%） |
| date / timeStamp | 行情日期（yyyyMMdd）/ 时间（HHmmss） |

> 本接口为**股票**行情，不是指数行情；仅当用户明确询问个股时才使用。

---
## 时间、单位与解释

- 行情数据时间：每条行情的 `date + timeStamp`；`serverTime` 只是服务器时间。实时口径回答以 `quote/index/list`、`quote/index/single` 的精确行情时间为准。
- 非交易时段表述为"接口返回的最新一笔行情"；盘前（9:10-9:30）涨跌幅显示 0.00%。
- 点位使用"点"；收益率、涨跌幅、权重、估值分位和基本面比例使用"%"。
- 估值倍数使用"倍"；金额按接口字段的元、万元口径换算（见各接口标注）。
- `quote/index/list` 与 `quote/index/single` 的 `latestQuote.changeValue`（涨跌额，点）可直接读取；其他接口无此字段时用 `lastPrice - yesterdayClosePrice` 计算并注明口径。
- `index/valuation` 估值字段为小写 p 系列（pETtm/pBLf/pSTtm/pCFTtm），其中 PCF 系列实际返回仍有（与 spec 声称"删除"矛盾，以实际为准）。
- `index/valuation` 若返回空数组（间歇性），用 `index/valuation/history`（不传日期）兜底取最新交易日估值，并注明 `trdDt`。
- 历史序列三接口（`index/valuation/history`、`index/financial-indicators/history`、`index/dividend-ratio/history`）：`indexCodes` 最多 20 个；不传日期=最新交易日/最新报告期，`endDate` 单传为 as-of（自动吸收周末节假日），`beginDate`+`endDate` 为区间且 `items` 倒序；前两者区间超 500 条交易日时 `truncated=true` 仅返回最近 500 条。
- 低历史分位只说明当前指标在自身历史中的位置，不等价于投资建议或未来回报判断。
- **凡给出估值倍数（PE/PB/PS/PCF），必须同屏给出对应历史分位**：默认近 5 年分位（`*5Y`），用户指定窗口则用其窗口（`*3Y`/`*Bgn` 等），并注明分位窗口与数据日期 `trdDt`；倍数与分位须分开表述（15 倍 ≠ 15% 分位），分位缺失时如实说明原因，不得只给倍数。
