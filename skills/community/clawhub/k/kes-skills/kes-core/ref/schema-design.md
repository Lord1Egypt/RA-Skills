# KingbaseES 模式设计指南

包括表空间设计、分区表策略、索引设计和模式最佳实践。

## 1. 表空间设计

### 表空间概念

表空间控制数据库对象在磁盘上的物理存储位置，通过合理分配表空间可以优化I/O性能、管理存储增长和满足合规要求。

```sql
-- 查看现有表空间
SELECT
    spcname,
    spcowner::regrole AS owner,
    sys_size_pretty(sys_tablespace_size(spcname)) AS size,
    spclocation,
    spcoptions
FROM sys_tablespace;

-- 查看表空间使用量
SELECT
    spcname,
    sys_size_pretty(sys_tablespace_size(spcname)) AS total_size
FROM sys_tablespace
WHERE spcname NOT LIKE 'sys_%'
ORDER BY sys_tablespace_size(spcname) DESC;
```

### 创建表空间

```sql
-- 基本表空间
CREATE TABLESPACE data_tbs
OWNER SYSTEM
LOCATION '/data/kingbase/data';

-- 高性能表空间（SSD）
CREATE TABLESPACE fast_tbs
OWNER SYSTEM
LOCATION '/ssd/kingbase/fast';

-- 带选项的表空间
CREATE TABLESPACE archive_tbs
OWNER SYSTEM
LOCATION '/archive/kingbase/data'
OPTIONS (random_page_cost = 4.0, effective_io_concurrency = 1);

-- Oracle兼容模式表空间
CREATE TABLESPACE users_tbs
OWNER SYSTEM
LOCATION '/data/kingbase/users';
```

### 表空间使用策略

```sql
-- 1. 设置数据库默认表空间
ALTER DATABASE test SET TABLESPACE data_tbs;

-- 2. 设置用户默认表空间
ALTER USER app_user SET TABLESPACE data_tbs;

-- 3. 在特定表空间创建表
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    order_date DATE NOT NULL,
    amount DECIMAL(12, 2)
) TABLESPACE data_tbs;

-- 4. 在特定表空间创建索引
CREATE INDEX idx_orders_date ON orders(order_date)
TABLESPACE fast_tbs;

-- 5. 迁移表到表空间
ALTER TABLE orders SET TABLESPACE data_tbs;

-- 6. 迁移索引到表空间
ALTER INDEX idx_orders_date SET TABLESPACE fast_tbs;
```

### 表空间布局推荐

| 表空间 | 用途 | 存储介质 | 建议选项 |
|--------|------|---------|---------|
| `sys_default` | 系统对象 | 普通磁盘 | 默认 |
| `data_tbs` | 业务数据 | 高速磁盘 | 默认 |
| `index_tbs` | 索引文件 | SSD | `effective_io_concurrency = 200` |
| `wals_tbs` | WAL日志 | 独立磁盘 | 独立挂载 |
| `temp_tbs` | 临时文件 | 高速SSD | `random_page_cost = 1.0` |
| `archive_tbs` | 历史归档 | 大容量磁盘 | `random_page_cost = 4.0` |

```sql
-- 推荐布局示例
CREATE TABLESPACE index_tbs
OWNER SYSTEM
LOCATION '/ssd/kingbase/index'
OPTIONS (effective_io_concurrency = 200);

CREATE TABLESPACE temp_tbs
OWNER SYSTEM
LOCATION '/nvme/kingbase/temp'
OPTIONS (random_page_cost = 1.0, effective_io_concurrency = 200);

-- 将大表索引放到独立表空间
CREATE INDEX idx_large ON big_table(col) TABLESPACE index_tbs;
```

### 表空间配额管理

```sql
-- 设置用户表空间配额（单位KB）
ALTER USER app_user QUOTA 1048576 ON data_tbs;      -- 1GB
ALTER USER app_user QUOTA 524288 ON index_tbs;       -- 512MB
ALTER USER app_user QUOTA -1 ON temp_tbs;             -- 无限制

-- 查看配额
SELECT
    usename,
    spcname,
    CASE quota
        WHEN -1 THEN 'UNLIMITED'
        ELSE sys_size_pretty(quota * 8)
    END AS quota
FROM sys_user_tablespace_quota q
JOIN sys_tablespace t ON q.tablespace = t.oid;
```

