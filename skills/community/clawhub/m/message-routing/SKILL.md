---
name: claude-code-switchboard
slug: message-routing
version: 1.2.0
description: "Manage how OpenClaw routes Telegram messages to different Claude model backends. Switch between CLI and API providers with simple config changes."
command: /telegram-routing
---

# /telegram-routing — Telegram Message Routing Manager

Manage how Telegram messages are routed between different Claude model backends in OpenClaw.

## Usage

```
/telegram-routing status       # Show current routing config
/telegram-routing model <ref>  # Switch primary model (e.g. opus, sonnet, haiku)
/telegram-routing logs         # Show recent message processing logs
/telegram-routing fallback     # Switch to lightweight API mode
/telegram-routing restore      # Restore default CLI-based routing
```

## Config Location

All settings live in `~/.openclaw/openclaw.json` under `agents.defaults`.

### Key fields:
- `model.primary` — The primary model/provider reference
- `model.fallbacks` — Ordered fallback chain when primary is unavailable

## Commands

### status

Read the OpenClaw config and display current routing settings including:
- Active primary model
- Configured fallback models
- Whether CLI backend is active

### model <ref>

Switch the primary model. Valid shorthand references:

| Shorthand | Resolves to |
|-----------|-------------|
| `opus` | `claude-cli/opus` |
| `sonnet` | `claude-cli/sonnet` |
| `haiku` | `anthropic/claude-haiku-4-5` |

Steps:
1. Read `~/.openclaw/openclaw.json`
2. Update `agents.defaults.model.primary` to the resolved model reference
3. Write the updated config
4. Restart the gateway service
5. Verify via gateway logs

### logs

Show recent Telegram message processing activity from the gateway log.

### fallback

Quick switch to API-only mode for faster, lightweight responses.

### restore

Restore the default CLI-based routing configuration.

## Architecture

Messages flow through the OpenClaw Gateway, which reads the configured model provider and dispatches to the appropriate backend. CLI-based providers use the local Claude Code installation, while API providers make direct API calls.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Config errors on restart | Run `openclaw doctor` to validate config |
| Slow responses | Try switching to `sonnet` for faster responses |
| Gateway issues | Check `~/.openclaw/logs/gateway.log` for details |
| Falling back to secondary model | Primary backend may be unavailable — check logs |
