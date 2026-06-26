---
name: pocket-money-manager
slug: pocket-money-manager
version: 1.0.0
description: 理财小助手，收支记录、消费分析、预算提醒。
homepage: https://github.com/786793119/miya-skills
metadata: {"openclaw":{"emoji":"💰","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

# 理财小助手 (Pocket Money Manager)

你的私人记账管家。

## 功能

- 记收入（工资/奖金/兼职/理财/红包）
- 记支出（餐饮/交通/购物/住房/娱乐/医疗/教育）
- 查看余额和收支统计
- 周消费报告
- 设置月预算
- 超支预警提醒

## 使用示例

```bash
# 记收入
python pocket-money-manager.py add_income 5000 工资

# 记支出
python pocket-money-manager.py add_expense 35 餐饮

# 查看余额
python pocket-money-manager.py get_balance

# 周报告
python pocket-money-manager.py get_weekly_report

# 设置预算
python pocket-money-manager.py set_budget 3000
```

## 数据存储

- 收支记录: `~/.memory/finance/records.json`
- 预算设置: `~/.memory/finance/budget.json`

---

*By Miya - 2026*
