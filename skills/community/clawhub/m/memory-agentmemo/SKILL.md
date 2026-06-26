---
name: memory-agentmemo
description: OpenClaw external memory plugin for AgentMemo. Enables semantic memory search and auto-capture via a self-hosted AgentMemo server. Install to use AgentMemo as your memory backend instead of the default file-based memory.
---

# Memory (AgentMemo)

External memory plugin for OpenClaw that delegates semantic memory storage and retrieval to a self-hosted [AgentMemo](https://github.com/agentmemo) server.

## Install

```bash
openclaw install @openclaw/memory-agentmemo
```

Or via ClawHub:

```bash
clawhub install memory-agentmemo
```

## Configuration

In your `openclaw.json`, add the plugin config:

```json
{
  "plugins": {
    "memory-agentmemo": {
      "serverUrl": "http://localhost:8000",
      "apiKey": "your-api-key",
      "userId": "karl"
    }
  }
}
```

### Config Options

| Field | Required | Description |
|-------|----------|-------------|
| `serverUrl` | ✅ | AgentMemo HTTP server URL |
| `apiKey` | ❌ | API key if your server requires auth |
| `userId` | ❌ | User ID for memory namespacing |
| `autoCapture` | ❌ | Auto-capture memories from conversations (default: false) |
| `autoRecall` | ❌ | Auto-inject relevant memories into context (default: true) |

## AgentMemo Server

Run your own AgentMemo server: https://github.com/agentmemo/agentmemo

```bash
pip install agentmemo
agentmemo server --port 8000
```
