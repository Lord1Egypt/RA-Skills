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
  - 内容：VMCOREINFO 完整字段规范，**x86_64 专用 KERNELOFFSET、X86_PAE；ARM64 专用 VA_BITS、kimage_voffset、PHYS_OFFSET、KERNELPACMASK、TCR_EL1.T1SZ**

- **[Crash Utility Whitepaper](https://crash-utility.github.io/crash_whitepaper.html)**
  - 原始缓存：本会话期间 WebFetch 抓取
  - 内容：crash utility 设计白皮书，涵盖所有核心命令

### 1.2 Oracle Linux kdump 文档

- **[Kdump Memory Reservation - Oracle Linux 9](https://docs.oracle.com/en/operating-systems/oracle-linux/9/boot/kdump-memory_reservation.html)**
  - 原始缓存：`.firecrawl/x86-search-3.md`
  - 内容：crashkernel 三种语法的清晰解释（`size`/`size@offset`/`size,high+size,low`），kdumpctl estimate 用法

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

> **特别说明**：以下 7 篇文章来自一线内核工程师 Herbert 的「Kernel panic 实验室」公众号和「Linux 内核之旅」公众号。所有内容均为实战经验总结，具有很高的参考价值。

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

---

## 4. 关键架构对比 (Architecture Comparison)

下表整理 ARM64 与 x86_64 在 kdump/crash 分析中的关键差异，所有字段交叉引用本文档各节。

| 维度 | x86_64 | ARM64 | 主要资料 |
|------|--------|-------|---------|
| crashkernel 推荐语法 | `crashkernel=256M` / `crashkernel=512M-2G:64M,2G-:128M` | `crashkernel=Y[@X]` (X 需 2MiB 对齐) | [§1.1 kernel.org kdump] |
| dump-capture kernel 镜像 | bzImage / vmlinuz（可重定位） | vmlinux / Image | [§1.1] |
| 启动参数 | `1 irqpoll nr_cpus=1 reset_devices` | `1 nr_cpus=1 reset_devices` | [§1.1] |
| KASLR 字段 | `KERNELOFFSET`（VMCOREINFO） | `kaslr_offset`（-m 显式传） | [§1.1 VMCOREINFO] |
| 物理地址转换 | `__START_KERNEL_map` 固定 | `kimage_voffset` 动态 | [§1.1] |
| 调用约定 | RDI/RSI/RDX/RCX/R8/R9 | X0-X7 | [§1.1 / §2.3] |
| 帧指针 | RBP（常被 -fomit-frame-pointer 优化） | FP (x29) 显式保存 | [§2.4 StackOverflow] |
| low memory 上限 | 4G（IA32 兼容） | RPi4=1G，其他多为 4G | [§1.1] |
| 特有 VMCOREINFO 字段 | `X86_PAE`、`KERNEL_IMAGE_SIZE` | `VA_BITS`、`kimage_voffset`、`PHYS_OFFSET`、`KERNELPACMASK`、`TCR_EL1.T1SZ` | [§1.1 VMCOREINFO] |
| SME/PA 加密 | `sme_mask`（AMD SME） | `KERNELPACMASK`（ARM64 PA） | [§1.1] |

---

## 5. 引用统计

| 类别 | 数量 | 状态 |
|------|------|------|
| 官方文档（kernel.org / Oracle） | 4 | ✅ 已抓取 |
| 经典 IBM/技术博客镜像 | 5 | ✅ 关键内容已转述 |
| 微信公众号实战 | 7 | ✅ 全部抓取（7 篇 Kernel panic 实验室 + Linux 内核之旅） |
| crash-utility 邮件列表 | 1 | ✅ 已抓取 |
| 技术问答（StackOverflow） | 2 | ✅ 已抓取 |
| 实战案例（Red Hat / NVIDIA） | 2 | ✅ 已抓取 |
| **合计** | **21** | |

---

## 6. 致谢

特别感谢以下贡献者：

- **Herbert**（Kernel panic 实验室公众号）— 提供了 6 篇高价值的 ARM64 内核调试实战文章
- **zhangskd**（Linux 内核之旅公众号）— 提供了 kdump 系列文章
- **Dave Anderson**、**Alexandr Terekhov** 等 crash-utility 维护者 — 维护了高质量的 crash 工具和邮件列表
- **Baoquan He**（Red Hat）— 编写了官方 ARM64 kdump 文档
