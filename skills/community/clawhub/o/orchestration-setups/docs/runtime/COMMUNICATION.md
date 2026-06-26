# Communication Model

The orchestration system uses 3 communication layers.

## 1. Stable shared context
Repository or worktree root context shared by all agents.

Canonical files:
- `README.md` — project overview, purpose, layout, usage
- `CLAUDE.md` — agent instructions, architecture notes, conventions, current status

This is the long-lived context every agent should read before doing meaningful work.

## 2. Directed handoff
Agent A -> Agent B transition packet.

Purpose:
- explain what was done
- point to canonical artifacts
- state how to verify
- classify retry mode if needed
- define the exact next action

Location:
- `agent/orchestration/runs/<run-id>/handoffs/`

## 3. Shared temporary context
Rich but temporary shared state for the active run.

Purpose:
- preserve reasoning breadcrumbs between agents
- recover after agent death / kill / timeout
- store partial findings, failed attempts, open questions, intermediate notes

Location:
- `agent/orchestration/runs/<run-id>/working-memory/`

Examples:
- failed approach notes
- partial decompositions
- module-specific TODOs
- unresolved reviewer concerns
- integration gotchas

## Git / worktree rule for project-builder
For `project-builder`, the execution context should be a git-backed project/worktree.

Requirements:
- one repository root or worktree per active project run
- `README.md` and `CLAUDE.md` at the worktree root
- isolated branches/worktrees for parallel builders when possible
- GitHub remote configured for durable sync when the project is meant to live on GitHub

This makes runs reproducible and lets another agent resume from real project state, not only chat memory.
