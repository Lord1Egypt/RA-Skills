---
name: mem-load
description: Global workflow for loading memory bank files based on recent activity and context Use when the user invokes $mem-load or asks for this workflow by name.
---

# mem-load

This skill is a Codex conversion of a personal Windsurf global workflow. Follow the workflow below, adapting Windsurf-specific slash-command wording to Codex skill invocation. If the workflow mentions running `/mem-load`, treat that as explicit invocation of `$mem-load`.

# Memory Load Workflow (mem-load)

## Purpose
Load relevant memory bank files by analyzing recent activity and context to determine which implementation docs are needed.

## Loading Logic

### Step 1: Load Core Context Files
```bash
read memory-bank/activeContext.md
read memory-bank/session_cache.md
```

### Step 2: Identify Most Recent Activity
Analyze the loaded context to determine:
- **Current Task**: Which task ID is marked as active focus
- **Recent Session**: Which session file has the most recent timestamp
- **Last Updated**: Which task or session files were modified most recently

### Step 3: Load Recent Task/Session Files
Based on the analysis from Step 2:

```bash
# Load current task file if ID identified
read memory-bank/tasks/T{ID}.md

# Load most recent session file
read memory-bank/sessions/YYYY-MM-DD-PERIOD.md
```

### Step 4: Determine Implementation Docs to Load
Based on the task and session context:

**Load these implementation docs if referenced or relevant:**
- Any implementation-detail files mentioned in task file
- Any files referenced in session working state
- Technical context if implementation approach unclear

```bash
# Load implementation docs as needed (examples)
read memory-bank/implementation-details/[specific-file].md
read memory-bank/techContext.md  # Only if technical details needed
read memory-bank/systemPatterns.md  # Only if architectural context needed
```

## Decision Logic

```
START
├─ Load activeContext.md + session_cache.md
├─ Identify current task ID and recent session file
├─ Load current task file + recent session file
├─ Check for implementation doc references
│  ├─ References found → Load those specific docs
│  └─ No references → Load based on task type
│     ├─ Implementation task → Load techContext.md
│     ├─ Architecture task → Load systemPatterns.md
│     └─ Other task → No additional docs needed
└─ Complete loading
```

## Loading Commands

### Core Load (Always)
```bash
read memory-bank/activeContext.md
read memory-bank/session_cache.md
```

### Contextual Load (Based on analysis)
```bash
# Task file (if current task identified)
read memory-bank/tasks/T{ID}.md

# Recent session file
read memory-bank/sessions/YYYY-MM-DD-PERIOD.md

# Implementation docs (only if referenced or needed)
read memory-bank/implementation-details/[specific-file].md
read memory-bank/techContext.md
read memory-bank/systemPatterns.md
```
