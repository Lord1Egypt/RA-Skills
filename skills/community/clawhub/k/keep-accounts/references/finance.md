# 家庭财务数据库参考文档

## 数据库位置
```
{WORKSPACE}/finances/db/finance.db
```

## 数据库结构

### accounts（账户表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | TEXT | 账户ID（如B001） |
| ledger | TEXT | 账本名称 |
| member | TEXT | 成员名称 |
| name | TEXT | 账户名称 |
| type | TEXT | 账户类型 |
| initial_balance | REAL | 初始余额 |
| budget | REAL | 预算额度 |
| remark | TEXT | 备注 |

### transactions（交易表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键自增 |
| date | TEXT | 日期（YYYY-MM-DD） |
| ledger | TEXT | 账本名称 |
| account_id | TEXT | 账户ID |
| type | TEXT | 类型（收入/支出/转账） |
| amount | REAL | 金额（始终为正数） |
| category | TEXT | 分类 |
| description | TEXT | 描述 |

### members（成员表）

| 字段 | 类型 | 说明 |
|------|------|------|
| feishu_id | TEXT | 飞书用户ID（主键） |
| nickname | TEXT | 昵称 |
| ledger | TEXT | 账本名称 |
| account_id | TEXT | 默认账户ID |
| role | TEXT | 角色（管理员/成员） |

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

## 数据库初始化SQL

如需重新初始化数据库，执行以下SQL：

```sql
CREATE TABLE IF NOT EXISTS accounts (
    id TEXT PRIMARY KEY,
    ledger TEXT NOT NULL,
    member TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    initial_balance REAL NOT NULL DEFAULT 0,
    budget REAL DEFAULT 0,
    remark TEXT
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    ledger TEXT NOT NULL,
    account_id TEXT NOT NULL,
    type TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    notes TEXT DEFAULT "",
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

CREATE TABLE IF NOT EXISTS members (
    feishu_id TEXT PRIMARY KEY,
    nickname TEXT NOT NULL,
    ledger TEXT NOT NULL,
    account_id TEXT NOT NULL,
    role TEXT DEFAULT 'member'
);
```

## 常用查询

### 查看账户余额
```python
import sqlite3
conn = sqlite3.connect('{WORKSPACE}/finances/db/finance.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute('SELECT * FROM accounts ORDER BY id')
for row in cur.fetchall():
    print(dict(row))
conn.close()
```

### 查找账户ID
```python
# 精确查找
account = conn.execute('SELECT id FROM accounts WHERE name = ? OR id = ?', (name, name)).fetchone()

# 模糊查找
account = conn.execute('SELECT id FROM accounts WHERE name LIKE ?', (f'%{name}%',)).fetchone()
```
