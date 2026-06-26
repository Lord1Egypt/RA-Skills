---
name: human-like-memory-plugin
description: "Long-term memory plugin for OpenClaw: automatic recall, storage, and agent tools"
homepage: https://plugin.human-like.me
metadata:
  openclaw:
    emoji: "🧠"
    kind: plugin
    requires:
      config: ["plugins.entries.human-like-mem.config.apiKey"]
---

# Human-Like Memory Plugin

Long-term memory plugin for OpenClaw. Gives your agent the ability to remember past conversations, user preferences, and important context across sessions.

## Features

- Automatic memory recall before each response
- Automatic conversation storage after each response
- Agent-callable tools: `memory_search` and `memory_store`
- Registered as a first-class memory slot (`kind: "memory"`)
- Runtime reads OpenClaw plugin config only
- Privacy-preserving by default: platform metadata extraction is disabled unless explicitly enabled
- Requires OpenClaw >= 2026.2.0

## Setup

### 1. Get API Key

Visit [plugin.human-like.me](https://plugin.human-like.me) → Register → Copy your `mp_xxx` key

### 2. Install

    openclaw plugins install @humanlikememory/human-like-mem

### 3. Configure

    # Set API key (required)
    openclaw config set plugins.entries.human-like-mem.config.apiKey "mp_your_key_here"

    # Set as the active memory engine
    openclaw config set plugins.slots.memory human-like-mem

    # Enable memory search for the agent
    openclaw config set agents.defaults.memorySearch '{"enabled":true}' --strict-json

### 4. Restart

    openclaw restart

### 5. Verify

    openclaw status

You should see:

    Memory │ 0 files · 0 chunks · sources remote-api · plugin human-like-mem · vector ready

## Configuration Options

All options via `openclaw config set plugins.entries.human-like-mem.config.<key> <value>`:

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `apiKey` | string | **(required)** | Your API key from plugin.human-like.me |
| `baseUrl` | string | `https://plugin.human-like.me` | API endpoint |
| `userId` | string | `openclaw-user` | User identifier |
| `agentId` | string | auto-detected | Agent identifier |
| `recallEnabled` | boolean | `true` | Enable automatic memory recall |
| `addEnabled` | boolean | `true` | Enable automatic memory storage |
| `memoryLimitNumber` | number | `6` | Max memories to recall per turn |
| `minScore` | number | `0.1` | Minimum relevance score (0-1) |
| `minTurnsToStore` | number | `5` | Store after N conversation turns |
| `stripPlatformMetadata` | boolean | `true` | Do not send Feishu/Discord platform IDs unless explicitly enabled |

## Agent Tools

Once installed, your agent can actively use memory:

- **`memory_search`** — Search past conversations and stored knowledge
- **`memory_store`** — Save important information for future recall

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not configured" | `openclaw config set plugins.entries.human-like-mem.config.apiKey "mp_xxx"` |
| "unavailable" in status | Set `plugins.slots.memory` to `human-like-mem` |
| Check logs | `openclaw logs \| grep "Memory Plugin"` |

## License

Apache-2.0
