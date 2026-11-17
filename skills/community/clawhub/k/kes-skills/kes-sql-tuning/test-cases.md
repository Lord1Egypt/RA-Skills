---
name: kes-sql-tuning
description: KingbaseES SQL 调优 — 测试用例
---

# KingbaseES SQL 调优测试用例

## 测试用例 1: 慢查询诊断

**场景**：用户反馈某个查询响应时间从 1 秒变成 10 秒

**输入问题**："一个查询突然变慢了，怎么排查？"

**期望答案要点**：
- 使用 EXPLAIN ANALYZE 分析执行计划
- 检查统计信息是否过期（ANALYZE）
- 使用 KWR 收集快照对比性能变化
- 使用 KDDM 自动诊断

**验证方法**：答案包含 EXPLAIN ANALYZE、KWR 快照、KDDM 诊断

---

## 测试用例 2: TOP SQL 定位

**场景**：数据库整体性能下降，需要定位 TOP SQL

**输入问题**："数据库 CPU 很高，怎么找到最耗资源的 SQL？"

**期望答案要点**：
- 查询 `v$sql_sa_top_sql_cpu_agg` 找 CPU 最高的 SQL
- 查询 `v$sql_sa_top_sql_time_agg` 找执行时间最长的 SQL
- 使用 KWR 报告分析

**验证方法**：答案引用了正确的动态性能视图

---

## 测试用例 3: HINT 使用

**场景**：需要强制 SQL 使用特定执行计划

**输入问题**："怎么让 SQL 强制走索引？"

**期望答案要点**：
- 使用 HINT 控制执行计划
- 参考 ref/sql-optimization-patterns.md 中的 HINT 用法

**验证方法**：答案包含 HINT 语法和使用场景
