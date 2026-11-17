# KingbaseES 索引设计策略指南

## 索引基本原则

### 索引是什么

索引是数据库中用于快速查找数据的数据结构，类似于书的目录。通过索引，数据库可以在无需扫描整张表的情况下快速定位数据。

**优点**
- 查询速度显著提升
- 支持排序和分组
- 减少磁盘I/O

**缺点**
- 增加存储空间
- INSERT/UPDATE/DELETE性能下降
- 维护开销（需要额外页面）

---

## 索引类型选择

### 1. B-Tree索引

**适用场景**：
- 等值查询（`=`）
- 范围查询（`>`, `<`, `BETWEEN`）
- 排序/分组（`ORDER BY`, `GROUP BY`）
- JOIN条件
- 精确的前导LIKE（`LIKE 'value%'`）

**SQL示例**
```sql
-- 创建B-Tree索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status_date ON users(status, created_at);  -- 复合索引
```

**性能特点**
- 所有操作效率高
- 准确的预计成本
- 最常用的索引类型

**限制**
- 不支持部分索引
- 不支持函数索引
- WHERE子句中的每列都可以用在B-Tree索引中

---

### 2. 哈希索引（Hash Index）

**适用场景**：
- 等值查询为主（`=`）
- 全等查询
- JOIN条件（高选择性列）

**特点**
- 仅支持`=`查询
- 查询效率极高（O(1)）
- 不支持范围查询和排序

**使用方式**
```sql
-- 在KingbaseES中，B-Tree索引本身包含哈希功能
-- 如果需要纯哈希索引，可通过GIN索引的哈希扩展实现（需额外配置）
```

**权衡**
- 适用范围窄
- 不支持排序
- 不支持范围查询

---

### 3. GIN索引

**适用场景**：
- JSON列/JSONB列
- 全文搜索（full-text search）
- 数组列
- 多个`IN`条件

**SQL示例**
```sql
-- 创建GIN索引
CREATE INDEX idx_products_tags ON products USING gin(tags gin_trgm_ops);
CREATE INDEX idx_users_profile ON users USING gin(profile jsonb_ops);

-- 全文搜索
CREATE INDEX idx_articles_content ON articles USING gin(content gin_trgm_ops);
```

**使用Gin扩展**
```sql
-- 安装扩展（如果未安装）
CREATE EXTENSION IF NOT EXISTS btree_gin;

-- 配置gin_trgm扩展
CREATE EXTENSION IF NOT EXISTS gin_trgm;

-- 使用
SELECT * FROM articles WHERE content LIKE '%workflow%';  -- gin_trgm加速
```

**特点**
- 支持复杂的包含查询
- 查询速度极快
- 占用空间较大

---

### 4. GiST索引

**适用场景**：
- 空间查询
- 全文搜索
- 范围值（支持不等性查询）
- 稀疏数据

**SQL示例**
```sql
-- GiST索引（空间查询）
CREATE INDEX idx_locations ON locations USING gist(location);

-- GaIN索引（混合类型）
CREATE INDEX idx_documents_metadata ON documents USING gin(metadata jsonb_ops, content gin_trgm_ops);
```

**特点**
- 支持范围查询
- 查询效率中等
- 适合多模数据

---

### 5. BRIN索引

**适用场景**：
- 超大表（数百万行以上）
- 数据具有序列性（天然排序）
- 读取大量数据，写极少

**SQL示例**
```sql
-- 创建BRIN索引（只需100字节）
CREATE INDEX idx_logs_create_date ON logs USING brin(create_time);
CREATE INDEX idx_sensor_readings_value ON sensor_readings USING brin(value);
```

**特点**
- 占用空间极小（通常几百字节）
- 仅检查表中的一小部分
 - 仅适合区间扫描和顺序查询

**内存开销**
```sql
-- 查看索引大小
SELECT
    schemaname,
    tablename,
    indexname,
    sys_size_pretty(sys_relation_size(idx), 'MB')
FROM sys_stats_user_indexes;
```

---

## 复合索引设计

### 原则1：最左前缀

**复合索引**：`CREATE INDEX idx ON table(col1, col2, col3);`

**可用查询类型**
```sql
-- ✅ 使用col1
SELECT * FROM table WHERE col1 = 'value';

-- ✅ 使用col1, col2
SELECT * FROM table WHERE col1 = 'value' AND col2 = 'value2';

-- ✅ 使用col1, col2, col3
SELECT * FROM table WHERE col1 = 'value' AND col2 = 'value2' AND col3 = 'value3';

-- ✅ 使用col1, col2，支持范围查询
SELECT * FROM table WHERE col1 = 'value' AND col2 > '2025-01-01';
```

