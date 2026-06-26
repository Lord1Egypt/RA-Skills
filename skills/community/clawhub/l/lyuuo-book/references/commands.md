# 命令参考手册

所有命令通过 `node <SKILL目录>/scripts/book.mjs <command> '<json>'` 调用。

输出格式统一为 JSON：
- 成功：`{"success": true, "data": {...}}`
- 失败：`{"success": false, "error": "错误信息"}`

---

## 账户管理

### account:add

创建新账户。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 账户名称（唯一） |
| type | string | 是 | CASH / BANK / CREDIT / ALIPAY / WECHAT / OTHER |
| initialBalance | string | 否 | 初始余额，默认 "0.00" |
| icon | string | 否 | 图标标识 |
| remark | string | 否 | 备注 |

示例：
```bash
npm run book -- account:add '{"name":"招商银行","type":"BANK","initialBalance":"10000.00"}'
```

### account:list

列出所有账户及当前余额。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| includeArchived | boolean | 否 | 是否包含已归档账户，默认 false |

示例：
```bash
npm run book -- account:list
npm run book -- account:list '{"includeArchived":true}'
```

### account:update

修改账户信息。只传需要修改的字段。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | number | 是 | 账户 ID |
| name | string | 否 | 新名称 |
| type | string | 否 | 新类型 |
| icon | string | 否 | 新图标 |
| remark | string | 否 | 新备注 |
| sortOrder | number | 否 | 排序权重 |

### account:archive

归档账户（软删除，数据保留但不在默认列表中显示）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | number | 是 | 账户 ID |

---

## 分类管理

### category:add

创建分类。支持子分类。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 分类名称 |
| direction | string | 是 | INCOME / EXPENSE |
| parentId | number | 否 | 父分类 ID，默认 0（顶级） |
| icon | string | 否 | 图标标识 |

示例：
```bash
npm run book -- category:add '{"name":"外卖","direction":"EXPENSE","parentId":1}'
```

### category:list

列出分类。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| direction | string | 否 | INCOME / EXPENSE，不指定返回全部 |
| includeArchived | boolean | 否 | 是否包含已归档，默认 false |
| tree | boolean | 否 | true 返回树形结构（含 children） |

示例：
```bash
npm run book -- category:list '{"direction":"EXPENSE"}'
npm run book -- category:list '{"direction":"EXPENSE","tree":true}'
```

### category:update

修改分类。只传需要修改的字段。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | number | 是 | 分类 ID |
| name | string | 否 | 新名称 |
| icon | string | 否 | 新图标 |
| sortOrder | number | 否 | 排序权重 |

### category:archive

归档分类。如果有未归档的子分类，会被拒绝。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | number | 是 | 分类 ID |

---

## 交易管理

### transaction:add

记录一笔交易。这是最核心的命令。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | 是 | INCOME / EXPENSE / TRANSFER |
| amount | string | 是 | 金额（字符串，如 "50.00"），必须大于 0 |
| accountId | number | 是 | 账户 ID |
| toAccountId | number | TRANSFER 时必填 | 目标账户 ID（不能与 accountId 相同） |
| categoryId | number | INCOME/EXPENSE 时必填 | 分类 ID（方向必须匹配交易类型） |
| remark | string | 否 | 备注 |
| happenTime | string | 否 | 发生时间 "YYYY-MM-DD HH:mm:ss"，默认当前时间 |

**余额联动：**
- INCOME → accountId 的余额 +amount
- EXPENSE → accountId 的余额 -amount
- TRANSFER → accountId 余额 -amount，toAccountId 余额 +amount

**校验规则：**
- 金额必须 > 0
- INCOME/EXPENSE 必须提供 categoryId，分类方向必须匹配
- TRANSFER 必须提供 toAccountId，不需要 categoryId，源和目标不能相同

示例：
```bash
# 支出
npm run book -- transaction:add '{"type":"EXPENSE","amount":"50.00","accountId":1,"categoryId":1,"remark":"午餐"}'

# 收入
npm run book -- transaction:add '{"type":"INCOME","amount":"15000.00","accountId":1,"categoryId":11,"remark":"四月工资"}'

# 转账
npm run book -- transaction:add '{"type":"TRANSFER","amount":"5000.00","accountId":1,"toAccountId":2,"remark":"转到支付宝"}'
```

### transaction:list

