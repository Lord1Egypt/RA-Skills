---
name: linux-kernel-crash-debug
version: 1.3.2
description: Debug Linux kernel crashes using the crash utility and memory debugging tools. Use when users mention kernel crash, kernel panic, vmcore analysis, kernel dump debugging, crash utility, kernel oops debugging, analyzing kernel crash dump files, using crash commands, locating root causes of kernel issues, KASAN, Kprobes, Kmemleak, memory corruption, out-of-bounds access, use-after-free, memory leak detection.
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

This skill guides you through analyzing Linux kernel crash dumps using the crash utility.

## Installation

### Claude Code
```bash
claude skill install linux-kernel-crash-debug.skill
```

### OpenClaw
```bash
# Method 1: Install via ClawHub
clawhub install linux-kernel-crash-debug

# Method 2: Manual installation
mkdir -p ~/.openclaw/workspace/skills/linux-kernel-crash-debug
cp SKILL.md ~/.openclaw/workspace/skills/linux-kernel-crash-debug/
```

## Quick Start

### Starting a Session

```bash
# Analyze a dump file
crash vmlinux vmcore

# Debug a running system
crash vmlinux

# Raw RAM dump
crash vmlinux ddr.bin --ram_start=0x80000000
```

### Core Debugging Workflow

```console
1. crash> sys              # Confirm panic reason
2. crash> log              # View kernel log
3. crash> bt               # Analyze call stack
4. crash> struct <type>    # Inspect data structures
5. crash> kmem <addr>      # Memory analysis
```

## 🤖 Agent Execution Directives
If you are an AI/Agent using this skill, **do not invoke `crash` interactively** as it will block your subshell.
1. Use the bundled wrapper `./scripts/agent-crash.sh` which maps precisely to the workflows below but safely truncates outputs:
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore triage` - Safely runs initial `sys`, `log`, and `bt`.
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore flow-oom` - Top 15 memory checks.
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore flow-deadlock` - Pulls UN task stacks.
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore dis-regs <func> <pid>` - Assembly regression.
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore check-poison <addr>` - Pattern match memory poisons.
2. **Fallback Strategy**: If macros don't solve the issue, fall back to basic primitives manually: `./scripts/agent-crash.sh -k vmlinux -c vmcore run "rd ffff880123456780"`.
3. Check `references/agentic-heuristics.md` for extended expert methodologies.

## Prerequisites

| Item | Requirement |
|------|-------------|
| **vmlinux** | Must have debug symbols (`CONFIG_DEBUG_INFO=y`) |
| **vmcore** | kdump/netdump/diskdump/ELF format |
| **Version** | vmlinux must exactly match the vmcore kernel version |

### Package Installation

#### Anolis OS / Alibaba Cloud Linux

```bash
# Install crash utility
sudo dnf install crash

# Install kernel debuginfo (match your kernel version)
sudo dnf install kernel-debuginfo-$(uname -r)

# Install additional analysis tools
sudo dnf install gdb readelf objdump makedumpfile

# Optional: Install kernel-devel for source code reference
sudo dnf install kernel-devel-$(uname -r)
```

#### RHEL / CentOS / Rocky / AlmaLinux

```bash
sudo dnf install crash kernel-debuginfo-$(uname -r)
sudo dnf install gdb binutils makedumpfile
```

#### Ubuntu / Debian

```bash
sudo apt install crash linux-crashdump gdb binutils makedumpfile
sudo apt install linux-image-$(uname -r)-dbgsym
```

### Self-compiled Kernel

```bash
# Enable debug symbols in kernel config
make menuconfig  # Enable CONFIG_DEBUG_INFO, CONFIG_DEBUG_INFO_REDUCED=n

# Or set directly
scripts/config --enable CONFIG_DEBUG_INFO
scripts/config --enable CONFIG_DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT
```

### Verify Installation

```bash
# Check crash version
crash --version