**不可用查询类型**
```sql
-- ❌ 使用col2（丢失col1优势）
SELECT * FROM table WHERE col2 = 'value2';

-- ❌ 使用col3（丢失col1, col2优势）
SELECT * FROM table WHERE col3 = 'value3';
```

### 原则2：选择性高的列在前，低选择性列在后

**选择性（Cardinality）**
- 高选择性col1：约50%行唯一
- 低选择性col2：约1%行唯一

**推荐顺序**
```sql
-- ✅ 高选择性在前
CREATE INDEX idx_selective ON table(high_selective_col, low_selective_col);

-- ❌ 低选择性在前
CREATE INDEX idx_non_selective ON table(low_selective_col, high_selective_col);
```

**选择性判断**
```sql
-- 估算列的选择性
SELECT
    relname as table,
    attname as column,
    ginistats_values as possible_values
FROM sys_stats_user_columns
WHERE tablename = 'your_table' AND attname = 'your_column';
```

### 原则3：WHERE, JOIN, ORDER BY混合使用

```sql
-- 场景：WHERE条件、JOIN条件和排序混合
-- 表结构：orders (customer_id, product_id, order_date, status)

-- ❌ 单一索引覆盖不了全部查询
CREATE INDEX idx_orders ON orders((customer_id, product_id));  -- 覆盖WHERE和JOIN，但是没有order_date

-- ✅ 复合索引：customer_id(高选择性, WHERE/JOIN) + order_date(范围, ORDER BY)
CREATE INDEX idx_orders_opt ON orders(customer_id, order_date);

-- 另外一个重排序查询
-- 只需在status列建索引
CREATE INDEX idx_orders_status ON orders(status);
```

**实际应用示例**
```sql
-- 查询1：WHERE customer_id = ? AND order_date > ?
SELECT ... FROM orders WHERE customer_id = 100 AND order_date > '2025-01-01';

-- 查询2：JOIN AND filter
SELECT * FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.status = 'pending';

-- 查询3：ORDER BY
SELECT * FROM orders WHERE customer_id = 100 ORDER BY order_date DESC;

-- 设计策略：
-- 1. 复合索引：customer_id, order_date (覆盖查询1和3)
-- 2. 单列索引：status (覆盖查询2)
CREATE INDEX idx_orders_composite ON orders(customer_id, order_date)
WHERE status IN ('pending', 'processing');  -- 部分索引
```

---

## 索引设计最佳实践

### 1. 为WHERE、JOIN和ORDER BY创建索引

**错误示范**
```sql
-- ❌ 只有SELECT语句中没有WHERE条件
SELECT * FROM users;

-- ✅ 为实际查询条件创建索引
CREATE INDEX idx_users_email ON users(email);
```

**检查方法**
```sql
-- 查看WHERE条件
SELECT
    query
FROM sys_stat_statements
WHERE query ILIKE '% WHERE %'
LIMIT 10;

-- 查看JOIN条件
SELECT
    query
FROM sys_stat_statements
WHERE query ILIKE '% JOIN %'
LIMIT 10;
```

### 2. 尽量不索引低选择性列

**低选择性列特点**
- 状态列（status, active, inactive）
- 性别（gender）
- 布尔值
- 元数据（created_at的时区字段等）

**错误示例**
```sql
-- ❌ 为低选择性列创建索引无用
CREATE INDEX idx_users_gender ON users(gender);

-- ✅ 索引高选择性列
CREATE INDEX idx_users_email ON users(email);
```

### 3. 覆盖索引（Covering Index）

**目标**：索引包含所有查询所需的列，避免回表

```sql
-- 查询
SELECT id, name, status FROM users WHERE email = 'test@example.com';

-- 传统索引（需要回表）
CREATE INDEX idx_users_email ON users(email);

-- 覆盖索引（不需要回表）
CREATE INDEX idx_users_covering ON users(email) INCLUDE (id, name, status);

-- EXPLAIN验证（期望 Index Only Scan）
EXPLAIN SELECT id, name, status FROM users WHERE email = 'test@example.com';
```

**注意**：KingbaseES使用`INCLUDE`子句实现覆盖索引（Oracle兼容模式）

### 4. 部分索引

**适用场景**：
- 只索引活跃数据
- 特定业务条件的组合
- 避免索引膨胀

```sql
-- ✅ 只索引活跃用户
CREATE INDEX idx_users_active ON users(email) WHERE status = 'active';

-- ✅ 只索引订单记录
CREATE INDEX idx_orders_past ON orders(customer_id, order_date)
WHERE status IN ('cancelled', 'completed');

-- 索引空间小（只索引10%数据）
SELECT sys_size_pretty(sys_relation_size('idx_users_active'), 'MB');
-- 输出：~28MB（对比全表3GB）
```