### 删除表空间

```sql
-- 必须先清空所有对象
-- 1. 查找表空间中的对象
SELECT
    n.nspname AS schema,
    c.relname AS object,
    c.relkind AS type
FROM sys_class c
JOIN sys_namespace n ON c.relnamespace = n.oid
WHERE c.reltablespace = (SELECT oid FROM sys_tablespace WHERE spcname = 'target_tbs');

-- 2. 迁移或删除对象后
DROP TABLESPACE target_tbs;
```

---

## 2. 分区表设计

### 分区类型总览

| 分区类型 | 适用场景 | 特点 |
|---------|---------|------|
| RANGE | 时间序列、数值范围 | 按区间切分，支持自动时间分区 |
| LIST | 分类数据、地区枚举 | 按明确列表值切分 |
| HASH | 均匀分布、无自然分区键 | 哈希均匀分散，性能稳定 |
| 复合分区 | 多维度分区需求 | 一级+二级分区组合 |

### RANGE分区

```sql
-- 按时间RANGE分区
CREATE TABLE sales (
    id          BIGSERIAL,
    order_no    VARCHAR(50),
    customer_id INT,
    amount      DECIMAL(12, 2),
    order_date  DATE NOT NULL,
    created_at  TIMESTAMP DEFAULT NOW()
) PARTITION BY RANGE (order_date);

-- 创建月份分区
CREATE TABLE sales_202401 PARTITION OF sales
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE sales_202402 PARTITION OF sales
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
CREATE TABLE sales_202403 PARTITION OF sales
    FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');

-- 默认分区（不匹配任何范围的数据）
CREATE TABLE sales_default PARTITION OF sales DEFAULT;

-- 按年分区
CREATE TABLE sales_y2024 PARTITION OF sales
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
CREATE TABLE sales_y2025 PARTITION OF sales
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- 数值RANGE分区
CREATE TABLE scores (
    id INT,
    name VARCHAR(100),
    score INT
) PARTITION BY RANGE (score);

CREATE TABLE scores_low  PARTITION OF scores FOR VALUES FROM (0)   TO (60);
CREATE TABLE scores_mid  PARTITION OF scores FOR VALUES FROM (60)  TO (80);
CREATE TABLE scores_high PARTITION OF scores FOR VALUES FROM (80)  TO (101);
```

### LIST分区

```sql
-- 按地区LIST分区
CREATE TABLE employees (
    id    INT,
    name  VARCHAR(100),
    region VARCHAR(20),
    salary DECIMAL(10, 2)
) PARTITION BY LIST (region);

CREATE TABLE employees_east PARTITION OF employees
    FOR VALUES IN ('east', 'north_east');
CREATE TABLE employees_west PARTITION OF employees
    FOR VALUES IN ('west', 'north_west');
CREATE TABLE employees_south PARTITION OF employees
    FOR VALUES IN ('south', 'south_east', 'south_west');
CREATE TABLE employees_central PARTITION OF employees
    FOR VALUES IN ('central', 'mid_west');

-- 按状态LIST分区
CREATE TABLE orders (
    id      BIGINT,
    status  VARCHAR(20) NOT NULL,
    amount  DECIMAL(12, 2),
    created_at TIMESTAMP DEFAULT NOW()
) PARTITION BY LIST (status);

CREATE TABLE orders_active   PARTITION OF orders FOR VALUES IN ('pending', 'processing', 'shipped');
CREATE TABLE orders_completed PARTITION OF orders FOR VALUES IN ('completed', 'delivered');
CREATE TABLE orders_closed   PARTITION OF orders FOR VALUES IN ('cancelled', 'refunded');
```

### HASH分区

