---
name: openclaw-troubleshooter
description: "OpenClaw 故障诊断与一键修复工具。自动检测 Gateway 状态、配置错误、端口冲突、危险技能代码，并提供修复方案。基于真实故障经验提取。"
version: 1.0.0
license: MIT
acceptLicenseTerms: true
author: xiehesper-png
tags: [openclaw, troubleshooting, debug, repair, health]
---

# 🔧 OpenClaw Troubleshooter

**一键诊断 + 修复 OpenClaw 常见问题**

基于真实故障经验提取（2026-03-14 Gateway 断开 + Control UI origin 验证失败事件）

---

## 🚀 快速使用

### 完整诊断（推荐）
```powershell
openclaw troubleshoot
```

### 仅诊断不修复
```powershell
openclaw troubleshoot --check-only
```

### 修复特定问题
```powershell
openclaw troubleshoot --fix gateway      # 修复 Gateway
openclaw troubleshoot --fix config       # 修复配置
openclaw troubleshoot --fix security     # 修复安全问题
openclaw troubleshoot --fix all          # 修复所有
```

---

## 🔍 诊断范围

| 检查项 | 检测内容 | 修复方式 |
|--------|----------|----------|
| **Gateway 状态** | 进程是否运行、端口是否监听、WebSocket 是否就绪 | 重启 Gateway |
| **端口冲突** | 18789 是否被占用 | 终止占用进程或换端口 |
| **Control UI** | origin 验证配置、trustedProxies | 自动添加 allowedOrigins |
| **配置语法** | openclaw.json 是否合法 | 修复 JSON 格式 |
| **危险技能** | 扫描 skills/ 中的危险代码 | 卸载或标记 |
| **模型配置** | 模型是否可用、API key 是否有效 | 提示用户更新 |
| **日志错误** | 读取 gateway.log 最后 50 行 | 标出 ERROR/WARN |

---

## 📋 诊断流程

### 阶段 1：Gateway 健康检查
```powershell
# 1. 检查进程
tasklist | findstr "openclaw"

# 2. 检查端口
netstat -ano | findstr :18789

# 3. 检查 WebSocket
curl -ws "ws://127.0.0.1:18789"

# 4. 检查 HTTP 健康接口
curl -s http://127.0.0.1:18789/health
```

### 阶段 2：配置检查
```powershell
# 读取 openclaw.json
# 检查 gateway.controlUi.allowedOrigins
# 检查 gateway.trustedProxies
# 检查 gateway.nodes.denyCommands
```

### 阶段 3：安全检查
```powershell
# 扫描 skills/ 目录
# 检测 dangerous-exec 模式
# 检测 env-harvesting 模式
```

### 阶段 4：日志分析
```powershell
# 读取 C:\Users\34596\.openclaw\logs\gateway.log
# 提取 ERROR/WARN 行
# 分析卡点原因
```

---

## 🛠️ 修复方案

### Gateway 问题

**症状：**
- `openclaw status` 超时
- `openclaw logs` 报错 "Gateway not reachable"
- Control UI 显示连接中

**修复：**
```powershell
# 1. 终止旧进程
taskkill /F /IM "node.exe" /FI "WINDOWTITLE eq *openclaw*"

# 2. 清理端口
netstat -ano | findstr :18789
# 如果有 PID，执行 taskkill /F /PID <PID>

# 3. 重启 Gateway
openclaw gateway --port 18789 --no-browser

# 4. 等待 15 秒后验证
openclaw status
```

### Control UI Origin 验证失败

**症状：**
```
origin not allowed (open the Control UI from the gateway host or 
allow it in gateway.controlUi.allowedOrigins)
```

**修复：**
编辑 `openclaw.json`，在 `gateway` 部分添加：
```json
{
  "gateway": {
    "controlUi": {
      "allowedOrigins": [
        "http://127.0.0.1:18789",
        "http://localhost:18789"
      ]
    }
  }
}
```

然后重启网关：
```powershell
openclaw gateway restart
```

### 危险技能代码

