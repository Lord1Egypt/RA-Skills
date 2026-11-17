# KingbaseES 自动 SQL 优化指南

包括 SQL 优化顾问、SQL 监控、等待事件优化和 CBO 优化器特性。

> 并行查询配置参见 `sql-optimization-patterns.md` 模式 8。
> KWR/KDDM/KSH 报告参见 `perf-kwr-reports.md`。
> VACUUM 自动清理参见 kes-db-optim 技能。

## 自动SQL优化组件

### SQL优化顾问（SQL Optimization Advisor）

**作用**：自动分析慢SQL并提供优化建议（索引、统计信息、SQL改写）

**使用方式**
```sql
-- 创建分析任务
CALL sys_kv_soa_analysis_task(
    task_name IN VARCHAR,     -- 任务名称
    target IN VARCHAR,          -- 分析对象（schema.table）
    analysis_params IN VARCHAR options
);

-- 分析SQL
SELECT * FROM sys_kv_soa_analysis_result
WHERE analysis_id = 'task_name';
```

**分析深度**
- 表级分析：索引情况、统计信息分析
- SQL级分析：SQL改写建议、性能提升预估
- 全局分析：系统性优化策略

**示例**

```sql
-- 识别慢SQL
SELECT * FROM sys_stat_statements
WHERE mean_time > 1000
ORDER BY mean_time DESC
LIMIT 10;

-- 对慢SQL进行分析
CREATE OR ALTER FUNCTION analyze_slow_sql()
RETURNS void AS
DECLARE
    sql_rec RECORD;
BEGIN
    FOR sql_rec IN
        SELECT query, calls, mean_time
        FROM sys_stat_statements
        WHERE mean_time > 1000
        LIMIT 5
    LOOP
        -- 创建分析任务
        CALL sys_kv_soa_analysis_task(
            'task_' || sql_rec.query::text,
            'your_schema.all_tables',
            'include_indexes=true,include_statistics=true'
        );

        -- 查看建议
        RAISE NOTICE 'SQL: %', sql_rec.query;
    END LOOP;
END;
```

---

## SQL监控组件

### SQL执行监控

**MONITOR HINT**

**MONITOR作用**：强制为特定查询生成监控记录

```sql
-- 使用MONITOR HINT
SELECT /*+MONITOR*/ *
FROM orders
WHERE customer_id = 100;
```

**查询监控视图**

```sql
-- 当前活跃查询监控
SELECT
    sql_id,
    client_sid,
    client_pid,
    session_rank,
    query_start_time,
    total_cputime,
    total_worktime,
    wait_time,
    current_state,
    current_state_status,
    virtual_memory_mb,
    io_wait
FROM v$active_sql_monitor
WHERE session_rank BETWEEN 1 AND 10
ORDER BY total_cputime DESC;

-- 查看SQL统计
SELECT
    query_id,
    client_sid,
    handle_sql,
    total_calls,
    total_exec_time,
    mean_exec_time,
    max_exec_time,
    min_exec_time,
    total_memory_usage
FROM v$sql_monitor
WHERE query LIKE '%OMIT%';
```

**监控记录**

```sql
-- 查看详细执行计划
SELECT
    sql_id,
    exec_id,
    execution_time,
    cost,
    plan,
    rows_predicted,
    rows_actual
FROM v$sql_plan_history
WHERE sql_id = 'your_sql_id';

-- 分析执行计划变化
SELECT * FROM v$sql_plan_graph
WHERE sql_id = 'your_sql_id';
```

**监控性能建议**

```sql
-- 开启监控性能分析
SET enable_monitor = on;
执SELECT /*+MONITOR*/ * FROM huge_table;

-- 查看并行执行情况
SELECT * FROM v$active_query_analysis
WHERE sql_id = 'your_sql_id';
```

---

> 并行查询完整配置参见 `sql-optimization-patterns.md` 模式 8。

---

## 等待事件优化

### 等待事件分类

| 分类 | 常见事件 | 解决方案 |
|-----|---------|---------|
| IO等待 | Disk reads, WAL I/O wait | 刷盘策略、SSD |
| 锁等待 | exclusive lock wait | 减少锁竞争 |
| 网络等待 | network wait | 增加带宽、本地cache |
| 空闲延迟 | client idle | 连接池管理 |
| 事务等待 | transaction block | 减少事务块大小 |

**查看等待事件**
```sql
-- 当前等待事件
SELECT
    sid,
    wait_event,
    wait_event_type,
    wait_state,
    time_waited,
    state
FROM v$session_wait
ORDER BY time_waited DESC;

-- 等待事件统计
SELECT
    wait_event,
    count(*) as count,
    total_wait_time,
    avg_wait_time
FROM v$session_wait_group
GROUP BY wait_event
ORDER BY total_wait_time DESC;
```

**优化示例**

**IO等待**
```sql
-- 扩大I/O并发
SET effective_io_concurrency = 200;  -- SSD
```

**锁等待**
```sql
-- 减少事务块大小
-- ❌ 低效：整个事务大量操作
BEGIN;
-- 几千条INSERT
COMMIT;

-- ✅ 高效：分批提交
BEGIN;
INSERT INTO big_table ...;
COMMIT;

BEGIN;
INSERT INTO big_table ...;
COMMIT;
```

---

## CBO优化器特性

### 优化器参数

