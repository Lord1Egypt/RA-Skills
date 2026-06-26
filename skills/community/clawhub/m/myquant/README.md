# 掘金量化 GoldMiner Skill

[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)](https://www.myquant.cn)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-BossQuant-purple.svg)](https://clawhub.com)

掘金量化 Python SDK，事件驱动平台支持 A 股、期货、期权回测与实盘。

## ✨ 特性

- ⚡ **事件驱动** - on_bar / on_tick 标准事件驱动架构
- 🔄 **回测 + 实盘统一代码** - 一套代码同时支持回测与实盘
- 📊 **多品种支持** - A 股、期货、期权全品种覆盖
- 📈 **Level2 数据** - 支持 Level2 逐笔行情数据

## 📥 安装

```bash
pip install gm
```

## 🔑 配置

1. 访问 [掘金量化官网](https://www.myquant.cn) 注册账号
2. 获取 Token 并配置：

```bash
export GM_TOKEN="your_token_here"
```

## 🚀 快速开始

```python
from gm.api import *

# 设置 Token
set_token("your_token_here")

# 订阅行情
subscribe(symbols="SHSE.600000", frequency="1d")

def init(context):
    context.symbol = "SHSE.600000"

def on_bar(context, bars):
    # 获取最新价格
    price = bars[0].close
    # 买入
    order_volume(symbol=context.symbol, volume=100, side=OrderSide_Buy, order_type=OrderType_Market, position_effect=PositionEffect_Open)

if __name__ == '__main__':
    run(strategy_id="your_strategy_id", filename="main.py", mode=MODE_BACKTEST, token="your_token", backtest_start_time="2024-01-01", backtest_end_time="2024-12-31")
```

## 📊 支持的功能

| 类别 | 说明 | 示例接口 |
|------|------|----------|
| 行情订阅 | 订阅实时行情 | `subscribe()` |
| Bar事件 | K线回调 | `on_bar()` |
| Tick事件 | 逐笔回调 | `on_tick()` |
| 按量下单 | 指定数量下单 | `order_volume()` |
| 按比例下单 | 按资金比例 | `order_percent()` |
| 目标仓位 | 调整到目标 | `order_target_percent()` |
| 历史数据 | 查询历史行情 | `history()` / `history_n()` |
| 持仓查询 | 查询当前持仓 | `context.account().positions()` |

## 📖 回测示例

```python
from gm.api import *

def init(context):
    context.symbol = "SHSE.600000"
    subscribe(symbols=context.symbol, frequency="1d")

def on_bar(context, bars):
    # 获取历史数据计算均线
    hist = history_n(symbol=context.symbol, frequency="1d", count=20, fields="close")
    ma20 = hist['close'].mean()

    if bars[0].close > ma20:
        order_target_percent(symbol=context.symbol, percent=0.9, order_type=OrderType_Market, position_effect=PositionEffect_Open)
    else:
        order_target_percent(symbol=context.symbol, percent=0, order_type=OrderType_Market, position_effect=PositionEffect_Close)
```

## 📄 许可证

Apache License 2.0

## 📊 更新日志

### v1.3.0 (2026-03-23)
- 🎉 增加更丰富的AI Agent演示和高阶使用指南
- 🔄 更新版本号并清理失效链接


### v1.2.0 (2026-03-15)
- 🎉 初始版本发布
- 📊 支持掘金量化回测与实盘交易

---

## 🤝 社区与支持

- **维护者**：大佬量化 (Boss Quant)
- **主页**：https://www.myquant.cn
- **ClawHub**：https://clawhub.com