# Verify debuginfo matches kernel
crash /usr/lib/debug/lib/modules/$(uname -r)/vmlinux /proc/kcore
```

## Core Command Reference

### Debugging Analysis

| Command | Purpose | Example |
|---------|---------|---------|
| `sys` | System info/panic reason | `sys`, `sys -i` |
| `log` | Kernel message buffer | `log`, `log \| tail` |
| `bt` | Stack backtrace | `bt`, `bt -a`, `bt -f` |
| `struct` | View structures | `struct task_struct <addr>` |
| `p/px/pd` | Print variables | `p jiffies`, `px current` |
| `kmem` | Memory analysis | `kmem -i`, `kmem -S <cache>` |

### Tasks and Processes

| Command | Purpose | Example |
|---------|---------|---------|
| `ps` | Process list | `ps`, `ps -m \| grep UN` |
| `set` | Switch context | `set <pid>`, `set -p` |
| `foreach` | Batch task operations | `foreach bt`, `foreach UN bt` |
| `task` | task_struct contents | `task <pid>` |
| `files` | Open files | `files <pid>` |

### Memory Operations

| Command | Purpose | Example |
|---------|---------|---------|
| `rd` | Read memory | `rd <addr>`, `rd -p <phys>` |
| `search` | Search memory | `search -k deadbeef` |
| `vtop` | Address translation | `vtop <addr>` |
| `list` | Traverse linked lists | `list task_struct.tasks -h <addr>` |

## bt Command Details

The most important debugging command:

```console
crash> bt              # Current task stack
crash> bt -a           # All CPU active tasks
crash> bt -f           # Expand stack frame raw data
crash> bt -F           # Symbolic stack frame data
crash> bt -l           # Show source file and line number
crash> bt -e           # Search for exception frames
crash> bt -v           # Check stack overflow
crash> bt -R <sym>     # Only show stacks referencing symbol
crash> bt <pid>        # Specific process
```

## Context Management

Crash session has a "current context" affecting `bt`, `files`, `vm` commands:

```console
crash> set              # View current context
crash> set <pid>        # Switch to specified PID
crash> set <task_addr>  # Switch to task address
crash> set -p           # Restore to panic task
```

## Session Control

```console
# Output control
crash> set scroll off   # Disable pagination
crash> sf               # Alias for scroll off

# Output redirection
crash> foreach bt > bt.all

# GDB passthrough
crash> gdb bt           # Single gdb invocation
crash> set gdb on       # Enter gdb mode
(gdb) info registers
(gdb) set gdb off

# Read commands from file
crash> < commands.txt
```

## ARM64 / x86_64 Quick Reference

### Architecture Differences in crash Analysis

| Aspect | x86_64 | ARM64 |
|--------|--------|-------|
| crash command | `crash vmlinux vmcore` | `crash_arm64 ... -m ... vmlinux vmcore` |
| KASLR | VMCOREINFO auto-handled | Must pass `-m kaslr=<offset>` |
| Virtual address bits | fixed | Must pass `-m vabits_actual=<N>` |
| Physical base | `phys_base` from VMCOREINFO | Must pass `-m phys_offset=<addr>` |
| VA-PA offset | `__START_KERNEL_map` | Must pass `-m kimage_voffset=<val>` |
| Frame pointer | RBP (often optimized away) | FP (x29) explicit |
| Calling convention | RDI/RSI/RDX/RCX/R8/R9 | X0-X7 |

> **For complete ARM64 address parameter derivation**, see `references/arm64-crash-params.md`.
> **For kdump end-to-end setup**, see `references/kdump-setup-guide.md`.

### ARM64 Crash Command Template

```bash
crash_arm64 \
  -m vabits_actual=39 \
  -m phys_offset=0x80000000 \
  -m kimage_voffset=0xffffffc000000000 \
  -m kaslr=0x0 \
  vmlinux vmcore
