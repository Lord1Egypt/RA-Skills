# API 参考

本文档与 `panda_tools` 中各 tool 的 JSON Schema 定义一致，供调用 `ToolRegistry.call_tool(name, **kwargs)` 或 LLM function calling 时查阅。

## 通用约定

| 约定 | 说明 |
|------|------|
| **日期** | 均为字符串 `YYYYMMDD`，如 `20250101` |
| **symbol / 代码类** | 多数支持 `string` 或 `string[]`；未传或空串在部分接口表示「全市场」。经 `ToolRegistry.call_tool` 时会对常见误写做规范化：A 股 `xxxxxx.SH`/`SZ` 按 `get_exchange_suffix` 规则推断；期货先将 `CFFEX`/`SHFE` 等长名映射为 CTP 三位码，再按 `panda_tools/future_ctp_reference.py` 中的**品种—CTP 后缀**对照表（中金所 CFE、郑商所 CZC、大商所 DCE、上期所 SHF、能源中心 INE、广期所 GFE）把与品种不符的后缀改对。`get_market_data` 在 `type=index` 下不改动 `symbol`；港股/美股代码不参与 A 股推断。 |
| **fields** | 返回列筛选；不传通常表示全部字段 |
| **返回值** | 成功时为格式化后的表格字符串（源自 DataFrame）；失败时为统一错误文案 |

---

## 行情数据 `market_data`

### get_market_data

**说明：** 获取日线行情（股票 / 指数 / 期货）。开始、结束日期间隔不超过 5 年。

**返回：** 含日期、代码、开高低收、成交量等。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始日期 YYYYMMDD |
| end_date | 是 | string | 结束日期 YYYYMMDD |
| symbol | 否 | string \| string[] | 代码；A股如 `000001.SZ`，期货如 `A2501.DCE`，指数如 `000001.SH` |
| fields | 否 | string \| string[] | 返回列 |
| type | 否 | enum | `stock`（默认）\|`future`\|`index` |
| indicator | 否 | string | 指数成分筛选，默认 `000985`；可选 `000300`、`000905`、`000985`、`000852`；仅 `type=stock` |
| st | 否 | boolean | 是否含 ST，默认 `true`；仅 `type=stock` |

**期货交易所映射：** CFFEX→CFE, CZCE→CZC, DCE→DCE, SHFE→SHF, INE→INE, GFEX→GFE。

---

### get_market_min_data

**说明：** 获取分钟线。频率与区间限制：`1m`≈1 个月，`5m`≈6 个月，`15m`≈1 年，`60m`≈5 年；指数仅支持 `1m`。

**注意：** 产品类型参数名为 **`symbol_type`**，不是 `type`。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始日期 YYYYMMDD |
| end_date | 是 | string | 结束日期 YYYYMMDD |
| symbol | 否 | string \| string[] | 代码 |
| fields | 否 | string \| string[] | 返回列 |
| symbol_type | 否 | enum | `stock`\|`future`\|`index` |
| time_zone | 否 | [string, string] | 两段交易时段，如 `["10:00","11:00"]` |
| frequency | 否 | enum | `1m`（默认）\|`5m`\|`15m`\|`60m` |

---

## 市场参考数据 `market_ref`

### get_stock_detail

**说明：** A 股 / 港股 / 美股基本信息。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 代码；空串可表示全市场 |
| fields | 否 | string \| string[] | 返回列 |
| market | 否 | enum | `cn`（默认）\|`hk`\|`us` |
| status | 否 | int | `1` 在市，`0` 退市，`-1` 未知 |

---

### get_index_detail

**说明：** 指数基本信息。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 指数代码；空串可全市场 |
| fields | 否 | string \| string[] | 返回列 |
| status | 否 | enum string | `1`\|`0`\|`-1` |

---

### get_concept_list

**说明：** 概念列表及纳入日期。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| concept | 否 | string \| string[] | 概念名，如「英伟达概念」 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |

---

### get_concept_constituents

**说明：** 概念成分股。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| concept | 否 | string \| string[] | 概念名 |
| concept_stock | 否 | string \| string[] | 股票代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| fields | 否 | string \| string[] | 返回列 |

---

### get_industry_detail

**说明：** 申万行业层级信息。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| fields | 否 | string \| string[] | 返回列 |
| level | 否 | string \| string[] | `L1` / `L2` / `L3` |

