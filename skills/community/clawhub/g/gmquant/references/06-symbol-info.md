# 标的信息查询

## get_symbol_infos - 查询标的基本信息（静态信息）

> 与时间无关，返回标的基础属性

```python
get_symbol_infos(sec_type1, sec_type2=None, exchanges=None, symbols=None, df=False)
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sec_type1 | int | **是** | 证券大类：1010=股票，1020=基金，1030=债券，1040=期货，1050=期权，1060=指数，1070=板块 |
| sec_type2 | int | 否 | 证券细类（见下表） |
| exchanges | str/list | 否 | 交易所代码，如 `'SHSE,SZSE'` |
| symbols | str/list | 否 | 标的代码 |
| df | bool | 否 | True=DataFrame，False=list[dict] |

**sec_type2 细类表**：
- 股票：101001=A股，101002=B股，101003=存托凭证
- 基金：102001=ETF，102002=LOF，102005=FOF
- 债券：103001=可转债，103003=国债，103006=企业债，103008=回购
- 期货：104001=股指期货，104003=商品期货，104006=国债期货
- 期权：105001=股票期权，105002=指数期权，105003=商品期权
- 指数：106001=股票指数，106002=基金指数，106003=债券指数

```python
from gm.api import *
set_token('YOUR_TOKEN')

# 查询指定股票
infos = get_symbol_infos(sec_type1=1010, symbols='SHSE.600000,SZSE.000001', df=True)

# 查询全部 A 股
infos = get_symbol_infos(sec_type1=1010, sec_type2=101001, df=True)

# 查询全部 ETF
infos = get_symbol_infos(sec_type1=1020, sec_type2=102001, df=True)

# 查询全部可转债
infos = get_symbol_infos(sec_type1=1030, sec_type2=103001, df=True)

# 查询上交所股票期权
infos = get_symbol_infos(sec_type1=1050, sec_type2=105001, exchanges='SHSE', df=True)
```

**返回字段**：`symbol`、`sec_type1`、`sec_type2`、`board`、`exchange`、`sec_id`、`sec_name`、`sec_abbr`、`price_tick`、`trade_n`、`listed_date`、`delisted_date`、`underlying_symbol`（期货/期权/可转债）、`option_type`（欧式E/美式A）、`call_or_put`（C/P）

---

## get_symbols - 查询指定交易日多标的交易信息

> 返回基本信息 + 当日行情信息（涨跌停、换手率等）

```python
get_symbols(sec_type1, sec_type2=None, exchanges=None, symbols=None,
            skip_suspended=True, skip_st=True, trade_date=None, df=False)
```

| 参数 | 说明 |
|------|------|
| skip_suspended | 是否跳过停牌，默认 True |
| skip_st | 是否跳过 ST 类股票，默认 True |
| trade_date | 交易日期 `%Y-%m-%d`，默认 None=最新截面 |

```python
# 获取全 A 股今日信息（含涨跌停价）
df = get_symbols(sec_type1=1010, sec_type2=101001, df=True)
symbols_list = df['symbol'].tolist()

# 指定交易日
df = get_symbols(sec_type1=1010, symbols='SHSE.600000,SZSE.000001',
                 trade_date='2024-01-15', df=True)
```

**额外返回字段（比 get_symbol_infos 多）**：
`trade_date`、`pre_close`、`upper_limit`（涨停价）、`lower_limit`（跌停价）、`turn_rate`（换手率%）、`adj_factor`（复权因子）、`is_suspended`（是否停牌）、`is_st`（是否ST）、`margin_ratio`（期货保证金比例）、`multiplier`（合约乘数）

---

## get_history_symbol - 查询指定标的多日历史交易信息

```python
get_history_symbol(symbol=None, start_date=None, end_date=None, df=False)
```

| 参数 | 说明 |
|------|------|
| symbol | 单个标的代码（必填） |
| start_date | 开始日期 `%Y-%m-%d` |
| end_date | 结束日期 `%Y-%m-%d` |

```python
# 查询某标的历史涨跌停价变化
df = get_history_symbol(symbol='SHSE.600000',
                        start_date='2024-01-01',
                        end_date='2024-12-31', df=True)
```

**注意**：`get_history_symbol` 可在 `init` 里批量预取，按 (symbol, date) 做索引，提高回测效率：
```python
def init(context):
    instruments = get_history_symbol(symbol='SZSE.000001',
                                     start_date=context.backtest_start_time,
                                     end_date=context.backtest_end_time)
    context.ins_dict = {(i.symbol, i.trade_date.date()): i for i in instruments}

def on_bar(context, bars):
    info = context.ins_dict[(bars[0].symbol, bars[0].eob.date())]
    print(info.upper_limit)
```
