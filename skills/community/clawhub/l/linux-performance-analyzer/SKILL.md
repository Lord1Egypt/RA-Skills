---
name: linux-performance-analyzer
description: >
  Linux 系统性能分析与调优全能专家。融合多个专项 skill 精华，覆盖 CPU、内存、磁盘 I/O、
  网络、内核参数、编译优化、容器/K8s 等全维度。触发场景：
  (1) 系统变慢/卡顿/负载高/响应慢
  (2) 内存不足/OOM Kill/Swap 使用率高
  (3) CPU 使用率异常/iowait 高/上下文切换过多
  (4) 磁盘读写慢/I/O 瓶颈/iowait 高
  (5) 网络延迟/丢包/TIME_WAIT 过多/吞吐不足
  (6) 需要调整 sysctl 内核参数
  (7) GCC/Clang/Rust 编译优化建议
  (8) 解读 top/vmstat/iostat/perf/sar/ss 等命令输出
  (9) 容器/K8s 资源争抢/CPU throttling
  (10) 建立性能基线/监控告警体系
---

# Linux 性能分析与调优全能手册 (linux-perf-master)

> 本 skill 整合了 linux-perf-advisor、linux-perf-analysis、linux-perf-tune、linux-performance-analyzer 四个专项 skill 的精华内容，提供完整的性能诊断→根因分析→优化实施→验证回滚闭环能力。

---

## 📋 分析工作流

```
第一步：收集现场数据（运行快照脚本或手动采集）
        ↓
第二步：识别瓶颈类型（CPU / 内存 / I/O / 网络 / 编译）
        ↓
第三步：查阅对应参考文档深入分析
        ↓
第四步：输出标准化分析报告（含问题/原因/方案/风险/验证/回滚）
        ↓
第五步：实施优化并验证效果
```

---

## 第一步：快速数据采集

### 方式一：使用采集脚本（推荐）

```bash
# 系统快照（全面）
bash scripts/collect_snapshot.sh

# 持续监控（后台运行，每5秒采样）
bash scripts/perf_monitor.sh &
```

### 方式二：手动快速诊断命令

```bash
# ① 负载概览
uptime && cat /proc/loadavg

# ② 内存状态
free -h && cat /proc/meminfo | grep -E "MemTotal|MemFree|MemAvailable|Buffers|Cached|SwapTotal|SwapFree|Dirty|AnonPages|Slab|HugePages"

# ③ CPU + 进程
top -bn1 | head -20
mpstat -P ALL 1 3

# ④ I/O
iostat -xz 1 3
iotop -o -b -n 3 | head -20

# ⑤ 网络
ss -s
ss -ant | awk '{print $1}' | sort | uniq -c | sort -rn

# ⑥ 内核参数现状
sysctl -a 2>/dev/null | grep -E "^vm\.|^net\.|^kernel\.sched" | head -60

# ⑦ 上下文切换
vmstat 1 5

# ⑧ OOM 历史
dmesg | grep -iE "oom|killed process" | tail -20

# ⑨ 中断分布
cat /proc/interrupts | sort -k2 -rn | head -20

# ⑩ 磁盘空间
df -h && lsblk
```

---

## 第二步：瓶颈快速识别表

| 现象 | 可能瓶颈 | 参考文档 |
|------|---------|---------|
| load average 持续 > CPU核数×2 | CPU 饱和 或 I/O 等待 | references/cpu.md |
| vmstat cs（上下文切换）> 10万/秒 | CPU 调度过频 | references/cpu.md |
| %iowait > 20% | 磁盘 I/O 瓶颈 | references/disk_io.md |
| MemAvailable < 总内存 10% | 内存压力 | references/memory.md |
| Swap 使用率 > 20% 且持续增长 | 内存严重不足 | references/memory.md |
| OOM Killer 日志出现 | 内存泄漏 或 配置不当 | references/memory.md |
| Dirty 持续 > 物理内存 5% | 写回积压 I/O 跟不上 | references/disk_io.md |
| 大量 TIME_WAIT / CLOSE_WAIT | 网络连接泄漏/未优化 | references/network.md |
| 网络丢包 / 重传率高 | TCP 参数/带宽/拥塞 | references/network.md |
| perf/gprof 热点在用户态代码 | 编译未优化 | references/compile_optimization.md |
| CPU throttling（容器） | cgroup CPU 限制过低 | references/cpu.md |

---

## 第三步：分析报告输出格式规范

每个问题按以下六要素输出，格式统一：

```markdown
### 🔴/🟡/🟢 问题名称（优先级 P0/P1/P2）

**【问题】**
观察到的指标数据和异常现象

**【原因】**
根因推断和分析

**【方案】**
```bash
# 具体优化命令
```

**【风险】**
改动的副作用和注意事项

**【验证】**
```bash
# 验证效果的命令
```

**【回滚】**
```bash
# 回滚命令
```
```

