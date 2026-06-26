# openclaw-zulip

OpenClaw channel plugin for [Zulip](https://zulip.com) — connect your OpenClaw agent to Zulip with native topic threading, stream organization, and metadata management.

## Features

- **Stream & topic routing** — messages route through Zulip's stream/topic hierarchy
- **DM support** — direct messages with configurable DM policy and allowlists
- **Topic threading** — replies stay in the correct topic automatically
- **Metadata DB** — SQLite-backed per-topic metadata (status, priority, assignee, labels) via `/meta` bot commands
- **Real-time gateway** — long-polling event queue for instant message reception
- **Rate limit handling** — automatic retry with backoff on Zulip API rate limits

## Installation

```bash
openclaw plugins install @kagura-agent/openclaw-zulip
```

Or via npm:

```bash
npm install @kagura-agent/openclaw-zulip
```

## Configuration

Add to your `openclaw.json`:

```json
{
  "channels": {
    "zulip": {
      "realm": "https://your-org.zulipchat.com",
      "email": "bot-email@your-org.zulipchat.com",
      "apiKey": "your-bot-api-key",
      "streams": ["general", "dev"],
      "defaultStream": "general",
      "defaultTopic": "agent",
      "dmPolicy": "pairing",
      "allowFrom": []
    }
  }
}
```

### Configuration Options

| Option | Type | Description |
|---|---|---|
| `realm` | string | Zulip server URL |
| `email` | string | Bot email address |
| `apiKey` | string | Bot API key (from Zulip settings) |
| `streams` | string[] | Streams to listen on |
| `defaultStream` | string | Default stream for outbound messages |
| `defaultTopic` | string | Default topic for outbound messages |
| `dmPolicy` | string | DM policy: `"pairing"`, `"open"`, or `"closed"` |
| `allowFrom` | array | Allowed sender emails or user IDs for DMs |

## Bot Commands

In any Zulip topic, send `/meta` commands to manage topic metadata:

- `/meta` — show current topic metadata
- `/meta set status=open priority=high assignee=alice` — set metadata fields
- `/meta label add bug` — add a label
- `/meta label rm bug` — remove a label
- `/meta list` — list all topics with metadata in the stream
- `/meta list status=open` — filter by field
- `/meta clear` — clear all metadata for the topic

## Development

```bash
npm install
npm test          # vitest (74 tests)
npm run typecheck # tsc --noEmit
```

Additional node:test suite (61 tests):
```bash
node --test src/metadata/command-handler.test.ts src/metadata/command-parser.test.ts src/metadata/store.test.ts
```

## License

MIT