查询交易记录。不指定日期范围时默认返回当月数据。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| startDate | string | 否 | 起始日期 "YYYY-MM-DD" |
| endDate | string | 否 | 结束日期 "YYYY-MM-DD" |
| type | string | 否 | INCOME / EXPENSE / TRANSFER |
| accountId | number | 否 | 按账户过滤 |
| categoryId | number | 否 | 按分类过滤 |
| keyword | string | 否 | 按备注关键词搜索 |
| limit | number | 否 | 返回条数，默认 20 |
| offset | number | 否 | 偏移量，用于分页 |

### transaction:get

查看单笔交易详情。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | number | 是 | 交易 ID |

### transaction:update

修改交易。系统自动回滚旧余额并应用新余额。只传需要修改的字段。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | number | 是 | 交易 ID |
| type | string | 否 | 新交易类型 |
| amount | string | 否 | 新金额 |
| accountId | number | 否 | 新账户 |
| toAccountId | number | 否 | 新目标账户 |
| categoryId | number | 否 | 新分类 |
| remark | string | 否 | 新备注 |
| happenTime | string | 否 | 新时间 |

### transaction:delete

软删除交易。系统自动回滚余额。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | number | 是 | 交易 ID |

---

## 预算管理

### budget:set

设置或更新预算。相同 categoryId + periodType + year + month 的预算会被更新（upsert）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| categoryId | number/null | 否 | 分类 ID，null 表示总预算 |
| amount | string | 是 | 预算金额 |
| periodType | string | 是 | MONTHLY / YEARLY |
| year | number | 是 | 年份 |
| month | number | MONTHLY 时必填 | 月份 1-12 |
| remark | string | 否 | 备注 |

### budget:list

列出预算。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| year | number | 是 | 年份 |
| month | number | 否 | 月份（不指定返回全年预算） |

### budget:status

查看预算执行情况。返回每个预算的已花金额、剩余金额、使用百分比。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| year | number | 是 | 年份 |
| month | number | 否 | 月份 |
| categoryId | number | 否 | 只查特定分类的预算 |

返回数据示例：
```json
{
  "budgetId": 1,
  "categoryId": 1,
  "categoryName": "餐饮",
  "budgetAmount": "2000.00",
  "spent": "1500.00",
  "remaining": "500.00",
  "percentUsed": 75
}
```

### budget:delete

删除预算。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | number | 是 | 预算 ID |

---

## 统计报表

### report:monthly

月度收支汇总。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| year | number | 是 | 年份 |
| month | number | 是 | 月份 |

返回：totalIncome, totalExpense, netBalance, incomeCount, expenseCount

### report:yearly

年度收支汇总，含各月明细。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| year | number | 是 | 年份 |

返回：totalIncome, totalExpense, netBalance, months (12个月的月度数据)

### report:category

分类统计。返回各分类的金额和占比。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| year | number | 是 | 年份 |
| month | number | 否 | 月份（不指定统计全年） |
| direction | string | 否 | INCOME / EXPENSE，默认 EXPENSE |

返回数组：categoryName, amount, percentage, count

### report:trend

月度趋势。返回一年中每月的收支数据。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| year | number | 是 | 年份 |

返回 12 个月的数组：month, income, expense, net

### report:balance

各账户余额概览。无需参数。

```bash
npm run book -- report:balance
```

---

## 导入导出

### data:export

导出交易数据为 CSV 或 JSON。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| format | string | 是 | csv / json |
| startDate | string | 否 | 起始日期 |
| endDate | string | 否 | 结束日期 |
| outputPath | string | 否 | 输出文件路径 |

### data:import

导入交易数据。使用本工具导出的 CSV 格式，自动按名称匹配分类和账户。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | string | 是 | 文件路径 |
| format | string | 是 | csv（目前仅支持本工具导出的 CSV 格式） |

---

## 默认种子数据

首次运行时自动创建：

**支出分类（10个，ID 1-10）：**
餐饮(1), 交通(2), 购物(3), 住房(4), 娱乐(5), 医疗(6), 学习(7), 通讯(8), 日用(9), 其他支出(10)

**收入分类（6个，ID 11-16）：**
工资(11), 奖金(12), 投资(13), 退款(14), 兼职(15), 其他收入(16)

**默认账户（3个，ID 1-3）：**
现金(1), 支付宝(2), 微信(3)

注意：以上 ID 是默认种子数据的 ID。如果用户添加了新的分类或账户，ID 会递增。使用前先通过 `account:list` 和 `category:list` 确认实际 ID。
