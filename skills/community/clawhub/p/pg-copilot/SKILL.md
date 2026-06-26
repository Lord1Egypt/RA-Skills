---
name: pg-copilot
description: "PostgreSQL AI 助手 - 自然语言转 SQL、SQL 转自然语言、ERD、性能优化、分区管理、实时同步。一个技能搞定 PostgreSQL 所有需求。"
---

# pg-copilot 🐘

PostgreSQL AI 助手 | 自然语言转 SQL | SQL 转自然语言 | 性能优化 | 实时同步

## 功能概览

| 功能 | 说明 |
|------|------|
| **数据库连接** | 多数据库配置、自动重连、连接池 |
| **Schema 管理** | 自动获取表结构、实时监听变化 |
| **自然语言查询** | 中文描述需求 → 自动生成 SQL |
| **SQL 执行** | 安全执行、危险操作拦截 |
| **SQL 解释** | 将查询结果转为自然语言 |
| **ERD 可视化** | Mermaid 关系图展示 |
| **性能优化** | EXPLAIN 分析、索引建议 |
| **分区管理** | Range/List/Hash 分区 |
| **实时同步** | 触发器 + 变更队列，自动同步到目标库（支持 MySQL） |
| **同步日志** | _sync_log 记录所有同步操作 |

---

## Quick Reference

| 场景 | 操作 |
|------|------|
| 配置数据库 | `config <host> <port> <user> <password> <database>` |
| 测试连接 | "测试连接" |
| 查询数据 | "查每个用户的订单总金额" |
| 解释结果 | "解释这个查询结果" |
| 生成 ERD | "画出用户表和订单表的关系" |
| 优化查询 | "优化这个查询" |
| 创建分区 | "按月份分区" |
| 配置同步 | "配置实时同步" |
| 执行 SQL | "执行上面的 SQL" |

---

## 核心功能

### 1. 自然语言查询

```
用户：帮我查每个用户的订单总金额

技能：
## 生成的 SQL
```sql
SELECT 
    u.name AS 用户名,
    SUM(o.amount) AS 订单总金额
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name
ORDER BY 订单总金额 DESC;
```
```

### 2. SQL 转自然语言

```
用户：解释这个查询结果
SELECT u.name, COUNT(o.id) as order_count 
FROM users u LEFT JOIN orders o ON u.id = o.user_id 
GROUP BY u.id, u.name

技能：
## 查询结果解释

**查询类型**：分组统计

**结果摘要**：共 5 条记录

**详细分析**：
| 用户名 | 订单数 |
|--------|--------|
| 李四 | 4 |
| 张三 | 4 |
| 王五 | 2 |

**统计**：
- 总订单数：10
- 平均订单数：2
- 最多订单：4
- 最少订单：0
```

**方式一：LLM 智能解释（推荐）**

需要配置 LLM API：

```bash
# 配置 LLM（支持 OpenAI/Claude 等兼容 API）
python scripts/pg_copilot.py config-llm <api_url> <api_key> [model]

# 示例
python scripts/pg_copilot.py config-llm https://api.openai.com/v1/chat/completions sk-xxx
```

**方式二：简单解析（默认）**

未配置 LLM 时自动使用。

### 3. ERD 可视化

