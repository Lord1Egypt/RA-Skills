---
name: plan-manager
description: |
  Unified plan management system for coordinating OpenClaw Agent and Human plans.

  Use when managing both AI agent execution workflows and human task plans in a unified structure.
version: 1.0.0
author: 文轩先师
---

# Plan Manager

Unified plan management system for coordinating **OpenClaw Agent** execution plans and **Human** task plans.

## Overview

This skill provides a dual-track planning system:

| Track | Purpose | Location |
|-------|---------|----------|
| **Agent Plans** | Track OpenClaw Agent's execution workflows, tool sequences, and task progress | `plans/agent/` |
| **Human Plans** | Track human tasks, todos, and project milestones | `plans/human/` |

## Directory Structure

```text
plans/
├── README.md                 # This file - overview and coordination guide
├── agent/
│   ├── plans-overview.md     # Agent's high-level execution board
│   ├── detailed/
│   │   ├── index.md          # Index of all detailed agent plans
│   │   └── XX-{plan-name}.md # Individual agent execution plans
│   └── archive/              # Completed agent plans
└── human/
    ├── plans-overview.md     # Human's high-level task board
    ├── detailed/
    │   ├── index.md          # Index of all detailed human plans
    │   └── XX-{plan-name}.md # Individual human task plans
    └── archive/              # Completed human plans
```

## When to Use Which Track

### Use Agent Track When:
- The OpenClaw Agent needs to execute multi-step tasks
- Tool sequences and execution workflows need documentation
- Tracking token usage and execution progress
- Breaking down complex user requests into actionable steps

### Use Human Track When:
- The human user has personal tasks or todos
- Project milestones and deadlines need tracking
- Long-term goals and plans need organization
- Human decision points or approvals are required

## Coordination Patterns

### Pattern 1: Agent Assists Human Plan
Human creates a plan → Agent creates corresponding execution plan → Agent executes → Both update status

**Example:**
```
Human: "Plan a trip to Japan"
  ↓
human/plans-overview.md: "Plan Japan trip" (Status: In Progress)
  ↓
agent/plans-overview.md: "Research flights, hotels, itinerary" (Status: In Progress)
  ↓
[Agent executes research tasks]
  ↓
Both tracks updated to Done
```

### Pattern 2: Agent Autonomous Execution
User requests complex task → Agent creates execution plan → Agent executes independently

**Example:**
```
User: "Refactor the auth module"
  ↓
agent/plans-overview.md: "Auth module refactor" (Status: In Progress)
  ↓
[Agent executes refactoring with detailed plan]
  ↓
Agent updates status to Done
```

### Pattern 3: Human Oversight
Agent creates plan → Requests human approval → Human approves/modifies → Agent executes

**Example:**
```
User: "Design a new feature"
  ↓
agent/plans-overview.md: "Design new feature" (Status: Pending Approval)
  ↓
[Agent presents plan to human]
  ↓
human/plans-overview.md: "Review and approve feature design" (Status: In Progress)
  ↓
[Human reviews, approves]
  ↓
Agent proceeds to execution
```

## Quick Start

### For Agent Tasks:

1. Create `plans/agent/plans-overview.md`
2. Add execution items to the status table
3. Create `plans/agent/detailed/XX-{plan-name}.md` for complex tasks
4. Update `plans/agent/detailed/index.md`
5. Mark steps complete as execution progresses

### For Human Tasks:

1. Create `plans/human/plans-overview.md`
2. Add task items to the status table
3. Create `plans/human/detailed/XX-{plan-name}.md` for complex tasks
4. Update `plans/human/detailed/index.md`
5. Update statuses weekly or as tasks complete

## Templates

Templates are organized by track:

```text
templates/
├── agent/           # Templates for Agent plans
│   ├── plans-overview.md
│   ├── detailed-plan.md
│   └── index.md
└── human/           # Templates for Human plans
    ├── plans-overview.md
    ├── detailed-plan.md
    └── index.md
```

## Status Values

| Status | Meaning |
|--------|---------|
| `Pending` | Plan created, not yet started |
| `In Progress` | Actively being worked on |
| `Blocked` | Waiting on dependency or approval |
| `Done` | Completed successfully |
| `Cancelled` | No longer needed |

## Tips

- **Prefix plan IDs**: Use `A-1`, `A-2` for agent plans and `H-1`, `H-2` for human plans when cross-referencing
- **Link related plans**: In the Notes column, reference related plans from the other track
- **Archive completed plans**: Move completed plans to the `archive/` folder monthly
- **Review weekly**: Check both tracks weekly to ensure coordination
- **Use consistent naming**: kebab-case for all filenames (`01-auth-refactor.md`)

## Example: Coordinated Web Development Project

**Human Track** (`plans/human/plans-overview.md`):
```markdown
| H-1 ||***|| Launch new website ||***|| In Progress ||***|| High ||***|| Q2 2025 ||***|| June 30 ||***|| A-1, A-2 |
```

**Agent Track** (`plans/agent/plans-overview.md`):
```markdown
| A-1 ||***|| Design database schema ||***|| Done ||***|| High ||***|| Week 1 ||***|| - ||***|| For H-1 |
| A-2 ||***|| Implement API endpoints ||***|| In Progress ||***|| High ||***|| Week 2-3 ||***|| - ||***|| For H-1 |
```

This structure ensures both human goals and agent execution are visible and coordinated.
