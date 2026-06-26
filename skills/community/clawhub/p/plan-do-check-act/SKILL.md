---
name: plan-do-check-act
description: PDCA workflow automation with session binding and progress recovery. Requires Python 3.6 and Git (optional).
---

# Plan-Do-Check-Act Skill

This skill implements the PDCA (Plan-Do-Check-Act) workflow to ensure tasks are systematically planned and executed.

## Requirements

- **Python 3.6+** - Required for all scripts
- **Git** - **Optional** - Only used for progress tracking. PDCA works perfectly without Git - it will use file modification times instead.

## Setup Guide (First Time)

After installing, run the setup wizard:

```bash
# Run interactive setup
python3 scripts/setup.py
```

The wizard will:
1. Check Python and Git dependencies
2. Create workspace directory (default: `~/pdca-workspace`)
3. Create a test plan
4. Optionally initialize Git for progress tracking
5. Show next steps

### Manual Setup

If you prefer manual setup:

```bash
# 1. Create workspace directory
mkdir -p ~/pdca-workspace

# 2. Create a test plan
cd ~/pdca-workspace
manage_plan.py create "My First Plan" "Task 1" "Task 2" "Task 3"

# 3. Verify it works
manage_plan.py check plan.md

# 4. (Optional) Set up git for progress tracking
git init
```

## Security Notes

- **Workspace Scope:** Only operates on `plan*.md` files in the configured workspace directory
- **Destructive Operations:** `cleanup` command deletes archived files older than specified days (default 7)
- **User Confirmation:** Archive operation prompts for confirmation if plan is not completed
- **Dry Run:** Use `cleanup --dry-run` to preview before deleting
- **Autonomous Invocation:** Should require user confirmation before cleanup/archive operations

---

## Core Process

### 1. Plan
When receiving a user task, create `plan.md`:
- Break down the task into executable subtasks
- Record the session ID
- Mark priorities and dependencies

### 2. Do
Execute tasks according to plan.md:
- Check off each completed task `[x]`
- Mark in-progress tasks as `[>]`
- Record issues during execution

### 3. Check
After all tasks are completed:
- Check for any missed items
- Verify output meets expectations
- Identify areas for improvement

### 4. Act
Based on check results:
- Fix identified issues
- Update plan.md with learnings
- Archive or iterate

---

## plan.md Template

```markdown
# Task Plan: [Task Name]

**Session:** discord:1488795270769676318
**Created:** YYYY-MM-DD HH:MM
**Status:** IN_PROGRESS | COMPLETED | PAUSED

## Current Task

> Task 3 - Implement Login API (in progress)

## Checklist

- [x] Task 1 - Database Design
- [x] Task 2 - User Model Creation
- [>] Task 3 - Implement Login API (in progress)
- [ ] Task 4 - Implement Registration API
- [ ] Task 5 - Unit Testing

## Notes

Records during execution...

## Check Results

Fill in after completion...
```

---

## Trigger Scenarios

### Core Logic: Step Analysis

After receiving a task, quickly analyze **how many steps are needed**:

**1-2 steps** → Execute directly, no plan
- "Rename a file"
- "Delete that test file"

**3-5 steps** → Optional plan (ask user)
- "Help me build a login feature"

**5+ steps** → Auto trigger PDCA
- "Build a complete user system with registration and login"
- "Refactor this project from React to Vue"

### Step Analysis Dimensions

| Dimension | 1 step | 2-3 steps | 5+ steps |
|-----------|--------|-----------|----------|
| **File Changes** | Single file | 2-3 files | Multiple modules/dirs |
| **Dependencies** | None | Simple | Multi-layer/sequential |
| **Tech Stack** | Single tech | 2 techs | Full-stack/multi-service |
| **Testing** | No testing | Simple validation | Full test suite |
| **Deploy/Config** | No deploy | Local run | Deploy + config + docs |

### Keyword Triggers

Trigger regardless of step count when user explicitly requests:
- "break down", "decompose", "plan", "checklist"
- "plan", "checklist", "todo", "track"

---

## Session Binding

### plan.md Records Session ID

```markdown
**Session:** discord:1488795270769676318
```

### Categorized Display After Wake

```
Uncompleted plans for current session:
1. plan.md - User System Development (2/5)

Uncompleted plans for other sessions:
2. plan-blog.md - Blog Setup (1/3) ← telegram:123456
```

---

## Interruption Recovery

### Two Interruption Scenarios

| Scenario | Handling |
|----------|----------|
| **Unexpected** (network down, crash) | Check file modifications within 10 minutes |
| **Manual Pause** ("pause for now") | Use `PAUSED` status explicitly |

