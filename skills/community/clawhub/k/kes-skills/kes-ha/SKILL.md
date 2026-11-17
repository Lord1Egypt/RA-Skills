---
name: kes-ha
name_for_command: kes-ha
description: KingbaseES 高可用指南。当用户提到 HA 集群、远程复制 rwc、故障转移、读写分离、主从复制、高可用、RPO/RTO 时，必须使用此技能。
---

# KingbaseES 高可用指南

本技能指导用户完成 KingbaseES 的高可用配置和管理，涵盖 HA 概念、远程复制 (rwc)、故障切换、读写分离和 RWC 集群部署。

## 场景选择

| 场景 | 方案 | 参考 |
|------|------|------|
| HA 概念与选型 | RPO/RTO/可用性级别 | `ref/ha-concepts.md` |
| 主从复制 | 远程复制 (rwc) | `ref/high-availability.md` §1 |
| 自动故障切换 | HA 集群 | `ref/high-availability.md` §2 |
| 读写分离 | 复制 + 代理 | `ref/high-availability.md` §3 |
| RWC 集群部署 | CLI/GUI 安装 + 运维 + 灾备 | `ref/rwc-cluster-deployment.md` |
| 监控告警 | 复制状态监控 | `ref/high-availability.md` §5 |

## 检查系统状态

```sql
-- 查看复制状态
SELECT * FROM v$replication;

-- 查看归档状态
SELECT archived, restarted FROM v$archived_log ORDER BY sequence# DESC LIMIT 5;
```

## 运维流程

```
第1步 定义 HA 目标 → 第2步 检查系统状态 → 第3步 选择方案
    → 第4步 执行配置 → 第5步 验证故障切换 → 第6步 记录文档 → 第7步 设置告警
```

**验证**：故障切换演练，确认 RPO/RTO 达标。

**告警配置**：
```sql
-- 复制延迟告警
SELECT * FROM v$replication;  -- 检查延迟时间

-- 连接数告警
SELECT count(*) FROM sys_stat_activity;  -- > max_connections * 0.8 告警
```

## 安全提醒

1. 备份优先：HA 变更前先备份
2. 故障演练：定期进行故障切换演练
3. 监控复制状态：持续监控复制延迟和连接数

## 参考文档

```
kes-ha/
├── SKILL.md                       # 本文件
├── ref/
│   ├── ha-concepts.md             # HA 概念与选型
│   ├── high-availability.md       # 高可用详细配置
│   └── rwc-cluster-deployment.md  # RWC 集群部署
└── test-cases.md
```
