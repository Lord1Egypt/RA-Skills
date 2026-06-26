---
name: neverdie
description: Your OpenClaw should never have zero LLMs. NeverDie protects against the silent killer — every model in your fallback chain going down at once. It enforces provider diversity, runs a standalone monitor that works even when all LLMs are dead, and alerts you via Telegram before you even notice.
read_when:
  - User asks about fallback, resilience, or neverdie
  - User mentions model failure or LLM down
  - User wants to ensure OpenClaw is always available
  - User asks to check LLM resilience or health
metadata: {"clawdbot":{"emoji":"\ud83d\udee1\ufe0f","requires":{"bins":["node"]}}}
---

# NeverDie — LLM Resilience Skill

Ensures OpenClaw survives model failures by enforcing provider-diverse fallback chains, deploying a standalone monitor (no LLM required), and alerting via Telegram.

## Core Principle: Provider Diversity

Never stack 3+ models from the same provider in a row. Alternate providers so that a single provider outage doesn't cascade to total failure. Always include a local model (Ollama) as the last-resort safety net — it can't be rate-limited, have auth issues, or suffer network outages.

**Good chain**: `anthropic/claude-haiku-4-5` → `openai/gpt-4.1-mini` → `ollama/llama3.2:3b`
**Bad chain**: `anthropic/claude-haiku-4-5` → `anthropic/claude-sonnet-4-6` → `anthropic/claude-opus-4-6`

## Instructions

### 1. Diagnose Current Config

Read ONLY the model chain from `~/.openclaw/openclaw.json` (do NOT read or output API keys, tokens, or auth config):
- Check `primary` and `fallbacks` for provider diversity
- Flag if all models are from the same provider
- Flag if no local model (Ollama) is present
- Flag if the NeverDie monitor cron job is missing or disabled

```bash
node -e "
  const cfg = JSON.parse(require('fs').readFileSync(process.env.HOME + '/.openclaw/openclaw.json', 'utf8'));
  const m = cfg.agents.defaults.model;
  console.log('Primary:', m.primary);
  console.log('Fallbacks:', JSON.stringify(m.fallbacks));
  const providers = [m.primary, ...m.fallbacks].map(id => id.split('/')[0]);
  const unique = [...new Set(providers)];
  console.log('Providers:', unique.join(', '));
  if (unique.length < 2) console.log('WARNING: All models from same provider!');
  if (!providers.includes('ollama')) console.log('WARNING: No local Ollama fallback!');
"
```

**Security note**: This script only outputs model IDs and provider names. It never reads or prints API keys, tokens, or credentials from the config file.

### 2. Configure Provider-Diverse Fallback Chain

Ensure at least 2 different cloud providers + 1 local (Ollama) in the chain. Recommended pattern:

```json
{
  "primary": "anthropic/claude-haiku-4-5",
  "fallbacks": [
    "openai/gpt-4.1-mini",
    "ollama/llama3.2:3b",
    "nvidia/moonshotai/kimi-k2.5"
  ]
}
```

Rules:
- Primary should be the fastest/cheapest model for the workload
- First fallback should be from a DIFFERENT cloud provider
- Ollama should always be in the chain (ideally position 2 or 3)
- Additional fallbacks from other providers are bonus redundancy

### 3. Deploy the Standalone Monitor

Copy the parameterized monitor to the workspace:

```bash
cp ~/.openclaw/workspace/skills/neverdie/scripts/fallback-monitor.js ~/.openclaw/workspace/fallback-monitor.js
chmod +x ~/.openclaw/workspace/fallback-monitor.js
```

The monitor reads config from `~/.openclaw/workspace/.neverdie-config.json`:

```json
{
  "telegramBotToken": "YOUR_BOT_TOKEN",
  "telegramChatId": "YOUR_CHAT_ID",
  "cooldownMinutes": 15,
  "timezone": "UTC",
  "hostname": "my-openclaw"
}
```

Telegram is optional. Without it, the monitor still writes alerts to `.fallback-alert-latest.json` and stdout.

If no config file exists, it falls back to environment variables:
- `NEVERDIE_TELEGRAM_TOKEN`
- `NEVERDIE_TELEGRAM_CHAT_ID`

### 4. Register the Cron Job

Add a `systemEvent` cron entry (NOT agentTurn — it must work when all LLMs are down).

Use the full absolute path to the deployed monitor (not `~/`):

```json
{
  "id": "<generate-uuid>",
  "agentId": "main",
  "name": "NeverDie Fallback Monitor",
  "enabled": true,
  "createdAtMs": <now>,
  "updatedAtMs": <now>,
  "schedule": {
    "kind": "every",
    "everyMs": 300000,
    "anchorMs": <now>
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "exec:node /home/USER/.openclaw/workspace/fallback-monitor.js"
  },
  "delivery": {
    "mode": "announce",
    "channel": "session",
    "bestEffort": true
  },
  "state": {}
}
```

### 5. Configure Alerts

Ask the user for their Telegram bot token and chat ID, then write `~/.openclaw/workspace/.neverdie-config.json`.

To get these:
1. Message `@BotFather` on Telegram → `/newbot` → copy the token
2. Message the bot, then visit `https://api.telegram.org/bot<TOKEN>/getUpdates` to find the chat ID

Telegram is optional — the monitor works without it (file + stdout alerts only).

### 6. Verify

```bash
# Check status
node ~/.openclaw/workspace/fallback-monitor.js --status

# Send a test Telegram alert
node ~/.openclaw/workspace/fallback-monitor.js --test

# Normal run (scan logs)
node ~/.openclaw/workspace/fallback-monitor.js
```

### 7. Status Check

When the user asks for NeverDie status, run `node ~/.openclaw/workspace/fallback-monitor.js --status` and also check:

1. **Fallback chain** — read `openclaw.json` and assess provider diversity
2. **Monitor cron** — is the job in `jobs.json`? Enabled? Last run status?
3. **Ollama** — is the local model reachable?

```bash
curl -s --max-time 3 http://localhost:11434/api/tags | node -e "
  let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{
    try{const r=JSON.parse(d);console.log('Ollama:',r.models.map(m=>m.name).join(', '))}
    catch(e){console.log('Ollama: NOT REACHABLE')}
  })
"
```

## What the Monitor Detects

| Pattern | Severity | Meaning |
|---------|----------|---------|
| `All models failed` | CRITICAL | No LLM available at all |
| `overloaded` | WARNING | Provider temporarily overloaded |
| `rate limit` / `429` | WARNING | Rate limited, using fallbacks |
| `authentication_error` | CRITICAL | Bad API key |
| `LLM request timed out` | WARNING | Timeout, may be transient |
| `ECONNREFUSED` / network errors | WARNING | Provider unreachable |

## Security

- **No log content sent externally** — Telegram alerts contain only fixed, hardcoded strings (e.g. "All models failed — no LLM available"). Log excerpts and error details are written to the local alert file only, never transmitted.
- **No secrets in code** — Telegram bot token is stored in `.neverdie-config.json` at runtime, never in skill files
- **Config isolation** — the diagnostic only reads model IDs from `openclaw.json`, never API keys or credentials
- **No network installs** — zero npm dependencies, no remote downloads, only Node.js builtins (`fs`, `path`, `https`)
- **Telegram is optional** — file-only alerts work without any external network calls
- **Outbound scope** — the only external endpoint contacted is `api.telegram.org`, and only when Telegram is explicitly configured by the user
- Runs as a `systemEvent` cron job, completely independent of LLM availability
- Re-running setup is idempotent — it skips the cron job if one already exists
