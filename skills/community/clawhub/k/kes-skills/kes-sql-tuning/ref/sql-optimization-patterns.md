# KingbaseES SQL 手动优化模式

## 查询优化器基础

### SQL 处理流水线

SQL 语句依次经过五个处理阶段：
1. **词法/语法分析**（parser）-- 验证语法，生成解析树
2. **语义分析**（analyzer）-- 验证语义，生成查询树
3. **查询重写**（rewriter）-- 展开视图和规则
4. **查询优化**（planner）-- 逻辑 + 物理优化，生成执行计划
5. **查询执行**（executor）-- 执行计划

优化器结合两种方法：
- **基于规则的优化（RBO）** -- 逻辑重写规则，始终能改善性能（如谓词下推、连接重排序）
- **基于成本的优化（CBO）** -- 物理优化，估计不同访问路径的成本

### 成本模型

总成本 = IO 成本 + CPU 成本 + 通信成本（并行）

关键成本参数：

| 参数 | 默认值 | 说明 |
|-----------|---------|-------------|
| `seq_page_cost` | 1.0 | 顺序扫描每数据块的成本 |
| `random_page_cost` | 4.0 | 索引扫描每数据块的成本 |
| `cpu_tuple_cost` | 0.01 | 处理每行元组的 CPU 成本 |
| `cpu_index_tuple_cost` | 0.005 | 处理每个索引元组的 CPU 成本 |
| `cpu_operator_cost` | 0.0025 | 每次算子执行的 CPU 成本 |

对于 SSD 存储，降低 `seq_page_cost` 和 `random_page_cost`（如 0.5 和 2.0）。CPU 成本与实际 CPU 性能成反比调整。

### 统计信息与选择性

优化器使用统计信息估算行数：
- **表级**：行数、页数（存储在 `sys_class` 中）
- **列级**：空值比例、平均宽度、NDV、MCV、直方图、相关性（存储在 `sys_stats` 中）
- **索引级**：行数、页数
- **扩展多列**：函数依赖、N-distinct、MCV 列表（存储在 `sys_stats_ext` 中）
- **表达式统计**：计算表达式上的统计信息

通过 `ANALYZE` 收集统计信息。默认样本大小：`300 * default_statistics_target = 30000`。

### 逻辑优化规则

由 `kdb_rbo.rbo_rule` 控制（默认关闭）：
- **子查询提升**：将 FROM 中的子查询提升为父查询的 JOIN
- **EXISTS/ANY 子链接转换**：转换为 semi-join/anti-join
- **外连接消除**：当不可能填充 NULL 时将外连接转为内连接
- **无用表消除**：当表仅在连接条件中使用且具有唯一约束时移除该表
- **谓词下推**：将 WHERE/ON/having 条件下推到基表
- **UNION 外条件下推**：将连接条件推入 UNION 子查询
- **COUNT(DISTINCT) 并行优化**：启用并行与哈希聚合
- **DISTINCT 消除**：当列具有唯一约束时跳过 DISTINCT
- **OR 展开**：将 OR 条件拆分为 UNION ALL（由 `kdb_rbo.or_expansion_layer` 控制）

启用特定规则：
```sql
SET kdb_rbo.rbo_rule = on;
SET kdb_rbo.enable_merge_comm_expr = on;
SET kdb_rbo.enable_push_joininfo_to_union = on;
```

## 从执行计划推导优化方向

`explain-plan.md` 文件详细介绍了执行计划的阅读方法。本节侧重于从执行计划中推导优化方向。

### 关键对比点

1. **预估 vs 实际行数**：如果比例超过 10 倍，统计信息已过时 -- 运行 `ANALYZE`
2. **排序方法**："external merge Disk" 表示 `work_mem` 太小
3. **连接方法不匹配**：小结果集上的 Hash Join 应使用 Nested Loop；大排序数据应使用 Merge Join
4. **大表上有选择性过滤却全表扫描**：考虑添加索引
5. **Rows Removed by Filter**：高移除数表明选择性差或缺少索引

### 计划调整策略

- 修复统计信息：`ANALYZE table_name`
- 调整索引：创建/删除索引以引导扫描方法
- 重写 SQL：改变连接顺序、添加谓词
- 调优参数：`work_mem`、`shared_buffers`、成本参数
- 使用 HINT：精确控制计划的最后手段

## 模式 1：使用索引

### 索引类型

| 类型 | 最佳适用场景 |
|------|----------|
| Btree（默认） | `=`、`>`、`<`、`>=`、`<=`、`IN`、`LIKE`；ORDER BY、MIN、MAX、MERGE JOIN |
| Hash | 仅等值查询；避免在高重复列上使用 |
| Bitmap | 多属性组合查询 |
| GIN | 数组、全文检索 |
| GiST | 多维数据、几何算子 |
| SP-GiST | 空间划分结构（四叉树、k-D 树） |
| BRIN | 仅追加的时间序列和流数据 |

### 何时不应建索引

- 列上有函数应用（除非使用函数索引）
- 选择性低 -- 全表扫描更高效
- 小表 -- 索引维护成本超过收益
- 大文本/二进制列 -- 存储开销过大

### 创建合适的索引

**缺失索引导致慢查询：**
```sql
-- 优化前：Seq Scan with Filter
CREATE INDEX ON t1(id);
ANALYZE t1;
-- 优化后：Bitmap Heap Scan using index
```

**表达式索引用于函数查询：**
```sql
-- 查询使用 UPPER(name)，普通索引无效
CREATE INDEX idx_t1_name_expr ON t1(UPPER(name));
ANALYZE t1;
-- 现在使用 Bitmap Index Scan on idx_t1_name_expr
```

