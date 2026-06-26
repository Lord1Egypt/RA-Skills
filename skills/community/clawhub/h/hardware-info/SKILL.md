---
name: hardware-info
description: |
  全面查询电脑硬件信息。当用户询问"电脑配置"、"硬件信息"、"系统信息"、"查看配置"、"电脑什么配置"、"硬件详情"、"设备信息"、"查看硬件"、"系统配置"、"电脑型号"、"CPU信息"、"内存多大"、"硬盘多大"、"显卡信息"等时触发。
  
  支持 macOS、Linux 和 Windows 系统，自动检测平台并使用对应命令获取全面的硬件信息，包括：
  - 系统概览（型号、序列号、操作系统）
  - CPU 信息（型号、核心数、架构、频率）
  - 内存信息（总容量、类型、频率、插槽）
  - 存储设备（硬盘/SSD 容量、型号、SMART状态、分区）
  - 显卡/GPU（型号、显存、分辨率）
  - 显示器（分辨率、刷新率、类型）
  - 网络设备（网卡、MAC地址、接口）
  - 电池信息（健康度、循环次数、容量）- 笔记本
  - USB/雷电设备
  - 蓝牙设备
  - 传感器/温度（如可用）
  - 实时状态（CPU负载、内存使用、磁盘使用）
---

# Hardware Info - 全面硬件信息查询

全面查询电脑硬件配置信息，支持 macOS、Linux 和 Windows。

## 使用方法

当用户询问硬件信息时，直接调用此 skill，无需询问具体要查什么，一次性提供全面的硬件概览。

## 信息收集策略

### macOS 系统

使用以下命令组合获取完整信息：

**1. 系统概览**
```bash
system_profiler SPHardwareDataType -json
```
获取：机型、序列号、处理器、内存、UUID、激活锁状态等

**2. CPU 详细信息**
```bash
sysctl -a | grep -E "(hw\.|machdep\.)"
```
获取：CPU型号、核心数、线程数、缓存、架构等

**3. 内存信息**
```bash
system_profiler SPMemoryDataType -json
vm_stat
sysctl hw.memsize
```
获取：内存容量、类型、频率、使用情况

**4. 存储设备**
```bash
system_profiler SPNVMeDataType SPStorageDataType SPSerialATADataType -json
diskutil list
df -h
```
获取：SSD/HDD型号、容量、协议、SMART状态、分区、使用情况

**5. 显卡和显示器**
```bash
system_profiler SPDisplaysDataType -json
```
获取：GPU型号、显存、显示器分辨率、刷新率

**6. 网络设备**
```bash
networksetup -listallhardwareports
ifconfig
system_profiler SPNetworkDataType -json
```
获取：网卡、MAC地址、接口类型

**7. 电池信息（笔记本）**
```bash
# 主要电池信息（JSON格式）
system_profiler SPPowerDataType -json

# 简要电池状态
pmset -g batt

# 详细电池数据（包括循环次数、温度、设计容量等）
ioreg -r -c "AppleSmartBattery" -d 1

# 提取关键信息
ioreg -l -w0 | grep -E "(CycleCount|DesignCapacity|MaxCapacity|CurrentCapacity|Temperature|ExternalConnected|FullyCharged)"
```
获取：电池健康度、循环次数、剩余容量、设计容量、当前容量、温度、充电状态、电源连接状态

**8. USB/雷电设备**
```bash
system_profiler SPUSBDataType SPThunderboltDataType -json
ioreg -p IOUSB -w0
```

**9. 蓝牙设备**
```bash
system_profiler SPBluetoothDataType -json
```

**10. 实时状态**
```bash
top -l 1 -n 0
sysctl vm.loadavg
```
获取：CPU负载、内存压力、进程数

### Linux 系统

**1. 系统概览**
```bash
hostnamectl
uname -a
cat /etc/os-release
```

**2. CPU 信息**
```bash
cat /proc/cpuinfo
lscpu
```

**3. 内存信息**
```bash
cat /proc/meminfo
free -h
dmidecode -t memory
```

**4. 存储设备**
```bash
lsblk -f
fdisk -l
smartctl -a /dev/sda
df -h
```

**5. 显卡信息**
```bash
lspci | grep -i vga
lspci | grep -i nvidia
nvidia-smi
```

**6. 网络设备**
```bash
ip addr
lspci | grep -i net
```

**7. 传感器/温度**
```bash
sensors
```

### Windows 系统

**1. 系统概览**
```powershell
Get-ComputerInfo
systeminfo
```

**2. CPU 信息**
```powershell
Get-WmiObject -Class Win32_Processor
```

**3. 内存信息**
```powershell
Get-WmiObject -Class Win32_PhysicalMemory
```

**4. 存储设备**
```powershell
Get-PhysicalDisk
Get-Disk
Get-Partition
```

**5. 显卡信息**
```powershell
Get-WmiObject -Class Win32_VideoController
```

## 输出格式

以结构化的 Markdown 格式呈现，包含以下章节：

```markdown
## 🖥️ 系统概览
- 型号: xxx
- 序列号: xxx
- 操作系统: xxx

## ⚡ 处理器 (CPU)
- 型号: xxx
- 架构: xxx
- 核心/线程: x/x
- 频率: x GHz

## 💾 内存 (RAM)
- 总容量: xx GB
- 类型: xxx
- 频率: xxx MHz
- 使用情况: xx%

## 💽 存储设备
### 磁盘 1
- 型号: xxx
- 容量: xxx GB
- 类型: SSD/HDD
- 健康状态: xxx

## 🎮 显卡/显示器
### GPU
- 型号: xxx
- 显存: xx GB

### 显示器
- 分辨率: xxx
- 刷新率: xx Hz

## 🌐 网络设备
- Wi-Fi: xxx (MAC: xx:xx:xx:xx:xx:xx)
- 以太网: xxx

## 🔋 电池（笔记本）
- 健康状态: xxx (Good/Fair/Poor)
- 最大容量: xx%
- 循环次数: xxx / 设计寿命 xxx
- 设计容量: xxx mAh
- 当前容量: xxx mAh
- 剩余电量: xx%
- 充电状态: 充电中/已充满/未充电
- 电源连接: 是/否
- 电池温度: xx°C

## 📊 实时状态
- CPU 负载: x%
- 内存使用: xx%
- 磁盘使用: xx%
```

## 执行流程

1. **检测操作系统**: 使用 `uname -s` 或 `platform` 命令
2. **并行收集**: 使用 `&` 后台执行多个命令提高效率
3. **解析输出**: 将命令输出转换为结构化数据
4. **格式化呈现**: 生成易读的 Markdown 报告

## 注意事项

- 某些命令可能需要管理员权限（如 `smartctl`）
- 部分信息可能因系统配置不同而无法获取
- 传感器数据需要安装相应驱动（如 `lm-sensors`）
- 笔记本电池信息仅在电池存在时显示
- 电池温度单位转换：ioreg 输出的温度单位为 0.01°C（如 2986 = 29.86°C）
- 部分电池数据需要从 ioreg 的原始输出中提取和计算
- 如遇到权限问题，尝试使用 `sudo`

## 示例查询

用户可能会这样询问：
- "帮我看看电脑配置"
- "这台电脑什么配置？"
- "查看硬件信息"
- "我的 Mac 是什么型号？"
- "内存多大？"
- "硬盘还剩多少空间？"
- "显卡是什么型号？"

对于所有这些查询，都使用此 skill 提供全面的硬件信息报告。
