# MT5 指标快速参考指南

> 按指标名称或关键词即可加载，无需记忆参数。AI Agent 会自动选择最优参数。

---

## 📈 趋势指标 (Trend)

| 关键词 | 全名 | 最佳用途 | 触发关键词 |
|--------|------|----------|-----------|
| `MA` | Moving Average | 趋势方向判断 | MA, 均线, 移动平均 |
| `EMA` | Exponential MA | 短期趋势跟踪 | EMA, 指数均线 |
| `MACD` | Moving Avg Convergence Divergence | 趋势强弱、金叉死叉 | MACD |
| `ADX` | Average Directional Index | 趋势强度 | ADX, 趋势强度 |
| `SuperTrend` | SuperTrend | 简洁买卖信号 | SuperTrend, 超级趋势 |
| `Ichimoku` | Ichimoku Cloud | 全面趋势分析 | 云图, Ichimoku |
| `VWAP` | Volume Weighted Average Price | 机构基准价格 | VWAP, 成交量均价 |
| `Parabolic SAR` | Parabolic SAR | 反转点探测 | SAR, 抛物线 |

## 📊 动量指标 (Momentum)

| 关键词 | 全名 | 最佳用途 | 触发关键词 |
|--------|------|----------|-----------|
| `RSI` | Relative Strength Index | 超买超卖 | RSI, 相对强弱 |
| `Stochastic` | 随机指标 KD | 动量交叉 | KD, KDJ, 随机 |
| `CCI` | Commodity Channel Index | 周期趋势 | CCI |
| `Williams %R` | 威廉指标 | 反转信号 | WR, 威廉 |
| `AO` | Awesome Oscillator | 动量变化 | AO, 动量柱 |

## 📐 波动率指标 (Volatility)

| 关键词 | 全名 | 最佳用途 | 触发关键词 |
|--------|------|----------|-----------|
| `BOLL` | Bollinger Bands | 布林带收窄=突破 | 布林带, BOLL, BB |
| `ATR` | Average True Range | 止损止距计算 | ATR, 波动, 止损 |
| `Keltner` | Keltner Channel | 通道策略 | Keltner, 凯特纳 |
| `Donchian` | Donchian Channel | 海龟突破 | Donchian |

## 📦 成交量指标 (Volume)

| 关键词 | 全名 | 最佳用途 | 触发关键词 |
|--------|------|----------|-----------|
| `MFI` | Money Flow Index | 量价确认 | MFI, 量价 |
| `OBV` | On Balance Volume | 资金流向 | OBV, 累计量 |
| `Volume` | 成交量 | 基础量 | 成交量, volume |

## 🎯 模式识别 (Pattern)

| 关键词 | 全名 | 最佳用途 | 触发关键词 |
|--------|------|----------|-----------|
| `ZigZag` | ZigZag | 高低点识别 | 锯齿, 高低点 |
| `Fractal` | Fractals | 关键反转 | 分形 |
| `Alligator` | Alligator | 趋势跟踪 | 鳄鱼 |

---

## 🔥 常用组合策略

| 策略名 | 组合 | 适用场景 |
|--------|------|----------|
| **经典金叉** | MA(50) + MA(200) | 长期趋势 |
| **RSI + BOLL** | RSI + 布林带 | 震荡行情 |
| **MACD + ADX** | MACD + ADX | 趋势行情 |
| **海龟突破** | Donchian + ATR | 突破交易 |
| **机构跟庄** | VWAP + Volume | 机构跟随 |

---

*提示：只需说"加载 [关键词]"即可，AI Agent 会自动调参和分析。*
