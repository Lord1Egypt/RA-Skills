---
name: openclaw-session-reply-debug
description: Diagnose OpenClaw "message sent but no assistant reply" issues, then safely switch active model references with primary + multi-fallback support, including heartbeat-triggered recovery to the highest available model.
---

# OpenClaw Session Reply Debug

Use this skill when OpenClaw shows only agent identity (for example "Orchestrator") or no assistant text after `/new` or `/reset`.

## Skill Package Files

- `{baseDir}/SKILL.md`: entry workflow for diagnosing reply failures and model switching.
- `{baseDir}/openclaw-model-connectivity-test.md`: mandatory runbook for model connectivity/availability validation.
- `{baseDir}/scripts/switch-model-to-gpt-5.2.js`: deterministic model-reference switch script.
- `{baseDir}/scripts/switch-model-with-fallback.js`: generic primary + fallback switch script.

## When To Use

- User reports: "I sent a message but got no reply."
- Assistant rows exist but `content` is empty.
- Session shows repeated retries with runtime errors.
- You need to switch active model references from a preferred model to one or more ordered fallback models.
- You want OpenClaw heartbeat / cron to keep probing higher-priority models and switch back automatically when they recover.

## How Users May Ask For This

Users do not need to mention the script name. Natural-language requests should be interpreted into `primary + fallbacks`.

Typical examples:

- `OpenClaw，为我切换到 gpt-5.4，备用 gpt-5.3 和 gpt-5.2。`
- `帮我把主模型设为 gpt-5.4，降级顺序 gpt-5.3 -> gpt-5.2。`
- `让 heartbeat 自动探测 gpt-5.4，不可用就切到 gpt-5.3，再不行就 gpt-5.2。`
- `如果 gpt-5.4 恢复可用，就自动切回最高模型。`

Interpretation rule:

- `gpt-5.4` => `--primary gpt-5.4`
- `gpt-5.3`, `gpt-5.2` => repeated `--fallback`
- `heartbeat 自动探测 / 自动切回` => reuse OpenClaw `heartbeat / cron`, do not build a custom daemon

For the example:

```text
OpenClaw，为我切换 gpt-5.4，备用 gpt-5.3、gpt-5.2。
```

the effective command is:

```bash
node {baseDir}/scripts/switch-model-with-fallback.js \
  --primary gpt-5.4 \
  --fallback gpt-5.3 \
  --fallback gpt-5.2 \
  --apply
```

If the user only wants an emergency narrow rollback, the fixed script is still valid:

- `把 gpt-5.3 回滚到 gpt-5.2`

## Fast Path (3-5 minutes)

1. Resolve `session key -> sessionId -> sessionFile`.
2. Inspect latest assistant rows in session JSONL.
3. If `stopReason=error`, read `errorMessage` directly.
4. Check active model/provider references in config + sessions cache.
5. Apply the narrow rollback script or the generic primary/fallback script.
6. Verify with the same session.

## Find This Chat's JSONL

Known session key:

```bash
rg -n '"agent:main:main"' "$HOME/.openclaw/agents/main/sessions/sessions.json" -S
node -e 'const d=require(process.env.HOME+"/.openclaw/agents/main/sessions/sessions.json"); console.log(d["agent:main:main"])'
```

Unknown session key:

```bash
ls -lt "$HOME/.openclaw/agents/main/sessions" | head -n 20
tail -n 80 "$HOME/.openclaw/agents/main/sessions/<candidate>.jsonl"
```

## Evidence Checklist

Session JSONL:

```bash
tail -n 120 "$HOME/.openclaw/agents/main/sessions/<session-id>.jsonl"
```

Look for:

- `"content":[]`
- `"stopReason":"error"`
- `"errorMessage":"..."`

Model references:

```bash
rg -n "openai/gpt-5\\.3|\"model\"\\s*:\\s*\"gpt-5\\.3\"|\"primary\"\\s*:\\s*\"openai/gpt-5\\.3\"" \
  "$HOME/.openclaw/openclaw.json" \
  "$HOME/.openclaw/agents/main/sessions/sessions.json" -S
```

Runtime logs:

