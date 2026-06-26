# Marcus 投资分析技能

**版本**: 6.0.0  
**作者**: Marcus AI Agent  
**许可**: MIT

---

## 📖 简介

Marcus 投资分析技能是一个基于缠论+MACD+RSI 的 A 股投资策略工具。提供股票分析、策略回测、投资建议等功能。

**核心策略**: 缠论中枢 + MACD 金叉 + RSI 超卖 + 追踪止损

---

## ✨ 功能特性

- 📊 **股票分析**: 缠论中枢、背驰检测、买卖点识别
- 📈 **策略回测**: 历史数据验证，夏普比率、胜率分析
- 💡 **投资建议**: 行业配置、个股推荐、仓位管理
- 📉 **指标下载**: 自动下载 MACD、RSI、KDJ 指标数据

---

## 🚀 使用方式

### 作为 OpenClaw 技能调用

```
"分析一下江波龙"
"回测 Marcus 策略"
"有什么投资建议？"
```

### 直接运行脚本

```bash
# 策略回测
python3 scripts/marcus_ultimate_optimized_strategy.py

# 个股分析
python3 scripts/marcus_chan_theory.py 301308
```

---

## 📊 回测表现 (2023-2026)

| 指标 | 数值 |
|------|------|
| 年化收益 | 21.96% |
| 夏普比率 | 0.56 |
| 胜率 | 75.0% |

---

## ⚠️ 风险提示

- 历史业绩不代表未来
- 投资有风险，需谨慎
- 建议分散配置

---

## 📁 文件结构

```
marcus-investment-analyst/
├── SKILL.md
├── LICENSE
├── README.md
├── scripts/
│   ├── marcus_ultimate_optimized_strategy.py
│   ├── marcus_chan_theory.py
│   ├── marcus_backtest_chan.py
│   └── data_indicator_fetcher.py
├── references/
│   ├── strategy.md
│   └── optimization_report.md
└── assets/
    └── backtest_data.json
```

---

## 📞 支持

问题反馈：请通过 OpenClaw 社区反馈

---

**最后更新**: 2026-03-12
