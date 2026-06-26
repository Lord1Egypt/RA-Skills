# 核心基础函数

## set_token - 设置用户 Token

```python
set_token('YOUR_TOKEN_ID')
```

- 纯数据查询时第一步必须调用
- Token 在掘金终端「系统设置 → 密钥管理」中获取
- Token 不正确会抛出异常

---

## run - 启动策略

```python
run(strategy_id='', filename='', mode=MODE_UNKNOWN, token='',
    backtest_start_time='', backtest_end_time='',
    backtest_initial_cash=1000000, backtest_transaction_ratio=1,
    backtest_commission_ratio=0, backtest_slippage_ratio=0,
    backtest_adjust=ADJUST_NONE, backtest_check_cache=1,
    serv_addr='', backtest_match_mode=0)
```

详细参数说明见 `01-quick-start.md`。

---

## stop - 停止策略

```python
stop()
```

- 停止策略，退出策略进程
- 示例：当订阅代码集合为空时停止
```python
if not context.symbols:
    stop()
```

---

## schedule - 定时任务

```python
schedule(schedule_func, date_rule, time_rule)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| schedule_func | function | 定时执行的函数 |
| date_rule | str | `n + d/w/m`，如 `'1d'`(每天)、`'1w'`(每周)、`'1m'`(每月) |
| time_rule | str | 执行时间 `HH:MM:SS`，**时分秒不可省略前导零**，如 `'09:40:00'` |

**注意**：`1w`、`1m` 仅回测可用；`time_rule` 不能写 `'9:40:0'` 这种格式。

```python
def init(context):
    schedule(schedule_func=algo_daily, date_rule='1d', time_rule='09:40:00')
    schedule(schedule_func=algo_monthly, date_rule='1m', time_rule='09:30:00')

def algo_daily(context):
    print('每天09:40执行', context.now)

def algo_monthly(context):
    print('每月第一个交易日09:30执行', context.now)
```

---

## timer / timer_stop - 毫秒级定时器

**仅实时/仿真模式可用，回测不生效。**

```python
# 设置定时器
result = timer(timer_func=my_func, period=60000, start_delay=0)
# result: {'timer_status': 0, 'timer_id': 1}

# 停止定时器
is_stopped = timer_stop(timer_id=result['timer_id'])
```

| 参数 | 类型 | 说明 |
|------|------|------|
| timer_func | function | 触发时执行的函数 |
| period | int | 间隔毫秒数，范围 [1, 43200000] |
| start_delay | int | 延迟启动毫秒数，范围 [0, 43200000] |

```python
def init(context):
    # 每60秒执行一次，立即启动
    context.timer_id = timer(timer_func=on_timer, period=60000, start_delay=0)

def on_timer(context):
    cash = context.account().cash
    print('定时检查资金:', cash['available'])
```

---

## log - 日志

**仅实时模式可用。**

```python
log(level='info', msg='信号触发', source='strategy')
```

| level | 说明 |
|-------|------|
| `'info'` | 信息级别 |
| `'warning'` | 警告级别 |
| `'error'` | 错误级别 |

---

## add_parameter - 动态参数

**仅实时模式可用，重启后重置。**

```python
add_parameter(key='k_value', value=23, min=0, max=100,
              name='K值阈值', intro='KDJ策略K值阈值',
              group='1', readonly=False)
```

- 在终端 UI 界面显示和实时修改参数
- 修改时触发 `on_parameter(context, parameter)` 事件

```python
def on_parameter(context, parameter):
    if parameter['name'] == 'K值阈值':
        context.k_value = parameter['value']
        print('参数已更新:', context.k_value)
```
