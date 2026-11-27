# 股票财务数据 API 字段速查（免费）

> 来源：掘金官方文档 `股票财务数据及基础数据函数（免费）.md`
> 本地文档路径: `D:\本地文档\mq-docs\sdk\python\API介绍\股票财务数据及基础数据函数（免费）.md`

---

## API 总览

| 函数 | 功能 | fields 必填 | 多标的 | 截面/时序 |
|------|------|:---:|:---:|:---:|
| `stk_get_index_constituents` | 指数成分股 | - | - | 截面 |
| `stk_get_fundamentals_balance_pt` | 资产负债表(截面) | Y | Y | 截面 |
| `stk_get_fundamentals_cashflow_pt` | 现金流量表(截面) | Y | Y | 截面 |
| `stk_get_fundamentals_income_pt` | 利润表(截面) | Y | Y | 截面 |
| `stk_get_finance_prime_pt` | 财务主要指标(截面) | Y | Y | 截面 |
| `stk_get_finance_deriv_pt` | 财务衍生指标(截面) | Y | Y | 截面 |
| `stk_get_daily_valuation_pt` | 估值指标(截面) | Y | Y | 截面 |
| `stk_get_daily_mktvalue_pt` | 市值指标(截面) | Y | Y | 截面 |
| `stk_get_daily_basic_pt` | 基础指标/股本(截面) | Y | Y | 截面 |
| `stk_get_fundamentals_balance` | 资产负债表(时序) | Y | N(单标的) | 时序 |
| `stk_get_fundamentals_cashflow` | 现金流量表(时序) | Y | N | 时序 |
| `stk_get_fundamentals_income` | 利润表(时序) | Y | N | 时序 |
| `stk_get_finance_prime` | 财务主要指标(时序) | Y | N | 时序 |
| `stk_get_finance_deriv` | 财务衍生指标(时序) | Y | N | 时序 |
| `stk_get_daily_valuation` | 估值指标(时序) | Y | N | 时序 |
| `stk_get_daily_mktvalue` | 市值指标(时序) | Y | N | 时序 |
| `stk_get_daily_basic` | 基础指标(时序) | Y | N | 时序 |

**关键区别**:
- `_pt` 后缀 = 截面数据(point-in-time), 多标的, 查询某日/最新
- 无 `_pt` 后缀 = 时序数据, 单标的, 需要 start_date/end_date
- **所有 fields 都是必填! 不能为空! 不能超过20个!**

---

## 常用字段速查

### 资产负债表 (stk_get_fundamentals_balance_pt)

| 字段名 | 中文 | 说明 |
|--------|------|------|
| mny_cptl | 货币资金 | 现金+存款 |
| invt | 存货 | |
| fix_ast | 固定资产 | |
| intg_ast | 无形资产 | |
| gw | 商誉 | |
| ttl_cur_ast | 流动资产合计 | |
| ttl_ncur_ast | 非流动资产合计 | |
| ttl_ast | 资产总计 | **最常用** |
| sht_ln | 短期借款 | |
| lt_ln | 长期借款 | |
| acct_pay | 应付账款 | |
| ttl_cur_liab | 流动负债合计 | |
| ttl_ncur_liab | 非流动负债合计 | |
| ttl_liab | 负债合计 | **最常用** |
| paid_in_cptl | 实收资本/股本 | |
| cptl_rsv | 资本公积 | |
| sur_rsv | 盈余公积 | |
| ret_prof | 未分配利润 | |
| ttl_eqy_pcom | 归属母公司股东权益合计 | **最常用** |
| ttl_eqy | 股东权益合计 | **最常用** |

### 利润表 (stk_get_fundamentals_income_pt)

| 字段名 | 中文 | 说明 |
|--------|------|------|
| ttl_inc_oper | 营业总收入 | |
| inc_oper | 营业收入 | **最常用** |
| cost_oper | 营业成本 | |
| ttl_cost_oper | 营业总成本 | |
| sell_exp | 销售费用 | |
| admin_exp | 管理费用 | |
| fin_exp | 财务费用 | |
| rd_exp | 研发费用 | |
| oper_prof | 营业利润 | **最常用** |
| ttl_prof | 利润总额 | |
| net_prof | 净利润 | **最常用** |
| net_prof_pcom | 归属母公司净利润 | **最常用** |
| net_prof_ncs | 少数股东损益 | |

