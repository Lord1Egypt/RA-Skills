# EXPLAIN Plan 执行计划解读指南

## 6步分析工作流

### 步骤1：获得执行计划

```sql
-- 基本EXPLAIN
EXPLAIN SELECT * FROM users WHERE id = 100;

-- ANALYZE模式（包含实际执行时间）
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM users WHERE id = 100;

-- 指定执行计划的成本详细信息
EXPLAIN (COSTS ON, VERBOSE ON)
SELECT * FROM orders WHERE customer_id = 10;
```

### 步骤2：自上而下的阅读

EXPLAIN输出树结构从上到下是：
- **树的根节点**：查询的物理执行计划
- **子节点**：树状结构的各个操作步骤
- 执行顺序：按照树的根节点到底部的顺序

**示例结构**
```
QUERY PLAN
- Nested Loop (Join cost, rows predicted)
  - Index Scan ON table1 (cost... rows...)
  - Bitmap Heap Scan ON table2 (cost... rows...)
    - Bitmap Index Scan ON 表2索引 (cost... rows...)
```

### 步骤3：检查统计信息准确性

**统计信息不准确的表现**
1. 预估行数与实际行数差异极大（超过10倍）
2. 执行计划中出现不合理的选择（如应该使用索引却全表扫描）
3. 估算值显示NULL或极小值

**重建统计信息**
```sql
-- 对单个表重建统计信息
ANALYZE users;

-- 对多个表重建
ANALYZE users, orders, products;

-- 分析系统所有表
ANALYZE;

-- 查看表的统计信息
SELECT
    schemaname,
    tablename,
    last_analyze,
    n_live_tup,
    n_dead_tup
FROM sys_stat_user_tables
ORDER BY last_analyze DESC;
```

**统计信息重要性**
- 扫描方法选择（索引扫描 vs 全表扫描）
- 连接顺序决定（大表小表先连接）
- 连接算法选择（NESTLOOP vs HASH vs MERGE）
- 行数估算影响内存分配

### 步骤4：识别耗时节点

**执行计划中的耗时节点特征**

1. **全表扫描（Seq Scan）**
   - 特征：没有索引参与，扫描整张表
   - 成本高：扫描所有数据块
   - 仅在小表或WHERE条件无法利用索引时出现

2. **索引扫描（Index Scan / IndexOnly Scan）**
   - Index Scan：扫描索引，再回表查询数据
   - IndexOnly Scan：仅使用索引即可满足查询（无回表）
   - 成本较低：只扫描索引结构，可能少部分数据块
   - 通常出现在WHERE条件有索引或JOIN条件下

3. **连接操作（Join）**
   ❓ 为什么连接操作耗时？
   - RBO成本模型中，连接是CPU密集型操作
   - 需要比较、排序、哈希等运算
   - 如果JOIN两边行数估算偏差大，可能导致算法选择不当

4. **排序/分组（Sort / HashAggregate）**
   - 需要读取大量数据到内存或磁盘
   - 内存不足时会溢出到磁盘（磁盘排序更慢）
   - `work_mem`参数过大或过小都会影响性能

5. **聚合操作（Aggregate / HashAggregate）**
   - 需要读取数据并进行汇总计算
   - 类似排序，内存规划很重要

### 步骤5：分析耗时节点的合理性

#### 5.1 数据扫描分析

**全表扫描应避免的情况**
```sql
-- ❌ 低效：无WHERE条件，必定全表扫描
SELECT * FROM large_table;

-- ❌ 低效：WHERE条件不选择性
SELECT * FROM users WHERE name LIKE '%smith%';

-- ❌ 低效：条件函数导致索引失效
SELECT * FROM logs WHERE DATE(create_time) = CURRENT_DATE;

-- ✅ 高效：使用索引
SELECT * FROM users WHERE id = 100;
```

**索引扫描正确使用的条件**
```sql
-- ✅ 高效：等值查询
SELECT * FROM users WHERE status = 'active';

-- ✅ 高效：索引列作为排序键
SELECT * FROM users ORDER BY created_at;

-- ✅ 高效：索引列作为JOIN条件
SELECT a.*, b.order_date
FROM account a
LEFT JOIN orders b ON a.account_id = b.account_id;
```

#### 5.2 连接顺序分析

**根据基数选择连接顺序**
```
连接顺序原则：从小表开始，逐步扩大规模

× 低效：大表在先
Seq Scan ON large_table1  (10,000,000 rows)
  Inner Hash Join ON key
    Seq Scan ON small_table2 (1,000 rows)
    -> Hash (cost=10...预算=1000)

✅ 高效：小表在先
Seq Scan ON small_table2 (1,000 rows)  → 先处理小表
  Inner Hash Join ON key
    Seq Scan ON large_table1 (10,000,000 rows)
```