---

### get_industry_constituents

**说明：** 行业成分股。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| industry_code | 否 | string \| string[] | 行业代码，如 `801780` |
| stock_symbol | 否 | string \| string[] | 股票代码 |
| level | 否 | enum | `L1`\|`L2`\|`L3` |
| fields | 否 | string \| string[] | 返回列 |

---

### get_stock_industry

**说明：** 单只股票所属行业。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| stock_symbol | **是** | string | 如 `000001.SZ` |
| level | 否 | enum | `L1`\|`L2`\|`L3` |

---

### get_index_indicator

**说明：** 指数估值（PB、PE 等）。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 指数代码；空串可全指数 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| fields | 否 | string \| string[] | 返回列 |

---

### get_index_weights

**说明：** 指数成分股权重。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| index_symbol | 否 | string \| string[] | 指数代码 |
| stock_symbol | 否 | string \| string[] | 成分股代码 |
| fields | 否 | string \| string[] | 返回列 |

---

### get_lhb_list

**说明：** 龙虎榜上榜记录。类型示例：`G0007`、`T0020`、`C0000`、`D0000` 等。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码 |
| type | 否 | string \| string[] | 龙虎榜类型代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| fields | 否 | string \| string[] | 返回列 |

---

### get_lhb_detail

**说明：** 龙虎榜营业部明细。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| symbol | 否 | string \| string[] | 股票代码 |
| type | 否 | string \| string[] | 龙虎榜类型 |
| side | 否 | enum | `buy`\|`sell`\|`cum` |
| fields | 否 | string \| string[] | 返回列 |

---

### get_repurchase

**说明：** 回购公告与进程。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| fields | 否 | string \| string[] | 返回列 |

---

### get_margin

**说明：** 融资融券余额与成交。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| symbol | 否 | string \| string[] | 股票代码 |
| fields | 否 | string \| string[] | 返回列 |
| margin_type | 否 | enum | `stock`（融券）\|`cash`（融资） |

---

### get_hsgt_hold

**说明：** 沪深港通持股。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| symbol | 否 | string \| string[] | 股票代码；空串可全市场 |
| fields | 否 | string \| string[] | 返回列 |

---

### get_investor_activity

**说明：** 投资者关系活动记录。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| symbol | 否 | string \| string[] | 股票代码 |
| fields | 否 | string \| string[] | 返回列 |

---

### get_restricted_list

**说明：** 限售解禁明细。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| symbol | 否 | string \| string[] | 股票代码 |
| fields | 否 | string \| string[] | 返回列 |
| market | 否 | string | 默认 `cn` |

---

### get_holder_count

**说明：** 股东户数等。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码；空串可全市场 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| fields | 否 | string \| string[] | 返回列 |

---

### get_top_holders

**说明：** 十大股东 / 流通股东等。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| symbol | 否 | string \| string[] | 股票代码 |
| fields | 否 | string \| string[] | 返回列 |
| market | 否 | string | 默认 `cn` |
| start_rank | 否 | int | 排名起 |
| end_rank | 否 | int | 排名止 |
| stock_type | 否 | enum | `flow`（流通）\|`total`（总股本口径） |

---

### get_block_trade

**说明：** A 股大宗交易。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| fields | 否 | string \| string[] | 返回列 |

---

### get_share_float

**说明：** 股本结构（流通、总股本等）。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| symbol | 否 | string \| string[] | 股票代码 |
| fields | 否 | string \| string[] | 返回列 |

---

## 财务与因子 `financial`

### get_fina_forecast

**说明：** 业绩预告。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码 |
| fields | 否 | string \| string[] | 返回列 |
| info_date | 否 | string | 公告日 YYYYMMDD |
| end_quarter | 否 | string | 报告季，如 `2025q4` |

---

### get_fina_performance

**说明：** 财务快报。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码 |
| fields | 否 | string \| string[] | 返回列 |
| info_date | 否 | string | 公告日 YYYYMMDD |
| end_quarter | 否 | string | 报告季，如 `2025q4` |

---

### get_fina_reports

