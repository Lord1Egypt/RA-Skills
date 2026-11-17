---
name: kes-core
name_for_command: kes-core
description: KingbaseES 核心 SQL 语法参考。当用户提到 SQL 语法、DDL/DML/DCL、数据类型、表空间、分区表、系统目录、事务控制、分页查询、窗口函数、CTE、JSON 操作时，必须使用此技能。
---

# KingbaseES 核心 SQL 语法参考

本技能提供 KingbaseES 的核心 SQL 语法快速参考，涵盖 DDL/DML/DCL、事务、常见查询模式和系统目录查询。

> **PL/SQL 编程** → 见 `kes-plsql` 技能（存储过程、函数、触发器、游标、包）
> **Oracle 兼容** → 见 `kes-oracle-compat` 技能（oracle_compatible、语法映射、类型对照）

## 快速导航

| 主题 | 参考文件 |
|------|---------|
| DDL/DML/DCL 完整语法 | `ref/sql-syntax.md` |
| 表空间/分区/索引策略 | `ref/schema-design.md` |
| 数据类型详解 | `ref/data-types.md` |
| 系统目录查询 | `ref/system-catalog.md` |
| 错误代码 | `ref/error-codes.md` |

## 1. DDL — 数据定义

```sql
-- 创建数据库
CREATE DATABASE db_name WITH ENCODING 'UTF8' TABLESPACE sys_default;

-- 创建表（完整语法）
CREATE TABLE employees (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(200) UNIQUE,
    dept_id     INT REFERENCES departments(id),
    salary      DECIMAL(10, 2) CHECK (salary > 0),
    hire_date   DATE DEFAULT CURRENT_DATE,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version     INT DEFAULT 1
) TABLESPACE data_tbs;

-- 分区表（RANGE）
CREATE TABLE sales (
    id      BIGSERIAL,
    amount  DECIMAL(12, 2),
    sold_at DATE NOT NULL
) PARTITION BY RANGE (sold_at);

CREATE TABLE sales_y2024 PARTITION OF sales
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
CREATE TABLE sales_y2025 PARTITION OF sales
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- 索引
CREATE INDEX idx_emp_dept ON employees(dept_id);
CREATE UNIQUE INDEX idx_emp_email ON employees(LOWER(email));
-- 部分索引
CREATE INDEX idx_active_emp ON employees(name) WHERE status = 'active';
-- 表达式索引
CREATE INDEX idx_salary_range ON employees((salary / 1000));
```

## 2. DML — 数据操作

```sql
-- 写入
INSERT INTO employees (name, email, dept_id, salary)
VALUES ('张三', 'zhangsan@co.com', 10, 15000);

-- 批量写入
INSERT INTO employees (name, dept_id, salary)
SELECT name, dept_id, avg_salary FROM temp_hires;

-- UPSERT（冲突更新）
INSERT INTO employees (id, name, salary)
VALUES (1, '张三', 16000)
ON CONFLICT (id) DO UPDATE SET
    name    = EXCLUDED.name,
    salary  = EXCLUDED.salary,
    version = employees.version + 1;

-- 更新（多表关联）
UPDATE employees e
SET salary = salary * 1.1
FROM departments d
WHERE e.dept_id = d.id AND d.name = '工程';

-- 删除（带条件）
DELETE FROM employees WHERE dept_id IN (SELECT id FROM departments WHERE budget = 0);

-- 合并操作
MERGE INTO target t
USING source s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET t.value = s.value
WHEN NOT MATCHED THEN INSERT (id, value) VALUES (s.id, s.value);
```

## 3. DCL — 数据控制

```sql
-- 授权
GRANT SELECT, INSERT ON employees TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT EXECUTE ON FUNCTION calc_salary(INT) TO app_user;

-- 批量授权
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reporter;

-- 默认权限
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO reporter;

-- 撤销
REVOKE DELETE ON employees FROM app_user;
```

## 4. 事务控制

```sql
BEGIN;
-- 或 START TRANSACTION;

SAVEPOINT sp1;
-- 操作...
ROLLBACK TO sp1;  -- 回滚到保存点
-- 或 COMMIT; / ROLLBACK;
```

## 5. 常见查询模式

### 分页查询

```sql
-- 标准分页
SELECT * FROM employees ORDER BY id LIMIT 20 OFFSET 40;  -- 第3页

-- 键集分页（高性能）
SELECT * FROM employees
WHERE id > 1000
ORDER BY id
LIMIT 20;
```

### 窗口函数

```sql
SELECT
    name,
    dept_id,
    salary,
    RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dept_rank,
    LEAD(name) OVER (PARTITION BY dept_id ORDER BY salary) AS next_colleague,
    AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg
FROM employees;
```

### CTE（公共表表达式）

```sql
-- 递归CTE：查询组织树
WITH RECURSIVE org_tree AS (
    SELECT id, name, manager_id, 1 AS depth
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, ot.depth + 1
    FROM employees e
    JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT * FROM org_tree ORDER BY depth, name;
```

### JSON操作

```sql
-- 创建JSON列
ALTER TABLE products ADD COLUMN attributes JSONB;

-- 查询
SELECT * FROM products WHERE attributes->>'color' = 'red';

-- 创建GIN索引
CREATE INDEX idx_prod_attr ON products USING GIN(attributes);

-- 更新
UPDATE products SET attributes = jsonb_set(attributes, '{color}', '"blue"');
```

## 6. 系统目录快速查询

```sql
-- 查看当前库所有表
SELECT schemaname, tablename FROM sys_tables WHERE schemaname NOT LIKE 'sys%';

-- 查看表结构
SELECT column_name, data_type, is_nullable, column_default
FROM sys_information_schema.columns
WHERE table_name = 'employees'
ORDER BY ordinal_position;

-- 查看索引
SELECT indexname, indexdef FROM sys_indexes WHERE tablename = 'employees';

-- 查看表大小
SELECT
    relname,
    sys_size_pretty(sys_total_relation_size(relid)),
    n_live_tup,
    n_dead_tup
FROM sys_stat_user_tables
ORDER BY sys_total_relation_size(relid) DESC;

-- 查看序列
SELECT sequencename, sequenceowner FROM sys_sequences;

-- 查看函数
SELECT routine_name, routine_type, data_type
FROM sys_information_schema.routines
WHERE routine_schema = 'public';
```

## 7. 关键原则

1. **标识符**: 双引号内保持大小写，无引号自动转小写
2. **字符串**: 单引号，转义用`''`，或使用`E'\n'`风格
3. **NULL处理**: `IS NULL` / `IS NOT NULL`，不用`= NULL`
4. **事务**: DDL自动隐式提交，需用`BEGIN...COMMIT`包裹
5. **锁**: 默认READ COMMITTED隔离级别，Serializable需显式指定
6. **数组**: 下标从1开始，`ARRAY[1,2,3]`，`ANY(array)`用于IN检查
7. **序列**: `SERIAL`自动创建序列，`LASTVAL()`获取最后使用的值

## 相关技能

- **kes-plsql** — PL/SQL 编程（存储过程、函数、触发器、游标、包）
- **kes-oracle-compat** — Oracle 兼容模式（语法映射、数据类型对照、迁移指南）

## 参考文档

```
kes-core/
├── SKILL.md            # 本文件
├── ref/
│   ├── sql-syntax.md   # DDL/DML/DCL 完整语法
│   ├── schema-design.md # 表空间/分区/索引策略
│   ├── data-types.md   # 数据类型详解
│   ├── system-catalog.md # 系统目录查询
│   └── error-codes.md  # 错误代码
└── test-cases.md
```