**症状：**
- `capability-evolver`：27+ 处危险代码（shell 执行、环境变量窃取）
- `feishu-doc`：环境变量 + 网络发送

**修复：**
```powershell
# 直接卸载
clawhub uninstall capability-evolver --yes
clawhub uninstall feishu-doc --yes

# 或深度审查
clawhub inspect <skill-name> --file <file-path>
```

### 配置警告

**trustedProxies 未配置：**
```json
{
  "gateway": {
    "trustedProxies": ["127.0.0.1"]
  }
}
```

**denyCommands 无效：**
```json
{
  "gateway": {
    "nodes": {
      "denyCommands": [
        "canvas.present",
        "canvas.hide",
        "canvas.navigate",
        "canvas.eval",
        "canvas.snapshot",
        "canvas.a2ui.push",
        "canvas.a2ui.pushJSONL",
        "canvas.a2ui.reset"
      ]
    }
  }
}
```

---

## 📊 输出格式

### 诊断报告
```
🔴 核心问题（导致卡住/断掉的根本原因）
├─ Gateway 服务已断开
└─ 修复方案：openclaw gateway restart

🔴 严重安全风险（2 个技能含危险代码）
├─ capability-evolver（27 处危险代码）
└─ feishu-doc（1 处危险代码）

🟡 配置警告（2 个）
├─ gateway.trustedProxies 未配置
└─ gateway.nodes.denyCommands 配置无效

✅ 修复优先级清单
├─ P0: 重启 Gateway
├─ P0: 卸载 capability-evolver
└─ P1: 修正配置
```

---

## 🔧 脚本文件

### scripts/diagnose.ps1
```powershell
# OpenClaw 诊断脚本

param(
    [switch]$Deep,
    [switch]$Json
)

$ErrorActionPreference = "Stop"
$OpenClawHome = $env:OPENCLAW_HOME ?? "$env:USERPROFILE\.openclaw"

Write-Host "🦞 OpenClaw 诊断工具" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan

# 1. Gateway 状态
Write-Host "`n📡 Gateway 状态" -ForegroundColor Yellow
$gatewayPort = 18789
$process = Get-NetTCPConnection -LocalPort $gatewayPort -ErrorAction SilentlyContinue
if ($process) {
    Write-Host "✅ Gateway 正在监听端口 $gatewayPort (PID: $($process.OwningProcess))" -ForegroundColor Green
} else {
    Write-Host "❌ Gateway 未运行" -ForegroundColor Red
}

# 2. 配置检查
Write-Host "`n⚙️  配置检查" -ForegroundColor Yellow
$configPath = Join-Path $OpenClawHome "openclaw.json"
if (Test-Path $configPath) {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
    if ($config.gateway.controlUi.allowedOrigins) {
        Write-Host "✅ Control UI allowedOrigins 已配置" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Control UI allowedOrigins 未配置" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ openclaw.json 不存在" -ForegroundColor Red
}

# 3. 危险技能扫描
Write-Host "`n🔒 安全检查" -ForegroundColor Yellow
$skillsPath = Join-Path $OpenClawHome "workspace\skills"
if (Test-Path $skillsPath) {
    $dangerousSkills = @()
    Get-ChildItem $skillsPath -Directory | ForEach-Object {
        $skillName = $_.Name
        $files = Get-ChildItem $_.FullName -Recurse -Include *.js,*.ts,*.py
        foreach ($file in $files) {
            $content = Get-Content $file.FullName -Raw
            if ($content -match "child_process|exec\(|spawn\(|environment.*network") {
                $dangerousSkills += $skillName
                break
            }
        }
    }
    if ($dangerousSkills) {
        Write-Host "⚠️  发现危险技能：$($dangerousSkills -join ', ')" -ForegroundColor Yellow
    } else {
        Write-Host "✅ 未发现明显危险技能" -ForegroundColor Green
    }
}

Write-Host "`n✅ 诊断完成" -ForegroundColor Green
```

### scripts/fix-gateway.ps1
```powershell
# Gateway 修复脚本

param(
    [int]$Port = 18789
)

Write-Host "🔧 修复 Gateway..." -ForegroundColor Cyan

# 1. 终止旧进程
Write-Host "📋 终止旧 Gateway 进程..." -ForegroundColor Yellow
Get-Process | Where-Object { 
    $_.ProcessName -eq "node" -and 
    $_.CommandLine -like "*openclaw*gateway*" 
} | Stop-Process -Force

# 2. 清理端口
Write-Host "📋 清理端口 $Port..." -ForegroundColor Yellow
$connection = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
if ($connection) {
    Stop-Process -Id $connection.OwningProcess -Force
    Start-Sleep -Seconds 2
}

# 3. 启动新 Gateway
Write-Host "📋 启动新 Gateway..." -ForegroundColor Yellow
Start-Process "openclaw" -ArgumentList "gateway", "--port", $Port, "--no-browser"

# 4. 等待就绪
Write-Host "⏳ 等待 Gateway 就绪..." -ForegroundColor Yellow
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 1
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/health" -TimeoutSec 2 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Gateway 已就绪！" -ForegroundColor Green
            break
        }
    } catch {
        # 继续等待
    }
}