**组合索引用于多列条件：**
```sql
-- 查询：WHERE t3.id=t4.id AND t4.val = 50 AND t3.val < 150
CREATE INDEX t3_id_val_idx ON t3(id, val);
-- 从 Hash Join（10ms）变为 Nested Loop（1ms）
```

**识别未使用的索引：**
```sql
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM sys_stat_user_indexes
WHERE idx_scan = 0;
```

## 模式 2：更新统计信息

### 过时统计信息示例

```sql
-- 预估 1667 行，实际 3900 行 -- 优化器错误选择了 Bitmap Scan
EXPLAIN ANALYZE SELECT * FROM tt3 WHERE a > 10;

-- 修复：更新统计信息
ANALYZE;

-- 现在正确预估 3900 行，选择 Seq Scan
EXPLAIN ANALYZE SELECT * FROM tt3 WHERE a > 10;
```

### 多列 MCV 统计信息

当多列值存在相关性时，单列统计信息会错误估计：
```sql
-- 由于列 a 和 b 存在相关性，连接过滤预估错误
CREATE STATISTICS tt1_stat(mcv) ON a, b FROM tt1;
ANALYZE tt1;
-- 从 Nested Loop（94ms）变为 Hash Join（8ms）
```

### 表达式统计信息

对于包含计算表达式的查询：
```sql
-- mod(c1,3) 预估：5 行预估，333 行实际
CREATE STATISTICS t1_expr_stat ON (mod(c1,3)) FROM t1;
ANALYZE t1;
-- 现在正确预估 333 行
```

### 自动分析

基于阈值的自动统计信息收集：
```sql
CREATE TABLE s1 (a int, b int) WITH (data_analyze_threshold = 30);
SET auto_analyze TO insert_on;
-- INSERT 30 行后自动触发 ANALYZE
```

模式：`all_on`、`insert_on`、`delete_on`、`update_on`、`copy_on`、`sys_bulkload_on`、`select_into_on`

## 模式 3：增加 work_mem

当排序超出 `work_mem` 时，计划显示 "external merge Disk"：
```sql
SET work_mem = 64;
EXPLAIN ANALYZE SELECT * FROM tt1 ORDER BY a;
-- Sort Method: external merge  Disk: 5872kB
-- Execution Time: 13.935 ms

SET work_mem = 10240;
EXPLAIN ANALYZE SELECT * FROM tt1 ORDER BY a;
-- Sort Method: quicksort  Memory: 10235kB
-- Execution Time: 6.474 ms
```

注意：`work_mem` 是按操作、按会话分配的。并发排序时，总内存 = `work_mem * 操作数 * 会话数`。

## 模式 4：使用分区

### 分区表执行计划优化

分区较多时，计划生成时间增加。使用 `partition_table_limit`：
```sql
-- 当修剪后的分区数 >= 此值时，计划使用父表信息（生成更快）
ALTER SYSTEM SET partition_table_limit = 30;
SELECT sys_reload_conf();
-- 或会话级别：
SET partition_table_limit = 3;
```

### 示例

```sql
CREATE TABLE measurement_range (
    city_id INT NOT NULL,
    logdate DATE NOT NULL,
    peaktemp INT,
    unitsales INT
) PARTITION BY RANGE (logdate);

CREATE TABLE q1 PARTITION OF measurement_range FOR VALUES FROM (MINVALUE) TO ('2006-04-01');
CREATE TABLE q2 PARTITION OF measurement_range FOR VALUES FROM ('2006-04-01') TO ('2006-07-01');
CREATE TABLE q3 PARTITION OF measurement_range FOR VALUES FROM ('2006-07-01') TO ('2006-10-01');
CREATE TABLE q4 PARTITION OF measurement_range FOR VALUES FROM ('2006-10-01') TO ('2007-01-01');
```

适用场景：分区多、索引多、高并发（100+）。不适用于：多级分区、SELECT FOR SHARE/UPDATE、INSERT SELECT、UPDATE/DELETE RETURNING。

## 模式 5：使用物化视图

物化视图缓存复杂查询结果。KingbaseES 不支持自动或增量刷新。

**最佳适用场景：** 低更新量的表配合复杂查询，或频繁访问外部数据源。

```sql
-- 外部表扫描耗时 95ms
CREATE materialized view wrd AS SELECT * FROM words;
CREATE UNIQUE INDEX wrd_word ON wrd(word);
ANALYZE wrd;
-- 相同查询在物化视图上：0.11ms（Index Only Scan）
```

## 模式 6：缓存执行计划

两种协议模式支持计划缓存：

**PBE（扩展协议）：** 缓存由会话管理。参数：
- `plan_cache_mode`：`auto`（默认）、`force_generic_plan`、`force_custom_plan`
- `auto` 模式：前 5 次执行跳过缓存，平均成本后比较再决定是否缓存
- `DISCARD PLANS` 清除所有缓存计划

**Q 消息（简单协议）：** 缓存在共享内存中，以 SQL 哈希为键。
```sql
SELECT * FROM get_plan_cache();           -- 查看所有缓存计划
SELECT remove_all_plan_cache();           -- 全部清除
SELECT remove_plan_cache(sqlid, sqlowner, sqldb); -- 清除指定计划

-- 参数：
-- simple_plan_cache_mode: OFF（默认）、EXACT、FORCE
-- simple_plan_cache_size: 1000（默认，最大缓存计划数）
-- simple_plan_cache_custom: 5（前 N 次执行跳过缓存）
-- simple_plan_cache_notcache_sql: 分号分隔的 SQL 模式，用于排除不缓存的语句
```

Q 协议不缓存：DDL、ORDER/GROUP BY 中包含常量的查询、LIKE 条件、类型转换、无参数的不可变函数、interval/Coalesce 关键字、临时表、列表/数组。

## 模式 7：调整性能参数

### 成本参数

