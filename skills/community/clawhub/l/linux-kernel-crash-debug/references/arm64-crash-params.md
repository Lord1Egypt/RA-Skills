# ARM64 Crash 命令关键地址参数详解

> Language note: Chinese explanations and original source titles are optional companion material. Follow the user’s preferred language and translate relevant passages when needed; no locale is required.


> **本文档解析 ARM64 平台在 raw RAM、VMCOREINFO 缺失/损坏或旧工具无法自动解析时，`crash` 需要的地址参数**。标准 kdump vmcore 应先尝试 `crash vmlinux vmcore`，因为现代转储会通过 VMCOREINFO 携带这些布局信息。
>
> **核心来源**：[Kernel panic 实验室 - Crash 分析中关键地址参数的含义](https://mp.weixin.qq.com/s/UPI8j-GacIPFStX_dbNP9Q) | [VMCOREINFO 官方文档](https://docs.kernel.org/admin-guide/kdump/vmcoreinfo.html)

---

## 1. 回退命令模板

```bash
crash \
  -m vabits_actual=<运行时VA位宽> \
  -m phys_offset=<物理基地址> \
  -m kimage_voffset=<VA-PA偏移> \
  --kaslr=<已验证的0x十六进制偏移> \
  vmlinux \
  vmcore
```

> ⚠️ **何时要带这些参数**？crash 需要还原代码段、数据段和物理/虚拟地址映射。标准 kdump 通常从 VMCOREINFO 获取；raw dump 或损坏/缺失 VMCOREINFO 时，才需要人工补齐。不要复制另一次启动的数值。
>
> 使用支持目标 ARM64 内核的 `crash` 构建；`crash_arm64` 可能是厂商或本地命名，不是通用命令名。当前上游接受 ARM64 `--kaslr=...`，但 `-m kaslr=...` 不在 ARM64 参数解析器中，会被忽略；旧版或厂商工具须核对其帮助与对应源码，不支持时报告工具能力缺口。原始连续 RAM 块使用上游的 `文件@物理起始地址` 语法，例如 `ddr.bin@0x80000000`，不能把 ELF vmcore 的文件偏移当作物理起始地址。这里的启动与 `crash>` 查询是授权人类的离线参考；代理仍须使用受限 wrapper，不能绕过不支持的查询或输入形式。

---

## 2. 四个关键参数

### 2.1 `vabits_actual` — 虚拟地址位宽

**含义**：转储所属启动实际使用的内核虚拟地址位宽。`CONFIG_ARM64_VA_BITS` / VMCOREINFO 的 `VA_BITS` 表示构建支持的最大位宽，不能总是直接当作 `vabits_actual`；例如支持较大地址空间的构建可能在硬件上回退到较小位宽。

**典型值**：
- 39（2^39 字节可寻址范围）— 常见配置之一
- 48（256T 虚拟地址空间）— 高端服务器

**来源**：优先读取该转储的 VMCOREINFO 和匹配内核实现。上游 crash 使用 `NUMBER(TCR_EL1_T1SZ)`（也兼容旧小写键）计算 `vabits_actual = 64 - T1SZ`。配置、页大小和 CPU 能力用于交叉核对，不替代实际启动数据。

**举例**：
```bash
crash -m vabits_actual=39 ...
```

---

### 2.2 `phys_offset` — 物理内存基地址

**含义**：该启动线性映射使用的物理基准（内核 `PHYS_OFFSET` / `memstart_addr`），不能无条件等同于首段 System RAM 的起始地址。上游可对 `memstart_addr` 做对齐、布局调整和随机化。

**示例值**：某平台可能为 `0x80000000` 或 `0x0`；它们都不是 ARM64 默认值。

**如何确定**：
- 优先读取该转储的 `NUMBER(PHYS_OFFSET)` 或匹配内核的 `memstart_addr`。
- SoC 映射和同一次启动保存的 System RAM 范围只能用于交叉核对，不足以单独推导该值。

**举例**（该启动的 `PHYS_OFFSET` 已确认为 0x80000000）：
```bash
crash -m phys_offset=0x80000000 ...
```

---

### 2.3 `kimage_voffset` — VA 与 PA 之间的固定偏移

**含义**：内核 `_text` 段虚拟地址与物理地址之间的差值。

**来源**：优先读取 VMCOREINFO 的 `NUMBER(kimage_voffset)`；匹配版本的启动汇编也可解释其来源，下面仅示意其运算关系：

```assembly
adrp    x0, KERNEL_START     // x0 = _text 的物理地址
ldr_l   x4, kimage_vaddr     // x4 = _text 的虚拟地址
sub     x4, x4, x0           // x4 = kimage_vaddr - __pa(_text)
str_l   x4, kimage_voffset, x5
```

**简化公式**：
```
kimage_voffset = VA_image(_text) - PA(_text)
```

这里 `VA_image(_text)` 是内核镜像映射中的运行时符号地址；`__va()` 接收物理地址并返回线性映射地址，不能写成 `__va(_text)`。内核源码中的物理符号转换可用匹配版本的 `__pa_symbol(_text)` 理解。

**适用范围**：此差值用于内核镜像映射，不能替代线性映射、vmalloc 或用户地址的完整转换。它同时依赖虚拟布局和镜像物理位置，不能仅从 VA 位宽推出。

**数值辨析**：`0xffffffc000000000` 的 64 位补码值为 `-2^38`，`0xffff800000000000` 为 `-2^47`；这些常数不代表所有 39/48 位内核的 `kimage_voffset`。

**举例**：
```bash
crash -m kimage_voffset=0xffffffc000000000 ...
```

---

### 2.4 `--kaslr` / `kaslr_offset` — KASLR 随机偏移

**含义**：内核实际加载的虚拟地址与预期虚拟加载地址之间的差值。

**验证关系**（比较同一个精确匹配符号）：
```
kaslr_offset = runtime_address(symbol) - link_time_address(symbol)
```

当前上游 ARM64 的 `kaslr_offset()` 使用 `(u64)&_text - KIMAGE_VADDR`，其中 `KIMAGE_VADDR = MODULES_END`。旧内核的符号、镜像头与布局可能不同，应使用对应版本关系；下文用 `kimage_vaddr` 作为 `_text` 运行时地址的示例标签，不假定所有内核都导出同名变量。

**如何确定**：优先读取该转储的 `KERNELOFFSET`，并以精确匹配 `vmlinux` 的未重定位符号地址、该启动的运行时符号与启动日志交叉验证。`KIMAGE_VADDR` 与 `_text` 的具体关系应核对匹配版本源码，不能从另一内核借用基址。

`/proc/kallsyms` 显示零地址可能是地址访问限制，既不说明符号真的位于零，也不证明 KASLR 关闭。缺少 `/sys/module/kaslr/parameters/offset` 或日志中没有匹配行，同样不能证明偏移为零；该 sysfs 路径不是所有内核都有的接口。

**举例**（KASLR 偏移 0x80000）：
```bash
crash --kaslr=0x80000 ...
```

**注意**：KASLR 关闭时此值为 0。

---

## 3. 完整推导实例

> **核心引用**：[Kernel panic 实验室 - Crash 分析中关键地址参数的含义](https://mp.weixin.qq.com/s/UPI8j-GacIPFStX_dbNP9Q) 中给出的标准示例。

**场景**：假设某 ARM64 平台已独立核对以下输入；这里只验证算术，不宣称复现原始转储：
- 构建与运行时 VA 位宽均为 39
- `phys_offset` = `0x80000000`（该启动的 `PHYS_OFFSET`）
- 预期虚拟加载地址 = `0xffffffc080000000`（= `MODULES_END`）
- KASLR 偏移 = `0x80000`

**推导过程**：

```
kimage_vaddr = 0xffffffc080000000 + 0x80000
             = 0xffffffc080080000   ← _text 段虚拟地址
```

本例另行假设已从该启动的证据确认 `_text` 段物理地址 = `0x80080000`；真实分析必须提供该证据，不能仅由 DDR 起始地址和虚拟 KASLR 偏移计算这个物理地址。

```
kimage_voffset = kimage_vaddr - __pa(_text)
              = 0xffffffc080080000 - 0x80080000
              = 0xffffffc000000000
```

**完整 crash 命令**：
```bash
crash \
  -m vabits_actual=39 \
  -m phys_offset=0x80000000 \
  -m kimage_voffset=0xffffffc000000000 \
  --kaslr=0x80000 \
  vmlinux \
  vmcore
```

---

## 4. ARM64 vs x86_64 参数对比

> **核心引用**：[VMCOREINFO 官方文档](https://docs.kernel.org/admin-guide/kdump/vmcoreinfo.html) 中对两架构的差异说明

| 维度 | x86_64 | ARM64 |
|------|--------|-------|
| 是否需要 `-m` 参数 | 通常不需要 | 标准 kdump 通常不需要；raw/元数据损坏时回退到显式参数 |
| KASLR 字段 | `KERNELOFFSET`（在 VMCOREINFO 中）| 同样可有 `KERNELOFFSET`；必要时核对工具支持后用 `--kaslr=0x...` |
| 虚拟地址位宽 | 自动 | 优先读取 VMCOREINFO；必要时 `-m vabits_actual=N` |
| 物理地址转换 | 内核镜像与直接映射分别核对 | 内核镜像用 `kimage_voffset`；线性映射另用 `PHYS_OFFSET` 等 |
| 物理基准 | 从该转储的 `phys_base` 等核对 | 从该转储的 `PHYS_OFFSET` 等核对，无通用常数 |
| 不同用途的掩码 | `sme_mask`（AMD 内存加密）| `KERNELPACMASK`（指针认证，不是内存加密）|

**为什么 ARM64 的回退参数更多？**

x86_64 也需要匹配其页表层级、物理基准等信息，不能认为单个 `KERNELOFFSET` 字段总能恢复所有映射。

ARM64 的虚拟地址布局**因平台和构建而异**（VA_BITS 可变、phys_offset 因 SoC 而异），所以在 VMCOREINFO 不可用时，需要分别恢复这些值。

---

## 5. 实战：优先使用转储所属启动的证据

保存 VMCOREINFO、精确匹配的 `vmlinux` 与配置、启动日志和物理段映射。配置给出支持范围，VMCOREINFO 和该启动的运行时数据给出实际值；分析主机或崩溃后另一启动的 `/proc` 内容不能替代它们。

授权人类在可信离线会话中可查询 `p kimage_voffset`、`p memstart_addr`，并结合匹配源码核对；若初始化所需的值尚未恢复，不能把失败的查询当作独立验证。`/dev/null` 不是符号文件，不应使用 `crash /dev/null /proc/kcore` 伪造输入。代理只使用 wrapper 支持的查询，缺少信息时记录缺口并请求精确的离线人工检查。

---

## 6. 常见问题

### 6.1 "vmcore data checksum error" 或 "invalid vaddr"

**可能原因**：地址布局参数不正确、转储截断或损坏、工具与内核不兼容等；不能仅凭错误文本锁定参数原因。

**排查**：
```bash
# 1. 核对保存的匹配配置，并与运行时 VMCOREINFO 对照
grep CONFIG_ARM64_VA_BITS kernel.config

# 2. 确认 _text 的虚拟地址
nm vmlinux | grep ' _text$'

# 3. 从转储段映射与该启动的元数据确认物理位置
# System.map/nm 仅给出符号值，不能单独恢复运行时物理加载地址
```

### 6.2 "page offset is negative" 或符号地址异常

**可能原因**：`kimage_voffset` 或 KASLR 信息不正确，亦应排查符号不匹配与转储质量。

**排查**：使用 [§3 完整推导实例](#3-完整推导实例) 的方法重新计算。

### 6.3 "could not determine kernel text map"

**可能原因**：`phys_offset` 不正确、符号/配置不匹配、工具不兼容或转储内容缺失。

**排查**：
```bash
# 初筛版本文本；不是精确构建匹配证明，且 strings 不是压缩页解析器
strings vmlinux | grep "Linux version"
strings vmcore | grep "Linux version"

# 再核对该转储的 PHYS_OFFSET 与物理段映射
# 不要用分析主机当前的 /proc/iomem 代替
```

### 6.4 KASLR 偏移变化

KASLR 偏移可能随启动变化，也可能重复；每份转储都要独立核对。ELF vmcore 可先检查其 VMCOREINFO note：

```bash
readelf -n vmcore
```

压缩的 kdump 文件不是 ELF，不能直接套用 `readelf`。使用支持其格式的工具读取元数据；`crash> sys -i` 显示 DMI 字符串，不是 VMCOREINFO。注意 `readelf -n` 的展示格式可能将 note 描述按十六进制显示，`grep` 没有命中不等于该字段不存在。

---

## 7. ARM64 VMCOREINFO 关键字段

> **核心引用**：[VMCOREINFO ARM64 节](https://docs.kernel.org/admin-guide/kdump/vmcoreinfo.html#arm64)

| 字段 | 含义 | crash 中的用途或回退参数 |
|------|------|--------------------|
| `VA_BITS` | 构建支持的虚拟地址最大位数 | 不能无条件赋给 `vabits_actual` |
| `kimage_voffset` | VA-PA 偏移 | `-m kimage_voffset=...` |
| `PHYS_OFFSET` | 该启动线性映射的物理基准 | `-m phys_offset=...` |
| `KERNELOFFSET` | KASLR 偏移 | 核对工具支持后用 `--kaslr=0x...` |
| `KERNELPACMASK` | Pointer Authentication 掩码 | crash 自动使用 |
| `NUMBER(TCR_EL1_T1SZ)` | TCR_EL1.T1SZ，运行时 TTBR1_EL1 区域大小偏移 | `vabits_actual = 64 - T1SZ` |
| `MODULES_VADDR/END` | 模块区地址范围 | crash 自动使用 |
| `VMALLOC_START/END` | vmalloc 区 | crash 自动使用 |
| `VMEMMAP_START/END` | vmemmap 区 | crash 自动使用 |

> `crash` 和 `makedumpfile` 会消费 VMCOREINFO。只有工具无法解析、元数据缺失/损坏或输入不是标准 kdump vmcore 时，才走人工参数恢复流程。
> 不同版本导出的字段不同；表中地址范围使用便于阅读的简称，必须核对转储中实际存在的 `NUMBER(...)` 键，不能假定所有字段均有。

---

## 8. 一行速查

```bash
# 标准 kdump vmcore：先让 crash 读取 VMCOREINFO
crash vmlinux vmcore

# raw/元数据损坏场景：显式恢复参数
crash \
  -m vabits_actual=39 -m phys_offset=0x80000000 \
  -m kimage_voffset=0xffffffc000000000 --kaslr=0x80000 \
  vmlinux vmcore

# 验证加载
crash ... -m vabits_actual=39 ... vmlinux vmcore
crash> sys            # 核对内核版本与 panic 上下文
crash> sym _text      # 核对重定位后的 _text 符号地址
crash> vtop <addr>     # 测试地址转换是否正常
```

---

## 9. 参考资料

完整引用列表见 `references/sources.md`，关键源：

- [Kernel panic 实验室 - Crash 分析中关键地址参数的含义](https://mp.weixin.qq.com/s/UPI8j-GacIPFStX_dbNP9Q)
- [VMCOREINFO - The Linux Kernel documentation](https://docs.kernel.org/admin-guide/kdump/vmcoreinfo.html)
- [crashkernel memory reservation on arm64 - kernel.org](https://docs.kernel.org/arch/arm64/kdump.html)
- [crash ARM64 参数解析器](https://github.com/crash-utility/crash/blob/master/arm64.c)
- [crash 启动选项解析器](https://github.com/crash-utility/crash/blob/master/main.c)
- [ARM64 地址宏与映射转换](https://github.com/torvalds/linux/blob/master/arch/arm64/include/asm/memory.h)
- [ARM64 VMCOREINFO 导出](https://github.com/torvalds/linux/blob/master/arch/arm64/kernel/vmcore_info.c)