```
用户：画出用户表和订单表的关系

技能：
```mermaid
erDiagram
    USERS ||--o{ ORDERS : places
    USERS { int id PK, varchar name, varchar email }
    ORDERS { int id PK, int user_id FK, numeric amount }
```
```

---

## 实时同步功能 ⚡

### 前置条件

**重要：使用同步功能前必须满足：**

1. **源表必须有主键** - 同步依赖主键定位记录
   ```sql
   -- 如果表没有主键，添加：
   ALTER TABLE my_table ADD COLUMN id SERIAL PRIMARY KEY;
   ```

2. **安装依赖** - 需要 pymysql 支持 MySQL 目标
   ```bash
   pip install pymysql
   ```

3. **目标数据库可访问** - 网络连通

---

### 同步表结构

#### _sync_config（配置表）

存储同步任务配置：

| 字段 | 类型 | 说明 | 必填 |
|------|------|------|------|
| source_table | VARCHAR(255) | 源表名 | ✅ |
| target_host | VARCHAR(255) | 目标数据库地址 | ✅ |
| target_port | INTEGER | 目标端口（PG默认5432，MySQL默认3306） | ✅ |
| target_user | VARCHAR(255) | 目标数据库用户名 | ✅ |
| target_password | VARCHAR(255) | 目标数据库密码（Base64加密存储） | ✅ |
| target_database | VARCHAR(255) | 目标数据库名 | ✅ |
| target_table | VARCHAR(255) | 目标表名（默认=源表名） | |
| target_type | VARCHAR(20) | 目标类型：**postgresql** 或 **mysql** | ✅ |
| sync_mode | VARCHAR(20) | 同步模式：realtime/batch | |
| enabled | BOOLEAN | 是否启用 | |
| **max_retries** | INTEGER | **失败重试次数（默认3）** | |
| **webhook_url** | TEXT | **告警 Webhook URL** | |
| **sync_batch_size** | INTEGER | **批量大小（默认100）** | |

#### _sync_changes（变更队列表）

自动记录所有变更（由触发器填充）：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGSERIAL | 主键 |
| table_name | VARCHAR(255) | 表名 |
| operation | VARCHAR(10) | 操作：INSERT/UPDATE/DELETE |
| record_id | INTEGER | 记录ID（主键值） |
| old_data | JSONB | 旧数据（UPDATE/DELETE） |
| new_data | JSONB | 新数据（INSERT/UPDATE） |
| synced | BOOLEAN | 是否已同步 |
| created_at | TIMESTAMP | 变更时间 |

#### _sync_log（同步日志表）

记录所有同步操作：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| table_name | VARCHAR(255) | 表名 |
| operation | VARCHAR(20) | 操作类型 |
| record_id | INTEGER | 记录ID |
| target_db | VARCHAR(255) | 目标数据库 |
| status | VARCHAR(20) | 状态：success/failed |
| error_message | TEXT | 错误信息 |
| created_at | TIMESTAMP | 执行时间 |

---

### 配置示例

**初始化同步表：**
```bash
python scripts/pg_copilot.py sync-init
```

**同步到 MySQL（生产环境）：**
```bash
# sync-add 参数说明
# <table> <host> <port> <user> <password> <db> <target_table> [type] [retries] [webhook] [batch]

python scripts/pg_copilot.py sync-add \
    users \
    <target_host> \
    <port> \
    <username> \
    <password> \
    <database> \
    users \
    mysql \
    3 \
    https://your-webhook-url \
    100
```

**同步到 PostgreSQL：**
```sql
INSERT INTO _sync_config 
    (source_table, target_host, target_port, target_user, target_password, target_database, target_table, target_type, max_retries, webhook_url)
VALUES 
    ('orders', '<target_host>', <port>, '<username>', '<password>', '<database>', 'orders', 'postgresql', 3, 'https://your-webhook-url');
```

### 生产环境特性

| 特性 | 说明 |
|------|------|
| **密码加密** | Base64 加密存储，支持环境变量覆盖 |
| **自动重试** | 失败自动重试 3 次（可配置） |
| **告警通知** | 失败时发送 Webhook 通知 |
| **批量同步** | 支持批量大小配置 |

---

### 查看同步状态

```bash
python scripts/pg_copilot.py sync-status
```

---

## 分区管理

### 范围分区（按时间）

```sql
CREATE TABLE orders_partitioned (
    LIKE orders INCLUDING ALL
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2024_01 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

### 列表分区（按状态）

```sql
CREATE TABLE orders_by_status (
    LIKE orders INCLUDING ALL
) PARTITION BY LIST (status);

CREATE TABLE orders_pending PARTITION OF orders_by_status
    FOR VALUES IN ('pending');
```

### 哈希分区（按 ID）

```sql
CREATE TABLE users_partitioned (
    LIKE users INCLUDING ALL
) PARTITION BY HASH (user_id);

CREATE TABLE users_p0 PARTITION OF users_partitioned
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);
```

---

## CLI 命令

```bash
# 配置数据库
python scripts/pg_copilot.py config <host> <port> <user> <password> <database>

# 基本操作
python scripts/pg_copilot.py test                    # 测试连接
python scripts/pg_copilot.py schema                  # 获取 Schema
python scripts/pg_copilot.py execute "SELECT..."   # 执行 SQL
python scripts/pg_copilot.py narrate "SELECT..."   # SQL 转自然语言
python scripts/pg_copilot.py explain "SELECT..."    # 性能分析

# 同步功能
python scripts/pg_copilot.py sync-init              # 初始化同步表
python scripts/pg_copilot.py sync-add <table> <host> ...  # 添加同步任务
python scripts/pg_copilot.py sync-status            # 查看状态
python scripts/pg_copilot.py sync-watch             # 监听同步
```

---

## 依赖

- Python 3.8+
- psycopg2-binary
- pymysql（用于 MySQL 目标同步）

---

*pg-copilot - 让 PostgreSQL 管理和同步像说话一样简单*