```

> Default kaslr=0 means KASLR disabled. Adjust based on `/proc/kallsyms` or VMCOREINFO.

## Typical Debugging Scenarios

### Kernel BUG Location

```console
crash> sys                    # Confirm panic
crash> log | tail -50         # View logs
crash> bt                     # Call stack
crash> bt -f                  # Expand frames for parameters
crash> struct <type> <addr>   # Inspect data structures
```

### Deadlock Analysis

```console
crash> bt -a                  # All CPU call stacks
crash> ps -m | grep UN        # Uninterruptible processes
crash> foreach UN bt          # View waiting reasons
crash> struct mutex <addr>    # Inspect lock state
```

### Memory Issues

```console
crash> kmem -i                # Memory statistics
crash> kmem -S <cache>        # Inspect slab
crash> vm <pid>               # Process memory mapping
crash> search -k <pattern>    # Search memory
```

### Stack Overflow

```console
crash> bt -v                  # Check stack overflow
crash> bt -r                  # Raw stack data
```

## Advanced Techniques

### Deriving Lock Pointers from Stack Backtrace (ARM64)

> **Source**: [Kernel panic 实验室 - Kernel panic 实战之读写锁推导](https://mp.weixin.qq.com/s/szDQ9wOJDwcWo2AStiikPw)

When a task is blocked waiting for a lock, you can derive the lock address by reading callee-saved registers from the stack:

```console
# 1. Find FP (frame pointer) from backtrace
#    The value in [...] is the FP of that function
crash> bt
PID: 1234
#3 [fffffc09c4f3ab0] schedule_preempt_disable
#4 [fffffc09c4f3b30] rwsem_down_write_slowpath
#5 [fffffc09c4f3b90] down_write

# 2. Disassemble the calling function to find where it puts the lock pointer
crash> dis -xl down_write
    mov  x0, x19                # x0 = x19 (lock pointer)
    mov  w1, #0x2
    bl   rwsem_down_write_slowpath

