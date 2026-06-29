---
name: PostgreSQL Query Optimizer
slug: postgres-query-optimizer
description: >
  AI 驱动的 PostgreSQL 查询性能优化专家。分析慢查询日志、执行计划和表结构，
  推荐最优索引策略、查询重写方案和配置调优参数，覆盖全球数百万 PostgreSQL 实例。
version: 1.0.0
author: ai-gaoqian
tags:
  - database
  - postgresql
  - query-optimization
  - sql-tuning
  - performance
metadata:
  openclaw:
    requires: ">=1.0.0"
---

# PostgreSQL Query Optimizer

## 概述

深度 Postgres 查询优化技能，将 EXPLAIN ANALYZE 输出转化为可执行的优化方案。

## 核心能力

### 1. 执行计划分析
- 解析 EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) 输出
- 识别 Seq Scan、Nested Loop 等低效算子
- 评估行数估算偏差（Rows Removed by Filter）
- 分析共享缓冲区命中率

### 2. 索引策略推荐
- 基于查询模式推荐最优索引组合
- 评估部分索引、覆盖索引、表达式索引适用性
- 检测缺失索引和冗余索引
- 生成 CREATE INDEX CONCURRENTLY 语句

### 3. 查询重写
- 优化 JOIN 顺序和类型
- 子查询转 CTE / LATERAL JOIN
- 识别 N+1 查询模式
- WHERE 条件优化（Sargability 检查）

### 4. 配置调优
- work_mem / shared_buffers / effective_cache_size 调优
- random_page_cost 与环境匹配分析
- autovacuum 参数优化建议
- 并行查询配置检查

### 5. 慢查询趋势分析
- 批量分析 pg_stat_statements 数据
- 识别性能退化趋势
- 生成优先级排序的优化清单
- 估算各优化方案的性能提升幅度

## 使用方式

```
分析这条慢查询: <SQL 和 EXPLAIN ANALYZE 输出>
审查数据库索引: <表结构 DDL 和查询模式>
优化查询性能: <查询 SQL 和表行数>
```

## 输出格式

- 问题诊断报告（严重程度、根因分析、修复方案）
- 优化前后对比（预估执行时间、I/O 减少比例）
- 可执行 SQL（索引创建、查询重写）

## 数据底座

基于 PostgreSQL 16 官方文档、The Art of PostgreSQL、Use The Index Luke、pgMustard 分析规则，覆盖 150+ 常见性能反模式和 300+ 检查规则。

## 定价

¥0.50 / 次优化
