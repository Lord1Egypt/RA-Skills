# Conversation Logger 📝

> 为 OpenClaw 设计的**按项目/场景自动记录对话**的轻量方案。
> A lightweight, project-based conversation logging system for OpenClaw agents.

## Features

- **Multi-project isolation** — Each project gets its own folder with daily log files
- **Auto-silent logging** — Agent writes structured summaries silently after each turn
- **Daily context continuity** — Auto-reads yesterday's log on the first turn of each day
- **Manual lookup** — On-demand retrieval of historical logs by date or keyword
- **Sub-agent support** — Spawned agents can write to the same daily log

## Quick Start

### 1. Place the skill file

Copy `SKILL.md` to your workspace:

```
{workspace}/skills/conversation-logger/SKILL.md
```

### 2. Create log directories

```powershell
# PowerShell
$projects = @("main", "your-project-a", "your-project-b")
$base = "D:\OpenClaw Memory"
foreach ($p in $projects) { New-Item -ItemType Directory -Path "$base\$p" -Force }
```

```bash
# Linux / macOS
mkdir -p ~/".openclaw-memory"/{main,project-a,project-b}
```

### 3. Update AGENTS.md

Add the conversation logger section to your `AGENTS.md` (see `SKILL.md` for the exact content).

## Log Format

Each entry follows this structure:

```markdown
## YYYY-MM-DD HH:mm

**主题/上下文**: Session summary
**我的提问**: User's core question
**决策/结论**: Decisions, tech choices, config changes
**涉及文件/配置**: File paths, config keys, tools used
```

## Directory Layout

```
D:\OpenClaw Memory\         # or ~/.openclaw-memory/ on Unix
├── main\                   # Default conversations
│   └── memory YYYY-MM-DD.md
├── project-foo\
│   └── memory YYYY-MM-DD.md
└── project-bar\
    └── memory YYYY-MM-DD.md
```

## License

MIT
