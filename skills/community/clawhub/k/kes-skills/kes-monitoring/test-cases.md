---
name: kes-monitoring
description: KingbaseES 监控管理 — 测试用例
---

# KingbaseES 监控管理测试用例

## 测试用例 1: 日常巡检

**场景**：每天需要检查数据库健康状态

**输入问题**："金仓数据库日常巡检要检查什么？"

**期望答案要点**：
- 检查实例状态：`SELECT version()`
- 检查连接数：`SELECT count(*) FROM sys_stat_activity`
- 检查表空间使用：`sys_tablespace_size`
- 检查死元组：`sys_stat_user_tables`
- 检查长事务：`sys_stat_activity` 中超过 1 小时的事务

**验证方法**：答案包含巡检 SQL 列表

---

## 测试用例 2: 告警配置

**场景**：需要设置连接数和表空间告警

**输入问题**："金仓数据库怎么设置告警？"

**期望答案要点**：
- 连接数告警：> max_connections * 0.8
- 表空间告警：使用率 > 80%
- 死元组告警：n_dead_tup > 10000
- 长事务告警：超过 1 小时
- 自定义监控脚本实现

**验证方法**：答案包含告警阈值和检查 SQL

---

## 测试用例 3: 性能指标收集

**场景**：需要收集性能指标做趋势分析

**输入问题**："金仓数据库怎么收集性能指标？"

**期望答案要点**：
- KWR 快照收集配置
- KSH 会话历史分析
- sys_stat_statements SQL 统计
- NMON 系统资源监控

**验证方法**：答案包含 KWR/KSH/sys_stat_statements 配置
