# KingbaseES 统计信息管理指南

包括统计信息收集、分析、使用和最佳实践。

## 统计信息的重要性

### 什么是统计信息

统计信息是数据库中关于表、索引、列的数据分布情况，包括：
- 表的总行数
- 列的数据类型和值分布
- 索引结构和选择性
- 字符集、编码、排序规则

### 为什么需要统计信息

**核心作用**：优化器（CBO）依赖统计信息决定执行计划

| 统计信息准确 | 执行计划正确 | 性能优化 |
|------------|------------|---------|
| ✅ 高选择性判断 | JOIN顺序正确 | 索引被使用 |
| ✅ 行数估算准确 | 算法选择合适 | 查询快速 |
| ✅ 范围查询优化 | 成本估算准确 | 资源合理分配 |

**不准确统计信息的后果**
```
统计信息过期：预估行数与实际差距大
  ↓
执行计划错误：全表扫描 vs 索引扫描
  ↓
性能恶化：查询变慢、资源浪费
```

---

## 统计信息类型

### 表级统计

包含信息：
- 表的总行数（`n_live_tup`）
- 表的页面数（`relpages`）
- 好死元组数（`n_dead_tup`）
- 最后分析时间（`last_analyze`）
- 最后清理时间（`last_vacuum`）

**查询示例**
```sql
-- 查看表的统计信息
SELECT
    relname,
    n_live_tup,
    n_dead_tup,
    last_analyze,
    last_vacuum
FROM sys_stat_user_tables
WHERE relname = 'your_table';

-- 查看表的详细统计
SELECT
    schemaname,
    relname,
    seq_scan,
    seq_tup_read,
    idx_scan,
    idx_tup_fetch,
    n_tup_ins,
    n_tup_upd,
    n_tup_del
FROM sys_stat_user_tables
WHERE schemaname = 'your_schema';
```

### 列级统计

包含信息：
- 非空值占比
- 值分布（直方图）
- 唯一值数量
- 平均重复度

**查询示例**
```sql
-- 查看列的统计信息
SELECT
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation,
    most_common_vals,
    most_common_freqs
FROM sys_stats
WHERE tablename = 'your_table' AND attname = 'your_column';

-- 解释字段说明
n_distinct: -1 / N（所有值唯一）/ 0/N（都重复）
-- -1.0: 所有值唯一
-- -0.5: 随机分配
-- 0.1: 90%值重复

correlation: 与排序相关性（-1到1）
```

### 索引级统计

包含信息：
- 索引使用次数
- 索引读取的元组数
- 索引选取的元组数

**查询示例**
```sql
-- 查看索引统计
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM sys_stat_user_indexes
WHERE tablename = 'your_table';
```

---

## 统计信息收集机制

### 自动统计信息收集

**自动ANALYZE触发条件**

当表数据变化超过一定比例时，自动触发统计信息收集：

```sql
-- 查看自动分析参数
SHOW autovacuum_analyze_scale_factor;
SHOW autovacuum_analyze_threshold;

-- 示例值：
-- autovacuum_analyze_scale_factor = 0.1  (10%变化量)
-- autovacuum_analyze_threshold = 50      (最少50行变化)
```

**逻辑**
```
如果 表变更行数 > (阈值行数 + 倍率 × 统计行数)
则自动ANALYZE

示例：
表有100万行
阈值50行，倍率10%
→ 50 + 10% × 1,000,000 = 100,050行变化 → 触发ANALYZE
```

**查看自动vacuum配置**
```sql
-- 查看所有自动vacuum参数
SELECT
    name,
    setting,
    unit,
    source,
    brief
FROM sys_settings
WHERE name LIKE 'autovacuum%';
```

### 手动统计信息收集

**ANALYZE命令**

```sql
-- 基本语法
ANALYZE [VERBOSE] table_name [column_name];
```

**使用示例**
```sql
-- ANALYZE单个表
ANALYZE orders;

-- ANALYZE指定列（只收集该列统计信息）
ANALYZE orders (status, customer_id);

-- ANALYZE包含verbose（显示详细过程）
ANALYZE VERBOSE users;

-- ANALYZE所有表
ANALYZE;

-- 检查是否需要ANALYZE
SELECT
    relid,
    schemaname,
    relname,
    last_analyze,
    last_autovacuum,
    last_autoanalyze
FROM sys_stat_user_tables
ORDER BY last_analyze NULLS LAST
LIMIT 10;
```

