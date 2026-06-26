---
name: model-handoff
description: Maintain a HANDOFF.md file in the workspace so context survives seamlessly when switching between LLM models (e.g. Claude → GPT → Gemini). Use when the user says they are switching models, asks how to preserve context across model switches, wants to save tokens by rotating models, or asks how a new model can pick up where the last one left off. Also use proactively during long sessions to keep HANDOFF.md current.
---

# Model Handoff Skill

Enables seamless context continuity when switching between LLM models mid-session. Maintains a `HANDOFF.md` file that any model can read to instantly understand the current project state, active tasks, and behavioral expectations.

## Core Concept

Every model starts a session cold. `HANDOFF.md` is a dense, always-current fast-boot file that eliminates the ramp-up. It is the single source of truth for model-to-model context transfer.

## HANDOFF.md Structure

Write `HANDOFF.md` to the workspace root with these sections:

```markdown
# HANDOFF.md — Model Switch Context

## Who you are
[Agent name, persona, tone, key behavioral rules. Reference SOUL.md if present.]

## Who you're helping
[User name, role, location, preferences. Reference USER.md and MEMORY.md if present.]

## Active projects
[For each project: name, status, key files, next steps. Be specific — include file paths.]

## Agent roster
[If multi-agent: list agent IDs, models, roles.]

## Key credentials & tools
[Point to credential files — never inline secrets. e.g. "Azure SP creds: azure-config.json"]

## Behavioral rules
[Critical rules a new model must follow. Keep to essentials only.]

## How to keep this file current
[Brief note on when to update.]

## Last updated
[Timestamp + 1-line session summary]
```

## When to Create/Update

**Create** `HANDOFF.md` when:
- User asks about switching models
- User asks how to preserve context
- `HANDOFF.md` does not yet exist

**Update** `HANDOFF.md` when:
- User says "switching to [model]" — update immediately before they go
- User says "update HANDOFF" or "log everything"
- A significant project milestone is reached (new project started, major decision made, new agent added)
- The session has been running for several hours with significant new context

**Keep current proactively** — do not wait to be asked. Update during long sessions when meaningful things happen.

## Wiring HANDOFF.md into the Workspace

After creating `HANDOFF.md`, add a reference in `AGENTS.md` so every model is instructed to read it on a model switch:

```markdown
## Every Session
...
- **If you are a new model taking over** (model switch): Read `HANDOFF.md` first — it's your fast-boot summary of everything active
```

## What to Say When Switching

Tell the user to open with this when switching to a new model:

> **"Read HANDOFF.md. You are [agent name]."**

That single line forces the new model to self-load before responding.

## Writing Guidelines

- **Dense, not verbose** — every line earns its place
- **File paths, not descriptions** — "see `azure-config.json`" not "credentials are stored somewhere"
- **Never inline secrets** — point to credential files only
- **No personal/private data** — HANDOFF.md may be shared; keep sensitive context in MEMORY.md
- **Remove stale content** — delete completed projects and outdated context on each update
- **Last updated timestamp** — always include so the receiving model knows how fresh it is

## References

- See `references/template.md` for a copy-paste HANDOFF.md starter template
