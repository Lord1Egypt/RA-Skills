---
name: ground-control
description: Post-upgrade verification system for OpenClaw. Defines a model/cron/channel ground truth file and a 5-phase automated verification flow (config integrity, API key liveness, cron integrity, session smoke test, channel liveness) with auto-repair for config and cron drift.
version: "0.3.5"
metadata:
  author: JonathanJing
  tags: [ops, verification, upgrade, config, cron, health]
  license: MIT
  credentials: none
---

# ground-control

Post-upgrade verification for OpenClaw. Keeps your system honest after every upgrade.

## 🛠️ Installation

### 1. Ask OpenClaw (Recommended)
Tell OpenClaw: *"Install the ground-control skill."* The agent will handle the installation and configuration automatically.

### 2. Manual Installation (CLI)
If you prefer the terminal, run:
```bash
clawhub install ground-control
```

## Permissions & Privileges

This skill requires the following OpenClaw capabilities:
- **`gateway config.get`** — read current config (all phases)
- **`gateway config.patch`** — auto-fix config drift (Phase 1 only)
- **`cron list` / `cron update`** — verify and auto-fix cron jobs (Phase 3)
- **`sessions_spawn`** — smoke test sessions (Phase 2, 4, 5)
- **`message send`** — channel liveness test + summary report (Phase 5)

**Auto-fix behavior:** Phases 1 and 3 will automatically patch config/cron to match GROUND_TRUTH. Use `--dry-run` to disable auto-fix and get a report-only run.

**Security & Redaction:** This skill enforces a Zero-Secret Logging protocol.
- **Immediate Redaction**: Sensitive nodes (`auth`, `plugins`) are stripped from memory after fetching runtime config.
- **Redacted Drift**: Mismatches in sensitive fields are reported as `[REDACTED_SENSITIVE_MISMATCH]`.
- **Functional Validation**: API keys are tested through functional calls (Phase 2), never through literal comparison.
- **No Persistence**: Literal credentials are never written to `memory/` files or messaging channels.

**Environment variables:** None.

## When to use

- After running `openclaw update` or `npm install -g openclaw@latest`
- When you suspect config drift (model changed, cron broken, channel down)
- Periodic health check via `/verify` command

## Setup

1. Copy `templates/MODEL_GROUND_TRUTH.md` to your workspace root
2. Fill in your actual config values (models, cron jobs, channels)
3. Add the GROUND_TRUTH sync rule to your AGENTS.md (see README)
4. Run `/verify` to test

## Files

- `templates/MODEL_GROUND_TRUTH.md` — Ground truth template (copy to workspace root)
- `scripts/post-upgrade-verify.md` — Agent execution prompt for 5-phase verification
- `scripts/UPGRADE_SOP.md` — Upgrade standard operating procedure