**适用时机**
```sql
-- 1. 大量INSERT/UPDATE后
INSERT INTO orders (...) VALUES (...);
-- 或大批量数据导战后
ANALYZE orders;

-- 2. 数据发生大规模变化后
UPDATE users SET status = CASE ...;  -- 许多行变更
ANALYZE users;

-- 3. 新增大量数据后
DROP TABLE temp_table;
CREATE TABLE temp_table AS SELECT ...;  -- 创建1千万行
ANALYZE temp_table;

-- 4. 索引重建后
REINDEX INDEX idx_stats;
ANALYZE target_table;

-- 5. 从备份恢复后
-- 恢复后表统计信息过时，必须ANALYZE
RECOVER DATABASE ...;
ANALYZE all;
```

---

## 统计信息分析

### 检查统计准确性

**方法1：对比预估vs实际**

```sql
-- 查询预估行数
EXPLAIN
SELECT * FROM users WHERE gender = 'MALE';

-- EXPLAIN输出寻找：
-- 生成的行
n_tup_ins = 10
n_tup_upd = 100

-- 对比统计信息
SELECT n_live_tup FROM sys_stat_user_tables WHERE tablename = 'users';
-- 结果：100万行

-- 推理：变化超过阈值，需要ANALYZE
```

**方法2：使用统计分布**

```sql
-- 查看具体列的值分布
SELECT
    attname,
    n_distinct,
    most_common_vals,
    most_common_freqs
FROM sys_stats
WHERE tablename = 'users' AND attname = 'status';
```

**判断n_distinct**
```
n_distinct = -1.0/100: 主键字段（唯一）
            -0.5/100: 低重复度
            0.0/100: 高重复度

示例：
status列：rating: 1..5
n_distinct = -0.8
→ 80%唯一值

rating列：rating: 1
n_distinct = 0.01
→ 99%重复，高选择性低
```

### 重置统计信息

```sql
-- 重置表的统计信息（会重新收集）
ANALYZE users;

-- 清理表的信事情计数（如果首次创建表）
-- 例如：TRUNCATE后或大量INSERT后
VACUUM FULL users;  -- 也会重置统计信息
```

---

## 统计信息与执行计划的影响

### 执行计划对统计信息的依赖

**示例：SELECT语句行为对比**

```sql
-- 创建测试表
CREATE TABLE test_stats (id INT, value INT);

-- 初始状态：显示1000行
INSERT INTO test_stats SELECT id, id % 100 FROM generate_series(1, 1000);

-- 添加100万行
INSERT INTO test_stats SELECT id, id % 100
FROM generate_series(1, 1000000);

-- 没有ANALYZE：统计信息仍显示1000行
EXPLAIN SELECT * FROM test_stats WHERE value = 50;  -- 全表扫描（预估1000行）

-- ANALYZE后：统计信息更新为100万行
ANALYZE test_stats;

-- 执行计划改善
EXPLAIN SELECT * FROM test_stats WHERE value = 50;  -- 使用索引
```

**执行计划中的统计信息标记**

```sql
-- EXPLAIN ANALYZ显示实际行数
EXPLAIN (ANALYZE)
SELECT * FROM orders WHERE customer_id = 100;

-- 输出示例：
-- Index Scan on orders  (cost=0.50..9000.00 rows=5000 width=100)
--    Index Cond: (customer_id = 100)
--    Index Rows: 5000
--    Tuple Filter: created_at > '2025-01-01'
--    actual rows: 5000
```

### 索引有效性检查

```sql
-- 检查索引是否被使用
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan as scan_count,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetch
FROM sys_stat_user_indexes
WHERE tablename = 'your_table';

-- 如果idx_scan为0，且有WHERE条件建议加索引
SELECT * FROM your_table WHERE some_column = 'value';
```

---

## 统计信息撤销

### 案例1：创建表后写入数据

```sql
-- 场景：恢复备份后写入大量数据

-- 第1步：从备份恢复（1千万行）
RECOVER DATABASE ...;
-- 统计信息变为约1行

-- 第2步：写入大量新数据（1千万行）
INSERT INTO logs (...) VALUES (...);
-- 统计信息仍显示1行！

-- 第3步：ANALYZE更新
ANALYZE logs;

-- 现在查询使用索引
```

### 案例2：TRUNCATE后重新写入

```sql
-- 场景：每天清空重置表

-- TRUNCATE后统计
SELECT n_live_tup FROM sys_stat_user_tables WHERE tablename = 'daily_sales';
-- 结果：0行

-- 写入1千万行数据
INSERT INTO daily_sales SELECT ... FROM ...

-- 没有ANALYZE
EXPLAIN SELECT * FROM daily_sales WHERE date = CURRENT_DATE;
-- 全表扫描（仍认为表为空）

-- ANALYZE后改善
ANALYZE daily_sales;
EXPLAIN SELECT * FROM daily_sales WHERE date = CURRENT_DATE;
-- 使用索引
```

