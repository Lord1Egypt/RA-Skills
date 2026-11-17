# KingbaseES 高可用与远程复制指南

包括远程复制（RWC）、HA 集群、故障切换、读写分离和监控配置。

## 1. 远程复制

### 架构概述

KingbaseES 远程复制基于 WAL 流复制，支持主从架构：

```
主库(Primary) --WAL流→ 备库(Standby)
       ↓                    ↓
   读写                只读(可选)
```

### 配置步骤

**主库配置**
```bash
# 1. kingbase.conf
max_wal_senders = 10
wal_level = replica
max_replication_slots = 10

# 2. sys_hba.conf 允许复制连接
host    replication    krc_user    192.168.1.0/24    scram-sha-256

# 3. 创建复制用户
CREATE ROLE krc_user WITH REPLICATION LOGIN PASSWORD 'replica_password';

# 4. 重启主库
systemctl restart kingbase
```

**备库配置**
```bash
# 1. 从主库做基础备份
sys_basebackup -h primary_host -p 54321 -U krc_user -D $KINGBASE_HOME/data -Fp -Xs -P

# 2. 配置备库 kingbase.conf
hot_standby = on
primary_conninfo = 'host=primary_host port=54321 user=krc_user password=replica_password'
primary_slot_name = 'standby_slot'

# 3. 创建备库信号文件
touch $KINGBASE_HOME/data/standby.signal

# 4. 启动备库
systemctl start kingbase
```

### 复制模式

| 模式 | 配置 | 特点 |
|------|------|------|
| 异步复制 | 默认 | 性能高，故障可能丢数据 |
| 同步复制 | `synchronous_standby_names = 'standby_slot'` | 零数据丢失，性能较低 |
| quorum | `synchronous_standby_names = '2 (standby1,standby2,standby3)'` | 多数确认，折中方案 |
| all | `synchronous_standby_names = 'ALL'` | 所有备库确认，最安全 |
| custom | 自定义表达式 | 灵活配置 |

### synchronous_commit 级别

| 级别 | 说明 |
|------|------|
| off | 不等待 WAL 落盘，性能最高但可能丢数据 |
| local | 仅等待本地 WAL 落盘 |
| remote_write | 等待同步备库 WAL 写入（默认） |
| on | 等待同步备库 WAL 刷盘 |
| remote_apply | 等待同步备库应用 WAL，最强一致性 |

### 复制状态监控

```sql
-- 主库查看复制状态
SELECT
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    sync_state
FROM sys_stat_replication;

-- 备库查看延迟
SELECT
    now() - sys_last_xact_replay_timestamp() AS replay_delay,
    sys_is_in_recovery() AS is_standby;
```

---

## 2. HA 高可用集群

### HA 架构

KingbaseES 原生高可用通过 repmgrd 守护进程和 kbha 实现，集群元数据存储在 esrep 数据库的 repmgr 模式下。

```
     ┌─────── 虚拟IP / 应用连接 ───────┐
     ↓                                   ↓
[主库] ←──── 心跳 + WAL 同步 ───→ [备库]
  ↑                                     ↑
应用                              repmgrd 监控
  ↓                                   ↓
repmgrd                           故障时自动提升
```

### repmgrd 守护进程

repmgrd 是 KingbaseES 原生 HA 管理守护进程，负责：
- 集群节点监控与健康检查
- 自动故障切换
- 主备同步状态管理
- 读写分离支持

**配置文件**：`repmgr.conf`

```ini
# 节点 ID
node_id = 1

# 节点名称
node_name = 'node1'

# 连接信息
conninfo = 'host=192.168.1.1 port=54321 user=esrep dbname=esrep'

# 复制用户
repluser = 'esrep'

# 主节点升主权重（0~100）
priority = 100

# 区域标识
location = 'default'

# 监控间隔
monitor_interval = 10

# 故障切换
event_notification = 'log'
```

### RWC（读写分离集群）

RWC 是 KingbaseES 的读写分离集群方案，提供：
- CLI 和 GUI 两种安装方式
- 原生 VIP 和心跳管理
- 自动故障切换
- 读写分离负载分发

**部署参考**：通过 RWC 安装向导或 CLI 工具部署集群，详细安装流程参见 RWC 快速安装和 CLI/GUI 安装文档。

### 集群元数据查询

集群信息存储在 `esrep` 数据库的 `repmgr` 模式下：

```sql
-- 查看集群节点信息
\c esrep
SELECT * FROM repmgr.show_nodes;
-- 字段：node_id, node_name, active, upstream_node_id, upstream_node_name, type, priority, conninfo

-- 查看集群事件
SELECT * FROM repmgr.events ORDER BY event_timestamp DESC;

-- 获取集群字符串信息
SELECT repmgr.get_cluster_info();

-- 查看集群参数配置
SELECT * FROM repmgr.conf;

-- 查看监控历史
SELECT * FROM repmgr.monitoring_history ORDER BY last_monitor_time DESC;
```

**节点类型（type）**：primary（主节点）、standby（备节点）

**节点状态（status）**：
- `* running`：运行正常
- `failed`：节点故障
- `? unreachable`：节点异常，无法获取状态
- `running as primary`：异常（注册为备库但以主库运行）
- `running as standby`：异常（注册为主库以备库运行）

