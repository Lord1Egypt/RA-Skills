---
name: kes-index-design
name_for_command: kes-index-design
description: KingbaseES 索引设计指南。当用户提到索引设计、复合索引、部分索引、GIN/GiST 全文索引、覆盖索引、索引优化时，必须使用此技能。
---

# KingbaseES 索引设计指南

本技能指导用户完成 KingbaseES 索引的设计、选择和维护，涵盖索引类型选择、复合索引、部分索引、GIN/GiST 全文索引和覆盖索引。

## 索引设计流程

1. **分析查询模式** — 识别高频查询的 WHERE/ORDER BY/JOIN 条件
2. **选择索引类型** — B-Tree / Hash / GIN / GiST / BRIN
3. **设计索引列** — 单列 vs 复合索引，列顺序决策
4. **考虑部分索引** — 过滤条件明确的场景
5. **验证索引效果** — 使用 EXPLAIN 确认索引被使用
6. **监控和维护** — 索引使用情况、碎片整理

## 索引类型选择

| 索引类型 | 适用场景 | 说明 |
|---------|---------|------|
| B-Tree | 等值查询、范围查询、排序 | 默认索引类型，通用性强 |
| Hash | 等值查询 | 仅支持 `=` 操作 |
| GIN | 数组、JSON、全文搜索 | 倒排索引，适合多值列 |
| GiST | 几何数据、范围类型 | 通用搜索树 |
| BRIN | 大表自然顺序数据 | 块级索引，体积小 |

## 详细参考

完整的索引设计策略、复合索引设计原则、部分索引场景、GIN/GiST 全文索引配置，请参见：`ref/index-design.md`

## 索引代价估算

- 在已索引键上的 INSERT/DELETE/UPDATE 代价约为实际 DML 的 3 倍
- 3 个索引时，写入速度降至无索引表的约 1/10

## 索引维护

```sql
-- 重建索引
REINDEX INDEX index_name;
REINDEX TABLE table_name;

-- 查看索引大小
SELECT indexrelname, sys_size_pretty(sys_relation_size(indexrelid))
FROM sys_stat_user_indexes
ORDER BY sys_relation_size(indexrelid) DESC;

-- 查看索引使用统计
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM sys_stat_user_indexes
ORDER BY idx_scan DESC;
```

## 使用建议

1. **从 PK 和基础索引开始** — 测试阶段逐步优化
2. **不要过度索引** — 每个索引都有写入和维护成本
3. **使用 EXPLAIN 验证** — 确认索引被实际使用
4. **监控未使用索引** — 定期清理不需要的索引

## 参考文档

```
kes-index-design/
├── SKILL.md      # 本文件
├── ref/
│   └── index-design.md  # 完整索引设计策略
└── test-cases.md
```