```sql
SET seq_page_cost = 0.5;   -- SSD 环境下降低
SET random_page_cost = 2.0;
```

### 节点控制开关

| 参数 | 说明 |
|-----------|-------------|
| `enable_seqscan` | 允许顺序扫描 |
| `enable_indexscan` | 允许索引扫描 |
| `enable_bitmapscan` | 允许位图扫描 |
| `enable_hashjoin` | 允许哈希连接 |
| `enable_nestloop` | 允许嵌套循环 |
| `enable_mergejoin` | 允许合并连接 |
| `enable_hashagg` | 允许哈希聚合 |
| `enable_sort` | 允许排序 |
| `enable_material` | 允许物化 |

优先使用 HINT 而非全局开关进行有针对性的控制。

### GEQO（遗传查询优化器）

对于 12 张以上表的查询：
- `geqo = on` -- 启用 GEQO（默认）
- `geqo_threshold = 12` -- 触发 GEQO 的表数量
- `geqo_effort = 5` -- 努力程度 1-10（默认 5）

### 内存参数

| 参数 | 默认值 | 用途 |
|-----------|---------|-------|
| `work_mem` | 4MB | 每次排序/哈希操作的内存 |
| `maintenance_work_mem` | 64MB | VACUUM、CREATE INDEX |
| `temp_buffers` | 8MB | 每会话临时表缓冲区 |
| `shared_buffers` | 128MB | 共享数据缓存（RAM 的 20-80%） |

总内存公式：`shared_buffers + wal_buffers + maintenance_work_mem + N*work_mem + 服务进程内存 + M*thread_stack_size`

### 其他参数

| 参数 | 默认值 | 说明 |
|-----------|---------|-------------|
| `cursor_tuple_fraction` | 0.1 | 游标规划：0.1 偏好首行快返回，1.0 偏好总成本最低 |
| `from_collapse_limit` | 8 | 子查询展平阈值 |
| `join_collapse_limit` | 8 | JOIN 重写阈值 |

## 模式 8：使用并行

### 工作原理

优化器在并行执行有益时生成 Gather/GatherMerge 节点。工作进程通过动态共享内存通信。

### 配置参数

**并行限制：**
```
max_worker_processes = 8             # 总工作进程数（需重启）
max_parallel_workers = 8             # 最大并行工作进程数
max_parallel_workers_per_gather = 2  # 每查询最大工作进程数
max_parallel_maintenance_workers = 2 # 维护操作最大工作进程数
```

约束：`max_parallel_workers_per_gather + max_parallel_maintenance_workers <= max_parallel_workers <= max_worker_processes`

**触发条件：**
```
min_parallel_table_scan_size = 8MB   # 并行扫描的最小表大小
min_parallel_index_scan_size = 512KB # 并行扫描的最小索引大小
```

**成本调优：**
```
parallel_setup_cost = 1000  # 降低此值鼓励并行
parallel_tuple_cost = 0.1   # 进程间元组传输成本
parallel_leader_participation = on  # 领导者参与工作
```

**控制开关：**
- `enable_parallel_append = on` -- 并行追加操作
- `enable_parallel_hash = on` -- 并行哈希操作
- `enable_parallel_dml = off` -- 并行 DML（默认关闭）
- `enable_temprel_use_sharedbuffer = 2` -- 临时表共享缓冲区访问

### 支持的操作

- **扫描节点**：Parallel Seq Scan、Parallel Bitmap Scan、Parallel Index Scan
- **连接节点**：Parallel Hash Join、Parallel Merge Join、Parallel Nested Loop（仅外部）
- **物化节点**：Parallel Sort、Partial/Finalize Aggregate
- **控制节点**：Parallel Append

### 强制并行执行

```sql
-- 通过 CREATE TABLE hint
CREATE TABLE test(n INT) WITH (parallel_workers = 4);

-- 通过 SQL HINT
SET enable_hint = on;
SELECT /*+Parallel(t2 2)*/ * FROM t2;

-- 通过 ParallelAppend 用于 UNION ALL
SELECT /*+ParallelAppend(2)*/ * FROM (SELECT * FROM t2 UNION ALL SELECT * FROM t3) a;
```

### 工作进程数与性能

性能不会随工作进程数线性增长。测试显示 3-4 个工作进程后收益递减。在 OLTP 环境中，过多工作进程会与并发会话竞争 CPU 和共享内存。

## 模式 9：SQL 重写 / 查询映射

查询映射基于存储在系统表中的预定义规则转换 SQL 语句。

### 配置

```sql
-- 在 kingbase.conf 中
enable_query_rule = on
query_mapping_spi = semantics  -- 选项：off、semantics、spi、all_on
```

### 创建规则

```sql
-- TEXT 模式：字符串替换，使用 $1、$2 参数代入
SELECT create_query_rule(
    'qm1',                                     -- 规则名称
    'SELECT id,val FROM t1 WHERE id<$1',       -- 匹配模式（$1 = 任意常量）
    'SELECT id FROM t1 WHERE id<($1-5)',       -- 替换 SQL
    true,                                      -- 启用
    'text'                                     -- 模式：text、wildcard、semantics
);

-- WILDCARD 模式：#1、#2 匹配任意内容（不限于常量）
SELECT create_query_rule('qm2', 'SELECT * FROM t WHERE #1 AND val=#2', 'SELECT 1', true, 'wildcard');

-- SEMANTICS 模式：已解析的查询树替换（仅 SELECT 和 CALL）
SELECT create_query_rule('qm3', 'SELECT $1::TEXT AS col', 'SELECT ''2222''', true, 'semantics');
```

### 管理函数

