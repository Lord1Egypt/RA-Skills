# 场外基金信息查询 — 接口字段权威参考（v3）

> 编写脚本前必读：数据路径、字段名、单位均以本文件为准。
>
> 说明：
> - 本文所有路径都是 JSON 路径。
> - `$` 表示返回 JSON 的根节点。
> - 所有接口响应外层信封统一为 `{success, code(string "0000"), message, data}`：`success` 为调用成功标识，`code="0000"` 表示成功，`message` 为结果描述。业务数据一律从 `data` 节点开始取值。
> - 默认按 catalog 中的路径取值；只有路径失败、字段缺失或结构可疑时，才先查看真实响应结构再继续。
> - 如果按 catalog 取值失败，不要跨接口猜路径。必须先请求该接口，检查根节点有哪些 key、`data` 是对象/数组/空值，以及列表真实位于哪一层。

---

## 公共请求头与约定（v3）

所有接口请求均需携带以下请求头：

```
# 认证格式：Authorization: Bearer <API_KEY>
# 请求来源标识：X-Caller-Type: external
```

- **GET 接口**参数走 URL query，数组参数用英文逗号拼接的字符串；**POST 接口**参数走 JSON body。
- 除 `search/offMarketIndex`、`search/oef-advanced` 外，POST 接口不再有公共 `requestId` 参数；GET 接口一律无 `requestId`。
- 所有 GET 接口的数组参数均以**英文逗号拼接的字符串**传递，不要传 JSON 数组。

---

## 回答口径说明模板（输出必守）

回答中涉及**数值/数据时，必须随数据给出完整口径**，否则判为口径说明缺失。逐项必守：

1. **凡涉及区间（收益、涨跌幅、跟踪误差、回撤、年化等），必须给出区间起止日期**，不得只说"近1年/近3个月"：
   - 正确示例：`近1年（2025-09-17~2026-09-17）收益 +12.3%`、`跟踪误差近1年（2025-09-17~2026-09-17）`。
   - 区间由查询日回推时，写明"自查询日（2026-09-17）往前推 N 个月/年"。
2. **凡实时/盘中行情，必须给出行情时间戳**；场外基金按净值成交无盘中价，须明确"以最新单位净值为准，净值日期 X"；分钟序列细节只能由相应接口（如 `quote/etf/realtime`）提供，无调用记录不得给出精确分钟数字。
3. **快照类数据（规模、持仓、费率、报告期指标）必须给出数据截止日/报告期**（如 `rptFundScale` 的 `rptDt`、`netValueDate`），不得只写"最新"。
4. **口径注与正文数据一一对应**：正文引用的每个数字在口径注中都能找到取数口径，正文未出现的数字不要出现在口径注中。
5. **多个相近数字并存时（如两个区间收益、两段任职区间），必须说明各自区间起点/边界差异**（如交接重叠关系）。
6. **单位换算必须标注**：元/万元/亿元，换算关系（如 `元 ÷ 1e8 = 亿`）在首次出现时说明。
7. **已废弃口径不得引用**（如 v4 删除的 `trackError1Y`），引用字段须与当前接口能力一致。
8. **口径矛盾必须解释**（如收益区间截至 09-17 但净值截至 09-04），不得同时出现冲突口径不解释。
9. **基金经理业绩口径**：回答"某经理管理哪些基金及业绩"时，每只基金必须给出该经理**管理以来（任职期间）业绩**，取 `oef/detail` 的 `fundManagerCurrent[].performance`（按 `psnName` 匹配），区间起点=该经理 `posiBgnDt`、终点=数据日期，随数据写明；主动基金（`oef/detail` 无数据）须如实说明"当前数据源暂缺主动基金的数据"，只列清单与任职起始日，不得编造业绩。

---

## `POST /skill/v3/search/offMarketIndex` — 关键词搜索场外基金（v3 改名自 search/oef）

