# Telegram Bot Setup Guide

Complete guide to set up Telegram integration with OpenClaw.

## Step 1: Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Follow the prompts:
   - Enter bot name (e.g., "My AI Assistant")
   - Enter bot username (must end with `bot`, e.g., "myai_assistant_bot")
4. BotFather will respond with your **Bot Token**

Example response:
```
Done! Congratulations on your new bot...
Use this token to access the HTTP API:
7123456789:AAHxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Keep your token secure...
```

## Step 2: Configure OpenClaw

### Method A: Using CLI

```bash
# Set bot token
openclaw credentials set telegram 7123456789:AAHxxxxxxxx

# Enable Telegram channel
openclaw config set telegram.enabled true
openclaw config set telegram.dmPolicy "open"
```

### Method B: Edit Config File

Edit `~/.openclaw/openclaw.json`:

```json5
{
  telegram: {
    enabled: true,
    botToken: "${TELEGRAM_BOT_TOKEN}",
    dmPolicy: "open",
    streaming: "partial",
    allowFrom: ["*"]
  }
}
```

Then set the credential:

```bash
openclaw credentials set telegram 7123456789:AAHxxxxxxxx
```

## Step 3: Restart Gateway

```bash
# Stop existing gateway
killall openclaw openclaw-gateway 2>/dev/null

# Start gateway
openclaw gateway
```

## Step 4: Test the Bot

1. Open Telegram
2. Find your bot (search by username)
3. Send a message like "Hello"
4. The bot should respond

## Security Configuration

### Open Mode (Public Bot)

Anyone can message the bot:

```json5
{
  telegram: {
    dmPolicy: "open",
    allowFrom: ["*"]
  }
}
```

### Pairing Mode (Private Bot)

Requires approval for new users:

```json5
{
  telegram: {
    dmPolicy: "pairing"
  }
}
```

When someone messages the bot, they receive a pairing code. To approve:

```bash
openclaw pairing approve telegram <code>
```

### Allowlist Mode

Only specific users can message:

```json5
{
  telegram: {
    dmPolicy: "open",
    allowFrom: ["+1234567890", "+0987654321"]
  }
}
```

## Group Chat Configuration

### Require Mention

Bot only responds when mentioned:

```json5
{
  telegram: {
    groups: {
      "*": {
        requireMention: true,
        activation: "mention"
      }
    }
  }
}
```

### Always Active

Bot responds to all messages:

```json5
{
  telegram: {
    groups: {
      "*": {
        requireMention: false,
        activation: "always"
      }
    }
  }
}
```

### Reply Tracking

Bot tracks replies to its messages:

```json5
{
  telegram: {
    groups: {
      "*": {
        activation: "reply"
      }
    }
  }
}
```

## Streaming Configuration

| Mode | Description |
|------|-------------|
| `none` | Send complete response only |
| `partial` | Stream partial responses (recommended) |
| `full` | Stream every token |

```json5
{
  telegram: {
    streaming: "partial"
  }
}
```

## Troubleshooting

### Bot Not Responding

1. Check gateway is running:
```bash
ps aux | grep openclaw | grep -v grep
```

2. Check bot token is correct:
```bash
openclaw credentials get telegram
```

3. Check logs:
```bash
tail -f ~/.openclaw/logs/gateway.log
```

### Rate Limiting

Telegram has rate limits. If experiencing issues:

```json5
{
  telegram: {
    rateLimit: {
      enabled: true,
      messagesPerSecond: 1
    }
  }
}
```

### Webhook vs Polling

OpenClaw uses long polling by default. For webhook mode:

```json5
{
  telegram: {
    webhook: {
      enabled: true,
      url: "https://your-domain.com/telegram/webhook"
    }
  }
}
```
