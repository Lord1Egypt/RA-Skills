---
name: linux-kernel-crash-debug
version: 1.5.2
description: 使用证据优先的 vmcore 分析、crash 工具和内存/并发调试工具定位 Linux 内核崩溃。当用户提到 kernel crash、kernel panic、vmcore、内核转储、oops、pstore/ramoops、soft/hard lockup、hung task、OOM、回归二分、mutex owner、ARM64 锁指针反推、KASAN、KFENCE、KCSAN、KMSAN、DMA API 调试、fail-nth、条件轨迹捕获、RCU stall、Lockdep、drgn、Kprobes、Kmemleak、内存损坏、越界、UAF、数据竞争、死锁或内存泄漏时，使用此 skill。
metadata:
  openclaw:
    requires:
      bins:
        - crash
    os:
      - linux
    homepage: https://github.com/crazyss/linux-kernel-crash-debug
---

# Linux Kernel Crash Debugging

本 skill 指导如何使用 crash 工具分析 Linux 内核崩溃转储。

## 安装

### Claude Code

从已核验的 release 归档解压全部 13 个运行时文件；脚本与参考文件须和
`SKILL.md` 一起安装。

```bash
mkdir -p ~/.claude/skills/linux-kernel-crash-debug
unzip linux-kernel-crash-debug.skill -d ~/.claude/skills/linux-kernel-crash-debug
```

### OpenClaw

仅在用户要求安装时执行以下步骤。这些命令仅放置技能文件，不授权启用服务、启动钩子或后台任务。
```bash
# 方式一：通过 ClawHub 安装
clawhub install linux-kernel-crash-debug

# 方式二：手动安装
mkdir -p ~/.openclaw/workspace/skills/linux-kernel-crash-debug
unzip linux-kernel-crash-debug.skill -d ~/.openclaw/workspace/skills/linux-kernel-crash-debug
```

