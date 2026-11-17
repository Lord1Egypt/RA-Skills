# KingbaseES SQL完整语法参考

包含DDL/DML/DCL/事务控制完整语法，Oracle兼容语法对照，数组操作和序列管理。

## 1. DDL — 数据定义语言

### 1.1 数据库操作

```sql
-- 创建数据库
CREATE DATABASE db_name
    [OWNER owner_name]
    [ENCODING encoding]
    [LC_COLLATE lc_collate]
    [LC_CTYPE lc_ctype]
    [TEMPLATE template]
    [TABLESPACE tablespace]
    [CONNECTION LIMIT connlimit];

-- 示例
CREATE DATABASE test
    OWNER SYSTEM
    ENCODING 'UTF8'
    TEMPLATE template0
    TABLESPACE sys_default
    CONNECTION LIMIT -1;

-- 修改数据库
ALTER DATABASE db_name RENAME TO new_name;
ALTER DATABASE db_name RENAME TO new_name;
ALTER DATABASE db_name ALTER SET TABLESPACE new_tablespace;
ALTER DATABASE db_name CONNECTION LIMIT 100;

-- 删除数据库
DROP DATABASE [IF EXISTS] db_name;

-- 查看数据库列表
SELECT datname, datowner, encoding, datconnlimit
FROM sys_database
ORDER BY datname;
```

### 1.2 模式(Schema)操作

```sql
-- 创建模式
CREATE SCHEMA schema_name [AUTHORIZATION owner_name];

-- 创建模式并同时创建对象
CREATE SCHEMA schema_name AUTHORIZATION owner_name
    CREATE TABLE t1 (id INT)
    CREATE VIEW v1 AS SELECT * FROM t1;

-- 修改模式
ALTER SCHEMA schema_name RENAME TO new_name;
ALTER SCHEMA schema_name OWNER TO new_owner;

-- 删除模式
DROP SCHEMA schema_name [CASCADE | RESTRICT];

-- 设置搜索路径
SET search_path TO "$user", public, my_schema;
-- 持久化
ALTER DATABASE db_name SET search_path TO "$user", public;
ALTER USER user_name SET search_path TO "$user", public;
```

### 1.3 表操作

```sql
-- 基本建表
CREATE [TEMPORARY | TEMP | UNLOGGED] TABLE [IF NOT EXISTS] table_name (
    column_name data_type [column_constraint [...]],
    ...
    [table_constraint [...]]
) [TABLESPACE tablespace_name];

-- 完整示例
CREATE TABLE employees (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    email           VARCHAR(200) UNIQUE,
    dept_id         INT REFERENCES departments(id) ON DELETE SET NULL,
    salary          DECIMAL(10, 2) CHECK (salary > 0 AND salary <= 9999999),
    hire_date       DATE DEFAULT CURRENT_DATE,
    status          CHAR(1) DEFAULT 'A' CHECK (status IN ('A', 'I', 'T')),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version         INT DEFAULT 1
) TABLESPACE data_tbs;

-- 约束命名
CREATE TABLE orders (
    id      SERIAL,
    cust_id INT,
    amount  DECIMAL(12, 2),
    CONSTRAINT pk_orders PRIMARY KEY (id),
    CONSTRAINT fk_cust FOREIGN KEY (cust_id) REFERENCES customers(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_amount CHECK (amount > 0),
    CONSTRAINT uq_cust_order UNIQUE (cust_id, id)
);

-- 临时表
CREATE TEMPORARY TABLE temp_results (
    id INT,
    result TEXT
) ON COMMIT DELETE ROWS;  -- 或 PRESERVE ROWS / DROP TABLE

-- 基于查询建表
CREATE TABLE sales_archive AS
SELECT * FROM sales WHERE sold_at < '2024-01-01';

-- CREATE TABLE ... LIKE (复制结构)
CREATE TABLE employees_backup (LIKE employees INCLUDING ALL);

-- 修改表
ALTER TABLE table_name ADD COLUMN column_name data_type [constraint];
ALTER TABLE table_name DROP COLUMN [IF EXISTS] column_name [CASCADE | RESTRICT];
ALTER TABLE table_name ALTER COLUMN column_name TYPE new_type [USING expression];
ALTER TABLE table_name ALTER COLUMN column_name SET DEFAULT default_expr;
ALTER TABLE table_name ALTER COLUMN column_name DROP DEFAULT;
ALTER TABLE table_name ALTER COLUMN column_name SET NOT NULL;
ALTER TABLE table_name ALTER COLUMN column_name DROP NOT NULL;
ALTER TABLE table_name RENAME COLUMN old_name TO new_name;
ALTER TABLE table_name RENAME TO new_table_name;
ALTER TABLE table_name OWNER TO new_owner;
ALTER TABLE table_name SET SCHEMA new_schema;
ALTER TABLE table_name SET TABLESPACE new_tablespace;

-- 约束管理
ALTER TABLE table_name ADD CONSTRAINT constraint_name constraint_def;
ALTER TABLE table_name DROP CONSTRAINT [IF EXISTS] constraint_name [CASCADE | RESTRICT];
ALTER TABLE table_name ALTER CONSTRAINT constraint_name ...;

-- 启用/禁用触发器
ALTER TABLE table_name ENABLE TRIGGER [trigger_name | ALL | USER];
ALTER TABLE table_name DISABLE TRIGGER [trigger_name | ALL | USER];

-- 删除表
DROP TABLE [IF EXISTS] table_name [, ...] [CASCADE | RESTRICT];
```

