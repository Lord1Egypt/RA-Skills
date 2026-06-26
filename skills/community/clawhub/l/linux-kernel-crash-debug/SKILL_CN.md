---
name: linux-kernel-crash-debug
version: 1.3.2
description: 使用 crash 工具和内存调试工具调试 Linux 内核崩溃。当用户提到 kernel crash、kernel panic、vmcore 分析、内核转储调试、crash utility、内核 oops 调试、分析内核崩溃转储文件、使用 crash 命令、定位内核问题根因、KASAN、Kprobes、Kmemleak、内存损坏、越界访问、释放后使用、内存泄漏检测时，使用此 skill。
metadata:
  openclaw:
    requires:
      bins:
        - crash
        - gdb
        - readelf
        - objdump
        - makedumpfile
        - kexec
        - kdumpctl
        - systemctl
        - journalctl
    homepage: https://github.com/crazyss/linux-kernel-crash-debug
---

# Linux Kernel Crash Debugging

本 skill 指导如何使用 crash 工具分析 Linux 内核崩溃转储。

## 安装

### Claude Code
```bash
claude skill install linux-kernel-crash-debug.skill
```

### OpenClaw
```bash
# 方式一：通过 ClawHub 安装
clawhub install linux-kernel-crash-debug

# 方式二：手动安装
mkdir -p ~/.openclaw/workspace/skills/linux-kernel-crash-debug
cp SKILL.md ~/.openclaw/workspace/skills/linux-kernel-crash-debug/
```

## 快速开始

### 启动会话

```bash
# 分析转储文件
crash vmlinux vmcore

# 调试运行中的系统
crash vmlinux

# 原始 RAM 转储
crash vmlinux ddr.bin --ram_start=0x80000000
```

### 核心调试流程

```
1. crash> sys              # 确认 panic 原因
2. crash> log              # 查看内核日志
3. crash> bt               # 分析调用栈
4. crash> struct <type>    # 检查数据结构
5. crash> kmem <addr>      # 内存分析
```

## 🤖 Agent Execution Directives (Agent 专用执行戒律)
如果您是使用本技能的 AI/Agent，**绝对不要尝试开启交互式的 `crash` 会话**（会导致沙盒阻塞和上下文溢出）。
1. 使用项目内自带的封套工具 `./scripts/agent-crash.sh`，它完美映射了下方的调试流程并自带长输出断路器：
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore triage` - 三合板基础环境探伤 (`sys`, `log`, `bt`)。
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore flow-oom` - 自动聚合提取内存 OOM Top 占用。
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore flow-deadlock` - 自动清洗空闲 CPU，仅抓取 UN 睡眠任务堆栈。
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore dis-regs <func> <pid>` - 获取崩溃反汇编与现场寄存器值的组合视图。
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore check-poison <addr>` - 特征码探测（检测 UAF、SLUB 等常见特征）。
2. **底层降级策略 (Fallback Strategy)**：如果上面的宏指令排查不出结果，请通过 wrapper 执行标准内核调试命令：`./scripts/agent-crash.sh -k vmlinux -c vmcore run "rd ffff8800..."`。
3. 如果您需要更高的专家视角，请查阅 `references/agentic-heuristics.md`（高阶内核黑客视角策略）。

## 前置要求

| 项目 | 要求 |
|------|------|
| **vmlinux** | 必须带 debug symbols (`CONFIG_DEBUG_INFO=y`) |
| **vmcore** | kdump/netdump/diskdump/ELF 格式 |
| **版本** | vmlinux 必须与 vmcore 内核版本完全匹配 |

获取 debuginfo：
```bash
# RHEL/CentOS
yum install kernel-debuginfo

# 自编译内核
make menuconfig  # 启用 CONFIG_DEBUG_INFO
```

## 核心命令速查

### 调试分析

| 命令 | 用途 | 示例 |
|------|------|------|
| `sys` | 系统信息/panic 原因 | `sys`, `sys -i` |
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

## 会话控制

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
| crash 命令 | `crash vmlinux vmcore` | `crash_arm64 ... -m ... vmlinux vmcore` |
| KASLR | VMCOREINFO 自动处理 | 必须传 `-m kaslr=<偏移>` |
| 虚拟地址位宽 | 固定 | 必须传 `-m vabits_actual=<位数>` |
| 物理基地址 | `phys_base`（VMCOREINFO）| 必须传 `-m phys_offset=<地址>` |
| VA-PA 偏移 | `__START_KERNEL_map` 固定映射 | 必须传 `-m kimage_voffset=<值>` |
| 帧指针 | RBP（常被 `-fomit-frame-pointer` 优化掉）| FP (x29) 显式保存 |
| 调用约定 | RDI/RSI/RDX/RCX/R8/R9 | X0-X7 |

> **完整的 ARM64 地址参数推导**，见 `references/arm64-crash-params.md`
> **kdump 端到端配置手册**，见 `references/kdump-setup-guide.md`

### ARM64 Crash 命令模板

```bash
crash_arm64 \
  -m vabits_actual=39 \
  -m phys_offset=0x80000000 \
  -m kimage_voffset=0xffffffc000000000 \
  -m kaslr=0x0 \
  vmlinux vmcore
