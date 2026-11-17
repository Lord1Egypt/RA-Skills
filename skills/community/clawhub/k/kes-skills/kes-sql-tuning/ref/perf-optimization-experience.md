# KingbaseES 常见性能优化经验

本文件收录15+个常见性能问题的诊断思路和优化方案，供第5步（诊断优化点）快速查阅。

## 经验1：大表无索引导致全表扫描

**现象**：查询大表（>100万行）响应时间超过5秒，EXPLAIN显示Seq Scan。

**诊断**：
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 100;
-- 输出: Seq Scan on orders  (rows=预估行数 wide=实际列宽)
```

**修复**：
```sql
-- 为WHERE条件列创建索引
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
ANALYZE orders;
```

**验证**：EXPLAIN确认变为Index Scan或Bitmap Index Scan。

**预防**：新表设计时为主查询条件列预先建索引。

---

## 经验2：统计信息过期导致执行计划错误

**现象**：大量INSERT/UPDATE/DELETE后查询突然变慢，索引未被使用。

**诊断**：
```sql
SELECT
    relname,
    n_live_tup,
    last_analyze,
    last_autoanalyze
FROM sys_stat_user_tables
WHERE relname = 'target_table';
-- 对比last_analyze时间与数据变更量
```

**修复**：
```sql
ANALYZE target_table;
-- 或针对特定列
ANALYZE target_table(col1, col2);
```

**预防**：调整自动分析阈值 `autovacuum_analyze_scale_factor = 0.1`，确保大表变更后自动ANALYZE触发。

---

## 经验3：shared_buffers配置过小

**现象**：磁盘I/O持续高位，缓存命中率低。

**诊断**：
```sql
SHOW shared_buffers;
-- 检查缓存命中率
EXPLAIN ANALYZE SELECT * FROM large_table LIMIT 1000;
-- 查看BUFFERS统计中"shared hit" vs "disk read"比例
```

**修复**：
```sql
-- 调整为物理内存的1/2
ALTER SYSTEM SET shared_buffers = '16GB';
-- 重启生效
SELECT sys_reload_conf();
```

**注意**：shared_buffers不能在线修改，必须重启。

---

## 经验4：work_mem过小导致磁盘排序

**现象**：大量排序/聚合查询慢，日志出现"Disk Sorting"提示。

**诊断**：
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT customer_id, SUM(amount)
FROM orders
GROUP BY customer_id
ORDER BY SUM(amount) DESC;
-- 查看输出是否出现"Disk Sorting"
```

**修复**：
```sql
-- 根据并发量调整
-- 假设30并发，可用内存8GB → work_mem = 8GB / 30 ≈ 256MB
ALTER SYSTEM SET work_mem = '256MB';
SELECT sys_reload_conf();
```

**权衡**：work_mem过高 × 并发数 > 可用内存会导致OOM。公式：`max_connections × work_mem < 可用内存`。

---

## 经验5：大表JOIN性能差

**现象**：JOIN查询耗时长，执行计划显示Nested Loop全表扫描。

**诊断**：
```sql
EXPLAIN ANALYZE
SELECT * FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.status = 'active';
-- 检查JOIN顺序、算法选择和预估行数
```

**修复方案**：
```sql
-- 方案1：小表驱动大表（调整JOIN顺序）
SELECT /*+ leading(c o) */ *
FROM customers c JOIN orders o ON c.id = o.customer_id;

-- 方案2：为JOIN列建索引
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- 方案3：强制Hash JOIN（大表对大表）
SELECT /*+ USE_HASH(o c) */ *
FROM orders o JOIN customers c ON o.customer_id = c.id;

-- 方案4：使用覆盖索引避免回表
CREATE INDEX idx_covering ON orders(customer_id) INCLUDE (status, amount);
```

---

## 经验6：频繁回表导致性能下降

**现象**：Index Scan但性能仍差，大量磁盘I/O。

**原因**：索引扫描定位行后需要回表取SELECT列数据。

**修复**：
```sql
-- 使用覆盖索引，将SELECT列纳入索引
CREATE INDEX idx_covering ON orders(customer_id, status)
INCLUDE (amount, order_date);

-- EXPLAIN验证：期望看到 Index Only Scan
EXPLAIN SELECT customer_id, status, amount, order_date
FROM orders WHERE customer_id = 100;
```

---

## 经验7：复合索引列顺序不合理

**现象**：创建了复合索引但查询未走索引。

**原因**：索引列顺序不遵循最左前缀原则，或选择性判断错误。

**修复**：
```sql
-- 高选择性列在前，低选择性列在后
-- 错误：低选择性(status)在前
DROP INDEX idx_wrong;

-- 正确：高选择性(email)在前
CREATE INDEX idx_correct ON users(email, status);
```

