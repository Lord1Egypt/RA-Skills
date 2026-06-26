# Architecture — Mjolnir Brain

## Design Philosophy

**Simple, reliable, zero-dependency.** No vector databases, no external services, no complex infrastructure. Just markdown, JSON, and bash.

This system trades sophistication for reliability. A RAG-based memory might be fancier, but this one works on any machine with a shell.

## Three-Layer Memory Architecture

```
Layer 1: Session Context (ephemeral)
  └─ Current conversation + tool calls
  └─ Lost when session ends

Layer 2: Working Memory (daily files)
  └─ memory/YYYY-MM-DD.md — raw daily logs
  └─ Write-through: captured in real-time during sessions
  └─ Lifecycle: active → consolidated → archived (30d) → deleted

Layer 3: Long-Term Memory (curated)
  └─ MEMORY.md — distilled knowledge (≤20KB)
  └─ AGENTS.md — behavioral rules
  └─ SOUL.md — personality
  └─ TOOLS.md — environment config
  └─ strategies.json — problem-solving patterns
  └─ playbooks/ — parameterized procedures
```

## Self-Learning Loop

```
   ┌──── Experience (session interaction) ────┐
   │                                           │
   ▼                                           │
Encounter Problem ──→ Check strategies.json    │
   │                      │                    │
   │  known?     ┌───yes──┘                    │
   │             ▼                             │
   │     Try solutions by success rate         │
   │             │                             │
   │     ┌──────┼──────┐                       │
   │     ▼      ▼      ▼                      │
   │  success  fail   fail                     │
   │     │      │      │                       │
   │     ▼      ▼      ▼                      │
   │  Update  Try    Try next                  │
   │  rate↑   next   solution                  │
   │     │                                     │
   │  not known? ──→ Explore & solve           │
   │                      │                    │
   │                      ▼                    │
   │              Create new strategy entry     │
   │                      │                    │
   └──────────────────────┘                    │
                                               │
   Write-Through ──→ daily log + relevant file │
   AI Consolidation ──→ MEMORY.md ─────────────┘
```

## Key Mechanisms

### 1. Write-Through Protocol
Every learning is written to a file the moment it's discovered. No batching, no "I'll remember this." Session death = data loss for anything not written.

### 2. Strategy Registry (strategies.json)
Problem→solution mappings with success rate tracking. Each attempt updates the rate via weighted average. Solutions auto-sort by effectiveness over time.

### 3. AI Consolidation
Daily at 04:00:
- bash script handles cleanup (garbage files, archiving, capacity checks)
- AI cron job reads pending logs and writes **real summaries** to MEMORY.md sections

This two-phase approach prevents the "fake consolidation" problem (blindly copying raw logs).

### 4. Playbook System
Frequently repeated operations (≥3 times) get parameterized playbooks. Not true "muscle memory," but equivalent — from thinking 30 seconds to looking up 3 seconds.

### 5. Heartbeat Self-Check
Every heartbeat poll includes a self-audit:
- Any failures not recorded?
- Any corrections not documented?
- Any better approaches not written?

## Capacity Management

| Resource | Limit | Enforcement |
|----------|-------|-------------|
| MEMORY.md | ≤20KB | AI trims during consolidation |
| Daily logs | 30 days | Auto-archive to gzip |
| Garbage files | <200B | Auto-delete |
| Backup copies | 7 | Auto-rotate oldest |

## What This System Cannot Do

Be honest about limitations:

1. **No semantic search** — grep/fuzzy match only. Works for <100 files, won't scale to thousands.
2. **No real-time adaptation** — learning requires file writes + next session read. No in-flight model updates.
3. **No cross-user transfer** — knowledge is environment-specific. Tagging `[general]` vs `[env-specific]` helps, but doesn't auto-transfer.
4. **Depends on AI discipline** — Write-through only works if the agent actually writes. The rules help, but can't force compliance.

These are architectural choices, not bugs. For a personal assistant, this coverage is sufficient.
