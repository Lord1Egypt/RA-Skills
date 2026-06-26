# New Agent

Create a new OpenClaw agent and connect it to any messaging channel.

## Supported Channels

| Channel | Credentials Needed |
|---------|-------------------|
| Telegram | Bot Token (from @BotFather) |
| Discord | Bot Token (from Developer Portal) |
| Slack | App Token + Bot Token |
| Feishu / Lark | App ID + App Secret |
| WhatsApp | QR code scan |
| Signal | QR code scan |
| Google Chat | Service Account JSON |

## Quick Start

```bash
clawhub install new-agent
```

Or clone from GitHub:
```bash
git clone https://github.com/joansongjr/new-agent.git
```

## Usage

Tell your OpenClaw agent:
> "Create a new agent called Luna, here's the Telegram token: 123456:ABC..."

The skill guides the agent through:
1. Creating a dedicated workspace with identity files
2. Registering the agent in your gateway config
3. Connecting the messaging channel
4. Verifying the setup

## Manual Setup

You can also use the helper script directly:
```bash
./scripts/setup-agent.sh luna telegram
```

## License

MIT-0
