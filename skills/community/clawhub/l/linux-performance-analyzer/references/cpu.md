# CPU 调优参考手册

## 目录
1. [快速诊断](#1-快速诊断)
2. [上下文切换优化](#2-上下文切换优化)
3. [CPU 调速与频率管理](#3-cpu-调速与频率管理)
4. [进程调度优化](#4-进程调度优化)
5. [CPU 亲和性与绑核](#5-cpu-亲和性与绑核)
6. [NUMA 优化](#6-numa-优化)
7. [中断绑核](#7-中断绑核)
8. [perf 性能剖析](#8-perf-性能剖析)
9. [容器 CPU 限制排查](#9-容器-cpu-限制排查)

---

## 1. 快速诊断

```bash
# 负载概览
uptime
cat /proc/loadavg

# 每核 CPU 使用率（1秒采样5次）
mpstat -P ALL 1 5

# 高 CPU 进程
top -bn1 | sort -k9 -rn | head -15
pidstat -u 1 5

# 上下文切换详情
vmstat 1 5          # 看 cs（上下文切换）和 r（运行队列）
pidstat -w 1 3      # 进程级上下文切换

# CPU 等待 I/O 分析
iostat -xz 1 3      # 看 %util 和 %iowait

# 调度延迟
perf sched latency 2>/dev/null | head -20
```

**关键指标解读：**
| 指标 | 正常范围 | 异常判断 |
|------|---------|---------|
| load1 / 核数 | < 0.7 | > 2.0 需关注 |
| vmstat r (运行队列) | ≤ 核数 | 持续 > 核数×2 严重 |
| vmstat cs (上下文切换/秒) | < 5万 | > 50万 需优化 |
| %iowait | < 5% | > 20% 为 I/O 瓶颈 |
| CPU %us + %sy | < 70% | > 90% 接近饱和 |

---

## 2. 上下文切换优化

```bash
# 查看当前调度器参数
sysctl kernel.sched_min_granularity_ns
sysctl kernel.sched_wakeup_granularity_ns
sysctl kernel.sched_migration_cost_ns

# 增大调度粒度，减少抢占频率（减少上下文切换）
sysctl -w kernel.sched_min_granularity_ns=10000000    # 10ms（默认3ms）
sysctl -w kernel.sched_wakeup_granularity_ns=15000000  # 15ms（默认4ms）
sysctl -w kernel.sched_migration_cost_ns=5000000       # 5ms（默认0.5ms）

# 持久化
cat >> /etc/sysctl.d/99-perf-master.conf << 'EOF'
kernel.sched_min_granularity_ns = 10000000
kernel.sched_wakeup_granularity_ns = 15000000
kernel.sched_migration_cost_ns = 5000000
EOF

# ⚠️ 副作用：增大粒度可能轻微增加交互响应延迟，桌面系统不建议调整
# 回滚：
sysctl -w kernel.sched_min_granularity_ns=3000000
sysctl -w kernel.sched_wakeup_granularity_ns=4000000
sysctl -w kernel.sched_migration_cost_ns=500000
```

---

## 3. CPU 调速与频率管理

```bash
# 查看当前调速策略
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor | sort -u
cpupower frequency-info 2>/dev/null

# 切换为性能模式（关闭节能）
cpupower frequency-set -g performance 2>/dev/null || \
  for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
      echo performance > $cpu
  done

# 持久化（systemd）
cat > /etc/systemd/system/cpu-performance.service << 'EOF'
[Unit]
Description=Set CPU governor to performance
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/bin/bash -c "for f in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do echo performance > $f; done"
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF
systemctl enable --now cpu-performance.service

# 查看 CPU 当前频率
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq | awk '{s+=$1; n++} END {printf "平均: %.0f MHz\n", s/n/1000}'

# 检查 CPU 是否处于节能降频
grep "cpu MHz" /proc/cpuinfo | awk '{sum+=$4; n++} END {printf "当前频率均值: %.0f MHz\n", sum/n}'
```

---

## 4. 进程调度优化

```bash
# 查看进程调度策略
chrt -p <PID>

# 设置实时调度（延迟敏感服务）
chrt -f -p 50 <PID>    # SCHED_FIFO，优先级50
chrt -r -p 50 <PID>    # SCHED_RR，优先级50

# 调整 nice 值（普通进程）
renice -5 -p <PID>     # 提高优先级（-20最高）
renice +10 -p <PID>    # 降低优先级（+19最低）

# 启动时设置 nice 值
nice -n -5 command

# 使用 cgroups 限制进程 CPU 使用（非容器场景）
cgcreate -g cpu:/limited_group
echo 50000 > /sys/fs/cgroup/cpu/limited_group/cpu.cfs_quota_us    # 50% CPU
cgclassify -g cpu:/limited_group <PID>

# cpulimit（简单方式）
cpulimit -p <PID> -l 50 &    # 限制50%
```

---

## 5. CPU 亲和性与绑核

```bash
# 查看进程当前 CPU 亲和性
taskset -p <PID>

# 将进程绑定到 CPU 0-3
taskset -cp 0-3 <PID>

# 启动时绑核
taskset -c 0-3 ./my_app

# 查看各 CPU 负载分布
mpstat -P ALL 1 1 | grep -v "^$\|^Linux\|^CPU\|Average" | awk '{print "CPU"$2": "$NF"%"}'

# NUMA 感知绑核（同时绑 CPU + 内存）
numactl --cpunodebind=0 --membind=0 ./my_app

# 查看 NUMA 节点上的进程
ps -eo pid,psr,comm | head -20   # psr=当前运行的CPU核
```

---

## 6. NUMA 优化

```bash
# 查看 NUMA 拓扑
numactl --hardware
lstopo 2>/dev/null

# 查看 NUMA 内存统计（命中率）
numastat -m 2>/dev/null
numastat -p <PID> 2>/dev/null

# 关闭自动 NUMA 均衡（减少进程迁移，降低延迟）
sysctl -w kernel.numa_balancing=0

# 开启（多 NUMA 节点服务器建议保持开启）
sysctl -w kernel.numa_balancing=1

# 查看 NUMA miss 率（高miss率说明跨节点访存）
numastat | grep -E "numa_miss|numa_foreign"

# 进程 NUMA 策略
numactl --preferred=0 ./app        # 优先使用节点0的内存
numactl --interleave=all ./app     # 内存在所有节点交错分配（适合大内存均匀访问）
```

---

## 7. 中断绑核

```bash
# 查看中断分布
cat /proc/interrupts | head -30

# 查看网卡中断
grep eth0 /proc/interrupts

# 关闭 irqbalance（手动管理时）
systemctl stop irqbalance
systemctl disable irqbalance

# 将网卡中断绑定到指定 CPU（以 eth0 为例）
# 找到网卡的中断号
NIC_IRQ=$(grep eth0 /proc/interrupts | awk -F: '{print $1}' | tr -d ' ')
# 绑定到 CPU2（bitmask: 4 = 00000100）
echo 4 > /proc/irq/${NIC_IRQ}/smp_affinity

# 多队列网卡绑核（自动脚本）
set_irq_affinity() {
    local nic=$1
    local irq_list=($(grep ${nic} /proc/interrupts | awk -F: '{print $1}' | tr -d ' '))
    local cpu_list=(0 1 2 3 4 5 6 7)  # 绑定到前8核
    for i in "${!irq_list[@]}"; do
        local cpu_mask=$((1 << ${cpu_list[$i % ${#cpu_list[@]}]}))
        printf "%x\n" $cpu_mask > /proc/irq/${irq_list[$i]}/smp_affinity
    done
}
# set_irq_affinity eth0
```

---

## 8. perf 性能剖析

```bash
# 安装 perf
apt install linux-perf 2>/dev/null || yum install perf 2>/dev/null

# 全系统 CPU 热点采样（10秒）
perf top

# 对指定进程采样
perf top -p <PID>

# 记录性能数据（30秒）
perf record -g -a -F 99 -- sleep 30
perf report --stdio | head -50

# CPU 硬件事件统计
perf stat -e cycles,instructions,cache-misses,cache-references,branch-misses -a sleep 10
# 重点指标：
# IPC (instructions/cycles) < 1.0 说明 CPU 利用率低（可能内存延迟）
# cache-miss率 > 5% 说明缓存命中差
# branch-misses率 > 3% 说明分支预测差

# 查看热点函数（火焰图准备）
perf record -g -p <PID> -- sleep 30
perf script > perf.data.txt
# 使用 FlameGraph 工具生成火焰图（需要安装 FlameGraph）
# git clone https://github.com/brendangregg/FlameGraph
# perf script | ./FlameGraph/stackcollapse-perf.pl | ./FlameGraph/flamegraph.pl > flame.svg

# 调度延迟分析
perf sched record -- sleep 10
perf sched latency | head -30

# 系统调用统计
perf stat -e syscalls:sys_enter_read,syscalls:sys_enter_write -p <PID> sleep 5
strace -c -p <PID>   # 更简单的系统调用统计
```

---

## 9. 容器 CPU 限制排查

```bash
# 查看当前容器 CPU 配额
cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us    # -1 表示不限制
cat /sys/fs/cgroup/cpu/cpu.cfs_period_us   # 通常 100000 (100ms)

# 计算 CPU 限制核数
# quota / period = CPU 核数限制
# 例：quota=200000, period=100000 → 2核

# 查看 CPU throttling（被限制次数）
cat /sys/fs/cgroup/cpu/cpu.stat
# nr_throttled 持续增长说明 CPU 经常被限制

# Kubernetes 中检查 throttling
kubectl exec <pod> -- cat /sys/fs/cgroup/cpu/cpu.stat
kubectl describe pod <pod> | grep -A5 "Limits\|Requests"
kubectl top pod <pod> --containers

# 判断是否需要提高 CPU limit
# throttled_time (纳秒) / 总运行时间 > 5% 建议扩容
```