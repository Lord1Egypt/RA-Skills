# Kdump 端到端配置指南

> **本文档为 Linux 内核崩溃转储机制的完整配置手册**，覆盖 x86_64 与 ARM64 两种主流架构。引用资料详见 `references/sources.md`。

---

## 1. Kdump 机制原理

### 1.1 双内核架构

Kdump 基于 **kexec** 系统调用实现，运行时使用**两个内核**：

```
+-------------------+         +-------------------+
|   Production      |  panic  |  Capture Kernel   |
|   Kernel (运行中) | ──────> │  (kdump kernel)   |
+-------------------+  kexec  +-------------------+
        │                            │
        │ 保留内存区域                │ /proc/vmcore
        │ (crashkernel 参数)         │ 写入磁盘
        v                            v
   保留的物理内存               vmcore + vmcore-dmesg.txt
   (含 CPU 寄存器、堆栈)
```

**关键路径**：
1. **第一阶段**：Production kernel 启动时，预留一块物理内存给 capture kernel
2. **第二阶段**：Production kernel panic → kexec 跳过 BIOS → 启动 capture kernel
3. **第三阶段**：Capture kernel 通过 `/proc/vmcore`（ELF 格式）将第一阶段内存写出

### 1.2 Kexec 工具链

| 组件 | 位置 | 作用 |
|------|------|------|
| `kexec_load()` 系统调用 | 内核空间 | 加载 capture kernel 到预留地址 |
| `kexec-tools` 用户态工具 | 用户空间 | 传递 capture kernel 地址给生产内核 |
| `purgatory` | 介于两内核之间 | 验证 capture kernel 完整性、桥接硬件状态 |

### 1.3 /dev/oldmem vs /proc/vmcore

| 接口 | 格式 | 用途 |
|------|------|------|
| `/proc/vmcore` | ELF 格式 | 标准方式，含完整 ELF 头，可被 crash/gdb 解析 |
| `/dev/oldmem` | 原始内存 | 旧式接口，需要 ELF header 通过 `elfcorehdr=` 参数传入 |

`/proc/vmcore` 的 ELF header 位置由 `elfcorehdr=` 内核参数传递。**x86 早期 640KB 区域需要特殊处理**。

---

## 2. crashkernel 参数完整语法