根据关键词模糊搜索场外指数基金（支持产品名称、代码等），返回匹配的场外基金列表，含净值、各周期涨跌幅、估值、跟踪指数、基金经理、费率、相关ETF、最大回撤等信息。适用于用户未提供具体代码、只知道名称或代码片段时的检索。

**请求参数**（body）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 否 | 搜索关键词，支持场外基金产品名称、代码等模糊搜索 |
| page | integer | 否 | 页码，从1开始，默认1 ⚠️ 注意是 `page` 不是 `pageNum` |
| pageSize | integer | 否 | 每页条数，建议10-100，默认10 |
| requestId | string | 否 | 请求唯一标识 |

> 本接口仅支持关键词与分页，无筛选（filters）、无排序参数；筛选、排序和比较基于搜索结果在本地完成。

**最终数据路径**：`$.data.data[]`（⚠️ 不是 `$.data.list[]`）

| 字段 | 类型 | 说明 |
|------|------|------|
| fundCode | string | 场外基金代码，6位数字 |
| fundName | string | 产品名称（全称，可能含 HTML 高亮标签） |
| fundSht | string | 产品简称 |
| indexCode / indexName / indexType | string | 跟踪指数 |
| pubDt | string | 净值数据发布日期，yyyy-MM-dd |
| unitNav | number | 单位净值（元） |
| fundScale | number | 基金规模（**元**，÷1e8=亿） |
| navPctChg1D | number | 日涨跌幅（%） |
| eodPctChg1W/1M/3M/TY/1Y/3Y/5Y | number | 各周期涨跌幅（%） |
| annTrackError1Y | number | 近一年跟踪误差（%） |
| excessReturn1Y | number | 近1年超额收益（%） |
| maxDown1W/1M/3M/6M/1Y/3Y/5Y/10Y/TY/Bgn | number | 各周期最大回撤（%） |
| unitAccBonus / accBonusCount / currBonusDt | | 分红信息（单位累计分红 元 / 累计次数 / 最近权益登记日） |
| dividendYield | number | 指数股息率（%） |
| PETtm/PETtm5Y、PBLf/PBLf5Y、PSTtm/PSTtm5Y | number | 估值与近5年分位 ⚠️ 注意大小写 |
| fundManageComp | string | 基金管理人 |
| fundManagerCurrent | array | 基金经理信息（managerName/startDate） |
| establishDt | string | 成立日，yyyy-MM-dd |
| mgtFee / trstFee / salesServiceFee | number | 管理费、托管费、销售服务费（%） |
| relatedETF | array | 相关ETF产品信息（fundCode/relatedETFCode/relatedETFSht） |
| trackError1Y | number | 近一年跟踪误差（%）⚠️ 无 trackErrorBgn 字段 |
| lastYearYield / prevYearYield | number | 上年 / 前年收益率（%） |

**分页信息路径**：`$.data.totalNum`、`$.data.pageNum`、`$.data.pageSize`；另有 `$.data.serverTime`（服务器时间）。

> **分页规则**：`pageSize` 取大值一次取回候选，以 `totalNum` 为界，仅当前几页确实无匹配时才翻页，最多翻页 5 页，仍覆盖不全时在回答中说明筛选条件、覆盖范围与排序口径，不得继续扫库；搜索响应已随附净值、规模、各周期收益、跟踪误差等比较字段，不为每只候选重复请求详情；多产品详情用批量接口一次传入全部代码，禁止逐个单查。
>
> ⚠️ `fundName`/`fundNameSht` 可能含 `<span style='color: ...'>` 高亮标签，展示时去掉标签。

---

## `POST /skill/v3/search/oef-advanced` — 场外基金高级搜索（v3 新增）

按关键词 + 服务端筛选（`filters`）+ 排序（`sortField`/`sortOrder`）检索场外基金。适用于需要按规模、估值、费率等条件精确筛选并排序的场景。

