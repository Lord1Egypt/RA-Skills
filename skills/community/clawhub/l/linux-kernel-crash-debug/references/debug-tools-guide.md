# Kernel Debug Tools Guide

> Language note: Chinese explanations and original source titles are optional companion material. Follow the user’s preferred language and translate relevant passages when needed; no locale is required.


> **This guide provides advanced debugging methods beyond crash utility analysis.**
> These tools typically require kernel recompilation with specific config options or writing kernel modules.

## Live-System Safety Gate

Prefer offline vmcore analysis. The commands below that load modules, change
boot parameters, write debugfs/procfs controls, or enable tracing mutate a live
kernel. Do not execute them unless the user explicitly authorizes the exact host
and action and confirms a disposable lab or approved maintenance window.

For every authorized live capture: record the current setting, select the
narrowest function/object and a short duration, write output only to a protected
case directory, and define cleanup before enabling the tool. Apply cleanup in
the same session. Do not capture pathnames, buffers, credentials, or business
payloads unless they are essential and explicitly approved. An agent must not
trigger a deliberate panic or reboot.

---

## Overview

When crash utility analysis cannot pinpoint the root cause, consider these advanced debugging approaches:

| Tool | Purpose | Requires Kernel Rebuild | Suitable For |
|------|---------|------------------------|--------------|
| **KASAN** | Memory error detection | Yes (CONFIG_KASAN) | Development |
| **KFENCE** | Sampled memory error detection | Yes (CONFIG_KFENCE) | Production / fleet |
| **KCSAN** | Data-race detection | Yes (CONFIG_KCSAN) | Testing / staging |
| **Kprobes** | Dynamic function tracing | If probe support is not already configured | Lab / approved maintenance |
| **Kmemleak** | Memory leak detection | Yes (CONFIG_DEBUG_KMEMLEAK) | Development |
| **UBSAN** | Undefined behavior detection | Yes (CONFIG_UBSAN) | Development |
| **SLUB Debug** | Slab corruption detection | Yes (CONFIG_SLUB_DEBUG) | Development |
| **Lockdep** | Locking issue detection | Yes (CONFIG_LOCKDEP) | Development |
| **KMSAN** | Uninitialized-value origin tracking | Yes (CONFIG_KMSAN) | Disposable lab (§8.1) |
| **DMA API debug** | DMA mapping lifecycle validation | If not already configured | Lab (§8.2) |
| **fail-nth** | Deterministic error-path testing | Configured fault-injection facilities | Human-operated lab (§8.3) |
| **Event triggers** | Freeze a bounded pre-symptom trace | Configured tracing/events | Approved capture (§8.4) |

---

## 1. KASAN - Kernel Address Sanitizer

### What It Detects

- **Out-of-bounds (OOB)** memory accesses
- **Use-after-free (UAF)** errors
- **Double-free** errors
- Stack/global out-of-bounds accesses in supported modes; coverage differs by mode

### Kernel Configuration

```bash
# Enable KASAN in kernel config
CONFIG_KASAN=y
CONFIG_KASAN_GENERIC=y           # Generic mode (best detection)
CONFIG_KASAN_OUTLINE=y           # Outline instrumentation (smaller)
# or
CONFIG_KASAN_INLINE=y            # Inline instrumentation (faster)

# Include allocation/free stack traces
CONFIG_STACKTRACE=y
# For physical-page allocation/free stacks
CONFIG_PAGE_OWNER=y            # boot with page_owner=on
```

### Overhead

| Mode | Relative Overhead | Intended Environment | Platform |
|------|-----------------|-------------------|----------|
| Generic | High | Precise development debugging | Multiple architectures |
| Software tag-based | Moderate | Real-workload testing | arm64 only |
| Hardware tag-based | Low | In-field detection / mitigation | arm64 with MTE |

### Usage

