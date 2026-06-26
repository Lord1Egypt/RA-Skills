# ARM64 Crash 命令关键地址参数详解

> **本文档专门解析 ARM64 平台 `crash` 工具启动时需要传递的地址参数**。这些参数是 x86_64 不需要但 ARM64 必须显式提供的。
>
> **核心来源**：[Kernel panic 实验室 - Crash 分析中关键地址参数的含义](https://mp.weixin.qq.com/s/UPI8j-GacIPFStX_dbNP9Q) | [VMCOREINFO 官方文档](https://docs.kernel.org/admin-guide/kdump/vmcoreinfo.html)

---

## 1. 完整命令

```bash
crash_arm64 \
  -m vabits_actual=<VA_BITS> \
  -m phys_offset=<物理基地址> \
  -m kimage_voffset=<VA-PA偏移> \
  -m kaslr=<KASLR随机偏移> \
  vmlinux \
  vmcore@<vmcore起始地址> \
  --kaslr=<KASLR偏移>
```

> ⚠️ **为什么要带这些参数**？crash 需要在 dump 数据中还原代码段、数据段、以及物理/虚拟地址之间的对照关系。没有这些参数，crash 无法正确解析 vmcore。

---

## 2. 四个关键参数

### 2.1 `vabits_actual` — 虚拟地址位宽

**含义**：内核虚拟地址空间的位数。对应内核的 `VA_BITS` 配置。

**典型值**：
- 39（4G 虚拟地址空间）— 主流
- 48（256T 虚拟地址空间）— 高端服务器

**来源**：内核编译配置 `CONFIG_ARM64_VA_BITS=39` 或 `=48`

**举例**：
```bash
crash_arm64 -m vabits_actual=39 ...
```

---

### 2.2 `phys_offset` — 物理内存基地址

**含义**：实际物理内存的起始地址。

**典型值**：
- `0x80000000`（2GB 起始）— 主流 ARM64 SoC
- `0x0`（低端起始）— 较少见

**如何确定**：
- 查看 SoC 参考手册（DDR 控制器映射）
- 或在运行系统中读 `/proc/iomem` 头部的 System RAM 段

**举例**（DDR 物理起始于 0x80000000）：
```bash
crash_arm64 -m phys_offset=0x80000000 ...
```

---

### 2.3 `kimage_voffset` — VA 与 PA 之间的固定偏移

**含义**：内核 `_text` 段虚拟地址与物理地址之间的差值。

**来源**（head.S 中 `__primary_switched` 函数）：

```assembly
adrp    x0, KERNEL_START     // x0 = _text 的物理地址
ldr_l   x4, kimage_vaddr     // x4 = _text 的虚拟地址
sub     x4, x4, x0           // x4 = kimage_vaddr - __pa(_text)
str_l   x4, kimage_voffset, x5
```

**简化公式**：
```
kimage_voffset = __va(_text) - __pa(_text) = kimage_vaddr - phys_of(_text)
```

**为什么需要？**：用于内核虚拟地址 ↔ 物理地址之间的转换。

**典型值**：
- 39 位 VA_BITS：`0xffffffc000000000`（`-2^39` 偏移）
- 48 位 VA_BITS：`0xffff800000000000`（`-2^48` 偏移）

**举例**：
```bash
crash_arm64 -m kimage_voffset=0xffffffc000000000 ...
```

---

### 2.4 `kaslr` / `kaslr_offset` — KASLR 随机偏移

**含义**：内核实际加载的虚拟地址与预期虚拟加载地址之间的差值。

**公式**：
```
kaslr_offset = kimage_vaddr - KIMAGE_VADDR
```

其中：
- `kimage_vaddr = (u64)&_text`（`_text` 段虚拟地址）
- `KIMAGE_VADDR = MODULES_END`（编译时预期虚拟加载地址）

**如何确定**：
```bash
# 在运行系统中：
cat /proc/kallsyms | head -1
# 0000000000000000 T _text   ← KASLR 关闭时

# 或：
sudo dmesg | grep "KASLR"
# [    0.000000] KASLR disabled
# 或带偏移：
# [    0.000000] KASLR offset: 0x80000
```

**举例**（KASLR 偏移 0x80000）：
```bash
crash_arm64 -m kaslr=0x80000 ...
```

**注意**：KASLR 关闭时此值为 0。

---

## 3. 完整推导实例

> **核心引用**：[Kernel panic 实验室 - Crash 分析中关键地址参数的含义](https://mp.weixin.qq.com/s/UPI8j-GacIPFStX_dbNP9Q) 中给出的标准示例。

**场景**：某 ARM64 平台
- `VA_BITS` = 39
- `phys_offset` = `0x80000000`（DDR 物理起始）
- 预期虚拟加载地址 = `0xffffffc080000000`（= `MODULES_END`）
- KASLR 偏移 = `0x80000`

**推导过程**：

```
kimage_vaddr = 0xffffffc080000000 + 0x80000
             = 0xffffffc080080000   ← _text 段虚拟地址
```

`_text` 段物理地址 = `0x80080000`（实际运算得到）

```
kimage_voffset = kimage_vaddr - __pa(_text)
              = 0xffffffc080080000 - 0x80080000
              = 0xffffffc000000000
```

**完整 crash 命令**：
```bash
crash_arm64 \
  -m vabits_actual=39 \
  -m phys_offset=0x80000000 \
  -m kimage_voffset=0xffffffc000000000 \
  -m kaslr=0x80000 \
  vmlinux \
  vmcore
```

---

## 4. ARM64 vs x86_64 参数对比

> **核心引用**：[VMCOREINFO 官方文档](https://docs.kernel.org/admin-guide/kdump/vmcoreinfo.html) 中对两架构的差异说明

| 维度 | x86_64 | ARM64 |
|------|--------|-------|
| 是否需要 `-m` 参数 | ❌ 不需要（VMCOREINFO 自动包含）| ✅ **必须**显式传 4 个参数 |
| KASLR 字段 | `KERNELOFFSET`（在 VMCOREINFO 中）| 需 `-m kaslr=xxx` 手动传 |
| 虚拟地址位宽 | 自动 | 需 `-m vabits_actual=N` |
| 物理地址转换 | `__START_KERNEL_map` 固定 | `kimage_voffset` 动态 |
| 物理基地址 | 通常 0 | 通常 0x80000000 |
| 加密/签名 | `sme_mask`（AMD SME）| `KERNELPACMASK`（ARM64 PA）|

**为什么 ARM64 必须显式传？**

x86_64 的虚拟地址空间布局**相对固定**（`__START_KERNEL_map` 固定映射），VMCOREINFO 中的 `KERNELOFFSET` 一个字段就够 crash 还原。

ARM64 的虚拟地址布局**因平台而异**（VA_BITS 可变、phys_offset 因 SoC 而异），所以需要 4 个独立参数。

---

## 5. 实战：从运行系统获取这些参数

如果能 ssh 到运行系统（不是分析 vmcore），可以这样获取：

```bash
# === vabits_actual ===
zcat /proc/config.gz | grep CONFIG_ARM64_VA_BITS
# 或
uname -m   # 不会显示 VA_BITS，需要从内核 config 推算

# === phys_offset ===
head /proc/iomem
# 00000000-00000fff : reserved
# 80000000-87ffffff : System RAM    ← 物理起始

# === kimage_voffset ===
# 没有 /proc 节点，需要从 vmlinux 反汇编 head.S 中的 __primary_switched 函数
# 或在 crash 中查看（如果有运行系统）：
crash /dev/null /proc/kcore -m vabits_actual=39
crash> p kimage_voffset

# === KASLR offset ===
dmesg | grep -i kaslr
# 或
sudo grep KASLR /var/log/kern.log

# 最简方法：
sudo cat /sys/module/kaslr/parameters/offset 2>/dev/null
# 不存在则 KASLR 关闭（值为 0）
```

---

## 6. 常见问题

### 6.1 "vmcore data checksum error" 或 "invalid vaddr"

**原因**：`vabits_actual` 或 `kimage_voffset` 不正确。

**排查**：
```bash
# 1. 确认内核 config 中的 VA_BITS
zcat /proc/config.gz | grep VA_BITS

# 2. 确认 _text 的虚拟地址
nm vmlinux | grep ' _text$'

# 3. 确认 _text 的物理地址（从 System.map 或 nm 配合 head.S）
```

### 6.2 "page offset is negative" 或符号地址异常

**原因**：`kimage_voffset` 计算错误或 `kaslr` 不正确。

**排查**：使用 [§3 完整推导实例](#3-完整推导实例) 的方法重新计算。

### 6.3 "could not determine kernel text map"

**原因**：`phys_offset` 不正确，或内核 config 与 vmcore 不匹配。

**排查**：
```bash
# 验证 vmlinux 与 vmcore 版本匹配
strings vmlinux | grep "Linux version"
strings vmcore | grep "Linux version"

# 确认 phys_offset
head /proc/iomem
```

### 6.4 KASLR 偏移变化

每次启动 KASLR 都会变化。需要从 vmcore 的 VMCOREINFO 中读取：

```bash
readelf -n vmcore | grep KERNELOFFSET
# x86_64: 0x0 或具体偏移
```

或在 crash 会话中查看：
```bash
crash> sys -i
```

---

## 7. ARM64 VMCOREINFO 关键字段

> **核心引用**：[VMCOREINFO ARM64 节](https://docs.kernel.org/admin-guide/kdump/vmcoreinfo.html#arm64)

| 字段 | 含义 | 与 crash `-m` 对应 |
|------|------|--------------------|
| `VA_BITS` | 虚拟地址最大位数 | `-m vabits_actual=VA_BITS` |
| `kimage_voffset` | VA-PA 偏移 | `-m kimage_voffset=...` |
| `PHYS_OFFSET` | 物理地址起始 | `-m phys_offset=...` |
| `KERNELOFFSET` | KASLR 偏移 | `-m kaslr=...` |
| `KERNELPACMASK` | Pointer Authentication 掩码 | crash 自动使用 |
| `TCR_EL1.T1SZ` | TTBR1_EL1 内存区大小偏移 | crash 自动使用 |
| `MODULES_VADDR/END` | 模块区地址范围 | crash 自动使用 |
| `VMALLOC_START/END` | vmalloc 区 | crash 自动使用 |
| `VMEMMAP_START/END` | vmemmap 区 | crash 自动使用 |

> **未来展望**：部分新版 crash 工具（>= 8.0）会**自动从 VMCOREINFO 读取**这些参数并自动注入 `-m`。如果你的 crash 版本较老，必须手动传。

---

## 8. 一行速查

```bash
# 标准 ARM64 crash 启动（所有参数显式）
crash_arm64 \
  -m vabits_actual=39 -m phys_offset=0x80000000 \
  -m kimage_voffset=0xffffffc000000000 -m kaslr=0x0 \
  vmlinux vmcore

# 验证加载
crash_arm64 ... -m vabits_actual=39 ... vmlinux vmcore
crash> sys -i          # 查看 VMCOREINFO
crash> p kimage_vaddr  # 验证 _text 虚拟地址
crash> vtop <addr>     # 测试地址转换是否正常
```

---

## 9. 参考资料

完整引用列表见 `references/sources.md`，关键源：

- [Kernel panic 实验室 - Crash 分析中关键地址参数的含义](https://mp.weixin.qq.com/s/UPI8j-GacIPFStX_dbNP9Q)
- [VMCOREINFO - The Linux Kernel documentation](https://docs.kernel.org/admin-guide/kdump/vmcoreinfo.html)
- [crashkernel memory reservation on arm64 - kernel.org](https://docs.kernel.org/arch/arm64/kdump.html)
