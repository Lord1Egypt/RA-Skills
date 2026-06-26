---
name: Family Account Book / 家庭财务记账
description: 家庭财务记账系统，负责记录家庭收支、查看余额、月度统计等财务操作。当用户提到以下场景时使用此技能：(1) 记录消费、支出、收入 - 如"花了XX钱"、"今天吃了顿饭XX元"、"发了工资XX"；(2) 查看账户余额 - 如"账户还剩多少钱"、"余额多少"；(3) 财务统计 - 如"这个月花了多少"、"月度报表"、"本周支出"；(4) 账户转账 - 如"从A账户转B账户"、"转账XX元"；(5) 创建新账户或初始化账本；(6) 询问预算或财务规划。
---

# 家庭财务记账技能

## 快速开始

### 常用命令

```bash
# 快速记账
python3 /path/to/finances/scripts/finance_db.py --add 账本 账户 类型 金额 分类 描述

# 查看所有账户余额
python3 /path/to/finances/scripts/finance_db.py -b

# 月度统计报表
python3 /path/to/finances/scripts/finance_db.py -s [YYYY-MM]
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| 账本 | 账本名称 | default |
| 账户 | 账户名称或ID | 主账户 / B001 |
| 类型 | 收入/支出/转账 | 收入 / 支出 |
| 金额 | 数字金额 | 79.7 |
| 分类 | 消费分类 | 餐饮 / 工资 / 购物 |
| 描述 | 交易描述 | 肯德基 / 月薪 |

## 记账工作流

### 1. 记录消费
```
用户: "今天搓一顿肯德基，79块7"
操作: python3 .../finance_db.py --add default 主账户 支出 79.7 餐饮 肯德基
```

### 2. 记录收入
```
用户: "今天发工资了，15000"
操作: python3 .../finance_db.py --add default 主账户 收入 15000 工资 月薪
```

### 3. 查看余额
```
用户: "看一下所有账户"
操作: python3 .../finance_db.py -b
```

### 4. 月度统计
```
用户: "看一下这个月花了多少"
操作: python3 .../finance_db.py -s 2026-04
```

### 5. 转账操作
转账需要记录**两条**交易（一出一入）：

假设用户说"从主账户转1000到日常支出"：
```python
# 第一条：主账户支出100（转出）
python3 .../finance_db.py --add default 主账户 支出 1000 转账 转至日常支出

# 第二条：日常支出收入1000（转入）
python3 .../finance_db.py --add default 日常支出 收入 1000 转账 来自主账户
```

### 6. 近7日/特定周期查询
使用Python脚本查询：
```python
python3 -c "
import sqlite3, datetime
conn = sqlite3.connect('{WORKSPACE}/finances/db/finance.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()
week_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
cur.execute('''
    SELECT t.date, t.amount, t.category, t.description, a.name as account
    FROM transactions t
    JOIN accounts a ON t.account_id = a.id
    WHERE t.date >= ?
    ORDER BY t.date DESC
''', (week_ago,))
for r in cur.fetchall():
    print(f\"  {r['date']}  ¥{r['amount']:.2f}  [{r['category']}] {r['description']}\")
conn.close()
"
```

## 核心原则

1. **严禁编造数据**：金额必须由用户主动提供
2. **统一用ID记录**：账户用ID（如B001），不是名称
3. **转账记录两条**：内部流动需要一出一入两条记录
4. **统计排除转账**：月度报表自动排除转账分类
5. **负数余额是合法的**：部分账户（如投资账户）设计为跟踪盈亏，负数表示亏损

## 数据库信息

- **数据库路径**: `{WORKSPACE}/finances/db/finance.db`
- **详细Schema**: 参见 `references/finance.md`

## 账户ID速查

| ID | 账户名称 |
|----|----------|
| B001 | 主账户 |
| B002 | 储蓄账户 |
| B003 | 日常支出 |
| B004 | 梦想基金 |
| B005 | 医疗基金 |
| B006 | 零花钱 |
| B007 | 游戏账户 |
| B008 | 数字资产 |
| B009 | 备用账户 |
| B010 | 养老账户A |
| B011 | 养老账户B |
| B012 | 子女基金 |
| B013 | 二手平台 |
| B014 | 投资账户 |