### 1.4 索引操作

```sql
-- 基本索引
CREATE [UNIQUE] INDEX [CONCURRENTLY] [IF NOT EXISTS] index_name
ON table_name [USING method] (column [OPCLASS] [ASC | DESC] [NULLS {FIRST | LAST}] [, ...])
[WITH (storage_parameter = value [, ...])]
[TABLESPACE tablespace_name]
[WHERE predicate];

-- B-Tree索引（默认）
CREATE INDEX idx_emp_dept ON employees(dept_id);

-- 唯一索引
CREATE UNIQUE INDEX idx_emp_email ON employees(LOWER(email));

-- 复合索引
CREATE INDEX idx_emp_dept_status ON employees(dept_id, status);

-- 部分索引
CREATE INDEX idx_active_emp ON employees(name) WHERE status = 'A';

-- 表达式索引
CREATE INDEX idx_salary_range ON employees((salary / 1000));

-- 哈希索引
CREATE INDEX idx_email_hash ON employees USING HASH(email);

-- GiN索引（用于数组/JSON）
CREATE INDEX idx_prod_attr ON products USING GIN(attributes);

-- GiST索引（用于全文检索/几何）
CREATE INDEX idx_content_gist ON documents USING GIST(to_tsvector('chinese', content));

-- BRIN索引（大型有序表）
CREATE INDEX idx_sales_date ON sales USING BRIN(sold_at);

-- 并发创建（不锁表）
CREATE INDEX CONCURRENTLY idx_large_table ON large_table(column_name);

-- 修改/删除索引
ALTER INDEX index_name RENAME TO new_name;
ALTER INDEX index_name SET TABLESPACE new_tablespace;
ALTER INDEX index_name SET (fillfactor = 70);
DROP INDEX [IF EXISTS] index_name [CONCURRENTLY];
```

### 1.5 视图操作

```sql
-- 创建视图
CREATE [OR REPLACE] [TEMPORARY] VIEW [IF NOT EXISTS] view_name [(column_list)]
AS query
[WITH [CASCADED | LOCAL] CHECK OPTION];

-- 示例
CREATE VIEW v_emp_dept AS
SELECT e.id, e.name, e.salary, d.name AS dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.id
WHERE e.status = 'A';

-- 可更新视图
CREATE VIEW v_active_emp AS
SELECT id, name, email, dept_id, salary
FROM employees
WHERE status = 'A'
WITH CHECK OPTION;

-- 物化视图
CREATE MATERIALIZED VIEW [IF NOT EXISTS] mv_name AS query;
REFRESH MATERIALIZED VIEW mv_name [CONCURRENTLY];
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_name;  -- 需唯一索引
CREATE UNIQUE INDEX ON mv_name(id);

-- 修改/删除视图
ALTER VIEW view_name RENAME TO new_name;
ALTER VIEW view_name RENAME COLUMN old_name TO new_name;
DROP VIEW [IF EXISTS] view_name [CASCADE | RESTRICT];
DROP MATERIALIZED VIEW [IF EXISTS] mv_name [CASCADE | RESTRICT];
```

### 1.6 序列操作

```sql
-- 创建序列
CREATE SEQUENCE [IF NOT EXISTS] seq_name
    [AS data_type]
    [INCREMENT BY increment]
    [MINVALUE minval | NO MINVALUE]
    [MAXVALUE maxval | NO MAXVALUE]
    [START WITH start]
    [CACHE cache]
    [[NO] CYCLE]
    [[NO] OWNED BY table.column | NONE];

-- 示例
CREATE SEQUENCE emp_seq
    START WITH 1000
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 999999
    CACHE 10
    NO CYCLE;

-- 使用序列
SELECT nextval('emp_seq');       -- 取值并递增
SELECT currval('emp_seq');       -- 当前会话最后一次取值
SELECT lastval();                -- 本会话最后一次nextval的值
SELECT setval('emp_seq', 5000);  -- 设置值
SELECT setval('emp_seq', 5000, true);  -- 设置值并标记is_called=true

-- 修改序列
ALTER SEQUENCE seq_name RESTART [WITH start];
ALTER SEQUENCE seq_name INCREMENT BY 5;
ALTER SEQUENCE seq_name MAXVALUE 9999999;

-- 删除序列
DROP SEQUENCE [IF EXISTS] seq_name [CASCADE | RESTRICT];

-- SERIAL快捷方式
-- SERIAL4 = INT + 序列, SERIAL8 = BIGINT + 序列
CREATE TABLE t (id SERIAL PRIMARY KEY);  -- 自动创建序列
-- 等价于:
-- CREATE SEQUENCE t_id_seq START 1 INCREMENT 1 NO MINVALUE MAXVALUE 2147483647;
-- ALTER TABLE t ALTER id SET DEFAULT nextval('t_id_seq');
-- ALTER SEQUENCE t_id_seq OWNED BY t.id;

-- 标识列（SQL标准方式）
CREATE TABLE t (
    id INT GENERATED ALWAYS AS IDENTITY,
    id2 INT GENERATED BY DEFAULT AS IDENTITY START WITH 100
);
--  Override: INSERT INTO t (id) OVERRIDING SYSTEM VALUE VALUES (1);
```

