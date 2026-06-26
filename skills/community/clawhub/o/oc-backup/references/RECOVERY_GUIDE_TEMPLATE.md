# OpenClaw 备份恢复指导模板

> 本文档是恢复指导书的模板，实际恢复指导书会在每次备份时自动生成，包含具体的备份信息。

---

## 1. 备份信息

| 项目 | 值 |
|------|-----|
| 备份时间 | `{timestamp}` |
| 备份类型 | `{backupType}` |
| 备份文件 | `{filename}` |
| 备份大小 | `{backupSize}` |
| 包含文件数 | `{fileCount}` |
| 备份来源 | `{hostname}` |
| 平台 | `{platform}` |

---

## 2. 前置准备

### 2.1 确认环境

在恢复之前，请确认目标机器已安装：

- **Node.js**: >= 18.0.0
- **OpenClaw**: 已正确安装

检查命令：

```bash
# 检查 Node.js 版本
node --version

# 检查 OpenClaw 是否安装
openclaw --version
```

### 2.2 创建安全备份

**⚠️ 重要：在恢复之前，请先备份当前配置！**

如果目标机器已有 OpenClaw 配置，请先创建安全备份：

#### Windows (PowerShell)

```powershell
# 备份当前配置
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
Rename-Item -Path "$env:USERPROFILE\.openclaw" -NewName ".openclaw.backup.$timestamp" -ErrorAction SilentlyContinue
```

#### macOS / Linux

```bash
# 备份当前配置
mv ~/.openclaw ~/.openclaw.backup.$(date +%Y%m%d%H%M%S) 2>/dev/null || true
```

---

## 3. 解压备份文件

### 3.1 Windows (PowerShell)

```powershell
# 创建临时目录
$tempDir = "$env:USERPROFILE\.openclaw\temp\restore"
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
Set-Location $tempDir

# 解压备份文件（替换为实际文件名）
tar -xzf "openclaw-backup-full-YYYYMMDD-HHMMSS.tar.gz"

# 查看解压内容
Get-ChildItem -Recurse
```

### 3.2 macOS / Linux

```bash
# 创建临时目录
mkdir -p ~/.openclaw/temp/restore
cd ~/.openclaw/temp/restore

# 解压备份文件（替换为实际文件名）
tar -xzf openclaw-backup-full-YYYYMMDD-HHMMSS.tar.gz

# 查看解压内容
ls -laR
```

---

## 4. 恢复各类文件

### 4.1 恢复系统配置

系统配置包含 OpenClaw 的核心设置，恢复后立即生效。

#### Windows (PowerShell)

```powershell
# 确保目标目录存在
$openclawDir = "$env:USERPROFILE\.openclaw"
New-Item -ItemType Directory -Path $openclawDir -Force | Out-Null

# 复制所有系统配置
Copy-Item -Path "openclaw-backup\system\*" -Destination $openclawDir -Recurse -Force

# 或者选择性恢复
Copy-Item -Path "openclaw-backup\system\openclaw.json" -Destination $openclawDir -Force
Copy-Item -Path "openclaw-backup\system\.env" -Destination $openclawDir -Force
```

#### macOS / Linux

```bash
# 确保目标目录存在
mkdir -p ~/.openclaw

# 复制所有系统配置
cp -r openclaw-backup/system/* ~/.openclaw/

# 或者选择性恢复
cp openclaw-backup/system/openclaw.json ~/.openclaw/
cp openclaw-backup/system/.env ~/.openclaw/

# 设置 .env 文件权限
chmod 600 ~/.openclaw/.env
```

**📝 注意事项**：
- `.env` 文件包含敏感信息，请确保权限设置正确
- 如果 API 密钥已更新，恢复后可能需要手动更新

### 4.2 恢复核心文件

核心文件定义了 AI 的行为和人格，恢复后需要重启 OpenClaw。

#### Windows (PowerShell)

```powershell
# 确保目标目录存在
$workspaceDir = "$env:USERPROFILE\.openclaw\workspace"
New-Item -ItemType Directory -Path $workspaceDir -Force | Out-Null

# 复制所有核心文件
Copy-Item -Path "openclaw-backup\workspace\*" -Destination $workspaceDir -Recurse -Force

# 或者选择性恢复特定文件
Copy-Item -Path "openclaw-backup\workspace\SOUL.md" -Destination $workspaceDir -Force
Copy-Item -Path "openclaw-backup\workspace\USER.md" -Destination $workspaceDir -Force
Copy-Item -Path "openclaw-backup\workspace\IDENTITY.md" -Destination $workspaceDir -Force
```

