---
name: lightweight-team-orchestration
description: Lightweight multi-agent team orchestration. Output structure simplified to two folders: agents/ and projects/.
---

# Lightweight Team Orchestration

A lightweight multi-agent team collaboration skill with a simplified output structure focused on core deliverables.

## Use Cases

- Creating simple teams with 2+ agents
- Agent role definition and task distribution
- Agent output artifact management (with versioning)
- Lightweight collaboration workflows (no complex workflow engine required)

## Quick Start

### Output Structure

```
[TEAM_NAME]/
├── agents/                   # Agent role definitions
│   ├── orchestrator/         # Orchestrator
│   │   └── SOUL.md           # Role definition
│   ├── builder/              # Executor
│   │   └── SOUL.md
│   └── reviewer/             # Reviewer (optional)
│       └── SOUL.md
└── projects/                 # Output artifacts (with versioning)
    ├── v1.0.0/               # Version directory
    │   ├── builder.md        # Builder output
    │   └── reviewer.md       # Reviewer output
    └── v1.1.0/               # Next version
```

### Workflow

1. **Create Agent Roles** → Create SOUL.md for each agent under `agents/`
2. **Distribute Tasks** → Launch agents using sessions_spawn
3. **Collect Artifacts** → Store artifacts in `projects/v{version}/`
4. **Version Management** → Create a new version directory for each delivery

## Agent Role Definitions

### agents/orchestrator/SOUL.md

```markdown
# Orchestrator

## Responsibilities
- Task distribution and progress tracking
- Coordination between agents
- Artifact version management

## Behaviors
- Use high-reasoning model
- Keep task status updated
```

### agents/builder/SOUL.md

```markdown
# Executor

## Responsibilities
- Execute specific tasks
- Produce deliverables

## Behaviors
- Deliver according to specifications
- Annotate version number
```

### agents/reviewer/SOUL.md (optional)

```markdown
# Reviewer

## Responsibilities
- Verify output quality
- Propose improvement suggestions
```

## Task Distribution

Launch agents using sessions_spawn:

```
Task: [Task description]
Output: projects/v{version}/{agent}.md
Verify: [Verification method]
```

## Version Management

- Initial version: v1.0.0
- Each iteration: Increment version number
- Preserve history: All versions retained in projects/

## When to Use

- Simple 2-3 person teams
- No complex workflow engine required
- Focus on artifact delivery over process

## When Not to Use

- Complex multi-stage workflows
- Real-time status tracking → Use task boards
- Large-scale agent coordination