**请求参数**（body）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 否 | 关键词 |
| pageNum / pageSize | number | 否 | 默认 1 / 10 |
| sortField | string | 否 | 排序字段：`rptFundScale`、`navPctChg1D/1W/1M/3M/6M/1Y/3Y/5Y/TY`、`trackError1Y`、`annTrackError1Y`、`excessReturn1Y`、`mgtFee`、`trstFee`、`saleServiceFee`、`unitAccBonus`、`accBonusCount`、`currBonusDt`、`dividendYield`、`PETtm/PBLf/PSTtm`、`PETtm5Y/PBLf5Y/PSTtm5Y`、`ROE`、`establishDt`、`lastYearYield/prevYearYield` 等 |
| sortOrder | string | 否 | `asc` / `desc` |
| fundCodes | array | 否 | 指定代码集合内筛选 |
| source | string | 否 | 数据来源 |
| filters | object | 否 | 复杂筛选条件：`productType[]`、`indexCode[]`、估值（PETtm/PETtm5Y/PBLf/PBLf5Y/PSTtm/PSTtm5Y）、基本面（dividendYield/ROE）、费率（mgtFee/trstFee/saleServiceFee）、规模（rptFundScale，**元**）、年度表现（lastYearYield/prevYearYield）、跟踪误差（trackError1Y）等（数值均为 `{"min":n,"max":n}`） |
| requestId | string | 否 | 请求唯一标识 |

**最终数据路径**：`$.data.data[]`；分页在 `$.data.pageNum`、`pageSize`、`totalNum`、`serverTime`。

---

## `POST /skill/v3/search/fund-manager` — 基金经理搜索（v3 新增）

按关键词搜索基金经理。

**请求参数**（body）：`keyword`（string，姓名关键词）、`pageNum`/`pageSize`（number）、`manageStatus`（string，任职业态）。

**最终数据路径**：`$.data.list[]`；分页在 `$.data.currentPage`、`totalPage`、`totalCount`。

---

## `POST /skill/v3/search/fund-manager-detail` — 基金经理详情搜索（v3 新增）

按关键词搜索基金经理并返回其管理产品等信息。

**请求参数**（body）：`keyword`（string，必填）、`pageNum`/`pageSize`（number）、`manageStatus`（string）。

**最终数据路径**：`$.data.list[]`；分页在 `$.data.currentPage`、`totalPage`、`totalCount`。

**返回内容**：命中基金经理的画像（`psnName`、`profYear` 从业年限、`manageYear` 任职年限、`annualReturn` 经理任职以来年化回报、`manageDesc` 任职经历说明）+ `managedProducts[]` 在管产品清单（`fundCode`/`fundName`/`fundStatusName` 状态/`manageStartDate` 任职起始日）。

**⚠️ 在管产品业绩的取数规则（回答"XX 管理哪些基金及业绩"时必守）**：

1. `managedProducts` **本身不含单只产品业绩**，只给代码/名称/状态/任职起始日；不要从该清单编造业绩。
2. 每只基金须**附带该基金经理"管理以来（任职期间）"的业绩**：
   - 用 `oef/detail`（`fundCodes` 批量传入，逗号分隔的 6 位场外代码）取详情；
   - 在返回的 `fundManagerCurrent[]` 中**按 `psnName` 匹配该基金经理**，取该条的 **`performance`（该经理任职期间业绩，数值为小数，×100 得百分比）** 与 **`posiBgnDt`（任职起始日）**；
   - 口径表述示例：`易方达沪深300ETF联接A（110020）：余海燕自 2016-04-16 任职以来业绩 +76.2%`；区间起点=该经理 `posiBgnDt`，区间终点=查询日/数据日期，须随数据写清。
   - 同接口还可顺带给出该基金各周期涨跌幅（`navPctChg1Y/3Y/5Y/TY`）、超额（`excessReturn1Y`）、跟踪误差（`annTrackError1Y`）等，但**"管理以来业绩"以 `fundManagerCurrent[].performance` 为准**。
