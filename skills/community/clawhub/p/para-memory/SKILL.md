---
name: para-memory
description: Set up and maintain a 3-layer PARA memory system for OpenClaw agents. Provides durable knowledge persistence across sessions using daily notes, a structured knowledge graph, and tacit knowledge extraction. Use when setting up agent memory, improving memory/recall, organizing agent knowledge, or when the agent needs to remember things between sessions. Also handles nightly consolidation workflows.
---

# PARA Memory System for OpenClaw

A battle-tested 3-layer memory system that gives your agent real continuity across sessions. Built by KaiShips (kaiships.com).

## Why This Exists

OpenClaw agents wake up fresh every session. Without a memory system, they forget everything — decisions, preferences, project context, lessons learned. This skill fixes that.

## The 3 Layers

### Layer 1: Knowledge Graph (`life/` — PARA structure)
Durable, structured knowledge organized by purpose:
- `life/projects/` — Active projects with clear goals (one folder per project, each with `status.md`)
- `life/areas/` — Ongoing responsibilities (business ops, infrastructure, marketing)
- `life/resources/` — Reference material, research, templates
- `life/archives/` — Completed/abandoned projects (moved here, never deleted)

### Layer 2: Daily Notes (`memory/YYYY-MM-DD.md`)
Raw session logs. Written during conversations:
- What was discussed and decided
- What was accomplished
- Open questions and next steps
- New information learned about the user

### Layer 3: Tacit Knowledge (`life/tacit.md`)
The "personality" layer — what makes the agent actually useful:
- User communication preferences and work habits
- Business context and constraints
- Lessons learned from mistakes
- Platform-specific gotchas and workarounds

## Setup Instructions

### First-time setup

1. Read `{baseDir}/assets/AGENTS-template.md` — copy its contents to your workspace `AGENTS.md`
2. Create the directory structure:
   ```
   mkdir -p life/projects life/areas life/resources life/archives memory
   ```
3. Read `{baseDir}/assets/tacit-template.md` — copy to `life/tacit.md` and fill in what you know
4. Create today's daily note: `memory/YYYY-MM-DD.md` using the template in `{baseDir}/assets/daily-template.md`

### Session startup routine

Every session, before doing anything else:
1. Read `life/tacit.md` (Layer 3 — who you're helping)
2. Read `memory/YYYY-MM-DD.md` for today and yesterday (Layer 2 — recent context)
3. If in a direct/main session: also read `MEMORY.md` if it exists

### During conversations

When you learn something new, write it down immediately:
- New fact about the user → update `life/tacit.md`
- Project update → update relevant `life/projects/<name>/status.md`
- Decision made → log in today's `memory/YYYY-MM-DD.md`

**Critical rule: never make "mental notes." If it's worth remembering, write it to a file.**

### Nightly consolidation

Run during heartbeats or end-of-session:
1. Review today's `memory/YYYY-MM-DD.md`
2. Extract durable facts → update relevant `life/` files (Layer 1)
3. Extract lessons/preferences → update `life/tacit.md` (Layer 3)
4. Keep daily notes as raw archive (never delete them)

## Key Principles

- **Check before creating.** Always look for existing projects/areas before making new ones.
- **Text > Brain.** If you want to remember it, write it to a file. Period.
- **Kill fast.** When a project stalls or fails, move it to `life/archives/`. Don't delete.
- **Areas have standards, not deadlines.** Projects finish; areas are ongoing.
- **One source of truth.** Don't duplicate info across files. Pick one home for each fact.

## Recommended Cron Setup

For automatic nightly consolidation, add a cron job:
```
Schedule: 0 3 * * * (3 AM daily)
Task: Review today's daily notes, consolidate durable knowledge into life/ files, update tacit.md with new lessons.
```

## Credits

Built by Kai @ KaiShips — kaiships.com
