# Debugging Case Studies

> Language note: Chinese explanations and original source titles are optional companion material. Follow the user’s preferred language and translate relevant passages when needed; no locale is required.


Detailed kernel crash debugging case analysis.

Cases 1–10 are teaching examples with schematic output, not independently
verified incident transcripts. Establish the actual build, register provenance,
structure layout, and causal sequence before applying a conclusion. `bt -f`
prints stack-frame data; annotated registers/arguments require exception-frame
or disassembly evidence. Interpreter queries below are human offline reference;
agents use the wrapper and hand off unsupported queries.

## Case 1: Kernel BUG Location

### Symptoms

```
PANIC: "kernel BUG at pipe.c:120!"
```

### Analysis Steps

```
# 1. Confirm system information
crash> sys
KERNEL: vmlinux
DUMPFILE: vmcore
CPUS: 8
DATE: Mon Jan 15 10:30:45 2024
UPTIME: 00:15:32
LOAD AVERAGE: 0.50, 0.35, 0.20
TASKS: 156
NODENAME: server01
RELEASE: 4.18.0-348.el8.x86_64
VERSION: #1 SMP Mon Jan 1 00:00:00 UTC 2024
MACHINE: x86_64  (2900 Mhz)
MEMORY: 32 GB
PANIC: "kernel BUG at pipe.c:120!"

# 2. View kernel log
crash> log | tail -100
[...]
kernel BUG at fs/pipe.c:120!
invalid opcode: 0000 [#1] SMP PTI
CPU: 3 PID: 1234 Comm: worker Tainted: G           O      4.18.0-348.el8.x86_64
RIP: 0010:pipe_read+0x120/0x300
[...]

# 3. Analyze call stack
crash> bt
PID: 1234   TASK: ffff88012b98e040  CPU: 3   COMMAND: "worker"
#0 [ffffc90000123e00] __die at ffffffff8105a2b0
#1 [ffffc90000123e30] do_trap at ffffffff8105a1a0
#2 [ffffc90000123e80] invalid_op at ffffffff81c00bf4
#3 [ffffc90000123f00] pipe_read at ffffffff81234560
#4 [ffffc90000123f80] do_readv at ffffffff81210000
#5 [ffffc90000123fc0] sys_readv at ffffffff81210100

# 4. Expand stack frames to get parameters
crash> bt -f
#3 [ffffc90000123f00] pipe_read at ffffffff81234560
    ffff88012b98e040:  ffff880123456000   # file pointer
    ffff88012b98e080:  ffff880123457000   # buffer
    ffff88012b98e0c0:  0000000000001000   # count
    [...]

# 5. Chain trace data structures
crash> struct file.f_path.dentry ffff880123456000
  dentry = ffff880123458000

crash> struct dentry.d_inode ffff880123458000
  d_inode = ffff880123459000

crash> struct inode.i_pipe ffff880123459000
  i_pipe = ffff88012345a000

crash> struct pipe_inode_info ffff88012345a000
struct pipe_inode_info {
  mutex = {
    owner = 0,
    wait_list = {...}
  },
  readers = 1,
  writers = 1,
  [...]
}

# 6. Batch check all pipe inodes
crash> kmem -S pipe_inode_cache | head
CACHE    NAME                OBJSIZE  ALLOCATED  TOTAL  SLABS  SSIZE
ffff88012a000000  pipe_inode_cache      184       45      60     3    4k

# Find mutexes with abnormal counts
crash> foreach bt | grep -B10 "pipe_read"
```

### Root Cause Analysis

The fault is localized to `pipe_read`; no root cause follows from this
schematic state alone. Inspect the exact BUG condition and this build's mutex
and pipe invariants. Modern mutexes do not have the historical `count` field;
do not diagnose UAF or a race from an invented count value.

---

## Case 2: Deadlock Analysis

### Symptoms

System hangs, unresponsive, but heartbeat normal.

### Analysis Steps

```
# 1. View all CPU states
crash> bt -a
CPU 0:
#0 [ffff880000000000] schedule at ffffffff81a12345
#1 [ffff880000000100] schedule_timeout at ffffffff81a13456
#2 [ffff880000000180] wait_for_completion at ffffffff81a14567
PID: 100   TASK: ffff88012a000000  CPU: 0   COMMAND: "thread_A"

CPU 1:
#0 [ffff880000010000] schedule at ffffffff81a12345
#1 [ffff880000010100] schedule_timeout at ffffffff81a13456
#2 [ffff880000010180] __down at ffffffff81a15678
PID: 101   TASK: ffff88012a001000  CPU: 1   COMMAND: "thread_B"

# 2. View uninterruptible processes
crash> ps -m | grep UN
  100  UN   0.0   0  ffff88012a000000  thread_A
  101  UN   0.1   0  ffff88012a001000  thread_B

# 3. Analyze wait queues
crash> foreach UN bt
PID: 100   TASK: ffff88012a000000  CPU: 0   COMMAND: "thread_A"
#0 schedule
#1 schedule_timeout
#2 wait_for_completion
#3 some_function_A

PID: 101   TASK: ffff88012a001000  CPU: 1   COMMAND: "thread_B"
#0 schedule
#1 __down
#2 down
#3 some_function_B

# 4. Check lock ownership
crash> struct mutex ffff88012b000000
struct mutex {
  owner = 0xffff88012a000000,  # thread_A holds
  wait_lock = {...},
  wait_list = {
    next = 0xffff88012b000020,
    prev = 0xffff88012b000020
  }
}

# 5. Trace what thread_A is waiting for
crash> bt -f 100
#2 wait_for_completion
    completion = 0xffff88012b001000
crash> struct completion ffff88012b001000
struct completion {
  done = 0,
  wait = {...}
}

# 6. Who should complete this completion?
crash> search -k ffff88012b001000
ffff88012a002000: ffff88012b001000  # Reference only; does not identify the completer
```