### 1.7 表空间操作

```sql
-- 创建表空间
CREATE TABLESPACE tablespace_name
    [OWNER owner_name]
    LOCATION 'directory_path'
    [OPTIONS (tablespace_option = value [, ...])];

CREATE TABLESPACE data_tbs
    OWNER SYSTEM
    LOCATION '/data/kingbase/data'
    OPTIONS (random_page_cost = 1.1);

-- 修改表空间
ALTER TABLESPACE tablespace_name RENAME TO new_name;
ALTER TABLESPACE tablespace_name OWNER TO new_owner;
ALTER TABLESPACE tablespace_name RESET (random_page_cost);
ALTER TABLESPACE tablespace_name SET (random_page_cost = 2.0);

-- 删除表空间（必须先清空）
DROP TABLESPACE [IF EXISTS] tablespace_name;
```

### 1.8 分区表

```sql
-- RANGE分区
CREATE TABLE sales (
    id      BIGSERIAL,
    amount  DECIMAL(12, 2),
    sold_at DATE NOT NULL
) PARTITION BY RANGE (sold_at);

CREATE TABLE sales_y2024 PARTITION OF sales
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01')
    TABLESPACE data_tbs_2024;

CREATE TABLE sales_y2025 PARTITION OF sales
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- LIST分区
CREATE TABLE regions (
    id      INT,
    name    VARCHAR(100),
    region  VARCHAR(20) NOT NULL
) PARTITION BY LIST (region);

CREATE TABLE regions_east PARTITION OF regions
    FOR VALUES IN ('east', 'north-east');

CREATE TABLE regions_west PARTITION OF regions
    FOR VALUES IN ('west', 'north-west');

-- HASH分区
CREATE TABLE hash_table (
    id    INT,
    data  TEXT
) PARTITION BY HASH (id);

CREATE TABLE hash_p0 PARTITION OF hash_table FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE hash_p1 PARTITION OF hash_table FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE hash_p2 PARTITION OF hash_table FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE hash_p3 PARTITION OF hash_table FOR VALUES WITH (MODULUS 4, REMAINDER 3);

-- 复合分区
CREATE TABLE复合分区 (
    id      BIGSERIAL,
    region  VARCHAR(20),
    sold_at DATE
) PARTITION BY RANGE (sold_at) SUBPARTITION BY LIST (region);

-- 分区管理
-- 附加分区
ALTER TABLE parent ATTACH PARTITION child FOR VALUES FROM (...) TO (...);

--  detach分区
ALTER TABLE parent DETACH PARTITION child [CONCURRENTLY];

-- 查看分区信息
SELECT
    parent,
    child,
    expr,
    moduls,
    remainder,
    range
FROM sys_inherits;
```

### 1.9 其他DDL

```sql
-- 同义词
CREATE SYNONYM syn_name FOR object_name;
DROP SYNONYM [IF EXISTS] syn_name;

-- 转换(字符集)
CREATE CONVERSION conversion_name FOR source_encoding TO dest_encoding FROM func_name;
DROP CONVERSION [IF EXISTS] conversion_name;

-- 文本搜索配置
CREATE TEXT SEARCH CONFIGURATION config_name (PARSER = parser_name);
ALTER TEXT SEARCH CONFIGURATION config_name
    ADD MAPPING FOR word WITH simple;

-- 领域(Domain)
CREATE DOMAIN phone_num AS VARCHAR(20)
    CHECK (VALUE ~ '^[0-9]{11}$');
DROP DOMAIN [IF EXISTS] phone_num;
```

## 2. DML — 数据操纵语言

### 2.1 INSERT

```sql
-- 单行写入
INSERT INTO table_name [(column_list)] VALUES (value_list);

-- 多行写入
INSERT INTO employees (name, dept_id, salary) VALUES
    ('张三', 10, 15000),
    ('李四', 20, 18000),
    ('王五', 10, 12000);

-- 从查询写入
INSERT INTO target_table (col1, col2)
SELECT col1, col2 FROM source_table WHERE condition;

-- 批量写入（VALUES构造）
INSERT INTO employees (name, dept_id)
SELECT * FROM (VALUES
    ('赵六', 30),
    ('孙七', 30)
) AS t(name, dept_id);

-- UPSERT（冲突处理）
INSERT INTO employees (id, name, salary, version)
VALUES (1, '张三', 16000, 2)
ON CONFLICT (id) DO UPDATE SET
    name    = EXCLUDED.name,
    salary  = EXCLUDED.salary,
    version = employees.version + 1,
    updated_at = NOW();

-- 多列冲突
INSERT INTO t (a, b, c) VALUES (...)
ON CONFLICT (a, b) DO NOTHING;

-- RETURNING子句
INSERT INTO employees (name, dept_id) VALUES ('张三', 10)
RETURNING id, name, created_at;
```