| 函数 | 说明 |
|----------|-------------|
| `create_query_rule(name, match_sql, replace_sql, enabled, mode)` | 创建规则 |
| `drop_query_rule(name)` | 删除指定规则 |
| `drop_query_rule()` | 删除所有规则 |
| `enable_query_rule(name)` | 启用指定规则 |
| `enable_query_rule()` | 启用所有规则 |
| `disable_query_rule(name)` | 禁用指定规则 |
| `disable_query_rule()` | 禁用所有规则 |

### 使用场景

1. **SQL 调优**：用等效的高效形式替换低效 SQL
2. **数据库迁移**：将源数据库语法翻译为 KingbaseES 语法
3. **条件下推**：转换带侧连接的 UNION 查询
4. **CTE 重写**：将简单查询映射为递归 CTE

当 HINT 与查询映射结合使用时，使用 `text` 模式。

## 模式 10：函数结果集缓存

缓存不可变、稳定或 result_cache 函数在单次 SQL 执行中的结果。

```sql
SET function_result_cache = on;
SET function_cache_number = 100;
```

示例：对于高重复列，`return_id(id)` 在未启用缓存时执行 6 次，启用缓存后仅执行 3 次。SQL 执行完成后释放缓存。

## 模式 11：缓存大小限制

控制会话级缓存的内存消耗：

```sql
SET session_plan_cache_size = 10;    -- MB，控制 PBE 计划缓存
SET session_catcache_size = 10;      -- MB，控制 syscache/relcache
```

通过 `memstat` 扩展监控：
```sql
CREATE EXTENSION memstat;
SELECT sum(totalspace)/1024/1024 FROM local_memory_stats() WHERE name = 'CachedPlan';
```

当 `cache_size > limit * 90%` 时，释放 10% 的缓存。仅在内存受限时使用 -- 可能降低性能。

## 模式 12：HINT 使用

### 启用 HINT

```sql
SET enable_hint = on;
-- 可选：调试输出
SET hint_debug_print = on;
SET hint_message_level = 'info';
```

### HINT 语法

放在 SELECT/UPDATE/DELETE/INSERT/MERGE 之后：`/*+HINT(arg)*/`

**HINT 中的表名**使用 SQL 别名。对于嵌套查询：`子查询名.表名` 或使用 `blockname(name)` 为子查询命名。

### 扫描 HINT

| HINT | 说明 |
|------|------|
| `SeqScan(t1)` | 偏好顺序扫描 |
| `IndexScan(t1 idx_name)` | 偏好索引扫描，可指定具体索引 |
| `IndexOnlyScan(t1)` | 偏好仅索引扫描 |
| `BitmapScan(t1)` | 偏好位图扫描 |
| `ForceSeqScan(t1)` | 强制顺序扫描 |
| `ForceIndexScan(t1 idx)` | 强制索引扫描 |
| `NoSeqScan(t1)` | 避免顺序扫描 |
| `NoIndexScan(t1)` | 避免索引扫描 |
| `NoBitmapScan(t1)` | 避免位图扫描 |

```sql
-- 强制顺序扫描而非索引扫描
SELECT /*+SeqScan(t1)*/ * FROM t1 WHERE id = 20;

-- 在分区表上使用全局索引
SELECT /*+IndexScan(pt pt_col2_idx_global)*/ * FROM pt WHERE col2 < 10;
```

### 并行 HINT

| HINT | 说明 |
|------|------|
| `Parallel(t1 2)` | 强制指定并行度的并行扫描 |
| `ParallelAppend(2)` | 并行 UNION/UNION ALL 执行 |

```sql
SELECT /*+Parallel(t2 2)*/ t2.id FROM t2, t3 WHERE t2.id = t3.val GROUP BY t2.id;
```

### Rows HINT

| HINT | 说明 |
|------|------|
| `Rows(t1 #5)` | 将预估行数设为 5 |
| `Rows(t1 +100)` | 在当前预估基础上加 100 |
| `Rows(t1 *2)` | 将预估行数乘以 2 |
| `PRows(t5 t4 #1)` | 用于参数化路径 |
| `Grows(t2.id #2)` | 用于 GROUP BY 组数 |

```sql
-- 修正错误的行数预估：t2 预估 1589，实际 5
SELECT /*+Rows(t2 #5)*/ t2.id FROM t2, t3 WHERE t2.id = t3.val AND t3.id < 5;
-- 优化器现在选择 Nested Loop 而非 Merge Join
```

### 连接 HINT

| HINT | 说明 |
|------|------|
| `NestLoop(t1 t2)` | 强制嵌套循环连接 |
| `HashJoin(t1 t2)` | 强制哈希连接 |
| `MergeJoin(t1 t2)` | 强制合并连接 |
| `NoHashJoin(t1 t2)` | 避免哈希连接 |
| `materialize(t1 t2)` | 强制嵌套循环且内表物化 |
| `use_nl_with_index(t1)` | 嵌套循环配合有索引的内表 |

```sql
-- 从 Merge Join 改为 Nested Loop
SELECT /*+NestLoop(t2 t3)*/ t2.id FROM t2, t3 WHERE t2.id = t3.val;
```

### Leading HINT（连接顺序）

| HINT | 说明 |
|------|------|
| `leading(t3 t2 t1)` | 先连接 t3 与 t2，再连接 t1（未指定内外表） |
| `leading(((t1 t3) t2))` | t1 连接 t3（t1=外表、t3=内表），结果再连接 t2 |
| `ordered` | 按 SQL 中出现的顺序连接表（优先级高于 leading） |

```sql
-- 同时指定连接顺序和内外表
SELECT /*+leading(((t1 t3) t2))*/ t2.id FROM t1, t2, t3 WHERE ...;
```

### Set HINT

