# 行情数据查询

## current - 查询当前行情快照

```python
current(symbols, fields='', include_call_auction=False)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| symbols | str or list | 标的代码 |
| fields | str | 返回字段，默认所有 |
| include_call_auction | bool | 是否支持集合竞价(09:15-09:25)取数，默认 False |

**返回值**：`list[dict]`，每项是一个 tick 字典

```python
from gm.api import *
set_token('YOUR_TOKEN')

result = current(symbols='SZSE.000001,SHSE.600000')
for item in result:
    print(item['symbol'], item['price'])
```

**注意**：
- 实时模式返回最新 tick，回测模式只有 symbol/price/created_at 有效
- 集合竞价阶段有效字段只有 quotes

**⚠️ 实时模式调用频次限制（2026-05-19 起）**：
- 5分钟内最多调用 **100 次**
- 24小时内最多调用 **1000 次**
- **2026-06-01 起**：单次查询标的数量上限调整为 **50 个**

> **强烈建议切换到新函数**：`last_tick`（多标的Tick快照）或 `current_price`（仅查最新价）完全不受上述频次限制，且返回数据更精简高效。详见下方说明。

---

## last_tick - 查询已订阅的最新 Tick（多标的，推荐替代 current）

> **推荐理由**：不受 `current()` 的调用频次限制（5分钟100次/24小时1000次），返回数据更精简高效。

```python
last_tick(symbols, fields="", include_call_auction=False)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| symbols | str or list | 标的代码，多个用英文逗号隔开或列表格式 |
| fields | str | 返回字段，默认所有（详见 tick 对象字段） |
| include_call_auction | bool | 是否支持集合竞价(09:15-09:25)取数，默认 False |

**返回值**：`list[dict]`，每个字典包含 `symbol`、`price`、`created_at` 等字段

```python
from gm.api import *
set_token('YOUR_TOKEN')

# 必须先订阅 tick 行情
subscribe(symbols='SZSE.000001,SHSE.600000', frequency='tick')

# 查询最新 tick
result = last_tick(symbols='SZSE.000001,SHSE.600000', fields='symbol,price,open,created_at')
for item in result:
    print(item['symbol'], item['price'])
```

**注意**：
- 输入的 `symbols` **必须先通过 `subscribe` 订阅 tick 行情**；若未订阅，返回字典中除 `symbol` 外均为空
- 实时模式获取集合竞价数据需指定 `include_call_auction=True`，集合竞价阶段有效字段仅 `quotes`
- 回测模式需先订阅 tick，返回回测当前时刻最新的 `tick.price`

---

## current_price - 查询当前最新价（更轻量替代 current）

> **推荐理由**：仅返回最新价，不受 `current()` 调用频次限制，数据量更小。

```python
current_price(symbols)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| symbols | str or list | 标的代码，多个用英文逗号隔开或列表格式 |

**返回值**：`list[dict]`，每个字典包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | str | 标的代码，如 `SHSE.600000` |
| price | float | 最新价；实时模式为当前 tick.price；回测模式根据订阅频度返回对应 bar.close 或 tick.price |
| created_at | datetime | 创建时间 |

```python
from gm.api import *
set_token('YOUR_TOKEN')

# 查询单标的最新价
result = current_price(symbols='SZSE.000001')
print(result[0]['symbol'], result[0]['price'])

# 查询多标的最新价
result = current_price(symbols='SZSE.000001,SHSE.600000')
```

**注意**：
- 若输入包含无效标的代码，返回列表仅包含有效代码对应的字典
- 回测模式：订阅 tick 或分钟 bar 后调用，返回当前时刻最新价；订阅日线时根据 `backtest_intraday` 参数决定返回值

---

## history - 查询历史行情

```python
history(symbol, frequency, start_time, end_time,
        fields=None, skip_suspended=True, fill_missing=None,
        adjust=ADJUST_NONE, adjust_end_time='', df=True)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| symbol | str or list | 标的代码，支持多标的 |
| frequency | str | 频率：`'tick'`、`'60s'`、`'300s'`、`'1d'` 等 |
| start_time | str/datetime | 开始时间 `%Y-%m-%d %H:%M:%S` |
| end_time | str/datetime | 结束时间 `%Y-%m-%d %H:%M:%S` |
| fields | str | 指定字段，默认全部 |
| adjust | int | 复权：`ADJUST_NONE=0`、`ADJUST_PREV=1`、`ADJUST_POST=2` |
| adjust_end_time | str | 复权基点时间，默认当前 |
| df | bool | True=返回 DataFrame，False=返回 list[dict] |

```python
# 查询日线（前复权），返回 DataFrame
df = history(symbol='SHSE.600000', frequency='1d',
             start_time='2024-01-01', end_time='2024-12-31',
             fields='open,high,low,close,volume,eob',
             adjust=ADJUST_PREV, df=True)

# 查询多标的
df = history(symbol='SHSE.600000,SZSE.000001', frequency='1d',
             start_time='2024-01-01', end_time='2024-01-31',
             df=True)

# 返回 list[dict]
data = history(symbol='SHSE.000300', frequency='1d',
               start_time='2024-01-01', end_time='2024-01-05',
               adjust=ADJUST_PREV, df=False)
```

**注意**：
- 数据区间采用**前开后闭**方式，按 eob 升序排序
- 单次最多返回 33000 条
- start_time/end_time 输入不存在的日期会报错
- `skip_suspended` 和 `fill_missing` 目前暂不支持

---

## history_n - 查询最新 N 条历史行情

```python
history_n(symbol, frequency, count, end_time=None,
          fields=None, skip_suspended=True, fill_missing=None,
          adjust=ADJUST_NONE, adjust_end_time='', df=False)
```

| 参数 | 说明 |
|------|------|
| symbol | 单标的代码（不支持多标的） |
| count | 取最新 N 条 |
| end_time | 结束时间，默认 None（取实际当前时间，非回测时间） |

```python
# 取最新100条日线（前复权）
df = history_n(symbol='SHSE.600519', frequency='1d', count=100,
               end_time='2024-12-31 15:30:00',
               fields='symbol,open,close,high,low,eob',
               adjust=ADJUST_PREV, df=True)
print(df.tail())
```

---

## context.data - 获取订阅数据滑窗

> 必须先调用 `subscribe` 才能使用

```python
data = context.data(symbol, frequency, count, fields)
```

| 参数 | 说明 |
|------|------|
| symbol | 单标的（不支持多标的） |
| frequency | 必须是已订阅的频率 |
| count | 必须 ≤ subscribe 里的 count |
| fields | 必须在 subscribe 的 fields 范围内 |

返回格式与 subscribe 的 format 参数一致：
- `format='df'`（默认）→ DataFrame
- `format='row'` → list[dict]
- `format='col'` → dict（col 模式下 tick 的 quotes 被拆分，只有买卖一档）

```python
def init(context):
    subscribe(symbols='SHSE.600519', frequency='60s', count=50,
              fields='symbol,close,eob', format='df')

def on_bar(context, bars):
    data = context.data(symbol=bars[0]['symbol'], frequency='60s', count=20)
    ma5 = data['close'].rolling(5).mean()
    print(ma5.tail())
```
