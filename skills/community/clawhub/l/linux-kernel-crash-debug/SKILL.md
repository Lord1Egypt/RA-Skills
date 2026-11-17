---
name: linux-kernel-crash-debug
version: 1.5.2
description: Debug Linux kernel crashes using evidence-first vmcore analysis, the crash utility, and memory/concurrency debugging tools. Use when users mention kernel crash, kernel panic, vmcore analysis, kernel dump debugging, crash utility, kernel oops debugging, pstore or ramoops, soft/hard lockup, hung task, OOM, locating root causes of kernel issues, regression bisection, mutex ownership, ARM64 lock-pointer recovery, KASAN, KFENCE, KCSAN, KMSAN, DMA API debugging, fail-nth, conditional trace capture, RCU stalls, Lockdep, drgn, Kprobes, Kmemleak, memory corruption, out-of-bounds access, use-after-free, race, deadlock, or memory leak detection.
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

This skill guides you through analyzing Linux kernel crash dumps using the crash utility.

## Installation

Install only when the user requests installation. These commands place skill files in the user workspace; they do not authorize services, startup hooks, or background jobs.

### Claude Code

Extract the verified release archive with all 13 runtime files; the scripts
and references are required alongside `SKILL.md`.

```bash
mkdir -p ~/.claude/skills/linux-kernel-crash-debug
unzip linux-kernel-crash-debug.skill -d ~/.claude/skills/linux-kernel-crash-debug
```

### OpenClaw
```bash
# Method 1: Install via ClawHub
clawhub install linux-kernel-crash-debug

# Method 2: Manual installation
mkdir -p ~/.openclaw/workspace/skills/linux-kernel-crash-debug
unzip linux-kernel-crash-debug.skill -d ~/.openclaw/workspace/skills/linux-kernel-crash-debug
```

