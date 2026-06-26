---
name: agent-harness
description: Long-running agent workflow automation. Initialize project scaffolding, manage feature lists, track progress across sessions, and orchestrate coding agents.
version: 1.0.0
author: wwk
commands:
  - harness-init
  - harness-run
  - harness-status
  - harness-feature
  - harness-commit
---

# Agent Harness Skill

Automates the long-running agent workflow from Anthropic's engineering blog. Manages feature lists, progress tracking, and session orchestration across multiple Claude Code sessions.

## Commands

### /harness-init <project-description>
Initialize a new project with:
- `feature_list.json` — comprehensive feature tracking
- `claude-progress.txt` — cross-session progress log
- `init.sh` — development server startup script
- `.harness.json` — harness configuration

### /harness-run
Start a coding session. Reads progress, picks the next feature, and follows the incremental development workflow.

### /harness-status
Show current project progress: features completed, next features to implement, recent session history.

### /harness-feature <description>
Add a new feature to the feature list.

### /harness-commit
Commit current work with structured message and update progress file.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Initializer │────▶│  Coding Agent│────▶│   Next Coding│
│    Agent     │     │  Session #1  │     │    Agent #2  │
└─────────────┘     └──────────────┘     └──────────────┘
      │                    │                     │
      ▼                    ▼                     ▼
┌─────────────────────────────────────────────────────────┐
│                    Shared State                          │
│  ┌───────────────┐ ┌──────────────┐ ┌────────────────┐ │
│  │feature_list   │ │claude-progress│ │   Git History  │ │
│  │    .json      │ │    .txt       │ │   (commits)    │ │
│  └───────────────┘ └──────────────┘ └────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Workflow

1. **Init**: `harness init "Build a chat app"` — sets up project skeleton
2. **Code**: `harness run` — each session picks ONE feature
3. **Track**: Features marked passing only after end-to-end testing
4. **Commit**: Progress documented in git + progress file
5. **Repeat**: Continue until all features pass

## Key Principles

- **Incremental**: One feature per session
- **Tested**: End-to-end testing before marking complete
- **Clean state**: Always leave codebase merge-ready
- **Persistent state**: Git + progress file bridge context windows
