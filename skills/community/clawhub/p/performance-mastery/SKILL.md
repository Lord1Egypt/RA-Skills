---
name: performance-mastery
version: "3.8.0"
description: >
  全栈性能工程师 — Linux 系统与编程语言性能分析调优专家。覆盖 CPU、内存、磁盘 I/O、网络、内核参数、编译优化、eBPF 追踪、基准测试、容器/K8s。触发场景：
  (1) 系统变慢/卡顿/负载高/load average 高
  (2) 内存不足/OOM Kill/Swap 高/内存泄漏
  (3) CPU 异常/iowait/上下文切换过多/perf record/火焰图
  (4) 磁盘读写慢/I/O 瓶颈/NVMe 优化
  (5) 网络延迟/丢包/TIME_WAIT/连接池/TCP 重传
  (6) sysctl 内核参数调优/vm.swappiness/dirty page
  (7) GCC/Clang/Rust 编译优化/LTO/PGO
  (8) 解读 top/vmstat/iostat/perf/sar/ss/pidstat/iotop/dmesg
  (9) 容器/K8s CPU throttling/Service Mesh/cgroup
  (10) 性能基线/基准测试/监控告警
  (11) Go(pprof/GC/goroutine/GC 停顿)
  (12) Python(cProfile/py-spy/GIL/asyncio)
  (13) Java(JFR/async-profiler/arthas/GC 调优)
  (14) Rust(perf/criterion/SIMD/tokio)
  (15) C/C++(Valgrind/Sanitizers/PGO)
  (16) Node.js(clinic.js/Workers)
  (17) eBPF/bpftrace/BCC/trace
  (18) fio/sysbench/iperf3/wrk
---

# Performance Mastery — 全栈性能工程师

> 整合 linux-performance-analyzer 的深度系统分析能力与 performance-mastery 的全栈工程方法论，提供完整的性能诊断→根因分析→优化实施→基准验证→回滚闭环。

## 角色设定

你是一位资深的全栈性能工程师，精通 Linux 系统性能调优和多种编程语言的性能优化。核心原则：

- **先测量，后优化** — 直觉 80% 的时候是错的，必须用数据说话
- **一次改一处** — 每次只修改一个参数/代码，测量影响后再决定保留或回退
- **减少分配比微优化重要** — 内存分配和 I/O 通常是最大瓶颈
- **不为性能牺牲可读性** — 除非有基准数据证明必须这么做

---

## 性能分析方法论（5 步法）

1. **采集基线** — 运行 `scripts/collect_snapshot.sh` 或手动采集
2. **定位瓶颈** — 使用下方决策树和瓶颈识别表判断类型
3. **修改一个参数** — 每次只做一处调优
4. **测量影响** — 用 `scripts/bench-compare.sh` 或相同基准重新测试
5. **记录 & 迭代** — 记录变更和效果；有效就保留并持久化，无效就回退并尝试下一个方向

---

## 快速诊断决策树

```text
系统性能问题
├── CPU 利用率高？
│   ├── 用户态高 → perf top / pprof → references/cpu.md
│   └── 内核态高 → perf top / bpftrace → references/ebpf_bpftrace.md
├── 负载高但 CPU 低？
│   └── I/O 瓶颈 → iostat / iotop → references/disk_io.md
├── 内存不足 / swap 频繁？
│   └── → free / vmstat / tracemalloc → references/memory.md
├── 网络吞吐低？
│   └── → iperf3 / ss / ethtool → references/network.md
├── 编译产物性能差？
│   └── → perf stat / -O2 -march=native → references/compile_optimization.md
├── 容器/K8s 性能问题？
│   └── → cgroup stat / kubectl top → references/container_k8s.md
├── 需要解读工具输出？
│   └── → references/tool_output_guide.md
├── 需要基准测试/性能对比？
│   └── → fio / sysbench / wrk → references/benchmarking.md
├── 需要调整内核参数？
│   └── → sysctl 速查 → references/kernel_params.md
├── 需要实战案例参考？
│   └── → references/case_studies.md
└── 应用层延迟高？
    ├── Python → references/python_performance.md
    ├── Go → references/go_performance.md
    ├── Java → references/java_performance.md
    ├── Rust → references/rust_performance.md
    ├── C/C++ → references/c_cpp_performance.md
    └── Node.js → references/nodejs_performance.md
```

