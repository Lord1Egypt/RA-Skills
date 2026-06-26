---
name: openclaw-output-metrics-footer
description: Install, configure, maintain, or troubleshoot a compact OpenClaw output footer that shows live context usage, output tokens, Codex quota remaining, model used, and optional subagent token aggregate under text responses across Discord, Telegram, Slack, WhatsApp, Signal, Matrix, Mattermost, and other supported providers.
---

# OpenClaw Output Metrics Footer

Use this skill when an OpenClaw workspace should show compact runtime metrics under text channel outputs.

Default footer:

```text
_🟢 ↑54k ↓157 · 21%ctx · 5h 89% · kimi-k2.6:cloud_
```

With subagent aggregate:

```text
_🟢 ↑54k ↓157 · 21%ctx · 5h 89% · openai-codex/gpt-5.5 · sub ↑31k ↓4k_
```

## What it does

- Adds a provider-agnostic channel delivery-time footer using OpenClaw plugin hooks.
- Uses `llm_output` for actual model/token metrics.
- Uses `message_sending` to append the footer without adding prompt tokens.
- Uses live/cached OpenAI Codex OAuth usage for `5h 89%` when available.
- Uses color status from context usage and quota remaining.
- Optionally aggregates nearby subagent LLM usage.

## Install into an OpenClaw workspace

Copy the bundled extension template:

```bash
mkdir -p ~/.openclaw/extensions/openclaw-output-metrics-footer
cp -R assets/extension-template/* ~/.openclaw/extensions/openclaw-output-metrics-footer/
```

Add this plugin config to `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "allow": ["openclaw-output-metrics-footer"],
    "load": {
      "paths": ["~/.openclaw/extensions/openclaw-output-metrics-footer"]
    },
    "entries": {
      "openclaw-output-metrics-footer": {
        "enabled": true,
        "hooks": {
          "allowConversationAccess": true
        },
        "config": {
          "enabledChannels": [],
          "cacheMs": 120000,
          "quotaCacheMs": 60000,
          "contextReserveTokens": 40000,
          "appendSubagents": true,
          "disabledChannels": [],
          "disabledConversations": []
        }
      }
    }
  }
}
```

Then validate and restart:

```bash
openclaw config validate
openclaw gateway restart
```

## Channel deployment

The plugin can run for any OpenClaw text channel that emits `message_sending`.

Use `enabledChannels` to restrict to specific providers, such as `['discord', 'telegram']`. Leave it empty to enable all text providers.

Use `disabledChannels` to disable whole providers.

Use `disabledConversations` to disable specific channel/chat/conversation IDs.

Recommended defaults:

- Enable in active work channels like `#general`, `#coding`, `#reasoning`, Telegram work chats, and audit channels.
- Disable in status-only channels like `#feed` and incident channels like `#system` if noise matters.

## Configuration

Fields:

- `enabledChannels`: optional provider allowlist. Empty means all supported text channels.
- `cacheMs`: window for matching recent LLM output and subagent output.
- `quotaCacheMs`: minimum interval between Codex quota refreshes.
- `contextReserveTokens`: safety reserve included in context percentage calculations.
- `appendSubagents`: append `sub ↑x ↓y` when nearby subagent usage is detected.
- `disabledChannels`: provider IDs where no footer should be appended.
- `disabledConversations`: channel/chat/conversation IDs where no footer should be appended.

## Color status

- `🟢`: context under 50% and quota over 50%.
- `🟡`: context 50-80% or quota 20-50%.
- `🔴`: context over 80% or quota under 20%.

If context and quota disagree, show the worse status.

## Guardrails

- Do not put footer instructions in agent prompts.
- Do not call an LLM to calculate footer metrics.
- Do not fetch Codex quota on every message; use cache.
- Do not show emails, OAuth profile names, token values, API key prefixes, or auth file paths.
- Do not add the footer when it would exceed the channel message limit.

Read `references/implementation.md` before changing the extension code.