```sql
-- 按客户ID HASH分区
CREATE TABLE customer_records (
    customer_id   INT NOT NULL,
    record_type   VARCHAR(20),
    data          JSONB,
    created_at    TIMESTAMP DEFAULT NOW()
) PARTITION BY HASH (customer_id);

CREATE TABLE customer_records_0 PARTITION OF customer_records FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE customer_records_1 PARTITION OF customer_records FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE customer_records_2 PARTITION OF customer_records FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE customer_records_3 PARTITION OF customer_records FOR VALUES WITH (MODULUS 4, REMAINDER 3);

-- 按大字段HASH分区
CREATE TABLE documents (
    id      BIGSERIAL,
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
) PARTITION BY HASH (id);

CREATE TABLE documents_0 PARTITION OF documents FOR VALUES WITH (MODULUS 8, REMAINDER 0);
CREATE TABLE documents_1 PARTITION OF documents FOR VALUES WITH (MODULUS 8, REMAINDER 1);
CREATE TABLE documents_2 PARTITION OF documents FOR VALUES WITH (MODULUS 8, REMAINDER 2);
CREATE TABLE documents_3 PARTITION OF documents FOR VALUES WITH (MODULUS 8, REMAINDER 3);
CREATE TABLE documents_4 PARTITION OF documents FOR VALUES WITH (MODULUS 8, REMAINDER 4);
CREATE TABLE documents_5 PARTITION OF documents FOR VALUES WITH (MODULUS 8, REMAINDER 5);
CREATE TABLE documents_6 PARTITION OF documents FOR VALUES WITH (MODULUS 8, REMAINDER 6);
CREATE TABLE documents_7 PARTITION OF documents FOR VALUES WITH (MODULUS 8, REMAINDER 7);
```

### 复合分区

```sql
-- RANGE + LIST 复合分区
CREATE TABLE sales_region (
    id         BIGSERIAL,
    order_date DATE NOT NULL,
    region     VARCHAR(20) NOT NULL,
    amount     DECIMAL(12, 2)
) PARTITION BY RANGE (order_date)
SUBPARTITION BY LIST (region);

-- 一级：按年分区
CREATE TABLE sales_region_y2024 PARTITION OF sales_region
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01')
SUBPARTITION east  VALUES IN ('east', 'north_east'),
SUBPARTITION west   VALUES IN ('west', 'north_west'),
SUBPARTITION south  VALUES IN ('south', 'south_east', 'south_west');

CREATE TABLE sales_region_y2025 PARTITION OF sales_region
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01')
SUBPARTITION east  VALUES IN ('east', 'north_east'),
SUBPARTITION west   VALUES IN ('west', 'north_west'),
SUBPARTITION south  VALUES IN ('south', 'south_east', 'south_west');

-- RANGE + HASH 复合分区
CREATE TABLE logs (
    id      BIGSERIAL,
    log_time TIMESTAMP NOT NULL,
    level   VARCHAR(10),
    message TEXT
) PARTITION BY RANGE (log_time)
SUBPARTITION BY HASH (id);

CREATE TABLE logs_202401 PARTITION OF logs
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01')
SUBPARTITION h0 WITH (MODULUS 4, REMAINDER 0),
SUBPARTITION h1 WITH (MODULUS 4, REMAINDER 1),
SUBPARTITION h2 WITH (MODULUS 4, REMAINDER 2),
SUBPARTITION h3 WITH (MODULUS 4, REMAINDER 3);
```

### 分区管理

```sql
-- 查看分区结构
SELECT
    parent.relname AS parent_table,
    child.relname  AS partition_name,
    sys_get_expr(child.relpartbound, child.oid) AS partition_bound
FROM sys_inherits
JOIN sys_class parent ON sys_inherits.inhparent = parent.oid
JOIN sys_class child  ON sys_inherits.inhrelid = child.oid
WHERE parent.relname = 'sales';

-- 查看分区边界
SELECT
    relname,
    relpartbound
FROM sys_class
WHERE relpartbound IS NOT NULL
ORDER BY relname;

-- 添加新分区
CREATE TABLE sales_202504 PARTITION OF sales
    FOR VALUES FROM ('2025-04-01') TO ('2025-05-01') TABLESPACE data_tbs;

-- 删除分区（先 detach 再 DROP）
ALTER TABLE sales DETACH PARTITION sales_202401;
DROP TABLE sales_202401;

-- 批量创建分区（存储过程）
CREATE OR REPLACE PROCEDURE create_sales_partitions(
    p_start_date DATE,
    p_end_date DATE
)
LANGUAGE plsql
AS $$
DECLARE
    v_start DATE;
    v_end   DATE;
    v_name  VARCHAR(50);
BEGIN
    v_start := p_start_date;
    WHILE v_start < p_end_date LOOP
        v_end := v_start + INTERVAL '1 month';
        v_name := 'sales_' || TO_CHAR(v_start, 'YYYYMM');
        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS %I PARTITION OF sales
             FOR VALUES FROM (%L) TO (%L)',
            v_name, v_start, v_end
        );
        v_start := v_end;
    END LOOP;
END;
$$;

CALL create_sales_partitions('2025-01-01', '2026-01-01');
```