**说明：** 财报季报（SDK：`get_fina_reports`）；字段前缀 `cfs_*`、`bs_*`、`is_*`、`ratio_*`。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码 |
| start_quarter | 否 | string | 如 `2024q1` |
| end_quarter | 否 | string | 如 `2024q4` |
| start_date | 否 | string | YYYYMMDD；未传季度时用于换算 `start_quarter` |
| end_date | 否 | string | YYYYMMDD；未传季度时用于换算 `end_quarter`，并作为 `date` |
| fields | 否 | string \| string[] | 返回列 |
| is_latest | 否 | bool | 是否每组只保留最新一条 |

---

### get_factor

**说明：** 回测因子（价量 + 可选财务因子）。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| factors | **是** | string \| string[] | 如 `open`、`close`、`volume`、`ratio_pe_ttm` 等 |
| symbol | 否 | string \| string[] | 股票或期货代码 |
| index_component | 否 | string | `100`（沪深300）、`010`（中证500）、`001`（中证1000）、`000`（其他） |
| type | 否 | enum | `stock`（默认）\|`future` |

---

### get_adj_factor

**说明：** 复权因子。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| fields | 否 | string \| string[] | 返回列 |

---

## 交易工具 `trade`

### get_trade_cal

**说明：** 交易日历（SH / HK / US）。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| exchange | 否 | enum | `SH`（默认）\|`HK`\|`US` |
| is_trading_day | 否 | int | `1` 仅交易日，`0` 仅非交易日 |
| fields | 否 | string \| string[] | 返回列 |

---

### get_prev_trade_date

**说明：** 返回**字符串** `YYYYMMDD`，为基准日前第 `n` 个交易日。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| date | **是** | string | 基准日 YYYYMMDD |
| exchange | 否 | enum | `SH`（默认）\|`HK`\|`US` |
| n | 否 | int | 前推交易日个数，默认 `1` |

---

### get_last_trade_date

**说明：** 返回**字符串**最新交易日，无则可能为 `None`。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| exchange | 否 | enum | `SH`（默认）\|`HK`\|`US` |

---

### get_stock_status_change

**说明：** ST、*ST、退市整理等状态变更。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| fields | 否 | string \| string[] | 返回列 |

---

### get_trade_list

**说明：** 指定日期的可交易股票列表。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| date | **是** | string \| string[] | YYYYMMDD，可多日期 |

---

## 期货 `futures`

### get_future_detail

**说明：** 期货合约元数据。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 合约代码 |
| fields | 否 | string \| string[] | 返回列 |
| is_trading | 否 | int | `1` 交易中，`0` 已退市 |

---

### get_future_market_post

**说明：** 期货后复权行情。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| symbol | 否 | string \| string[] | 合约代码 |
| fields | 否 | string \| string[] | 返回列 |

---

### get_future_dominant

**说明：** 品种主力合约序列（参数为**品种**代码，如 `A`、`ZN`，非具体合约）。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| underlying_symbol | 否 | string \| string[] | 品种代码 |

---

## 维护说明

若业务侧 Schema 有变更，请以 `panda_tools/tools/*.py` 中 `TOOLS` 的 `parameters` 为准，并同步更新本文档。

---

## readers 扩展补充（按 TOOLS.parameters）

以下为本次 readers 接入新增方法，按所属章节归类。

### 行情数据 `market_data`（新增）

#### get_hk_daily

**说明：** 港股日线行情。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 港股代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| fields | 否 | string \| string[] | 返回列 |

#### get_us_daily

**说明：** 美股日线行情。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 美股代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| fields | 否 | string \| string[] | 返回列 |

### 市场参考数据 `market_ref`（新增）

#### get_stock_cash_dividend

**说明：** 股票现金分红信息。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| market | 否 | string | 市场，默认 cn |
| fields | 否 | string \| string[] | 返回列 |

#### get_stock_dividend_info

**说明：** 股票分红方案与实施信息。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| market | 否 | string | 市场，默认 cn |
| fields | 否 | string \| string[] | 返回列 |

#### get_stock_split_info

**说明：** 股票送转拆合信息。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| market | 否 | string | 市场，默认 cn |
| fields | 否 | string \| string[] | 返回列 |

#### get_stock_dividend_amount

**说明：** 股票分红金额与分红比例。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| market | 否 | string | 市场，默认 cn |
| fields | 否 | string \| string[] | 返回列 |

#### get_stock_private_placement

**说明：** 股票定向增发信息。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| market | 否 | string | 市场，默认 cn |
| fields | 否 | string \| string[] | 返回列 |

