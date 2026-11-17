# KingbaseES RWC 集群部署与运维指南

包括 RWC 架构、CLI 安装、GUI 安装、日常运维操作、备份恢复、应急预案和灾难恢复演练。

## 1. RWC 架构概述

### 什么是 RWC

RWC（Read-Write Cluster）是 KingbaseES 的读写分离集群方案，通过物理复制保障企业数据的高可用性、数据保护和灾难恢复，同时具备读请求的负载均衡能力。

### 核心组件

```
     ┌─────── 虚拟IP / 应用连接 ───────┐
     ↓                                   ↓
[主库] ←──── 心跳 + WAL 同步 ───→ [备库]
  ↑          │                        ↑
  └──── repmgrd ─────┘               ↑
          │                        repmgrd
          ↓
        kbha (守护进程)
```

| 组件 | 职责 |
|------|------|
| repmgrd | 集群节点监控、健康检查、自动故障切换、主备同步状态管理 |
| kbha | repmgrd 的守护进程，环境监控（网卡、网关、磁盘），repmgrd 进程保护 |
| sys_securecmdd | 集群内节点间的安全命令执行工具，替代 SSH 进行集群通信 |
| VIP | 虚拟 IP，故障时自动漂移，应用通过 VIP 实现透明连接 |

### 复制模式

| 模式 | 配置值 | 特点 |
|------|--------|------|
| 异步复制 | `async` | 性能高，故障可能丢数据 |
| 同步复制 | `sync` | 零数据丢失，性能较低 |
| 优选同步 | `quorum` | 所有备库中最先同步完成的为同步备库 |
| 全同步 | `all` | 所有备库为同步备库，最安全 |
| 自定义 | `custom` | 支持自定义每个节点的同异步类型 |

### 内置保护机制

- **进程保护**：kbha 守护 repmgrd 进程，repmgrd 异常退出时自动重启
- **自动故障切换**：主库不可达时，根据 LSN、priority、node_id 选举备库提升
- **VIP 管理**：VIP 跟随主库，故障切换时自动漂移
- **网络自诊断**：通过 trusted_servers 参数配置信任网关，防止脑裂
- **磁盘自诊断**：检测数据文件所在磁盘是否故障
- **在线块修复**（auto_bmr）：备库检测到坏块时，自动从主库获取正确数据块进行修复
- **集群自启动**：系统重启后，集群自动恢复运行

---

## 2. CLI 安装部署

### 环境准备

**硬件要求**

| 项目 | 最低配置 | 推荐配置 |
|------|---------|---------|
| CPU | 4核 | 8核+ |
| 内存 | 8GB | 16GB+ |
| 磁盘 | 100GB | 500GB+ |

**系统用户与组**
```bash
# 创建 kingbase 用户组
groupadd kingbase

# 创建 kingbase 用户
useradd -g kingbase -m kingbase
```

**OS 服务要求**
```bash
# 关闭 SELINUX
setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config

# 关闭防火墙（或添加端口白名单）
systemctl stop firewalld
systemctl disable firewalld

# 关闭 RemoveIPC
# /etc/systemd/logind.conf
RemoveIPC=no
```

**系统参数配置**

`/etc/security/limits.conf`
```
kingbase  soft  nofile  655360
kingbase  hard  nofile  655360
kingbase  soft  nproc   655360
kingbase  hard  nproc   655360
kingbase  soft  core    unlimited
kingbase  hard  core    unlimited
```

`/etc/sysctl.conf`
```
kernel.sem = 500 1024000 500 1024
```

**时钟同步**：集群节点间必须配置时钟同步（NTP/chrony），否则可能触发错误的故障切换。

### 安装路径规划

```bash
# 推荐路径结构
/opt/kingbase/           # 软件安装目录
/home/kingbase/data/     # 数据目录
```

### 参数配置

**install.conf 核心参数**

配置文件位于安装包目录，部署前需根据实际情况修改。