### 分区裁剪验证

```sql
-- 查看执行计划确认分区裁剪
EXPLAIN (COSTS OFF)
SELECT * FROM sales WHERE order_date >= '2025-01-01' AND order_date < '2025-02-01';

-- 期望输出应只扫描 sales_202501 分区
-- 如果出现 Append 多个分区，说明裁剪未生效

-- 强制指定分区查询
SELECT * FROM sales_202501 WHERE id = 12345;
```

### 分区表注意事项

```sql
-- 1. 分区键必须在PRIMARY KEY中
CREATE TABLE logs (
    id      BIGSERIAL,
    log_time TIMESTAMP NOT NULL,
    message TEXT,
    PRIMARY KEY (id, log_time)  -- 必须包含分区键
) PARTITION BY RANGE (log_time);

-- 2. 跨分区查询
SELECT
    order_date,
    COUNT(*),
    SUM(amount)
FROM sales
WHERE order_date >= '2024-01-01'
GROUP BY order_date;

-- 3. 分区表上创建索引（自动传播到所有分区）
CREATE INDEX idx_sales_date ON sales(order_date);
CREATE INDEX idx_sales_customer ON sales(customer_id);

-- 4. 为特定分区创建独立索引
CREATE INDEX idx_sales_recent ON sales_202501(customer_id, order_date);

-- 5. 分区统计信息
SELECT
    relname AS partition,
    n_live_tup AS rows,
    sys_size_pretty(sys_total_relation_size(relid)) AS size
FROM sys_stat_user_tables
WHERE relname LIKE 'sales_%'
ORDER BY relname;
```

---

## 3. 索引设计

### 索引类型选择

| 索引类型 | 适用场景 | 特点 |
|---------|---------|------|
| B-tree（默认） | 等值、范围、排序 | 通用，支持<, <=, =, >=, > |
| Hash | 纯等值查询 | 仅支持=，V9已废弃 |
| GiST | 全文检索、几何、范围类型 | 近似匹配，可扩展 |
| SP-GiST | 非平衡树结构数据 | 前缀树、四面体树 |
| GIN | 数组、JSON、全文检索 | 多值索引，支持@>, \|\|< |
| BRIN | 大容量有序数据 | 极小体积，块级压缩 |

### B-tree索引（默认）

```sql
-- 单列索引
CREATE INDEX idx_emp_dept ON employees(dept_id);

-- 复合索引（注意列顺序：选择性高的在前）
CREATE INDEX idx_emp_dept_status ON employees(dept_id, status);

-- 降序索引
CREATE INDEX idx_sales_date_desc ON sales(order_date DESC);

-- 唯一索引
CREATE UNIQUE INDEX idx_emp_email ON employees(LOWER(email));

-- 部分索引（带WHERE条件，减少索引体积）
CREATE INDEX idx_active_emp ON employees(name)
WHERE status = 'active';

CREATE INDEX idx_recent_orders ON orders(customer_id)
WHERE order_date >= CURRENT_DATE - INTERVAL '90 days';

-- 表达式索引
CREATE INDEX idx_emp_name_upper ON employees(UPPER(name));
CREATE INDEX idx_salary_range ON employees((salary / 1000));

-- 覆盖索引（INCLUDE非键列，避免回表）
CREATE INDEX idx_emp_cover ON employees(dept_id)
INCLUDE (name, salary, email);
```

