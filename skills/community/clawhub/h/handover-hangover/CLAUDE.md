# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Handover Hangover** — OpenClaw skill for seamless mid-session model handoff across a 6-model fallback chain. When the gateway silently switches to a fallback model, the new model inherits conversation history but not context. This skill fixes that via a three-channel defense.

## Architecture

Three-channel design, each compensating for the others' failure modes:

1. **Channel 1: System prompt** (`SKILL.md`, `always: true`) — instructions that survive model switch because the gateway resends system prompt on every API call
2. **Channel 2: Filesystem** (`memory/handoff-note.md`, `memory/current-task.md`) — persistent handoff data on disk
3. **Channel 3: Bash watchdog** (`scripts/handoff.sh`) — deterministic fallback if the model didn't follow prompt instructions

Pattern borrowed from `context-anchor` (SKILL.md + scripts/anchor.sh).

## Deliverables

| File | Role | Status |
|------|------|--------|
| `SKILL.md` | System prompt — write-side, detection, read-side, epistemic reset | Done |
| `scripts/handoff.sh` | Watchdog — closed-loop check, INIT/DIRTY SWITCH, fallback generation | Done |
| `README.md` | Public-facing documentation | Done |

## Language

**All artifacts are in English:** `SKILL.md`, `scripts/handoff.sh` (code + comments), `README.md`, `DESIGN.md`, `ARCHITECTURE.md`, and any user-facing messages.

## File conventions

- **Internal docs** (`DESIGN.md`, `ARCHITECTURE.md`): English (translated from Russian). In `.gitignore` and `.clawhubignore` — not published.
- **Public docs** (`README.md`, `SKILL.md`): English.
- **SKILL.md format**: OpenClaw skill — YAML frontmatter + markdown body. See existing skills at `~/.openclaw/workspace/skills/*/SKILL.md` for reference.
- **`scripts/handoff.sh`**: Bash. Must be POSIX-compatible where possible. Only writes to `memory/` directory. Comments in English.

## OpenClaw skill structure

```yaml
# SKILL.md frontmatter
name: handover-hangover
description: Seamless model handoff for OpenClaw agents
always: true          # bypass relevance gate — always in system prompt
category: system
```

The skill body is markdown injected into the model's system prompt. `always: true` means it's present every turn regardless of relevance scoring.

## Key concepts

- **INIT vs DIRTY SWITCH**: `no handoff-note + no .prev.md` = first run. `no handoff-note + .prev.md exists` = model failed to write.
- **Separation of concerns**: Model writes semantic state (cognitive mode, confidence, hypotheses). Script writes mechanical state (timestamps, file changes, git status).
- **Epistemic reset**: On detected switch, incoming model must not treat prior assistant messages as its own.
- **Security scope**: Skill only writes to `memory/` directory. Never reads `openclaw.json`.

## No build system

This is a markdown + bash project. No compilation, no package manager, no tests framework (yet). Validation is manual dry-run testing with OpenClaw agents.

## Testing approach

Dry-run: trigger a model switch mid-session and verify the incoming model correctly reads handoff state, performs epistemic reset, and continues without scope collapse.
