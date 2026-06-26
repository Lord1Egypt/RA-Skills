---
name: polymarket-autopilot
version: 1.0.0
description: Automated paper trading on Polymarket using AI agents. Monitors trends, manages portfolio, and executes trades based on strategies.
author: sunnyhot
license: MIT
keywords:
  - polymarket
  - trading
  - ai-trading
  - automation
  - prediction-markets
---

# Polymarket AutoPilot - AI 预测市场自动交易

**使用 AI 智能体自动监控和交易 Polymarket 预测市场**

---

## ✨ 核心功能

### 🔍 **市场监控**
- ✅ 自动监控预测市场数据
- ✅ 追踪市场趋势变化
- ✅ 实时价格更新

### 📊 **数据分析**
- ✅ 技术指标分析
- ✅ 市场情绪分析
- ✅ 交易量分析

### 🤖 **自动交易**
- ✅ 策略自动执行
- ✅ 风险管理
- ✅ 止损/止盈设置

### 📈 **投资组合管理**
- ✅ 头寸跟踪
- ✅ 盈亏计算
- ✅ 绩效分析

### 💬 **Discord 通知**
- ✅ 交易信号提醒
- ✅ 每日报告
- ✅ 异常告警

---

## 🚀 使用方法

### **1. 自动监控模式**（推荐）

定时任务已配置，每天早上 8 点运行：

```bash
# 运行频率: 每天 8:00 AM
# 推送频道: Discord
# 报告类型: 市场分析和交易机会
```

---

### **2. 手动触发**

```bash
node /Users/xufan65/.openclaw/workspace/skills/polymarket-autopilot/scripts/autopilot.cjs
```

**功能**:
- 获取市场数据
- 分析趋势
- 生成报告
- 推送到 Discord

---

## 📋 报告格式

```
📊 Polymarket 每日报告

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

日期: 2026-03-14

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 如览

总头寸: 3
总价值: $1,234.56
盈亏: +$56.78 (+4.8%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 市场分析

交易量: 1,234,567
趋势: 上涨
情绪: 看涨

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 交易机会

1. BTC > $100,000 - 强烈看涨
2. ETH > $50,000 - 中性
3. SOL > $25,000 - 上涨

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ 风险提示

- 市场波动性增加
- 注意风险管理
```

---

## 🔧 配置文件

### `config/settings.json`

```json
{
  "polymarket": {
    "apiKey": "YOUR_POLYMARKET_API_KEY"
  },
  "discord": {
    "channel": "discord",
    "to": "channel:YOUR_DISCORD_CHANNEL_ID"
  },
  "trading": {
    "maxPositions": 10,
    "stopLoss": 0.05,
    "takeProfit": 0.10
  }
}
```

---

## 📝 更新日志

### v1.0.0 (2026-03-14)
- ✅ 初始版本
- ✅ 市场监控
- ✅ 数据分析
- ✅ Discord 报告

---

**🚀 让 AI 噶💰 为你自动交易 Polymarket！**
