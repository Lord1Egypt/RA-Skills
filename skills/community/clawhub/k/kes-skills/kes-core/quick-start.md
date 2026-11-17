# KingbaseES 新手入门教程

从零开始：安装 → 连接 → 创建表 → 写入数据 → 查询 → 存储过程 → 导出数据。

---

## 1. 环境准备

### 确认安装

```bash
# 检查KingbaseES是否已安装
kb --version

# 检查数据目录
echo $KINGBASE_HOME
# 典型路径: /opt/Kingbase/ES/V8

# 检查实例状态
sys_isready -h localhost -p 54321
# 输出: localhost:54321 - accepting connections
```

### 启动/停止数据库

```bash
# 启动
sys_ctl start -D $KINGBASE_HOME/data

# 停止
sys_ctl stop -D $KINGBASE_HOME/data -m fast

# 重启
sys_ctl restart -D $KINGBASE_HOME/data

# 查看运行状态
sys_ctl status -D $KINGBASE_HOME/data
```

### 系统服务方式（推荐生产环境）

```bash
# 查看服务状态
systemctl status kingbase

# 启动/停止/重启
systemctl start kingbase
systemctl stop kingbase
systemctl restart kingbase

# 开机自启
systemctl enable kingbase
```

---

## 2. 连接数据库

### 使用 ksql 命令行

```bash
# 基本连接
ksql -h localhost -p 54321 -U SYSTEM -d test

# 本地连接（省略主机和端口）
ksql -U SYSTEM -d test

# 带密码提示
ksql -h localhost -p 54321 -U SYSTEM -W -d test

# 执行单条SQL后退出
ksql -U SYSTEM -d test -c "SELECT version();"

# 静默模式（适合脚本）
ksql -U SYSTEM -d test -c "SELECT count(*) FROM employees;" -t
```

### 连接字符串

```
KSQL:
  KSQL_CONNECT='host=localhost port=54321 dbname=test user=SYSTEM'
```

### 退出 ksql

```sql
\q          -- 退出
\c dbname   -- 切换数据库
\du         -- 列出用户
\dt         -- 列出表
\d tablename -- 查看表结构
\di         -- 列出索引
```

---

## 3. 创建数据库

```sql
-- 创建数据库
CREATE DATABASE myapp WITH
    ENCODING 'UTF8'
    TABLESPACE sys_default
    OWNER SYSTEM;

-- 查看数据库列表
\l
-- 或
SELECT datname FROM sys_database;

-- 切换数据库
\c myapp

-- 删除数据库（需先断开所有连接）
DROP DATABASE myapp;
```

---

## 4. 创建表

### 基本建表

```sql
-- 创建部门表
CREATE TABLE departments (
    id          INT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    budget      DECIMAL(12, 2) DEFAULT 0,
    created_at  TIMESTAMP DEFAULT NOW()
);

-- 创建员工表（带外键）
CREATE TABLE employees (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(200) UNIQUE,
    dept_id     INT REFERENCES departments(id),
    salary      DECIMAL(10, 2) CHECK (salary > 0),
    hire_date   DATE DEFAULT CURRENT_DATE,
    status      VARCHAR(20) DEFAULT 'active',
    created_at  TIMESTAMP DEFAULT NOW()
);

-- 查看表结构
\d employees
```

### Oracle 兼容建表

```sql
-- 在Oracle兼容模式下
CREATE TABLE emp (
    emp_no      NUMBER(6) PRIMARY KEY,
    emp_name    VARCHAR2(100) NOT NULL,
    dept_no     NUMBER(4),
    salary      NUMBER(10, 2),
    hire_date   DATE DEFAULT SYSDATE
);
```

---

## 5. 写入数据

### 单条写入

```sql
INSERT INTO departments (id, name, budget)
VALUES (10, '工程部', 5000000);

INSERT INTO departments (id, name, budget)
VALUES (20, '市场部', 3000000);

INSERT INTO departments (id, name, budget)
VALUES (30, '人力资源部', 2000000);

INSERT INTO employees (name, email, dept_id, salary)
VALUES ('张三', 'zhangsan@company.com', 10, 15000);

INSERT INTO employees (name, email, dept_id, salary)
VALUES ('李四', 'lisi@company.com', 10, 12000);

INSERT INTO employees (name, email, dept_id, salary)
VALUES ('王五', 'wangwu@company.com', 20, 13000);
```

