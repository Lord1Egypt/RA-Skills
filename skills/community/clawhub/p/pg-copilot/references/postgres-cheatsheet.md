# PostgreSQL 速查表

## 数据类型

### 数值
| 类型 | 说明 |
|------|------|
| `SERIAL` | 自增整数 |
| `BIGSERIAL` | 大自增整数 |
| `DECIMAL(p,s)` | 精确数值 |
| `REAL` | 浮点数 |
| `DOUBLE PRECISION` | 双精度浮点 |

### 字符串
| 类型 | 说明 |
|------|------|
| `VARCHAR(n)` | 变长 |
| `CHAR(n)` | 定长 |
| `TEXT` | 无限长 |

### 时间
| 类型 | 说明 |
|------|------|
| `TIMESTAMP` | 日期+时间 |
| `DATE` | 日期 |
| `TIME` | 时间 |
| `INTERVAL` | 时间间隔 |

### JSON
| 类型 | 说明 |
|------|------|
| `JSON` | 文本 JSON |
| `JSONB` | 二进制 JSON（推荐） |

---

## 常用函数

### 字符串
```sql
-- 拼接
SELECT 'Hello' || ' World';
SELECT CONCAT('Hello', ' World');

-- 大小写
SELECT UPPER('hello');
SELECT LOWER('HELLO');

-- 子串
SELECT SUBSTRING('Hello World', 1, 5);  -- Hello

-- 替换
SELECT REPLACE('Hello World', 'World', 'PostgreSQL');
```

### 时间
```sql
-- 当前时间
SELECT NOW();
SELECT CURRENT_DATE;
SELECT CURRENT_TIMESTAMP;

-- 格式化
SELECT TO_CHAR(NOW(), 'YYYY-MM-DD HH24:MI:SS');

-- 解析
SELECT TO_DATE('2024-01-01', 'YYYY-MM-DD');
SELECT TO_TIMESTAMP('2024-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');

-- 日期间隔
SELECT NOW() + INTERVAL '7 days';
SELECT AGE(NOW(), birth_date);
```

### 聚合
```sql
SELECT COUNT(*), SUM(amount), AVG(amount), MAX(amount), MIN(amount)
FROM orders;

-- 带条件
SELECT COUNT(*) FILTER (WHERE status = 'paid') FROM orders;
```

### JSON
```sql
-- 创建
SELECT '{"name": "John", "age": 30}'::jsonb;

-- 提取
SELECT '{"name": "John"}'::jsonb ->> 'name';  -- John
SELECT '{"user": {"name": "John"}}'::jsonb #>> '{user,name}';

-- 操作
SELECT jsonb_set('{"a": 1}'::jsonb, '{b}', '2');
SELECT '["a", "b", "c"]'::jsonb - 1;  -- 删除元素
```

---

## 索引类型

| 类型 | 使用场景 |
|------|---------|
| `B-tree` | 默认，等值/范围查询 |
| `Hash` | 简单等值查询 |
| `GIN` | JSON/数组/全文搜索 |
| `GiST` | 地理数据、范围 |
| `BRIN` | 大表时间序列 |

### 创建索引
```sql
-- 普通索引
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- 唯一索引
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- 复合索引
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- 部分索引
CREATE INDEX idx_orders_paid ON orders(user_id) WHERE status = 'paid';

-- GIN 索引 (JSON)
CREATE INDEX idx_products_data ON products USING GIN(data);

-- BRIN 索引 (时序)
CREATE INDEX idx_logs_created ON logs USING BRIN(created_at);
```

---

## 窗口函数

### 基础
```sql
-- 行号
SELECT ROW_NUMBER() OVER (ORDER BY created_at DESC) AS row_num, *
FROM orders;

-- 排名
SELECT RANK() OVER (ORDER BY score DESC) AS rank, *
FROM users;

-- 并列排名
SELECT DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank, *
FROM users;
```

### 偏移
```sql
-- 前一行
SELECT LAG(amount) OVER (ORDER BY created_at) AS prev_amount FROM orders;

-- 后一行
SELECT LEAD(amount) OVER (ORDER BY created_at) AS next_amount FROM orders;

-- N 行前/后
SELECT amount - LAG(amount, 2) OVER (ORDER BY created_at) AS diff_2 FROM orders;
```

### 分区
```sql
-- 按用户分组
SELECT 
    user_id,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS user_order
FROM orders;

-- 累计
SELECT 
    amount,
    SUM(amount) OVER (ORDER BY created_at) AS running_total
FROM orders;
```

---

## CTE (WITH)

### 基础
```sql
WITH active_users AS (
    SELECT * FROM users WHERE status = 'active'
)
SELECT * FROM active_users WHERE created_at > '2024-01-01';
```

### 多次引用
```sql
WITH 
    total AS (SELECT SUM(amount) AS sum FROM orders),
    count AS (SELECT COUNT(*) AS cnt FROM orders)
SELECT sum/cnt AS avg FROM total, count;
```

### 递归
```sql
WITH RECURSIVE org AS (
    -- 起点：CEO
    SELECT id, name, manager_id, 1 AS level
    FROM employees WHERE manager_id IS NULL
    
    UNION ALL
    
    -- 递归：下属
    SELECT e.id, e.name, e.manager_id, o.level + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT * FROM org;
```

---

## 常见模式

### 分页
```sql
-- 方法1: OFFSET/LIMIT
SELECT * FROM orders 
ORDER BY created_at DESC 
LIMIT 10 OFFSET 20;

-- 方法2: 游标 (更高效)
SELECT * FROM orders 
WHERE id > 100 
ORDER BY id 
LIMIT 10;
```

### upsert
```sql
INSERT INTO users (email, name) VALUES ('john@example.com', 'John')
ON CONFLICT (email) 
DO UPDATE SET name = EXCLUDED.name;
```

### 批量插入
```sql
INSERT INTO orders (user_id, amount) VALUES 
(1, 100),
(2, 200),
(3, 300);
```

### 返回修改的行
```sql
-- INSERT 返回
INSERT INTO orders (user_id, amount) VALUES (1, 100)
RETURNING id, created_at;

-- UPDATE 返回
UPDATE orders SET status = 'paid' WHERE id = 1
RETURNING *;

-- DELETE 返回
DELETE FROM orders WHERE id = 1
RETURNING *;
```

---

## 性能优化

### EXPLAIN ANALYZE
```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) 
SELECT * FROM orders WHERE user_id = 1;
```

### 关键指标
- **Seq Scan** vs **Index Scan**：顺序扫描说明没有索引
- **Bitmap**： bitmap 扫描适合多列
- **Nested Loop**：小表可以，大表要避免
- **Hash Join**：适合大表等值连接
- **Sort / Hash**：内存排序还是磁盘

### 优化建议
1. **避免 SELECT ***：只查需要的字段
2. **合理使用索引**：WHERE/JOIN 字段加索引
3. **EXPLAIN 分析**：检查执行计划
4. **VACUUM ANALYZE**：更新统计信息
5. **连接池**：用 PgBouncer

---

## 常用配置

### 连接
```sql
-- 查看连接数
SELECT count(*) FROM pg_stat_activity;

-- 最大连接数
SHOW max_connections;
```

### 表大小
```sql
-- 查看表大小
SELECT pg_size_pretty(pg_total_relation_size('orders'));

-- 查看索引大小
SELECT pg_size_pretty(pg_indexes_size('orders'));

-- 查看所有表大小
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

---

*更多请参考官方文档：https://www.postgresql.org/docs/*
