---
name: openclaw-feishu-quota-guard
description: Use when a user wants OpenClaw itself to diagnose or fix Feishu/Lark quota burn caused by heartbeats, health checks, webhook probes, or overly expensive background runs. Start by running the bundled run-once fixer, then only do manual follow-up if custom gateway or webhook code is detected.
---

# OpenClaw Feishu Quota Guard

Use this skill when OpenClaw is connected to Feishu/Lark and a user reports that free quota or paid API budget is draining unexpectedly.

This skill is based on a short Bilibili video about `OpenClaw + Feishu` quota burn and cross-checked against current OpenClaw docs. The likely failure mode is not "chat usage" itself, but background traffic:

- OpenClaw heartbeat runs that still hit a cloud model
- Feishu webhook or custom gateway health probes that accidentally trigger model work

Read [references/source-notes.md](references/source-notes.md) only if you need the exact source-backed assumptions.

## Quick Start

1. Run the bundled fixer in the native shell for that machine:
   - macOS/Linux: `bash scripts/run-once.sh --dry-run`
   - Windows PowerShell: `powershell -ExecutionPolicy Bypass -File scripts/run-once.ps1 --dry-run`
   - Any OS with Python: `python scripts/apply_feishu_quota_fix.py --dry-run`
2. If the summary only reports official/current OpenClaw heartbeat settings, run the same command without `--dry-run`.
3. If the summary reports custom webhook or gateway health routes, keep the automatic heartbeat fix and then inspect those files manually.
4. Restart the relevant process and verify from logs that repeated probes no longer trigger expensive model calls.

## Default behavior of the bundled fixer

The bundled fixer makes only safe automatic changes to standard OpenClaw config:

- `agents.defaults.heartbeat.every = "1h"`
- `agents.defaults.heartbeat.lightContext = true`
- `agents.defaults.heartbeat.isolatedSession = true`
- if `target` is missing, set `target = "none"`

If you want a full stop instead of throttling, run:

```bash
bash scripts/run-once.sh --mode disable
```

On Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-once.ps1 --mode disable
```

That sets:

- `agents.defaults.heartbeat.every = "0m"`

## Workflow

### 1. Confirm the topology first

Do not patch blindly.

- If the install uses the bundled/current Feishu plugin, treat this as a heartbeat-cost problem first.
- If the install uses a webhook bridge or custom gateway, inspect the health route before touching heartbeat settings.

Useful search terms:

- `channels.feishu`
- `@openclaw/feishu`
- `heartbeat`
- `HEARTBEAT.md`
- `connectionMode`
- `webhook`
- `verificationToken`
- `health`
- `gateway`

### 2. Fix path A: reduce or cheapen OpenClaw heartbeat work

Use this path for the official/current plugin, or anytime logs show scheduled heartbeat runs causing the spend.

Focus on:

- `~/.openclaw/openclaw.json` or the workspace config the user actually runs
- `agents.defaults.heartbeat`
- `agents.list[].heartbeat`
- `HEARTBEAT.md`

Preferred order of fixes:

1. First run the bundled fixer in throttle mode.
   It applies the lowest-risk cost reduction settings supported by current OpenClaw heartbeat docs.
2. If heartbeat is not needed, disable it or make the heartbeat prompt effectively empty.
   OpenClaw docs say an effectively empty `HEARTBEAT.md` skips the heartbeat run and saves API calls.
3. If heartbeat is needed, lower frequency first.
   Safe first move: change `every` from a short interval to `1h` or longer.
4. Reduce token and context cost.
   Prefer `lightContext: true`, `isolatedSession: true` when appropriate, and avoid sending heartbeat output anywhere unless the user really wants it.
5. Route heartbeat away from an expensive cloud model.
   If the install supports a separate heartbeat model, use a cheap or local model for heartbeat-only checks.
6. Keep `HEARTBEAT.md` tiny.
   A bloated checklist wastes tokens every run.

When editing configs manually, prefer minimal changes like:

```jsonc
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "1h",
        "lightContext": true,
        "target": "none"
      }
    }
  }
}
```

Only add a heartbeat-specific local model if the config format in that install already supports it.

### 3. Fix path B: stop Feishu/webhook health probes from touching the model

Use this path for older installs, custom bridges, or any codebase where `/health`, `/ready`, or webhook verification ends up invoking OpenClaw chat/model logic.

Goal: liveness checks must return a cheap static success unless the user explicitly wants an end-to-end synthetic test.

Preferred order of fixes:

1. Do not auto-patch arbitrary app code unless the relevant route is obvious and isolated.
2. Separate liveness from end-to-end checks.
   `/health` should usually return a static `200 OK` plus lightweight process info.
3. If a real downstream check is required, cache the successful result.
   A 24-hour cache is a good default for "bot still works" validation when the alternative is paying every minute.
4. Never let Feishu verification or heartbeat probes call the main chat pipeline.
5. If a custom bridge currently pings the model every 60 seconds, patch that route first before changing user-facing chat behavior.

For route handlers, acceptable outcomes are:

- static `ok`
- cached status object
- cheap local state check

Avoid:

- calling the main message handler
- creating a new OpenClaw chat turn
- invoking the paid model just to answer a health probe

### 4. Verify after the patch

After editing:

1. Restart the OpenClaw gateway, plugin host, or custom bridge.
2. Watch logs for 3-5 minutes.
3. Confirm one of these outcomes:
   - heartbeat frequency dropped to the intended interval
   - `/health` still gets hit, but no model invocation follows
   - quota burn rate stops climbing abnormally

If the user is on Docker, check container logs rather than assuming host paths.

## Guardrails

- Do not change unrelated chat routing.
- Do not remove webhook verification unless the user is intentionally leaving webhook mode.
- Prefer the smallest patch that stops repeated paid calls.
- If the system mixes official Feishu config with custom gateway code, patch the custom health route first and then review heartbeat settings.
- If the bundled fixer already solved the standard heartbeat cost issue, say so clearly and stop there unless custom webhook code still appears in the scan.
