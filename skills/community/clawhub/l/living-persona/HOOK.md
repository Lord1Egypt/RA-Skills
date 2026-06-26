---
name: living-persona
description: "Dynamic personality engine — signal-based trait propagation + hysteresis + structural voice injection for OpenClaw agents"
homepage: https://docs.openclaw.ai/automation/hooks
metadata:
  {
    "openclaw": {
      "emoji": "✨",
      "events": ["message:preprocessed"],
      "requires": { "config": ["workspace.dir"] }
    }
  }
---

# Living Persona Hook

Fires on `message:preprocessed` — after the message is enriched but before the agent sees it.

## What It Does

1. **Analyzes** the message for topic and tone signals
2. **Propagates** trait activations through a resonance network
3. **Applies hysteresis decay** — traits fade slowly, not instantly
4. **Writes structural injection** — `persona-inject.md` with generation directives
5. **Writes voice guide** — `persona-inbound.md` with readable trait context
6. **Persists state** — `persona-state.json` across turns

## Files Written

| File | Purpose | Include in prompt? |
|------|---------|-------------------|
| `persona-inject.md` | Structural generation directive | ✅ Yes |
| `persona-inbound.md` | Full voice guide with traits | Optional |
| `persona-state.json` | Trait persistence | Read on startup |
| `persona-trigger.txt` | Sentinel for last run timestamp | No |

## Structural Injection

The hook rewrites `persona-inject.md` with the top 2 active traits as generation directives. Include this file in your agent's prompt template:

```
{memory}/persona-inject.md
```

## Configuration

Edit `hook.json` to tune:
- `hysteresis.*` — trait decay rates
- `thresholds.*` — minimum trait strength, top N for injection
- `mode` — `"structural"` (default) or `"ambient"`

## Reset on New Session

Run `scripts/reset_persona.py` on `/new` or `/reset` to clear residual trait state.