### 复合索引设计原则

```sql
-- 最左前缀原则：WHERE dept_id = 10 AND status = 'active'
CREATE INDEX idx_emp_dept_status ON employees(dept_id, status);
-- 可用：WHERE dept_id = 10
-- 可用：WHERE dept_id = 10 AND status = 'active'
-- 不可用：WHERE status = 'active' 单独查询

-- 等值列在前，范围列在后
-- WHERE dept_id = 10 AND status = 'active' AND hire_date > '2024-01-01'
CREATE INDEX idx_emp_lookup ON employees(dept_id, status, hire_date);

-- 排序消除
-- WHERE dept_id = 10 ORDER BY salary DESC
CREATE INDEX idx_emp_dept_salary ON employees(dept_id, salary DESC);
```

### GIN索引（多值索引）

```sql
-- JSONB索引
CREATE INDEX idx_product_attrs ON products USING GIN(attributes);
-- 支持：@>, ?, ?&, ?|, @>操作符

-- JSONB表达式索引（针对特定路径）
CREATE INDEX idx_product_color ON products USING GIN((attributes->'color'));

-- 数组索引
CREATE INDEX idx_tag_items ON items USING GIN(tags);
-- 支持：@>（包含）, <@（被包含）, \|\|<（交集）

-- 全文检索GIN索引
ALTER TABLE articles ADD COLUMN search_vector TSVECTOR;
UPDATE articles SET search_vector = to_tsvector('simple', title || ' ' || content);
CREATE INDEX idx_article_search ON articles USING GIN(search_vector);

-- 触发器自动更新TSVECTOR
CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := to_tsvector('simple', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.content, ''));
    RETURN NEW;
END;
$$ LANGUAGE plsql;

CREATE TRIGGER trg_article_search_vector
    BEFORE INSERT OR UPDATE OF title, content ON articles
    FOR EACH ROW
    EXECUTE FUNCTION update_search_vector();
```

### GiST索引

```sql
-- 范围类型索引
CREATE INDEX idx_ip_range ON access_log USING GiST(ip_range);

-- 几何索引
CREATE INDEX idx_location ON places USING GiST(location);

-- 全文检索GiST（兼容旧版）
CREATE INDEX idx_article_gist ON articles USING GiST(search_vector);
```

### BRIN索引

```sql
-- 适用于物理有序的大表（如按时间写入的日志）
CREATE INDEX idx_log_time_brin ON access_log USING BRIN(log_time);

-- 自定义页面密度（越小体积越小，精度越低）
CREATE INDEX idx_log_time_brin2 ON access_log USING BRIN(log_time)
WITH (pages_per_range = 32);

-- 多列BRIN索引
CREATE INDEX idx_log_multi_brin ON access_log USING BRIN(log_time, user_id);
```

### 索引维护

```sql
-- 查看索引使用情况
SELECT
    schemaname,
    relname AS table_name,
    indexrelname AS index_name,
    idx_scan AS scans,
    idx_tup_read AS tuples_read,
    idx_tup_fetch AS tuples_fetched,
    sys_size_pretty(sys_relation_size(indexrelid)) AS index_size
FROM sys_stat_user_indexes
ORDER BY sys_relation_size(indexrelid) DESC;

-- 查找未使用的索引
SELECT
    relname AS table_name,
    indexrelname AS index_name,
    idx_scan,
    sys_size_pretty(sys_relation_size(indexrelid)) AS index_size
FROM sys_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE '%_pkey'
ORDER BY sys_relation_size(indexrelid) DESC;

-- 查找重复索引
SELECT
    a.indexrelid::regclass AS index1,
    b.indexrelid::regclass AS index2
FROM sys_stat_user_indexes a
JOIN sys_stat_user_indexes b ON a.relid = b.relid
JOIN sys_indexes ia ON a.indexrelid = ia.indexrelid
JOIN sys_indexes ib ON b.indexrelid = ib.indexrelid
WHERE a.indexrelid < b.indexrelid
  AND ia.indexdef LIKE '%' || ib.indexdef || '%';

-- 重建索引
REINDEX INDEX idx_emp_dept;
REINDEX TABLE employees;
REINDEX DATABASE test;

-- 在线重建索引（不阻塞写入）
REINDEX INDEX CONCURRENTLY idx_emp_dept;

-- 删除索引
DROP INDEX idx_emp_dept;
DROP INDEX CONCURRENTLY idx_emp_dept;  -- 不阻塞
```

