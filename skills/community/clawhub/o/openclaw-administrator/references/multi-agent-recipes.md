# Multi-Agent Recipes

Practical configuration examples for running multiple agents in one Gateway.

## Concepts Recap

| Term | Meaning |
|---|---|
| `agentId` | One isolated brain (workspace, auth, sessions) |
| `accountId` | One channel account (e.g. `"personal"` WhatsApp vs `"biz"`) |
| `binding` | Routes `(channel, accountId, peer)` inbound to an `agentId` |
| `agentDir` | `~/.openclaw/agents/<agentId>/agent` — auth profiles, model registry |

**Never reuse `agentDir` across agents.** Never share `auth-profiles.json` between agents without deliberately copying it.

---

## Recipe 1: Two WhatsApp Accounts → Two Agents

```bash
# Link both accounts first
openclaw channels login --channel whatsapp --account personal
openclaw channels login --channel whatsapp --account biz
```

`~/.openclaw/openclaw.json`:
```json
{
  "agents": {
    "list": [
      {
        "id": "home",
        "default": true,
        "name": "Home",
        "workspace": "~/.openclaw/workspace-home",
        "agentDir": "~/.openclaw/agents/home/agent"
      },
      {
        "id": "work",
        "name": "Work",
        "workspace": "~/.openclaw/workspace-work",
        "agentDir": "~/.openclaw/agents/work/agent"
      }
    ]
  },
  "bindings": [
    { "agentId": "home", "match": { "channel": "whatsapp", "accountId": "personal" } },
    { "agentId": "work", "match": { "channel": "whatsapp", "accountId": "biz" } },
    {
      "agentId": "work",
      "match": {
        "channel": "whatsapp",
        "accountId": "personal",
        "peer": { "kind": "group", "id": "120363012345678901@g.us" }
      }
    }
  ],
  "channels": {
    "whatsapp": {
      "accounts": {
        "personal": {},
        "biz": {}
      }
    }
  }
}
```

---

## Recipe 2: WhatsApp DM Split (One Number → Multiple Agents)

Route different phone numbers to different agents on the same WhatsApp account.

```json
{
  "agents": {
    "list": [
      { "id": "alex", "workspace": "~/.openclaw/workspace-alex" },
      { "id": "mia", "workspace": "~/.openclaw/workspace-mia" }
    ]
  },
  "bindings": [
    {
      "agentId": "alex",
      "match": { "channel": "whatsapp", "peer": { "kind": "direct", "id": "+15551230001" } }
    },
    {
      "agentId": "mia",
      "match": { "channel": "whatsapp", "peer": { "kind": "direct", "id": "+15551230002" } }
    }
  ],
  "channels": {
    "whatsapp": {
      "dmPolicy": "allowlist",
      "allowFrom": ["+15551230001", "+15551230002"]
    }
  }
}
```

Notes:
- DM access control is global per WhatsApp account (not per agent).
- Direct chats collapse to `agent:<agentId>:main` — true isolation requires one agent per person.

---

## Recipe 3: Discord — One Bot Per Agent

```json
{
  "agents": {
    "list": [
      { "id": "main", "workspace": "~/.openclaw/workspace-main" },
      { "id": "coding", "workspace": "~/.openclaw/workspace-coding" }
    ]
  },
  "bindings": [
    { "agentId": "main", "match": { "channel": "discord", "accountId": "default" } },
    { "agentId": "coding", "match": { "channel": "discord", "accountId": "coding" } }
  ],
  "channels": {
    "discord": {
      "groupPolicy": "allowlist",
      "accounts": {
        "default": {
          "token": "DISCORD_BOT_TOKEN_MAIN",
          "guilds": {
            "123456789012345678": {
              "channels": {
                "222222222222222222": { "allow": true, "requireMention": false }
              }
            }
          }
        },
        "coding": {
          "token": "DISCORD_BOT_TOKEN_CODING",
          "guilds": {
            "123456789012345678": {
              "channels": {
                "333333333333333333": { "allow": true, "requireMention": false }
              }
            }
          }
        }
      }
    }
  }
}
```

