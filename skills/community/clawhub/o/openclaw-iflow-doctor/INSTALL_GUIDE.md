# OpenClaw iFlow Doctor - 三端安装指南

**版本**: 1.1.0  
**更新日期**: 2026-03-01  
**支持系统**: Linux / Windows / macOS

---

## 📋 系统要求

| 组件 | 要求 | 说明 |
|------|------|------|
| OpenClaw | 2026.2.0+ | 必须安装 |
| Python | 3.8+ | 必须 |
| iflow-helper | 1.0.0+ | 推荐（复杂修复） |
| systemd | 219+ | 仅 Linux 需要 |

---

## 🐧 Linux 安装（systemd）

### 方式 1: 自动安装（推荐）

```bash
# 1. 进入技能目录
cd ~/.openclaw/skills/openclaw-iflow-doctor

# 2. 运行安装脚本
sudo ./install-systemd.sh

# 3. 验证安装
systemctl status openclaw-iflow-doctor
```

### 方式 2: 手动安装

```bash
# 1. 复制服务文件
sudo cp openclaw-iflow-doctor.service /etc/systemd/system/

# 2. 重载 systemd
sudo systemctl daemon-reload

# 3. 启用服务（开机自启）
sudo systemctl enable openclaw-iflow-doctor

# 4. 启动服务
sudo systemctl start openclaw-iflow-doctor

# 5. 查看状态
systemctl status openclaw-iflow-doctor
```

### 常用命令

```bash
# 查看状态
systemctl status openclaw-iflow-doctor

# 停止服务
sudo systemctl stop openclaw-iflow-doctor

# 重启服务
sudo systemctl restart openclaw-iflow-doctor

# 查看日志
journalctl -u openclaw-iflow-doctor -f

# 禁用开机自启
sudo systemctl disable openclaw-iflow-doctor
```

### 测试

```bash
# 1. 测试自动重启（手动 kill gateway）
pkill -f openclaw-gateway

# 2. 等待 10 秒
sleep 10

# 3. 检查是否自动恢复
openclaw gateway status
```

---

## 🪟 Windows 安装

### 前提条件

1. **Python 3.8+** - 下载安装 https://python.org
2. **OpenClaw** - 已安装并配置
3. **PowerShell 管理员权限**

### 安装步骤

```powershell
# 1. 打开 PowerShell（管理员）

# 2. 进入技能目录
cd ~\.openclaw\skills\openclaw-iflow-doctor

# 3. 运行安装脚本
python install.py

# 4. 验证安装
python -c "import watchdog; print('OK')"
```

### 手动启动监控

```powershell
# 方式 1: 前台运行
python watchdog.py --start

# 方式 2: 后台运行（当前会话）
Start-Process python -ArgumentList "watchdog.py --start" -WindowStyle Hidden
```

### 开机自启（任务计划程序）

```powershell
# 创建任务计划
$action = New-ScheduledTaskAction -Execute "python" -Argument "watchdog.py --start" -WorkingDirectory "$env:USERPROFILE\.openclaw\skills\openclaw-iflow-doctor"
$trigger = New-ScheduledTaskTrigger -AtLogon
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "OpenClaw iFlow Doctor" -Action $action -Trigger $trigger -Principal $principal -Description "OpenClaw self-healing watchdog"
```

### 测试

```powershell
# 1. 测试 gateway 重启
Stop-Process -Name "node" -Filter "openclaw-gateway" -ErrorAction SilentlyContinue

# 2. 等待 10 秒
Start-Sleep -Seconds 10

# 3. 检查 gateway 状态
openclaw gateway status
```

---

## 🍎 macOS 安装（launchd）

### 前提条件

1. **Python 3.8+** - `brew install python@3.12`
2. **OpenClaw** - 已安装并配置

### 安装步骤

```bash
# 1. 创建 launchd plist 文件
cat > ~/Library/LaunchAgents/com.openclaw.iflow-doctor.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.iflow-doctor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/YOUR_USERNAME/.openclaw/skills/openclaw-iflow-doctor/watchdog.py</string>
        <string>--start</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/YOUR_USERNAME/.openclaw/skills/openclaw-iflow-doctor</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/openclaw-iflow-doctor.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/openclaw-iflow-doctor.err</string>
</dict>
</plist>
EOF

# 2. 加载服务
launchctl load ~/Library/LaunchAgents/com.openclaw.iflow-doctor.plist

# 3. 验证状态
launchctl list | grep iflow-doctor
```

### 常用命令

```bash
# 查看状态
launchctl list | grep iflow-doctor

# 停止服务
launchctl unload ~/Library/LaunchAgents/com.openclaw.iflow-doctor.plist

# 启动服务
launchctl load ~/Library/LaunchAgents/com.openclaw.iflow-doctor.plist

# 查看日志
tail -f /tmp/openclaw-iflow-doctor.log
```

---

## 🧪 验证安装

### 通用验证（所有平台）

```bash
# 1. 检查技能是否启用
openclaw skills list | grep iflow-doctor

# 2. 运行诊断测试
openclaw skills run openclaw-iflow-doctor --test

# 3. 查看统计
openclaw skills run openclaw-iflow-doctor --stats
```

### 预期输出

```
✓ OpenClaw iFlow Doctor installed
✓ Watchdog running
✓ Case library loaded (10 cases)
✓ Records loaded (N records)
✓ iflow-helper integration ready
```

---

## 🔧 故障排查

### Linux: 服务无法启动

```bash
# 查看详细错误
journalctl -u openclaw-iflow-doctor -n 50

# 检查 Python 路径
which python3

# 检查文件权限
ls -la ~/.openclaw/skills/openclaw-iflow-doctor/watchdog.py
chmod +x watchdog.py
```

### Windows: 脚本无法运行

```powershell
# 检查执行策略
Get-ExecutionPolicy

# 如果 Restricted，改为 RemoteSigned
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 检查 Python 是否在 PATH
python --version
```

### macOS: launchd 无法加载

```bash
# 检查 plist 语法
plutil -lint ~/Library/LaunchAgents/com.openclaw.iflow-doctor.plist

# 查看系统日志
log show --predicate 'process == "launchd"' --last 5m
```

---

## 📊 版本对比

| 功能 | Linux | Windows | macOS |
|------|-------|---------|-------|
| 自动安装 | ✅ | ✅ | ⚠️ 手动 |
| 开机自启 | ✅ systemd | ✅ 任务计划 | ✅ launchd |
| 进程监控 | ✅ | ✅ | ✅ |
| 自动重启 | ✅ | ✅ | ✅ |
| 日志查看 | ✅ journalctl | ✅ 事件查看器 | ✅ log show |

---

## 📞 获取帮助

- **文档**: https://github.com/kosei-echo/openclaw-iflow-doctor
- **问题反馈**: https://github.com/kosei-echo/openclaw-iflow-doctor/issues
- **讨论**: https://github.com/kosei-echo/openclaw-iflow-doctor/discussions

---

**最后更新**: 2026-03-01  
**版本**: 1.1.0  
**维护者**: kosei-echo