### 2.2 UPDATE

```sql
-- 基本更新
UPDATE table_name
SET column = value [, ...]
[FROM source_tables]
[WHERE condition]
[RETURNING output_list];

-- 单表更新
UPDATE employees
SET salary = salary * 1.1, updated_at = NOW()
WHERE dept_id = 10;

-- 多表关联更新
UPDATE employees e
SET salary = salary * d.bonus_rate
FROM departments d
WHERE e.dept_id = d.id AND d.name = '工程';

-- 子查询更新
UPDATE employees
SET salary = (SELECT avg_salary FROM dept_stats WHERE dept_id = employees.dept_id)
WHERE dept_id IN (SELECT dept_id FROM dept_stats);

-- 批量条件更新
UPDATE employees
SET status = CASE
    WHEN salary > 20000 THEN 'senior'
    WHEN salary > 10000 THEN 'mid'
    ELSE 'junior'
END
WHERE updated_at < NOW() - INTERVAL '7 days';

-- CTE更新
WITH updated AS (
    UPDATE employees
    SET salary = salary * 1.1
    WHERE dept_id = 10
    RETURNING id, name, salary
)
SELECT * FROM updated;
```

### 2.3 DELETE

```sql
-- 基本删除
DELETE FROM table_name [WHERE condition] [RETURNING output_list];

-- 条件删除
DELETE FROM employees WHERE status = 'I' AND hire_date < '2020-01-01';

-- 关联删除
DELETE FROM employees
WHERE dept_id IN (SELECT id FROM departments WHERE budget = 0);

-- 使用CTE删除
WITH to_delete AS (
    SELECT id FROM employees WHERE status = 'I' LIMIT 1000
)
DELETE FROM employees WHERE id IN (SELECT id FROM to_delete)
RETURNING id, name;

-- 清空表
TRUNCATE TABLE table_name [RESTART IDENTITY] [CASCADE];
TRUNCATE TABLE orders, order_items RESTART IDENTITY CASCADE;
```

### 2.4 SELECT

```sql
-- 完整SELECT语法
SELECT [ALL | DISTINCT [ON (column_list)]]
    select_list
[INTO [TEMPORARY] target_table]
[FROM from_clause]
[WHERE where_condition]
[GROUP BY [ALL | DISTINCT] column_list [HAVING condition]]
[WINDOW window_name AS (window_def)]
[ORDER BY column [ASC | DESC] [NULLS {FIRST | LAST}] [, ...]]
[LIMIT count [OFFSET start]]
[FETCH {FIRST | NEXT} [count] {ROW | ROWS} {ONLY | WITH TIES}]
[FOR {UPDATE | NO KEY UPDATE | SHARE | KEY SHARE} [OF table_list] [NOWAIT | SKIP LOCKED]];

-- DISTINCT ON
SELECT DISTINCT ON (dept_id) name, salary
FROM employees
ORDER BY dept_id, salary DESC;

-- LATERAL子查询
SELECT d.name, sub.top_sal
FROM departments d,
LATERAL (
    SELECT MAX(e.salary) AS top_sal
    FROM employees e
    WHERE e.dept_id = d.id
) sub;

-- FULL OUTER JOIN
SELECT a.name, b.name
FROM table_a a
FULL OUTER JOIN table_b b ON a.id = b.a_id;

-- CROSS JOIN
SELECT * FROM table_a CROSS JOIN table_b;

-- 多表JOIN
SELECT e.name, d.name AS dept, p.name AS project
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id
INNER JOIN project_assignments pa ON e.id = pa.emp_id
LEFT JOIN projects p ON pa.project_id = p.id
WHERE e.status = 'A';
```

### 2.5 MERGE（V9支持）

```sql
MERGE INTO target USING source ON condition
WHEN MATCHED THEN
    UPDATE SET column = value [, ...] [WHERE condition]
WHEN NOT MATCHED THEN
    INSERT [(column_list)] VALUES (value_list) [WHERE condition]
[WHEN NOT MATCHED BY SOURCE THEN
    DELETE [WHERE condition]];

-- 示例
MERGE INTO emp_sal e
USING salary_updates s ON e.id = s.emp_id
WHEN MATCHED THEN
    UPDATE SET salary = s.new_salary, updated_at = NOW()
    WHERE e.salary != s.new_salary
WHEN NOT MATCHED THEN
    INSERT (id, name, salary) VALUES (s.emp_id, s.name, s.new_salary);
```

### 2.6 聚合函数