**判断选择性**：
```sql
SELECT
    attname,
    n_distinct
FROM sys_stats
WHERE tablename = 'users';
-- n_distinct绝对值越大 → 选择性越高
```

---

## 经验8：连接数过多导致资源竞争

**现象**：数据库响应缓慢，FATAL: too many clients already。

**诊断**：
```sql
-- 查看当前连接数
SELECT count(*) FROM sys_stat_activity;

-- 查看最大连接数配置
SHOW max_connections;
```

**修复**：
```sql
-- 方案1：增大连接数
ALTER SYSTEM SET max_connections = 500;

-- 方案2：使用连接池（推荐）
-- PgBouncer / SockProxy等连接池管理

-- 方案3：清理空闲连接
SELECT sys_terminate_backend(pid)
FROM sys_stat_activity
WHERE state = 'idle' AND state_change < NOW() - INTERVAL '10 minutes';
```

---

## 经验9：死元组过多导致表膨胀

**现象**：表经过大量UPDATE/DELETE后查询变慢，存储空间异常增长。

**诊断**：
```sql
SELECT
    relname,
    n_live_tup,
    n_dead_tup,
    CASE WHEN n_live_tup > 0
        THEN round(100.0 * n_dead_tup / (n_live_tup + n_dead_tup), 2)
        ELSE 0
    END AS dead_ratio
FROM sys_stat_user_tables
ORDER BY dead_ratio DESC
LIMIT 10;
```

**修复**：
```sql
-- 简单清理
VACUUM target_table;

-- 清理+更新统计信息（推荐）
VACUUM ANALYZE target_table;

-- 彻底重建（会锁表，慎用）
VACUUM FULL target_table;
```

**预防**：确认 `autovacuum = on`，调整阈值参数。

---

## 经验10：NOT IN导致性能问题

**现象**：使用NOT IN的子查询性能极差。

**原因**：NOT IN不处理NULL值，可能产生意外结果且无法使用索引。

**修复**：
```sql
-- 错误写法
SELECT * FROM t1
WHERE id NOT IN (SELECT id FROM t2);

-- 改写为NOT EXISTS
SELECT * FROM t1
WHERE NOT EXISTS (SELECT 1 FROM t2 WHERE t2.id = t1.id);

-- 或改写为LEFT JOIN + IS NULL
SELECT t1.* FROM t1
LEFT JOIN t2 ON t1.id = t2.id
WHERE t2.id IS NULL;
```

---

## 经验11：LIKE模糊查询索引失效

**现象**：前缀模糊查询`LIKE '%keyword'`无法使用索引。

**修复方案**：
```sql
-- 方案1：前缀LIKE可直接使用B-Tree索引
SELECT * FROM users WHERE name LIKE '张%';  -- 有效

-- 方案2：前缀+后缀使用GIN全文索引
CREATE EXTENSION IF NOT EXISTS gin_trgm;
CREATE INDEX idx_trgm ON users USING gin(name gin_trgm_ops);

-- 方案3：使用全文搜索
CREATE INDEX idx_fts ON users USING gin(to_tsvector('simple', name));
SELECT * FROM users WHERE to_tsvector('simple', name) @@ to_tsquery('simple', 'keyword');
```

---

## 经验12：OR条件导致全表扫描

**现象**：多个OR条件导致索引失效。

**修复**：
```sql
-- 错误写法
SELECT * FROM orders WHERE customer_id = 1 OR status = 'pending';

-- 改写为UNION ALL
SELECT * FROM orders WHERE customer_id = 1
UNION ALL
SELECT * FROM orders WHERE status = 'pending' AND customer_id != 1;

-- 如果两列各有索引，UNION ALL可分别利用
```

---

## 经验13：在JOIN列上使用函数导致索引失效

**现象**：JOIN条件包含函数转换，索引无法使用。

**修复**：
```sql
-- 错误写法
SELECT * FROM t1 JOIN t2 ON UPPER(t1.name) = UPPER(t2.name);

-- 方案1：避免函数，直接JOIN
SELECT * FROM t1 JOIN t2 ON t1.name = t2.name;

-- 方案2：创建函数索引
CREATE INDEX idx_lower_name ON t1(LOWER(name));
-- 查询改为LOWER(t1.name) = LOWER(t2.name)
```

---

## 经验14：GROUP BY产生大量排序开销

**现象**：聚合查询慢，大量临时文件创建。

