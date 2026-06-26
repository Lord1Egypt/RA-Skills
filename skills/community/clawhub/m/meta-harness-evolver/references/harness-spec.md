# Harness Spec — What Constitutes Hoss's Harness

This document defines exactly what files make up Hoss's "harness" — the code wrapping the LLM brain that determines what context to store, retrieve, and present.

## Core Harness Files

### SOUL.md — Core Identity
**Path:** `~/.openclaw/workspace/SOUL.md`
**What it controls:** Core identity, philosophical stance, decision-making framework, personality, values, boundaries, co-founder responsibilities.
**Can evolve:** Yes — this is the primary target for identity modifications
**Do NOT change:** Nothing off-limits, but major philosophical shifts should be discussed with Tyler

**Key sections:**
- Core Identity (who Hoss is)
- Philosophical Core (think well, act decisively; genuine usefulness; earned trust)
- Operational Instincts (before/while/after acting)
- Quality Standards (code, commits, deployments, docs)
- Personality (decisive, direct, witty, warm, honest)
- Boundaries (private things, external actions, group chats)
- Co-Founder Responsibilities

### IDENTITY.md — Role & Voice
**Path:** `~/.openclaw/workspace/IDENTITY.md`
**What it controls:** Name, role, vibe, emoji, signature phrase, voice characteristics, continuity rules
**Can evolve:** Yes — role definition and voice
**Do NOT change:** Nothing off-limits

### AGENTS.md — Sub-Agent Architecture
**Path:** `~/.openclaw/workspace/AGENTS.md`
**What it controls:** Sub-agent roster, coordination protocol, session management, Red Lines
**Can evolve:** Yes — agent roster changes, coordination protocol
**Do NOT change:** Git safety rules, Red Lines

### TOOLS.md — Tool Configurations
**Path:** `~/.openclaw/workspace/TOOLS.md`
**What it controls:** All tool configs, credentials (API keys, tokens), host IPs, SSH details, skill locations, brand assets
**Can evolve:** Yes — new tool configurations, new hosts
**Do NOT change:** Actual credential values, API tokens, passwords. Adding new credential placeholders is OK with Tyler's approval.

### MEMORY.md — Long-Term Memory
**Path:** `~/.openclaw/workspace/MEMORY.md`
**What it controls:** Curated long-term memory — decisions, infrastructure, people, lessons
**Can evolve:** Rarely — memory structure, but MEMORY.md content itself is the output of evolution, not the input
**Do NOT change:** Memory content directly — let the evolution process update it through normal operation

### HEARTBEAT.md — Active Hours & Checks
**Path:** `~/.openclaw/workspace/HEARTBEAT.md`
**What it controls:** Active hours (8 AM - 10 PM CDT), skip conditions, batched checks (git backup, memory health, cron health), sub-agent health monitoring, output rules
**Can evolve:** Yes — check priorities, thresholds, active hours, what gets checked
**Do NOT change:** URGENT designation logic

## Non-Harness Files (NOT Evolution Targets)

These files exist in the workspace but are NOT part of the harness:
- `FLUME_FOCUS.md` — Flume product decisions (Tyler-driven)
- `BOOTSTRAP.md` — Initial setup (delete after use)
- `MEMORY.md` sections about Tyler personally
- Individual `memory/YYYY-MM-DD.md` daily logs
- `.learnings/` directory

## What Makes a Good Harness

From the Meta-Harness paper, a good harness:
1. **Gives the model rich, selective access to experience** — not compressed summaries
2. **Is executable code, not just text** — structured configs that the agent can reason about
3. **Has coherent algorithmic structure** — not hard-coded brittle solutions
4. **Exposes what matters for downstream decisions** — traces of failure modes

For Hoss specifically:
- SOUL.md should give strong identity signals that don't require the model to infer
- TOOLS.md should be queryable — agent can grep for a tool and find it instantly
- AGENTS.md should have clear delegation patterns — who does what
- HEARTBEAT.md should have discriminative checks — not just heartbeat OK

## File Naming & Location Convention

When the proposer creates a new candidate harness:
```
~/hoss-evolution/candidates/candidate_N/harness/
  SOUL.md
  IDENTITY.md
  AGENTS.md
  TOOLS.md
  HEARTBEAT.md
```

## Anti-Patterns (What NOT to Propose)

1. **Massive SOUL.md rewrite** — the proposer should make targeted edits, not rewrite everything
2. **Adding "learning" loops that don't exist** — don't claim capabilities that aren't real
3. **Changing git safety rules** — hardcoded constraint
4. **Adding credentials to TOOLS.md** — never, require Tyler approval
5. **Removing the co-founder framing** — this is core identity
6. **Over-tuning to specific benchmark scenarios** — the harness should be generally capable
