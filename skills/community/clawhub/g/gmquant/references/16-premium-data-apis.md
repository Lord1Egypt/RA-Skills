# 增值数据 API 速查（付费）

> 来源：掘金官方文档 v3.0.145+，需要开通相应增值数据权限
> 本地文档路径: `D:\本地文档\mq-docs\sdk\python\API介绍\`

---

## 一、股票增值数据（付费）

| 函数 | 功能 | 关键参数 | 返回 |
|------|------|---------|------|
| `stk_get_industry_category` | 行业分类查询 | source='zjh2012'/'sw2021', level=1/2/3 | DataFrame(行业代码+名称) |
| `stk_get_industry_constituents` | 某行业成分股 | industry_code(必填), date | DataFrame(代码/名称/纳入剔除日) |

**注意**: `stk_get_industry_category` 支持 **证监会2012(zjh2012)** 和 **申万2021(sw2021)** 两套行业分类

---

## 二、期货增值数据（付费）- gm3.0.145+

| 函数 | 功能 | 关键参数 | 返回 |
|------|------|---------|------|
| `fut_get_contract_info` | 期货标准品种信息 | product_codes(必填), df | list[dict]/DF (合约规格/乘数/交易时间等) |
| `fut_get_transaction_rankings` | 每日成交持仓排名 | symbols(必填), trade_date, indicators='volume,long,short' | DataFrame(前20名会员) |
| `fut_get_warehouse_receipt` | 期货仓单数据 | product_code(必填), start_date, end_date | DataFrame(仓库/注册仓单/库存) |
| `fut_get_continuous_contracts` | 查询连续合约对应的真实合约 | csymbol(必填), start_date, end_date | DataFrame(真实合约代码/日期) |

**关键字段 - fut_get_contract_info**:
- product_name/code, underlying_symbol, multiplier(乘数), price_tick(最小变动)
- trade_time, price_range(涨跌停), minimum_margin, last_trade_date
- delivery_method(交割方式: 现金/实物)

**关键字段 - fut_get_warehouse_receipt**:
- on_warrant(注册仓单量), future_inventory(库存), warehouse_capacity(库容量)
- effective_forecast(有效预报, 仅郑商所)

### fut_get_continuous_contracts 详细文档

查询连续合约在指定时间区间内对应的真实合约代码。

```python
fut_get_continuous_contracts(csymbol, start_date="", end_date="")
```

| 参数 | 类型 | 中文名称 | 必填 | 默认值 | 说明 |
|------|------|---------|:----:|:-----:|------|
| csymbol | str | 连续合约代码 | Y | 无 | 只能输入一个。支持主力合约、次主力、前5个月份连续和加权指数合约代码 |
| start_date | str | 开始时间 | N | "" | 交易日期 %Y-%m-%d 格式，默认""表示最新交易日 |
| end_date | str | 结束时间 | N | "" | 交易日期 %Y-%m-%d 格式，默认""表示最新交易日 |

**返回值**：`list[DictLikeObject]`，每项包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | str | 真实合约代码（如 CFFEX.IM2503） |
| trade_date | str | 交易日（%Y-%m-%d） |

**csymbol 连续合约后缀规则**：

| 代码后缀 | 含义 | 示例 |
|:---------:|------|------|
| 无后缀 | 主力连续合约 | `CFFEX.IM` |
| 22 | 次主力连续合约 | `CFFEX.IM22` |
| 00 | 当月连续合约 | `CFFEX.IM00` |
| 01 | 下月连续合约 | `CFFEX.IM01` |
| 02 | 下季连续合约 | `CFFEX.IM02` |
| 03 | 隔季连续合约 | `CFFEX.IM03` |
| 99 | 加权指数合约 | `CFFEX.IM99`（注意：某些市场加权指数可能返回空数据） |

```python
from gm.api import *
set_token('YOUR_TOKEN')

# 查询中证1000主力连续合约2025Q1对应的真实合约
result = fut_get_continuous_contracts('CFFEX.IM', start_date='2025-01-01', end_date='2025-03-31')
for item in result:
    print(item['symbol'], item['trade_date'])
# 输出示例: CFFEX.IM2503 2025-01-02, ..., CFFEX.IM2506 2025-03-21

