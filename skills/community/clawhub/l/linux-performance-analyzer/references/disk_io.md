# 磁盘 I/O 调优参考手册

## 目录
1. [快速诊断](#1-快速诊断)
2. [I/O 调度器选择](#2-io-调度器选择)
3. [读预读优化](#3-读预读优化)
4. [脏页回写（与内存联动）](#4-脏页回写)
5. [文件系统挂载优化](#5-文件系统挂载优化)
6. [磁盘队列深度](#6-磁盘队列深度)
7. [fio 性能测试](#7-fio-性能测试)
8. [NVMe/SSD 专项优化](#8-nvmessd-专项优化)
9. [RAID 与 LVM 优化](#9-raid-与-lvm-优化)
10. [磁盘健康监控](#10-磁盘健康监控)

---

## 1. 快速诊断

```bash
# I/O 实时统计（关键指标：%util, await, r/s, w/s）
iostat -xz 1 5

# 找 I/O 密集进程
iotop -o -b -n 3 | head -20
pidstat -d 1 5

# 查看磁盘等待进程
ps aux | awk '$8 ~ /D/ {print $0}'

# 磁盘空间
df -h
du -sh /* 2>/dev/null | sort -rh | head -20

# 当前 I/O 调度器
for d in /sys/block/*/queue/scheduler; do
    echo "$(basename $(dirname $(dirname $d))): $(cat $d)"
done

# 检查文件系统挂载选项
mount | grep -v 'tmpfs\|proc\|sys\|dev\|cgroup'
```

**iostat 关键指标解读：**
| 指标 | 正常范围 | 告警阈值 |
|------|---------|---------|
| %util | < 60% | > 80% 接近饱和 |
| await (ms) | HDD<20ms, SSD<5ms | > 50ms 严重 |
| r_await | HDD<20ms, SSD<2ms | 参考 await |
| w_await | HDD<20ms, SSD<2ms | 参考 await |
| svctm (ms) | < await | 若≈await说明无队列 |
| avgqu-sz | < 队列深度 | > 32 可能拥堵 |

---

## 2. I/O 调度器选择

```bash
# 查看可用调度器
cat /sys/block/sda/queue/scheduler
# [mq-deadline] none kyber bfq

# 设置调度器
echo mq-deadline > /sys/block/sda/queue/scheduler

# 调度器选择指南：
# ┌─────────────┬──────────────────────────────────────┐
# │ 调度器      │ 适用场景                              │
# ├─────────────┼──────────────────────────────────────┤
# │ none        │ NVMe SSD、虚拟机磁盘（依赖宿主调度）  │
# │ mq-deadline │ 通用 SSD、混合读写、数据库             │
# │ bfq         │ HDD、桌面系统、多进程公平 I/O          │
# │ kyber       │ 低延迟 SSD/NVMe                       │
# └─────────────┴──────────────────────────────────────┘

# 持久化（udev 规则，推荐）
cat > /etc/udev/rules.d/60-ioscheduler.rules << 'EOF'
# NVMe SSD
ACTION=="add|change", KERNEL=="nvme[0-9]*", ATTR{queue/scheduler}="none"
# SATA SSD
ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/rotational}=="0", ATTR{queue/scheduler}="mq-deadline"
# HDD
ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/rotational}=="1", ATTR{queue/scheduler}="bfq"
EOF
udevadm control --reload-rules && udevadm trigger

# 验证
cat /sys/block/sda/queue/scheduler   # 确认调度器已切换

# 回滚
echo none > /sys/block/sda/queue/scheduler
```

---

## 3. 读预读优化

```bash
# 查看当前预读设置（KB）
blockdev --getra /dev/sda
cat /sys/block/sda/queue/read_ahead_kb

# 调整建议：
# 随机读（数据库）：128~512KB（较小，减少无效预读）
# 顺序读（日志/流媒体）：2048~8192KB（较大，减少 I/O 次数）
blockdev --setra 4096 /dev/sda   # 2MB (单位512字节，4096×512=2MB)
echo 2048 > /sys/block/sda/queue/read_ahead_kb  # 直接设置KB

# 持久化
cat > /etc/rc.local << 'EOF'
#!/bin/bash
blockdev --setra 4096 /dev/sda
EOF
chmod +x /etc/rc.local

# 验证效果（顺序读性能对比）
dd if=/dev/sda of=/dev/null bs=1M count=1024 2>&1 | tail -1
# 调整前后对比 MB/s
```

---

## 4. 脏页回写

> 与内存章节 references/memory.md 第6节联动

```bash
# 写密集型服务（防止脏页积累导致 I/O 尖峰）
sysctl -w vm.dirty_ratio=10
sysctl -w vm.dirty_background_ratio=5
sysctl -w vm.dirty_expire_centisecs=1500   # 15秒强制刷盘
sysctl -w vm.dirty_writeback_centisecs=300  # 3秒唤醒回写线程

# 高吞吐批量写（允许积累更多，减少 I/O 频率）
sysctl -w vm.dirty_bytes=536870912         # 512MB 触发阻塞
sysctl -w vm.dirty_background_bytes=134217728  # 128MB 触发后台回写

# 监控脏页实时情况
watch -n 1 'grep -E "Dirty|Writeback" /proc/meminfo'
```

---

## 5. 文件系统挂载优化

```bash
# 查看当前挂载选项
mount | grep "^/dev"

# ext4 优化挂载选项
# /etc/fstab 示例：
# /dev/sdb1 /data ext4 noatime,nodiratime,data=writeback,barrier=0 0 2
# noatime：禁用访问时间记录（减少写操作）
# nodiratime：禁用目录访问时间
# data=writeback：写回模式（性能最好，但断电可能数据不一致）
# barrier=0：关闭写屏障（有 UPS 时可开启，有数据丢失风险）

# XFS 优化挂载选项
# /dev/vdb1 /data xfs noatime,nodiratime,logbufs=8,logbsize=256k 0 2

# Btrfs 优化挂载选项
# /dev/vdc1 /data btrfs noatime,compress=zstd:1,space_cache=v2 0 2
# compress=zstd:1：压缩比和性能平衡

# 临时重新挂载（不重启）
mount -o remount,noatime /data

# 检查文件系统碎片
e2fsck -n /dev/sda1 2>/dev/null | grep "non-contiguous"   # ext4
xfs_db -c frag -r /dev/sdb1 2>/dev/null                   # XFS
```

---

## 6. 磁盘队列深度

```bash
# 查看队列深度
cat /sys/block/sda/queue/nr_requests
cat /sys/block/sda/queue/queue_depth   # NVMe

# 调整队列深度
# HDD：64~128（过大会增加延迟）
# SSD：128~256
# NVMe：256~1024
echo 256 > /sys/block/sda/queue/nr_requests

# 持久化（udev 规则）
cat >> /etc/udev/rules.d/60-ioscheduler.rules << 'EOF'
ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/rotational}=="0", ATTR{queue/nr_requests}="256"
ACTION=="add|change", KERNEL=="nvme[0-9]*", ATTR{queue/nr_requests}="1024"
EOF

# 检查是否有 I/O 合并（相邻请求合并）
cat /sys/block/sda/queue/nomerges   # 0=开启合并（默认）
```

---

## 7. fio 性能测试

```bash
# 安装 fio
apt install fio 2>/dev/null || yum install fio 2>/dev/null

# 顺序读测试（大文件，测试吞吐量）
fio --name=seq-read --ioengine=libaio --iodepth=32 \
    --rw=read --bs=1M --size=4G --numjobs=1 \
    --filename=/data/fio_test --direct=1 \
    --runtime=30 --time_based --group_reporting

# 随机读测试（小块，测试 IOPS）
fio --name=rand-read --ioengine=libaio --iodepth=64 \
    --rw=randread --bs=4k --size=4G --numjobs=4 \
    --filename=/data/fio_test --direct=1 \
    --runtime=30 --time_based --group_reporting

# 混合读写（7:3，模拟业务负载）
fio --name=mixed-rw --ioengine=libaio --iodepth=32 \
    --rw=randrw --rwmixread=70 --bs=4k --size=4G --numjobs=4 \
    --filename=/data/fio_test --direct=1 \
    --runtime=30 --time_based --group_reporting

# 清理测试文件
rm /data/fio_test

# 性能参考（常见磁盘类型）：
# ┌─────────────┬──────────────┬──────────────┬────────────┐
# │ 磁盘类型    │ 顺序读       │ 顺序写       │ 随机4K读   │
# ├─────────────┼──────────────┼──────────────┼────────────┤
# │ HDD 7200rpm │ 100-200 MB/s │ 80-150 MB/s  │ 0.5K IOPS  │
# │ SATA SSD    │ 500-560 MB/s │ 450-520 MB/s │ 90K IOPS   │
# │ NVMe SSD    │ 3-7 GB/s     │ 2-5 GB/s     │ 500K IOPS  │
# └─────────────┴──────────────┴──────────────┴────────────┘
```

---

## 8. NVMe/SSD 专项优化

```bash
# 查看 NVMe 设备信息
nvme list 2>/dev/null
nvme smart-log /dev/nvme0 2>/dev/null | grep -E "temperature|wear|available_spare"

# NVMe 队列深度优化
echo 1024 > /sys/block/nvme0n1/queue/nr_requests

# NVMe 调度器（使用 none，完全依赖 NVMe 内部调度）
echo none > /sys/block/nvme0n1/queue/scheduler

# SSD TRIM 支持（定期释放无效块）
fstrim -v /data 2>/dev/null   # 手动 TRIM
# 开启定时 TRIM（systemd timer）
systemctl enable fstrim.timer
systemctl start fstrim.timer
# 验证
systemctl status fstrim.timer

# SSD 磨损均衡检查
smartctl -A /dev/sda | grep -E "Wear_Leveling|SSD_Life|Percent_Lifetime"

# 写放大因子 (WAF) 监控
nvme smart-log /dev/nvme0 | grep "data_units"
```

---

## 9. RAID 与 LVM 优化

```bash
# 查看 RAID 状态
cat /proc/mdstat
mdadm --detail /dev/md0

# RAID 条带大小优化
# 建议与文件系统 block size 和应用 I/O size 对齐
# 数据库随机 I/O：32KB~64KB
# 顺序大文件：128KB~256KB

# LVM 条带化（提升性能）
lvcreate -L 100G -n data_lv -i 4 -I 64 vg0   # 4 盘条带，64KB 条带大小

# 查看 LVM 配置
lvdisplay -m /dev/vg0/data_lv

# RAID 重建优先级（降低重建对业务的影响）
echo 100000 > /proc/sys/dev/raid/speed_limit_max   # 限制重建速度 100MB/s
```

---

## 10. 磁盘健康监控

```bash
# 安装 smartmontools
apt install smartmontools 2>/dev/null || yum install smartmontools 2>/dev/null

# 查看 SMART 状态
smartctl -H /dev/sda   # 健康状态（PASSED/FAILED）
smartctl -A /dev/sda   # 详细属性

# 关键 SMART 指标：
# Reallocated_Sector_Ct：重分配扇区数（> 0 需关注）
# Current_Pending_Sector：待定扇区数（> 0 需关注）
# Uncorrectable_Sector_Cnt：不可纠正扇区（> 0 磁盘即将损坏）
# SSD_Life_Left / Percent_Lifetime_Remain：SSD 剩余寿命

# 批量检查所有磁盘
for disk in /dev/sd? /dev/nvme?; do
    [ -b "$disk" ] && echo "=== $disk ===" && smartctl -H $disk 2>/dev/null | grep -E "result|PASSED|FAILED|overall"
done

# 开启 SMART 后台监控（smartd）
systemctl enable --now smartd
# 配置 /etc/smartd.conf 发现问题时发邮件

# 添加定期检查到 crontab
echo "0 3 * * 0 smartctl -a /dev/sda > /var/log/smart-sda-$(date +\%Y\%W).log" >> /etc/crontab
```