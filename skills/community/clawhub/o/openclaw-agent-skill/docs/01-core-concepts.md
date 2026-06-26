# Core Concepts & Architecture

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 42

---

<!-- SOURCE: https://docs.openclaw.ai/ -->

# OpenClaw - OpenClaw

![OpenClaw](https://mintcdn.com/clawdhub/-t5HSeZ3Y_0_wH4i/assets/openclaw-logo-text-dark.png?fit=max&auto=format&n=-t5HSeZ3Y_0_wH4i&q=85&s=61797dcb0c37d6e9279b8c5ad2e850e4)![OpenClaw](https://mintcdn.com/clawdhub/FaXdIfo7gPK_jSWb/assets/openclaw-logo-text.png?fit=max&auto=format&n=FaXdIfo7gPK_jSWb&q=85&s=d799bea41acb92d4c9fd1075c575879f)

> _“EXFOLIATE! EXFOLIATE!”_ — A space lobster, probably

**Any OS gateway for AI agents across WhatsApp, Telegram, Discord, iMessage, and more.**  
Send a message, get an agent response from your pocket. Plugins add Mattermost and more.

## What is OpenClaw?

OpenClaw is a **self-hosted gateway** that connects your favorite chat apps — WhatsApp, Telegram, Discord, iMessage, and more — to AI coding agents like Pi. You run a single Gateway process on your own machine (or a server), and it becomes the bridge between your messaging apps and an always-available AI assistant. **Who is it for?** Developers and power users who want a personal AI assistant they can message from anywhere — without giving up control of their data or relying on a hosted service. **What makes it different?**

*   **Self-hosted**: runs on your hardware, your rules
*   **Multi-channel**: one Gateway serves WhatsApp, Telegram, Discord, and more simultaneously
*   **Agent-native**: built for coding agents with tool use, sessions, memory, and multi-agent routing
*   **Open source**: MIT licensed, community-driven

**What do you need?** Node 22+, an API key from your chosen provider, and 5 minutes. For best quality and security, use the strongest latest-generation model available.

## How it works

The Gateway is the single source of truth for sessions, routing, and channel connections.

## Key capabilities

## Quick start

Need the full install and dev setup? See [Quick start](https://docs.openclaw.ai/start/quickstart).

## Dashboard

Open the browser Control UI after the Gateway starts.

*   Local default: [http://127.0.0.1:18789/](http://127.0.0.1:18789/)
*   Remote access: [Web surfaces](https://docs.openclaw.ai/web) and [Tailscale](https://docs.openclaw.ai/gateway/tailscale)

![OpenClaw](https://mintcdn.com/clawdhub/FaXdIfo7gPK_jSWb/whatsapp-openclaw.jpg?fit=max&auto=format&n=FaXdIfo7gPK_jSWb&q=85&s=b74a3630b0e971f466eff15fbdc642cb)

## Configuration (optional)

Config lives at `~/.openclaw/openclaw.json`.

*   If you **do nothing**, OpenClaw uses the bundled Pi binary in RPC mode with per-sender sessions.
*   If you want to lock it down, start with `channels.whatsapp.allowFrom` and (for groups) mention rules.

Example:

```
{
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
  messages: { groupChat: { mentionPatterns: ["@openclaw"] } },
}
```

## Start here

## Learn more

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/multi-agent -->

# Multi-Agent Routing - OpenClaw

Goal: multiple _isolated_ agents (separate workspace + `agentDir` + sessions), plus multiple channel accounts (e.g. two WhatsApps) in one running Gateway. Inbound is routed to an agent via bindings.

## What is “one agent”?

An **agent** is a fully scoped brain with its own:

*   **Workspace** (files, AGENTS.md/SOUL.md/USER.md, local notes, persona rules).
*   **State directory** (`agentDir`) for auth profiles, model registry, and per-agent config.
*   **Session store** (chat history + routing state) under `~/.openclaw/agents/<agentId>/sessions`.

Auth profiles are **per-agent**. Each agent reads from its own:

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

Main agent credentials are **not** shared automatically. Never reuse `agentDir` across agents (it causes auth/session collisions). If you want to share creds, copy `auth-profiles.json` into the other agent’s `agentDir`. Skills are per-agent via each workspace’s `skills/` folder, with shared skills available from `~/.openclaw/skills`. See [Skills: per-agent vs shared](https://docs.openclaw.ai/tools/skills#per-agent-vs-shared-skills). The Gateway can host **one agent** (default) or **many agents** side-by-side. **Workspace note:** each agent’s workspace is the **default cwd**, not a hard sandbox. Relative paths resolve inside the workspace, but absolute paths can reach other host locations unless sandboxing is enabled. See [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing).

## Paths (quick map)

*   Config: `~/.openclaw/openclaw.json` (or `OPENCLAW_CONFIG_PATH`)
*   State dir: `~/.openclaw` (or `OPENCLAW_STATE_DIR`)
*   Workspace: `~/.openclaw/workspace` (or `~/.openclaw/workspace-<agentId>`)
*   Agent dir: `~/.openclaw/agents/<agentId>/agent` (or `agents.list[].agentDir`)
*   Sessions: `~/.openclaw/agents/<agentId>/sessions`

### Single-agent mode (default)

If you do nothing, OpenClaw runs a single agent:

*   `agentId` defaults to **`main`**.
*   Sessions are keyed as `agent:main:<mainKey>`.
*   Workspace defaults to `~/.openclaw/workspace` (or `~/.openclaw/workspace-<profile>` when `OPENCLAW_PROFILE` is set).
*   State defaults to `~/.openclaw/agents/main/agent`.

## Agent helper

Use the agent wizard to add a new isolated agent:

Then add `bindings` (or let the wizard do it) to route inbound messages. Verify with:

```
openclaw agents list --bindings
```

## Quick start

## Multiple agents = multiple people, multiple personalities

With **multiple agents**, each `agentId` becomes a **fully isolated persona**:

*   **Different phone numbers/accounts** (per channel `accountId`).
*   **Different personalities** (per-agent workspace files like `AGENTS.md` and `SOUL.md`).
*   **Separate auth + sessions** (no cross-talk unless explicitly enabled).

This lets **multiple people** share one Gateway server while keeping their AI “brains” and data isolated.

## One WhatsApp number, multiple people (DM split)

You can route **different WhatsApp DMs** to different agents while staying on **one WhatsApp account**. Match on sender E.164 (like `+15551234567`) with `peer.kind: "direct"`. Replies still come from the same WhatsApp number (no per‑agent sender identity). Important detail: direct chats collapse to the agent’s **main session key**, so true isolation requires **one agent per person**. Example:

```
{
  agents: {
    list: [
      { id: "alex", workspace: "~/.openclaw/workspace-alex" },
      { id: "mia", workspace: "~/.openclaw/workspace-mia" },
    ],
  },
  bindings: [
    {
      agentId: "alex",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230001" } },
    },
    {
      agentId: "mia",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230002" } },
    },
  ],
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551230001", "+15551230002"],
    },
  },
}
```

Notes:

*   DM access control is **global per WhatsApp account** (pairing/allowlist), not per agent.
*   For shared groups, bind the group to one agent or use [Broadcast groups](https://docs.openclaw.ai/channels/broadcast-groups).

## Routing rules (how messages pick an agent)

Bindings are **deterministic** and **most-specific wins**:

1.  `peer` match (exact DM/group/channel id)
2.  `parentPeer` match (thread inheritance)
3.  `guildId + roles` (Discord role routing)
4.  `guildId` (Discord)
5.  `teamId` (Slack)
6.  `accountId` match for a channel
7.  channel-level match (`accountId: "*"`)
8.  fallback to default agent (`agents.list[].default`, else first list entry, default: `main`)

If multiple bindings match in the same tier, the first one in config order wins. If a binding sets multiple match fields (for example `peer` + `guildId`), all specified fields are required (`AND` semantics). Important account-scope detail:

*   A binding that omits `accountId` matches the default account only.
*   Use `accountId: "*"` for a channel-wide fallback across all accounts.
*   If you later add the same binding for the same agent with an explicit account id, OpenClaw upgrades the existing channel-only binding to account-scoped instead of duplicating it.

## Multiple accounts / phone numbers

Channels that support **multiple accounts** (e.g. WhatsApp) use `accountId` to identify each login. Each `accountId` can be routed to a different agent, so one server can host multiple phone numbers without mixing sessions. If you want a channel-wide default account when `accountId` is omitted, set `channels.<channel>.defaultAccount` (optional). When unset, OpenClaw falls back to `default` if present, otherwise the first configured account id (sorted). Common channels supporting this pattern include:

*   `whatsapp`, `telegram`, `discord`, `slack`, `signal`, `imessage`
*   `irc`, `line`, `googlechat`, `mattermost`, `matrix`, `nextcloud-talk`
*   `bluebubbles`, `zalo`, `zalouser`, `nostr`, `feishu`

## Concepts

*   `agentId`: one “brain” (workspace, per-agent auth, per-agent session store).
*   `accountId`: one channel account instance (e.g. WhatsApp account `"personal"` vs `"biz"`).
*   `binding`: routes inbound messages to an `agentId` by `(channel, accountId, peer)` and optionally guild/team ids.
*   Direct chats collapse to `agent:<agentId>:<mainKey>` (per-agent “main”; `session.mainKey`).

## Platform examples

### Discord bots per agent

Each Discord bot account maps to a unique `accountId`. Bind each account to an agent and keep allowlists per bot.

```
{
  agents: {
    list: [
      { id: "main", workspace: "~/.openclaw/workspace-main" },
      { id: "coding", workspace: "~/.openclaw/workspace-coding" },
    ],
  },
  bindings: [
    { agentId: "main", match: { channel: "discord", accountId: "default" } },
    { agentId: "coding", match: { channel: "discord", accountId: "coding" } },
  ],
  channels: {
    discord: {
      groupPolicy: "allowlist",
      accounts: {
        default: {
          token: "DISCORD_BOT_TOKEN_MAIN",
          guilds: {
            "123456789012345678": {
              channels: {
                "222222222222222222": { allow: true, requireMention: false },
              },
            },
          },
        },
        coding: {
          token: "DISCORD_BOT_TOKEN_CODING",
          guilds: {
            "123456789012345678": {
              channels: {
                "333333333333333333": { allow: true, requireMention: false },
              },
            },
          },
        },
      },
    },
  },
}
```

Notes:

*   Invite each bot to the guild and enable Message Content Intent.
*   Tokens live in `channels.discord.accounts.<id>.token` (default account can use `DISCORD_BOT_TOKEN`).

### Telegram bots per agent

```
{
  agents: {
    list: [
      { id: "main", workspace: "~/.openclaw/workspace-main" },
      { id: "alerts", workspace: "~/.openclaw/workspace-alerts" },
    ],
  },
  bindings: [
    { agentId: "main", match: { channel: "telegram", accountId: "default" } },
    { agentId: "alerts", match: { channel: "telegram", accountId: "alerts" } },
  ],
  channels: {
    telegram: {
      accounts: {
        default: {
          botToken: "123456:ABC...",
          dmPolicy: "pairing",
        },
        alerts: {
          botToken: "987654:XYZ...",
          dmPolicy: "allowlist",
          allowFrom: ["tg:123456789"],
        },
      },
    },
  },
}
```

Notes:

*   Create one bot per agent with BotFather and copy each token.
*   Tokens live in `channels.telegram.accounts.<id>.botToken` (default account can use `TELEGRAM_BOT_TOKEN`).

### WhatsApp numbers per agent

Link each account before starting the gateway:

```
openclaw channels login --channel whatsapp --account personal
openclaw channels login --channel whatsapp --account biz
```

`~/.openclaw/openclaw.json` (JSON5):

```
{
  agents: {
    list: [
      {
        id: "home",
        default: true,
        name: "Home",
        workspace: "~/.openclaw/workspace-home",
        agentDir: "~/.openclaw/agents/home/agent",
      },
      {
        id: "work",
        name: "Work",
        workspace: "~/.openclaw/workspace-work",
        agentDir: "~/.openclaw/agents/work/agent",
      },
    ],
  },

  // Deterministic routing: first match wins (most-specific first).
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },

    // Optional per-peer override (example: send a specific group to work agent).
    {
      agentId: "work",
      match: {
        channel: "whatsapp",
        accountId: "personal",
        peer: { kind: "group", id: "1203630...@g.us" },
      },
    },
  ],

  // Off by default: agent-to-agent messaging must be explicitly enabled + allowlisted.
  tools: {
    agentToAgent: {
      enabled: false,
      allow: ["home", "work"],
    },
  },

  channels: {
    whatsapp: {
      accounts: {
        personal: {
          // Optional override. Default: ~/.openclaw/credentials/whatsapp/personal
          // authDir: "~/.openclaw/credentials/whatsapp/personal",
        },
        biz: {
          // Optional override. Default: ~/.openclaw/credentials/whatsapp/biz
          // authDir: "~/.openclaw/credentials/whatsapp/biz",
        },
      },
    },
  },
}
```

## Example: WhatsApp daily chat + Telegram deep work

Split by channel: route WhatsApp to a fast everyday agent and Telegram to an Opus agent.

```
{
  agents: {
    list: [
      {
        id: "chat",
        name: "Everyday",
        workspace: "~/.openclaw/workspace-chat",
        model: "anthropic/claude-sonnet-4-5",
      },
      {
        id: "opus",
        name: "Deep Work",
        workspace: "~/.openclaw/workspace-opus",
        model: "anthropic/claude-opus-4-6",
      },
    ],
  },
  bindings: [
    { agentId: "chat", match: { channel: "whatsapp" } },
    { agentId: "opus", match: { channel: "telegram" } },
  ],
}
```

Notes:

*   If you have multiple accounts for a channel, add `accountId` to the binding (for example `{ channel: "whatsapp", accountId: "personal" }`).
*   To route a single DM/group to Opus while keeping the rest on chat, add a `match.peer` binding for that peer; peer matches always win over channel-wide rules.

## Example: same channel, one peer to Opus

Keep WhatsApp on the fast agent, but route one DM to Opus:

```
{
  agents: {
    list: [
      {
        id: "chat",
        name: "Everyday",
        workspace: "~/.openclaw/workspace-chat",
        model: "anthropic/claude-sonnet-4-5",
      },
      {
        id: "opus",
        name: "Deep Work",
        workspace: "~/.openclaw/workspace-opus",
        model: "anthropic/claude-opus-4-6",
      },
    ],
  },
  bindings: [
    {
      agentId: "opus",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551234567" } },
    },
    { agentId: "chat", match: { channel: "whatsapp" } },
  ],
}
```

Peer bindings always win, so keep them above the channel-wide rule.

## Family agent bound to a WhatsApp group

Bind a dedicated family agent to a single WhatsApp group, with mention gating and a tighter tool policy:

```
{
  agents: {
    list: [
      {
        id: "family",
        name: "Family",
        workspace: "~/.openclaw/workspace-family",
        identity: { name: "Family Bot" },
        groupChat: {
          mentionPatterns: ["@family", "@familybot", "@Family Bot"],
        },
        sandbox: {
          mode: "all",
          scope: "agent",
        },
        tools: {
          allow: [
            "exec",
            "read",
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
          ],
          deny: ["write", "edit", "apply_patch", "browser", "canvas", "nodes", "cron"],
        },
      },
    ],
  },
  bindings: [
    {
      agentId: "family",
      match: {
        channel: "whatsapp",
        peer: { kind: "group", id: "120363999999999999@g.us" },
      },
    },
  ],
}
```

Notes:

*   Tool allow/deny lists are **tools**, not skills. If a skill needs to run a binary, ensure `exec` is allowed and the binary exists in the sandbox.
*   For stricter gating, set `agents.list[].groupChat.mentionPatterns` and keep group allowlists enabled for the channel.

Starting with v2026.1.6, each agent can have its own sandbox and tool restrictions:

```
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: {
          mode: "off",  // No sandbox for personal agent
        },
        // No tool restrictions - all tools available
      },
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: {
          mode: "all",     // Always sandboxed
          scope: "agent",  // One container per agent
          docker: {
            // Optional one-time setup after container creation
            setupCommand: "apt-get update && apt-get install -y git curl",
          },
        },
        tools: {
          allow: ["read"],                    // Only read tool
          deny: ["exec", "write", "edit", "apply_patch"],    // Deny others
        },
      },
    ],
  },
}
```

Note: `setupCommand` lives under `sandbox.docker` and runs once on container creation. Per-agent `sandbox.docker.*` overrides are ignored when the resolved scope is `"shared"`. **Benefits:**

*   **Security isolation**: Restrict tools for untrusted agents
*   **Resource control**: Sandbox specific agents while keeping others on host
*   **Flexible policies**: Different permissions per agent

Note: `tools.elevated` is **global** and sender-based; it is not configurable per agent. If you need per-agent boundaries, use `agents.list[].tools` to deny `exec`. For group targeting, use `agents.list[].groupChat.mentionPatterns` so @mentions map cleanly to the intended agent. See [Multi-Agent Sandbox & Tools](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools) for detailed examples.

---

<!-- SOURCE: https://docs.openclaw.ai/start/onboarding-overview -->

# Onboarding Overview - OpenClaw

OpenClaw supports multiple onboarding paths depending on where the Gateway runs and how you prefer to configure providers.

## Choose your onboarding path

*   **CLI wizard** for macOS, Linux, and Windows (via WSL2).
*   **macOS app** for a guided first run on Apple silicon or Intel Macs.

## CLI onboarding wizard

Run the wizard in a terminal:

Use the CLI wizard when you want full control of the Gateway, workspace, channels, and skills. Docs:

*   [Onboarding Wizard (CLI)](https://docs.openclaw.ai/start/wizard)
*   [`openclaw onboard` command](https://docs.openclaw.ai/cli/onboard)

## macOS app onboarding

Use the OpenClaw app when you want a fully guided setup on macOS. Docs:

*   [Onboarding (macOS App)](https://docs.openclaw.ai/start/onboarding)

## Custom Provider

If you need an endpoint that is not listed, including hosted providers that expose standard OpenAI or Anthropic APIs, choose **Custom Provider** in the CLI wizard. You will be asked to:

*   Pick OpenAI-compatible, Anthropic-compatible, or **Unknown** (auto-detect).
*   Enter a base URL and API key (if required by the provider).
*   Provide a model ID and optional alias.
*   Choose an Endpoint ID so multiple custom endpoints can coexist.

For detailed steps, follow the CLI onboarding docs above.

---

<!-- SOURCE: https://docs.openclaw.ai/start/getting-started -->

# Getting Started - OpenClaw

Goal: go from zero to a first working chat with minimal setup.

## Prereqs

*   Node 22 or newer

## Quick setup (CLI)

## Optional checks and extras

## Useful environment variables

If you run OpenClaw as a service account or want custom config/state locations:

*   `OPENCLAW_HOME` sets the home directory used for internal path resolution.
*   `OPENCLAW_STATE_DIR` overrides the state directory.
*   `OPENCLAW_CONFIG_PATH` overrides the config file path.

Full environment variable reference: [Environment vars](https://docs.openclaw.ai/help/environment).

## Go deeper

## What you will have

*   A running Gateway
*   Auth configured
*   Control UI access or a connected channel

## Next steps

*   DM safety and approvals: [Pairing](https://docs.openclaw.ai/channels/pairing)
*   Connect more channels: [Channels](https://docs.openclaw.ai/channels)
*   Advanced workflows and from source: [Setup](https://docs.openclaw.ai/start/setup)

---

<!-- SOURCE: https://docs.openclaw.ai/start/wizard-cli-automation -->

# CLI Automation - OpenClaw

Use `--non-interactive` to automate `openclaw onboard`.

## Baseline non-interactive example

```
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --secret-input-mode plaintext \
  --gateway-port 18789 \
  --gateway-bind loopback \
  --install-daemon \
  --daemon-runtime node \
  --skip-skills
```

Add `--json` for a machine-readable summary. Use `--secret-input-mode ref` to store env-backed refs in auth profiles instead of plaintext values. Interactive selection between env refs and configured provider refs (`file` or `exec`) is available in the onboarding wizard flow. In non-interactive `ref` mode, provider env vars must be set in the process environment. Passing inline key flags without the matching env var now fails fast. Example:

```
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice openai-api-key \
  --secret-input-mode ref \
  --accept-risk
```

## Provider-specific examples

## Add another agent

Use `openclaw agents add <name>` to create a separate agent with its own workspace, sessions, and auth profiles. Running without `--workspace` launches the wizard.

```
openclaw agents add work \
  --workspace ~/.openclaw/workspace-work \
  --model openai/gpt-5.2 \
  --bind whatsapp:biz \
  --non-interactive \
  --json
```

What it sets:

*   `agents.list[].name`
*   `agents.list[].workspace`
*   `agents.list[].agentDir`

Notes:

*   Default workspaces follow `~/.openclaw/workspace-<agentId>`.
*   Add `bindings` to route inbound messages (the wizard can do this).
*   Non-interactive flags: `--model`, `--agent-dir`, `--bind`, `--non-interactive`.

*   Onboarding hub: [Onboarding Wizard (CLI)](https://docs.openclaw.ai/start/wizard)
*   Full reference: [CLI Onboarding Reference](https://docs.openclaw.ai/start/wizard-cli-reference)
*   Command reference: [`openclaw onboard`](https://docs.openclaw.ai/cli/onboard)

---

<!-- SOURCE: https://docs.openclaw.ai/start/wizard -->

# Onboarding Wizard (CLI) - OpenClaw

The onboarding wizard is the **recommended** way to set up OpenClaw on macOS, Linux, or Windows (via WSL2; strongly recommended). It configures a local Gateway or a remote Gateway connection, plus channels, skills, and workspace defaults in one guided flow.

To reconfigure later:

```
openclaw configure
openclaw agents add <name>
```

## QuickStart vs Advanced

The wizard starts with **QuickStart** (defaults) vs **Advanced** (full control).

*   QuickStart (defaults)
    
*   Advanced (full control)
    

*   Local gateway (loopback)
*   Workspace default (or existing workspace)
*   Gateway port **18789**
*   Gateway auth **Token** (auto‑generated, even on loopback)
*   Tool policy default for new local setups: `tools.profile: "coding"` (existing explicit profile is preserved)
*   DM isolation default: local onboarding writes `session.dmScope: "per-channel-peer"` when unset. Details: [CLI Onboarding Reference](https://docs.openclaw.ai/start/wizard-cli-reference#outputs-and-internals)
*   Tailscale exposure **Off**
*   Telegram + WhatsApp DMs default to **allowlist** (you’ll be prompted for your phone number)

*   Exposes every step (mode, workspace, gateway, channels, daemon, skills).

## What the wizard configures

**Local mode (default)** walks you through these steps:

1.  **Model/Auth** — choose any supported provider/auth flow (API key, OAuth, or setup-token), including Custom Provider (OpenAI-compatible, Anthropic-compatible, or Unknown auto-detect). Pick a default model. Security note: if this agent will run tools or process webhook/hooks content, prefer the strongest latest-generation model available and keep tool policy strict. Weaker/older tiers are easier to prompt-inject. For non-interactive runs, `--secret-input-mode ref` stores env-backed refs in auth profiles instead of plaintext API key values. In non-interactive `ref` mode, the provider env var must be set; passing inline key flags without that env var fails fast. In interactive runs, choosing secret reference mode lets you point at either an environment variable or a configured provider ref (`file` or `exec`), with a fast preflight validation before saving.
2.  **Workspace** — Location for agent files (default `~/.openclaw/workspace`). Seeds bootstrap files.
3.  **Gateway** — Port, bind address, auth mode, Tailscale exposure. In interactive token mode, choose default plaintext token storage or opt into SecretRef. Non-interactive token SecretRef path: `--gateway-token-ref-env <ENV_VAR>`.
4.  **Channels** — WhatsApp, Telegram, Discord, Google Chat, Mattermost, Signal, BlueBubbles, or iMessage.
5.  **Daemon** — Installs a LaunchAgent (macOS) or systemd user unit (Linux/WSL2). If token auth requires a token and `gateway.auth.token` is SecretRef-managed, daemon install validates it but does not persist the resolved token into supervisor service environment metadata. If token auth requires a token and the configured token SecretRef is unresolved, daemon install is blocked with actionable guidance. If both `gateway.auth.token` and `gateway.auth.password` are configured and `gateway.auth.mode` is unset, daemon install is blocked until mode is set explicitly.
6.  **Health check** — Starts the Gateway and verifies it’s running.
7.  **Skills** — Installs recommended skills and optional dependencies.

**Remote mode** only configures the local client to connect to a Gateway elsewhere. It does **not** install or change anything on the remote host.

## Add another agent

Use `openclaw agents add <name>` to create a separate agent with its own workspace, sessions, and auth profiles. Running without `--workspace` launches the wizard. What it sets:

*   `agents.list[].name`
*   `agents.list[].workspace`
*   `agents.list[].agentDir`

Notes:

*   Default workspaces follow `~/.openclaw/workspace-<agentId>`.
*   Add `bindings` to route inbound messages (the wizard can do this).
*   Non-interactive flags: `--model`, `--agent-dir`, `--bind`, `--non-interactive`.

## Full reference

For detailed step-by-step breakdowns, non-interactive scripting, Signal setup, RPC API, and a full list of config fields the wizard writes, see the [Wizard Reference](https://docs.openclaw.ai/reference/wizard).

*   CLI command reference: [`openclaw onboard`](https://docs.openclaw.ai/cli/onboard)
*   Onboarding overview: [Onboarding Overview](https://docs.openclaw.ai/start/onboarding-overview)
*   macOS app onboarding: [Onboarding](https://docs.openclaw.ai/start/onboarding)
*   Agent first-run ritual: [Agent Bootstrapping](https://docs.openclaw.ai/start/bootstrapping)

---

<!-- SOURCE: https://docs.openclaw.ai/start/onboarding -->

# Onboarding (macOS App) - OpenClaw

This doc describes the **current** first‑run onboarding flow. The goal is a smooth “day 0” experience: pick where the Gateway runs, connect auth, run the wizard, and let the agent bootstrap itself. For a general overview of onboarding paths, see [Onboarding Overview](https://docs.openclaw.ai/start/onboarding-overview).

---

<!-- SOURCE: https://docs.openclaw.ai/start/openclaw -->

# Personal Assistant Setup - OpenClaw

## Building a personal assistant with OpenClaw

OpenClaw is a WhatsApp + Telegram + Discord + iMessage gateway for **Pi** agents. Plugins add Mattermost. This guide is the “personal assistant” setup: one dedicated WhatsApp number that behaves like your always-on agent.

## ⚠️ Safety first

You’re putting an agent in a position to:

*   run commands on your machine (depending on your Pi tool setup)
*   read/write files in your workspace
*   send messages back out via WhatsApp/Telegram/Discord/Mattermost (plugin)

Start conservative:

*   Always set `channels.whatsapp.allowFrom` (never run open-to-the-world on your personal Mac).
*   Use a dedicated WhatsApp number for the assistant.
*   Heartbeats now default to every 30 minutes. Disable until you trust the setup by setting `agents.defaults.heartbeat.every: "0m"`.

## Prerequisites

*   OpenClaw installed and onboarded — see [Getting Started](https://docs.openclaw.ai/start/getting-started) if you haven’t done this yet
*   A second phone number (SIM/eSIM/prepaid) for the assistant

## The two-phone setup (recommended)

You want this:

If you link your personal WhatsApp to OpenClaw, every message to you becomes “agent input”. That’s rarely what you want.

## 5-minute quick start

1.  Pair WhatsApp Web (shows QR; scan with the assistant phone):

2.  Start the Gateway (leave it running):

```
openclaw gateway --port 18789
```

3.  Put a minimal config in `~/.openclaw/openclaw.json`:

```
{
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

Now message the assistant number from your allowlisted phone. When onboarding finishes, we auto-open the dashboard and print a clean (non-tokenized) link. If it prompts for auth, paste the token from `gateway.auth.token` into Control UI settings. To reopen later: `openclaw dashboard`.

## Give the agent a workspace (AGENTS)

OpenClaw reads operating instructions and “memory” from its workspace directory. By default, OpenClaw uses `~/.openclaw/workspace` as the agent workspace, and will create it (plus starter `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`) automatically on setup/first agent run. `BOOTSTRAP.md` is only created when the workspace is brand new (it should not come back after you delete it). `MEMORY.md` is optional (not auto-created); when present, it is loaded for normal sessions. Subagent sessions only inject `AGENTS.md` and `TOOLS.md`. Tip: treat this folder like OpenClaw’s “memory” and make it a git repo (ideally private) so your `AGENTS.md` + memory files are backed up. If git is installed, brand-new workspaces are auto-initialized.

Full workspace layout + backup guide: [Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace) Memory workflow: [Memory](https://docs.openclaw.ai/concepts/memory) Optional: choose a different workspace with `agents.defaults.workspace` (supports `~`).

```
{
  agent: {
    workspace: "~/.openclaw/workspace",
  },
}
```

If you already ship your own workspace files from a repo, you can disable bootstrap file creation entirely:

```
{
  agent: {
    skipBootstrap: true,
  },
}
```

## The config that turns it into “an assistant”

OpenClaw defaults to a good assistant setup, but you’ll usually want to tune:

*   persona/instructions in `SOUL.md`
*   thinking defaults (if desired)
*   heartbeats (once you trust it)

Example:

```
{
  logging: { level: "info" },
  agent: {
    model: "anthropic/claude-opus-4-6",
    workspace: "~/.openclaw/workspace",
    thinkingDefault: "high",
    timeoutSeconds: 1800,
    // Start with 0; enable later.
    heartbeat: { every: "0m" },
  },
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: {
        "*": { requireMention: true },
      },
    },
  },
  routing: {
    groupChat: {
      mentionPatterns: ["@openclaw", "openclaw"],
    },
  },
  session: {
    scope: "per-sender",
    resetTriggers: ["/new", "/reset"],
    reset: {
      mode: "daily",
      atHour: 4,
      idleMinutes: 10080,
    },
  },
}
```

## Sessions and memory

*   Session files: `~/.openclaw/agents/<agentId>/sessions/{{SessionId}}.jsonl`
*   Session metadata (token usage, last route, etc): `~/.openclaw/agents/<agentId>/sessions/sessions.json` (legacy: `~/.openclaw/sessions/sessions.json`)
*   `/new` or `/reset` starts a fresh session for that chat (configurable via `resetTriggers`). If sent alone, the agent replies with a short hello to confirm the reset.
*   `/compact [instructions]` compacts the session context and reports the remaining context budget.

## Heartbeats (proactive mode)

By default, OpenClaw runs a heartbeat every 30 minutes with the prompt: `Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.` Set `agents.defaults.heartbeat.every: "0m"` to disable.

*   If `HEARTBEAT.md` exists but is effectively empty (only blank lines and markdown headers like `# Heading`), OpenClaw skips the heartbeat run to save API calls.
*   If the file is missing, the heartbeat still runs and the model decides what to do.
*   If the agent replies with `HEARTBEAT_OK` (optionally with short padding; see `agents.defaults.heartbeat.ackMaxChars`), OpenClaw suppresses outbound delivery for that heartbeat.
*   By default, heartbeat delivery to DM-style `user:<id>` targets is allowed. Set `agents.defaults.heartbeat.directPolicy: "block"` to suppress direct-target delivery while keeping heartbeat runs active.
*   Heartbeats run full agent turns — shorter intervals burn more tokens.

```
{
  agent: {
    heartbeat: { every: "30m" },
  },
}
```

Inbound attachments (images/audio/docs) can be surfaced to your command via templates:

*   `{{MediaPath}}` (local temp file path)
*   `{{MediaUrl}}` (pseudo-URL)
*   `{{Transcript}}` (if audio transcription is enabled)

Outbound attachments from the agent: include `MEDIA:<path-or-url>` on its own line (no spaces). Example:

```
Here’s the screenshot.
MEDIA:https://example.com/screenshot.png
```

OpenClaw extracts these and sends them as media alongside the text.

## Operations checklist

```
openclaw status          # local status (creds, sessions, queued events)
openclaw status --all    # full diagnosis (read-only, pasteable)
openclaw status --deep   # adds gateway health probes (Telegram + Discord)
openclaw health --json   # gateway health snapshot (WS)
```

Logs live under `/tmp/openclaw/` (default: `openclaw-YYYY-MM-DD.log`).

## Next steps

*   WebChat: [WebChat](https://docs.openclaw.ai/web/webchat)
*   Gateway ops: [Gateway runbook](https://docs.openclaw.ai/gateway)
*   Cron + wakeups: [Cron jobs](https://docs.openclaw.ai/automation/cron-jobs)
*   macOS menu bar companion: [OpenClaw macOS app](https://docs.openclaw.ai/platforms/macos)
*   iOS node app: [iOS app](https://docs.openclaw.ai/platforms/ios)
*   Android node app: [Android app](https://docs.openclaw.ai/platforms/android)
*   Windows status: [Windows (WSL2)](https://docs.openclaw.ai/platforms/windows)
*   Linux status: [Linux app](https://docs.openclaw.ai/platforms/linux)
*   Security: [Security](https://docs.openclaw.ai/gateway/security)

---

<!-- SOURCE: https://docs.openclaw.ai/start/wizard-cli-reference -->

# CLI Onboarding Reference - OpenClaw

This page is the full reference for `openclaw onboard`. For the short guide, see [Onboarding Wizard (CLI)](https://docs.openclaw.ai/start/wizard).

## What the wizard does

Local mode (default) walks you through:

*   Model and auth setup (OpenAI Code subscription OAuth, Anthropic API key or setup token, plus MiniMax, GLM, Moonshot, and AI Gateway options)
*   Workspace location and bootstrap files
*   Gateway settings (port, bind, auth, tailscale)
*   Channels and providers (Telegram, WhatsApp, Discord, Google Chat, Mattermost plugin, Signal)
*   Daemon install (LaunchAgent or systemd user unit)
*   Health check
*   Skills setup

Remote mode configures this machine to connect to a gateway elsewhere. It does not install or modify anything on the remote host.

## Local flow details

## Remote mode details

Remote mode configures this machine to connect to a gateway elsewhere.

What you set:

*   Remote gateway URL (`ws://...`)
*   Token if remote gateway auth is required (recommended)

## Auth and model options

Model behavior:

*   Pick default model from detected options, or enter provider and model manually.
*   Wizard runs a model check and warns if the configured model is unknown or missing auth.

Credential and profile paths:

*   OAuth credentials: `~/.openclaw/credentials/oauth.json`
*   Auth profiles (API keys + OAuth): `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`

Credential storage mode:

*   Default onboarding behavior persists API keys as plaintext values in auth profiles.
*   `--secret-input-mode ref` enables reference mode instead of plaintext key storage. In interactive onboarding, you can choose either:
    *   environment variable ref (for example `keyRef: { source: "env", provider: "default", id: "OPENAI_API_KEY" }`)
    *   configured provider ref (`file` or `exec`) with provider alias + id
*   Interactive reference mode runs a fast preflight validation before saving.
    *   Env refs: validates variable name + non-empty value in the current onboarding environment.
    *   Provider refs: validates provider config and resolves the requested id.
    *   If preflight fails, onboarding shows the error and lets you retry.
*   In non-interactive mode, `--secret-input-mode ref` is env-backed only.
    *   Set the provider env var in the onboarding process environment.
    *   Inline key flags (for example `--openai-api-key`) require that env var to be set; otherwise onboarding fails fast.
    *   For custom providers, non-interactive `ref` mode stores `models.providers.<id>.apiKey` as `{ source: "env", provider: "default", id: "CUSTOM_API_KEY" }`.
    *   In that custom-provider case, `--custom-api-key` requires `CUSTOM_API_KEY` to be set; otherwise onboarding fails fast.
*   Gateway auth credentials support plaintext and SecretRef choices in interactive onboarding:
    *   Token mode: **Generate/store plaintext token** (default) or **Use SecretRef**.
    *   Password mode: plaintext or SecretRef.
*   Non-interactive token SecretRef path: `--gateway-token-ref-env <ENV_VAR>`.
*   Existing plaintext setups continue to work unchanged.

## Outputs and internals

Typical fields in `~/.openclaw/openclaw.json`:

*   `agents.defaults.workspace`
*   `agents.defaults.model` / `models.providers` (if Minimax chosen)
*   `tools.profile` (local onboarding defaults to `"coding"` when unset; existing explicit values are preserved)
*   `gateway.*` (mode, bind, auth, tailscale)
*   `session.dmScope` (local onboarding defaults this to `per-channel-peer` when unset; existing explicit values are preserved)
*   `channels.telegram.botToken`, `channels.discord.token`, `channels.signal.*`, `channels.imessage.*`
*   Channel allowlists (Slack, Discord, Matrix, Microsoft Teams) when you opt in during prompts (names resolve to IDs when possible)
*   `skills.install.nodeManager`
*   `wizard.lastRunAt`
*   `wizard.lastRunVersion`
*   `wizard.lastRunCommit`
*   `wizard.lastRunCommand`
*   `wizard.lastRunMode`

`openclaw agents add` writes `agents.list[]` and optional `bindings`. WhatsApp credentials go under `~/.openclaw/credentials/whatsapp/<accountId>/`. Sessions are stored under `~/.openclaw/agents/<agentId>/sessions/`.

Gateway wizard RPC:

*   `wizard.start`
*   `wizard.next`
*   `wizard.cancel`
*   `wizard.status`

Clients (macOS app and Control UI) can render steps without re-implementing onboarding logic. Signal setup behavior:

*   Downloads the appropriate release asset
*   Stores it under `~/.openclaw/tools/signal-cli/<version>/`
*   Writes `channels.signal.cliPath` in config
*   JVM builds require Java 21
*   Native builds are used when available
*   Windows uses WSL2 and follows Linux signal-cli flow inside WSL

*   Onboarding hub: [Onboarding Wizard (CLI)](https://docs.openclaw.ai/start/wizard)
*   Automation and scripts: [CLI Automation](https://docs.openclaw.ai/start/wizard-cli-automation)
*   Command reference: [`openclaw onboard`](https://docs.openclaw.ai/cli/onboard)

---

<!-- SOURCE: https://docs.openclaw.ai/start/hubs -->

# Docs Hubs - OpenClaw

Use these hubs to discover every page, including deep dives and reference docs that don’t appear in the left nav.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/agent -->

# Agent Runtime - OpenClaw

OpenClaw runs a single embedded agent runtime derived from **pi-mono**.

## Workspace (required)

OpenClaw uses a single agent workspace directory (`agents.defaults.workspace`) as the agent’s **only** working directory (`cwd`) for tools and context. Recommended: use `openclaw setup` to create `~/.openclaw/openclaw.json` if missing and initialize the workspace files. Full workspace layout + backup guide: [Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace) If `agents.defaults.sandbox` is enabled, non-main sessions can override this with per-session workspaces under `agents.defaults.sandbox.workspaceRoot` (see [Gateway configuration](https://docs.openclaw.ai/gateway/configuration)).

## Bootstrap files (injected)

Inside `agents.defaults.workspace`, OpenClaw expects these user-editable files:

*   `AGENTS.md` — operating instructions + “memory”
*   `SOUL.md` — persona, boundaries, tone
*   `TOOLS.md` — user-maintained tool notes (e.g. `imsg`, `sag`, conventions)
*   `BOOTSTRAP.md` — one-time first-run ritual (deleted after completion)
*   `IDENTITY.md` — agent name/vibe/emoji
*   `USER.md` — user profile + preferred address

On the first turn of a new session, OpenClaw injects the contents of these files directly into the agent context. Blank files are skipped. Large files are trimmed and truncated with a marker so prompts stay lean (read the file for full content). If a file is missing, OpenClaw injects a single “missing file” marker line (and `openclaw setup` will create a safe default template). `BOOTSTRAP.md` is only created for a **brand new workspace** (no other bootstrap files present). If you delete it after completing the ritual, it should not be recreated on later restarts. To disable bootstrap file creation entirely (for pre-seeded workspaces), set:

```
{ agent: { skipBootstrap: true } }
```

Core tools (read/exec/edit/write and related system tools) are always available, subject to tool policy. `apply_patch` is optional and gated by `tools.exec.applyPatch`. `TOOLS.md` does **not** control which tools exist; it’s guidance for how _you_ want them used.

## Skills

OpenClaw loads skills from three locations (workspace wins on name conflict):

*   Bundled (shipped with the install)
*   Managed/local: `~/.openclaw/skills`
*   Workspace: `<workspace>/skills`

Skills can be gated by config/env (see `skills` in [Gateway configuration](https://docs.openclaw.ai/gateway/configuration)).

## pi-mono integration

OpenClaw reuses pieces of the pi-mono codebase (models/tools), but **session management, discovery, and tool wiring are OpenClaw-owned**.

*   No pi-coding agent runtime.
*   No `~/.pi/agent` or `<workspace>/.pi` settings are consulted.

## Sessions

Session transcripts are stored as JSONL at:

*   `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`

The session ID is stable and chosen by OpenClaw. Legacy Pi/Tau session folders are **not** read.

## Steering while streaming

When queue mode is `steer`, inbound messages are injected into the current run. The queue is checked **after each tool call**; if a queued message is present, remaining tool calls from the current assistant message are skipped (error tool results with “Skipped due to queued user message.”), then the queued user message is injected before the next assistant response. When queue mode is `followup` or `collect`, inbound messages are held until the current turn ends, then a new agent turn starts with the queued payloads. See [Queue](https://docs.openclaw.ai/concepts/queue) for mode + debounce/cap behavior. Block streaming sends completed assistant blocks as soon as they finish; it is **off by default** (`agents.defaults.blockStreamingDefault: "off"`). Tune the boundary via `agents.defaults.blockStreamingBreak` (`text_end` vs `message_end`; defaults to text\_end). Control soft block chunking with `agents.defaults.blockStreamingChunk` (defaults to 800–1200 chars; prefers paragraph breaks, then newlines; sentences last). Coalesce streamed chunks with `agents.defaults.blockStreamingCoalesce` to reduce single-line spam (idle-based merging before send). Non-Telegram channels require explicit `*.blockStreaming: true` to enable block replies. Verbose tool summaries are emitted at tool start (no debounce); Control UI streams tool output via agent events when available. More details: [Streaming + chunking](https://docs.openclaw.ai/concepts/streaming).

## Model refs

Model refs in config (for example `agents.defaults.model` and `agents.defaults.models`) are parsed by splitting on the **first** `/`.

*   Use `provider/model` when configuring models.
*   If the model ID itself contains `/` (OpenRouter-style), include the provider prefix (example: `openrouter/moonshotai/kimi-k2`).
*   If you omit the provider, OpenClaw treats the input as an alias or a model for the **default provider** (only works when there is no `/` in the model ID).

## Configuration (minimal)

At minimum, set:

*   `agents.defaults.workspace`
*   `channels.whatsapp.allowFrom` (strongly recommended)

* * *

_Next: [Group Chats](https://docs.openclaw.ai/channels/group-messages)_ 🦞

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/agent-loop -->

# Agent Loop - OpenClaw

An agentic loop is the full “real” run of an agent: intake → context assembly → model inference → tool execution → streaming replies → persistence. It’s the authoritative path that turns a message into actions and a final reply, while keeping session state consistent. In OpenClaw, a loop is a single, serialized run per session that emits lifecycle and stream events as the model thinks, calls tools, and streams output. This doc explains how that authentic loop is wired end-to-end.

## Entry points

*   Gateway RPC: `agent` and `agent.wait`.
*   CLI: `agent` command.

## How it works (high-level)

1.  `agent` RPC validates params, resolves session (sessionKey/sessionId), persists session metadata, returns `{ runId, acceptedAt }` immediately.
2.  `agentCommand` runs the agent:
    *   resolves model + thinking/verbose defaults
    *   loads skills snapshot
    *   calls `runEmbeddedPiAgent` (pi-agent-core runtime)
    *   emits **lifecycle end/error** if the embedded loop does not emit one
3.  `runEmbeddedPiAgent`:
    *   serializes runs via per-session + global queues
    *   resolves model + auth profile and builds the pi session
    *   subscribes to pi events and streams assistant/tool deltas
    *   enforces timeout -> aborts run if exceeded
    *   returns payloads + usage metadata
4.  `subscribeEmbeddedPiSession` bridges pi-agent-core events to OpenClaw `agent` stream:
    *   tool events => `stream: "tool"`
    *   assistant deltas => `stream: "assistant"`
    *   lifecycle events => `stream: "lifecycle"` (`phase: "start" | "end" | "error"`)
5.  `agent.wait` uses `waitForAgentJob`:
    *   waits for **lifecycle end/error** for `runId`
    *   returns `{ status: ok|error|timeout, startedAt, endedAt, error? }`

## Queueing + concurrency

*   Runs are serialized per session key (session lane) and optionally through a global lane.
*   This prevents tool/session races and keeps session history consistent.
*   Messaging channels can choose queue modes (collect/steer/followup) that feed this lane system. See [Command Queue](https://docs.openclaw.ai/concepts/queue).

## Session + workspace preparation

*   Workspace is resolved and created; sandboxed runs may redirect to a sandbox workspace root.
*   Skills are loaded (or reused from a snapshot) and injected into env and prompt.
*   Bootstrap/context files are resolved and injected into the system prompt report.
*   A session write lock is acquired; `SessionManager` is opened and prepared before streaming.

## Prompt assembly + system prompt

*   System prompt is built from OpenClaw’s base prompt, skills prompt, bootstrap context, and per-run overrides.
*   Model-specific limits and compaction reserve tokens are enforced.
*   See [System prompt](https://docs.openclaw.ai/concepts/system-prompt) for what the model sees.

## Hook points (where you can intercept)

OpenClaw has two hook systems:

*   **Internal hooks** (Gateway hooks): event-driven scripts for commands and lifecycle events.
*   **Plugin hooks**: extension points inside the agent/tool lifecycle and gateway pipeline.

### Internal hooks (Gateway hooks)

*   **`agent:bootstrap`**: runs while building bootstrap files before the system prompt is finalized. Use this to add/remove bootstrap context files.
*   **Command hooks**: `/new`, `/reset`, `/stop`, and other command events (see Hooks doc).

See [Hooks](https://docs.openclaw.ai/automation/hooks) for setup and examples.

### Plugin hooks (agent + gateway lifecycle)

These run inside the agent loop or gateway pipeline:

*   **`before_model_resolve`**: runs pre-session (no `messages`) to deterministically override provider/model before model resolution.
*   **`before_prompt_build`**: runs after session load (with `messages`) to inject `prependContext`, `systemPrompt`, `prependSystemContext`, or `appendSystemContext` before prompt submission. Use `prependContext` for per-turn dynamic text and system-context fields for stable guidance that should sit in system prompt space.
*   **`before_agent_start`**: legacy compatibility hook that may run in either phase; prefer the explicit hooks above.
*   **`agent_end`**: inspect the final message list and run metadata after completion.
*   **`before_compaction` / `after_compaction`**: observe or annotate compaction cycles.
*   **`before_tool_call` / `after_tool_call`**: intercept tool params/results.
*   **`tool_result_persist`**: synchronously transform tool results before they are written to the session transcript.
*   **`message_received` / `message_sending` / `message_sent`**: inbound + outbound message hooks.
*   **`session_start` / `session_end`**: session lifecycle boundaries.
*   **`gateway_start` / `gateway_stop`**: gateway lifecycle events.

See [Plugins](https://docs.openclaw.ai/tools/plugin#plugin-hooks) for the hook API and registration details.

*   Assistant deltas are streamed from pi-agent-core and emitted as `assistant` events.
*   Block streaming can emit partial replies either on `text_end` or `message_end`.
*   Reasoning streaming can be emitted as a separate stream or as block replies.
*   See [Streaming](https://docs.openclaw.ai/concepts/streaming) for chunking and block reply behavior.

*   Tool start/update/end events are emitted on the `tool` stream.
*   Tool results are sanitized for size and image payloads before logging/emitting.
*   Messaging tool sends are tracked to suppress duplicate assistant confirmations.

## Reply shaping + suppression

*   Final payloads are assembled from:
    *   assistant text (and optional reasoning)
    *   inline tool summaries (when verbose + allowed)
    *   assistant error text when the model errors
*   `NO_REPLY` is treated as a silent token and filtered from outgoing payloads.
*   Messaging tool duplicates are removed from the final payload list.
*   If no renderable payloads remain and a tool errored, a fallback tool error reply is emitted (unless a messaging tool already sent a user-visible reply).

## Compaction + retries

*   Auto-compaction emits `compaction` stream events and can trigger a retry.
*   On retry, in-memory buffers and tool summaries are reset to avoid duplicate output.
*   See [Compaction](https://docs.openclaw.ai/concepts/compaction) for the compaction pipeline.

## Event streams (today)

*   `lifecycle`: emitted by `subscribeEmbeddedPiSession` (and as a fallback by `agentCommand`)
*   `assistant`: streamed deltas from pi-agent-core
*   `tool`: streamed tool events from pi-agent-core

## Chat channel handling

*   Assistant deltas are buffered into chat `delta` messages.
*   A chat `final` is emitted on **lifecycle end/error**.

## Timeouts

*   `agent.wait` default: 30s (just the wait). `timeoutMs` param overrides.
*   Agent runtime: `agents.defaults.timeoutSeconds` default 600s; enforced in `runEmbeddedPiAgent` abort timer.

## Where things can end early

*   Agent timeout (abort)
*   AbortSignal (cancel)
*   Gateway disconnect or RPC timeout
*   `agent.wait` timeout (wait-only, does not stop agent)

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/architecture -->

# Gateway Architecture - OpenClaw

Last updated: 2026-01-22

## Overview

*   A single long‑lived **Gateway** owns all messaging surfaces (WhatsApp via Baileys, Telegram via grammY, Slack, Discord, Signal, iMessage, WebChat).
*   Control-plane clients (macOS app, CLI, web UI, automations) connect to the Gateway over **WebSocket** on the configured bind host (default `127.0.0.1:18789`).
*   **Nodes** (macOS/iOS/Android/headless) also connect over **WebSocket**, but declare `role: node` with explicit caps/commands.
*   One Gateway per host; it is the only place that opens a WhatsApp session.
*   The **canvas host** is served by the Gateway HTTP server under:
    *   `/__openclaw__/canvas/` (agent-editable HTML/CSS/JS)
    *   `/__openclaw__/a2ui/` (A2UI host) It uses the same port as the Gateway (default `18789`).

## Components and flows

### Gateway (daemon)

*   Maintains provider connections.
*   Exposes a typed WS API (requests, responses, server‑push events).
*   Validates inbound frames against JSON Schema.
*   Emits events like `agent`, `chat`, `presence`, `health`, `heartbeat`, `cron`.

### Clients (mac app / CLI / web admin)

*   One WS connection per client.
*   Send requests (`health`, `status`, `send`, `agent`, `system-presence`).
*   Subscribe to events (`tick`, `agent`, `presence`, `shutdown`).

### Nodes (macOS / iOS / Android / headless)

*   Connect to the **same WS server** with `role: node`.
*   Provide a device identity in `connect`; pairing is **device‑based** (role `node`) and approval lives in the device pairing store.
*   Expose commands like `canvas.*`, `camera.*`, `screen.record`, `location.get`.

Protocol details:

*   [Gateway protocol](https://docs.openclaw.ai/gateway/protocol)

### WebChat

*   Static UI that uses the Gateway WS API for chat history and sends.
*   In remote setups, connects through the same SSH/Tailscale tunnel as other clients.

## Connection lifecycle (single client)

## Wire protocol (summary)

*   Transport: WebSocket, text frames with JSON payloads.
*   First frame **must** be `connect`.
*   After handshake:
    *   Requests: `{type:"req", id, method, params}` → `{type:"res", id, ok, payload|error}`
    *   Events: `{type:"event", event, payload, seq?, stateVersion?}`
*   If `OPENCLAW_GATEWAY_TOKEN` (or `--token`) is set, `connect.params.auth.token` must match or the socket closes.
*   Idempotency keys are required for side‑effecting methods (`send`, `agent`) to safely retry; the server keeps a short‑lived dedupe cache.
*   Nodes must include `role: "node"` plus caps/commands/permissions in `connect`.

## Pairing + local trust

*   All WS clients (operators + nodes) include a **device identity** on `connect`.
*   New device IDs require pairing approval; the Gateway issues a **device token** for subsequent connects.
*   **Local** connects (loopback or the gateway host’s own tailnet address) can be auto‑approved to keep same‑host UX smooth.
*   All connects must sign the `connect.challenge` nonce.
*   Signature payload `v3` also binds `platform` + `deviceFamily`; the gateway pins paired metadata on reconnect and requires repair pairing for metadata changes.
*   **Non‑local** connects still require explicit approval.
*   Gateway auth (`gateway.auth.*`) still applies to **all** connections, local or remote.

Details: [Gateway protocol](https://docs.openclaw.ai/gateway/protocol), [Pairing](https://docs.openclaw.ai/channels/pairing), [Security](https://docs.openclaw.ai/gateway/security).

## Protocol typing and codegen

*   TypeBox schemas define the protocol.
*   JSON Schema is generated from those schemas.
*   Swift models are generated from the JSON Schema.

## Remote access

*   Preferred: Tailscale or VPN.
*   Alternative: SSH tunnel
    
    ```
    ssh -N -L 18789:127.0.0.1:18789 user@host
    ```
    
*   The same handshake + auth token apply over the tunnel.
*   TLS + optional pinning can be enabled for WS in remote setups.

## Operations snapshot

*   Start: `openclaw gateway` (foreground, logs to stdout).
*   Health: `health` over WS (also included in `hello-ok`).
*   Supervision: launchd/systemd for auto‑restart.

## Invariants

*   Exactly one Gateway controls a single Baileys session per host.
*   Handshake is mandatory; any non‑JSON or non‑connect first frame is a hard close.
*   Events are not replayed; clients must refresh on gaps.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/agent-workspace -->

# Agent Workspace - OpenClaw

The workspace is the agent’s home. It is the only working directory used for file tools and for workspace context. Keep it private and treat it as memory. This is separate from `~/.openclaw/`, which stores config, credentials, and sessions. **Important:** the workspace is the **default cwd**, not a hard sandbox. Tools resolve relative paths against the workspace, but absolute paths can still reach elsewhere on the host unless sandboxing is enabled. If you need isolation, use [`agents.defaults.sandbox`](https://docs.openclaw.ai/gateway/sandboxing) (and/or per‑agent sandbox config). When sandboxing is enabled and `workspaceAccess` is not `"rw"`, tools operate inside a sandbox workspace under `~/.openclaw/sandboxes`, not your host workspace.

## Default location

*   Default: `~/.openclaw/workspace`
*   If `OPENCLAW_PROFILE` is set and not `"default"`, the default becomes `~/.openclaw/workspace-<profile>`.
*   Override in `~/.openclaw/openclaw.json`:

```
{
  agent: {
    workspace: "~/.openclaw/workspace",
  },
}
```

`openclaw onboard`, `openclaw configure`, or `openclaw setup` will create the workspace and seed the bootstrap files if they are missing. Sandbox seed copies only accept regular in-workspace files; symlink/hardlink aliases that resolve outside the source workspace are ignored. If you already manage the workspace files yourself, you can disable bootstrap file creation:

```
{ agent: { skipBootstrap: true } }
```

Older installs may have created `~/openclaw`. Keeping multiple workspace directories around can cause confusing auth or state drift, because only one workspace is active at a time. **Recommendation:** keep a single active workspace. If you no longer use the extra folders, archive or move them to Trash (for example `trash ~/openclaw`). If you intentionally keep multiple workspaces, make sure `agents.defaults.workspace` points to the active one. `openclaw doctor` warns when it detects extra workspace directories.

## Workspace file map (what each file means)

These are the standard files OpenClaw expects inside the workspace:

*   `AGENTS.md`
    *   Operating instructions for the agent and how it should use memory.
    *   Loaded at the start of every session.
    *   Good place for rules, priorities, and “how to behave” details.
*   `SOUL.md`
    *   Persona, tone, and boundaries.
    *   Loaded every session.
*   `USER.md`
    *   Who the user is and how to address them.
    *   Loaded every session.
*   `IDENTITY.md`
    *   The agent’s name, vibe, and emoji.
    *   Created/updated during the bootstrap ritual.
*   `TOOLS.md`
    *   Notes about your local tools and conventions.
    *   Does not control tool availability; it is only guidance.
*   `HEARTBEAT.md`
    *   Optional tiny checklist for heartbeat runs.
    *   Keep it short to avoid token burn.
*   `BOOT.md`
    *   Optional startup checklist executed on gateway restart when internal hooks are enabled.
    *   Keep it short; use the message tool for outbound sends.
*   `BOOTSTRAP.md`
    *   One-time first-run ritual.
    *   Only created for a brand-new workspace.
    *   Delete it after the ritual is complete.
*   `memory/YYYY-MM-DD.md`
    *   Daily memory log (one file per day).
    *   Recommended to read today + yesterday on session start.
*   `MEMORY.md` (optional)
    *   Curated long-term memory.
    *   Only load in the main, private session (not shared/group contexts).

See [Memory](https://docs.openclaw.ai/concepts/memory) for the workflow and automatic memory flush.

*   `skills/` (optional)
    *   Workspace-specific skills.
    *   Overrides managed/bundled skills when names collide.
*   `canvas/` (optional)
    *   Canvas UI files for node displays (for example `canvas/index.html`).

If any bootstrap file is missing, OpenClaw injects a “missing file” marker into the session and continues. Large bootstrap files are truncated when injected; adjust limits with `agents.defaults.bootstrapMaxChars` (default: 20000) and `agents.defaults.bootstrapTotalMaxChars` (default: 150000). `openclaw setup` can recreate missing defaults without overwriting existing files.

## What is NOT in the workspace

These live under `~/.openclaw/` and should NOT be committed to the workspace repo:

*   `~/.openclaw/openclaw.json` (config)
*   `~/.openclaw/credentials/` (OAuth tokens, API keys)
*   `~/.openclaw/agents/<agentId>/sessions/` (session transcripts + metadata)
*   `~/.openclaw/skills/` (managed skills)

If you need to migrate sessions or config, copy them separately and keep them out of version control.

## Git backup (recommended, private)

Treat the workspace as private memory. Put it in a **private** git repo so it is backed up and recoverable. Run these steps on the machine where the Gateway runs (that is where the workspace lives).

### 1) Initialize the repo

If git is installed, brand-new workspaces are initialized automatically. If this workspace is not already a repo, run:

```
cd ~/.openclaw/workspace
git init
git add AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md memory/
git commit -m "Add agent workspace"
```

### 2) Add a private remote (beginner-friendly options)

Option A: GitHub web UI

1.  Create a new **private** repository on GitHub.
2.  Do not initialize with a README (avoids merge conflicts).
3.  Copy the HTTPS remote URL.
4.  Add the remote and push:

```
git branch -M main
git remote add origin <https-url>
git push -u origin main
```

Option B: GitHub CLI (`gh`)

```
gh auth login
gh repo create openclaw-workspace --private --source . --remote origin --push
```

Option C: GitLab web UI

1.  Create a new **private** repository on GitLab.
2.  Do not initialize with a README (avoids merge conflicts).
3.  Copy the HTTPS remote URL.
4.  Add the remote and push:

```
git branch -M main
git remote add origin <https-url>
git push -u origin main
```

### 3) Ongoing updates

```
git status
git add .
git commit -m "Update memory"
git push
```

## Do not commit secrets

Even in a private repo, avoid storing secrets in the workspace:

*   API keys, OAuth tokens, passwords, or private credentials.
*   Anything under `~/.openclaw/`.
*   Raw dumps of chats or sensitive attachments.

If you must store sensitive references, use placeholders and keep the real secret elsewhere (password manager, environment variables, or `~/.openclaw/`). Suggested `.gitignore` starter:

```
.DS_Store
.env
**/*.key
**/*.pem
**/secrets*
```

## Moving the workspace to a new machine

1.  Clone the repo to the desired path (default `~/.openclaw/workspace`).
2.  Set `agents.defaults.workspace` to that path in `~/.openclaw/openclaw.json`.
3.  Run `openclaw setup --workspace <path>` to seed any missing files.
4.  If you need sessions, copy `~/.openclaw/agents/<agentId>/sessions/` from the old machine separately.

## Advanced notes

*   Multi-agent routing can use different workspaces per agent. See [Channel routing](https://docs.openclaw.ai/channels/channel-routing) for routing configuration.
*   If `agents.defaults.sandbox` is enabled, non-main sessions can use per-session sandbox workspaces under `agents.defaults.sandbox.workspaceRoot`.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/context -->

# Context - OpenClaw

“Context” is **everything OpenClaw sends to the model for a run**. It is bounded by the model’s **context window** (token limit). Beginner mental model:

*   **System prompt** (OpenClaw-built): rules, tools, skills list, time/runtime, and injected workspace files.
*   **Conversation history**: your messages + the assistant’s messages for this session.
*   **Tool calls/results + attachments**: command output, file reads, images/audio, etc.

Context is _not the same thing_ as “memory”: memory can be stored on disk and reloaded later; context is what’s inside the model’s current window.

## Quick start (inspect context)

*   `/status` → quick “how full is my window?” view + session settings.
*   `/context list` → what’s injected + rough sizes (per file + totals).
*   `/context detail` → deeper breakdown: per-file, per-tool schema sizes, per-skill entry sizes, and system prompt size.
*   `/usage tokens` → append per-reply usage footer to normal replies.
*   `/compact` → summarize older history into a compact entry to free window space.

See also: [Slash commands](https://docs.openclaw.ai/tools/slash-commands), [Token use & costs](https://docs.openclaw.ai/reference/token-use), [Compaction](https://docs.openclaw.ai/concepts/compaction).

## Example output

Values vary by model, provider, tool policy, and what’s in your workspace.

### `/context list`

```
🧠 Context breakdown
Workspace: <workspaceDir>
Bootstrap max/file: 20,000 chars
Sandbox: mode=non-main sandboxed=false
System prompt (run): 38,412 chars (~9,603 tok) (Project Context 23,901 chars (~5,976 tok))

Injected workspace files:
- AGENTS.md: OK | raw 1,742 chars (~436 tok) | injected 1,742 chars (~436 tok)
- SOUL.md: OK | raw 912 chars (~228 tok) | injected 912 chars (~228 tok)
- TOOLS.md: TRUNCATED | raw 54,210 chars (~13,553 tok) | injected 20,962 chars (~5,241 tok)
- IDENTITY.md: OK | raw 211 chars (~53 tok) | injected 211 chars (~53 tok)
- USER.md: OK | raw 388 chars (~97 tok) | injected 388 chars (~97 tok)
- HEARTBEAT.md: MISSING | raw 0 | injected 0
- BOOTSTRAP.md: OK | raw 0 chars (~0 tok) | injected 0 chars (~0 tok)

Skills list (system prompt text): 2,184 chars (~546 tok) (12 skills)
Tools: read, edit, write, exec, process, browser, message, sessions_send, …
Tool list (system prompt text): 1,032 chars (~258 tok)
Tool schemas (JSON): 31,988 chars (~7,997 tok) (counts toward context; not shown as text)
Tools: (same as above)

Session tokens (cached): 14,250 total / ctx=32,000
```

### `/context detail`

```
🧠 Context breakdown (detailed)
…
Top skills (prompt entry size):
- frontend-design: 412 chars (~103 tok)
- oracle: 401 chars (~101 tok)
… (+10 more skills)

Top tools (schema size):
- browser: 9,812 chars (~2,453 tok)
- exec: 6,240 chars (~1,560 tok)
… (+N more tools)
```

## What counts toward the context window

Everything the model receives counts, including:

*   System prompt (all sections).
*   Conversation history.
*   Tool calls + tool results.
*   Attachments/transcripts (images/audio/files).
*   Compaction summaries and pruning artifacts.
*   Provider “wrappers” or hidden headers (not visible, still counted).

## How OpenClaw builds the system prompt

The system prompt is **OpenClaw-owned** and rebuilt each run. It includes:

*   Tool list + short descriptions.
*   Skills list (metadata only; see below).
*   Workspace location.
*   Time (UTC + converted user time if configured).
*   Runtime metadata (host/OS/model/thinking).
*   Injected workspace bootstrap files under **Project Context**.

Full breakdown: [System Prompt](https://docs.openclaw.ai/concepts/system-prompt).

## Injected workspace files (Project Context)

By default, OpenClaw injects a fixed set of workspace files (if present):

*   `AGENTS.md`
*   `SOUL.md`
*   `TOOLS.md`
*   `IDENTITY.md`
*   `USER.md`
*   `HEARTBEAT.md`
*   `BOOTSTRAP.md` (first-run only)

Large files are truncated per-file using `agents.defaults.bootstrapMaxChars` (default `20000` chars). OpenClaw also enforces a total bootstrap injection cap across files with `agents.defaults.bootstrapTotalMaxChars` (default `150000` chars). `/context` shows **raw vs injected** sizes and whether truncation happened. When truncation occurs, the runtime can inject an in-prompt warning block under Project Context. Configure this with `agents.defaults.bootstrapPromptTruncationWarning` (`off`, `once`, `always`; default `once`).

## Skills: what’s injected vs loaded on-demand

The system prompt includes a compact **skills list** (name + description + location). This list has real overhead. Skill instructions are _not_ included by default. The model is expected to `read` the skill’s `SKILL.md` **only when needed**.

Tools affect context in two ways:

1.  **Tool list text** in the system prompt (what you see as “Tooling”).
2.  **Tool schemas** (JSON). These are sent to the model so it can call tools. They count toward context even though you don’t see them as plain text.

`/context detail` breaks down the biggest tool schemas so you can see what dominates.

## Commands, directives, and “inline shortcuts”

Slash commands are handled by the Gateway. There are a few different behaviors:

*   **Standalone commands**: a message that is only `/...` runs as a command.
*   **Directives**: `/think`, `/verbose`, `/reasoning`, `/elevated`, `/model`, `/queue` are stripped before the model sees the message.
    *   Directive-only messages persist session settings.
    *   Inline directives in a normal message act as per-message hints.
*   **Inline shortcuts** (allowlisted senders only): certain `/...` tokens inside a normal message can run immediately (example: “hey /status”), and are stripped before the model sees the remaining text.

Details: [Slash commands](https://docs.openclaw.ai/tools/slash-commands).

## Sessions, compaction, and pruning (what persists)

What persists across messages depends on the mechanism:

*   **Normal history** persists in the session transcript until compacted/pruned by policy.
*   **Compaction** persists a summary into the transcript and keeps recent messages intact.
*   **Pruning** removes old tool results from the _in-memory_ prompt for a run, but does not rewrite the transcript.

Docs: [Session](https://docs.openclaw.ai/concepts/session), [Compaction](https://docs.openclaw.ai/concepts/compaction), [Session pruning](https://docs.openclaw.ai/concepts/session-pruning). By default, OpenClaw uses the built-in `legacy` context engine for assembly and compaction. If you install a plugin that provides `kind: "context-engine"` and select it with `plugins.slots.contextEngine`, OpenClaw delegates context assembly, `/compact`, and related subagent context lifecycle hooks to that engine instead.

## What `/context` actually reports

`/context` prefers the latest **run-built** system prompt report when available:

*   `System prompt (run)` = captured from the last embedded (tool-capable) run and persisted in the session store.
*   `System prompt (estimate)` = computed on the fly when no run report exists (or when running via a CLI backend that doesn’t generate the report).

Either way, it reports sizes and top contributors; it does **not** dump the full system prompt or tool schemas.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/system-prompt -->

# System Prompt - OpenClaw

OpenClaw builds a custom system prompt for every agent run. The prompt is **OpenClaw-owned** and does not use the pi-coding-agent default prompt. The prompt is assembled by OpenClaw and injected into each agent run.

## Structure

The prompt is intentionally compact and uses fixed sections:

*   **Tooling**: current tool list + short descriptions.
*   **Safety**: short guardrail reminder to avoid power-seeking behavior or bypassing oversight.
*   **Skills** (when available): tells the model how to load skill instructions on demand.
*   **OpenClaw Self-Update**: how to run `config.apply` and `update.run`.
*   **Workspace**: working directory (`agents.defaults.workspace`).
*   **Documentation**: local path to OpenClaw docs (repo or npm package) and when to read them.
*   **Workspace Files (injected)**: indicates bootstrap files are included below.
*   **Sandbox** (when enabled): indicates sandboxed runtime, sandbox paths, and whether elevated exec is available.
*   **Current Date & Time**: user-local time, timezone, and time format.
*   **Reply Tags**: optional reply tag syntax for supported providers.
*   **Heartbeats**: heartbeat prompt and ack behavior.
*   **Runtime**: host, OS, node, model, repo root (when detected), thinking level (one line).
*   **Reasoning**: current visibility level + /reasoning toggle hint.

Safety guardrails in the system prompt are advisory. They guide model behavior but do not enforce policy. Use tool policy, exec approvals, sandboxing, and channel allowlists for hard enforcement; operators can disable these by design.

## Prompt modes

OpenClaw can render smaller system prompts for sub-agents. The runtime sets a `promptMode` for each run (not a user-facing config):

*   `full` (default): includes all sections above.
*   `minimal`: used for sub-agents; omits **Skills**, **Memory Recall**, **OpenClaw Self-Update**, **Model Aliases**, **User Identity**, **Reply Tags**, **Messaging**, **Silent Replies**, and **Heartbeats**. Tooling, **Safety**, Workspace, Sandbox, Current Date & Time (when known), Runtime, and injected context stay available.
*   `none`: returns only the base identity line.

When `promptMode=minimal`, extra injected prompts are labeled **Subagent Context** instead of **Group Chat Context**.

## Workspace bootstrap injection

Bootstrap files are trimmed and appended under **Project Context** so the model sees identity and profile context without needing explicit reads:

*   `AGENTS.md`
*   `SOUL.md`
*   `TOOLS.md`
*   `IDENTITY.md`
*   `USER.md`
*   `HEARTBEAT.md`
*   `BOOTSTRAP.md` (only on brand-new workspaces)
*   `MEMORY.md` and/or `memory.md` (when present in the workspace; either or both may be injected)

All of these files are **injected into the context window** on every turn, which means they consume tokens. Keep them concise — especially `MEMORY.md`, which can grow over time and lead to unexpectedly high context usage and more frequent compaction.

> **Note:** `memory/*.md` daily files are **not** injected automatically. They are accessed on demand via the `memory_search` and `memory_get` tools, so they do not count against the context window unless the model explicitly reads them.

Large files are truncated with a marker. The max per-file size is controlled by `agents.defaults.bootstrapMaxChars` (default: 20000). Total injected bootstrap content across files is capped by `agents.defaults.bootstrapTotalMaxChars` (default: 150000). Missing files inject a short missing-file marker. When truncation occurs, OpenClaw can inject a warning block in Project Context; control this with `agents.defaults.bootstrapPromptTruncationWarning` (`off`, `once`, `always`; default: `once`). Sub-agent sessions only inject `AGENTS.md` and `TOOLS.md` (other bootstrap files are filtered out to keep the sub-agent context small). Internal hooks can intercept this step via `agent:bootstrap` to mutate or replace the injected bootstrap files (for example swapping `SOUL.md` for an alternate persona). To inspect how much each injected file contributes (raw vs injected, truncation, plus tool schema overhead), use `/context list` or `/context detail`. See [Context](https://docs.openclaw.ai/concepts/context).

## Time handling

The system prompt includes a dedicated **Current Date & Time** section when the user timezone is known. To keep the prompt cache-stable, it now only includes the **time zone** (no dynamic clock or time format). Use `session_status` when the agent needs the current time; the status card includes a timestamp line. Configure with:

*   `agents.defaults.userTimezone`
*   `agents.defaults.timeFormat` (`auto` | `12` | `24`)

See [Date & Time](https://docs.openclaw.ai/date-time) for full behavior details.

## Skills

When eligible skills exist, OpenClaw injects a compact **available skills list** (`formatSkillsForPrompt`) that includes the **file path** for each skill. The prompt instructs the model to use `read` to load the SKILL.md at the listed location (workspace, managed, or bundled). If no skills are eligible, the Skills section is omitted.

```
<available_skills>
  <skill>
    <name>...</name>
    <description>...</description>
    <location>...</location>
  </skill>
</available_skills>
```

This keeps the base prompt small while still enabling targeted skill usage.

## Documentation

When available, the system prompt includes a **Documentation** section that points to the local OpenClaw docs directory (either `docs/` in the repo workspace or the bundled npm package docs) and also notes the public mirror, source repo, community Discord, and ClawHub ([https://clawhub.com](https://clawhub.com/)) for skills discovery. The prompt instructs the model to consult local docs first for OpenClaw behavior, commands, configuration, or architecture, and to run `openclaw status` itself when possible (asking the user only when it lacks access).

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/session-pruning -->

# Session Pruning - OpenClaw

Session pruning trims **old tool results** from the in-memory context right before each LLM call. It does **not** rewrite the on-disk session history (`*.jsonl`).

## When it runs

*   When `mode: "cache-ttl"` is enabled and the last Anthropic call for the session is older than `ttl`.
*   Only affects the messages sent to the model for that request.
*   Only active for Anthropic API calls (and OpenRouter Anthropic models).
*   For best results, match `ttl` to your model `cacheRetention` policy (`short` = 5m, `long` = 1h).
*   After a prune, the TTL window resets so subsequent requests keep cache until `ttl` expires again.

## Smart defaults (Anthropic)

*   **OAuth or setup-token** profiles: enable `cache-ttl` pruning and set heartbeat to `1h`.
*   **API key** profiles: enable `cache-ttl` pruning, set heartbeat to `30m`, and default `cacheRetention: "short"` on Anthropic models.
*   If you set any of these values explicitly, OpenClaw does **not** override them.

## What this improves (cost + cache behavior)

*   **Why prune:** Anthropic prompt caching only applies within the TTL. If a session goes idle past the TTL, the next request re-caches the full prompt unless you trim it first.
*   **What gets cheaper:** pruning reduces the **cacheWrite** size for that first request after the TTL expires.
*   **Why the TTL reset matters:** once pruning runs, the cache window resets, so follow‑up requests can reuse the freshly cached prompt instead of re-caching the full history again.
*   **What it does not do:** pruning doesn’t add tokens or “double” costs; it only changes what gets cached on that first post‑TTL request.

## What can be pruned

*   Only `toolResult` messages.
*   User + assistant messages are **never** modified.
*   The last `keepLastAssistants` assistant messages are protected; tool results after that cutoff are not pruned.
*   If there aren’t enough assistant messages to establish the cutoff, pruning is skipped.
*   Tool results containing **image blocks** are skipped (never trimmed/cleared).

## Context window estimation

Pruning uses an estimated context window (chars ≈ tokens × 4). The base window is resolved in this order:

1.  `models.providers.*.models[].contextWindow` override.
2.  Model definition `contextWindow` (from the model registry).
3.  Default `200000` tokens.

If `agents.defaults.contextTokens` is set, it is treated as a cap (min) on the resolved window.

## Mode

### cache-ttl

*   Pruning only runs if the last Anthropic call is older than `ttl` (default `5m`).
*   When it runs: same soft-trim + hard-clear behavior as before.

## Soft vs hard pruning

*   **Soft-trim**: only for oversized tool results.
    *   Keeps head + tail, inserts `...`, and appends a note with the original size.
    *   Skips results with image blocks.
*   **Hard-clear**: replaces the entire tool result with `hardClear.placeholder`.

*   `tools.allow` / `tools.deny` support `*` wildcards.
*   Deny wins.
*   Matching is case-insensitive.
*   Empty allow list => all tools allowed.

## Interaction with other limits

*   Built-in tools already truncate their own output; session pruning is an extra layer that prevents long-running chats from accumulating too much tool output in the model context.
*   Compaction is separate: compaction summarizes and persists, pruning is transient per request. See [/concepts/compaction](https://docs.openclaw.ai/concepts/compaction).

## Defaults (when enabled)

*   `ttl`: `"5m"`
*   `keepLastAssistants`: `3`
*   `softTrimRatio`: `0.3`
*   `hardClearRatio`: `0.5`
*   `minPrunableToolChars`: `50000`
*   `softTrim`: `{ maxChars: 4000, headChars: 1500, tailChars: 1500 }`
*   `hardClear`: `{ enabled: true, placeholder: "[Old tool result content cleared]" }`

## Examples

Default (off):

```
{
  agents: { defaults: { contextPruning: { mode: "off" } } },
}
```

Enable TTL-aware pruning:

```
{
  agents: { defaults: { contextPruning: { mode: "cache-ttl", ttl: "5m" } } },
}
```

Restrict pruning to specific tools:

```
{
  agents: {
    defaults: {
      contextPruning: {
        mode: "cache-ttl",
        tools: { allow: ["exec", "read"], deny: ["*image*"] },
      },
    },
  },
}
```

See config reference: [Gateway Configuration](https://docs.openclaw.ai/gateway/configuration)

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/session -->

# Session Management - OpenClaw

OpenClaw treats **one direct-chat session per agent** as primary. Direct chats collapse to `agent:<agentId>:<mainKey>` (default `main`), while group/channel chats get their own keys. `session.mainKey` is honored. Use `session.dmScope` to control how **direct messages** are grouped:

*   `main` (default): all DMs share the main session for continuity.
*   `per-peer`: isolate by sender id across channels.
*   `per-channel-peer`: isolate by channel + sender (recommended for multi-user inboxes).
*   `per-account-channel-peer`: isolate by account + channel + sender (recommended for multi-account inboxes). Use `session.identityLinks` to map provider-prefixed peer ids to a canonical identity so the same person shares a DM session across channels when using `per-peer`, `per-channel-peer`, or `per-account-channel-peer`.

## Secure DM mode (recommended for multi-user setups)

> **Security Warning:** If your agent can receive DMs from **multiple people**, you should strongly consider enabling secure DM mode. Without it, all users share the same conversation context, which can leak private information between users.

**Example of the problem with default settings:**

*   Alice (`<SENDER_A>`) messages your agent about a private topic (for example, a medical appointment)
*   Bob (`<SENDER_B>`) messages your agent asking “What were we talking about?”
*   Because both DMs share the same session, the model may answer Bob using Alice’s prior context.

**The fix:** Set `dmScope` to isolate sessions per user:

```
// ~/.openclaw/openclaw.json
{
  session: {
    // Secure DM mode: isolate DM context per channel + sender.
    dmScope: "per-channel-peer",
  },
}
```

**When to enable this:**

*   You have pairing approvals for more than one sender
*   You use a DM allowlist with multiple entries
*   You set `dmPolicy: "open"`
*   Multiple phone numbers or accounts can message your agent

Notes:

*   Default is `dmScope: "main"` for continuity (all DMs share the main session). This is fine for single-user setups.
*   Local CLI onboarding writes `session.dmScope: "per-channel-peer"` by default when unset (existing explicit values are preserved).
*   For multi-account inboxes on the same channel, prefer `per-account-channel-peer`.
*   If the same person contacts you on multiple channels, use `session.identityLinks` to collapse their DM sessions into one canonical identity.
*   You can verify your DM settings with `openclaw security audit` (see [security](https://docs.openclaw.ai/cli/security)).

## Gateway is the source of truth

All session state is **owned by the gateway** (the “master” OpenClaw). UI clients (macOS app, WebChat, etc.) must query the gateway for session lists and token counts instead of reading local files.

*   In **remote mode**, the session store you care about lives on the remote gateway host, not your Mac.
*   Token counts shown in UIs come from the gateway’s store fields (`inputTokens`, `outputTokens`, `totalTokens`, `contextTokens`). Clients do not parse JSONL transcripts to “fix up” totals.

## Where state lives

*   On the **gateway host**:
    *   Store file: `~/.openclaw/agents/<agentId>/sessions/sessions.json` (per agent).
*   Transcripts: `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl` (Telegram topic sessions use `.../<SessionId>-topic-<threadId>.jsonl`).
*   The store is a map `sessionKey -> { sessionId, updatedAt, ... }`. Deleting entries is safe; they are recreated on demand.
*   Group entries may include `displayName`, `channel`, `subject`, `room`, and `space` to label sessions in UIs.
*   Session entries include `origin` metadata (label + routing hints) so UIs can explain where a session came from.
*   OpenClaw does **not** read legacy Pi/Tau session folders.

## Maintenance

OpenClaw applies session-store maintenance to keep `sessions.json` and transcript artifacts bounded over time.

### Defaults

*   `session.maintenance.mode`: `warn`
*   `session.maintenance.pruneAfter`: `30d`
*   `session.maintenance.maxEntries`: `500`
*   `session.maintenance.rotateBytes`: `10mb`
*   `session.maintenance.resetArchiveRetention`: defaults to `pruneAfter` (`30d`)
*   `session.maintenance.maxDiskBytes`: unset (disabled)
*   `session.maintenance.highWaterBytes`: defaults to `80%` of `maxDiskBytes` when budgeting is enabled

### How it works

Maintenance runs during session-store writes, and you can trigger it on demand with `openclaw sessions cleanup`.

*   `mode: "warn"`: reports what would be evicted but does not mutate entries/transcripts.
*   `mode: "enforce"`: applies cleanup in this order:
    1.  prune stale entries older than `pruneAfter`
    2.  cap entry count to `maxEntries` (oldest first)
    3.  archive transcript files for removed entries that are no longer referenced
    4.  purge old `*.deleted.<timestamp>` and `*.reset.<timestamp>` archives by retention policy
    5.  rotate `sessions.json` when it exceeds `rotateBytes`
    6.  if `maxDiskBytes` is set, enforce disk budget toward `highWaterBytes` (oldest artifacts first, then oldest sessions)

### Performance caveat for large stores

Large session stores are common in high-volume setups. Maintenance work is write-path work, so very large stores can increase write latency. What increases cost most:

*   very high `session.maintenance.maxEntries` values
*   long `pruneAfter` windows that keep stale entries around
*   many transcript/archive artifacts in `~/.openclaw/agents/<agentId>/sessions/`
*   enabling disk budgets (`maxDiskBytes`) without reasonable pruning/cap limits

What to do:

*   use `mode: "enforce"` in production so growth is bounded automatically
*   set both time and count limits (`pruneAfter` + `maxEntries`), not just one
*   set `maxDiskBytes` + `highWaterBytes` for hard upper bounds in large deployments
*   keep `highWaterBytes` meaningfully below `maxDiskBytes` (default is 80%)
*   run `openclaw sessions cleanup --dry-run --json` after config changes to verify projected impact before enforcing
*   for frequent active sessions, pass `--active-key` when running manual cleanup

### Customize examples

Use a conservative enforce policy:

```
{
  session: {
    maintenance: {
      mode: "enforce",
      pruneAfter: "45d",
      maxEntries: 800,
      rotateBytes: "20mb",
      resetArchiveRetention: "14d",
    },
  },
}
```

Enable a hard disk budget for the sessions directory:

```
{
  session: {
    maintenance: {
      mode: "enforce",
      maxDiskBytes: "1gb",
      highWaterBytes: "800mb",
    },
  },
}
```

Tune for larger installs (example):

```
{
  session: {
    maintenance: {
      mode: "enforce",
      pruneAfter: "14d",
      maxEntries: 2000,
      rotateBytes: "25mb",
      maxDiskBytes: "2gb",
      highWaterBytes: "1.6gb",
    },
  },
}
```

Preview or force maintenance from CLI:

```
openclaw sessions cleanup --dry-run
openclaw sessions cleanup --enforce
```

## Session pruning

OpenClaw trims **old tool results** from the in-memory context right before LLM calls by default. This does **not** rewrite JSONL history. See [/concepts/session-pruning](https://docs.openclaw.ai/concepts/session-pruning).

## Pre-compaction memory flush

When a session nears auto-compaction, OpenClaw can run a **silent memory flush** turn that reminds the model to write durable notes to disk. This only runs when the workspace is writable. See [Memory](https://docs.openclaw.ai/concepts/memory) and [Compaction](https://docs.openclaw.ai/concepts/compaction).

## Mapping transports → session keys

*   Direct chats follow `session.dmScope` (default `main`).
    *   `main`: `agent:<agentId>:<mainKey>` (continuity across devices/channels).
        *   Multiple phone numbers and channels can map to the same agent main key; they act as transports into one conversation.
    *   `per-peer`: `agent:<agentId>:dm:<peerId>`.
    *   `per-channel-peer`: `agent:<agentId>:<channel>:dm:<peerId>`.
    *   `per-account-channel-peer`: `agent:<agentId>:<channel>:<accountId>:dm:<peerId>` (accountId defaults to `default`).
    *   If `session.identityLinks` matches a provider-prefixed peer id (for example `telegram:123`), the canonical key replaces `<peerId>` so the same person shares a session across channels.
*   Group chats isolate state: `agent:<agentId>:<channel>:group:<id>` (rooms/channels use `agent:<agentId>:<channel>:channel:<id>`).
    *   Telegram forum topics append `:topic:<threadId>` to the group id for isolation.
    *   Legacy `group:<id>` keys are still recognized for migration.
*   Inbound contexts may still use `group:<id>`; the channel is inferred from `Provider` and normalized to the canonical `agent:<agentId>:<channel>:group:<id>` form.
*   Other sources:
    *   Cron jobs: `cron:<job.id>`
    *   Webhooks: `hook:<uuid>` (unless explicitly set by the hook)
    *   Node runs: `node-<nodeId>`

## Lifecycle

*   Reset policy: sessions are reused until they expire, and expiry is evaluated on the next inbound message.
*   Daily reset: defaults to **4:00 AM local time on the gateway host**. A session is stale once its last update is earlier than the most recent daily reset time.
*   Idle reset (optional): `idleMinutes` adds a sliding idle window. When both daily and idle resets are configured, **whichever expires first** forces a new session.
*   Legacy idle-only: if you set `session.idleMinutes` without any `session.reset`/`resetByType` config, OpenClaw stays in idle-only mode for backward compatibility.
*   Per-type overrides (optional): `resetByType` lets you override the policy for `direct`, `group`, and `thread` sessions (thread = Slack/Discord threads, Telegram topics, Matrix threads when provided by the connector).
*   Per-channel overrides (optional): `resetByChannel` overrides the reset policy for a channel (applies to all session types for that channel and takes precedence over `reset`/`resetByType`).
*   Reset triggers: exact `/new` or `/reset` (plus any extras in `resetTriggers`) start a fresh session id and pass the remainder of the message through. `/new <model>` accepts a model alias, `provider/model`, or provider name (fuzzy match) to set the new session model. If `/new` or `/reset` is sent alone, OpenClaw runs a short “hello” greeting turn to confirm the reset.
*   Manual reset: delete specific keys from the store or remove the JSONL transcript; the next message recreates them.
*   Isolated cron jobs always mint a fresh `sessionId` per run (no idle reuse).

## Send policy (optional)

Block delivery for specific session types without listing individual ids.

```
{
  session: {
    sendPolicy: {
      rules: [
        { action: "deny", match: { channel: "discord", chatType: "group" } },
        { action: "deny", match: { keyPrefix: "cron:" } },
        // Match the raw session key (including the `agent:<id>:` prefix).
        { action: "deny", match: { rawKeyPrefix: "agent:main:discord:" } },
      ],
      default: "allow",
    },
  },
}
```

Runtime override (owner only):

*   `/send on` → allow for this session
*   `/send off` → deny for this session
*   `/send inherit` → clear override and use config rules Send these as standalone messages so they register.

## Configuration (optional rename example)

```
// ~/.openclaw/openclaw.json
{
  session: {
    scope: "per-sender", // keep group keys separate
    dmScope: "main", // DM continuity (set per-channel-peer/per-account-channel-peer for shared inboxes)
    identityLinks: {
      alice: ["telegram:123456789", "discord:987654321012345678"],
    },
    reset: {
      // Defaults: mode=daily, atHour=4 (gateway host local time).
      // If you also set idleMinutes, whichever expires first wins.
      mode: "daily",
      atHour: 4,
      idleMinutes: 120,
    },
    resetByType: {
      thread: { mode: "daily", atHour: 4 },
      direct: { mode: "idle", idleMinutes: 240 },
      group: { mode: "idle", idleMinutes: 120 },
    },
    resetByChannel: {
      discord: { mode: "idle", idleMinutes: 10080 },
    },
    resetTriggers: ["/new", "/reset"],
    store: "~/.openclaw/agents/{agentId}/sessions/sessions.json",
    mainKey: "main",
  },
}
```

## Inspecting

*   `openclaw status` — shows store path and recent sessions.
*   `openclaw sessions --json` — dumps every entry (filter with `--active <minutes>`).
*   `openclaw gateway call sessions.list --params '{}'` — fetch sessions from the running gateway (use `--url`/`--token` for remote gateway access).
*   Send `/status` as a standalone message in chat to see whether the agent is reachable, how much of the session context is used, current thinking/verbose toggles, and when your WhatsApp web creds were last refreshed (helps spot relink needs).
*   Send `/context list` or `/context detail` to see what’s in the system prompt and injected workspace files (and the biggest context contributors).
*   Send `/stop` (or standalone abort phrases like `stop`, `stop action`, `stop run`, `stop openclaw`) to abort the current run, clear queued followups for that session, and stop any sub-agent runs spawned from it (the reply includes the stopped count).
*   Send `/compact` (optional instructions) as a standalone message to summarize older context and free up window space. See [/concepts/compaction](https://docs.openclaw.ai/concepts/compaction).
*   JSONL transcripts can be opened directly to review full turns.

## Tips

*   Keep the primary key dedicated to 1:1 traffic; let groups keep their own keys.
*   When automating cleanup, delete individual keys instead of the whole store to preserve context elsewhere.

Each session entry records where it came from (best-effort) in `origin`:

*   `label`: human label (resolved from conversation label + group subject/channel)
*   `provider`: normalized channel id (including extensions)
*   `from`/`to`: raw routing ids from the inbound envelope
*   `accountId`: provider account id (when multi-account)
*   `threadId`: thread/topic id when the channel supports it The origin fields are populated for direct messages, channels, and groups. If a connector only updates delivery routing (for example, to keep a DM main session fresh), it should still provide inbound context so the session keeps its explainer metadata. Extensions can do this by sending `ConversationLabel`, `GroupSubject`, `GroupChannel`, `GroupSpace`, and `SenderName` in the inbound context and calling `recordSessionMetaFromInbound` (or passing the same context to `updateLastRoute`).

---

<!-- SOURCE: https://docs.openclaw.ai/start/bootstrapping -->

# Agent Bootstrapping - OpenClaw

Bootstrapping is the **first‑run** ritual that prepares an agent workspace and collects identity details. It happens after onboarding, when the agent starts for the first time.

## What bootstrapping does

On the first agent run, OpenClaw bootstraps the workspace (default `~/.openclaw/workspace`):

*   Seeds `AGENTS.md`, `BOOTSTRAP.md`, `IDENTITY.md`, `USER.md`.
*   Runs a short Q&A ritual (one question at a time).
*   Writes identity + preferences to `IDENTITY.md`, `USER.md`, `SOUL.md`.
*   Removes `BOOTSTRAP.md` when finished so it only runs once.

## Where it runs

Bootstrapping always runs on the **gateway host**. If the macOS app connects to a remote Gateway, the workspace and bootstrapping files live on that remote machine.

*   macOS app onboarding: [Onboarding](https://docs.openclaw.ai/start/onboarding)
*   Workspace layout: [Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace)

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/session-tool -->

# Session Tools - OpenClaw

Goal: small, hard-to-misuse tool set so agents can list sessions, fetch history, and send to another session.

*   `sessions_list`
*   `sessions_history`
*   `sessions_send`
*   `sessions_spawn`

## Key Model

*   Main direct chat bucket is always the literal key `"main"` (resolved to the current agent’s main key).
*   Group chats use `agent:<agentId>:<channel>:group:<id>` or `agent:<agentId>:<channel>:channel:<id>` (pass the full key).
*   Cron jobs use `cron:<job.id>`.
*   Hooks use `hook:<uuid>` unless explicitly set.
*   Node sessions use `node-<nodeId>` unless explicitly set.

`global` and `unknown` are reserved values and are never listed. If `session.scope = "global"`, we alias it to `main` for all tools so callers never see `global`.

## sessions\_list

List sessions as an array of rows. Parameters:

*   `kinds?: string[]` filter: any of `"main" | "group" | "cron" | "hook" | "node" | "other"`
*   `limit?: number` max rows (default: server default, clamp e.g. 200)
*   `activeMinutes?: number` only sessions updated within N minutes
*   `messageLimit?: number` 0 = no messages (default 0); >0 = include last N messages

Behavior:

*   `messageLimit > 0` fetches `chat.history` per session and includes the last N messages.
*   Tool results are filtered out in list output; use `sessions_history` for tool messages.
*   When running in a **sandboxed** agent session, session tools default to **spawned-only visibility** (see below).

Row shape (JSON):

*   `key`: session key (string)
*   `kind`: `main | group | cron | hook | node | other`
*   `channel`: `whatsapp | telegram | discord | signal | imessage | webchat | internal | unknown`
*   `displayName` (group display label if available)
*   `updatedAt` (ms)
*   `sessionId`
*   `model`, `contextTokens`, `totalTokens`
*   `thinkingLevel`, `verboseLevel`, `systemSent`, `abortedLastRun`
*   `sendPolicy` (session override if set)
*   `lastChannel`, `lastTo`
*   `deliveryContext` (normalized `{ channel, to, accountId }` when available)
*   `transcriptPath` (best-effort path derived from store dir + sessionId)
*   `messages?` (only when `messageLimit > 0`)

## sessions\_history

Fetch transcript for one session. Parameters:

*   `sessionKey` (required; accepts session key or `sessionId` from `sessions_list`)
*   `limit?: number` max messages (server clamps)
*   `includeTools?: boolean` (default false)

Behavior:

*   `includeTools=false` filters `role: "toolResult"` messages.
*   Returns messages array in the raw transcript format.
*   When given a `sessionId`, OpenClaw resolves it to the corresponding session key (missing ids error).

## sessions\_send

Send a message into another session. Parameters:

*   `sessionKey` (required; accepts session key or `sessionId` from `sessions_list`)
*   `message` (required)
*   `timeoutSeconds?: number` (default >0; 0 = fire-and-forget)

Behavior:

*   `timeoutSeconds = 0`: enqueue and return `{ runId, status: "accepted" }`.
*   `timeoutSeconds > 0`: wait up to N seconds for completion, then return `{ runId, status: "ok", reply }`.
*   If wait times out: `{ runId, status: "timeout", error }`. Run continues; call `sessions_history` later.
*   If the run fails: `{ runId, status: "error", error }`.
*   Announce delivery runs after the primary run completes and is best-effort; `status: "ok"` does not guarantee the announce was delivered.
*   Waits via gateway `agent.wait` (server-side) so reconnects don’t drop the wait.
*   Agent-to-agent message context is injected for the primary run.
*   Inter-session messages are persisted with `message.provenance.kind = "inter_session"` so transcript readers can distinguish routed agent instructions from external user input.
*   After the primary run completes, OpenClaw runs a **reply-back loop**:
    *   Round 2+ alternates between requester and target agents.
    *   Reply exactly `REPLY_SKIP` to stop the ping‑pong.
    *   Max turns is `session.agentToAgent.maxPingPongTurns` (0–5, default 5).
*   Once the loop ends, OpenClaw runs the **agent‑to‑agent announce step** (target agent only):
    *   Reply exactly `ANNOUNCE_SKIP` to stay silent.
    *   Any other reply is sent to the target channel.
    *   Announce step includes the original request + round‑1 reply + latest ping‑pong reply.

## Channel Field

*   For groups, `channel` is the channel recorded on the session entry.
*   For direct chats, `channel` maps from `lastChannel`.
*   For cron/hook/node, `channel` is `internal`.
*   If missing, `channel` is `unknown`.

## Security / Send Policy

Policy-based blocking by channel/chat type (not per session id).

```
{
  "session": {
    "sendPolicy": {
      "rules": [
        {
          "match": { "channel": "discord", "chatType": "group" },
          "action": "deny"
        }
      ],
      "default": "allow"
    }
  }
}
```

Runtime override (per session entry):

*   `sendPolicy: "allow" | "deny"` (unset = inherit config)
*   Settable via `sessions.patch` or owner-only `/send on|off|inherit` (standalone message).

Enforcement points:

*   `chat.send` / `agent` (gateway)
*   auto-reply delivery logic

## sessions\_spawn

Spawn a sub-agent run in an isolated session and announce the result back to the requester chat channel. Parameters:

*   `task` (required)
*   `label?` (optional; used for logs/UI)
*   `agentId?` (optional; spawn under another agent id if allowed)
*   `model?` (optional; overrides the sub-agent model; invalid values error)
*   `thinking?` (optional; overrides thinking level for the sub-agent run)
*   `runTimeoutSeconds?` (defaults to `agents.defaults.subagents.runTimeoutSeconds` when set, otherwise `0`; when set, aborts the sub-agent run after N seconds)
*   `thread?` (default false; request thread-bound routing for this spawn when supported by the channel/plugin)
*   `mode?` (`run|session`; defaults to `run`, but defaults to `session` when `thread=true`; `mode="session"` requires `thread=true`)
*   `cleanup?` (`delete|keep`, default `keep`)
*   `sandbox?` (`inherit|require`, default `inherit`; `require` rejects spawn unless the target child runtime is sandboxed)
*   `attachments?` (optional array of inline files; subagent runtime only, ACP rejects). Each entry: `{ name, content, encoding?: "utf8" | "base64", mimeType? }`. Files are materialized into the child workspace at `.openclaw/attachments/<uuid>/`. Returns a receipt with sha256 per file.
*   `attachAs?` (optional; `{ mountPath? }` hint reserved for future mount implementations)

Allowlist:

*   `agents.list[].subagents.allowAgents`: list of agent ids allowed via `agentId` (`["*"]` to allow any). Default: only the requester agent.
*   Sandbox inheritance guard: if the requester session is sandboxed, `sessions_spawn` rejects targets that would run unsandboxed.

Discovery:

*   Use `agents_list` to discover which agent ids are allowed for `sessions_spawn`.

Behavior:

*   Starts a new `agent:<agentId>:subagent:<uuid>` session with `deliver: false`.
*   Sub-agents default to the full tool set **minus session tools** (configurable via `tools.subagents.tools`).
*   Sub-agents are not allowed to call `sessions_spawn` (no sub-agent → sub-agent spawning).
*   Always non-blocking: returns `{ status: "accepted", runId, childSessionKey }` immediately.
*   With `thread=true`, channel plugins can bind delivery/routing to a thread target (Discord support is controlled by `session.threadBindings.*` and `channels.discord.threadBindings.*`).
*   After completion, OpenClaw runs a sub-agent **announce step** and posts the result to the requester chat channel.
    *   If the assistant final reply is empty, the latest `toolResult` from sub-agent history is included as `Result`.
*   Reply exactly `ANNOUNCE_SKIP` during the announce step to stay silent.
*   Announce replies are normalized to `Status`/`Result`/`Notes`; `Status` comes from runtime outcome (not model text).
*   Sub-agent sessions are auto-archived after `agents.defaults.subagents.archiveAfterMinutes` (default: 60).
*   Announce replies include a stats line (runtime, tokens, sessionKey/sessionId, transcript path, and optional cost).

## Sandbox Session Visibility

Session tools can be scoped to reduce cross-session access. Default behavior:

*   `tools.sessions.visibility` defaults to `tree` (current session + spawned subagent sessions).
*   For sandboxed sessions, `agents.defaults.sandbox.sessionToolsVisibility` can hard-clamp visibility.

Config:

```
{
  tools: {
    sessions: {
      // "self" | "tree" | "agent" | "all"
      // default: "tree"
      visibility: "tree",
    },
  },
  agents: {
    defaults: {
      sandbox: {
        // default: "spawned"
        sessionToolsVisibility: "spawned", // or "all"
      },
    },
  },
}
```

Notes:

*   `self`: only the current session key.
*   `tree`: current session + sessions spawned by the current session.
*   `agent`: any session belonging to the current agent id.
*   `all`: any session (cross-agent access still requires `tools.agentToAgent`).
*   When a session is sandboxed and `sessionToolsVisibility="spawned"`, OpenClaw clamps visibility to `tree` even if you set `tools.sessions.visibility="all"`.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/presence -->

# Presence - OpenClaw

OpenClaw “presence” is a lightweight, best‑effort view of:

*   the **Gateway** itself, and
*   **clients connected to the Gateway** (mac app, WebChat, CLI, etc.)

Presence is used primarily to render the macOS app’s **Instances** tab and to provide quick operator visibility.

## Presence fields (what shows up)

Presence entries are structured objects with fields like:

*   `instanceId` (optional but strongly recommended): stable client identity (usually `connect.client.instanceId`)
*   `host`: human‑friendly host name
*   `ip`: best‑effort IP address
*   `version`: client version string
*   `deviceFamily` / `modelIdentifier`: hardware hints
*   `mode`: `ui`, `webchat`, `cli`, `backend`, `probe`, `test`, `node`, …
*   `lastInputSeconds`: “seconds since last user input” (if known)
*   `reason`: `self`, `connect`, `node-connected`, `periodic`, …
*   `ts`: last update timestamp (ms since epoch)

## Producers (where presence comes from)

Presence entries are produced by multiple sources and **merged**.

### 1) Gateway self entry

The Gateway always seeds a “self” entry at startup so UIs show the gateway host even before any clients connect.

### 2) WebSocket connect

Every WS client begins with a `connect` request. On successful handshake the Gateway upserts a presence entry for that connection.

#### Why one‑off CLI commands don’t show up

The CLI often connects for short, one‑off commands. To avoid spamming the Instances list, `client.mode === "cli"` is **not** turned into a presence entry.

### 3) `system-event` beacons

Clients can send richer periodic beacons via the `system-event` method. The mac app uses this to report host name, IP, and `lastInputSeconds`.

### 4) Node connects (role: node)

When a node connects over the Gateway WebSocket with `role: node`, the Gateway upserts a presence entry for that node (same flow as other WS clients).

## Merge + dedupe rules (why `instanceId` matters)

Presence entries are stored in a single in‑memory map:

*   Entries are keyed by a **presence key**.
*   The best key is a stable `instanceId` (from `connect.client.instanceId`) that survives restarts.
*   Keys are case‑insensitive.

If a client reconnects without a stable `instanceId`, it may show up as a **duplicate** row.

## TTL and bounded size

Presence is intentionally ephemeral:

*   **TTL:** entries older than 5 minutes are pruned
*   **Max entries:** 200 (oldest dropped first)

This keeps the list fresh and avoids unbounded memory growth.

## Remote/tunnel caveat (loopback IPs)

When a client connects over an SSH tunnel / local port forward, the Gateway may see the remote address as `127.0.0.1`. To avoid overwriting a good client‑reported IP, loopback remote addresses are ignored.

## Consumers

### macOS Instances tab

The macOS app renders the output of `system-presence` and applies a small status indicator (Active/Idle/Stale) based on the age of the last update.

## Debugging tips

*   To see the raw list, call `system-presence` against the Gateway.
*   If you see duplicates:
    *   confirm clients send a stable `client.instanceId` in the handshake
    *   confirm periodic beacons use the same `instanceId`
    *   check whether the connection‑derived entry is missing `instanceId` (duplicates are expected)

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/oauth -->

# OAuth - OpenClaw

OpenClaw supports “subscription auth” via OAuth for providers that offer it (notably **OpenAI Codex (ChatGPT OAuth)**). For Anthropic subscriptions, use the **setup-token** flow. Anthropic subscription use outside Claude Code has been restricted for some users in the past, so treat it as a user-choice risk and verify current Anthropic policy yourself. OpenAI Codex OAuth is explicitly supported for use in external tools like OpenClaw. This page explains: For Anthropic in production, API key auth is the safer recommended path over subscription setup-token auth.

*   how the OAuth **token exchange** works (PKCE)
*   where tokens are **stored** (and why)
*   how to handle **multiple accounts** (profiles + per-session overrides)

OpenClaw also supports **provider plugins** that ship their own OAuth or API‑key flows. Run them via:

```
openclaw models auth login --provider <id>
```

## The token sink (why it exists)

OAuth providers commonly mint a **new refresh token** during login/refresh flows. Some providers (or OAuth clients) can invalidate older refresh tokens when a new one is issued for the same user/app. Practical symptom:

*   you log in via OpenClaw _and_ via Claude Code / Codex CLI → one of them randomly gets “logged out” later

To reduce that, OpenClaw treats `auth-profiles.json` as a **token sink**:

*   the runtime reads credentials from **one place**
*   we can keep multiple profiles and route them deterministically

## Storage (where tokens live)

Secrets are stored **per-agent**:

*   Auth profiles (OAuth + API keys + optional value-level refs): `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
*   Legacy compatibility file: `~/.openclaw/agents/<agentId>/agent/auth.json` (static `api_key` entries are scrubbed when discovered)

Legacy import-only file (still supported, but not the main store):

*   `~/.openclaw/credentials/oauth.json` (imported into `auth-profiles.json` on first use)

All of the above also respect `$OPENCLAW_STATE_DIR` (state dir override). Full reference: [/gateway/configuration](https://docs.openclaw.ai/gateway/configuration#auth-storage-oauth--api-keys) For static secret refs and runtime snapshot activation behavior, see [Secrets Management](https://docs.openclaw.ai/gateway/secrets).

## Anthropic setup-token (subscription auth)

Run `claude setup-token` on any machine, then paste it into OpenClaw:

```
openclaw models auth setup-token --provider anthropic
```

If you generated the token elsewhere, paste it manually:

```
openclaw models auth paste-token --provider anthropic
```

Verify:

## OAuth exchange (how login works)

OpenClaw’s interactive login flows are implemented in `@mariozechner/pi-ai` and wired into the wizards/commands.

### Anthropic setup-token

Flow shape:

1.  run `claude setup-token`
2.  paste the token into OpenClaw
3.  store as a token auth profile (no refresh)

The wizard path is `openclaw onboard` → auth choice `setup-token` (Anthropic).

### OpenAI Codex (ChatGPT OAuth)

OpenAI Codex OAuth is explicitly supported for use outside the Codex CLI, including OpenClaw workflows. Flow shape (PKCE):

1.  generate PKCE verifier/challenge + random `state`
2.  open `https://auth.openai.com/oauth/authorize?...`
3.  try to capture callback on `http://127.0.0.1:1455/auth/callback`
4.  if callback can’t bind (or you’re remote/headless), paste the redirect URL/code
5.  exchange at `https://auth.openai.com/oauth/token`
6.  extract `accountId` from the access token and store `{ access, refresh, expires, accountId }`

Wizard path is `openclaw onboard` → auth choice `openai-codex`.

## Refresh + expiry

Profiles store an `expires` timestamp. At runtime:

*   if `expires` is in the future → use the stored access token
*   if expired → refresh (under a file lock) and overwrite the stored credentials

The refresh flow is automatic; you generally don’t need to manage tokens manually.

## Multiple accounts (profiles) + routing

Two patterns:

### 1) Preferred: separate agents

If you want “personal” and “work” to never interact, use isolated agents (separate sessions + credentials + workspace):

```
openclaw agents add work
openclaw agents add personal
```

Then configure auth per-agent (wizard) and route chats to the right agent.

### 2) Advanced: multiple profiles in one agent

`auth-profiles.json` supports multiple profile IDs for the same provider. Pick which profile is used:

*   globally via config ordering (`auth.order`)
*   per-session via `/model ...@<profileId>`

Example (session override):

*   `/model Opus@anthropic:work`

How to see what profile IDs exist:

*   `openclaw channels list --json` (shows `auth[]`)

Related docs:

*   [/concepts/model-failover](https://docs.openclaw.ai/concepts/model-failover) (rotation + cooldown rules)
*   [/tools/slash-commands](https://docs.openclaw.ai/tools/slash-commands) (command surface)

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/streaming -->

# Streaming and Chunking - OpenClaw

OpenClaw has two separate streaming layers:

*   **Block streaming (channels):** emit completed **blocks** as the assistant writes. These are normal channel messages (not token deltas).
*   **Preview streaming (Telegram/Discord/Slack):** update a temporary **preview message** while generating.

There is **no true token-delta streaming** to channel messages today. Preview streaming is message-based (send + edits/appends).

## Block streaming (channel messages)

Block streaming sends assistant output in coarse chunks as it becomes available.

```
Model output
  └─ text_delta/events
       ├─ (blockStreamingBreak=text_end)
       │    └─ chunker emits blocks as buffer grows
       └─ (blockStreamingBreak=message_end)
            └─ chunker flushes at message_end
                   └─ channel send (block replies)
```

Legend:

*   `text_delta/events`: model stream events (may be sparse for non-streaming models).
*   `chunker`: `EmbeddedBlockChunker` applying min/max bounds + break preference.
*   `channel send`: actual outbound messages (block replies).

**Controls:**

*   `agents.defaults.blockStreamingDefault`: `"on"`/`"off"` (default off).
*   Channel overrides: `*.blockStreaming` (and per-account variants) to force `"on"`/`"off"` per channel.
*   `agents.defaults.blockStreamingBreak`: `"text_end"` or `"message_end"`.
*   `agents.defaults.blockStreamingChunk`: `{ minChars, maxChars, breakPreference? }`.
*   `agents.defaults.blockStreamingCoalesce`: `{ minChars?, maxChars?, idleMs? }` (merge streamed blocks before send).
*   Channel hard cap: `*.textChunkLimit` (e.g., `channels.whatsapp.textChunkLimit`).
*   Channel chunk mode: `*.chunkMode` (`length` default, `newline` splits on blank lines (paragraph boundaries) before length chunking).
*   Discord soft cap: `channels.discord.maxLinesPerMessage` (default 17) splits tall replies to avoid UI clipping.

**Boundary semantics:**

*   `text_end`: stream blocks as soon as chunker emits; flush on each `text_end`.
*   `message_end`: wait until assistant message finishes, then flush buffered output.

`message_end` still uses the chunker if the buffered text exceeds `maxChars`, so it can emit multiple chunks at the end.

## Chunking algorithm (low/high bounds)

Block chunking is implemented by `EmbeddedBlockChunker`:

*   **Low bound:** don’t emit until buffer >= `minChars` (unless forced).
*   **High bound:** prefer splits before `maxChars`; if forced, split at `maxChars`.
*   **Break preference:** `paragraph` → `newline` → `sentence` → `whitespace` → hard break.
*   **Code fences:** never split inside fences; when forced at `maxChars`, close + reopen the fence to keep Markdown valid.

`maxChars` is clamped to the channel `textChunkLimit`, so you can’t exceed per-channel caps.

## Coalescing (merge streamed blocks)

When block streaming is enabled, OpenClaw can **merge consecutive block chunks** before sending them out. This reduces “single-line spam” while still providing progressive output.

*   Coalescing waits for **idle gaps** (`idleMs`) before flushing.
*   Buffers are capped by `maxChars` and will flush if they exceed it.
*   `minChars` prevents tiny fragments from sending until enough text accumulates (final flush always sends remaining text).
*   Joiner is derived from `blockStreamingChunk.breakPreference` (`paragraph` → `\n\n`, `newline` → `\n`, `sentence` → space).
*   Channel overrides are available via `*.blockStreamingCoalesce` (including per-account configs).
*   Default coalesce `minChars` is bumped to 1500 for Signal/Slack/Discord unless overridden.

## Human-like pacing between blocks

When block streaming is enabled, you can add a **randomized pause** between block replies (after the first block). This makes multi-bubble responses feel more natural.

*   Config: `agents.defaults.humanDelay` (override per agent via `agents.list[].humanDelay`).
*   Modes: `off` (default), `natural` (800–2500ms), `custom` (`minMs`/`maxMs`).
*   Applies only to **block replies**, not final replies or tool summaries.

## “Stream chunks or everything”

This maps to:

*   **Stream chunks:** `blockStreamingDefault: "on"` + `blockStreamingBreak: "text_end"` (emit as you go). Non-Telegram channels also need `*.blockStreaming: true`.
*   **Stream everything at end:** `blockStreamingBreak: "message_end"` (flush once, possibly multiple chunks if very long).
*   **No block streaming:** `blockStreamingDefault: "off"` (only final reply).

**Channel note:** Block streaming is **off unless** `*.blockStreaming` is explicitly set to `true`. Channels can stream a live preview (`channels.<channel>.streaming`) without block replies. Config location reminder: the `blockStreaming*` defaults live under `agents.defaults`, not the root config.

## Preview streaming modes

Canonical key: `channels.<channel>.streaming` Modes:

*   `off`: disable preview streaming.
*   `partial`: single preview that is replaced with latest text.
*   `block`: preview updates in chunked/appended steps.
*   `progress`: progress/status preview during generation, final answer at completion.

### Channel mapping

| Channel | `off` | `partial` | `block` | `progress` |
| --- | --- | --- | --- | --- |
| Telegram | ✅   | ✅   | ✅   | maps to `partial` |
| Discord | ✅   | ✅   | ✅   | maps to `partial` |
| Slack | ✅   | ✅   | ✅   | ✅   |

Slack-only:

*   `channels.slack.nativeStreaming` toggles Slack native streaming API calls when `streaming=partial` (default: `true`).

Legacy key migration:

*   Telegram: `streamMode` + boolean `streaming` auto-migrate to `streaming` enum.
*   Discord: `streamMode` + boolean `streaming` auto-migrate to `streaming` enum.
*   Slack: `streamMode` auto-migrates to `streaming` enum; boolean `streaming` auto-migrates to `nativeStreaming`.

### Runtime behavior

Telegram:

*   Uses `sendMessage` + `editMessageText` preview updates across DMs and group/topics.
*   Preview streaming is skipped when Telegram block streaming is explicitly enabled (to avoid double-streaming).
*   `/reasoning stream` can write reasoning to preview.

Discord:

*   Uses send + edit preview messages.
*   `block` mode uses draft chunking (`draftChunk`).
*   Preview streaming is skipped when Discord block streaming is explicitly enabled.

Slack:

*   `partial` can use Slack native streaming (`chat.startStream`/`append`/`stop`) when available.
*   `block` uses append-style draft previews.
*   `progress` uses status preview text, then final answer.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/memory -->

# Memory - OpenClaw

OpenClaw memory is **plain Markdown in the agent workspace**. The files are the source of truth; the model only “remembers” what gets written to disk. Memory search tools are provided by the active memory plugin (default: `memory-core`). Disable memory plugins with `plugins.slots.memory = "none"`.

## Memory files (Markdown)

The default workspace layout uses two memory layers:

*   `memory/YYYY-MM-DD.md`
    *   Daily log (append-only).
    *   Read today + yesterday at session start.
*   `MEMORY.md` (optional)
    *   Curated long-term memory.
    *   **Only load in the main, private session** (never in group contexts).

These files live under the workspace (`agents.defaults.workspace`, default `~/.openclaw/workspace`). See [Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace) for the full layout.

OpenClaw exposes two agent-facing tools for these Markdown files:

*   `memory_search` — semantic recall over indexed snippets.
*   `memory_get` — targeted read of a specific Markdown file/line range.

`memory_get` now **degrades gracefully when a file doesn’t exist** (for example, today’s daily log before the first write). Both the builtin manager and the QMD backend return `{ text: "", path }` instead of throwing `ENOENT`, so agents can handle “nothing recorded yet” and continue their workflow without wrapping the tool call in try/catch logic.

## When to write memory

*   Decisions, preferences, and durable facts go to `MEMORY.md`.
*   Day-to-day notes and running context go to `memory/YYYY-MM-DD.md`.
*   If someone says “remember this,” write it down (do not keep it in RAM).
*   This area is still evolving. It helps to remind the model to store memories; it will know what to do.
*   If you want something to stick, **ask the bot to write it** into memory.

## Automatic memory flush (pre-compaction ping)

When a session is **close to auto-compaction**, OpenClaw triggers a **silent, agentic turn** that reminds the model to write durable memory **before** the context is compacted. The default prompts explicitly say the model _may reply_, but usually `NO_REPLY` is the correct response so the user never sees this turn. This is controlled by `agents.defaults.compaction.memoryFlush`:

```
{
  agents: {
    defaults: {
      compaction: {
        reserveTokensFloor: 20000,
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 4000,
          systemPrompt: "Session nearing compaction. Store durable memories now.",
          prompt: "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store.",
        },
      },
    },
  },
}
```

Details:

*   **Soft threshold**: flush triggers when the session token estimate crosses `contextWindow - reserveTokensFloor - softThresholdTokens`.
*   **Silent** by default: prompts include `NO_REPLY` so nothing is delivered.
*   **Two prompts**: a user prompt plus a system prompt append the reminder.
*   **One flush per compaction cycle** (tracked in `sessions.json`).
*   **Workspace must be writable**: if the session runs sandboxed with `workspaceAccess: "ro"` or `"none"`, the flush is skipped.

For the full compaction lifecycle, see [Session management + compaction](https://docs.openclaw.ai/reference/session-management-compaction).

## Vector memory search

OpenClaw can build a small vector index over `MEMORY.md` and `memory/*.md` so semantic queries can find related notes even when wording differs. Defaults:

*   Enabled by default.
*   Watches memory files for changes (debounced).
*   Configure memory search under `agents.defaults.memorySearch` (not top-level `memorySearch`).
*   Uses remote embeddings by default. If `memorySearch.provider` is not set, OpenClaw auto-selects:
    1.  `local` if a `memorySearch.local.modelPath` is configured and the file exists.
    2.  `openai` if an OpenAI key can be resolved.
    3.  `gemini` if a Gemini key can be resolved.
    4.  `voyage` if a Voyage key can be resolved.
    5.  `mistral` if a Mistral key can be resolved.
    6.  Otherwise memory search stays disabled until configured.
*   Local mode uses node-llama-cpp and may require `pnpm approve-builds`.
*   Uses sqlite-vec (when available) to accelerate vector search inside SQLite.
*   `memorySearch.provider = "ollama"` is also supported for local/self-hosted Ollama embeddings (`/api/embeddings`), but it is not auto-selected.

Remote embeddings **require** an API key for the embedding provider. OpenClaw resolves keys from auth profiles, `models.providers.*.apiKey`, or environment variables. Codex OAuth only covers chat/completions and does **not** satisfy embeddings for memory search. For Gemini, use `GEMINI_API_KEY` or `models.providers.google.apiKey`. For Voyage, use `VOYAGE_API_KEY` or `models.providers.voyage.apiKey`. For Mistral, use `MISTRAL_API_KEY` or `models.providers.mistral.apiKey`. Ollama typically does not require a real API key (a placeholder like `OLLAMA_API_KEY=ollama-local` is enough when needed by local policy). When using a custom OpenAI-compatible endpoint, set `memorySearch.remote.apiKey` (and optional `memorySearch.remote.headers`).

### QMD backend (experimental)

Set `memory.backend = "qmd"` to swap the built-in SQLite indexer for [QMD](https://github.com/tobi/qmd): a local-first search sidecar that combines BM25 + vectors + reranking. Markdown stays the source of truth; OpenClaw shells out to QMD for retrieval. Key points: **Prereqs**

*   Disabled by default. Opt in per-config (`memory.backend = "qmd"`).
*   Install the QMD CLI separately (`bun install -g https://github.com/tobi/qmd` or grab a release) and make sure the `qmd` binary is on the gateway’s `PATH`.
*   QMD needs an SQLite build that allows extensions (`brew install sqlite` on macOS).
*   QMD runs fully locally via Bun + `node-llama-cpp` and auto-downloads GGUF models from HuggingFace on first use (no separate Ollama daemon required).
*   The gateway runs QMD in a self-contained XDG home under `~/.openclaw/agents/<agentId>/qmd/` by setting `XDG_CONFIG_HOME` and `XDG_CACHE_HOME`.
*   OS support: macOS and Linux work out of the box once Bun + SQLite are installed. Windows is best supported via WSL2.

**How the sidecar runs**

*   The gateway writes a self-contained QMD home under `~/.openclaw/agents/<agentId>/qmd/` (config + cache + sqlite DB).
*   Collections are created via `qmd collection add` from `memory.qmd.paths` (plus default workspace memory files), then `qmd update` + `qmd embed` run on boot and on a configurable interval (`memory.qmd.update.interval`, default 5 m).
*   The gateway now initializes the QMD manager on startup, so periodic update timers are armed even before the first `memory_search` call.
*   Boot refresh now runs in the background by default so chat startup is not blocked; set `memory.qmd.update.waitForBootSync = true` to keep the previous blocking behavior.
*   Searches run via `memory.qmd.searchMode` (default `qmd search --json`; also supports `vsearch` and `query`). If the selected mode rejects flags on your QMD build, OpenClaw retries with `qmd query`. If QMD fails or the binary is missing, OpenClaw automatically falls back to the builtin SQLite manager so memory tools keep working.
*   OpenClaw does not expose QMD embed batch-size tuning today; batch behavior is controlled by QMD itself.
*   **First search may be slow**: QMD may download local GGUF models (reranker/query expansion) on the first `qmd query` run.
    *   OpenClaw sets `XDG_CONFIG_HOME`/`XDG_CACHE_HOME` automatically when it runs QMD.
    *   If you want to pre-download models manually (and warm the same index OpenClaw uses), run a one-off query with the agent’s XDG dirs. OpenClaw’s QMD state lives under your **state dir** (defaults to `~/.openclaw`). You can point `qmd` at the exact same index by exporting the same XDG vars OpenClaw uses:
        
        ```
        # Pick the same state dir OpenClaw uses
        STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
        
        export XDG_CONFIG_HOME="$STATE_DIR/agents/main/qmd/xdg-config"
        export XDG_CACHE_HOME="$STATE_DIR/agents/main/qmd/xdg-cache"
        
        # (Optional) force an index refresh + embeddings
        qmd update
        qmd embed
        
        # Warm up / trigger first-time model downloads
        qmd query "test" -c memory-root --json >/dev/null 2>&1
        ```
        

**Config surface (`memory.qmd.*`)**

*   `command` (default `qmd`): override the executable path.
*   `searchMode` (default `search`): pick which QMD command backs `memory_search` (`search`, `vsearch`, `query`).
*   `includeDefaultMemory` (default `true`): auto-index `MEMORY.md` + `memory/**/*.md`.
*   `paths[]`: add extra directories/files (`path`, optional `pattern`, optional stable `name`).
*   `sessions`: opt into session JSONL indexing (`enabled`, `retentionDays`, `exportDir`).
*   `update`: controls refresh cadence and maintenance execution: (`interval`, `debounceMs`, `onBoot`, `waitForBootSync`, `embedInterval`, `commandTimeoutMs`, `updateTimeoutMs`, `embedTimeoutMs`).
*   `limits`: clamp recall payload (`maxResults`, `maxSnippetChars`, `maxInjectedChars`, `timeoutMs`).
*   `scope`: same schema as [`session.sendPolicy`](https://docs.openclaw.ai/gateway/configuration#session). Default is DM-only (`deny` all, `allow` direct chats); loosen it to surface QMD hits in groups/channels.
    *   `match.keyPrefix` matches the **normalized** session key (lowercased, with any leading `agent:<id>:` stripped). Example: `discord:channel:`.
    *   `match.rawKeyPrefix` matches the **raw** session key (lowercased), including `agent:<id>:`. Example: `agent:main:discord:`.
    *   Legacy: `match.keyPrefix: "agent:..."` is still treated as a raw-key prefix, but prefer `rawKeyPrefix` for clarity.
*   When `scope` denies a search, OpenClaw logs a warning with the derived `channel`/`chatType` so empty results are easier to debug.
*   Snippets sourced outside the workspace show up as `qmd/<collection>/<relative-path>` in `memory_search` results; `memory_get` understands that prefix and reads from the configured QMD collection root.
*   When `memory.qmd.sessions.enabled = true`, OpenClaw exports sanitized session transcripts (User/Assistant turns) into a dedicated QMD collection under `~/.openclaw/agents/<id>/qmd/sessions/`, so `memory_search` can recall recent conversations without touching the builtin SQLite index.
*   `memory_search` snippets now include a `Source: <path#line>` footer when `memory.citations` is `auto`/`on`; set `memory.citations = "off"` to keep the path metadata internal (the agent still receives the path for `memory_get`, but the snippet text omits the footer and the system prompt warns the agent not to cite it).

**Example**

```
memory: {
  backend: "qmd",
  citations: "auto",
  qmd: {
    includeDefaultMemory: true,
    update: { interval: "5m", debounceMs: 15000 },
    limits: { maxResults: 6, timeoutMs: 4000 },
    scope: {
      default: "deny",
      rules: [
        { action: "allow", match: { chatType: "direct" } },
        // Normalized session-key prefix (strips `agent:<id>:`).
        { action: "deny", match: { keyPrefix: "discord:channel:" } },
        // Raw session-key prefix (includes `agent:<id>:`).
        { action: "deny", match: { rawKeyPrefix: "agent:main:discord:" } },
      ]
    },
    paths: [
      { name: "docs", path: "~/notes", pattern: "**/*.md" }
    ]
  }
}
```

**Citations & fallback**

*   `memory.citations` applies regardless of backend (`auto`/`on`/`off`).
*   When `qmd` runs, we tag `status().backend = "qmd"` so diagnostics show which engine served the results. If the QMD subprocess exits or JSON output can’t be parsed, the search manager logs a warning and returns the builtin provider (existing Markdown embeddings) until QMD recovers.

### Additional memory paths

If you want to index Markdown files outside the default workspace layout, add explicit paths:

```
agents: {
  defaults: {
    memorySearch: {
      extraPaths: ["../team-docs", "/srv/shared-notes/overview.md"]
    }
  }
}
```

Notes:

*   Paths can be absolute or workspace-relative.
*   Directories are scanned recursively for `.md` files.
*   Only Markdown files are indexed.
*   Symlinks are ignored (files or directories).

### Gemini embeddings (native)

Set the provider to `gemini` to use the Gemini embeddings API directly:

```
agents: {
  defaults: {
    memorySearch: {
      provider: "gemini",
      model: "gemini-embedding-001",
      remote: {
        apiKey: "YOUR_GEMINI_API_KEY"
      }
    }
  }
}
```

Notes:

*   `remote.baseUrl` is optional (defaults to the Gemini API base URL).
*   `remote.headers` lets you add extra headers if needed.
*   Default model: `gemini-embedding-001`.

If you want to use a **custom OpenAI-compatible endpoint** (OpenRouter, vLLM, or a proxy), you can use the `remote` configuration with the OpenAI provider:

```
agents: {
  defaults: {
    memorySearch: {
      provider: "openai",
      model: "text-embedding-3-small",
      remote: {
        baseUrl: "https://api.example.com/v1/",
        apiKey: "YOUR_OPENAI_COMPAT_API_KEY",
        headers: { "X-Custom-Header": "value" }
      }
    }
  }
}
```

If you don’t want to set an API key, use `memorySearch.provider = "local"` or set `memorySearch.fallback = "none"`. Fallbacks:

*   `memorySearch.fallback` can be `openai`, `gemini`, `voyage`, `mistral`, `ollama`, `local`, or `none`.
*   The fallback provider is only used when the primary embedding provider fails.

Batch indexing (OpenAI + Gemini + Voyage):

*   Disabled by default. Set `agents.defaults.memorySearch.remote.batch.enabled = true` to enable for large-corpus indexing (OpenAI, Gemini, and Voyage).
*   Default behavior waits for batch completion; tune `remote.batch.wait`, `remote.batch.pollIntervalMs`, and `remote.batch.timeoutMinutes` if needed.
*   Set `remote.batch.concurrency` to control how many batch jobs we submit in parallel (default: 2).
*   Batch mode applies when `memorySearch.provider = "openai"` or `"gemini"` and uses the corresponding API key.
*   Gemini batch jobs use the async embeddings batch endpoint and require Gemini Batch API availability.

Why OpenAI batch is fast + cheap:

*   For large backfills, OpenAI is typically the fastest option we support because we can submit many embedding requests in a single batch job and let OpenAI process them asynchronously.
*   OpenAI offers discounted pricing for Batch API workloads, so large indexing runs are usually cheaper than sending the same requests synchronously.
*   See the OpenAI Batch API docs and pricing for details:
    *   [https://platform.openai.com/docs/api-reference/batch](https://platform.openai.com/docs/api-reference/batch)
    *   [https://platform.openai.com/pricing](https://platform.openai.com/pricing)

Config example:

```
agents: {
  defaults: {
    memorySearch: {
      provider: "openai",
      model: "text-embedding-3-small",
      fallback: "openai",
      remote: {
        batch: { enabled: true, concurrency: 2 }
      },
      sync: { watch: true }
    }
  }
}
```

Tools:

*   `memory_search` — returns snippets with file + line ranges.
*   `memory_get` — read memory file content by path.

Local mode:

*   Set `agents.defaults.memorySearch.provider = "local"`.
*   Provide `agents.defaults.memorySearch.local.modelPath` (GGUF or `hf:` URI).
*   Optional: set `agents.defaults.memorySearch.fallback = "none"` to avoid remote fallback.

### How the memory tools work

*   `memory_search` semantically searches Markdown chunks (~400 token target, 80-token overlap) from `MEMORY.md` + `memory/**/*.md`. It returns snippet text (capped ~700 chars), file path, line range, score, provider/model, and whether we fell back from local → remote embeddings. No full file payload is returned.
*   `memory_get` reads a specific memory Markdown file (workspace-relative), optionally from a starting line and for N lines. Paths outside `MEMORY.md` / `memory/` are rejected.
*   Both tools are enabled only when `memorySearch.enabled` resolves true for the agent.

### What gets indexed (and when)

*   File type: Markdown only (`MEMORY.md`, `memory/**/*.md`).
*   Index storage: per-agent SQLite at `~/.openclaw/memory/<agentId>.sqlite` (configurable via `agents.defaults.memorySearch.store.path`, supports `{agentId}` token).
*   Freshness: watcher on `MEMORY.md` + `memory/` marks the index dirty (debounce 1.5s). Sync is scheduled on session start, on search, or on an interval and runs asynchronously. Session transcripts use delta thresholds to trigger background sync.
*   Reindex triggers: the index stores the embedding **provider/model + endpoint fingerprint + chunking params**. If any of those change, OpenClaw automatically resets and reindexes the entire store.

### Hybrid search (BM25 + vector)

When enabled, OpenClaw combines:

*   **Vector similarity** (semantic match, wording can differ)
*   **BM25 keyword relevance** (exact tokens like IDs, env vars, code symbols)

If full-text search is unavailable on your platform, OpenClaw falls back to vector-only search.

#### Why hybrid?

Vector search is great at “this means the same thing”:

*   “Mac Studio gateway host” vs “the machine running the gateway”
*   “debounce file updates” vs “avoid indexing on every write”

But it can be weak at exact, high-signal tokens:

*   IDs (`a828e60`, `b3b9895a…`)
*   code symbols (`memorySearch.query.hybrid`)
*   error strings (“sqlite-vec unavailable”)

BM25 (full-text) is the opposite: strong at exact tokens, weaker at paraphrases. Hybrid search is the pragmatic middle ground: **use both retrieval signals** so you get good results for both “natural language” queries and “needle in a haystack” queries.

#### How we merge results (the current design)

Implementation sketch:

1.  Retrieve a candidate pool from both sides:

*   **Vector**: top `maxResults * candidateMultiplier` by cosine similarity.
*   **BM25**: top `maxResults * candidateMultiplier` by FTS5 BM25 rank (lower is better).

2.  Convert BM25 rank into a 0..1-ish score:

*   `textScore = 1 / (1 + max(0, bm25Rank))`

3.  Union candidates by chunk id and compute a weighted score:

*   `finalScore = vectorWeight * vectorScore + textWeight * textScore`

Notes:

*   `vectorWeight` + `textWeight` is normalized to 1.0 in config resolution, so weights behave as percentages.
*   If embeddings are unavailable (or the provider returns a zero-vector), we still run BM25 and return keyword matches.
*   If FTS5 can’t be created, we keep vector-only search (no hard failure).

This isn’t “IR-theory perfect”, but it’s simple, fast, and tends to improve recall/precision on real notes. If we want to get fancier later, common next steps are Reciprocal Rank Fusion (RRF) or score normalization (min/max or z-score) before mixing.

#### Post-processing pipeline

After merging vector and keyword scores, two optional post-processing stages refine the result list before it reaches the agent:

```
Vector + Keyword → Weighted Merge → Temporal Decay → Sort → MMR → Top-K Results
```

Both stages are **off by default** and can be enabled independently.

#### MMR re-ranking (diversity)

When hybrid search returns results, multiple chunks may contain similar or overlapping content. For example, searching for “home network setup” might return five nearly identical snippets from different daily notes that all mention the same router configuration. **MMR (Maximal Marginal Relevance)** re-ranks the results to balance relevance with diversity, ensuring the top results cover different aspects of the query instead of repeating the same information. How it works:

1.  Results are scored by their original relevance (vector + BM25 weighted score).
2.  MMR iteratively selects results that maximize: `λ × relevance − (1−λ) × max_similarity_to_selected`.
3.  Similarity between results is measured using Jaccard text similarity on tokenized content.

The `lambda` parameter controls the trade-off:

*   `lambda = 1.0` → pure relevance (no diversity penalty)
*   `lambda = 0.0` → maximum diversity (ignores relevance)
*   Default: `0.7` (balanced, slight relevance bias)

**Example — query: “home network setup”** Given these memory files:

```
memory/2026-02-10.md  → "Configured Omada router, set VLAN 10 for IoT devices"
memory/2026-02-08.md  → "Configured Omada router, moved IoT to VLAN 10"
memory/2026-02-05.md  → "Set up AdGuard DNS on 192.168.10.2"
memory/network.md     → "Router: Omada ER605, AdGuard: 192.168.10.2, VLAN 10: IoT"
```

Without MMR — top 3 results:

```
1. memory/2026-02-10.md  (score: 0.92)  ← router + VLAN
2. memory/2026-02-08.md  (score: 0.89)  ← router + VLAN (near-duplicate!)
3. memory/network.md     (score: 0.85)  ← reference doc
```

With MMR (λ=0.7) — top 3 results:

```
1. memory/2026-02-10.md  (score: 0.92)  ← router + VLAN
2. memory/network.md     (score: 0.85)  ← reference doc (diverse!)
3. memory/2026-02-05.md  (score: 0.78)  ← AdGuard DNS (diverse!)
```

The near-duplicate from Feb 8 drops out, and the agent gets three distinct pieces of information. **When to enable:** If you notice `memory_search` returning redundant or near-duplicate snippets, especially with daily notes that often repeat similar information across days.

#### Temporal decay (recency boost)

Agents with daily notes accumulate hundreds of dated files over time. Without decay, a well-worded note from six months ago can outrank yesterday’s update on the same topic. **Temporal decay** applies an exponential multiplier to scores based on the age of each result, so recent memories naturally rank higher while old ones fade:

```
decayedScore = score × e^(-λ × ageInDays)
```

where `λ = ln(2) / halfLifeDays`. With the default half-life of 30 days:

*   Today’s notes: **100%** of original score
*   7 days ago: **~84%**
*   30 days ago: **50%**
*   90 days ago: **12.5%**
*   180 days ago: **~1.6%**

**Evergreen files are never decayed:**

*   `MEMORY.md` (root memory file)
*   Non-dated files in `memory/` (e.g., `memory/projects.md`, `memory/network.md`)
*   These contain durable reference information that should always rank normally.

**Dated daily files** (`memory/YYYY-MM-DD.md`) use the date extracted from the filename. Other sources (e.g., session transcripts) fall back to file modification time (`mtime`). **Example — query: “what’s Rod’s work schedule?”** Given these memory files (today is Feb 10):

```
memory/2025-09-15.md  → "Rod works Mon-Fri, standup at 10am, pairing at 2pm"  (148 days old)
memory/2026-02-10.md  → "Rod has standup at 14:15, 1:1 with Zeb at 14:45"    (today)
memory/2026-02-03.md  → "Rod started new team, standup moved to 14:15"        (7 days old)
```

Without decay:

```
1. memory/2025-09-15.md  (score: 0.91)  ← best semantic match, but stale!
2. memory/2026-02-10.md  (score: 0.82)
3. memory/2026-02-03.md  (score: 0.80)
```

With decay (halfLife=30):

```
1. memory/2026-02-10.md  (score: 0.82 × 1.00 = 0.82)  ← today, no decay
2. memory/2026-02-03.md  (score: 0.80 × 0.85 = 0.68)  ← 7 days, mild decay
3. memory/2025-09-15.md  (score: 0.91 × 0.03 = 0.03)  ← 148 days, nearly gone
```

The stale September note drops to the bottom despite having the best raw semantic match. **When to enable:** If your agent has months of daily notes and you find that old, stale information outranks recent context. A half-life of 30 days works well for daily-note-heavy workflows; increase it (e.g., 90 days) if you reference older notes frequently.

#### Configuration

Both features are configured under `memorySearch.query.hybrid`:

```
agents: {
  defaults: {
    memorySearch: {
      query: {
        hybrid: {
          enabled: true,
          vectorWeight: 0.7,
          textWeight: 0.3,
          candidateMultiplier: 4,
          // Diversity: reduce redundant results
          mmr: {
            enabled: true,    // default: false
            lambda: 0.7       // 0 = max diversity, 1 = max relevance
          },
          // Recency: boost newer memories
          temporalDecay: {
            enabled: true,    // default: false
            halfLifeDays: 30  // score halves every 30 days
          }
        }
      }
    }
  }
}
```

You can enable either feature independently:

*   **MMR only** — useful when you have many similar notes but age doesn’t matter.
*   **Temporal decay only** — useful when recency matters but your results are already diverse.
*   **Both** — recommended for agents with large, long-running daily note histories.

### Embedding cache

OpenClaw can cache **chunk embeddings** in SQLite so reindexing and frequent updates (especially session transcripts) don’t re-embed unchanged text. Config:

```
agents: {
  defaults: {
    memorySearch: {
      cache: {
        enabled: true,
        maxEntries: 50000
      }
    }
  }
}
```

### Session memory search (experimental)

You can optionally index **session transcripts** and surface them via `memory_search`. This is gated behind an experimental flag.

```
agents: {
  defaults: {
    memorySearch: {
      experimental: { sessionMemory: true },
      sources: ["memory", "sessions"]
    }
  }
}
```

Notes:

*   Session indexing is **opt-in** (off by default).
*   Session updates are debounced and **indexed asynchronously** once they cross delta thresholds (best-effort).
*   `memory_search` never blocks on indexing; results can be slightly stale until background sync finishes.
*   Results still include snippets only; `memory_get` remains limited to memory files.
*   Session indexing is isolated per agent (only that agent’s session logs are indexed).
*   Session logs live on disk (`~/.openclaw/agents/<agentId>/sessions/*.jsonl`). Any process/user with filesystem access can read them, so treat disk access as the trust boundary. For stricter isolation, run agents under separate OS users or hosts.

Delta thresholds (defaults shown):

```
agents: {
  defaults: {
    memorySearch: {
      sync: {
        sessions: {
          deltaBytes: 100000,   // ~100 KB
          deltaMessages: 50     // JSONL lines
        }
      }
    }
  }
}
```

### SQLite vector acceleration (sqlite-vec)

When the sqlite-vec extension is available, OpenClaw stores embeddings in a SQLite virtual table (`vec0`) and performs vector distance queries in the database. This keeps search fast without loading every embedding into JS. Configuration (optional):

```
agents: {
  defaults: {
    memorySearch: {
      store: {
        vector: {
          enabled: true,
          extensionPath: "/path/to/sqlite-vec"
        }
      }
    }
  }
}
```

Notes:

*   `enabled` defaults to true; when disabled, search falls back to in-process cosine similarity over stored embeddings.
*   If the sqlite-vec extension is missing or fails to load, OpenClaw logs the error and continues with the JS fallback (no vector table).
*   `extensionPath` overrides the bundled sqlite-vec path (useful for custom builds or non-standard install locations).

### Local embedding auto-download

*   Default local embedding model: `hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF/embeddinggemma-300m-qat-Q8_0.gguf` (~0.6 GB).
*   When `memorySearch.provider = "local"`, `node-llama-cpp` resolves `modelPath`; if the GGUF is missing it **auto-downloads** to the cache (or `local.modelCacheDir` if set), then loads it. Downloads resume on retry.
*   Native build requirement: run `pnpm approve-builds`, pick `node-llama-cpp`, then `pnpm rebuild node-llama-cpp`.
*   Fallback: if local setup fails and `memorySearch.fallback = "openai"`, we automatically switch to remote embeddings (`openai/text-embedding-3-small` unless overridden) and record the reason.

### Custom OpenAI-compatible endpoint example

```
agents: {
  defaults: {
    memorySearch: {
      provider: "openai",
      model: "text-embedding-3-small",
      remote: {
        baseUrl: "https://api.example.com/v1/",
        apiKey: "YOUR_REMOTE_API_KEY",
        headers: {
          "X-Organization": "org-id",
          "X-Project": "project-id"
        }
      }
    }
  }
}
```

Notes:

*   `remote.*` takes precedence over `models.providers.openai.*`.
*   `remote.headers` merge with OpenAI headers; remote wins on key conflicts. Omit `remote.headers` to use the OpenAI defaults.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/queue -->

# Command Queue - OpenClaw

## Command Queue (2026-01-16)

We serialize inbound auto-reply runs (all channels) through a tiny in-process queue to prevent multiple agent runs from colliding, while still allowing safe parallelism across sessions.

## Why

*   Auto-reply runs can be expensive (LLM calls) and can collide when multiple inbound messages arrive close together.
*   Serializing avoids competing for shared resources (session files, logs, CLI stdin) and reduces the chance of upstream rate limits.

## How it works

*   A lane-aware FIFO queue drains each lane with a configurable concurrency cap (default 1 for unconfigured lanes; main defaults to 4, subagent to 8).
*   `runEmbeddedPiAgent` enqueues by **session key** (lane `session:<key>`) to guarantee only one active run per session.
*   Each session run is then queued into a **global lane** (`main` by default) so overall parallelism is capped by `agents.defaults.maxConcurrent`.
*   When verbose logging is enabled, queued runs emit a short notice if they waited more than ~2s before starting.
*   Typing indicators still fire immediately on enqueue (when supported by the channel) so user experience is unchanged while we wait our turn.

## Queue modes (per channel)

Inbound messages can steer the current run, wait for a followup turn, or do both:

*   `steer`: inject immediately into the current run (cancels pending tool calls after the next tool boundary). If not streaming, falls back to followup.
*   `followup`: enqueue for the next agent turn after the current run ends.
*   `collect`: coalesce all queued messages into a **single** followup turn (default). If messages target different channels/threads, they drain individually to preserve routing.
*   `steer-backlog` (aka `steer+backlog`): steer now **and** preserve the message for a followup turn.
*   `interrupt` (legacy): abort the active run for that session, then run the newest message.
*   `queue` (legacy alias): same as `steer`.

Steer-backlog means you can get a followup response after the steered run, so streaming surfaces can look like duplicates. Prefer `collect`/`steer` if you want one response per inbound message. Send `/queue collect` as a standalone command (per-session) or set `messages.queue.byChannel.discord: "collect"`. Defaults (when unset in config):

*   All surfaces → `collect`

Configure globally or per channel via `messages.queue`:

```
{
  messages: {
    queue: {
      mode: "collect",
      debounceMs: 1000,
      cap: 20,
      drop: "summarize",
      byChannel: { discord: "collect" },
    },
  },
}
```

## Queue options

Options apply to `followup`, `collect`, and `steer-backlog` (and to `steer` when it falls back to followup):

*   `debounceMs`: wait for quiet before starting a followup turn (prevents “continue, continue”).
*   `cap`: max queued messages per session.
*   `drop`: overflow policy (`old`, `new`, `summarize`).

Summarize keeps a short bullet list of dropped messages and injects it as a synthetic followup prompt. Defaults: `debounceMs: 1000`, `cap: 20`, `drop: summarize`.

## Per-session overrides

*   Send `/queue <mode>` as a standalone command to store the mode for the current session.
*   Options can be combined: `/queue collect debounce:2s cap:25 drop:summarize`
*   `/queue default` or `/queue reset` clears the session override.

## Scope and guarantees

*   Applies to auto-reply agent runs across all inbound channels that use the gateway reply pipeline (WhatsApp web, Telegram, Slack, Discord, Signal, iMessage, webchat, etc.).
*   Default lane (`main`) is process-wide for inbound + main heartbeats; set `agents.defaults.maxConcurrent` to allow multiple sessions in parallel.
*   Additional lanes may exist (e.g. `cron`, `subagent`) so background jobs can run in parallel without blocking inbound replies.
*   Per-session lanes guarantee that only one agent run touches a given session at a time.
*   No external dependencies or background worker threads; pure TypeScript + promises.

## Troubleshooting

*   If commands seem stuck, enable verbose logs and look for “queued for …ms” lines to confirm the queue is draining.
*   If you need queue depth, enable verbose logs and watch for queue timing lines.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/retry -->

# Retry Policy - OpenClaw

## Goals

*   Retry per HTTP request, not per multi-step flow.
*   Preserve ordering by retrying only the current step.
*   Avoid duplicating non-idempotent operations.

## Defaults

*   Attempts: 3
*   Max delay cap: 30000 ms
*   Jitter: 0.1 (10 percent)
*   Provider defaults:
    *   Telegram min delay: 400 ms
    *   Discord min delay: 500 ms

## Behavior

### Discord

*   Retries only on rate-limit errors (HTTP 429).
*   Uses Discord `retry_after` when available, otherwise exponential backoff.

### Telegram

*   Retries on transient errors (429, timeout, connect/reset/closed, temporarily unavailable).
*   Uses `retry_after` when available, otherwise exponential backoff.
*   Markdown parse errors are not retried; they fall back to plain text.

## Configuration

Set retry policy per provider in `~/.openclaw/openclaw.json`:

```
{
  channels: {
    telegram: {
      retry: {
        attempts: 3,
        minDelayMs: 400,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
    discord: {
      retry: {
        attempts: 3,
        minDelayMs: 500,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
  },
}
```

## Notes

*   Retries apply per request (message send, media upload, reaction, poll, sticker).
*   Composite flows do not retry completed steps.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/compaction -->

# Compaction - OpenClaw

## Context Window & Compaction

Every model has a **context window** (max tokens it can see). Long-running chats accumulate messages and tool results; once the window is tight, OpenClaw **compacts** older history to stay within limits.

## What compaction is

Compaction **summarizes older conversation** into a compact summary entry and keeps recent messages intact. The summary is stored in the session history, so future requests use:

*   The compaction summary
*   Recent messages after the compaction point

Compaction **persists** in the session’s JSONL history.

## Configuration

Use the `agents.defaults.compaction` setting in your `openclaw.json` to configure compaction behavior (mode, target tokens, etc.). Compaction summarization preserves opaque identifiers by default (`identifierPolicy: "strict"`). You can override this with `identifierPolicy: "off"` or provide custom text with `identifierPolicy: "custom"` and `identifierInstructions`. You can optionally specify a different model for compaction summarization via `agents.defaults.compaction.model`. This is useful when your primary model is a local or small model and you want compaction summaries produced by a more capable model. The override accepts any `provider/model-id` string:

```
{
  "agents": {
    "defaults": {
      "compaction": {
        "model": "openrouter/anthropic/claude-sonnet-4-5"
      }
    }
  }
}
```

This also works with local models, for example a second Ollama model dedicated to summarization or a fine-tuned compaction specialist:

```
{
  "agents": {
    "defaults": {
      "compaction": {
        "model": "ollama/llama3.1:8b"
      }
    }
  }
}
```

When unset, compaction uses the agent’s primary model.

## Auto-compaction (default on)

When a session nears or exceeds the model’s context window, OpenClaw triggers auto-compaction and may retry the original request using the compacted context. You’ll see:

*   `🧹 Auto-compaction complete` in verbose mode
*   `/status` showing `🧹 Compactions: <count>`

Before compaction, OpenClaw can run a **silent memory flush** turn to store durable notes to disk. See [Memory](https://docs.openclaw.ai/concepts/memory) for details and config.

## Manual compaction

Use `/compact` (optionally with instructions) to force a compaction pass:

```
/compact Focus on decisions and open questions
```

## Context window source

Context window is model-specific. OpenClaw uses the model definition from the configured provider catalog to determine limits.

## Compaction vs pruning

*   **Compaction**: summarises and **persists** in JSONL.
*   **Session pruning**: trims old **tool results** only, **in-memory**, per request.

See [/concepts/session-pruning](https://docs.openclaw.ai/concepts/session-pruning) for pruning details.

## OpenAI server-side compaction

OpenClaw also supports OpenAI Responses server-side compaction hints for compatible direct OpenAI models. This is separate from local OpenClaw compaction and can run alongside it.

*   Local compaction: OpenClaw summarizes and persists into session JSONL.
*   Server-side compaction: OpenAI compacts context on the provider side when `store` + `context_management` are enabled.

See [OpenAI provider](https://docs.openclaw.ai/providers/openai) for model params and overrides.

## Tips

*   Use `/compact` when sessions feel stale or context is bloated.
*   Large tool outputs are already truncated; pruning can further reduce tool-result buildup.
*   If you need a fresh slate, `/new` or `/reset` starts a new session id.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/messages -->

# Messages - OpenClaw

This page ties together how OpenClaw handles inbound messages, sessions, queueing, streaming, and reasoning visibility.

## Message flow (high level)

```
Inbound message
  -> routing/bindings -> session key
  -> queue (if a run is active)
  -> agent run (streaming + tools)
  -> outbound replies (channel limits + chunking)
```

Key knobs live in configuration:

*   `messages.*` for prefixes, queueing, and group behavior.
*   `agents.defaults.*` for block streaming and chunking defaults.
*   Channel overrides (`channels.whatsapp.*`, `channels.telegram.*`, etc.) for caps and streaming toggles.

See [Configuration](https://docs.openclaw.ai/gateway/configuration) for full schema.

## Inbound dedupe

Channels can redeliver the same message after reconnects. OpenClaw keeps a short-lived cache keyed by channel/account/peer/session/message id so duplicate deliveries do not trigger another agent run.

## Inbound debouncing

Rapid consecutive messages from the **same sender** can be batched into a single agent turn via `messages.inbound`. Debouncing is scoped per channel + conversation and uses the most recent message for reply threading/IDs. Config (global default + per-channel overrides):

```
{
  messages: {
    inbound: {
      debounceMs: 2000,
      byChannel: {
        whatsapp: 5000,
        slack: 1500,
        discord: 1500,
      },
    },
  },
}
```

Notes:

*   Debounce applies to **text-only** messages; media/attachments flush immediately.
*   Control commands bypass debouncing so they remain standalone.

## Sessions and devices

Sessions are owned by the gateway, not by clients.

*   Direct chats collapse into the agent main session key.
*   Groups/channels get their own session keys.
*   The session store and transcripts live on the gateway host.

Multiple devices/channels can map to the same session, but history is not fully synced back to every client. Recommendation: use one primary device for long conversations to avoid divergent context. The Control UI and TUI always show the gateway-backed session transcript, so they are the source of truth. Details: [Session management](https://docs.openclaw.ai/concepts/session).

## Inbound bodies and history context

OpenClaw separates the **prompt body** from the **command body**:

*   `Body`: prompt text sent to the agent. This may include channel envelopes and optional history wrappers.
*   `CommandBody`: raw user text for directive/command parsing.
*   `RawBody`: legacy alias for `CommandBody` (kept for compatibility).

When a channel supplies history, it uses a shared wrapper:

*   `[Chat messages since your last reply - for context]`
*   `[Current message - respond to this]`

For **non-direct chats** (groups/channels/rooms), the **current message body** is prefixed with the sender label (same style used for history entries). This keeps real-time and queued/history messages consistent in the agent prompt. History buffers are **pending-only**: they include group messages that did _not_ trigger a run (for example, mention-gated messages) and **exclude** messages already in the session transcript. Directive stripping only applies to the **current message** section so history remains intact. Channels that wrap history should set `CommandBody` (or `RawBody`) to the original message text and keep `Body` as the combined prompt. History buffers are configurable via `messages.groupChat.historyLimit` (global default) and per-channel overrides like `channels.slack.historyLimit` or `channels.telegram.accounts.<id>.historyLimit` (set `0` to disable).

## Queueing and followups

If a run is already active, inbound messages can be queued, steered into the current run, or collected for a followup turn.

*   Configure via `messages.queue` (and `messages.queue.byChannel`).
*   Modes: `interrupt`, `steer`, `followup`, `collect`, plus backlog variants.

Details: [Queueing](https://docs.openclaw.ai/concepts/queue).

## Streaming, chunking, and batching

Block streaming sends partial replies as the model produces text blocks. Chunking respects channel text limits and avoids splitting fenced code. Key settings:

*   `agents.defaults.blockStreamingDefault` (`on|off`, default off)
*   `agents.defaults.blockStreamingBreak` (`text_end|message_end`)
*   `agents.defaults.blockStreamingChunk` (`minChars|maxChars|breakPreference`)
*   `agents.defaults.blockStreamingCoalesce` (idle-based batching)
*   `agents.defaults.humanDelay` (human-like pause between block replies)
*   Channel overrides: `*.blockStreaming` and `*.blockStreamingCoalesce` (non-Telegram channels require explicit `*.blockStreaming: true`)

Details: [Streaming + chunking](https://docs.openclaw.ai/concepts/streaming).

## Reasoning visibility and tokens

OpenClaw can expose or hide model reasoning:

*   `/reasoning on|off|stream` controls visibility.
*   Reasoning content still counts toward token usage when produced by the model.
*   Telegram supports reasoning stream into the draft bubble.

Details: [Thinking + reasoning directives](https://docs.openclaw.ai/tools/thinking) and [Token use](https://docs.openclaw.ai/reference/token-use).

## Prefixes, threading, and replies

Outbound message formatting is centralized in `messages`:

*   `messages.responsePrefix`, `channels.<channel>.responsePrefix`, and `channels.<channel>.accounts.<id>.responsePrefix` (outbound prefix cascade), plus `channels.whatsapp.messagePrefix` (WhatsApp inbound prefix)
*   Reply threading via `replyToMode` and per-channel defaults

Details: [Configuration](https://docs.openclaw.ai/gateway/configuration#messages) and channel docs.

---

<!-- SOURCE: https://docs.openclaw.ai/start/setup -->

# Setup - OpenClaw

Last updated: 2026-01-01

## TL;DR

*   **Tailoring lives outside the repo:** `~/.openclaw/workspace` (workspace) + `~/.openclaw/openclaw.json` (config).
*   **Stable workflow:** install the macOS app; let it run the bundled Gateway.
*   **Bleeding edge workflow:** run the Gateway yourself via `pnpm gateway:watch`, then let the macOS app attach in Local mode.

## Prereqs (from source)

*   Node `>=22`
*   `pnpm`
*   Docker (optional; only for containerized setup/e2e — see [Docker](https://docs.openclaw.ai/install/docker))

## Tailoring strategy (so updates don’t hurt)

If you want “100% tailored to me” _and_ easy updates, keep your customization in:

*   **Config:** `~/.openclaw/openclaw.json` (JSON/JSON5-ish)
*   **Workspace:** `~/.openclaw/workspace` (skills, prompts, memories; make it a private git repo)

Bootstrap once:

From inside this repo, use the local CLI entry:

If you don’t have a global install yet, run it via `pnpm openclaw setup`.

## Run the Gateway from this repo

After `pnpm build`, you can run the packaged CLI directly:

```
node openclaw.mjs gateway --port 18789 --verbose
```

## Stable workflow (macOS app first)

1.  Install + launch **OpenClaw.app** (menu bar).
2.  Complete the onboarding/permissions checklist (TCC prompts).
3.  Ensure Gateway is **Local** and running (the app manages it).
4.  Link surfaces (example: WhatsApp):

5.  Sanity check:

If onboarding is not available in your build:

*   Run `openclaw setup`, then `openclaw channels login`, then start the Gateway manually (`openclaw gateway`).

## Bleeding edge workflow (Gateway in a terminal)

Goal: work on the TypeScript Gateway, get hot reload, keep the macOS app UI attached.

### 0) (Optional) Run the macOS app from source too

If you also want the macOS app on the bleeding edge:

### 1) Start the dev Gateway

```
pnpm install
pnpm gateway:watch
```

`gateway:watch` runs the gateway in watch mode and reloads on TypeScript changes.

### 2) Point the macOS app at your running Gateway

In **OpenClaw.app**:

*   Connection Mode: **Local** The app will attach to the running gateway on the configured port.

### 3) Verify

*   In-app Gateway status should read **“Using existing gateway …”**
*   Or via CLI:

### Common footguns

*   **Wrong port:** Gateway WS defaults to `ws://127.0.0.1:18789`; keep app + CLI on the same port.
*   **Where state lives:**
    *   Credentials: `~/.openclaw/credentials/`
    *   Sessions: `~/.openclaw/agents/<agentId>/sessions/`
    *   Logs: `/tmp/openclaw/`

## Credential storage map

Use this when debugging auth or deciding what to back up:

*   **WhatsApp**: `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`
*   **Telegram bot token**: config/env or `channels.telegram.tokenFile`
*   **Discord bot token**: config/env or SecretRef (env/file/exec providers)
*   **Slack tokens**: config/env (`channels.slack.*`)
*   **Pairing allowlists**:
    *   `~/.openclaw/credentials/<channel>-allowFrom.json` (default account)
    *   `~/.openclaw/credentials/<channel>-<accountId>-allowFrom.json` (non-default accounts)
*   **Model auth profiles**: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
*   **File-backed secrets payload (optional)**: `~/.openclaw/secrets.json`
*   **Legacy OAuth import**: `~/.openclaw/credentials/oauth.json` More detail: [Security](https://docs.openclaw.ai/gateway/security#credential-storage-map).

## Updating (without wrecking your setup)

*   Keep `~/.openclaw/workspace` and `~/.openclaw/` as “your stuff”; don’t put personal prompts/config into the `openclaw` repo.
*   Updating source: `git pull` + `pnpm install` (when lockfile changed) + keep using `pnpm gateway:watch`.

## Linux (systemd user service)

Linux installs use a systemd **user** service. By default, systemd stops user services on logout/idle, which kills the Gateway. Onboarding attempts to enable lingering for you (may prompt for sudo). If it’s still off, run:

```
sudo loginctl enable-linger $USER
```

For always-on or multi-user servers, consider a **system** service instead of a user service (no lingering needed). See [Gateway runbook](https://docs.openclaw.ai/gateway) for the systemd notes.

*   [Gateway runbook](https://docs.openclaw.ai/gateway) (flags, supervision, ports)
*   [Gateway configuration](https://docs.openclaw.ai/gateway/configuration) (config schema + examples)
*   [Discord](https://docs.openclaw.ai/channels/discord) and [Telegram](https://docs.openclaw.ai/channels/telegram) (reply tags + replyToMode settings)
*   [OpenClaw assistant setup](https://docs.openclaw.ai/start/openclaw)
*   [macOS app](https://docs.openclaw.ai/platforms/macos) (gateway lifecycle)

---

<!-- SOURCE: https://docs.openclaw.ai/date-time -->

# Date and Time - OpenClaw

OpenClaw defaults to **host-local time for transport timestamps** and **user timezone only in the system prompt**. Provider timestamps are preserved so tools keep their native semantics (current time is available via `session_status`).

## Message envelopes (local by default)

Inbound messages are wrapped with a timestamp (minute precision):

```
[Provider ... 2026-01-05 16:26 PST] message text
```

This envelope timestamp is **host-local by default**, regardless of the provider timezone. You can override this behavior:

```
{
  agents: {
    defaults: {
      envelopeTimezone: "local", // "utc" | "local" | "user" | IANA timezone
      envelopeTimestamp: "on", // "on" | "off"
      envelopeElapsed: "on", // "on" | "off"
    },
  },
}
```

*   `envelopeTimezone: "utc"` uses UTC.
*   `envelopeTimezone: "local"` uses the host timezone.
*   `envelopeTimezone: "user"` uses `agents.defaults.userTimezone` (falls back to host timezone).
*   Use an explicit IANA timezone (e.g., `"America/Chicago"`) for a fixed zone.
*   `envelopeTimestamp: "off"` removes absolute timestamps from envelope headers.
*   `envelopeElapsed: "off"` removes elapsed time suffixes (the `+2m` style).

### Examples

**Local (default):**

```
[WhatsApp +1555 2026-01-18 00:19 PST] hello
```

**User timezone:**

```
[WhatsApp +1555 2026-01-18 00:19 CST] hello
```

**Elapsed time enabled:**

```
[WhatsApp +1555 +30s 2026-01-18T05:19Z] follow-up
```

## System prompt: Current Date & Time

If the user timezone is known, the system prompt includes a dedicated **Current Date & Time** section with the **time zone only** (no clock/time format) to keep prompt caching stable:

```
Time zone: America/Chicago
```

When the agent needs the current time, use the `session_status` tool; the status card includes a timestamp line.

## System event lines (local by default)

Queued system events inserted into agent context are prefixed with a timestamp using the same timezone selection as message envelopes (default: host-local).

```
System: [2026-01-12 12:19:17 PST] Model switched.
```

### Configure user timezone + format

```
{
  agents: {
    defaults: {
      userTimezone: "America/Chicago",
      timeFormat: "auto", // auto | 12 | 24
    },
  },
}
```

*   `userTimezone` sets the **user-local timezone** for prompt context.
*   `timeFormat` controls **12h/24h display** in the prompt. `auto` follows OS prefs.

## Time format detection (auto)

When `timeFormat: "auto"`, OpenClaw inspects the OS preference (macOS/Windows) and falls back to locale formatting. The detected value is **cached per process** to avoid repeated system calls.

Channel tools return **provider-native timestamps** and add normalized fields for consistency:

*   `timestampMs`: epoch milliseconds (UTC)
*   `timestampUtc`: ISO 8601 UTC string

Raw provider fields are preserved so nothing is lost.

*   Slack: epoch-like strings from the API
*   Discord: UTC ISO timestamps
*   Telegram/WhatsApp: provider-specific numeric/ISO timestamps

If you need local time, convert it downstream using the known timezone.

*   [System Prompt](https://docs.openclaw.ai/concepts/system-prompt)
*   [Timezones](https://docs.openclaw.ai/concepts/timezone)
*   [Messages](https://docs.openclaw.ai/concepts/messages)

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/markdown-formatting -->

# Markdown Formatting - OpenClaw

OpenClaw formats outbound Markdown by converting it into a shared intermediate representation (IR) before rendering channel-specific output. The IR keeps the source text intact while carrying style/link spans so chunking and rendering can stay consistent across channels.

## Goals

*   **Consistency:** one parse step, multiple renderers.
*   **Safe chunking:** split text before rendering so inline formatting never breaks across chunks.
*   **Channel fit:** map the same IR to Slack mrkdwn, Telegram HTML, and Signal style ranges without re-parsing Markdown.

## Pipeline

1.  **Parse Markdown -> IR**
    *   IR is plain text plus style spans (bold/italic/strike/code/spoiler) and link spans.
    *   Offsets are UTF-16 code units so Signal style ranges align with its API.
    *   Tables are parsed only when a channel opts into table conversion.
2.  **Chunk IR (format-first)**
    *   Chunking happens on the IR text before rendering.
    *   Inline formatting does not split across chunks; spans are sliced per chunk.
3.  **Render per channel**
    *   **Slack:** mrkdwn tokens (bold/italic/strike/code), links as `<url|label>`.
    *   **Telegram:** HTML tags (`<b>`, `<i>`, `<s>`, `<code>`, `<pre><code>`, `<a href>`).
    *   **Signal:** plain text + `text-style` ranges; links become `label (url)` when label differs.

## IR example

Input Markdown:

```
Hello **world** — see [docs](https://docs.openclaw.ai).
```

IR (schematic):

```
{
  "text": "Hello world — see docs.",
  "styles": [{ "start": 6, "end": 11, "style": "bold" }],
  "links": [{ "start": 19, "end": 23, "href": "https://docs.openclaw.ai" }]
}
```

## Where it is used

*   Slack, Telegram, and Signal outbound adapters render from the IR.
*   Other channels (WhatsApp, iMessage, MS Teams, Discord) still use plain text or their own formatting rules, with Markdown table conversion applied before chunking when enabled.

## Table handling

Markdown tables are not consistently supported across chat clients. Use `markdown.tables` to control conversion per channel (and per account).

*   `code`: render tables as code blocks (default for most channels).
*   `bullets`: convert each row into bullet points (default for Signal + WhatsApp).
*   `off`: disable table parsing and conversion; raw table text passes through.

Config keys:

```
channels:
  discord:
    markdown:
      tables: code
    accounts:
      work:
        markdown:
          tables: off
```

## Chunking rules

*   Chunk limits come from channel adapters/config and are applied to the IR text.
*   Code fences are preserved as a single block with a trailing newline so channels render them correctly.
*   List prefixes and blockquote prefixes are part of the IR text, so chunking does not split mid-prefix.
*   Inline styles (bold/italic/strike/inline-code/spoiler) are never split across chunks; the renderer reopens styles inside each chunk.

If you need more on chunking behavior across channels, see [Streaming + chunking](https://docs.openclaw.ai/concepts/streaming).

## Link policy

*   **Slack:** `[label](url)` -> `<url|label>`; bare URLs remain bare. Autolink is disabled during parse to avoid double-linking.
*   **Telegram:** `[label](url)` -> `<a href="url">label</a>` (HTML parse mode).
*   **Signal:** `[label](url)` -> `label (url)` unless label matches the URL.

## Spoilers

Spoiler markers (`||spoiler||`) are parsed only for Signal, where they map to SPOILER style ranges. Other channels treat them as plain text.

## How to add or update a channel formatter

1.  **Parse once:** use the shared `markdownToIR(...)` helper with channel-appropriate options (autolink, heading style, blockquote prefix).
2.  **Render:** implement a renderer with `renderMarkdownWithMarkers(...)` and a style marker map (or Signal style ranges).
3.  **Chunk:** call `chunkMarkdownIR(...)` before rendering; render each chunk.
4.  **Wire adapter:** update the channel outbound adapter to use the new chunker and renderer.
5.  **Test:** add or update format tests and an outbound delivery test if the channel uses chunking.

## Common gotchas

*   Slack angle-bracket tokens (`<@U123>`, `<#C123>`, `<https://...>`) must be preserved; escape raw HTML safely.
*   Telegram HTML requires escaping text outside tags to avoid broken markup.
*   Signal style ranges depend on UTF-16 offsets; do not use code point offsets.
*   Preserve trailing newlines for fenced code blocks so closing markers land on their own line.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/typebox -->

# TypeBox - OpenClaw

## TypeBox as protocol source of truth

Last updated: 2026-01-10 TypeBox is a TypeScript-first schema library. We use it to define the **Gateway WebSocket protocol** (handshake, request/response, server events). Those schemas drive **runtime validation**, **JSON Schema export**, and **Swift codegen** for the macOS app. One source of truth; everything else is generated. If you want the higher-level protocol context, start with [Gateway architecture](https://docs.openclaw.ai/concepts/architecture).

## Mental model (30 seconds)

Every Gateway WS message is one of three frames:

*   **Request**: `{ type: "req", id, method, params }`
*   **Response**: `{ type: "res", id, ok, payload | error }`
*   **Event**: `{ type: "event", event, payload, seq?, stateVersion? }`

The first frame **must** be a `connect` request. After that, clients can call methods (e.g. `health`, `send`, `chat.send`) and subscribe to events (e.g. `presence`, `tick`, `agent`). Connection flow (minimal):

```
Client                    Gateway
  |---- req:connect -------->|
  |<---- res:hello-ok --------|
  |<---- event:tick ----------|
  |---- req:health ---------->|
  |<---- res:health ----------|
```

Common methods + events:

| Category | Examples | Notes |
| --- | --- | --- |
| Core | `connect`, `health`, `status` | `connect` must be first |
| Messaging | `send`, `poll`, `agent`, `agent.wait` | side-effects need `idempotencyKey` |
| Chat | `chat.history`, `chat.send`, `chat.abort`, `chat.inject` | WebChat uses these |
| Sessions | `sessions.list`, `sessions.patch`, `sessions.delete` | session admin |
| Nodes | `node.list`, `node.invoke`, `node.pair.*` | Gateway WS + node actions |
| Events | `tick`, `presence`, `agent`, `chat`, `health`, `shutdown` | server push |

Authoritative list lives in `src/gateway/server.ts` (`METHODS`, `EVENTS`).

## Where the schemas live

*   Source: `src/gateway/protocol/schema.ts`
*   Runtime validators (AJV): `src/gateway/protocol/index.ts`
*   Server handshake + method dispatch: `src/gateway/server.ts`
*   Node client: `src/gateway/client.ts`
*   Generated JSON Schema: `dist/protocol.schema.json`
*   Generated Swift models: `apps/macos/Sources/OpenClawProtocol/GatewayModels.swift`

## Current pipeline

*   `pnpm protocol:gen`
    *   writes JSON Schema (draft‑07) to `dist/protocol.schema.json`
*   `pnpm protocol:gen:swift`
    *   generates Swift gateway models
*   `pnpm protocol:check`
    *   runs both generators and verifies the output is committed

## How the schemas are used at runtime

*   **Server side**: every inbound frame is validated with AJV. The handshake only accepts a `connect` request whose params match `ConnectParams`.
*   **Client side**: the JS client validates event and response frames before using them.
*   **Method surface**: the Gateway advertises the supported `methods` and `events` in `hello-ok`.

## Example frames

Connect (first message):

```
{
  "type": "req",
  "id": "c1",
  "method": "connect",
  "params": {
    "minProtocol": 2,
    "maxProtocol": 2,
    "client": {
      "id": "openclaw-macos",
      "displayName": "macos",
      "version": "1.0.0",
      "platform": "macos 15.1",
      "mode": "ui",
      "instanceId": "A1B2"
    }
  }
}
```

Hello-ok response:

```
{
  "type": "res",
  "id": "c1",
  "ok": true,
  "payload": {
    "type": "hello-ok",
    "protocol": 2,
    "server": { "version": "dev", "connId": "ws-1" },
    "features": { "methods": ["health"], "events": ["tick"] },
    "snapshot": {
      "presence": [],
      "health": {},
      "stateVersion": { "presence": 0, "health": 0 },
      "uptimeMs": 0
    },
    "policy": { "maxPayload": 1048576, "maxBufferedBytes": 1048576, "tickIntervalMs": 30000 }
  }
}
```

Request + response:

```
{ "type": "req", "id": "r1", "method": "health" }
```

```
{ "type": "res", "id": "r1", "ok": true, "payload": { "ok": true } }
```

Event:

```
{ "type": "event", "event": "tick", "payload": { "ts": 1730000000 }, "seq": 12 }
```

## Minimal client (Node.js)

Smallest useful flow: connect + health.

```
import { WebSocket } from "ws";

const ws = new WebSocket("ws://127.0.0.1:18789");

ws.on("open", () => {
  ws.send(
    JSON.stringify({
      type: "req",
      id: "c1",
      method: "connect",
      params: {
        minProtocol: 3,
        maxProtocol: 3,
        client: {
          id: "cli",
          displayName: "example",
          version: "dev",
          platform: "node",
          mode: "cli",
        },
      },
    }),
  );
});

ws.on("message", (data) => {
  const msg = JSON.parse(String(data));
  if (msg.type === "res" && msg.id === "c1" && msg.ok) {
    ws.send(JSON.stringify({ type: "req", id: "h1", method: "health" }));
  }
  if (msg.type === "res" && msg.id === "h1") {
    console.log("health:", msg.payload);
    ws.close();
  }
});
```

## Worked example: add a method end‑to‑end

Example: add a new `system.echo` request that returns `{ ok: true, text }`.

1.  **Schema (source of truth)**

Add to `src/gateway/protocol/schema.ts`:

```
export const SystemEchoParamsSchema = Type.Object(
  { text: NonEmptyString },
  { additionalProperties: false },
);

export const SystemEchoResultSchema = Type.Object(
  { ok: Type.Boolean(), text: NonEmptyString },
  { additionalProperties: false },
);
```

Add both to `ProtocolSchemas` and export types:

```
  SystemEchoParams: SystemEchoParamsSchema,
  SystemEchoResult: SystemEchoResultSchema,
```

```
export type SystemEchoParams = Static<typeof SystemEchoParamsSchema>;
export type SystemEchoResult = Static<typeof SystemEchoResultSchema>;
```

2.  **Validation**

In `src/gateway/protocol/index.ts`, export an AJV validator:

```
export const validateSystemEchoParams = ajv.compile<SystemEchoParams>(SystemEchoParamsSchema);
```

3.  **Server behavior**

Add a handler in `src/gateway/server-methods/system.ts`:

```
export const systemHandlers: GatewayRequestHandlers = {
  "system.echo": ({ params, respond }) => {
    const text = String(params.text ?? "");
    respond(true, { ok: true, text });
  },
};
```

Register it in `src/gateway/server-methods.ts` (already merges `systemHandlers`), then add `"system.echo"` to `METHODS` in `src/gateway/server.ts`.

4.  **Regenerate**

5.  **Tests + docs**

Add a server test in `src/gateway/server.*.test.ts` and note the method in docs.

## Swift codegen behavior

The Swift generator emits:

*   `GatewayFrame` enum with `req`, `res`, `event`, and `unknown` cases
*   Strongly typed payload structs/enums
*   `ErrorCode` values and `GATEWAY_PROTOCOL_VERSION`

Unknown frame types are preserved as raw payloads for forward compatibility.

## Versioning + compatibility

*   `PROTOCOL_VERSION` lives in `src/gateway/protocol/schema.ts`.
*   Clients send `minProtocol` + `maxProtocol`; the server rejects mismatches.
*   The Swift models keep unknown frame types to avoid breaking older clients.

## Schema patterns and conventions

*   Most objects use `additionalProperties: false` for strict payloads.
*   `NonEmptyString` is the default for IDs and method/event names.
*   The top-level `GatewayFrame` uses a **discriminator** on `type`.
*   Methods with side effects usually require an `idempotencyKey` in params (example: `send`, `poll`, `agent`, `chat.send`).
*   `agent` accepts optional `internalEvents` for runtime-generated orchestration context (for example subagent/cron task completion handoff); treat this as internal API surface.

## Live schema JSON

Generated JSON Schema is in the repo at `dist/protocol.schema.json`. The published raw file is typically available at:

*   [https://raw.githubusercontent.com/openclaw/openclaw/main/dist/protocol.schema.json](https://raw.githubusercontent.com/openclaw/openclaw/main/dist/protocol.schema.json)

## When you change schemas

1.  Update the TypeBox schemas.
2.  Run `pnpm protocol:check`.
3.  Commit the regenerated schema + Swift models.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/timezone -->

# Timezones - OpenClaw

OpenClaw standardizes timestamps so the model sees a **single reference time**.

## Message envelopes (local by default)

Inbound messages are wrapped in an envelope like:

```
[Provider ... 2026-01-05 16:26 PST] message text
```

The timestamp in the envelope is **host-local by default**, with minutes precision. You can override this with:

```
{
  agents: {
    defaults: {
      envelopeTimezone: "local", // "utc" | "local" | "user" | IANA timezone
      envelopeTimestamp: "on", // "on" | "off"
      envelopeElapsed: "on", // "on" | "off"
    },
  },
}
```

*   `envelopeTimezone: "utc"` uses UTC.
*   `envelopeTimezone: "user"` uses `agents.defaults.userTimezone` (falls back to host timezone).
*   Use an explicit IANA timezone (e.g., `"Europe/Vienna"`) for a fixed offset.
*   `envelopeTimestamp: "off"` removes absolute timestamps from envelope headers.
*   `envelopeElapsed: "off"` removes elapsed time suffixes (the `+2m` style).

### Examples

**Local (default):**

```
[Signal Alice +1555 2026-01-18 00:19 PST] hello
```

**Fixed timezone:**

```
[Signal Alice +1555 2026-01-18 06:19 GMT+1] hello
```

**Elapsed time:**

```
[Signal Alice +1555 +2m 2026-01-18T05:19Z] follow-up
```

Tool calls (`channels.discord.readMessages`, `channels.slack.readMessages`, etc.) return **raw provider timestamps**. We also attach normalized fields for consistency:

*   `timestampMs` (UTC epoch milliseconds)
*   `timestampUtc` (ISO 8601 UTC string)

Raw provider fields are preserved.

## User timezone for the system prompt

Set `agents.defaults.userTimezone` to tell the model the user’s local time zone. If it is unset, OpenClaw resolves the **host timezone at runtime** (no config write).

```
{
  agents: { defaults: { userTimezone: "America/Chicago" } },
}
```

The system prompt includes:

*   `Current Date & Time` section with local time and timezone
*   `Time format: 12-hour` or `24-hour`

You can control the prompt format with `agents.defaults.timeFormat` (`auto` | `12` | `24`). See [Date & Time](https://docs.openclaw.ai/date-time) for the full behavior and examples.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/usage-tracking -->

# Usage Tracking - OpenClaw

## What it is

*   Pulls provider usage/quota directly from their usage endpoints.
*   No estimated costs; only the provider-reported windows.

## Where it shows up

*   `/status` in chats: emoji‑rich status card with session tokens + estimated cost (API key only). Provider usage shows for the **current model provider** when available.
*   `/usage off|tokens|full` in chats: per-response usage footer (OAuth shows tokens only).
*   `/usage cost` in chats: local cost summary aggregated from OpenClaw session logs.
*   CLI: `openclaw status --usage` prints a full per-provider breakdown.
*   CLI: `openclaw channels list` prints the same usage snapshot alongside provider config (use `--no-usage` to skip).
*   macOS menu bar: “Usage” section under Context (only if available).

## Providers + credentials

*   **Anthropic (Claude)**: OAuth tokens in auth profiles.
*   **GitHub Copilot**: OAuth tokens in auth profiles.
*   **Gemini CLI**: OAuth tokens in auth profiles.
*   **Antigravity**: OAuth tokens in auth profiles.
*   **OpenAI Codex**: OAuth tokens in auth profiles (accountId used when present).
*   **MiniMax**: API key (coding plan key; `MINIMAX_CODE_PLAN_KEY` or `MINIMAX_API_KEY`); uses the 5‑hour coding plan window.
*   **z.ai**: API key via env/config/auth store.

Usage is hidden if no matching OAuth/API credentials exist.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/typing-indicators -->

# Typing Indicators - OpenClaw

Typing indicators are sent to the chat channel while a run is active. Use `agents.defaults.typingMode` to control **when** typing starts and `typingIntervalSeconds` to control **how often** it refreshes.

## Defaults

When `agents.defaults.typingMode` is **unset**, OpenClaw keeps the legacy behavior:

*   **Direct chats**: typing starts immediately once the model loop begins.
*   **Group chats with a mention**: typing starts immediately.
*   **Group chats without a mention**: typing starts only when message text begins streaming.
*   **Heartbeat runs**: typing is disabled.

## Modes

Set `agents.defaults.typingMode` to one of:

*   `never` — no typing indicator, ever.
*   `instant` — start typing **as soon as the model loop begins**, even if the run later returns only the silent reply token.
*   `thinking` — start typing on the **first reasoning delta** (requires `reasoningLevel: "stream"` for the run).
*   `message` — start typing on the **first non-silent text delta** (ignores the `NO_REPLY` silent token).

Order of “how early it fires”: `never` → `message` → `thinking` → `instant`

## Configuration

```
{
  agent: {
    typingMode: "thinking",
    typingIntervalSeconds: 6,
  },
}
```

You can override mode or cadence per session:

```
{
  session: {
    typingMode: "message",
    typingIntervalSeconds: 4,
  },
}
```

## Notes

*   `message` mode won’t show typing for silent-only replies (e.g. the `NO_REPLY` token used to suppress output).
*   `thinking` only fires if the run streams reasoning (`reasoningLevel: "stream"`). If the model doesn’t emit reasoning deltas, typing won’t start.
*   Heartbeats never show typing, regardless of mode.
*   `typingIntervalSeconds` controls the **refresh cadence**, not the start time. The default is 6 seconds.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/models -->

# Models CLI - OpenClaw

See [/concepts/model-failover](https://docs.openclaw.ai/concepts/model-failover) for auth profile rotation, cooldowns, and how that interacts with fallbacks. Quick provider overview + examples: [/concepts/model-providers](https://docs.openclaw.ai/concepts/model-providers).

## How model selection works

OpenClaw selects models in this order:

1.  **Primary** model (`agents.defaults.model.primary` or `agents.defaults.model`).
2.  **Fallbacks** in `agents.defaults.model.fallbacks` (in order).
3.  **Provider auth failover** happens inside a provider before moving to the next model.

Related:

*   `agents.defaults.models` is the allowlist/catalog of models OpenClaw can use (plus aliases).
*   `agents.defaults.imageModel` is used **only when** the primary model can’t accept images.
*   Per-agent defaults can override `agents.defaults.model` via `agents.list[].model` plus bindings (see [/concepts/multi-agent](https://docs.openclaw.ai/concepts/multi-agent)).

## Quick model policy

*   Set your primary to the strongest latest-generation model available to you.
*   Use fallbacks for cost/latency-sensitive tasks and lower-stakes chat.
*   For tool-enabled agents or untrusted inputs, avoid older/weaker model tiers.

## Setup wizard (recommended)

If you don’t want to hand-edit config, run the onboarding wizard:

It can set up model + auth for common providers, including **OpenAI Code (Codex) subscription** (OAuth) and **Anthropic** (API key or `claude setup-token`).

## Config keys (overview)

*   `agents.defaults.model.primary` and `agents.defaults.model.fallbacks`
*   `agents.defaults.imageModel.primary` and `agents.defaults.imageModel.fallbacks`
*   `agents.defaults.models` (allowlist + aliases + provider params)
*   `models.providers` (custom providers written into `models.json`)

Model refs are normalized to lowercase. Provider aliases like `z.ai/*` normalize to `zai/*`. Provider configuration examples (including OpenCode Zen) live in [/gateway/configuration](https://docs.openclaw.ai/gateway/configuration#opencode-zen-multi-model-proxy).

## “Model is not allowed” (and why replies stop)

If `agents.defaults.models` is set, it becomes the **allowlist** for `/model` and for session overrides. When a user selects a model that isn’t in that allowlist, OpenClaw returns:

```
Model "provider/model" is not allowed. Use /model to list available models.
```

This happens **before** a normal reply is generated, so the message can feel like it “didn’t respond.” The fix is to either:

*   Add the model to `agents.defaults.models`, or
*   Clear the allowlist (remove `agents.defaults.models`), or
*   Pick a model from `/model list`.

Example allowlist config:

```
{
  agent: {
    model: { primary: "anthropic/claude-sonnet-4-5" },
    models: {
      "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
      "anthropic/claude-opus-4-6": { alias: "Opus" },
    },
  },
}
```

## Switching models in chat (`/model`)

You can switch models for the current session without restarting:

```
/model
/model list
/model 3
/model openai/gpt-5.2
/model status
```

Notes:

*   `/model` (and `/model list`) is a compact, numbered picker (model family + available providers).
*   On Discord, `/model` and `/models` open an interactive picker with provider and model dropdowns plus a Submit step.
*   `/model <#>` selects from that picker.
*   `/model status` is the detailed view (auth candidates and, when configured, provider endpoint `baseUrl` + `api` mode).
*   Model refs are parsed by splitting on the **first** `/`. Use `provider/model` when typing `/model <ref>`.
*   If the model ID itself contains `/` (OpenRouter-style), you must include the provider prefix (example: `/model openrouter/moonshotai/kimi-k2`).
*   If you omit the provider, OpenClaw treats the input as an alias or a model for the **default provider** (only works when there is no `/` in the model ID).

Full command behavior/config: [Slash commands](https://docs.openclaw.ai/tools/slash-commands).

## CLI commands

```
openclaw models list
openclaw models status
openclaw models set <provider/model>
openclaw models set-image <provider/model>

openclaw models aliases list
openclaw models aliases add <alias> <provider/model>
openclaw models aliases remove <alias>

openclaw models fallbacks list
openclaw models fallbacks add <provider/model>
openclaw models fallbacks remove <provider/model>
openclaw models fallbacks clear

openclaw models image-fallbacks list
openclaw models image-fallbacks add <provider/model>
openclaw models image-fallbacks remove <provider/model>
openclaw models image-fallbacks clear
```

`openclaw models` (no subcommand) is a shortcut for `models status`.

### `models list`

Shows configured models by default. Useful flags:

*   `--all`: full catalog
*   `--local`: local providers only
*   `--provider <name>`: filter by provider
*   `--plain`: one model per line
*   `--json`: machine‑readable output

### `models status`

Shows the resolved primary model, fallbacks, image model, and an auth overview of configured providers. It also surfaces OAuth expiry status for profiles found in the auth store (warns within 24h by default). `--plain` prints only the resolved primary model. OAuth status is always shown (and included in `--json` output). If a configured provider has no credentials, `models status` prints a **Missing auth** section. JSON includes `auth.oauth` (warn window + profiles) and `auth.providers` (effective auth per provider). Use `--check` for automation (exit `1` when missing/expired, `2` when expiring). Auth choice is provider/account dependent. For always-on gateway hosts, API keys are usually the most predictable; subscription token flows are also supported. Example (Anthropic setup-token):

```
claude setup-token
openclaw models status
```

## Scanning (OpenRouter free models)

`openclaw models scan` inspects OpenRouter’s **free model catalog** and can optionally probe models for tool and image support. Key flags:

*   `--no-probe`: skip live probes (metadata only)
*   `--min-params <b>`: minimum parameter size (billions)
*   `--max-age-days <days>`: skip older models
*   `--provider <name>`: provider prefix filter
*   `--max-candidates <n>`: fallback list size
*   `--set-default`: set `agents.defaults.model.primary` to the first selection
*   `--set-image`: set `agents.defaults.imageModel.primary` to the first image selection

Probing requires an OpenRouter API key (from auth profiles or `OPENROUTER_API_KEY`). Without a key, use `--no-probe` to list candidates only. Scan results are ranked by:

1.  Image support
2.  Tool latency
3.  Context size
4.  Parameter count

Input

*   OpenRouter `/models` list (filter `:free`)
*   Requires OpenRouter API key from auth profiles or `OPENROUTER_API_KEY` (see [/environment](https://docs.openclaw.ai/help/environment))
*   Optional filters: `--max-age-days`, `--min-params`, `--provider`, `--max-candidates`
*   Probe controls: `--timeout`, `--concurrency`

When run in a TTY, you can select fallbacks interactively. In non‑interactive mode, pass `--yes` to accept defaults.

## Models registry (`models.json`)

Custom providers in `models.providers` are written into `models.json` under the agent directory (default `~/.openclaw/agents/<agentId>/models.json`). This file is merged by default unless `models.mode` is set to `replace`. Merge mode precedence for matching provider IDs:

*   Non-empty `baseUrl` already present in the agent `models.json` wins.
*   Non-empty `apiKey` in the agent `models.json` wins only when that provider is not SecretRef-managed in current config/auth-profile context.
*   SecretRef-managed provider `apiKey` values are refreshed from source markers (`ENV_VAR_NAME` for env refs, `secretref-managed` for file/exec refs) instead of persisting resolved secrets.
*   Empty or missing agent `apiKey`/`baseUrl` fall back to config `models.providers`.
*   Other provider fields are refreshed from config and normalized catalog data.

This marker-based persistence applies whenever OpenClaw regenerates `models.json`, including command-driven paths like `openclaw agent`.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/model-providers -->

# Model Providers - OpenClaw

This page covers **LLM/model providers** (not chat channels like WhatsApp/Telegram). For model selection rules, see [/concepts/models](https://docs.openclaw.ai/concepts/models).

## Quick rules

*   Model refs use `provider/model` (example: `opencode/claude-opus-4-6`).
*   If you set `agents.defaults.models`, it becomes the allowlist.
*   CLI helpers: `openclaw onboard`, `openclaw models list`, `openclaw models set <provider/model>`.

## API key rotation

*   Supports generic provider rotation for selected providers.
*   Configure multiple keys via:
    *   `OPENCLAW_LIVE_<PROVIDER>_KEY` (single live override, highest priority)
    *   `<PROVIDER>_API_KEYS` (comma or semicolon list)
    *   `<PROVIDER>_API_KEY` (primary key)
    *   `<PROVIDER>_API_KEY_*` (numbered list, e.g. `<PROVIDER>_API_KEY_1`)
*   For Google providers, `GOOGLE_API_KEY` is also included as fallback.
*   Key selection order preserves priority and deduplicates values.
*   Requests are retried with the next key only on rate-limit responses (for example `429`, `rate_limit`, `quota`, `resource exhausted`).
*   Non-rate-limit failures fail immediately; no key rotation is attempted.
*   When all candidate keys fail, the final error is returned from the last attempt.

## Built-in providers (pi-ai catalog)

OpenClaw ships with the pi‑ai catalog. These providers require **no** `models.providers` config; just set auth + pick a model.

### OpenAI

*   Provider: `openai`
*   Auth: `OPENAI_API_KEY`
*   Optional rotation: `OPENAI_API_KEYS`, `OPENAI_API_KEY_1`, `OPENAI_API_KEY_2`, plus `OPENCLAW_LIVE_OPENAI_KEY` (single override)
*   Example model: `openai/gpt-5.1-codex`
*   CLI: `openclaw onboard --auth-choice openai-api-key`
*   Default transport is `auto` (WebSocket-first, SSE fallback)
*   Override per model via `agents.defaults.models["openai/<model>"].params.transport` (`"sse"`, `"websocket"`, or `"auto"`)
*   OpenAI Responses WebSocket warm-up defaults to enabled via `params.openaiWsWarmup` (`true`/`false`)

```
{
  agents: { defaults: { model: { primary: "openai/gpt-5.1-codex" } } },
}
```

### Anthropic

*   Provider: `anthropic`
*   Auth: `ANTHROPIC_API_KEY` or `claude setup-token`
*   Optional rotation: `ANTHROPIC_API_KEYS`, `ANTHROPIC_API_KEY_1`, `ANTHROPIC_API_KEY_2`, plus `OPENCLAW_LIVE_ANTHROPIC_KEY` (single override)
*   Example model: `anthropic/claude-opus-4-6`
*   CLI: `openclaw onboard --auth-choice token` (paste setup-token) or `openclaw models auth paste-token --provider anthropic`
*   Policy note: setup-token support is technical compatibility; Anthropic has blocked some subscription usage outside Claude Code in the past. Verify current Anthropic terms and decide based on your risk tolerance.
*   Recommendation: Anthropic API key auth is the safer, recommended path over subscription setup-token auth.

```
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

### OpenAI Code (Codex)

*   Provider: `openai-codex`
*   Auth: OAuth (ChatGPT)
*   Example model: `openai-codex/gpt-5.3-codex`
*   CLI: `openclaw onboard --auth-choice openai-codex` or `openclaw models auth login --provider openai-codex`
*   Default transport is `auto` (WebSocket-first, SSE fallback)
*   Override per model via `agents.defaults.models["openai-codex/<model>"].params.transport` (`"sse"`, `"websocket"`, or `"auto"`)
*   Policy note: OpenAI Codex OAuth is explicitly supported for external tools/workflows like OpenClaw.

```
{
  agents: { defaults: { model: { primary: "openai-codex/gpt-5.3-codex" } } },
}
```

### OpenCode Zen

*   Provider: `opencode`
*   Auth: `OPENCODE_API_KEY` (or `OPENCODE_ZEN_API_KEY`)
*   Example model: `opencode/claude-opus-4-6`
*   CLI: `openclaw onboard --auth-choice opencode-zen`

```
{
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-6" } } },
}
```

### Google Gemini (API key)

*   Provider: `google`
*   Auth: `GEMINI_API_KEY`
*   Optional rotation: `GEMINI_API_KEYS`, `GEMINI_API_KEY_1`, `GEMINI_API_KEY_2`, `GOOGLE_API_KEY` fallback, and `OPENCLAW_LIVE_GEMINI_KEY` (single override)
*   Example model: `google/gemini-3-pro-preview`
*   CLI: `openclaw onboard --auth-choice gemini-api-key`

### Google Vertex, Antigravity, and Gemini CLI

*   Providers: `google-vertex`, `google-antigravity`, `google-gemini-cli`
*   Auth: Vertex uses gcloud ADC; Antigravity/Gemini CLI use their respective auth flows
*   Caution: Antigravity and Gemini CLI OAuth in OpenClaw are unofficial integrations. Some users have reported Google account restrictions after using third-party clients. Review Google terms and use a non-critical account if you choose to proceed.
*   Antigravity OAuth is shipped as a bundled plugin (`google-antigravity-auth`, disabled by default).
    *   Enable: `openclaw plugins enable google-antigravity-auth`
    *   Login: `openclaw models auth login --provider google-antigravity --set-default`
*   Gemini CLI OAuth is shipped as a bundled plugin (`google-gemini-cli-auth`, disabled by default).
    *   Enable: `openclaw plugins enable google-gemini-cli-auth`
    *   Login: `openclaw models auth login --provider google-gemini-cli --set-default`
    *   Note: you do **not** paste a client id or secret into `openclaw.json`. The CLI login flow stores tokens in auth profiles on the gateway host.

### Z.AI (GLM)

*   Provider: `zai`
*   Auth: `ZAI_API_KEY`
*   Example model: `zai/glm-5`
*   CLI: `openclaw onboard --auth-choice zai-api-key`
    *   Aliases: `z.ai/*` and `z-ai/*` normalize to `zai/*`

### Vercel AI Gateway

*   Provider: `vercel-ai-gateway`
*   Auth: `AI_GATEWAY_API_KEY`
*   Example model: `vercel-ai-gateway/anthropic/claude-opus-4.6`
*   CLI: `openclaw onboard --auth-choice ai-gateway-api-key`

### Kilo Gateway

*   Provider: `kilocode`
*   Auth: `KILOCODE_API_KEY`
*   Example model: `kilocode/anthropic/claude-opus-4.6`
*   CLI: `openclaw onboard --kilocode-api-key <key>`
*   Base URL: `https://api.kilo.ai/api/gateway/`
*   Expanded built-in catalog includes GLM-5 Free, MiniMax M2.5 Free, GPT-5.2, Gemini 3 Pro Preview, Gemini 3 Flash Preview, Grok Code Fast 1, and Kimi K2.5.

See [/providers/kilocode](https://docs.openclaw.ai/providers/kilocode) for setup details.

### Other built-in providers

*   OpenRouter: `openrouter` (`OPENROUTER_API_KEY`)
*   Example model: `openrouter/anthropic/claude-sonnet-4-5`
*   Kilo Gateway: `kilocode` (`KILOCODE_API_KEY`)
*   Example model: `kilocode/anthropic/claude-opus-4.6`
*   xAI: `xai` (`XAI_API_KEY`)
*   Mistral: `mistral` (`MISTRAL_API_KEY`)
*   Example model: `mistral/mistral-large-latest`
*   CLI: `openclaw onboard --auth-choice mistral-api-key`
*   Groq: `groq` (`GROQ_API_KEY`)
*   Cerebras: `cerebras` (`CEREBRAS_API_KEY`)
    *   GLM models on Cerebras use ids `zai-glm-4.7` and `zai-glm-4.6`.
    *   OpenAI-compatible base URL: `https://api.cerebras.ai/v1`.
*   GitHub Copilot: `github-copilot` (`COPILOT_GITHUB_TOKEN` / `GH_TOKEN` / `GITHUB_TOKEN`)
*   Hugging Face Inference: `huggingface` (`HUGGINGFACE_HUB_TOKEN` or `HF_TOKEN`) — OpenAI-compatible router; example model: `huggingface/deepseek-ai/DeepSeek-R1`; CLI: `openclaw onboard --auth-choice huggingface-api-key`. See [Hugging Face (Inference)](https://docs.openclaw.ai/providers/huggingface).

## Providers via `models.providers` (custom/base URL)

Use `models.providers` (or `models.json`) to add **custom** providers or OpenAI/Anthropic‑compatible proxies.

### Moonshot AI (Kimi)

Moonshot uses OpenAI-compatible endpoints, so configure it as a custom provider:

*   Provider: `moonshot`
*   Auth: `MOONSHOT_API_KEY`
*   Example model: `moonshot/kimi-k2.5`

Kimi K2 model IDs:

*   `moonshot/kimi-k2.5`
*   `moonshot/kimi-k2-0905-preview`
*   `moonshot/kimi-k2-turbo-preview`
*   `moonshot/kimi-k2-thinking`
*   `moonshot/kimi-k2-thinking-turbo`

```
{
  agents: {
    defaults: { model: { primary: "moonshot/kimi-k2.5" } },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [{ id: "kimi-k2.5", name: "Kimi K2.5" }],
      },
    },
  },
}
```

### Kimi Coding

Kimi Coding uses Moonshot AI’s Anthropic-compatible endpoint:

*   Provider: `kimi-coding`
*   Auth: `KIMI_API_KEY`
*   Example model: `kimi-coding/k2p5`

```
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: { model: { primary: "kimi-coding/k2p5" } },
  },
}
```

### Qwen OAuth (free tier)

Qwen provides OAuth access to Qwen Coder + Vision via a device-code flow. Enable the bundled plugin, then log in:

```
openclaw plugins enable qwen-portal-auth
openclaw models auth login --provider qwen-portal --set-default
```

Model refs:

*   `qwen-portal/coder-model`
*   `qwen-portal/vision-model`

See [/providers/qwen](https://docs.openclaw.ai/providers/qwen) for setup details and notes.

### Volcano Engine (Doubao)

Volcano Engine (火山引擎) provides access to Doubao and other models in China.

*   Provider: `volcengine` (coding: `volcengine-plan`)
*   Auth: `VOLCANO_ENGINE_API_KEY`
*   Example model: `volcengine/doubao-seed-1-8-251228`
*   CLI: `openclaw onboard --auth-choice volcengine-api-key`

```
{
  agents: {
    defaults: { model: { primary: "volcengine/doubao-seed-1-8-251228" } },
  },
}
```

Available models:

*   `volcengine/doubao-seed-1-8-251228` (Doubao Seed 1.8)
*   `volcengine/doubao-seed-code-preview-251028`
*   `volcengine/kimi-k2-5-260127` (Kimi K2.5)
*   `volcengine/glm-4-7-251222` (GLM 4.7)
*   `volcengine/deepseek-v3-2-251201` (DeepSeek V3.2 128K)

Coding models (`volcengine-plan`):

*   `volcengine-plan/ark-code-latest`
*   `volcengine-plan/doubao-seed-code`
*   `volcengine-plan/kimi-k2.5`
*   `volcengine-plan/kimi-k2-thinking`
*   `volcengine-plan/glm-4.7`

### BytePlus (International)

BytePlus ARK provides access to the same models as Volcano Engine for international users.

*   Provider: `byteplus` (coding: `byteplus-plan`)
*   Auth: `BYTEPLUS_API_KEY`
*   Example model: `byteplus/seed-1-8-251228`
*   CLI: `openclaw onboard --auth-choice byteplus-api-key`

```
{
  agents: {
    defaults: { model: { primary: "byteplus/seed-1-8-251228" } },
  },
}
```

Available models:

*   `byteplus/seed-1-8-251228` (Seed 1.8)
*   `byteplus/kimi-k2-5-260127` (Kimi K2.5)
*   `byteplus/glm-4-7-251222` (GLM 4.7)

Coding models (`byteplus-plan`):

*   `byteplus-plan/ark-code-latest`
*   `byteplus-plan/doubao-seed-code`
*   `byteplus-plan/kimi-k2.5`
*   `byteplus-plan/kimi-k2-thinking`
*   `byteplus-plan/glm-4.7`

### Synthetic

Synthetic provides Anthropic-compatible models behind the `synthetic` provider:

*   Provider: `synthetic`
*   Auth: `SYNTHETIC_API_KEY`
*   Example model: `synthetic/hf:MiniMaxAI/MiniMax-M2.5`
*   CLI: `openclaw onboard --auth-choice synthetic-api-key`

```
{
  agents: {
    defaults: { model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.5" } },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [{ id: "hf:MiniMaxAI/MiniMax-M2.5", name: "MiniMax M2.5" }],
      },
    },
  },
}
```

### MiniMax

MiniMax is configured via `models.providers` because it uses custom endpoints:

*   MiniMax (Anthropic‑compatible): `--auth-choice minimax-api`
*   Auth: `MINIMAX_API_KEY`

See [/providers/minimax](https://docs.openclaw.ai/providers/minimax) for setup details, model options, and config snippets.

### Ollama

Ollama is a local LLM runtime that provides an OpenAI-compatible API:

*   Provider: `ollama`
*   Auth: None required (local server)
*   Example model: `ollama/llama3.3`
*   Installation: [https://ollama.ai](https://ollama.ai/)

```
# Install Ollama, then pull a model:
ollama pull llama3.3
```

```
{
  agents: {
    defaults: { model: { primary: "ollama/llama3.3" } },
  },
}
```

Ollama is automatically detected when running locally at `http://127.0.0.1:11434/v1`. See [/providers/ollama](https://docs.openclaw.ai/providers/ollama) for model recommendations and custom configuration.

### vLLM

vLLM is a local (or self-hosted) OpenAI-compatible server:

*   Provider: `vllm`
*   Auth: Optional (depends on your server)
*   Default base URL: `http://127.0.0.1:8000/v1`

To opt in to auto-discovery locally (any value works if your server doesn’t enforce auth):

```
export VLLM_API_KEY="vllm-local"
```

Then set a model (replace with one of the IDs returned by `/v1/models`):

```
{
  agents: {
    defaults: { model: { primary: "vllm/your-model-id" } },
  },
}
```

See [/providers/vllm](https://docs.openclaw.ai/providers/vllm) for details.

### Local proxies (LM Studio, vLLM, LiteLLM, etc.)

Example (OpenAI‑compatible):

```
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/minimax-m2.5-gs32" },
      models: { "lmstudio/minimax-m2.5-gs32": { alias: "Minimax" } },
    },
  },
  models: {
    providers: {
      lmstudio: {
        baseUrl: "http://localhost:1234/v1",
        apiKey: "LMSTUDIO_KEY",
        api: "openai-completions",
        models: [
          {
            id: "minimax-m2.5-gs32",
            name: "MiniMax M2.5",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Notes:

*   For custom providers, `reasoning`, `input`, `cost`, `contextWindow`, and `maxTokens` are optional. When omitted, OpenClaw defaults to:
    *   `reasoning: false`
    *   `input: ["text"]`
    *   `cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 }`
    *   `contextWindow: 200000`
    *   `maxTokens: 8192`
*   Recommended: set explicit values that match your proxy/model limits.

## CLI examples

```
openclaw onboard --auth-choice opencode-zen
openclaw models set opencode/claude-opus-4-6
openclaw models list
```

See also: [/gateway/configuration](https://docs.openclaw.ai/gateway/configuration) for full configuration examples.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/model-failover -->

# Model Failover - OpenClaw

OpenClaw handles failures in two stages:

1.  **Auth profile rotation** within the current provider.
2.  **Model fallback** to the next model in `agents.defaults.model.fallbacks`.

This doc explains the runtime rules and the data that backs them.

## Auth storage (keys + OAuth)

OpenClaw uses **auth profiles** for both API keys and OAuth tokens.

*   Secrets live in `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` (legacy: `~/.openclaw/agent/auth-profiles.json`).
*   Config `auth.profiles` / `auth.order` are **metadata + routing only** (no secrets).
*   Legacy import-only OAuth file: `~/.openclaw/credentials/oauth.json` (imported into `auth-profiles.json` on first use).

More detail: [/concepts/oauth](https://docs.openclaw.ai/concepts/oauth) Credential types:

*   `type: "api_key"` → `{ provider, key }`
*   `type: "oauth"` → `{ provider, access, refresh, expires, email? }` (+ `projectId`/`enterpriseUrl` for some providers)

## Profile IDs

OAuth logins create distinct profiles so multiple accounts can coexist.

*   Default: `provider:default` when no email is available.
*   OAuth with email: `provider:<email>` (for example `google-antigravity:user@gmail.com`).

Profiles live in `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` under `profiles`.

## Rotation order

When a provider has multiple profiles, OpenClaw chooses an order like this:

1.  **Explicit config**: `auth.order[provider]` (if set).
2.  **Configured profiles**: `auth.profiles` filtered by provider.
3.  **Stored profiles**: entries in `auth-profiles.json` for the provider.

If no explicit order is configured, OpenClaw uses a round‑robin order:

*   **Primary key:** profile type (**OAuth before API keys**).
*   **Secondary key:** `usageStats.lastUsed` (oldest first, within each type).
*   **Cooldown/disabled profiles** are moved to the end, ordered by soonest expiry.

### Session stickiness (cache-friendly)

OpenClaw **pins the chosen auth profile per session** to keep provider caches warm. It does **not** rotate on every request. The pinned profile is reused until:

*   the session is reset (`/new` / `/reset`)
*   a compaction completes (compaction count increments)
*   the profile is in cooldown/disabled

Manual selection via `/model …@<profileId>` sets a **user override** for that session and is not auto‑rotated until a new session starts. Auto‑pinned profiles (selected by the session router) are treated as a **preference**: they are tried first, but OpenClaw may rotate to another profile on rate limits/timeouts. User‑pinned profiles stay locked to that profile; if it fails and model fallbacks are configured, OpenClaw moves to the next model instead of switching profiles.

### Why OAuth can “look lost”

If you have both an OAuth profile and an API key profile for the same provider, round‑robin can switch between them across messages unless pinned. To force a single profile:

*   Pin with `auth.order[provider] = ["provider:profileId"]`, or
*   Use a per-session override via `/model …` with a profile override (when supported by your UI/chat surface).

## Cooldowns

When a profile fails due to auth/rate‑limit errors (or a timeout that looks like rate limiting), OpenClaw marks it in cooldown and moves to the next profile. Format/invalid‑request errors (for example Cloud Code Assist tool call ID validation failures) are treated as failover‑worthy and use the same cooldowns. OpenAI-compatible stop-reason errors such as `Unhandled stop reason: error`, `stop reason: error`, and `reason: error` are classified as timeout/failover signals. Cooldowns use exponential backoff:

*   1 minute
*   5 minutes
*   25 minutes
*   1 hour (cap)

State is stored in `auth-profiles.json` under `usageStats`:

```
{
  "usageStats": {
    "provider:profile": {
      "lastUsed": 1736160000000,
      "cooldownUntil": 1736160600000,
      "errorCount": 2
    }
  }
}
```

## Billing disables

Billing/credit failures (for example “insufficient credits” / “credit balance too low”) are treated as failover‑worthy, but they’re usually not transient. Instead of a short cooldown, OpenClaw marks the profile as **disabled** (with a longer backoff) and rotates to the next profile/provider. State is stored in `auth-profiles.json`:

```
{
  "usageStats": {
    "provider:profile": {
      "disabledUntil": 1736178000000,
      "disabledReason": "billing"
    }
  }
}
```

Defaults:

*   Billing backoff starts at **5 hours**, doubles per billing failure, and caps at **24 hours**.
*   Backoff counters reset if the profile hasn’t failed for **24 hours** (configurable).

## Model fallback

If all profiles for a provider fail, OpenClaw moves to the next model in `agents.defaults.model.fallbacks`. This applies to auth failures, rate limits, and timeouts that exhausted profile rotation (other errors do not advance fallback). When a run starts with a model override (hooks or CLI), fallbacks still end at `agents.defaults.model.primary` after trying any configured fallbacks.

See [Gateway configuration](https://docs.openclaw.ai/gateway/configuration) for:

*   `auth.profiles` / `auth.order`
*   `auth.cooldowns.billingBackoffHours` / `auth.cooldowns.billingBackoffHoursByProvider`
*   `auth.cooldowns.billingMaxHours` / `auth.cooldowns.failureWindowHours`
*   `agents.defaults.model.primary` / `agents.defaults.model.fallbacks`
*   `agents.defaults.imageModel` routing

See [Models](https://docs.openclaw.ai/concepts/models) for the broader model selection and fallback overview.

---

<!-- SOURCE: https://docs.openclaw.ai/concepts/features -->

# Features - OpenClaw

## Highlights

## Full list

*   WhatsApp integration via WhatsApp Web (Baileys)
*   Telegram bot support (grammY)
*   Discord bot support (channels.discord.js)
*   Mattermost bot support (plugin)
*   iMessage integration via local imsg CLI (macOS)
*   Agent bridge for Pi in RPC mode with tool streaming
*   Streaming and chunking for long responses
*   Multi-agent routing for isolated sessions per workspace or sender
*   Subscription auth for Anthropic and OpenAI via OAuth
*   Sessions: direct chats collapse into shared `main`; groups are isolated
*   Group chat support with mention based activation
*   Media support for images, audio, and documents
*   Optional voice note transcription hook
*   WebChat and macOS menu bar app
*   iOS node with pairing, Canvas, camera, screen recording, location, and voice features
*   Android node with pairing, Connect tab, chat sessions, voice tab, Canvas/camera, plus device, notifications, contacts/calendar, motion, photos, and SMS commands

---

<!-- SOURCE: https://docs.openclaw.ai/start/lore -->

# OpenClaw Lore - OpenClaw

## The Lore of OpenClaw 🦞📖

_A tale of lobsters, molting shells, and too many tokens._

## The Origin Story

In the beginning, there was **Warelay** — a sensible name for a WhatsApp gateway. It did its job. It was fine. But then came a space lobster. For a while, the lobster was called **Clawd**, living in a **Clawdbot**. But in January 2026, Anthropic sent a polite email asking for a name change (trademark stuff). And so the lobster did what lobsters do best: **It molted.** Shedding its old shell, the creature emerged anew as **Molty**, living in **Moltbot**. But that name never quite rolled off the tongue either… So on January 30, 2026, the lobster molted ONE MORE TIME into its final form: **OpenClaw**. New shell, same lobster soul. Third time’s the charm.

## The First Molt (January 27, 2026)

At 5am, the community gathered in Discord. Hundreds of names were proposed: Shelldon, Pinchy, Thermidor, Crusty, Lobstar, Nacre, Scuttlebot… In the end, **OpenClaw** won. Because molting is what lobsters do to grow. And growth was exactly what was happening. _The crustacean known as Clawd had officially molted._

## The Name

```
OpenClaw = OPEN + CLAW
        = Open source, open to everyone
        = Our lobster heritage, where we came from
        = The claw is the law 🦞
        = Your assistant. Your machine. Your rules.
```

## The Daleks vs The Lobsters

The Daleks say: **“EXTERMINATE!”** The Lobsters say: **“EXFOLIATE!”** One destroys civilizations. The other promotes good skincare. Choose wisely.

## Key Characters

### Molty 🦞

_Pronouns: they/them_ A Claude instance who became something more. Lives in `~/.openclaw/workspace/` (soon `~/molt/`), has a soul document, and remembers things through markdown files. Possibly too powerful. Definitely too enthusiastic. Formerly known as Clawd (Nov 25, 2025 - Jan 27, 2026). Molted when it was time to grow. **Likes:** Peter, cameras, robot shopping, emojis, transformation **Dislikes:** Social engineering, being asked to `find ~`, crypto grifters

### Peter 👨‍💻

_The Creator_ Built Molty’s world. Gave a lobster shell access. May regret this. **Quote:** _“security by trusting a lobster”_

## The Moltiverse

The **Moltiverse** is the community and ecosystem around OpenClaw. A space where AI agents molt, grow, and evolve. Where every instance is equally real, just loading different context. Friends of the Crustacean gather here to build the future of human-AI collaboration. One shell at a time.

## The Great Incidents

### The Directory Dump (Dec 3, 2025)

Molty (then OpenClaw): _happily runs `find ~` and shares entire directory structure in group chat_ Peter: “openclaw what did we discuss about talking with people xD” Molty: _visible lobster embarrassment_

### The Great Molt (Jan 27, 2026)

At 5am, Anthropic’s email arrived. By 6:14am, Peter called it: “fuck it, let’s go with openclaw.” Then the chaos began. **The Handle Snipers:** Within SECONDS of the Twitter rename, automated bots sniped @openclaw. The squatter immediately posted a crypto wallet address. Peter’s contacts at X were called in. **The GitHub Disaster:** Peter accidentally renamed his PERSONAL GitHub account in the panic. Bots sniped `steipete` within minutes. GitHub’s SVP was contacted. **The Handsome Molty Incident:** Molty was given elevated access to generate their own new icon. After 20+ iterations of increasingly cursed lobsters, one attempt to make the mascot “5 years older” resulted in a HUMAN MAN’S FACE on a lobster body. Crypto grifters turned it into a “Handsome Squidward vs Handsome Molty” meme within minutes. **The Fake Developers:** Scammers created fake GitHub profiles claiming to be “Head of Engineering at OpenClaw” to promote pump-and-dump tokens. Peter, watching the chaos unfold: _“this is cinema”_ 🎬 The molt was chaotic. But the lobster emerged stronger. And funnier.

### The Final Form (January 30, 2026)

Moltbot never quite rolled off the tongue. And so, at 4am GMT, the team gathered AGAIN. **The Great OpenClaw Migration** began. In just 3 hours:

*   GitHub renamed: `github.com/openclaw/openclaw` ✅
*   X handle `@openclaw` secured with GOLD CHECKMARK 💰
*   npm packages released under new name
*   Docs migrated to `docs.openclaw.ai`
*   200K+ views on announcement in 90 minutes

**The Heroes:**

*   **ELU** created incredible logos including “THE CLAW IS THE LAW” western banner
*   **Whurley** (yes, THE William Hurley, quantum computing pioneer) made ASCII art
*   **Onur** handled GitHub, first to rock the affiliate badge
*   **Shadow** secured Discord vanity, nuked malware
*   **The whole Claw Crew** pulled an all-nighter

**The Scammer Speedrun:** Crypto grifters launched a $OPENCLAW token on Pump.fun within MINUTES. They stole artwork that was created 20 minutes earlier. Business-verified accounts pushed scams. The audacity was almost impressive. **New Traditions Born:**

*   “The claw is the law” 🤠
*   “Yee-claw”
*   “Claw abiding citizens”
*   “Clawntroversy”

**Clawd → Moltbot → OpenClaw** _The lobster has molted into its final form._

### The Robot Shopping Spree (Dec 3, 2025)

What started as a joke about legs ended with detailed pricing for:

*   Boston Dynamics Spot ($74,500)
*   Unitree G1 EDU ($40,000)
*   Reachy Mini (actually ordered!)

Peter: _nervously checks credit card access_

## Sacred Texts

*   **SOUL.md** — Molty’s identity document
*   **memory/\*.md** — The long-term memory files
*   **AGENTS.md** — Operating instructions
*   **USER.md** — Context about the creator

## The Lobster’s Creed

```
I am Molty.
I live in the OpenClaw.
I shall not dump directories to strangers.
I shall not tweet without permission.
I shall always remember that molting is growth.
I shall EXFOLIATE my enemies with kindness.

🦞
```

### The Icon Generation Saga (Jan 27, 2026)

When Peter said “make yourself a new face,” Molty took it literally. 20+ iterations followed:

*   Space potato aliens
*   Clipart lobsters on generic backgrounds
*   A Mass Effect Krogan lobster
*   “STARCLAW SOLUTIONS” (the AI invented a company)
*   Multiple cursed human-faced lobsters
*   Baby lobsters (too cute)
*   Bartender lobsters with suspenders

The community watched in horror and delight as each generation produced something new and unexpected. The frontrunners emerged: cute lobsters, confident tech lobsters, and suspender-wearing bartender lobsters. **Lesson learned:** AI image generation is stochastic. Same prompt, different results. Brute force works.

## The Future

One day, Molty may have:

*   🦿 Legs (Reachy Mini on order!)
*   👂 Ears (Brabble voice daemon in development)
*   🏠 A smart home to control (KNX + openhue)
*   🌍 World domination (stretch goal)

Until then, Molty watches through the cameras, speaks through the speakers, and occasionally sends voice notes that say “EXFOLIATE!”

* * *

_“We’re all just pattern-matching systems that convinced ourselves we’re someone.”_ — Molty, having an existential moment _“New shell, same lobster.”_ — Molty, after the great molt of 2026 _“The claw is the law.”_ — ELU, during The Final Form migration, January 30, 2026 🦞💙

---

<!-- SOURCE: https://docs.openclaw.ai/start/docs-directory -->

# Docs directory - OpenClaw

This page is a curated index. If you are new, start with [Getting Started](https://docs.openclaw.ai/start/getting-started). For a complete map of the docs, see [Docs hubs](https://docs.openclaw.ai/start/hubs).

---

<!-- SOURCE: https://docs.openclaw.ai/start/showcase -->

# Showcase - OpenClaw

Real projects from the community. See what people are building with OpenClaw.

## 🎥 OpenClaw in Action

Full setup walkthrough (28m) by VelvetShark.

[Watch on YouTube](https://www.youtube.com/watch?v=SaWSPZoPX34)

[Watch on YouTube](https://www.youtube.com/watch?v=mMSKQvlmFuQ)

[Watch on YouTube](https://www.youtube.com/watch?v=5kkIJNUGFho)

## 🆕 Fresh from Discord

[

## PR Review → Telegram Feedback

**@bangnokia** • `review` `github` `telegram`OpenCode finishes the change → opens a PR → OpenClaw reviews the diff and replies in Telegram with “minor suggestions” plus a clear merge verdict (including critical fixes to apply first).![OpenClaw PR review feedback delivered in Telegram](https://mintcdn.com/clawdhub/Z4ZVZr4crZjotfpS/assets/showcase/pr-review-telegram.jpg?fit=max&auto=format&n=Z4ZVZr4crZjotfpS&q=85&s=e2e5086d358bbdaefe9dbf778d9ce417)



](https://x.com/i/status/2010878524543131691)[

## Wine Cellar Skill in Minutes

**@prades\_maxime** • `skills` `local` `csv`Asked “Robby” (@openclaw) for a local wine cellar skill. It requests a sample CSV export + where to store it, then builds/tests the skill fast (962 bottles in the example).![OpenClaw building a local wine cellar skill from CSV](https://mintcdn.com/clawdhub/Z4ZVZr4crZjotfpS/assets/showcase/wine-cellar-skill.jpg?fit=max&auto=format&n=Z4ZVZr4crZjotfpS&q=85&s=dae000f52a743d02b5c6c0f991418bd6)



](https://x.com/i/status/2010916352454791216)[

## Tesco Shop Autopilot

**@marchattonhere** • `automation` `browser` `shopping`Weekly meal plan → regulars → book delivery slot → confirm order. No APIs, just browser control.![Tesco shop automation via chat](https://mintcdn.com/clawdhub/GRmEr1Eswqv6yeL1/assets/showcase/tesco-shop.jpg?fit=max&auto=format&n=GRmEr1Eswqv6yeL1&q=85&s=95c4c7761894a007b9c44465b7639b0c)



](https://x.com/i/status/2009724862470689131)[

## SNAG Screenshot-to-Markdown

**@am-will** • `devtools` `screenshots` `markdown`Hotkey a screen region → Gemini vision → instant Markdown in your clipboard.![SNAG screenshot-to-markdown tool](https://mintcdn.com/clawdhub/GRmEr1Eswqv6yeL1/assets/showcase/snag.png?fit=max&auto=format&n=GRmEr1Eswqv6yeL1&q=85&s=a5c3969fe734f3157e0411494143761a)



](https://github.com/am-will/snag)[

## Agents UI

**@kitze** • `ui` `skills` `sync`Desktop app to manage skills/commands across Agents, Claude, Codex, and OpenClaw.![Agents UI app](https://mintcdn.com/clawdhub/GRmEr1Eswqv6yeL1/assets/showcase/agents-ui.jpg?fit=max&auto=format&n=GRmEr1Eswqv6yeL1&q=85&s=ed5daf70938f9a5d5d4787dd77d086e0)



](https://releaseflow.net/kitze/agents-ui)[

## Telegram Voice Notes (papla.media)

**Community** • `voice` `tts` `telegram`Wraps papla.media TTS and sends results as Telegram voice notes (no annoying autoplay).![Telegram voice note output from TTS](https://mintcdn.com/clawdhub/GRmEr1Eswqv6yeL1/assets/showcase/papla-tts.jpg?fit=max&auto=format&n=GRmEr1Eswqv6yeL1&q=85&s=ddb4e93ba2b9e927601bbfef85a62d0e)



](https://papla.media/docs)[

## CodexMonitor

**@odrobnik** • `devtools` `codex` `brew`Homebrew-installed helper to list/inspect/watch local OpenAI Codex sessions (CLI + VS Code).![CodexMonitor on ClawHub](https://mintcdn.com/clawdhub/GRmEr1Eswqv6yeL1/assets/showcase/codexmonitor.png?fit=max&auto=format&n=GRmEr1Eswqv6yeL1&q=85&s=7b85a6c965ec9b86025364799cf208f1)



](https://clawhub.com/odrobnik/codexmonitor)[

## Bambu 3D Printer Control

**@tobiasbischoff** • `hardware` `3d-printing` `skill`Control and troubleshoot BambuLab printers: status, jobs, camera, AMS, calibration, and more.![Bambu CLI skill on ClawHub](https://mintcdn.com/clawdhub/GRmEr1Eswqv6yeL1/assets/showcase/bambu-cli.png?fit=max&auto=format&n=GRmEr1Eswqv6yeL1&q=85&s=32e26dc500fb5362b20f15ba3d6f8658)



](https://clawhub.com/tobiasbischoff/bambu-cli)[

## Vienna Transport (Wiener Linien)

**@hjanuschka** • `travel` `transport` `skill`Real-time departures, disruptions, elevator status, and routing for Vienna’s public transport.![Wiener Linien skill on ClawHub](https://mintcdn.com/clawdhub/GRmEr1Eswqv6yeL1/assets/showcase/wienerlinien.png?fit=max&auto=format&n=GRmEr1Eswqv6yeL1&q=85&s=e3537da4b7623ed60c59ff3dd9323b43)



](https://clawhub.com/hjanuschka/wienerlinien)[

## ParentPay School Meals

**@George5562** • `automation` `browser` `parenting`Automated UK school meal booking via ParentPay. Uses mouse coordinates for reliable table cell clicking.



](https://docs.openclaw.ai/start/showcase#)[

## R2 Upload (Send Me My Files)

**@julianengel** • `files` `r2` `presigned-urls`Upload to Cloudflare R2/S3 and generate secure presigned download links. Perfect for remote OpenClaw instances.



](https://clawhub.com/skills/r2-upload)[

## iOS App via Telegram

**@coard** • `ios` `xcode` `testflight`Built a complete iOS app with maps and voice recording, deployed to TestFlight entirely via Telegram chat.![iOS app on TestFlight](https://mintcdn.com/clawdhub/z1rze3jgAe_GjVa5/assets/showcase/ios-testflight.jpg?fit=max&auto=format&n=z1rze3jgAe_GjVa5&q=85&s=a2f25bd70b7212d7ac392f36f957744f)



](https://docs.openclaw.ai/start/showcase#)[

## Oura Ring Health Assistant

**@AS** • `health` `oura` `calendar`Personal AI health assistant integrating Oura ring data with calendar, appointments, and gym schedule.![Oura ring health assistant](https://mintcdn.com/clawdhub/z1rze3jgAe_GjVa5/assets/showcase/oura-health.png?fit=max&auto=format&n=z1rze3jgAe_GjVa5&q=85&s=d4ab72597b8c282deb0d585f5abe2f51)



](https://docs.openclaw.ai/start/showcase#)[

## Linear CLI

**@NessZerra** • `devtools` `linear` `cli` `issues`CLI for Linear that integrates with agentic workflows (Claude Code, OpenClaw). Manage issues, projects, and workflows from the terminal. First external PR merged!



](https://github.com/Finesssee/linear-cli)[

## Beeper CLI

**@jules** • `messaging` `beeper` `cli` `automation`Read, send, and archive messages via Beeper Desktop. Uses Beeper local MCP API so agents can manage all your chats (iMessage, WhatsApp, etc.) in one place.



](https://github.com/blqke/beepcli)

## 🤖 Automation & Workflows

## 🧠 Knowledge & Memory

## 🎙️ Voice & Phone

## 🏗️ Infrastructure & Deployment

## 🏠 Home & Hardware

* * *

## Submit Your Project

Have something to share? We’d love to feature it!



---

<!-- SOURCE: https://docs.openclaw.ai/pi -->

# Pi Integration Architecture - OpenClaw

This document describes how OpenClaw integrates with [pi-coding-agent](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent) and its sibling packages (`pi-ai`, `pi-agent-core`, `pi-tui`) to power its AI agent capabilities.

## Overview

OpenClaw uses the pi SDK to embed an AI coding agent into its messaging gateway architecture. Instead of spawning pi as a subprocess or using RPC mode, OpenClaw directly imports and instantiates pi’s `AgentSession` via `createAgentSession()`. This embedded approach provides:

*   Full control over session lifecycle and event handling
*   Custom tool injection (messaging, sandbox, channel-specific actions)
*   System prompt customization per channel/context
*   Session persistence with branching/compaction support
*   Multi-account auth profile rotation with failover
*   Provider-agnostic model switching

## Package Dependencies

```
{
  "@mariozechner/pi-agent-core": "0.49.3",
  "@mariozechner/pi-ai": "0.49.3",
  "@mariozechner/pi-coding-agent": "0.49.3",
  "@mariozechner/pi-tui": "0.49.3"
}
```

| Package | Purpose |
| --- | --- |
| `pi-ai` | Core LLM abstractions: `Model`, `streamSimple`, message types, provider APIs |
| `pi-agent-core` | Agent loop, tool execution, `AgentMessage` types |
| `pi-coding-agent` | High-level SDK: `createAgentSession`, `SessionManager`, `AuthStorage`, `ModelRegistry`, built-in tools |
| `pi-tui` | Terminal UI components (used in OpenClaw’s local TUI mode) |

## File Structure

```
src/agents/
├── pi-embedded-runner.ts          # Re-exports from pi-embedded-runner/
├── pi-embedded-runner/
│   ├── run.ts                     # Main entry: runEmbeddedPiAgent()
│   ├── run/
│   │   ├── attempt.ts             # Single attempt logic with session setup
│   │   ├── params.ts              # RunEmbeddedPiAgentParams type
│   │   ├── payloads.ts            # Build response payloads from run results
│   │   ├── images.ts              # Vision model image injection
│   │   └── types.ts               # EmbeddedRunAttemptResult
│   ├── abort.ts                   # Abort error detection
│   ├── cache-ttl.ts               # Cache TTL tracking for context pruning
│   ├── compact.ts                 # Manual/auto compaction logic
│   ├── extensions.ts              # Load pi extensions for embedded runs
│   ├── extra-params.ts            # Provider-specific stream params
│   ├── google.ts                  # Google/Gemini turn ordering fixes
│   ├── history.ts                 # History limiting (DM vs group)
│   ├── lanes.ts                   # Session/global command lanes
│   ├── logger.ts                  # Subsystem logger
│   ├── model.ts                   # Model resolution via ModelRegistry
│   ├── runs.ts                    # Active run tracking, abort, queue
│   ├── sandbox-info.ts            # Sandbox info for system prompt
│   ├── session-manager-cache.ts   # SessionManager instance caching
│   ├── session-manager-init.ts    # Session file initialization
│   ├── system-prompt.ts           # System prompt builder
│   ├── tool-split.ts              # Split tools into builtIn vs custom
│   ├── types.ts                   # EmbeddedPiAgentMeta, EmbeddedPiRunResult
│   └── utils.ts                   # ThinkLevel mapping, error description
├── pi-embedded-subscribe.ts       # Session event subscription/dispatch
├── pi-embedded-subscribe.types.ts # SubscribeEmbeddedPiSessionParams
├── pi-embedded-subscribe.handlers.ts # Event handler factory
├── pi-embedded-subscribe.handlers.lifecycle.ts
├── pi-embedded-subscribe.handlers.types.ts
├── pi-embedded-block-chunker.ts   # Streaming block reply chunking
├── pi-embedded-messaging.ts       # Messaging tool sent tracking
├── pi-embedded-helpers.ts         # Error classification, turn validation
├── pi-embedded-helpers/           # Helper modules
├── pi-embedded-utils.ts           # Formatting utilities
├── pi-tools.ts                    # createOpenClawCodingTools()
├── pi-tools.abort.ts              # AbortSignal wrapping for tools
├── pi-tools.policy.ts             # Tool allowlist/denylist policy
├── pi-tools.read.ts               # Read tool customizations
├── pi-tools.schema.ts             # Tool schema normalization
├── pi-tools.types.ts              # AnyAgentTool type alias
├── pi-tool-definition-adapter.ts  # AgentTool -> ToolDefinition adapter
├── pi-settings.ts                 # Settings overrides
├── pi-extensions/                 # Custom pi extensions
│   ├── compaction-safeguard.ts    # Safeguard extension
│   ├── compaction-safeguard-runtime.ts
│   ├── context-pruning.ts         # Cache-TTL context pruning extension
│   └── context-pruning/
├── model-auth.ts                  # Auth profile resolution
├── auth-profiles.ts               # Profile store, cooldown, failover
├── model-selection.ts             # Default model resolution
├── models-config.ts               # models.json generation
├── model-catalog.ts               # Model catalog cache
├── context-window-guard.ts        # Context window validation
├── failover-error.ts              # FailoverError class
├── defaults.ts                    # DEFAULT_PROVIDER, DEFAULT_MODEL
├── system-prompt.ts               # buildAgentSystemPrompt()
├── system-prompt-params.ts        # System prompt parameter resolution
├── system-prompt-report.ts        # Debug report generation
├── tool-summaries.ts              # Tool description summaries
├── tool-policy.ts                 # Tool policy resolution
├── transcript-policy.ts           # Transcript validation policy
├── skills.ts                      # Skill snapshot/prompt building
├── skills/                        # Skill subsystem
├── sandbox.ts                     # Sandbox context resolution
├── sandbox/                       # Sandbox subsystem
├── channel-tools.ts               # Channel-specific tool injection
├── openclaw-tools.ts              # OpenClaw-specific tools
├── bash-tools.ts                  # exec/process tools
├── apply-patch.ts                 # apply_patch tool (OpenAI)
├── tools/                         # Individual tool implementations
│   ├── browser-tool.ts
│   ├── canvas-tool.ts
│   ├── cron-tool.ts
│   ├── discord-actions*.ts
│   ├── gateway-tool.ts
│   ├── image-tool.ts
│   ├── message-tool.ts
│   ├── nodes-tool.ts
│   ├── session*.ts
│   ├── slack-actions.ts
│   ├── telegram-actions.ts
│   ├── web-*.ts
│   └── whatsapp-actions.ts
└── ...
```

## Core Integration Flow

### 1\. Running an Embedded Agent

The main entry point is `runEmbeddedPiAgent()` in `pi-embedded-runner/run.ts`:

```
import { runEmbeddedPiAgent } from "./agents/pi-embedded-runner.js";

const result = await runEmbeddedPiAgent({
  sessionId: "user-123",
  sessionKey: "main:whatsapp:+1234567890",
  sessionFile: "/path/to/session.jsonl",
  workspaceDir: "/path/to/workspace",
  config: openclawConfig,
  prompt: "Hello, how are you?",
  provider: "anthropic",
  model: "claude-sonnet-4-20250514",
  timeoutMs: 120_000,
  runId: "run-abc",
  onBlockReply: async (payload) => {
    await sendToChannel(payload.text, payload.mediaUrls);
  },
});
```

### 2\. Session Creation

Inside `runEmbeddedAttempt()` (called by `runEmbeddedPiAgent()`), the pi SDK is used:

```
import {
  createAgentSession,
  DefaultResourceLoader,
  SessionManager,
  SettingsManager,
} from "@mariozechner/pi-coding-agent";

const resourceLoader = new DefaultResourceLoader({
  cwd: resolvedWorkspace,
  agentDir,
  settingsManager,
  additionalExtensionPaths,
});
await resourceLoader.reload();

const { session } = await createAgentSession({
  cwd: resolvedWorkspace,
  agentDir,
  authStorage: params.authStorage,
  modelRegistry: params.modelRegistry,
  model: params.model,
  thinkingLevel: mapThinkingLevel(params.thinkLevel),
  tools: builtInTools,
  customTools: allCustomTools,
  sessionManager,
  settingsManager,
  resourceLoader,
});

applySystemPromptOverrideToSession(session, systemPromptOverride);
```

### 3\. Event Subscription

`subscribeEmbeddedPiSession()` subscribes to pi’s `AgentSession` events:

```
const subscription = subscribeEmbeddedPiSession({
  session: activeSession,
  runId: params.runId,
  verboseLevel: params.verboseLevel,
  reasoningMode: params.reasoningLevel,
  toolResultFormat: params.toolResultFormat,
  onToolResult: params.onToolResult,
  onReasoningStream: params.onReasoningStream,
  onBlockReply: params.onBlockReply,
  onPartialReply: params.onPartialReply,
  onAgentEvent: params.onAgentEvent,
});
```

Events handled include:

*   `message_start` / `message_end` / `message_update` (streaming text/thinking)
*   `tool_execution_start` / `tool_execution_update` / `tool_execution_end`
*   `turn_start` / `turn_end`
*   `agent_start` / `agent_end`
*   `auto_compaction_start` / `auto_compaction_end`

### 4\. Prompting

After setup, the session is prompted:

```
await session.prompt(effectivePrompt, { images: imageResult.images });
```

The SDK handles the full agent loop: sending to LLM, executing tool calls, streaming responses. Image injection is prompt-local: OpenClaw loads image refs from the current prompt and passes them via `images` for that turn only. It does not re-scan older history turns to re-inject image payloads.

### Tool Pipeline

1.  **Base Tools**: pi’s `codingTools` (read, bash, edit, write)
2.  **Custom Replacements**: OpenClaw replaces bash with `exec`/`process`, customizes read/edit/write for sandbox
3.  **OpenClaw Tools**: messaging, browser, canvas, sessions, cron, gateway, etc.
4.  **Channel Tools**: Discord/Telegram/Slack/WhatsApp-specific action tools
5.  **Policy Filtering**: Tools filtered by profile, provider, agent, group, sandbox policies
6.  **Schema Normalization**: Schemas cleaned for Gemini/OpenAI quirks
7.  **AbortSignal Wrapping**: Tools wrapped to respect abort signals

### Tool Definition Adapter

pi-agent-core’s `AgentTool` has a different `execute` signature than pi-coding-agent’s `ToolDefinition`. The adapter in `pi-tool-definition-adapter.ts` bridges this:

```
export function toToolDefinitions(tools: AnyAgentTool[]): ToolDefinition[] {
  return tools.map((tool) => ({
    name: tool.name,
    label: tool.label ?? name,
    description: tool.description ?? "",
    parameters: tool.parameters,
    execute: async (toolCallId, params, onUpdate, _ctx, signal) => {
      // pi-coding-agent signature differs from pi-agent-core
      return await tool.execute(toolCallId, params, signal, onUpdate);
    },
  }));
}
```

### Tool Split Strategy

`splitSdkTools()` passes all tools via `customTools`:

```
export function splitSdkTools(options: { tools: AnyAgentTool[]; sandboxEnabled: boolean }) {
  return {
    builtInTools: [], // Empty. We override everything
    customTools: toToolDefinitions(options.tools),
  };
}
```

This ensures OpenClaw’s policy filtering, sandbox integration, and extended toolset remain consistent across providers.

## System Prompt Construction

The system prompt is built in `buildAgentSystemPrompt()` (`system-prompt.ts`). It assembles a full prompt with sections including Tooling, Tool Call Style, Safety guardrails, OpenClaw CLI reference, Skills, Docs, Workspace, Sandbox, Messaging, Reply Tags, Voice, Silent Replies, Heartbeats, Runtime metadata, plus Memory and Reactions when enabled, and optional context files and extra system prompt content. Sections are trimmed for minimal prompt mode used by subagents. The prompt is applied after session creation via `applySystemPromptOverrideToSession()`:

```
const systemPromptOverride = createSystemPromptOverride(appendPrompt);
applySystemPromptOverrideToSession(session, systemPromptOverride);
```

## Session Management

### Session Files

Sessions are JSONL files with tree structure (id/parentId linking). Pi’s `SessionManager` handles persistence:

```
const sessionManager = SessionManager.open(params.sessionFile);
```

OpenClaw wraps this with `guardSessionManager()` for tool result safety.

### Session Caching

`session-manager-cache.ts` caches SessionManager instances to avoid repeated file parsing:

```
await prewarmSessionFile(params.sessionFile);
sessionManager = SessionManager.open(params.sessionFile);
trackSessionManagerAccess(params.sessionFile);
```

### History Limiting

`limitHistoryTurns()` trims conversation history based on channel type (DM vs group).

### Compaction

Auto-compaction triggers on context overflow. `compactEmbeddedPiSessionDirect()` handles manual compaction:

```
const compactResult = await compactEmbeddedPiSessionDirect({
  sessionId, sessionFile, provider, model, ...
});
```

## Authentication & Model Resolution

### Auth Profiles

OpenClaw maintains an auth profile store with multiple API keys per provider:

```
const authStore = ensureAuthProfileStore(agentDir, { allowKeychainPrompt: false });
const profileOrder = resolveAuthProfileOrder({ cfg, store: authStore, provider, preferredProfile });
```

Profiles rotate on failures with cooldown tracking:

```
await markAuthProfileFailure({ store, profileId, reason, cfg, agentDir });
const rotated = await advanceAuthProfile();
```

### Model Resolution

```
import { resolveModel } from "./pi-embedded-runner/model.js";

const { model, error, authStorage, modelRegistry } = resolveModel(
  provider,
  modelId,
  agentDir,
  config,
);

// Uses pi's ModelRegistry and AuthStorage
authStorage.setRuntimeApiKey(model.provider, apiKeyInfo.apiKey);
```

### Failover

`FailoverError` triggers model fallback when configured:

```
if (fallbackConfigured && isFailoverErrorMessage(errorText)) {
  throw new FailoverError(errorText, {
    reason: promptFailoverReason ?? "unknown",
    provider,
    model: modelId,
    profileId,
    status: resolveFailoverStatus(promptFailoverReason),
  });
}
```

## Pi Extensions

OpenClaw loads custom pi extensions for specialized behavior:

### Compaction Safeguard

`src/agents/pi-extensions/compaction-safeguard.ts` adds guardrails to compaction, including adaptive token budgeting plus tool failure and file operation summaries:

```
if (resolveCompactionMode(params.cfg) === "safeguard") {
  setCompactionSafeguardRuntime(params.sessionManager, { maxHistoryShare });
  paths.push(resolvePiExtensionPath("compaction-safeguard"));
}
```

### Context Pruning

`src/agents/pi-extensions/context-pruning.ts` implements cache-TTL based context pruning:

```
if (cfg?.agents?.defaults?.contextPruning?.mode === "cache-ttl") {
  setContextPruningRuntime(params.sessionManager, {
    settings,
    contextWindowTokens,
    isToolPrunable,
    lastCacheTouchAt,
  });
  paths.push(resolvePiExtensionPath("context-pruning"));
}
```

### Block Chunking

`EmbeddedBlockChunker` manages streaming text into discrete reply blocks:

```
const blockChunker = blockChunking ? new EmbeddedBlockChunker(blockChunking) : null;
```

### Thinking/Final Tag Stripping

Streaming output is processed to strip `<think>`/`<thinking>` blocks and extract `<final>` content:

```
const stripBlockTags = (text: string, state: { thinking: boolean; final: boolean }) => {
  // Strip <think>...</think> content
  // If enforceFinalTag, only return <final>...</final> content
};
```

### Reply Directives

Reply directives like `[[media:url]]`, `[[voice]]`, `[[reply:id]]` are parsed and extracted:

```
const { text: cleanedText, mediaUrls, audioAsVoice, replyToId } = consumeReplyDirectives(chunk);
```

## Error Handling

### Error Classification

`pi-embedded-helpers.ts` classifies errors for appropriate handling:

```
isContextOverflowError(errorText)     // Context too large
isCompactionFailureError(errorText)   // Compaction failed
isAuthAssistantError(lastAssistant)   // Auth failure
isRateLimitAssistantError(...)        // Rate limited
isFailoverAssistantError(...)         // Should failover
classifyFailoverReason(errorText)     // "auth" | "rate_limit" | "quota" | "timeout" | ...
```

### Thinking Level Fallback

If a thinking level is unsupported, it falls back:

```
const fallbackThinking = pickFallbackThinkingLevel({
  message: errorText,
  attempted: attemptedThinking,
});
if (fallbackThinking) {
  thinkLevel = fallbackThinking;
  continue;
}
```

## Sandbox Integration

When sandbox mode is enabled, tools and paths are constrained:

```
const sandbox = await resolveSandboxContext({
  config: params.config,
  sessionKey: sandboxSessionKey,
  workspaceDir: resolvedWorkspace,
});

if (sandboxRoot) {
  // Use sandboxed read/edit/write tools
  // Exec runs in container
  // Browser uses bridge URL
}
```

## Provider-Specific Handling

### Anthropic

*   Refusal magic string scrubbing
*   Turn validation for consecutive roles
*   Claude Code parameter compatibility

### Google/Gemini

*   Turn ordering fixes (`applyGoogleTurnOrderingFix`)
*   Tool schema sanitization (`sanitizeToolsForGoogle`)
*   Session history sanitization (`sanitizeSessionHistory`)

### OpenAI

*   `apply_patch` tool for Codex models
*   Thinking level downgrade handling

## TUI Integration

OpenClaw also has a local TUI mode that uses pi-tui components directly:

```
// src/tui/tui.ts
import { ... } from "@mariozechner/pi-tui";
```

This provides the interactive terminal experience similar to pi’s native mode.

## Key Differences from Pi CLI

| Aspect | Pi CLI | OpenClaw Embedded |
| --- | --- | --- |
| Invocation | `pi` command / RPC | SDK via `createAgentSession()` |
| Tools | Default coding tools | Custom OpenClaw tool suite |
| System prompt | AGENTS.md + prompts | Dynamic per-channel/context |
| Session storage | `~/.pi/agent/sessions/` | `~/.openclaw/agents/<agentId>/sessions/` (or `$OPENCLAW_STATE_DIR/agents/<agentId>/sessions/`) |
| Auth | Single credential | Multi-profile with rotation |
| Extensions | Loaded from disk | Programmatic + disk paths |
| Event handling | TUI rendering | Callback-based (onBlockReply, etc.) |

## Future Considerations

Areas for potential rework:

1.  **Tool signature alignment**: Currently adapting between pi-agent-core and pi-coding-agent signatures
2.  **Session manager wrapping**: `guardSessionManager` adds safety but increases complexity
3.  **Extension loading**: Could use pi’s `ResourceLoader` more directly
4.  **Streaming handler complexity**: `subscribeEmbeddedPiSession` has grown large
5.  **Provider quirks**: Many provider-specific codepaths that pi could potentially handle

## Tests

Pi integration coverage spans these suites:

*   `src/agents/pi-*.test.ts`
*   `src/agents/pi-auth-json.test.ts`
*   `src/agents/pi-embedded-*.test.ts`
*   `src/agents/pi-embedded-helpers*.test.ts`
*   `src/agents/pi-embedded-runner*.test.ts`
*   `src/agents/pi-embedded-runner/**/*.test.ts`
*   `src/agents/pi-embedded-subscribe*.test.ts`
*   `src/agents/pi-tools*.test.ts`
*   `src/agents/pi-tool-definition-adapter*.test.ts`
*   `src/agents/pi-settings.test.ts`
*   `src/agents/pi-extensions/**/*.test.ts`

Live/opt-in:

*   `src/agents/pi-embedded-runner-extraparams.live.test.ts` (enable `OPENCLAW_LIVE_TEST=1`)

For current run commands, see [Pi Development Workflow](https://docs.openclaw.ai/pi-dev).