| HINT | 说明 |
|------|------|
| `Set(enable_mergejoin off)` | 禁用合并连接 |
| `Set(work_mem 8192)` | 设置 work_mem（同时影响计划器和执行器） |
| `Set(plan_cache_mode force_generic_plan)` | 强制通用计划缓存 |
| `Set(plan_cache_mode force_custom_plan)` | 强制每次执行自定义计划 |

```sql
-- 组合 work_mem 和聚合 HINT
SELECT /*+Set(work_mem 8192) parallelhashagg*/ id FROM t6 GROUP BY id;
```

### 聚合 HINT

| HINT | 说明 |
|------|------|
| `hashagg` | 使用哈希聚合 |
| `groupagg` | 使用排序分组聚合 |
| `parallelhashagg` | 使用并行哈希聚合 |
| `parallelgroupagg` | 使用并行排序分组聚合 |
| `unihashagg` | 使用组合哈希聚合 |

### Blockname HINT

为子查询命名以进行跨块 HINT 引用：
```sql
SELECT /*+HashJoin(t2 blk.t2)*/ t2.id
FROM t2 WHERE t2.id IN (
    SELECT /*+blockname(blk)*/ id FROM t2 WHERE t2.val < 9
);
```

### HINT 与查询映射结合

当无法修改应用 SQL 时，将查询映射与 HINT 结合使用：
```sql
SELECT create_query_rule(
    'qm1',
    'SELECT * FROM t WHERE id=1',
    'SELECT /*+SeqScan(t)*/ * FROM t WHERE id=1',
    true,
    'text'
);
```

### 存储过程 HINT

在调用过程时应用 HINT：
```sql
CALL /*+Set(work_mem 2MB)*/ foo_sel(10, 30);
```

支持的 GUC 参数：节点控制开关和 `work_mem`。

### HINT 常见问题

- HINT 中的表名必须与 SQL 别名匹配，而非物理表名
- 每个子查询只能有一个 `leading` HINT；必须包含所有连接的表
- 强制并行需要 `max_parallel_workers_per_gather >= 请求的工作进程数`
- 函数中的 HINT 仅在与 `text` 模式的查询映射结合使用时有效
- 调试输出：`SET hint_debug_print = on; SET hint_message_level = 'info';` 显示已使用、未使用、重复和错误的 HINT

## 最佳实践

1. 在进行其他优化之前，始终先检查统计信息：`ANALYZE table_name`
2. 对关联列使用扩展统计信息（MCV、ndistinct、dependencies）
3. 优先调优 `work_mem` 而非使用磁盘排序/哈希操作
4. 对大表扫描（>8MB）使用并行查询，但在 OLTP 环境中限制工作进程数
5. 对重复的参数化查询通过 PBE 协议启用计划缓存
6. 仅在其他方法（统计信息、索引、SQL 重写）无效时才使用 HINT
7. 始终使用 `EXPLAIN ANALYZE` 测试所有优化以验证实际改进
8. 当应用 SQL 无法修改时，将查询映射与 HINT 结合使用

---

## 常见慢 SQL 改写模式

### 模式 1：全表扫描（Seq Scan）

**问题表现**
```
Seq Scan ON large_table  (cost=0.00..500000.00 rows=500 width=100)
  Filter: (field = 'value')
```

**解决方案**

**1. 添加合适的索引**
```sql
-- ✅ 创建索引（等值查询）
CREATE INDEX idx_table_field ON large_table(field);

-- ✅ 创建复合索引（多条件）
CREATE INDEX idx_table_field_other ON large_table(field, other_field);

-- ✅ 如果用于排序
CREATE INDEX idx_table_create_time ON large_table(field) INCLUDE other_columns;
```

**2. 改写SQL以利用索引**
```sql
-- ❌ 低效（AND条件，但other_field参与运算）
SELECT * FROM large_table
WHERE field = 'value' AND other_field + 1 = 10;

-- ✅ 高效（改写使索引可用）
SELECT * FROM large_table
WHERE field = 'value' AND other_field = 9;
```

---

### 模式2：大数据排序（Sort / HashAggregate性能差）

**问题表现**
```
Sort (cost=12345.67..12400.00 rows=10000 width=200)
  Sorting Method: External Merge  调用到磁盘
```

**解决方案**

**1. 增大work_mem**
```sql
SET work_mem = '256MB';  -- 根据排序需求调整
```

**2. 使用HINT强制特定算法**
```sql
EXPLAIN sensitize
SELECT /*+ FORCE_SORT */ *
FROM large_table
ORDER BY created_at LIMIT 1000;
```

**3. 改写SQL避免排序**
```sql
-- ❌ 低效：排序+分页
SELECT * FROM large_table ORDER BY created_at LIMIT 10 OFFSET 1000000;

-- ✅ 高效：使用游标或延迟关联（结合OFFSET）
-- 更优：WHERE id > last_id ORDER BY id LIMIT 10
```

**4. 考虑索引覆盖**
```sql
-- 创建包含排序字段的索引
CREATE INDEX idx_table_created_at ON large_table(created_at)
INCLUDE (id, other_columns);

-- 完全覆盖
EXPLAIN SELECT id, name FROM large_table ORDER BY created_at;
-- 期望：Index Only Scan（无回表）
```

---

### 模式3：连接性能差（JOIN瓶颈）

**问题表现**
```
Nested Loop  (cost=... rows=... 10分钟)
  Join Filter: (c.id = o.customer_id)
```

**解决方案**

**1. 正确的连接顺序**
```sql
-- ❌ 低效：大表驱动
Seq Scan ON orders  (100万行)
  Inner Hash Join ON customer_id
    Seq Scan ON customers  (1000行)

-- ✅ 高效：从小表驱动
Seq Scan ON customers  (1000行)
  Inner Hash Join ON customer_id
    Seq Scan ON orders  (100万行)
```

