---
name: lyuuo-book
description: >
  Personal bookkeeping tool — record income, expenses, transfers, manage accounts
  and categories, track budgets, and generate financial reports via local CLI commands
  backed by SQLite. Use this skill whenever the user wants to: record a purchase or
  payment ("午餐花了50", "买了个东西", "打车280"), log income ("发工资了", "收到退款"),
  record transfers between accounts ("转账到支付宝"), check spending ("这个月花了多少",
  "钱花哪了"), view financial summaries or reports ("收支情况", "月度总结", "年度报告"),
  manage budgets ("设个预算", "预算还剩多少"), check account balances ("余额多少",
  "各账户情况"), or import/export financial data. Trigger this skill even when the user
  doesn't explicitly say "记账" — any intent involving tracking personal money flow or
  viewing personal financial status should use this tool. Do NOT trigger for: building
  accounting software, analyzing company financials/stocks, database schema design,
  or general programming tasks that happen to mention money.
---

# 记账工具使用指南

通过 CLI 命令帮用户管理个人财务。数据存储在本地 SQLite 数据库中，首次运行时自动初始化。

## 环境检查（每次对话首次使用前执行）

在执行任何记账命令前，先检查依赖是否就绪：

```bash
node -e "require('better-sqlite3')" 2>&1 && echo "ready" || echo "not_installed"
```

**如果输出 `not_installed`**，安装依赖（只需一次）：

```bash
npm install -g better-sqlite3
```

安装完成后告诉用户："记账工具环境已就绪，可以开始使用了。"

## 调用方式

所有命令通过 `node` 直接运行本 skill 目录下的 `scripts/book.mjs`：

```bash
node <SKILL目录>/scripts/book.mjs <command> '<json_params>'
```

其中 `<SKILL目录>` 是本文件（SKILL.md）所在的目录。

- 命令格式：`模块:动作`（如 `transaction:add`、`report:monthly`）
- 参数：JSON 字符串，用单引号包裹
- 无参数的命令直接执行：`node <SKILL目录>/scripts/book.mjs report:balance`
- 输出：JSON 格式 `{"success":true,"data":{...}}` 或 `{"success":false,"error":"..."}`

**错误处理**：当返回 `"success":false` 时，读取 `error` 字段的中文信息理解原因（如"分类方向不匹配"、"账户不存在"等），然后向用户说明情况或调整参数重试。

## 记账工作流

### 记录一笔支出/收入

**用户说了类似"午餐花了50"这样的话时：**

1. 先获取账户和分类的 ID（如果本次对话中还没获取过）：
   ```bash
   node <SKILL目录>/scripts/book.mjs account:list
   node <SKILL目录>/scripts/book.mjs category:list '{"direction":"EXPENSE"}'
   ```

2. 根据用户的描述推断：
   - **交易类型**：花钱 → EXPENSE，赚钱/收到 → INCOME，转账 → TRANSFER
   - **分类**：午餐/吃饭 → 餐饮，打车/地铁 → 交通，淘宝/京东 → 购物，发工资 → 工资
   - **账户**：微信付的 → 微信，支付宝 → 支付宝，现金 → 现金，刷卡 → 对应银行卡
   - **时间**：不指定默认当前时间。"昨天"/"上周五"等需要转换为具体时间

3. 执行记账命令：
   ```bash
   node <SKILL目录>/scripts/book.mjs transaction:add '{"type":"EXPENSE","amount":"50.00","accountId":1,"categoryId":1,"remark":"午餐"}'
   ```

4. 确认时用简洁的自然语言回复：
   > 已记录：餐饮支出 ¥50.00（现金），备注：午餐

**推断不确定时要询问用户**，比如"这笔是从哪个账户出的？"或"想归到哪个分类？"。不要猜。

### 记录转账

转账不需要分类，但需要源账户和目标账户：

```bash
node <SKILL目录>/scripts/book.mjs transaction:add '{"type":"TRANSFER","amount":"1000.00","accountId":1,"toAccountId":2,"remark":"转到支付宝"}'
```

