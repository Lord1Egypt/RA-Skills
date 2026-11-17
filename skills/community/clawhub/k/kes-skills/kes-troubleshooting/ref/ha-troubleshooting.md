# 高可用故障排查

## 概述

服务连续性运维的目标是保障需求制定的 RTO 达成，主要工作是识别并处置风险、问题。造成停机的计划外原因包括：站点故障、集群故障、节点故障、网络故障、存储故障、数据损坏、人为错误、资源耗尽。

## 典型问题概览

### 站点故障

站点范围的服务不可用，典型原因包括：站点范围的断电、网络中断、自然灾害导致的站点无法运作。

### 集群故障

集群范围的服务不可用，可能包括：

- 集群节点故障数量超过容错的范围
- 集群管理软件失效导致集群停机
- 特定失效导致集群同步阻塞

### 节点故障

- 节点硬件故障
- 节点操作系统中数据库依赖的子系统故障
- KingbaseES 实例故障

### 网络故障

可能由硬件或软件引起，具体包括：网络中断、端口被屏蔽、DNS 解析失败、网络延迟（高）、丢包、网络分割。

### 人为错误

- 误操作：错误的关闭/重启集群、数据库、集群守护进程
- 配置错误：集群参数、数据库参数、操作系统参数配置错误或遗漏
- 恶意数据修改：篡改数据

### 资源耗尽

- 环境资源：存储容量、存储处理能力、内存容量、CPU 处理能力、网络带宽、文件句柄、信号量等
- 数据库资源：连接数、事务号、对象封锁冲突、license 过期等

## 监控指标

### 集群状态

| 监控项 | 频率 | 告警条件 | 采集命令 |
|--------|------|---------|---------|
| 节点状态 | 1 分钟 | status 非 running；upstream 非 primary | `repmgr cluster show` |
| 守护进程 | 1 分钟 | repmgrd 非 running | `repmgr service status` |
| 流复制 | 1 分钟 | state 非 streaming；sync_state 与预期不符 | `SELECT * FROM sys_stat_replication;` |
| 复制槽 | 10 分钟 | 复制槽个数/active 状态异常 | `SELECT * FROM sys_replication_slots;` |

### 资源耗尽

| 监控项 | 频率 | 告警条件 | 采集命令 |
|--------|------|---------|---------|
| 存储容量 | 5 分钟 | 超过预设比例 | `df -h` |
| CPU/内存/网络/IO | 1 分钟 | 超过预设比例 | nmon |
| 连接数 | 5 分钟 | 超过 max_connections 的 80% | `SELECT count(*) FROM sys_stat_activity WHERE backend_type IN ('client backend', 'walsender');` |
| 长事务 | 1 小时 | age 超过 2^32 - 30000000 | `SELECT pid, datname, query, age(backend_xmin) FROM sys_stat_activity WHERE backend_xmin IS NOT NULL ORDER BY age(backend_xmin) DESC LIMIT 1;` |
| 事务号 | 1 小时 | age/mxid_age 超过 2^32 - 30000000 | `SELECT datname, age(datfrozenxid), mxid_age(datminmxid) FROM sys_database;` |
| 封锁 | 1 分钟 | 等待封锁进程数异常 | `SELECT count(*) FROM sys_locks WHERE granted = false;` |
| License | 每天 | 剩余天数 > 0 且 < 30 | `SELECT get_license_validdays();` |

## 节点状态异常排查

### 网关故障关库（老版本）

**关键错误（kbha.log）**：

```
[WARNING] ping host"10.10.0.1" failed
[DETAIL] average RTT value is not greater than zero
[INFO] stop database ...
```

**原因**：kbha 进程连续多次 ping 信任网关失败后关闭当前节点数据库（2021 年 7 月之前的版本）。

**处理步骤**：

1. 确认是否存在网络波动
2. 如无主库存活：确认主库（数据量最多）后直接启动 `sys_ctl -D data start`
3. 故障节点手动恢复：`kbha -A rejoin -h ${主库IP}`
4. 等待集群自动恢复：`repmgr service status`

### 磁盘故障关库（use_check_disk=on）

**关键错误（kbha.log）**：

```
[ERROR] [thread xx] Failed to check the mount_point_list 6 / 6, all failed
[NOTICE] [thread xx] the use_check_disk = on, will stop the database
[INFO] stop database ...
```

**原因**：kbha 每隔 60 秒检测目录 I/O 状况，连续 mount_check_max_retries（默认 6）次失败后关闭数据库。

**处理方式**：

- 方法 1：设置 `use_check_disk=off`，仅检测不关库
- 方法 2：增大检测次数 `mount_check_max_retries=20`

### 数据库 Coredump

**关键错误（sys_log）**：

```
[PANIC] XXXX
Failed process was running XXXX
```

或 data 目录中出现 core 文件。请联系 KingbaseES 技术服务人员处理。

### 检查点错误

**关键错误**：

```
LOG: invalid primary checkpoint record
PANIC: could not locate a valid checkpoint record
```

**处理步骤**：

1. 获取控制文件中记录的 WAL file 名称：`sys_controldata -D data`（第 8 行）
2. 重置控制文件：`sys_resetwal -l ${WAL file} data`
3. 启动数据库

注意：重置后可能会丢失数据。集群环境下最好只修改主库，修改后备库需重新克隆。

### 时间线错误

**关键错误**：

```
FATAL: requested timeline 6 is not a child of this server's history
```

**处理步骤**：

