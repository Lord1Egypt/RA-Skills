# Low-Spec Configuration Guide

## Recommended OpenClaw config for machines with ≤4GB RAM

### Model selection

Use **free/lightweight models** to avoid API costs and latency:

```json
{
  "agents": {
    "defaults": {
      "model": "openrouter/hunter-alpha"
    }
  }
}
```

**Good free/cheap models:**
- `openrouter/hunter-alpha` — decent quality, free tier
- `z-ai/glm-4.5-air` — free, good for research
- `nvidia/z-ai/glm4.7` — free via NVIDIA API

### Thinking level

Set to `"off"` unless doing complex reasoning:
```json
{ "agents": { "thinking": "off" } }
```

### Subagent limits

Avoid spawning more than 2 subagents simultaneously:
- Each subagent session uses ~100-200MB RAM
- `mode: "run"` is lighter than `mode: "session"` (auto-cleans)

### Heartbeat tuning

Reduce heartbeat frequency to save cycles:
```json
{ "heartbeat": { "intervalMs": 1800000 } }
```

### Browser usage

- **Always close browser** after use (`browser(action="close")`)
- Use `web_fetch` instead of browser when possible (10x lighter)
- One browser at a time, never parallel

### Cron job strategy

Use `sessionTarget: "isolated"` with `agentTurn` for lightweight scheduled tasks.
Avoid scheduling multiple cron jobs at the same time.

## Resource thresholds

| State | RAM % | Action |
|-------|-------|--------|
| OK | < 60% | Normal operation |
| ELEVATED | 60-75% | Avoid spawning subagents |
| WARNING | 75-90% | Close browser, cleanup sessions |
| CRITICAL | > 90% | Emergency cleanup, alert user |

## Process management

**Killable processes** (safe to close if consuming RAM):
- Old browser instances (Playwright/Chromium)
- Stale subagent sessions
- Package manager caches (npm, pip)
- System journal logs (>3 days old)

**Never kill:**
- OpenClaw gateway process
- User's own browser/apps
- SSH sessions
- Systemd essentials
