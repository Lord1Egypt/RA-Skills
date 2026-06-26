---
name: model-config
version: 1.0.0
description: "Configure and troubleshoot OpenClaw model providers, routing, session model locks, cron model pinning, and provider switching. Lessons from real failures."
allowed-tools: [cron, exec, read, session_status]
---

# Model Configuration

Everything about configuring models in OpenClaw — providers, routing, sessions, and cron pinning. Learned the hard way through many errors.

## Provider setup

### Adding a provider

Edit `openclaw.json`:

```json
{
  "providers": {
    "deepseek": {
      "apiKey": "sk-...",
      "baseUrl": "https://api.deepseek.com"
    }
  }
}
```

If using API key from file: reference env var or key file. Direct env var injection via `~/.openclaw/openclaw.json`.

**Never restart gateway and immediately assume the model is live.** Check after restart.

### Checking what model is active

```bash
openclaw status           # shows current model
session_status            # shows session-level model
```

### Provider priority

If multiple providers offer the same model, Gateway resolves via: plugin providers > config providers > default fallback chain. A DeepSeek plugin can sit alongside a MiniMax config provider — the plugin wins if enabled.

## The session model lock (most common mistake)

**The trap:** When you change the default model in config, the *current Telegram session* stays locked to its **birth model** — the model that was default when the session was created.

```
Session created at 18:05 → model = MiniMax (was default)
Gateway restarted at 18:06 → config now says DeepSeek
Session at 18:07 → STILL MiniMax ← TRAP
New session created at 18:08 → DeepSeek ← Correct
```

**The fix:**
- Existing sessions keep their model until the session expires or is reset
- `/model <provider/model>` — force-switches the current session immediately
- For Telegram: sending a message to a brand new session (or after session expiry) picks up the current default
- Closing and reopening a Telegram chat does NOT reset the session (Telegram chats can't be "closed")

**Lesson:** After changing model config, either:
1. Send `/model deepseek/deepseek-v4-flash` to switch running session
2. Wait for session to expire naturally (~24h inactivity)
3. Accept that cron sessions (always new) will use new config immediately

## Cron model pinning (second most common mistake)

**Time-sensitive cron jobs MUST pin the model explicitly.** The global default can get stuck on model cold-start resolution (MiniMax especially bad — up to 300s delay).

```json
{
  "payload": {
    "kind": "agentTurn",
    "message": "...",
    "timeoutSeconds": 600,
    "model": "deepseek/deepseek-v4-flash"
  }
}
```

**Crons that ALWAYS need pinning:**

| Cron | Why |
|------|-----|
| Expense check-ins (10am, 1:30pm, 10pm) | Time-sensitive, Hobo waits for them |
| Expense sync (9:30am) | Must run on schedule |
| News briefings (7:30am, 3pm, 10pm) | Hobo expects them on time |
| Investment check-in (Sat 10am) | Weekly, must fire |
| Investment sync (Sat 11am) | Same |
| Transport check-in (9am) | Previous-day ask |

**Crons that don't need pinning:**
- Dashboard regeneration, token tracker, backup, security audit — delay is harmless

**Failure symptom:** `lastDiagnostics.summary = "cron: job execution timed out (last phase: model-call-started)"`. Fix: pin model.

## dmScope (multi-agent routing)

In multi-agent setups (Patch + Muthu), messages can route to the wrong agent's session unless `dmScope` is set correctly:

```json
{
  "telegram": {
    "dmScope": "per-channel-peer-account"
  }
}
```

**per-channel-peer-account** — each Telegram bot + user combo gets its own session. Without this, messages from both bots could land in the same session.

**Symptom of wrong dmScope:** Hobo messages Patch but Muthu's session receives them, or vice versa.

## Plugins vs config providers

- **Plugins** (installed via ClawHub or `openclaw`): can introduce new model providers
- **Config providers** (in `openclaw.json`): directly configured API endpoints
- Both can coexist. Plugin providers take priority over config providers for same model.

**To check loaded providers:**

```bash
openclaw plugin list | grep -i model
grep -A5 '"providers"' ~/.openclaw/openclaw.json
```

## Model switching during session

| Method | Scope | Persistence |
|--------|-------|-------------|
| `/model deepseek/deepseek-v4-flash` | Current session only | Until session expires |
| Change `"model" in openclaw.json` | All new sessions | Permanent (requires gateway restart) |
| Pin `"model" in cron payload` | That cron only | Permanent until changed |

## Safety checklist (when changing models)

1. Edit `openclaw.json` → add/change provider + model
2. Restart gateway: `openclaw gateway restart`
3. CHECK: `openclaw status` — confirms the new model is live
4. CHECK: Send a test message — verify which model responds
5. If wrong model responds → `/model <correct/provider/model>`
6. Update cron pinning for any time-sensitive crons
7. Verify cron test runs pick up the new model (check lastRunStatus)
