# context 对象完整参考

## context.now - 当前时间

```python
context.now  # 回测时=回测当前时间，实时时=系统本地时间
# 返回: datetime.datetime, 如 2024-01-22 09:40:00+08:00
```

## context.mode - 运行模式

```python
context.mode  # 1=实时，2=回测
if context.mode == 1:
    print('实时模式')
elif context.mode == 2:
    print('回测模式')
```

## context.symbols - 已订阅代码集合

```python
context.symbols  # set(str)，如 {'SHSE.600000', 'SZSE.000001'}
```

## context.data() - 数据滑窗

```python
data = context.data(symbol='SHSE.600000', frequency='1d', count=20)
```

详见 `04-market-data.md`。

## context.account() - 账户对象

```python
# 默认账户
acc = context.account()

# 多账户时指定
acc = context.account(account_id='YOUR_ACCOUNT_ID')

# 查询持仓
all_positions = acc.positions()
pos = acc.position(symbol='SHSE.600000', side=PositionSide_Long)

# 查询资金
cash = acc.cash

# 查询账户状态
status = acc.status  # {'state': 3, 'error': {'code': 0, ...}}
```

**账户状态 state**：0=未知，1=正常，2=错误，3=连接中

## context.parameters - 动态参数

```python
# 获取所有动态参数 dict
params = context.parameters
# {'k_value': {'key': 'k_value', 'value': 23.0, 'max': 100.0, ...}}
```

## context.backtest_start_time / end_time

```python
context.backtest_start_time  # 回测开始时间（datetime）
context.backtest_end_time    # 回测结束时间（datetime）
```

## context.自定义属性

```python
def init(context):
    context.my_threshold = 0.05     # 自定义阈值
    context.stock_pool = []         # 自定义股票池
    context.hold_days = {}          # 自定义持仓天数字典
```

## 实用模式：init 预加载数据

```python
def init(context):
    # 一次性拿取全回测期的涨跌停数据
    instruments = get_history_symbol(
        symbol='SZSE.000001',
        start_date=context.backtest_start_time,
        end_date=context.backtest_end_time
    )
    context.inst_dict = {
        (i.symbol, i.trade_date.date()): i
        for i in instruments
    }
    subscribe(symbols='SZSE.000001', frequency='1d')

def on_bar(context, bars):
    key = (bars[0].symbol, bars[0].eob.date())
    info = context.inst_dict.get(key)
    if info:
        print(f'涨停价: {info.upper_limit}，跌停价: {info.lower_limit}')
```