### 批量写入

```sql
-- 从SELECT结果写入
INSERT INTO employees (name, email, dept_id, salary)
SELECT name, email, 30, 10000
FROM temp_candidates
WHERE approved = true;

-- 使用VALUES多行写入
INSERT INTO employees (name, email, dept_id, salary)
VALUES
    ('赵六', 'zhaoliu@company.com', 10, 14000),
    ('孙七', 'sunqi@company.com', 20, 11000),
    ('周八', 'zhouba@company.com', 30, 9500);
```

### UPSERT（冲突更新）

```sql
INSERT INTO employees (id, name, salary)
VALUES (1, '张三', 16000)
ON CONFLICT (id) DO UPDATE SET
    name    = EXCLUDED.name,
    salary  = EXCLUDED.salary;
```

---

## 6. 查询数据

### 基本查询

```sql
-- 查询所有员工
SELECT * FROM employees;

-- 带条件查询
SELECT name, salary, hire_date
FROM employees
WHERE dept_id = 10
  AND salary > 12000
ORDER BY salary DESC;

-- 聚合查询
SELECT
    d.name AS department,
    COUNT(e.id) AS employee_count,
    AVG(e.salary) AS avg_salary,
    MAX(e.salary) AS max_salary,
    MIN(e.salary) AS min_salary
FROM departments d
LEFT JOIN employees e ON d.id = e.dept_id
GROUP BY d.name
ORDER BY avg_salary DESC;
```

### 分页查询

```sql
-- 标准分页（第2页，每页10条）
SELECT * FROM employees
ORDER BY id
LIMIT 10 OFFSET 10;

-- 键集分页（性能更好）
SELECT * FROM employees
WHERE id > 100
ORDER BY id
LIMIT 10;
```

### 子查询

```sql
-- 查询高于部门平均薪资的员工
SELECT e.name, e.salary, e.dept_id
FROM employees e
WHERE e.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.dept_id = e.dept_id
);
```

### 窗口函数

```sql
SELECT
    name,
    dept_id,
    salary,
    RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dept_rank,
    AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg_salary
FROM employees;
```

### CTE（公共表表达式）

```sql
WITH dept_stats AS (
    SELECT
        dept_id,
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
)
SELECT e.name, e.salary, ds.avg_salary
FROM employees e
JOIN dept_stats ds ON e.dept_id = ds.dept_id
WHERE e.salary > ds.avg_salary;
```

---

## 7. 更新与删除

### 更新数据

```sql
-- 单表更新
UPDATE employees
SET salary = salary * 1.1
WHERE dept_id = 10;

-- 多表关联更新
UPDATE employees e
SET salary = salary * 1.15
FROM departments d
WHERE e.dept_id = d.id
  AND d.name = '工程部';

-- 带事务的更新
BEGIN;
UPDATE employees SET salary = 17000 WHERE id = 1;
-- 验证
SELECT * FROM employees WHERE id = 1;
COMMIT;
-- 或 ROLLBACK;
```

### 删除数据

```sql
-- 单条删除
DELETE FROM employees WHERE id = 5;

-- 条件删除
DELETE FROM employees
WHERE dept_id IN (
    SELECT id FROM departments WHERE budget = 0
);

-- 清空表（快速，不记录单行日志）
TRUNCATE TABLE employees;
-- 或带级联
TRUNCATE TABLE employees CASCADE;
```

---

## 8. 创建索引

```sql
-- 普通索引
CREATE INDEX idx_emp_dept ON employees(dept_id);

-- 唯一索引
CREATE UNIQUE INDEX idx_emp_email ON employees(email);

-- 表达式索引
CREATE INDEX idx_emp_email_lower ON employees(LOWER(email));

-- 部分索引
CREATE INDEX idx_active_emp ON employees(name)
WHERE status = 'active';

-- 复合索引
CREATE INDEX idx_emp_dept_status ON employees(dept_id, status);

-- 查看索引
\d employees
-- 或
SELECT indexname, indexdef FROM sys_indexes WHERE tablename = 'employees';
```

