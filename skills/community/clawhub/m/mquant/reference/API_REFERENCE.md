# API 速查手册

## Market Data 行情数据

### subscribe - 订阅行情
```python
subscribe(symbol, MarketDataType.XXX)
```

| 数据类型 | 说明 | 回调函数 |
|---------|------|---------|
| `MarketDataType.TICK` | Tick 行情 | `handle_tick(context, tick, msg_type)` |
| `MarketDataType.KLINE_1M` | 1 分钟 K 线 ✅ 最常用 | `handle_data(context, kline_data)` |
| `MarketDataType.RECORD_ORDER` | 逐笔委托 | - |
| `MarketDataType.RECORD_TRANSACTION` | 逐笔成交 | - |

⚠️ **重要**：不支持日线订阅，需用 `KLINE_1M` 累积数据

### get_kline_data - 查询历史 K 线
```python
get_kline_data(symbol, count, period)
```

---

## Trading 交易

### order - 下单
```python
order(symbol, amount, style=None)
```
- `amount > 0`：买入
- `amount < 0`：卖出

### cancel_order - 撤单
```python
cancel_order(order_id)
```

### get_open_orders - 查询未完成订单
```python
get_open_orders()
```

---

## Query 查询

### get_positions - 查询持仓
```python
positions = get_positions()  # 返回 dict<symbol, Position>

# 正确用法1：使用 get() 从字典获取
pos = positions.get('000001.SZ')
amount = pos.amount if pos else 0

# 正确用法2：遍历字典的值
for symbol, pos in positions.items():
    if symbol == g_security:
        amount = pos.amount
```

⚠️ **重要**：返回的是字典，不是列表！

如需列表，使用 `get_positions_ex()` 返回 `list<Position>`

### get_fund_info - 查询资金
```python
fund_info = get_fund_info()
```

---

## 常用结构体字段

### Tick
| 字段 | 说明 |
|------|------|
| `tick.code` | 股票代码 |
| `tick.current` | 当前价格 |
| `tick.open` | 开盘价 |
| `tick.high` | 最高价 |
| `tick.low` | 最低价 |

### Position
| 字段 | 说明 |
|------|------|
| `pos.symbol` | 股票代码 |
| `pos.amount` | 持仓数量 |

### KLineDataPush
| 字段 | 说明 |
|------|------|
| `kline.close` | 收盘价 |
| `kline.high` | 最高价 |
| `kline.low` | 最低价 |
| `kline.open` | 开盘价 |
| `kline.volume` | 成交量 |

---

## 常见错误 ❌

### API 核对清单

| API | 正确用法 | 常见错误 |
|-----|----------|----------|
| `subscribe` | `subscribe(security, MarketDataType.XXX)` | 使用字符串 `'1d'` ❌ |
| `handle_tick` | `handle_tick(context, tick, msg_type)` | 参数顺序错误 ❌ |
| `handle_data` | `handle_data(context, kline_data)` | 参数名错误 ❌ |
| `order` | `order(symbol, amount)` | 参数类型错误 ❌ |
| `get_positions` | `get_positions()` 返回字典 | 当列表遍历 ❌ |

### subscribe() 常见错误

**❌ 错误：使用字符串订阅日线**
```python
subscribe(symbol, '1d')  # 不支持！
```

**✅ 正确：使用 MarketDataType 订阅分钟 K 线**
```python
subscribe(symbol, MarketDataType.KLINE_1M)  # 然后在代码中累积日线数据
```

**说明**：`subscribe()` 只支持 Tick 和分钟 K 线，**不支持日线订阅**。策略需使用 `KLINE_1M` 订阅 1 分钟 K 线，在代码中累积数据实现日线逻辑。

### get_positions() 常见错误

**❌ 错误用法：**
```python
positions = get_positions()
for pos in positions:  # 这样遍历得到的是 symbol 字符串
    if pos.symbol == g_security:  # 'str' object has no attribute 'symbol'
        ...
```

**✅ 正确用法：**
```python
# 方法1: 使用 get() 从字典获取
positions = get_positions()
pos = positions.get(g_security)
amount = pos.amount if pos else 0

# 方法2: 遍历字典的值
positions = get_positions()
for symbol, pos in positions.items():
    if symbol == g_security:
        amount = pos.amount
```

### 结构体字段常见错误

| 结构体 | 正确字段 | 常见错误 |
|--------|----------|----------|
| Tick | `tick.code`, `tick.current` | `tick.last` ❌ |
| Position | `pos.symbol`, `pos.amount` | `pos.code` ❌ |

---

## 完整示例

```python
from mquant_api import *
from mquant_struct import *

def initialize(context):
    # 订阅 1 分钟 K 线
    subscribe('000001.SZ', MarketDataType.KLINE_1M)

def handle_data(context, kline_data):
    # 获取当前价格
    price = kline_data.close
    
    # 查询持仓
    positions = get_positions()
    pos = positions.get('000001.SZ')
    current_amount = pos.amount if pos else 0
    
    # 交易逻辑：没有持仓就买入
    if current_amount == 0:
        order('000001.SZ', 100)  # 买入 100 股
        write_log('INFO', f'买入 100 股，价格 {price}')
```