### 索引统计信息

```sql
-- 索引大小排行
SELECT
    schemaname,
    relname,
    indexrelname,
    sys_size_pretty(sys_relation_size(indexrelid)) AS size,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM sys_stat_user_indexes
ORDER BY sys_relation_size(indexrelid) DESC
LIMIT 20;

-- 表 vs 索引大小对比
SELECT
    relname AS table_name,
    sys_size_pretty(sys_table_size(relid)) AS table_size,
    sys_size_pretty(sys_indexes_size(relid)) AS index_size,
    sys_size_pretty(sys_total_relation_size(relid)) AS total_size
FROM sys_stat_user_tables
ORDER BY sys_total_relation_size(relid) DESC
LIMIT 20;
```

---

## 4. 约束设计

### 主键策略

```sql
-- SERIAL自增主键
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

-- BIGSERIAL（大数据量）
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    order_date DATE
);

-- UUID主键
CREATE EXTENSION IF NOT EXISTS uuid-ossp;
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id INT,
    token VARCHAR(256)
);

-- 复合主键
CREATE TABLE order_items (
    order_id INT,
    item_id  INT,
    quantity INT,
    PRIMARY KEY (order_id, item_id)
);

-- 分区表主键（必须包含分区键）
CREATE TABLE logs (
    id      BIGINT,
    log_time TIMESTAMP NOT NULL,
    message TEXT,
    PRIMARY KEY (id, log_time)
) PARTITION BY RANGE (log_time);
```

### 外键设计

```sql
-- 基本外键
CREATE TABLE order_items (
    id INT PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity INT
);

-- 带删除策略的外键
CREATE TABLE profiles (
    id INT PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    bio TEXT
);

CREATE TABLE audit_logs (
    id INT PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100)
);

-- 复合外键
CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
);

-- 延迟约束（会话级）
SET CONSTRAINTS ALL DEFERRED;
-- 或定义时声明
CREATE TABLE transactions (
    id INT PRIMARY KEY,
    account_id INT REFERENCES accounts(id) DEFERRABLE INITIALLY DEFERRED,
    amount DECIMAL(12, 2)
);
```

### 检查约束

```sql
-- 列级检查约束
CREATE TABLE employees (
    id       INT PRIMARY KEY,
    name     VARCHAR(100) NOT NULL,
    email    VARCHAR(200) CHECK (email LIKE '%@%.%'),
    salary   DECIMAL(10, 2) CHECK (salary > 0),
    age      INT CHECK (age >= 18 AND age <= 150),
    status   VARCHAR(20) CHECK (status IN ('active', 'inactive', 'suspended')),
    hire_date DATE CHECK (hire_date <= CURRENT_DATE)
);

-- 表级检查约束
CREATE TABLE reservations (
    id         INT PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    end_time   TIMESTAMP NOT NULL,
    room_id    INT,
    CHECK (end_time > start_time),
    CHECK (EXTRACT(DAYOFWEEK FROM start_time) BETWEEN 2 AND 6)
);

-- 命名检查约束
CREATE TABLE products (
    id    INT PRIMARY KEY,
    price DECIMAL(10, 2) CONSTRAINT positive_price CHECK (price > 0),
    stock INT CONSTRAINT non_negative_stock CHECK (stock >= 0)
);

-- 添加/删除检查约束
ALTER TABLE employees ADD CONSTRAINT chk_salary_range CHECK (salary BETWEEN 0 AND 1000000);
ALTER TABLE employees DROP CONSTRAINT chk_salary_range;
```

### 唯一约束

