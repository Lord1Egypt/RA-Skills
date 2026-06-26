# Long-term Task Progress Management (LTPM)

> A universal protocol for managing long-term, multi-stage projects in AI agent systems.

**Version**: 2.1  
**Purpose**: Transform short-term conversation memory into structured long-term documents for seamless project resumption.

---

## Overview

LTPM ensures you can instantly understand your project status after days or weeks:

1. **What** the project aims to achieve
2. **Where** you left off  
3. **What** needs to be done next

### Design Philosophy

- **Passive Mechanism**:利用 HEARTBEAT.md 机制防止进度丢失
- **Active Mechanism**: 关键里程碑主动记录
- **Dual-track Collaboration**: 平衡系统健壮性与资源消耗

---

## Quick Start

```bash
# Create project structure
projects/
└── {project_name}/
    ├── MISSION.md        # Project goals
    ├── PROGRESS.md       # Current status
    └── NEXT_STEPS.md     # Action items
```

### Core Commands

| Command | Description |
|---------|-------------|
| `init_project {name}` | Initialize new project |
| `checkpoint` | Save current progress (active) |
| `resume {project}` | Load project context |
| `next` | Show next action |
| `mark_milestone {desc}` | Mark key milestone |
| `auto_sync_status` | Check sync status |

---

## v2.1 New Features

### 1. Dynamic Thresholds
Adaptive silence thresholds based on project complexity and session activity:

| Complexity | Files | Base Threshold |
|------------|-------|----------------|
| Simple | <10 | 15 min |
| Medium | 10-50 | 10 min |
| Complex | 50-200 | 5 min |
| Very Complex | >200 | 3 min |

### 2. File Watcher (Low Resource Mode)
Use `fswatch` for file change detection when system resources allow.

### 3. Conflict Resolution
- Timestamp-based conflict detection
- Last-write-wins strategy
- Automatic `.auto-save` backup before overwrite

### 4. Explicit Active Triggers
Prompt templates to remind users when to record progress:

```
✓ Complete significant tasks
✓ Make important decisions
✓ End work session
✓ Achieve milestones
```

### 5. Natural Language Triggers

**Chinese**: 开始/进度/完成/暂停/结束/里程碑  
**English**: start/progress/completed/pause/end/milestone

### 6. Structured Format Support
Optional JSON/YAML formats alongside Markdown.

---

## Document Templates

### MISSION.md
```markdown
# {Project Name}

**Created**: {YYYY-MM-DD}
**Status**: Active / Paused / Completed

## Vision
What are we building?

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### PROGRESS.md
```markdown
# Progress: {Project Name}

**Last Updated**: {YYYY-MM-DD}
**Overall Progress**: {x%}

## Current Stage
{Stage description}

## Milestones
- [x] Completed
- [ ] In Progress
- [ ] Pending

## Recent Activity
- {YYYY-MM-DD}: {Activity}
```

### NEXT_STEPS.md
```markdown
# Next Steps: {Project Name}

## Immediate Priority
1. [ ] Task 1
2. [ ] Task 2
```

---

## Configuration

Create `.ltpm/config.json`:

```json
{
  "version": "2.1",
  "thresholds": {
    "simple": 15,
    "medium": 10,
    "complex": 5
  },
  "backup": {
    "enabled": true,
    "max_count": 5
  },
  "format": {
    "default": "markdown"
  }
}
```

---

## Requirements

| Tool | Purpose |
|------|---------|
| `fswatch` | File watcher (optional) |
| `jq` | JSON processing |
| `python3` | Script execution |

---

*LTPM v2.1 - Smart, adaptive, robust project management for AI agents.*

**Version History**: v1.0 → v2.0 → v2.1
