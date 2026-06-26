---
name: openclaw-safe-update
description: Safely verify and apply OpenClaw upgrades with isolated sidecar checks. Use when asked to update OpenClaw, verify a target version before upgrading, avoid global package pollution, or run a production-safe upgrade flow with verify-only default and explicit --apply.
homepage: https://docs.openclaw.ai/install/updating
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires": { "bins": ["openclaw", "node", "npm", "curl", "bash"] },
      },
  }
---

# OpenClaw Safe Update

Run production-safe OpenClaw upgrades with isolation-first defaults.

## Workflow

1. Use bundled script: `scripts/openclaw-safe-update.sh`.
2. Run verify-only first (default):
   - `bash scripts/openclaw-safe-update.sh`
   - Optional target pin: `--target <version>`
   - Port is auto-selected from free ports starting at `18000`.
3. If verify fails, inspect log path printed by script and report the root cause.
4. If verify passes, ask whether to apply.
5. Apply only on explicit confirmation:
   - `bash scripts/openclaw-safe-update.sh --apply`

## Platform references

Detect OS first, then read exactly one platform guide:

- macOS (`uname` = `Darwin`) → `references/macos.md`
- Linux (`uname` = `Linux`) → `references/linux.md`

## Rules

- Default to verify-only; never apply without explicit user consent.
- Keep candidate install isolated (`npm --prefix ~/.openclaw/versions/<version>`).
- Keep sidecar isolated (`--profile sidecar-verify`, dedicated `--port`).
- Preserve logs on failure and include path in status updates.
- If verify fails, do not mutate global install.
