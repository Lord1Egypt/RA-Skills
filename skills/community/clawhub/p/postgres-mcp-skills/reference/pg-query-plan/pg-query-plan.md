---
name: pg-query-plan
description: |
  PostgreSQL 查询执行计划分析工具。通过 EXPLAIN 分析查询性能，识别瓶颈，模拟假设索引的影响。
  当用户询问查询为什么慢、如何优化查询、想看执行计划、分析查询性能时使用。
---

## 功能说明

pg-query-plan 帮助理解查询的执行过程，识别性能瓶颈，并提供优化建议。

## 执行流程

### 1. 前置检查

确认 postgres-mcp MCP 工具可用（参考根 SKILL.md 的前置检查）。

### 2. 获取查询

用户提供需要分析的 SQL 查询。

### 3. 执行 EXPLAIN

使用 `analyze_query_plan` 或类似的 MCP 工具获取查询执行计划。

有多种 EXPLAIN 选项：

#### EXPLAIN（基础）
```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 123;
```
- 显示查询计划，但不实际执行
- 成本估算基于统计信息

#### EXPLAIN ANALYZE（推荐）
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
```
- 实际执行查询并收集真实数据
- 显示实际执行时间和行数
- **注意**：会真实执行查询，对于写操作要小心

#### EXPLAIN (ANALYZE, BUFFERS)
```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 123;
```
- 额外显示缓冲区使用情况
- 帮助识别 I/O 瓶颈

#### EXPLAIN (ANALYZE, VERBOSE)
```sql
EXPLAIN (ANALYZE, VERBOSE) SELECT * FROM orders WHERE user_id = 123;
```
- 显示更详细的信息
- 包括输出列、过滤条件等

### 4. 分析执行计划

解读执行计划，识别性能问题：

#### 常见节点类型

**扫描节点**：
- **Seq Scan（顺序扫描）** — 全表扫描，大表上很慢
- **Index Scan（索引扫描）** — 使用索引，通常很快
- **Index Only Scan（仅索引扫描）** — 只读索引，不访问表，最快
- **Bitmap Index Scan** — 位图索引扫描，适合返回多行

**连接节点**：
- **Nested Loop** — 嵌套循环，小表连接快
- **Hash Join** — 哈希连接，大表连接快
- **Merge Join** — 归并连接，已排序数据快

**聚合节点**：
- **Aggregate** — 聚合操作（SUM、COUNT 等）
- **GroupAggregate** — 分组聚合
- **HashAggregate** — 哈希聚合

**排序节点**：
- **Sort** — 内存排序
- **Sort (external merge)** — 磁盘排序，很慢

#### 关键指标

**成本（Cost）**：
- `cost=0.00..100.00` — 启动成本..总成本
- 成本是相对值，用于比较不同计划

**行数（Rows）**：
- `rows=1000` — 预估返回行数
- 如果与实际差距大，说明统计信息过期

**实际时间（Actual Time）**：
- `actual time=0.123..45.678` — 实际执行时间（毫秒）
- 只在 EXPLAIN ANALYZE 中显示

**缓冲区（Buffers）**：
- `Buffers: shared hit=100 read=50` — 缓存命中和磁盘读取
- `hit` 高说明缓存好，`read` 高说明 I/O 瓶颈

### 5. 识别性能瓶颈

根据执行计划识别问题：

#### 全表扫描
```
Seq Scan on orders  (cost=0.00..10000.00 rows=100000)
  Filter: (user_id = 123)
```
**问题**：大表全表扫描
**建议**：在 user_id 上创建索引

#### 排序溢出到磁盘
```
Sort  (cost=5000.00..5500.00 rows=100000)
  Sort Method: external merge  Disk: 12345kB
```
**问题**：内存不足，排序使用磁盘
**建议**：增加 work_mem 或优化查询减少排序数据量

#### 嵌套循环连接大表
```
Nested Loop  (cost=0.00..1000000.00 rows=1000000)
  -> Seq Scan on orders
  -> Index Scan on users
```
**问题**：大表嵌套循环效率低
**建议**：考虑 Hash Join 或添加索引

#### 统计信息不准确
```
Hash Join  (cost=100.00..200.00 rows=100)
  (actual time=1000.00..2000.00 rows=100000)
