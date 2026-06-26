# 系统资源

## CPU

```bash
top                         # 动态监控
htop                        # 更友好
mpstat                      # CPU 统计
lscpu                       # CPU 信息
nproc                       # CPU 核心数
uptime                      # 负载
cat /proc/loadavg           # 负载详情
```

## 内存

```bash
free -h                     # 内存使用
free -m                     # MB 单位
cat /proc/meminfo           # 详细信息
ps aux --sort=-%mem | head  # 进程内存排序
top -o %MEM                 # 动态排序
```

## 磁盘

```bash
df -h                       # 磁盘使用
df -i                       # inode 使用
du -sh /var/log             # 目录大小
du -h --max-depth=1 /var    # 子目录大小
lsblk                       # 块设备
fdisk -l                    # 分区信息
```

## 查找大文件

```bash
find / -type f -size +100M 2>/dev/null
du -ah / | sort -rh | head -20
```

## I/O

```bash
iostat                      # I/O 统计
iostat -x 1                 # 详细，每秒刷新
iotop                       # I/O 监控
pidstat -d 1                # 进程 I/O
```
