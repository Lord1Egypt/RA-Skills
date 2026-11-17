---
name: mem-update
description: Memory Bank Update Workflow — v6.12 compliant with project-repo awareness. Use when the user invokes $mem-update or asks for this workflow by name. Triggers on "update memory bank", "create edit chunk", "update tasks.md", "update session cache", "memory bank update workflow". NOT for database-native workflows (use mb-db-workflow instead).
---

# Memory Bank Update Workflow (v6.12)

## Path Conventions

- `${MB_CORE_PATH}` — path to your local `mb-core` clone (the memory-bank spec repo). Set it as an environment variable; if unset, treat it as a placeholder for wherever you keep the v6.12 rules + templates.
- `<workspace>` — your working root (e.g. the parent of your `memory-bank/` and `code/` directories).
- `<project-repo>` — any project repository that has its own `memory-bank/` directory.


This skill implements the 8-step manual memory bank update workflow from integrated-rules v6.12, enhanced with project-repo awareness. All updates are done by directly editing markdown files — no database involved. For the SQLite/`mb` CLI path, use `mb-db-workflow`.

Merged from `mem-update` and `mb-text-workflow` (faithful §6.5 encoding). Key additions:
- **Step 0:** Project-repo awareness — scan project repos before workspace to prevent duplicate tasks
- **Correct edit-chunk handling:** `edit_history.md` is a GENERATED VIEW — create chunk files, never edit the view directly
- **Correct commit format:** `(type)TID: Headline - Details (% complete)`

## Documentation Philosophy

The memory bank has two complementary documentation layers:

**Chronological Layer** (tells the story):
- Task files — what was done, when, current status
- Session files — work completed in each session
- Edit history — precise record of every file change
- These answer: "What happened? When? In what order?"

**Knowledge Layer** (stores the understanding):
- Implementation docs — architecture, design decisions, APIs, patterns
- Technical context — system architecture, dependencies, constraints
- Product context — goals, user stories, feature specifications
- These answer: "How does this work? Why was it built this way? How do I use it?"

Both layers are essential. The chronological layer without the knowledge layer becomes an unreadable pile of session logs. The knowledge layer without the chronological layer loses traceability and becomes stale. They must be maintained together.

## Prerequisites

Before starting, determine:
1. Current system time and timezone (format: `YYYY-MM-DD HH:MM:SS TZ`)
2. Active task ID being worked on
3. Files modified and their change descriptions
4. Whether implementation documentation needs updating (ALWAYS check this)

## Step 0: Identify Correct Memory Bank Location + Discovery

This skill has TWO Step-0 responsibilities. Handle both before touching any file.

### 0A. Project-Repo Awareness (Location)

- **Check if working on a project:** Before touching ANY memory-bank files, determine:
  - Is there an active project with its own memory-bank? (e.g., ``<project-repo>/memory-bank/``)
  - Is this workspace/infrastructure work? (e.g., ``<workspace>/memory-bank/``)