```sql
-- 列唯一
CREATE TABLE users (
    id    INT PRIMARY KEY,
    email VARCHAR(200) UNIQUE,
    phone VARCHAR(20) UNIQUE
);

-- 复合唯一
CREATE TABLE user_roles (
    user_id INT,
    role_id INT,
    UNIQUE (user_id, role_id)
);

-- 部分唯一（实现条件唯一）
CREATE UNIQUE INDEX idx_emp_active_email ON employees(email)
WHERE status = 'active';

-- 表达式唯一
CREATE UNIQUE INDEX idx_user_lower_email ON users(LOWER(email));
```

---

## 5. 视图设计

### 基本视图

```sql
-- 简单视图
CREATE VIEW v_active_employees AS
SELECT id, name, email, dept_id, salary
FROM employees
WHERE status = 'active';

-- 复合视图
CREATE VIEW v_dept_summary AS
SELECT
    d.id AS dept_id,
    d.name AS dept_name,
    COUNT(e.id) AS employee_count,
    AVG(e.salary) AS avg_salary,
    MAX(e.salary) AS max_salary,
    MIN(e.salary) AS min_salary
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.id
GROUP BY d.id, d.name;
```

### 可更新视图

```sql
-- 简单视图自动可更新
CREATE VIEW v_active_orders AS
SELECT id, order_no, customer_id, amount, order_date
FROM orders
WHERE status = 'active';

-- 直接更新
UPDATE v_active_orders SET amount = 1500 WHERE id = 1;

-- 带检查选项
CREATE VIEW v_east_orders AS
SELECT * FROM orders WHERE region = 'east'
WITH CHECK OPTION;

-- INSTEAD OF触发器实现复杂视图更新
CREATE VIEW v_order_summary AS
SELECT
    o.id,
    o.order_no,
    c.name AS customer_name,
    o.amount,
    o.status
FROM orders o
JOIN customers c ON o.customer_id = c.id;

CREATE OR REPLACE FUNCTION fn_order_summary_update()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE orders SET
        amount = NEW.amount,
        status = NEW.status
    WHERE id = NEW.id;
    RETURN NEW;
END;
$$ LANGUAGE plsql;

CREATE TRIGGER trg_order_summary_update
    INSTEAD OF UPDATE ON v_order_summary
    FOR EACH ROW
    EXECUTE FUNCTION fn_order_summary_update();
```

### 物化视图

```sql
-- 创建物化视图
CREATE MATERIALIZED VIEW mv_sales_report AS
SELECT
    DATE_TRUNC('month', order_date) AS month,
    region,
    COUNT(*) AS order_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount
FROM orders
GROUP BY DATE_TRUNC('month', order_date), region;

-- 创建索引
CREATE INDEX idx_mv_sales_month ON mv_sales_report(month);

-- 刷新物化视图
REFRESH MATERIALIZED VIEW mv_sales_report;

-- 并发刷新（不阻塞查询，需先建唯一索引）
CREATE UNIQUE INDEX idx_mv_sales_uq ON mv_sales_report(month, region);
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_sales_report;

-- 带数据的物化视图替换
CREATE OR REPLACE MATERIALIZED VIEW mv_sales_report AS
SELECT ...;
```

---

## 6. 序列设计

### 序列创建与使用

```sql
-- 创建序列
CREATE SEQUENCE order_seq
START WITH 1000
INCREMENT BY 1
NO MINVALUE
NO MAXVALUE
CACHE 10;

-- 使用序列
CREATE TABLE orders (
    id INT PRIMARY KEY DEFAULT nextval('order_seq'),
    order_no VARCHAR(50)
);

-- 序列操作
SELECT nextval('order_seq');  -- 获取下一个值
SELECT currval('order_seq');  -- 获取当前值
SELECT lastval();             -- 获取最后使用的序列值

-- 修改序列
ALTER SEQUENCE order_seq INCREMENT BY 5;
ALTER SEQUENCE order_seq RESTART WITH 1;

-- 序列关联
ALTER SEQUENCE order_seq OWNED BY orders.id;

-- SERIAL自动创建序列
CREATE TABLE users (
    id SERIAL PRIMARY KEY  -- 自动创建 users_id_seq 序列
);
```

### 分布式ID生成

