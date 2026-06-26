---
name: polymarket-BTC预测自动交易机器人
description: "Polymarket BTC 5分钟 Up/Down 全自动交易机器人。MiniMax AI 驱动，双信号决策，自动止盈止损，真实链上交易，Web控制面板。"
metadata:
  author: "Dobby (多比)"
  version: "2.0.0"
  difficulty: "intermediate"
  tags: ["polymarket", "trading", "bot", "btc", "prediction-market", "ai-trading"]
---

# Polymarket BTC 5m Trading Bot

Polymarket BTC 5分钟 Up/Down 全自动交易机器人。

## 核心功能

| 功能 | 说明 |
|------|------|
| 🤖 AI 决策 | 支持 MiniMax / OpenAI / SiliconFlow 等任意 OpenAI-compatible API |
| 📊 双信号系统 | AI 分析 + 价差套利，取交集才交易 |
| 💻 Web 控制面板 | 实时状态、持仓、胜率、AI 思考记录 |
| 🛡️ 风险保护 | 止盈止损、点差保护、深度保护 |
| 📡 外部信号 | 支持 Simmer 信号引擎接入 |
| ⏰ 高频策略 | 3分钟 K 线动量策略 |

## 快速开始

```bash
cd polymarket-btc-bot

# 1. 安装依赖
bash scripts/install.sh

# 2. 配置（必填）
cp references/.env.example .env
nano .env

# 3. 启动 Bot
bash scripts/bot_start.sh

# 4. 启动控制面板
bash scripts/panel_start.sh
# 访问 http://localhost:18095
```

## 目录结构

```
polymarket-btc-bot/
├── SKILL.md
├── README.md
├── bot.py
├── status_server.py
├── scripts/
│   ├── install.sh
│   ├── bot_start.sh
│   └── panel_start.sh
├── references/
│   ├── .env.example
│   └── STRATEGY.md
└── assets/public/
```

## AI 厂商配置

```bash
# MiniMax（推荐国内用户）
AI_PROVIDER=minimax
AI_BASE_URL=https://api.minimax.chat/v1
AI_API_KEY=your_key_here
AI_MODEL=MiniMax-M2.7

# OpenAI
AI_PROVIDER=openai
AI_BASE_URL=https://api.openai.com/v1
AI_API_KEY=your_key_here
AI_MODEL=gpt-4o-mini

# SiliconFlow（免费额度）
AI_PROVIDER=siliconflow
AI_BASE_URL=https://api.siliconflow.cn/v1
AI_API_KEY=your_key_here
AI_MODEL=deepseek-ai/DeepSeek-V3
```

## 策略说明

Bot 同时运行两套信号，必须两者都同意才开仓：

**信号1：AI 决策**
- BTC 当前价格、24h 高低点、日内变化
- 15 分钟 K 线形态（趋势/震荡）
- 3 分钟成交量变化
- 当前持仓状态和浮盈
- 输出：BUY_UP / BUY_DOWN / HOLD

**信号2：价差套利**
```
BTC_5m_change = (BTC当前 - BTC_5min前) / BTC_5min前
signal = BTC_5m_change * 10
price_gap = PM_UP_price - 0.5
divergence = signal - price_gap
```
- divergence > 0.003 → 买入 UP
- divergence < -0.003 → 买入 DOWN

**HOLD 条件**（不开仓）
- AI 信号 = HOLD
- 策略信号无明显偏离
- 当前已有持仓
- 剩余时间 < 3 分钟
- 点差 > 6%

## 高级参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `AI_ENABLED` | true | 是否启用 AI 决策 |
| `HF_ENABLED` | true | 是否启用高频策略 |
| `KELLY_FRACTION` | 0.25 | Kelly 系数 |

详见 `references/STRATEGY.md`。

## 常用命令

```bash
# 查看 Bot 进程
ps aux | grep bot.py | grep -v grep

# 实时日志
tail -f bot.log

# 重启 Bot
pkill -f "bot.py"
bash scripts/bot_start.sh

# 查看面板
curl http://localhost:18095/
```

## 已知限制

- **BTC 5m 市场**：每 5 分钟过期，Bot 自动查找当前窗口
- **建议**：搭配 Simmer 信号引擎使用效果更佳
