# OpenClaw Backup Skill

一键备份和恢复 OpenClaw 工作空间、Skills 和配置。

## 触发词

- "备份 OpenClaw"
- "备份工作空间"
- "恢复备份"
- "创建备份"
- "备份配置"
- "备份技能"
- "完整备份"
- "快速备份"
- "显示备份"
- "列出备份"
- "删除备份"
- "backup openclaw"
- "restore backup"
- "list backups"

## 能力

### 1. 快速备份
- 备份核心配置文件
- 备份记忆文件
- 备份 Skills
- 排除 node_modules 和 .git
- 生成时间戳 ZIP 文件
- 自动清理旧备份（保留最近 5 个）

### 2. 完整备份
- 包含 node_modules
- 包含所有项目文件
- 包含 .git 目录
- 适合迁移到新设备
- 自动清理旧备份（保留最近 3 个）

### 3. 恢复操作
- 从 ZIP 备份恢复
- 自动备份现有配置（.bak.*）
- 选择性恢复（配置/Skills/记忆）
- DryRun 模式预览
- 验证备份完整性

### 4. 备份管理
- 列出所有可用备份
- 显示备份详情（大小、文件数、Skills）
- 删除指定备份
- 查看备份清单

## 配置

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
| backupDir | `D:\\OpenClaw_Backup` | 备份文件存储目录 |
| keepLastN | `5` | 保留最近 N 个备份 |
| autoBackup | `false` | 是否启用自动备份 |
| autoBackupSchedule | `"0 2 * * *"` | 自动备份 cron 表达式 |

## 使用示例

### 快速备份
```
备份 OpenClaw
```

输出：
```
📦 OpenClaw 快速备份
======================

📦 备份 Skills...
   ✅ 74 个文件

📁 备份 Workspace...
   ✅ 1234 个文件（已排除 node_modules）

⚙️  备份 OpenClaw 配置...
   ✅ openclaw.json

💰 备份 FluxA Wallet...
   ✅ FluxA 配置

📋 生成备份清单...
   ✅ 清单已生成

🗜️  压缩备份...
   ✅ 压缩完成：85.23 MB

🧹 清理临时文件...
   ✅ 清理完成

🗑️  清理旧备份（保留最近 5 个）...
   ✅ 无需清理（当前 3 个备份）

================================
✅ 备份完成！
================================

📦 备份文件：D:\OpenClaw_Backup\OpenClaw_Backup_2026-03-17_15-14-30.zip
📊 文件大小：85.23 MB
📄 文件总数：2345
🧩 Skills 数量：74

💡 提示：
   恢复命令：.\restore_backup.ps1 -BackupZip "D:\OpenClaw_Backup\OpenClaw_Backup_2026-03-17_15-14-30.zip"
```

### 完整备份
```
完整备份 OpenClaw
```

### 恢复备份
```
从备份恢复 D:\OpenClaw_Backup\OpenClaw_Backup_2026-03-17_15-14-30.zip
```

### 查看备份列表
```
显示所有备份
```

输出：
```
📦 OpenClaw 备份列表
====================

备份目录：D:\OpenClaw_Backup
找到 3 个备份

名称                                          类型    大小_MB  文件数  Skills  创建时间
----                                          ----    -------  ------  ------  ----------
OpenClaw_Backup_2026-03-17_15-14-30.zip       快速    85.23    2345    74      2026-03-17 15:14
OpenClaw_Backup_2026-03-17_14-23-41.zip       快速    82.15    2340    74      2026-03-17 14:23
OpenClaw_FullBackup_2026-03-16_10-00-00.zip   完整    2742.46  45946   74      2026-03-16 10:00

💡 恢复命令示例：
   .\restore_backup.ps1 -BackupZip "D:\OpenClaw_Backup\OpenClaw_Backup_2026-03-17_15-14-30.zip"
```

## 脚本说明

### quick_backup.ps1
**用途**: 快速备份核心文件  
**参数**: 
- `BackupDir` (默认：`D:\OpenClaw_Backup`)
- `KeepLastN` (默认：`5`)

**特点**:
- 排除 node_modules 和 .git
- 适合日常备份
- 文件大小：~50-100 MB

### full_backup.ps1
**用途**: 完整备份所有内容  
**参数**: 
- `BackupDir` (默认：`D:\OpenClaw_Backup`)
- `KeepLastN` (默认：`3`)

**特点**:
- 包含所有内容
- 适合设备迁移
- 文件大小：~2-5 GB

### restore_backup.ps1
**用途**: 从备份恢复  
**参数**: 
- `BackupZip` (必需): 备份 ZIP 文件路径
- `SkipSkills` (可选): 跳过 Skills 恢复
- `SkipWorkspace` (可选): 跳过 Workspace 恢复
- `SkipConfig` (可选): 跳过配置恢复
- `SkipFluxa` (可选): 跳过 FluxA 恢复
- `DryRun` (可选): 测试模式，不实际恢复

**特点**:
- 自动备份现有配置
- 支持选择性恢复
- 支持 DryRun 模式

### list_backups.ps1
**用途**: 列出所有备份  
**参数**: 
- `BackupDir` (默认：`D:\OpenClaw_Backup`)
- `Limit` (默认：`10`)

**特点**:
- 显示备份详情
- 读取 manifest 信息
- 提供恢复命令示例

## 依赖

- PowerShell 5.1+
- .NET Framework 4.5+ (用于 ZIP 压缩)
- Windows/Linux/macOS 跨平台支持

## 注意事项

1. 完整备份可能较大（包含 node_modules）
2. 建议定期清理旧备份
3. 恢复前建议先备份当前状态
4. 恢复后需要重启 OpenClaw Gateway
5. PowerShell 执行策略需要允许运行脚本

## 故障排除

### PowerShell 执行策略阻止
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### 恢复后 Skills 不加载
```bash
openclaw gateway restart
```

### 备份文件过大
使用快速备份模式：
```powershell
.\quick_backup.ps1
```

## 版本历史

### 1.0.0 (2026-03-17)
- ✅ 初始版本发布
- ✅ 快速备份功能
- ✅ 完整备份功能
- ✅ 恢复功能
- ✅ 备份列表功能
- ✅ 自动清理旧备份
- ✅ 选择性恢复
- ✅ DryRun 模式

## 发布说明

**包名**: `openclaw-backup`  
**版本**: `1.0.0`  
**许可证**: MIT  
**仓库**: https://github.com/openclaw/skills  

### 发布到 ClawHub

```bash
# 登录
clawhub login

# 发布
cd skills/openclaw-backup
clawhub publish

# 验证
clawhub info openclaw-backup
```

### 更新版本

```bash
# 更新 _meta.json 版本号
# 发布
clawhub publish --bump patch  # minor/major
```
