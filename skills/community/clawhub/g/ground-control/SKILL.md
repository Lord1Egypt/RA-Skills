---
name: ground-control
description: Verify OpenClaw after upgrades against an operator-maintained model, cron, and channel ground truth. Use for report-only config integrity, provider liveness, cron integrity, session smoke tests, and channel checks; require explicit approval before applying repairs.
metadata:
  openclaw:
    version: "0.3.6"
    emoji: "🛰️"
    homepage: https://clawhub.ai/jonathanjing/ground-control
    requires:
      bins: [openclaw]
---

# ground-control

Post-upgrade verification for OpenClaw. Keeps your system honest after every upgrade.

## 🛠️ Installation

### 1. Ask OpenClaw (Recommended)
Tell OpenClaw: *"Install the ground-control skill."* Installation does not authorize runtime config or cron changes.

### 2. Manual Installation (CLI)
If you prefer the terminal, run:
```bash
openclaw skills install @jonathanjing/ground-control
```

## Permissions & Privileges

This skill requires the following OpenClaw capabilities:
- **`gateway config.get`** — read current config (all phases)
- **`gateway config.patch`** — apply an operator-approved config repair (Phase 1 only)
- **`cron list` / `cron update`** — verify cron jobs and apply operator-approved repairs (Phase 3)
- **`sessions_spawn`** — smoke test sessions (Phase 2, 4, 5)
- **`message send`** — channel liveness test + summary report (Phase 5)

**Change-control behavior:** Every run is report-only by default. Present a redacted repair plan and obtain explicit operator approval immediately before any `gateway config.patch` or `cron update`.

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

1. Copy `{baseDir}/templates/MODEL_GROUND_TRUTH.md` to your workspace root
2. Fill in your actual config values (models, cron jobs, channels)
3. (Optional) For large configs, split into `refs/ground-truth/*.md` sub-files
4. Add the GROUND_TRUTH sync rule to your AGENTS.md (see README)
5. Run `/verify` to test

## Files

- `{baseDir}/templates/MODEL_GROUND_TRUTH.md` — Ground truth template (copy to workspace root)
- `{baseDir}/scripts/post-upgrade-verify.md` — Agent execution prompt for 5-phase verification
- `{baseDir}/scripts/UPGRADE_SOP.md` — Upgrade standard operating procedure
