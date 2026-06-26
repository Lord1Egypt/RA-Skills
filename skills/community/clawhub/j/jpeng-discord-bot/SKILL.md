---
name: jpeng-discord-bot
description: "Send messages to Discord"
version: "1.0.0"
author: "jpeng"
tags: ["chat", "discord", "communication"]
---

# Discord Bot

Send messages to Discord

## When to Use

- User needs chat related functionality
- Automating discord tasks
- Communication operations

## Usage

```bash
python3 scripts/discord_bot.py --input <input> --output <output>
```

## Configuration

Set required environment variables:

```bash
export DISCORD_API_KEY="your-api-key"
```

## Output

Returns JSON with results:

```json
{
  "success": true,
  "data": {}
}
```
