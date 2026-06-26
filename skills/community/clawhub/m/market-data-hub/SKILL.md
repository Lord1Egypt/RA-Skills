# Market Data Hub - 股票行情数据获取技能

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

一个功能强大的股票行情数据获取技能，支持多数据源、自动限流、故障切换和技术指标计算。

## 功能特性

- **多数据源支持**
  - 腾讯财经：实时行情，速度快
  - AKShare：A股完整数据，功能全面
  - Baostock：高质量历史数据，复权因子

- **智能限流与重试**
  - 漏斗桶（Token Bucket）限流算法
  - 指数退避重试策略
  - 熔断器保护机制

- **自动故障切换**
  - 主数据源失败自动切换备用源
  - 可配置的优先级策略

- **丰富的技术指标**
  - 移动平均线（MA/EMA/WMA）
  - MACD指标
  - RSI相对强弱指标
  - 布林带（Bollinger Bands）
  - KDJ随机指标

## 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖：
- `akshare>=1.10.0` - AKShare数据接口
- `baostock>=0.8.8` - Baostock数据接口
- `pandas>=1.5.0` - 数据处理
- `requests>=2.28.0` - HTTP请求

## 快速开始

```python
from src import MarketDataHub

# 创建实例
hub = MarketDataHub()

# 获取实时行情
quote = hub.get_realtime_quote('300502')  # 新易盛
print(f"当前价格: {quote['price']}")
print(f"涨跌幅: {quote['change_pct']}%")

# 获取K线数据
df = hub.get_kline('300502', period='day', start_date='2024-01-01')
print(df.head())
```

## API文档

### MarketDataHub

#### 初始化参数

```python
hub = MarketDataHub(
    rate_limits=None,           # 自定义限流配置
    source_priority=None,       # 数据源优先级
    enable_rate_limit=True,     # 是否启用限流
    enable_retry=True,          # 是否启用重试
    enable_circuit_breaker=True # 是否启用熔断器
)
```

#### 获取实时行情

```python
quote = hub.get_realtime_quote(
    symbol='300502',    # 股票代码
    source='auto'       # 数据源：'auto', 'tencent', 'akshare', 'baostock'
)
```

返回数据示例：
```json
{
    "symbol": "300502",
    "name": "新易盛",
    "price": 125.80,
    "change": 5.20,
    "change_pct": 4.31,
    "volume": 15234500,
    "amount": 1914829000,
    "open": 120.50,
    "high": 128.00,
    "low": 119.80,
    "pre_close": 120.60,
    "timestamp": "2024-01-15T10:30:00",
    "source": "tencent"
}
```

#### 获取K线数据

```python
df = hub.get_kline(
    symbol='300502',
    period='day',           # 周期：'day', 'week', 'month'
    start_date='2024-01-01',
    end_date='2024-03-01',
    source='auto'
)
```

#### 批量获取行情

```python
quotes = hub.get_batch_quotes(
    symbols=['300502', '600519', '000858'],
    source='tencent'
)
```

#### 获取资金流向

```python
flow = hub.get_capital_flow('300502')
print(f"主力净流入: {flow['main_inflow']}")
print(f"散户净流入: {flow['retail_inflow']}")
```

#### 获取龙虎榜

```python
df = hub.get_lhb_data(trade_date='2024-01-15')
```

### 技术指标计算

#### 移动平均线

```python
# 计算MA5, MA10, MA20, MA60
df = hub.calculate_ma(df, periods=[5, 10, 20, 60])

# 计算EMA
df = hub.calculate_ma(df, periods=[12, 26], ma_type='ema')

# 计算WMA
df = hub.calculate_ma(df, periods=[10], ma_type='wma')
```

#### MACD

```python
df = hub.calculate_macd(
    df,
    fast_period=12,
    slow_period=26,
    signal_period=9
)
# 输出列: MACD_DIF, MACD_DEA, MACD_HIST, MACD_golden_cross, MACD_death_cross
```