**错误处理参数**
```sql
-- 并行去归并界限
casa_traversal_limit = 100  -- 查询优化器深度

-- 子树限制
casa_subtree_limit = 87
```

**成本控制**
```sql
-- 禁用sort导致不确定性（强制EX）;  -- 如果数据库无法确定排序情况

-- 禁用hash join（强制NESTLOOP）
SET enable_hash_join = off;
ExecSELECT * FROM t1 JOIN t2 ON t1.key = t2.key;
SET enable_hash_join = on;  -- 恢复默认

-- 禁用merge join
SET enable_merge_join = off;
```

**查询控制**
```sql
-- 调度器延迟（延迟执行）
SET enable_constraint_expr = off;  -- Oracle兼容

-- 查询超时
SET statement_timeout = '5min';
```

---

## 微型优化器

### 成本模型

**CBO成本角度**
```
开销 = IO开销 + CPU开销 + 通信开销

IO开销占用高：
- 磁盘读取块数 × 每块读IO时间
- （随机I/O vs 顺序I/O）

CPU开销占用高：
- 运算复杂度（Join、Sort、Aggregate）
- 每个操作的处理行数

通信开销：
- 网络传输数据量
- 传输大小
```

**Cost计算示例**
```
Seq Scan cost = 1.0 + 1 * TUPLE_SIZE
Index Scan cost = 2.0 + 2 * TUPLE_SIZE
Hash Join cost = 10.0 + ... + 逻辑复杂度
```

---

## 自动优化策略

### 优化模式库

**常见优化场景**
```
1. 大表扫描
   — 添加索引
   — 分区表
   — 使用HINT强制并行

2. 排序性能差
   — 增大work_mem
   — 使用覆盖索引
   — 使用SEMI JOIN避免排序

3. JOIN性能差
   — 调整JOIN顺序
   — 改写SQL
   — 使用HINT控制JOIN类型

4. 回表频繁
   — 删除无关列
   — 使用覆盖索引
   — 改写SQL减少回表

5. 聚合慢
   — 先过滤再聚合
   -- 增大work_mem
```

**自动优化流程**
```
观察现象（查询慢）
  ↓
诊断问题（EXPLAIN + 监控）
  ↓
选择策略（索引/SQL/HINT/参数）
  ↓
应用优化
  ↓
验证效果（性能对比）
```

---

## 最佳实践

### 使用SQL优化顾问

```sql
-- 定期分析慢SQL
SELECT * FROM sys_stat_statements
WHERE mean_time > 1000
ORDER BY mean_time DESC
LIMIT 5;

-- 对上述SQL调用优化顾问
CALL sys_kv_soa_analysis_task(
    'optimize_' || query,
    'schema.table',
    'exhaustive=true'
);

-- 查看建议
SELECT * FROM sys_kv_soa_analysis_result
WHERE task_name LIKE 'optimize_%';
```

### 定期使用KDDM

```sql
-- 每周生成诊断报告
CALL sys_kv_kddm_analysis();
```

### 开启SQL监控

```sql
-- 对关键业务SQL使用MONITOR HINT
SELECT /*+MONITOR*/ *
FROM orders
WHERE customer_id = 100;
```

---

## 非自动优化的调整

### 硬核优化（当自动优化不生效时）

**HINT使用**
```sql
-- 强制并行
SELECT /*+ Parallel(t1 8) */
    * FROM large_table t1;

-- 强制JOIN顺序
SELECT /*+ leading(t_small t_large) */
    * FROM t_small JOIN t_large ON ...

-- 强制JOIN算法
SELECT /*+ USE_HASH(t1 t2 t3) */
    * FROM t1 JOIN t2 JOIN t3 ...

-- 强制扫描类型
SELECT /*+ Parallel(t1 4) */
    * FROM t1;
```

**SQL改写**
```sql
-- 避免NOT IN
SELECT * FROM t1
WHERE id NOT IN (SELECT id FROM t2);

-- 改写为NOT EXISTS
SELECT * FROM t1
WHERE NOT EXISTS (SELECT 1 FROM t2 WHERE t2.id = t1.id);
```

**索引设计**
```sql
-- 复合索引设计
CREATE INDEX idx_optimize ON table (col1, col2, col3);

-- 覆盖索引
CREATE INDEX idx_covering ON table (col1, col2) INCLUDE (col3, col4);
```

---

## 自动优化局限

### 无法自动解决的问题

1. **业务逻辑错误**（如数据不一致）
2. **架构设计缺陷**（如单表太大、无缓存层）
3. **硬件不足**（如内存过小、磁盘慢）
4. **表设计不当**（无主键、无规则、大量NULL）

### 需要人工介入的场景

- 复杂数据模型重构
- 性能瓶颈根本解决（架构调整）
- 安全性提升
- 并发控制优化

---

## 总结

自动SQL优化的核心组件：

| 组件 | 作用 | 使用场景 |
|-----|------|---------|
| SQL优化顾问 | 自动分析慢SQL建议索引/改写 | 定期执行慢SQL分析 |
| SQL监控 | 追踪SQL执行过程 | 关键SQL/监控需求 |

> 并行查询配置参见 `sql-optimization-patterns.md` 模式 8。
> KWR/KDDM/KSH 报告生成参见 `perf-kwr-reports.md`。
> VACUUM 自动清理参见 kes-db-optim 技能。