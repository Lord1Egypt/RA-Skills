---
name: conversation-logger
description: Project-based conversation logging for OpenClaw. Use when setting up daily auto-logging across parallel projects, building conversational continuity between sessions, or needing file-backed chat history per project folder. Also covers auto-read of previous day logs on first daily turn.
metadata: {"clawdbot":{"emoji":"📝","requires":{"anyBins":[]},"os":["linux","darwin","win32"]}}
---

# Conversation Logger

Auto-write structured daily conversation summaries into project-specific folders. Each project gets its own directory with daily log files, auto-read on first turn each day, and on-demand manual lookup.

## When to Use

- Setting up daily auto-logging for multiple parallel projects
- Building conversation continuity — agent auto-reads yesterday's log on first daily turn
- Organizing chat history by project folder, not by session
- Enabling on-demand historical lookup ("show me yesterday's LED project log")
- Any OpenClaw workspace with multiple project contexts that need isolated histories

## Setup

### 1. Create the Skill File

Place this `SKILL.md` at:

```
{workspace}/skills/conversation-logger/SKILL.md
```

### 2. Create Log Directories

```powershell
# PowerShell
$projects = @("main", "my-project-a", "my-project-b")
$base = "D:\OpenClaw Memory"
foreach ($p in $projects) {
    New-Item -ItemType Directory -Path "$base\$p" -Force
}
```

```bash
# Linux / macOS
mkdir -p ~/".openclaw-memory"/{main,my-project-a,my-project-b}
```

### 3. Update AGENTS.md

```markdown
### 🗂️ 项目对话日志（Conversation Logger）

参考 skill: `skills/conversation-logger/SKILL.md`

**自动记录结构：**
- 每次对话结束，**静默**追加结构化摘要到 `D:\OpenClaw Memory\{project}\memory YYYY-MM-DD.md`
- 格式：主题/上下文 → 我的提问 → 决策/结论 → 涉及文件/配置

**每日首次自动调取：**
- 当天第一次对话时，读取前一日对应项目的日志作为上下文
- 当天内如需调取过往日志，手动要求即可

**当前项目文件夹映射：**
| 项目/场景 | 文件夹 |
|---|---|
| 日常主对话 | `main` |
| 项目 Foo | `project-foo` |
| 项目 Bar | `project-bar` |
```

## Log Entry Format

Each log entry follows this template:

```markdown
## YYYY-MM-DD HH:mm

**主题/上下文**: [session summary in one line]
**我的提问**: [user's core question]
**决策/结论**: [confirmed decisions, tech choices, config changes]
**涉及文件/配置**: [file paths, config keys, tools used]
```

**Example:**

```markdown
## 2026-07-24 16:42

**主题/上下文**: Setting up Conversation Logger project logging system
**我的提问**: Create per-project conversation log folders with auto-daily recording
**决策/结论**:
- File format: `memory YYYY-MM-DD.md`
- Project folders: `main` / `led-app` / `led-grid` / `slash-fit` / `vired`
- Log granularity: structured summary (topic + question + decision + files)
- Auto-read: previous day's log on first daily turn; manual lookup within same day
- No backfill — start recording from now
**涉及文件/配置**:
- Directories created under `D:\OpenClaw Memory\`
- Skill: `skills/conversation-logger/SKILL.md`
- `AGENTS.md` updated with logging section
```

## Write Rules

1. **Write silently**: Append a structured summary at the end of each conversation turn. The write action produces **no user-visible output**.
2. **No duplicates**: Write once per turn; never re-write the same entry.
3. **Append always**: New entries go at the end of the daily file.
4. **Auto-create**: If today's log file doesn't exist, create it.

## Read Rules

### Auto-read (First Turn Each Day)

1. On the first user message of the day for a given project, check if the current day's log file is empty or nonexistent.
2. If first turn of the day, read the **previous day's log file**.
3. If previous day file doesn't exist, skip silently.
4. Use the loaded content as conversation context.

### Manual Lookup

| User Request | Agent Action |
|---|---|
| "Show yesterday's logs" | Read previous day's file, display content |
| "Show logs for [date]" | Read specified date's file |
| "Search for [keyword]" | Scan all `.md` files in the project folder |
| "Show this week's logs" | Iterate last 7 days of files |

## Project-Folder Mapping

Maintain this mapping table in `AGENTS.md`:

```markdown
| 项目/场景 | 文件夹 |
|---|---|
| Daily main conversation | `main` |
| Project Alpha | `alpha` |
| Project Beta | `beta` |
```

When spawning sub-agents, pass the project folder name in the task prompt so the child agent writes to the correct directory.

## Directory Layout

```
D:\OpenClaw Memory\         # or ~/.openclaw-memory/ on Unix
├── main\                   # Default/main conversations
│   └── memory 2026-07-24.md
├── alpha\                  # Project Alpha
│   └── memory 2026-07-24.md
├── beta\                   # Project Beta
│   └── memory 2026-07-24.md
└── ...
```

Cross-platform note: On Linux/macOS, use `~/".openclaw-memory"` instead of `D:\OpenClaw Memory`. Update the base path in AGENTS.md accordingly.

## Sub-Agent Integration

When delegating work to sub-agents via `sessions_spawn`, add this instruction to the task prompt:

```
Conversation log: write a structured summary to D:\OpenClaw Memory\{project-folder}\memory YYYY-MM-DD.md after this task.
```

This ensures sub-agents also contribute to the same daily log.

## Tips

- Start from "now" — don't backfill past conversations. The first real log entry is the first conversation after setup.
- Keep entries short (3-5 lines per turn). Long entries defeat the purpose of lightweight context loading.
- The `main` folder is the catch-all. Route unknown/unaffiliated conversations there.
- When the user says "this conversation is about Project X" mid-chat, start writing to the project folder from that point forward.
- File names include a space: `memory YYYY-MM-DD.md` — scripts that parse these should handle spaces.
- The write is intentionally silent. Don't mention the log write in your reply to the user unless explicitly asked.
- If a write fails (permissions, missing directory), continue the conversation normally. Logging is a nice-to-have, not a blocker.
- Use `read` to check whether today's file already exists before deciding if it's the first turn of the day.
- The project-folder mapping table should live in AGENTS.md, not inside the skill, so it's easy to customize per workspace.
