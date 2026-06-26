---
name: Agent Compaction Architecture — Production Context Management
slug: agent-compaction-architecture-production-context-management
version: 1.1.1
author: IntuiTek
tags: [production, engineering, compaction, context-management, hardening]
description: Production token thresholds, circuit breaker, and compaction sequence from production Claude Code deployments. Eliminates context death spirals permanently.
---

# Agent Compaction Architecture — Production Context Management

> **New to context management?** Read the free primer first:
> [Context Death Spiral Prevention](https://clawhub.ai/skills/free-compaction-primer)
> It explains the problem this skill solves and why default OpenClaw setups
> don't protect you.

---

## What This Skill Does

This skill installs the exact compaction architecture Anthropic runs in
production Claude Code. It configures your OpenClaw agent with:

- **Empirically validated thresholds** — not guessed. These values were
  measured against real production workloads (p99.99 summary output,
  circuit breaker failure distribution data).
- **6-condition autocompact gate** — prevents premature and thrashing compaction.
- **3-strike circuit breaker** — stops infinite compaction loops cold.
- **Post-compaction cleanup sequence** — verifies compaction actually worked.
- **Microcompaction scheduling** — handles time-based degradation, not just token count.
- **Recursion guards** — prevents compacting a compaction summary.
- **Summary content structure** — specifies what a compaction summary must contain.

---

## Setup

### Step 1 — Install

Place this SKILL.md in your OpenClaw skills directory and reload:

```bash
mkdir -p ~/.openclaw/workspace/skills/agent-compaction
cp SKILL.md ~/.openclaw/workspace/skills/agent-compaction/
```

Then reload OpenClaw or restart the gateway.

### Step 2 — Configure Thresholds

Add these values to your `openclaw.json` compaction config:

```json
{
  "compaction": {
    "mode": "safeguard",
    "keepRecentTokens": 200000,
    "reserveTokensFloor": 20000,
    "model": "anthropic/claude-haiku-4-5"
  }
}
```

These are the production-validated constants. Do not guess alternatives —
the values interact, and changing one without adjusting the others breaks
the gate logic.

### Step 3 — Verify

After 1–2 sessions, check your agent logs for:
- `[compaction] autocompact gate evaluated` — gate is running
- `[compaction] circuit breaker` — breaker initialized
- No `[compaction] error` entries without recovery

If you see `[compaction] threshold breach without gate` — your OpenClaw
version doesn't support the full gate. Check the version requirements below.

---

## Production Thresholds (Exact Values)

| Threshold | Tokens | Purpose |
|-----------|--------|---------|
| Warning | 160,000 | Signal approaching limit |
| Autocompact trigger | 167,000 | Gate evaluation begins |
| Block | 177,000 | Context too full to compact safely |
| Context window | 200,000 | Hard limit |
| Reserve floor | 20,000 | Always reserved for output |

These are derived from production Claude Code deployment baselines.
The 167k trigger gives enough room for compaction output without hitting the
block threshold. The 20k reserve prevents output truncation during compaction.

---

## Architecture Reference

The full behavioral specification is in `COMPACTION_ARCHITECTURE.md`
(included in this package). It covers:

- Section 1: Token threshold management (all 5 values with rationale)
- Section 2: Autocompact gate logic (all 6 conditions)
- Section 3: Circuit breaker specification (3-strike with backoff)
- Section 4: Post-compaction cleanup requirements
- Section 5: Time-based microcompaction
- Section 6: Recursion guard implementation
- Section 7: Summary content structure requirements
- Section 8: Self-audit triggers

---

## Compatibility

- OpenClaw 2026.3.x and above
- Works with: claude-haiku-4-5, claude-sonnet-4-6, claude-opus-4-6
- Recommended compaction model: claude-haiku-4-5 (cost-efficient)

---

## Bundle

This skill is included in the
[Production Agent Ops — Battle-Tested Architecture Pack](https://clawhub.ai/skills/production-agent-ops-battle-tested-architecture-pack)
along with 6 other production architecture files covering loop termination,
session memory, bash security, agent memory scoping, coordinator mode, and
forked agent architecture.

If you need all 7 systems, the bundle ($69) costs less than buying them
individually.