```
**问题**：预估 100 行，实际 100000 行
**建议**：运行 ANALYZE 更新统计信息

#### 缓存命中率低
```
Buffers: shared hit=10 read=1000
```
**问题**：大量磁盘读取
**建议**：增加 shared_buffers 或优化查询

### 6. 生成分析报告

将执行计划分析整理成易读的报告：

```
🔍 查询执行计划分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 查询：
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending'

⏱️ 执行时间：2.5 秒

🔴 性能瓶颈：

1. 全表扫描 orders 表
   • 扫描 1,000,000 行，只返回 100 行
   • 成本：10000.00
   • 建议：在 (user_id, status) 上创建索引

2. 缓存命中率低
   • 缓存命中：10 块
   • 磁盘读取：1000 块
   • 建议：增加 shared_buffers 或优化查询

💡 优化建议：

CREATE INDEX idx_orders_user_status 
ON orders(user_id, status);

预期效果：查询时间从 2.5s 降至 0.1s（提速 96%）
```

### 7. 模拟假设索引

在不实际创建索引的情况下，预测索引的效果：

```sql
-- 创建假设索引
SELECT * FROM hypopg_create_index(
  'CREATE INDEX ON orders(user_id, status)'
);

-- 查看使用假设索引的执行计划
EXPLAIN SELECT * FROM orders 
WHERE user_id = 123 AND status = 'pending';

-- 清理假设索引
SELECT hypopg_reset();
```

### 8. 提供优化建议

根据分析结果，提供具体的优化建议：

**索引优化**：
- 添加缺失的索引
- 使用覆盖索引（Index Only Scan）
- 考虑部分索引或表达式索引

**查询重写**：
- 避免 SELECT *，只查询需要的列
- 使用 EXISTS 代替 IN（子查询）
- 分解复杂查询为多个简单查询

**配置调优**：
- 增加 work_mem（排序、哈希）
- 增加 shared_buffers（缓存）
- 调整 random_page_cost（SSD）

**统计信息**：
- 运行 ANALYZE 更新统计
- 增加统计目标（ALTER TABLE ... ALTER COLUMN ... SET STATISTICS）

## 使用示例

**基础分析**：
```
用户：这个查询为什么这么慢？
     SELECT * FROM orders WHERE user_id = 123

助手：[执行 EXPLAIN ANALYZE]
     [分析执行计划]
     发现问题：全表扫描 orders 表
     建议：创建索引 CREATE INDEX ON orders(user_id)
```

**对比优化前后**：
```
用户：创建索引后性能提升了多少？

助手：[对比优化前后的执行计划]
     优化前：Seq Scan，2.5s
     优化后：Index Scan，0.1s
     提速：96%
```

**复杂查询分析**：
```
用户：这个 JOIN 查询很慢，帮我看看

助手：[分析多表连接的执行计划]
     [识别连接顺序、连接方式]
     [提供优化建议]
```

## 可视化工具

推荐使用可视化工具更直观地查看执行计划：

- **explain.depesz.com** — 在线执行计划可视化
- **explain.dalibo.com** — 另一个在线工具
- **pgAdmin** — 图形化执行计划
- **DataGrip** — IDE 内置执行计划可视化

## 注意事项

1. **EXPLAIN ANALYZE 会实际执行** — 对于写操作（UPDATE、DELETE）要小心
2. **使用事务回滚** — 分析写操作时用 BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;
3. **统计信息要准确** — 定期运行 ANALYZE 保持统计信息最新
4. **生产环境谨慎** — EXPLAIN ANALYZE 会消耗资源，高峰期避免使用
5. **缓存影响** — 第一次执行和后续执行可能有差异（缓存预热）

## 相关命令

```sql
-- 更新统计信息
ANALYZE orders;

-- 查看表统计信息
SELECT * FROM pg_stats WHERE tablename = 'orders';

-- 查看索引使用情况
SELECT * FROM pg_stat_user_indexes WHERE relname = 'orders';

-- 重置查询统计
SELECT pg_stat_reset();
```