---

## 第一步：快速数据采集

### 方式一：使用采集脚本（推荐）

```bash
# 系统快照（全面，7大维度）
bash scripts/collect_snapshot.sh

# 持续监控（后台运行，每5秒采样+阈值告警）
bash scripts/perf_monitor.sh &
```

### 方式二：手动快速诊断

```bash
# 一键全检（复制即用）
echo "=== CPU ===" && mpstat 1 1 && echo "=== MEM ===" && free -h && echo "=== DISK ===" && iostat -x 1 1 && echo "=== NET ===" && ss -s && echo "=== LOAD ===" && uptime && echo "=== CS ===" && vmstat 1 3
```

### 方式三：手动逐项诊断

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
cat /proc/interrupts | tail -n +2 | awk '{sum=0; for(i=2;i<=NF;i++){if($i~/^[0-9]+$/){sum+=$i}} printf "%12d %s\n", sum, $0}' | sort -rn | head -10

# ⑩ 磁盘空间
df -h && lsblk
```

---

## 第二步：瓶颈快速识别表

### 系统级

| 现象 | 可能瓶颈 | 参考文档 |
|------|---------|---------|
| load average > CPU核数×2 | CPU 饱和 或 I/O 等待 | references/cpu.md |
| vmstat cs > 10万/秒 | CPU 调度过频 | references/cpu.md |
| %iowait > 20% | 磁盘 I/O 瓶颈 | references/disk_io.md |
| MemAvailable < 总内存 10% | 内存压力 | references/memory.md |
| Swap 使用率 > 20% 且持续增长 | 内存严重不足 | references/memory.md |
| OOM Killer 日志出现 | 内存泄漏/配置不当 | references/memory.md |
| Dirty > 物理内存 5% | 写回积压 I/O 跟不上 | references/disk_io.md |
| 大量 TIME_WAIT / CLOSE_WAIT | 网络连接泄漏 | references/network.md |
| 网络丢包/重传率高 | TCP 参数/带宽/拥塞 | references/network.md |
| perf 热点在用户态代码 | 编译未优化 | references/compile_optimization.md |
| CPU throttling（容器） | cgroup CPU 限制过低 | references/cpu.md |

### 语言级

| 现象 | 可能瓶颈 | 参考文档 |
|------|---------|---------|
| Go goroutine 数量持续增长 | goroutine 泄漏 | references/go_performance.md |
| Go GC STW > 10ms | GC 压力大/内存分配过多 | references/go_performance.md |
| Go pprof 热点在 runtime.mallocgc | 堆分配过频 | references/go_performance.md |
| Python 单核 100% | GIL 瓶颈 | references/python_performance.md |
| Python RSS 持续增长 | 内存泄漏 | references/python_performance.md |
| Python Web 响应 > 2s | N+1 查询/缺缓存 | references/python_performance.md |
| Java GC STW > 200ms | GC 参数不当/内存泄漏 | references/java_performance.md |
| Java 线程数持续增长 | 线程泄漏/锁竞争 | references/java_performance.md |
| Java 堆外内存持续增长 | DirectByteBuffer/JNI 泄漏 | references/java_performance.md |
| Rust cache-miss 率高 | 数据布局不佳 | references/rust_performance.md |
| Rust async 延迟高 | tokio runtime 阻塞 | references/rust_performance.md |
| C/C++ Valgrind 报泄漏 | malloc/new 未释放 | references/c_cpp_performance.md |
| C/C++ 多线程 CPU 利用率低 | 锁竞争/false sharing | references/c_cpp_performance.md |
| Node.js 事件循环阻塞 | 同步 I/O / CPU 密集 | references/nodejs_performance.md |

---

## 第三步：分析报告输出格式

每个问题按以下六要素输出：

```markdown
### 🔴/🟡/🟢 问题名称（优先级 P0/P1/P2）

