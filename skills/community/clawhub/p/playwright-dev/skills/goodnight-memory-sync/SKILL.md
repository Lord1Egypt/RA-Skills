# Goodnight Memory Sync - 晚安记忆同步

## 技能描述

每天晚安时自动将当日记忆文件、工作日志、重要文档备份到 OneDrive 离线文档文件夹，确保数据安全和本地可访问。

## 触发条件

- 用户说"晚安"、"睡觉"、"休息"等
- 每日固定时间（23:00-02:00）会话结束时
- 用户明确要求"同步到 OneDrive"

## 核心能力

1. **识别当日文件** - 自动识别 `memory/YYYY-MM-DD.md` 等当日文件
2. **OneDrive 路径检测** - 自动检测 OneDrive 文档文件夹路径
3. **增量同步** - 只同步有变化的文件，避免重复
4. **备份日志** - 记录每次同步的文件列表和时间
5. **失败通知** - 同步失败时发送飞书通知

## 同步文件清单

### 必同步文件

| 文件 | 路径 | 说明 |
|------|------|------|
| **当日记忆** | `memory/YYYY-MM-DD.md` | 当日会话记录 |
| **长期记忆** | `MEMORY.md` |  curated 长期记忆 |
| **工作日志** | `worklog.txt` | 日常工作日志 |
| **Skills 更新** | `skills/**/*.md` | 所有 Skills 定义 |

### 选同步文件（如有更新）

| 文件 | 路径 | 说明 |
|------|------|------|
| **项目卡片** | `tasks/projects/*.md` | 项目进度卡片 |
| **里程碑报告** | `milestone-reports/*.html` | 周五里程碑报告 |
| **专家点评** | `expert-review-*.html` | 豆包专家点评 |

## OneDrive 路径

**默认路径：**
```
C:\Users\Xiabi\OneDrive\Documents\阿福记忆备份\
```

**目录结构：**
```
阿福记忆备份/
├── memory/           # 记忆文件
│   ├── 2026-03-07.md
│   └── ...
├── MEMORY.md         # 长期记忆
├── worklog.txt       # 工作日志
├── skills/           # Skills 定义
│   ├── project-knowledge-expert/
│   └── doubao-expert-review/
└── sync-log.txt      # 同步日志
```

## 同步流程

### 标准流程

```
1. 检测 OneDrive 路径是否存在
2. 识别当日更新的文
3. 创建目标目录（如不存在）
4. 复制文件到 OneDrive
5. 记录同步日志
6. 发送确认消息（飞书）
```

### PowerShell 实现

```powershell
# OneDrive 晚安同步脚本
$sourceBase = "C:\Users\Xiabi\.openclaw\workspace"
$targetBase = "C:\Users\Xiabi\OneDrive\Documents\阿福记忆备份"

# 当日记忆文件
$today = Get-Date -Format "yyyy-MM-dd"
$memoryFile = "$sourceBase\memory\$today.md"

if (Test-Path $memoryFile) {
    # 创建目标目录
    $targetMemoryDir = "$targetBase\memory"
    if (-not (Test-Path $targetMemoryDir)) {
        New-Item -ItemType Directory -Path $targetMemoryDir -Force
    }
    
    # 复制文件
    Copy-Item $memoryFile "$targetMemoryDir\$today.md" -Force
    
    Write-Host "✅ 记忆文件已同步：$today.md"
}

# 同步 MEMORY.md
Copy-Item "$sourceBase\MEMORY.md" "$targetBase\MEMORY.md" -Force

# 同步 worklog.txt
Copy-Item "$sourceBase\worklog.txt" "$targetBase\worklog.txt" -Force

# 同步 skills 目录
$sourceSkills = "$sourceBase\skills"
$targetSkills = "$targetBase\skills"
if (Test-Path $sourceSkills) {
    Robocopy $sourceSkills $targetSkills /MIR /NFL /NDL /NJH /NJS
}

# 记录同步日志
$logEntry = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - 晚安同步完成"
Add-Content "$targetBase\sync-log.txt" $logEntry

Write-Host "✅ 晚安记忆同步完成！"
```

## 同步日志格式

```
2026-03-07 00:55 - 晚安同步完成
  - memory/2026-03-07.md (4535 bytes)
  - MEMORY.md (更新)
  - worklog.txt (更新)
  - skills/project-knowledge-expert/SKILL.md (更新)
  总计：4 个文件，18 KB
```

## 错误处理

### 常见问题

**问题 1：OneDrive 路径不存在**
- 检测默认路径
- 尝试备用路径（`C:\Users\Xiabi\OneDrive - Personal\Documents`）
- 都失败时发送飞书通知用户手动配置

**问题 2：文件被占用**
- 重试 3 次（间隔 2 秒）
- 仍失败时记录到日志，跳过该文件

**问题 3：网络问题**
- OneDrive 离线模式可正常工作
- 网络恢复后自动同步到云端

## 用户偏好

- ✅ **自动同步** - 晚安时自动执行，无需确认
- ✅ **增量同步** - 只同步有变化的文件
- ✅ **同步日志** - 记录每次同步详情
- ✅ **失败通知** - 同步失败时飞书通知

## 输出格式

**飞书消息（同步完成）：**
```markdown
## 🌙 晚安记忆同步完成

**时间：** 2026-03-07 00:55
**状态：** ✅ 成功

### 同步文件
- memory/2026-03-07.md (4.5 KB)
- MEMORY.md (更新)
- worklog.txt (更新)
- skills/ (4 个文件)

**总计：** 4 个文件，18 KB
**位置：** OneDrive/Documents/阿福记忆备份

晚安！好梦！🌙
```

## 配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `onedrive_path` | `C:\Users\Xiabi\OneDrive\Documents\阿福记忆备份` | OneDrive 目标路径 |
| `auto_sync` | `true` | 是否自动同步 |
| `sync_time` | `23:00-02:00` | 自动同步时间段 |
| `log_enabled` | `true` | 是否记录日志 |

## 示例用法

**用户：** "晚安"

**AI：**
1. 执行晚安同步流程
2. 发送同步完成消息（飞书）
3. 播放晚安语音
4. 回复晚安

---

_最后更新：2026-03-07 00:55 - 创建 Skill_