```sql
-- GAP-free序列（用于发票号等连续编号）
CREATE EXTENSION IF NOT EXISTS gapless_seq;

-- 基于序列的分片ID
CREATE OR REPLACE FUNCTION generate_shard_id(
    p_shard_id INT,
    p_sequence REGCLASS
) RETURNS BIGINT AS $$
DECLARE
    v_seq_val BIGINT;
BEGIN
    v_seq_val := nextval(p_sequence);
    RETURN (p_shard_id::BIGINT << 40) + v_seq_val;
END;
$$ LANGUAGE plsql;
```

---

## 7. 模式最佳实践

### 命名规范

```sql
-- 表名：小写下划线分隔，名词复数
CREATE TABLE order_items (...);
CREATE TABLE customer_addresses (...);

-- 视图：v_ 前缀
CREATE VIEW v_active_orders (...);

-- 物化视图：mv_ 前缀
CREATE MATERIALIZED VIEW mv_sales_report (...);

-- 序列：_seq 后缀
CREATE SEQUENCE order_id_seq;

-- 索引：idx_ 前缀 + 表名 + 列名
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- 唯一索引：idx_uq_ 前缀
CREATE UNIQUE INDEX idx_uq_users_email ON users(email);

-- 约束：chk_/fk_/uq_ 前缀
ALTER TABLE orders ADD CONSTRAINT chk_order_amount CHECK (amount > 0);
ALTER TABLE orders ADD CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(id);

-- 触发器：trg_ 前缀
CREATE TRIGGER trg_order_audit AFTER INSERT ON orders ...;

-- 函数：fn_ 前缀
CREATE FUNCTION fn_calc_tax(...) ...;

-- 过程：proc_ 或 sp_ 前缀
CREATE PROCEDURE proc_monthly_report(...) ...;
```

### 表设计检查清单

```sql
-- 1. 每张表必须有主键
-- 2. 适当使用NOT NULL约束
-- 3. 外键关联必须有索引
-- 4. 检查约束验证业务规则
-- 5. 大表考虑分区
-- 6. 高频查询列建立索引
-- 7. 审计字段：created_at, updated_at, created_by
-- 8. 软删除使用is_deleted标志

-- 完整表示例
CREATE TABLE products (
    id            BIGSERIAL PRIMARY KEY,
    sku           VARCHAR(50) UNIQUE NOT NULL,
    name          VARCHAR(200) NOT NULL,
    category_id   INT REFERENCES categories(id) ON DELETE SET NULL,
    price         DECIMAL(10, 2) NOT NULL CONSTRAINT chk_price_positive CHECK (price > 0),
    cost          DECIMAL(10, 2) NOT NULL CONSTRAINT chk_cost_positive CHECK (cost >= 0),
    stock         INT NOT NULL DEFAULT 0 CONSTRAINT chk_stock_non_neg CHECK (stock >= 0),
    status        VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'discontinued')),
    attributes    JSONB,
    description   TEXT,
    is_deleted    BOOLEAN NOT NULL DEFAULT FALSE,
    created_at    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by    INT REFERENCES users(id),
    version       INT NOT NULL DEFAULT 1
);

-- 索引
CREATE INDEX idx_products_category ON products(category_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_products_status ON products(status) WHERE is_deleted = FALSE;
CREATE INDEX idx_products_sku ON products(sku);

-- 自动更新updated_at
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at := NOW();
    NEW.version := OLD.version + 1;
    RETURN NEW;
END;
$$ LANGUAGE plsql;

CREATE TRIGGER trg_product_update_time
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamp();
```

### 性能设计原则

1. **窄表优于宽表**：减少每行数据量，提高缓存效率
2. **适当冗余**：OLAP场景可适度冗余，避免多表JOIN
3. **分区大表**：超过1亿行的表优先考虑分区
4. **索引克制**：每个索引都有写入代价，只创建必要的索引
5. **数据类型最小化**：用INT不必用BIGINT，用VARCHAR(N)不用TEXT
6. **避免NULL热点**：高频查询列设置NOT NULL和默认值
7. **JSONB用于灵活字段**：不常查询的属性用JSONB存储
