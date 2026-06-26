# OpenClaw Subagents — Configuration Reference

Source: https://docs.openclaw.ai/tools/subagents and https://docs.openclaw.ai/gateway/configuration

---

## Full openclaw.json Schema for Subagents

```json5
{
  agents: {
    defaults: {
      // Default model for all agents
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["anthropic/claude-haiku-4-5"]
      },

      // Subagent-specific defaults (applies to all spawned subagents)
      subagents: {
        model: "anthropic/claude-haiku-4-5",  // cheaper model for background work
        thinking: "basic",                     // none | basic | deep
        maxSpawnDepth: 1,                      // 1 = no nesting (default), 2 = orchestrator pattern, max 5
        maxChildrenPerAgent: 5,               // active children per session, range 1-20
        maxConcurrent: 8,                     // global concurrency lane across all agents
        runTimeoutSeconds: 900,               // default timeout; 0 = no timeout
        archiveAfterMinutes: 60               // auto-archive transcript after N minutes
      }
    },

    // Individual agent definitions
    list: [
      {
        id: "main",                                        // unique agent identifier
        workspace: "~/.openclaw/workspace-main",           // workspace directory
        // agentDir: "~/.openclaw/agents/main/agent",     // auth/config dir (default)

        // Per-agent subagent overrides (can only restrict, not expand beyond defaults)
        subagents: {
          allowAgents: ["researcher", "writer"],           // which agents this agent can spawn; ["*"] for any
          model: "anthropic/claude-haiku-4-5",            // override model for subagents spawned by this agent
          thinking: "none"
        },

        // Per-agent tool restrictions
        tools: {
          allow: ["read", "exec", "process"],
          deny: ["gateway", "cron"]
        },

        // Per-agent sandbox
        sandbox: {
          mode: "all",    // none | exec | all
          scope: "agent"  // agent | session
        }
      },
      {
        id: "researcher",
        workspace: "~/.openclaw/workspace-researcher"
      }
    ]
  },

  // Global tool policy for subagents
  tools: {
    subagents: {
      tools: {
        deny: ["gateway", "cron", "sessions_send"],
        allow: ["read", "exec", "process", "browser"]
      }
    }
  },

  // Discord thread binding (Discord only)
  channels: {
    discord: {
      threadBindings: {
        enabled: true,
        idleHours: 24,
        maxAgeHours: 168,
        spawnSubagentSessions: true   // messages in thread route to same subagent session
      }
    }
  }
}
```

---

## Key Field Notes

### maxSpawnDepth
- `1` (default): Main agent can spawn subagents, but subagents cannot spawn further children
- `2`: Enables orchestrator pattern — depth-1 subagents can spawn depth-2 workers
- Max allowed: 5 (but 2 is the practical recommendation)
- Setting this on the `agents.defaults.subagents` object applies globally

### maxChildrenPerAgent
- Controls how many active subagents one session can have at once
- Range: 1–20
- Default: 5
- Increase for parallel workloads; decrease to control costs

### maxConcurrent
- Global queue concurrency lane across all agents in the gateway
- Acts as a safety valve to prevent runaway parallelism
- Default: 8

### model (subagents)
- Format: `"provider/model-id"` e.g. `"anthropic/claude-haiku-4-5"`
- If omitted, subagents inherit the caller's model
- Per-agent overrides in `agents.list[].subagents.model` take priority over `agents.defaults.subagents.model`

### archiveAfterMinutes
- Subagent session transcript is renamed to `*.deleted.<timestamp>` after this duration
- Default: 60 minutes
- Setting `cleanup: "delete"` in sessions_spawn overrides this and archives immediately post-announce

### allowAgents
- Restricts which agent IDs a given agent can target when spawning subagents
- Use `["*"]` to allow any agent
- This is a security boundary — prevents rogue agents from spawning arbitrary sessions

---

## Path Structure

```
~/.openclaw/
├── openclaw.json                    # Main config file
├── workspace-<agentId>/             # Agent workspace (files, memory, SOUL.md)
│   ├── SOUL.md
│   ├── AGENTS.md
│   ├── HEARTBEAT.md
│   └── memory/
│       ├── WORKING.md
│       ├── MEMORY.md
│       └── YYYY-MM-DD.md
└── agents/
    └── <agentId>/
        ├── agent/                   # agentDir: auth profiles, per-agent config
        │   └── auth-profiles.json
        └── sessions/                # Session history (JSONL files)
```

---

## CLI Commands for Setup

```bash
# Initialize a new agent
openclaw agents add <agentId>

# List all agents and their bindings
openclaw agents list --bindings

# Start the gateway daemon
openclaw gateway start

# Add a cron heartbeat
openclaw cron add \
  --name "agent-heartbeat" \
  --cron "*/15 * * * *" \
  --session "isolated" \
  --message "Check for work..."

# Send a message to a specific session
openclaw sessions send \
  --session "agent:main:main" \
  --message "Your task here"
```

---

## Routing / Bindings

Bindings determine which agent receives a message. Hierarchy (most-specific wins):

1. Peer match (exact DM/group/channel ID)
2. Parent peer match (thread inheritance)
3. Guild ID + Discord roles
4. Guild ID alone
5. Team ID (Slack)
6. Account ID match
7. Channel-wide match
8. Fallback to default agent

Example multi-agent binding:

```json5
{
  bindings: [
    { agentId: "work", match: { channel: "telegram", accountId: "biz-account" } },
    { agentId: "main", match: { channel: "telegram" } }   // fallback
  ]
}
```
