# Personal OS Framework

## What is it?

A personal operating system built on the idea that humans should have a "second brain" that AI can understand and maintain.

## Core Principle

**Not a tool. A collaboration.**

The human does things. The AI records, organizes, and helps. The AI reads the system to understand the human. The human and AI grow together.

## Workflow

```
Capture → Structure → Execute → Reflect
```

## Core Modules

### 1. Decision Log
Record important decisions with rationale, consequences, and follow-up actions.

### 2. Review Operator
Generate periodic reviews (daily, weekly, monthly) from project state and recent activity.

### 3. Routing Assistant
Classify incoming information: where should it go? What type is it?

### 4. Task Layer
Define what a "task" looks like. Track status and ownership.

### 5. Execution Layer
Record when work starts. Feed execution state into reviews.

### 6. Decision Support Layer
Monitor decision follow-ups, task health, and system state.

### 7. Memory Distiller
Convert accumulated raw captures into structured, reusable knowledge.

## Architecture

```
Human Action → AI records → System updated → AI reads → AI helps
                        ↑                              ↓
                     Memory                    Understanding
```

## Key Idea

The AI does not wait for commands. The AI reads the system, understands the human, and acts proactively.

## Files

- `STATE.md` — current project states
- `TODO.md` — active tasks
- `DECISIONS.md` — decision log
- `PENDING-DECISIONS.md` — blocked decisions
- `HEARTBEAT-LOG.md` — system activity log

## For AI Collaborators

Read `personal-os` after each conversation. Update relevant files. The system stays current because the AI keeps it current.

## Templates

See `templates/` directory for review, decision, and task templates.