### 查看和管理交易

```bash
# 查本月交易（默认）
node <SKILL目录>/scripts/book.mjs transaction:list

# 按条件查
node <SKILL目录>/scripts/book.mjs transaction:list '{"startDate":"2026-04-01","endDate":"2026-04-30","type":"EXPENSE","keyword":"午餐"}'

# 修改一笔交易（余额自动重新计算）
node <SKILL目录>/scripts/book.mjs transaction:update '{"id":5,"amount":"60.00","remark":"午餐加饮料"}'

# 删除一笔交易（余额自动回滚）
node <SKILL目录>/scripts/book.mjs transaction:delete '{"id":5}'
```

## 查看报表和统计

用户问"这个月花了多少"、"钱花哪了"、"收支情况"等问题时，调用报表命令：

```bash
# 月度汇总
node <SKILL目录>/scripts/book.mjs report:monthly '{"year":2026,"month":4}'

# 分类统计（看钱花在哪些类别）
node <SKILL目录>/scripts/book.mjs report:category '{"year":2026,"month":4,"direction":"EXPENSE"}'

# 年度汇总
node <SKILL目录>/scripts/book.mjs report:yearly '{"year":2026}'

# 月度趋势（12个月的收支变化）
node <SKILL目录>/scripts/book.mjs report:trend '{"year":2026}'

# 各账户余额一览
node <SKILL目录>/scripts/book.mjs report:balance
```

**呈现报表数据时使用表格或列表格式**，让数据一目了然。例如：

> **2026年4月收支汇总**
> | 项目 | 金额 |
> |------|------|
> | 总收入 | ¥15,000.00 |
> | 总支出 | ¥3,200.00 |
> | 净结余 | ¥11,800.00 |

分类统计用排序列表：

> **支出分类 Top 3**
> 1. 餐饮 ¥1,200.00 (37.5%)
> 2. 购物 ¥800.00 (25.0%)
> 3. 交通 ¥500.00 (15.6%)

## 预算管理

用户设定预算或问"预算还剩多少"时：

```bash
# 设置月度预算
node <SKILL目录>/scripts/book.mjs budget:set '{"categoryId":1,"amount":"2000.00","periodType":"MONTHLY","year":2026,"month":4}'

# 查看预算执行情况
node <SKILL目录>/scripts/book.mjs budget:status '{"year":2026,"month":4}'
```

**预算超支时主动提醒用户**，比如：
> 注意：餐饮预算已使用 85%（¥1,700/¥2,000），剩余 ¥300。

## 账户和分类管理

当用户需要新增账户或分类时才操作，日常记账不需要主动管理这些：

```bash
# 新增账户
node <SKILL目录>/scripts/book.mjs account:add '{"name":"招商银行","type":"BANK","initialBalance":"50000.00"}'

# 新增子分类
node <SKILL目录>/scripts/book.mjs category:add '{"name":"外卖","direction":"EXPENSE","parentId":1}'
```

## 导入导出

```bash
# 导出交易数据
node <SKILL目录>/scripts/book.mjs data:export '{"format":"csv","startDate":"2026-01-01","endDate":"2026-12-31"}'

# 导入 CSV 数据（使用本工具导出的 CSV 格式）
node <SKILL目录>/scripts/book.mjs data:import '{"file":"./records.csv","format":"csv"}'
```

## 关键规则

- **金额格式**：字符串，两位小数，如 `"50.00"`（不是数字 50）
- **分类方向匹配**：EXPENSE 交易只能用 EXPENSE 分类，INCOME 同理
- **TRANSFER 不需要分类**：转账只需 accountId 和 toAccountId
- **余额自动更新**：增删改交易时系统自动调整账户余额，无需手动管理
- **余额可以为负**：信用卡等场景允许负余额
- **本次对话中缓存 ID**：获取过一次账户/分类列表后，在同一对话内可以直接使用 ID，不用每次都重新查

## 完整命令参考

所有命令的详细参数说明见 `references/commands.md`。当不确定某个命令的参数时，查阅该文件。
