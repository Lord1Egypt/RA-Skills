---
name: notes-know-you
description: Sync Evernote notebooks to local Markdown, analyze your notes, and update USER.md + Memory files so the AI truly understands who you are
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: [python, pandoc]
      env: [NOTES_DB_PATH]
    primaryEnv: NOTES_DB_PATH
    emoji: "📓"
    os: [darwin, linux, win32]
---

# notes-know-you

通过你的印象笔记，让 AI 真正了解你。

This skill syncs your Evernote/Yinxiang notebooks to local Markdown files, analyzes
the content, and updates the agent's USER.md and Memory files with structured insights —
so your AI assistant always has the right context about who you are.

---

## Configuration

Set the following environment variables before using this skill:

| Variable | Required | Description |
|---|---|---|
| `NOTES_DB_PATH` | Yes | Absolute path to your `evernote-backup` database file (e.g., `F:\notes\en_backup.db`) |
| `NOTES_BACKEND` | No | `china` for Yinxiang (default), `evernote` for international |
| `NOTES_TOKEN` | No | Developer token (use if password auth fails) |
| `NOTES_EXPORT_DIR` | No | Where to write exported Markdown files (default: same directory as db, under `evernote/markdown/`) |
| `NOTES_MEMORY_DIR` | No | Where to write memory files (default: auto-detected) |

---

## Usage

```
/notes-know-you              — full sync: pull → convert → analyze → update memory
/notes-know-you sync         — same as above
/notes-know-you analyze      — skip sync, re-analyze existing Markdown files only
/notes-know-you setup-cron [interval]  — set up recurring auto-sync (e.g., setup-cron 24h)
```

---

## Step-by-Step Instructions

### Step 0 — Check Configuration

1. Verify `NOTES_DB_PATH` is set and the file exists.
2. If not set, ask the user:
   - "Where is your evernote-backup database file?"
   - "Are you using Yinxiang (China) or international Evernote?"
   - "Do you have a developer token?"
3. If the database doesn't exist yet, guide them through first-time setup (see references/setup.md).
4. Determine:
   - `db_path` = `$NOTES_DB_PATH`
   - `db_dir` = parent directory of `db_path`
   - `enex_dir` = `$NOTES_EXPORT_DIR/../enex` or `{db_dir}/evernote/`
   - `markdown_dir` = `$NOTES_EXPORT_DIR` or `{db_dir}/evernote/markdown/`
   - `backend` = `$NOTES_BACKEND` or `china`
   - `skill_scripts_dir` = directory containing this skill's scripts/

### Step 1 — Sync from Evernote

Run:
```bash
python -m evernote_backup sync -d "{db_path}"
```

**If rate limited** (`CRITICAL: Rate limit reached`): stop and tell the user to wait 25–30 minutes before retrying.

**If auth fails**: guide the user to get a developer token:
- Yinxiang: visit `https://app.yinxiang.com/api/DeveloperToken.action` while logged in
- International: visit `https://www.evernote.com/api/DeveloperToken.action`

Then update auth:
```bash
python -m evernote_backup reauth -d "{db_path}" -t "{token}"
```

### Step 2 — Export to ENEX

```bash
python -m evernote_backup export -d "{db_path}" "{enex_dir}"
```

This creates one `.enex` file per notebook under `enex_dir`.

### Step 3 — Convert ENEX to Markdown

For every `.enex` file found recursively under `enex_dir`, run:
```bash
python "{skill_scripts_dir}/enex_to_markdown_bundle.py" "{enex_file}" "{markdown_dir}"
```

This produces one merged Markdown file per notebook (e.g., `Daily.md`, `Books.md`).

Keep a list of all generated Markdown files and their notebook names.

### Step 4 — Analyze Notes Content

Read the generated Markdown files. Notes can be large — skim for structure first, then read
recent entries (last 60 days) in full and older entries at a summary level.

Extract insights by notebook type:

