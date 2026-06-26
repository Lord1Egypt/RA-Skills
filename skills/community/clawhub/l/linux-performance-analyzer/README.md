# linux-performance-analyzer

> Linux 系统性能分析与调优全能专家 Skill，适用于 OpenClaw 智能助手平台。

---

## 📖 简介

**linux-performance-analyzer** 是一个覆盖 Linux 全维度性能诊断与调优的 OpenClaw Skill，整合了 CPU、内存、磁盘 I/O、网络、内核参数、编译优化、容器/K8s 等多个专项领域的最佳实践，提供从「发现问题」到「解决问题」的完整闭环能力。

### 核心能力

| 维度 | 能力描述 |
|------|---------|
| 🔥 CPU | 负载分析、上下文切换优化、NUMA调优、中断绑核、perf 火焰图 |
| 💾 内存 | OOM 排查与预防、Swap 调优、透明大页、HugePage、内存泄漏定位 |
| 💿 磁盘 I/O | 调度器选型、预读优化、fio 基准测试、SSD/NVMe 专项、RAID/LVM |
| 🌐 网络 | TCP 栈调优、TIME_WAIT 优化、BBR 拥塞控制、conntrack、高并发配置 |
| ⚙️ 内核参数 | sysctl 全参数速查（默认值/建议值/场景说明） |
| 🛠️ 编译优化 | GCC/Clang -O2/-O3、PGO、LTO、SIMD 向量化 |
| ☸️ 容器/K8s | CPU Throttling 排查、cgroup 资源限制、Pod QoS 调优 |
| 📊 实战案例 | MySQL/Nginx/日志服务器/Java/K8s 五大场景完整复盘 |

---

## 🗂️ 仓库结构

```
linux-performance-analyzer/
├── README.md                          # 本文档
├── SKILL.md                           # Skill 主文件（工作流 + 快速命令手册）
├── scripts/
│   ├── collect_snapshot.sh            # 一键系统全量快照采集脚本
│   └── perf_monitor.sh                # 持续性能监控 + 超阈值告警脚本
└── references/
    ├── cpu.md                         # CPU 调优深度参考手册
    ├── memory.md                      # 内存调优深度参考手册
    ├── disk_io.md                     # 磁盘 I/O 调优深度参考手册
    ├── network.md                     # 网络调优深度参考手册
    ├── kernel_params.md               # 内核参数速查全表
    ├── compile_optimization.md        # 编译优化指南（GCC/Clang/PGO/LTO）
    └── case_studies.md                # 实战案例分析（5 大场景）
```

---

## 🚀 快速开始

### 触发场景

在 OpenClaw 中，遇到以下问题时 Skill 会自动激活：

- 「系统变慢/卡顿/负载高/响应慢」
- 「内存不足 / OOM Kill / Swap 飙高」
- 「CPU 使用率异常 / iowait 高 / 上下文切换过多」
- 「磁盘读写慢 / I/O 瓶颈」
- 「网络延迟 / 丢包 / TIME_WAIT 过多 / 吞吐不足」
- 「帮我调一下内核参数」
- 「GCC/Clang/Rust 编译优化建议」
- 「解读一下这段 top/vmstat/iostat/perf/sar/ss 输出」
- 「容器 CPU Throttling / K8s 资源争抢」
- 「帮我建立性能基线」

### 诊断工作流（5 步闭环）

```
第一步：采集现场数据
        ↓
第二步：识别瓶颈类型（CPU / 内存 / I/O / 网络 / 编译）
        ↓
第三步：查阅对应参考文档深入分析
        ↓
第四步：输出标准化分析报告（问题 / 原因 / 方案 / 风险 / 验证 / 回滚）
        ↓
第五步：实施优化并验证效果
```

---

## 🛠️ 采集脚本使用说明

### collect_snapshot.sh — 全量快照采集

一键采集系统全维度性能数据，输出结构化报告，覆盖 7 大模块：

```bash
# 直接打印到终端
bash scripts/collect_snapshot.sh

# 保存到文件（推荐）
bash scripts/collect_snapshot.sh --output /tmp/perf-snapshot-20260325_1046.txt
```

采集内容：
- 系统基础信息（CPU型号、内存、磁盘）
- CPU 性能（负载、中断、软中断、NUMA拓扑）
- 内存性能（meminfo、Slab、透明大页、cgroup限制）
- 磁盘 I/O（iostat、调度器、队列深度）
- 网络性能（ss、ip、conntrack）
- 关键内核参数（vm/net/kernel/fs）
- 进程状态（D状态/僵尸/OOM历史）

