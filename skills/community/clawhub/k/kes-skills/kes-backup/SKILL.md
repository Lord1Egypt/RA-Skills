---
name: kes-backup
name_for_command: kes-backup
description: KingbaseES 备份恢复指南。当用户提到备份、KRB 冷备、KRC 热备、逻辑备份、PITR 时间点恢复、增量备份、灾难恢复时，必须使用此技能。
---

# KingbaseES 备份恢复指南

本技能指导用户完成 KingbaseES 的备份和恢复操作，涵盖 KRB 冷备、KRC 热备、逻辑备份、PITR 和增量备份。

## 运维流程（7 步）

```
第1步 定义备份目标 → 第2步 检查系统状态 → 第3步 选择工具链
    → 第4步 执行操作 → 第5步 验证结果 → 第6步 记录文档 → 第7步 设置告警
```

## 场景选择

| 场景 | 工具 | 参考 |
|------|------|------|
| 冷备份（停机） | KRB 离线备份 | `ref/backup-recovery.md` §1 |
| 热备份（在线） | KRC 在线备份 | `ref/backup-recovery.md` §2 |
| 逻辑备份 | sys_dump 工具 | `ref/backup-recovery.md` §3 |
| 时间点恢复 (PITR) | WAL 归档回放 | `ref/backup-recovery.md` §4 |
| 增量备份 | KRC 增量 | `ref/backup-recovery.md` §5 |
| 灾难恢复 | 全量 + WAL 恢复 | `ref/backup-recovery.md` §6 |

## 检查系统状态

```sql
-- 查看数据库版本
SELECT version();

-- 查看表空间使用
SELECT spcname, sys_size_pretty(sys_tablespace_size(spcname)) FROM sys_tablespace;

-- 查看归档状态
SELECT archived, restarted FROM v$archived_log ORDER BY sequence# DESC LIMIT 5;
```

## 验证与告警

**备份验证**：恢复测试到临时环境，校验数据完整性。

**备份告警**：
```sql
-- 检查最近备份时间
-- 表空间使用率告警 (>80%)
SELECT sys_size_pretty(sys_tablespace_size('sys_default'));
```

## 紧急恢复流程

```
1. 评估数据丢失范围 → 确定恢复时间点
2. 准备恢复环境 → 隔离生产流量
3. 执行恢复 → KRC/KRB 恢复
4. PITR → WAL 回放至目标时间
5. 验证数据完整性 → 应用测试
6. 切换流量 → 恢复正常服务
```

## 安全提醒

1. 备份优先：任何破坏性操作前先备份
2. 操作审计：所有运维操作记录审计日志
3. 变更窗口：高风险操作在维护窗口执行
4. 回滚方案：每个操作准备回滚步骤

## 参考文档

```
kes-backup/
├── SKILL.md                 # 本文件
├── ref/
│   ├── backup-recovery.md   # 完整备份恢复操作指南
│   └── sys-rman-ops.md      # sys_rman 物理备份恢复（增量/PITR）
└── test-cases.md
```
