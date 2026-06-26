# NeverDie

LLM resilience for OpenClaw. Ensures your instance survives model failures with provider-diverse fallback chains, standalone monitoring, and Telegram alerts.

## Why

OpenClaw's default fallback config often has all models from the same provider. When that provider goes down, everything goes down. The built-in health checks require a working LLM to detect LLM failures — a catch-22. NeverDie fixes both problems.

## Install

```bash
clawhub install neverdie
```

Then tell OpenClaw: **"set up NeverDie"**

## What It Does

1. **Provider-diverse fallback chains** — ensures your model config alternates providers (Anthropic, OpenAI, Ollama, etc.) so a single provider outage doesn't take you down
2. **Standalone monitor** — a zero-dependency Node.js script that scans gateway error logs every 5 minutes via `systemEvent` cron — works even when ALL LLMs are down
3. **Telegram alerts** — immediate notification on failures, with 15-minute cooldown to prevent spam (optional — file-only alerts work without Telegram)
4. **Ollama safety net** — always includes a local model as the last resort

## Prerequisites

- **Node.js** (any recent version)
- **Ollama** (recommended) — `brew install ollama && ollama pull llama3.2:3b`
- **Telegram bot** (optional) — message `@BotFather` on Telegram to create one

## What It Detects

| Pattern | Severity | Meaning |
|---------|----------|---------|
| All models failed | CRITICAL | No LLM available |
| Service overloaded | WARNING | Provider overloaded, using fallbacks |
| Rate limited / 429 | WARNING | Rate limited, using fallbacks |
| Auth error | CRITICAL | Bad API key |
| LLM timeout | WARNING | Request timed out |
| Connection refused | WARNING | Provider unreachable |

## Manual Setup (without the agent)

```bash
# Full setup with Telegram alerts
bash ~/.openclaw/workspace/skills/neverdie/scripts/setup.sh \
  --telegram-token YOUR_BOT_TOKEN \
  --chat-id YOUR_CHAT_ID \
  --hostname my-openclaw \
  --timezone America/New_York

# File-only alerts (no Telegram)
bash ~/.openclaw/workspace/skills/neverdie/scripts/setup.sh

# Uninstall
bash ~/.openclaw/workspace/skills/neverdie/scripts/setup.sh --uninstall
```

## CLI

```bash
node ~/.openclaw/workspace/fallback-monitor.js           # Scan logs, send alerts
node ~/.openclaw/workspace/fallback-monitor.js --test     # Send test alert
node ~/.openclaw/workspace/fallback-monitor.js --status   # Show monitor state
node ~/.openclaw/workspace/fallback-monitor.js --version  # Print version
```

## Architecture

```
systemEvent cron (every 5 min)
  └→ fallback-monitor.js
       ├── reads gateway.err.log (incremental, position-tracked)
       ├── matches 6 failure patterns
       ├── applies 15-min cooldown per alert type
       ├── writes .fallback-alert-latest.json (session pickup)
       ├── sends Telegram alert (if configured)
       └── prints to stdout (visible in session)
```

No LLM involvement at any point. Pure Node.js builtins (`fs`, `path`, `https`).

## Config

Stored at `~/.openclaw/workspace/.neverdie-config.json`:

```json
{
  "telegramBotToken": "",
  "telegramChatId": "",
  "cooldownMinutes": 15,
  "timezone": "UTC",
  "hostname": "my-openclaw"
}
```

Falls back to environment variables: `NEVERDIE_TELEGRAM_TOKEN`, `NEVERDIE_TELEGRAM_CHAT_ID`.

## Security

- **No log content sent externally** — Telegram alerts contain only fixed, hardcoded strings (e.g. "All models failed"). Log details stay in the local alert file on your machine, never transmitted
- **No secrets in skill files** — Telegram credentials are stored in your local config at runtime, never in the published skill
- **Config isolation** — only reads model IDs from `openclaw.json`, never API keys or credentials
- **Telegram is optional** — works in file-only mode with zero external network calls
- **No dependencies** — no npm packages, no remote downloads, only Node.js builtins
- **Single outbound endpoint** — only contacts `api.telegram.org`, and only when you explicitly configure it