### 5. 函数索引

**Oracle兼容模式**：使用函数作为索引列

```sql
-- ❌ 查询使用函数，索引失效
SELECT * FROM logs WHERE DATE(created_at) = '2025-01-01';

-- ✅ 创建函数索引
CREATE INDEX idx_logs_date ON logs(DATE(created_at));
CREATE INDEX idx_logs_trim_name ON users(TRIM(name));

-- 查询可以正常使用索引
SELECT * FROM logs WHERE created_at >= '2025-01-01' AND created_at < '2025-01-02';
```

**原则**：索引列的函数必须与查询中的函数一致

```sql
-- 传统模式（PostgreSQL兼容）
CREATE INDEX idx_ln_upper ON users(LOWER(name));

-- 查询不做函数转换即可使用
SELECT * FROM users WHERE LOWER(name) = 'test';
```

### 6. 避免在JOIN列上使用函数

**错误示例**
```sql
-- ❌ 排序后JOIN
SELECT * FROM table1 a
JOIN table2 b ON UPPER(a.name) = UPPER(b.name);

-- ✅ 避免函数，使用传统JOIN
SELECT * FROM table1 a
JOIN table2 b ON a.name COLLATE "POSIX" = b.name COLLATE "POSIX";
```

---

## 特殊场景索引策略

### 1. 日志表索引

**场景**：每日日志，需要按时间范围查询

**方案1：BRIN索引（适用海量日志）**
```sql
-- 只索引时间列
CREATE INDEX idx_logs_time ON logs USING brin(create_time);

-- 占用空间极小，适合每天数百万行日志
```

**方案2：复合索引**
```sql
-- 按时间+日志类型索引
CREATE INDEX idx_logs_time_type ON logs(create_time, log_type)
INCLUDE (message, level);

-- 部分索引（只索引错误日志）
CREATE INDEX idx_logs_errors ON logs(create_time)
INCLUDE (message)
WHERE level IN ('ERROR', 'FATAL');
```

### 2. 维护表索引（INSERT频繁，SELECT少）

**策略**：极简索引

```sql
-- ❌ 维护表建太多索引
CREATE INDEX ON maintenance_log (created_at);
CREATE INDEX ON maintenance_log (worker_id);
CREATE INDEX ON maintenance_log (status);
CREATE INDEX ON maintenance_log (task_type);

-- ✅ 只保留必要索引
CREATE INDEX idx_maintenance_status ON maintenance_log(status) WHERE status = 'pending';
```

**建议**：
- SELECT < 10次/秒的表少建索引
- 维护表中只索引WHERE条件高的列

### 3. 大表JOIN优化索引

**场景**：大表JOIN小表

```sql
-- 表：orders (1000万行), customers (10万行)
-- 查询：JOIN orders c ON c.customer_id = o.customer_id WHERE o.status = 'active'

-- ❌ 两个表都没有索引
SELECT *
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.status = 'active';

-- ✅ 小表customers建主键索引，orders建复合索引
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);

-- 或使用部分索引
CREATE INDEX idx_orders_active ON orders(customer_id, status)
WHERE status = 'active';
```

### 4. 分区表索引策略

**策略1：每个分区独立索引**
```sql
-- 建分区表
CREATE TABLE sales (
    id SERIAL,
    amount DECIMAL,
    sale_date DATE
) PARTITION BY RANGE (sale_date);

-- 为每个分区建索引
CREATE INDEX idx_sales_date_sale_date ON sales_202501 PARTITION BY RANGE (sale_date);
CREATE INDEX idx_sales_date_sale_amount ON sales_202501 PARTITION BY RANGE (sale_date, amount);
```

**策略2：全局索引（索引跨分区）**
```sql
-- 如果查询跨分区，使用全局索引
CREATE INDEX idx_sales_date_global ON sales(sale_date);
```

---

## 索引性能评估

### 查找索引使用情况

```sql
-- 查看所有索引的使用情况
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan as scan_count,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetch
FROM sys_stat_user_indexes
ORDER BY idx_scan ASC;

-- 识别未使用的索引
SELECT
    schemaname,
    tablename,
    indexname,
    sys_size_pretty(sys_relation_size(idx::regclass)) as size
FROM sys_stat_user_indexes
WHERE idx_scan = 0;

-- 识别建立预估成本高的索引
SELECT
    schemaname,
    tablename,
    indexname,
    relpages as pages,
    reltuples as tuples,
    sys_size_pretty(sys_relation_size(idx::regclass)) as size
FROM sys_stat_user_indexes
WHERE relpages > 50000  -- 筛选大索引
ORDER BY pages DESC;
```