```

> 默认 `kaslr=0` 表示 KASLR 关闭。可根据 `/proc/kallsyms` 或 VMCOREINFO 调整。

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

### 从栈回溯推导锁指针（ARM64 专用）

> **来源**：[Kernel panic 实验室 - Kernel panic 实战之读写锁推导](https://mp.weixin.qq.com/s/szDQ9wOJDwcWo2AStiikPw)

当任务阻塞在某个锁上时，可以通过读取栈中的 callee-saved 寄存器反推锁地址：

```
# 1. 从 bt 输出中找到 FP（帧指针，方括号中的值）
crash> bt
PID: 1234
#3 [fffffc09c4f3ab0] schedule_preempt_disable
#4 [fffffc09c4f3b30] rwsem_down_write_slowpath
#5 [fffffc09c4f3b90] down_write

# 2. 反汇编调用者，定位锁指针如何传入
crash> dis -xl down_write
    mov  x0, x19                # x0 = x19（锁指针）
    mov  w1, #0x2
    bl   rwsem_down_write_slowpath

# 3. 反汇编被调者，定位 x19 在哪里压栈
crash> dis -xl rwsem_down_write_slowpath
    stp  x20, x19, [sp, #176]   # x19 存在 sp+176

# 4. 从 FP 推算 SP：SP = FP - 0x60（来自 "add x29, sp, #0x60"）
#    rwsem_down_write_slowpath FP = 0xfffffc09c4f3b30
#    SP = 0xfffffc09c4f3b30 - 0x60 = 0xfffffc09c4f3ad0

# 5. 读 x19：SP + 176 = 0xfffffc09c4f3b88
crash> rd 0xfffffc09c4f3b88
    fffffc09c4f3b88:  fffff80f78b0b00    ← 这就是锁地址！

# 6. 检查锁
crash> struct rw_semaphore fffff80f78b0b00 -x
```

**原理**：AArch64 ABI 中 x19-x28 是 callee-saved，被调函数必须先压栈才能使用。从反汇编找到保存位置，就能在栈里读出原值。

> **x86_64 等价方案**：使用 RBP 链 + `bt -f`。注意 `-fomit-frame-pointer` 优化会导致此方法失败，此时改用 `bt -F` 或显式栈帧定位。

### 内存泄露三层诊断法

> **来源**：[Kernel panic 实验室 - Kernel driver 内存泄露问题排查指南](https://mp.weixin.qq.com/s/RER260p6MN5NmymYdyKn0g)

三条独立诊断路径：

```
# === 第一层：/proc 三件套（读运行系统或捕获信息）===
# MemAvailable 持续下降 + SUnreclaim 持续增加 → slab 内存泄露
cat /proc/meminfo
cat /proc/slabinfo
cat /proc/buddyinfo

# === 第二层：SLAB 专项（slub_debug）===
# 启动参数加：slub_debug=u,kmalloc-512
# 然后读：
cat /sys/kernel/debug/slab/kmalloc-512/alloc_traces
cat /sys/kernel/debug/slab/kmalloc-512/free_traces

# === 第三层：>8K 的大块分配（page_owner）===
# SUnreclaim 上涨但 slabinfo 平稳 → kmalloc > 8K 走 alloc_pages 路径
# 启用 CONFIG_PAGE_OWNER + bootargs 加 page_owner=on
# 然后：
echo 1 > /sys/kernel/debug/page_owner/enable
# 周期性抓 snapshot，对比：
./page_owner_sort --cull name,ator,stacktrace page_owner_begin.txt > begin.txt
./page_owner_sort --cull name,ator,stacktrace page_owner_end.txt   > end.txt
# 对比两份结果，增长的调用栈即为泄露

# === 备选：kmemleak ===
# CONFIG_DEBUG_KMEMLEAK + bootarg 加 kmemleak=on
echo scan > /sys/kernel/debug/kmemleak
cat /sys/kernel/debug/kmemleak
```

### 链式查询

```
crash> bt -f                  # 获取指针
crash> struct file.f_dentry <addr>
crash> struct dentry.d_inode <addr>
crash> struct inode.i_pipe <addr>
```

### 批量检查 Slab

```
crash> kmem -S inode_cache | grep counter | grep -v "= 1"
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
| `references/case-studies.md` | 详细调试案例：kernel BUG、死锁、OOM、NULL指针、栈溢出 |
| `references/kdump-setup-guide.md` | **新增** kdump 端到端配置（x86_64 + ARM64 双架构、crashkernel 语法、sysrq 触发） |
| `references/arm64-crash-params.md` | **新增** ARM64 专用 crash 地址参数（vabits_actual、phys_offset、kimage_voffset、kaslr） |
| `references/sources.md` | **新增** 完整的参考资料引用列表（含微信公众号、kernel.org、邮件列表） |

使用方式：
```
crash> help <command>        # 内置帮助
# 或在 Claude 中请求查看参考文件
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