---

## 3. 读写分离

### 架构

```
           ┌── 备库1 (只读)
应用 → RWC ── 主库 (读写)
           └── 备库2 (只读)
```

### RWC 读写分离

RWC 集群原生支持读写分离，配置节点类型为 standby 的备库可接收只读查询。

### 应用层实现

```python
# Python 示例
import kingbase

# 写操作走主库（通过 RWC VIP）
write_conn = kingbase.connect(
    host='vip_host', port=54321, database='test', user='app_user'
)

# 读操作走备库
read_conn = kingbase.connect(
    host='standby_host', port=54321, database='test', user='app_user'
)

# 写
with write_conn.cursor() as cur:
    cur.execute("INSERT INTO orders (...) VALUES (...)")
write_conn.commit()

# 读
with read_conn.cursor() as cur:
    cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    result = cur.fetchall()
```

---

## 4. 故障切换

### 手动切换

```bash
# 方法1：promote 信号文件
touch $KINGBASE_HOME/data/promote
# 备库检测到文件后自动提升为主库

# 方法2：SQL 命令
SELECT sys_promote();

# 方法3：repmgr 命令
repmgr -h standby_host -U esrep standby promote
```

### 自动切换

repmgrd 自动故障切换流程：
1. repmgrd 持续监控主库健康状态
2. 主库不可达时触发故障检测
3. 根据 priority 权重选择备库提升
4. 选中的备库自动 promote 为主库
5. 其他备库重新指向新主库
6. 旧主库恢复后作为备库加入

### 切换后验证

```sql
-- 1. 确认新主库状态
SELECT sys_is_in_recovery();  -- 应返回 false

-- 2. 确认数据完整性
SELECT count(*) FROM important_table;

-- 3. 确认应用连接
SELECT count(*) FROM sys_stat_activity;

-- 4. 查看集群状态
\c esrep
SELECT * FROM repmgr.show_nodes;
```

---

## 5. 复制监控

### 关键指标

| 指标 | 监控方法 | 告警阈值 |
|------|---------|---------|
| 复制延迟 | `replay_lag` | > 10秒 |
| 复制状态 | `sys_stat_replication.state` | 非 streaming |
| WAL 产生速率 | `sys_stat_database.xact_commit` | 突增/突降 |
| 备库只读连接 | `sys_stat_activity` | 异常增长 |
| 磁盘空间 | `df -h` | > 85% |

### 监控脚本

```sql
-- 复制延迟监控
SELECT
    client_addr AS standby_host,
    state,
    now() - sys_last_xact_replay_timestamp() AS replay_delay,
    sys_wal_lsn_diff(sent_lsn, replay_lsn) AS lag_bytes
FROM sys_stat_replication;

-- 复制槽监控
SELECT
    slot_name,
    active,
    sys_wal_lsn_diff(sys_current_wal_lsn(), restart_lsn) AS lag_bytes
FROM sys_replication_slots;

-- 未活动的复制槽会阻止 WAL 清理
```

### 告警脚本示例

```bash
#!/bin/bash
# 复制延迟告警
LAG=$(ksql -U SYSTEM -tAc "
    SELECT EXTRACT(EPOCH FROM (now() - sys_last_xact_replay_timestamp()))
    WHERE sys_is_in_recovery();
")

if [ $(echo "$LAG > 10" | bc) -eq 1 ]; then
    echo "WARNING: replication lag is ${LAG}s" | mail -s "HA Alert" dba@company.com
fi
```

---

## 6. 常见问题

### 问题1：复制延迟过大

**原因**：主库写入量过大、备库性能不足、网络延迟

**解决**：
```sql
-- 1. 检查主库写入负载
SELECT sum(xact_commit) + sum(xact_rollback) AS total_txns
FROM sys_stat_database;

-- 2. 备库增大资源
-- 增大 shared_buffers, work_mem

-- 3. 优化网络
-- 使用专用复制网络
```

### 问题2：备库提升后原主库恢复

**解决**：原主库需要重新作为备库初始化
```bash
# 1. 停止旧主库
systemctl stop kingbase

# 2. 清空数据目录
rm -rf $KINGBASE_HOME/data/*

# 3. 从新主库做基础备份
sys_basebackup -h new_primary -p 54321 -U krc_user -D $KINGBASE_HOME/data

# 4. 配置 standby 信号
touch $KINGBASE_HOME/data/standby.signal

# 5. 启动
systemctl start kingbase
```

### 问题3：脑裂（Split Brain）

**原因**：网络分区导致两个节点都认为自己是主库

**预防**：
- 使用 repmgrd 内置仲裁机制
- 确保心跳网络独立
- 配置合理的节点优先级

---

## 最佳实践

1. **至少一主一备**：生产环境必须有备库
2. **定期演练故障切换**：每季度至少一次
3. **监控复制延迟**：延迟 > 30 秒立即告警
4. **独立心跳网络**：心跳与业务流量隔离
5. **VIP 自动漂移**：应用通过 VIP 连接
6. **WAL 归档保留**：至少保留 7 天 WAL
7. **使用原生 HA**：优先使用 repmgrd/RWC 而非第三方方案
