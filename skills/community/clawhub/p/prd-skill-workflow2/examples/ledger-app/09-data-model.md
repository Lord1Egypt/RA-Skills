# 09 数据模型

## 9.1 实体关系图

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    User     │ 1   N │   Ledger    │ 1   N │ Transaction │
│             │◄──────│             │◄──────│             │
│  id (PK)    │       │  id (PK)    │       │  id (PK)    │
│  phone      │       │  user_id(FK)│       │  ledger_id  │
│  nickname   │       │  name       │       │  amount     │
│  avatar     │       │  type       │       │  type       │
│  created_at │       │  created_at │       │  category   │
└─────────────┘       └─────────────┘       │  remark     │
                                            │  created_at │
                                            └─────────────┘
```

## 9.2 数据表设计

### 用户表 (user)

| 字段 | 类型 | 约束 | 说明 |
|-----|------|------|------|
| id | BIGINT | PK, AUTO | 主键 |
| phone | VARCHAR(20) | UNIQUE | 手机号 |
| password_hash | VARCHAR(255) | NOT NULL | 密码哈希 |
| nickname | VARCHAR(50) | - | 昵称 |
| avatar | VARCHAR(500) | - | 头像URL |
| default_ledger_id | BIGINT | FK | 默认账本ID |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |

### 账本田 (ledger)

| 字段 | 类型 | 约束 | 说明 |
|-----|------|------|------|
| id | BIGINT | PK, AUTO | 主键 |
| user_id | BIGINT | FK, NOT NULL | 用户ID |
| name | VARCHAR(50) | NOT NULL | 账本名称 |
| type | TINYINT | DEFAULT 1 | 1-个人 2-生意 3-旅行 |
| currency | VARCHAR(10) | DEFAULT 'CNY' | 币种 |
| is_default | BOOLEAN | DEFAULT false | 是否默认账本 |
| created_at | DATETIME | NOT NULL | 创建时间 |

### 记账记录表 (transaction)

| 字段 | 类型 | 约束 | 说明 |
|-----|------|------|------|
| id | BIGINT | PK, AUTO | 主键 |
| ledger_id | BIGINT | FK, NOT NULL | 账本ID |
| amount | DECIMAL(10,2) | NOT NULL | 金额 |
| type | TINYINT | NOT NULL | 1-支出 2-收入 |
| category_id | INT | NOT NULL | 分类ID |
| remark | VARCHAR(200) | - | 备注 |
| record_date | DATE | NOT NULL | 记账日期 |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |
| is_deleted | BOOLEAN | DEFAULT false | 软删除 |

### 预算表 (budget)

| 字段 | 类型 | 约束 | 说明 |
|-----|------|------|------|
| id | BIGINT | PK, AUTO | 主键 |
| ledger_id | BIGINT | FK, NOT NULL | 账本ID |
| amount | DECIMAL(10,2) | NOT NULL | 预算金额 |
| period_type | TINYINT | DEFAULT 1 | 1-月度 2-年度 |
| year_month | VARCHAR(10) | NOT NULL | 年月 (如 2024-01) |
| alert_threshold | TINYINT | DEFAULT 80 | 提醒阈值(%) |
| created_at | DATETIME | NOT NULL | 创建时间 |

## 9.3 索引设计

| 表名 | 索引名 | 字段 | 说明 |
|-----|-------|------|------|
| user | idx_phone | phone | 登录查询 |
| ledger | idx_user_id | user_id | 查询用户账本 |
| transaction | idx_ledger_date | ledger_id, record_date | 账单列表查询 |
| transaction | idx_category | category_id | 分类统计 |