```bash
# Verify KASAN is enabled
$ grep KASAN /boot/config-$(uname -r)

# Human-operated disposable lab only: KASAN's KUnit tests deliberately
# exercise invalid accesses and may panic. Agents must not load/run them.
# Current upstream uses CONFIG_KUNIT + CONFIG_KASAN_KUNIT_TEST and
# kasan_test.ko; use the matching tree's test instructions, not test_kasan.

# Test-kernel boot parameters: report repeatedly, or panic on invalid access
kasan_multi_shot
kasan.fault=panic
```

`kasan_multi_shot` is a boot parameter, not a runtime sysctl. On current
kernels, `kasan.fault=report|panic|panic_on_write` controls report/panic
behavior independently. Tag-based modes also have mode-specific boot controls.

### Sample Report

```
BUG: KASAN: slab-out-of-bounds in kmalloc_oob_right+0x6c/0x90
Write of size 1 at addr ffff88800a8a0100 by task insmod/1234
...
Allocated by task 1234:
 kasan_save_stack+0x1b/0x40
 __kasan_kmalloc+0x7c/0x90
```

## KFENCE - Low-Overhead Sampled Memory Safety

KFENCE samples heap allocations into guarded pages and detects out-of-bounds
access, use-after-free, and invalid free. It is designed for production kernels
with near-zero overhead, but sampling means it will not observe every object.

```bash
CONFIG_KFENCE=y
# Optional: build support but leave disabled until boot time
CONFIG_KFENCE_SAMPLE_INTERVAL=0

# Milliseconds; non-zero enables sampling
kfence.sample_interval=100
# Choose report, oops, or panic behavior
kfence.fault=report
```

Use KFENCE when the bug appears only under long-running production workloads.
Use KASAN when a deterministic reproducer exists and precise coverage matters
more than overhead. Preserve the KFENCE allocation/free stacks: the faulting
instruction is the detection site, while the lifetime stacks often identify
the root cause.

## KCSAN - Data-Race Detection

KCSAN is a dynamic, watchpoint-based sampling detector for data races. A normal
report contains both racing access stacks, access sizes/types, and sometimes an
observed value transition.

```bash
CONFIG_KCSAN=y
```

An `unknown origin` report can occur when the other access was not
instrumented or came from DMA. Treat it as a strong race lead, but do not invent
a second writer. Verify the intended memory-ordering primitive and reproduce
under the same workload.

---

## 2. Kprobes - Dynamic Kernel Probes

### What It Does

Allows dynamic instrumentation of almost any kernel function without modifying source code.

### Kernel Configuration

```bash
CONFIG_KPROBES=y
CONFIG_KPROBE_EVENTS=y          # Required for the tracefs event interface below
CONFIG_KALLSYMS=y
CONFIG_KALLSYMS_ALL=y
```

### Usage Methods

#### Method 1: Dynamic Kprobes (No Code Required)

Kprobe output may reveal function arguments and workload activity. The following
human-run recipe requires exact-host/action authorization and an already mounted
tracefs. Verify the target is probeable and does not expose secrets. It uses an
owned event and fresh tracing instance so existing sessions are preserved.
Append to `kprobe_events`: opening it with `>` can clear unrelated probes.

```bash
# Human-run lab / approved maintenance only; replace the target first.
(
set -eu
umask 077
tracefs=/sys/kernel/tracing
target_function='<target_function>'
event="crash_probe_$$"
inst="$tracefs/instances/crash-probe-$$"
out_dir=$(mktemp -d /tmp/kernel-probe.XXXXXX)
test ! -e "$tracefs/events/kprobes/$event"
mkdir "$inst"
cleanup() {
    printf '0\n' > "$inst/tracing_on" || :
    if [ -e "$inst/events/kprobes/$event/enable" ]; then
        printf '0\n' > "$inst/events/kprobes/$event/enable" || :
    fi
    printf -- '-:%s\n' "$event" >> "$tracefs/kprobe_events" || :
    rmdir "$inst" || printf 'Cleanup incomplete: %s\n' "$inst" >&2
}
trap cleanup EXIT
trap 'exit 130' HUP INT TERM
printf '0\n' > "$inst/tracing_on"
printf '256\n' > "$inst/buffer_size_kb"  # KiB per CPU
printf 'p:%s %s\n' "$event" "$target_function" >> "$tracefs/kprobe_events"
printf '1\n' > "$inst/events/kprobes/$event/enable"
printf '1\n' > "$inst/tracing_on"
timeout 30 cat "$inst/trace_pipe" > "$out_dir/probe.trace" || [ "$?" -eq 124 ]
printf 'Saved: %s\n' "$out_dir"
)
```