3. **主动基金（非指数基金）数据暂缺**：`oef/detail` 对该类代码返回空/全 null（如张坤管理的易方达蓝筹精选 005827、易方达优质精选 110011 等主动混合基金）。此时**如实说明"该基金为主动管理基金，当前数据源暂缺主动基金的数据"**，只列出 `managedProducts` 中的代码、名称、状态与任职起始日，**不得编造业绩**；经理画像中的 `annualReturn`（任职以来年化）仍可给出，但需注明是经理维度口径。
4. **场内代码区分**：`managedProducts` 中可能混有场内代码（LOF/ETF，如 502048/512560/513040 等 5 开头或场内 6 位），`oef/detail` 只覆盖场外份额；对场内代码同样按第 3 条处理（说明不在场外数据源），不要强查。
5. 命中多人的场景（如"张坤"与"陆海燕"等重名/近名）：以 `psnName` 与用户所指完全一致为准，必要时列出各候选并说明管理产品不同，不要混用。

---

## `POST /skill/v3/search/fund-product` — 全市场基金产品搜索（v3 新增）

按关键词搜索基金产品（全市场口径）。

**请求参数**（body）：`keyword`（string）、`pageNum`/`pageSize`（number）。

**最终数据路径**：`$.data.list[]`；分页在 `$.data.currentPage`、`totalPage`、`totalCount`。

---

## `GET /skill/v3/discovery/fund-manager-list` — 基金管理人列表（v3 新增）

按关键词查询基金管理人列表（供筛选）。

**请求参数**（URL query）：`keyword`（string，可选）。

**最终数据路径**：`$.data[]` → `label`（管理人名称）、`key`（管理人代码）、`pyIndex`（拼音索引）。

---

## `GET /skill/v3/oef/detail` — 批量场外基金详情（v3 方法改 GET）

批量查询多只场外指数基金的详细信息：代码/名称/全称、成立日、费率、管理人/托管人、业绩比较基准、跟踪指数与分类、净值（元）、各周期涨跌幅（%）、近1年超额收益与跟踪误差（%）、报告日期与产品规模（元）、现任及历任基金经理、相关ETF/相关份额、全周期最大回撤（%）、风险等级等。

> **调用前检查**：`search/offMarketIndex`、`search/oef-advanced` 的响应**已随附**规模（`fundScale`）、费率（`mgtFee`/`trstFee`/`salesServiceFee`）、各周期涨跌幅、近1年超额收益与跟踪误差等比较字段，**禁止为这些字段重复调用本接口**；仅当需要搜索未覆盖的字段（业绩比较基准、管理人/托管人、相关份额、风险等级、历任基金经理等）时才调用，且一次批量传入全部代码，不要逐只查询。

**请求参数**（URL query）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| fundCodes | string | 是 | 场外基金代码，英文逗号分隔，最多 10 个 |

**最终数据路径**：`$.data.data[]`（⚠️ v3 多包一层 `data`；`$.data.serverTime` 为服务器时间）

> ⚠️ v3 起响应**去掉** `fundCode`/`availabilityStatus`/`detail` 包装，字段直接平铺在每项上；不再有 `availabilityStatus` 标记，代码类型不匹配或未找到时该项直接缺失或为空。

`$.data.data[]` 每项字段（平铺）：

| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | 交易代码 |
| fundName | string | 基金名称（对外展示优先使用） |
| chiName | string | 基金全称（法律全称） |
| establishDt | string | 成立日，yyyy-MM-dd |
| mgtFee / trstFee / saleServiceFee | number | 管理费、托管费、销售服务费（%） |
| fundManageComp / fundManageSht | string | 基金管理人全称/简称 |
| fundCustComp / fundCustCompSht | string | 基金托管人全称/简称 |
| benchMark | string | 业绩比较基准 |
| indexCode / indexName / indexSht / indexType | string | 标的指数 |
| firstClass / secondClass / thirdClassMarketType / thirdClassMarketValue / className | string | 指数分类 |
| pubDt | string | 净值数据发布日期 |
| unitNav / accuUnitNav / navPctChg1D | number | 单位净值、累计净值（元）、日涨跌幅（%） |
| navPctChg1W/1M/3M/6M/1Y/3Y/5Y/TY/Bgn | number | 各周期净值涨跌幅（%） |
| excessReturn1Y / trackError1Y / annTrackError1Y | number | 超额收益 / 跟踪误差 / 年化跟踪误差（%） |
| rptDt / rptFundScale | string/number | 报告期、报告期规模（**元**，÷1e8=亿） |
| unitAccBonus / accBonusCount / currBonusDt | | 分红信息（单位累计分红 元 / 次数 / 最近权益登记日） |
| fundManagerCurrent | array | 现任基金经理（trdCode、psnCode、psnName、posiBgnDt、posiEndDt、gender、managementTime、manageStatus 1在职/0离任、performance 任期业绩%、sequence） |
| fundManagerFormer | array | 历任基金经理 |
| relatedETF / relatedShareFunds | array | 相关ETF / 相关份额（⚠️ 子字段为 `trdCode` 非 fundCode：relatedETF 为 trdCode/fundSht/fundType/fundScale/navPctChg1Y/navPctChg1D；relatedShareFunds 为 trdCode/relatedTrdCode/relatedFundSht） |
| riskLevel | string | 风险等级（如 "3"，⚠️ 实际仍返回，非空字符串，读作 string） |
| maxDown1W~Bgn | number | 各周期最大回撤（%） |
| lastYearYield / prevYearYield | number | 上年/前年收益率（%） |
| authorizedIndex | boolean | 跟踪指数是否有权限 |
| sinfoWindcode / indexSInfoWindcode | string | 基金/指数万德代码 |
| fundNavJson / benchmarkReturnJson | string | 数据文件路径，不当作内嵌 JSON 解析 |

---

## `POST /skill/v3/oef/holdings` — 批量场外基金持仓（v3 平铺列表）

批量查询场外指数基金的最新（或指定日期）重仓股。

**请求参数**（body）：`fundCodes`（array，基金代码列表，最多 10 个）、`date`（string，可选，yyyy-MM-dd）。

**最终数据路径**：`$.data.data[]`（⚠️ 实际响应为 `{serverTime, data:[...]}`，列表在 `data.data` 下；v3 起为**平铺列表**，不再按基金分组，也无 fundCode/availabilityStatus/holdingItems 包装）

| 字段 | 说明 |
|---|---|
| `trdCode` | 基金代码 |
| `endDt` | 报告期截止日期 |
| `stockCode` / `secuSht` | 股票代码、简称 |
| `holdNavRat` | 占净值比例（%） |
| `stockWindcode` / `sinfoWindcode` | 万德代码 |

> ⚠️ v3 平铺后需按 `trdCode` 分组再回答"每只基金的重仓股"。

---

## `GET /skill/v3/oef/return` — 批量场外基金区间收益（v3 方法改 GET）

批量查询多只场外基金在预设周期或自定义区间内的收益率（%）。

**请求参数**（URL query）：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `codes` | string | 是 | 场外基金代码，逗号分隔，最多 10 只 |
| `timeMode` | string | 是 | `PERIOD` / `RANGE` |
| `period` | string | PERIOD时必填 | `1M/3M/6M/1Y/3Y/5Y/TY/INCE` ⚠️ v3 无 1D/1W |
| `startDate` / `endDate` | string | RANGE时必填 | yyyy-MM-dd |
| `boundaryMatchMode` | string | 否 | `FLEXIBLE`（默认）/ `STRICT` |

**最终数据路径**：`$.data.data[]`（⚠️ v3 多包一层 data）

| 字段 | 说明 |
|---|---|
| `trdCode` | 场外基金代码 |
| `indexCode` | 与 trdCode 相同的代码本身；RANGE 模式下可能为 null |
| `startDate` / `endDate` | 实际区间起止日期 |
| `returnRate` | 区间收益率（%，null 判空处理） |
| `availabilityStatus` | 有数据 / API接口无数据 / 历史查询无数据 / 不支持的期间 / API调用异常 / 系统异常 |