```ini
# 必填参数
all_ip = 192.168.1.10,192.168.1.11
cluster_name = mycluster
server_user_name = kingbase
kingbase_path = /opt/kingbase

# 网络参数
trusted_servers = 192.168.1.1
virtual_ip = 192.168.1.100
virtual_ip_mask = 24

# 数据库参数
db_port = 54321
system_pass = 12345678ab
max_connections = 100

# 集群参数
synchronous = async
reconnect_attempts = 10
reconnect_interval = 6
recovery = standby
failover = automatic
```

**关键参数说明**

| 参数 | 说明 |
|------|------|
| `trusted_servers` | 信任网关列表（逗号分隔），集群网络自诊断依赖此参数。至少一个可达即可，防止脑裂 |
| `virtual_ip` | 虚拟 IP，必须为无法 ping 通的 IP 地址。支持多 cluster 时可留空 |
| `synchronous` | 同异步模式：async, sync, quorum, all, custom |
| `reconnect_attempts` | 连接重试次数。服务可用优先=3，数据保护优先=10 |
| `reconnect_interval` | 连接重试间隔（秒），最小值 3。服务可用优先=5，数据保护优先=6 |
| `recovery` | 故障自动恢复模式：automatic（所有节点）, standby（仅备机）, manual（关闭） |
| `failover` | 故障自动切换：automatic, manual |
| `running_under_failure_trusted_servers` | 网关故障后数据库是否继续运行：on（默认）/ off |

### 集群部署

部署脚本为 `cluster_install.sh`，根据安装场景不同有四类方式。

**场景 1：root 用户 + SSH 方式**
```bash
# 1. 配置 root 互信
ssh-keygen -t rsa
ssh-copy-id root@node1
ssh-copy-id root@node2

# 2. 执行安装脚本
./cluster_install.sh -i install.conf -ssh -root

# 3. 验证集群状态
repmgr cluster show
```

**场景 2：常规用户 + SSH 方式**
```bash
# 1. 配置 kingbase 用户互信
su - kingbase
ssh-keygen -t rsa
ssh-copy-id kingbase@node1
ssh-copy-id kingbase@node2

# 2. 执行安装脚本
./cluster_install.sh -i install.conf -ssh -user kingbase
```

**场景 3：root 用户 + securecmdd 方式**
```bash
# 1. 在各节点部署 sys_securecmdd 服务
# 2. 执行安装脚本
./cluster_install.sh -i install.conf -scmd -root
```

**场景 4：常规用户 + securecmdd 方式**
```bash
# 1. 在各节点部署 sys_securecmdd 服务
# 2. 执行安装脚本
./cluster_install.sh -i install.conf -scmd -user kingbase
```

> 推荐生产环境使用 securecmdd 方式，避免 SSH 互信带来的安全风险。

### 部署后验证

```bash
# 1. 查看集群状态
repmgr cluster show

# 2. 查看服务状态
repmgr service status

# 3. 查看复制状态
SELECT * FROM sys_stat_replication;

# 4. 验证 VIP 加载
ip addr show | grep virtual_ip
```

---

## 3. GUI 安装部署

### 部署工具介绍

KingbaseES 提供数据库部署工具（GUI），支持项目管理、集群创建、节点管理和监控管理。工具提供 Windows 和 Linux 两个版本。

**启动方式**
```bash
# Linux 版本
./sys_deploy_tool

# Windows 版本
# 直接运行安装程序
```

### 部署流程

**第一步：创建项目**

1. 关闭欢迎窗口，点击"窗口"菜单
2. 右键"集群项目名称"，选择"创建项目"
3. 输入项目名称（英文、数字、下划线组合）

**第二步：创建集群**

右键项目节点，选择"创建集群"，分为两个配置阶段：

**节点通用配置**（创建后不可修改）
- 集群名称
- 节点类型（通用机/专用机）
- securecmd 端口（默认 8890）
- 常规用户（默认 kingbase，不存在则自动创建，密码 123456）
- 默认路径（自动拼接，不可修改）

**db & repmgr 配置**
- 数据库 zip 包选择
- max_connections（默认 100，最小 100）
- listenerPort（默认 54321）
- 加密算法（scram-sha-256 / md5）
- synchronous 模式
- archive_path（归档路径）
- archive_mode（WAL 归档开关，always 模式下恢复时也会归档）
- virtual_ip 及掩码
- failover（automatic / manual）
- recovery（automatic / standby / manual）
- 服务可用优先 / 数据保护优先（影响 reconnect_attempts, reconnect_interval, synchronous_commit 默认值）