### 报告汇总表格模板

```markdown
| 优先级 | 问题 | 影响范围 | 操作难度 | 建议操作 |
|--------|------|----------|----------|----------|
| 🔴 P0 | ... | ... | 低/中/高 | ... |
```

---

## 第四步：常见场景快速处理

### 🔴 内存问题

**诊断命令：**
```bash
cat /proc/meminfo
dmesg | grep -i "oom\|killed process" | tail -20
ps aux --sort=-%mem | head -15
slabtop -o | head -20
numastat -m 2>/dev/null          # NUMA 信息（多路服务器）
```

**核心调优（详见 references/memory.md）：**
```bash
# Swap 倾向（服务器推荐 10，数据库推荐 1）
sysctl -w vm.swappiness=10

# 增大内核保留内存（防止 OOM 误杀关键进程）
sysctl -w vm.min_free_kbytes=262144   # 256MB

# 脏页回写（写密集场景）
sysctl -w vm.dirty_ratio=10
sysctl -w vm.dirty_background_ratio=5

# 透明大页（数据库/延迟敏感服务关闭）
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag

# 保护关键进程免遭 OOM Kill
echo -1000 > /proc/<PID>/oom_score_adj
```

---

### 🔴 CPU 问题

**诊断命令：**
```bash
mpstat -P ALL 1 5
pidstat -u 1 5
vmstat 1 5                          # 重点看 r（运行队列）和 cs（上下文切换）
cat /proc/interrupts | sort -k2 -rn | head -20
perf stat -e cycles,instructions,cache-misses -a sleep 5
```

**核心调优（详见 references/cpu.md）：**
```bash
# 减少上下文切换（调度粒度）
sysctl -w kernel.sched_min_granularity_ns=10000000
sysctl -w kernel.sched_wakeup_granularity_ns=15000000
sysctl -w kernel.sched_migration_cost_ns=5000000

# 关闭 NUMA 均衡（延迟敏感场景）
sysctl -w kernel.numa_balancing=0

# CPU 性能模式
echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

# 进程 CPU 亲和性绑核
taskset -pc 0-3 <PID>

# 调整进程优先级
renice -5 -p <PID>    # 提高优先级
renice +10 -p <PID>   # 降低优先级
```

---

### 🔴 磁盘 I/O 问题

**诊断命令：**
```bash
iostat -xz 1 5
iotop -o -n 3 -b | head -30
cat /sys/block/sda/queue/nr_requests
cat /sys/block/sda/queue/scheduler
mount | grep -v "tmpfs\|proc\|sys\|dev"
```

**核心调优（详见 references/disk_io.md）：**
```bash
# I/O 调度器（SSD: mq-deadline 或 none；HDD: bfq）
echo mq-deadline > /sys/block/sda/queue/scheduler

# 读预读（顺序读为主时增大）
blockdev --setra 4096 /dev/sda    # 2MB 预读

# 增大内核请求队列
echo 256 > /sys/block/sda/queue/nr_requests

# 脏页控制（防止写爆）
sysctl -w vm.dirty_bytes=268435456         # 256MB
sysctl -w vm.dirty_background_bytes=67108864  # 64MB
```

---

### 🔴 网络问题

**诊断命令：**
```bash
ss -s
ss -ant | awk '{print $1}' | sort | uniq -c
netstat -s | grep -E "fail|error|drop|overflow|reject" | grep -v " 0 "
ip -s link
ping -c 100 <target> | tail -3
```

**核心调优（详见 references/network.md）：**
```bash
# TIME_WAIT 回收（高并发短连接）
sysctl -w net.ipv4.tcp_tw_reuse=1
sysctl -w net.ipv4.tcp_fin_timeout=30

# 端口范围（主动发起连接的服务）
sysctl -w net.ipv4.ip_local_port_range="1024 65535"

# 连接队列（高并发服务）
sysctl -w net.core.somaxconn=65535
sysctl -w net.ipv4.tcp_max_syn_backlog=16384
sysctl -w net.core.netdev_max_backlog=16384

# TCP 缓冲区（高带宽场景）
sysctl -w net.core.rmem_max=16777216
sysctl -w net.core.wmem_max=16777216
sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216"
sysctl -w net.ipv4.tcp_wmem="4096 65536 16777216"

# 文件描述符
sysctl -w fs.file-max=2097152
ulimit -n 65535
```

---

### 🟡 编译优化（详见 references/compile_optimization.md）

> **触发条件**：perf/gprof 热点集中在用户态自编译代码，且当前编译选项为 -O0/-O1