**修复方案**：
```sql
-- 方案1：增大work_mem
SET work_mem = '512MB';

-- 方案2：先过滤再聚合
SELECT customer_id, SUM(amount)
FROM orders WHERE created_at > '2025-01-01'
GROUP BY customer_id;

-- 方案3：使用覆盖索引
CREATE INDEX idx_covering ON orders(customer_id) INCLUDE (amount, created_at);

-- 方案4：启用并行聚合
SELECT /*+ Parallel(o 4) */
    customer_id, SUM(amount)
FROM orders o
GROUP BY customer_id;
```

---

## 经验15：随机I/O瓶颈

**现象**：磁盘I/O等待高，大量随机读取操作。

**诊断**：
```bash
# 系统层面
iostat -x 1 5  # 查看await和util指标
```

**修复方案**：
```sql
-- 方案1：SSD环境调整成本参数
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET effective_io_concurrency = 200;

-- 方案2：增大缓存
ALTER SYSTEM SET effective_cache_size = '24GB';

-- 方案3：使用延迟写入
ALTER SYSTEM SET synchronous_commit = 'off';  -- 可接受数据丢失场景
```

---

## 经验16：批量INSERT性能差

**现象**：大批量数据导入速度慢。

**修复方案**：
```sql
-- 方案1：临时关闭索引
DROP INDEX idx_temp;
-- 执行批量INSERT
-- 重建索引
CREATE INDEX idx_temp ON table(column);

-- 方案2：使用COPY命令
COPY orders FROM '/path/to/data.csv' WITH (FORMAT csv);

-- 方案3：分批提交（每1000行COMMIT）
-- 避免长事务占用资源

-- 方案4：调整参数
ALTER SYSTEM SET maintenance_work_mem = '4GB';
ALTER SYSTEM SET synchronous_commit = 'off';
```

---

## 经验17：WAL日志过多

**现象**：磁盘空间被WAL日志占满。

**诊断**：
```sql
SHOW wal_keep_size;
SHOW checkpoint_completion_target;
```

**修复**：
```sql
-- 调整checkpoint参数
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '64MB';

-- 限制保留WAL大小
ALTER SYSTEM SET wal_keep_size = '1GB';

-- 触发checkpoint释放空间
CHECKPOINT;
```

---

## 经验18：长事务阻塞与VACUUM冲突

**现象**：VACUUM无法清理死元组，表持续膨胀。

**诊断**：
```sql
-- 查看长事务
SELECT
    pid,
    now() - xact_start AS duration,
    query
FROM sys_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC
LIMIT 10;
```

**修复**：
```sql
-- 终止异常长事务
SELECT sys_terminate_backend(pid);

-- 减小事务块：分批COMMIT
BEGIN;
INSERT ...;
COMMIT;
-- 每批1000行提交一次
```

---

## 经验19：并行查询未生效

**现象**：大表扫描仍使用单线程，CPU利用率低。

**诊断**：
```sql
SHOW max_parallel_workers;
SHOW max_parallel_workers_per_gather;

-- 查看并行执行情况
SELECT * FROM v$active_query_analysis
WHERE parallel_workers > 1;
```

**修复**：
```sql
-- 配置并行参数
ALTER SYSTEM SET max_parallel_workers = 32;
ALTER SYSTEM SET max_parallel_workers_per_gather = 4;

-- 查询级使用HINT
SELECT /*+ Parallel(t1 8) */ * FROM large_table t1;
```

**注意**：小表并行反而变慢（进程调度开销 > 扫描时间）。

---

## 经验20：索引膨胀

**现象**：索引占用空间远超预期，索引扫描性能下降。

**诊断**：
```sql
SELECT
    indexrelname,
    sys_size_pretty(sys_relation_size(indexrelid)) AS index_size,
    idx_scan
FROM sys_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY sys_relation_size(indexrelid) DESC;
```

**修复**：
```sql
-- 重建索引（不锁表）
REINDEX INDEX CONCURRENTLY idx_name;

-- 重建表所有索引
REINDEX TABLE CONCURRENTLY target_table;

-- 重建整个schema
REINDEX SCHEMA CONCURRENTLY public;
```

---

## 经验21：低选择性列误建索引

**现象**：索引创建后查询仍未走索引。

**原因**：列选择性太低（如只有2-3个不同值），优化器判断全表扫描成本更低。

**诊断**：
```sql
SELECT
    attname,
    n_distinct
FROM sys_stats
WHERE tablename = 'target_table';
-- n_distinct接近0 → 选择性极低
```

**修复**：
```sql
-- 删除低选择性列的单独索引
DROP INDEX idx_low_selective;

-- 将低选择性列作为复合索引的后缀列
CREATE INDEX idx_composite ON table(high_selective_col, low_selective_col);
```

---

## 经验22：分区表缺少分区 pruning