**高级设置**
- wal_keep_segments（默认 512）
- max_wal_senders（最小 n+4，n 为节点数）
- hot_standby_feedback（默认 on）
- wal_compression（默认 on）
- encoding（默认 utf8）
- auto_cluster_recovery_level（全故障自动恢复，0=关闭，1=打开）
- use_check_disk（磁盘故障检测，默认 off）

> 警告：集群部署完成后，请不要修改 repmgrd_pid_file、kbha_pid_file 参数的值，修改后可能同时启动多个 kbha 或 repmgrd 进程。

**第三步：新增节点**

1. 展开集群，右键"新增节点"
2. SSH 配置：主机名/IP、端口、用户名、密码、securecmd 文件选择
3. 节点配置：显示名称、网卡名称、VIP 绑定网卡、license 文件
4. 环境检测：一键检查系统参数，一键修改，关闭防火墙
5. 预览信息：确认配置汇总
6. 执行部署

**第四步：新增 Witness 节点**（可选）

Witness 节点用于故障转移仲裁，证明主服务器确实不可用，而非仅因网络问题失联。配置流程同新增节点，选择"新增Witness节点"即可。

---

## 4. 日常运维操作

### 集群启停

**一键启停**（推荐）
```bash
# 启动集群
./sys_monitor.sh start kingbase

# 停止集群
./sys_monitor.sh stop kingbase

# 重启集群
./sys_monitor.sh restart kingbase
```

**手动启停**
```bash
# 启动数据库
systemctl start kingbase

# 停止数据库
systemctl stop kingbase

# 启动 repmgrd
repmgrd -f /opt/cluster/kingbase/etc/repmgr.conf

# 停止 repmgrd
repmgrd stop -f /opt/cluster/kingbase/etc/repmgr.conf
```

### 集群状态查看

```bash
# 1. 集群总览
repmgr cluster show

# 2. 服务状态
repmgr service status

# 3. 集群事件
repmgr event -f /path/to/repmgr.conf

# 4. 集群矩阵
repmgr cluster matrix

# 5. 节点交叉检查
repmgr cluster crosscheck
```

```sql
-- 6. 节点信息表
\c esrep
SELECT * FROM repmgr.show_nodes;

-- 7. 复制状态
SELECT client_addr, state, sent_lsn, write_lsn, flush_lsn, replay_lsn, sync_state
FROM sys_stat_replication;

-- 8. 复制槽状态
SELECT slot_name, active, sys_wal_lsn_diff(sys_current_wal_lsn(), restart_lsn) AS lag_bytes
FROM sys_replication_slots;

-- 9. 集群字符串信息
SELECT repmgr.get_cluster_info();
```

### 主备切换

```bash
# 手动主备切换
repmgr standby switchover --standby -h standby_host -U esrep

# 备库提升为主库
repmgr standby promote -h standby_host -U esrep

# 信号文件方式
touch $KINGBASE_HOME/data/promote
```

### 扩容与缩容

**扩容（增加备节点）**
```bash
# 1. 在新节点准备环境（用户、路径、系统参数）

# 2. 克隆备库
repmgr standby clone -h primary_host -U esrep -d esrep

# 3. 注册节点
repmgr standby register -h new_standby -U esrep

# 4. 启动新节点
systemctl start kingbase

# 5. 启动 repmgrd
repmgrd -f /path/to/repmgr.conf
```

**缩容（删除节点）**
```bash
# 1. 注销节点
repmgr node unregister -h target_host -U esrep

# 2. 停止服务
systemctl stop kingbase

# 3. 清理数据（可选）
rm -rf $KINGBASE_HOME/data/*
```

### 节点维护

```bash
# 暂停节点（维护前）
repmgr service pause -h target_host -U esrep

# 恢复节点（维护后）
repmgr service resume -h target_host -U esrep

# 节点重新加入集群
repmgr node rejoin -h rejoined_host -U esrep

# 节点健康检查
repmgr node check -h target_host -U esrep
```