### 现金流量表 (stk_get_fundamentals_cashflow_pt)

| 字段名 | 中文 | 说明 |
|--------|------|------|
| cash_rcv_sale | 销售收到现金 | |
| cash_pur_gds_svc | 购买商品支付现金 | |
| net_cf_oper | 经营活动现金流净额 | **最常用** |
| cash_rcv_sale_inv | 收回投资收到现金 | |
| cash_pay_inv | 投资支付现金 | |
| net_cf_inv | 投资活动现金流净额 | **最常用** |
| cash_rcv_cptl | 吸收投资收到现金 | |
| cash_rpay_brw | 偿还债务支付现金 | |
| net_cf_fin | 筹资活动现金流净额 | **最常用** |
| net_incr_cash_eq | 现金净增加额 | |

### 财务主要指标 (stk_get_finance_prime_pt)

| 字段名 | 中文 | 说明 |
|--------|------|------|
| eps_basic | 基本每股收益 | 元 |
| eps_dil | 稀释每股收益 | 元 |
| eps_basic_cut | 扣非基本每股收益 | 元 |
| bps_sh | 归属普通股每股净资产 | 元 |
| ttl_inc_oper | 营业总收入 | 元 |
| inc_oper | 营业收入 | 元 |
| net_prof_pcom | 归母净利润 | 元 |
| roe | 全面摊薄ROE | % |
| **roe_weight_avg** | 加权平均ROE | % ⚠️不是roe_waa! |
| roe_weight_avg_cut | 扣非加权ROE | % |
| inc_oper_yoy | 营收同比 | % |
| net_prof_pcom_yoy | 归母净利润同比 | % |

### 财务衍生指标 (stk_get_finance_deriv_pt)

| 字段名 | 中文 | 说明 |
|--------|------|------|
| eps_basic | 每股收益EPS(基本) | 元 |
| eps_dil2 | 每股收益EPS(稀释) | 元 ⚠️不是eps_dil! |
| eps_dil | 每股收益EPS(期末股本摊薄) | 元 |
| ttl_inc_oper_ps | 每股营业总收入 | 元 |
| inc_oper_ps | 每股营业收入 | 元 |
| ebit_ps | 每股息税前利润 | 元 |
| ttl_inc_oper_yoy | 营业总收入同比增长率 | % |
| inc_oper_yoy | 营业收入同比增长率 | % |
| oper_prof_yoy | 营业利润同比增长率 | % |

### 估值指标 (stk_get_daily_valuation_pt)

| 字段名 | 中文 | 说明 |
|--------|------|------|
| **pe_ttm** | 市盈率(TTM) | 倍 ⭐最常用 |
| pe_lyr | 市盈率(最新年报LYR) | 倍 |
| pe_mrq | 市盈率(最新报告期MRQ) | 倍 |
| pe_ttm_cut | 市盈率TTM扣非 | 倍 |
| **pb_mrq** | 市净率(最新MRQ) | 倍 ⭐最常用 |
| pb_lyr | 市净率(最新年报LYR) | 倍 |
| ps_ttm | 市销率(TTM) | 倍 |
| ps_lyr | 市销率(LYR) | 倍 |
| pcf_ttm_oper | 市现率(经营现金流TTM) | 倍 |
| pcf_ttm_ncf | 市现率(现金净流量TTM) | 倍 |
| peg_lyr | PEG值 | |
| **dy_ttm** | 股息率(TTM) | % ⭐最常用 |

### 市值指标 (stk_get_daily_mktvalue_pt)

| 字段名 | 中文 | 说明 |
|--------|------|------|
| **tot_mv** | 总市值 | 元 ⭐最常用 |
| tot_mv_csrc | 总市值(证监会算法) | 元 |
| **a_mv** | A股流通市值(含限售) | 元 ⭐最常用 |
| a_mv_ex_ltd | A股流通市值(不含限售) | 元 |
| ev | 企业价值(含货币资金) | 元 |
| ev_ex_curr | 企业价值(剔除货币资金) | 元 |
| ev_ebitda | 企业倍数 | 倍 |
| equity_value | 股权价值 | 元 |

### 基础指标/股本 (stk_get_daily_basic_pt / stk_get_daily_basic)

**函数原型**

```python
stk_get_daily_basic_pt(symbols, fields, trade_date=None, df=False)          # 截面，多标的
stk_get_daily_basic(symbol, fields, start_date=None, end_date=None, df=False)  # 时序，单标的
```