### perf_monitor.sh — 持续监控 + 告警

后台运行，每 5 秒采样一次，超阈值自动记录告警日志：

```bash
# 前台运行（Ctrl+C 停止，自动打印告警汇总）
bash scripts/perf_monitor.sh

# 后台运行
bash scripts/perf_monitor.sh &

# 查看告警汇总报告
bash scripts/perf_monitor.sh --report
```

默认告警阈值：

| 指标 | 告警阈值 |
|------|---------|
| CPU 使用率 | > 80% |
| 内存可用率 | < 10% |
| load / CPU核数 | > 2.0x |
| iowait | > 20% |
| 上下文切换/秒 | > 100,000 |
| Swap 使用率 | > 30% |

---

## 📊 性能告警阈值参考

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

## 📚 参考文档说明

### [references/cpu.md](references/cpu.md)
CPU 全维度调优手册，包含：快速诊断、上下文切换优化、CPU 调速策略、进程调度、绑核（taskset/numactl）、中断绑核、perf 火焰图分析、容器 CPU Throttling 排查。

### [references/memory.md](references/memory.md)
内存全维度调优手册，包含：OOM Kill 处理与预防、swappiness 调优、透明大页 THP 关闭、HugePage 配置、脏页回写优化、Slab 缓存、内存泄漏排查（Valgrind/ASAN/jmap）、容器内存限制。

### [references/disk_io.md](references/disk_io.md)
磁盘 I/O 全维度调优手册，包含：iostat 指标解读、I/O 调度器选型（none/mq-deadline/bfq）、读预读优化、文件系统挂载选项（noatime/data=writeback）、fio 基准测试、NVMe 专项、RAID/LVM 条带优化、SMART 健康监控。

### [references/network.md](references/network.md)
网络全维度调优手册，包含：TCP 连接状态优化、缓冲区调优（BDP计算）、连接队列（somaxconn/backlog）、端口与文件描述符、BBR 拥塞控制、conntrack 管理、网卡多队列 RPS/RFS、延迟排查（mtr/curl timing）、高并发完整配置模板。

### [references/kernel_params.md](references/kernel_params.md)
全量内核参数速查表，分类涵盖：内存参数（vm.*）、CPU/调度参数（kernel.sched_*）、网络参数（net.core/net.ipv4）、I/O 参数、文件系统参数，每项均标注默认值、建议值和适用场景。附完整持久化配置模板和回滚方案。

### [references/compile_optimization.md](references/compile_optimization.md)
编译优化指南，包含：GCC/Clang 优化等级速查（-O0~-Ofast）、架构指令集优化（-march=native）、PGO 性能引导优化（三步流程）、LTO 链接时优化（ThinLTO）、SIMD 向量化（AVX2/AVX-512）、典型场景编译命令、效果验证方法。

### [references/case_studies.md](references/case_studies.md)
5 个典型实战案例完整复盘：
1. **MySQL OOM 优化** — swappiness + THP 关闭 + oom_score_adj
2. **Nginx 高并发连接** — TIME_WAIT + 端口范围 + 文件描述符
3. **日志服务器 I/O 瓶颈** — bfq 调度器 + 脏页回写 + 磁盘健康
4. **Java 内存泄漏** — GC 日志 + 堆转储 + G1 GC 调优
5. **K8s CPU Throttling** — cgroup cpu.stat + limits 调整 + Guaranteed QoS

---

## ⚠️ 注意事项

> **生产环境修改内核参数前必读：**
>
> 1. **先备份原始值**： 记录当前值
> 2. **先临时生效**： 方式临时修改，观察效果后再持久化
> 3. **测试环境验证**：生产环境修改前务必先在测试环境验证
> 4. **每次只改一个**：方便定位效果，出问题易回滚
> 5. **版本注意**： 在内核 4.12+ 已移除
> 6. **容器特殊性**：容器内 sysctl 修改需宿主机/平台侧配合

---

## 🔗 相关资源

- [Linux Performance](http://www.brendangregg.com/linuxperf.html) — Brendan Gregg 的 Linux 性能工具全图
- [perf Examples](http://www.brendangregg.com/perf.html) — perf 使用示例
- [Linux TCP Tuning](https://fasterdata.es.net/host-tuning/linux/) — Linux TCP 调优指南
- [sysctl Explorer](https://sysctl-explorer.net/) — 内核参数在线查询

---

## 📄 License

MIT License — 欢迎 fork 和贡献改进。