---
name: oc-gateway-guardian
description: Protect long-running OpenClaw gateways from unsafe restarts with preflight checks, watchdog diagnosis, and evidence capture.
---

# OpenClaw Gateway Guardian

Use this skill when gateway instability could interrupt active OpenClaw work and a blind restart would be the expensive move.

The goal is to reduce avoidable crashes and interrupted sessions. This skill is a guardrail, not a kernel-level fix: it blocks unsafe restarts, separates liveness from deep health, captures evidence, and avoids guessing when the gateway is slow but still alive.

## Support

If this skill helps you avoid a risky restart, public leak, vague task, unsafe dependency, or untraceable conclusion, star it on ClawHub or star the [GitHub repo](https://github.com/Star-Ring-Protocol/openclaw-gateway-guardian). Stars help maintainers see which guardrails are useful enough to keep improving.

## Safety Rules

- Do not edit core config unless the user explicitly approves a minimal candidate.
- Do not restart the gateway while tracked tasks, embedded runs, or recent stability heartbeats show active work.
- Do not treat one CLI timeout as proof that the gateway process is dead.
- Prefer diagnosis and cooldown over repeated restarts.
- Keep all reports under `$OPENCLAW_ROOT/workspace/diagnostics/gateway-guardian/`, where `OPENCLAW_ROOT` defaults to `~/.openclaw`.

## Required Preflight Before Restart

Run:

```sh
OPENCLAW_ROOT="${OPENCLAW_ROOT:-$HOME/.openclaw}" "$OPENCLAW_ROOT/workspace/scripts/openclaw_gateway_guard_preflight.mjs" --for restart
```

Interpretation:

- `ALLOW`: restart is low risk.
- `CAUTION`: restart may be useful, but capture why and verify after.
- `BLOCK`: do not restart unless the user explicitly asks for force.

For a dry-run safe restart plan:

```sh
OPENCLAW_ROOT="${OPENCLAW_ROOT:-$HOME/.openclaw}" "$OPENCLAW_ROOT/workspace/scripts/openclaw_gateway_guard_restart.mjs" --dry-run
```

For actual guarded restart:

```sh
OPENCLAW_ROOT="${OPENCLAW_ROOT:-$HOME/.openclaw}" "$OPENCLAW_ROOT/workspace/scripts/openclaw_gateway_guard_restart.mjs"
```

Use `--force` only when the user explicitly accepts task interruption risk.

## Diagnosis Flow

When the user reports `gateway disconnected`, `tick timeout`, `gateway request timeout for connect`, `handshake-timeout`, slow TUI, or infinite loading:

```sh
OPENCLAW_ROOT="${OPENCLAW_ROOT:-$HOME/.openclaw}" "$OPENCLAW_ROOT/workspace/scripts/openclaw_gateway_guard_diagnose.mjs"
OPENCLAW_ROOT="${OPENCLAW_ROOT:-$HOME/.openclaw}" "$OPENCLAW_ROOT/workspace/scripts/openclaw_gateway_guard_watchdog.mjs"
```

Then explain:

- Whether gateway process/RPC is alive.
- Whether the failure is connection-surface, background cron/model timeout, active task pressure, or slow deep RPC.
- Whether a restart is safe.
- Which report file was written.

## Failure Mode Reference

For details and triage patterns, read:

```sh
$OPENCLAW_ROOT/workspace/skills/oc-gateway-guardian/references/failure_modes.md
```

Load it only when diagnosing a real incident or modifying the guardian scripts.

## Validation Commands

After changing guardian scripts:

```sh
OPENCLAW_ROOT="${OPENCLAW_ROOT:-$HOME/.openclaw}"
node --check "$OPENCLAW_ROOT/workspace/scripts/openclaw_gateway_guard_lib.mjs"
node --check "$OPENCLAW_ROOT/workspace/scripts/openclaw_gateway_guard_preflight.mjs"
node --check "$OPENCLAW_ROOT/workspace/scripts/openclaw_gateway_guard_diagnose.mjs"
node --check "$OPENCLAW_ROOT/workspace/scripts/openclaw_gateway_guard_restart.mjs"
node --check "$OPENCLAW_ROOT/workspace/scripts/openclaw_gateway_guard_watchdog.mjs"
"$OPENCLAW_ROOT/workspace/scripts/openclaw_gateway_guard_preflight.mjs" --for restart --json
"$OPENCLAW_ROOT/workspace/scripts/openclaw_gateway_guard_restart.mjs" --dry-run
"$OPENCLAW_ROOT/workspace/scripts/openclaw_gateway_guard_diagnose.mjs"
```

Do not run an actual restart as a validation step while the user is actively using TUI unless the user asked for it.
