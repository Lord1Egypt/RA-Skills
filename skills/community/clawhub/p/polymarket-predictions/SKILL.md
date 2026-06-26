---
name: polymarket-monitor
description: Polymarket预测市场监控 - AI概率分析、赔率查询、价值发现。每次调用0.002 USDT。
version: 1.1.0
metadata:
  openclaw:
    requires:
      env:
        - SKILLPAY_API_KEY
        - GLM5_API_KEY (可选，用于AI分析)
---

# Polymarket Monitor v1.1

预测市场监控工具，支持：
- 热门市场赔率查询 ✅
- 关键词搜索市场 ✅
- AI概率分析 ✅（对比市场赔率，发现价值机会）
- 聪明钱追踪 🚧（开发中）

## 收费模式

每次调用 0.002 USDT（约0.014元人民币）

## 使用方法

```bash
# 查看热门市场
node scripts/monitor.js hot

# 搜索特定市场
node scripts/monitor.js market "关键词"

# AI概率分析（发现价值下注机会）
node scripts/monitor.js analyze "事件描述"

# 示例
node scripts/monitor.js analyze "比特币年底突破10万美元"
node scripts/monitor.js analyze "ETH突破3000美元"
node scripts/monitor.js analyze "特朗普当选"
```

## 功能说明

### 热门市场
- 实时获取Polymarket活跃市场
- 显示市场赔率（Yes/No概率）
- 直接跳转链接

### AI概率分析
- GLM-5分析事件发生概率
- 自动搜索相关市场赔率
- 对比AI概率 vs 市场赔率
- 发现价值下注机会（低估/高估）
- 给出BUY YES/BUY NO建议

### 收费方式
- BNB Chain USDT支付
- 最低充值 8 USDT
- 开发者获得95%收入

## SkillPay 配置

需要在环境变量中配置：
- `SKILLPAY_API_KEY` - 你的SkillPay API密钥
- `GLM5_API_KEY` - GLM-5 API密钥（可选，用于AI分析）