> ⚠️ `availabilityStatus`≠有数据 时 `returnRate` 为 null，用 `.get('returnRate')` 取值，不把无数据当 0；展示以返回的 startDate/endDate 为准。
> ⚠️ 查"今年以来"用 RANGE 模式（startDate=当年1月1日），本接口无 YTD 周期。

---

## `GET /skill/v3/oef/interval-return` — 单只场外基金区间收益（v3 新增）

查询**单只**场外基金的区间收益率（%）。与 `oef/return` 区别：一次只查一只，返回单对象。

**请求参数**（URL query）：`code`（string，单只基金代码）、`timeMode`（`PERIOD`/`RANGE`）、`period`、`startDate`/`endDate`、`boundaryMatchMode`（同上）。

**最终数据路径**：`$.data`（单对象）

| 字段 | 说明 |
|---|---|
| `trdCode` / `indexCode` | 基金代码 / 与 trdCode 相同 |
| `startDate` / `endDate` | 实际区间起止日期 |
| `returnRate` | 区间收益率（%，null 判空处理） |
| `availabilityStatus` | 数据可用性状态 |
| `serverTime` | 服务器时间 |

---

## `POST /skill/v3/oef/dividends` — 批量场外基金分红明细（v3 平铺列表）

批量查询多只场外基金的历史分红明细。

**请求参数**（body）：`fundCodes`（array，最多 10 只）、`startDate`（string，可选）、`endDate`（string，可选）。

**最终数据路径**：`$.data.data[]`（⚠️ 实际响应为 `{serverTime, data:[...]}`，列表在 `data.data` 下；v3 起为**平铺列表**，不再按基金分组，也无 fundCode/availabilityStatus/dividendItems 包装）

| 字段 | 说明 |
|---|---|
| `trdCode` | 基金代码 |
| `eqyRecordDt` | 权益登记日 |
| `dvdBenDt` | 分红计算基准日 |
| `cashDvdPerShTax` | 每份分红金额（元） |
| `payDt` | 红利发放日（场内，通常 null） |
| `divPayDt` | 红利发放日（场外） |

> ⚠️ v3 平铺后需按 `trdCode` 分组再回答"每只基金的分红历史"；无分红时该项缺失需判空。

---

## `POST /skill/v3/oef/financial-report` — 批量场外基金财报（季报/年报）

批量查询场外基金的财务报告数据（利润、净值、现金流等）。适用于「最近一期季报的利润和净值」类问题。

**请求参数**（body）：`trdCodes`（array，基金代码列表，最多 10 个）、`beginDate`（string，可选，yyyy-MM-dd）、`endDate`（string，可选，yyyy-MM-dd）。**不传日期默认返回最新一期**。

**最终数据路径**：`$.data[]`（按基金分组）

| 字段 | 说明 |
|---|---|
| `trdCode` / `fundName` | 基金代码、名称 |
| `availabilityStatus` | 有数据 / 未找到该基金 / 查询失败 |
| `financialReports[]` | 财务报告列表 |

`financialReports[]` 内字段：`endDt`（报告期）、`pubDt`（披露日）、`totalProfit`（本期利润，元）、`netIncome`（净利润，元）、`fairValueChangeIncome`（公允价值变动损益）、`totalProfitPerShare`（每股收益）、`netIncomePerShare`、`netAsset`（期末基金资产净值，元）、`nvPerShare`（每份净值）、`netOperateCashflow`、`totalRevenue`。

---

## `GET /skill/v3/quote/etf/list` — 关联ETF批量精简行情（v3 改名自 quote/etf）

批量获取多个 ETF 的最新价、涨跌幅、成交额与规模。⚠️ **v3 批量接口不再返回完整盘口**（IOPV、溢折率、成交量、换手率、昨收、精确行情时间 timeStamp 均无），核心字段为 `lastPrice`/`changeRate`/`dealBalance`/`fundScale`，并随附 `date`（行情日期）及 `navPctChg*`/`eodPctChg*` 各周期涨跌幅。