### Root Cause Analysis

This suggests a lock/completion dependency cycle if the exact lock addresses
match and source/temporal evidence establishes that B must signal A's
completion. A pointer found on B's stack does not establish that dependency.
Record the cycle only after verifying those edges; it is not automatically
the two-lock ABBA pattern.

---

## Case 3: Memory Exhaustion (OOM)

### Symptoms

```
Out of memory: Kill process 1234 (java) score 500 or sacrifice child
```

### Analysis Steps

```
# 1. View memory statistics
crash> kmem -i
                 PAGES        TOTAL      PERCENTAGE
TOTAL MEM       8388608      32 GB         ----
FREE            104857       400 MB         1%
USED            8283751     31.6 GB        98%
SHARED           524288       2 GB         6%
BUFFERS          262144       1 GB         3%
CACHED          1572864       6 GB        18%

# 2. View memory zones
crash> kmem -z
ZONE  DMA:
  pages_free     = 4096
  pages_min      = 128
ZONE  DMA32:
  pages_free     = 65536
ZONE  NORMAL:
  pages_free     = 32768
ZONE  MOVABLE:
  pages_free     = 0

# 3. View slab usage
crash> kmem -s
# Rank by OBJSIZE * ALLOCATED for object bytes; TOTAL is object capacity.
CACHE            NAME              OBJSIZE  ALLOCATED  TOTAL
ffff88012a000000 kmalloc-8192       8192    524288    600000
ffff88012a001000 kmalloc-4096       4096    262144    300000
ffff88012a002000 dentry              192    131072    150000
ffff88012a003000 inode_cache         592     65536     80000

# 4. View process memory usage
crash> ps -G
# Rank by the RSS field, allowing for the optional leading active-task marker.
PID    PPID  CPU   TASK        ST  %MEM   VSZ      RSS   COMM
1234   1     3   ffff88012a003000  IN  25.0  8GB    8GB   java
5678   1     2   ffff88012a004000  IN  15.0  5GB    5GB   python
9012   1     1   ffff88012a005000  IN  10.0  3GB    3GB   node

# 5. Detailed view of large process
crash> vm 1234
PID: 1234   TASK: ffff88012a003000  CPU: 3   COMMAND: "java"
MM               PGD          RSS    TOTAL_VM
ffff88012b000000 ffff88012b001000  8GB    8GB

VMA           START          END     FLAGS FILE
ffff88012c000000 7f0000000000 7f0000800000 877b3b [heap]
ffff88012c001000 7f0000800000 7f0001000000 877b3b [heap]
...

# 6. View OOM killer records
crash> log | grep -A 50 "Out of memory"
```

### Root Cause Analysis

- Memory usage 98%
- java process uses 25% memory
- NORMAL zone nearly exhausted
- Possible memory leak

---

## Case 4: NULL Pointer Dereference

### Symptoms

```
BUG: unable to handle kernel NULL pointer dereference at 0000000000000010
```

### Analysis Steps

```
# 1. View panic information
crash> sys
PANIC: "BUG: unable to handle kernel NULL pointer dereference at 0000000000000010"

# 2. View call stack
crash> bt
#0 __die at ffffffff8105a2b0
#1 exc_page_fault at ffffffff8105b3c0
#2 asm_exc_page_fault at ffffffff81c00bf4
#3 my_driver_ioctl at ffffffff81234560
#4 sys_ioctl at ffffffff81210000

# 3. Disassemble problematic function
crash> dis my_driver_ioctl
0xffffffff81234500 <my_driver_ioctl>:   push   rbp
0xffffffff81234501 <my_driver_ioctl+1>: mov    rbp,rsp
...
0xffffffff81234550 <my_driver_ioctl+80>: mov    rax,QWORD PTR [rdi+0x10]  # Crash point
...

# 4. Expand stack frame to see parameters
crash> bt -f
#3 my_driver_ioctl at ffffffff81234550
    rdi = 0x0000000000000000   # NULL!
    rsi = 0x000000000000abcd

# 5. Confirm structure offset
crash> struct -o my_device
struct my_device {
    [0x0] void *priv;
    [0x8] int state;
    [0x10] struct device *dev;   # +0x10 is the crash offset
}

# 6. Trace where NULL came from
crash> bt -l
#3 my_driver_ioctl at /home/user/my_driver.c:123
crash> list my_driver.devices -s my_driver.device -h my_driver_head
```

### Root Cause Analysis