```bash
# 快速升级：从 -O1 升到 -O2（大多数场景无需其他改动）
gcc -O2 -march=native -mtune=native -fno-omit-frame-pointer -o app src/*.c

# 高性能计算场景：-O3 + LTO
gcc -O3 -march=native -flto=thin -fno-omit-frame-pointer -o app src/*.c

# 最优：PGO + LTO 组合（提升 10-20%）
# 见 references/compile_optimization.md 第4-5节
```

---

## 参数修改规范

### 临时生效（立即，重启失效）
```bash
sysctl -w 参数名=值
echo 值 > /proc/sys/...
```

### 持久化（重启后仍生效）
```bash
# 推荐：独立配置文件，易于管理和回滚
cat > /etc/sysctl.d/99-perf-analyzer.conf << 'EOF'
vm.swappiness=10
vm.dirty_ratio=10
# ... 其他参数
EOF
sysctl --system
```

### 回滚
```bash
# 临时回滚（立即生效）
sysctl -w 参数名=原始值

# 持久化回滚
rm /etc/sysctl.d/99-perf-analyzer.conf
sysctl --system
```

---

## 性能基线与告警阈值

### 告警阈值参考

| 指标 | 正常 | 警告 | 严重 |
|------|------|------|------|
| CPU 使用率 | < 60% | > 70% | > 90% |
| 内存可用 | > 30% | < 20% | < 10% |
| Swap 使用率 | 0% | > 10% | > 30% |
| 磁盘使用率 | < 70% | > 80% | > 95% |
| load average | < 核数 | > 核数×1.5 | > 核数×2 |
| I/O await | < 10ms | > 20ms | > 50ms |
| 磁盘 %util | < 60% | > 80% | > 95% |
| 上下文切换/秒 | < 5万 | > 10万 | > 50万 |
| TCP 重传率 | < 0.1% | > 1% | > 5% |

### 建立性能基线

```bash
# 在系统正常时保存基线
bash scripts/collect_snapshot.sh > /var/log/perf-baseline-$(date +%Y%m%d).txt

# 定期对比（加入 crontab）
# 每月更新基线
0 4 1 * * bash /path/to/scripts/collect_snapshot.sh > /var/log/perf-baseline.log

# 每日清理日志
0 2 * * * journalctl --vacuum-time=7d
```

---

## 参考文档索引

| 文档 | 内容 |
|------|------|
| [references/cpu.md](references/cpu.md) | CPU 调优（调度器/亲和性/NUMA/中断绑核/perf profiling） |
| [references/memory.md](references/memory.md) | 内存调优（swappiness/OOM/THP/HugePage/NUMA） |
| [references/disk_io.md](references/disk_io.md) | 磁盘 I/O 调优（调度器/readahead/fio/文件系统） |
| [references/network.md](references/network.md) | 网络调优（TCP 栈/连接队列/BBR/conntrack） |
| [references/kernel_params.md](references/kernel_params.md) | 内核参数速查全表（含默认值/建议值/适用场景） |
| [references/compile_optimization.md](references/compile_optimization.md) | 编译优化（GCC/Clang/PGO/LTO/SIMD） |
| [references/case_studies.md](references/case_studies.md) | 实战案例（MySQL/Nginx/日志服务器/Java/K8s） |

---

## 故障排查清单（10步法）

当性能问题发生时，按顺序检查：

1. [ ] `uptime` 检查负载均值
2. [ ] `free -h` 检查内存可用量
3. [ ] `df -h` 检查磁盘空间
4. [ ] `top -bn1` 检查 CPU 使用率和高耗进程
5. [ ] `vmstat 1 3` 检查上下文切换和 I/O 等待
6. [ ] `iostat -xz 1 3` 检查磁盘 I/O 详情
7. [ ] `ss -s` 检查网络连接状态
8. [ ] `dmesg | tail -50` 检查内核日志（OOM/硬件错误）
9. [ ] `dmesg | grep -i "oom\|killed"` 检查 OOM 事件
10. [ ] 对比基线数据，确认问题时间点

---

## 注意事项

> ⚠️ **生产环境修改前必读**：
>
> 1. 记录原始值：`sysctl 参数名` 保存当前值
> 2. 先临时生效观察效果，确认无副作用再持久化
> 3. 生产环境修改前，务必先在测试环境验证
> 4. `vm.overcommit_memory=2`（严格模式）与多数应用不兼容，慎用
> 5. 透明大页关闭需持久化到启动脚本，重启会还原
> 6. `net.ipv4.tcp_tw_recycle` 在内核 4.12+ 已移除，使用前确认版本
> 7. 容器环境中部分参数（cgroup 限制）需宿主机/平台侧配合修改