### 密码修改

```bash
# 修改集群密码（通过 sys_monitor.sh）
./sys_monitor.sh password kingbase new_password

# 修改 repmgrd 端口
./sys_monitor.sh scmd_port 8891
```

### 同步模式切换

```bash
# 通过 sys_monitor.sh 切换
./sys_monitor.sh sync_config kingbase async

# 或直接修改
sys_monitor.sh set_sync_config kingbase sync
```

### 历史数据清理

```bash
# 清理监控历史
repmgr cluster cleanup -f /path/to/repmgr.conf

# 保留指定天数
repmgr cluster cleanup -f /path/to/repmgr.conf --days 7
```

---

## 5. 日志管理

### 日志文件位置

| 日志 | 路径 | 描述 |
|------|------|------|
| hamgr.log | `${install_dir}/kingbase/log/hamgr.log` | repmgrd 守护进程日志 |
| kbha.log | `${install_dir}/kingbase/log/kbha.log` | kbha 守护进程日志 |
| 数据库日志 | `${KINGBASE_DATA}/sys_log` | KingbaseES 数据库日志 |
| 系统日志 | `/var/log/message` | 操作系统日志 |

### 日志自动清理

hamgr.log 和 kbha.log 通过 crontab 定时调用 logrotate 清理。

**默认清理策略**（`logrotate_ha.conf`）
```
/opt/cluster/kingbase/log/kbha.log {
    weekly
    maxsize 100M
    su kingbase kingbase
    create 0600 kingbase kingbase
    rotate 3
    copytruncate
    dateext
}
```

- 每周轮换，最大 100M 触发
- 保留最近 3 次轮换
- 默认每天凌晨 0 时执行

### halog_analyse 日志分析工具

跨节点日志收集分析工具，解决多节点日志关联困难的问题。

**工具位置**
- `halog_analyse` / `halog_collect`：位于 bin 目录
- `halog_analyse.conf`：位于 share 目录

**配置文件关键参数**
```ini
# 必填参数
kb_bin_path = /home/kingbase/cluster/test/kingbase/bin
local_ip = 192.168.1.10
node_ips = 192.168.1.10,192.168.1.11
remote_user = kingbase

# 可选参数
begin_time = 2025-07-24 10:00:00
end_time = 2025-07-24 12:00:00
anal_file_save_path = /home/kingbase/anal_files
result_file = /home/kingbase/halog_analyse.result
use_ssh = true
loga_port = 65432
```

**使用示例**
```bash
# 收集并分析日志
./bin/halog_analyse -f share/halog_analyse.conf

# 仅分析已收集的日志
./bin/halog_analyse -f share/halog_analyse.conf -a
```

---

## 6. 备份与恢复

### sys_rman 备份工具

KingbaseES 提供 sys_rman 备份恢复管理工具，支持集群环境下的物理备份。

**备份类型**

| 类型 | 说明 |
|------|------|
| 全量备份 | 备份全部数据文件 |
| 增量备份 | 仅备份自上次全量备份以来的变化 |
| 差异备份 | 仅备份自上次备份以来的变化 |
| 页级备份 | 针对特定数据页的备份 |

**配置示例**（`sys_backup.conf`）
```ini
# 备份基础配置
user = SYSTEM
password = 12345678ab
cluster_name = mycluster
backup_type = full

# 备份路径
backup_path = /opt/backup/kingbase
```

**常用操作**
```bash
# 初始化
sys_rman init -c sys_backup.conf

# 手动执行备份
sys_rman backup -c sys_backup.conf -b full

# 查看备份集
sys_rman list -c sys_backup.conf

# 删除备份集
sys_rman delete -c sys_backup.conf -l backup_label
```

### 恢复方法

| 恢复方式 | 命令 | 说明 |
|---------|------|------|
| 恢复到最新 | `sys_rman restore` | 恢复到最近的备份点 |
| 指定备份集 | `sys_rman restore -l label` | 恢复到指定备份集 |
| 按 XID 恢复 | `sys_rman restore -x xid` | 恢复到指定事务 ID |
| 时间点恢复 | `sys_rman restore -t timestamp` | PITR，精确到秒 |

