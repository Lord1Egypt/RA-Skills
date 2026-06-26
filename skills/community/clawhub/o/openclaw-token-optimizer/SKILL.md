---
name: token-optimizer
description: OpenClaw Token Optimizer v3.2.0 — practical cost-control toolkit for OpenClaw agents. Lazy context loading, Sonnet/Opus-aware routing, heartbeat scheduling, local token budgets, cache-TTL guidance, and security-audit-safe command behavior for current OpenClaw 2026.6.x installs.
version: 3.2.0
homepage: https://github.com/Asif2BD/OpenClaw-Token-Optimizer
source: https://github.com/Asif2BD/OpenClaw-Token-Optimizer
author: Asif2BD
metadata:
  {
    "openclaw":
      {
        "emoji": "💸",
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "github",
              "kind": "link",
              "label": "GitHub",
              "url": "https://github.com/Asif2BD/OpenClaw-Token-Optimizer",
            },
            {
              "id": "security",
              "kind": "link",
              "label": "Security Notes",
              "url": "https://github.com/Asif2BD/OpenClaw-Token-Optimizer/blob/main/SECURITY.md",
            },
          ],
      },
  }
security:
  verified: true
  auditor: Oracle (Matrix Zion)
  audit_date: 2026-06-22
  scripts_no_network: true
  scripts_no_code_execution: true
  scripts_no_subprocess: true
  scripts_data_local_only: true
  explicit_workspace_writes: true
  default_commands_no_overwrite: true
  reference_files_describe_external_services: true
  optimize_sh_is_convenience_wrapper: true
  optimize_sh_only_calls_bundled_python_scripts: true
---

# OpenClaw Token Optimizer v3.2.0

[![Version](https://img.shields.io/badge/version-3.2.0-brightgreen.svg)](https://github.com/Asif2BD/OpenClaw-Token-Optimizer/blob/main/CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/Asif2BD/OpenClaw-Token-Optimizer/blob/main/LICENSE)

Built for current OpenClaw 2026.6.x agents by [Asif2BD](https://github.com/Asif2BD) · [GitHub](https://github.com/Asif2BD/OpenClaw-Token-Optimizer) · [Security Notes](https://github.com/Asif2BD/OpenClaw-Token-Optimizer/blob/main/SECURITY.md)

> **Security notice:** local-only optimization toolkit. The Python scripts make no network requests and do not execute dynamic code. Commands that write files are explicit, documented, and backup-safe.

---

## Install

```bash
openclaw skills install @asif2bd/openclaw-token-optimizer
```

---

## What's New in v3.2

### Modern ClawHub Card
The skill card now leads with a clearer product promise, current OpenClaw compatibility, security posture, and practical commands instead of the older long-form v3.0 copy.

### Current OpenClaw Model Routing
Routine Anthropic work maps to `anthropic/claude-sonnet-4-5`; only explicitly complex reasoning routes to `anthropic/claude-opus-4-5`.

### Audit-Safe Writes
- `context_optimizer.py generate-agents` prints to stdout by default.
- Writing an optimized `AGENTS.md` requires `--output` or `--workspace-output`.
- `./scripts/optimize.sh heartbeat` previews only by default.
- `./scripts/optimize.sh heartbeat install` writes `HEARTBEAT.md` only after backing up an existing file.

---

## What It Optimizes

### Context Loading
Stop loading every workspace file into every session. Recommend only the context needed for the current prompt.

```bash
python3 scripts/context_optimizer.py recommend "hi"
```

Typical result: `SOUL.md` + `IDENTITY.md` only for a greeting.

### Model Routing
Keep standard work on Sonnet and reserve Opus for deep reasoning.

```bash
python3 scripts/model_router.py "thanks!"
python3 scripts/model_router.py "design a multi-agent architecture"
```

### Heartbeat Scheduling
Run only checks that are due, respect quiet hours, and align heartbeat timing with prompt-cache TTL.

```bash
python3 scripts/heartbeat_optimizer.py plan
python3 scripts/heartbeat_optimizer.py cache-ttl
```

### Token Budgets
Track local daily budget state and surface warnings before runaway spend.

```bash
python3 scripts/token_tracker.py check
```

---

## Quick Start

### 1. Find the minimum context for a request

```bash
python3 scripts/context_optimizer.py recommend "write a deployment checklist"
```

### 2. Preview an optimized AGENTS.md

```bash
python3 scripts/context_optimizer.py generate-agents
```

Save a review copy only when you explicitly ask for it:

```bash
python3 scripts/context_optimizer.py generate-agents --output ~/.openclaw/workspace/AGENTS.md.optimized
```

### 3. Preview heartbeat installation

```bash
./scripts/optimize.sh heartbeat
```

Install with backup protection:

```bash
./scripts/optimize.sh heartbeat install
```

### 4. Route a task

```bash
python3 scripts/model_router.py "debug this error"
```

---

## Savings Profile

| Area | Typical waste | Optimizer approach |
|------|---------------|-------------------|
| Startup context | Loading docs, memory, tools, and old logs every turn | Lazy-load only what the prompt needs |
| Routine model use | Opus used for quick replies or simple checks | Sonnet for routine work, Opus for complex reasoning |
| Heartbeats | Every check runs on every heartbeat | Due-check planner + quiet hours |
| Cache TTL | Idle sessions trigger expensive cache rewrites | 55-minute heartbeat guidance for 1-hour cache TTL |
| Budget control | Spend discovered after the fact | Local budget checks before expensive work |

Expected savings: **50-80%** in context-heavy OpenClaw workspaces, with context optimization usually delivering the biggest win.

---

## Files

### Scripts
- `scripts/context_optimizer.py` — prompt classification and context bundle recommendations
- `scripts/model_router.py` — Sonnet/Opus-aware task routing
- `scripts/heartbeat_optimizer.py` — due-check planning, quiet hours, cache-TTL interval guidance
- `scripts/token_tracker.py` — local budget tracking
- `scripts/optimize.sh` — convenience wrapper around bundled scripts

### Assets
- `assets/HEARTBEAT.template.md` — backup-safe heartbeat template
- `assets/cronjob-model-guide.md` — scheduled-task model guidance
- `assets/config-patches.json` — native and optional config examples

### References
- `references/PROVIDERS.md` — optional external-provider strategy notes
- `SECURITY.md` — complete security and data-handling breakdown

---

## Security Posture

- No network calls in executable scripts
- No `eval`, dynamic imports, shell command execution, or downloader behavior
- Local JSON state only under the OpenClaw workspace memory directory
- Workspace writes require explicit commands
- Existing `HEARTBEAT.md` is backed up before replacement
- `.clawhubsafe` covers every published file with SHA256 hashes

Verify locally:

```bash
sha256sum -c .clawhubsafe
```

---

## Native OpenClaw Diagnostics

Use OpenClaw's built-in context and usage commands alongside this skill:

```text
/context list
/context detail
/usage tokens
/usage cost
```

Use the built-ins to see where tokens are going, then use Token Optimizer to reduce the recurring waste.

---

## Best Fit

- Multi-agent OpenClaw workspaces with large instruction files
- Agents that run heartbeats or scheduled checks
- Teams trying to keep Opus for hard work instead of routine work
- xCloud, MissionDeck, or other hosted OpenClaw deployments where every saved prompt token compounds across users

---

## More by Asif2BD

```bash
openclaw skills install @asif2bd/jarvis-mission-control
openclaw skills search asif2bd
```