Use an empty destination for a new installation; handle an existing installation
as an explicit upgrade. Copying only the manifest leaves its helpers missing.
[Claude Code skill locations](https://code.claude.com/docs/en/skills).

## Quick Start

**Language choice:** Respond in the user’s preferred language. `SKILL_CN.md` and Chinese references are optional companion material; translate relevant explanations when requested. Source titles retain their original language for attribution.

### Starting a Session

These are human reference commands. Agents use the offline wrapper below;
raw RAM requires the loader/format checks in `references/vmcore-format.md`.

```bash
# Analyze a dump file
crash vmlinux vmcore

# Debug a running system
crash vmlinux

# Raw RAM loading is format- and tool-version-specific; see the reference above.
```

### Core Debugging Workflow

```console
0. Preserve checksums, vmcore-dmesg, build IDs, modules, config, and command line
1. crash> sys              # Validate release/build and panic context
2. crash> log              # Find the FIRST anomaly, not only the last panic
3. crash> bt / bt -a       # Compare panic task with all active CPUs
4. crash> mod              # Confirm faulting module symbols are available
5. crash> struct / kmem    # Test a specific object-lifetime hypothesis
6. Search upstream and verify good/bad kernels before claiming a regression
```

Read `references/evidence-first-workflow.md` before deep analysis. It defines
the evidence-quality gates, failure-type routing, hypothesis ledger, tool
escalation rules, and root-cause report format. Never equate the panic task,
fault site, corruption site, and root cause without supporting evidence.

For worked evidence chains, read Cases 13–15 in `references/case-studies.md`:
GRO header-offset reconstruction, InfiniBand error-path double free, and
filesystem writeback/reclaim deadlock. Treat a bisect result as a candidate
trigger, an NMI frame as interrupted context, and collection overhead as a
possible contributor to stalls; verify each before assigning a root cause.

For suspected single-bit corruption of an ARM64 pointer, follow the
[candidate-validation method](references/evidence-first-workflow.md#511-arm64-single-bit-pointer-corruption-hypotheses)
and [Case 16](references/case-studies.md#case-16-arm64-single-bit-pointer-corruption-hypothesis).
A plausible reconstructed pointer does not establish DDR failure.

### When the first pass leaves an evidence gap

Choose one targeted playbook rather than enabling every detector:

| Missing evidence | Next playbook |
|---|---|
| Where an uninitialized value originated | [KMSAN origin tracking](references/debug-tools-guide.md#81-uninitialized-values-kmsan-origin-tracking) |
| Whether a driver misused DMA mappings | [DMA API lifecycle checks](references/debug-tools-guide.md#82-device-corruption-dma-api-lifecycle-checks) |
| Which failed allocation breaks cleanup | [Per-task fault injection](references/debug-tools-guide.md#83-error-paths-deterministic-per-task-fault-injection) |
| Events immediately preceding a rare symptom | [Conditional flight recorder](references/debug-tools-guide.md#84-rare-symptoms-conditional-flight-recorder) |
| What actually prevents an RCU grace period completing | [RCU stall differential reading](references/evidence-first-workflow.md#521-rcu-stalls-compare-the-same-grace-period) |

These complement the existing OOB/UAF, race, leak, and lock-order tools. Start
with saved evidence; live experiments still follow the safety contract below.

## Live-System Safety Contract

Default to offline, read-only analysis. Treat `sudo`, module load/unload, boot
or service configuration, writes under debugfs or `/proc/sys`, live tracing,
and SysRq actions as live-host mutations.

- Do not perform a mutation unless the user explicitly authorizes the exact
  host and action and confirms a lab or approved maintenance context. If the
  environment is unknown, stop after read-only checks and provide a runbook.
- Before authorized tracing or detector changes, record the baseline, set a
  narrow target and time limit, choose a protected output path, and define the
  cleanup/rollback command. Apply cleanup in the same session and report it.
- Minimize captured arguments and payloads. Trace output and vmcores may expose
  credentials, paths, keys, and process memory; never upload or share them
  without explicit approval and an approved sanitization process.
- An agent must never initiate a deliberate panic, reboot, SysRq crash, or
  `kdumpctl test`. Explain the prerequisites and hand the final trigger to an
  authorized human following an approved drill with console access, backups,
  workload evacuation, and a verified rollback/recovery plan.

## 🤖 Agent Execution Directives
If you are an AI/Agent using this skill, **do not invoke `crash` interactively** as it will block your subshell.
1. Use the bundled wrapper `./scripts/agent-crash.sh` for offline regular-file dumps under an unprivileged account. It enforces a narrow command allowlist and truncates displayed output:
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore triage` - Runs `sys`, a high-signal log index, panic/all-CPU backtraces, and module inventory.
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore flow-oom` - Top 15 memory checks.
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore flow-deadlock` - Pulls UN task stacks.
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore dis-regs <func> <pid>` - Matching disassembly and stack-frame data.
   - `./scripts/agent-crash.sh -k vmlinux -c vmcore check-poison <addr>` - Pattern match memory poisons.
2. **Restricted primitives**: Use `./scripts/agent-crash.sh -k vmlinux -c vmcore read-memory ffff880123456780 64`, `backtrace <pid>`, or `disassemble <symbol>` when macros are insufficient. `run` is removed. Both input paths are mandatory; live `/proc`, `/sys`, `/dev` inputs, root execution, and local/home `.gdbinit` files are rejected. Startup `.crashrc` files are disabled. No arbitrary crash/GDB commands, shell escapes, pipelines, redirection, command files, or extensions are exposed by this wrapper. Memory reads are limited to 1..256 words.
   Keep dumps and collected output access-controlled. Use a trusted installed `crash` executable in an isolated analysis environment; the wrapper is not an OS sandbox or a defense against parser vulnerabilities in malformed dumps/symbol files. If a needed query is unsupported, report the evidence gap and hand a precise offline query to an authorized human rather than bypassing the wrapper.
3. Check `references/agentic-heuristics.md` for extended expert methodologies.
4. Follow `references/evidence-first-workflow.md`: report symbol/dump quality,
   identify the earliest anomaly, keep competing hypotheses, and attach a
   confidence level plus a disproof test to the conclusion.

## Prerequisites

| Item | Requirement |
|------|-------------|
| **vmlinux** | Must have debug symbols (`CONFIG_DEBUG_INFO=y`) |
| **vmcore** | kdump/netdump/diskdump/ELF format |
| **Version** | vmlinux must exactly match the vmcore kernel version |

### Package Installation

Package installation changes the host and may need administrator privileges. Require explicit authorization for the exact host and packages; prefer already-installed tools. Offline dump analysis runs as an unprivileged account.

Package examples use the current host's `uname -r`. For a dump from another
host or boot, query/install symbols for the captured kernel release and build,
not the analysis host's running kernel.

#### Anolis OS / Alibaba Cloud Linux

```bash
# Install crash utility
sudo dnf install crash

# Install kernel debuginfo (match your kernel version)
sudo dnf install kernel-debuginfo-$(uname -r)

# Install additional analysis tools
sudo dnf install gdb binutils makedumpfile

# Optional: Install kernel-devel for source code reference
sudo dnf install kernel-devel-$(uname -r)
```

#### RHEL / CentOS / Rocky / AlmaLinux

```bash
sudo dnf install crash gdb binutils makedumpfile kexec-tools
# Enable the matching debuginfo repository first if needed
sudo dnf debuginfo-install kernel-$(uname -r)
```

#### Ubuntu / Debian

```bash
sudo apt install crash kdump-tools kexec-tools gdb binutils makedumpfile
# Debian and Ubuntu use different debug-symbol repositories/package suffixes;
# query the exact running-kernel package before installing it.
apt-cache search --names-only "linux-image-$(uname -r).*(dbg|dbgsym)"
```

#### SLES / openSUSE

```bash
sudo zypper install crash kexec-tools makedumpfile
# Optional SUSE kdump UI and matching kernel debuginfo
sudo zypper install yast2-kdump
zypper se -s 'kernel*debug*'
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
| `sys` | System info/panic reason; `-i` shows DMI | `sys`, `sys -i` |
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

## Session Control (Human Reference)

The following interpreter features are for an authorized human in a trusted offline session. Agents must use the wrapper above; do not invoke GDB passthrough, redirection, or command-file inclusion as a fallback. Review command files before any human use and protect output paths.

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
| crash command | `crash vmlinux vmcore` | `crash vmlinux vmcore`; add `-m` only as a recovery path |
| KASLR | Usually auto-handled from VMCOREINFO | Usually auto-handled; explicit `--kaslr=<offset>` requires verified ARM64 tool support |
| Virtual address bits | fixed for the analyzed build | VMCOREINFO first; `-m vabits_actual=<N>` is a fallback |
| Physical base | `phys_base` from VMCOREINFO | VMCOREINFO first; `-m phys_offset=<addr>` is a fallback |
| VA-PA offset | `__START_KERNEL_map` | VMCOREINFO first; `-m kimage_voffset=<val>` is a fallback |
| Frame pointer | RBP (often optimized away) | FP (x29) explicit |
| Calling convention | RDI/RSI/RDX/RCX/R8/R9 | X0-X7 |

> **For complete ARM64 address parameter derivation**, see `references/arm64-crash-params.md`.
> **For kdump end-to-end setup**, see `references/kdump-setup-guide.md`.

### ARM64 Raw/Damaged-Dump Fallback Template

```bash
crash_arm64 \
  -m vabits_actual=39 \
  -m phys_offset=0x80000000 \
  -m kimage_voffset=0xffffffc000000000 \
  --kaslr=0x0 \
  vmlinux vmcore
```

> First try `crash vmlinux vmcore`. Use explicit values only when VMCOREINFO is
> absent/damaged or the input is raw RAM, and verify the installed tool's ARM64
> support for `--kaslr`. A zero offset must be established from this boot's
> evidence; never assume it or reuse another boot's parameters. `-m kaslr` is
> not an upstream ARM64 override.

## Typical Debugging Scenarios

### Kernel BUG Location

```console
crash> sys                    # Confirm panic
crash> log | tail -50         # View logs
crash> bt                     # Call stack
crash> bt -f                  # Raw stack-frame data; recover arguments from matching assembly
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

### Recovering Lock Pointers and Mutex Owners (ARM64)

> **Sources**: [mutex lock pointer](https://mp.weixin.qq.com/s/HueZ8rFiOeZ1cwZK1XPHww) and [rwsem lock derivation](https://mp.weixin.qq.com/s/szDQ9wOJDwcWo2AStiikPw), Kernel Panic Lab.

When a task sleeps in `mutex_lock()` or a rwsem slow path, trace the first ARM64 argument (`x0`) at the call site:

```console
# Path A: a global lock is constructed directly
    adrp x0, 0xffffffc00ac1e000
    add  x0, x0, #0x7f0         # lock = page + offset
    bl   mutex_lock

# Path B: the caller passes a callee-saved register
    mov  x0, x19                # lock pointer is the saved x19 value
    bl   mutex_lock
# Find the exact "add x29, sp, #N" and "stp/str ..., x19, [sp,#M]",
# derive SP from the frame pointer, then read the x19 stack slot with rd.

crash> struct mutex <lock_addr> -x
# mutex.owner packs flags into its low 3 bits on common kernels:
# owner_task = owner.counter & ~0x7
crash> struct task_struct <owner_task>
crash> bt <owner_pid>
```

`stp x20, x19, [sp,#32]` saves `x20` at `sp+32` and `x19` at `sp+40`. Never reuse example offsets blindly: derive them from the vmcore's matching `vmlinux`. Verify the mutex layout and owner flag definitions against the analyzed kernel.

> For exact FP/SP arithmetic, `stp` slot ordering, owner masking, and failure checks, read `references/arm64-lock-analysis.md`. For a complete rwsem example, read Case 11 in `references/case-studies.md`.

> **x86_64 equivalent**: Inspect matching disassembly and the unwinder's saved
> stack state. `bt -f` shows frame data; `bt -F` symbolizes that data. Neither
> recreates optimized-away arguments or missing registers. A manual RBP walk
> requires preserved frame pointers; other builds need supported unwind metadata.

### Memory Leak Diagnostic (Three-Layer Check)

> **Source**: [Kernel panic 实验室 - Kernel driver 内存泄露问题排查指南](https://mp.weixin.qq.com/s/RER260p6MN5NmymYdyKn0g)

Three independent paths to diagnose memory leaks:

The first path is read-only. Enabling `page_owner` or writing kmemleak controls
changes a live kernel and must follow the Live-System Safety Contract above.
Preserve the current output before clearing detector state.

```console
# === Layer 1: /proc 三件套 (read from running system or captured info) ===
# Falling MemAvailable with rising SUnreclaim suggests slab growth; verify retention.
cat /proc/meminfo
cat /proc/slabinfo
cat /proc/buddyinfo

# === Layer 2: SLAB-specific (slub_debug) ===
# In bootargs: slub_debug=u,kmalloc-512
# Then read:
cat /sys/kernel/debug/slab/kmalloc-512/alloc_traces
cat /sys/kernel/debug/slab/kmalloc-512/free_traces

# === Layer 3: page allocations not explained by slab growth (page_owner) ===
# Large kmalloc allocations can bypass slab; the cutoff depends on PAGE_SIZE/build.
# Enable CONFIG_PAGE_OWNER + boot with page_owner=on
# If page_owner is not already enabled, use an approved maintenance runbook;
# do not enable it as part of automated triage.
# Periodic dumps, then diff:
./page_owner_sort --cull name,ator,stacktrace page_owner_begin.txt begin.txt
./page_owner_sort --cull name,ator,stacktrace page_owner_end.txt end.txt
# Compare retained allocations across equivalent workload phases; growth is a lead, not proof of a leak.

# === Alternative: kmemleak ===
# CONFIG_DEBUG_KMEMLEAK + kmemleak=on bootarg
echo scan > /sys/kernel/debug/kmemleak
cat /sys/kernel/debug/kmemleak
```

### Chained Queries

```console
crash> bt -f                  # Recover pointer candidates using matching assembly
crash> struct file.f_path.dentry <addr>
crash> struct dentry.d_inode <addr>
crash> struct inode.i_pipe <addr>
```

### Batch Slab Inspection

```console
crash> kmem -S inode_cache     # Slab metadata, not inode reference-count validation
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
| `references/case-studies.md` | Debugging cases, including sourced GRO offset, InfiniBand double-free, writeback/reclaim, and ARM64 single-bit pointer evidence chains (Cases 13–16) |
| `references/debug-tools-guide.md` | Detector selection; KMSAN origins, DMA lifecycle checks, per-task failure injection, and conditional trace capture (§8) |
| `references/kdump-setup-guide.md` | **NEW** End-to-end kdump configuration (x86_64 + ARM64, crashkernel syntax, sysrq triggers) |
| `references/arm64-crash-params.md` | **NEW** ARM64-specific crash address parameters (vabits_actual, phys_offset, kimage_voffset, kaslr) |
| `references/arm64-lock-analysis.md` | ARM64 assembly/stack recovery of mutex and rwsem pointers, plus mutex owner decoding |
| `references/evidence-first-workflow.md` | **NEW** Evidence gates, timeline reconstruction, failure routing, tool escalation, regression verification, report template |
| `references/sources.md` | **NEW** Complete bibliography of reference materials used to enhance this skill |

Usage:
```console
crash> help <command>        # Built-in help
# Or ask your agent to view reference files
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
| GDB passthrough | Unrestricted memory access | Human-only trusted offline reference; agents must not use passthrough |
| Kprobes/ftrace/debugfs writes | Changes live instrumentation and may expose runtime data | Require explicit authorization, bounded capture, and cleanup |
| Boot/service configuration | Persists across reboot or changes crash recovery | Back up current state and provide rollback before applying |
| SysRq crash / `kdumpctl test` | Deliberately panics the host | Human-operated approved drill only; agents must not execute |

🔒 **Sensitive Data Handling**

- **vmcore files** may contain kernel and process memory, potentially including:
  - User process memory and credentials
  - Encryption keys and secrets
  - Network connection data and passwords
- **Access control**: Restrict vmcore file access to authorized personnel
- **Secure storage**: Store dump files in encrypted or access-controlled directories
- **Disposal**: Follow the storage system's approved retention and sanitization
  process. `shred` cannot guarantee erasure on SSDs, snapshots, or copy-on-write storage.

🛡️ **Best Practices**

1. Only analyze vmcore files in isolated/test environments when possible
2. Never share raw vmcore files publicly without sanitization
3. Record `makedumpfile -d` filtering and resulting evidence gaps; filtering alone does not prove sanitization
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
