# @openclaw/memory-agentmemo

OpenClaw memory plugin that connects to an external [AgentMemo](https://github.com/yxjsxy/agentMemo) HTTP service for semantic memory search, auto-recall, and auto-capture.

## Why AgentMemo?

Unlike the built-in memory system (which embeds local Markdown files), AgentMemo provides:

- **Hybrid semantic search** — dense + sparse + temporal decay
- **Version history** — every memory write is recorded with full provenance
- **Multi-agent namespaces** — isolate memories by user, agent, or project
- **REST API** — self-hostable, language-agnostic
- **Persistence across node restarts** without re-embedding

## Installation

```bash
openclaw install @openclaw/memory-agentmemo
```

## Setup

### 1. Start AgentMemo server

Follow the [AgentMemo README](https://github.com/yxjsxy/agentMemo) to start the HTTP service:

```bash
# Example (defaults to port 8790)
cd agentMemo
python -m agentmemo.server
```

### 2. Configure the plugin in `openclaw.json`

**Minimal (local server, no auth):**

```json
{
  "plugins": {
    "memory-agentmemo": {}
  }
}
```

**Full configuration:**

```json
{
  "plugins": {
    "memory-agentmemo": {
      "serverUrl": "http://localhost:8790",
      "apiKey": "${AGENTMEMO_API_KEY}",
      "userId": "karl",
      "autoRecall": true,
      "autoCapture": false
    }
  }
}
```

**Remote server:**

```json
{
  "plugins": {
    "memory-agentmemo": {
      "serverUrl": "https://memo.yourdomain.com",
      "apiKey": "${AGENTMEMO_API_KEY}",
      "userId": "myagent",
      "autoRecall": true,
      "autoCapture": true
    }
  }
}
```

## Configuration Reference

| Field        | Type    | Required | Default                   | Description                                          |
|--------------|---------|----------|---------------------------|------------------------------------------------------|
| `serverUrl`  | string  | No       | `http://localhost:8790`   | Base URL of AgentMemo HTTP service                   |
| `apiKey`     | string  | No       | —                         | Bearer token for authenticated instances. Supports `${ENV_VAR}` |
| `userId`     | string  | No       | —                         | User/namespace ID for scoping memories               |
| `autoRecall` | boolean | No       | `true`                    | Inject relevant memories before agent starts         |
| `autoCapture`| boolean | No       | `false`                   | Auto-store important user messages after conversation |

## API Endpoints Used

| Feature       | Endpoint              | Method |
|---------------|-----------------------|--------|
| Semantic search | `POST /memories/search` | POST |
| Add memory    | `POST /memories/`     | POST   |
| Health probe  | `GET /health`         | GET    |

## How It Works

### Auto-Recall
Before each agent turn, the plugin searches AgentMemo for memories relevant to the user's prompt and injects them into the system context as `<relevant-memories>` block.

### Auto-Capture
After each conversation turn, if `autoCapture: true`, the plugin analyzes user messages for memorable content (preferences, facts, decisions) and stores them to AgentMemo automatically.

## Background

This plugin was refactored from a core PR ([openclaw/openclaw#54712](https://github.com/openclaw/openclaw/pull/54712)) into a standalone ClawHub external plugin, following OpenClaw's recommended extension architecture.

## License

MIT
