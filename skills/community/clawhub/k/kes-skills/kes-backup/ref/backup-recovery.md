# KingbaseES 备份与恢复指南

包括离线备份、在线备份、逻辑备份、时间点恢复(PITR)、增量备份和灾难恢复。

## 1. 离线备份（冷备份）

### 适用场景

- 数据库可停机维护
- 全量物理备份
- 灾难恢复基线

### 使用 sys_rman 工具

sys_rman（Kingbase 物理备份恢复工具），类似 Oracle RMAN。

**基本语法**
```bash
# 全量备份
sys_rman backup full -U SYSTEM -W -H localhost -p 54321 -d test

# 指定备份目录
sys_rman backup full -U SYSTEM -W -H localhost -p 54321 -d test -D /backup/krc

# 压缩备份
sys_rman backup full -U SYSTEM -W -H localhost -p 54321 -d test -D /backup/krc --compress
```

**备份类型**
```bash
# 全量备份
sys_rman backup full ...

# 增量备份（基于上一次全量）
sys_rman backup incremental ...

# 差异备份（基于上一次全量）
sys_rman backup differential ...
```

**Oracle RMAN 类比**
```
RMAN:          sys_rman:
backup database;     →  sys_rman backup full
backup incremental   →  sys_rman backup incremental
restore database;    →  sys_rman restore
recover database;    →  sys_rman recover
```

### 恢复步骤

```bash
# 停止数据库
systemctl stop kingbase

# 恢复数据文件
sys_rman restore -D /backup/krc/latest -t $KINGBASE_HOME/data

# 如有WAL归档，执行恢复
sys_rman recover -D /backup/krc/latest --wal-archive /archive/wal

# 启动数据库
systemctl start kingbase
```

### 注意事项

- 离线备份需要停机，适合维护窗口
- 备份目录应与数据目录分离
- 定期测试恢复流程

---

## 2. 在线备份（热备份）

### 适用场景

- 不能停机的生产环境
- 连续保护需求
- RPO要求较低的场景

### 使用 sys_backup 工具

sys_backup 是在线备份工具，基于 WAL 连续归档。

**启动在线备份**
```bash
# 开始在线备份
sys_backup start -U SYSTEM -W -H localhost -p 54321 -d test \
    -D /backup/sys_backup --label daily_backup

# 查看备份状态
sys_backup status -U SYSTEM -W -H localhost -p 54321 -d test

# 停止备份（通常自动停止）
sys_backup stop -U SYSTEM -W -H localhost -p 54321 -d test
```

**配置WAL归档**
```bash
# kingbase.conf 配置
archive_mode = on
archive_command = 'cp %p /archive/wal/%f'
archive_timeout = 300  # 5分钟强制切换WAL
```

**在线恢复**
```bash
# 恢复备份
sys_backup restore -D /backup/sys_backup/daily_backup -t $KINGBASE_HOME/data

# 配置恢复
echo "restore_command = 'cp /archive/wal/%f %p'" >> $KINGBASE_HOME/data/kingbase.conf

# 启动恢复
systemctl start kingbase
```

### 备份策略建议

```
每日增量备份（凌晨2点）
每周全量备份（周日凌晨1点）
每月归档备份（保留6个月）
```

---

## 3. 逻辑备份

### 适用场景

- 跨版本迁移
- 部分表/Schema备份
- 数据导出导入

### 使用 sys_dump 逻辑备份工具

```bash
# 导出整个数据库
sys_dump -U SYSTEM -W -H localhost -p 54321 -d test > /backup/full_dump.sql

# 导出特定表
sys_dump -U SYSTEM -W -H localhost -p 54321 -d test -t table_name > /backup/table_dump.sql

# 导出特定Schema
sys_dump -U SYSTEM -W -H localhost -p 54321 -d test -n schema_name > /backup/schema_dump.sql

# 自定义格式（推荐，支持并行）
sys_dump -U SYSTEM -W -H localhost -p 54321 -d test -F c -f /backup/custom_dump.sys

# 导入数据库
ksql -U SYSTEM -W -H localhost -p 54321 -d test < /backup/full_dump.sql

# 导入自定义格式（支持并行）
sys_restore -U SYSTEM -W -H localhost -p 54321 -d test -j 4 /backup/custom_dump.sys
```

**Oracle 类比**
```
expdp/impdp  →  sys_dump/sys_restore (自定义格式)
exp/imp      →  sys_dump/ksql (SQL格式)
```

### 格式选择

| 格式 | 参数 | 优点 | 缺点 |
|------|------|------|------|
| SQL文本 | 默认 | 可读、可编辑 | 慢、不支持大对象 |
| 自定义 | `-F c` | 快、可并行、压缩 | 二进制、不可编辑 |
| 目录 | `-F d` | 分文件、可并行 | 需要目录空间 |

---

## 4. 时间点恢复（PITR）

### 原理

利用WAL归档将数据库恢复到指定时间点。

### 配置PITR