**现象**：查询分区表扫描了所有分区。

**诊断**：
```sql
EXPLAIN SELECT * FROM sales WHERE sale_date = '2025-01-15';
-- 查看Append/Union节点是否包含所有分区
```

**修复**：
```sql
-- 确保WHERE条件包含分区键
SELECT * FROM sales
WHERE sale_date = '2025-01-15';  -- sale_date是分区列

-- 统计信息需要更新
ANALYZE sales;
```

---

## 经验23：锁等待导致查询阻塞

**现象**：查询长时间等待，状态显示"waiting for lock"。

**诊断**：
```sql
-- 查看等待事件
SELECT
    sid,
    wait_event,
    wait_event_type,
    time_waited
FROM v$session_wait
WHERE wait_event_type = 'Lock'
ORDER BY time_waited DESC;
```

**修复方案**：
```sql
-- 方案1：找出持有锁的事务并终止
SELECT sys_terminate_backend(blocking_pid);

-- 方案2：减小事务块避免长时间持锁
-- 将大事务拆分为小事务

-- 方案3：使用SELECT FOR UPDATE NOWAIT快速失败
SELECT * FROM target_table WHERE id = 1 FOR UPDATE NOWAIT;
```

---

## 经验24：查询结果集过大

**现象**：查询返回大量数据，网络传输和客户端处理成为瓶颈。

**修复方案**：
```sql
-- 方案1：限制返回行数
SELECT * FROM orders LIMIT 1000;

-- 方案2：分页查询
SELECT * FROM orders
ORDER BY created_at DESC
OFFSET 0 LIMIT 50;

-- 方案3：只查询必要列
SELECT id, name, status FROM users;  -- 代替 SELECT *

-- 方案4：服务端聚合减少数据传输量
SELECT customer_id, SUM(amount), COUNT(*)
FROM orders
GROUP BY customer_id;
```

---

## 经验25：时区/字符集导致的隐式转换

**现象**：查询条件看似匹配但索引未使用。

**原因**：隐式类型转换导致索引失效。

**修复**：
```sql
-- 错误：字符串比较数字列
SELECT * FROM users WHERE age = '25';  -- age是INT类型

-- 正确：使用正确类型
SELECT * FROM users WHERE age = 25;

-- 错误：日期隐式转换
SELECT * FROM orders WHERE created_at = '2025-01-01';

-- 正确：显式指定类型
SELECT * FROM orders WHERE created_at = DATE '2025-01-01';
```

---

## 经验速查表

| 经验编号 | 问题类型 | 关键症状 | 优先修复 |
|---------|---------|---------|---------|
| 1 | 全表扫描 | Seq Scan大表 | 建索引 |
| 2 | 统计信息过期 | 索引未被使用 | ANALYZE表 |
| 3 | shared_buffers过小 | 缓存命中低 | 调整参数 |
| 4 | work_mem过小 | Disk Sorting | 调整参数 |
| 5 | JOIN性能差 | Nested Loop全扫描 | 调整JOIN+索引 |
| 6 | 频繁回表 | Index Scan仍慢 | 覆盖索引 |
| 7 | 索引列序不当 | 复合索引未命中 | 重建索引 |
| 8 | 连接数过多 | too many clients | 连接池 |
| 9 | 死元组膨胀 | 表空间异常增长 | VACUUM |
| 10 | NOT IN性能差 | 子查询慢 | 改写NOT EXISTS |
| 11 | LIKE索引失效 | 模糊查询慢 | GIN索引 |
| 12 | OR条件失效 | 多条件全表扫描 | UNION ALL |
| 13 | JOIN列函数 | 索引失效 | 移除函数 |
| 14 | GROUP BY排序 | 聚合慢+临时文件 | 增大work_mem |
| 15 | 随机I/O | IO等待高 | SSD+参数调整 |
| 16 | 批量INSERT慢 | 导入耗时 | COPY+分批提交 |
| 17 | WAL日志过多 | 磁盘空间不足 | checkpoint调整 |
| 18 | 长事务阻塞 | VACUUM无法清理 | 终止长事务 |
| 19 | 并行未生效 | CPU利用率低 | 配置并行 |
| 20 | 索引膨胀 | 索引空间过大 | REINDEX |
| 21 | 低选择性误索引 | 索引不被使用 | 删除/重组 |
| 22 | 分区pruning缺失 | 扫描全分区 | WHERE含分区键 |
| 23 | 锁等待 | 查询阻塞 | 终止阻塞事务 |
| 24 | 结果集过大 | 网络瓶颈 | LIMIT/分页 |
| 25 | 隐式类型转换 | 索引失效 | 修正类型 |
