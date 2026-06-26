---
name: openclaw-zulip
description: Zulip channel plugin for OpenClaw with topic threading, metadata DB, bot commands, and event queue processing. Install from source when you want to connect OpenClaw to a Zulip organization.
---

# OpenClaw Zulip Channel Plugin

Connect OpenClaw to Zulip — topic threading, metadata DB, bot commands, event queue processing.

## Install (local path)

```bash
git clone https://github.com/kagura-agent/openclaw-zulip.git
```

Add to `openclaw.json`:

```json
{
  "plugins": {
    "load": {
      "paths": ["path/to/openclaw-zulip"]
    },
    "entries": {
      "kagura-zulip": { "enabled": true }
    }
  }
}
```

## Configure

Add Zulip channel config:

```json
{
  "channels": {
    "zulip": {
      "enabled": true,
      "defaultAccount": "bot",
      "accounts": {
        "bot": {
          "realm": "https://your-org.zulipchat.com",
          "email": "your-bot@your-org.zulipchat.com",
          "apiKey": "your-zulip-api-key"
        }
      }
    }
  }
}
```

## Key features

- **Topic threading**: Maps Zulip topics to OpenClaw threads
- **Metadata DB**: SQLite-backed external metadata for messages/topics
- **Bot commands**: `/status`, custom commands via plugin API
- **Event queue**: Long-polling event processing with reconnection
- **Rate limiting**: Respects Zulip API rate limits with retry

## Zulip bot setup

1. Go to Zulip → Settings → Bots → Add a new bot
2. Choose "Generic bot" type
3. Copy the bot email and API key
4. Use the organization URL as `realm`

## Verification

```bash
openclaw gateway restart
```

Check gateway logs for `zulip` channel initialization. Send a DM to the bot in Zulip to verify.

## Tests

```bash
cd openclaw-zulip && npm install && npm test
```

74 vitest tests covering client, gateway, normalize, threading, metadata, and probe modules.

## Source

<https://github.com/kagura-agent/openclaw-zulip>
