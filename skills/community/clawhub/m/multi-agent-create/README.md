# Multi-Agent Create

> **⚡ One-line install:**
> ```bash
> clawhub install multi-agent-create
> ```

Create a new OpenClaw agent and connect it to any messaging channel — with an interactive guided workflow.

## Supported Channels

| Channel | Credentials Needed |
|---------|-------------------|
| **Telegram** | Bot Token (from [@BotFather](https://t.me/BotFather)) |
| **Discord** | Bot Token (from [Developer Portal](https://discord.com/developers/applications)) |
| **Slack** | App Token + Bot Token (from [Slack API](https://api.slack.com/apps)) |
| **Feishu / Lark** | App ID + App Secret (from [飞书开放平台](https://open.feishu.cn/)) |
| **WhatsApp** | QR code scan |
| **Signal** | QR code scan |
| **Google Chat** | Service Account JSON |

## How It Works

Just tell your agent:
> "Create a new agent" / "Add a bot"

The skill guides you step by step:

1. 🤖 **Pick a name & channel** — Choose from 7 supported platforms
2. 🔑 **Get credentials** — Platform-specific instructions (where to go, what to click)
3. 📁 **Workspace created** — Identity, personality, and memory files auto-generated
4. ⚙️ **Registered & configured** — Gateway config updated automatically
5. ✅ **Verify & go live** — Restart, pair, done!

No extra API keys needed — all agents share your existing model credentials.

## Manual Setup

You can also use the helper script directly:

```bash
./scripts/setup-agent.sh luna telegram
```

## Tags

`create-agent` · `new-agent` · `multi-agent` · `add-agent` · `bot-setup` · `telegram` · `discord` · `slack` · `feishu` · `whatsapp` · `signal`

## License

MIT-0
