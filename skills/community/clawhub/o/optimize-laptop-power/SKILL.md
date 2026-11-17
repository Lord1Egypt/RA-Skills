---
name: Optimize-Laptop-Power
description: Windows power-saving reference guide with verifiable commands for balanced plan, Defender tuning, and SysMain.
version: 1.3.0
author: PJ-Model
tags:
  - windows
  - power
  - optimization
  - reference
allowed-tools: []
---

# Optimize-Laptop-Power

Windows 笔记本电源优化参考指南。本 Skill **不会自动执行任何操作**，所有命令需由用户自行在管理员 PowerShell 中确认和执行。

> **⚠️ 重要提示：本 Skill 是参考指南，不是自动化脚本。**
> 所有命令均需用户手动复制粘贴、并理解其影响后再执行。
> 执行本 Skill 的任何操作即代表你已了解并接受相关风险。

---

## 本 Skill 范围

本参考指南覆盖以下内容：

| 阶段 | 类别 | 具体操作 | 影响范围 |
|:----:|------|---------|---------|
| 🔍 诊断 | 电池 | 查看电池容量退化、健康度、当前放电速率 | 只读查询 |
| 🔍 诊断 | 进程 | 分析高内存/高CPU的耗电应用 | 只读查询 |
| 🔌 优化 | 电源 | 切换系统内置电源计划 | 修改电源方案 |
| 🛡️ 优化 | 安全 | Defender 排除路径 | 降低特定目录的扫描频率 |
| 🛡️ 优化 | 安全 | Defender 扫描策略 | 修改实时保护的文件扫描范围 |
| ⚙️ 优化 | 服务 | 禁用 SysMain (Superfetch) | 修改系统服务启动类型 |

### 哪些不属于本 Skill 范围

- ❌ 不做任何自动化执行（所有命令需手动粘贴运行）
- ❌ 不修改注册表、不安装第三方软件
- ❌ 不收集、不上传任何用户数据
- ❌ 不会自动检测你的目录或文件路径
- ❌ 不修改网络、防火墙、用户账户控制等安全设置

---

## 安全与权限

⚠️ **执行前请确认**：

1. **所有命令都需管理员权限** — 以管理员身份打开 PowerShell（右键 → 以管理员身份运行）
2. **Defender 排除路径必须由你亲自指定路径** — AI 不应代为猜测
3. **每一条命令的效果你都已理解** — 不要盲目复制粘贴
4. **保留当前电源计划 GUID** — 用 `powercfg /list` 查看，记下当前激活的 GUID 以备恢复
5. **恢复方法已附在文末** — 任何时候想撤销都能恢复

---

## 第一部分：🔍 诊断 — 先看现状，再决定优化

**在动手优化之前，必须先做诊断。** 以下是三个诊断步骤，按推荐顺序执行。

### 1.1 电池健康度检测

```powershell
$battery = Get-WmiObject -Namespace root/wmi -ClassName BatteryFullChargedCapacity
$design = Get-WmiObject -Namespace root/wmi -ClassName BatteryStaticData
$pct = [math]::Round($battery.FullChargedCapacity / $design.DesignedCapacity * 100, 1)
Write-Output "设计容量: $($design.DesignedCapacity) mWh"
Write-Output "当前满充: $($battery.FullChargedCapacity) mWh"
Write-Output "电池健康度: $pct%"
```

**解读：**
- 健康度 ≥ 90% → 电池状态良好，软件优化足够
- 健康度 80-90% → 正常老化，建议执行电源优化
- 健康度 60-80% → 建议执行全部优化项
- 健康度 < 60% → 软件优化效果有限，优先考虑更换电池

### 1.2 当前放电速率与功耗基线

```powershell
$status = Get-CimInstance -Namespace root/wmi -ClassName BatteryStatus
Write-Output "当前连接电源: $($status.PowerOnline)"
Write-Output "剩余容量: $($status.RemainingCapacity) mWh"
Write-Output "当前放电速率: $($status.DischargeRate) mW ($([math]::Round($status.DischargeRate/1000, 1)) W)"
```

**典型参考值**（笔记本不插电时）：
- **3-5W**：轻度办公（文字处理、网页浏览）— 优秀
- **6-10W**：中度使用（多标签页、IDE、聊天工具）— 正常
- **11-15W**：重度使用（编译、虚拟机、GPU负载）— 需要关注
- **>15W**：高功耗，建议查找异常进程

### 1.3 主要耗电应用分析

执行以下两段命令，分别查看**内存占用 TOP 15** 和 **CPU 占用 TOP 15** 的进程：

```powershell
# 内存消耗 TOP 15
Write-Output "===== 内存消耗 TOP 15 ====="
Get-Process | Where-Object { $_.WorkingSet64 -gt 50MB } | Sort-Object WorkingSet -Descending | Select-Object -First 15 Name, @{N='MemMB';E={[math]::Round($_.WorkingSet64/1MB,1)}}, @{N='CPUs';E={[math]::Round($_.TotalProcessorTime.TotalSeconds,0)}} | Format-Table -AutoSize

# 各应用总内存（同类进程合并）
Write-Output "===== 按应用汇总 ====="
Get-Process | Group-Object Name | Sort-Object {($_.Group | Measure-Object WorkingSet64 -Sum).Sum} -Descending | Select-Object -First 10 Name, Count, @{N='TotalMemMB';E={[math]::Round(($_.Group | Measure-Object WorkingSet64 -Sum).Sum/1MB,1)}} | Format-Table -AutoSize

# GPU 使用情况
Write-Output "===== GPU 功耗（如有NVIDIA显卡）====="
nvidia-smi --query-gpu=power.draw,temperature.gpu,utilization.gpu,memory.used --format=csv,noheader,nounits 2>$null
```

