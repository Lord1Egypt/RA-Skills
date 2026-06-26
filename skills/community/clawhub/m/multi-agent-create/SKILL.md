---
name: multi-agent-create
description: Create new OpenClaw agents and connect them to messaging channels (Telegram, Discord, Slack, Feishu, WhatsApp, Signal, Google Chat). Includes workspace scaffolding and channel configuration guide.
tags:
  - create-agent
  - new-agent
  - multi-agent
  - add-agent
  - bot-setup
  - telegram-bot
  - discord-bot
  - slack-bot
  - feishu-bot
  - whatsapp-bot
  - signal-bot
---

# Multi-Agent Create

> **⚡ One-line install:**
> ```bash
> clawhub install multi-agent-create
> ```

Add a new AI agent to your OpenClaw gateway and connect it to any messaging channel.

---

## Interactive Workflow

When the user triggers this skill (e.g. "create a new agent", "add a bot"), follow this guided flow:

### Step 1: Ask for Agent Name & Channel

Prompt the user:

> 🤖 Let's create a new agent! First, tell me:
>
> 1. **Agent name** — What should this agent be called? (e.g. Luna, Marketing Bot)
> 2. **Which channel** do you want to connect it to?
>
> Supported channels:
> | # | Channel | Description |
> |---|---------|-------------|
> | 1 | **Telegram** | Telegram Bot |
> | 2 | **Discord** | Discord Bot |
> | 3 | **Slack** | Slack App |
> | 4 | **Feishu / Lark** | 飞书 / Lark Bot |
> | 5 | **WhatsApp** | WhatsApp (QR scan) |
> | 6 | **Signal** | Signal (QR scan) |
> | 7 | **Google Chat** | Google Workspace Bot |
>
> Reply with the agent name and channel number (or name), e.g. "Luna, Telegram"

Wait for the user's reply before proceeding.

### Step 2: Guide Credential Setup (per channel)

Based on the user's chosen channel, provide the specific credential instructions:

#### Telegram
> 🔑 **Get your Telegram Bot Token:**
> 1. Open Telegram and search for **@BotFather**
> 2. Send `/newbot` and follow the prompts to name your bot
> 3. BotFather will give you a **Bot Token** like `123456789:ABCdefGHI...`
> 4. Paste that token here

Required: `botToken`

#### Discord
> 🔑 **Get your Discord Bot Token:**
> 1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
> 2. Click **New Application** → name it → go to **Bot** tab
> 3. Click **Reset Token** and copy the token
> 4. Under **Privileged Gateway Intents**, enable **Message Content Intent**
> 5. Paste the token here

Required: `token`

#### Slack
> 🔑 **Get your Slack App credentials:**
> 1. Go to [Slack API](https://api.slack.com/apps) → **Create New App**
> 2. Enable **Socket Mode** → copy the **App-Level Token** (starts with `xapp-`)
> 3. Go to **OAuth & Permissions** → install to workspace → copy the **Bot Token** (starts with `xoxb-`)
> 4. Paste both tokens here

Required: `appToken`, `botToken`

#### Feishu / Lark
> 🔑 **获取飞书机器人凭证：**
> 1. 打开 [飞书开放平台](https://open.feishu.cn/) → **创建企业自建应用**
> 2. 在应用的 **凭证与基本信息** 页面找到 **App ID** 和 **App Secret**
> 3. 在 **机器人** 功能页启用机器人能力
> 4. 把 App ID 和 App Secret 发给我
>
> For **Lark** (international): same steps at [Lark Developer](https://open.larksuite.com/)

Required: `appId`, `appSecret` (add `"domain": "lark"` for Lark international)

#### WhatsApp
> 📱 **WhatsApp uses QR code login:**
> 1. I'll run the login command for you
> 2. A QR code will appear — scan it with your WhatsApp app
> 3. That's it!
>
> Ready? Just say "go" and I'll start the QR scan.

Action: run `openclaw channels login --channel whatsapp --account {name}`

#### Signal
> 📱 **Signal uses QR code login:**
> 1. I'll run the login command for you
> 2. A QR code will appear — scan it with your Signal app (Settings → Linked Devices)
> 3. That's it!
>
> Ready? Just say "go" and I'll start the QR scan.

Action: run `openclaw channels login --channel signal --account {name}`

#### Google Chat
> 🔑 **Get your Google Chat Service Account:**
> 1. Go to [Google Cloud Console](https://console.cloud.google.com/) → create/select a project
> 2. Enable the **Google Chat API**
> 3. Create a **Service Account** → download the JSON key file
> 4. Send me the path to the JSON file on this server

Required: `serviceAccountPath`

Wait for the user to provide credentials before proceeding.

### Step 3: Create Workspace

Run the helper script or create manually:

```bash
./scripts/setup-agent.sh {name} {channel}
```

This creates a workspace at `workspace-groups/{name}/` with standard files:
- `IDENTITY.md` — Name, role, emoji
- `SOUL.md` — Personality and behavior
- `AGENTS.md` — Startup instructions
- `USER.md` — Owner info
- `HEARTBEAT.md`, `TOOLS.md`

### Step 4: Register Agent

```bash
openclaw agents add {name}-agent
```

### Step 5: Configure Channel

Add account entry and binding to the gateway config.

**Binding format (all channels):**
```json
{
  "agentId": "{name}-agent",
  "match": {
    "channel": "{channel}",
    "accountId": "{name}"
  }
}
```

> Use `accountId` in the match block — not `account`.

**Channel account config reference:**

| Channel | Config Path | Required Fields |
|---------|------------|-----------------|
| Telegram | `channels.telegram.accounts.{name}` | `botToken` |
| Discord | `channels.discord.accounts.{name}` | `token` |
| Slack | `channels.slack.accounts.{name}` | `mode: "socket"`, `appToken`, `botToken` |
| Feishu | `channels.feishu.accounts.{name}` | `appId`, `appSecret` |
| WhatsApp | `channels.whatsapp.accounts.{name}` | QR scan via CLI |
| Signal | `channels.signal.accounts.{name}` | QR scan via CLI |
| Google Chat | `channels.googlechat.accounts.{name}` | `serviceAccountPath` |

### Step 6: Verify & Restart

```bash
openclaw gateway restart
openclaw agents list --bindings
openclaw channels status --probe
```

### Step 7: Pairing

For DM-based channels, the owner sends `/start` (or first message) to the bot, then approves:

```bash
openclaw pairing approve {channel} {CODE}
```

Report completion:
> ✅ Agent **{name}** is live on **{channel}**!
>
> - Workspace: `~/.openclaw/workspace-groups/{name}/`
> - All agents share your existing model API keys — no extra keys needed
> - Add more channels anytime by running this skill again

---

## Notes

- All agents share existing model credentials — no extra API keys needed
- One channel is enough to bring an agent online
- Add more channels later by repeating the workflow
