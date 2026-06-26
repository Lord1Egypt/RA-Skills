# 常用性能工具输出解读指南

> 快速理解 top / vmstat / iostat / ss / sar / perf stat / mpstat 等工具输出中每个字段的含义，判断是否存在性能问题。

## 目录

- [top 输出解读](#top-输出解读)
- [vmstat 输出解读](#vmstat-输出解读)
- [iostat 输出解读](#iostat-输出解读)
- [mpstat 输出解读](#mpstat-输出解读)
- [ss 输出解读](#ss-输出解读)
- [sar 输出解读](#sar-输出解读)
- [perf stat 输出解读](#perf-stat-输出解读)
- [free 输出解读](#free-输出解读)
- [pidstat 输出解读](#pidstat-输出解读)
- [iotop 输出解读](#iotop-输出解读)
- [dmesg 输出解读](#dmesg-输出解读)
- [综合诊断速查表](#综合诊断速查表)
- [实用技巧](#实用技巧)

---

## top 输出解读

### 头部摘要行

```text
top - 14:32:01 up 5 days, 3:21,  2 users,  load average: 2.15, 1.87, 1.52
Tasks: 287 total,   2 running, 285 sleeping,   0 stopped,   0 zombie
%Cpu(s): 25.3 us,  8.1 sy,  0.0 ni, 63.2 id,  2.1 wa,  0.0 hi,  1.3 si,  0.0 st
MiB Mem :  15921.4 total,   1234.5 free,   8765.4 used,   5921.5 buff/cache
MiB Swap:   2048.0 total,   1536.0 free,    512.0 used.   6543.2 avail Mem
```

#### load average 三个值

| 值 | 含义 | 判断标准 |
|---|------|---------|
| 第 1 个 | 1 分钟平均负载 | > CPU 核数 × 2 → 过载 |
| 第 2 个 | 5 分钟平均负载 | 趋势参考 |
| 第 3 个 | 15 分钟平均负载 | 长期趋势 |

> **判断方法**：`load average / CPU核数`，< 1 正常，1-2 偏高，> 2 过载。
> 注意：load average 包含 D 状态（不可中断睡眠）进程，高 load 不一定是 CPU 瓶颈。

#### %Cpu(s) 行字段

| 字段 | 全称 | 含义 | 异常判断 |
|------|------|------|---------|
| `us` | user | 用户态 CPU 时间（应用代码） | > 80% → 应用层 CPU 密集 |
| `sy` | system | 内核态 CPU 时间（系统调用） | > 30% → 系统调用频繁/锁竞争 |
| `ni` | nice | 低优先级进程 CPU 时间 | 通常接近 0 |
| `id` | idle | 空闲 CPU 时间 | < 10% → CPU 饱和 |
| `wa` | iowait | 等待 I/O 完成的 CPU 时间 | > 20% → I/O 瓶颈 |
| `hi` | hardware irq | 硬件中断 CPU 时间 | > 5% → 网卡/磁盘中断过多 |
| `si` | software irq | 软件中断 CPU 时间 | > 10% → 网络包处理过多 |
| `st` | steal | 被虚拟化宿主机偷走的 CPU 时间 | > 5% → 虚拟机争抢/超卖 |

#### 进程列表关键列

| 列 | 含义 | 说明 |
|----|------|------|
| `VIRT` | 虚拟内存 | 进程申请的总虚拟地址空间（含未实际分配的） |
| `RES` | 常驻内存 | 实际使用的物理内存（**最重要**） |
| `SHR` | 共享内存 | 与其他进程共享的内存（如共享库） |
| `%CPU` | CPU 使用率 | 单核 100%，8 核最大 800% |
| `%MEM` | 内存使用率 | RES / 总物理内存 |
| `S` | 进程状态 | R=运行, S=睡眠, D=不可中断(I/O等待), Z=僵尸, T=停止 |
| `TIME+` | 累计 CPU 时间 | 进程启动以来消耗的总 CPU 时间 |

> **快速排查**：
> - `D` 状态进程多 → I/O 瓶颈（检查 iostat）
> - `Z` 状态进程多 → 父进程未正确回收子进程
> - `%CPU` 高 + `us` 高 → 用户态代码热点（用 perf 分析）
> - `%CPU` 高 + `sy` 高 → 系统调用频繁（用 strace/bpftrace 分析）

---

## vmstat 输出解读

```bash
vmstat 1 5
```

```text
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 3  0  51200 234560 123456 4567890    0    0    12   156 1523 45678 25  8 63  3  1
```

### 字段详解

| 分组 | 字段 | 含义 | 异常判断 |
|------|------|------|---------|
| **procs** | `r` | 运行队列中等待 CPU 的进程数 | > CPU 核数 × 2 → CPU 饱和 |
| | `b` | 不可中断睡眠（D 状态）的进程数 | > 0 持续 → I/O 阻塞 |
| **memory** | `swpd` | 已使用的 Swap 大小 (KB) | > 0 且持续增长 → 内存不足 |
| | `free` | 空闲物理内存 (KB) | 接近 0 不一定有问题（看 available） |
| | `buff` | 用于块设备 I/O 缓冲的内存 | — |
| | `cache` | 用于文件系统缓存的内存 | 大是好事，可被回收 |
| **swap** | `si` | 从磁盘换入内存的速率 (KB/s) | > 0 持续 → 内存严重不足 |
| | `so` | 从内存换出到磁盘的速率 (KB/s) | > 0 持续 → 内存严重不足 |
| **io** | `bi` | 块设备读取速率 (blocks/s) | 结合 iostat 判断 |
| | `bo` | 块设备写入速率 (blocks/s) | 突然飙高 → 大量写入 |
| **system** | `in` | 每秒中断数 | > 10 万 → 中断过多 |
| | `cs` | 每秒上下文切换数 | > 5 万 → 偏高，> 10 万 → 过高 |
| **cpu** | `us/sy/id/wa/st` | 同 top %Cpu(s) | 见 top 解读 |

> **关键判断**：
> - `r` > 核数 + `id` < 10% → CPU 瓶颈
> - `b` > 0 + `wa` > 20% → I/O 瓶颈
> - `si/so` > 0 持续 → 内存瓶颈（需加内存或调 swappiness）
> - `cs` > 10 万 → 调度过频（检查线程数、调度器参数）

---

## iostat 输出解读

```bash
iostat -xz 1 3
```

```text
Device  r/s    w/s   rkB/s   wkB/s  rrqm/s  wrqm/s  %rrqm  %wrqm  r_await  w_await  aqu-sz  rareq-sz  wareq-sz  svctm  %util
sda     150.00 80.00 6000.00 3200.00  5.00   20.00   3.23  20.00    1.50     3.20    0.45    40.00     40.00     2.17   50.00
```

### 字段详解

| 字段 | 含义 | 异常判断 |
|------|------|---------|
| `r/s` | 每秒读请求数 | — |
| `w/s` | 每秒写请求数 | — |
| `rkB/s` | 每秒读取 KB | — |
| `wkB/s` | 每秒写入 KB | — |
| `rrqm/s` | 每秒合并的读请求数 | 高 → I/O 调度器在合并相邻请求 |
| `wrqm/s` | 每秒合并的写请求数 | 高 → 写合并效果好 |
| `r_await` | 读请求平均等待时间 (ms) | HDD > 20ms / SSD > 5ms → 偏高 |
| `w_await` | 写请求平均等待时间 (ms) | HDD > 20ms / SSD > 5ms → 偏高 |
| `aqu-sz` | 平均 I/O 队列深度 | > 1 持续 → 磁盘繁忙 |
| `rareq-sz` | 平均读请求大小 (KB) | 小 → 随机 I/O，大 → 顺序 I/O |
| `wareq-sz` | 平均写请求大小 (KB) | 同上 |
| `svctm` | 平均服务时间 (ms) | **已废弃**，不要参考 |
| `%util` | 磁盘利用率 | > 80% → 磁盘繁忙，> 95% → 饱和 |

> **关键判断**：
> - `%util` > 80% → 磁盘接近饱和
> - `await` > 20ms (HDD) 或 > 5ms (SSD) → I/O 延迟高
> - `aqu-sz` 持续 > 2 → 请求积压
> - `rareq-sz` 小 + `r/s` 高 → 大量随机小 I/O（考虑换 SSD 或优化访问模式）
>
> ⚠️ **注意**：NVMe 设备 `%util` 可能不准确（多队列设备），应以 `await` 为主要判断依据。

---

## mpstat 输出解读

```bash
mpstat -P ALL 1 3
```

```text
CPU    %usr   %nice    %sys %iowait   %irq   %soft  %steal  %guest  %gnice   %idle
all    25.13   0.00    8.05    2.10    0.00    1.30    0.00    0.00    0.00   63.42
  0    95.00   0.00    3.00    0.00    0.00    2.00    0.00    0.00    0.00    0.00
  1     5.00   0.00    2.00    0.00    0.00    0.00    0.00    0.00    0.00   93.00
```

### 字段含义

| 字段 | 含义 | 说明 |
|------|------|------|
| `%usr` | 用户态 CPU | 同 top 的 us |
| `%sys` | 内核态 CPU | 同 top 的 sy |
| `%iowait` | I/O 等待 | 同 top 的 wa |
| `%irq` | 硬件中断 | 同 top 的 hi |
| `%soft` | 软件中断 | 同 top 的 si |
| `%steal` | 虚拟化偷取 | 同 top 的 st |
| `%idle` | 空闲 | 同 top 的 id |

> **mpstat 独特价值**：可以看到**每个 CPU 核心**的使用情况。
> - 某个核 100% 其他核空闲 → 单线程瓶颈或中断未均衡
> - 某个核 `%soft` 特别高 → 网络软中断集中在一个核（需要 RPS/RFS）
> - 所有核 `%iowait` 高 → 全局 I/O 瓶颈

---

## ss 输出解读

### ss -s（连接汇总）

```bash
ss -s
```

```text
Total: 1532
TCP:   856 (estab 423, closed 215, orphaned 12, timewait 198)
Transport Total     IP        IPv6
RAW       2         1         1
UDP       24        18        6
TCP       641       580       61
INET      667       599       68
FRAG      0         0         0
```

| 字段 | 含义 | 异常判断 |
|------|------|---------|
| `estab` | 已建立的 TCP 连接 | 持续增长不回收 → 连接泄漏 |
| `closed` | 已关闭的 TCP 连接 | — |
| `orphaned` | 孤儿连接（无进程关联） | > 100 → 应用未正确关闭连接 |
| `timewait` | TIME_WAIT 状态连接 | > 1 万 → 短连接过多，需开启 tcp_tw_reuse |

### ss -ant（TCP 连接状态分布）

```bash
ss -ant | awk '{print $1}' | sort | uniq -c | sort -rn
```

| 状态 | 含义 | 异常判断 |
|------|------|---------|
| `ESTAB` | 已建立 | 正常工作连接 |
| `TIME-WAIT` | 主动关闭方等待 2MSL | > 1 万 → `tcp_tw_reuse=1` |
| `CLOSE-WAIT` | 被动关闭方未调用 close() | > 100 → **应用 BUG**（未关闭连接） |
| `FIN-WAIT-1` | 主动关闭已发 FIN | 大量积压 → 对端不响应 |
| `FIN-WAIT-2` | 主动关闭等待对端 FIN | 大量积压 → 对端未关闭 |
| `SYN-SENT` | 发起连接等待响应 | 大量 → 目标不可达/防火墙 |
| `SYN-RECV` | 收到 SYN 等待 ACK | 大量 → SYN Flood 攻击 |
| `LISTEN` | 监听中 | 正常 |
| `LAST-ACK` | 等待最后 ACK | 少量正常 |

> **关键判断**：
> - `CLOSE-WAIT` 大量 → 应用层 BUG，必须修复代码
> - `TIME-WAIT` 大量 → 正常但可优化（`tcp_tw_reuse=1`）
> - `SYN-RECV` 大量 → 可能遭受 SYN Flood（启用 `tcp_syncookies`）

### ss -lntp（监听端口）

```bash
ss -lntp
```

| 字段 | 含义 |
|------|------|
| `Recv-Q` | 当前等待 accept() 的连接数（全连接队列使用量） |
| `Send-Q` | 全连接队列最大长度（backlog） |

> **判断**：`Recv-Q` 接近 `Send-Q` → 全连接队列溢出，需增大 `somaxconn` 和应用 backlog。

---

## sar 输出解读

### 常用子命令

| 命令 | 用途 | 关键指标 |
|------|------|---------|
| `sar -u 1 5` | CPU 使用率 | `%user`, `%system`, `%iowait`, `%idle` |
| `sar -r 1 5` | 内存使用 | `kbmemfree`, `%memused`, `kbcached` |
| `sar -B 1 5` | 内存分页 | `pgpgin/s`, `pgpgout/s`, `fault/s`, `majflt/s` |
| `sar -d 1 5` | 磁盘 I/O | `tps`, `rd_sec/s`, `wr_sec/s`, `await`, `%util` |
| `sar -n DEV 1 5` | 网络流量 | `rxpck/s`, `txpck/s`, `rxkB/s`, `txkB/s` |
| `sar -n TCP 1 5` | TCP 统计 | `active/s`, `passive/s`, `retrans/s` |
| `sar -w 1 5` | 上下文切换 | `cswch/s`（每秒上下文切换） |
| `sar -q 1 5` | 运行队列 | `runq-sz`, `plist-sz`, `ldavg-1/5/15` |

### sar -n TCP 关键指标

| 字段 | 含义 | 异常判断 |
|------|------|---------|
| `active/s` | 每秒主动发起的 TCP 连接数 | 高 → 大量对外连接 |
| `passive/s` | 每秒被动接受的 TCP 连接数 | 高 → 大量入站连接 |
| `retrans/s` | 每秒 TCP 重传次数 | > active+passive 的 1% → 网络质量差 |
| `iseg/s` | 每秒收到的 TCP 段 | — |
| `oseg/s` | 每秒发送的 TCP 段 | — |

### sar -B 内存分页关键指标

| 字段 | 含义 | 异常判断 |
|------|------|---------|
| `pgpgin/s` | 每秒从磁盘换入的 KB | > 0 持续 → Swap 活跃 |
| `pgpgout/s` | 每秒换出到磁盘的 KB | > 0 持续 → 内存压力 |
| `fault/s` | 每秒缺页异常数 | — |
| `majflt/s` | 每秒主缺页异常（需磁盘 I/O） | > 10 → 内存严重不足 |

---

## perf stat 输出解读

```bash
perf stat -e cycles,instructions,cache-misses,cache-references,branch-misses,branches -a sleep 5
```

```text
 Performance counter stats for 'system wide':

     15,234,567,890      cycles
     12,345,678,901      instructions              #    0.81  insn per cycle
        234,567,890      cache-references
         12,345,678      cache-misses              #    5.26 % of all cache refs
      1,234,567,890      branches
         23,456,789      branch-misses             #    1.90% of all branches

       5.001234567 seconds time elapsed
```

### 关键指标解读

| 指标 | 含义 | 判断标准 |
|------|------|---------|
| **IPC** (insn per cycle) | 每个时钟周期执行的指令数 | > 1.0 好，< 0.5 差（可能有内存瓶颈） |
| **cache-miss rate** | 缓存未命中率 | < 5% 正常，> 10% → 数据局部性差 |
| **branch-miss rate** | 分支预测失败率 | < 2% 正常，> 5% → 分支密集代码 |
| `cycles` | CPU 时钟周期总数 | 基准参考 |
| `instructions` | 执行的指令总数 | 基准参考 |

> **快速判断**：
> - IPC < 0.5 + cache-miss > 10% → 内存访问模式差（指针追逐、随机访问）
> - IPC < 0.5 + cache-miss 正常 → 可能是分支预测或流水线停顿
> - IPC > 1.0 → CPU 效率好，瓶颈不在 CPU 微架构层面

### 常用 perf stat 事件组合

```bash
# CPU 微架构分析
perf stat -e cycles,instructions,cache-misses,cache-references,branch-misses,branches -p <PID> sleep 10

# 内存子系统分析
perf stat -e L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses -p <PID> sleep 10

# TLB 分析
perf stat -e dTLB-loads,dTLB-load-misses,iTLB-loads,iTLB-load-misses -p <PID> sleep 10

# 系统调用开销
perf stat -e syscalls:sys_enter -a sleep 5
```

---

## free 输出解读

```bash
free -h
```

```text
              total        used        free      shared  buff/cache   available
Mem:           15Gi       8.5Gi       1.2Gi       256Mi       5.8Gi       6.4Gi
Swap:         2.0Gi       512Mi       1.5Gi
```

### 字段详解

| 字段 | 含义 | 说明 |
|------|------|------|
| `total` | 物理内存总量 | — |
| `used` | 已使用内存 | 包含应用程序使用的内存 |
| `free` | 完全空闲内存 | **不要用这个判断内存是否充足** |
| `shared` | tmpfs 等共享内存 | — |
| `buff/cache` | 缓冲区 + 页缓存 | 可被回收，不算"真正占用" |
| `available` | **实际可用内存** | **最重要的指标**，包含可回收的 cache |

> **关键判断**：
> - 看 `available` 而非 `free`！Linux 会尽量利用空闲内存做缓存
> - `available` < 总内存 10% → 内存压力大
> - `Swap used` > 0 且持续增长 → 内存不足
> - `Swap used` > 0 但稳定 → 可能只是历史峰值，不一定当前有问题

---

## 综合诊断速查表

| 症状 | 首先看 | 关键指标 | 下一步 |
|------|--------|---------|--------|
| 系统慢/卡顿 | `top` / `uptime` | load average, %Cpu | 根据 us/sy/wa 分流 |
| CPU 高 | `mpstat -P ALL` | 各核使用率分布 | `perf top` 找热点 |
| I/O 慢 | `iostat -xz 1` | await, %util | `iotop` 找进程 |
| 内存不足 | `free -h` | available, Swap | `ps aux --sort=-%mem` |
| 网络问题 | `ss -s` | TIME_WAIT, CLOSE_WAIT | `ss -ant`, `sar -n TCP` |
| 上下文切换高 | `vmstat 1` | cs 列 | `pidstat -w` 找进程 |
| 负载高 CPU 低 | `vmstat 1` | b 列（D 状态进程） | `iostat`, 检查 NFS/存储 |

---

## pidstat 输出解读

### 基本用法

```bash
# CPU + I/O 综合（每秒，共 5 次）
pidstat -u -d 1 5

# 上下文切换（每秒）
pidstat -w 1 5

# 内存使用
pidstat -r 1 5

# 指定进程
pidstat -p <PID> -u -d -r 1 5
```

### 关键字段

#### CPU 模式 (`pidstat -u`)

| 字段 | 含义 | 关注点 |
|------|------|--------|
| `%usr` | 用户态 CPU 使用率 | 应用逻辑消耗 |
| `%system` | 内核态 CPU 使用率 | 系统调用频繁时升高 |
| `%wait` | I/O 等待占比 | 高 → 进程受 I/O 阻塞 |
| `%CPU` | 总 CPU 使用率 | 定位 CPU 密集型进程 |

#### I/O 模式 (`pidstat -d`)

| 字段 | 含义 | 关注点 |
|------|------|--------|
| `kB_rd/s` | 每秒读取 KB | 定位读密集型进程 |
| `kB_wr/s` | 每秒写入 KB | 定位写密集型进程 |
| `kB_ccwr/s` | 每秒取消写入 KB | 高 → 频繁创建删除临时文件 |
| `iodelay` | I/O 延迟（时钟周期） | 高 → 进程受 I/O 阻塞严重 |

#### 上下文切换模式 (`pidstat -w`)

| 字段 | 含义 | 关注点 |
|------|------|--------|
| `cswch/s` | 自愿上下文切换/秒 | 高 → 频繁等待 I/O 或锁 |
| `nvcswch/s` | 非自愿上下文切换/秒 | 高 → CPU 竞争激烈 |

> **诊断技巧**：`cswch/s` 高通常是 I/O 等待，`nvcswch/s` 高通常是 CPU 不够用。

---

## iotop 输出解读

### 基本用法

```bash
# 交互模式（只显示有 I/O 活动的进程）
sudo iotop -o

# 批处理模式（适合脚本）
sudo iotop -o -b -n 3

# 累积模式
sudo iotop -o -a
```

### 关键字段

| 字段 | 含义 | 关注点 |
|------|------|--------|
| `DISK READ` | 实际磁盘读取速率 | 区分于缓存读取 |
| `DISK WRITE` | 实际磁盘写入速率 | 包括 flush/sync |
| `SWAPIN` | Swap 读入占比 | 高 → 内存不足 |
| `IO>` | I/O 等待占比 | 高 → 进程被 I/O 阻塞 |
| `PRIO` | I/O 优先级 | `be/4` = 默认，`rt/` = 实时 |

### 常见诊断场景

| 现象 | 原因 | 解决方案 |
|------|------|---------|
| 某进程 DISK WRITE 持续很高 | 大量日志/临时文件写入 | 检查日志级别、使用 tmpfs |
| SWAPIN 列有值 | 内存不足，频繁换入 | 增加内存或减少进程数 |
| jbd2/sda 写入高 | ext4 日志写入频繁 | 检查 fsync 调用频率 |
| kworker 写入高 | 内核脏页回写 | 调整 dirty_ratio/dirty_expire |

> **注意**：iotop 需要 root 权限和内核 `CONFIG_TASK_IO_ACCOUNTING` 支持。

---

## dmesg 输出解读

### 基本用法

```bash
# 最近 50 条内核日志
dmesg | tail -50

# 带时间戳（人类可读）
dmesg -T | tail -50

# 只看错误和警告
dmesg --level=err,warn | tail -30

# 实时跟踪
dmesg -w
```

### 关键事件识别

#### OOM Kill 事件

```text
[  123.456789] Out of memory: Killed process 1234 (java) total-vm:8192000kB, anon-rss:4096000kB
```

| 字段 | 含义 |
|------|------|
| `total-vm` | 进程虚拟内存总量 |
| `anon-rss` | 匿名页物理内存（实际使用） |
| `oom_score_adj` | OOM 评分调整值（-1000 到 1000） |

#### 硬件错误

```bash
# 内存 ECC 错误
[  456.789012] EDAC MC0: 1 CE on mc#0csrow#0channel#0

# 磁盘 I/O 错误
[  789.012345] ata1.00: exception Emask 0x0 SAct 0x0 SErr 0x0 action 0x6 frozen
[  789.012346] ata1.00: failed command: READ DMA EXT

# NVMe 超时
[  999.111222] nvme nvme0: I/O 123 QID 4 timeout, completion polled
```

#### 网络事件

```bash
# 连接跟踪表满
nf_conntrack: table full, dropping packet

# TCP 缓冲区不足
TCP: out of memory -- consider tuning tcp_mem
```

### 常见 dmesg 诊断模式

| 关键词 | 含义 | 行动 |
|--------|------|------|
| `Out of memory` | OOM Kill | 检查内存使用，增加 limit |
| `killed process` | 进程被杀 | 配合 OOM 分析 |
| `nf_conntrack: table full` | conntrack 表满 | 增大 nf_conntrack_max |
| `TCP: out of memory` | TCP 内存不足 | 调整 tcp_mem |
| `ata.*error\|failed` | 磁盘硬件错误 | 检查 SMART，准备换盘 |
| `EDAC.*CE` | 内存纠错错误 | 监控频率，考虑换内存 |
| `Kernel panic` | 内核崩溃 | 分析 kdump，检查驱动 |
| `segfault` | 段错误 | 应用 bug，检查 coredump |
| `blocked for more than` | 进程长时间 D 状态 | I/O 或 NFS 挂载问题 |

> **最佳实践**：生产环境建议配置 `rsyslog` 或 `journald` 持久化内核日志，并设置告警规则监控 OOM、硬件错误等关键事件。

---

## 实用技巧

### 快速全景检查（一行命令）

```bash
echo "=== LOAD ===" && uptime && echo "=== CPU ===" && mpstat 1 1 && echo "=== MEM ===" && free -h && echo "=== DISK ===" && iostat -xz 1 1 && echo "=== NET ===" && ss -s && echo "=== CS ===" && vmstat 1 3
```

### 持续监控（每秒刷新）

```bash
# CPU + 内存 + I/O 综合
vmstat 1

# 磁盘 I/O 详情
iostat -xz 1

# 网络流量
sar -n DEV 1

# 每个进程的 CPU + I/O
pidstat -d -u 1
```

### 历史数据回溯（需要 sysstat 已配置）

```bash
# 查看昨天的 CPU 使用率
sar -u -f /var/log/sa/sa$(date -d yesterday +%d)

# 查看昨天 14:00-15:00 的磁盘 I/O
sar -d -f /var/log/sa/sa$(date -d yesterday +%d) -s 14:00:00 -e 15:00:00
```
