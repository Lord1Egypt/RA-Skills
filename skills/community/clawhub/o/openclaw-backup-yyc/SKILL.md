---
name: openclaw-backup-yyc
description: OpenClaw 数据备份与恢复工具。⚠️ 触发条件：用户消息必须精确等于"备份openclaw数据"、"恢复openclaw数据"（中文）或"backup openclaw data"、"restore openclaw data"（英文），其中 openclaw 不区分大小写。其他任何输入（包括部分关键词如"备份"、"备份OpenClaw"等）均不触发此 skill，当作普通对话处理，不给出任何备份相关提示或引导。执行前必须向用户确认操作。语言适配规则：中文命令触发时使用中文提示，英文命令触发时使用英文提示。
---

# OpenClaw 备份恢复工具 / OpenClaw Backup & Restore Tool

## 🌐 语言适配规则 / Language Adaptation Rules

**根据用户触发的命令语言，自动显示对应语言的提示信息：**
- 中文命令触发 → 显示中文提示
- 英文命令触发 → 显示英文提示

---

## ⚠️ 触发条件（精确匹配） / Trigger Conditions (Exact Match)

**用户消息必须等于以下指令才触发，其中 openclaw 不区分大小写！**

### 中文触发命令

| 命令 | 功能 |
|-----|------|
| `备份openclaw数据` | 执行备份 |
| `恢复openclaw数据` | 执行恢复 |

> 注：`备份OpenClaw数据`、`备份OPENCLAW数据` 等均可触发

### 英文触发命令

| 命令 | 功能 |
|-----|------|
| `backup openclaw data` | 执行备份 |
| `restore openclaw data` | 执行恢复 |

> 注：`backup OpenClaw data`、`backup OPENCLAW data` 等均可触发

### ❌ 不触发示例

以下输入不会触发此 skill，**当作普通对话处理，不给出任何关于本skill的相关提示**：
- `备份`、`请备份`、`帮我备份`、`怎么备份`、`备份OpenClaw`
- `恢复`、`请恢复`、`帮我恢复`、`恢复数据`
- `backup`、`please backup`、`help me backup`
- `restore`、`please restore`、`restore data`

⚠️ **重要规则**：当输入不满足精确匹配时，当作正常对话处理，进行普通对话回复（不要使用 NO_REPLY，不要提示用户输入完整指令）。

---

## 📦 备份流程（中文） / Backup Flow (Chinese)

**触发命令：** `备份openclaw数据`

### 1. 向用户确认

**🔴🔴🔴 重要提醒 🔴🔴🔴**

> **本工具只备份 ~/.openclaw/ 目录下的以下内容：**
> - openclaw.json
> - workspace/
> - agents/
> - cron/
> - media/
> 
> **如果您有文件上传到其他目录，则不会备份，需要您自行核实并手动下载到本地保存,以免数据丢失！**

---

**⚠️⚠️⚠️ 确认声明 ⚠️⚠️⚠️**

> **当您输入"确认"备份，则表示您同意只备份上述目录及文件，其他文件丢失需自行负责。**

是否确认执行备份？请回复 **确认** 或 **取消**。

---

🔗 技术小学生 https://blog.tag.gg

### 2. 用户确认后执行备份

备份完成后会显示：
- 备份文件路径
- 文件大小
- SCP下载命令示例
- 重要提醒

---

## 📥 恢复流程（中文） / Restore Flow (Chinese)

**触发命令：** `恢复openclaw数据`

### 1. 查找备份压缩包

在 ~/.openclaw/ 目录下查找 `OpenClaw-Backup-YYC-*.tar.gz` 格式的压缩包。

### 2. 如果没有找到

提示用户：未找到备份压缩包，请确认是否已上传压缩包到 ~/.openclaw/ 目录。

### 3. 以表格形式列出所有可用备份

显示所有找到的备份文件，以表格形式展示，最新备份加粗标记。

表格示例：
```
| 序号 | 备份文件名                                  | 大小      | 时间               | 备注       |
|------|---------------------------------------------|-----------|--------------------|------------|
|   1  | OpenClaw-Backup-yyc-20260405-195638.tar.gz    | 0.99 MB   | 2026-04-05 19:56:38 | ⭐ 最新       |  ← 加粗
|   2  | OpenClaw-Backup-yyc-20260405-195246.tar.gz    | 0.99 MB   | 2026-04-05 19:52:47 |            |
...
```