> **用途**：本技能用它查询用户关注的**关联ETF**（经 `oef/detail` 或搜索取 `relatedETF` 代码）的场内表现。场外基金本身按净值成交，无盘中价格/成交额/换手率/IOPV/溢折率，**禁止**直接对场外代码调用本接口。

**请求参数**（URL query）：`symbol`（string，ETF代码，英文逗号分隔，单次最多 50 个）

**最终数据路径**：`$.data.dataInfo[]`（`$.data.serverTime` 为服务器时间）

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | string | ETF代码 |
| lastPrice | number | 最新价（元） |
| changeRate | number | 涨跌幅（%） |
| dealBalance | number | 成交额（元） |
| fundScale | number | 基金规模（**元**，÷1e8=亿） |
| date | integer | 行情日期，yyyyMMdd |
| navPctChg1M/1W/3M/6M/1Y/3Y/5Y/Bgn | number | 各周期净值收益率（%） |
| eodPctChg1W / eodPctChgTW | number | 近1周 / 本周以来收盘涨跌幅（%） |

> ⚠️ 本接口**无** IOPV/溢折率/换手率/昨收/成交量/精确行情时间（有 `date` 无 `timeStamp`）。需要**完整盘口**（IOPV、溢折率、换手率、昨收、精确行情时间）时改用 `quote/etf/single`（单只）。

---

## `GET /skill/v3/quote/etf/single` — 关联ETF单只完整盘口+分钟（v3 新增）

查询**单只** ETF 的完整实时盘口（含 IOPV、溢折率、成交量、换手率、昨收、精确行情时间 `date + timeStamp`）及当日分钟序列。承接原 `quote/etf` 的完整盘口能力，但**仅单只**。

**请求参数**（URL query）：`symbol`（string，单只ETF代码）、`lastTimestamp`（number，可选，>0 仅返回新增分钟）。

**最终数据路径**：`$.data.latestQuote{}` + `$.data.list[]`；`$.data.serverTime` 为服务器时间。

`latestQuote{}` 字段：`symbol`、`lastPrice`（元）、`changeRate`（%）、`changeValue`（涨跌额，元）、`yesterdayClosePrice`（元）、`dealBalance`/`dealVolume`（成交额/成交量）、`turnoverRatio`（换手率 %）、`iopv`（IOPV 元）、`deviationRate`（溢折率 %）、`date`（yyyyMMdd 整数）+ `timeStamp`（HHmmss 整数）精确行情时间。

`list[]` 字段：`minute`（分钟时间戳，如 930）、`lastPrice`、`iopv`、`changeRate`。

> `date + timeStamp` 是行情数据时间，`serverTime` 是服务器时间；回答"现在/实时/盘中"口径问题必须注明精确行情时间。

---

## `POST /skill/v3/quote/etf/realtime` — 关联ETF分时分钟行情（v3.1 改名自 quote/etf/minite）

批量获取多个 ETF 当日分时分钟行情。⚠️ **v3 语义收窄为仅 ETF**，且不再返回 `latestQuote` 最新快照。

**请求参数**（body）：`fundCodeList`（array，ETF代码列表，最多 50 个）、`date`（string，可选，yyyyMMdd，默认当天）、`lastTimestamp`（number，0 全量 / >0 增量）。

**最终数据路径**：`$.data.dataList[]`（`$.data.serverTime` 为服务器时间）

| 字段 | 说明 |
|---|---|
| `trdCode` | ETF代码 ⚠️ v3 用 `trdCode`（v2 为 symbol） |
| `quoteList[]` | 分钟序列：`minute`（930=9:30）、`lastPrice`（元）、`iopv`（元）、`changeRate`（%） |

> 需要最新快照（含精确行情时间）时改用 `quote/etf/single`。

---

## `GET /skill/v3/discovery/hot-search-recommend` — 场外基金热搜推荐（v3 结构变化）

返回热搜 ETF、热搜场外基金、热搜指数三组推荐。⚠️ v3 起无 `type` 参数，一次返回全部三组，响应结构改为 `$.data.{etfList, otcList, indexList}`。