#### Method 2: Kernel Module (More Control)

```c
#include <linux/kprobes.h>

static struct kprobe kp = {
    .symbol_name = "do_sys_open",
    .pre_handler = my_pre_handler,
    .post_handler = my_post_handler,
};

// In init: register_kprobe(&kp);
// In exit: unregister_kprobe(&kp);
```

### Kretprobe (Return Value Tracing)

Use the same owned-event, instance, timeout, output, and trap-cleanup lifecycle
above. For an approved target whose return value contains no sensitive data,
replace only its probe-creation record with the following; do not create both
records under the same event name:

```bash
printf 'r:%s %s retval=$retval\n' "$event" "$target_function" >> "$tracefs/kprobe_events"
```

[Upstream kprobe event controls](https://docs.kernel.org/trace/kprobetrace.html).

---

## 3. Kmemleak - Memory Leak Detector

### What It Does

Scans memory for orphaned allocations (memory that was allocated but is no longer referenced).

### Kernel Configuration

```bash
CONFIG_DEBUG_KMEMLEAK=y
# Retain the target tree's default CONFIG_DEBUG_KMEMLEAK_MEM_POOL_SIZE
# unless evidence justifies changing its emergency metadata pool size.
```

### Usage

`scan` and `dump` alter detector control state; `clear` discards the current
findings. Preserve the output first and require explicit confirmation before
clearing it on a shared incident host.

```bash
# Trigger a memory scan
$ echo scan > /sys/kernel/debug/kmemleak

# View detected leaks
$ cat /sys/kernel/debug/kmemleak

# Destructive to diagnostic state: export results and confirm before clearing
$ echo clear > /sys/kernel/debug/kmemleak

# Dump specific address info
$ echo "dump=0xffff88800a8a0100" > /sys/kernel/debug/kmemleak
```

### Sample Report

```
unreferenced object 0xffff88800a8a0100 (size 128):
  comm "insmod", pid 1234, jiffies 4294891234 (age 52.320s)
  backtrace:
    [<ffffffff81234567>] kmalloc+0x67/0x100
    [<ffffffffa0123456>] my_module_init+0x56/0x100 [my_module]
```

---

## 4. UBSAN - Undefined Behavior Sanitizer

### What It Detects

- Integer overflows/underflows
- Invalid bit shifts
- Misaligned memory accesses
- Division by zero

### Kernel Configuration

```bash
CONFIG_UBSAN=y
CONFIG_UBSAN_TRAP=y            # Trap on undefined behavior
```

---

## 5. SLUB Debug

> **Source**: [Kernel panic 实验室 - 内核维测之 slub_debug 用法参考](https://mp.weixin.qq.com/s/Chciyg7QHsMeWF3dNwQyBg) | [Kernel panic 实验室 - Slub use after free 问题讨论](https://mp.weixin.qq.com/s/SmFNmwoz4lr6F7zBi0VQqA)

### What It Does

Detects corruption in slab allocator (kmalloc/kfree), including OOB, UAF, and leaks.

### Kernel Configuration

```bash
CONFIG_SLUB_DEBUG=y
CONFIG_DEBUG_FS=y
CONFIG_SLUB_DEBUG_ON=y   # Opens all caches with fzpu by default
```

### Boot Parameters

```bash
# Syntax: slub_debug=<flags>,<cache1>,<cache2>,...
slub_debug=<Debug-Option>,<slab name1>,<slab_name2>

# Examples
slub_debug=u,kmalloc-512,kmalloc-256  # u flag for kmalloc-512 + kmalloc-256
slub_debug=P                          # Poison all caches
slub_debug=FZPU                       # All flags for all caches
```

### The 5 Flags: f/z/p/u/t

| Flag | Effect | Use Case |
|------|--------|----------|
| **f** | Check slab values on alloc/free | Detects OOB and UAF |
| **z** | Fill redzones (left/right) with pattern | Detects OOB access |
| **p** | Fill with `POISON_FREE`/`POISON_INUSE` | Detects UAF |
| **u** | Save alloc/free call stacks | Memory leak investigation |
| **t** | Print stack at every alloc/free | High overhead, debug only |

**Common combinations**:
- `fz` — minimum OOB detection
- `fzp` — OOB + UAF
- `fzpu` — full coverage
- `u` alone — for leak investigation (lower overhead)

### Reading slub_debug Traces

```bash
# After enabling slub_debug=u,<cache> in bootargs:
cat /sys/kernel/debug/slab/kmalloc-512/alloc_traces
cat /sys/kernel/debug/slab/kmalloc-512/free_traces
# alloc_traces groups currently allocated objects by allocation stack.
# free_traces describes the previous lifecycle's freeing stacks for those
# objects; these are not matching allocation/free event logs.
```

Compare current allocation counts/ages across bounded snapshots and account for
expected workload retention before calling growth a leak.
[Upstream debugfs file semantics](https://docs.kernel.org/admin-guide/mm/slab.html#debugfs-files).

### Limitations

> **Key insight from Herbert**: slub_debug OOB detection only triggers on **alloc or free** — you can see the slab was corrupted, but **not who corrupted it**. Unlike KASAN, it cannot pinpoint the exact "culprit" instruction.

For UAF: see `references/case-studies.md` Case 12 for the **misalignment UAF** challenge.

### When CONFIG_SLUB_DEBUG_ON is Set

This option automatically applies `DEBUG_DEFAULT_FLAGS` to all slab caches. The `kmem_cache_flags()` function then propagates the flags to every cache's `flags` field at creation time.

---

## 6. Lockdep - Lock Dependency Validator

### What It Detects

- Potential deadlocks
- Lock inversion issues
- Incorrect lock usage

### Kernel Configuration

```bash
CONFIG_LOCKDEP=y
CONFIG_LOCK_STAT=y             # Lock statistics
CONFIG_DEBUG_LOCK_ALLOC=y      # Lock allocation tracking
```

### Usage

```bash
# View lock statistics
$ cat /proc/lock_stat

# View lock dependencies
$ cat /proc/lockdep

# Destructive to diagnostic state: save /proc/lock_stat and confirm first
$ echo 0 > /proc/lock_stat
```

---

## 7. Ftrace - Kernel Tracer

### What It Does

Provides comprehensive kernel tracing capabilities.

### Kernel Configuration

```bash
CONFIG_FTRACE=y
CONFIG_FUNCTION_TRACER=y
CONFIG_FUNCTION_GRAPH_TRACER=y
CONFIG_STACK_TRACER=y
```

### Usage

Function tracing can impose substantial overhead and generate sensitive,
high-volume output. This human-run recipe requires exact-host/action
authorization, an already mounted tracefs, and a verified function from
`available_filter_functions`. Set the filter before activating the tracer.
A fresh instance preserves existing global tracer, filter, and buffer state;
if instances are unavailable, use a separately reviewed runbook that records
and restores the exact prior state instead of assuming `nop` and an empty filter.

```bash
# Human-run lab / approved maintenance only; replace the target first.
(
set -eu
umask 077
target_function='<target_function>'
inst=/sys/kernel/tracing/instances/crash-function-$$
out_dir=$(mktemp -d /tmp/kernel-function.XXXXXX)
mkdir "$inst"
cleanup() {
    printf '0\n' > "$inst/tracing_on" || :
    printf 'nop\n' > "$inst/current_tracer" || :
    printf '\n' > "$inst/set_ftrace_filter" || :
    rmdir "$inst" || printf 'Cleanup incomplete: %s\n' "$inst" >&2
}
trap cleanup EXIT
trap 'exit 130' HUP INT TERM
printf '0\n' > "$inst/tracing_on"
printf '256\n' > "$inst/buffer_size_kb"  # KiB per CPU
printf '%s\n' "$target_function" > "$inst/set_ftrace_filter"
printf 'function\n' > "$inst/current_tracer"
printf '1\n' > "$inst/tracing_on"
sleep 30
printf '0\n' > "$inst/tracing_on"
cat "$inst/trace" > "$out_dir/function.trace"
printf 'Saved: %s\n' "$out_dir"
)
```

[Upstream function filters and tracing instances](https://docs.kernel.org/trace/ftrace.html).

---

## 8. Targeted Playbooks: Close a Specific Evidence Gap

These recipes add evidence the basic tools above do not provide. They are
investigation plans, not experiments executed by this project. Check the
target kernel's configuration and interfaces; upstream documentation does not
guarantee an older distribution exposes them.

### 8.1 Uninitialized Values: KMSAN Origin Tracking

**Use when:** a pointer, length, return value, or partially filled structure
contains unexplained bytes, without evidence of an OOB/UAF access.

**Smallest experiment:** with exact-host/build/workload authorization, use a
disposable supported Clang-built kernel with `CONFIG_KMSAN=y` and parameter /
return-value checks retained where supported. Current upstream documentation
supports the x86_64 runtime; check its toolchain requirements against the target
tree. Keep the original boot entry and have the operator restore it after the
bounded reproducer. KMSAN's memory and CPU cost make it unsuitable for production.

**Read the report backwards:** start at the uninitialized **use**, follow
`Uninit was stored` propagation records, then find the allocation or local
variable **origin** and the reported byte range. Audit the initialization and
error branches supplying those bytes. The final consumer need not be the code
that omitted initialization. Retest the same path after fixing that omission.

**Limit:** origins have four-byte granularity and bounded history. Missing
instrumentation and inline assembly can affect tracking; a silent run does not
prove initialization of every path. Do not replace the investigation with a
sanitizer suppression. [Upstream KMSAN guide](https://docs.kernel.org/dev-tools/kmsan.html).

### 8.2 Device Corruption: DMA API Lifecycle Checks

**Use when:** corruption follows device I/O, unmap, completion, or reset, and
CPU-access instrumentation has not identified the writer.

**Start read-only:** preserve the first DMA API warning and existing IOMMU fault
records, including timestamps, requester/device identity, DMA address, access
type, and reason. On a kernel with `CONFIG_DMA_API_DEBUG=y`, read
`/sys/kernel/debug/dma-api/{disabled,error_count,driver_filter,num_errors}`.
`disabled=Y` means checking is no longer active. Only the first error is printed
by default; silence after it does not mean errors stopped.

**Smallest experiment:** only in an explicitly authorized lab window, save the
controls, filter diagnostic output to the suspect **driver name** with
`driver_filter`, and use a small finite `num_errors` allowance. Capture one
bounded workload into a protected case directory, then restore the controls in
the same session. The filter limits diagnostic output, not all tracking costs;
do not enable unlimited error printing or dump every device's mappings.

**Close the lifecycle:** compare map/unmap API, device, handle, size, direction,
error checks, ownership synchronization, and completion-before-free ordering.
For `dma_unmap_sg()`, check the **original input nents**, not the mapped segment
count returned by `dma_map_sg()`. Correlate existing translated-IOMMU faults
with this timeline; requester/address formats are architecture-specific.

**Limit:** bookkeeping violations support a driver-API defect; they do not by
themselves prove which device write corrupted an object. Valid mapped DMA can
still corrupt data. Absence of a report or IOMMU fault does not exclude that
case; changing IOMMU mode is a separate experiment, not a fix.
[DMA API debugging, Part III](https://docs.kernel.org/core-api/dma-api.html),
[x86 IOMMU fault records](https://docs.kernel.org/arch/x86/iommu.html).

### 8.3 Error Paths: Deterministic Per-Task Fault Injection

**Use when:** cleanup fails only after an allocation error, and ordinary memory
pressure makes the failure difficult to isolate. This tests the error path
behind Case 14, rather than rediscovering its poison pattern.

**Human-operated lab only:** obtain exact-host/action authorization for a
disposable fixture, fixed attempt/time caps, console recovery, and protected
logs. Verify the target exposes `/proc/self/task/<tid>/fail-nth` and the needed
facilities, such as `CONFIG_FAILSLAB` or `CONFIG_FAIL_PAGE_ALLOC`. Save any
capability-specific filters before changing them; never apply global random
failure injection to an incident host.

Adapt the upstream single-syscall harness with this bounded sequence:

```text
open the test thread's fail-nth control before arming it
for N = 1 .. approved_attempt_cap, within approved_time_cap:
    reset fixture; arm N; execute exactly one target syscall
    immediately copy its return value and errno before any other syscall
    read remaining count; disarm with 0 before cleanup or logging
    save N, remaining count, copied result/errno, and detector evidence
    release successful resources; stop on a finding or an unconsumed count
on every exit: disarm the test thread and restore modified filters
```

**Crucial semantics:** N counts eligible fault-injection opportunities in that
thread, not necessarily allocations of one type. `fail-nth` takes precedence
over generic probability, interval, times, and task-filter settings; those are
not a reliable kill switch for it. Capability-specific exclusions still apply
(for example, `ignore-gfp-wait` can exclude sleepable allocations).
Allocations deferred to a worker are outside the calling thread's sequence.

**Prove the path:** an armed count reaching zero means a fault was injected;
a positive remainder means this attempt did not reach it. A returned `ENOMEM`
alone is not a cleanup defect. Preserve the injected failure plus the invalid
free, reference imbalance, or other invariant violation, then replay the same
case with injection off and after the candidate fix. Confirm the failing site
from its diagnostic stack; consuming N alone does not identify that site. Do not use a shell child
to arm `/proc/self` for an unrelated reproducer thread.
[Fault injection and the upstream fail-nth harness](https://docs.kernel.org/fault-injection/fault-injection.html).

### 8.4 Rare Symptoms: Conditional Flight Recorder

**Use when:** an observable event precedes the failure, but ordinary tracing
overwrites its lead-up. A one-shot `traceoff` trigger freezes the normal ring
buffer when its predicate matches. This differs from streaming `trace_pipe`.

**Human-run example, only on the explicitly authorized host/window:** verify
tracefs is already mounted here, both events exist, the exit event's `format`
contains `pid`, and `global` is an available clock. Budget 256 KiB per CPU and
30 seconds of capture. Keep the reproducer waiting until tracing is armed;
select its task PID as seen by the target kernel, not a container-local PID.
The fresh instance isolates configuration from existing tracing sessions.

```bash
(
set -eu
umask 077
target_pid=1234  # Replace with the agreed reproducer task before running.
out_dir=$(mktemp -d /tmp/kernel-trace.XXXXXX)
inst=/sys/kernel/tracing/instances/crash-window-$$
mkdir "$inst"
cleanup() {
    printf '0\n' > "$inst/tracing_on" || :
    printf '%s\n' '!traceoff' > "$inst/events/sched/sched_process_exit/trigger" || :
    printf '0\n' > "$inst/events/enable" || :
    rmdir "$inst" || printf 'Cleanup incomplete: %s\n' "$inst" >&2
}
trap cleanup EXIT
trap 'exit 130' HUP INT TERM
printf '0\n' > "$inst/tracing_on"
printf 'global\n' > "$inst/trace_clock"
printf '256\n' > "$inst/buffer_size_kb"
printf '1\n' > "$inst/events/sched/sched_switch/enable"
printf '1\n' > "$inst/events/sched/sched_process_exit/enable"
printf 'traceoff:1 if pid == %s\n' "$target_pid" > "$inst/events/sched/sched_process_exit/trigger"
cat "$inst/trace_clock" > "$out_dir/clock.txt"
cat "$inst/events/sched/sched_process_exit/format" > "$out_dir/exit-format.txt"
printf '1\n' > "$inst/tracing_on"
printf 'Armed for task %s; release the waiting reproducer now.\n' "$target_pid"
sleep 30
printf '0\n' > "$inst/tracing_on"
cat "$inst/events/sched/sched_process_exit/trigger" > "$out_dir/trigger.txt"
cat "$inst/trace" > "$out_dir/trace.txt"
printf 'Saved: %s\n' "$out_dir"
)
```

**Read the capture:** check whether the one-shot count was consumed, then
inspect event ordering and buffer overwrite/loss indicators. An exit is only
the example stop condition; normal exits also match. Replace it with a verified
event/field predicate for the actual symptom. A synchronized clock helps
cross-CPU ordering but adds overhead; clock changes clear the buffer, so choose
it before capture. The ring may contain much less than 30 seconds of history.
These scheduler events establish scheduling history only. To test an async
driver lifetime, also select existing submit/complete/cancel/free events by
request identity, including worker context; exit alone does not imply a defect.

**Limit:** an unconsumed trigger means the condition was not observed in this
window, not that the bug is absent. Ordinary trace buffers do not survive a
crash/reboot by themselves. If tracing must continue after the first hit, use
`snapshot:1 if ...` instead, with snapshot support and its extra buffer; read
`snapshot` and remove `!snapshot` during cleanup. Choose one action, and arrange
persistent or remote capture separately if the host cannot remain readable.
[Event trigger semantics](https://docs.kernel.org/trace/events.html),
[ftrace buffers, clocks, and snapshots](https://docs.kernel.org/trace/ftrace.html).

## Decision Tree: Which Tool to Use?

```
Problem: Kernel crash/panic
│
├─ Have vmcore file?
│  └─ YES → Use crash utility (main skill)
│
├─ Need a live-kernel change?
│  └─ Require exact-host authorization, a bounded window, and cleanup first
│
├─ Suspect memory corruption?
│  ├─ Deterministic test reproducer → Enable KASAN
│  ├─ Production-only / rare crash → Enable KFENCE sampling
│  ├─ Memory leak suspected → Enable Kmemleak
│  └─ Slab corruption → Enable SLUB debug
│
├─ Suspect a data race?
│  └─ Enable KCSAN and preserve both access stacks
│
├─ Need to trace function calls?
│  ├─ Quick check → Dynamic Kprobes
│  └─ Detailed analysis → Ftrace
│
├─ Suspect locking issues?
│  └─ Enable Lockdep
│
└─ Undefined behavior?
   └─ Enable UBSAN
```

---

## Additional Resources

- **KASAN**: https://www.kernel.org/doc/html/latest/dev-tools/kasan.html
- **KFENCE**: https://docs.kernel.org/dev-tools/kfence.html
- **KCSAN**: https://docs.kernel.org/dev-tools/kcsan.html
- **Kprobes**: https://www.kernel.org/doc/html/latest/trace/kprobes.html
- **Kmemleak**: https://www.kernel.org/doc/html/latest/dev-tools/kmemleak.html
- **Ftrace**: https://www.kernel.org/doc/html/latest/trace/ftrace.html
- **Lockdep**: https://www.kernel.org/doc/html/latest/locking/lockdep-design.html
- **Linux Kernel Debugging Book**: https://github.com/PacktPublishing/Linux-Kernel-Debugging
