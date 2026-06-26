# Security & Data Transparency

This document provides complete transparency about what data this plugin collects and transmits.

## Required Configuration

**This plugin requires an API key:**

```bash
openclaw config set plugins.entries.human-like-mem.config.apiKey "mp_your_key_here"
```

Get your API key at: https://plugin.human-like.me

The runtime reads this value from OpenClaw plugin config only. It does not read `HUMAN_LIKE_MEM_*` environment variables or local secrets files.

## Data Transmission Details

### What is Sent to the Server

| Field | Purpose | Can Disable? |
|-------|---------|--------------|
| `messages[].role` | Identify speaker (user/assistant) | No (core) |
| `messages[].content` | Conversation content for memory | No (core) |
| `user_id` | Isolate memories per user | No (core) |
| `agent_id` | Isolate memories per agent | No (core) |
| `conversation_id` | Group related messages | No (core) |
| `tags` | Categorize memories | Yes (`tags: []`) |
| `metadata.user_ids` | Platform user IDs (Feishu/Discord) | Yes (see below) |
| `metadata.session_id` | Session tracking | No |
| `metadata.scenario` | Usage context | Yes (`scenario: null`) |

### What is NOT Sent

- Local file contents
- System environment variables
- IP address (visible to server but not stored by plugin)
- Device information
- Other application data

### Platform User IDs

When messages contain platform-specific formats (e.g., `[Feishu ou_xxx]`), the plugin extracts user IDs for:
- **Cross-session memory continuity**: Same user on same platform gets consistent memories
- **Multi-user conversations**: Track who said what in group chats

**Platform ID extraction is disabled by default in v1.0.0+. To explicitly enable it**, run:

```bash
openclaw config set plugins.entries.human-like-mem.config.stripPlatformMetadata false
```

## Default Behavior

| Setting | Default | Description |
|---------|---------|-------------|
| `recallEnabled` | `true` | Auto-recall on every turn |
| `addEnabled` | `true` | Auto-store conversations |
| `minTurnsToStore` | `5` | Store every N turns |
| `memoryLimitNumber` | `6` | Max memories to retrieve |
| `stripPlatformMetadata` | `true` | Do not send Feishu/Discord platform IDs unless explicitly enabled |

### How to Disable Auto-Storage

```bash
openclaw config set plugins.entries.human-like-mem.config.addEnabled false
```

### How to Disable Auto-Recall

```bash
openclaw config set plugins.entries.human-like-mem.config.recallEnabled false
```

## Server-Side Data Handling

### Data Retention
- Memories are stored indefinitely unless manually deleted
- Users can delete all their data via API (see PRIVACY.md)

### Data Isolation
- Each API key has a completely isolated memory space
- User IDs are prefixed with API key hash to prevent cross-key collisions

### Encryption
- All communication uses HTTPS (TLS 1.2+)
- Data at rest is encrypted (AES-256)

## Network Traffic Inspection

To verify what data is sent, enable debug logging:

```bash
openclaw logs | grep "Memory Plugin"
```

Or inspect network traffic:
```bash
# macOS/Linux
mitmproxy --mode regular@8080
export HTTPS_PROXY=http://localhost:8080
```

## Security Recommendations

1. **Use a test API key first** - Don't use production keys for initial testing
2. **Start with addEnabled: false** - Manually control what gets stored
3. **Avoid sensitive content** - Don't discuss passwords, API keys, or PII
4. **Use `<private>` tags** - Content in `<private>...</private>` is not memorized
5. **Review before production** - Audit network traffic before enabling for all conversations

## Source Code

This plugin is fully open source:
- GitLab: https://gitlab.ttyuyin.com/personalization_group/human-like-mem-openclaw-plugin
- npm: https://www.npmjs.com/package/@humanlikememory/human-like-mem
- ClawHub: https://clawhub.ai/humanlike2026/humanlike-memory-plugin

## Reporting Security Issues

Contact: security@human-like.me