**无请求参数**

**最终数据路径**：`$.data.otcList[]`（本技能读取）→ `code`（基金代码）、`name`（基金名称）、`navPctChg1Y`（近一年涨跌幅 %，仅场外基金类型返回）。

> 热搜与历史涨跌幅不代表未来收益。

---


## `POST /skill/v3/quote/stock/list` — 批量股票实时行情（补充能力）

按代码批量查询个股最新价、涨跌幅、行情时间。用于回答涉及**个股**行情的补充问题（如场外基金重仓股当日表现）。

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

> 本接口为**股票**行情，不是基金/ETF 行情；仅当用户明确询问个股时才使用。

---
## 数据路径速查

| 接口 | 结果路径 | 常见错误 |
|------|---------|---------|
| search/offMarketIndex | `$.data.data[]` | ⚠️ 不是 `$.data.list[]`；无 filters/sortField |
| search/oef-advanced | `$.data.data[]` | 分页在 `$.data.pageNum/totalNum` |
| search/fund-manager(-detail) / fund-product | `$.data.list[]` | 分页在 `$.data.currentPage/totalPage/totalCount` |
| discovery/fund-manager-list | `$.data[]` | label/key/pyIndex |
| oef/detail | `$.data.data[]`（平铺） | ⚠️ v3 多包一层 data；无 availabilityStatus/detail 包装 |
| oef/holdings | `$.data.data[]`（平铺） | ⚠️ 实际多包一层 data+serverTime；已不再按基金分组，需按 trdCode 自行分组 |
| oef/return | `$.data.data[]` | ⚠️ v3 多包一层 data；status≠有数据时 returnRate 为 null |
| oef/interval-return | `$.data`（单对象） | 单只接口 |
| oef/dividends | `$.data.data[]`（平铺） | ⚠️ 实际多包一层 data+serverTime；已不再按基金分组 |
| oef/financial-report | `$.data[].financialReports[]` | 不传日期只返回最新一期 |
| quote/etf/list | `$.data.dataInfo[]` | ⚠️ 核心 4 字段 + date + navPctChg*/eodPctChg* 各周期涨跌幅；无 IOPV/溢折率/成交量/精确时间 |
| quote/etf/single | `$.data.latestQuote{}` + `$.data.list[]` | 单只完整盘口 + 分钟 |
| quote/etf/realtime | `$.data.dataList[].quoteList[]` | v3 字段是 `trdCode`；无 latestQuote |
| discovery/hot-search-recommend | `$.data.otcList[]` | ⚠️ v3 无 type 参数，返回 etfList/otcList/indexList 三组 |

## OEF vs ETF 关键差异

| 维度 | ETF | OEF |
|------|-----|-----|
| 搜索 | `search/all`（searchType=etf） | `search/offMarketIndex`（仅关键词+分页）/ `search/oef-advanced` |
| 详情规模字段 | fundScale（**万元**，v3） | rptFundScale（**元**） |
| 销售服务费 | 无 | saleServiceFee（detail）/ salesServiceFee（搜索） |
| 溢折率/实时行情 | 有（quote/etf/list、quote/etf/single） | 无（场外无盘中价、成交量、换手率、IOPV、溢折率） |
| 场内分红发放日 | payDt | payDt（通常null） |
| 场外分红发放日 | divPayDt | divPayDt |
| 上市日 | lstDt | 无 |

## 单位速查

| 字段 | 接口 | 单位 | 换算 |
|------|------|------|------|
| fundScale | search/offMarketIndex、oef-advanced | 元 | ÷1e8=亿 |
| rptFundScale | oef/detail | 元 | ÷1e8=亿 |
| cashDvdPerShTax | oef/dividends | 元/份 | 直接展示 |
| totalProfit / netAsset 等 | oef/financial-report | 元 | ÷1e8=亿 |
| holdNavRat | oef/holdings | % | 直接展示 |
| 各涨跌幅 / returnRate / 跟踪误差 | 全部接口 | % | 直接展示 |
