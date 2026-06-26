# Routing Deep Dive

## How Feishu Message Routing Works

When a message arrives from Feishu, the Gateway processes it through this chain:

```
Feishu WebSocket → identify source app (appId)
    → match to accountId in channels.feishu.accounts
    → find matching binding in bindings[]
    → route to agentId in agents.list
    → agent processes message
    → response sent back through same Feishu app
```

Every step depends on correct configuration. A break anywhere in the chain means the message is either dropped or misrouted.

## accountId Consistency Check

The single most common misconfiguration. Run this mental (or actual) check for every agent:

```
For agent "content-writer":

1. channels.feishu.accounts has key "writer-bot"?           ✓/✗
2. That account's "agent" field = "content-writer"?          ✓/✗
3. bindings[] has entry with accountId = "writer-bot"?       ✓/✗
4. That binding's agentId = "content-writer"?                ✓/✗
5. agents.list has entry with id = "content-writer"?         ✓/✗
```

All five must be ✓. One ✗ = broken routing for that agent.

Quick validation command:
```bash
# Extract all accountIds from config and check consistency
grep -n "accountId\|\"agent\":" ~/.openclaw/openclaw.json
```

## Binding Rules

### Type Must Be "route"

```json
{"type": "route", "agentId": "...", "match": {"channel": "feishu", "accountId": "..."}}
```

The only valid `type` for Feishu bot routing is `"route"`. Other values (`"delivery"`, `"default"`, etc.) will cause the gateway to fail at startup.

### Default Agent Fallback

If a message arrives from the primary Feishu app (the top-level `appId`/`appSecret` in `channels.feishu`), it routes to whichever agent has `"default": true` in `agents.list`. No explicit binding needed for the default agent.

### Binding Order

When multiple bindings could match the same message, the first match wins. Place more specific bindings before general ones:

```json
{
  "bindings": [
    {"type": "route", "agentId": "writer", "match": {"channel": "feishu", "accountId": "writer-bot"}},
    {"type": "route", "agentId": "coder", "match": {"channel": "feishu", "accountId": "coder-bot"}},
    {"type": "route", "agentId": "main", "match": {"channel": "feishu"}}
  ]
}
```

The last binding catches any unmatched Feishu messages as a fallback.

## Group-Based Isolation

### Why Isolate

When running multiple product lines or projects, announce messages from different agents will all flow back to wherever the orchestrator's conversation is. Without isolation, a content review result and a code review result end up in the same chat thread.

### How to Isolate

Create dedicated Feishu groups per product line:

```
Group: "Content Pipeline"
  Members: orchestrator-bot, writer-bot
  Purpose: All content creation announces land here

Group: "Dev Pipeline"  
  Members: orchestrator-bot, coder-bot
  Purpose: All code-related announces land here
```

When the orchestrator spawns a sub-agent from within a specific group, the announce comes back to that same group.

### Private Chat vs Group Chat

- **Private chat** (DM with bot): Good for ad-hoc requests, cross-project work, memory management
- **Group chat** (bot in group): Good for product-line workflows, team visibility, historical traceability

## Per-Agent Tool Permissions

Each agent's tool access is configured independently. Principle: grant minimum necessary.

```json
{
  "id": "content-writer",
  "tools": {
    "allow": ["read", "write", "edit", "web_search", "feishu_doc"]
  }
}
```

Available Feishu-specific tools:
- `feishu_doc` — Read/write Feishu documents
- `feishu_chat` — Send messages in Feishu chats
- `feishu_wiki` — Access Feishu wiki/knowledge base

Not all agents need all Feishu tools. A code-expert probably doesn't need `feishu_wiki`; an analyst probably doesn't need `feishu_chat`.

## Sub-Agent Announce Routing

When the orchestrator spawns a sub-agent:
1. The sub-agent runs in its own session
2. On completion, it announces results
3. The announce is delivered to the **orchestrator's** chat channel (not the sub-agent's own Feishu bot)

This means: even if the sub-agent has its own Feishu bot, orchestrated work results flow through the orchestrator's conversation. The sub-agent's Feishu bot is only used for direct user interaction.