### 分析特定查询的索引使用

```sql
-- 添加MONITOR HINT追踪执行计划
SELECT /*+MONITOR*/ *
FROM orders
WHERE customer_id = 100 AND status = 'active';

-- 查看监控历史
SELECT *
FROM v$active_sql_monitor
WHERE sql_id = 'your_sql_id';
```

---

## 索引维护

### 1. 删除未使用索引

```sql
-- 找出未使用的索引
SELECT
    schemaname,
    tablename,
    indexname
FROM sys_stat_user_indexes
WHERE idx_scan = 0;

-- 删除索引
DROP INDEX CONCURRENTLY idx_unused_table_column;  -- 并发删除（不锁表）
```

### 2. 重建膨胀索引

```sql
-- 查看索引大小排序
SELECT
    schemaname,
    tablename,
    indexname,
    sys_size_pretty(sys_relation_size(idx::regclass)) as size,
    sys_relation_size(idx::regclass)/ARRAY[ ARRAY[12],ARRAY[6] ]::int[] as defects_count
FROM sys_stats_user_indexes
ORDER BY sys_relation_size(idx::regclass) DESC;

-- 选择膨胀指数列（缺陷数 > 1）
DROP INDEX idx_high_defects;

-- 重建索引
REINDEX INDEX idx_rebuild;
```

### 3. 批量优化索引

```sql
-- 重构表所有索引
REINDEX TABLE CONCURRENTLY target_table;

-- 批量表重建索引
REINDEX SCHEMA CONCURRENTLY your_schema;
```

---

## 索引设计决策流程

```
开始
  ↓
识别高频WHERE条件
  ↓
评估列选择性（高/低）
  ↓
最左前缀分析 → 查询能否利用
  ↓
索引是否满足多个查询（多列复合索引）
  ↓
是否需要覆盖索引
  ↓
是否考虑部分索引
  ↓
是否适用特殊索引（GIN/GiST/BRIN）
  ↓
完成索引设计 → 创建
```

---

## 常见索引设计错误

### 错误1：为高选择性列建复合索引

```sql
-- ❌ 错误：email高选择性在前，gender低选择性在后
CREATE INDEX idx_wrong ON users(email, gender);

-- 正确：gender在前（虽然低选择性），email在后
CREATE INDEX idx_correct ON users(gender, email);
```

### 错误2：忽略WHERE条件

```sql
-- ❌ 只索引高频查询列
CREATE INDEX idx_users_count ON users(count_col);
-- 但WHERE子句使用的是email

-- ✅ 创建WHERE子句中使用的索引
CREATE INDEX idx_users_email ON users(email);
```

### 错误3：过度索引

```sql
-- ❌ 为所有条件建索引
CREATE INDEX idx_t1 ON t1(col1);
CREATE INDEX idx_t1 ON t1(col2);
CREATE INDEX idx_t1 ON t1(col3);

-- ✅ 只保留最优索引
CREATE INDEX idx_t1 ON t1(col1, col2) WHERE col3 = 'value';
```

### 错误4：忽略部分索引

```sql
-- ❌ 为所有状态建索引
CREATE INDEX idx_orders_status ON orders(status, user_id);

-- ✅ 只为活跃订单建索引
CREATE INDEX idx_orders_active ON orders(status, user_id)
WHERE status = 'active';
```

---

## 索引与性能的权衡

**索引越多 → 查询越快，写入越慢**

| 指标 | 无索引 | 高索引密度 | 激进索引 |
|------|--------|-----------|----------|
| SELECT性能 | 差（全表扫描） | 优秀 | 优秀 |
| WRITE性能 | 快 | 慢 | 非常慢 |
| 增长速度 | 快 | 较慢 | 稳定但不慢 |
| 存储占用 | 0% | 50-100% | 100%+ |

**平衡策略**
1. SELECT 10000次/秒的表：高索引密度
2. SELECT 100次/秒的表：适度索引
3. SELECT < 10次/秒的表：最小索引

---

## 总结

索引设计三原则：

1. **选择高选择性列**：WHERE、JOIN、ORDER BY的高频列
2. **考虑最左前缀**：复合索引的正确使用顺序
3. **平衡读写**：高查询频繁度 vs 低写入频率

设计索引时：
- 使用EXPLAIN ANALYZE验证执行计划
- 优先考虑覆盖索引（避免回表）
- 必要时使用部分索引（过滤非必要数据）
- 定期回收未使用的索引
- 避免过度索引，存储和性能都需要权衡