### Progress Inference (Active Check)

1. **Check git status** - Uncommitted changes
2. **Check file modification time** - Files within 10 minutes
3. **Compare task description** - Keyword matching
4. **Identify task type** - Code/Test/Deploy/Docs/General
5. **Ask user confirmation** - Final confirmation

### Recovery Flow

```
Wake → on-start → Read plan.md → Check files within 10 min
                                    ↓
                    "login_api.py modified 3 min ago, continue?"
```

---

## Consumption Mechanism

### Status Flow

```
CREATED → IN_PROGRESS → PAUSED ↔ RESUMED → COMPLETED → ARCHIVED
```

### Execution Rules

- Consume one task at a time
- Check off immediately upon completion `[x]`
- Skip and record if blocked

### Concurrency Control

- Only one active plan at a time
- When new task arrives: if incomplete plan exists → ask "Finish previous or create new?"

---

## Destruction Mechanism

### Archive Strategy

| Status | Retention | Action |
|--------|-----------|--------|
| **COMPLETED** | 7 days | Move to `archive/plan-YYYY-MM-DD-taskname.md` |
| **PAUSED** | 30 days | Ask user to continue or delete |
| **STALE** (no update >14 days) | Immediate | Mark as `ABANDONED`, wait for confirmation |

### Cleanup Commands

```bash
# Archive completed
manage_plan.py archive

# Cleanup expired files (>7 days)
manage_plan.py cleanup --days 7

# List all plans
manage_plan.py list
```

---

## Usage

### Agent Workflow

### Trigger Conditions

**Automatically trigger PDCA when user:**
- Asks about incomplete tasks: "What's not done?", "What's pending?", "Any unfinished tasks?"
- Asks about progress: "How's it going?", "Progress check", "What's the status?"
- Asks about the plan: "What's the plan?", "Show me the plan"
- Submits a complex task (5+ steps)
- Explicitly requests: "break down", "create a plan", "make a checklist"

### Plan Phase
1. Analyze steps with `analyze_steps.py`
2. If 5+ steps → create plan.md
3. **Output plan content to user**

### Do Phase
1. Execute tasks one by one
2. After each task → update plan.md
3. **Report progress to user**

**Example:**
```
「✓ Task 1 complete (Database Design)
→ Starting Task 2 (User Model Creation)」
```

### Check Phase
1. When user asks "What's not done?" → run `manage_plan.py on-start`
2. Output incomplete plans with progress
3. **Example response:**
```
「You have 1 incomplete plan:

**User System Development** (2/5 complete)
✓ Database Design
✓ User Model Creation
○ Implement Login API (in progress)
○ Implement Registration API
○ Unit Testing

Next task: Implement Login API」
```

### Act Phase
1. Fix identified issues
2. Archive completed plans

### Create Plan

```bash
# Simple create
manage_plan.py create "User System" "Database Design" "User Model" "Login API"

# With session
manage_plan.py create "User System" "Task 1" "Task 2" \
  --session "discord:1488795270769676318"

# Specify output file
manage_plan.py create "Blog Setup" "Buy Domain" "Deploy" \
  --output plan-blog.md
```

### Update Status

```bash
# Complete tasks 1 and 2
manage_plan.py update plan.md --completed 0,1

# Mark current task (in progress)
manage_plan.py update plan.md --current 2
```

### Pause/Resume

```bash
# Pause
manage_plan.py pause plan.md --reason "Waiting for API response"

# Resume
manage_plan.py resume plan.md
```

### Session Start Check

```bash
# Check incomplete plans
manage_plan.py on-start . "discord:1488795270769676318"
```

### Progress Check

```bash
# Check current progress
manage_plan.py check plan.md

# Detailed progress check (with git and files)
python3 scripts/check_progress.py . plan.md
```

---

## Scripts

| Script | Function |
|--------|----------|
| `manage_plan.py` | Main management script (create/update/pause/resume/archive) |
| `check_progress.py` | Progress check (git + file modification + keyword matching) |
| `analyze_steps.py` | Step analysis (decide whether to plan) |
| `check_deps.py` | Dependency check |

---

## Configuration

Default workspace: `~/.openclaw/workspace/`
Plan files: `plan.md` or `plan-*.md`
Archive directory: `archive/`

**Security:**
- Only operates on `plan*.md` files in the workspace
- Does not modify non-plan files
- Archive/cleanup only affects `archive/` directory
- Use `--dry-run` to preview cleanup before deleting