**使用Leading Hint控制连接顺序**
```sql
SELECT /*+ leading(customers orders) */ * FROM customers JOIN orders ...;
```

**2. 选择合适的JOIN算法**
```sql
-- NESTLOOP适合：小表驱动 + 高选择性
-- HASH JOIN适合：大表JOIN + 资源充足
-- MERGE JOIN适合：已排序 + JOIN条件可排序
SELECT /*+ USE_HASH(customers orders) */ * FROM customers JOIN orders ...;
```

**3. 批量数据处理**
```sql
-- ❌ 低效：单条更新（性能差）
UPDATE large_table SET status = 'active' WHERE id = 10000;

-- ✅ 高效：批量更新（In条件）
UPDATE large_table SET status = 'active'
WHERE id IN (SELECT id FROM small_list);

-- 更高效：批量UPDATE
UPDATE large_table SET status = 'active'
WHERE id IN (1, 2, 3, 4, 5, 10000);
```

**4. 避免不必要的连接**
```sql
-- ❌ 低效：冗余连接
SELECT * FROM t1
JOIN t2 ON t1.id = t2.id
JOIN t3 ON t1.id = t3.id
WHERE t2.status = 'active';

-- ✅ 高效：去掉冗余条件
SELECT * FROM t1
JOIN t2 ON t1.id = t2.id
WHERE t2.status = 'active';
-- 如果t3只是冗余或通过t2访问，则去掉
```

---

### 模式4：函数导致索引失效

**问题表现**
```
No Index Scan... (索引存在但未使用)
WHERE DATE(created_at) = '2025-01-01'
```

**解决方案**

**1. 改写为索引列比较**
```sql
-- ❌ 低效：函数影响索引
SELECT * FROM logs WHERE DATE(created_at) = '2025-01-01';

-- ✅ 高效：增加索引或使用函数推导公式
SELECT * FROM logs WHERE created_at >= '2025-01-01' AND created_at < '2025-01-02';

-- ✅ 更高效：添加BETWEEN索引
CREATE INDEX idx_log_created_date ON logs(created_at) include (other_columns);
```

**2. 使用函数索引（Oracle兼容）**
```sql
-- Oracle兼容模式
CREATE INDEX idx_log_date ON logs(DATE(created_at));
```

**3. 删除不必要的日期转换**
```sql
-- ❌ 低效
WHERE YEAR(created_at) = 2025

-- ✅ 高效
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01'
```

---

### 模式5：聚合查询性能差

**问题表现**
```
Aggregate (cost=... rows=1 width=10)
  -> HashAggregate  (cost=... rows=10000 width=10)
    -> Seq Scan ON table  (111万行)
```

**解决方案**

**1. 先过滤再聚合**
```sql
-- ❌ 低效：全表聚合
SELECT dept_name, COUNT(*), AVG(salary)
FROM employees
WHERE year_hire_date >= 2020  -- 只过滤10%,其他90%仍处理

-- ✅ 高效：先过滤
SELECT dept_name, COUNT(*), AVG(salary)
FROM employees
WHERE dept_id = 10
GROUP BY dept_name;
```

**2. 使用DISTINCT而不是GROUP BY**
```sql
-- ❌ 低效：GROUP BY
SELECT d.department, u.user_id FROM departments d JOIN users u ...

-- ✅ 高效：DISTINCT（去重）
SELECT DISTINCT d.department, u.user_id FROM departments d JOIN users u ...
```

**3. 避免在SELECT中使用函数**
```sql
-- ❌ 低效：不必要的函数计算
SELECT COUNT(*) FROM users WHERE LOWER(name) = 'test';

-- ✅ 高效：通过索引或CUF实现
-- 方案1：优化数据结构
-- 方案2：使用UNION实现
SELECT * FROM users WHERE name = 'test' UNION ALL SELECT * FROM users WHERE name = 'TEST';
```

---

### 模式6：LIKE查询非索引

**问题表现**
```
Seq Scan ON users  (cost=... rows=100 width=100)
  Filter: (name LIKE '%TOME')
```

**解决方案**

**1. 前导%）确认数据分布**
```sql
-- 如果大量数据匹配前导%
-- 考虑使用全文搜索（Full-Text Search）
CREATE INDEX idx_name_trgm ON users USING gin(name gin_trgm_ops);
```

**2. LIKE '%TOME%'**
```
如果使用gin_trgm索引：
SELECT * FROM users WHERE name LIKE '%TOME%'  -- 可用索引
```

**3. 使用提示或策略**
```sql
-- 使用模糊匹配
SELECT * FROM users WHERE name ILIKE 'TOME%';
```

---

### 模式7：NOT IN vs NOT EXISTS

**问题表现**
```
-- NOT IN可能效率低
SELECT * FROM orders WHERE order_id NOT IN (SELECT order_id FROM returned_orders);
```

**解决方案**

**1. 使用NOT EXISTS**
```sql
SELECT o.* FROM orders o
WHERE NOT EXISTS (
    SELECT 1 FROM returned_orders r WHERE r.order_id = o.order_id
);
```

**2. 如果IN子查询是简单的**
```sql
-- 简单IN，性能可接受
SELECT * FROM orders WHERE order_id IN (
    SELECT order_id FROM returned_orders
    WHERE status = 'returned'
);
```

---

### 模式8：OR条件导致索引失效

**问题表现**
```
-- OR条件可能导致索引不能使用
WHERE field1 = 'value1' OR field2 = 'value2'
```

**解决方案**

**1. 使用UNION ALL替代OR**
```sql
-- ❌ 低效：OR（可能索引失效）
SELECT * FROM users WHERE last_login = '2025-01-01' OR registration_time = '2025-01-01';

-- ✅ 高效：UNION ALL
SELECT * FROM users WHERE last_login = '2025-01-01'
UNION ALL
SELECT * FROM users WHERE registration_time = '2025-01-01';
```

