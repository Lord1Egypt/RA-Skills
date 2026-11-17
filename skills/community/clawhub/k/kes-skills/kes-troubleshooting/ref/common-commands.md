# 常用命令速查

## 数据库启停

### 单机环境

```bash
# 启动
sys_ctl start -D /home/kingbase/KingbaseES/V9/data

# 关闭
sys_ctl -D /home/kingbase/KingbaseES/V9/data stop

# 重启
sys_ctl -D /home/kingbase/KingbaseES/V9/data restart

# 查看控制文件
sys_controldata -D /home/kingbase/KingbaseES/V9/data
```

**查找 data 路径**：

```bash
# 通过进程（已启动）
ps -ef | grep kingbase

# 通过参数（已启动）
ksql -U SYSTEM -d TEST -c "show data_directory;"

# 通过文件搜索（未启动）
find / -name kingbase.conf
```

### 集群环境

```bash
# 启动集群
./sys_monitor.sh start

# 停止集群
./sys_monitor.sh stop

# 停止本节点（包括集群管理和数据库服务）
./sys_monitor.sh stoplocal

# 重启集群
./sys_monitor.sh restart

# 配置单个节点同步类型
./sys_monitor.sh node1 sync

# 配置多个节点同步类型（覆盖已有配置）
./sys_monitor.sh sync_nodes "node1,node2,node3"

# 切换 synchronous 模式
./sys_monitor.sh switch_synchronous custom
```

### 常见故障处理

**arping 权限问题**：

```bash
chown -R root.root arping
chmod u+s arping
```

**备节点 inactive**：

```bash
repmgr standby register --force
```

**data-directory-config 检查失败**：启动数据库时 -D 后使用绝对路径。

## 常用 SQL 命令

### 版本与连接

```sql
-- 数据库版本
SELECT version();

-- 最大连接数
SHOW max_connections;

-- 所有连接状态
SELECT * FROM sys_stat_activity;

-- 关闭连接
SELECT sys_terminate_backend(pid);

-- License 到期时间
SELECT get_license_validdays();
```

### 慢 SQL 查看

```sql
-- 方法一：配置文件设置（重启生效）
-- Log_min_duration_statement = 1000
-- Log_statement = 'mod'

-- 方法二：会话级别（超级用户）
SET Log_min_duration_statement = 1000;
SET Log_statement = 'mod';
```

### 统计对象数量

```sql
-- 表（r=普通表, t=TOAST, f=外部表, p=分区表）
SELECT count(*) FROM sys_class WHERE relkind IN ('r','t','f','p');

-- 视图
SELECT count(*) FROM sys_class WHERE relkind = 'v';

-- 序列
SELECT count(*) FROM sys_class WHERE relkind = 'S';

-- 函数
SELECT count(*) FROM sys_proc WHERE prokind IN ('f','a','w');

-- 存储过程
SELECT count(*) FROM sys_proc WHERE prokind = 'p';

-- 类型
SELECT count(*) FROM sys_type;

-- 无效对象
SELECT count(*) FROM sys_class WHERE reloptions = '{status=false}';
```

### 获取对象 DDL

```sql
-- 需先创建 dbms_metadata 插件
SELECT dbms_metadata.get_ddl('TABLE','t1');
```

### 查询表及行数

```sql
SELECT relname, reltuples
FROM sys_class cls LEFT JOIN sys_namespace n ON (n.oid = cls.relnamespace)
WHERE nspname NOT IN ('sys_catalog', 'information_schema')
  AND cls.relkind = 'r'
ORDER BY reltuples DESC;
```

### 查询包含 LOB 字段的表

```sql
SELECT relname
FROM sys_class, sys_attribute, sys_type
WHERE sys_class.oid = sys_attribute.attrelid
  AND sys_attribute.atttypid = sys_type.oid
  AND sys_type.typname LIKE '%lob';
```

## 操作系统常用命令

### 硬件配置

```bash
# CPU 信息
cat /proc/cpuinfo
lscpu | grep -E "Architecture|^CPU\(s\)|^CPU MHz|Model name"

# 内存
cat /proc/meminfo
free -m

# 磁盘空间
df -m        # 文件系统使用率
df -i        # inode 使用率
fdisk -l | grep -i disk

# 多路径
multipath -ll

# 网卡
ifconfig -a
ethtool <网卡名>

# swap
swapon -s

# PCI 设备
lspci
```

### 系统配置

```bash
# 操作系统版本
cat /etc/system-release

# 内核版本
uname -a

# 系统参数
sysctl -a

# 资源限制
ulimit -Ha

# 用户进程限制
cat /etc/security/limits.d/*conf

# Selinux
cat /etc/selinux/config | grep ^SELINUX

# 防火墙
systemctl status firewalld.service

# IO 调度算法
ls /sys/block/|while read diskname; do fdisk -l /dev/$diskname >& /dev/null; test $? -eq 0 && (echo -n "磁盘 $diskname : "; cat /sys/block/$diskname/queue/scheduler); done
```

### 系统运行状态

```bash
# 内存
sar -r 2 2

# CPU 利用率
sar -u 2 2

# IO
iostat 2 2

# TOP IO 进程
iotop -b -k -P -n 4

# TOP CPU 进程
top -o %CPU -i -b -n 4

# 网络流量
sar -n DEV 2 2

# 文件系统使用率
df -m

# 进程内存排名
ps auxc --sort=-%mem | more

# 内存段/信号量
ipcs --human -a

# 操作系统日志
systemctl | more

# crontab
cat /etc/cron.d/*
cat /var/spool/cron/*

# core 文件
ls -l /var/spool/abrt
```

### Core 文件配置

以 CentOS 7 为例：

1. 确认 core 文件大小：`ulimit -c`
2. 修改 `/etc/abrt/abrt-action-save-package-data.conf`：

```ini
OpenGPGCheck = no
ProcessUnpackaged = yes
```

3. 重启 abrtd 服务，确认 `/var/spool/abrt` 下有 ccpp\* 文件

### Core 文件分析

```bash
gdb {kingbase二进制路径} {core文件路径}
# 进入 gdb 后：
# bt        — 显示堆栈
# bt full   — 显示参数值的堆栈
```

## 数据库常用工具

### ksql

```bash
# 登录
ksql -U 用户名 -W 数据库名

# 元命令
\q          # 退出
\l          # 查看数据库列表
\dt         # 查看默认模式下表
\d 表名     # 查看表结构
\?          # 帮助
```

### 集群管理

```bash
# 集群状态
repmgr cluster show

# 服务状态
repmgr service status

# 暂停/恢复
repmgr service pause
repmgr service unpause

# 集群事件
repmgr cluster event
```

### 备份恢复

```bash
# sys_rman 查看备份信息
sys_rman --config=/path/sys_rman.conf --stanza=kingbase info

# sys_rman 检查备份完整性
sys_rman --config=/path/sys_rman.conf --stanza=kingbase check

# 归档检查
grep -rn "archive-push" data/sys_log
```
