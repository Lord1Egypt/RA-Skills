# 沪深京数据 / 特色数据 / 个股诊断 / dcf估值模型

---

## DCF估值模型结果

接口路径：`stock/dcf-result`
请求方式：**`POST`**
tool_id：`list_stock_dcf_result`

接口说明：支持通过单只股票代码、多只股票代码列表，结合基准报告截止日期范围（格式yyyy-MM-dd）及分页参数，查询股票的DCF估值模型结果，包含发布日期、股票代码与名称、基准报告截止日期、场景类型、预测年数、预测期FCF现值合计、永续增长率、终值、终值现值、企业价值EV、加权平均资本成本WACC等核心数据，可用于股票估值分析、企业价值研究等投研场景。

### 输入参数

**Query 参数**

_无参数_

**Body JSON 参数**

| 参数名 | 必填 | 类型 | 说明 | 示例 |
|--------|:----:|------|------|------|
| `stockCode` | — | string | 股票代码【与stockCodes组成多选一参数，必须且只能传递其中一个】 | `002594` |
| `stockCodes` | — | array | 股票代码列表【与stockCode组成多选一参数，必须且只能传递其中一个】 | `['000001', '600519']` |
| `beginDate` | — | string | 开始日期（格式yyyy-MM-dd）。 最小值:2020-01-01; | `2020-01-01` |
| `endDate` | — | string | 结束日期（格式yyyy-MM-dd） | — |
| `pageNum` | — | integer | 页码。 最小值:1; | `1` |
| `pageSize` | — | integer | 页长。 最小值:1; 最大值:500; | `10` |

### 输出参数

| 字段名 | 说明 | 示例 |
|--------|------|------|
| `publishDate` | 发布日期 | — |
| `stockCode` | 股票代码 | — |
| `stockName` | 股票名称 | — |
| `reportPeriodEnd` | 基准报告截止日期 | `2024-12-31 00:00:00` |
| `scenarioType` | 情景类型 | `1` |
| `forecastYears` | 预测年份数 | `5` |
| `sumFcfPv` | 预测期FCF现值合计 | `123456.789` |
| `terminalGrowthRate` | 永续增长率 | `0.03` |
| `terminalValue` | 终值 | `123456.789` |
| `terminalValuePv` | 终值现值 | `123456.789` |
| `enterpriseValueEv` | 企业价值EV | `123456.789` |
| `wacc` | 加权平均资本成本 | `0.085` |

### 接口示例

```bash
# Body JSON 可选参数: stockCode, stockCodes, beginDate, endDate, pageNum, pageSize
investoday-api stock/dcf-result --method POST --body-json '{"stockCode":"002594","stockCodes":["000001","600519"],"beginDate":"2020-01-01"}'
```

---