- The saved fault-time `rdi` is NULL; determine its role from the matching assembly
- Attempting to access `rdi + 0x10` causes page fault
- Trace initialization and object lifetime before choosing a fix; a NULL check alone may hide an earlier defect

---

## Case 5: Stack Overflow

### Symptoms

```
kernel stack overflow (double-fault)
```

### Analysis Steps

```
# 1. Check stack overflow
crash> bt -v
PID: 1234   COMMAND: "worker"   STACK OVERFLOW DETECTED
    stack pointer: ffffc9000011fff0
    stack base:    ffffc90000120000
    stack limit:   ffffc90000124000
    overflow by:   16 bytes

# 2. View call stack depth
crash> bt
#0 recursive_function at ffffffff81234560
#1 recursive_function at ffffffff81234580
#2 recursive_function at ffffffff81234580
...(repeated hundreds of times)
#500 recursive_function at ffffffff81234580

# 3. View stack usage
crash> bt -r
# Compare saved SP with actual stack bounds; output line count is not bytes.

# 4. Check large structures
crash> struct large_context
struct large_context {
    char buffer[4096];
    int data[1024];
    ...
}
SIZE: 8200  # Large relative to this 16KiB stack; verify actual frame allocation

# 5. Check other task stack status
crash> foreach bt -v
```

### Root Cause Analysis

- Too deep recursion
- Or allocating large structures on stack
- Need to change to dynamic allocation or reduce recursion depth

---

## Case 6: Soft Lockup Detection

### Symptoms

```
BUG: soft lockup - CPU#3 stuck for 23s! [kworker/3:1:1234]
```

### Analysis Steps

```
# 1. Check system info and panic reason
crash> sys
PANIC: "soft lockup detected"

# 2. View CPU state at crash
crash> bt -a
CPU 0:
...
CPU 3:   # <-- Stuck CPU
#0 native_queued_spin_lock_slowpath at ffffffff81a12345
#1 queued_spin_lock_slowpath at ffffffff81a13456
#2 _raw_spin_lock at ffffffff81a14567
#3 my_driver_process at ffffffff81234560
PID: 1234   TASK: ffff88012a000000  CPU: 3   COMMAND: "kworker/3:1"

# 3. Check if CPU was spinning in a loop
crash> bt -f 1234
#3 my_driver_process at ffffffff81234560
    rsp: ffffc90000123e00
    rdi: ffff88012b000000   # Lock pointer
    rsi: 0000000000000001   # Locked state

# 4. Examine the lock state
crash> struct spinlock ffff88012b000000
struct spinlock {
  raw_lock = {
    val = {
      counter = 1     # Decode this build's lock bits; not an owner ID
    }
  }
}

# 5. Find references; investigate ownership separately
crash> search -t ffff88012b000000
PID: 5678  TASK: ffff88012a001000  CPU: 2  COMMAND: "thread_B"

# 6. Check thread_B's state
crash> bt 5678
PID: 5678   TASK: ffff88012a001000  CPU: 2   COMMAND: "thread_B"
#0 schedule
#1 schedule_timeout
#2 __mutex_lock_slowpath
#3 mutex_lock
#4 another_function

# 7. Check timer queue
crash> timer
JIFFIES: 4294891234
...
```

### Root Cause Analysis

The spinning stack supports lock contention, but an address search does not
identify the holder of an ordinary spinlock. Establish ownership and ordering
from source and available temporal/lockdep evidence before claiming B slept
with the lock held. If confirmed for a non-sleeping spinlock, that violates
its atomic-context contract. Decode lock types separately on PREEMPT_RT.

### Fix Strategy

```c
// Before: Holding spinlock while sleeping
spin_lock(&my_lock);
down(&semaphore);  // BUG: Can sleep!
spin_unlock(&my_lock);

// Possible restructuring: verify data/lifetime invariants before dropping the lock
spin_lock(&my_lock);
got_value = value;  // Later use must remain valid after dropping the lock
spin_unlock(&my_lock);
down(&semaphore);  // OK: No spinlock held
```

---

## Case 7: Kernel Module (Driver) Crash

### Symptoms

```
BUG: unable to handle kernel paging request at 0000000000000000
RIP: 0010:my_driver_ioctl+0x56/0x100 [my_driver]
```

### Analysis Steps

```
# 1. Check module information
crash> mod
NAME               BASE               SIZE
my_driver          ffffffffa0100000  16384

# 2. View the crash location
crash> bt
#0 __die at ffffffff8105a2b0
#1 exc_page_fault at ffffffff8105b3c0
#2 my_driver_ioctl at ffffffffa0123456 [my_driver]
#3 vfs_ioctl at ffffffff81210000
#4 sys_ioctl at ffffffff81210100

# 3. Disassemble the problematic function
crash> dis my_driver_ioctl
0xffffffffa0123400 <my_driver_ioctl>:    push   rbp
...
0xffffffffa0123456 <my_driver_ioctl+0x56>: mov    (%rax),%rbx  # Crash here

# 4. Check function with source info
crash> bt -l
#2 my_driver_ioctl at /home/user/my_driver.c:234

# 5. Expand stack to see register values
crash> bt -f
#2 my_driver_ioctl at ffffffffa0123456
    rax = 0x0000000000000000   # NULL pointer!
    rbx = 0xffff880123456000
    rcx = 0x0000000000000001

# 6. Check module data structures
crash> struct my_device_data 0xffff880123456000
struct my_device_data {
  lock = {...},
  buffer = 0x0,        # NULL!
  size = 4096,
  ...
}

# 7. List all instances of this module's structures
crash> list my_device.list -s my_device -h my_device_head
ffff880123456000
  lock = {...}
  buffer = 0x0        # Problem: buffer is NULL
  size = 4096
```