```sql
-- 基本聚合
SELECT
    COUNT(*),
    COUNT(DISTINCT dept_id),
    SUM(salary),
    AVG(salary),
    MIN(salary),
    MAX(salary),
    STDDEV(salary),
    VARIANCE(salary)
FROM employees;

-- GROUP BY + HAVING
SELECT dept_id, COUNT(*) AS cnt, AVG(salary) AS avg_sal
FROM employees
GROUP BY dept_id
HAVING COUNT(*) > 5 AND AVG(salary) > 10000
ORDER BY avg_sal DESC;

-- 滚动聚合
SELECT
    dept_id,
    name,
    salary,
    SUM(salary) OVER (PARTITION BY dept_id) AS dept_total,
    AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg,
    RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rank,
    ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS row_num,
    DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dense_rank,
    NTILE(4) OVER (ORDER BY salary) AS quartile,
    PERCENT_RANK() OVER (PARTITION BY dept_id ORDER BY salary) AS pct_rank,
    CUME_DIST() OVER (ORDER BY salary) AS cume_dist,
    LEAD(name, 1) OVER (PARTITION BY dept_id ORDER BY salary) AS next_colleague,
    LAG(name, 1) OVER (PARTITION BY dept_id ORDER BY salary) AS prev_colleague,
    FIRST_VALUE(name) OVER (PARTITION BY dept_id ORDER BY salary DESC) AS top_earner,
    LAST_VALUE(name) OVER (PARTITION BY dept_id ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS bottom_earner
FROM employees;
```

### 2.7 子查询与CTE

```sql
-- 标量子查询
SELECT name, salary, (SELECT AVG(salary) FROM employees WHERE dept_id = e.dept_id) AS dept_avg
FROM employees e;

-- EXISTS子查询
SELECT * FROM departments d
WHERE EXISTS (
    SELECT 1 FROM employees e WHERE e.dept_id = d.id AND e.salary > 20000
);

-- 普通CTE
WITH dept_stats AS (
    SELECT dept_id, COUNT(*) AS cnt, AVG(salary) AS avg_sal
    FROM employees
    GROUP BY dept_id
)
SELECT d.name, ds.cnt, ds.avg_sal
FROM departments d
JOIN dept_stats ds ON d.id = ds.dept_id;

-- 多CTE
WITH
    active_emps AS (
        SELECT * FROM employees WHERE status = 'A'
    ),
    dept_stats AS (
        SELECT dept_id, AVG(salary) AS avg_sal FROM active_emps GROUP BY dept_id
    )
SELECT ae.name, ae.salary, ds.avg_sal
FROM active_emps ae
JOIN dept_stats ds ON ae.dept_id = ds.dept_id;

-- 递归CTE
WITH RECURSIVE org_tree AS (
    -- 锚点
    SELECT id, name, manager_id, 1 AS depth, ARRAY[id] AS path
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    -- 递归
    SELECT e.id, e.name, e.manager_id, ot.depth + 1, ot.path || e.id
    FROM employees e
    JOIN org_tree ot ON e.manager_id = ot.id
    WHERE NOT (ot.path && ARRAY[e.id])  -- 防环
)
SELECT * FROM org_tree ORDER BY depth, name;

-- 可写CTE（V9）
WITH deleted AS (
    DELETE FROM temp_table WHERE created_at < NOW() - INTERVAL '7 days'
    RETURNING *
)
SELECT count(*) FROM deleted;
```

### 2.8 UNION / INTERSECT / EXCEPT

```sql
-- UNION（去重）/ UNION ALL（保留重复）
SELECT name, email FROM employees
UNION ALL
SELECT name, email FROM contractors;

-- INTERSECT（交集）
SELECT id FROM table_a
INTERSECT
SELECT id FROM table_b;

-- EXCEPT（差集）
SELECT id FROM table_a
EXCEPT
SELECT id FROM table_b;
```

### 2.9 类型转换

```sql
-- CAST（SQL标准）
SELECT CAST('123' AS INT), CAST(123 AS VARCHAR);

-- ::操作符
SELECT '123'::INT, 123::VARCHAR, '2024-01-01'::DATE;

-- TO_CHAR / TO_DATE / TO_TIMESTAMP
SELECT TO_CHAR(NOW(), 'YYYY-MM-DD HH24:MI:SS');
SELECT TO_DATE('2024-01-15', 'YYYY-MM-DD');
SELECT TO_TIMESTAMP('2024-01-15 10:30:00', 'YYYY-MM-DD HH24:MI:SS');

-- TO_NUMBER（Oracle兼容）
SELECT TO_NUMBER('1,234.56', '999,999.99');
```

## 3. DCL — 数据控制语言

### 3.1 用户/角色管理

