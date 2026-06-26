---
name: openclaw-self-heal
description: Diagnose and self-resolve OpenClaw system breakage autonomously. Use when: the Control UI / webchat is broken or unreachable, a channel (Discord, Telegram) goes offline or stops responding, the gateway crashes or won't start, memory/plugins report errors, pairing fails, or any OpenClaw component appears broken. Also use proactively during heartbeats when `openclaw status` shows errors. Resolves issues without asking Jake unless the fix requires destructive action or manual intervention.
---

# openclaw-self-heal

Diagnose and fix OpenClaw issues autonomously. Fix first, report after (unless destructive).

## Quick Triage (run first)

```bash
openclaw status 2>&1
openclaw logs --limit 100 2>&1
```

Parse output for: `error`, `warn`, `SIGTERM`, `failed`, `pairing required`, `disconnected`, `crash`.

See `references/diagnostics.md` for symptom → fix mappings.

## Fix Philosophy

1. **Try the safe fix first** — restart gateway, reload config, clear cache
2. **Fix → verify → report** — don't ask Jake until you've tried
3. **Escalate only for:** data loss risk, credential resets, config changes Jake must approve, or repeated failure after 2 attempts
4. **Always log what you did** to `memory/YYYY-MM-DD.md`

## Common Commands

```bash
# Gateway control
openclaw gateway status
openclaw gateway restart
openclaw gateway stop && sleep 3 && openclaw gateway start

# Status + logs
openclaw status
openclaw status --deep
openclaw logs --limit 200
openclaw logs --follow   # use briefly, then kill

# Security audit
openclaw security audit
```

## Verification

After any fix, confirm resolution:
```bash
openclaw status 2>&1 | grep -E "(Gateway|Channel|Error|CRITICAL|WARN)"
```

If still broken after restart, consult `references/diagnostics.md` for deeper fixes.

## Reporting

After resolving: brief summary to Jake — what broke, what you did, current state.
If you couldn't fix it: tell Jake what you found + what you tried, with the exact error.