新安装使用空目录；已有安装按明确的升级任务处理。只复制入口文件会缺少其
引用的脚本和参考资料。[Claude Code 技能位置](https://code.claude.com/docs/en/skills)。

## 快速开始

**语言选择**：按用户偏好回复。中文入口与中文参考资料为可选内容；需要英文时使用 `SKILL.md` 并翻译相关说明。引用标题保留原文用于溯源。

### 启动会话

以下为人工参考命令；Agent 使用下方离线封套。raw RAM 的加载方式须先按
`references/vmcore-format.md` 核对格式与工具版本。

```bash
# 分析转储文件
crash vmlinux vmcore

# 调试运行中的系统
crash vmlinux

# 原始 RAM 的加载方式取决于格式和工具版本，见上述参考。
```

### 核心调试流程

```console
0. 保存校验和、vmcore-dmesg、build ID、模块、config 和内核命令行
1. crash> sys              # 校验 release/build 与 panic 上下文
2. crash> log              # 找最早异常，而不是只看最后一次 panic
3. crash> bt / bt -a       # 对比 panic task 与所有活动 CPU
4. crash> mod              # 确认故障模块符号完整
5. crash> struct / kmem    # 验证具体的对象生命周期假设
6. 搜索上游，并验证 good/bad 内核后再判定回归
```

深入分析前先阅读 `references/evidence-first-workflow.md`。其中定义了证据
质量门控、故障路由、假设账本、工具升级规则和根因报告模板。没有直接证据
时，不要把 panic task、故障点、破坏点和根因当成同一件事。

完整证据链示例见 `references/case-studies.md` 的 Case 13–15：GRO 包头偏移
反推、InfiniBand 错误清理路径重复释放、文件系统 writeback/reclaim 死锁。
二分结果先视为候选触发变更，NMI 栈帧先视为被中断上下文，采集开销也可能
促成停顿；均需验证后才能归因。

怀疑 ARM64 指针出现单 bit 损坏时，按
[候选地址验证方法](references/evidence-first-workflow.md#511-arm64-single-bit-pointer-corruption-hypotheses)
和 [Case 16](references/case-studies.md#case-16-arm64-single-bit-pointer-corruption-hypothesis)
分析。恢复出合理指针并不等于证明 DDR 硬件故障。

### 首轮分析仍缺证据时

按缺失的证据选一种打法，不要同时打开所有 detector：

| 证据缺口 | 下一步打法 |
|---|---|
| 未初始化的值从哪里来 | [KMSAN 来源链追踪](references/debug-tools-guide.md#81-uninitialized-values-kmsan-origin-tracking) |
| 驱动是否误用了 DMA 映射 | [DMA API 生命周期核对](references/debug-tools-guide.md#82-device-corruption-dma-api-lifecycle-checks) |
| 哪次分配失败会破坏清理路径 | [按任务定点故障注入](references/debug-tools-guide.md#83-error-paths-deterministic-per-task-fault-injection) |
| 偶发症状之前发生了什么 | [条件触发飞行记录器](references/debug-tools-guide.md#84-rare-symptoms-conditional-flight-recorder) |
| 谁阻止了 RCU grace period 完成 | [同轮 GP 差分判读](references/evidence-first-workflow.md#521-rcu-stalls-compare-the-same-grace-period) |

这些方法补充现有越界/UAF、竞争、泄漏与锁序工具。先分析已有证据；需要活系统
实验时仍须遵守下方安全契约。参考文件为英文，按用户语言解释即可。

## 活系统安全契约

默认只做离线、只读分析。凡是使用 `sudo`、装卸模块、修改启动项或服务、
写 debugfs 或 `/proc/sys`、开启活系统 tracing、执行 SysRq，均视为修改活系统。

- 只有用户明确授权具体主机与具体动作，并确认处于实验环境或已批准维护窗口
  时才可执行；环境不明时，只完成只读检查并提供人工 runbook。
- 经授权开启 tracing 或 detector 前，记录基线，限制目标与持续时间，选择受控
  输出目录并给出清理/回滚命令；同一会话内完成清理并报告结果。
- 尽量不采集函数参数和业务 payload。trace 与 vmcore 可能包含凭据、路径、密钥
  和进程内存；未经明确批准和合规脱敏，不得上传或对外分享。
- Agent 绝不能主动触发 panic、重启、SysRq crash 或 `kdumpctl test`。只能说明
  前置条件，并把最终触发交给有授权的人，按已批准演练流程在具备控制台、备份、
  业务疏散以及恢复/回滚方案的前提下操作。

## 🤖 Agent Execution Directives (Agent 专用执行戒律)
如果您是使用本技能的 AI/Agent，**绝对不要尝试开启交互式的 `crash` 会话**（会导致沙盒阻塞和上下文溢出）。
1. 使用项目内自带的封套工具 `./scripts/agent-crash.sh`，仅用非 root 账号分析离线普通文件。工具强制执行受限命令白名单，并截断显示输出：
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore triage` - 输出 `sys`、高信号日志索引、panic/全 CPU 栈和模块清单。
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore flow-oom` - 自动聚合提取内存 OOM Top 占用。
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore flow-deadlock` - 自动清洗空闲 CPU，仅抓取 UN 睡眠任务堆栈。
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore dis-regs <func> <pid>` - 组合查看反汇编与栈帧数据；寄存器值仍须由现场证据确认。
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore check-poison <addr>` - 查找可能的 poison 数据；匹配结果不是 UAF 诊断。
2. **受限底层操作**：宏不足时可用 `./scripts/agent-crash.sh -k vmlinux -c vmcore read-memory ffff880123456780 64`、`backtrace <pid>` 或 `disassemble <symbol>`。已移除 `run`。必须同时指定两个输入文件；工具拒绝实时 `/proc`、`/sys`、`/dev` 输入、root 执行以及当前目录/用户目录的 `.gdbinit`，并禁用启动 `.crashrc`。不开放任意 crash/GDB 命令、shell 转义、管道、重定向、命令文件或扩展加载。内存读取限定为 1..256 个字。
   对 vmcore 和采集输出实施访问控制。在隔离分析环境中使用可信已安装的 `crash`；封套不是操作系统沙盒，也不能防御畸形转储/符号文件触发的解析器漏洞。不支持的查询应报告证据缺口，将明确的离线查询交给有授权的人，不得绕过封套。
3. 如果您需要更高的专家视角，请查阅 `references/agentic-heuristics.md`（高阶内核黑客视角策略）。
4. 遵循 `references/evidence-first-workflow.md`：报告符号/转储质量，定位最早
   异常，保留竞争假设，并为结论给出置信度与证伪方法。

## 前置要求

| 项目 | 要求 |
|------|------|
| **vmlinux** | 必须带 debug symbols (`CONFIG_DEBUG_INFO=y`) |
| **vmcore** | kdump/netdump/diskdump/ELF 格式 |
| **版本** | vmlinux 必须与 vmcore 内核版本完全匹配 |

软件安装会改变主机；仅在获得具体主机和软件包的明确授权后执行。优先使用已安装工具，离线转储分析使用非 root 账号。按发行版安装工具与匹配的 debuginfo：

示例中的 `uname -r` 指当前主机；分析其他主机或启动的转储时，须改用转储
对应的内核 release 与 build 查询符号，不能安装分析机当前内核的符号来代替。

```bash
# RHEL / CentOS / Rocky / AlmaLinux
sudo dnf install crash gdb binutils makedumpfile kexec-tools
sudo dnf debuginfo-install kernel-$(uname -r)

# Debian / Ubuntu
sudo apt install crash kdump-tools kexec-tools gdb binutils makedumpfile
apt-cache search --names-only "linux-image-$(uname -r).*(dbg|dbgsym)"

# SLES / openSUSE
sudo zypper install crash kexec-tools makedumpfile
sudo zypper install yast2-kdump
zypper se -s 'kernel*debug*'

# 自编译内核
make menuconfig  # 启用 CONFIG_DEBUG_INFO
```

ClawHub 元数据只把所有路径都需要的 `crash` 声明为硬依赖。`kdumpctl`
（RHEL 系）、`kdump-config`（Debian 系）、YaST 和其他分析工具按发行版与任务
安装，不能作为跨发行版的全局必需命令。

## 核心命令速查

### 调试分析

| 命令 | 用途 | 示例 |
|------|------|------|
| `sys` | 系统信息/panic 原因；`-i` 显示 DMI | `sys`, `sys -i` |
| `log` | 内核消息缓冲区 | `log`, `log \| tail` |
| `bt` | 调用栈回溯 | `bt`, `bt -a`, `bt -f` |
| `struct` | 结构体查看 | `struct task_struct <addr>` |
| `p/px/pd` | 打印变量 | `p jiffies`, `px current` |
| `kmem` | 内存分析 | `kmem -i`, `kmem -S <cache>` |

### 任务和进程

| 命令 | 用途 | 示例 |
|------|------|------|
| `ps` | 进程列表 | `ps`, `ps -m \| grep UN` |
| `set` | 切换上下文 | `set <pid>`, `set -p` |
| `foreach` | 批量任务操作 | `foreach bt`, `foreach UN bt` |
| `task` | task_struct 内容 | `task <pid>` |
| `files` | 打开的文件 | `files <pid>` |

### 内存操作

| 命令 | 用途 | 示例 |
|------|------|------|
| `rd` | 读取内存 | `rd <addr>`, `rd -p <phys>` |
| `search` | 搜索内存 | `search -k deadbeef` |
| `vtop` | 地址翻译 | `vtop <addr>` |
| `list` | 遍历链表 | `list task_struct.tasks -h <addr>` |

## bt 命令详解

最重要的调试命令：

```
crash> bt              # 当前任务调用栈
crash> bt -a           # 所有 CPU 活动任务
crash> bt -f           # 展开栈帧原始数据
crash> bt -F           # 符号化栈帧数据
crash> bt -l           # 显示源文件和行号
crash> bt -e           # 搜索异常帧
crash> bt -v           # 检查栈溢出
crash> bt -R <sym>     # 仅显示引用该符号的栈
crash> bt <pid>        # 指定进程
```

## 上下文管理

Crash 会话有一个"当前上下文"，影响 `bt`, `files`, `vm` 等命令：

```
crash> set              # 查看当前上下文
crash> set <pid>        # 切换到指定 PID
crash> set <task_addr>  # 切换到任务地址
crash> set -p           # 恢复到 panic 任务
```

## 会话控制（人工参考）

以下解释器功能仅供有授权的人在可信离线会话中使用。Agent 必须使用上面的封套，不得降级调用 GDB 直通、重定向或命令文件。人工使用前审核命令文件，并保护输出路径。

```
# 输出控制
crash> set scroll off   # 禁用分页
crash> sf               # scroll off 别名

# 输出重定向
crash> foreach bt > bt.all

# GDB 直通
crash> gdb bt           # 单次调用 gdb
crash> set gdb on       # 进入 gdb 模式
(gdb) info registers
(gdb) set gdb off

# 从文件读取命令
crash> < commands.txt
```

## ARM64 / x86_64 快速参考

### 两种架构在 crash 分析中的差异

| 维度 | x86_64 | ARM64 |
|------|--------|-------|
| crash 命令 | `crash vmlinux vmcore` | 先用 `crash vmlinux vmcore`，恢复场景再加 `-m` |
| KASLR | 通常由 VMCOREINFO 自动处理 | 通常自动处理；显式 `--kaslr=<偏移>` 须核实工具的 ARM64 支持 |
| 虚拟地址位宽 | 对当前构建固定 | VMCOREINFO 优先；`-m vabits_actual=<位数>` 是回退 |
| 物理基地址 | `phys_base`（VMCOREINFO）| VMCOREINFO 优先；`-m phys_offset=<地址>` 是回退 |
| VA-PA 偏移 | `__START_KERNEL_map` 固定映射 | VMCOREINFO 优先；`-m kimage_voffset=<值>` 是回退 |
| 帧指针 | RBP（常被 `-fomit-frame-pointer` 优化掉）| FP (x29) 显式保存 |
| 调用约定 | RDI/RSI/RDX/RCX/R8/R9 | X0-X7 |

> **完整的 ARM64 地址参数推导**，见 `references/arm64-crash-params.md`
> **kdump 端到端配置手册**，见 `references/kdump-setup-guide.md`

### ARM64 raw/元数据损坏转储的回退模板

```bash
crash_arm64 \
  -m vabits_actual=39 \
  -m phys_offset=0x80000000 \
  -m kimage_voffset=0xffffffc000000000 \
  --kaslr=0x0 \
  vmlinux vmcore
```

> 首先尝试 `crash vmlinux vmcore`。仅在 VMCOREINFO 缺失/损坏或输入为 raw
> RAM 时显式传值，并核实所用工具对 ARM64 `--kaslr` 的支持。零偏移必须由
> 本次启动的证据确认，不能默认假设，更不能复用另一次启动的参数。
> `-m kaslr` 不是上游 ARM64 支持的覆盖参数。

## 典型调试场景

### kernel BUG 定位

```
crash> sys                    # 确认 panic
crash> log | tail -50         # 查看日志
crash> bt                     # 调用栈
crash> bt -f                  # 展开栈帧获取参数
crash> struct <type> <addr>   # 检查数据结构
```

### 死锁分析

```
crash> bt -a                  # 所有 CPU 调用栈
crash> ps -m | grep UN        # 不可中断睡眠进程
crash> foreach UN bt          # 查看等待原因
crash> struct mutex <addr>    # 检查锁状态
```

### 内存问题

```
crash> kmem -i                # 内存统计
crash> kmem -S <cache>        # 检查 slab
crash> vm <pid>               # 进程内存映射
crash> search -k <pattern>    # 搜索内存
```

### 栈溢出

```
crash> bt -v                  # 检查栈溢出
crash> bt -r                  # 原始栈数据
```

## 高级技巧

### 从汇编和栈帧恢复锁指针与 mutex owner（ARM64）

> **来源**：[mutex lock 指针定位](https://mp.weixin.qq.com/s/HueZ8rFiOeZ1cwZK1XPHww)与[读写锁推导](https://mp.weixin.qq.com/s/szDQ9wOJDwcWo2AStiikPw)，Kernel Panic Lab。

任务阻塞在 `mutex_lock()` 或 rwsem 慢路径时，先在调用点追踪 ARM64 第一个参数 `x0`：

```
# 路径一：直接构造全局锁地址
    adrp x0, 0xffffffc00ac1e000
    add  x0, x0, #0x7f0         # lock = 页基址 + 页内偏移
    bl   mutex_lock

# 路径二：调用者通过 callee-saved 寄存器传参
    mov  x0, x19                # 锁指针就是栈中保存的 x19
    bl   mutex_lock
# 从实际反汇编找到 "add x29, sp, #N" 和 "stp/str ..., x19, [sp,#M]"，
# 由 FP 反推 SP，再用 rd 读取 x19 对应的栈槽。

crash> struct mutex <lock_addr> -x
# 常见内核的 mutex.owner 低 3 位是状态标志：
# owner_task = owner.counter & ~0x7
crash> struct task_struct <owner_task>
crash> bt <owner_pid>
```

`stp x20, x19, [sp,#32]` 把 `x20` 保存到 `sp+32`，把 `x19` 保存到 `sp+40`。不要照搬示例偏移；必须使用 vmcore 匹配的 `vmlinux` 重新推导，并核对当前内核的 mutex 布局和 owner flag 定义。

> FP/SP 精确计算、`stp` 槽位顺序、owner mask 和失败检查见 `references/arm64-lock-analysis.md`；完整 rwsem 案例见 `references/case-studies.md` Case 11。

> **x86_64 等价方案**：结合匹配反汇编与 unwinder 保存的栈状态。`bt -f`
> 显示栈帧数据，`bt -F` 对其符号化；都不能恢复已被优化掉的参数或缺失的
> 寄存器。手工遍历 RBP 链要求保留帧指针，否则需要工具支持的展开元数据。

### 内存泄露三层诊断法

> **来源**：[Kernel panic 实验室 - Kernel driver 内存泄露问题排查指南](https://mp.weixin.qq.com/s/RER260p6MN5NmymYdyKn0g)

三条独立诊断路径：

第一条路径只读；启用 `page_owner` 或写 kmemleak 控制接口会改变活内核状态，
必须遵循上面的安全契约。清空 detector 状态前先保存当前输出。

```
# === 第一层：/proc 三件套（读运行系统或捕获信息）===
# MemAvailable 持续下降且 SUnreclaim 增加提示 slab 增长，仍需验证保留原因。
cat /proc/meminfo
cat /proc/slabinfo
cat /proc/buddyinfo

# === 第二层：SLAB 专项（slub_debug）===
# 启动参数加：slub_debug=u,kmalloc-512
# 然后读：
cat /sys/kernel/debug/slab/kmalloc-512/alloc_traces
cat /sys/kernel/debug/slab/kmalloc-512/free_traces

# === 第三层：slab 增长不能解释的 page 分配（page_owner）===
# 大块 kmalloc 可绕过 slab，阈值取决于 PAGE_SIZE 与具体构建。
# 启用 CONFIG_PAGE_OWNER + bootargs 加 page_owner=on
# 如果 page_owner 尚未启用，使用已批准的维护 runbook；
# 不要在自动分诊过程中临时开启。
# 周期性抓 snapshot，对比：
./page_owner_sort --cull name,ator,stacktrace page_owner_begin.txt begin.txt
./page_owner_sort --cull name,ator,stacktrace page_owner_end.txt end.txt
# 对比相同工作负载阶段的保留分配；增长是线索，不能单独证明泄漏。

# === 备选：kmemleak ===
# CONFIG_DEBUG_KMEMLEAK + bootarg 加 kmemleak=on
echo scan > /sys/kernel/debug/kmemleak
cat /sys/kernel/debug/kmemleak
```

### 链式查询

```
crash> bt -f                  # 结合匹配反汇编恢复候选指针
crash> struct file.f_path.dentry <addr>
crash> struct dentry.d_inode <addr>
crash> struct inode.i_pipe <addr>
```

### 批量检查 Slab

```
crash> kmem -S inode_cache     # 查看 slab 元数据，不是验证 inode 引用计数
```

### 遍历内核链表

```
crash> list task_struct.tasks -s task_struct.pid -h <start>
crash> list -h <addr> -s dentry.d_name.name
```

## 扩展参考

详细信息请查阅以下参考文件：

| 文件 | 内容 |
|------|------|
| `references/advanced-commands.md` | 高级命令详解：list, rd, search, vtop, kmem, foreach |
| `references/vmcore-format.md` | vmcore 文件格式、ELF 结构、VMCOREINFO |
| `references/case-studies.md` | 调试案例，含有来源的 GRO 偏移、InfiniBand 重复释放、writeback/reclaim、ARM64 单 bit 指针损坏证据链（Case 13–16） |
| `references/debug-tools-guide.md` | 工具选择；KMSAN 来源链、DMA 生命周期、按任务故障注入与条件轨迹捕获（§8） |
| `references/kdump-setup-guide.md` | **新增** kdump 端到端配置（x86_64 + ARM64 双架构、crashkernel 语法、sysrq 触发） |
| `references/arm64-crash-params.md` | **新增** ARM64 专用 crash 地址参数（vabits_actual、phys_offset、kimage_voffset、kaslr） |
| `references/arm64-lock-analysis.md` | ARM64 mutex/rwsem 锁指针的汇编与栈恢复，以及 mutex owner 解码 |
| `references/evidence-first-workflow.md` | **新增** 证据门控、时间线、故障路由、工具升级、回归验证和根因报告模板 |
| `references/sources.md` | **新增** 完整的参考资料引用列表（含微信公众号、kernel.org、邮件列表） |

使用方式：
```
crash> help <command>        # 内置帮助
# 或请所用 agent 查看参考文件
```

## 常见错误

```
crash: vmlinux and vmcore do not match!
# → 确保 vmlinux 版本与 vmcore 完全匹配

crash: cannot find booted kernel
# → 明确指定 vmlinux 路径

crash: cannot resolve symbol
# → 检查 vmlinux 是否带 debug symbols
```

## 注意事项

1. **版本匹配**: vmlinux 必须与 vmcore 内核版本完全匹配
2. **调试信息**: 必须使用带 debug symbols 的 vmlinux
3. **上下文意识**: `bt`, `files`, `vm` 等命令受当前上下文影响
4. **活系统修改**: `wr` 命令会修改运行中的内核，极其危险
5. **Tracing 与 detector**: 必须明确授权、限制采集范围和时间，并在同一会话清理
6. **主动 panic**: 仅限有控制台和恢复方案的人工批准演练，Agent 不得执行

## 资源

- [Crash Utility Whitepaper](https://crash-utility.github.io/crash_whitepaper.html)
- [Crash Utility Documentation](https://crash-utility.github.io/)
- [Crash Help Pages](https://crash-utility.github.io/help_pages/)

## 贡献

这是一个开源项目，欢迎贡献！

- **GitHub 仓库**: https://github.com/crazyss/linux-kernel-crash-debug
- **报告问题**: [GitHub Issues](https://github.com/crazyss/linux-kernel-crash-debug/issues)
- **提交 PR**: 欢迎提交 Pull Request，包括 bug 修复、新功能或文档改进

详见 [CONTRIBUTING.md](https://github.com/crazyss/linux-kernel-crash-debug/blob/main/CONTRIBUTING.md)。
