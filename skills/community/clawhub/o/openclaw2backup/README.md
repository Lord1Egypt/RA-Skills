# OpenClaw Backup

一键备份和恢复 OpenClaw 工作空间、Skills 和配置。

## 📦 安装

```bash
clawhub install openclaw-backup
```

或通过 ClawHub 网页：https://clawhub.com/skills/openclaw-backup

## 🚀 快速开始

### 备份 OpenClaw

**快速备份**（推荐，不含 node_modules）：
```
备份 OpenClaw
```

**完整备份**（包含 node_modules，适合迁移）：
```
完整备份 OpenClaw
```

### 恢复备份

```
从备份恢复 D:\OpenClaw_Backup_2026-03-17_14-23-41.zip
```

### 查看备份列表

```
显示所有备份
```

## 📁 脚本说明

### quick_backup.ps1
- 快速备份核心文件
- 排除 node_modules 和 .git
- 适合日常备份
- 文件大小：~50-100 MB
- 保留最近 5 个备份

### full_backup.ps1
- 完整备份所有内容
- 包含 node_modules
- 适合设备迁移
- 文件大小：~2-5 GB
- 保留最近 3 个备份

### restore_backup.ps1
- 从 ZIP 备份恢复
- 自动备份现有配置
- 支持选择性恢复
- 支持 DryRun 模式

### list_backups.ps1
- 显示所有可用备份
- 显示备份详情（大小、文件数、Skills 数量）
- 提供恢复命令示例

## ⚙️ 配置选项

在 `openclaw.json` 中添加：

```json
{
  "skills": {
    "openclaw-backup": {
      "backupDir": "D:\\OpenClaw_Backup",
      "keepLastN": 5,
      "autoBackup": false,
      "autoBackupSchedule": "0 2 * * *"
    }
  }
}
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| backupDir | D:\OpenClaw_Backup | 备份文件存储目录 |
| keepLastN | 5 | 保留最近 N 个备份 |
| autoBackup | false | 是否启用自动备份 |
| autoBackupSchedule | "0 2 * * *" | 自动备份 cron 表达式 |

## 📊 备份内容

### 快速备份包含：
- ✅ Skills（所有已安装技能）
- ✅ Workspace 配置（不含 node_modules）
- ✅ openclaw.json
- ✅ FluxA Wallet 配置（如果存在）
- ✅ 记忆文件（MEMORY.md + daily）

### 完整备份额外包含：
- ✅ node_modules（所有项目依赖）
- ✅ .git 目录
- ✅ 所有构建产物

## 🔧 高级用法

### 选择性恢复

```powershell
# 只恢复 Skills
.\restore_backup.ps1 -BackupZip "backup.zip" -SkipWorkspace -SkipConfig -SkipFluxa

# 只恢复配置
.\restore_backup.ps1 -BackupZip "backup.zip" -SkipSkills -SkipWorkspace -SkipFluxa

# 测试模式（不实际恢复）
.\restore_backup.ps1 -BackupZip "backup.zip" -DryRun
```

### 定时备份

使用 Windows 任务计划程序：

```powershell
# 每天凌晨 2 点备份
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
  -Argument "-ExecutionPolicy Bypass -File `"$PSScriptRoot\scripts\quick_backup.ps1`""
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
Register-ScheduledTask -TaskName "OpenClaw Backup" `
  -Action $action -Trigger $trigger -Description "每日自动备份 OpenClaw"
```

### 使用 OpenClaw Cron

在 openclaw.json 中配置定时备份任务：

```json
{
  "cron": {
    "jobs": [
      {
        "name": "每日备份",
        "schedule": {
          "kind": "cron",
          "expr": "0 2 * * *"
        },
        "payload": {
          "kind": "systemEvent",
          "text": "备份 OpenClaw"
        },
        "enabled": true
      }
    ]
  }
}
```

## 🛡️ 安全特性

1. **自动备份现有文件** - 恢复前自动备份当前配置到 `.bak.*` 目录
2. **验证备份完整性** - 读取 manifest.json 验证备份内容
3. **DryRun 模式** - 预览恢复操作，不实际修改文件
4. **选择性恢复** - 可选择只恢复 Skills、配置或记忆
5. **版本保留** - 自动清理旧备份，保留最近 N 个

## ⚠️ 注意事项

1. **完整备份较大** - 包含 node_modules 可能达到数 GB，建议仅在迁移时使用
2. **恢复需要重启** - 恢复后需重启 OpenClaw Gateway 使配置生效
3. **备份验证** - 建议定期测试恢复流程，确保备份可用
4. **存储位置** - 建议将备份文件同步到外部存储或云盘
5. **权限要求** - PowerShell 执行策略需要允许运行脚本

## 📝 备份清单示例

```json
{
  "WorkspaceFiles": 45946,
  "BackupSize": 2742.46,
  "BackupTime": "2026-03-17 14:27:46",
  "Source": "MAGICBOOK",
  "Skills": 74,
  "Type": "Full"
}
```

## 🆘 故障排除

### 问题：恢复后 Skills 不加载
**解决**：重启 OpenClaw Gateway
```bash
openclaw gateway restart
```

### 问题：备份文件过大
**解决**：使用快速备份模式
```powershell
.\quick_backup.ps1
```

### 问题：恢复失败
**解决**：检查备份文件完整性
```powershell
.\list_backups.ps1
```

### 问题：PowerShell 执行策略阻止脚本运行
**解决**：临时允许执行
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### 问题：备份目录磁盘空间不足
**解决**：更改备份目录到空间更大的磁盘
```json
{
  "skills": {
    "openclaw-backup": {
      "backupDir": "E:\\Backups\\OpenClaw"
    }
  }
}
```

## 📦 发布到 ClawHub

### 发布前检查清单

- [ ] 更新 `_meta.json` 中的版本号
- [ ] 更新 `README.md` 文档
- [ ] 测试所有脚本功能
- [ ] 添加 LICENSE 文件
- [ ] 验证跨平台兼容性

### 发布命令

```bash
# 登录 ClawHub
clawhub login

# 发布技能
cd skills/openclaw-backup
clawhub publish

# 验证发布
clawhub info openclaw-backup
```

### 版本更新

```bash
# 更新版本号（_meta.json）
# 1.0.0 -> 1.0.1 (bug fix)
# 1.0.0 -> 1.1.0 (feature)
# 1.0.0 -> 2.0.0 (breaking change)

# 发布新版本
clawhub publish --bump patch  # 或 minor/major
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/openclaw/skills.git
cd skills/packages/openclaw-backup

# 安装依赖（如有）
npm install

# 测试脚本
./scripts/quick_backup.ps1
./scripts/list_backups.ps1
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- OpenClaw 团队提供的优秀框架
- ClawHub 社区的支持
- 所有贡献者的帮助

## 📞 支持

遇到问题？欢迎通过以下方式联系：

- GitHub Issues: https://github.com/openclaw/skills/issues
- ClawHub 讨论区：https://clawhub.com/discuss
- 邮件：support@openclaw.ai

---

**最后更新**: 2026-03-17  
**当前版本**: 1.0.0  
**维护者**: 夏夏 😘
