# powershell-sandbox - PowerShell 安全沙箱

**版本**: 0.1.0  
**作者**: 小蒲萄 (Clawd)  
**创建日期**: 2026-03-18  
**平台**: Windows PowerShell 5.1+ / PowerShell 7+

---

## 📖 简介

在受限的 PowerShell 环境中安全执行用户脚本，提供：

- ✅ **超时控制** - 防止无限循环
- ✅ **命令白名单** - 只允许安全命令
- ✅ **输出限制** - 防止日志炸弹
- ✅ **安全检查** - 执行前扫描危险代码
- ✅ **审计日志** - 记录所有执行
- ✅ **文件隔离** - 限制在工作目录内

---

## 🚀 快速开始

### 基本用法

```powershell
# 执行脚本（默认 30 秒超时）
.\src\sandbox.ps1 -ScriptPath "C:\path\to\script.ps1"

# 自定义超时时间
.\src\sandbox.ps1 -ScriptPath "script.ps1" -TimeoutSeconds 60

# 指定工作目录
.\src\sandbox.ps1 -ScriptPath "script.ps1" -WorkingDirectory "C:\workspace"

# 允许网络访问（谨慎使用！）
.\src\sandbox.ps1 -ScriptPath "script.ps1" -AllowNetwork
```

### 在 OpenClaw 中使用

```powershell
# 通过 exec 调用
exec(
  command: '.\skills\powershell-sandbox\src\sandbox.ps1 -ScriptPath "C:\Users\99236\.openclaw\workspace\scripts\user-script.ps1"',
  timeout: 60
)
```

---

## ⚙️ 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `-ScriptPath` | string | **必填** | 要执行的脚本路径 |
| `-TimeoutSeconds` | int | 30 | 执行超时时间（秒） |
| `-MaxOutputLines` | int | 1000 | 最大输出行数 |
| `-MaxOutputChars` | int | 50000 | 最大输出字符数 |
| `-WorkingDirectory` | string | 脚本目录 | 工作目录 |
| `-AllowNetwork` | switch | $false | 允许网络访问（⚠️ 高风险） |
| `-AllowedCommands` | string[] | 内置白名单 | 自定义允许的命令 |

---

## 🔒 安全特性

### 1. 命令白名单

**允许的命令**（部分）：
- 基础输出：`Write-Host`, `Write-Output`, `Write-Warning`
- 文件操作：`Get-Content`, `Set-Content`, `Get-ChildItem`, `Test-Path`
- 路径操作：`Join-Path`, `Split-Path`, `Resolve-Path`
- 数据处理：`Select-Object`, `Where-Object`, `ForEach-Object`, `Sort-Object`
- 格式转换：`ConvertTo-Json`, `ConvertFrom-Json`, `ConvertTo-Csv`
- 日期时间：`Get-Date`, `Get-TimeSpan`, `Start-Sleep`

**禁止的命令**：
- ❌ 网络访问：`Invoke-WebRequest`, `Invoke-RestMethod`, `Start-BitsTransfer`
- ❌ 进程管理：`Start-Process`, `Invoke-Expression`, `Get-Process`
- ❌ 远程执行：`Enter-PSSession`, `Invoke-Command`, `New-PSSession`
- ❌ 注册表：`Get-ItemProperty -Path HKLM:*`
- ❌ 服务管理：`Get-Service`, `Start-Service`, `Stop-Service`
- ❌ 计划任务：`Get-ScheduledTask`, `Register-ScheduledTask`
- ❌ WMI/CIM：`Get-WmiObject`, `Get-CimInstance`
- ❌ 代码执行：`Invoke-Expression`, `Add-Type`, `IEX`

### 2. .NET 类型限制

**允许的类型**：
- `System.String`, `System.Int32`, `System.DateTime`
- `System.IO.Path`, `System.IO.File`, `System.IO.Directory`
- `System.Math`, `System.Convert`, `System.Guid`
- `System.Text.StringBuilder`, `System.Text.RegularExpressions.Regex`

**禁止的类型**：
- ❌ `System.Net.*`（网络）
- ❌ `System.Diagnostics.Process`（进程）
- ❌ `System.Reflection.*`（反射）
- ❌ `System.Management.Automation.*`（PowerShell 内部）
- ❌ `System.ServiceProcess.*`（服务）
- ❌ `System.Threading.*`（线程）

### 3. 执行前安全检查

沙箱会在执行前扫描脚本内容，检测：
- 禁止的命令调用
- 禁止的 .NET 类型
- URL（可能尝试网络访问）
- `IEX` 缩写（Invoke-Expression）

发现违规会立即拒绝执行并报告具体问题。

### 4. 超时保护

使用 PowerShell Job 机制，超时后自动终止：
```powershell
$job = Start-Job -ScriptBlock $script
$completed = Wait-Job -Job $job -Timeout $TimeoutSeconds
if (-not $completed) {
    Stop-Job -Job $job
    Write-Error "执行超时！"
}
```

### 5. 输出限制

- 最大行数：1000 行（可配置）
- 最大字符数：50000 字符（可配置）
- 超出部分自动截断并提示

### 6. 文件路径隔离

脚本只能访问工作目录内的文件，防止遍历到系统目录。

---

## 📋 退出代码

