# Project Management System

> A universal project management foundation. Any agent with this system can manage projects from initiation to acceptance.

## What is This?

A complete project management framework covering the full process from project initiation to delivery.

**Core Features:**
- 📋 **Full lifecycle management** — Initiate project, execute, review, deliver
- 📚 **14 documentation files** — Detailed rules for each stage
- 📝 **10 templates** — Ready-to-use project documents
- ✅ **Quality gates** — Built-in review and acceptance mechanisms
- 🔄 **Self-sustaining** — Runtime recovery and self-loop guarantee

## Installation

### Method 1: Clone from GitHub (Recommended)

```bash
git clone https://github.com/openclaw/project-management.git
cd project-management

# Fill in your resources
# Edit resource-profiles.md to record your agents and tools
```

### Method 2: Download ZIP

Download and extract from [GitHub Releases](https://github.com/openclaw/project-management/releases).

> **Note**: When installing as an OpenClaw Skill, clone to `~/.openclaw/skills/`.

### Method 3: Download ZIP

Download and extract from [GitHub Releases](https://github.com/openclaw/project-management/releases).

### First Use

1. Fill in `resource-profiles.md` to record your execution resources
2. If managing projects, read `docs/coordinator.md`
3. If executing tasks, read `docs/executor.md`
4. Start using templates in `templates/`

## Core Process

### Project Lifecycle

```
Initiate project → Requirement confirmation → Break down → Dispatch → Execute → Review → Acceptance → Archive
```

### Task Status

```
Pending dispatch → In progress → Pending review → Accepted
                                  ↓
                               Rework → Pending review
```

## Directory Structure

```
project-management/
├── SKILL.md              # OpenClaw Skill definition
├── README.md             # English documentation
├── README_CN.md          # This file
├── CHANGELOG.md          # Version history
├── LICENSE               # MIT license
├── resource-profiles.md  # Executor resource profiles (needs to be filled)
├── docs/                 # Detailed documentation
│   ├── coordinator.md    # Dispatcher operation manual
│   ├── executor.md       # Executor operation manual
│   ├── philosophy.md     # Design philosophy
│   └── ...               # More documentation
├── templates/            # Template library
│   ├── project-brief.md  # Project initiation
│   ├── task-spec.md      # Task specification
│   ├── review-record.md  # Review record
│   └── ...               # More templates
└── tools/                # Optional tools
```

## Key Documentation

| Document | Purpose |
|----------|---------|
| `coordinator.md` | How to manage projects |
| `executor.md` | How to execute tasks |
| `task-management.md` | Task state machine |
| `quality.md` | Quality assurance |
| `templates/` | Copy and use |

## Template List

| Template | Purpose |
|----------|---------|
| `project-brief.md` | Start a new project |
| `task-spec.md` | Define tasks |
| `review-record.md` | Review completed work |
| `final-report.md` | Project delivery |
| `risk-register.md` | Track risks |

## License

MIT License — Free to use, modify, and distribute.
