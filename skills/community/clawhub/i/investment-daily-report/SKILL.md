---
name: investment-daily-report
description: |
  每日投研日报自动生成器。当用户需要生成每日金融市场投资研究报告、投研日报、市场复盘、行情总结时使用此 Skill。
  覆盖 A 股、港股、美股三大市场，自动采集行情、资金流向、板块轮动、重要公告、技术面分析等维度，
  生成结构化 Markdown 日报，适合个人投资者、投资小组日常使用。
metadata: {"openclaw": {"emoji": "📊"}}
---

# 投研日报生成器 — Investment Daily Report Generator

> **一句话概述**：一键生成覆盖 A 股、港股、美股的每日投研日报，结构化 Markdown 输出。

## 功能概述

自动采集多维度金融数据，生成专业级投研日报：

| 维度 | 内容 |
|------|------|
| **大盘概览** | 上证/深证/创业板/恒生/纳斯达克/标普500 收盘数据 |
| **板块轮动** | 涨跌幅 Top5 板块 + 龙头股 |
| **个股异动** | 涨停/跌停/振幅 Top5 |
| **资金流向** | 北向资金、主力资金净流入/流出 Top10 |
| **重要公告** | 重大事项、业绩预告、增减持 |
| **技术面信号** | 主要指数 MACD/KDJ/均线支撑压力位 |
| **隔夜外盘** | 美股收盘、欧股、大宗商品、汇率 |
| **明日展望** | 关键事件日历 + 市场情绪判断 |

## 使用方式

```bash
# 生成完整日报（默认 A 股 + 港股 + 美股）
node scripts/generate_report.cjs

# 仅 A 股
node scripts/generate_report.cjs --market cn

# 仅美股
node scripts/generate_report.cjs --market us

# 指定输出路径
node scripts/generate_report.cjs --output ./reports/2026-04-20.md

# 快速模式（仅大盘 + 板块 + 个股异动）
node scripts/generate_report.cjs --quick
```

## 数据源

1. **NeoData Financial Search** — 股票行情、资金流向、板块数据、研报
2. **在线搜索** — 重要公告、重大事件、政策解读
3. **Trade Arena** — 持仓盈亏跟踪（如已配置）

## 输出格式

Markdown 日报文件，包含：

```markdown
# 投研日报 | 2026-04-20

## 📈 大盘概览
| 指数 | 收盘 | 涨跌幅 | 成交额 |
|------|------|--------|--------|

## 🔥 板块轮动
### 涨幅 Top5 | 跌幅 Top5
...

## 📊 资金流向
### 北向资金 | 主力净流入 Top10
...

## 🚨 重要公告
...

## 📉 技术面信号
...

## 🌍 隔夜外盘
...

## 🔮 明日展望
...
```

## 目录结构

```
investment-daily-report/
├── SKILL.md              # 本文件
├── README.md             # 使用说明
├── CHANGELOG.md          # 变更日志
└── scripts/
    └── generate_report.cjs  # 主脚本（Node.js，零依赖）
```

## 环境要求

- Node.js ≥ 18（已内置）
- 网络连接（调用 NeoData API + 在线搜索）
- 无需额外 npm 依赖

## 注意事项

1. 盘中生成的数据为实时快照，收盘后数据更完整
2. 资金流向数据基于 NeoData 实时接口，可能存在延迟
3. 技术面信号仅供参考，不构成投资建议
4. 日报内容基于公开市场数据，不包含任何内幕信息