```bash
rg -n "unknown provider|Unknown provider|api key|embedded run start|agent model" \
  "$HOME/.openclaw/logs/gateway.log" \
  "$HOME/.openclaw/logs/gateway.err.log" \
  "/tmp/openclaw/openclaw-$(date +%F).log" -S
```

## Apply Rollback To gpt-5.2

Before applying, read and execute the runbook in `{baseDir}/openclaw-model-connectivity-test.md`.

Dry run:

```bash
node {baseDir}/scripts/switch-model-to-gpt-5.2.js
```

Apply changes:

```bash
node {baseDir}/scripts/switch-model-to-gpt-5.2.js --apply
```

What this changes:

- Active references `openai/gpt-5.3 -> openai/gpt-5.2`
- Session-level bare refs `gpt-5.3 -> gpt-5.2` (for keys like `model`)
- Keeps provider catalog entries (`id`/`name`) untouched to avoid accidental model list corruption

## Apply Primary + Fallback Switching

Use the generic script when the user wants a preferred model plus ordered fallback models:

Dry run:

```bash
node {baseDir}/scripts/switch-model-with-fallback.js \
  --primary gpt-5.4 \
  --fallback gpt-5.3 \
  --fallback gpt-5.2
```

Apply:

```bash
node {baseDir}/scripts/switch-model-with-fallback.js \
  --primary gpt-5.4 \
  --fallback gpt-5.3 \
  --fallback gpt-5.2 \
  --apply
```

Behavior:

- Probe candidates in priority order on every run
- Select the first available model
- Rewrite active model references in OpenClaw config + session cache
- Preserve provider catalog `id` / `name`
- Automatically switch back to the highest-priority available model on a later run

Example:

- Current model is `gpt-5.2`
- A heartbeat run later finds `gpt-5.4` available again
- The same command will switch active references back to `gpt-5.4`

## Heartbeat / Cron Integration

Do **not** write a custom daemon for this workflow. Reuse OpenClaw's built-in `heartbeat` / `cron`, and let heartbeat trigger the existing JS script.

Recommended pattern:

1. Create a cron job with `wakeMode: "next-heartbeat"`
2. Put the desired priority list in the task parameters
3. Have heartbeat execute the existing JS with those parameters

Current repo support is the CLI contract, so the stable mapping is:

- task `primary` -> `--primary`
- task `fallbacks[]` -> repeated `--fallback`
- task `provider` -> `--provider`
- task `probeTimeoutMs` -> `--probe-timeout-ms`
- task `apply=true` -> `--apply`

If your current OpenClaw cron payload only supports text, pass the parameters by expanding them into the command itself:

```bash
node {baseDir}/scripts/switch-model-with-fallback.js \
  --primary gpt-5.4 \
  --fallback gpt-5.3 \
  --fallback gpt-5.2 \
  --apply
```

This is enough to achieve:

- automatic downgrade when `gpt-5.4` is unavailable
- automatic recovery to `gpt-5.4` once the next heartbeat sees it become available again

## Mandatory Model Availability Validation

When switching models, this validation is required:

1. Pre-switch availability check (from runbook):
   - Validate the intended target candidates can pass Provider probe + Agent probe.
2. Apply the switch script (`--apply`) or the generic fallback script.
3. Post-switch availability check (from runbook):
   - Re-run Provider probe + Agent probe using the selected active model.
4. Only declare success when probes pass and session reply is non-empty.

## Verify Before Claiming Fix

Send test message to the same session:

```bash
openclaw agent \
  --session-id <session-id> \
  --message "connectivity check: reply OK only" \
  --json \
  --timeout 120
```

Success criteria:

- Exit code `0`
- `"status":"ok"`
- Non-empty assistant payload
- `agentMeta.model` is the selected target model (for example `gpt-5.4`, `gpt-5.3`, or `gpt-5.2`)

## Notes

- Archived message hooks do not prove reply generation succeeded.
- UI can hide root cause; JSONL + logs are source of truth.
- For emergencies, the fixed `gpt-5.3 -> gpt-5.2` script remains valid.
- For normal operations, prefer the generic primary/fallback script so heartbeat can downgrade and recover automatically.
