# Communication Platforms

## Supported Platforms

### Discord
- **Skill**: `discord`
- Send messages, embeds, reactions
- Polls, threads, channels
- Slash commands, buttons
- Format: No markdown tables, use bullet lists
- Wrap links in `<>` to suppress embeds

### Telegram
- **Native**: Built-in message tool
- Send messages, media, files
- Inline buttons, polls
- Voice messages (asVoice)
- Reply threading

### Slack
- **Skill**: `slack`
- Messages, reactions, pins
- Channel management
- Thread replies

### WhatsApp
- **Skill**: `wacli`
- Send messages to contacts
- Search/sync history
- Format: No markdown headers, use **bold**

### iMessage
- **Skills**: `imsg`, `bluebubbles`
- Send/receive messages
- Chat history search
- Group messaging

### Signal
- Via OpenClaw message tool
- End-to-end encrypted

### X (Twitter)
- **Skill**: `xurl`
- Post tweets, replies, quotes
- Search, read posts
- DMs, media upload
- Follower management

### Google Chat
- Via OpenClaw message tool
- Spaces and DMs

### LINE
- Via OpenClaw message tool

## Cross-Platform Guidelines

### Formatting by Platform
| Feature | Discord | Telegram | WhatsApp | Slack |
|---|---|---|---|---|
| Markdown | ✅ | ✅ | ⚠️ | ✅ |
| Tables | ❌ | ✅ | ❌ | ✅ |
| Headers | ✅ | ✅ | ❌ | ✅ |
| Code blocks | ✅ | ✅ | ✅ | ✅ |
| Links | Wrap in `<>` | Auto | Auto | Auto |

### Unified Patterns
- Use `message` tool with appropriate `channel`
- Adapt formatting per platform
- Batch sends when possible (rate limits)
- Silent sends for non-urgent notifications
- Reactions for acknowledgment (where supported)

## Bot Behavior
- Respond when directly mentioned
- Don't flood channels
- Use threads for long discussions
- Respect platform norms
- One reaction per message max
