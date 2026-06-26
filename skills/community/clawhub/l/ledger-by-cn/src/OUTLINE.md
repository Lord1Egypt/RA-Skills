# SQLite 记账工具架构大纲

## 1. 设计目标

将被 skill 调用的 Python 工具从 JSONL 文件存储迁移到 SQLite，保留与 `SKILL.md` 兼容的功能。

## 2. 当前项目结构

```
src/
├── main.py
└── app/
    ├── core/
    │   └── init_app.py
    ├── schemas/
    └── settings/
        └── config.py
```

## 3. 推荐结构

```
src/
├── __init__.py             # 导出核心函数
├── main.py                 # CLI 入口
├── db/
│   ├── __init__.py
│   ├── connection.py       # SQLite 连接管理
│   └── models.py           # 数据模型
├── services/
│   ├── __init__.py
│   ├── ledger.py          # 记账核心服务
│   ├── report.py           # 报表统计服务
│   └── export.py           # 导出服务
└── utils/
    ├── __init__.py
    ├── parser.py           # 自然语言解析
    └── formatters.py       # 输出格式化
```

## 4. 数据模型

### 4.1 账本表 (ledgers)

| 字段 | 类型 | 描述 |
|------|------|------|
| id | INTEGER PK | 账本ID |
| name | TEXT UNIQUE | 账本名称 |
| created_at | TIMESTAMP | 创建时间 |

### 4.2 账户表 (accounts)

| 字段 | 类型 | 描述 |
|------|------|------|
| id | INTEGER PK | 账户ID |
| ledger_id | INTEGER FK | 账本ID |
| name | TEXT | 账户名称（现金/银行卡等）|
| created_at | TIMESTAMP | 创建时间 |

### 4.3 交易表 (transactions)

| 字段 | 类型 | 描述 |
|------|------|------|
| id | INTEGER PK | 交易ID |
| ledger_id | INTEGER FK | 账本ID |
| date | DATE | 交易日期 |
| amount | REAL | 金额（正=收入，负=支出）|
| category | TEXT | 分类 |
| account | TEXT | 账户 |
| description | TEXT | 备注 |
| created_at | TIMESTAMP | 创建时间 |

### 4.4 期初表 (openings)

| 字段 | 类型 | 描述 |
|------|------|------|
| id | INTEGER PK | ID |
| ledger_id | INTEGER FK | 账本ID |
| month | TEXT | 期初月份（YYYY-MM）|
| amount | REAL | 期初金额 |
| created_at | TIMESTAMP | 创建时间 |

## 5. 核心函数接口

### 5.1 账本管理

```python
# 创建账本
def create_ledger(name: str) -> int

# 获取账本ID
def get_ledger_id(name: str) -> int | None
```

### 5.2 记账服务

```python
# 添加单笔交易
def add_transaction(
    ledger_name: str,
    date: str,           # YYYY-MM-DD
    amount: float,       # 正=收入，负=支出
    category: str = "其他",
    account: str = "现金",
    description: str = ""
) -> int

# 批量添加交易
def batch_add_transactions(
    ledger_name: str,
    transactions: List[dict]
) -> int  # 返回添加数量

# 设置期初结余
def set_opening_balance(
    ledger_name: str,
    month: str,          # YYYY-MM
    amount: float
) -> bool
```

### 5.3 查询服务

```python
# 获取指定月份交易
def get_transactions(
    ledger_name: str,
    month: str = None    # YYYY-MM，为空则获取全部
) -> List[dict]

# 获取月度汇总
def get_monthly_summary(
    ledger_name: str,
    month: str
) -> dict:
    # {
    #   "opening": 0,
    #   "income": 1000,
    #   "expense": -500,
    #   "closing": 500,
    #   "transactions": [...]
    # }

# 获取余额趋势
def get_balance_trend(
    ledger_name: str,
    months: List[str]
) -> List[dict]:
    # [{"month": "2026-01", "balance": -15206}, ...]
```

### 5.4 导出服务

```python
# 导出 CSV
def export_csv(
    ledger_name: str,
    month: str = None,
    output_path: str = None
) -> str  # 返回文件路径
```

## 6. 工具函数

### 6.1 自然语言解析

```python
# 解析用户输入为交易列表
def parse_input(text: str) -> List[dict]
# 支持格式：
# "2026-03-15 -50 餐饮 现金 午餐"
# "3月15日 花了50元 餐饮"
# 批量多行输入
```

### 6.2 日期解析

```python
# 智能解析日期
def parse_date(text: str, current_month: str = None) -> str
# 支持：14, 0314, 3月15日, 2026-3-5, 上个月 等
```

## 7. CLI 入口

```bash
# 记账
python -m ledger add "2026-03-15 -50 餐饮"

# 查询月度汇总
python -m ledger summary default 2026-03

# 导出CSV
python -m ledger export default 2026-03 -o output.csv

# 设置期初
python -m ledger opening default 2025-12 -15206
```

## 8. 与现有 SKILL.md 兼容

- 数据路径：`~/.openclaw/skills_data/ledger/<账本名>/`
- SQLite 数据库位置：`~/.openclaw/skills_data/ledger/<账本名>/ledger.db`
- 输出格式兼容现有 Markdown 表格
- CSV 使用 UTF-8 BOM 编码

## 9. 实现优先级

1. **第一阶段**：数据库连接 + 交易 CRUD
2. **第二阶段**：期初结余 + 月度汇总
3. **第三阶段**：批量记账 + 自然语言解析
4. **第四阶段**：余额趋势 + CSV 导出
