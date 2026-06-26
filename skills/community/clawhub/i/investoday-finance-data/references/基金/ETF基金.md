# 基金 / ETF基金

---

## ETF申购赎回清单基本信息

接口路径：`fund/etf-sub-redemption-list`
请求方式：**`POST`**
tool_id：`list_etf_sub_red_lists`

接口说明：根据基金代码和日期范围（格式为yyyy-MM-dd HH:mm:ss）查询ETF基金的申购赎回清单基本信息，包括基金代码、名称、标的指数、发布及上一交易日日期、现金差额、最小申赎单位资产净值、基金份额净值、预估现金部分、现金替代比例上限、最小申赎单位、单位分红金额、IOPV收盘价以及申购赎回相关的各类状态和限额信息，适用于投资者进行ETF申赎操作前的详细规则查询和投资决策分析。

### 输入参数

**Query 参数**

_无参数_

**Body JSON 参数**

| 参数名 | 必填 | 类型 | 说明 | 示例 |
|--------|:----:|------|------|------|
| `fundCode` | — | string | 基金代码【与fundCodes组成多选一参数，必须且只能传递其中一个】 | `000001` |
| `fundCodes` | — | array | 基金代码列表【与fundCode组成多选一参数，必须且只能传递其中一个】 | `['000001', '000006']` |
| `beginDate` | — | string | 开始日期（格式yyyy-MM-dd） | `2025-01-01` |
| `endDate` | — | string | 结束日期（格式yyyy-MM-dd） | `2025-01-01` |
| `pageNum` | — | integer | 页码。 最小值:1; | `1` |
| `pageSize` | — | integer | 页长。 最小值:1; 最大值:500; | `10` |

### 输出参数

| 字段名 | 说明 | 示例 |
|--------|------|------|
| `publishDate` | 发布日期 | `2008-04-21 00:00:00` |
| `fundId` | 今日投资内部编码 | `KF0183SK` |
| `fundCode` | 基金代码 | `510181` |
| `fundName` | 基金名称 | `平安` |
| `underlyingIndexCode` | 标的指数代码 | `000010` |
| `prevTradeDate` | 上一交易日期 | `2008-04-18 00:00:00` |
| `cashBalance` | 现金差额(元) | `1327.5700` |
| `navPerCreationUnit` | 最小申赎单位资产净值(元) | `2175819.57` |
| `nav` | 基金份额净值(元) | `7.253` |
| `estimatedCashComponent` | 预估现金部分(元) | `-320.43` |
| `cashSubstitutionRatioLimit` | 现金替代比例上限 | `0.2` |
| `creationUnit` | 最小申赎单位(份) | `300000` |
| `dividendPerCreationUnit` | 最小申赎单位分红金额(元) | `0.85` |
| `iopvPublishDesc` | 是否需要公布IOPV描述 | `1` |
| `subscribeAllowedDesc` | 是否允许申购描述 | `1` |
| `redeemAllowedDesc` | 是否允许赎回描述 | `1` |
| `isIopvPublished` | 是否需要公布IOPV | `1` |
| `isSubscribeAllowed` | 是否允许申购 | `1` |
| `isRedeemAllowed` | 是否允许赎回 | `1` |
| `subscribeShareLimit` | 申购份额上限(份) | `1000000` |
| `redeemShareLimit` | 赎回份额上限(份) | `1000000` |
| `dailySubscribeLimitPerAccount` | 单个账户当日累计申购上限(份) | `1000000` |
| `dailyRedeemLimitPerAccount` | 单个账户当日累计赎回上限(份) | `1000000` |
| `netSubscribeShareLimit` | 净申购份额上限(份) | `1000000` |
| `netRedeemShareLimit` | 净赎回份额上限(份) | `1000000` |
| `dailyNetSubscribeLimitPerAccount` | 单个账户当日净申购上限(份) | `1000000` |
| `dailyNetRedeemLimitPerAccount` | 单个账户当日净赎回上限(份) | `1000000` |
| `iopvClosePrice` | IOPV收盘价 | `1.2345` |

### 接口示例

```bash
# Body JSON 可选参数: fundCode, fundCodes, beginDate, endDate, pageNum, pageSize
investoday-api fund/etf-sub-redemption-list --method POST --body-json '{"fundCode":"000001","fundCodes":["000001","000006"],"beginDate":"2025-01-01"}'
```

---

## ETF申购赎回成份股信息

接口路径：`fund/etf-constituent-stocks`
请求方式：**`POST`**
tool_id：`list_etf_constituent_stks`

接口说明：通过ETF基金代码和日期范围（格式为yyyy-MM-dd HH:mm:ss），查询ETF申购赎回清单中的成分股信息，包括成分股代码、名称、数量、现金替代标志及比例、申购赎回的现金替代溢价/折扣比例、固定及申购赎回替代金额、以及成分股市值占比等详细数据，适用于分析ETF持仓结构、现金替代机制和投资组合管理。

### 输入参数

**Query 参数**

_无参数_

**Body JSON 参数**

| 参数名 | 必填 | 类型 | 说明 | 示例 |
|--------|:----:|------|------|------|
| `fundCode` | — | string | 基金代码【与fundCodes组成多选一参数，必须且只能传递其中一个】 | `000001` |
| `fundCodes` | — | array | 基金代码列表【与fundCode组成多选一参数，必须且只能传递其中一个】 | `['000001', '000006']` |
| `beginDate` | — | string | 开始日期（格式yyyy-MM-dd） | `2025-01-01` |
| `endDate` | — | string | 结束日期（格式yyyy-MM-dd） | `2025-01-01` |
| `pageNum` | — | integer | 页码。 最小值:1; | `1` |
| `pageSize` | — | integer | 页长。 最小值:1; 最大值:500; | `10` |

### 输出参数

| 字段名 | 说明 | 示例 |
|--------|------|------|
| `publishDate` | 发布日期 | `2026-01-08 00:00:00` |
| `fundId` | 今日投资内部编码 | `159720JK` |
| `fundCode` | 基金代码 | `159720` |
| `fundName` | 基金名称 | `泰康中证智能电动汽车ETF` |
| `stockCode` | 股票代码 | `000009` |
| `stockName` | 股票名称 | `中国宝安` |
| `stockQuantity` | 股票数量(股) | `500` |
| `cashSubstituteFlagDesc` | 现金替代标志描述 | `允许` |
| `cashSubstituteFlag` | 现金替代标志 | `1` |
| `cashSubstituteRatio` | 现金替代比例 | `0.15` |
| `subscribeCashSubstitutePremiumRatio` | 申购现金替代溢价比例 | — |
| `redeemCashSubstituteDiscountRatio` | 赎回现金替代折价比例 | — |
| `fixedSubstituteAmount` | 固定替代金额(元) | `1250.75` |
| `subscribeSubstituteAmount` | 申购替代金额(元) | `0` |
| `redeemSubstituteAmount` | 赎回替代金额(元) | `0` |
| `constituentMarketCapWeight` | 成份股市值占比 | `0.0061` |

### 接口示例

```bash
# Body JSON 可选参数: fundCode, fundCodes, beginDate, endDate, pageNum, pageSize
investoday-api fund/etf-constituent-stocks --method POST --body-json '{"fundCode":"000001","fundCodes":["000001","000006"],"beginDate":"2025-01-01"}'
```

---
