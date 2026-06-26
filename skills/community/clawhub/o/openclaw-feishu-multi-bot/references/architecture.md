# Architecture: Multi-Bot Feishu Integration

## Core Design

**One Gateway, multiple Feishu identities.** Each Agent maps to an independent Feishu enterprise app. The Gateway's channel layer multiplexes all WebSocket connections through a single process.

```
┌──────────────────────────────────────────────────────┐
│                  OpenClaw Gateway                     │
│                                                      │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │ Agent A │ │ Agent B │ │ Agent C │ │ Agent D │   │
│  │orchestr.│ │ writer  │ │  coder  │ │ analyst │   │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘   │
│       │           │           │           │         │
├───────┼───────────┼───────────┼───────────┼─────────┤
│  Feishu Channel Layer (WebSocket multiplexer)       │
│       │           │           │           │         │
│  ┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐   │
│  │ App 1   │ │ App 2   │ │ App 3   │ │ App 4   │   │
│  │总调度bot│ │写作bot  │ │开发bot  │ │分析bot  │   │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘   │
└──────────────────────────────────────────────────────┘
         ↕             ↕           ↕           ↕
    Feishu Users / Groups (each bot has independent identity)
```

## Three-Block Configuration Model

The entire routing system depends on three JSON blocks in `openclaw.json` that must be mutually consistent.

### Block 1: Channel Credentials (`channels.feishu`)

Declares all Feishu app credentials. The top-level `appId`/`appSecret` is the primary app; `accounts` holds additional bot identities.

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_primary_app_id",
      "appSecret": "primary_secret",
      "connectionMode": "websocket",
      "accounts": {
        "writer-bot": {
          "appId": "cli_writer_app_id",
          "appSecret": "writer_secret",
          "agent": "content-writer"
        },
        "coder-bot": {
          "appId": "cli_coder_app_id",
          "appSecret": "coder_secret",
          "agent": "code-expert"
        }
      }
    }
  }
}
```

Key points:
- Each key under `accounts` is the **accountId** — the routing identifier
- The `agent` field links this account to an agent ID in `agents.list`
- `connectionMode: "websocket"` is the standard mode for Feishu

### Block 2: Route Bindings (`bindings`)

Maps incoming messages from each Feishu account to the correct Agent.

```json
{
  "bindings": [
    {
      "type": "route",
      "agentId": "content-writer",
      "match": {
        "channel": "feishu",
        "accountId": "writer-bot"
      }
    },
    {
      "type": "route",
      "agentId": "code-expert",
      "match": {
        "channel": "feishu",
        "accountId": "coder-bot"
      }
    }
  ]
}
```

Key points:
- `type` **must** be `"route"` — no other value works
- `accountId` must exactly match the key in `channels.feishu.accounts`
- The primary app (top-level credentials) is typically bound to the main/default agent

### Block 3: Agent Definitions (`agents.list`)

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "name": "Orchestrator",
        "workspace": "~/.openclaw/workspace",
        "subagents": {
          "allowAgents": ["content-writer", "code-expert"]
        }
      },
      {
        "id": "content-writer",
        "name": "Writer",
        "workspace": "~/.openclaw/workspace-writer",
        "model": "your-model",
        "tools": {
          "allow": ["read", "write", "edit", "web_search"]
        }
      },
      {
        "id": "code-expert",
        "name": "Coder",
        "workspace": "~/.openclaw/workspace-coder",
        "model": "your-model",
        "tools": {
          "allow": ["read", "write", "edit", "exec", "browser"]
        }
      }
    ]
  }
}
```

## accountId: The Routing Key

The accountId connects all three blocks:

```
channels.feishu.accounts.{accountId}     ← credentials
         ↕
channels.feishu.accounts.{accountId}.agent → agents.list[].id   ← agent binding
         ↕
bindings[].match.accountId               ← route matching
```

If accountId is inconsistent in any one location, messages either go to the wrong agent or disappear entirely — with no error message.

## Feishu App Independence

Each Feishu app is a fully independent bot:
- **Own name**: Displayed in chat and group member lists
- **Own avatar**: Different icon per bot
- **Own groups**: Can be added to different Feishu groups independently
- **Own permissions**: Each app has its own Feishu permission scope

Users perceive them as completely separate assistants. They have no idea a single OpenClaw Gateway is behind all of them.

## Orchestrator + Sub-Agent Pattern

The orchestrator agent can spawn sub-agents that have their own Feishu bots:

```json
{
  "id": "orchestrator",
  "subagents": {
    "allowAgents": ["content-writer", "code-expert", "analyst"]
  }
}
```

When the orchestrator spawns a sub-agent, the sub-agent's work result is announced back through the orchestrator's Feishu channel — not through the sub-agent's own Feishu bot. Direct user interaction goes through each bot's own channel; orchestrated work flows through the orchestrator's channel.

## Group-Based Isolation

For multi-project or multi-product-line setups, create dedicated Feishu groups:

```
Group: "Project Alpha"  → Add: orchestrator-bot, writer-bot
Group: "Project Beta"   → Add: orchestrator-bot, coder-bot
Group: "General"        → Add: orchestrator-bot only
```

Benefits:
- Announce messages from different product lines don't mix
- Each group shows the complete progress chain for its project
- Historical traceability by group chat history
