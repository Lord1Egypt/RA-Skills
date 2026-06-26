---
name: openclaw-growth-pack
description: Turn a fresh OpenClaw install into a reliable execution agent. Use when users report "asks step-by-step only", stalls mid-task, token mismatch, or model routing/auth failures. Apply a production onboarding baseline: model routing, gateway token consistency, anti-stall heartbeat, lightweight autonomy loop, and verification checklist.
---

# OpenClaw Growth Pack

Apply this skill to bootstrap a new OpenClaw instance into a stable, task-completing setup.

Use this workflow in order:
1. Align model routing and provider endpoint.
2. Align gateway token values across runtime surfaces.
3. Install anti-stall execution contract in `AGENTS.md` and `HEARTBEAT.md`.
4. Enable lightweight periodic self-check.
5. Run verification gates before calling setup complete.

Keep changes minimal, auditable, and reversible.

## 1) Model Routing Baseline

Use one source of truth in `~/.openclaw/openclaw.json`:

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "bailian": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "YOUR_CODING_PLAN_KEY"
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "bailian/qwen3-coder-plus"
      }
    }
  }
}
```

Rules:
- Do not keep `coding-intl.dashscope.aliyuncs.com` in active config.
- Do not duplicate provider definitions in multiple files unless strictly needed.
- If `~/.openclaw/agents/main/agent/models.json` exists, remove conflicting provider overrides.

## 2) Gateway Token Consistency

Keep all token surfaces aligned:
- `gateway.auth.token` in `openclaw.json`
- `gateway.remote.token` in `openclaw.json` (if present)
- Dashboard Control UI token (paste the same value)

PowerShell audit:

```powershell
$cfg = Get-Content "$HOME/.openclaw/openclaw.json" -Raw | ConvertFrom-Json
$auth = $cfg.gateway.auth.token
$remote = $cfg.gateway.remote.token
"auth.token   = $auth"
"remote.token = $remote"
if ($remote -and $auth -ne $remote) { Write-Warning "Token mismatch in openclaw.json" }
```

After any token change:

```powershell
openclaw gateway restart
```

## 3) Anti-Stall Contract

Write or update `AGENTS.md` with these mandatory constraints:
- Output state on each substantial task: `Goal`, `Progress`, `Next`.
- Do not stop before completion except for explicit blocker or user stop.
- On failure: retry, then fallback, then report minimal unblock input.
- Multi-step completion must include evidence artifact path or command result summary.

Write or update `HEARTBEAT.md`:
- Each cycle performs at most 1-2 checks.
- Either produce execution evidence or exactly `HEARTBEAT_OK`.
- If queue item exists, execute one concrete step, then log evidence to `memory/YYYY-MM-DD.md`.

## 4) Lightweight Autonomy Loop

If cron/system events are available, create conservative jobs:
- Daily: unfinished-task check.
- Weekly: memory review and friction pattern extraction.

If cron is unavailable, enforce manual equivalent:
- Start-of-day: review `tasks/QUEUE.md`, pick one actionable item.
- End-of-day: append one lesson to `memory/YYYY-MM-DD.md`.

## 5) Verification Gates (Do Not Skip)

Setup is complete only when all pass:
- Model call succeeds with primary route.
- Gateway access succeeds without token mismatch.
- A 3+ step task finishes with evidence.
- At least one blocker path is documented in `memory/blocked-items.md`.

Recommended evidence:
- command summary
- artifact path or URL
- final status (`done` or `blocked` with required input)

## 6) Rollback

Before edits, create backups:

```powershell
Copy-Item "$HOME/.openclaw/openclaw.json" "$HOME/.openclaw/openclaw.json.bak" -Force
```

Rollback:

```powershell
Copy-Item "$HOME/.openclaw/openclaw.json.bak" "$HOME/.openclaw/openclaw.json" -Force
openclaw gateway restart
```

## References

For concrete command examples and troubleshooting playbooks, read:
- `references/examples.md`
