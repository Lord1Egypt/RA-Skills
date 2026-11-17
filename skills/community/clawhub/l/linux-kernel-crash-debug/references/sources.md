# 参考资料索引 (References Index)

本文件汇总了增强本 skill 时所引用的全部外部技术资料。供读者进一步阅读和溯源。

> **维护说明**：本文件由 `references/` 目录下的所有文档共享。引用时使用相对路径 `references/<file>.md`。

---

## 1. 经典官方文档 (Official Documentation)

### 1.1 kernel.org 官方 kdump 文档

- **[Documentation for Kdump - The kexec-based Crash Dumping Solution](https://docs.kernel.org/admin-guide/kdump/kdump.html)**
  - 文件：`references/kdump-setup-guide.md`（整理后引用）
  - 原始缓存：`.firecrawl/kdump-official.md`
  - 内容：完整 kdump 端到端手册，含 i386/x86_64、ppc64、arm、arm64 四个架构的 dump-capture kernel 配置、crashkernel 三种语法、kexec 加载、sysrq 触发、GDB macros

- **[crashkernel memory reservation on arm64](https://docs.kernel.org/arch/arm64/kdump.html)**
  - 作者：Baoquan He (Red Hat)
  - 原始缓存：`.firecrawl/kdump-arm64-official.md`
  - 内容：ARM64 专属 kdump 内存预留规范，解释 low/high memory 划分（ARM64 上 low memory 上限 RPi4 为 1G，其他多为 4G）

- **[VMCOREINFO - The Linux Kernel Documentation](https://docs.kernel.org/admin-guide/kdump/vmcoreinfo.html)**
  - 原始缓存：`.firecrawl/x86-kaslr.md`
  - 内容：VMCOREINFO 字段规范；`KERNELOFFSET` 可见于 x86_64 与 ARM64 等架构，并非 x86_64 专属。ARM64 的 `VA_BITS` 是构建最大位宽；运行时位宽需结合 TCR_EL1.T1SZ，实际导出键可为 `NUMBER(TCR_EL1_T1SZ)`。

- **[Crash Utility Whitepaper](https://crash-utility.github.io/crash_whitepaper.html)**
  - 原始缓存：本会话期间 WebFetch 抓取
  - 内容：crash utility 设计白皮书，涵盖所有核心命令

### 1.2 Oracle Linux kdump 文档

- **[Kdump Memory Reservation - Oracle Linux 9](https://docs.oracle.com/en/operating-systems/oracle-linux/9/boot/kdump-memory_reservation.html)**
  - 原始缓存：`.firecrawl/x86-search-3.md`
  - 内容：crashkernel 三种语法的清晰解释（`size`/`size@offset`/`size,high+size,low`），kdumpctl estimate 用法

### 1.3 证据优先诊断与现代调试工具

以下资料用于 `references/evidence-first-workflow.md` 和更新后的
`references/debug-tools-guide.md`。本轮通过 Firecrawl 检索并抓取，以当前
kernel.org 文档为主：

- **[Bug hunting](https://docs.kernel.org/admin-guide/bug-hunting.html)**
  - Oops 保存路径、`decode_stacktrace.sh`、GDB 定位和 kdump 证据采集
- **[Tainted kernels](https://docs.kernel.org/admin-guide/tainted-kernels.html)**
  - taint 的持久语义、`kernel-chktaint` 以及各位标志的诊断意义
- **[Ramoops oops/panic logger](https://docs.kernel.org/admin-guide/ramoops.html)**
  - kdump 失败或机器直接复位时，通过持久 RAM 保存 panic/oops 的方案
- **[Magic SysRq](https://docs.kernel.org/admin-guide/sysrq.html)**
  - `l/w/d/m` 现场采集与 `c` 主动触发 crashdump 的官方语义
- **[Softlockup and hardlockup detectors](https://docs.kernel.org/admin-guide/lockup-watchdogs.html)**
  - soft/hard lockup 的不同检测机制、阈值和 panic 控制
- **[KASAN](https://docs.kernel.org/dev-tools/kasan.html)**
  - Generic、ARM64 SW_TAGS/HW_TAGS 三种模式、当前启动参数及 KUnit 测试接口；旧版测试模块名不能直接套用于现代内核。
- **[KFENCE](https://docs.kernel.org/dev-tools/kfence.html)**
  - 面向生产环境的低开销采样式 OOB/UAF/invalid-free 检测
- **[KCSAN](https://docs.kernel.org/dev-tools/kcsan.html)**
  - 基于 watchpoint sampling 的数据竞争检测和 unknown-origin 限制
- **[Kmemleak](https://docs.kernel.org/dev-tools/kmemleak.html)**
  - 扫描算法、clear/scan 用法与 false positive/negative 限制；配置项如 `CONFIG_DEBUG_KMEMLEAK_MEM_POOL_SIZE` 须以匹配版本核对，不照搬旧 `EARLY_LOG_SIZE`。
- **[Lockdep design](https://docs.kernel.org/locking/lockdep-design.html)**
  - lock class、dependency chain、观测范围和故障排查
- **[GDB kernel debugging helpers](https://docs.kernel.org/dev-tools/gdb-kernel-debugging.html)**
  - `vmlinux-gdb.py` 与内核 GDB helper 的官方用法
- **[Verifying bugs and bisecting regressions](https://docs.kernel.org/admin-guide/verify-bugs-and-bisect-regressions.html)**
  - good/bad endpoint 验证、同配置复现和上游回归二分流程
- **[drgn User Guide](https://drgn.readthedocs.io/en/latest/user_guide.html)**
  - 对 live kernel/vmcore 进行可重复 Python 结构遍历和 stack trace 分析
- **[RHEL 10: Analyzing a core dump](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/managing_monitoring_and_updating_the_kernel/analyzing-a-core-dump)**
  - 发行版 debuginfo、partial dump 和 `vmcore-dmesg.txt` 的工程实践

### 1.4 发行版 kdump 管理

- **[Debian `kdump-config(8)`](https://manpages.debian.org/testing/kdump-tools/kdump-config.8.en.html)**
  - `kdump-tools`、`/etc/default/kdump-tools`，以及 `test/show/status` 的准确语义
- **[RHEL 10: Installing kdump](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/managing_monitoring_and_updating_the_kernel/installing-kdump)**
  - `kexec-tools`/`kdump-utils`/`makedumpfile` 包、`/etc/kdump.conf` 和服务管理
- **[RHEL 10: Supported kdump configurations and targets](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/managing_monitoring_and_updating_the_kernel/supported-kdump-configurations-and-targets)**
  - 当前支持的目标与 `failure_action` 等配置；旧版 `default` 指令或动作不能作为跨版本模板。
- **[SLES 15 SP7: Kexec and Kdump](https://documentation.suse.com/sles/15-SP7/html/SLES-all/cha-tuning-kexec.html)**
  - `yast2-kdump`、`/etc/sysconfig/kdump`、`kdump.service`、`KDUMP_SAVEDIR` 与 debuginfo

---

### 1.5 定点取证新打法（2026-10-30，Exa 检索与一手资料核对）

以下补充用于 `debug-tools-guide.md` §8 和 `evidence-first-workflow.md`
§5.2.1；已有 KASAN/KFENCE/KCSAN、SLUB、基础 ftrace 和二分不计为新增方法。

- **[KMSAN](https://docs.kernel.org/dev-tools/kmsan.html)**：未初始化值的 use/store/origin 链、字节范围、平台与插桩限制。
- **[DMA API, Part III: Debugging drivers' use of the DMA-API](https://docs.kernel.org/core-api/dma-api.html)**：`dma-api` 控制与计数、映射/解映射约束，含 scatter-gather 的原始 `nents` 规则。
- **[x86 IOMMU Support](https://docs.kernel.org/arch/x86/iommu.html)**：按设备、地址与原因核对 IOMMU fault；不把架构格式推广到其他平台。
- **[Fault injection infrastructure](https://docs.kernel.org/fault-injection/fault-injection.html)**：`fail-nth` 单线程单 syscall 用法、优先级、能力特定排除项，以及上游 C harness。
- **[Event tracing: triggers](https://docs.kernel.org/trace/events.html)**：`traceoff:1` / `snapshot:1`、条件、计数与移除语法。
- **[ftrace](https://docs.kernel.org/trace/ftrace.html)**：私有 instance、同步 clock、每 CPU 环形缓冲与 snapshot 语义；先设置过滤再启用，`trace_pipe` 会消费记录。
- **[Kprobe-based Event Tracing](https://docs.kernel.org/trace/kprobetrace.html)**：`CONFIG_KPROBE_EVENTS`、追加创建与定点删除事件；对 `kprobe_events` 使用 `>` 会截断现有定义，不能用于共享状态的无差别清理。
- **[RCU stall warnings](https://docs.kernel.org/RCU/stallwarn.html)**：同轮 GP 的 CPU/task、softirq 进度与稳定栈比较，以及 GP kthread 饥饿。

这些是来源核对后的操作方案；本轮未执行活系统插桩、故障注入或内核复现。

### 1.6 ARM64 异常指针与符号判读（2026-11-10 核对）

以下一手资料用于 `case-studies.md` Case 16 与异常指针候选验证约束：

- **[crash sym help](https://crash-utility.github.io/help_pages/sym.html)**：地址查询可返回符号加偏移；结果不单独证明对象身份、类型或边界，须结合精确匹配构建的符号、结构体布局和内存内容验证。
- **[Pointer authentication in AArch64 Linux](https://docs.kernel.org/arch/arm64/pointer-authentication.html)**：PAC 所占高位随虚拟地址宽度和 tagging 配置变化，指令与数据指针的掩码可能不同；文中调试 regset 的 TTBR0 掩码不能用于 TTBR1 内核地址。
- **[Tagged virtual addresses in AArch64 Linux](https://docs.kernel.org/arch/arm64/tagged-pointers.html)**：TBI 忽略的 top byte 为 bits 63:56；不能把 bit 52 差异解释为普通 top-byte tag，也不能据此擅自清位修复指针。
- 复用 §1.1 的 **VMCOREINFO** 官方资料：结合 `KERNELPACMASK`、`TCR_EL1.T1SZ` 等转储元数据核对内核 PAC 与地址宽度，保留原始指针并把规范化候选与原值分开记录。

### 1.7 工具语义与构建相关约束（2026-11-10 核对）

- **[crash manual](https://github.com/crash-utility/crash/blob/master/crash.8)**：原始 RAM 使用 `MEMORY-IMAGE@ADDRESS`，`-S` 选择 `/boot/System.map`，`--no_kallsyms` 控制模块 kallsyms，而非跳过转储完整性检查。
- **[crash 启动选项解析](https://github.com/crash-utility/crash/blob/master/main.c)**、**[ARM64 参数解析](https://github.com/crash-utility/crash/blob/master/arm64.c)**、**[符号重定位](https://github.com/crash-utility/crash/blob/master/symbols.c)**：当前源码支持 ARM64 `--kaslr`；ARM64 `-m` 参数中没有 `kaslr`。源码比未同步架构列表的手册更精确，实际使用仍须核对工具版本与厂商差异。
- **[crash sys help](https://crash-utility.github.io/help_pages/sys.html)**：`sys -i` 是 DMI 字符串，`sys -t` 是 taint 信息；不能分别当成 VMCOREINFO 和 panic 时间，也没有通用的 `sys -n` NMI 查询。
- **[crash bt help](https://crash-utility.github.io/help_pages/bt.html)**、**[crash search help](https://crash-utility.github.io/help_pages/search.html)**：前者展示栈帧数据，后者查找指定值；本 skill 据此要求再结合 ABI、实际反汇编与对象生命周期验证，不能把栈值当成必然完整的入参，也不能把地址命中当成锁 owner 的证明。
- **[crash ps help](https://crash-utility.github.io/help_pages/ps.html)**、**[crash kmem help](https://crash-utility.github.io/help_pages/kmem.html)**：任务表 RSS 与 cache 表 OBJSIZE/ALLOCATED/TOTAL 等列的含义；解析前核对格式与版本，不能把 `ps -G` 解释为内存排序。
- **[APT search 实现](https://github.com/Debian/apt/blob/main/apt-private/private-search.cc)**：`apt-cache search` 的扩展正则使用 `|` 表示候选分支；不能照搬 basic grep 的 `\|` 写法。
- **[makedumpfile manual](https://github.com/makedumpfile/makedumpfile/blob/master/makedumpfile.8.in)**、**[格式检查源码](https://github.com/makedumpfile/makedumpfile/blob/master/makedumpfile.c)**：`-f` 强制覆盖，不是信息检查；ELF 输出不支持其逐页压缩，且 `-E` 不能把已有 kdump-compressed 输入转换为 ELF。
- **[ARM64 memory.h](https://github.com/torvalds/linux/blob/master/arch/arm64/include/asm/memory.h)**、**[内存初始化](https://github.com/torvalds/linux/blob/master/arch/arm64/mm/init.c)**、**[VMCOREINFO 导出](https://github.com/torvalds/linux/blob/master/arch/arm64/kernel/vmcore_info.c)**：区分构建最大 VA 位宽与运行时位宽、镜像与线性映射；`PHYS_OFFSET` 可经对齐和布局调整，不能直接取首段 RAM 地址，`kimage_voffset` 也不能仅由 VA 位宽推定。
- **[kernel sysctl: kptr_restrict](https://docs.kernel.org/admin-guide/sysctl/kernel.html#kptr-restrict)**：内核地址可因访问限制显示为零；这不证明 KASLR 关闭。
- **[Linux preempt.h](https://github.com/torvalds/linux/blob/master/include/linux/preempt.h)**：`preempt_count` 的上下文 mask 与 helper 定义随版本/配置核对，不能把 `0x100` 无条件解释成 hard IRQ 上下文，也不能把 tasklet 当成可睡眠线程。
- **[Linux v6.12 poison.h](https://github.com/torvalds/linux/blob/v6.12/include/linux/poison.h)**：`POISON_FREE`、`POISON_INUSE` 与带架构 delta 的 `LIST_POISON1/2` 是不同模式；匹配源码中的模式值只构成线索，不能单独证明 UAF。
- **[SLAB debugfs files](https://docs.kernel.org/admin-guide/mm/slab.html#debugfs-files)**：`alloc_traces` 与 `free_traces` 的生命周期语义；**[page_owner_sort.c](https://github.com/torvalds/linux/blob/master/tools/mm/page_owner_sort.c)**：输入与输出参数；**[slab.h](https://github.com/torvalds/linux/blob/master/include/linux/slab.h)**：`kmalloc` slab 阈值依赖 `PAGE_SIZE`，不能固定为所有系统的 8 KiB。
- **[GNU Coreutils: shred](https://www.gnu.org/software/coreutils/manual/html_node/shred-invocation.html)**：SSD 磨损均衡、快照及文件系统/存储层副本可保留数据；逐文件覆盖不能保证 vmcore 已从所有副本安全清除。
- **[Claude Code: Skills](https://code.claude.com/docs/en/skills)**：个人 skill 位于 `~/.claude/skills/<名称>/SKILL.md`，可随目录携带支持文件；官方文档未提供 `claude skill install` 命令，安装本 skill 应保留完整运行时目录。

---

## 2. 经典技术文章 (Articles)

### 2.1 IBM developerWorks（中国站，已迁移）

原始 URL（`developerworks/cn/linux/l-cn-kdumpN/`）已 403/404。镜像及内容转述来源：

- **[深入探索 Kdump - 阿里云开发者社区](https://developer.aliyun.com/article/683880)**（原 IBM l-cn-kdump1 镜像）
  - 内容：kexec 系统调用、crashkernel 配置、kexec-tools 工具链、捕获内核启动流程

- **[kdump实现原理 - CSDN](https://blog.csdn.net/faxiang1230/article/details/103782317)**（原 IBM l-cn-kdump1/2 镜像）
  - 内容：kexec_file_load 与 kexec_load 对比，purgatory 机制

- **[Linux内核调试：kdump、vmcore、crash、kernel-debuginfo - 博客园](https://www.cnblogs.com/sky-heaven/p/10415953.html)**（原 IBM dump 分析镜像）
  - 内容：完整 crash 工具使用流程，crash 命令与 gdb 集成

- **[使用 Crash 工具分析 Linux dump 文件 - CSDN](https://blog.csdn.net/zjy900507/article/details/80653249)**
  - 内容：crash 内部命令实战，结构体分析

- **[kdump机制和crash常见使用 - 博客园](https://www.cnblogs.com/muahao/p/9884175.html)**
  - 内容：kdump 端到端配置 + crash 命令实战，结构体成员访问

### 2.2 微信公众号：Kernel panic 实验室（Herbert）

> **特别说明**：以下 8 篇文章来自一线内核工程师 Herbert 的「Kernel panic 实验室」公众号和「Linux 内核之旅」公众号。所有内容均为实战经验总结，具有很高的参考价值。

- **[内核调试工具（一）-Kdump](https://mp.weixin.qq.com/s/Nd2Ral3IyqfV0Aa-ZkEanQ)**
  - 作者：zhangskd（Linux 内核之旅）
  - 原始缓存：`.firecrawl/wechat-1.md`
  - 内容：kexec 双内核原理、crashkernel 配置、kdump.conf、sysrq 触发、capture kernel 加载

- **[Slub use after free 问题讨论](https://mp.weixin.qq.com/s/SmFNmwoz4lr6F7zBi0VQqA)**
  - 作者：Herbert（Kernel panic 实验室）
  - 原始缓存：`.firecrawl/wechat-2.md`
  - 内容：SLUB UAF 两种场景（简单 UAF / 错位 UAF），slub_debug 强化方案

- **[Crash 分析中关键地址参数的含义](https://mp.weixin.qq.com/s/UPI8j-GacIPFStX_dbNP9Q)**
  - 作者：Herbert
  - 原始缓存：`.firecrawl/wechat-3.md`
  - 内容：**ARM64 专用** vabits_actual/phys_offset/kaslr_offset/kimage_voffset 完整推导

- **[Kernel driver 内存泄露问题排查指南](https://mp.weixin.qq.com/s/RER260p6MN5NmymYdyKn0g)**
  - 作者：Herbert
  - 原始缓存：`.firecrawl/wechat-4.md`
  - 内容：meminfo/slabinfo/buddyinfo 三板斧、slub_debug、page_owner、kmemleak 全流程

- **[内核维测之 slub_debug 用法参考](https://mp.weixin.qq.com/s/Chciyg7QHsMeWF3dNwQyBg)**
  - 作者：Herbert
  - 原始缓存：`.firecrawl/wechat-5.md`
  - 内容：slub_debug 完整 f/z/p/u/t 详解，CONFIG_SLUB_DEBUG_ON 行为

- **[Kernel Panic 案例分享之 icache 中的指令跳变](https://mp.weixin.qq.com/s/giO2VvD3zM7VkzH3QIc94Q)**
  - 作者：Herbert
  - 原始缓存：`.firecrawl/wechat-6.md`
  - 内容：cachedump 排查 DDR vs icache 机器码不一致，ARM64 实测案例

- **[Kernel panic 实战之读写锁推导](https://mp.weixin.qq.com/s/szDQ9wOJDwcWo2AStiikPw)**
  - 作者：Herbert
  - 原始缓存：`.firecrawl/wechat-7.md`
  - 内容：从栈回溯推导 x19→rwsem 地址，FP/x29 与 SP 关系，ARM64 调用约定

- **[Kernel panic之如何通过汇编定位mutex lock指针](https://mp.weixin.qq.com/s/HueZ8rFiOeZ1cwZK1XPHww)**
  - 作者：Herbert
  - 原始缓存：`.firecrawl/weixin-HueZ8rFiOeZ1cwZK1XPHww.md`
  - 内容：通过 `adrp/add` 或栈中保存的 x19 恢复 mutex 地址，清除 `owner.counter` 低 3 位后定位持锁 task

### 2.3 crash-utility 邮件列表

- **[Re: [Crash-utility] x86_64: Function parameters from stack frames](https://lists.crash-utility.osci.io/archives/list/devel@lists.crash-utility.osci.io/message/WVR6XCWCIU26EAYIRPGAGE635AIJSEKT/)**
  - 作者：Alexandr Terekhov, Dave Anderson (crash utility 维护者)
  - 日期：2013-07-31
  - 原始缓存：`.firecrawl/x86-frame-mailing.md`
  - 内容：x86_64 栈帧在 crash 中的实际行为，RDI/RSI/RDX 参数展示

### 2.4 其他技术问答

- **[About interrupt context, atomic context and process context](https://stackoverflow.com/questions/22317043/about-interrupt-context-atomic-context-and-process-context-in-linux-kernel)**
  - 原始缓存：`.firecrawl/x86-irq.md`
  - 内容：in_interrupt() 与 preempt_count 原理

- **[What is the purpose of the RBP register in x86_64 assembler?](https://stackoverflow.com/questions/41912684/what-is-the-purpose-of-the-rbp-register-in-x86_64-assembler)**
  - 原始缓存：`.firecrawl/x86-search-2.md`
  - 内容：x86_64 帧指针原理

---

## 3. 实战案例 (Real Cases)

### 3.1 x86_64 案例

- **[Red Hat Solutions 7017534 - Kernel panic with NULL pointer dereference](https://access.redhat.com/solutions/7017534)**
  - 原始缓存：`.firecrawl/x86-null-ptr.md`
  - 内容：bdevname+0x1a RIP NULL 指针 dereference 完整分析

- **[NVIDIA Developer Forum - BUG: unable to handle kernel paging request](https://forums.developer.nvidia.com/t/bug-unable-to-handle-kernel-paging-request-at-0000000000002b20/174591)**
  - 原始缓存：`.firecrawl/x86-oops.md`
  - 内容：GPU 服务器内核分页请求失败案例

### 3.2 crash-utility GitHub

- **[crash-utility/crash GitHub](https://github.com/crash-utility/crash)**
  - 原始缓存：`.firecrawl/x86-search-1.md`
  - 内容：crash utility 官方仓库、help 页面索引

### 3.3 新增证据链案例与诊断约束（2026-10-08 核对）

- **[Cloudflare: The tale of a single register value](https://blog.cloudflare.com/the-tale-of-a-single-register-value/)**
  - 原作者 Jakub Sitnicki，2021-11-03；Case 13：Oops 寄存器差值、sk_buff 布局、GRO 路径和修复后验证。
  - 文中实验补充的信息应与原始 Oops 分开记录；不能把特定构建的偏移用于其他内核。
- **[Red Hat Solution 6407811: slab failures under memory pressure](https://access.redhat.com/solutions/6407811)**
  - Case 14：InfiniBand 分配失败、slab poison、分配/释放记录和 kobject 清理路径的证据链。
- **[Red Hat Solution 2973771: filesystem writeback/reclaim deadlock](https://access.redhat.com/solutions/2973771)**
  - Case 15：从栈恢复 page，经 mapping 定位 inode，结合 I/O 提交顺序证明循环等待。
- **[Guillaume Tucker: Split Kernel #1 – kthread use-after-free](https://gtucker.io/posts/2026-06-23-splitk-no1/)**
  - 原报告者的二分、维护者讨论与修复测试记录；用于区分暴露问题的布局变更和缺陷起源。
- **[Alice Goldfuss: Debugging a Hardware Panic](https://blog.alicegoldfuss.com/debugging-hardware-panic/)**
  - 原作者的 vmcore、NMI 与 ESM/PCIe 事件排查；用于提醒被中断函数不自动等于根因。
  - 原文记录了硬件更换申请，未提供更换后长期验证；不采用其早期 intel_idle 归因。
- **[Linux kernel: Using RCU's CPU Stall Detector](https://docs.kernel.org/RCU/stallwarn.html)**
  - 官方说明慢速 console 和高开销 tracing 可促成 stall；用于采集开销约束。

以上为来源核对与分析方法转述，不代表在本项目中执行过故障复现。涉及生产
主机的原文操作不继承授权；保留离线 wrapper、精确授权和人工崩溃测试边界。

### 3.4 ARM64 单 bit 指针候选案例（2026-11-10 核对）

- **[从一段 Kernel 日志，判断 DDR Bit Flip 特征](https://mp.weixin.qq.com/s/HkV9H8FkyRkYW2s0_W6q0w)**
  - 作者：一杯linux；公众号：Linux调酒师；发布日期：2026-11-10。
  - Case 16：转述原作者从 ARM64 ESR、故障指令、寄存器与 KASLR 信息推导异常指针，并以单 bit 差异提出 `generic_file_vm_ops` 候选的证据链。
  - 原文的符号查询结果须按 §1.6 的语义解释；区分操作表地址、回调槽地址与槽内的函数指针值，偏移须以精确匹配的构建验证。候选命中和单 bit 模式不证明原始指针或 DRAM 故障。
  - 本项目未获得原始转储或精确匹配的 `vmlinux`；这是署名已发表案例的方法转述与算术核对，不是独立复现、内存对象验证或硬件根因确认。

---

## 4. 关键架构对比 (Architecture Comparison)

下表整理 ARM64 与 x86_64 在 kdump/crash 分析中的关键差异，所有字段交叉引用本文档各节。

| 维度 | x86_64 | ARM64 | 主要资料 |
|------|--------|-------|---------|
| crashkernel 推荐语法 | `crashkernel=256M` / `crashkernel=512M-2G:64M,2G-:128M` | `crashkernel=Y[@X]` (X 需 2MiB 对齐) | [§1.1 kernel.org kdump] |
| dump-capture kernel 镜像 | bzImage / vmlinuz（可重定位） | vmlinux / Image | [§1.1] |
| 启动参数 | `1 irqpoll nr_cpus=1 reset_devices` | `1 nr_cpus=1 reset_devices` | [§1.1] |
| KASLR 字段 | `KERNELOFFSET`（VMCOREINFO） | 也可有 `KERNELOFFSET`；人工恢复用经版本核对的 `--kaslr`，不是 `-m kaslr` | [§1.1 VMCOREINFO / §1.7] |
| 物理地址转换 | 分别核对镜像与直接映射 | 镜像用 `kimage_voffset`，线性映射另核对 `PHYS_OFFSET` 等 | [§1.1 / §1.7] |
| 调用约定 | RDI/RSI/RDX/RCX/R8/R9 | X0-X7 | [§1.1 / §2.3] |
| 帧指针 | RBP（常被 -fomit-frame-pointer 优化） | FP (x29) 显式保存 | [§2.4 StackOverflow] |
| low memory 上限 | 4G（IA32 兼容） | RPi4=1G，其他多为 4G | [§1.1] |
| 部分架构相关 VMCOREINFO 字段 | `phys_base`、`KERNEL_IMAGE_SIZE`；`X86_PAE` 属于 x86_32 | `VA_BITS`、`kimage_voffset`、`PHYS_OFFSET`、`KERNELPACMASK`、`TCR_EL1_T1SZ` | [§1.1 VMCOREINFO] |
| 不同用途的掩码 | `sme_mask`（AMD 内存加密） | `KERNELPACMASK`（指针认证，不是内存加密） | [§1.1] |

---

## 5. 历史引用统计

以下保留历史统计快照，不随后续新增来源更新；
完整来源以各节链接为准，避免把历史数量误读为当前总数。

| 类别 | 数量 | 状态 |
|------|------|------|
| 官方文档（kernel.org / Debian / SUSE / Oracle / Red Hat） | 20 | ✅ 已抓取 |
| 上游工具文档（crash / drgn） | 2 | ✅ 已抓取 |
| 经典 IBM/技术博客镜像 | 5 | ✅ 关键内容已转述 |
| 微信公众号实战 | 8 | ✅ 全部抓取（8 篇 Kernel panic 实验室 + Linux 内核之旅） |
| crash-utility 邮件列表 | 1 | ✅ 已抓取 |
| 技术问答（StackOverflow） | 2 | ✅ 已抓取 |
| 实战案例（Red Hat / NVIDIA） | 2 | ✅ 已抓取 |
| **合计** | **40** | |

---

## 6. 致谢

特别感谢以下贡献者：

- **Herbert**（Kernel panic 实验室公众号）— 提供了 7 篇高价值的 ARM64 内核调试实战文章
- **zhangskd**（Linux 内核之旅公众号）— 提供了 kdump 系列文章
- **Dave Anderson**、**Alexandr Terekhov** 等 crash-utility 维护者 — 维护了高质量的 crash 工具和邮件列表
- **Baoquan He**（Red Hat）— 编写了官方 ARM64 kdump 文档

## Offline wrapper security references (v1.4.4)

- [crash rd help](https://crash-utility.github.io/help_pages/rd.html): `rd -r` writes an output file; the wrapper permits only a hexadecimal address and bounded count.
- [crash dis help](https://crash-utility.github.io/help_pages/dis.html): the wrapper permits symbol-only disassembly, without expressions or arbitrary options.
- [crash startup source](https://github.com/crash-utility/crash/blob/master/main.c): documents `--no_crashrc` and startup file handling. The wrapper disables crash rc files and rejects local/home GDB init files.