**Diary / Daily notes** (filenames containing: Daily, Diary, Journal, 日记, 每日, 每天):
- Daily routines and recurring habits
- Emotional patterns and frequent concerns
- Goals and aspirations mentioned
- Recent life events (last 30 days) — record with approximate dates

**Work / Project notes** (Work, Project, Todo, Tasks, 工作, 项目):
- Current active projects and their status
- Professional skills and tools used
- Goals and deadlines

**Personal / People notes** (人, People, Friends, Family, 朋友, 家人):
- Key relationships and social context
- Personal values and beliefs expressed

**Reading / Clippings** (Books, 我的剪藏, Clippings, Reading, 读书):
- Topics and domains of sustained interest
- Preferred content formats (books, articles, videos)

**General / Other notebooks**:
- Any recurring themes or topics
- Explicit preferences or opinions stated

### Step 5 — Update USER.md

Locate the memory directory:
1. Check `$NOTES_MEMORY_DIR`
2. Check `.openclaw/` in the current project root
3. Check `~/.claude/projects/{current_project_hash}/memory/`
4. Fall back to creating `.memory/` in the current directory

Read existing `USER.md` if it exists. **Merge, do not overwrite** — preserve facts not
contradicted by the notes.

Write (or update) `USER.md` with this structure:

```markdown
# User Profile

_Last updated from notes: {today's date}_

## Identity
[Name if found, role/occupation if mentioned, location if mentioned]

## Interests & Domains
[Topics that appear frequently — be specific, e.g. "投资/财经" not just "finance"]

## Daily Habits & Routines
[Patterns from diary: sleep schedule, exercise, diet, work patterns]

## Goals
### Short-term (within 3 months)
[Specific goals with any deadlines found]
### Long-term
[Life goals, career goals, major aspirations]

## Values & Principles
[Core values or recurring philosophical themes in the notes]

## Skills & Expertise
[Professional and personal skills with rough proficiency level if inferable]

## Current Context
[What's happening in their life right now — active projects, recent events, current focus]

## Relationships
[Key people mentioned and their relationship to the user]
```

### Step 6 — Write Memory Files

For each significant, specific insight, create a memory file in the memory directory.

Use the formats below, saved as `{type}_{topic}.md`:

**User memory** (personal attributes, preferences, background facts):
```markdown
---
name: {descriptive name}
description: {one-line summary — specific enough to judge relevance}
type: user
---

{fact or insight}
```

**Project memory** (ongoing projects, goals with context):
```markdown
---
name: {project name}
description: {what this project is and why it matters}
type: project
---

{fact or insight}

**Why:** {motivation behind this project}
**How to apply:** {how knowing this should shape AI responses}
```

**Feedback memory** (explicit preferences the user has expressed in notes):
```markdown
---
name: {preference topic}
description: {what the user wants or doesn't want}
type: feedback
---

{the rule or preference}

**Why:** {reason given or inferred from notes}
**How to apply:** {when this guidance is relevant}
```

After writing all memory files, update `MEMORY.md` (the index file) with one line per
new or updated memory:
```
- [Title](file.md) — one-line hook
```

### Step 7 — Report to User

Summarize what was done:

```
✅ Synced {N} notebooks, {M} notes total
📄 Converted to Markdown: {list of notebook names}
👤 USER.md updated — {N} sections changed
🧠 Memory files: {N} created, {M} updated
📌 Top insights extracted:
   1. ...
   2. ...
   3. ...
```

---

## Cron Setup

When the user runs `/notes-know-you setup-cron [interval]`:

1. Default interval: `24h`
2. Parse the interval (e.g., `6h`, `12h`, `24h`, `7d`)
3. Use the agent's cron/scheduler to register a recurring job that runs `/notes-know-you sync`
4. Confirm to the user: "Scheduled notes-know-you to run every {interval}. Next run: {datetime}."

---

## Privacy Note

All note content stays local. Nothing is sent to external services beyond passing note
text through the AI model's context window for analysis. ENEX files and Markdown files
remain on your machine.
