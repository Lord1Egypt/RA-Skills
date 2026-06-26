# eBPF / bpftrace / BCC 高级追踪工具

## 目录
1. [eBPF 概述](#ebpf-概述)
2. [bpftrace 安装与使用](#bpftrace-安装与使用)
3. [BCC 工具集](#bcc-工具集)
4. [eBPF 程序类型](#ebpf-程序类型)
5. [libbpf 与 CO-RE](#libbpf-与-co-re)
6. [eBPF Map 类型](#ebpf-map-类型)
7. [生产环境最佳实践](#生产环境最佳实践)
8. [安全约束与限制](#安全约束与限制)

---

## eBPF 概述

eBPF（extended Berkeley Packet Filter）是 Linux 内核中的一个革命性技术，允许在内核空间安全运行沙箱化的程序，无需修改内核源码或加载内核模块。

### 核心能力

| 能力 | 说明 | 典型场景 |
|------|------|---------|
| **可观测性** | 无侵入式追踪内核和用户态函数 | 性能分析、延迟追踪 |
| **网络** | 高性能数据包处理 | 负载均衡（Cilium）、防火墙 |
| **安全** | 系统调用过滤和审计 | 容器安全、入侵检测 |
| **调试** | 动态追踪内核行为 | 故障排查、根因分析 |

### eBPF 架构

```text
用户态                          内核态
┌──────────────┐    ┌──────────────────────────┐
│ BCC/bpftrace │    │  eBPF 验证器（Verifier）  │
│ libbpf       │───>│  ↓                        │
│ 用户程序     │    │  JIT 编译器               │
└──────────────┘    │  ↓                        │
       ↑            │  eBPF 程序（沙箱运行）    │
       │            │  ↕                        │
       │            │  eBPF Maps（数据共享）     │
       └────────────│  ↕                        │
                    │  Hook 点（kprobe/tp/XDP）  │
                    └──────────────────────────┘
```

---

## bpftrace 安装与使用

### 安装

```bash
sudo apt install bpftrace         # Debian/Ubuntu 20.04+
sudo dnf install bpftrace         # Fedora/RHEL 8+
sudo pacman -S bpftrace           # Arch Linux

# 验证安装
bpftrace --version
bpftrace -l 'tracepoint:syscalls:*' | head -10  # 列出可用追踪点
```

### 常用单行命令

```bash
# === 进程追踪 ===
# 跟踪新进程
sudo bpftrace -e 'tracepoint:sched:sched_process_exec { printf("exec %s (pid=%d)\n", comm, pid); }'

# 按进程统计系统调用
sudo bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[comm] = count(); }'

# 按系统调用类型统计
sudo bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[ksym(*(kaddr("sys_call_table") + args->id * 8))] = count(); }'

# 进程生命周期追踪
sudo bpftrace -e 'tracepoint:sched:sched_process_fork { printf("fork: %s (pid=%d) -> child pid=%d\n", comm, pid, args->child_pid); }'

# === I/O 追踪 ===
# 读系统调用延迟分布
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_read { @start[tid] = nsecs; } tracepoint:syscalls:sys_exit_read /@start[tid]/ { @us = hist((nsecs - @start[tid]) / 1000); delete(@start[tid]); }'

# 写系统调用延迟分布
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_write { @start[tid] = nsecs; } tracepoint:syscalls:sys_exit_write /@start[tid]/ { @us = hist((nsecs - @start[tid]) / 1000); delete(@start[tid]); }'

# VFS 读写统计（按进程）
sudo bpftrace -e 'kprobe:vfs_read { @reads[comm] = count(); } kprobe:vfs_write { @writes[comm] = count(); }'

# 磁盘 I/O 延迟分布
sudo bpftrace -e 'tracepoint:block:block_rq_issue { @start[args->dev, args->sector] = nsecs; } tracepoint:block:block_rq_complete /@start[args->dev, args->sector]/ { @us = hist((nsecs - @start[args->dev, args->sector]) / 1000); delete(@start[args->dev, args->sector]); }'

# === 网络追踪 ===
# TCP 连接延迟
sudo bpftrace -e 'kprobe:tcp_v4_connect { @start[tid] = nsecs; } kretprobe:tcp_v4_connect /@start[tid]/ { @us = hist((nsecs - @start[tid]) / 1000); delete(@start[tid]); }'

# TCP 重传追踪
sudo bpftrace -e 'kprobe:tcp_retransmit_skb { @retrans[comm, pid] = count(); }'

# DNS 查询追踪
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_connect /comm == "curl"/ { printf("connect by %s pid=%d\n", comm, pid); }'

# === 调度器追踪 ===
# 调度延迟（运行队列等待时间）
sudo bpftrace -e 'tracepoint:sched:sched_wakeup { @qtime[args->pid] = nsecs; } tracepoint:sched:sched_switch /@qtime[args->next_pid]/ { @us = hist((nsecs - @qtime[args->next_pid]) / 1000); delete(@qtime[args->next_pid]); }'

# 每秒中断统计
sudo bpftrace -e 'hardirq:hardirq_entry { @[args->name] = count(); } interval:s:1 { print(@); clear(@); }'

# 上下文切换统计（按进程）
sudo bpftrace -e 'tracepoint:sched:sched_switch { @[args->prev_comm] = count(); }'

# === 内存追踪 ===
# 页错误统计（按进程）
sudo bpftrace -e 'software:page-faults:1 { @[comm] = count(); }'

# brk 系统调用追踪（堆增长）
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_brk { @[comm] = count(); }'

# mmap 调用追踪
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_mmap { @[comm] = count(); }'
```

### bpftrace 脚本示例

```bash
# 保存为 latency.bt，追踪特定进程的系统调用延迟
cat > /tmp/latency.bt << 'EOF'
#!/usr/bin/env bpftrace

BEGIN {
    printf("Tracing syscall latency... Hit Ctrl-C to end.\n");
}

tracepoint:raw_syscalls:sys_enter /pid == $1/ {
    @start[tid] = nsecs;
}

tracepoint:raw_syscalls:sys_exit /@start[tid]/ {
    $duration = nsecs - @start[tid];
    @syscall_latency = hist($duration / 1000);  // 微秒
    if ($duration > 1000000) {  // > 1ms
        printf("SLOW syscall by %s (pid=%d tid=%d): %d us\n",
               comm, pid, tid, $duration / 1000);
    }
    delete(@start[tid]);
}

END {
    clear(@start);
}
EOF

# 运行：sudo bpftrace /tmp/latency.bt <PID>
```

---

## BCC 工具集

### 安装

```bash
sudo apt install bpfcc-tools linux-headers-$(uname -r)  # Debian/Ubuntu
sudo dnf install bcc-tools kernel-devel                   # Fedora/RHEL
```

### 常用工具

```bash
# === 进程与 CPU ===
sudo execsnoop-bpfcc              # 跟踪新进程执行
sudo runqlat-bpfcc                # 调度队列延迟直方图
sudo runqlen-bpfcc                # 调度队列长度
sudo cpudist-bpfcc                # CPU 时间片分布
sudo offcputime-bpfcc -p <PID> 5  # Off-CPU 分析（5秒）
sudo profile-bpfcc -F 99 30       # CPU 采样 30 秒

# === 磁盘 I/O ===
sudo biolatency-bpfcc             # 块 I/O 延迟直方图
sudo biosnoop-bpfcc               # 每次 I/O 详细信息
sudo biotop-bpfcc                 # 类似 top 的 I/O 视图
sudo ext4slower-bpfcc 1           # 慢 ext4 操作（>1ms）
sudo xfsslower-bpfcc 1            # 慢 xfs 操作（>1ms）
sudo fileslower-bpfcc 1           # 慢文件操作（>1ms）
sudo filetop-bpfcc                # 文件 I/O top

# === 网络 ===
sudo tcpconnect-bpfcc             # 跟踪 TCP 主动连接
sudo tcpaccept-bpfcc              # 跟踪 TCP 被动连接
sudo tcpretrans-bpfcc             # TCP 重传跟踪
sudo tcplife-bpfcc                # TCP 连接生命周期
sudo tcptop-bpfcc                 # TCP 吞吐量 top

# === 内存 ===
sudo cachestat-bpfcc 1            # 页缓存命中率（每秒）
sudo memleak-bpfcc -p <PID>       # 内存泄漏检测
sudo oomkill-bpfcc                # OOM Kill 追踪
sudo slabratetop-bpfcc            # Slab 分配速率 top

# === 文件系统 ===
sudo opensnoop-bpfcc              # 跟踪文件打开
sudo funccount-bpfcc 'vfs_*'      # 统计 VFS 函数调用
sudo filelife-bpfcc               # 文件创建到删除的生命周期
```

### BCC 工具速查表

| 工具 | 用途 | 典型场景 |
|------|------|---------|
| `execsnoop` | 新进程跟踪 | 发现异常进程创建 |
| `opensnoop` | 文件打开跟踪 | 找丢失的配置文件 |
| `biolatency` | I/O 延迟直方图 | 磁盘性能分析 |
| `biosnoop` | 每次 I/O 详情 | I/O 延迟尖刺定位 |
| `tcpconnect` | TCP 连接跟踪 | 网络延迟分析 |
| `tcpretrans` | TCP 重传 | 网络丢包诊断 |
| `tcplife` | TCP 生命周期 | 短连接问题 |
| `cachestat` | 缓存命中率 | 内存压力分析 |
| `runqlat` | 调度延迟 | CPU 饱和诊断 |
| `profile` | CPU 采样 | 函数级 CPU 分析 |
| `offcputime` | Off-CPU 分析 | I/O 等待/锁竞争 |
| `memleak` | 内存泄漏 | C/C++ 泄漏排查 |
| `oomkill` | OOM 追踪 | OOM 根因分析 |

---

## eBPF 程序类型

| 类型 | Hook 点 | 用途 | 示例 |
|------|---------|------|------|
| **kprobe/kretprobe** | 内核函数入口/返回 | 追踪内核函数 | 追踪 tcp_sendmsg |
| **uprobe/uretprobe** | 用户态函数入口/返回 | 追踪应用函数 | 追踪 malloc |
| **tracepoint** | 内核静态追踪点 | 稳定的内核事件 | sched:sched_switch |
| **raw_tracepoint** | 原始追踪点 | 低开销追踪 | 系统调用入口 |
| **XDP** | 网卡驱动层 | 高性能包处理 | DDoS 防护、负载均衡 |
| **TC** | 流量控制层 | 网络策略 | 包过滤、QoS |
| **cgroup** | cgroup 事件 | 容器级控制 | 网络/设备访问控制 |
| **socket_filter** | Socket 层 | 包过滤 | tcpdump 替代 |
| **perf_event** | 硬件/软件事件 | 性能计数器 | CPU cache miss |
| **LSM** | 安全模块钩子 | 安全策略 | 文件访问控制 |

### kprobe vs tracepoint

```bash
# kprobe：灵活但不稳定（内核升级可能变化）
sudo bpftrace -e 'kprobe:tcp_sendmsg { @[comm] = count(); }'

# tracepoint：稳定 API（推荐优先使用）
sudo bpftrace -e 'tracepoint:tcp:tcp_send_reset { @[comm] = count(); }'

# 列出所有可用追踪点
sudo bpftrace -l 'tracepoint:*' | wc -l        # 通常 2000+
sudo bpftrace -l 'kprobe:tcp_*' | head -20      # TCP 相关内核函数
```

---

## libbpf 与 CO-RE

### CO-RE（Compile Once, Run Everywhere）

CO-RE 解决了 eBPF 程序在不同内核版本间的可移植性问题。

```c
// 传统方式：需要内核头文件，每个内核版本重新编译
#include <linux/sched.h>

// CO-RE 方式：使用 BTF（BPF Type Format）
// 编译一次，运行在任何支持 BTF 的内核上
#include "vmlinux.h"  // 由 bpftool btf dump 生成
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_core_read.h>

SEC("kprobe/tcp_sendmsg")
int BPF_KPROBE(tcp_sendmsg, struct sock *sk, struct msghdr *msg, size_t size)
{
    // CO-RE 自动处理结构体偏移差异
    u16 family = BPF_CORE_READ(sk, __sk_common.skc_family);
    // ...
    return 0;
}
```

### libbpf-bootstrap 快速入门

```bash
# 克隆 libbpf-bootstrap
git clone https://github.com/libbpf/libbpf-bootstrap.git
cd libbpf-bootstrap/examples/c

# 编译示例
make minimal

# 运行
sudo ./minimal

# 检查内核是否支持 BTF
ls /sys/kernel/btf/vmlinux && echo "BTF supported" || echo "No BTF"

# 生成 vmlinux.h
bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h
```

---

## eBPF Map 类型

Map 是 eBPF 程序与用户态程序之间共享数据的核心机制。

| Map 类型 | 用途 | 特点 |
|----------|------|------|
| `BPF_MAP_TYPE_HASH` | 键值存储 | 通用哈希表 |
| `BPF_MAP_TYPE_ARRAY` | 固定大小数组 | 索引快速访问 |
| `BPF_MAP_TYPE_PERCPU_HASH` | 每 CPU 哈希表 | 无锁，高性能 |
| `BPF_MAP_TYPE_PERCPU_ARRAY` | 每 CPU 数组 | 无锁计数器 |
| `BPF_MAP_TYPE_LRU_HASH` | LRU 哈希表 | 自动淘汰旧条目 |
| `BPF_MAP_TYPE_RINGBUF` | 环形缓冲区 | 高效事件流（推荐） |
| `BPF_MAP_TYPE_PERF_EVENT_ARRAY` | 事件数组 | 传统事件流 |
| `BPF_MAP_TYPE_STACK_TRACE` | 堆栈追踪 | 调用栈采集 |
| `BPF_MAP_TYPE_LPM_TRIE` | 最长前缀匹配 | IP 路由表 |

```bash
# 查看系统中的 eBPF Map
sudo bpftool map list

# 查看 Map 内容
sudo bpftool map dump id <MAP_ID>
```

---

## 生产环境最佳实践

### 1. 性能开销控制

```bash
# ❌ 避免：高频追踪点 + 大量数据处理
sudo bpftrace -e 'kprobe:* { @[probe] = count(); }'  # 追踪所有内核函数！

# ✅ 推荐：精确追踪 + 过滤
sudo bpftrace -e 'kprobe:tcp_sendmsg /comm == "nginx"/ { @bytes = sum(arg2); }'

# 开销评估：
# - tracepoint: ~100ns/event
# - kprobe: ~200ns/event
# - uprobe: ~1-5μs/event（用户态切换开销）
```

### 2. 常用诊断流程

```bash
# 第一步：全局概览
sudo runqlat-bpfcc 10 1          # 10 秒调度延迟
sudo biolatency-bpfcc 10 1       # 10 秒 I/O 延迟
sudo cachestat-bpfcc 1 10        # 10 秒缓存命中率

# 第二步：定位进程
sudo profile-bpfcc -F 99 10      # CPU 采样 10 秒
sudo offcputime-bpfcc 10         # Off-CPU 10 秒

# 第三步：深入追踪
sudo funccount-bpfcc 'tcp_*' 10  # TCP 函数调用频率
sudo tcpretrans-bpfcc            # TCP 重传详情
```

### 3. 火焰图生成

```bash
# CPU 火焰图（使用 profile）
sudo profile-bpfcc -F 99 -f 30 > /tmp/cpu.folded
flamegraph.pl /tmp/cpu.folded > /tmp/cpu.svg

# Off-CPU 火焰图
sudo offcputime-bpfcc -f 30 > /tmp/offcpu.folded
flamegraph.pl --color=io /tmp/offcpu.folded > /tmp/offcpu.svg

# 使用 bpftrace 生成
sudo bpftrace -e 'profile:hz:99 { @[kstack] = count(); }' -c 'sleep 30' > /tmp/stacks.txt
```

### 4. 持续监控集成

```bash
# 与 Prometheus 集成（使用 ebpf_exporter）
# https://github.com/cloudflare/ebpf_exporter
# 将 eBPF 指标暴露为 Prometheus 格式

# 与 Grafana 集成
# 通过 ebpf_exporter → Prometheus → Grafana 可视化
```

---

## 安全约束与限制

### 内核要求

| 功能 | 最低内核版本 |
|------|:----------:|
| 基础 eBPF | 3.18 |
| kprobe | 4.1 |
| tracepoint | 4.7 |
| XDP | 4.8 |
| bpftrace | 4.9（推荐 5.0+） |
| BTF/CO-RE | 5.2 |
| BPF ring buffer | 5.8 |
| BPF LSM | 5.7 |

### 安全限制

```bash
# 检查 eBPF 权限
cat /proc/sys/kernel/unprivileged_bpf_disabled
# 0 = 非特权用户可用, 1 = 仅 root, 2 = 完全禁用

# 容器中使用 eBPF
# 需要以下 capabilities:
# - CAP_SYS_ADMIN（传统）
# - CAP_BPF + CAP_PERFMON（内核 5.8+，更细粒度）

# K8s Pod 中启用
# securityContext:
#   capabilities:
#     add: ["SYS_ADMIN"]  # 或 ["BPF", "PERFMON"]
#   privileged: false

# 验证器限制
# - 最大指令数：100 万条（内核 5.2+）
# - 最大栈大小：512 字节
# - 禁止无限循环（必须有界）
# - 禁止访问未初始化内存
```

### 注意事项

- 需要内核 >= 4.9（bpftrace 推荐 >= 5.0）
- 容器中需要 `--privileged` 或 `CAP_SYS_ADMIN` + `CAP_BPF`
- macOS 不支持 eBPF（用 dtrace 替代）
- WSL2 支持但可能需要自编译内核
- 生产环境建议使用 tracepoint 而非 kprobe（更稳定）
- 高频追踪点需评估性能开销