**JOIN基数估计不准确的表现**
```sql
-- 场景：表面试大但实际数据少
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT,  -- 索引
    order_date DATE
);
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- 问题：统计信息不准确，估计customer_id=100时有10,000行
EXPLAIN SELECT * FROM orders WHERE customer_id = 100;
-- 结果：即使customer_id分布不均匀，也可能选择错误的JOIN顺序

-- 解决：重建收集统计信息
ANALYZE orders;

-- 或使用HINT强制顺序
EXPLAIN SELECT /*+ leading(customer orders) */
    * FROM customer JOIN orders ON customer.id = orders.customer_id;
```

#### 5.3 连接算法分析

**三种主要JOIN算法**

1. **NESTLOOP（嵌套循环）**
   - 适用：小表驱动大表，WHERE条件使得驱动表选择性高
   - 优点：不需要额外内存，支持排序Join
   - 缺点：效率低，最好用于小表JOIN

2. **HASH JOIN（哈希连接）**
   - 适用：大表JOIN，可以构建哈希表
   - 优点：效率高，适合大表join
   - 缺点：需要内存哈希表

3. **MERGE JOIN（归并连接）**
   - 适用：两表都排序好，顺序JOIN
   - 优点：可以利用预排序数据
   - 缺点：需要排序操作，开销较大

**算法选择示例**
```sql
-- 默认情况：估算基数准确
SELECT *
FROM sales
JOIN customers ON sales.customer_id = customers.id;

-- 如果使用错误算法（例如小表驱动大表仍用NESTLOOP）
-- 可以用HINT调整
SELECT * FROM /*+ USE_HASH(sales customers) */
    sales JOIN customers ON sales.customer_id = customers.id;
```

#### 5.4 行数估算分析

**行数估算偏差导致的问题**
```sql
-- 场景：统计信息严重过期
-- 实际表有1,000,000行，统计信息显示100,000行
ANALYZE big_table;  -- 重新收集统计信息
```

**使用HINT调整估算**
```sql
-- 自定义行数估算
EXPLAIN SELECT * FROM /*+ cards(sales 5000) */
    sales JOIN products ON sales.product_id = products.id;
```

#### 5.5 内存分析

**排序内存不足的表现**
- 执行计划中出现"Disk Sorting"
- 无法在内存中完成，溢出到磁盘
- 性能严重下降

**内存需求评估**
```sql
-- 错误的内存规划（work_mem过小）
Set work_mem = 1MB;

-- 正确的内存规划
-- 假设需要排序100,000行数据，每行100字节
-- 内存需求 = 100,000行 × 100字节 = 10MB
SET work_mem = 256MB;  -- 适度预留
```

**如何调整work_mem**
```sql
-- 根据系统负载动态调整
-- 建议值：排序平均需求的5-10倍
-- 单个session建议不超过1-2GB

-- 全局影响：
-- small work_mem → 性能差（频繁磁盘排序）
-- huge work_mem → 导致系统内存耗尽
```

### 步骤6：执行计划影响因素

#### 影响因素1：数据规模

**小规模表 vs 大规模表**
- 小表（<1,000行）：全表扫描可能比索引扫描快
- 中表（10,000-100,000行）：索引扫描有优势
- 大表（>100,000行）：必须使用索引，考虑分区

#### 影响因素2：索引膨胀

**索引膨胀问题**
```sql
-- 成因：大量UPDATE/DELETE/INSERT
-- 影响：索引页面膨胀，扫描更慢
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM sys_stat_user_indexes
WHERE idx_scan = 0;  -- 索引未使用
```

**解决索引膨胀**
```sql
-- 删除未使用的索引
DROP INDEX IF EXISTS unused_index_name;

-- 对长期使用的表定期进行VACUUM
VACUUM FULL large_table;

-- 考虑重建索引
REINDEX INDEX index_name;
REINDEX TABLE table_name;
```

#### 影响因素3：统计准确性

**统计信息更新频率**
```sql
-- 自动统计信息（默认）
-- 数据变化超过10%时自动更新

-- 查看自动统计配置
SELECT
    name,
    setting,
    unit
FROM sys_settings
WHERE name IN ('autovacuum_vacuum_scale_factor', 'autovacuum_analyze_scale_factor');

-- 手动触发ANALYZE
ANALYZE table_name;
```

**统计信息漂移案例**
```sql
-- 场景：批处理大量变更后忘记ANALYZE
-- 执行前结果：统计信息准确
EXPLAIN SELECT * FROM orders WHERE status = 'shipped';
-- Index Scan (1行估算)

-- 执行完成后忘记ANALYZE
-- 执行后结果：统计信息严重过时
EXPLAIN SELECT * FROM orders WHERE status = 'shipped';
-- Seq Scan (10000行估算)  ← 错误！

-- 解决：执行变更后ANALYZE
UPDATE orders SET shipped_at = now() WHERE ...;
ANALYZE orders;
```

## 高级分析技巧

### EXPLAIN FORMAT JSON

**JSON格式包含执行细节**
```sql
EXPLAIN (ANALYZE, FORMAT JSON)
SELECT * FROM users WHERE id = 100;
-- 结果包含：实际运行时间、I/O次数、内存分配等详细信息
```

### BUFFERS 开关

**查看I/O统计**
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE customer_id = 10;

