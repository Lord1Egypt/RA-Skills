# sys_rman 备份恢复操作

## sys_rman 概述

sys_rman 是 KingbaseES 的物理备份恢复工具，基于 WAL 归档实现增量备份。

## 基本语法

```bash
# 全量备份
sys_rman backup -B full -D /data/kingbase/data -U SYSTEM

# 增量备份
sys_rman backup -B incremental -D /data/kingbase/data -U SYSTEM

# 查看备份集
sys_rman list -D /data/kingbase/data

# 恢复
sys_rman restore -D /data/kingbase/data -l /data/kingbase/data/recovery.signal

# 恢复至指定时间点
sys_rman restore -D /data/kingbase/data -t "2024-01-01 12:00:00"
```

## 备份类型

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| full | 全量备份 | 首次备份、定期全量 |
| incremental | 增量备份 | 日常备份，基于上次备份 |
| differential | 差异备份 | 基于上次全量备份 |

## 备份策略示例

```bash
# 每周日全量备份
0 2 * * 0 sys_rman backup -B full -D /data/kingbase/data -U SYSTEM

# 周一到周六增量备份
0 2 * * 1-6 sys_rman backup -B incremental -D /data/kingbase/data -U SYSTEM
```

## 恢复流程

### 完全恢复

```bash
# 1. 停止数据库
sys_ctl stop -D /data/kingbase/data

# 2. 备份当前数据（可选）
cp -r /data/kingbase/data /data/kingbase/data.bak

# 3. 执行恢复
sys_rman restore -D /data/kingbase/data

# 4. 启动数据库
sys_ctl start -D /data/kingbase/data
```

### 时间点恢复（PITR）

```bash
# 恢复至指定时间点
sys_rman restore -D /data/kingbase/data -t "2024-01-01 12:00:00"

# 恢复至指定 SCN
sys_rman restore -D /data/kingbase/data -s 123456789
```

## 备份验证

```bash
# 查看备份集信息
sys_rman list -D /data/kingbase/data

# 验证备份集完整性
sys_rman check -D /data/kingbase/data -b <backup_id>
```

## 注意事项

1. 执行备份前确保归档模式已开启
2. 增量备份需基于已有的全量备份
3. 恢复操作会覆盖现有数据，操作前建议备份
4. 备份目录需有足够空间（全量备份约等于数据目录大小）
5. 定期清理过期备份集以释放空间

## 配置参数

### kingbase.conf

```ini
# 归档配置
archive_mode = on
archive_command = 'cp %p /archive/%f'

# WAL 级别
wal_level = replica
```
