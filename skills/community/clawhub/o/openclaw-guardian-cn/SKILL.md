---
name: openclaw-guardian-cn
description: |
  OpenClaw 系统守护 skill。每日定时自检、自动检测异常并尝试自救。
  用于：(1) 每日定时检查 Gateway 状态 (2) 自动检测进程/WebSocket/插件异常 (3) 自动尝试恢复服务 (4) 用户可自定义自检时间
  当用户要求设置每日自检、自助恢复、系统守护、自动重启 Gateway 时触发。
---

# OpenClaw Guardian - 系统守护

> 💡 **跨平台支持**：Linux + Windows 自动适配

## 功能概述

- **定时自检**：每日固定时间检查 OpenClaw Gateway 状态
- **异常检测**：检测进程、WebSocket 连接、插件状态
- **自动自救**：尝试自动恢复常见异常（重启服务、重新连接等）
- **自定义时间**：用户可设置自检时间

## 自检项目

### 0. Skills 状态检查
- 检查目录是否存在
- 统计 skill 数量
- 对比基线检测丢失
- 检查每个 skill 是否有 SKILL.md

### 0.5 Channels 配置检查
```bash
cat ~/.openclaw/openclaw.json | grep -A 2 '"channels"'
ls ~/.openclaw/extensions/
```
- 检查配置文件中的 channels
- 统计已启用的 channels
- 检查 extensions 目录

### 1. Gateway 进程状态
```bash
openclaw gateway status
```
- 检查是否 running
- 检查 PID 是否存在

### 2. WebSocket 连接状态
- 检查 Gateway 与各插件的连接
- 检测 1006 断开错误

### 3. 插件状态
```bash
openclaw status
```

### 4. 系统资源
- CPU/内存使用率
- 磁盘空间

## 自救策略

| 异常 | 检测方式 | 自救动作 |
|------|----------|----------|
| Gateway 未运行 | `pgrep -f "openclaw-gateway"` 无结果 | `openclaw gateway start` |
| 进程崩溃 | PID 不存在 | `openclaw gateway restart` |
| 端口占用 | 端口检查失败 | 释放端口或更换端口 |
| 连接断开 | WebSocket 1006 | 重启 Gateway |

## 自救验证流程

每次自救操作后必须验证是否成功：

```bash
# 自救函数示例
try_recover() {
    local action="$1"
    echo "🔧 尝试自救: $action"
    
    # 执行自救动作
    eval "$action"
    
    # 等待服务启动
    sleep 5
    
    # 验证是否成功
    if pgrep -f "openclaw-gateway" > /dev/null; then
        echo "✅ 自救成功"
        return 0
    else
        echo "❌ 自救失败，需要手动处理"
        return 1
    fi
}
```

### 各自救动作的验证方法

| 自救动作 | 验证命令 | 成功标志 |
|----------|----------|----------|
| 启动 Gateway | `pgrep -f "openclaw-gateway"` | 返回 PID |
| 重启 Gateway | `pgrep -f "openclaw-gateway"` | 返回 PID |
| 重连插件 | `openclaw status` | 插件状态正常 |

### 自救流程完整示例

```
1. 检测异常: Gateway 进程不存在
2. 记录状态: 当前进程数=0
3. 尝试自救: openclaw gateway start
4. 等待 5 秒
5. 验证结果: pgrep -f "openclaw-gateway"
6. 成功? → 报告 ✅ 已恢复
   失败? → 报告 ❌ 需要手动处理
```

### 自救失败处理

当自救失败时：
1. 不要重复尝试（避免死循环）
2. 明确报告异常情况
3. 提示用户手动处理
4. 记录详细日志供排查

## 使用方法

### Heartbeat 轻量检查（可选）

在 HEARTBEAT.md 中添加轻量检查，每次 Heartbeat 轮询时快速检查：

```
## OpenClaw Guardian

- 检查 Gateway 进程是否存活: `pgrep -f "openclaw gateway"`
- 如果进程不在，尝试启动: `openclaw gateway start`
- 如果之前正常，这次突然挂了，报告异常
```

**检查频率**：每 1-2 个 Heartbeat 周期做一次（避免太频繁）

### Cron 完整自检

告诉用户使用 `openclaw cron` 设置定时任务：

```bash
# 添加每日自检（早上 9 点）
openclaw cron add --name "guardian-daily" --schedule "0 9 * * *" --command "openclaw guardian check"
```

### 手动触发自检

用户可以说：
- "运行自检"
- "检查系统状态"
- "帮我看看 Gateway 还好吗"

### 自检时自动配置外部守护

**首次运行自检时**，自动检测操作系统并配置对应守护：

1. 检测当前系统：`$OSTYPE` 或 `[Environment]::OSVersion`
2. Linux → 检查 crontab 是否有守护 → 没有则添加
3. Windows → 检查任务计划程序是否有守护 → 没有则提示用户配置
4. 报告配置结果

```bash
# 自动配置脚本
# 注意：以下路径假设 OpenClaw 安装在 ~/.openclaw 目录下
# 如果你的安装路径不同，请修改对应的路径
OPENCLAW_PATH=~/.openclaw
if ! crontab -l 2>/dev/null | grep -q "openclaw-gateway"; then
    (crontab -l 2>/dev/null; echo "*/5 * * * * pgrep -f \"openclaw-gateway\" > /dev/null || cd $OPENCLAW_PATH && node ./dist/daemon-cli.js start >> /tmp/gateway_guardian.log 2>&1") | crontab -
    echo "✅ 已自动配置外部守护（每 5 分钟检查）"
else
    echo "✅ 外部守护已配置"
fi
```

