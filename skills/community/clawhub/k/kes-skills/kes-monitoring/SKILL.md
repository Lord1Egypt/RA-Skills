---
name: kes-monitoring
name_for_command: kes-monitoring
description: KingbaseES 监控管理指南。当用户提到监控、NMON、KWR、KSH、sys_stat_statements、性能监控、告警配置、日常巡检时，必须使用此技能。
---

# KingbaseES 监控管理指南

本技能指导用户完成 KingbaseES 的监控和告警配置，涵盖 NMON、KWR、KSH 和 sys_stat_statements。

## 监控模块

| 场景 | 工具 | 参考 |
|------|------|------|
| 系统资源 | NMON / iostat / free | `ref/monitoring.md` §1 |
| 性能指标 | KWR / KDDM | `ref/monitoring.md` §2 |
| 会话管理 | KSH | `ref/monitoring.md` §3 |
| SQL 统计 | sys_stat_statements | `ref/monitoring.md` §4 |
| 告警配置 | 自定义脚本 | `ref/monitoring.md` §5 |

## 日常巡检

```
1. 检查实例状态
   SELECT version();
   SELECT datname, state, restart_required FROM sys_database;

2. 检查连接数
   SELECT count(*) FROM sys_stat_activity;

3. 检查表空间使用
   SELECT spcname, sys_size_pretty(sys_tablespace_size(spcname)) FROM sys_tablespace;

4. 检查死元组
   SELECT relname, n_dead_tup FROM sys_stat_user_tables WHERE n_dead_tup > 10000;

5. 检查长事务
   SELECT pid, now() - xact_start FROM sys_stat_activity
   WHERE state != 'idle' AND xact_start < NOW() - INTERVAL '1 hour';
```

## 告警配置

```sql
-- 连接数告警 (>max_connections * 0.8)
SELECT count(*) FROM sys_stat_activity;

-- 表空间告警 (>80%)
SELECT sys_size_pretty(sys_tablespace_size('sys_default'));

-- 死元组告警
SELECT relname, n_dead_tup FROM sys_stat_user_tables WHERE n_dead_tup > 10000;

-- 长事务告警
SELECT pid, now() - xact_start FROM sys_stat_activity
WHERE state != 'idle' AND xact_start < NOW() - INTERVAL '1 hour';
```

## 参考文档

```
kes-monitoring/
├── SKILL.md              # 本文件
├── ref/
│   ├── monitoring.md                 # 完整监控指南
│   ├── perf-kwr-reports.md           # KWR/KDDM/KSH 报告详解
│   └── perf-views-log.md             # 动态性能视图 + kbbadger
└── test-cases.md
```