- **Rule:** Project tasks → project memory-bank. Workspace tasks → workspace memory-bank.
- **Scan locations:**
  - ``<workspace>/code/*/memory-bank/`` (project repos)
  - ``<workspace>/memory-bank/`` (workspace)
  - `${MB_CORE_PATH}/` (mb-core repo for reference)
- **Critical:** If a task exists in a project repo, DO NOT create it in workspace memory-bank.

### 0B. Discovery — What Work Needs Documentation?

**Use this when you do not already have a complete record of what was done.** If you have been tracking work as it happened, skip to the 8-step workflow.

**Use discovery when:**
- You are resuming after a session restart or context loss
- You were not the agent that performed the work
- The user says "update the memory bank" without specifying what changed
- You suspect work was done that you are not aware of

#### 0.1 Check Last Memory-Bank Update
Read `memory-bank/edit_history.md` or `memory-bank/session_cache.md` to find the last update timestamp.

#### 0.2 Examine Git History (if needed)
```bash
cd <project-root>
git log --since="<last-memory-bank-update-date>" --oneline
```

#### 0.3 Check Uncommitted Changes (if needed)
```bash
git status
git diff --stat
```

#### 0.4 Review Existing Edit Chunks
```bash
ls -la memory-bank/edits/
cat memory-bank/edits/YYYY-MM-DD/HHMMSS-*.md
```

#### 0.5 Build Work Summary
| Task ID | Description | Files Changed | Status |
|---------|-------------|---------------|--------|
| Txx | What was done | file1, file2 | in_progress / completed |

**Anti-pattern:** Documenting only what you remember without verifying completeness.

## The 8-Step Workflow

### Step 1: Update Individual Task File

File: `memory-bank/tasks/Txx.md`

If the task file exists, append progress updates. If not, request user approval to create it.

**Status emojis (STRICT):**
- 🔄 = In Progress
- ✅ = Completed
- ⏸️ = Paused
- ❌ = Cancelled

Update `*Last Updated*` timestamp. Keep Progress section current (✅ / 🔄 / ⬜).

### Step 2: Update tasks.md Registry

File: `memory-bank/tasks.md`

MUST use the strict table schema:
```markdown
| ID | Title | Status | Priority | Started | Dependencies | Details |
|----|-------|--------|----------|---------|--------------|---------|
| T1 | [Title] | 🔄 | HIGH | 2025-04-10 | - | [Details](tasks/T1.md) |
```

**Rules:**
- Details column MUST be a link: `[Details](tasks/Txx.md)` or `[Details](archive/Txx.md)`
- Status MUST use standard emojis only (🔄 / ✅ / ⏸️ / ❌)
- Keep active tasks at top, completed below

### Step 3: Update Implementation Documentation (CRITICAL)

**This step is not optional.** Every significant change must be reflected here.

**When to update:**
- New feature or capability → document how it works
- API changed → update usage examples and signatures
- Architecture decision made → document the rationale
- Bug fixed with non-obvious root cause → document for future reference
- Pattern or convention established → document as project standard

**Files to consider:**
- `implementation-details/` — technical deep-dives, architecture decisions
- `techContext.md` — system architecture, dependencies, constraints
- `productContext.md` — goals, user stories, feature specifications
- `systemPatterns.md` — established patterns and conventions
- `activeContext.md` — current focus and recent decisions

**Anti-pattern:** "I'll document it later." Later never comes. Document while the context is fresh.

### Step 4: Handle Session File

File: `memory-bank/sessions/YYYY-MM-DD-PERIOD.md`

Check if current session file exists. If yes, append to it **while preserving all existing content**. If no, create it.

Periods: morning, afternoon, evening, night

### Step 5: Update Session Cache

File: `memory-bank/session_cache.md`

Update the Current Session block, Overview counts, Task Registry, and Session History (last 5). Preserve all existing history.

### Step 6: Update Other Memory Bank Files

- `activeContext.md` — if focus task or current context changed
- `errorLog.md` — if errors were encountered and fixed
- `progress.md` — if milestones were completed
- `changelog.md` — if features or bugs were addressed

### Step 7: Create Edit Chunk (CRITICAL — canonical record)

File: `memory-bank/edits/YYYY-MM-DD/HHMMSS-Txx-edit-chunk.md`

**`edit_history.md` is a GENERATED VIEW — NEVER edit it directly.** The chunk file is the canonical record.

Template:
```markdown
---
kind: edit_chunk
id: [unique-id]
created_at: YYYY-MM-DD HH:MM:SS TZ
task_ids: [Txx]
source_branch: [branch-name]
source_commit: [40-char-sha]
---

#### HH:MM:SS TZ - Txx: Description
- Modified `file/path` - Specific technical change description
- Created `file/path` - What was created and why
```

**STRICT Format Requirements:**
- Header: `#### HH:MM:SS TZ - TaskID: Description` (timezone MANDATORY)
- Bullets: `- Action \`filepath\` - Description`
- Action MUST be one of: `Created`, `Modified`, `Updated`, `Deleted`
- Filepath MUST be in backticks AND relative to project root
- No summary statements or evaluative content

### Step 8: Regenerate edit_history.md

Regenerate `memory-bank/edit_history.md` as a GENERATED VIEW (newest entries on top) from the chunk files. Do not hand-edit it.

## Commit Message Format

```
(type)TID: Headline - Details (% complete)
```

Types: feat, fix, docs, refactor, test
Example: `(feat)T3: Database Migration Complete - Added user table, seed data (90%)`

## Anti-Patterns

- NEVER edit `edit_history.md` directly — always create chunk files and regenerate the view
- NEVER use relative paths or tildes (~) in file operations — absolute paths only (per §1.4)
- NEVER overwrite whole files unless creating new ones — use targeted edits (§1.4)
- NEVER add features without user approval
- NEVER skip the edit chunk step — it's the canonical record
- NEVER delete session files — append-only
- NEVER create a task in workspace memory-bank if it belongs to a project repo (Step 0A)

## References

- `${MB_CORE_PATH}/integrated-rules-v6.12.md` — full v6.12 rules (read Sections 1.4, 1.5, 4.8, 6.5)
- `${MB_CORE_PATH}/memory-bank/templates/` — all file templates