---

## 9. 存储过程与函数

### 创建函数

```sql
-- 创建薪资计算函数
CREATE OR ALTER FUNCTION calc_bonus(emp_id INT, rate DECIMAL)
RETURNS DECIMAL AS
DECLARE
    base_salary DECIMAL;
    bonus DECIMAL;
BEGIN
    SELECT salary INTO base_salary
    FROM employees
    WHERE id = emp_id;

    IF base_salary IS NULL THEN
        RAISE EXCEPTION '员工不存在: %', emp_id;
    END IF;

    bonus := base_salary * rate;
    RETURN bonus;
END;

-- 调用函数
SELECT calc_bonus(1, 0.2);
```

### 创建存储过程

```sql
-- 创建调薪存储过程
CREATE OR ALTER PROCEDURE raise_salary(
    p_dept_id INT,
    p_rate DECIMAL
) AS
DECLARE
    affected_count INT;
BEGIN
    UPDATE employees
    SET salary = salary * (1 + p_rate)
    WHERE dept_id = p_dept_id;

    GET DIAGNOSTICS affected_count = ROW_COUNT;
    RAISE NOTICE '调薪完成: 影响 % 人', affected_count;
END;

-- 执行存储过程
CALL raise_salary(10, 0.1);
```

### 创建触发器

```sql
-- 审计日志表
CREATE TABLE emp_audit (
    id          SERIAL PRIMARY KEY,
    emp_id      INT,
    action      VARCHAR(10),
    old_salary  DECIMAL(10, 2),
    new_salary  DECIMAL(10, 2),
    changed_at  TIMESTAMP DEFAULT NOW()
);

-- 触发器函数
CREATE OR ALTER FUNCTION log_salary_change()
RETURNS TRIGGER AS
BEGIN
    IF OLD.salary != NEW.salary THEN
        INSERT INTO emp_audit (emp_id, action, old_salary, new_salary)
        VALUES (NEW.id, 'UPDATE', OLD.salary, NEW.salary);
    END IF;
    RETURN NEW;
END;

-- 创建触发器
CREATE TRIGGER trg_salary_change
AFTER UPDATE OF salary ON employees
FOR EACH ROW
EXECUTE FUNCTION log_salary_change();

-- 测试触发器
UPDATE employees SET salary = 18000 WHERE id = 1;

-- 查看审计日志
SELECT * FROM emp_audit ORDER BY changed_at DESC;
```

---

## 10. 权限管理

```sql
-- 创建用户
CREATE USER app_user WITH ENCRYPTED PASSWORD 'P@ssw0rd123';

-- 授予数据库连接权限
GRANT CONNECT ON DATABASE myapp TO app_user;

-- 授予Schema访问权限
GRANT USAGE ON SCHEMA public TO app_user;

-- 授予表查询权限
GRANT SELECT ON employees TO app_user;
GRANT SELECT, INSERT, UPDATE ON employees TO app_user;

-- 批量授予
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_user;

-- 设置新表默认权限
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO app_user;

-- 授予序列使用权限
GRANT USAGE, SELECT ON SEQUENCE employees_id_seq TO app_user;

-- 撤销权限
REVOKE DELETE ON employees FROM app_user;
```

---

## 11. 事务控制

```sql
-- 开始事务
BEGIN;

-- 操作1
UPDATE employees SET salary = 20000 WHERE id = 1;

-- 设置保存点
SAVEPOINT before_dept_update;

-- 操作2
UPDATE departments SET budget = budget - 100000 WHERE id = 10;

-- 回滚到保存点（撤销操作2，保留操作1）
ROLLBACK TO before_dept_update;

-- 提交剩余操作
COMMIT;

-- 或完全回滚
-- ROLLBACK;

-- 设置事务隔离级别
BEGIN ISOLATION LEVEL SERIALIZABLE;
-- 或
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

---

## 12. 导出数据

### 使用 kdump

```bash
# 导出整个数据库
kdump -U SYSTEM -d myapp > myapp_backup.sql