#### macOS / Linux

```bash
# 确保目标目录存在
mkdir -p ~/.openclaw/workspace

# 复制所有核心文件
cp -r openclaw-backup/workspace/* ~/.openclaw/workspace/

# 或者选择性恢复特定文件
cp openclaw-backup/workspace/SOUL.md ~/.openclaw/workspace/
cp openclaw-backup/workspace/USER.md ~/.openclaw/workspace/
cp openclaw-backup/workspace/IDENTITY.md ~/.openclaw/workspace/
```

### 4.3 恢复技能目录

技能目录包含自定义技能，恢复后立即可用。

#### Windows (PowerShell)

```powershell
# 确保目标目录存在
$skillsDir = "$env:USERPROFILE\.openclaw\workspace\skills"
New-Item -ItemType Directory -Path $skillsDir -Force | Out-Null

# 复制所有技能
Copy-Item -Path "openclaw-backup\skills\*" -Destination $skillsDir -Recurse -Force

# 或者恢复单个技能
Copy-Item -Path "openclaw-backup\skills\your-skill-name" -Destination $skillsDir -Recurse -Force
```

#### macOS / Linux

```bash
# 确保目标目录存在
mkdir -p ~/.openclaw/workspace/skills

# 复制所有技能
cp -r openclaw-backup/skills/* ~/.openclaw/workspace/skills/

# 或者恢复单个技能
cp -r openclaw-backup/skills/your-skill-name ~/.openclaw/workspace/skills/
```

**📝 注意事项**：
- 如果技能包含 `package.json`，需要运行 `npm install` 安装依赖
- 某些技能可能需要额外配置

### 4.4 恢复其他数据

#### 恢复记忆数据

```bash
# macOS / Linux
mkdir -p ~/.openclaw/memory
cp -r openclaw-backup/memory/* ~/.openclaw/memory/
```

```powershell
# Windows
New-Item -ItemType Directory -Path "$env:USERPROFILE\.openclaw\memory" -Force | Out-Null
Copy-Item -Path "openclaw-backup\memory\*" -Destination "$env:USERPROFILE\.openclaw\memory" -Recurse -Force
```

#### 恢复定时任务

```bash
# macOS / Linux
mkdir -p ~/.openclaw/cron
cp -r openclaw-backup/cron/* ~/.openclaw/cron/
```

```powershell
# Windows
New-Item -ItemType Directory -Path "$env:USERPROFILE\.openclaw\cron" -Force | Out-Null
Copy-Item -Path "openclaw-backup\cron\*" -Destination "$env:USERPROFILE\.openclaw\cron" -Recurse -Force
```

#### 恢复设备配置

```bash
# macOS / Linux
mkdir -p ~/.openclaw/devices
cp -r openclaw-backup/devices/* ~/.openclaw/devices/
```

```powershell
# Windows
New-Item -ItemType Directory -Path "$env:USERPROFILE\.openclaw\devices" -Force | Out-Null
Copy-Item -Path "openclaw-backup\devices\*" -Destination "$env:USERPROFILE\.openclaw\devices" -Recurse -Force
```

---

## 5. 验证恢复结果

### 5.1 检查文件完整性

#### Windows (PowerShell)

```powershell
# 检查关键文件是否存在
Test-Path "$env:USERPROFILE\.openclaw\openclaw.json"
Test-Path "$env:USERPROFILE\.openclaw\.env"
Test-Path "$env:USERPROFILE\.openclaw\workspace\SOUL.md"
Test-Path "$env:USERPROFILE\.openclaw\workspace\skills"

# 列出已恢复的技能
Get-ChildItem "$env:USERPROFILE\.openclaw\workspace\skills" -Directory
```

#### macOS / Linux

```bash
# 检查关键文件是否存在
ls -la ~/.openclaw/openclaw.json
ls -la ~/.openclaw/.env
ls -la ~/.openclaw/workspace/SOUL.md
ls -la ~/.openclaw/workspace/skills/

# 列出已恢复的技能
ls ~/.openclaw/workspace/skills/
```

### 5.2 重启 OpenClaw

恢复配置后，需要重启 OpenClaw 服务：

```bash
# 重启 Gateway
openclaw gateway restart

# 或者停止后启动
openclaw gateway stop
openclaw gateway start

# 检查状态
openclaw gateway status
```