```sql
-- 创建角色
CREATE ROLE role_name [LOGIN | NOLOGIN]
    [SUPERUSER | NOSUPERUSER]
    [CREATEDB | NOCREATEDB]
    [CREATEROLE | NOCREATEROLE]
    [INHERIT | NOINHERIT]
    [CONNECTION LIMIT connlimit]
    [VALID UNTIL 'timestamp']
    [IN ROLE role_list]
    [ROLE role_list]
    [PASSWORD 'password' | ENCRYPTED PASSWORD 'password'];

-- 创建用户（等价于 ROLE + LOGIN）
CREATE USER user_name WITH ENCRYPTED PASSWORD 'password' CONNECTION LIMIT 50;

-- 修改角色
ALTER ROLE role_name [LOGIN | NOLOGIN];
ALTER ROLE role_name WITH SUPERUSER;
ALTER ROLE role_name RENAME TO new_name;
ALTER ROLE role_name WITH ENCRYPTED PASSWORD 'new_password';
ALTER ROLE role_name CONNECTION LIMIT 20;
ALTER ROLE role_name VALID UNTIL '2026-12-31';
ALTER ROLE role_name SET parameter TO value;
ALTER ROLE role_name ACCOUNT LOCK;
ALTER ROLE role_name ACCOUNT UNLOCK;

-- 删除角色
DROP ROLE [IF EXISTS] role_name;

-- 角色成员管理
GRANT role_name TO target_role [ADMIN OPTION];
REVOKE role_name FROM target_role;

-- 所有权转移
REASSIGN OWNED BY old_role TO new_role;
DROP OWNED BY old_role;
```

### 3.2 权限管理

```sql
-- 授予权限
GRANT {privilege_list | ALL PRIVILEGES} ON object_type object_name TO grantee [GRANT OPTION];

-- 数据库级
GRANT CONNECT ON DATABASE db_name TO user_name;
GRANT TEMPORARY ON DATABASE db_name TO user_name;

-- Schema级
GRANT USAGE ON SCHEMA schema_name TO user_name;
GRANT CREATE ON SCHEMA schema_name TO user_name;

-- 表级
GRANT SELECT, INSERT, UPDATE ON table_name TO user_name;
GRANT ALL PRIVILEGES ON table_name TO user_name;

-- 列级
GRANT SELECT(id, name) ON table_name TO user_name;
GRANT UPDATE(salary) ON table_name TO user_name;

-- 批量授权
GRANT SELECT ON ALL TABLES IN SCHEMA public TO user_name;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO user_name;

-- 函数级
GRANT EXECUTE ON FUNCTION function_name TO user_name;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO user_name;

-- 表空间级
GRANT CREATE ON TABLESPACE tablespace_name TO user_name;

-- 默认权限（新对象自动授权）
ALTER DEFAULT PRIVILEGES [FOR ROLE role_name] [IN SCHEMA schema_name]
    GRANT privilege ON object_type TO grantee;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO reporter;

ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE ON TABLES TO app_user;

-- 撤销权限
REVOKE [GRANT OPTION FOR] {privilege_list | ALL PRIVILEGES} ON object FROM grantee;

REVOKE SELECT ON table_name FROM user_name;
REVOKE ALL ON table_name FROM user_name;
REVOKE ALL PRIVILEGES ON DATABASE db_name FROM PUBLIC;
```

### 3.3 权限查询

```sql
-- 查看表权限
SELECT grantee, table_name, privilege_type, is_grantable
FROM sys_table_privileges
WHERE table_name = 'employees'
ORDER BY grantee, privilege_type;

-- 查看列权限
SELECT grantee, table_name, column_name, privilege_type
FROM sys_column_privileges
WHERE table_name = 'employees';

-- 查看Schema权限
SELECT grantee, table_schema, privilege_type
FROM sys_schema_privileges
WHERE table_schema = 'public';

-- 查看角色成员
SELECT
    r.rolname AS role,
    m.rolname AS member,
    am.admin_member
FROM sys_auth_members am
JOIN sys_authid r ON am.roleid = r.oid
JOIN sys_authid m ON am.member = m.oid;
```

## 4. 事务控制

### 4.1 基本事务

```sql
-- 开始事务
BEGIN [WORK | TRANSACTION]
    [ISOLATION LEVEL {READ UNCOMMITTED | READ COMMITTED | REPEATABLE READ | SERIALIZABLE}]
    [{READ WRITE | READ ONLY}]
    [DEFERRABLE];

-- 提交
COMMIT [WORK];

-- 回滚
ROLLBACK [WORK];

-- 保存点
SAVEPOINT savepoint_name;
ROLLBACK TO [SAVEPOINT] savepoint_name;
RELEASE SAVEPOINT savepoint_name;
```

### 4.2 事务示例

```sql
-- 完整事务
BEGIN;

SAVEPOINT sp1;

UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
UPDATE accounts SET balance = balance + 1000 WHERE id = 2;

-- 如果有问题，回滚到保存点
-- ROLLBACK TO sp1;

COMMIT;

-- 只读事务
BEGIN READ ONLY;
SELECT * FROM large_report;
COMMIT;

-- 可串行化事务
BEGIN ISOLATION LEVEL SERIALIZABLE;
-- 操作...
COMMIT;
```

### 4.3 锁机制

