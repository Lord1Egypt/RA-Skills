---
name: gramgate
description: "Telegram gateway for AI agents and automation. Use GramGate to access a real Telegram account over REST or MCP: read channels and history, search across chats, click inline buttons, join groups, and send messages as a user account rather than a bot."
metadata:
  {
    "openclaw":
      {
        "emoji": "📬",
        "requires": { "bins": ["python3"] }
      }
  }
---

# GramGate

**Telegram gateway for AI agents and automation.**

Use GramGate when you need **real Telegram account access via MTProto**, not the limitations of the Bot API.

GitHub: <https://github.com/zakirovdmr/gramgate>

## Why GramGate

Telegram bots cannot reliably do the things many serious workflows need: read subscribed channels, browse full history, search across chats, join by link, or click inline buttons as a normal user.

GramGate solves that by exposing a **real Telegram account** through:
- **REST API** for scripts, automations, and HTTP tools
- **MCP server** for Claude, GPT, IDE agents, and agent frameworks

## Best Use Cases

Use this skill for:
- **channel research and monitoring**, including subscribed-channel analysis and news tracking
- **content workflows**, from research collection to drafting triggers and publishing operations
- **Telegram E2E testing**, including bot flows that require real user interaction and button clicks
- **support, CRM, and notification flows** inside Telegram
- **agent integrations**, where an AI system needs structured Telegram read/write access

## What It Can Do

GramGate exposes 40+ Telegram endpoints and supports workflows like:
- reading dialogs, chats, channels, contacts, and full message history
- searching within a chat or globally across Telegram
- joining or leaving channels and groups
- sending, editing, deleting, forwarding, copying, pinning, and reacting to messages
- reading rich history with inline buttons and clicking those buttons
- working with polls, media, contacts, locations, members, and live feed events

Typical local endpoints:

```bash
REST: http://127.0.0.1:18791
MCP:  http://127.0.0.1:18793/sse
```

## Common REST Calls

### Health and account

```bash
curl -s http://127.0.0.1:18791/health
curl -s http://127.0.0.1:18791/api/me
curl -s http://127.0.0.1:18791/api/dialogs?limit=30
```

### Read chats and channels

```bash
curl -s -X POST http://127.0.0.1:18791/api/chat/info \
  -H 'Content-Type: application/json' \
  -d '{"chat_id":"@durov"}'

curl -s -X POST http://127.0.0.1:18791/api/chat/history \
  -H 'Content-Type: application/json' \
  -d '{"chat_id":"-1001234567890","limit":20}'
```

### Search and join

```bash
curl -s -X POST http://127.0.0.1:18791/api/message/search \
  -H 'Content-Type: application/json' \
  -d '{"chat_id":"-1001234567890","query":"keyword","limit":20}'

curl -s -X POST http://127.0.0.1:18791/api/chat/join \
  -H 'Content-Type: application/json' \
  -d '{"link":"@channel_name"}'
```

### Send a message

```bash
curl -s -X POST http://127.0.0.1:18791/api/message/send \
  -H 'Content-Type: application/json' \
  -d '{"recipient":"@username","text":"Hello from GramGate!"}'
```

### Click an inline button

```bash
curl -s -X POST http://127.0.0.1:18791/api/button/click \
  -H 'Content-Type: application/json' \
  -d '{"chat_id":123456789,"message_id":42,"callback_data":"btn_action"}'
```

## MCP Use

Use GramGate MCP when another agent should be able to:
- list dialogs
- inspect a chat or channel
- fetch history
- search messages
- join channels
- send messages
- click Telegram inline buttons

## Notes

- `chat_id` may be numeric or `@username`
- groups and channels usually use negative numeric ids
- this is **user-account access**, so privacy and operational safety matter
- prefer fewer, larger reads and avoid tight write loops
- if exposing GramGate beyond localhost, use authentication and sane rate limits

## Recommended Workflow

1. Confirm the service is healthy.
2. Discover the right chat or channel.
3. Read history before taking action.
4. Batch reads where possible.
5. Write only when the task actually requires it.

## Full Documentation

For setup, architecture, authentication, rate limiting, and the complete endpoint list, use the GitHub repo as the canonical reference:

<https://github.com/zakirovdmr/gramgate>