| 字段名 | 中文 | 量纲 | 说明 |
|--------|------|------|------|
| tclose | 收盘价 | 元 | 当日收盘价（算市值要用上一交易日的） |
| turnrate | 当日换手率 | % | 成交量 ÷ 流通股本 |
| **ttl_shr** | 总股本 | 股 | ⭐常用 |
| **circ_shr** | 流通股本 | 股 | = 无限售条件流通股本 + 有限售条件流通股本。⚠️不是 float_shr |
| ttl_shr_unl | 无限售条件流通股本 | 股 | **A股 + H股**。⚠️注意：不是"行情软件的流通股" |
| ttl_shr_ltd | 有限售条件股本 | 股 | |
| a_shr_unl | 无限售条件流通A股股本 | 股 | **行情软件显示的"流通股"就是这个** |
| h_shr_unl | 无限售条件流通H股股本 | 股 | |
| **free_shr** | **自由流通股本** | 股 | ⭐新增。= A股总股本 − A股限售股本 − 减持受控非限售股本 − 合计持股5%以上大股东持有的其他非限售股本 |
| **free_turnrate** | **自由流通换手率** | % | ⭐新增。= 成交量 ÷ 自由流通股本 × 100% |

**字段语义变更提醒（2026-11 官方更新）**

旧版本字段含义：
- `ttl_shr_unl` = 无限售条件流通股本（行情软件定义的流通股）
- `a_shr_unl` = 无限售条件流通股本（A股）

新版本字段含义：
- `ttl_shr_unl` = 无限售条件流通股本（**A股 + H股**）
- `a_shr_unl` = 无限售条件流通A股股本（**行情软件定义的流通股**）

> 对纯 A 股标的（无 H 股）两者数值相同；对有 H 股的标的（如 A+H 上市的银行股）才会不同。做全市场截面筛选时要注意这个差异。

**流通市值怎么算**

```python
import pandas as pd

d = stk_get_daily_basic(symbol='SHSE.600519',
                        fields='tclose,circ_shr,free_shr',
                        start_date='2026-11-18', end_date='2026-11-26', df=True)
d = d.sort_values('trade_date').reset_index(drop=True)

# 必须用上一交易日收盘价，否则是"当日收盘市值"，引入未来函数
d['free_mv'] = d['free_shr'] * d['tclose'].shift(1)   # 自由流通市值
d['circ_mv'] = d['circ_shr'] * d['tclose'].shift(1)   # 流通市值
d['free_mv_yi'] = d['free_mv'] / 1e8                  # 换成亿元
```

> `_pt` 截面版没有历史序列，要自己再查一次上一交易日的 `tclose`。

**实测样例（SHSE.600519，2026-11-26）**

| 字段 | 值 | 说明 |
|------|-----|------|
| tclose | 1469.00 | 元 |
| turnrate | 0.2593 | % |
| free_turnrate | 0.5185 | % |
| circ_shr | 1,250,081,601 | 股 |
| free_shr | 625,040,801 | 股 |
| ttl_shr | 1,250,081,601 | 股 |
| a_shr_unl | 1,250,081,601 | 股 |
| h_shr_unl | 0 | 股 |
| ttl_shr_ltd | 0 | 股 |

自洽校验：`free_turnrate / turnrate = 0.5185 / 0.2593 ≈ 2.0`，等于 `circ_shr / free_shr = 2.0`。两个换手率口径互相印证。

---

## rpt_type 报表类型枚举

| 值 | 含义 |
|----|------|
| 1 | 一季度报 |
| 2 | 第二季度 |
| 3 | 第三季度 |
| 4 | 第四季度 |
| 6 | 中报 |
| 9 | 前三季报 |
| 12 | 年报 |

## data_type 数据类型枚举

| 值 | 含义 |
|----|------|
| 100 | 合并最初(未修正) |
| 101 | 合并原始 |
| 102 | 合并调整(默认) |
| 200 | 母公司最初 |
| 201 | 母公司原始 |
| 202 | 母公司调整 |

---

*整理于 2026-04-17, 已测试 9/9 通过*
*2026-11-27 更新：基础指标新增 `free_shr`（自由流通股本）、`free_turnrate`（自由流通换手率），并修正 `ttl_shr_unl` / `a_shr_unl` 的语义（ttl_shr_unl 现为 A股+H股）。已实测通过（SHSE.600519）。*