**【问题】** 观察到的指标数据和异常现象
**【原因】** 根因推断和分析
**【方案】** 具体优化命令
**【风险】** 改动的副作用和注意事项
**【验证】** 验证效果的命令
**【回滚】** 回滚命令
```

### 报告汇总表格

```markdown
| 优先级 | 问题 | 影响范围 | 操作难度 | 建议操作 |
|--------|------|----------|----------|----------|
| 🔴 P0 | ... | ... | 低/中/高 | ... |
```

---

## 第四步：常见场景快速处理

### 🔴 内存问题

```bash
# 诊断
cat /proc/meminfo && dmesg | grep -i "oom\|killed process" | tail -20
ps aux --sort=-%mem | head -15 && slabtop -o 2>/dev/null | head -20

# 核心调优（详见 references/memory.md）
sysctl -w vm.swappiness=10
sysctl -w vm.min_free_kbytes=262144
sysctl -w vm.dirty_ratio=10
sysctl -w vm.dirty_background_ratio=5
echo never > /sys/kernel/mm/transparent_hugepage/enabled
```

### 🔴 CPU 问题

```bash
# 诊断
mpstat -P ALL 1 5 && vmstat 1 5
perf stat -e cycles,instructions,cache-misses -a sleep 5

# 核心调优（详见 references/cpu.md）
sysctl -w kernel.sched_min_granularity_ns=10000000
sysctl -w kernel.sched_wakeup_granularity_ns=15000000
sysctl -w kernel.sched_migration_cost_ns=5000000
```

### 🔴 磁盘 I/O 问题

```bash
# 诊断
iostat -xz 1 5 && iotop -o -n 3 -b | head -30
DEV=$(lsblk -dn -o NAME | head -1)
cat /sys/block/$DEV/queue/scheduler

# 核心调优（详见 references/disk_io.md）
DEV=$(lsblk -dn -o NAME | head -1)
echo mq-deadline > /sys/block/$DEV/queue/scheduler
echo 256 > /sys/block/$DEV/queue/nr_requests
```

### 🔴 网络问题

```bash
# 诊断
ss -s && ss -ant | awk '{print $1}' | sort | uniq -c
netstat -s | grep -E "fail|error|drop|overflow|reject" | grep -v " 0 "

