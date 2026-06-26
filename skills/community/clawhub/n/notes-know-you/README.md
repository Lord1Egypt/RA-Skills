# notes-know-you · 笔记懂你

> 把你的印象笔记变成 AI 对你的深度理解。
> Turn your Evernote notebooks into deep AI knowledge about you.

通过同步印象笔记内容、分析你的日记和笔记，自动更新 AI 的 `USER.md` 和 Memory 文件，让 AI 助手真正了解你是谁、你在做什么、你关心什么。

By syncing your Evernote/Yinxiang notebooks, analyzing your diaries and notes, and automatically updating the AI's `USER.md` and Memory files — so your AI assistant truly knows who you are, what you're working on, and what matters to you.

---

## 目录 · Contents

- [功能 · Features](#功能--features)
- [快速开始 · Quick Start](#快速开始--quick-start)
- [用法 · Usage](#用法--usage)
- [工作原理 · How It Works](#工作原理--how-it-works)
- [配置 · Configuration](#配置--configuration)
- [依赖 · Dependencies](#依赖--dependencies)
- [隐私说明 · Privacy](#隐私说明--privacy)

---

## 功能 · Features

- **全量同步** — 拉取所有笔记本，无需手动选择
  **Full sync** — pulls all your notebooks automatically
- **智能分析** — 按笔记本类型（日记、工作、阅读、人际）提取不同维度的洞察
  **Smart analysis** — extracts insights by notebook type (diary, work, reading, relationships)
- **USER.md 更新** — 生成结构化用户画像（兴趣、习惯、目标、价值观）
  **USER.md update** — builds a structured user profile (interests, habits, goals, values)
- **Memory 写入** — 将具体事实写入独立 Memory 文件，支持 user / project / feedback 三种类型
  **Memory writing** — writes specific facts into Memory files (user / project / feedback types)
- **增量合并** — 不覆盖现有 Memory，只补充和更新
  **Incremental merge** — never overwrites existing Memory, only adds and updates
- **定时运行** — 支持配置 cron 定期自动同步
  **Scheduled sync** — supports cron for recurring automatic runs
- **双平台兼容** — 同时支持 OpenClaw (`USER.md`) 和 Claude Code (memory 目录)
  **Dual-platform** — compatible with both OpenClaw and Claude Code memory systems

---

## 快速开始 · Quick Start

### 1. 安装依赖 · Install dependencies

```bash
pip install evernote-backup beautifulsoup4 lxml
```

macOS:
```bash
brew install pandoc
```

Windows:
```bash
winget install JohnMacFarlane.Pandoc
```

> 详细安装说明见 [references/setup.md](references/setup.md)
> Full installation guide: [references/setup.md](references/setup.md)

### 2. 初始化数据库 · Initialize database

印象笔记（中国区）· Yinxiang (China):
```bash
python -m evernote_backup init-db --backend china -d "path/to/en_backup.db" -t "YOUR_TOKEN"
```

国际版 · International:
```bash
python -m evernote_backup init-db -d "path/to/en_backup.db" -t "YOUR_TOKEN"
```

> 获取 Token · Get your token:
> 中国区: `https://app.yinxiang.com/api/DeveloperToken.action`
> 国际版: `https://www.evernote.com/api/DeveloperToken.action`

### 3. 设置环境变量 · Set environment variables

```bash
export NOTES_DB_PATH="/path/to/en_backup.db"
export NOTES_BACKEND="china"   # 中国区用户必填 / required for Yinxiang
```

### 4. 运行 · Run

```
/notes-know-you
```

---

## 用法 · Usage

| 命令 · Command | 说明 · Description |
|---|---|
| `/notes-know-you` | 完整流程：同步 → 转换 → 分析 → 更新 Memory<br>Full pipeline: sync → convert → analyze → update |
| `/notes-know-you sync` | 同上 · Same as above |
| `/notes-know-you analyze` | 跳过同步，只重新分析已有 Markdown<br>Skip sync, re-analyze existing Markdown only |
| `/notes-know-you setup-cron 24h` | 设置每 24 小时自动运行<br>Schedule automatic sync every 24h |

---

## 工作原理 · How It Works

```
印象笔记云端          本地数据库           ENEX 文件           Markdown
Evernote Cloud  →  en_backup.db   →   *.enex files   →   *.md files
                   (evernote-backup)  (evernote-backup)  (pandoc + scripts)
                                                               ↓
                                                         AI 分析 · AI Analysis
                                                               ↓
                                              ┌────────────────┴────────────────┐
                                         USER.md                        Memory files
                                       用户画像                        具体事实/项目/偏好
                                      User Profile                  Facts / Projects / Prefs
```

**分析维度 · Analysis dimensions:**

| 笔记本类型 · Notebook type | 提取内容 · What's extracted |
|---|---|
| 日记 / Daily | 习惯、情绪、近期事件、日常规律 · Habits, emotions, recent events, routines |
| 工作 / Work | 当前项目、技能、目标、截止日期 · Projects, skills, goals, deadlines |
| 人 / People | 人际关系、价值观 · Relationships, values |
| 阅读 / Reading | 兴趣领域、阅读偏好 · Interests, reading preferences |

---

## 配置 · Configuration

| 环境变量 · Variable | 必填 · Required | 默认值 · Default | 说明 · Description |
|---|---|---|---|
| `NOTES_DB_PATH` | ✅ | — | evernote-backup 数据库路径 · Database file path |
| `NOTES_BACKEND` | — | `china` | `china` 或 `evernote` |
| `NOTES_TOKEN` | — | — | 开发者 Token（认证失败时使用）· Developer token |
| `NOTES_EXPORT_DIR` | — | `{db_dir}/evernote/markdown/` | Markdown 输出目录 · Markdown output directory |
| `NOTES_MEMORY_DIR` | — | 自动检测 · Auto-detected | Memory 文件写入目录 · Memory files directory |

**Memory 目录自动检测顺序 · Auto-detection order:**
1. `$NOTES_MEMORY_DIR`
2. `.openclaw/` (OpenClaw project)
3. `~/.claude/projects/{hash}/memory/` (Claude Code)
4. `.memory/` (fallback)

---

## 依赖 · Dependencies

| 工具 · Tool | 用途 · Purpose | 安装 · Install |
|---|---|---|
| Python 3.9+ | 运行脚本 · Run scripts | [python.org](https://python.org) |
| pandoc | HTML → Markdown 转换 · Conversion | `brew install pandoc` / `winget install JohnMacFarlane.Pandoc` |
| evernote-backup | 同步印象笔记 · Sync Evernote | `pip install evernote-backup` |
| beautifulsoup4 | 解析 ENML · Parse ENML | `pip install beautifulsoup4` |
| lxml | XML 解析 · XML parsing | `pip install lxml` |

---

## 隐私说明 · Privacy

所有笔记数据均在本地处理，不上传到任何第三方服务。笔记内容仅在分析阶段经过 AI 模型的上下文窗口，`.enex` 文件和生成的 Markdown 文件始终保留在你的本地磁盘。

All note data is processed locally and never uploaded to any third-party service. Note content only passes through the AI model's context window during the analysis step. ENEX files and generated Markdown files always remain on your local disk.

---

## License

MIT-0
