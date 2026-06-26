# OpenClaw Output Metrics Footer

Compact runtime telemetry for OpenClaw channel responses.

This skill installs an OpenClaw extension that appends a one-line footer under text outputs for OpenClaw channels such as Discord, Telegram, Slack, WhatsApp, Signal, Matrix, Mattermost, and other providers that pass through OpenClaw's `message_sending` hook.

```text
_🟢 ↑54k ↓157 · 21%ctx · 5h 89% · kimi-k2.6:cloud_
```

With subagents:

```text
_🟢 ↑54k ↓157 · 21%ctx · 5h 89% · openai-codex/gpt-5.5 · sub ↑31k ↓4k_
```

## What it shows

- `↑54k`: input/context tokens used for the turn.
- `↓157`: assistant output tokens for the turn.
- `21%ctx`: current context window usage, including configured reserve.
- `5h 89%`: live/cached OpenAI Codex short-window quota remaining.
- `kimi-k2.6:cloud`: model used for the turn.
- `sub ↑31k ↓4k`: optional best-effort aggregate of nearby subagent usage.

## Supported channels

Supported in principle for OpenClaw text providers that emit `message_sending`:

- Discord
- Telegram
- Slack
- WhatsApp
- Signal
- Matrix
- Mattermost
- Google Chat
- Microsoft Teams
- IRC
- Other OpenClaw text providers using the shared delivery runtime

Media-only messages are ignored. Rich cards or embeds may fall back to text behavior depending on provider support.

## Color status

- `🟢`: context under 50% and quota over 50%.
- `🟡`: context 50-80% or quota 20-50%.
- `🔴`: context over 80% or quota under 20%.

If context and quota disagree, the footer shows the worse status.

## Install

Install this skill into your OpenClaw workspace, then copy the bundled extension template:

```bash
mkdir -p ~/.openclaw/extensions/openclaw-output-metrics-footer
cp -R assets/extension-template/* ~/.openclaw/extensions/openclaw-output-metrics-footer/
```

Add the plugin to `~/.openclaw/openclaw.json`:

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

Validate and restart:

```bash
openclaw config validate
openclaw gateway restart
```

## Channel deployment

Leave `enabledChannels` empty to enable all supported text channels.

Restrict to specific providers:

```json
{
  "enabledChannels": ["discord", "telegram"]
}
```

Disable whole providers:

```json
{
  "disabledChannels": ["email"]
}
```

Disable specific channel/chat/conversation IDs:

```json
{
  "disabledConversations": ["1496200429644681386"]
}
```

Recommended:

- Enable in work channels such as `#general`, `#coding`, `#reasoning`, Telegram work chats, and audit channels.
- Disable in status-only or incident channels such as `#feed` and `#system` if you want less noise.

## Configuration

| Field | Default | Purpose |
| --- | --- | --- |
| `enabledChannels` | `[]` | Optional allowlist of channel providers. Empty means all text channels. |
| `cacheMs` | `120000` | Window for matching recent LLM output and subagent output. |
| `quotaCacheMs` | `60000` | Minimum interval between Codex quota refreshes. |
| `contextReserveTokens` | `40000` | Safety reserve included in context usage percentage. |
| `appendSubagents` | `true` | Append `sub ↑x ↓y` when nearby subagent usage is detected. |
| `disabledChannels` | `[]` | Channel providers where no footer should be appended. |
| `disabledConversations` | `[]` | Channel/chat/conversation IDs where no footer should be appended. |

## Privacy

The extension must never print:

- OAuth tokens.
- API keys.
- Email addresses.
- Auth profile names.
- Local auth file paths.

If Codex quota cannot be fetched, the footer omits the quota field rather than blocking delivery.

## Files

```text
openclaw-output-metrics-footer/
├── SKILL.md
├── README.md
├── assets/
│   └── extension-template/
│       ├── index.ts
│       ├── openclaw.plugin.json
│       └── package.json
└── references/
    └── implementation.md
```

## Publish to ClawHub

```bash
clawhub publish . --slug openclaw-output-metrics-footer --name "OpenClaw Output Metrics Footer" --version 0.2.1 --changelog "Parse current Codex quota usage windows"
```

## License

MIT