```sql
-- 表级锁
LOCK TABLE table_name IN {ACCESS SHARE | ROW SHARE | ROW EXCLUSIVE | SHARE UPDATE EXCLUSIVE | SHARE | SHARE ROW EXCLUSIVE | EXCLUSIVE | ACCESS EXCLUSIVE} MODE
[NOWAIT];

-- 行级锁（SELECT FOR UPDATE）
SELECT * FROM employees WHERE dept_id = 10 FOR UPDATE;
SELECT * FROM employees WHERE dept_id = 10 FOR SHARE;
SELECT * FROM employees WHERE dept_id = 10 FOR NO KEY UPDATE;
SELECT * FROM employees WHERE dept_id = 10 FOR KEY SHARE;

-- 不等待
SELECT * FROM employees WHERE id = 1 FOR UPDATE NOWAIT;

-- 跳过被锁行
SELECT * FROM employees WHERE dept_id = 10 FOR UPDATE SKIP LOCKED;

--  advisory锁（应用级锁）
SELECT sys_advisory_lock(key INT);
SELECT sys_advisory_unlock(key INT);
SELECT sys_try_advisory_lock(key INT);
```

### 4.4 咨询锁

```sql
-- 会话级咨询锁
SELECT sys_advisory_lock(12345);           -- 获取锁（阻塞）
SELECT sys_try_advisory_lock(12345);       -- 尝试获取（不阻塞，返回boolean）
SELECT sys_advisory_unlock(12345);         -- 释放锁

-- 数据库级咨询锁
SELECT sys_advisory_lock(hashtext('my_resource'));
SELECT sys_advisory_unlock(hashtext('my_resource'));
```

## 5. Oracle兼容语法

### 5.1 函数对照

```sql
-- 空值处理
-- Oracle: NVL(col, default)
-- KES标准: COALESCE(col, default)
SELECT COALESCE(salary, 0) FROM employees;
-- Oracle兼容模式下NVL也可用

-- 条件表达式
-- Oracle: DECODE(x, a, b, c, default)
-- KES标准: CASE WHEN x=a THEN b WHEN x=c THEN d ELSE default END
SELECT CASE dept_id WHEN 10 THEN '工程' WHEN 20 THEN '销售' ELSE '其他' END FROM employees;
-- Oracle兼容模式下DECODE也可用

-- 空值比较
-- Oracle: NVL2(expr, if_not_null, if_null)
-- KES标准: CASE WHEN expr IS NOT NULL THEN ... END
```

### 5.2 层级查询

```sql
-- Oracle: START WITH ... CONNECT BY PRIOR
-- KES标准: WITH RECURSIVE

-- Oracle写法:
-- SELECT * FROM employees
-- START WITH manager_id IS NULL
-- CONNECT BY PRIOR id = manager_id;

-- KES标准写法:
WITH RECURSIVE emp_tree AS (
    SELECT id, name, manager_id, 0 AS lvl
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, et.lvl + 1
    FROM employees e JOIN emp_tree et ON e.manager_id = et.id
)
SELECT * FROM emp_tree;
```

### 5.3 序列语法

```sql
-- Oracle: seq.NEXTVAL, seq.CURRVAL
-- KES标准: nextval('seq'), currval('seq')

SELECT nextval('emp_seq');  -- KES标准
SELECT emp_seq.NEXTVAL;     -- Oracle兼容模式
```

### 5.4 分页

```sql
-- Oracle: ROWNUM / FETCH FIRST
-- KES标准: LIMIT / OFFSET

SELECT * FROM employees LIMIT 20 OFFSET 40;

-- Oracle兼容FETCH语法（也支持）
SELECT * FROM employees ORDER BY id FETCH FIRST 20 ROWS ONLY;
SELECT * FROM employees ORDER BY id OFFSET 40 ROWS FETCH NEXT 20 ROWS ONLY;
```

### 5.5 双引号行为

```sql
-- 标准模式: 双引号标识符保持大小写
CREATE TABLE "MyTable" ("Id" INT);  -- 必须用双引号访问

-- Oracle兼容模式: 双引号标识符转大写
CREATE TABLE "MyTable" ("Id" INT);  -- 等价于 MYTABLE / ID
```

### 5.6 Oracle类型映射

| Oracle类型 | KES等价类型 | 说明 |
|-----------|------------|------|
| VARCHAR2(n) | VARCHAR(n) | Oracle兼容模式可直接使用VARCHAR2 |
| NUMBER(p,s) | DECIMAL(p,s) / NUMERIC(p,s) | INTEGER当p<=0且s=0 |
| NUMBER | DECIMAL(38,0) | 无精度指定 |
| NVARCHAR2(n) | VARCHAR(n) |  Unicode字符串 |
| RAW(n) | BYTEA | 二进制数据 |
| LONG | TEXT | 已废弃，建议用TEXT |
| CLOB | TEXT | 兼容模式支持CLOB关键字 |
| BLOB | BYTEA | 二进制大对象 |
| TIMESTAMP | TIMESTAMP WITHOUT TIME ZONE | 或带TIME ZONE变体 |
| INTERVAL | INTERVAL | 间隔类型 |

## 6. 数组操作

### 6.1 数组基础