# 导出单张表
kdump -U SYSTEM -d myapp -t employees > employees.sql

# 导出为CSV格式
kdump -U SYSTEM -d myapp -t employees --csv > employees.csv

# 导入数据
kdump -U SYSTEM -d target_db < myapp_backup.sql
```

### 使用 COPY 命令

```sql
-- 导出CSV
COPY employees TO '/tmp/employees.csv' WITH (FORMAT CSV, HEADER);

-- 导入CSV
COPY employees FROM '/tmp/employees.csv' WITH (FORMAT CSV, HEADER);

-- 导出为Insert语句（便于跨库迁移）
COPY (SELECT * FROM employees) TO '/tmp/employees_insert.sql';
```

### 使用 ksql \copy

```sql
-- 客户端导出（不需要服务器权限）
\copy employees TO '/tmp/employees.csv' WITH (FORMAT CSV, HEADER)

-- 客户端导入
\copy employees FROM '/tmp/employees.csv' WITH (FORMAT CSV, HEADER)
```

---

## 13. 常用维护操作

### 更新统计信息

```sql
-- 分析单表
ANALYZE employees;

-- 分析全库
ANALYZE;

-- VACUUM回收空间
VACUUM employees;

-- VACUUM ANALYZE 同时进行
VACUUM ANALYZE employees;
```

### 查看数据库状态

```sql
-- 数据库版本
SELECT version();

-- 当前连接数
SELECT count(*) FROM sys_stat_activity;

-- 表大小
SELECT
    relname,
    sys_size_pretty(sys_relation_size(relid)) AS size,
    n_live_tup AS rows
FROM sys_stat_user_tables
ORDER BY sys_relation_size(relid) DESC;

-- 表空间使用
SELECT
    spcname,
    sys_size_pretty(sys_tablespace_size(spcname)) AS size
FROM sys_tablespace;

-- 当前用户
SELECT current_user, current_database();
```

### 清理数据库

```sql
-- 删除表
DROP TABLE IF EXISTS employees CASCADE;

-- 删除模式下所有对象
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO SYSTEM;

-- 删除数据库
DROP DATABASE myapp;
```

---

## 14. 常见问题

### 无法连接数据库

```bash
# 检查实例状态
sys_isready -h localhost -p 54321

# 检查sys_hba.conf认证配置
# $KINGBASE_HOME/data/sys_hba.conf

# 确保有以下行（本地信任）
# local all all trust
# 或
# host all all 127.0.0.1/32 scram-sha-256
```

### 忘记SYSTEM密码

```bash
# 修改sys_hba.conf，设置本地信任认证
# local all all trust

# 重启数据库
sys_ctl restart -D $KINGBASE_HOME/data

# 重置密码
ksql -U SYSTEM -d test -c "ALTER USER SYSTEM WITH ENCRYPTED PASSWORD 'new_password';"

# 恢复sys_hba.conf为原配置，再重启
```

### 编码问题

```sql
-- 查看数据库编码
SELECT sys_encoding_to_char(encoding) FROM sys_database WHERE datname = 'myapp';

-- 创建UTF8数据库
CREATE DATABASE myapp WITH ENCODING 'UTF8';
```

### 表空间不足

```sql
-- 查看磁盘空间
df -h $KINGBASE_HOME/data

-- 创建新表空间
CREATE TABLESPACE data_tbs LOCATION '/data/kingbase/data';

-- 迁移表到新表空间
ALTER TABLE large_table SET TABLESPACE data_tbs;
```

---

## 15. 下一步学习

完成本教程后，建议按以下顺序深入学习：

1. **核心SQL参考** — 查阅 `ref/sql-syntax.md` 了解完整DDL/DML语法
2. **PL/SQL编程** — 查阅 `ref/plsql.md` 掌握存储过程和触发器
3. **数据类型** — 查阅 `ref/data-types.md` 了解所有可用类型
4. **系统设计** — 查阅 `ref/schema-design.md` 学习分区和索引策略
5. **Oracle兼容** — 查阅 `ref/oracle-compat.md` 了解迁移路径
6. **性能调优** — 切换到 `kes-performance` 技能
7. **运维管理** — 切换到 `kes-operations` 技能
