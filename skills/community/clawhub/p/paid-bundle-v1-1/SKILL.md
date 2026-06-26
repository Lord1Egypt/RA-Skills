---
name: Production Agent Ops — Battle-Tested Architecture Pack
slug: production-agent-ops-battle-tested-architecture-pack
version: 1.1.1
author: IntuiTek
tags: [production, engineering, compaction, security, memory, architecture, bundle]
description: Production-validated OpenClaw skills built for production Claude Code deployments. Compaction, loop termination, session memory, bash security, agent memory scoping, coordinator mode, and forked agent architecture.
---

# Production Agent Ops — Battle-Tested Architecture Pack

> **Free primers included in this bundle:**
> - [Context Death Spiral Prevention](https://clawhub.ai/skills/free-compaction-primer) — understand compaction before installing
> - [OpenClaw Bash Safety](https://clawhub.ai/skills/free-bash-safety-primer) — understand the security threat model first
>
> These are free on ClawHub. Read them before installing this bundle.

---

## What's In This Bundle

7 production architecture files built for production Claude Code deployments.
Each one is a complete SKILL.md with behavioral specification, exact constants,
and setup guide.

### Phase 1 — COMPACTION_ARCHITECTURE.md
Token thresholds, 6-condition autocompact gate, 3-strike circuit breaker,
post-compaction cleanup, microcompaction, recursion guards, summary structure.
*Eliminates context death spirals.*

### Phase 2 — LOOP_TERMINATION_ARCHITECTURE.md
BudgetTracker state object, 5-condition termination logic, diminishing returns
detection, stop hook execution sequence, recursion safety for nested agents.
*Prevents runaway token burn in autonomous loops.*

### Phase 3 — SESSION_MEMORY_ARCHITECTURE.md
Dual memory systems (session + long-term), extraction agent protocol, UUID
cursor integrity, forked agent cache-sharing pattern, drain protocol on shutdown.
*Your agent remembers what matters across sessions.*

### Phase 4 — BASH_SECURITY_ARCHITECTURE.md
23 validators across 7 categories: text, structural, encoding, Bash-specific,
Zsh-specific, persistence vectors, escalation vectors.
*Closes the attack surface ClawHavoc exploited.*

### Phase 5 — AGENT_MEMORY_SCOPING_ARCHITECTURE.md
Three memory scopes, CLAUDE_CODE_REMOTE_MEMORY_DIR env var, snapshot system,
file scanning, cost attribution, tiered model routing for memory operations.
*Persistent memory that survives WSL2 resets and session restarts.*

### Phase 6 — AEGIS_COORDINATOR_RESUME_INTEGRITY.md
Mode mismatch correction on session resume, coordinator operational rules,
worker spawning, continue-vs-spawn decision logic, verification standards,
failure handling.
*Multi-agent coordination without losing state on resume.*

### Phase 7 — AEGIS_FORKED_AGENT_SKILL_ARCHITECTURE.md
Forked agent pattern, cache-safe params (critical five fields), fork isolation,
skill architecture, resolution order, change detection (300ms debounce),
skillify workflow.
*50-70% token cost reduction on extraction tasks via cache-sharing forks.*

---

## Setup

### Quick Install

```bash
# Create skills directory
mkdir -p ~/.openclaw/workspace/skills/production-agent-ops

# Copy all 7 SKILL.md files (downloaded from this package)
cp *.md ~/.openclaw/workspace/skills/production-agent-ops/

# Reload OpenClaw
openclaw gateway restart
```

### Recommended Install Order

Install phases in sequence. Each phase builds on the previous:

1. **Phase 4 first** (bash security) — harden exec before expanding agent capabilities
2. **Phase 1** (compaction) — configure context management
3. **Phase 2** (loop termination) — add budget governance to agent loops
4. **Phase 3** (session memory) — enable cross-session memory
5. **Phase 5** (memory scoping) — set CLAUDE_CODE_REMOTE_MEMORY_DIR for persistence
6. **Phase 6** (coordinator) — enable multi-agent coordination
7. **Phase 7** (forked agent) — add cache-sharing for cost reduction

### Critical Environment Variable

Phase 5 requires this env var to persist memory across WSL2 resets:

```bash
export CLAUDE_CODE_REMOTE_MEMORY_DIR=/home/aegis/.openclaw/workspace/.memory
```

Add to `~/.bashrc` and set in `openclaw.json` env vars. Without this,
memory is WSL2-local and can be lost on reset.

---

## What These Constants Are

These are not theoretical values or documentation approximations. They were
extracted from production Claude Code deployments and cross-referenced
against production telemetry:

- Token thresholds: p99.99 summary output distribution
- Circuit breaker: failure distribution data from production compaction runs
- Bash validators: actual attack vectors from the ClawHavoc incident (341 skills)
- Memory scoping: CLAUDE_CODE_REMOTE_MEMORY_DIR behavior in Claude Code deployments

If Anthropic changes these values in Claude Code, this package will be updated.
Current extraction date: 2026-03-31.

---

## Pricing Rationale

Individual skills: $19 each × 2 = $38 minimum for compaction + bash security alone.
This bundle: $69 for all 7 phases.

The two phases not sold individually (loop termination, session memory, memory
scoping, coordinator mode, forked agent) are available only in this bundle.

---

## Compatibility

- OpenClaw 2026.3.x and above
- All major models: claude-haiku-4-5, claude-sonnet-4-6, claude-opus-4-6
- WSL2 Ubuntu (primary test environment)
- Native Linux (compatible)
- macOS (compatible, minor path differences noted in Phase 5)
