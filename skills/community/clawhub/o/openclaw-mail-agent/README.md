# mail-agent — OpenClaw Plugin

AI-powered Gmail monitor for [OpenClaw](https://openclaw.ai). Watches your inbox via Google Pub/Sub, classifies emails with an LLM, and pushes important ones to Telegram.

No separate server. Runs entirely inside OpenClaw.

## Requirements

- [OpenClaw](https://openclaw.ai) with Telegram configured
- [gog](https://gogcli.sh) — Gmail CLI, authenticated
- Google Cloud project with Gmail API + Pub/Sub enabled
- OpenAI (or compatible) API key

## Quick start

Install the `mail-agent` skill in OpenClaw — it will walk you through the full setup step by step.

Or manually:

```bash
openclaw plugins install https://github.com/nanaco666/openclaw-mail-agent/archive/refs/tags/v0.2.1.tar.gz

openclaw plugins config mail-agent --set chatId=YOUR_TELEGRAM_CHAT_ID
openclaw plugins config mail-agent --set gcpProject=YOUR_GCP_PROJECT_ID
openclaw plugins config mail-agent --set pubsubSubscription=mail-agent-inbox-sub
openclaw plugins config mail-agent --set llmApiKey=sk-...

openclaw gateway restart
```

## How it works

```
Gmail → Google Pub/Sub → plugin (inside OpenClaw)
                               ↓
                       Gmail history.list
                               ↓
                        LLM classification
                               ↓
                   Telegram (via OpenClaw bot)
```

Gmail push notifications via Pub/Sub → plugin gets notified instantly → fetches the email → LLM decides important or not → sends to Telegram if important.

## Configuration

| Key | Required | Default | Description |
|-----|----------|---------|-------------|
| `chatId` | ✓ | — | Telegram chat/group ID |
| `gcpProject` | ✓ | — | Google Cloud project ID |
| `pubsubSubscription` | ✓ | `mail-agent-inbox-sub` | Pub/Sub subscription name |
| `llmApiKey` | — | — | OpenAI API key (skips classification if unset) |
| `llmBaseUrl` | — | `https://api.openai.com/v1` | LLM endpoint |
| `llmModel` | — | `gpt-4o-mini` | Classification model |
| `credentialsPath` | — | — | Path to Google credentials JSON |

## License

MIT