#### RSI

```python
df = hub.calculate_rsi(df, period=14)
# 输出列: RSI, RSI_oversold, RSI_overbought
```

#### 布林带

```python
df = hub.calculate_bollinger_bands(
    df,
    period=20,
    std_multiplier=2.0
)
# 输出列: BB_MIDDLE, BB_UPPER, BB_LOWER, BB_WIDTH, BB_percent_b
```

#### KDJ

```python
df = hub.calculate_kdj(df, n_period=9)
# 输出列: KDJ_K, KDJ_D, KDJ_J, KDJ_golden_cross, KDJ_death_cross
```

#### 计算所有指标

```python
df = hub.get_all_indicators(df)
# 包含所有上述指标
```

## 限流配置

默认限流配置：

```python
rate_limits = {
    'akshare': {'rate': 0.5, 'capacity': 10},   # 每2秒1次，突发10次
    'tencent': {'rate': 2.0, 'capacity': 20},   # 每秒2次，突发20次
    'baostock': {'rate': 1.0, 'capacity': 10}   # 每秒1次，突发10次
}

hub = MarketDataHub(rate_limits=rate_limits)
```

## 数据源优先级

默认优先级：`['baostock', 'tencent', 'akshare']`

- **Baostock**: 数据质量高，历史数据完整，优先使用
- **腾讯**: 实时性好，适合获取最新行情
- **AKShare**: 功能全面，作为备选

```python
# 使用默认优先级
hub = MarketDataHub()

# 或自定义优先级
hub = MarketDataHub(
    source_priority=['baostock', 'tencent', 'akshare']
)

# 自动模式下按优先级尝试
quote = hub.get_realtime_quote('300502', source='auto')
```

## 使用统计

```python
stats = hub.get_usage_stats()
print(f"腾讯请求次数: {stats['requests']['tencent']}")
print(f"失败次数: {stats['failures']['tencent']}")
```

## 测试运行

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试
python tests/test_market_data_hub.py
python tests/test_strategies.py
python tests/test_limiter.py
python tests/test_indicators.py
```

## 文件结构

```
market-data-hub/
├── SKILL.md                    # 本文件
├── requirements.txt            # 依赖包
├── example.py                  # 示例脚本
├── src/
│   ├── __init__.py
│   ├── market_data_hub.py      # 主入口类
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── base_strategy.py    # 策略基类
│   │   ├── akshare_strategy.py
│   │   ├── tencent_strategy.py
│   │   └── baostock_strategy.py
│   ├── limiter/
│   │   ├── __init__.py
│   │   └── token_bucket.py     # 漏斗桶限流
│   ├── retry/
│   │   ├── __init__.py
│   │   └── retry_strategy.py   # 重试策略
│   └── indicators/
│       ├── __init__.py
│       ├── moving_average.py
│       ├── macd.py
│       ├── rsi.py
│       ├── bollinger.py
│       └── kdj.py
└── tests/
    ├── test_market_data_hub.py
    ├── test_strategies.py
    ├── test_limiter.py
    └── test_indicators.py
```

## 注意事项

1. **数据源可用性**
   - AKShare需要安装 `pip install akshare`
   - Baostock需要安装 `pip install baostock`
   - 腾讯接口无需额外依赖

2. **网络限制**
   - 部分数据源可能有IP频率限制
   - 建议启用限流功能

3. **数据质量**
   - 历史数据：Baostock > AKShare
   - 实时行情：腾讯 > AKShare
   - 资金流向：仅AKShare支持

4. **默认优先级**
   - Baostock（数据质量高）> 腾讯（实时性好）> AKShare（备选）

4. **股票代码格式**
   - 支持纯数字代码：`'300502'`
   - 自动识别交易所
   - 支持带前缀：`'sz300502'`, `'sh600519'`

## 许可证

MIT License
