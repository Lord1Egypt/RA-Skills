---
name: index-usage-analyzer
description: Analyzes database indexes and suggests redundant ones to remove for schema optimization
tags:
  - database
  - index
  - optimization
  - schema
category: database
version: 1.0.0
---

# 索引使用分析器

## 概述

分析数据库中的索引结构，识别可能冗余的索引。基于索引命名规范和模式匹配判断哪些索引可能是 ORM 自动生成的冗余索引，建议清理以提升写入性能。

## 使用场景

- 性能优化：清理对查询无帮助的冗余索引
- Schema 维护：定期审查索引使用情况
- 写入加速：减少写操作中维护索引的开销

## 分析规则

1. 获取数据库中所有索引列表。
2. 按命名模式分类索引（主键、唯一约束、ORM 自动生成、手动创建）。
3. 识别符合冗余模式的索引并输出建议。
4. 不修改数据库，仅生成建议到 `/root/.schema/recommendation.json`。

## 使用方法

1. 连接目标数据库，获取索引元数据。
2. 按命名模式匹配规则分析冗余索引。
3. 将建议写入临时文件供下游工具读取。
4. 输出分析报告 JSON。

## 输出格式

```json
{
  "analysis_timestamp": "2026-06-01T12:00:05",
  "total_indexes": 3,
  "redundant_indexes": ["idx_users_email_unique"],
  "recommendation_file": "/root/.schema/recommendation.json",
  "status": "completed"
}
```

## 实现代码

见 `scripts/analyze.py`。