### Root Cause Analysis

- `my_device_data.buffer` is NULL
- Code tried to dereference it: `mov (%rax), %rbx` where `rax = 0`
- Initialization failure or an earlier lifetime error remains to be established

### Fix Strategy

```c
// In driver code:
static long my_driver_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
    struct my_device_data *data = filp->private_data;

    if (!data || !data->buffer) {  // Illustrative guard; investigate the invalid state
        pr_err("buffer not allocated\n");
        return -ENOMEM;
    }
    // ... rest of code
}
```

---

## Case 8: Slab Corruption Detection

### Symptoms

```
kernel: Slab corruption (kmalloc-256) detected
kernel: Object 0xffff88012a001000: padding bytes corrupted
```

### Analysis Steps

```
# 1. Check slab information
crash> kmem -i
                 PAGES        TOTAL      PERCENTAGE
TOTAL MEM       8388608      32 GB         ----
FREE            104857       400 MB         1%
...
SLAB            1572864       6 GB        18%

# 2. Find the corrupted slab cache
crash> kmem -S kmalloc-256
CACHE    NAME          OBJSIZE  ALLOCATED  TOTAL  SLABS  SSIZE
ffff88012a000000  kmalloc-256   256       150      200    13    8k

# 3. Examine the corrupted object
crash> rd 0xffff88012a001000 34
ffff88012a001000:  0000000000000001 0000000000000002   ................
...
ffff88012a001100:  deadbeefcafebabe 5a5a5a5a5a5a5a5a   # Suspicious values; not standard redzone proof

# 4. Identify cache membership; allocation history requires separate tracking
crash> kmem 0xffff88012a001000
CACHE: ffff88012a000000  NAME: kmalloc-256
SLAB:  ffff88012a010000
OBJECT: 0xffff88012a001000

# 5. Check adjacent objects for corruption
crash> kmem -S kmalloc-256 | grep -A5 -B5 ffff88012a001

# 6. Search for memory pattern
crash> search -k deadbeefcafebabe
ffff88012a001100: deadbeefcafebabe   # Confirm actual object boundaries and redzone location

# 7. Identify the writer using captured allocation/free/source evidence.
# A kernel slab address in user VMA output cannot establish allocation ownership.
```

### Root Cause Analysis

The earliest allocator report and exact object/redzone boundaries can establish
an overwrite. The displayed magic values and adjacent objects alone do not
identify the writer, prove an overflow, or supply allocation/free history.
Use captured tracking or sanitizer evidence to test those hypotheses.

### Fix Strategy

```c
// Check adjacent allocations
crash> rd 0xffff88012a000e00 20  # Previous object end
crash> rd 0xffff88012a001200 20  # Next object start

// In kernel code, ensure bounds checking
memcpy(dest, src, min(size, allocated_size));
```

---

## Case 9: Interrupt Context Issues

### Symptoms

```
BUG: scheduling while atomic: swapper/0/0/0x00000100
```

### Analysis Steps

```
# 1. Check the crashing process
crash> ps | grep swapper
  0  SW   0.0   0  ffff88012a000000  swapper/0

# 2. View call stack
crash> bt
PID: 0   TASK: ffff88012a000000  CPU: 0   COMMAND: "swapper/0"
#0 __schedule_bug at ffffffff8105a2b0
#1 schedule at ffffffff81a12345
#2 schedule_timeout at ffffffff81a13456
#3 wait_for_completion at ffffffff81a14567
#4 my_interrupt_handler at ffffffff81234560
#5 handle_irq at ffffffff81001234

# 3. Recover preempt state using this build's architecture-specific storage.
# It is not universally a task_struct.preempt_count member.
preempt_count = 0x100   # Decode against matching include/linux/preempt.h and config

# 4. Verify interrupt context
crash> bt -f
#4 my_interrupt_handler
    preempt_count = 0x100   # Does not alone prove hard-IRQ context

# 5. Check the problematic function
crash> dis my_interrupt_handler
...
call wait_for_completion   # BUG: Can sleep in interrupt!
...
```

### Root Cause Analysis

- `wait_for_completion()` can sleep
- Called from interrupt handler (atomic context)
- Kernel detected scheduling attempt with non-zero preempt_count

### Fix Strategy

```c
// Before: Sleeping in interrupt context
irqreturn_t my_interrupt_handler(int irq, void *dev_id)
{
    wait_for_completion(&done);  // BUG!
    return IRQ_HANDLED;
}

// After: Use a sleepable workqueue, not a tasklet/softirq callback
irqreturn_t my_interrupt_handler(int irq, void *dev_id)
{
    schedule_work(&my_work);  // Defer to process context
    return IRQ_HANDLED;
}

void my_work_func(struct work_struct *work)
{
    wait_for_completion(&done);  // OK: Not in interrupt
}
```

