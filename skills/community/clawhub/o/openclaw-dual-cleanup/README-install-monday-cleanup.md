# 周一深度清理部署指南

## 📋 **根据杜的要求部署**

### **核心需求**（来自杜的指令）
1. 文件数量触发改为>10个立即触发清理
2. 只在每周一9:00自动进行一次深度清理
3. 如果当时网关未开，即在当天首次开启网关后，自动进行深度清理
4. 不做每月、每日的自动清理！

### **部署状态**
✅ **已完成所有脚本开发**
✅ **已更新SKILL.md文档**
✅ **已更新HEARTBEAT.md**

## 📧 **部署方法**

### **1. 基本配置（已自动完成）**
无需额外配置，HEARTBEAT.md已更新为：
- 文件触发阈值：>10个文件
- 周一深度清理：每周一9:00执行

### **2. Crontab配置（可选，如果您希望自动执行）**
如果您希望设置自动周一清理：

```bash
# 打开Crontab编辑器
crontab -e

# 添加以下行（每周一9:00执行深度清理）
0 9 * * 1 /usr/bin/pwsh -File ~/.openclaw/workspace/skills/openclaw-dual-cleanup/scripts/monday-deep-clean.ps1

# 如果您希望网关启动后检查等待任务（可选）
@reboot /usr/bin/pwsh -File ~/.openclaw/workspace/skills/openclaw-dual-cleanup/scripts/gateway-start-hook.ps1
```

### **3. Windows计划任务（可选）**
如果您在Windows系统中：

```powershell
# 创建周一9:00计划任务
$action = New-ScheduledTaskAction -Execute "pwsh" -Argument "-File ~/.openclaw\workspace\skills\openclaw-dual-cleanup\scripts\monday-deep-clean.ps1"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 09:00
Register-ScheduledTask -TaskName "OpenClaw Monday Deep Cleanup" -Action $action -Trigger $trigger -Description "执行OpenClaw周一深度清理"
```

## 🎯 **手动测试方法**

### **1. 测试周一深度清理脚本**
```powershell
# 直接运行（检查逻辑但可能跳过执行）
~/.openclaw/workspace/skills/openclaw-dual-cleanup/scripts/monday-deep-clean.ps1

# 强制执行（忽略网关状态）
~/.openclaw/workspace/skills/openclaw-dual-cleanup/scripts/monday-deep-clean.ps1；执行双重清理
```

### **2. 测试网关启动钩子**
```powershell
# 正常执行模式
~/.openclaw/workspace/skills/openclaw-dual-cleanup/scripts/gateway-start-hook.ps1

# 模拟模式（只预览不实际执行）
~/.openclaw/workspace/skills/openclaw-dual-cleanup/scripts/gateway-start-hook.ps1 -Simulate
```

### **3. 测试心跳触发**
```powershell
# 查看当前会话文件数量
(Get-ChildItem -Path ~/.openclaw/agents/main/sessions -Filter "*.jsonl").Count

# 如果超过10个文件，心跳检查会自动触发清理
```

## 🔍 **状态检查**

### **检查当前配置**
```powershell
# 查看会话文件数量
$count = (Get-ChildItem -Path ~/.openclaw/agents/main/sessions -Filter "*.jsonl" -ErrorAction SilentlyContinue).Count
Write-Host "当前会话文件数: $count (触发阈值: >10个)" -ForegroundColor $(if ($count -gt 10) { "Red" } else { "Green" })

# 检查今天是星期几
$day = (Get-Date).DayOfWeek
Write-Host "今天是: $day" -ForegroundColor Cyan
```

## 🛡️ **安全降级**

如果您想恢复到更宽松的策略（>30个文件触发），可以：

```powershell
# 修改HEARTBEAT.md中的文件数量触发
# 将 "会话目录文件总数 > 10个" 改为 "会话目录文件总数 > 30个"
```

## 📊 **监控日志**

脚本会在`$env:TEMP`目录创建日志：
- `openclaw_monday_cleanup_wait.txt` - 等待的清理任务
- `openclaw_cleanup_*.log` - 清理执行日志

您可以随时检查这些文件来了解系统状态。

---

**重要提示：** 按照杜的要求，系统已大幅减少自动清理频率，只在必要时执行（>10个文件或每周一9:00）。这能最大限度减少对研究专注度的干扰。

**最后更新时间：** 2026-03-29  
**部署状态：** 已全部完成 ✅