### 案例3：定时JOB更新后

```sql
-- 场景：定时任务会导致大量UPDATE

-- 触发UPDATE操作
UPDATE users SET status = CASE
    WHEN last_login > NOW() - INTERVAL '7 days' THEN 'active' ELSE 'inactive' END;

-- 统计信息漂移
SELECT last_analyze FROM sys_stat_user_tables WHERE tablename = 'users';
-- 显示3天前分析过，但UPDATE影响了行数

-- 为保证准确性
ANALYZE users;

-- 避免"静默"更新后索引被忽略
```

---

## 统计信息最佳实践

### 1. 定期ANALYZE

**定时策略**

```sql
-- 方案A：定期JOB
-- 每天凌晨4点分析核心表
-- 创建定时脚本
CREATE OR ALTER FUNCTION analyze_daily()
RETURNS void AS
BEGIN
    ANALYZE logs;
    ANALYZE orders;
    ANALYZE users;
    ANALYZE products;
END;

-- 添加到crontab或sys_cron（如果支持）
-- 0 4 * * * ksql -U SYSTEM -d test -c "SELECT analyze_daily();"

-- 方案B：手动检查后ANALYZE
-- 查看最少分析的表
SELECT
    schemaname,
    relname,
    last_analyze,
    last_autoanalyze,
    sys_size_pretty(sys_relation_size(relid::OID)) as size
FROM sys_stat_user_tables
WHERE last_analyze < last_autoanalyze OR last_analyze < NOW() - INTERVAL '7 days'
ORDER BY last_analyze ASC
LIMIT 20;

-- 对上述表ANALYZE
```

### 2. 并发操作注意

**多线程并发ANALYZE**

```sql
-- 检查当前是否有ANALYZE在执行
SELECT state, pid, query
FROM sys_stat_activity
WHERE program LIKE 'postgres: .* analizar%' OR query LIKE '%ANALYZE%';

-- 如果系统负载高，可以分批ANALYZE
-- 高峰期：只分析频繁访问的大表
ANALYZE users;  -- 高频访问
-- 低谷期：可以分析所有表
```

### 3. 大表ANALYZE优化

**分批ANALYZE大表**

```sql
-- 避免长时间锁表
-- 方案1：分批ANALYZE
BEGIN;
-- 分析前10%
ANALYZE large_table LIMIT 100000;  -- 并非SQL语句，而是分批
UPDATE sys_class SET relpages = relpages / 10 WHERE relname = 'large_table';
-- 分析中间10%
...
-- 分析后10%
...
COMMIT;

-- 方案2：使用VACUUM ANALYZE（但会锁表）
VACUUM ANALYZE large_table;
```

### 4. 统计信息老化检查

```sql
-- 查询统计信息老化的表
SELECT
    schemaname,
    relname,
    n_live_tup,
    last_analyze,
    last_autoanalyze,
    sys_difftime(last_analyze, now()) as analyze_age
FROM sys_stat_user_tables
WHERE last_analyze IS NOT NULL
ORDER BY analyze_age DESC
LIMIT 20;

-- 判断是否需要分析（超过30天未分析）
-- 更新统计信息
ANALYZE target_table;
```

### 5. 重点关注高频查询

```sql
-- 查看慢查询SQL
SELECT
    query,
    calls,
    total_time,
    mean_time
FROM sys_stat_statements
WHERE query ILIKE '%users%'
ORDER BY mean_time DESC
LIMIT 10;

-- 根据慢查询SQL检查统计信息
-- 提前ANALYZE相关表
```

---

## 统计信息与索引

### 索引创建后ANALYZE

```sql
-- 创建索引后，统计信息不变
CREATE INDEX idx_users_email ON users(email);
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
-- 可能仍全表扫描，因为统计信息未更新

-- ANALYZE后使用索引
ANALYZE users;
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
-- 现在使用索引

-- 并且，如果索引列选择性高，改写后的查询也会生效
-- 例如：
SELECT * FROM orders WHERE customer_id IN (...);
```

### 索引选择性与统计信息

```sql
-- 场景：列选择性变化

-- 创建无选择性索引（区域列）
CREATE INDEX idx_goods_region ON goods(region);
ANALYZE goods;

EXPLAIN SELECT * FROM goods WHERE region = 'North';
-- 使用索引（因为选择性低，全表扫描更慢）

-- INSERT大量数据
INSERT INTO goods SELECT generate_series(1, 10000000), 'North', ...;

-- 统计信息过期（仍估为5000行）
EXPLAIN SELECT * FROM goods WHERE region = 'North';
-- 可能仍使用索引

-- ANALYZE后改善
ANALYZE goods;
EXPLAIN SELECT * FROM goods WHERE region = 'North';
-- 使用索引
```