| 代码 | 含义 |
|------|------|
| 0 | 执行成功 |
| 1 | 脚本文件不存在 |
| 2 | 安全检查失败 |
| 3 | 脚本执行错误 |
| 4 | 执行超时 |

---

## 🧪 测试用例

### 测试 1：安全脚本执行

```powershell
# test-safe.ps1
Write-Host "Hello from sandbox!"
$numbers = 1..10
$sum = ($numbers | Measure-Object -Sum).Sum
Write-Host "Sum of 1-10: $sum"
```

执行：
```powershell
.\src\sandbox.ps1 -ScriptPath "test-safe.ps1"
```

预期输出：
```
[2026-03-18 09:15:00] [INFO] 开始沙箱执行
[2026-03-18 09:15:00] [INFO] 安全检查通过 ✓
[2026-03-18 09:15:01] [INFO] 执行完成

========== 执行输出 ==========
Hello from sandbox!
Sum of 1-10: 55

========== 执行统计 ==========
状态：成功
行数：2
字符数：38
```

### 测试 2：危险命令拦截

```powershell
# test-dangerous.ps1
Invoke-WebRequest -Uri "https://example.com"
```

执行：
```powershell
.\src\sandbox.ps1 -ScriptPath "test-dangerous.ps1"
```

预期输出：
```
[2026-03-18 09:15:00] [INFO] 执行安全检查...
[2026-03-18 09:15:00] [ERROR] 安全检查失败！
[2026-03-18 09:15:00] [ERROR]   - 包含禁止命令：Invoke-WebRequest
```

### 测试 3：超时保护

```powershell
# test-timeout.ps1
Write-Host "Starting..."
Start-Sleep -Seconds 60
Write-Host "Done!"
```

执行（30 秒超时）：
```powershell
.\src\sandbox.ps1 -ScriptPath "test-timeout.ps1" -TimeoutSeconds 30
```

预期输出：
```
[2026-03-18 09:15:00] [INFO] 等待脚本执行（超时：30 秒）...
[2026-03-18 09:15:30] [ERROR] 超时！强制终止执行...
```

### 测试 4：文件操作（工作目录内）

```powershell
# test-file.ps1
$content = Get-Content "data.txt"
Write-Host "File content: $content"
Set-Content "output.txt" "Processed: $content"
```

执行：
```powershell
.\src\sandbox.ps1 -ScriptPath "test-file.ps1" -WorkingDirectory "C:\workspace"
```

---

## 📁 文件结构

```
skills/powershell-sandbox/
├── SKILL.md                 # 技能文档（本文件）
├── src/
│   ├── sandbox.ps1          # 沙箱执行器（核心）
│   ├── test-safe.ps1        # 测试用例 - 安全脚本
│   ├── test-dangerous.ps1   # 测试用例 - 危险脚本
│   └── test-timeout.ps1     # 测试用例 - 超时脚本
└── README.md                # 使用说明（可选）
```

---

## 🔧 自定义配置

### 扩展命令白名单

编辑 `sandbox.ps1` 中的 `$DEFAULT_ALLOWED_COMMANDS` 数组：

```powershell
$DEFAULT_ALLOWED_COMMANDS = @(
    # ... 现有命令 ...
    "Your-Safe-Cmdlet"  # 添加新命令
)
```

### 调整安全级别

**更严格**（推荐用于不受信任的脚本）：
```powershell
.\src\sandbox.ps1 -ScriptPath "script.ps1" `
    -TimeoutSeconds 10 `
    -MaxOutputLines 100 `
    -MaxOutputChars 5000
```

**更宽松**（仅用于可信脚本）：
```powershell
.\src\sandbox.ps1 -ScriptPath "script.ps1" `
    -TimeoutSeconds 300 `
    -AllowNetwork
```

---

## 📊 使用场景

### ✅ 适合的场景

- 执行用户提交的数据处理脚本
- 运行自动化任务（文件整理、日志分析）
- 测试 PowerShell 代码片段
- 教学/演示环境
- 需要隔离的批处理任务

### ❌ 不适合的场景

- 需要访问网络的脚本（使用 `-AllowNetwork` 需谨慎）
- 需要调用外部程序的脚本
- 需要管理员权限的操作
- 长时间运行的任务（>5 分钟）
- 需要交互式输入的脚本

---

## 🛡️ 安全建议

1. **始终使用沙箱** - 即使脚本来自可信来源
2. **设置合理超时** - 根据任务复杂度调整
3. **限制输出大小** - 防止日志炸弹
4. **审计所有执行** - 记录到 `.learnings/sandbox-log.md`
5. **定期更新白名单** - 根据实际需求调整
6. **不要在外部接口使用** - Feishu/Telegram/WhatsApp 中拒绝执行

---

## 📝 更新日志

### v0.1.0 (2026-03-18)
- ✅ 初始版本发布
- ✅ 命令白名单/黑名单机制
- ✅ .NET 类型限制
- ✅ 执行前安全检查
- ✅ 超时保护（Job 机制）
- ✅ 输出限制
- ✅ 审计日志
- ✅ 退出代码规范

---

## 🤝 贡献

欢迎提交 Issue 和 PR 来改进沙箱的安全性和功能！

**安全报告**：如发现安全漏洞，请优先通过私密渠道报告。

---

## 📄 许可证

MIT License

---

*最后更新：2026-03-18*