### 自救操作

当检测到异常时：
1. 先尝试自动恢复
2. 记录操作日志
3. 报告恢复结果
4. **必须验证自救是否成功**（见上文"自救验证流程"）

## 输出格式

自检完成后，报告格式：

```
🛡️ OpenClaw 自检报告
时间: YYYY-MM-DD HH:mm
----------------
✅ Gateway: 运行中 (PID: xxx)
✅ 内存: 45%
✅ 磁盘: 60%
----------------
自检完成，无异常
```

或：

```
🛡️ OpenClaw 自检报告
时间: YYYY-MM-DD HH:mm
----------------
❌ Gateway: 已停止
🔧 尝试自救: 重启 Gateway...
✅ 自救成功！
----------------
状态: 已恢复
```

## 注意事项

- 自救前记录当前状态
- 自救失败时提示用户手动处理
- 避免频繁重启（间隔至少 30 秒）

## 外部守护配置（推荐）

**问题**：如果 Gateway 完全挂了，Agent 本身无法工作，需要外部守护。

**解决方案**：根据操作系统自动选择对应方案

### 自动检测操作系统

首次自检时，自动检测并配置对应平台的守护：

```bash
# 检测操作系统
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🟢 Linux 系统，使用 Cron 守护"
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "🪟 Windows 系统，使用任务计划程序"
else
    echo "⚠️ 未知系统"
fi
```

### Linux → Cron 守护

### 自动配置（首次使用）

当用户运行自检时，自动检查并配置 cron 守护：

```bash
# 检查是否已有守护
crontab -l | grep "openclaw-gateway"

# 如果没有，自动添加（路径需要根据实际安装位置修改）
# 假设 OpenClaw 安装在 ~/.openclaw
(crontab -l 2>/dev/null; echo '*/5 * * * * pgrep -f "openclaw-gateway" > /dev/null || cd ~/.openclaw && node ./dist/daemon-cli.js start >> /tmp/gateway_guardian.log 2>&1') | crontab -
```

### 守护逻辑

```
系统 Cron（独立于 Gateway）
    ↓ 每 5 分钟
pgrep 检查 Gateway 进程
    ↓ 如果不存在
执行启动命令
```

### 优势

- 不需要 sudo 权限
- 不依赖 Agent 本身
- 系统级守护，Gateway 挂了也能救

### 手动配置（可选）

如果需要修改检查间隔：

```bash
crontab -e

# 每 3 分钟检查一次
*/3 * * * * pgrep -f "openclaw-gateway" > /dev/null || /path/to/start_gateway.sh
```

### 日志位置

- 守护日志：`/tmp/gateway_guardian.log`

---

### Windows → 任务计划程序 / PowerShell

当检测到 Windows 系统时，使用以下方案：

#### 方案 A: PowerShell 守护脚本

复制 `scripts/guardian-windows.ps1` 到用户目录并配置：

```powershell
# 1. 修改脚本中的 Gateway 路径
# 2. 设置开机自启
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File C:\Users\你的用户名\.openclaw\scripts\guardian-windows.ps1"
$trigger = New-ScheduledTaskTrigger -At Startup
Register-ScheduledTask -TaskName "OpenClaw Guardian" -Trigger $trigger -Action $action -RunLevel Highest
```

#### 方案 B: 定时检查（每 5 分钟）

```powershell
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File C:\Users\你的用户名\.openclaw\scripts\guardian-windows.ps1"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 9999)
Register-ScheduledTask -TaskName "OpenClaw Guardian" -Trigger $trigger -Action $action -RunLevel Highest
```

#### 自动配置逻辑

```powershell
# 检测是否已有守护任务
$task = Get-ScheduledTask -TaskName "OpenClaw Guardian" -ErrorAction SilentlyContinue

if ($null -eq $task) {
    # 未配置，自动添加
    # ... 执行上面的注册命令
    Write-Host "✅ 已自动配置 Windows 守护（每 5 分钟检查）"
} else {
    Write-Host "✅ 守护已配置"
}
```

#### 日志位置

- 守护日志：`$env:USERPROFILE\.openclaw\logs\guardian.log`

---

## 一键配置（首次使用）

首次运行自检时自动检测操作系统并配置：

### Linux

```bash
# 复制脚本到 ~/.openclaw/
mkdir -p ~/.openclaw
cp -r /path/to/openclaw-guardian/scripts/guardian-daily.sh ~/.openclaw/

# 添加 cron 任务（路径根据实际安装位置修改）
(crontab -l 2>/dev/null; echo '*/5 * * * * pgrep -f "openclaw-gateway" > /dev/null || cd ~/.openclaw && node ./dist/daemon-cli.js start >> /tmp/gateway_guardian.log 2>&1') | crontab -

# 添加每日报告任务
(crontab -l 2>/dev/null; echo '0 9 * * * ~/.openclaw/guardian-daily.sh >> /tmp/daily_report.txt 2>&1') | crontab -
```

### Windows

```powershell
# 复制脚本
Copy-Item -Path "C:\path\to\openclaw-guardian\scripts\guardian-windows.ps1" -Destination "$env:USERPROFILE\.openclaw\scripts\"

# 手动修改 Gateway 路径后配置定时任务
# （需要用户修改脚本中的 $GatewayPath 变量）
```

**分享给小伙伴：**
1. 把整个 `openclaw-guardian` 文件夹发给他
2. 他放到 `~/.openclaw/skills/` 下
3. 运行自检时会自动配置
