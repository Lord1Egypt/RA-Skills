---
name: lm-studio-discord
description: Connect a local LM Studio model directly to Discord as a lightweight chat bot. Use when you want to expose a local LLM (running via LM Studio on CPU) to Discord without OpenClaw's overhead. Bypasses the main OpenClaw gateway for speed on CPU-only machines.
---

# LM Studio Discord Bot

A minimal Discord bot that routes messages directly to LM Studio — no OpenClaw gateway in the path.

## When to Use

- LM Studio model is fast in direct chat but slow through OpenClaw
- CPU-only setup where OpenClaw's tool system adds too much latency
- You want a simple Discord bot without the full OpenClaw feature set

## How It Works

```
Discord → bot.js → LM Studio API → bot.js → Discord
```

The bot uses Discord.js to receive messages and axios to call LM Studio's `/v1/chat/completions` endpoint directly. No tools, no workspace files, no system prompt overhead.

## Setup

### 1. Create the bot project

```bash
mkdir lm-studio-discord-bot
cd lm-studio-discord-bot
npm init -y
npm install discord.js axios
```

### 2. Create bot.js

See `scripts/bot-template.js` for the ready-to-use template.

### 3. Configure

Edit these constants in `bot.js`:

```javascript
const DISCORD_TOKEN = 'YOUR_DISCORD_BOT_TOKEN';
const LM_STUDIO_URL = 'http://127.0.0.1:1234/v1/chat/completions';
const MODEL = 'qwen2-0.5b-instruct';  // Must match loaded model in LM Studio
const GUILD_ID = 'YOUR_DISCORD_SERVER_ID';
```

To get your bot token: https://discord.com/developers/applications

To get the Guild ID: Enable Developer Mode in Discord → Right-click your server → Copy ID

### 4. Add bot to your server

```
https://discord.com/oauth2/authorize?client_id=BOT_CLIENT_ID&permissions=1024&scope=bot
```

Replace `BOT_CLIENT_ID` with your bot's Application ID from the Discord Developer Portal.

### 5. Run

```bash
node bot.js
```

The bot will log in and respond to messages in any channel of the configured guild.

## Configuration Tips

| Parameter | Default | Notes |
|-----------|---------|-------|
| `max_tokens` | 512 | Lower = faster, less verbose |
| `timeout` | 60000ms | Increase if slow on CPU |
| `stream` | `false` | Set `true` for streaming replies |

## Known Limitations

- No tool access (file read/write, web search, etc.)
- No conversation memory — each message is stateless
- No slash commands
- Single model per bot instance

## Extending

To add conversation history, modify the `messages` array in the axios call to include prior exchanges. Note: this increases token usage and context window pressure.
