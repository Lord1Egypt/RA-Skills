---
name: new-agent
description: Create new OpenClaw agents and connect them to messaging channels (Telegram, Discord, Slack, Feishu, WhatsApp, Signal, Google Chat). Supports single and batch mode. Batch mode creates all agents at once with a single config write and gateway restart to avoid connection churn.
---

# New Agent

Add one or more agents to your OpenClaw gateway with dedicated workspaces and messaging channels.

## When to Use

- User wants to add a new AI agent or bot
- User wants to connect a bot to a messaging platform
- User wants to create a **team of agents** at once (batch mode)

## Modes

| Mode | When | Script |
|------|------|--------|
| **Single** | Add one agent | `scripts/setup-agent.sh` |
| **Batch** | Add multiple agents at once | `scripts/batch-setup.sh` |

> ⚠️ **Always prefer batch mode when creating 2+ agents.** Single-agent creation modifies `openclaw.json` each time, triggering a gateway hot reload per agent. For channels with persistent connections (Feishu WebSocket, Discord gateway), this causes repeated disconnects. Batch mode writes config **once** and restarts **once**.

---

## Single Agent Mode

### Required Information

| Field | Example |
|-------|---------|
| Agent name | "Luna" |
| Channel | telegram / discord / slack / feishu / whatsapp / signal / googlechat |
| Credentials | Bot token, app secret, or QR scan |

### Step 1: Workspace + Registration

```bash
./scripts/setup-agent.sh {name}
```

This creates workspace files and registers the agent with `openclaw agents add --non-interactive --workspace`.

### Step 2: Channel Configuration

Each channel needs **two things** in `openclaw.json`:
1. An **account entry** under `channels.{channel}.accounts`
2. A **binding** in the **top-level `bindings` array**

> ⚠️ The `bindings` array is at the **root level** of `openclaw.json`, NOT under `agents`.

#### Account Entry Templates

Add under `channels.{channel}.accounts.{name}`:

**Telegram:**
```json
{
  "dmPolicy": "pairing",
  "botToken": "YOUR_BOT_TOKEN",
  "groupPolicy": "open",
  "streaming": "partial"
}
```

**Discord:**
```json
{
  "token": "YOUR_BOT_TOKEN"
}
```

**Slack:**
```json
{
  "mode": "socket",
  "appToken": "xapp-...",
  "botToken": "xoxb-..."
}
```

**Feishu / Lark:**
```json
{
  "appId": "YOUR_APP_ID",
  "appSecret": "YOUR_APP_SECRET"
}
```
For Lark (global), add `"domain": "lark"`.

**WhatsApp / Signal** — Use interactive login:
```bash
openclaw channels login --channel whatsapp --account {name}
openclaw channels login --channel signal --account {name}
```

#### Binding (Top-Level)

```json
{
  "agentId": "{name}-agent",
  "match": {
    "channel": "{channel}",
    "accountId": "{name}"
  }
}
```

#### Agent-to-Agent (Optional)

Add `"{name}-agent"` to `tools.agentToAgent.allow`.

### Step 3: Verify & Pair

```bash
openclaw gateway restart
openclaw agents list --bindings
openclaw channels status --probe
```

For DM channels, send `/start` to the bot, then:
```bash
openclaw pairing approve {channel} {CODE}
```

---

## Batch Mode (Recommended for 2+ Agents)

### Why Batch?

When creating multiple agents one-by-one:
- Each `openclaw agents add` modifies `openclaw.json` → triggers hot reload
- Each channel account addition → another hot reload
- **Feishu/Discord WebSocket disconnects and reconnects each time**
- Messages sent during reload may be lost

Batch mode: **all workspaces first, one config write, one restart.**

### Step 1: Define Agents

Create a JSON manifest file listing all agents:

```json
[
  {
    "name": "基金经理",
    "id": "fund-manager",
    "role": "管理投资研究团队",
    "emoji": "📈",
    "channel": "feishu",
    "appId": "cli_xxx",
    "appSecret": "xxx"
  },
  {
    "name": "科技研究员",
    "id": "tech-researcher",
    "role": "科技行业投资研究",
    "emoji": "💻",
    "channel": "feishu",
    "appId": "cli_yyy",
    "appSecret": "yyy"
  }
]
```

Fields:
- `name` — Display name (used in IDENTITY.md)
- `id` — Agent ID slug (lowercase, used for agent-id, account-id, workspace dir)
- `role` — Role description (used in SOUL.md)
- `emoji` — Agent emoji
- `channel` — Channel type
- For Telegram: add `"botToken": "..."`
- For Feishu: add `"appId": "..."` and `"appSecret": "..."`
- For Discord: add `"token": "..."`
- For Slack: add `"appToken": "..."` and `"botToken": "..."`

### Step 2: Run Batch Setup

```bash
./scripts/batch-setup.sh agents.json
```

This will:
1. ✅ Create all workspaces (IDENTITY.md, SOUL.md, AGENTS.md, USER.md)
2. ✅ Register all agents (`openclaw agents add --non-interactive`)
3. ✅ Add all channel accounts to `openclaw.json` in **one write**
4. ✅ Add all bindings in **one write**
5. ✅ Add all agents to `agentToAgent.allow` in **one write**
6. ✅ Restart gateway **once**

### Step 3: Pair

For each agent, send a message in the channel, then approve:

```bash
openclaw pairing approve {channel} {CODE}
```

---

## Shared Channel (Multiple Agents, One Bot)

You can route multiple agents through a **single bot** using group-based bindings:

```json
{
  "agentId": "tech-researcher",
  "match": {
    "channel": "feishu",
    "accountId": "shared-bot",
    "groupId": "oc_xxxxx"
  }
}
```

- DM → routes to default agent for that account
- Group messages → route based on `groupId` match
- One bot, multiple brains

---

## Notes

- All agents share existing model credentials — no extra API keys needed
- One channel is enough to bring an agent online
- Add more channels later by repeating the single-agent steps
- The default model comes from `agents.defaults.model.primary` in your config
- **Batch mode prevents hot-reload churn** — always use it for 2+ agents
