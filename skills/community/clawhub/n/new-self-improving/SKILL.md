---
name: new-self-improving
description: >-
  Log corrections, errors, feature requests, and recurring patterns into
  structured workspace learning files, then promote stable patterns into
  tiered memory and OpenClaw workspace files (AGENTS.md, SOUL.md, TOOLS.md,
  MEMORY.md). Use when: (1) user corrects you or points out mistakes,
  (2) a command or tool fails, (3) user requests a missing capability,
  (4) you notice a recurring pattern worth remembering, (5) reviewing
  learnings during heartbeat or maintenance, (6) promoting lessons to
  permanent workspace memory. Designed for OpenClaw personal-assistant
  and coding workflows with heartbeat integration.
metadata:
  openclaw:
    emoji: "\U0001F9E0"
    homepage: https://github.com/muhamadbasim/oktoclaw
---

# Self-Improving OpenClaw

Structured learning loop for OpenClaw agents: capture → review → promote → maintain.

## Quick Start

On first activation, run the init script to create workspace directories:

```bash
bash scripts/init-workspace.sh
```

This creates `.learnings/` and `.self-improving/` in the workspace root.

## Core Workflow

### 1. Capture

When a learning signal fires, log it to the right file in `.learnings/`:

| Signal | Target file | Category |
|--------|-------------|----------|
| User corrects you | `LEARNINGS.md` | `correction` |
| User says "always/never do X" | `LEARNINGS.md` | `preference` |
| You discover something non-obvious | `LEARNINGS.md` | `insight` |
| Your knowledge was outdated | `LEARNINGS.md` | `knowledge_gap` |
| Found a better approach | `LEARNINGS.md` | `best_practice` |
| Command returns non-zero | `ERRORS.md` | — |
| Tool/API fails unexpectedly | `ERRORS.md` | — |
| User wants missing capability | `FEATURE_REQUESTS.md` | — |

Use the entry format defined in [references/logging-format.md](references/logging-format.md).

### 2. Review

During heartbeat or manual review, scan `.learnings/` and evaluate each pending item:

1. Check recurrence — search for similar entries.
2. If related entry exists: bump `Recurrence-Count`, link with `See Also`.
3. If `Recurrence-Count >= 3` within 30 days: add to `.learnings/REVIEW_QUEUE.md`.
4. Update `.self-improving/heartbeat-state.md` with review timestamp.

See [references/heartbeat-review.md](references/heartbeat-review.md) for the full review procedure.

### 3. Promote

Move validated patterns up the memory tiers:

| Condition | Promote to | Example |
|-----------|-----------|---------|
| Pattern used 2x, context-specific | `.self-improving/domains/*.md` or `projects/*.md` | "This repo uses pnpm" |
| Pattern used 3x in 7-30 days, cross-task | `.self-improving/HOT.md` | "User prefers concise answers" |
| Stable, long-term applicable | `SOUL.md` / `AGENTS.md` / `TOOLS.md` / `MEMORY.md` | "Never force push" |

See [references/promotion-rules.md](references/promotion-rules.md) for the full promotion/demotion rules.

### 4. Maintain

Periodically (every 1-2 weeks during heartbeat):

- **Demote** HOT entries unused for 30 days → domain/project memory.
- **Archive** domain/project entries unused for 90 days → `.self-improving/archive/`.
- **Compact** files exceeding size limits: merge similar entries, summarize verbose ones.
- **Never delete** without explicit user confirmation. Prefer archive over delete.

## Detection Triggers

Log automatically when you notice these signals:

**Corrections** (→ LEARNINGS.md, category: correction):
- "No, that's not right..."
- "Actually, it should be..."
- "You're wrong about..."
- "I told you before..."
- "Stop doing X"

**Preferences** (→ LEARNINGS.md, category: preference):
- "I like when you..."
- "Always do X for me"
- "Never do Y"
- "My style is..."

**Feature requests** (→ FEATURE_REQUESTS.md):
- "Can you also..."
- "I wish you could..."
- "Is there a way to..."

**Errors** (→ ERRORS.md):
- Non-zero exit codes
- Exceptions or stack traces
- Timeout or connection failure

**Ignore** (don't log):
- One-time instructions ("do X now")
- Pure context ("in this file...")
- Hypotheticals ("what if...")

## Memory Tiers

| Tier | Location | Size limit | Behavior |
|------|----------|-----------|----------|
| RAW | `.learnings/` | Unlimited | Intake only, not auto-loaded |
| HOT | `.self-improving/HOT.md` | ≤80 lines | Always loaded at session start |
| WARM | `.self-improving/domains/`, `projects/` | ≤200 lines each | Load on context match |
| COLD | `.self-improving/archive/` | Unlimited | Load on explicit query |

### Conflict Resolution

When patterns contradict:
1. Most specific wins: project > domain > HOT/global.
2. Same level: most recent wins.
3. If ambiguous: ask user.

## Promotion Targets

When a learning is stable enough for permanent workspace memory:

| Learning type | Promote to | Example |
|--------------|-----------|---------|
| Behavioral patterns | `SOUL.md` | "Be concise, avoid disclaimers" |
| Workflow improvements | `AGENTS.md` | "Spawn sub-agents for long tasks" |
| Tool gotchas | `TOOLS.md` | "Git push needs auth first" |
| User preferences/decisions | `MEMORY.md` | "Basim prefers Indonesian for casual chat" |

Mark promoted entries as `Status: promoted` with `Promoted-To: <file>`.

## Transparency

- When applying a learned pattern, cite the source: `(from HOT.md)` or `(from domains/coding.md:15)`.
- On "memory stats" request, report entry counts per tier.
- On "what have you learned?" request, show recent corrections and HOT entries.

## Security Boundaries

- Never store credentials, API keys, tokens, or passwords.
- Never store health data or sensitive personal information.
- Never store third-party private data.
- Redact secrets in error logs — use `[REDACTED]` placeholders.
- Only write to memory files in private/local workspace sessions.

## Workspace Layout

See [references/workspace-layout.md](references/workspace-layout.md) for the complete directory structure and file descriptions.

## Resources

### scripts/
- `init-workspace.sh` — Create `.learnings/` and `.self-improving/` directories with template files.

### references/
- `logging-format.md` — Entry format for learnings, errors, and feature requests.
- `promotion-rules.md` — Full promotion, demotion, and archival rules.
- `heartbeat-review.md` — Heartbeat review procedure and state tracking.
- `workspace-layout.md` — Complete directory structure reference.

### assets/
- Template files copied by `init-workspace.sh` into the workspace.