Each Discord bot account needs its token at `channels.discord.accounts.<id>.token`. Invite each bot to the guild and enable Message Content Intent in the Discord developer portal.

---

## Recipe 4: Telegram — One Bot Per Agent

```json
{
  "agents": {
    "list": [
      { "id": "main", "workspace": "~/.openclaw/workspace-main" },
      { "id": "alerts", "workspace": "~/.openclaw/workspace-alerts" }
    ]
  },
  "bindings": [
    { "agentId": "main", "match": { "channel": "telegram", "accountId": "default" } },
    { "agentId": "alerts", "match": { "channel": "telegram", "accountId": "alerts" } }
  ],
  "channels": {
    "telegram": {
      "accounts": {
        "default": {
          "botToken": "123456:ABC...",
          "dmPolicy": "pairing"
        },
        "alerts": {
          "botToken": "987654:XYZ...",
          "dmPolicy": "allowlist",
          "allowFrom": ["tg:123456789"]
        }
      }
    }
  }
}
```

---

## Recipe 5: Channel Split (WhatsApp Fast + Telegram Deep)

Route WhatsApp to a fast everyday agent and Telegram to a higher-reasoning agent.

```json
{
  "agents": {
    "list": [
      {
        "id": "chat",
        "name": "Everyday",
        "workspace": "~/.openclaw/workspace-chat",
        "model": "anthropic/claude-haiku-4-5"
      },
      {
        "id": "deep",
        "name": "Deep Work",
        "workspace": "~/.openclaw/workspace-deep",
        "model": "anthropic/claude-opus-4-6"
      }
    ]
  },
  "bindings": [
    { "agentId": "chat", "match": { "channel": "whatsapp" } },
    { "agentId": "deep", "match": { "channel": "telegram" } }
  ]
}
```

To also route a specific WhatsApp DM to the deep agent:
```json
{
  "bindings": [
    {
      "agentId": "deep",
      "match": { "channel": "whatsapp", "peer": { "kind": "direct", "id": "+15551234567" } }
    },
    { "agentId": "chat", "match": { "channel": "whatsapp" } },
    { "agentId": "deep", "match": { "channel": "telegram" } }
  ]
}
```

Peer bindings always win over channel-wide rules.

---

## Recipe 6: Agent-to-Agent Messaging (Explicit Enable)

Off by default. Must be explicitly enabled and allowlisted:

```json
{
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["main", "coding", "research"]
    }
  }
}
```

---

## Recipe 7: Sub-Agent Allowlist for Named Agents

Allow the `main` agent to spawn specific configured agents as sub-agents:

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "workspace": "~/.openclaw/workspace-main",
        "subagents": {
          "allowAgents": ["coding", "research"]
        }
      },
      { "id": "coding", "workspace": "~/.openclaw/workspace-coding" },
      { "id": "research", "workspace": "~/.openclaw/workspace-research" }
    ]
  }
}
```

Use `["*"]` to allow any configured agent.

---

## Recipe 8: Per-Agent Model Override

Each agent can use a different model regardless of the global default:

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-sonnet-4-6"
    },
    "list": [
      { "id": "main" },
      {
        "id": "heavy",
        "workspace": "~/.openclaw/workspace-heavy",
        "model": "anthropic/claude-opus-4-6"
      },
      {
        "id": "fast",
        "workspace": "~/.openclaw/workspace-fast",
        "model": "anthropic/claude-haiku-4-5"
      }
    ]
  }
}
```

---

## Recipe 9: Cross-Agent Memory Search

Let one agent search another agent's session transcripts:

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "workspace": "~/.openclaw/workspace-main",
        "memorySearch": {
          "qmd": {
            "extraCollections": [
              { "path": "~/.openclaw/agents/coding/sessions", "name": "coding-sessions" }
            ]
          }
        }
      },
      { "id": "coding", "workspace": "~/.openclaw/workspace-coding" }
    ]
  }
}
```

---

## Verify Everything

After any multi-agent config change:

```bash
openclaw gateway restart
openclaw agents list --bindings
openclaw channels status --probe
openclaw health --verbose
```
