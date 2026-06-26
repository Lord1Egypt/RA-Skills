---
name: openclaw-add-agent
description: "Add a new agent to OpenClaw configuration. Use when user wants to add a new Telegram bot agent to OpenClaw. Triggers: add agent, new agent, bind telegram."
---

# Add Agent to OpenClaw

## Workflow

### Step 1: Collect Agent Info

Required info from user:
- **Bot token**: Telegram bot token (format: `123456789:ABCdef...`)
- **Agent ID**: Unique identifier (e.g., `translator`, `customer_support`)
- **Purpose/Name**: Display name (optional, defaults to agent ID)
- **Allow users**: Telegram user IDs that can access this bot (default: same as existing agents)

### Step 2: Update openclaw.json

Edit `/home/xgao/.openclaw/openclaw.json`:

**A. Add agent to `agents.list`**:
```json
{
  "id": "<agent_id>",
  "name": "<name>",
  "workspace": "/home/xgao/clawd-workspace/<agent_id>"
}
```

**B. Add binding**:
```json
{
  "agentId": "<agent_id>",
  "match": {
    "channel": "telegram",
    "accountId": "<agent_id>"
  }
}
```

**C. Add telegram account**:
```json
"<agent_id>": {
  "enabled": true,
  "dmPolicy": "allowlist",
  "botToken": "<token>",
  "allowFrom": [<user_ids>],
  "groupPolicy": "allowlist",
  "streaming": "partial"
}
```

### Step 3: Create Workspace Directory

```bash
mkdir -p /home/xgao/clawd-workspace/<agent_id>
```

### Step 4: Ask About Memory Isolation

Ask user: "是否需要独立的memory？"
- **Yes** → Each agent already has independent workspace, memory is automatically isolated
- **No** → Share workspace (not recommended)

### Step 5: Restart OpenClaw

Inform user to restart: `openclaw restart`

## Minimal Config Example

For a simple translator bot:
```json
// agents.list
{ "id": "translator", "name": "translator", "workspace": "/home/xgao/clawd-workspace/translator" }

// bindings
{ "agentId": "translator", "match": { "channel": "telegram", "accountId": "translator" } }

// channels.telegram.accounts
"translator": { "enabled": true, "dmPolicy": "allowlist", "botToken": "8223784004:AAE-...", "allowFrom": ["8538882690"], "groupPolicy": "allowlist", "streaming": "partial" }
```