---

## 统计信息与表结构变更

### 临时表

```sql
-- 临时表不会自动ANALYZE
CREATE TEMP TABLE temp_orders AS PRAGMA TABLE_SALES AS ...;

-- 写入1千万行数据
INSERT INTO temp_orders ...

-- EXPLAIN仍然显示0行（临时的）
-- 需要手动ANALYZE
ANALYZE temp_orders;

-- 临时表删除后自动清理统计信息
```

### 索引删除后

```sql
-- 删除索引
DROP INDEX idx_users_email;

-- 表的统计信息仍保留（n_live_tup等）
-- 但索引统计信息丢失

-- ANALYZE清除并重新收集完整统计信息
ANALYZE users;
```

---

## 高级统计信息

### 扩展名

**sys_stat_statements**（SQL统计）

```sql
-- 启用扩展
create extension sys_stat_statements;

-- 查看SQL执行统计
SELECT
    query,
    calls,
    total_time,
    mean_time,
    max_time,
    min_time,
    rows,
    shared_blks_hit,
    shared_blks_read,
    temp_blks_read,
    temp_blks_written
FROM sys_stat_statements
ORDER BY total_time DESC
LIMIT 20;

-- 查看特定SQL
SELECT * FROM sys_stat_statements
WHERE query ILIKE '%users%';
```

**自制扩展**

```sql
-- sys_stat_user_tables增强版本
CREATE VIEW sys_stat_enhanced_tables AS
SELECT
    s.schemaname,
    s.relname,
    s.n_live_tup as live_rows,
    s.n_dead_tup as dead_rows,
    s.last_analyze,
    s.last_autoanalyze,
    CASE
        WHEN s.last_analyze < NOW() - INTERVAL '7 days' THEN 'needs_analyze'
        ELSE 'current'
    END as status,
    sys_size_pretty(sys_relation_size(s.relid::OID)) as size
FROM sys_stat_user_tables s
ORDER BY s.last_analyze DESC NULLS LAST;
```

---

## 统计信息错误诊断

### 错误1：乐观型vs悲观型查询

**症状**：突然变慢

```sql
-- 查询1：乐观型（统计信息支持）
SELECT * FROM users WHERE id = 100;  -- 索引扫描，快

-- 查询2：悲观型（统计信息不支持）
SELECT * FROM users WHERE email LIKE 'abc%DE%';  -- 可能全表扫描
```

**解决**
```sql
-- 改写SQL以支持索引
SELECT * FROM users WHERE email LIKE 'abc%' AND email LIKE '%DE%';
-- 如果email有索引，优化器会使用
```

### 错误2：DEXERT错误

```sql
-- 查询60105
-- 错误：统计信息类型错误

SELECT * FROM productions
WHERE path ~ '1/1(2,4)';
-- 错误的统计信息类型
```

**解决**
```sql
-- ANALYZE表
ANALYZE productions;

-- 特定列ANALYZE
ANALYZE productions(path);
```

---

## 统计信息收集策略总结

### 动态调整

```
1. 监控表变化
   - 监控INSERT/UPDATE/DELETE
2. 评估变化量
   - 如果变化 < 10%，等待自动ANALYZE
   - 如果变化 > 10%，手动ANALYZE

3. 检查关键表
   - 高频查询的表优先ANALYZE
   - 日志表定期ANALYZE
   - 大表选择性ANALYZE

4. 验证效果
   - 使用EXPLAIN ANALYZE验证
   - 检查执行计划变化
   - 性能改善证明
```

### 关键建议

1. **每天都ANALYZE核心表**
   ```sql
   ANALYZE users;
   ANALYZE orders;
   ```

2. **大数据量变更后ANALYZE**
   ```sql
   TRUNCATE TABLE logs;
   INSERT INTO logs SELECT ...;  -- 1000万行
   ANALYZE logs;
   ```

3. **定时JOB定期检查**
   ```sql
   -- 每天检查表老化
   SELECT * FROM sys_stat_user_tables
   WHERE last_analyze < NOW() - INTERVAL '7 days';
   ```

4. **EXPLAIN ANALYZE验证**
   ```sql
   -- 每次查询验证
   EXPLAIN ANALYZE SELECT ...;
   -- 检查"actual rows" vs "rows"
   ```

5. **关注统计信息准确性**
   ```sql
   SELECT n_distinct FROM sys_stats
   WHERE tablename = 'your_table' AND attname = 'your_column';
   -- n_distinct = 1.0: 理论统计信息真实
   -- n_distinct < 0: 随机性取值
   ```