> **核心引用**：[kernel.org kdump 文档 §crashkernel syntax](https://docs.kernel.org/admin-guide/kdump/kdump.html#crashkernel-syntax) | [Oracle Linux 9 kdump 文档](https://docs.oracle.com/en/operating-systems/oracle-linux/9/boot/kdump-memory_reservation.html)

### 2.1 语法 1：`crashkernel=size`

```
crashkernel=256M
```

- 内核先在 **low memory** 搜索；失败则降级到 **high memory**
- 若 high memory 成功预留，会自动在 low memory 预留默认 128MB
- ✅ **推荐用法**（用户无需关心平台内存布局）

### 2.2 语法 2：`crashkernel=size@offset`

```
crashkernel=64M@16M       # 64MB 起始于 16MB 物理地址
crashkernel=256M@0        # 64MB 起始于 0（自动放置）
```

- 显式指定起始地址
- **对齐要求**：
  - x86_64：1MB 对齐（CONFIG_PHYSICAL_START=0x1000000 即可）
  - ARM64：**2MiB 对齐**（0x200000）
  - ppc64：32MB

### 2.3 语法 3：`crashkernel=size,high + crashkernel=size,low`

```
# 256M 从 high memory 预留，low memory 用默认值
crashkernel=256M,high

# 显式分别指定
crashkernel=512M,high crashkernel=128M,low

# 禁用 low memory 分配
crashkernel=0,low
```

- 优先从 high memory 预留；high 失败时降级到 low
- 适用于**4G 以上内存**系统，节省宝贵的 low memory
- x86_64 low memory 上限 4G；ARM64 视平台而定（**RPi4=1G，其他多为 4G**）

### 2.4 语法 4：区间语法 `range1:size1[,range2:size2,...][@offset]`

```
crashkernel=512M-2G:64M,2G-:128M
```

含义：
- 内存 < 512M：不预留（rescue 场景）
- 512M ≤ 内存 < 2G：预留 64M
- 内存 ≥ 2G：预留 128M

适用于**预装系统/分销商**的预配置场景。

### 2.5 语法 5：`crashkernel=size,cma`

- 从 CMA（Contiguous Memory Allocator）预留
- ⚠️ 风险：DMA 传输可能损坏 capture kernel 内存
- 仅在**无法承担标准预留**的系统上使用

### 2.6 跨架构推荐配置

| 架构 | 推荐配置 | 备注 |
|------|---------|------|
| x86_64 通用 | `crashkernel=auto` 或 `crashkernel=256M` | 128M 起，复杂模块可加 |
| x86_64 大内存（>4G） | `crashkernel=256M,high` | 节省 low memory |
| ARM64 通用 | `crashkernel=256M` | 256M 起，2MiB 对齐 |
| ARM64 RPi4 | `crashkernel=128M` | low memory 上限 1G |
| ppc64 | `crashkernel=128M@32M` | 32M 起始 |

> **快速估算**：`sudo kdumpctl estimate`（Oracle Linux）或参考 `crashkernel=auto` 自动选择。

---

## 3. 架构特定的 dump-capture kernel 配置

### 3.1 x86 / x86_64 配置

```
CONFIG_CRASH_DUMP=y
CONFIG_HIGHMEM4G=y            # i386 启用
CONFIG_RELOCATABLE=y          # 推荐：可重定位
CONFIG_PHYSICAL_START=0x1000000   # 非可重定位时设为预留区起始
```

dump-capture kernel 启动参数（`kexec -p --append="..."`）：

```
"1 irqpoll nr_cpus=1 reset_devices"
```

| 参数 | 作用 |
|------|------|
| `1` | 进入单用户模式，不启动网络 |
| `irqpoll` | 减少共享中断导致的驱动初始化失败 |
| `nr_cpus=1` | kdump 内核单 CPU 即可 dump（节省内存） |
| `reset_devices` | 重置周边设备到干净状态 |

**使用 bzImage 还是 vmlinux？**
- 可重定位内核 → bzImage/vmlinuz
- 不可重定位 → vmlinux

### 3.2 ARM64 配置

```
CONFIG_CRASH_DUMP=y
```

dump-capture kernel 启动参数：

```
"1 nr_cpus=1 reset_devices"
```

| 参数 | 作用 |
|------|------|
| `1` | 单用户模式 |
| `nr_cpus=1` | 单 CPU |
| `reset_devices` | 设备重置 |
| ⚠️ `kvm` 在非 VHE 系统上**不会被启用**（CPU 在 panic 时不会重置到 EL2）|

**使用 Image 还是 vmlinux？**
- 通常使用 vmlinux 或 Image
- 通过 `kexec -p <image> --initrd=<initrd> --append="..."` 加载

### 3.3 跨架构启动参数对比

| 架构 | 启动参数 |
|------|---------|
| i386 / x86_64 | `1 irqpoll nr_cpus=1 reset_devices` |
| ppc64 | `1 maxcpus=1 noirqdistrib reset_devices` |
| s390x | `1 nr_cpus=1 cgroup_disable=memory` |
| arm | `1 maxcpus=1 reset_devices` |
| arm64 | `1 nr_cpus=1 reset_devices` |

---

## 4. /etc/kdump.conf 详解

> **核心引用**：[Linux 内核之旅 - Kdump 原理与配置](https://mp.weixin.qq.com/s/Nd2Ral3IyqfV0Aa-ZkEanQ)

### 4.1 核心配置项

```bash
# === Dump 目标 ===

# path /var/crash                            # 默认存储路径
#                                         # 实际目录：/var/crash/%HOST-%DATE/
#                                         # 生成两个文件：vmcore 和 vmcore-dmesg.txt
# raw /dev/sda2                             # 直接写入裸设备
# nfs my.nfs.server:/export/dump            # NFS 存储
# ssh user@server                           # SSH 远程传输
#                                        # 拷贝到 <user@server>:<path>/%HOST-%DATE/

# === Dump 动作（失败时）===

# default <reboot | halt | poweroff | shell | mount_root_run_init>
# 转储失败时执行的默认动作

# === Dump 过滤（makedumpfile 级别）===

# core_collector makedumpfile -l --message-level 1 -d 31
# -d 31: 过滤掉所有可丢弃页（0+cache+private+user+free）
# -l:    lzo 压缩
# -c:    zlib 压缩
# -p:    snappy 压缩

# === Kdump 启动配置 ===

# kdump_post /var/crash/scripts/post.sh    # 收集 vmcore 之后执行
# kdump_pre /var/crash/scripts/pre.sh      # 收集 vmcore 之前执行
# extra_bins /usr/bin/gzip                 # initramfs 中包含的额外工具
# extra_modules gfs2                       # 额外加载的内核模块
```

### 4.2 makedumpfile dump level 位图

| 位 | 含义 | 过滤的页 |
|----|------|---------|
| 1 | 排除 zero pages | 全零页 |
| 2 | 排除 cache pages | 缓存页 |
| 4 | 排除 cache private | 私有缓存页 |
| 8 | 排除 user data | 用户数据 |
| 16 | 排除 free pages | 空闲页 |
| 31 | 全部过滤 | 最小化 vmcore |

```
makedumpfile -d 31 -c vmcore vmcore.small   # 最小化
```

### 4.3 服务管理

```bash
# === Systemd 系统（现代发行版）===
sudo systemctl enable kdump
sudo systemctl start kdump
sudo systemctl status kdump

# === SysVinit 系统（RHEL 5/6、CentOS 6）===
chkconfig kdump on
service kdump start
service kdump status

# === 查看预留大小 ===
cat /sys/kernel/kexec_crash_size

# === 查看 capture kernel 是否加载 ===
cat /sys/kernel/kexec_crash_loaded
```

---

## 5. 测试 Kdump

### 5.1 Magic SysRq 触发

> **核心引用**：[Linux 内核之旅 - Kdump 原理与配置](https://mp.weixin.qq.com/s/Nd2Ral3IyqfV0Aa-ZkEanQ)

```bash
echo c > /proc/sysrq-trigger    # 通过 NULL pointer 触发 panic
```

⚠️ 需要内核配置 `CONFIG_MAGIC_SYSRQ=y`。

### 5.2 常用 SysRq 组合

| 键 | 作用 | 破坏性 |
|---|------|-------|
| `c` | 触发 NULL pointer dereference panic（测试 kdump） | 🔴 高（系统会 panic）|
| `f` | 调用 oom_kill 杀掉内存占用最多进程 | 🟡 中（可能杀错进程）|
| `l` | 打印所有 active CPU 的 stack backtrace | 🟢 低 |
| `m` | 打印当前内存使用信息 | 🟢 低 |
| `p` | 打印当前 CPU 寄存器和 flags | 🟢 低 |
| `t` | 打印当前任务列表 | 🟢 低 |
| `s` | 同步所有挂载的文件系统 | 🟡 中（IO 阻塞）|
| `u` | 重新挂载为只读 | 🟡 中 |
| `b` | 立即重启（不 sync）| 🔴 高（数据丢失）|

### 5.3 测试流程

```bash
# 1. 确认 kdump 服务运行
systemctl status kdump

# 2. 验证预留内存已生效
cat /sys/kernel/kexec_crash_size    # 应 > 0
cat /sys/kernel/kexec_crash_loaded # 应为 1

# 3. 触发 panic（⚠️ 会断开会话）
echo c > /proc/sysrq-trigger

# 4. 重启后查看 vmcore
ls -la /var/crash/$(date +%Y%m%d-%H%M%S)/

# 5. 用 crash 分析
crash /usr/lib/debug/lib/modules/$(uname -r)/vmlinux /var/crash/*/vmcore
```

---

## 6. vmcore 后续处理

### 6.1 makedumpfile 高级用法

```bash
# === 压缩 ===
makedumpfile -c vmcore vmcore.zlib   # zlib
makedumpfile -l vmcore vmcore.lzo    # lzo
makedumpfile -p vmcore vmcore.snappy # snappy

# === 过滤 + 压缩 ===
makedumpfile -d 31 -c vmcore vmcore.small

# === 转换为 ELF 格式 ===
makedumpfile -E vmcore.kdump vmcore.elf

# === 分片（用于传输/存储限制）===
makedumpfile --split vmcore part1 part2 part3
makedumpfile --reassemble part1 part2 part3 vmcore

# === 查看信息 ===
makedumpfile -f vmcore

# === 验证完整性 ===
file vmcore
readelf -n vmcore | grep VMCOREINFO
crash --osrelease vmcore
```

### 6.2 跨架构 vmcore 分析准备

> **核心引用**：[VMCOREINFO 官方文档](https://docs.kernel.org/admin-guide/kdump/vmcoreinfo.html) | [Kernel panic 实验室 - crash 关键地址参数](https://mp.weixin.qq.com/s/UPI8j-GacIPFStX_dbNP9Q)

#### x86_64：通常无需额外参数

```bash
# 标准用法
crash vmlinux vmcore

# VMCOREINFO 中 KERNELOFFSET 自动被 crash 读取
# KASLR 启用时由 KERNELOFFSET 处理
```

#### ARM64：必须显式传地址参数

```bash
crash_arm64 \
  -m vabits_actual=39 \
  -m phys_offset=0x80000000 \
  -m kimage_voffset=0xffffffc000000000 \
  -m kaslr=0x80000 \
  vmlinux vmcore
```

**关键参数详解**：

| 参数 | 含义 | 来源 |
|------|------|------|
| `vabits_actual` | 虚拟地址位宽（= VA_BITS） | 内核配置 |
| `phys_offset` | 物理内存基地址 | DTS / 系统设计 |
| `kimage_voffset` | `_text` 虚拟地址 - `_text` 物理地址 | head.S 计算 |
| `kaslr` | KASLR 随机偏移 | = kimage_vaddr - KIMAGE_VADDR |

> 完整推导实例见 `references/arm64-crash-params.md`（新建文件将详述）。

---

## 7. 故障排除

### 7.1 Kdump 触发失败

| 症状 | 排查方向 |
|------|---------|
| panic 后直接重启 | `cat /proc/cmdline` 确认 `crashkernel=` 存在 |
| 重启后没有 vmcore | `journalctl -u kdump` 查看服务日志 |
| vmcore 损坏 | `crash --osrelease vmcore` 验证；用 `makedumpfile -f` 检查 |
| capture kernel 启动失败 | 减小 `crashkernel=` 大小；检查 `reset_devices` 参数 |

### 7.2 内存不足

```bash
# 估算合适大小
sudo kdumpctl estimate    # Oracle Linux
# 或参考：
# 128M  - 最小可用（基础场景）
# 256M  - 标准
# 512M  - 复杂模块（GPU、大文件系统）
# 1G+   - 大内存 + makedumpfile 多线程
```

### 7.3 dump-capture kernel panic

- 添加 `irqpoll` 减少驱动中断问题
- 添加 `reset_devices` 强制设备重置
- 减小 `nr_cpus=1` 减少内存占用
- 检查 initramfs 是否包含必要驱动（`extra_modules` in kdump.conf）

### 7.4 ARM64 特殊问题

- **KASLR 未生效**：`/proc/kallsyms` 与 vmcore 中符号地址对不上
  - 解决：在 `crash_arm64` 命令行加 `-m kaslr=<offset>`
- **non-VHE 系统 kvm 失败**：忽略，kdump 不需要 kvm
- **CMA 内存干扰**：避免使用 `crashkernel=size,cma`

---

## 8. 各发行版差异

### 8.1 RHEL / CentOS / Rocky / AlmaLinux

```bash
# 安装
sudo dnf install kexec-tools crash
sudo dnf install kernel-debuginfo-$(uname -r)

# 配置
sudo kdumpctl reset-crashkernel    # 自动写入 grub
sudo systemctl enable --now kdump

# 测试
sudo kdumpctl test
```

**vmcore 默认位置**：`/var/crash/%HOST-%DATE/`

### 8.2 Ubuntu / Debian

```bash
# 安装
sudo apt install kexec-tools makedumpfile crash linux-crashdump
sudo apt install linux-image-$(uname -r)-dbgsym

# 配置（手动编辑 /etc/default/grub）
GRUB_CMDLINE_LINUX="crashkernel=256M"
sudo update-grub
sudo systemctl enable --now kdump-tools
```

**vmcore 默认位置**：`/var/crash/`

### 8.3 SLES / openSUSE

**vmcore 默认位置**：`/var/log/dump/`

### 8.4 Anolis OS / Alibaba Cloud Linux

类似 RHEL，使用 `dnf` + `kdumpctl`。

---

## 9. 安全与合规

> **重要**：vmcore 文件包含完整内核内存，**可能包含**：
> - 用户进程内存和凭据
> - 加密密钥、密钥派生数据
> - 网络连接数据、密码
> - 业务敏感信息

**最佳实践**：
1. 仅在**隔离/测试环境**分析 vmcore
2. 限制文件访问权限：`chmod 600 vmcore` + `chown root:root`
3. 使用 `makedumpfile -d 31` 过滤用户数据后再分析
4. 处置时使用 `shred -u vmcore` 安全删除
5. 审计所有分析会话以满足合规要求

---

## 10. 速查表

| 任务 | 命令 |
|------|------|
| 启用 kdump | `systemctl enable --now kdump` |
| 测试 kdump | `echo c > /proc/sysrq-trigger` |
| 估算 crashkernel 大小 | `sudo kdumpctl estimate` |
| 自动配置 grub | `sudo kdumpctl reset-crashkernel` |
| 查看预留大小 | `cat /sys/kernel/kexec_crash_size` |
| 查找 vmcore | `ls -lt /var/crash/ \| head` |
| 验证 vmcore | `crash --osrelease vmcore` |
| 过滤 vmcore | `makedumpfile -d 31 -c vmcore vmcore.small` |
| 分析 vmcore（x86_64） | `crash vmlinux vmcore` |
| 分析 vmcore（ARM64） | `crash_arm64 -m vabits_actual=N -m phys_offset=X -m kimage_voffset=Y -m kaslr=Z vmlinux vmcore` |

---

## 11. 参考资料

完整引用列表见 `references/sources.md`，关键源：

- [kernel.org 官方 kdump 文档](https://docs.kernel.org/admin-guide/kdump/kdump.html)
- [kernel.org ARM64 kdump 文档](https://docs.kernel.org/arch/arm64/kdump.html)
- [VMCOREINFO 官方规范](https://docs.kernel.org/admin-guide/kdump/vmcoreinfo.html)
- [Oracle Linux 9 kdump 内存预留](https://docs.oracle.com/en/operating-systems/oracle-linux/9/boot/kdump-memory_reservation.html)
- [Linux 内核之旅 - Kdump 原理与配置](https://mp.weixin.qq.com/s/Nd2Ral3IyqfV0Aa-ZkEanQ)