### 集群重建

```bash
# 1. 停止集群
./sys_monitor.sh stop kingbase

# 2. 从备份恢复主库
sys_rman restore -c sys_backup.conf

# 3. 启动主库
systemctl start kingbase

# 4. 从新主库重新克隆备库
repmgr standby clone -h new_primary -U esrep

# 5. 注册并启动备库
repmgr standby register -h standby -U esrep
systemctl start kingbase
```

---

## 7. 应急预案

### 双主故障

主备节点同时异常，可能出现两个节点都认为自己是主库的情况。

**排查步骤**
```bash
# 1. 检查两个节点的数据库状态
sys_controldata $KINGBASE_HOME/data

# 2. 比较 TimeLineID 和 oldestActiveXID
# TimeLineID 更大的节点通常是正确的主库
# 若 TimeLineID 相同，选择 oldestActiveXID 更大的节点

# 3. 保留正确的主库，将错误的主库重新作为备库加入
repmgr node rejoin -h failed_host -U esrep
```

### 磁盘空间不足

**紧急处理**
```bash
# 1. 清理数据库日志
# 进入 ${KINGBASE_DATA}/sys_log，删除旧的日志文件

# 2. 清理 WAL 归档
sys_archivecleanup ${KINGBASE_DATA}/sys_wal <oldest_needed_wal_file>

# 3. 临时扩容（LVM）
lvextend -L +50G /dev/mapper/vg-data
resize2fs /dev/mapper/vg-data
```

### 数据紧急恢复

```bash
# 1. 逻辑恢复
sys_restore -h localhost -p 54321 -U SYSTEM -d dbname /path/to/backup.dump

# 2. 物理恢复
sys_rman restore -c sys_backup.conf

# 3. WAL 挖掘（误操作恢复）
walminer -h localhost -p 54321 -U SYSTEM

# 4. 数据页修复
sys_walrepairdata -h localhost -p 54321 -U SYSTEM -d dbname -t tablename
```

### 集群连接异常排查

```bash
# 1. 网络连通性
ping target_host
ifconfig

# 2. 服务状态
repmgr service status

# 3. 连接参数验证
ksql -h target_host -p 54321 -U esrep -d esrep

# 4. 检查 sys_hba.conf
# 确认目标 IP 在允许列表中

# 5. 资源检查
df -h
free -m
top
```

---

## 8. 灾难恢复演练

### 计划内切换演练

```bash
# 1. 通知业务停止写入
# 2. 执行主备切换
repmgr standby switchover --standby -h standby_host -U esrep

# 3. 验证新主库连接
ksql -h new_primary -p 54321 -U SYSTEM -d test \
    -c "SELECT sys_is_in_recovery();"
# 应返回 false

# 4. 业务验证
# 确认应用可以正常读写

# 5. 切换回原主库
# 原主库以 standby 身份重新加入
repmgr node rejoin -h original_primary -U esrep
```

### 计划外切换演练

```bash
# 1. 模拟主库故障
# 停止主库服务（演练环境）
systemctl stop kingbase

# 2. 等待自动故障切换
# repmgrd 将自动选举备库提升

# 3. 验证
sys_controldata $KINGBASE_HOME/data
# 确认 TimeLineID

# 4. 如果自动切换未生效，手动提升
SELECT sys_promote();

# 5. 应用连接测试
ksql -h vip -p 54321 -U SYSTEM -d test -c "SELECT 1;"

# 6. 原主库恢复后重新加入
repmgr node rejoin -h recovered_host -U esrep
```

> 建议每 3-6 个月进行一次灾难恢复演练。

---

## 9. 附录

### 常用命令速查

**repmgr 命令**
```bash
# 节点注册
repmgr primary register -h host -U esrep
repmgr standby register -h host -U esrep
repmgr witness register -h host -U esrep

# 节点注销
repmgr node unregister -h host -U esrep

# 备库操作
repmgr standby clone -h primary -U esrep
repmgr standby promote -h standby -U esrep
repmgr standby follow -h standby -U esrep
repmgr standby switchover --standby -h standby -U esrep

# 节点操作
repmgr node rejoin -h host -U esrep
repmgr node check -h host -U esrep
repmgr node status -h host -U esrep

# 集群操作
repmgr cluster show
repmgr cluster matrix
repmgr cluster crosscheck
repmgr cluster cleanup
repmgr service status
repmgr service pause
repmgr service resume
```

