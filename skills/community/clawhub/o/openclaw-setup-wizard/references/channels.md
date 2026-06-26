# Channel Connection Reference

## Telegram (Recommended for beginners)

1. Message @BotFather on Telegram → `/newbot`
2. Copy the bot token
3. Message @userinfobot → get your numeric user ID
4. Configure:
```bash
openclaw configure --section channels
# Select: telegram
# Token: paste bot token
# AllowFrom: your user ID
```
5. Restart gateway: `openclaw gateway restart`
6. Message your bot on Telegram

## Discord

1. Go to https://discord.com/developers/applications
2. New Application → Bot tab → Create Bot → Copy token
3. Enable MESSAGE CONTENT INTENT under Privileged Gateway Intents
4. Generate invite URL: Bot tab → OAuth2 URL Generator → Select `bot` scope
5. Configure:
```bash
openclaw configure --section channels
# Select: discord
# Token: bot token
# AllowFrom: your Discord user ID
```

## Signal

1. Register a phone number with Signal
2. Link as secondary device or use signal-cli
3. Configure via `openclaw configure --section channels`

## WhatsApp

Requires WhatsApp Business API or third-party bridge.
See OpenClaw docs for current WhatsApp integration options.

## Slack

1. Create app at https://api.slack.com/apps
2. Enable Socket Mode
3. Get bot token (`xoxb-...`) and app token (`xapp-...`)
4. Configure both tokens via `openclaw configure`

## iMessage (macOS only)

Works natively on macOS with AppleScript bridge.
Configure via `openclaw configure --section channels`

## Multi-Channel

OpenClaw supports multiple channels simultaneously.
Configure each channel separately, restart gateway once.
Messages route to/from the correct channel automatically.
