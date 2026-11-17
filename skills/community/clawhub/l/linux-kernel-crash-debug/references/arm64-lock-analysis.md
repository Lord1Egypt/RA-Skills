# ARM64 锁指针与 mutex owner 反推

> Language note: Chinese explanations and original source titles are optional companion material. Follow the user’s preferred language and translate relevant passages when needed; no locale is required.


本文说明任务阻塞在 `mutex_lock()`、`__mutex_lock()` 或 rwsem 慢路径时，如何从 ARM64 反汇编和栈帧恢复锁地址，并继续定位持锁任务。

> 下面的地址和偏移仅用于演示。必须以当前 vmcore 对应的 `vmlinux`、实际反汇编和栈帧为准。

## 目录

1. [统一思路](#1-统一思路)
2. [路径一：从全局地址直接计算锁指针](#2-路径一从全局地址直接计算锁指针)
3. [路径二：从栈中恢复锁指针](#3-路径二从栈中恢复锁指针)
4. [解析 mutex owner](#4-解析-mutex-owner)
5. [验证与易错点](#5-验证与易错点)

## 1. 统一思路

AArch64 调用约定使用 `x0-x7` 传递前八个整数或指针参数。`mutex_lock(struct mutex *lock)` 和 `down_write(struct rw_semaphore *sem)` 的锁指针都是第一个参数，因此先在调用点追踪 `x0`：

```console
crash> bt <pid>
crash> dis -xl <caller>
crash> dis -xl mutex_lock
```

根据调用点选择路径：

- `adrp/add` 直接构造 `x0`：计算全局锁地址。
- `mov x0, x19` 等寄存器传递：寻找 callee 将该寄存器保存到栈上的位置。
- `adrp/ldr`：`ldr` 可能读取“存放在全局变量中的指针”，不要误把全局变量槽地址当作锁对象地址。

## 2. 路径一：从全局地址直接计算锁指针

调用点可能直接构造全局 `struct mutex` 的地址：

```asm
adrp x0, 0xffffffc00ac1e000
add  x0, x0, #0x7f0
bl   mutex_lock
```

`adrp` 得到 4 KiB 对齐的页基址，`add` 补上页内偏移：

```text
lock = 0xffffffc00ac1e000 + 0x7f0
     = 0xffffffc00ac1e7f0
```

直接检查候选对象：

```console
crash> struct mutex 0xffffffc00ac1e7f0 -x
```

使用当前内核的运行时反汇编；不要把另一版本内核、未重定位的静态地址或文章示例中的常数代入 vmcore。

## 3. 路径二：从栈中恢复锁指针

如果调用者把锁地址保存在 callee-saved 寄存器中：

```asm
func_x:
    mov x0, x19
    bl  mutex_lock
```

则锁地址等于调用时的 `x19`。AArch64 ABI 规定 `x19-x28` 为 callee-saved；查找后续函数序言中保存 `x19` 的指令：

```asm
mutex_lock:
    sub sp, sp, #0x30
    stp x29, x30, [sp, #16]
    add x29, sp, #0x10
    stp x20, x19, [sp, #32]
```

假设 `bt` 中该帧的 FP/x29 为 `0xffffffc00804bb70`：

```text
FP = SP + 0x10
SP = 0xffffffc00804bb70 - 0x10
   = 0xffffffc00804bb60
```

`stp` 连续保存两个 64 位寄存器：第一个寄存器 `x20` 在 `sp+32`，第二个寄存器 `x19` 在 `sp+32+8`：

```text
x19 slot = SP + 0x20 + 0x8
         = 0xffffffc00804bb88
```

读取该槽即可恢复锁指针：

```console
crash> rd 0xffffffc00804bb88
```

不要固定套用 `0x10`、`0x20` 或 `x19`。编译器可能选择不同的栈帧大小、寄存器和保存顺序；始终从实际的 `add x29, sp, #N` 与 `stp/str` 指令重新计算。若当前函数没有保存目标寄存器，继续检查相邻调用帧。

## 4. 解析 mutex owner

得到锁地址后读取 `struct mutex`：

```console
crash> struct mutex <lock_addr> -x
```

常见内核版本把 owner task 指针和状态位编码在 `mutex.owner`（通常显示为 `owner.counter`）中。低 3 位通常是 WAITERS、HANDOFF、PICKUP 标志，因此：

```text
owner_task = owner.counter & ~0x7
flags      = owner.counter &  0x7
```

例如：

```text
owner.counter = 0xffffff8083afb601
owner_task    = 0xffffff8083afb600
flags         = 0x1
```

继续检查 owner 及其调用栈：

```console
crash> struct task_struct 0xffffff8083afb600
crash> bt <owner_pid>
```

若 `owner_task == 0`，不要虚构 owner；结合 wait list、锁状态、任务栈和具体内核实现继续分析。不同内核版本的 `struct mutex` 布局或 flag 定义可能变化，可用 `struct mutex`、`whatis mutex` 和对应内核源码确认。

## 5. 验证与易错点

- 确认候选地址是合法、对齐的内核虚拟地址，并能被 `struct mutex` 或 `struct rw_semaphore` 正常解释。
- 核对调用点确实把候选值放入 `x0`；不要只凭某个栈值“看起来像指针”。
- 对 `stp Rt, Rt2, [...]`，`Rt` 位于低地址，`Rt2` 位于低地址加 8 字节。
- 区分十进制偏移和十六进制偏移：反汇编中的 `#32` 等于 `0x20`。
- 先清除 `mutex.owner` 的 flag 位，再把结果解释为 `task_struct *`。
- 找到 owner 后必须执行 `bt <owner_pid>`；owner 的等待链才能区分正常长临界区、资源依赖和 ABBA 死锁。

## 来源

- [Kernel panic之如何通过汇编定位mutex lock指针](https://mp.weixin.qq.com/s/HueZ8rFiOeZ1cwZK1XPHww)，Herbert，Kernel Panic Lab。
- [Kernel panic 实战之读写锁推导](https://mp.weixin.qq.com/s/szDQ9wOJDwcWo2AStiikPw)，Herbert，Kernel Panic Lab。
