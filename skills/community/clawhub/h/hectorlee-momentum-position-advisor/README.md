# hectorlee-momentum-position-advisor 动量持仓顾问

![Version](https://img.shields.io/badge/version-1.3.8-blue) ![License](https://img.shields.io/badge/license-MIT--0-green) ![Python](https://img.shields.io/badge/python-3.10%2B-yellow)

纯量价动量持仓评估系统，回答一个核心问题：**「从量价动量角度看，这只股票现在该持有、减仓还是卖出？」**

输出 HOLD / WATCH / REDUCE / SELL 四级决策 + 108 分制多维评分 + 减仓比例建议。设计理念是**默认不轻易卖**——持有类形态覆盖拉升途中的各种调整，只有出现明确的衰竭/破位证据才发出减仓/卖出信号，并通过决策滞回机制防震荡误杀。

三段式量化流水线的第三层：

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  VPS 量价初筛        │     │  DPP 每日精选        │     │  MPA 持仓管理        │
│  全A ~5,200 → ~159  │ ──▶ │  4层漏斗 → 1-3 只    │ ──▶ │  HOLD/WATCH/        │
│  （姊妹仓库）        │     │  （姊妹仓库）        │     │  REDUCE/SELL        │
│                     │     │                     │     │  （本仓库）          │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

- 上游初筛：[hectorlee-volume-price-screener](https://github.com/xiyanjun/hectorlee-volume-price-screener)
- 每日精选：[hectorlee-daily-precision-picker](https://github.com/xiyanjun/hectorlee-daily-precision-picker)

## 形态体系（8 持有 + 6 预警 + 4 卖出 + 4 加仓 + 3 反弹）

| 类别 | 数量 | 代表形态 |
|:-----|:----:|:-----|
| 🟢 持有 | 8 + M0兜底 | M1 底部启动加速、M2 均线多头发散、M4 缩量回踩支撑、M12 V形反转、M13 双底反转 |
| 🟡 预警 | 5 + 1前置 | M7 高位搏杀、W1 涨幅过热、W2 乖离过大、Pre-M11 预破位预警（提前1-3天） |
| 🔴 卖出 | 4 | M8 高开诱多、M9 缩量连阴、M10 峰值回撤、M11 趋势破位 |
| 🟢 加仓 | 4 | B1 反包阳线、B2 回踩确认、B3 整理突破、B4 缩尽首阳（需 VP 共振确认） |
| 🎲 反弹博弈 | 3 | R1 恐慌抛售反弹、R2 缩量衰竭反弹、R3 超跌均值回归（仅卖出区间触发，严格止损） |

## 评分体系（108 分制）

| 维度 | 分值 |
|:-----|:--:|
| 趋势强度（MA 结构） | 25 |
| 量能健康度 | 20 |
| 衰竭信号 | 25 |
| 均线支撑 | 15 |
| 形态匹配 | 15 |
| 加仓信号 | +10 |
| 量价共振（与 VPS 形态融合） | -10~+12 |
| 持仓成本 | ±8 |
| 资金流向 | +8 |

决策引擎综合分数、反弹形态、MA 结构、信号覆盖、底部反弹判定、**决策滞回**（防震荡来回打脸）和市场自适应（牛市/熊市阈值动态调整）输出最终评级，附减仓比例建议。

## 快速开始

```bash
git clone https://github.com/xiyanjun/hectorlee-momentum-position-advisor.git
cd hectorlee-momentum-position-advisor
pip install requests

# 准备持仓文件（参考 data/positions.example.json）
cp data/positions.example.json data/positions.json

cd scripts

# 单股诊断（五维评分明细）
python advisor.py 600406 --detail

# 单股带成本价
python advisor.py 688981 --cost 55.0

# 持仓组合批量诊断
python advisor.py --portfolio --file ../data/positions.json

# 全市场动量扫描 Top20
python advisor.py --scan --top 20

# 搜索股票名称
python advisor.py --search 中芯国际
```

`portfolio.py` / `sector_resonance.py` / `momentum_detect.py` 等为 `advisor.py` 调用的内部模块。本仓库同时也是 WorkBuddy / Claude Code 的 Agent Skill（见 [SKILL.md](SKILL.md)），可由 AI 助手按其中的工作流自动执行持仓诊断。

## 免责声明

本项目仅供技术研究和学习交流，所有信号基于历史量价数据的统计规律，**不构成任何投资建议**。股市有风险，入市需谨慎。

## License

[MIT-0](LICENSE)
