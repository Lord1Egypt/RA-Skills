# QNX命令参考

## 概述

J6B板端运行QNX实时操作系统，常用命令与Linux有差异。本节整理QNX特有及常用命令。

---

## 进程管理

### pidin - 查看进程详情（QNX特有）

```bash
# 查看所有进程
pidin

# 查看特定进程
pidin -p <PID>

# 查看进程树
pidin -T

# 查看进程内存信息
pidin -m

# 查看进程线程
pidin -t

# 查看进程文件描述符
pidin -f
```

### slay - 结束进程（QNX特有）

```bash
# 结束进程
slay <PID>

# 结束进程及其子进程
slay -f <PID>

# 按名称结束进程
slay planning
```

### 其他进程命令

```bash
# 查看进程状态（类似ps）
ps

# 查看特定用户的进程
ps -u root
```

---

## 日志查看

### slog2info - 系统日志查看（QNX特有）

```bash
# 查看所有系统日志
slog2info

# 查看最近的日志
slog2info | tail -100

# 搜索关键词
slog2info | grep -i planning

# 搜索错误
slog2info | grep -i "error\|fail"

# 实时跟踪
slog2info -w
```

---

## 资源监控

### hogs - 进程资源监控

```bash
# 基本用法
hogs

# 按CPU占用排序
hogs -i

# 1秒刷新
hogs -s 1

# 只显示进程名
hogs -n

# 组合使用
hogs -i -s 1
```

### top - 系统监控

```bash
# 基本用法
top

# 查看特定进程
top -p <PID>

# 查看多个进程
top -p 12345,67890

# 交互：按o+列名排序（如：o cpu）
```

---

## 网络相关

### 查看网络配置

```bash
# 查看网络接口
ifconfig

# 查看网络连接
netstat -an

# 查看路由表
route show
```

### 网络测试

```bash
# Ping测试
ping 192.168.1.10

# SSH连接
ssh root@192.168.1.10

# SCP传输
scp root@192.168.1.10:/path/to/file ./
```

---

## 文件操作

### 基本文件命令

```bash
# 列出文件
ls
ls -la

# 进入目录
cd /app/apa

# 查看文件内容
cat file.txt

# 查看文件前几行
head -20 file.txt

# 查看文件后几行
tail -20 file.txt

# 实时跟踪文件
tail -f file.txt

# 搜索文件内容
grep "pattern" file.txt
```

### 文件搜索

```bash
# 按名称搜索
find /path -name "*.log"

# 按类型搜索
find /path -type f

# 搜索最近修改的文件
find /path -mtime -1

# 按大小搜索
find /path -size +10M
```

### 压缩与解压

```bash
# 打包压缩
tar czf archive.tar.gz directory/

# 解压
tar xzf archive.tar.gz

# 查看压缩包内容
tar tzf archive.tar.gz
```

---

## 系统信息

### 查看系统信息

```bash
# 查看系统版本
uname -a

# 查看CPU信息
pidin info

# 查看内存信息
showmem

# 查看磁盘使用
df -h

# 查看目录大小
du -sh /app/apa
```

---

## 设备相关

### 查看设备信息

```bash
# 查看设备列表
ls /dev

# 查看串口
ls /dev/ser*

# 查看块设备
ls /dev/hd*

# 查看CAN设备
ls /dev/can*
```

---

## QNX vs Linux 命令对照表

| 功能 | QNX | Linux | 说明 |
|------|-----|-------|------|
| 进程详情 | `pidin` | `ps` | QNX pidin 信息更丰富 |
| 结束进程 | `slay` | `kill` | 用法相同 |
| 系统日志 | `slog2info` | `journalctl` | 格式不同 |
| 内存信息 | `showmem` | `free` | 输出格式不同 |
| 资源监控 | `hogs` | `htop` | QNX hogs 是进程级 |

---

## 常用组合命令

### 查看planning进程状态

```bash
# 方法1：使用pidin
pidin | grep planning

# 方法2：使用top
top | grep planning

# 方法3：使用hogs
hogs | grep planning
```

### 查看最近错误日志

```bash
# 从系统日志
slog2info | grep -i "error\|fail" | tail -20

# 从应用日志
find /app/apa/log/ -name "*.log" -exec grep -l "error" {} \;
```

### 监控实时日志

```bash
# 单个文件
tail -f /app/apa/log/planning/*.log

# 多个文件
tail -f /app/apa/log/planning/*.log /app/apa/log/od/*.log
```

### 查看网络连接状态

```bash
# 查看所有连接
netstat -an

# 查看SSH连接
netstat -an | grep 22

# 测试网络
ping 192.168.1.10
```

---

## 权限管理

### 切换用户

```bash
# 切换到root
su -

# 以root执行命令
sudo command
```

### 修改文件权限

```bash
# 修改权限
chmod 755 file.sh

# 修改所有者
chown root:root file.sh

# 递归修改
chmod -R 755 /app/apa/log
```

---

## 系统服务

### SSH服务

```bash
# 查看SSH进程
pidin | grep sshd

# 重启SSH（需要root权限）
# 使用slay结束后手动启动
```

### 系统时间

```bash
# 查看时间
date

# 设置时间（需要root）
date -s "2026-03-28 16:00:00"
```

---

## 故障排查常用命令

### 进程异常

```bash
# 查看进程状态
pidin
top
hogs -i

# 结束问题进程
slay <PID>
```

### 系统卡顿

```bash
# 查看资源占用
hogs -i -s 1
top

# 查看内存
showmem
cat /log/lowmem.dmesg.txt
```

### 进程崩溃

```bash
# 查看coredump
ls /log/coredump/

# 查看系统日志
slog2info | grep -i "crash\|segmentation"

# 查看重启原因
cat /log/reset_reason.txt
```

### 日志问题

```bash
# 查看日志目录
ls -la /app/apa/log/

# 查看最近修改的日志
find /app/apa/log/ -name "*.log" -mmin -10

# 搜索错误
grep -i "error" /app/apa/log/*/*.log
```
