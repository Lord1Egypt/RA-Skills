---
name: expense-tracker
description: Personal expense tracker - record expenses, auto-categorize, monthly statistics with total and category breakdown
version: v1.0.0
tags: expense-tracking, personal-finance, budget-management, auto-categorization
---

# Expense Tracker

Simple personal expense tracking assistant.

## Usage Scenarios

### Scenario 1: Record a Daily Expense
**User input:** "记录早餐花了10元。"

**Expected output:** Entry saved successfully - 早餐 | ¥10.00 | food | 2026-06-19 09:54. Category auto-detected as food. Running today total shown.

### Scenario 2: Get Monthly Statistics
**User input:** "这个月花了多少钱？"

**Expected output:** Monthly statistics: total ¥3,250.50, breakdown by category - food ¥1,200 (37%), transport ¥450 (14%), shopping ¥800 (25%), others ¥800.50 (24%). Average daily spend ¥108.35.

### Scenario 3: Check Category Breakdown
**User input:** "查看本周食品类支出了多少。"

**Expected output:** Food category breakdown this week: Mon ¥35, Tue ¥42.50, Wed ¥28, Thu ¥55, Fri ¥30, Sat ¥0, Sun ¥0. Weekly food total ¥190.50.
### Scenario 4: 花呗账单吓到我了
**User input:** "看了下这个月花呗要还5800，但我想不起来钱花哪了，帮我做个月度开支分析。"
**Expected output:** 分析花呗账单的支出类别分布（餐饮/交通/购物/娱乐等大类），找出最大支出项和非必要支出。对比过去3个月的消费趋势，给出优化建议：设置支付宝每月支出上限、关闭免密支付、为'大件消费'设立24小时等待期。推荐使用随手记/挖财App做详细记账，并设定每月储蓄目标。

## Features
- Record expense with amount and note
- Auto-categorize (food/transport/shopping/others)
- Monthly statistics (total + category breakdown)

## Constraints
- ❌ No budget alerts
- ❌ No bank payment integration
- ❌ No cross-device sync

## Usage
```bash
python3 scripts/expense-tracker.py add "早餐" 10
python3 scripts/expense-tracker.py stats
```
