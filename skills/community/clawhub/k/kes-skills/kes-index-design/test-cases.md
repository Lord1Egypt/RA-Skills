---
name: kes-index-design
description: KingbaseES 索引设计 — 测试用例
---

# KingbaseES 索引设计测试用例

## 测试用例 1: 复合索引设计

**场景**：多列查询如何设计索引

**输入问题**："查询有 WHERE name = ? AND age > ?，索引怎么建？"

**期望答案要点**：
- 等值查询列放前面，范围查询列放后面
- `CREATE INDEX idx_name_age ON users(name, age)`

**验证方法**：答案遵循等值先于范围的原则

---

## 测试用例 2: 全文索引

**场景**：需要对文本列做全文搜索

**输入问题**："金仓数据库怎么建全文搜索索引？"

**期望答案要点**：
- 使用 GIN 索引
- `CREATE INDEX idx_fulltext ON content USING GIN(to_tsvector('chinese', content))`

**验证方法**：答案包含 GIN 索引类型

---

## 测试用例 3: 索引维护

**场景**：索引碎片需要清理

**输入问题**："怎么重建索引？哪些索引在使用？"

**期望答案要点**：
- `REINDEX INDEX index_name` 重建索引
- `sys_stat_user_indexes` 查看使用统计

**验证方法**：答案包含 REINDEX 命令
