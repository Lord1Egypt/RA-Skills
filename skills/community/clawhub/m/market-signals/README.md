# 📈 Market Signals

## 快速开始
```bash
# 查看帮助
python3 scripts/market_signals.py --help

# 单股票分析
python3 scripts/market_signals.py --file stock.csv --price-col close

# 多股票扫描
python3 scripts/market_signals.py --file portfolio.csv --scan

# 信号历史
python3 scripts/market_signals.py --file stock.csv --history

# ASCII价格图
python3 scripts/market_signals.py --file stock.csv --chart
```

## 功能
技术信号扫描器 v1.1.0。从价格数据计算 RSI、均线(5/10/20)、成交量异动、ATR波动率、MACD、布林带(±2σ)、VWAP。支持多股票一键扫描、信号历史追踪、支撑/阻力位识别、综合评分(0-100)。

## 许可证
MIT

## 作者
ChengQian (成乾)