-- 输出示例：
-- Buffers: shared hit=100, shared read=500, temp read=2, temp written=5
-- shared hit: 缓存命中（热数据）
-- shared read: 磁盘读取（冷数据）
```

### TIMING 开关

**查看节点级性能**
```sql
EXPLAIN (ANALYZE, TIMING)
SELECT * FROM sales JOIN customers ON sales.customer_id = customers.id;
-- 显示每个节点的实际执行时间
```

### 常见执行计划模式

#### 模式1：Filter vs Recheck（索引过滤）
```sql
-- Index Scan + Filter（扫描索引后过滤部分行）
Index Scan ON orders USING idx_date ON orders (order_date)  (cost=0.50..100.00 rows=10 width=100)
  Filter: status = 'paid'

-- Index Scan + Recheck（已索引，重新检查条件）
Index Scan ON orders USING idx_status ON orders (status)  (cost=0.50..200.00 rows=100 width=100)
  Index Cond: (status = 'paid')
  Filter: (customer_id = 100)  -- Recheck
```

#### 模式2：Bitmap Scan（位图扫描）
```sql
-- 适合：多个索引条件组合
Bitmap Heap Scan ON users (cost=20..100.00 rows=500 width=100)
  Recheck Cond: (status = 'active')
  Filter: (created_at > '2025-01-01')
  -> Bitmap Index Scan ON users_idx_status  (cost=10..50.00 rows=5000)
```

#### 模式3：Nested Loop with Parameter

```sql
-- 嵌套循环，外层为参数化查询（批量处理）
Nested Loop  (cost=0.50..200.00 rows=10 width=100)
  Join Filter: (users.id = orders.user_id  -- 参数化
  Rows Removed by Join Filter: 9
  -> Index Scan ON users  (cost=0.50..100.00 rows=1000 width=50)
```

## 常见问题排查

### 问题1：执行计划选择错误（错误表扫描）

**症状**
- 本应走索引却走全表扫描
- 全表扫描却走了错误的JOIN顺序

**排查步骤**
```sql
-- 第1步：检查统计信息
SELECT reltuples::bigint
FROM sys_class
WHERE relname = 'your_table';

-- 第2步：重建统计信息
ANALYZE your_table;

-- 第3步：查看索引使用情况
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

### 问题2：执行计划性能差

**症状**
- EXPLAIN显示的预计成本很高，实际执行时间也长

**解决方案**
1. 检查执行计划的每个节点
2. 识别耗时节点（CPU密集、IO密集）
3. 根据第5节的方法逐个优化

### 问题3：Hash Join vs NESTLOOP 选择不当

**症状**
- 小表用Hash Join导致资源浪费
- 大表使用NESTLOOP性能极慢

**解决方案**
```sql
-- 使用HINT控制算法
-- Hash Join适合大表/多表JOIN
SELECT /*+ USE_HASH(t1 t2 t3) */ * FROM t1 JOIN t2 ... JOIN t3;

-- NESTLOOP只在小表驱动时使用
SELECT /*+ USE_NESTLOOP(t1 t2) */ * FROM t1 JOIN t2 ...
```

### 问题4：并行查询（Parallel Query）

**症状**
- 呆表查询，单线程执行慢

**启用并行查询**
```sql
-- 系统参数
SET max_parallel_workers = 4;
SET max_parallel_maintenance_workers = 2;

-- 单句启用
SET enable_seqscan = off;  -- 禁用Seq Scan
```

**PARALLEL HINT控制**
```sql
EXPLAIN
SELECT /*+ Parallel(t1 4) Parallel(t2 2) */
    t1.col1, t2.col2
FROM t1
JOIN t2 ON t1.id = t2.id;
```

## 工具与方法

### KWR分析

```sql
-- 查询慢SQL的执行计划
SELECT
    sql_id,
    sql_text,
    child_number,
    execution_count,
    total_cputime,
    total_diskreadtime,
    plan
FROM v$sql_sa_top_sql_time_agg
WHERE sql_text LIKE '%your_query%';
```

### 动态性能视图

```sql
-- 查看特定SQL的执行计划
SELECT plan, plan_filter_info
FROM v$sql_plan
WHERE sql_id = 'your_sql_id';

-- 查看SQL文本（查询优化后的）
SELECT sql_text
FROM v$sqlarea
WHERE sql_id = 'your_sql_id';
```

## 总结

EXPLAIN Plan解读是性能问题的核心诊断工具，遵循**自上而下**的原则：

1. ✅ 先看全貌：HEAP SCAN / Index Scan / JOIN
2. ✅ 再看细节：节点成本、行数、内存
3. ✅ 诊断时 Combine（结合）KWR、统计信息、业务理解
4. ✅ 优化时免去（避免）：不支持索引、统计信息过期、JOIN顺序错误

当执行计划不合理时，优先调节：
- 统计信息（ANALYZE）
- 索引设计（创建/删除）
- SQL改写（JOIN顺序、过滤条件）
- 参数调优（work_mem、shared_buffers）
- 使用HINT（最后手段）
