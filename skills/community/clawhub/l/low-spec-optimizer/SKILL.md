---
name: low-spec-optimizer
description: "Optimize OpenClaw performance on machines with limited resources (4GB RAM or less, old CPUs). Use when (1) user mentions slow performance, high RAM usage, or system lag, (2) running on Raspberry Pi, old laptops, or budget VPS, (3) proactively during heartbeats to check system health, (4) before spawning multiple subagents on low-resource machines. Provides resource monitoring, automatic cleanup, session management, and configuration recommendations for constrained environments."
---

# Low-Spec Optimizer

Help OpenClaw run smoothly on machines with limited resources.

## Quick Start

Check current resources:

```bash
bash <skill-dir>/scripts/check_resources.sh
```

Parse output with `jq`:
```bash
bash <skill-dir>/scripts/check_resources.sh | jq '.alert, .ram.pct, .cpu.pct'
```

## Workflow

### 1. Check resources before heavy operations

Before spawning subagents, opening browser, or running intensive tasks:

```bash
bash <skill-dir>/scripts/check_resources.sh
```

Decision matrix based on `alert` field:
- **OK** (< 60% RAM): Proceed normally
- **ELEVATED** (60-75%): Limit to 1 subagent, close browser first
- **WARNING** (75-90%): Run cleanup, avoid spawning, warn user
- **CRITICAL** (> 90%): Emergency cleanup, ask user before proceeding

### 2. Cleanup when needed

```bash
# Dry run first
bash <skill-dir>/scripts/cleanup_sessions.sh --dry-run

# Execute cleanup
bash <skill-dir>/scripts/cleanup_sessions.sh

# Aggressive (includes npm/pip/journal)
bash <skill-dir>/scripts/cleanup_sessions.sh --aggressive
```

### 3. Apply config recommendations

For machines with ≤4GB RAM, suggest OpenClaw config changes.
See [references/config-guide.md](references/config-guide.md) for full details.

Key recommendations:
- Use free/lightweight models (hunter-alpha, GLM-4.5-air)
- Set thinking to `"off"` unless needed
- Limit concurrent subagents to 2 max
- Always close browser after use
- Prefer `web_fetch` over browser automation
- Use `mode: "run"` for subagents (auto-cleanup)

### 4. Proactive monitoring (heartbeat)

During heartbeats on low-spec machines:

```bash
bash <skill-dir>/scripts/check_resources.sh | jq -r '.alert'
```

If alert is `WARNING` or `CRITICAL`, notify the user with specifics:
- Which process is consuming most memory
- How much is free
- Recommended action (cleanup, close apps, restart)

## Rules for constrained environments

1. **One browser at a time** — never parallel browser sessions
2. **Close everything after use** — browser, subagent sessions, temp files
3. **Check before opening** — always check RAM before heavy operations
4. **Prefer lightweight alternatives** — `web_fetch` > browser, `mode: "run"` > `mode: "session"`
5. **Batch operations** — combine tasks instead of spawning separate sessions
6. **Use cron over heartbeat** — for precise scheduling, use cron with isolated sessions