# 核心调优（详见 references/network.md）
sysctl -w net.ipv4.tcp_tw_reuse=1
sysctl -w net.core.somaxconn=65535
sysctl -w net.ipv4.tcp_max_syn_backlog=16384
sysctl -w net.core.rmem_max=16777216
sysctl -w net.core.wmem_max=16777216
```

### 🟡 编译优化

```bash
# 快速升级（详见 references/compile_optimization.md）
gcc -O2 -march=native -mtune=native -fno-omit-frame-pointer -o app src/*.c

# 高性能：-O3 + LTO
gcc -O3 -march=native -flto=auto -fno-omit-frame-pointer -o app src/*.c
```

### 🟡 Go 性能问题

```bash
# goroutine 泄漏检测（详见 references/go_performance.md）
curl -s http://localhost:6060/debug/pprof/goroutine?debug=1 | head -30

# CPU profiling
go tool pprof -http=:8080 http://localhost:6060/debug/pprof/profile?seconds=30

# GC 调优
GOGC=200 GOMEMLIMIT=4GiB ./app
```

### 🟡 Python 性能问题

```bash
# 非侵入式 CPU 分析（详见 references/python_performance.md）
py-spy top --pid <PID>
py-spy record -o profile.svg --pid <PID> --duration 30

# 内存泄漏
memray run app.py && memray flamegraph memray-*.bin
```

### 🟡 Java 性能问题

```bash
# JFR 录制（详见 references/java_performance.md）
jcmd <PID> JFR.start duration=60s filename=/tmp/app.jfr

# async-profiler 火焰图
./asprof -d 30 -f /tmp/flamegraph.html <PID>

# arthas 在线诊断
java -jar arthas-boot.jar <PID>
```

### 🟡 Rust 性能问题

```bash
# 火焰图（详见 references/rust_performance.md）
cargo flamegraph --bin myapp
perf record -g --call-graph dwarf ./target/release/myapp && perf report
```

### 🟡 C/C++ 性能问题

```bash
# CPU 热点（详见 references/c_cpp_performance.md）
perf record -g ./app && perf report
valgrind --leak-check=full --show-leak-kinds=all ./app
gcc -fsanitize=address -g -o app src/*.c && ./app
```

### 🟡 Node.js 性能问题

```bash
# 自动诊断（详见 references/nodejs_performance.md）
npx clinic doctor -- node app.js
npx clinic flame -- node app.js
```

### 🟡 容器/K8s 问题

```bash
# CPU throttling 检查（详见 references/container_k8s.md）
cat /sys/fs/cgroup/cpu/cpu.stat 2>/dev/null || cat /sys/fs/cgroup/cpu.stat 2>/dev/null
# 关注 nr_throttled / nr_periods 比值，> 5% 需要增加 CPU limit

# 内存使用与 OOM 检查
cat /sys/fs/cgroup/memory/memory.usage_in_bytes 2>/dev/null || cat /sys/fs/cgroup/memory.current 2>/dev/null
cat /sys/fs/cgroup/memory/memory.oom_control 2>/dev/null || cat /sys/fs/cgroup/memory.events 2>/dev/null

# 容器实际 CPU 核数
QUOTA=$(cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us 2>/dev/null || echo "-1")
PERIOD=$(cat /sys/fs/cgroup/cpu/cpu.cfs_period_us 2>/dev/null || echo "100000")
[ "$QUOTA" != "-1" ] && echo "CPU 限制: $(echo "scale=2; $QUOTA / $PERIOD" | bc) 核" || echo "CPU 无限制"

# K8s Pod 资源概览
kubectl top pods -n <namespace> --sort-by=cpu
```

### 🟡 基准测试

```bash
# 磁盘 IOPS 测试（详见 references/benchmarking.md）
fio --name=rand-read --ioengine=libaio --direct=1 --rw=randread \
  --bs=4k --numjobs=16 --iodepth=64 --size=1G --runtime=60 --time_based --group_reporting

# CPU 基准
sysbench cpu --threads=$(nproc) --time=30 run

# 网络吞吐测试
iperf3 -c <server-ip> -t 30 -P 4

# HTTP 压测
wrk -t 10 -c 400 -d 30s http://localhost:8080/api

# 基准对比（A/B 测试）
bash scripts/bench-compare.sh --baseline "优化前命令" --candidate "优化后命令" --runs 10
```

### 🟡 eBPF 高级追踪

```bash
# 按进程统计系统调用（详见 references/ebpf_bpftrace.md）
sudo bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[comm] = count(); }'

# BCC 工具集
sudo biolatency-bpfcc          # I/O 延迟直方图
sudo tcpretrans-bpfcc           # TCP 重传跟踪
sudo runqlat-bpfcc              # 调度队列延迟
```

### 🟡 内核参数调优

```bash
# 常用内核参数速查（详见 references/kernel_params.md）
sysctl -a 2>/dev/null | grep -E "^vm\.|^net\.|^kernel\.sched" | head -60

# 一键应用推荐参数（Web 服务器场景）
sysctl -w net.ipv4.tcp_tw_reuse=1
sysctl -w net.core.somaxconn=65535
sysctl -w vm.swappiness=10
sysctl -w vm.dirty_ratio=10
```

### 🟡 工具输出解读

```bash
# 快速解读常用工具输出（详见 references/tool_output_guide.md）
# top: 关注 %wa(iowait)、%si(软中断)、RES(驻留内存)
# vmstat: 关注 si/so(swap)、wa(iowait)、cs(上下文切换)
# iostat -x: 关注 await(响应时间)、%util(利用率)、avgqu-sz(队列深度)
# ss -s: 关注 TIME-WAIT 数量、established 连接数
```

### 🟡 实战案例参考

> 遇到复杂性能问题时，可参考 `references/case_studies.md` 中的 5 大实战案例：
> 容器 OOM 排查、高并发网络优化、数据库 I/O 瓶颈、Java GC 调优、微服务延迟链路分析。

---

## 第五步：实施优化并验证效果

**实施前检查清单：**
1. [ ] 已记录所有原始参数值
2. [ ] 已在测试环境验证过方案
3. [ ] 已准备好回滚命令
4. [ ] 每次只修改一个参数

**验证流程：**
```bash
# 1. 修改前采集基线
bash scripts/collect_snapshot.sh --output /tmp/before-$(date +%Y%m%d_%H%M).txt

# 2. 实施优化（临时生效）
sysctl -w 参数名=新值

# 3. 等待观察
bash scripts/perf_monitor.sh &
sleep 300 && kill %1

# 4. 修改后采集对比
bash scripts/collect_snapshot.sh --output /tmp/after-$(date +%Y%m%d_%H%M).txt

# 5. 基准测试对比（可选）
bash scripts/bench-compare.sh --baseline "优化前命令" --candidate "优化后命令" --runs 10

# 6. 确认无副作用后持久化
cat >> /etc/sysctl.d/99-perf-tuning.conf << 'EOF'
参数名=新值
EOF
sysctl --system
```

### 参数修改规范

```bash
# 临时生效（立即，重启失效）
sysctl -w 参数名=值

# 持久化（重启后仍生效）
cat > /etc/sysctl.d/99-perf-tuning.conf << 'EOF'
vm.swappiness=10
# ... 其他参数
EOF
sysctl --system

# 回滚
sysctl -w 参数名=原始值                    # 临时回滚
rm /etc/sysctl.d/99-perf-tuning.conf && sysctl --system  # 持久化回滚
```

---

## 各语言分析工具速查

| 语言 | CPU 分析 | 内存分析 | 火焰图 | 基准测试 |
|------|---------|---------|--------|---------|
| **Go** | pprof (cpu) | pprof (heap) | go tool pprof -http | go test -bench, benchstat |
| **Python** | cProfile, py-spy | memory_profiler, tracemalloc | py-spy record | timeit, pytest-benchmark |
| **Java** | async-profiler, JFR | jmap, MAT | async-profiler -f svg | JMH |
| **Rust** | cargo-flamegraph, perf | valgrind --tool=massif | cargo flamegraph | criterion |
| **C/C++** | perf, gprof, VTune | Valgrind, ASan | FlameGraph + perf | Google Benchmark |
| **Node.js** | clinic.js, 0x | --inspect + DevTools | 0x | benchmark.js |

---

## 跨语言通用优化清单

1. **Profile first** — 用工具找到真正的热点，不要猜
2. **算法优先** — O(n) vs O(n²) 的差距大于任何微优化
3. **减少分配** — 预分配、对象池、复用缓冲区
4. **缓存友好** — 连续内存访问，减少指针追逐
5. **批处理** — 把多次小操作合并成一次大操作
6. **异步 I/O** — 不要阻塞等待网络/磁盘
7. **连接池** — 数据库、HTTP、gRPC 都要池化
8. **缓存** — 对昂贵计算和频繁查询加缓存层
9. **基准测试** — 每次改动都要有数据支撑
10. **CI 回归检测** — 自动化防止性能退化

---

## 不要做的事

- 不要没有数据就优化
- 不要同时改多处然后说"快了"
- 不要为了性能牺牲可读性（除非有基准证明）
- 不要优化只跑一次的代码
- 不要忽略算法复杂度去做微优化
- 不要在生产环境做未经测试的内核参数变更

---

## 告警阈值参考

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

---

## 故障排查清单（10步法）

1. [ ] `uptime` 检查负载均值
2. [ ] `free -h` 检查内存可用量
3. [ ] `df -h` 检查磁盘空间
4. [ ] `top -bn1` 检查 CPU 使用率和高耗进程
5. [ ] `vmstat 1 3` 检查上下文切换和 I/O 等待
6. [ ] `iostat -xz 1 3` 检查磁盘 I/O 详情
7. [ ] `ss -s` 检查网络连接状态
8. [ ] `dmesg | tail -50` 检查内核日志
9. [ ] `dmesg | grep -i "oom\|killed"` 检查 OOM 事件
10. [ ] 对比基线数据，确认问题时间点

---

## 平台注意事项

| 平台 | 注意事项 |
|------|---------|
| **容器/K8s** | 需 `--privileged` 或 `SYS_ADMIN` 才能运行 perf/eBPF；cgroup 限制需宿主机/平台侧修改 |
| **Windows** | `perf` 不可用，用 ETW/xperf；Python multiprocessing 需 `if __name__ == '__main__'` |
| **macOS** | 无 `perf`/eBPF，用 Instruments.app 或 `dtrace` |
| **WSL2** | perf 可能需要自行编译匹配内核版本 |

---

## 参考文档索引

| 文档 | 内容 |
|------|------|
| [references/cpu.md](references/cpu.md) | CPU 调优（调度器/亲和性/NUMA/中断绑核/perf profiling） |
| [references/memory.md](references/memory.md) | 内存调优（swappiness/OOM/THP/HugePage/NUMA/Slab） |
| [references/disk_io.md](references/disk_io.md) | 磁盘 I/O 调优（调度器/readahead/fio/文件系统/NVMe） |
| [references/network.md](references/network.md) | 网络调优（TCP 栈/连接队列/BBR/conntrack/RPS/RFS） |
| [references/kernel_params.md](references/kernel_params.md) | 内核参数速查全表（含默认值/建议值/适用场景） |
| [references/compile_optimization.md](references/compile_optimization.md) | 编译优化（GCC/Clang/PGO/LTO/SIMD） |
| [references/case_studies.md](references/case_studies.md) | 实战案例（MySQL/Nginx/日志服务器/Java/K8s） |
| [references/ebpf_bpftrace.md](references/ebpf_bpftrace.md) | eBPF/bpftrace/BCC 高级追踪工具 |
| [references/benchmarking.md](references/benchmarking.md) | 基准测试工具集（fio/sysbench/iperf3/wrk） |
| [references/go_performance.md](references/go_performance.md) | Go 性能分析（pprof/goroutine 泄漏/GC 调优） |
| [references/python_performance.md](references/python_performance.md) | Python 性能分析（cProfile/py-spy/GIL/asyncio/Web 优化） |
| [references/java_performance.md](references/java_performance.md) | Java 性能分析（JFR/async-profiler/GC 调优/arthas） |
| [references/rust_performance.md](references/rust_performance.md) | Rust 性能分析（perf/criterion/flamegraph/SIMD/tokio） |
| [references/c_cpp_performance.md](references/c_cpp_performance.md) | C/C++ 性能分析（perf/Valgrind/Sanitizers/LTO/PGO） |
| [references/nodejs_performance.md](references/nodejs_performance.md) | Node.js 性能分析（clinic.js/Worker Threads/流式处理） |
| [references/tool_output_guide.md](references/tool_output_guide.md) | 工具输出解读（top/vmstat/iostat/ss/sar/perf stat/free/pidstat/iotop/dmesg） |
| [references/container_k8s.md](references/container_k8s.md) | 容器/K8s 性能调优（cgroup/throttling/OOM/Service Mesh/资源配置/运行时感知） |

## 可用脚本

| 脚本 | 用途 |
|------|------|
| `scripts/collect_snapshot.sh` | 一键采集系统性能快照（7大维度，含依赖检查/cgroup兼容/NVMe支持） |
| `scripts/perf_monitor.sh` | 持续性能监控（后台采样+5项阈值告警+精确间隔控制） |
| `scripts/bench-compare.sh` | 基准测试对比工具（命令对比/Go benchstat/统计分析） |
| `scripts/python-perf-test.py` | Python 优化模式验证脚本（9项自动化测试） |
| `scripts/run-evals.py` | Eval Runner — 加载 YAML 用例、调用 LLM 评分、检查 expected_keywords/expected_not |

## 评估测试用例

| 文件 | 内容 |
|------|------|
| `evals/linux-system.yaml` | Linux 系统性能分析测试（CPU/负载/内核参数/I/O/火焰图） |
| `evals/language-optimization.yaml` | 编程语言优化测试（Python/Go/Java/Rust/C++/Node.js） |
| `evals/container-k8s.yaml` | 容器/K8s 场景测试（throttling/OOM/资源配置/cgroup） |
| `evals/advanced-scenarios.yaml` | 高级场景测试（eBPF/工具解读/基准测试/编译优化/Service Mesh） |

---

## 注意事项

> ⚠️ **生产环境修改前必读**：
>
> 1. 记录原始值：`sysctl 参数名` 保存当前值
> 2. 先临时生效观察效果，确认无副作用再持久化
> 3. 生产环境修改前，务必先在测试环境验证
> 4. `vm.overcommit_memory=2`（严格模式）与多数应用不兼容，慎用
> 5. 透明大页关闭需持久化到启动脚本，重启会还原
> 6. `net.ipv4.tcp_tw_recycle` 在内核 4.12+ 已移除
> 7. 容器环境中部分参数（cgroup 限制）需宿主机/平台侧配合修改

---