```sql
-- 数组字面量
SELECT ARRAY[1, 2, 3]::INT[];
SELECT ARRAY[['a', 'b'], ['c', 'd']]::VARCHAR[][];

-- 多维数组
SELECT ARRAY[[1, 2], [3, 4]]::INT[][];

-- 访问元素（下标从1开始）
SELECT (ARRAY[10, 20, 30])[1];  -- 返回10
SELECT (ARRAY[10, 20, 30])[2];  -- 返回20

-- 修改元素
SELECT ARRAY_REPLACE(ARRAY[1, 2, 3], 2, 99);  -- {1,99,3}

-- 数组长度
SELECT ARRAY_LENGTH(ARRAY[1, 2, 3], 1);  -- 3

-- 数组维度
SELECT ARRAY_DIMS(ARRAY[[1,2],[3,4]]);  -- [1:2][1:2]
```

### 6.2 数组操作符

```sql
-- 数组连接
SELECT ARRAY[1, 2] || ARRAY[3, 4];  -- {1,2,3,4}
SELECT 1 || ARRAY[2, 3];             -- {1,2,3}

-- 元素检查
SELECT 1 = ANY(ARRAY[1, 2, 3]);     -- true
SELECT 1 = ALL(ARRAY[1, 2, 3]);     -- false
SELECT 5 IS NULL::INT = ANY(ARRAY[1, 2, 3]);  -- false

-- IN + ANY
SELECT * FROM employees WHERE dept_id = ANY(ARRAY[10, 20, 30]);

-- 数组包含
SELECT ARRAY[1, 2] <@ ARRAY[1, 2, 3];  -- true (子数组)
SELECT ARRAY[1, 2] && ARRAY[2, 3];     -- true (有重叠)
```

### 6.3 数组函数

```sql
-- 数组拼接
SELECT array_cat(ARRAY[1, 2], ARRAY[3, 4]);  -- {1,2,3,4}

-- 数组去重
SELECT array_agg(DISTINCT x) FROM unnest(ARRAY[1, 1, 2, 3]) AS t(x);

-- 展开数组
SELECT unnest(ARRAY[1, 2, 3]);
-- 结果: 1, 2, 3 (多行)

-- 带序号展开
SELECT * FROM unnest(ARRAY[1, 2, 3]) WITH ORDINALITY AS t(val, idx);

-- 多个数组同时展开
SELECT * FROM unnest(ARRAY['a', 'b', 'c'], ARRAY[1, 2, 3]) AS t(letter, num);

-- 数组聚合
SELECT array_agg(id ORDER BY id) FROM employees WHERE dept_id = 10;
SELECT array_agg(DISTINCT dept_id) FROM employees;

-- 字符串转数组
SELECT string_to_array('a,b,c', ',');  -- {a,b,c}

-- 数组转字符串
SELECT array_to_string(ARRAY['a', 'b', 'c'], ', ');  -- "a, b, c"

-- 数组切片
SELECT (ARRAY[1, 2, 3, 4, 5])[2:4];  -- {2,3,4}

-- 数组长度
SELECT cardinality(ARRAY[1, 2, 3]);  -- 3
```

## 7. 常见模式

### 7.1 分页

```sql
-- 偏移分页
SELECT * FROM employees ORDER BY id LIMIT 20 OFFSET 40;

-- 键集分页（高性能）
SELECT * FROM employees
WHERE id > 1000
ORDER BY id
LIMIT 20;

-- Oracle兼容FETCH
SELECT * FROM employees ORDER BY id OFFSET 40 ROWS FETCH NEXT 20 ROWS ONLY;
```

### 7.2 条件聚合

```sql
SELECT
    dept_id,
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE status = 'A') AS active_count,
    AVG(salary) FILTER (WHERE status = 'A') AS active_avg_sal,
    MAX(salary) FILTER (WHERE dept_id = 10) AS dept10_max_sal
FROM employees
GROUP BY dept_id;
```

### 7.3 交叉表

```sql
-- 使用CASE实现透视
SELECT
    dept_id,
    SUM(CASE WHEN EXTRACT(MONTH FROM hire_date) = 1 THEN 1 ELSE 0 END) AS jan,
    SUM(CASE WHEN EXTRACT(MONTH FROM hire_date) = 2 THEN 1 ELSE 0 END) AS feb,
    SUM(CASE WHEN EXTRACT(MONTH FROM hire_date) = 3 THEN 1 ELSE 0 END) AS mar
FROM employees
GROUP BY dept_id;
```

### 7.4 数据去重

```sql
-- 保留一行
DELETE FROM employees
WHERE ctid NOT IN (
    SELECT MIN(ctid) FROM employees GROUP BY email
);

-- 使用窗口函数
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn
    FROM employees
)
DELETE FROM employees WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
```

### 7.5 临时数据操作

```sql
-- 创建临时表
CREATE TEMP TABLE temp_analysis ON COMMIT DROP AS
SELECT dept_id, COUNT(*), AVG(salary)
FROM employees
GROUP BY dept_id;

-- 带索引的临时表
CREATE TEMP TABLE temp_work (
    id INT PRIMARY KEY,
    data TEXT
) ON COMMIT PRESERVE ROWS;
CREATE INDEX ON temp_work(data);
```