```bash
# 1. kingbase.conf 配置
archive_mode = on
archive_command = 'cp %p /archive/wal/%f'
wal_level = archive

# 2. 创建备份
sys_backup start -U SYSTEM -W -H localhost -p 54321 -d test \
    -D /backup/sys_backup --label pitr_base
```

### 执行PITR

```bash
# 1. 停止数据库
systemctl stop kingbase

# 2. 恢复基础备份
sys_backup restore -D /backup/sys_backup/pitr_base -t $KINGBASE_HOME/data

# 3. 配置恢复到时间点
# 在 kingbase.conf 中添加
restore_command = 'cp /archive/wal/%f %p'
recovery_target_time = '2025-01-15 14:30:00'
# 或使用其他恢复目标
# recovery_target_xid = '12345'
# recovery_target_name = 'my_restore_point'

# 4. 启动恢复
systemctl start kingbase

# 5. 恢复完成后清理
# 删除 kingbase.conf 中的recovery_target*参数
```

### 恢复目标选项

```sql
-- 按时间点恢复
recovery_target_time = '2025-01-15 14:30:00'

-- 按事务ID恢复
recovery_target_xid = '12345'

-- 按恢复点恢复
recovery_target_name = 'my_restore_point'
-- 提前创建恢复点
SELECT sys_create_restore_point('my_restore_point');

-- 恢复到最后一个可用WAL
recovery_target_time = 'infinity'
```

---

## 5. 增量备份

### 适用场景

- 数据量大、全量备份时间长
- 需要频繁备份
- 存储空间有限

### sys_backup 增量备份

```bash
# 首次全量备份
sys_backup start -U SYSTEM -W -H localhost -p 54321 -d test \
    -D /backup/sys_backup --label full_baseline --level 0

# 增量备份（基于上次备份）
sys_backup start -U SYSTEM -W -H localhost -p 54321 -d test \
    -D /backup/sys_backup --label incr_01 --level 1

# 差异备份（基于全量备份）
sys_backup start -U SYSTEM -W -H localhost -p 54321 -d test \
    -D /backup/sys_backup --label diff_01 --level 2
```

### 增量恢复

```bash
# 恢复顺序：全量 → 增量（按时间顺序）
# 1. 恢复全量备份
sys_backup restore -D /backup/sys_backup/full_baseline -t $KINGBASE_HOME/data

# 2. 应用增量备份
sys_backup apply -D /backup/sys_backup/incr_01 -t $KINGBASE_HOME/data
sys_backup apply -D /backup/sys_backup/incr_02 -t $KINGBASE_HOME/data

# 3. 应用WAL归档（如需要PITR）
# 配置restore_command后启动
```

### 备份计划示例

```
周一 01:00  全量备份（level 0）
周二-周六 02:00  增量备份（level 1）
周日 01:00  全量备份（level 0）
```

---

## 6. 灾难恢复

### 恢复场景

| 场景 | 恢复方案 | RPO |
|------|---------|-----|
| 单表误删 | 逻辑备份恢复单表 | 上次备份时间 |
| 数据库损坏 | PITR到故障前 | 上次WAL归档 |
| 磁盘故障 | 从备份服务器恢复 | 上次备份时间 |
| 站点灾难 | 异地备份恢复 | 异地复制延迟 |

### 单表恢复

```bash
# 方法1：从逻辑备份恢复单表到新库
ksql -U SYSTEM -W -H localhost -p 54321 -d temp_db < /backup/full_dump.sql
sys_dump -U SYSTEM -W -H localhost -p 54321 -d temp_db -t table_name | \
    ksql -U SYSTEM -W -H localhost -p 54321 -d test

# 方法2：从PITR恢复到临时实例
# 1. 将数据库恢复到故障前时间点（临时实例）
# 2. 导出需要的表
# 3. 导入生产库
```

### 异地灾备

```bash
# 主库配置
archive_mode = on
archive_command = 'rsync -az %p standby_server:/archive/wal/%f'

# 备库配置
restore_command = 'cp /archive/wal/%f %p'
hot_standby = on  # 允许备库只读查询
```

---

## 备份验证

### 定期测试

```bash
# 1. 检查备份完整性
sys_backup verify -D /backup/sys_backup/latest

# 2. 恢复测试（临时环境）
sys_backup restore -D /backup/sys_backup/latest -t /tmp/test_restore

# 3. 数据完整性校验
# 启动临时实例后检查
SELECT count(*) FROM important_table;
```

### 监控备份状态

```sql
-- 检查最近备份
SELECT * FROM sys_stat_backup ORDER BY backup_start_time DESC LIMIT 5;

-- 检查WAL归档状态
SELECT archived, sequence#, archived_time
FROM v$archived_log
ORDER BY sequence# DESC LIMIT 10;
```

---

## 最佳实践

1. **3-2-1原则**：3份副本、2种介质、1份异地
2. **定期测试恢复**：至少每季度一次
3. **监控备份成功率**：失败立即告警
4. **保留策略**：全量保留7天、增量保留30天、归档保留90天
5. **加密备份**：敏感数据备份应加密存储
6. **文档记录**：记录备份策略、恢复流程和联系人