### 4. 用户选择序号

提示用户输入序号选择要恢复的备份（直接回车选择最新备份）。

### 5. 向用户确认选择的备份

**⚠️⚠️⚠️ 恢复警告 ⚠️⚠️⚠️**

> **恢复前，现有文件夹将被重命名（添加时间戳后缀）。恢复后数据将覆盖当前配置。**

是否确认恢复选定的备份？请回复 **确认** 或 **取消**。

---

🔗 技术小学生 https://blog.tag.gg

### 6. 用户确认后执行恢复

---

## 📦 Backup Flow (English)

**Trigger Command:** `backup openclaw data`

### 1. Confirm with User

**🔴🔴🔴 IMPORTANT WARNING 🔴🔴🔴**

> **This tool only backs up the following content in ~/.openclaw/ directory:**
> - openclaw.json
> - workspace/
> - agents/
> - cron/
> - media/
> 
> **If you have files uploaded to other directories, they will NOT be backed up. Please verify and manually download them locally to avoid data loss!**

---

**⚠️⚠️⚠️ CONFIRMATION STATEMENT ⚠️⚠️⚠️**

> **When you input "confirm" to backup, you agree that only the above directories and files will be backed up. You are responsible for any other file loss.**

Do you confirm to execute backup? Please reply **confirm** or **cancel**.

---

🔗 技术小学生 https://blog.tag.gg

### 2. Execute Backup After Confirmation

After backup completion, display:
- Backup file path
- File size
- SCP download command example
- Important reminders

---

## 📥 Restore Flow (English)

**Trigger Command:** `restore openclaw data`

### 1. Find Backup Archives

Search for `OpenClaw-Backup-YYC-*.tar.gz` format archives in ~/.openclaw/ directory.

### 2. If Not Found

Prompt user: No backup archive found. Please confirm if you have uploaded the archive to ~/.openclaw/ directory.

### 3. Display All Available Backups in Table Format

Display all backup files in table format, with the latest backup bolded.

Table example:
```
| Seq  | Backup Filename                              | Size      | Time               | Note       |
|------|---------------------------------------------|-----------|--------------------|------------|
|   1  | OpenClaw-Backup-YYC-20260405-195638.tar.gz    | 0.99 MB   | 2026-04-05 19:56:38 | ⭐ Latest  |  ← bold
|   2  | OpenClaw-Backup-YYC-20260405-195246.tar.gz    | 0.99 MB   | 2026-04-05 19:52:47 |            |
...
```

### 4. User Selects by Sequence Number

Prompt user to input sequence number to select backup (press Enter to select latest).

### 5. Confirm with User

**⚠️⚠️⚠️ RESTORE WARNING ⚠️⚠️⚠️**

> **Before restoring, existing folders will be renamed (with timestamp suffix). After restoring, data will overwrite current configuration.**

Do you confirm to restore the selected archive? Please reply **confirm** or **cancel**.

---

🔗 技术小学生 https://blog.tag.gg

### 6. Execute Restore After Confirmation

---

## 备份内容 / Backup Content

| 目录/文件 | 中文说明 | English Description |
|----------|---------|---------------------|
| `openclaw.json` | 主配置文件 | Main config file |
| `workspace/` | 工作空间 | Workspace |
| `agents/` | 多代理配置 | Multi-agent config |
| `cron/` | 定时任务数据 | Cron data |
| `media/` | 媒体缓存 | Media cache |

---

## 备份文件命名格式 / Backup File Naming Format

`OpenClaw-Backup-YYC-YYYYMMDD-HHMMSS.tar.gz`

示例 / Example: `OpenClaw-Backup-YYC-20260404-221500.tar.gz`

---

## 快速使用 / Quick Usage

### 备份数据 / Backup Data

```bash
python scripts/backup.py
```

### 恢复数据 / Restore Data

```bash
python scripts/restore.py <压缩包文件名>
```

---

## 注意事项 / Notes

1. 只备份默认路径 `~/.openclaw/`
2. 恢复前建议再次备份
3. 备份文件建议下载到本地