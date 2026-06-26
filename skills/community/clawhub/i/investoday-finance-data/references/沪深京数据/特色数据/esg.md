# 沪深京数据 / 特色数据 / esg

---

## 股票ESG综合评级

接口路径：`stock/esg_rating`
请求方式：**`POST`**
tool_id：`list_stock_esg_rating`

接口说明：支持通过单个股票代码、批量股票代码列表、指定数据来源机构（如中证、MSCI）、发布日期范围（格式yyyy-MM-dd），并可配合分页参数，查询沪深京市场股票的ESG综合评级数据，包括评级发布日期、数据来源、股票代码及名称、市场代码，以及ESG总分与等级、环境维度得分与等级、社会维度得分与等级、公司治理维度得分与等级，可用于ESG投资分析、企业社会责任评估等场景

### 输入参数

**Query 参数**

_无参数_

**Body JSON 参数**

| 参数名 | 必填 | 类型 | 说明 | 示例 |
|--------|:----:|------|------|------|
| `stockCode` | — | string | 股票代码【与stockCodes组成多选一参数，必须且只能传递其中一个】 | `002594` |
| `stockCodes` | — | array | 股票代码列表【与stockCode组成多选一参数，必须且只能传递其中一个】 | `['000001', '600519']` |
| `dataSource` | ✅ | integer | 数据来源机构 | `1` |
| `beginDate` | — | string | 开始日期（格式yyyy-MM-dd）。 最小值:2020-01-01; | `2020-01-01` |
| `endDate` | — | string | 结束日期（格式yyyy-MM-dd） | `2020-01-01` |
| `pageNum` | — | integer | 页码。 最小值:1; | `1` |
| `pageSize` | — | integer | 页长。 最小值:1; 最大值:500; | `10` |

### 输出参数

| 字段名 | 说明 | 示例 |
|--------|------|------|
| `publishDate` | 评级发布日期 | — |
| `dataSource` | 数据来源机构 | — |
| `stockCode` | 股票代码 | — |
| `stockName` | 股票名称 | — |
| `marketCode` | 市场代码 | — |
| `esgScore` | ESG评分 | — |
| `esgLevel` | ESG等级 | — |
| `environmentScore` | 环境得分 | — |
| `environmentLevel` | 环境等级 | — |
| `socialScore` | 社会得分 | — |
| `socialLevel` | 社会等级 | — |
| `governanceScore` | 公司治理得分 | — |
| `governanceLevel` | 公司治理等级 | — |

### 接口示例

```bash
# Body JSON 可选参数: stockCode, stockCodes, beginDate, endDate, pageNum, pageSize
investoday-api stock/esg_rating --method POST --body-json '{"dataSource":1}'
```

---
