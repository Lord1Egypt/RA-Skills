---
name: kes-db-optim
name_for_command: kes-db-optim
description: KingbaseES 数据库参数调优指南。当用户提到参数优化、shared_buffers、work_mem、容量规划、统计信息、kingbase.conf 调优时，必须使用此技能。
---

# KingbaseES 数据库参数调优指南

本技能指导用户完成 KingbaseES 数据库级别的参数调优、统计信息管理和容量规划。

## 调优流程

1. **评估当前配置** — 检查 kingbase.conf 关键参数
2. **分析资源瓶颈** — CPU / 内存 / 磁盘 IO / 网络
3. **调整参数** — 根据瓶颈修改对应参数
4. **收集统计信息** — 确保优化器有准确的数据
5. **容量规划** — 评估当前和未来的资源需求
6. **验证效果** — 使用 KWR 对比优化前后

## 关键参数参考

**内存参数**：
- `shared_buffers` — 物理内存的 1/3 ~ 1/2
- `work_mem` — 排序/哈希操作内存，根据负载调整
- `maintenance_work_mem` — 维护操作内存（CREATE INDEX / ANALYZE）
- `effective_cache_size` — 物理内存的 3/4 ~ 1 倍

**连接参数**：
- `max_connections` — 最大连接数
- `superuser_reserved_connections` — 超级用户保留连接（默认 3）

**IO 参数**：
- `random_page_cost` — 随机读代价，SSD 建议设为 1.1-1.5
- `effective_io_concurrency` — 有效 IO 并发度，SSD 建议设为 200

## 统计信息管理

```sql
-- 查看统计信息
SELECT * FROM sys_stat_sys_tables;

-- 手动收集统计信息
ANALYZE table_name;

-- 全量统计信息收集
ANALYZE VERBOSE;
```

## VACUUM 自动清理

```sql
-- 启用自动清理
autovacuum = on

-- 手动清理死元组
VACUUM ANALYZE table_name;

-- 高频 DML 表定期维护，日志类表在 logrotate 后清理
```

详见 `ref/db-optimization.md` VACUUM 章节。

## 容量规划

容量规划包含 6 步流程：资源评估 → 增长预测 → 瓶颈识别 → 扩容方案 → 实施计划 → 验证测试。

## 操作系统优化

- 设置合理的磁盘调度算法
- 配置预读参数
- 检查写缓存策略
- 确保文件系统高效

## 参考文档

```
kes-db-optim/
├── SKILL.md      # 本文件
├── ref/
│   ├── db-optimization.md   # 完整参数配置指南
│   ├── statistics.md        # 统计信息管理
│   └── capacity-planning.md # 容量规划 + 内存管理
└── test-cases.md
```