**注意**：UNION ALL的代价是重复数据可能需要去重。

---

### 模式9：子查询嵌套过深

**问题表现**
```
-- 多层子查询
SELECT * FROM (
    SELECT * FROM (
        SELECT * FROM large_table WHERE id = 10
    ) WHERE col1 = 'value'
)
```

**解决方案**

**1. 减少子查询层次**
```sql
-- ❌ 低效：嵌套子查询
SELECT * FROM (
    SELECT * FROM (
        SELECT a.*, b.value FROM a JOIN b ON a.id = b.parent_id WHERE a.id = 10
    ) WHERE status = 'active'
) t

-- ✅ 高效：单个查询
SELECT a.*, b.value FROM a JOIN b ON a.id = b.parent_id
WHERE a.id = 10 AND a.status = 'active';
```

**2. 转换为JOIN**
```sql
-- 子查询 -> JOIN
SELECT * FROM table1 t1 WHERE id IN (SELECT id FROM table2 t2 WHERE t2.value = 'X');

-- 转换为JOIN
SELECT t1.* FROM table1 t1 JOIN table2 t2 ON t1.id = t2.id WHERE t2.value = 'X';
```

**3. 使用CTE（Common Table Expression）提高可读性**
```sql
WITH qualified_data AS (
    SELECT a.*, b.value
    FROM a JOIN b ON a.id = b.parent_id
)
SELECT * FROM qualified_data WHERE status = 'active';
```

---

### 模式10：使用删除列表删除

**问题表现**
```
DELETE FROM large_table WHERE id IN (SELECT id FROM small_list WHERE should_delete = 1);
```

**解决方案**

**1. 使用EXISTS**
```sql
DELETE FROM t1
WHERE EXISTS (SELECT 1 FROM t2 WHERE t2.reference_id = t1.id);

-- 或者
DELETE FROM t1 WHERE id IN (SELECT id FROM t2 WHERE t2.should_delete = 1);
```

**2. 使用 correlated UPDATE/DELETE**
```sql
-- 可以在WHERE中使用子查询
DELETE FROM users
WHERE id IN (
    SELECT id FROM orders
    WHERE amount > 10000
);
```

---

### 模式11：时间范围查询效率

**问题表现**
```
-- ❌ 低效：复杂日期计算
SELECT * FROM logs WHERE (DATE(create_time) = '2025-01-01' AND hour(created_time) = 8)
```

**解决方案**

**1. 使用BETWEEN（推荐）**
```sql
-- ✅ 高效（如果已有索引）
SELECT * FROM logs WHERE create_time > '2025-01-01 08:00:00' AND create_time <= '2025-01-01 09:00:00';

-- ✅ 更高效：使用索引
SELECT * FROM logs WHERE create_time BETWEEN '2025-01-01 08:00:00' AND '2025-01-02 00:00:00';
```

**2. 添加索引**
```sql
CREATE INDEX idx_log_create_time ON logs(create_time) INCLUDE (other_columns);
```

---

### 模式12：分组聚合后再次过滤

**问题表现**
```
-- ❌ 低效：聚合后过滤
SELECT dept_id, AVG(salary) as avg_salary
FROM employees
WHERE year_hire_date >= 2020
GROUP BY dept_id
HAVING AVG(salary) > 50000;

-- 如果无法用WHERE提前过滤则需谨慎
```

**解决方案**

**1. 尽量在WHERE中过滤**
```sql
-- ✅ 优先使用WHERE过滤
SELECT dept_id, AVG(salary) as avg_salary
FROM employees
WHERE year_hire_date >= 2020
GROUP BY dept_id;
```

**2. HAVING合理使用**
```sql
-- ✅ 使用HAVING做聚合后的过滤（必需时）
SELECT dept_id, AVG(salary) as avg_salary
FROM employees
GROUP BY dept_id
HAVING AVG(salary) > 50000 AND COUNT(*) >= 10;
```

---

## 高级SQL改写模式

### 模式13：CTE提高可读性和性能

**使用场景**：
- 连接多表并重复使用中间结果集
- 嵌套子查询改写

```sql
-- ❌ 低效：嵌套子查询
SELECT * FROM (
    SELECT * FROM (
        SELECT a.*, b.value
        FROM a JOIN b ON a.id = b.parent_id
        WHERE a.active = true
    ) t1
    JOIN c ON t1.id = c.id
) t2 WHERE t2.status = 'active';

-- ✅ 高效：使用CTE
WITH qualified_a AS (
    SELECT a.*, b.value
    FROM a JOIN b ON a.id = b.parent_id
    WHERE a.active = true
)
SELECT qa.*, c.status FROM qualified_a qa JOIN c ON qa.id = c.id WHERE c.status = 'active';
```

### 模式14：SEMI JOIN改写

**使用场景**：`EXISTS`或`IN`子查询优化

```sql
-- ❌ 低效：IN（可能转换为SEMI JOIN但性能不稳定）
SELECT * FROM orders
WHERE order_id IN (SELECT order_id FROM shipments);

-- ✅ 高效：使用SEMI JOIN特性
SELECT * FROM orders
WHERE EXISTS (SELECT 1 FROM shipments WHERE shipments.order_id = orders.order_id);

-- 期望优化器自动转换为SEMI JOIN
```

### 模式15：窗口函数优化聚合

**使用场景**：需要聚合同时保留行数据

```sql
-- ❌ 低效：相关子查询
SELECT t1.*, (SELECT COUNT(*) FROM t2 WHERE t2.group_id = t1.group_id) as cnt
FROM t1;

-- ✅ 高效：窗口函数
SELECT t1.*, SUM(cnt) OVER (
    PARTITION BY group_id ORDER BY created_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
) as running_total
FROM t1, (
    SELECT group_id, COUNT(*) as cnt
    FROM t2
    GROUP BY group_id
) t2r WHERE t1.group_id = t2r.group_id;
```