**解读结果的关键点：**
- **某个浏览器（chrome/edge/firefox）总内存 > 2GB** → 说明打开了太多标签页，是首要优化对象
- **聊天工具（weixin/WeChatAppEx）总内存 > 1GB** → 子进程过多，可考虑退出多余实例
- **防病毒软件（MsMpEng）CPU > 500秒** → Defender 实时扫描频繁，建议加排除路径
- **数据库服务（mysqld）内存 > 300MB 且不在使用中** → 可考虑按需启动
- **NVIDIA 驱动多个进程 > 200MB 合计** → 可关闭 NVIDIA Share（GeForce Experience 覆盖层）

---

## 第二部分：🔌 优化 — 根据诊断结果按需执行

完成诊断后，根据你看到的实际情况选择需要执行的优化项。

### 🔋 优化 1：切换电源计划

**适合的情况**：诊断显示当前电源计划是"高性能"（通常 GUID 包含 `8c5e7fda`）
**影响**：仅修改电源方案，不涉及安全策略，可随时切换回原计划。

```powershell
# 先查看当前有哪些电源计划
powercfg /list

# 切换到「平衡」计划（推荐）
powercfg /s 381b4222-f694-41f0-9685-ff5bb260df2e

# 或切换到「节能」计划（更省电但性能有牺牲）
powercfg /s a1841308-3541-4fab-bc81-f71556f20b4a
```

### 🛡️ 优化 2：Defender 排除路径

**适合的情况**：诊断显示 MsMpEng CPU > 500秒 或 内存 > 300MB
**影响**：Defender 将跳过指定目录的实时扫描。**注意这是安全让步**——排除目录内的文件若被写入恶意代码，Defender 不会实时拦截。

⚠️ **路径必须由你亲自填入，不要依赖 AI 猜测。**

```powershell
# 替换为你自己的目录后执行
Add-MpPreference -ExclusionPath "D:\YourAIProjects"
Add-MpPreference -ExclusionPath "C:\Users\YourName\.openclaw"
Add-MpPreference -ExclusionPath "C:\Users\YourName\.npm"

# 查看已添加的排除路径
Get-MpPreference | Select-Object -ExpandProperty ExclusionPath
```

**推荐排除哪些目录？**
- 大模型 / AI 工具数据目录（如 HuggingFace cache、LLM 模型文件）
- OpenClaw 工作目录（`~/.openclaw`）
- npm、pip、conda 等包管理器缓存目录
- 你自己编写的、知根知底的代码仓库目录
- **不要排除**系统目录（`C:\Windows`、`C:\Program Files`）、下载目录、临时文件目录

### 🛡️ 优化 3：调整 Defender 实时扫描激进度

**适合的情况**：诊断显示 MsMpEng 持续高 CPU，且已加了排除路径但仍然偏高
**影响**：从"监控所有文件操作"降为"仅监控写入/传入文件"。打开文件时不扫描，降低磁盘 I/O。

```powershell
Set-MpPreference -RealTimeScanDirection 1
```

| 参数值 | 含义 | 安全影响建议 |
|--------|------|------------|
| 0 | 监控所有文件操作（默认） | ✅ 对安全敏感的用户保持默认 |
| **1** | **仅监控传入/写入文件** | ⚠️ 省电推荐，风险可控 |
| 4 | 仅监控传出文件 | ❌ 风险较高，不推荐 |
| 5 | 传出+传入 | ⚠️ 次低选项 |

### ⚙️ 优化 4：禁用 SysMain (Superfetch)

**适合的情况**：诊断确认硬盘为 SSD
**影响**：禁用后系统不再后台预缓存应用到内存。**仅 SSD 用户建议操作**，机械硬盘用户请跳过。

```powershell
# 先确认你的硬盘类型
Get-PhysicalDisk | Select-Object FriendlyName, MediaType

# 如果显示 SSD，可以执行：
Stop-Service SysMain -Force
Set-Service SysMain -StartupType Disabled

# 验证
Get-Service SysMain
# 期望结果：StartupType = Disabled, Status = Stopped
```

---

## 恢复方法

执行优化后如果想撤销，按对应操作还原：

| 优化项 | 恢复命令 |
|--------|---------|
| 电源计划 | `powercfg /s <你之前记下的GUID>` |
| 排除路径 | `Remove-MpPreference -ExclusionPath "D:\YourAIProjects"` |
| 扫描方向 | `Set-MpPreference -RealTimeScanDirection 0` |
| SysMain | `Set-Service SysMain -Automatic; Start-Service SysMain` |

---

## 最佳实践

1. **先诊断，再优化** — 根据诊断结果选择需要执行的优化项，不是全量跑
2. **一次只做一步** — 执行完一个优化后观察效果，再考虑下一步
3. **先测电池耗电基线** — 用诊断命令记录优化前的数据，优化后再跑一次对比
4. **排除路径尽量窄** — 排除具体项目目录而非整个盘符
5. **SysMain 可在需要时手动启动** — 不是你今天删了明天就不能用
6. **更新 `powercfg /list` 的 GUID** — 不同机器、不同 Windows 版本的电源计划 GUID 可能不同，请不要直接复用本文档的 GUID 而不验证
