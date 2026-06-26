# 快速开始 & 策略架构

## 策略三大结构

掘金量化策略主要有 3 种结构：

### 1. 定时任务型
```python
from gm.api import *

def init(context):
    schedule(schedule_func=algo, date_rule='1d', time_rule='14:50:00')

def algo(context):
    order_volume(symbol='SHSE.600000', volume=200, side=OrderSide_Buy,
                 order_type=OrderType_Market, position_effect=PositionEffect_Open, price=0)

if __name__ == '__main__':
    run(strategy_id='YOUR_ID', filename='main.py', mode=MODE_BACKTEST,
        token='YOUR_TOKEN', backtest_start_time='2024-01-01 09:00:00',
        backtest_end_time='2024-06-30 15:30:00', backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=1000000, backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001)
```

### 2. 数据事件驱动型
```python
from gm.api import *

def init(context):
    subscribe(symbols='SHSE.600000', frequency='60s')

def on_bar(context, bars):
    print(bars)
```

### 3. 时间序列滑窗型
```python
from gm.api import *

def init(context):
    subscribe(symbols='SHSE.600000', frequency='60s', count=50,
              format='df', fields='symbol,close,eob')

def on_bar(context, bars):
    data = context.data(symbol=bars[0]['symbol'], frequency='60s', count=50)
    data['ma5'] = data['close'].rolling(5).mean()
    print(data.tail())
```

## 纯数据研究（无需 run）

```python
from gm.api import *
set_token('YOUR_TOKEN')  # 掘金终端需保持打开

data = history(symbol='SHSE.600000', frequency='1d',
               start_time='2024-01-01 09:00:00', end_time='2024-12-31 16:00:00',
               fields='open,high,low,close,eob', adjust=ADJUST_PREV, df=True)
print(data)
```

## 模式说明

| 模式 | 常量 | 说明 |
|------|------|------|
| 实时模式 | `MODE_LIVE = 1` | 仿真/实盘交易，接收实时行情 |
| 回测模式 | `MODE_BACKTEST = 2` | 历史数据回放，快速验证策略 |

## 运行参数 `run()` 全解

| 参数 | 类型 | 说明 |
|------|------|------|
| strategy_id | str | 掘金终端生成的策略 ID |
| filename | str | 策略文件名（如 `main.py`） |
| mode | int | MODE_LIVE 或 MODE_BACKTEST |
| token | str | 用户 token（终端系统设置-密钥管理） |
| backtest_start_time | str | 回测开始时间 `%Y-%m-%d %H:%M:%S` |
| backtest_end_time | str | 回测结束时间 `%Y-%m-%d %H:%M:%S` |
| backtest_initial_cash | float | 初始资金，默认 1000000 |
| backtest_transaction_ratio | float | 成交比例，默认 1.0 |
| backtest_commission_ratio | float | 佣金比例，默认 0 |
| backtest_slippage_ratio | float | 滑点比例，默认 0 |
| backtest_adjust | int | 复权方式：ADJUST_NONE/ADJUST_PREV/ADJUST_POST |
| backtest_match_mode | int | 0=延时撮合(下一bar开盘价)，1=实时撮合(当前收盘价) |
| backtest_check_cache | int | 是否用缓存，默认 1 |
| serv_addr | str | 终端地址，默认本地，可指定 `ip:port` |

## 注意事项
- filename 必须与实际文件名一致
- 前复权/后复权回测不处理分红送转事件（已通过复权因子调整）
- 不复权模式会自动处理分红送转