---

## SQL改写最佳实践

### 1. 始终使用EXPLAIN ANALYZE验证

```sql
-- 改写前
EXPLAIN ANALYZE SELECT * FROM ...;

-- 改写后
EXPLAIN ANALYZE SELECT ...;

-- 对比执行计划变化
```

### 2. 优先使用INDEX SCAN

```sql
-- 检查是否使用了索引
SELECT * FROM sys_stat_user_indexes WHERE idx_scan = 0;

-- 如果没有使用，检查统计信息
ANALYZE table_name;
```

### 3. 避免在WHERE中使用函数

```sql
-- ❌ 低效
WHERE YEAR(created_at) = 2025

-- ✅ 高效
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01'
```

### 4. 连接顺序从小到大

```sql
-- ❌ 低效：大表驱动
SELECT * FROM t_large JOIN t_small ON t_large.id = t_small.id;

-- ✅ 高效：小表驱动
SELECT /*+ leading(t_small t_large) */ * FROM t_small JOIN t_large ...
```

### 5. 分页查询处理

**LIMIT OFFSET问题**
```sql
-- ❌ 性能问题：OFFSET 1000000
SELECT * FROM large_table ORDER BY id LIMIT 10 OFFSET 1000000;

-- ✅ 高效：使用游标或WHERE条件
SELECT * FROM large_table WHERE id > last_id ORDER BY id LIMIT 10;

-- ✅ 使用延迟关联
SELECT d.* FROM (
    SELECT id FROM large_table ORDER BY id LIMIT 10 OFFSET 1000000
) d JOIN large_table ON large_table.id = d.id;
```

### 6. 批量操作优于单条

```sql
-- ❌ 低效：单条UPDATE
UPDATE large_table SET status = 'active' WHERE id IN (SELECT id FROM list WHERE flag=1);
-- 内部优化器可能拆为1万次UPDATE

-- ✅ 高效：一次性UPDATE多行
UPDATE large_table SET status = 'active'
WHERE id IN (1, 2, 3, 10000, 10001, 10002);
```

---

## 改写案例

### 案例1：电商订单查询优化

**原始查询**
```sql
SELECT o.*, c.*, p.*
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN products p ON o.product_id = p.id
WHERE o.order_date BETWEEN '2025-01-01' AND '2025-01-31'
AND c.region = 'North'
AND p.category = 'Electronics';
```

**问题分析**
- 多个RANGE条件（date, region, category）
- JOIN顺序可能不合理
- 没有特定索引但应当使用复合索引

**优化方案**
```sql
-- 添加复合索引
CREATE INDEX idx_orders_customer_product_date
ON orders(customer_id, product_id, order_date)
INCLUDE (status, total);

-- 可选：改写为CTE提高可读性
WITH annual_orders AS (
    SELECT o.*, c.region as customer_region, p.category as product_category
    FROM orders o JOIN customers c ON o.customer_id = c.id JOIN products p ON o.product_id = p.id
    WHERE o.order_date BETWEEN '2025-01-01' AND '2025-01-31'
)
SELECT * FROM annual_orders
WHERE customer_region = 'North' AND product_category = 'Electronics';

-- 使用HINT控制执行计划
SELECT /*+ leading(c p o) */
    o.*, c.*, p.*
FROM orders o
JOIN customers c ON o.customer_id = c.id AND c.region = 'North'
JOIN products p ON o.product_id = p.id AND p.category = 'Electronics'
WHERE o.order_date BETWEEN '2025-01-01' AND '2025-01-31';
```

---

### 案例2：日志查询优化

**原始查询**
```sql
SELECT * FROM system_logs
WHERE date = '2025-01-15'
AND level IN ('ERROR', 'FATAL')
AND message LIKE '%timeout%';
```

**问题分析**
- IN条件使用不当
- 提取date格式函数可能影响索引
- LIKE前导%导致索引失效

**优化方案**
```sql
-- 方案1：改写LIKE为索引列
-- 创建gin_trgm索引
CREATE INDEX idx_logs_message_pattern ON system_logs USING gin(message gin_trgm_ops);

-- 优化查询（如果gin_trgm索引存在）
SELECT * FROM system_logs
WHERE date = '2025-01-15'
AND level IN ('ERROR', 'FATAL')
AND message LIKE '%timeout%';  -- gin_trgm才能高效处理

-- 方案2：如果message内容不是关键匹配，只使用date和level
SELECT * FROM system_logs
WHERE date = '2025-01-15'
AND level IN ('ERROR', 'FATAL');

-- 方案3：使用UNION ALL处理多个条件
SELECT * FROM system_logs
WHERE date = '2025-01-15'
AND level = 'ERROR'
AND message LIKE '%timeout%'
UNION ALL
SELECT * FROM system_logs
WHERE date = '2025-01-15'
AND level = 'FATAL'
AND message LIKE '%timeout%';
```

---

## 总结

SQL改写的核心原则：

1. **让查询利用索引**：优先使用WHERE等值比较
2. **减少数据扫描量**：先过滤再JOIN再聚合
3. **合理使用连接顺序**：小表驱动大表
4. **避免函数**：不要在WHERE中用函数操作列
5. **验证改写结果**：永远使用EXPLAIN ANALYZE

改写SQL时：
- 先诊断（看执行计划）
- 再改写（避免全表扫描、优化JOIN、缩小结果集）
- 验证（对比执行计划、验证实际性能）

对于遇到的具体慢查询，使用EXPLAIN ANALYZE查看执行计划，然后对照本文档的相应模式进行改写。