**sys_monitor.sh 命令**
```bash
# 集群启停
sys_monitor.sh start kingbase
sys_monitor.sh stop kingbase
sys_monitor.sh restart kingbase

# HA 操作
sys_monitor.sh ha_start
sys_monitor.sh ha_stop
sys_monitor.sh ha_restart

# 同步配置
sys_monitor.sh sync_config kingbase async|sync|quorum|all|custom

# 密码修改
sys_monitor.sh password kingbase new_password

# 端口修改
sys_monitor.sh scmd_port 8891
sys_monitor.sh ssh_port 22
```

### repmgr.conf 核心参数

| 参数 | 说明 |
|------|------|
| `node_id` | 节点 ID，集群内唯一 |
| `node_name` | 节点名称 |
| `conninfo` | 数据库连接串 |
| `repluser` | 复制用户名 |
| `priority` | 升主权重（0-100） |
| `failover` | 故障切换模式：automatic / manual |
| `recovery` | 故障恢复模式：automatic / standby / manual |
| `synchronous` | 同步模式 |
| `virtual_ip` | 虚拟 IP |
| `trusted_servers` | 信任网关列表 |
| `monitor_interval` | 监控间隔 |
| `use_scmd` | 是否使用 securecmdd 通信 |
| `ha_running_mode` | HA 运行模式 |
| `running_under_failure_trusted_servers` | 网关故障时数据库是否继续运行 |

### es_rep.conf 核心参数

| 参数 | 说明 |
|------|------|
| `wal_level` | WAL 级别，需设置为 replica |
| `synchronous_commit` | 同步提交级别 |
| `max_connections` | 最大连接数 |
| `max_wal_senders` | 最大 WAL sender 数 |
| `wal_keep_segments` | 保留的 WAL 文件数 |
| `hot_standby_feedback` | 备库反馈机制 |
| `archive_mode` | WAL 归档模式 |

### 集群事件类型速查

| 事件 | 说明 |
|------|------|
| `standby_promote` | 备库提升为主库 |
| `standby_switchover` | 主备切换 |
| `node_rejoin` | 节点重新加入 |
| `repmgrd_failover_promote` | 自动故障转移提升 |
| `repmgrd_failover_aborted` | 故障转移中止 |
| `child_node_disconnect` | 子节点断开连接 |
| `child_node_reconnect` | 子节点恢复连接 |
| `repmgrd_upstream_disconnect` | 上游节点断开 |
| `node_recovery_success` | 节点自动恢复成功 |
| `node_recovery_failed` | 节点自动恢复失败 |

### 节点状态说明

| 状态 | 含义 |
|------|------|
| `* running` | 运行正常 |
| `running` | 运行正常 |
| `failed` | 节点故障，停止运行 |
| `? unreachable` | 节点异常，无法获取状态 |
| `running as primary` | 异常 - 注册为备库但以主库运行 |
| `running as standby` | 异常 - 注册为主库以备库运行 |

---

## 最佳实践

1. **时钟同步**：集群节点间必须配置 NTP/chrony，时间差不能超过监控间隔
2. **trusted_servers 必配**：防止脑裂，配置独立的信任网关
3. **独立心跳网络**：心跳与业务流量隔离
4. **定期演练**：每 3-6 个月进行一次灾难恢复演练
5. **日志监控**：配置 halog_analyse 定期收集分析集群日志
6. **备份验证**：周期性对备份做数据校验和恢复验证
7. **VIP 管理**：应用统一通过 VIP 连接，禁止直连节点 IP
8. **使用 securecmdd**：生产环境优先使用 sys_securecmdd 而非 SSH
9. **参数不随意修改**：部署完成后不要修改 repmgrd_pid_file、kbha_pid_file
10. **监控复制延迟**：延迟 > 30 秒立即告警
