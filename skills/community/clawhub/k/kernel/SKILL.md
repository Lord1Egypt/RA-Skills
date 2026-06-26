---
name: Kernel
description: Avoid common Linux kernel mistakes — atomic context violations, allocation failures, and locking traps.
metadata: {"clawdbot":{"emoji":"🐧","os":["linux"]}}
---

## Atomic Context Traps
- `spin_lock` held = cannot sleep — no `kmalloc(GFP_KERNEL)`, no `mutex_lock`, no `copy_from_user`
- Interrupt can take same spinlock — must use `spin_lock_irqsave`, not plain `spin_lock`
- `rcu_read_lock()` section cannot sleep — no blocking calls inside RCU read-side
- `might_sleep()` annotation — add to functions that may sleep, catches bugs with `CONFIG_DEBUG_ATOMIC_SLEEP`

## Allocation Failures
- `GFP_ATOMIC` can return NULL — always check, don't assume success
- `vmalloc` memory not physically contiguous — cannot use for DMA
- `kzalloc` over `kmalloc` — uninitialized memory leaks kernel info to userspace
- Allocation in loop risks OOM — preallocate or use memory pool

## User Pointer Handling
- `copy_from_user` returns bytes NOT copied — 0 means success, not failure
- Never use `%s` with user pointer in printk — kernel crash or info leak
- User memory can change during syscall — copy to kernel buffer, validate the copy
- `__user` annotation is documentation — doesn't enforce anything, you must use copy functions

## Memory Ordering
- `READ_ONCE`/`WRITE_ONCE` for lockless shared data — prevents compiler from caching/reordering
- Spinlock release has implicit barrier — but check-then-act patterns still need care
- `smp_wmb()` before publishing pointer — ensures data visible before pointer is

## Module Error Paths
- Init fails midway — must undo everything already done
- Reverse order cleanup — unregister in opposite order of register
- `goto err_*` pattern standard — cleaner than nested ifs
- Check what's actually initialized — don't free/unregister what wasn't set up

## Locking Mistakes
- Same lock acquired twice = deadlock — even in different functions
- Inconsistent lock ordering — document order, acquire in same sequence everywhere
- `mutex_trylock` returns 1 on success — opposite of `pthread_mutex_trylock`
- Reader-writer locks rarely worth it — contention overhead usually exceeds benefit
