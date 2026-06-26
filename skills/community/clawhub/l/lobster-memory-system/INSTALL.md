# 🦞 龙虾记忆体系统 - 安装指南

## 快速开始

### 方式 1：ClawHub 安装（推荐）

```bash
# 1. 搜索技能
clawdhub search "lobster-memory-system"

# 2. 安装技能
clawdhub install lobster-memory-system

# 3. 初始化
cd ~/.openclaw/skills/lobster-memory-system
powershell -ExecutionPolicy Bypass -File scripts/init.ps1
```

### 方式 2：手动安装

```bash
# 1. 下载技能包（ZIP 或 Git 克隆）
# 2. 复制到 ~/.openclaw/skills/lobster-memory-system
# 3. 运行初始化脚本
powershell -ExecutionPolicy Bypass -File scripts/init.ps1
```

---

## 初始化后配置

### 1️⃣ 编辑身份信息

打开 `memory-system/CORE/identity.json`：

```json
{
  "name": "你的龙虾名字",
  "creature": "AI 助手",
  "vibe": "正式且带点幽默",
  "emoji": "🦞",
  "version": "1.0.0"
}
```

### 2️⃣ 编辑人格设定

打开 `memory-system/CORE/soul.md`，根据你的需求修改人格描述。

### 3️⃣ 配置自动备份

```powershell
cd memory-system/scripts
powershell -ExecutionPolicy Bypass -File setup-auto-backup.ps1
```

这会创建 Windows 任务计划，每天 18:00 自动备份。

### 4️⃣ 配置心跳检查

编辑工作区的 `HEARTBEAT.md`：

```markdown
## 🔄 自我改进检查

### 每次心跳时检查：
- [ ] 分析最近任务的用户反馈
- [ ] 记录需要改进的点（如有）

### 每周日生成周报：
- [ ] 汇总本周改进日志
- [ ] 生成自我改进报告
```

---

## 目录结构说明

```
memory-system/
├── CORE/                    # 核心身份（每次必加载）
│   ├── identity.json        # AI 身份信息
│   ├── soul.md             # 人格设定
│   └── constraints.md      # 行为约束
├── MEMORY/                  # 记忆数据
│   ├── long-term/          # 长期记忆
│   │   ├── preferences.json  # 用户偏好
│   │   ├── knowledge.json    # 知识库
│   │   ├── people.json       # 人员信息
│   │   ├── projects.json     # 项目信息
│   │   └── security-rules.json # 安全规则
│   └── short-term/         # 短期记忆（每日）
│       └── YYYY-MM-DD.json
├── CONFIG/                  # 配置数据
│   ├── channels.json       # 频道配置
│   ├── tools.json          # 工具配置
│   └── permissions.json    # 权限控制
├── SKILLS/                  # 技能注册表
│   └── registry.json
├── SNAPSHOTS/              # 自动备份
│   └── auto-backup-YYYYMMDD.zip
├── scripts/                 # 工具脚本
│   ├── init.ps1            # 初始化
│   ├── check-first-session.ps1
│   ├── auto-backup.ps1
│   └── setup-auto-backup.ps1
└── README.md
```

---

## 使用工作流

### 首次会话（每天）

```powershell
# 检查是否是首次会话
$isFirst = powershell -File scripts/check-first-session.ps1

if ($isFirst -eq "true") {
    # 加载全部记忆
    # 更新 session-tracker.json
}
```

### 其他会话

只加载：
- `CORE/identity.json`
- `MEMORY/long-term/preferences.json`
- `MEMORY/short-term/今日.json`

### 按需加载

使用 `memory_search` 工具搜索历史记忆。

---

## 维护命令

### 手动备份
```powershell
powershell -File scripts/auto-backup.ps1
```

### 查看备份状态
```powershell
Get-ChildItem SNAPSHOTS\*.zip | Sort-Object LastWriteTime -Descending
```

### 恢复备份
```powershell
# 解压备份文件
Expand-Archive -Path SNAPSHOTS\auto-backup-20260420.zip -DestinationPath TEMP\restore\
```

### 清理旧备份
```powershell
# 保留最近 30 天
Get-ChildItem SNAPSHOTS\*.zip | 
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | 
    Remove-Item
```

---

## 故障排除

### 备份失败
```powershell
# 检查任务计划
Get-ScheduledTask -TaskName "LobsterMemoryBackup*"

# 查看日志
Get-Content memory-system/backup-log.txt -Tail 20
```

### 记忆加载异常
```powershell
# 验证 JSON 文件
Get-Content CORE/identity.json | ConvertFrom-Json

# 修复权限
icacls memory-system /grant "$env:USERNAME:(OI)(CI)F" /T
```

### 首次会话检测失败
```powershell
# 重置追踪器
Remove-Item session-tracker.json
```

---

## 升级指南

### 从旧版本升级

1. **备份现有数据**
   ```powershell
   Copy-Item memory-system memory-system.backup -Recurse
   ```

2. **安装新版本**
   ```bash
   clawdhub update lobster-memory-system
   ```

3. **运行迁移脚本**（如有）
   ```powershell
   powershell -File scripts/migrate.ps1
   ```

4. **验证数据**
   ```powershell
   powershell -File scripts/validate.ps1
   ```

---

## 最佳实践

### ✅ 推荐做法

- 每日检查备份日志
- 每周审查改进日志
- 每月清理短期记忆（保留最近 30 天）
- 定期更新 SOUL.md 反映成长

### ❌ 避免做法

- 不要手动修改 JSON 文件（使用脚本）
- 不要删除 CORE 目录
- 不要在群聊中分享记忆文件
- 不要禁用自动备份

---

## 支持

- 📖 完整文档：查看 SKILL.md
- 🐛 问题报告：提交 Issue
- 💡 功能建议：欢迎 PR

---

**让所有龙虾都拥有优秀的记忆力！** 🦞