### 5.3 测试基本功能

```bash
# 测试 OpenClaw 是否正常工作
openclaw --version

# 检查配置是否生效
openclaw config list
```

---

## 6. 故障排除

### 6.1 权限问题

**症状**: 复制文件时提示 "Permission denied"

**解决方案**:

```bash
# macOS / Linux - 修复文件权限
chmod 600 ~/.openclaw/.env
chmod -R u+rw ~/.openclaw/workspace/
chmod -R u+rw ~/.openclaw/workspace/skills/
```

```powershell
# Windows - 以管理员身份运行 PowerShell
# 或检查文件属性，确保当前用户有读写权限
```

### 6.2 文件不存在

**症状**: 恢复时提示目标目录不存在

**解决方案**:

```bash
# 手动创建必要的目录结构
mkdir -p ~/.openclaw/workspace/skills
mkdir -p ~/.openclaw/memory
mkdir -p ~/.openclaw/cron
mkdir -p ~/.openclaw/devices
```

### 6.3 配置冲突

**症状**: 恢复后 OpenClaw 行为异常

**解决方案**:

1. 对比新旧配置文件差异
2. 手动合并重要配置
3. 特别注意 `.env` 中的敏感信息

```bash
# 对比文件差异
diff ~/.openclaw/openclaw.json ~/.openclaw.backup.*/openclaw.json
```

### 6.4 技能不工作

**症状**: 恢复后某些技能无法使用

**解决方案**:

1. 检查技能目录是否完整
2. 安装技能依赖

```bash
cd ~/.openclaw/workspace/skills/{skill-name}
npm install
```

### 6.5 Gateway 启动失败

**症状**: `openclaw gateway start` 失败

**解决方案**:

1. 检查端口是否被占用
2. 检查配置文件格式是否正确
3. 查看日志文件

```bash
# 检查端口
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# 查看日志
cat ~/.openclaw/logs/gateway.log
```

---

## 7. 完整命令参考

### 快速恢复（全量）

#### Windows (PowerShell)

```powershell
# 一键恢复脚本
$backupFile = "openclaw-backup-full-YYYYMMDD-HHMMSS.tar.gz"
$tempDir = "$env:USERPROFILE\.openclaw\temp\restore"

# 备份当前配置
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
Rename-Item -Path "$env:USERPROFILE\.openclaw" -NewName ".openclaw.backup.$timestamp" -ErrorAction SilentlyContinue

# 解压并恢复
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
Set-Location $tempDir
tar -xzf $backupFile
Copy-Item -Path "openclaw-backup\*" -Destination "$env:USERPROFILE\.openclaw" -Recurse -Force

# 清理
Set-Location ~
Remove-Item -Path $tempDir -Recurse -Force

# 重启服务
openclaw gateway restart
```

#### macOS / Linux

```bash
#!/bin/bash
# 一键恢复脚本

BACKUP_FILE="openclaw-backup-full-YYYYMMDD-HHMMSS.tar.gz"
TEMP_DIR="$HOME/.openclaw/temp/restore"

# 备份当前配置
[ -d "$HOME/.openclaw" ] && mv "$HOME/.openclaw" "$HOME/.openclaw.backup.$(date +%Y%m%d%H%M%S)"

# 解压并恢复
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"
tar -xzf "$BACKUP_FILE"
cp -r openclaw-backup/* "$HOME/.openclaw/"

# 清理
cd ~
rm -rf "$TEMP_DIR"

# 设置权限
chmod 600 "$HOME/.openclaw/.env"

# 重启服务
openclaw gateway restart
```

---

## 8. 注意事项

1. **敏感文件**: `.env` 文件包含 API 密钥等敏感信息
   - 备份文件请妥善保管
   - 不要将备份文件上传到公共仓库

2. **恢复后验证**: 
   - 恢复后请检查 OpenClaw 是否正常运行
   - 测试关键技能是否可用

3. **定期备份**: 
   - 建议定期创建备份
   - 重要修改后立即备份

4. **备份保管**: 
   - 备份文件保存在安全位置
   - 考虑加密存储敏感备份

5. **跨平台恢复**:
   - Windows ↔ macOS/Linux 恢复可能需要调整路径
   - 注意换行符差异 (CRLF vs LF)

---

*本恢复指导由 OpenClaw Backup 自动生成*
*版本: 1.0.0*