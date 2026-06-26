---
name: project-management-system
description: A comprehensive project management system for AI agents. Manage projects from initiation to delivery with structured workflows, templates, quality gates, and role-based operation manuals. Supports both dispatcher and executor roles.
---

# Project Management System

A comprehensive project management system for AI agents. Manage projects from initiation to delivery with structured workflows, templates, and quality gates.

## Description

A universal project management system. Covers full process management from project initiation to acceptance, including:
- Role operation manuals (Dispatcher/Executor)
- 14 rule documents
- 10 template files
- Quality assurance mechanisms
- Task state machine
- Self-loop guarantee

## When to Use

- User requests project initiation or planning
- User mentions "project management", "task dispatch", "review and acceptance"
- Multi-agent collaboration needed for complex tasks
- Need to track project progress and quality

## Installation

```bash
clawhub install project-management-system
```

Or with OpenClaw CLI:
```bash
openclaw skills install project-management-system
```

## Quick Start

### 1. Configure Resources

Fill in esource-profiles.md with your execution resources (agents, tools, etc.)

### 2. Read Documentation

| Role | Start With |
|------|------------|
| Project Lead | docs/coordinator.md |
| Task Executor | docs/executor.md |
| Both Roles | docs/philosophy.md |

### 3. Start a Project

1. Create project brief: 	emplates/project-brief.md
2. Break down tasks: 	emplates/task-spec.md
3. Dispatch to executors
4. Review and accept: 	emplates/review-record.md

## Core Concepts

### Roles

| Role | Responsibility |
|------|----------------|
| Decision Maker | Approves projects and changes |
| Dispatcher | Plans, dispatches, reviews, accepts |
| Executor | Executes tasks, delivers outputs |

### Project Lifecycle

```
Initiate -> Break Down -> Dispatch -> Execute -> Review -> Accept
     |                                              |
     +------------------ Rework -------------------+
```

### Task States

| State | Meaning |
|-------|---------|
| Pending | Not yet dispatched |
| In Progress | Being executed |
| Completed | Awaiting review |
| Accepted | Passed review |
| Rework | Needs fixes |

## Documentation

| Document | Purpose |
|----------|---------|
| coordinator.md | Dispatcher operations |
| executor.md | Executor operations |
| philosophy.md | Design principles |
| quality.md | Quality gates |
| 	ask-management.md | Task states and transitions |
| communication.md | Communication protocols |

## Templates

| Template | Use When |
|----------|----------|
| project-brief.md | Starting a new project |
| 	ask-spec.md | Defining a task |
| eview-record.md | Reviewing deliverables |
| change-request.md | Requesting scope change |
| milestone-report.md | Reporting milestone completion |

## Dependencies

- OpenClaw >= 2026.3.0 (optional, for skill integration)
- Python 3.8+ (optional, for dashboard tools)

## License

MIT License