#### get_stock_allotment

**说明：** 股票配股信息。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| market | 否 | string | 市场，默认 cn |
| fields | 否 | string \| string[] | 返回列 |

### 财务与因子 `financial`（新增）

#### get_audit_opinion

**说明：** 审计意见数据。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 股票代码 |
| start_quarter | 否 | string | 起始季度 yyyyqN |
| end_quarter | 否 | string | 结束季度 yyyyqN |
| market | 否 | string | 市场，默认 cn |
| fields | 否 | string \| string[] | 返回列 |

### 期货 `futures`（新增）

#### get_future_netposi_rank

**说明：** 净持仓排名。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| underlying_symbol | 否 | string \| string[] | 品种代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| max_rank | 否 | int | 最大排名 |
| fields | 否 | string \| string[] | 返回列 |
| type | 否 | string | 持仓类型 |

#### get_future_symbol_posi_rank

**说明：** 合约席位持仓排名。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| symbol | 否 | string \| string[] | 合约代码 |
| position_type | 否 | string | 持仓方向 |
| broker_name | 否 | string \| string[] | 席位名称 |
| rank_max | 否 | int | 最大排名 |
| fields | 否 | string \| string[] | 返回列 |

#### get_future_variety_posi_rank

**说明：** 品种席位持仓排名。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| symbol | 否 | string \| string[] | 品种代码 |
| position_type | 否 | string | 持仓方向 |
| broker_name | 否 | string \| string[] | 席位名称 |
| rank_max | 否 | int | 最大排名 |
| fields | 否 | string \| string[] | 返回列 |

#### get_future_contract_daily_indicators

**说明：** 合约日度指标。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| symbol | 否 | string \| string[] | 合约代码 |
| fields | 否 | string \| string[] | 返回列 |

#### get_broker_variety_profit

**说明：** 席位品种盈利。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| symbol | 否 | string \| string[] | 品种代码 |
| fields | 否 | string \| string[] | 返回列 |
| broker | 否 | string \| string[] | 席位名称 |

#### get_broker_grade

**说明：** 席位评级。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| grade | 否 | string | 评级 |

#### get_broker_net_margin

**说明：** 席位净保证金。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| underlying_symbol | 否 | string \| string[] | 品种代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| fields | 否 | string \| string[] | 返回列 |
| broker | 否 | string \| string[] | 席位名称 |

#### get_broker_net_margin_change

**说明：** 席位净保证金变化。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| underlying_symbol | 否 | string \| string[] | 品种代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| fields | 否 | string \| string[] | 返回列 |
| broker | 否 | string \| string[] | 席位名称 |

#### get_broker_total_margin

**说明：** 席位总保证金。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| underlying_symbol | 否 | string \| string[] | 品种代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| fields | 否 | string \| string[] | 返回列 |
| broker | 否 | string \| string[] | 席位名称 |

#### get_future_net_flow

**说明：** 期货净资金流向。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | **是** | string | YYYYMMDD |
| end_date | **是** | string | YYYYMMDD |
| symbol | 否 | string \| string[] | 合约代码 |
| fields | 否 | string \| string[] | 返回列 |
| broker_name | 否 | string \| string[] | 席位名称 |
| position_type | 否 | string | 持仓方向 |

#### get_future_basis

**说明：** 期货基差。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| underlying_symbol | 否 | string \| string[] | 品种代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| fields | 否 | string \| string[] | 返回列 |

#### get_future_wr

**说明：** 期货仓单比率。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| underlying_symbol | 否 | string \| string[] | 品种代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| fields | 否 | string \| string[] | 返回列 |

#### get_future_ls_ratio

**说明：** 期货多空比。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 合约代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |

#### get_future_net_cap_change

**说明：** 期货净资金变化。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 合约代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| broker | 否 | string \| string[] | 席位名称 |

#### get_future_contract_rank

**说明：** 期货合约席位排名。

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| symbol | 否 | string \| string[] | 合约代码 |
| underlying_symbol | 否 | string \| string[] | 品种代码 |
| start_date | 否 | string | YYYYMMDD |
| end_date | 否 | string | YYYYMMDD |
| type | 否 | string | 统计类型 |
| max_rank | 否 | int | 最大排名 |
| rank_type | 否 | string | 排名类型 |
