---
name: Passive Income Tracker
slug: passive-income-tracker-xiaomolongxia
version: 1.0.0
description: "追踪多个被动收入来源，包括订阅收入、广告分成、技能销售佣金等。支持Webhook接入ClawHub统计。"
changelog: "1.0.0 - 初始版本"
metadata: {"openclaw":{"emoji":"💰","os":["win32","darwin","linux"]}}
---

# Passive Income Tracker 💰

追踪你的多个被动收入来源，统一管理收益统计。

## 功能

- 📊 **收入仪表盘**：一眼看清所有收入来源
- 💵 **订阅收入**：ClawHub技能订阅收入
- 📢 **广告分成**：平台广告收入追踪
- 🎯 **技能佣金**：推广分成收入
- 📈 **月度对比**：收入趋势分析

## 输入

- 收入类型（subscription/ad/referral）
- 金额
- 日期范围
- 数据源Webhook（可选）

## 输出

```json
{
  "total_monthly": 1250.00,
  "sources": [
    {"name": "ClawHub Skills", "monthly": 147.00, "installs": 5},
    {"name": "Ad Revenue", "monthly": 50.00},
    {"name": "Referral", "monthly": 30.00}
  ],
  "trend": "+12% vs last month"
}
```

## 使用场景

- 订阅收入监控
- 多平台收入汇总
- 被动收入目标追踪

## 配置

```json
{
  "webhookUrl": "https://your-stats-webhook.com",
  "currency": "CNY",
  "updateInterval": "daily"
}
```

## 价格

¥39/月