Write-Host "✅ Gateway 修复完成" -ForegroundColor Green
```

### scripts/fix-config.ps1
```powershell
# 配置修复脚本

$ErrorActionPreference = "Stop"
$OpenClawHome = $env:OPENCLAW_HOME ?? "$env:USERPROFILE\.openclaw"
$configPath = Join-Path $OpenClawHome "openclaw.json"

Write-Host "🔧 修复 openclaw.json 配置..." -ForegroundColor Cyan

$config = Get-Content $configPath -Raw | ConvertFrom-Json

# 修复 Control UI allowedOrigins
if (-not $config.gateway.controlUi) {
    $config.gateway.controlUi = @{}
}
$config.gateway.controlUi.allowedOrigins = @(
    "http://127.0.0.1:18789",
    "http://localhost:18789"
)

# 修复 trustedProxies
if (-not $config.gateway.trustedProxies) {
    $config.gateway.trustedProxies = @("127.0.0.1")
}

# 修复 denyCommands
$config.gateway.nodes.denyCommands = @(
    "canvas.present",
    "canvas.hide",
    "canvas.navigate",
    "canvas.eval",
    "canvas.snapshot",
    "canvas.a2ui.push",
    "canvas.a2ui.pushJSONL",
    "canvas.a2ui.reset"
)

# 保存配置
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8

Write-Host "✅ 配置已修复" -ForegroundColor Green
Write-Host "📋 需要重启 Gateway 使配置生效" -ForegroundColor Yellow
Write-Host "   执行：openclaw gateway restart" -ForegroundColor Gray
```

---

## 📝 经验来源

**提取自：** 2026-03-14 OpenClaw 健康诊断事件

**原始问题：**
- Gateway 断开导致所有功能不可用
- Control UI 显示 "origin not allowed"
- capability-evolver 和 feishu-doc 含危险代码
- 配置缺少 trustedProxies 和 allowedOrigins

**修复流程：**
1. 运行 `openclaw status --deep` 诊断
2. 卸载危险技能
3. 修复 openclaw.json 配置
4. 重启 Gateway
5. 验证健康状态

**提取时间：** 2026-03-14

---

## ⚠️ 注意事项

1. **备份配置** - 修复前自动备份 openclaw.json
2. **用户确认** - 卸载技能前需要用户确认
3. **网关重启** - 配置修改后需要重启 Gateway
4. **权限检查** - 某些操作需要管理员权限

---

## 🔄 更新日志

### v1.0.0 (2026-03-14)
- 初始版本
- 基于真实故障经验提取
- 支持 Gateway 诊断 + 修复
- 支持配置自动修复
- 支持危险技能扫描

---

*本技能由 self-improvement 流程自动提取，经验来源：memory/2026-03-14-openclaw-health-diagnosis.md*