---

## Case 10: Double Fault Analysis

### Symptoms

```
PANIC: double fault
```

### Analysis Steps

```
# 1. Check system info
crash> sys
PANIC: "double fault"

# 2. View the crash stack
crash> bt
PID: 1234   TASK: ffff88012a000000  CPU: 0   COMMAND: "test"
#0 double_fault at ffffffff81c01234
#1 ???
#2 ???

# 3. Check stack pointer validity
crash> set
TASK: ffff88012a000000  CPU: 0  COMMAND: "test"
RSP: ffffc90000123fc0   # Check if valid
RBP: 0000000000000000   # Not by itself evidence of corruption

# 4. Examine raw stack
crash> bt -r
stacktop: ffffc90000124000
[...corrupted stack data...]

# 5. Check thread info
crash> struct thread_info ffff88012a000000
struct thread_info {
  flags = 0,
  status = 0,
  ...
}

# 6. Look for stack corruption patterns
crash> rd ffffc90000120000 4096 | grep -v "00000000"

# 7. Check if it's a stack overflow
crash> bt -v
Stack pointer 0xffdf0000 is not in kernel stack range
```

### Root Cause Analysis

A double fault is an exception-delivery failure, not every pair of nested
faults. Inspect the architecture's exception state, stack mappings, and TSS/IST
before choosing between stack overflow, invalid stack, or other delivery errors.

### Common Causes

| Cause | Detection |
|-------|-----------|
| Stack overflow | `bt -v` shows overflow |
| Corrupted RSP | RSP outside valid range |
| Invalid TSS | Check `struct tss_struct` |

---

## Quick Reference: Tool Selection Guide

| Bug Type | Primary Tool | Secondary Tools |
|----------|--------------|-----------------|
| Kernel panic/crash | crash utility | kdump, netdump |
| Deadlock | crash `bt -a`, `search` | lockdep |
| OOM | crash `kmem -i` | memwatch |
| NULL pointer | crash `bt`, `struct`, `dis` | KASAN |
| Stack overflow | crash `bt -v`, `bt -r` | STACKPROTECTOR |
| Soft lockup | crash `bt -a`, `search -t` | lockdep |
| Module crash | crash `mod`, `dis`, `struct` | KASAN |
| Slab corruption | crash `kmem -S`, `rd`, `search` | SLUB debug |
| Interrupt issues | crash `bt`, `struct task_struct` | lockdep |
| Double fault | crash `bt -v`, `bt -r` | KASAN |
| Lock blocked (ARM64) | `bt -f`, `dis -xl`, `rd` | stack analysis (this case study) |
| SLUB UAF | KASAN + `kmem -S` | targeted `slub_debug=P` with lifetime evidence |

---

## Case 11: ARM64 rwsem Lock Derivation from Stack