1. 获取控制文件中记录的 TimeLineID：`sys_controldata -D data`（第 9 行）
2. 删除 `data/sys_wal` 和归档目录中高于该 TimeLineID 的 history 文件
3. 启动数据库

### 存在双主

**关键错误（hamgr.log）**：

```
[ERROR] [thread pid: xx] there may be multiple nodes running as primary, can not do recovery for failed node
```

**处理步骤**：

1. 确认多个主库数据情况：`select sys_current_wal_lsn();`
2. 备份所有主节点数据目录
3. 如果 recovery=automatic，先暂停集群：`repmgr service pause`
4. 关闭数据较少的主库：`sys_ctl -D data stop`
5. 取消暂停：`repmgr service unpause`
6. 恢复原主库为备库：`kbha -A rejoin -h ${新主库IP}`

如新主库时间线较低，使用：`repmgr node rejoin --force-rewind --no-check-wal -h ${新主库IP} -U esrep -d esrep -p ${新主库端口}`

### 无法判断节点是备库（recovery=standby）

**关键错误**：

```
[INFO] unable to connect via ES to host "xxxx", can't confirm if it's a standby node
[INFO] [thread pid: xx] can not do auto-recovery because not confirmed a standby node
```

**处理步骤**：

- SSH/sys_securecmd 连接失败：在主库手动执行 `ssh kingbase@[故障节点IP] date` 排查
- 缺少 standby.signal：在故障节点执行 `touch data/standby.signal`

### 故障节点 TimeLine 更高

**关键错误**：

```
ERROR: this node's timeline is ahead of the rejoin target node's timeline
DETAIL: this node's timeline is 8, rejoin target node's timeline is 7
```

**处理步骤**（确认故障节点无数据需找回后）：

```bash
repmgr node rejoin -h ${主库IP} -U esrep -d esrep -p ${主库端口} --force-rewind --no-check-wal
```

## 守护进程异常

### 节点未注册

**关键错误**：

```
[ERROR] no metadata record for this node - terminating
[HINT] Check that "repmgr (primary|standby) register" was executed
```

**处理**：`repmgr standby register -F`

## 流复制异常

### 缺少 WAL 文件

**关键错误**：

```
FATAL: could not receive data from WAL stream: ERROR: requested WAL segment 000000010000000A00000026 has already been removed
```

**处理步骤**：

1. 主库暂停集群：`repmgr service pause`
2. 备库重做：`repmgr standby clone -F -h ${主库IP} -U esrep -d esrep -p ${主库端口} --fast-checkpoint`
3. 启动并注册：`sys_ctl -D data start` 然后 `repmgr standby register -F`
4. 取消暂停：`repmgr service unpause`

## 复制槽异常

- **数量/类型异常**：确认是否符合预期。非预期时手动创建或删除：
  - `select sys_create_physical_replication_slot('名称');`
  - `select sys_drop_replication_slot('名称');`
- **活动状态异常**：修复备机故障或复制状态异常即可自动恢复

## 数据库进程无响应

**排查步骤**：

1. `top` 查看进程状态，确认 S 列为 D（不可中断睡眠）
2. 如果是 D 状态，说明请求在 OS 内核中没有响应
3. 通过 `cat /proc/<PID>/stack` 获取进程调用栈
4. 协调 OS 工程师排查存储/I/O 问题
5. 非 D 状态的无响应，排查资源耗尽类问题

## 资源耗尽处理

### 存储容量

| 原因 | 紧急处理 | 完整处理 |
|------|---------|---------|
| 残留临时文件 | 手动删除 | 更新到 R6 最新版 |
| 表膨胀 | 删除低使用率索引 | 处理表索引膨胀 |
| 业务增长 | 创建表空间迁移/历史数据压缩 | 扩容存储 |
| 备机故障 | 手动删除复制槽 | 恢复备节点 |
| 归档失败 | archive_command 置空重载 | 修复归档问题 |

### 连接数

- **紧急处理**：释放空闲连接池连接，或调整 max_connections（需重启）
- **完整处理**：根据新业务模式调整连接数总量或各业务连接池参数

### 长事务

| 原因 | 紧急处理 | 完整处理 |
|------|---------|---------|
| 客户端工具未关闭 | 终止连接 | 调整空闲连接自动断开参数 |
| 应用缺陷 | 取消/终止连接 | 修复缺陷并更新应用 |
| 两阶段提交未结束 | 回滚事务 | 确认业务逻辑后处理 |
| 性能/资源阻塞 | 依赖性能诊断 | 依赖性能优化 |

### 事务号使用

- **清理未启动**：确认 age 最长对象，手动 `VACUUM FREEZE VERBOSE`，临时表则终止使用进程
- **长事务**：参见长事务处理
- **残留复制槽**：短时间无法恢复备节点时手动删除复制槽

### 封锁

- **DDL 持有高级别锁**：取消/终止对应操作，变更操作方式或时间段
- **长事务阻塞**：参见长事务处理

### License

- **试用版到期**：替换可用试用 license，申请新 license
- **未使用正确 license**：使用正确的 license 替换

## 事务状态访问异常

**常见报错**：

```
could not access status of transaction xxxx
could not open file "sys_xact/xxxx": No such file or directory
```

**排查思路**：

1. 新 xact 文件丢失：`sys_controldata data目录 | grep NextXID` 对比报错事务 ID
2. 旧 xact 文件被异常清理：查找存储异常信息
3. 被 frozen 的数据元组：通过 pageinspect 插件检查元组头信息
4. 数据损坏导致 xid 异常：使用 `for i in {1..N}; do printf '125'; done > xxxx` 创建丢失的 xact 文件（N=32*block_size）