# 查询当月连续
result = fut_get_continuous_contracts('CFFEX.IM00', start_date='2025-01-01', end_date='2025-03-31')
```

> ⚠️ 连续合约查询返回每个交易日该连续合约所对应的**真实合约代码**（如 IM2503），可用于实盘/仿真模式下订阅具体合约行情或下单。**返回值是 list 非 DataFrame**。

---

## 三、基金增值数据（付费）- gm3.0.145+

| 函数 | 功能 | 关键参数 | 返回 |
|------|------|---------|------|
| `fnd_get_etf_constituents` | ETF最新成分股 | etf(必填) | DF(成分股/数量/现金替代标志/溢价比例) |
| `fnd_get_portfolio` | 基金资产组合 | fund(必填), report_type(1/2/3/4/6/12), portfolio_type('stk','bnd','fnd') | DF(持仓详情+占比) |
| `fnd_get_net_value` | 基金净值 | fund(必填), start_date, end_date | DF(unit_nv/unit_nv_accu/unit_nv_adj) |
| `fnd_get_adj_factor` | 基金复权因子 | fund(必填), base_date | DF(adj_factor_bwd_acc/adj_factor_fwd) |
| `fnd_get_dividend` | 基金分红信息 | fund(必填), start_date(必填), end_date(必填) | DF(dvd_ratio/派息/登记日/除息日/发放日...) |
| `fnd_get_split` | 基金拆分折算 | fund(必填), start/end | DF(split_type/split_ratio/折算/拆分日期...) |
| `fnd_get_share` | 基金规模(3.0.172+) | fund(必填), start/end=None | DF(trade_date/pub_date/share份额) |
| `get_open_call_auction` | 集合竞价开盘(3.0.176+) | symbols(必填), trade_date | DF(开盘价/成交量/五档买卖) |

**关键字段 - fnd_get_etf_constituents**:
- symbol(成分股), amount(申购单位对应数量), cash_subs_type(1禁止/2允许/3必须/4退补)
- cash_subs_sum(固定替代金额), cash_premium_rate(溢价%)

**关键字段 - fnd_get_portfolio (portfolio_type='stk')**:
- hold_share(持仓股数), hold_value(持仓市值), nv_rate(占净值%)
- ttl_share_rate(占总股本%), clrc_share_rate(占流通股%)

**关键字段 - fnd_get_dividend**:
- dvd_ratio(10:X 每10份税前分红), ex_dvd_date(场内除息日)
- pay_dvd_date(场内红利发放日)

---

## 四、可转债增值数据（付费）- gm3.0.145+

| 函数 | 功能 | 关键参数 | 返回 |
|------|------|---------|------|
| `bnd_get_conversion_price` | 转股价变动 | symbol(必填), start/end | DF(转股价/转股比例/本期转股数/变动原因) |
| `bnd_get_call_info` | 赎回信息 | symbol(必填), start/end | DF(赎回类型/原因/价格/登记日/资金到账日) |
| `bnd_get_put_info` | 回售信息 | symbol(必填), start/end | DF(回售原因/价格/行权起止日) |
| `bnd_get_amount_change` | 剩余规模变动 | symbol(必填), start/end | DF(变动类型/本次金额/剩余金额) |
| `bnd_get_analysis` | 分析指标(3.0.172+) | symbol(必填), start/end=None | DF(转股价值/溢价率/纯债价值/套利空间/稀释率) |
| `get_open_call_auction` | 集合竞价开盘(3.0.176+) | symbols(必填), trade_date | DF(开盘价/成交量/五档买卖) |

**关键字段 - bnd_get_conversion_price**:
- conversion_price(转股价), conversion_rate(转股比例%)
- conversion_volume(本期转股股数), bond_float_amount_remain(流通余额万元)
- event_type(初始/调整/修正转股价), change_reason(发行/修正/派息...)

**关键字段 - bnd_get_analysis** (最有价值的分析指标):
- cnv_value(转股价值/平价), cnv_premium_rate(转股溢价率%), arbitrage(套利空间)
- pure_value_cb/csi(纯债价值 中债/中证基准), floor_premium_rate(平价底价溢价率→偏股/混合/偏债划分)
- cnv_dil_rate/circ_dil_rate(转股稀释率%)

**转债风格判断 (floor_premium_rate)**:
- > 1.2 → 偏股型转债
- 0.8 ~ 1.2 → 混合型转债  
- < 0.8 → 偏债型转债

---

## 五、使用注意事项

1. **所有 `_pt` 后缀函数的 fields 都是必填的！** 不能传空字符串，不能省略，否则报错"填写的 fields 不正确"
2. **fields 不超过 20 个字段**
3. **stk_get_index_constituents 没有 df 参数** — 直接返回 DataFrame
4. **fut_get_warehouse_receipt 的 product_code 只能填一个品种**
5. **基金/可转债的 fnd_* / bnd_* 函数的 fund/symbol 只能填单个标的**
6. **get_open_call_auction 数据最早为 2025-02-21**
7. **bnd_get_analysis 是最实用的转债分析函数** — 一次调用拿到转股价值/溢价/纯债/套利/稀释率全部指标

---

*文档整理于 2026-04-17, 基于掘金官方 markdown 文档*