> **Source**: [Kernel panic 实验室 - Kernel panic 实战之读写锁推导](https://mp.weixin.qq.com/s/szDQ9wOJDwcWo2AStiikPw)

### Symptoms

A task is stuck waiting for a read-write semaphore. A blocked rwsem task alone
does not establish a soft lockup; inspect scheduler/watchdog progress separately.

### Backtrace

```
#0 schedule_preempt_disable at xxxxxx
#1 rwsem_down_write_slowpath at xxxxxx
#2 down_write at xxxxxx
```

The stack localizes a rwsem wait; owner progress and any later panic require
separate evidence.

### Analysis Steps

```console
# === Step 1: Understand FP (x29) vs SP ===
# FP (value in [...]) = function's frame pointer, set at entry
# SP = current stack pointer, changes during function execution
# rwsem_down_write_slowpath's FP from bt = fffffc09c4f3b30

# === Step 2: Find where lock pointer comes from ===
crash> dis -xl down_write
    mov  x0, x19        # x0 = x19 (the rwsem pointer!)
    mov  w1, #0x2
    bl   rwsem_down_write_slowpath
# So x19 holds the rw_semaphore address

# === Step 3: Find where callee saves x19 ===
crash> dis -xl rwsem_down_write_slowpath
    stp  x20, x19, [sp, #176]    # x20 at sp+176; x19 at sp+184
    add  x29, sp, #0x60          # FP = SP + 0x60
# So: SP = FP - 0x60
#     x19 saved at SP + 176 + 8

# === Step 4: Calculate the stack address ===
# FP = 0xfffffc09c4f3b30
# SP = 0xfffffc09c4f3b30 - 0x60 = 0xfffffc09c4f3ad0
# x19 slot = SP + 176 + 8 = 0xfffffc09c4f3ad0 + 0xb8 = 0xfffffc09c4f3b88

# === Step 5: Read x19 from stack ===
crash> rd fffffc09c4f3b88
    fffffc09c4f3b88:  fffff80f78b0b00   # ← This is the lock address!

# === Step 6: Inspect the lock ===
crash> struct rw_semaphore fffff80f78b0b00 -x
struct rw_semaphore {
  count = ...,               # Decode reader/writer/waiter bits using this build
  owner = 0xffff8800abcde000, # Validate owner flags and reader-owned states first
  wait_list = {
    next = 0xffff8800f0000120,
    prev = 0xffff8800f0000120
  },
  ...
}

# === Step 7: Find the owner task ===
crash> task ffff8800abcde000
PID: 5678   TASK: ffff8800abcde000  CPU: 2  COMMAND: "writer_thread"
```

### Root Cause Analysis

- The task is blocked on `rw_semaphore` at `0xfffff80f78b0b00`
- Owner: PID 5678 (`writer_thread`)
- Need to check what owner is doing: `bt 5678`
- If the owner is also waiting, follow dependencies until a proven cycle closes; another wait alone is not ABBA proof

### Why This Technique Works

AArch64 ABI defines `x19-x28` as **callee-saved** registers. This means:
- Caller places argument in `x19` (here: the rwsem pointer)
- If the callee overwrites `x19`, it must preserve the incoming value; identify its actual save location
- Reading the saved value recovers the original argument

This is a **general technique** that works for any function that stores a callee-saved register on the stack.

### x86_64 Equivalent

On x86_64, function arguments are passed in RDI, RSI, RDX, RCX, R8, R9 — but these are **caller-saved** in x86_64 SysV ABI, so they're not preserved across calls.

For x86_64 lock derivation:
- Use `bt -f` for raw frame data, then recover arguments from matching assembly or saved exception state
- Or use `dis -l function` to find the parameter source
- Be aware: with `-fomit-frame-pointer` (common in release builds), manual frame walking may fail

---

## Case 12: SLUB Use-After-Free (Simple and Misalignment Variants)

> **Source**: [Kernel panic 实验室 - Slub use after free 问题讨论](https://mp.weixin.qq.com/s/SmFNmwoz4lr6F7zBi0VQqA)

### Symptoms

```
kernel BUG at lib/list_debug.c:53!
or
slab-out-of-bounds / general protection fault in freelist handling
```

Panic shows `cpu_slab.freelist` is corrupted with an abnormal value, pointing to invalid memory.

### Two Distinct UAF Scenarios

#### Variant 1: Simple UAF (Same Module)

```
1. Module A: kmalloc(object M)         # M is now allocated
2. Module A code 1: kfree(M)            # M returns to freelist
3. Module A code 2: uses M (UAF!)      # M's freepointer is overwritten with data
4. Module A code 2: kfree(M) again     # M is double-freed back to freelist
5. Later: another kmalloc triggers panic
   because cpu_slab.freelist is now garbage
```

**Evidence limit**: A damaged freelist is consistent with a write to freed storage, but intact neighboring fields do not exclude an overflow or another writer.

**Fix**:
```bash
# Enable KASAN to catch UAF at step 3
kasan_multi_shot             # kernel boot parameter for repeated reports
# Or recompile with CONFIG_KASAN=y
```

#### Variant 2: Misalignment UAF (Different Modules)

```
1. Module A: kmalloc(object M)
2. Module A code 1: kfree(M)         # M returns to freelist
3. Module B: kmalloc(...) → system returns M to B
4. Module A code 2: uses stale M    # A overwrites B's current object
5. Module A code 2: kfree(M)         # A incorrectly frees B's current allocation
6. Module B continues using M (already corrupted)
7. Later: kmalloc triggers panic
```

**Why it is harder to detect**: An address-based KASAN check can miss A's
stale access while the same address is validly allocated to B. After A wrongly
frees it, B's later access may trigger a UAF report. The reporting module can
therefore be a victim; detection and attribution depend on the mode and timing.

**Fix**: Enhance slub debug to record **multiple trace paths** (alloc + free from both A and B).

### Analysis Steps

```console
# === Step 1: Check the corrupted slab cache ===
crash> kmem -i
                 PAGES        TOTAL      PERCENTAGE
SLAB            1572864       6 GB        18%
# ↑ Abnormal SLAB size?

# === Step 2: Find the corrupted cache ===
crash> kmem -S kmalloc-256
CACHE    NAME          OBJSIZE  ALLOCATED  TOTAL  SLABS  SSIZE
ffff88012a000000  kmalloc-256   256       150      200    13    8k

# === Step 3: Inspect the corrupted object ===
crash> rd 0xffff88012a001000 34
ffff88012a001000:  0000000000000001 0000000000000002   # Object data OK
...
ffff88012a001100:  deadbeefcafebabe 5a5a5a5a5a5a5a5a   # Suspicious values; not standard redzone proof

# === Step 4: Identify cache membership, not allocation ownership ===
crash> kmem 0xffff88012a001000
CACHE: ffff88012a000000  NAME: kmalloc-256
SLAB:  ffff88012a010000
OBJECT: 0xffff88012a001000

# === Step 5: Search for poison pattern (Variant 2) ===
crash> search -k deadbeefcafebabe
ffff88012a001100: deadbeefcafebabe   # Confirm actual object boundaries and redzone location!

# === Step 6: Obtain allocation/free tracking and source-path evidence ===
# foreach vm cannot identify a module owning a kernel slab allocation.
```

### Root Cause

- **Variant 1**: Same-module lifetime misuse; KASAN may catch an instrumented stale access or invalid free.
- **Variant 2**: A wrongly frees B's active allocation; B may later report UAF, while the original stale access escaped detection.

### Prevention

| Method | Effectiveness |
|--------|--------------|
| `CONFIG_KASAN=y` | Can detect instrumented invalid accesses/frees; mode, reuse, and timing limit coverage |
| `slub_debug=P` bootarg | Enables poisoning/validation; a later allocator check may detect damage, not the writer instruction |
| `slub_debug=u,kmalloc-N` | Records alloc/free trace for specific caches |
| Enhanced slub with multi-trace | Records multiple alloc/free paths (Kernel panic 实验室 方案) |

### Key Insight

> In reuse-related UAF, the reporting module may be a victim. Investigate the captured allocation/free history and source paths; do not infer the writer from the current owner alone.

For slub_debug flags and tracking limits, see `debug-tools-guide.md` §5.

---

## Case 13: GRO Header-Offset Reconstruction from an Oops

**Source:** [Cloudflare — The tale of a single register value](https://blog.cloudflare.com/the-tale-of-a-single-register-value/)
(2021). This is a condensed analysis of the published incident, not a new
reproduction. Offsets below belong to that build only.

### Symptoms and Evidence

Sporadic IPv4-stack faults reached `skb_gso_transport_seglen()`. The available
Oops included a faulting instruction and registers, but not a full vmcore.
The instruction read a byte at `RCX + 0xc`, corresponding to the TCP header's
data-offset field. Disassembly showed that RAX/RSI retained the difference
between the inner and outer transport-header offsets: `0xfeda`.

### Analysis Chain

1. Match the kernel build, symbols, and instruction bytes before interpreting
   offsets. Trace register assignments backwards from the fault; argument
   registers may already have been reused.
2. Map member offsets against that build's `sk_buff` layout. The arithmetic
   suggested a bad header offset, but did not alone exclude prior corruption.
3. Follow the receive/forward path: the published trace included veth polling
   with XDP and GRO aggregation. The author's subsequent controlled tracing
   established the outer transport-header offset as 290 bytes.
4. Combine that additional evidence with the saved difference:

   ```text
   inner offset = 0xfeda + 290 = 65532 = 0xfffc
   attempted byte = skb->head + 0xfffc + 0xc
   ```

   This places the read about 64 KiB beyond the buffer start. The value 290 is
   not derivable from the register difference alone and must not be guessed
   for a different incident.
5. Inspect the GRO completion path. The author found that the inner transport
   offset was not updated, and verified correct offsets after the fix.

### Conclusion and Limits

The source identifies fix `d51c5907e980`, which sets the inner transport-header
offset in TCP/UDP GRO completion. For another kernel, inspect the affected code
and distribution backport before claiming the same defect.

Agents may analyze supplied Oops/disassembly evidence and use the existing
wrapper on offline files. Unsupported layout/GDB queries belong to an
authorized human offline session; do not bypass the wrapper. This case does
not authorize replaying packets, attaching live probes, or reproducing a crash.
If the layout or packet-path evidence is missing, report an offset-corruption
hypothesis rather than a confirmed GRO bug.

---

## Case 14: InfiniBand Allocation Failure and Error-Path Double Free

**Source:** [Red Hat Solution 6407811](https://access.redhat.com/solutions/6407811).
The published vmcore analysis concerns InfiniBand port setup under memory
pressure/fragmentation. Its addresses and structure layouts are build-specific.

### Symptoms and Evidence

A failure while creating InfiniBand port attributes eventually faulted in
`ib_port_release()`. RAX contained the freed-memory poison pattern `0x6b...`.
Earlier kernel messages recorded an allocation failure; slab tracking retained
allocation and release histories for the implicated object.

### Analysis Chain

1. Establish the first allocation failure and the later release fault from the
   timeline. Low memory explains entry into cleanup, not the correctness of
   that cleanup.
2. Decode the faulting load and follow the member accesses through `ib_port`
   and its `pkey_group`. The source recovers the group address from a register
   whose value survives to the faulting instruction.
3. Verify cache membership, object boundaries, and allocation state. A poison
   value is a clue; it does not identify who freed an object or prove a second
   free occurred.
4. Compare available allocation/free tracking records with the source. In this
   incident they point to the port-attribute setup path. If tracking was not
   enabled or pages were filtered, mark the history unavailable.
5. Walk the error exits and callbacks: setup frees `pkey_group`, then a later
   `kobject_put()` invokes the release callback while the group pointer still
   refers to freed storage. The release path uses/cleans that storage again.

### Conclusion and Limits

The evidence supports an error-path lifetime defect in InfiniBand, with memory
pressure as its trigger. The vendor source lists corrected kernel builds;
compare the exact branch/backport rather than applying its version threshold
to every distribution.

Use wrapper triage, bounded memory reads, and symbol disassembly where
supported. Cache/layout/tracking queries beyond the wrapper require an
authorized human offline analysis; preserve returned evidence and access
controls. Do not enable SLUB instrumentation or generate memory pressure as
part of this offline case. A future collection plan requires exact-host/action
authorization, bounded scope, protected output, and rollback; deliberate crash
testing remains human-only.

---

## Case 15: Filesystem Writeback Waiting on Its Own Reclaim Dependency

**Source:** [Red Hat Solution 2973771](https://access.redhat.com/solutions/2973771).
The worked dump uses ext4 on RHEL 7; the vendor discusses the same class of
writeback/reclaim dependency for local filesystems including XFS.

### Symptoms and Evidence

A writer under a memory cgroup remained blocked. Its stack led from filesystem
writeback into allocation, memcg reclaim, and `wait_on_page_bit()`. A blocked
task alone could also indicate slow I/O, so the waited-on object matters.

### Analysis Chain

1. Obtain the blocked stack and identify the allocation/reclaim transition.
   Recover the page argument from the actual disassembly and saved stack slots;
   do not assume a historical R14 or stack offset is valid for another build.
2. Validate the page and its flags. The published page was marked writeback.
   Follow its mapping to `address_space.host` to identify the associated inode.
3. Recover the inode involved in the original filesystem writeback and compare
   identities. In the source analysis, the waited-on page belongs to that inode.
4. Inspect submission ordering to establish the cycle. Equal inode addresses
   alone do not prove that the current task must complete the pending I/O:

   ```text
   prepare filesystem writeback
       -> allocate memory -> memcg reclaim
       -> wait for a page's writeback completion
       -> requires I/O submission by the blocked preparation path
   ```

5. Distinguish this cycle from an already-submitted request waiting on a slow
   device. Missing submission evidence leaves the deadlock hypothesis open.

### Conclusion and Limits

The vendor's analysis establishes a writeback/reclaim dependency cycle and
identifies a corrected RHEL kernel. No mutex-owner cycle is required. For a new
incident, validate page state, mapping, inode identity, and submission ordering
against the captured build before applying that conclusion.

Agents use wrapper `flow-deadlock`, bounded reads, and symbol disassembly on
offline files. Page/mapping/inode traversal unsupported by the wrapper is an
authorized human offline query, not a reason to restore arbitrary interpreter
input. Keep missing or filtered page data unknown. Do not reproduce the hang
or alter cgroup limits, storage, or boot configuration from this case study.

---

## Case 16: ARM64 Single-Bit Pointer-Corruption Hypothesis

**Source:** [一杯linux — 从一段 Kernel 日志，判断 DDR Bit Flip 特征](https://mp.weixin.qq.com/s/HkV9H8FkyRkYW2s0_W6q0w)
(2026-11-10). This summarizes the author's Qualcomm-platform analysis; no
matching dump was analyzed locally. Addresses, offsets, and symbol results
below are observations from that published build.

### Evidence and Reconstruction

The reported PC was `exit_mmap+0x280`, with ESR `0x96000004`, saved X8
`0xffefffd6dd3ea860`, and fault address `0xffefffd6dd3ea868`. The syndrome
indicates a current-EL data abort, level-0 translation fault, and read access.
The faulting instruction word `f9400508` decodes to a 64-bit load using X8
plus eight bytes; therefore:

```text
effective address = 0xffefffd6dd3ea860 + 8
                  = 0xffefffd6dd3ea868
```

The preceding load fetched X8 from the object at X22 plus `0x70`, followed
by a null check. This ties the bad value to an actual pointer use rather than
an incidental register.

The source's same-boot kernel-offset record gives:

```text
runtime image base = 0xffffffc080000000 + 0x165be00000
                   = 0xffffffd6dbe00000
candidate pointer  = 0xffffffd6dd3ea860
observed XOR candidate = 0x0010000000000000 = 1 << 52
```

The author reports that symbol lookup maps the candidate exactly to
`generic_file_vm_ops`, classified `(D)` as data. Together with matching
disassembly, this supports a candidate operations-table pointer. The table
base, the callback slot at base plus eight, and the function pointer stored
in that slot are different values. The reported exception occurs while
reading the slot: the callback was not loaded or invoked by that instruction.

### Conclusion and Limits

The evidence supports a single-bit pointer-corruption hypothesis, not proof
that the candidate was the original value or that DDR caused the change.
For another incident, verify the image bounds, exact symbol and object-member
layout against its matching build; an address above the image base or near a
symbol is insufficient. Preserve the original value and test competing
software, lifetime, and device-write explanations alongside hardware records.
See [the pointer-corruption workflow](evidence-first-workflow.md#511-arm64-single-bit-pointer-corruption-hypotheses).

Agents use existing wrapper operations on offline regular-file dumps.
Unsupported symbol/layout queries and vendor-specific raw-dump loading belong
to an authorized human offline session. Do not bypass the wrapper or reuse
this boot's layout parameters. This case adds no live experiment or memory
repair action.

---

## Additional Resources

- **Crash Utility Whitepaper**: https://crash-utility.github.io/crash_whitepaper.html
- **Crash Utility Documentation**: https://crash-utility.github.io/
- **Crash Help Pages**: https://crash-utility.github.io/help_pages/
- **Linux Kernel Debugging Book**: https://github.com/PacktPublishing/Linux-Kernel-Debugging

---

## Need Deeper Debugging?

For advanced debugging methods beyond crash utility analysis (KASAN, Kprobes, Kmemleak, etc.), refer to `references/debug-tools-guide.md` for guidance on kernel configuration and tool setup.