# 3. Disassemble the callee to find where x19 is saved to stack
crash> dis -xl rwsem_down_write_slowpath
    stp  x20, x19, [sp, #176]   # x19 saved at sp+176

# 4. Calculate SP from FP: SP = FP - 0x60 (from "add x29, sp, #0x60")
#    rwsem_down_write_slowpath FP = 0xfffffc09c4f3b30
#    SP = 0xfffffc09c4f3b30 - 0x60 = 0xfffffc09c4f3ad0

# 5. Read x19 from stack: SP + 176 = 0xfffffc09c4f3b88
crash> rd 0xfffffc09c4f3b88
    fffffc09c4f3b88:  fffff80f78b0b00    ← This is the lock address!

# 6. Inspect the lock
crash> struct rw_semaphore fffff80f78b0b00 -x
```

**Why it works**: x19-x28 are callee-saved in AArch64 ABI, so callees must save them on stack before clobbering. By finding where callee saved the register, you can recover the lock address.

> **x86_64 equivalent**: Use RBP chain with `bt -f`. Note that with `-fomit-frame-pointer`, this technique may fail; in that case use `bt -F` or look for explicit stack frames.

### Memory Leak Diagnostic (Three-Layer Check)

> **Source**: [Kernel panic 实验室 - Kernel driver 内存泄露问题排查指南](https://mp.weixin.qq.com/s/RER260p6MN5NmymYdyKn0g)

Three independent paths to diagnose memory leaks:

```console
# === Layer 1: /proc 三件套 (read from running system or captured info) ===
# MemAvailable 持续下降 + SUnreclaim 持续增加 → slab 内存泄露
cat /proc/meminfo
cat /proc/slabinfo
cat /proc/buddyinfo

# === Layer 2: SLAB-specific (slub_debug) ===
# In bootargs: slub_debug=u,kmalloc-512
# Then read:
cat /sys/kernel/debug/slab/kmalloc-512/alloc_traces
cat /sys/kernel/debug/slab/kmalloc-512/free_traces

# === Layer 3: >8K allocations (page_owner) ===
# SUnreclaim rises but slabinfo flat → kmalloc > 8K uses alloc_pages directly
# Enable CONFIG_PAGE_OWNER + boot with page_owner=on
# Then:
echo 1 > /sys/kernel/debug/page_owner/enable
# Periodic dumps, then diff:
./page_owner_sort --cull name,ator,stacktrace page_owner_begin.txt > begin.txt
./page_owner_sort --cull name,ator,stacktrace page_owner_end.txt   > end.txt
# Compare begin.txt vs end.txt - rising stacks are leaks

# === Alternative: kmemleak ===
# CONFIG_DEBUG_KMEMLEAK + kmemleak=on bootarg
echo scan > /sys/kernel/debug/kmemleak
cat /sys/kernel/debug/kmemleak
```

### Chained Queries

```console
crash> bt -f                  # Get pointers
crash> struct file.f_dentry <addr>
crash> struct dentry.d_inode <addr>
crash> struct inode.i_pipe <addr>
```

### Batch Slab Inspection

```console
crash> kmem -S inode_cache | grep counter | grep -v "= 1"
```

### Kernel Linked List Traversal

```console
crash> list task_struct.tasks -s task_struct.pid -h <start>
crash> list -h <addr> -s dentry.d_name.name
```

## Extended Reference

For detailed information, refer to the following reference files:

| File | Content |
|------|---------|
| `references/advanced-commands.md` | Advanced commands: list, rd, search, vtop, kmem, foreach |
| `references/vmcore-format.md` | vmcore file format, ELF structure, VMCOREINFO |
| `references/case-studies.md` | Debugging cases: kernel BUG, deadlock, OOM, NULL pointer, stack overflow |
| `references/debug-tools-guide.md` | Advanced debugging tools: KASAN, Kprobes, Kmemleak, UBSAN (require kernel rebuild) |
| `references/kdump-setup-guide.md` | **NEW** End-to-end kdump configuration (x86_64 + ARM64, crashkernel syntax, sysrq triggers) |
| `references/arm64-crash-params.md` | **NEW** ARM64-specific crash address parameters (vabits_actual, phys_offset, kimage_voffset, kaslr) |
| `references/sources.md` | **NEW** Complete bibliography of reference materials used to enhance this skill |

Usage:
```console
crash> help <command>        # Built-in help
# Or ask Claude to view reference files
```

## Common Errors

```text
crash: vmlinux and vmcore do not match!
# -> Ensure vmlinux version exactly matches vmcore

crash: cannot find booted kernel
# -> Specify vmlinux path explicitly

crash: cannot resolve symbol
# -> Check if vmlinux has debug symbols
```

## Security Warnings

⚠️ **Dangerous Operations**

The following commands can cause system damage or data loss:

| Command | Risk | Recommendation |
|---------|------|----------------|
| `wr` | Writes to live kernel memory | **NEVER use on production systems** - can crash or corrupt running kernel |
| GDB passthrough | Unrestricted memory access | Use with caution, may modify memory or registers |

🔒 **Sensitive Data Handling**

- **vmcore files** contain complete kernel memory, potentially including:
  - User process memory and credentials
  - Encryption keys and secrets
  - Network connection data and passwords
- **Access control**: Restrict vmcore file access to authorized personnel
- **Secure storage**: Store dump files in encrypted or access-controlled directories
- **Secure disposal**: Use `shred` or secure delete when disposing of vmcore files

🛡️ **Best Practices**

1. Only analyze vmcore files in isolated/test environments when possible
2. Never share raw vmcore files publicly without sanitization
3. Consider using `makedumpfile -d` to filter sensitive pages before analysis
4. Document and audit all crash analysis sessions for compliance

## Important Notes

1. **Version Match**: vmlinux must exactly match the vmcore kernel version
2. **Debug Info**: Must use vmlinux with debug symbols
3. **Context Awareness**: `bt`, `files`, `vm` commands are affected by current context
4. **Live System Modification**: `wr` command modifies running kernel, extremely dangerous

## Resources

- [Crash Utility Whitepaper](https://crash-utility.github.io/crash_whitepaper.html)
- [Crash Utility Documentation](https://crash-utility.github.io/)
- [Crash Help Pages](https://crash-utility.github.io/help_pages/)

## Contributing

This is an open-source project. Contributions are welcome!

- **GitHub Repository**: https://github.com/crazyss/linux-kernel-crash-debug
- **Report Issues**: [GitHub Issues](https://github.com/crazyss/linux-kernel-crash-debug/issues)
- **Submit PRs**: Pull requests are welcome for bug fixes, new features, or documentation improvements

See [CONTRIBUTING.md](https://github.com/crazyss/linux-kernel-crash-debug/blob/main/CONTRIBUTING.md) for guidelines.