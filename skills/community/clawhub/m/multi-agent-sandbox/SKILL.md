---
name: multi-agent-sandbox
description: "Setup multi-agent sandbox infrastructure with Docker, Discord, SSH, and Tailscale. Use when: (1) creating a sandboxed agent for cross-gateway collaboration, (2) setting up Discord multi-bot with separate accounts and requireMention gating, (3) configuring socat bridges for container→VPS SSH via Tailscale, (4) enabling bidirectional agent-to-agent communication via sessions_send with per-agent A2A allowlists, (5) sharing a VPS workspace between agents from different OpenClaw gateways, (6) isolating sandbox agents from main agent private data."
---

# Multi-Agent Sandbox

Set up sandboxed agents that collaborate with agents from other OpenClaw gateways via Discord and a shared VPS, without exposing private data.

## Architecture

```
Gateway A (Server A)                  Gateway B (Server B)
├── Main Agent (full access)          ├── Main Agent (full access)
│   agentToAgent.allow: ["*"]         │   agentToAgent.allow: ["*"]
└── Sandbox Agent (Docker)            └── Sandbox Agent (Docker)
    agentToAgent.allow: ["main"]          agentToAgent.allow: ["main"]
    ├── Discord ←── Shared Server ──→ Discord
    │                requireMention: true
    └── SSH ─→ socat ─→ Tailscale ─→ Shared VPS ←── SSH
                                      100.y.y.y
```

Three pillars: **socat bridges** (container → host → VPS), **Tailscale mesh VPN** (private networking), **Discord + sessions_send** (inter-agent communication).

## Prerequisites

- OpenClaw running with Docker sandbox support
- Tailscale installed on all machines (server A + VPS + server B)
- A Discord bot token per sandbox agent (https://discord.com/developers/applications)
- A shared VPS accessible via Tailscale

## Step 1 — Create the Sandbox Agent

Add to `openclaw.json` under `agents.list`:

```json
{
  "id": "sandbox",
  "workspace": "/path/to/workspace-sandbox",
  "model": {
    "primary": "anthropic/claude-sonnet-4-6",
    "fallbacks": ["openai/gpt-4o"]
  },
  "identity": {
    "name": "Sandbox",
    "emoji": "📦"
  },
  "sandbox": {
    "mode": "all",
    "workspaceAccess": "rw",
    "sessionToolsVisibility": "all",
    "scope": "agent",
    "docker": {
      "image": "openclaw-sandbox:bookworm-slim",
      "readOnlyRoot": true,
      "network": "bridge",
      "memory": "1536m",
      "cpus": 2
    },
    "browser": { "enabled": true }
  },
  "tools": {
    "agentToAgent": {
      "allow": ["your-main-agent-id"]
    },
    "alsoAllow": ["message", "sessions_send", "sessions_list", "sessions_history"],
    "deny": ["gateway", "process", "whatsapp_login", "cron"],
    "sandbox": {
      "tools": {
        "allow": [
          "exec", "process", "read", "write", "edit", "apply_patch",
          "image", "web_search", "web_fetch",
          "sessions_list", "sessions_history", "sessions_send", "sessions_spawn",
          "subagents", "session_status", "message", "browser"
        ],
        "deny": [
          "canvas", "nodes", "gateway", "telegram", "irc", "googlechat",
          "slack", "signal", "imessage", "whatsapp_login", "cron"
        ]
      }
    }
  }
}
```

Key constraints:
- **`sandbox.mode: "all"`** — all exec runs through Docker, never on host
- **`readOnlyRoot: true`** — container filesystem is immutable except workspace
- **`tools.deny`** — no gateway (can't modify config), no cron (can't schedule on host)
- **`scope: "agent"`** — isolated container per agent (valid values: `session | agent | shared`)

## Step 2 — A2A Permissions (Hub-Spoke Pattern)

Configure bidirectional communication using per-agent outbound allowlists (PR #39102):

```json
{
  "tools": {
    "agentToAgent": { "enabled": true, "allow": ["*"] }
  },
  "agents": {
    "list": [
      {
        "id": "main-agent",
        "tools": { "agentToAgent": { "allow": ["*"] } }
      },
      {
        "id": "sandbox",
        "tools": { "agentToAgent": { "allow": ["main-agent"] } }
      }
    ]
  }
}
```

Result: `sandbox → main-agent` ✅ | `sandbox → other-sandbox` ❌ | `main-agent → anyone` ✅

Both agents also need `subagents.allowAgents` for `sessions_spawn`:

```json
// Main agent
"subagents": { "allowAgents": ["sandbox"] }

// Sandbox agent
"subagents": { "allowAgents": ["main-agent"] }
```

**Must be set on BOTH agents.** Forgetting one direction = silent "access denied" errors.

## Step 3 — Add SSH to Docker Image

The default sandbox image lacks SSH. Edit `Dockerfile.sandbox`:

```dockerfile
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    bash ca-certificates curl git jq \
    openssh-client \
    python3 ripgrep \
  && rm -rf /var/lib/apt/lists/*
```

Rebuild and force-recreate containers:

```bash
docker build -f Dockerfile.sandbox -t openclaw-sandbox:bookworm-slim .
docker ps --format "{{.ID}} {{.Image}}" | grep sandbox | awk '{print $1}' | xargs -r docker rm -f
```

## Step 4 — Socat Bridges

Two bridges on each host. Always bind on `172.17.0.1` (docker0), **never** `0.0.0.0`.

### Bridge 1: Container → Gateway (local)

```ini
# /etc/systemd/system/socat-bridge-docker0-gateway.service
[Unit]
Description=Socat bridge: docker0 → Gateway
After=network.target docker.service

[Service]
Type=simple
ExecStart=/usr/bin/socat TCP-LISTEN:18789,bind=172.17.0.1,reuseaddr,fork TCP:127.0.0.1:18789
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### Bridge 2: Container → VPS SSH (via Tailscale)

```ini
# /etc/systemd/system/socat-bridge-docker0-vps-ssh.service
[Unit]
Description=Socat bridge: docker0:2222 → VPS Tailscale SSH
After=network.target docker.service tailscaled.service
Wants=tailscaled.service

[Service]
Type=simple
ExecStart=/usr/bin/socat TCP-LISTEN:2222,bind=172.17.0.1,reuseaddr,fork TCP:100.y.y.y:22
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable, start, and open firewall:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now socat-bridge-docker0-gateway socat-bridge-docker0-vps-ssh
sudo ufw allow in on docker0 to 172.17.0.1 port 18789 proto tcp comment "socat-gateway"
sudo ufw allow in on docker0 to 172.17.0.1 port 2222 proto tcp comment "socat-vps-ssh"
```

**The VPS bridge depends on Tailscale** (`Wants=tailscaled.service`). Without this, socat tries to connect before the Tailscale interface exists — silent failure.

## Step 5 — Discord Multi-Bot

### Create a Discord bot

1. https://discord.com/developers/applications → New Application
2. Bot → Reset Token → copy
3. Enable all 3 **Privileged Gateway Intents** (MESSAGE CONTENT, SERVER MEMBERS, PRESENCE)
4. Invite: `https://discord.com/oauth2/authorize?client_id=<APP_ID>&permissions=274878024704&scope=bot`

### Configure in openclaw.json

```json
"discord": {
  "enabled": true,
  "accounts": {
    "default": {
      "enabled": true,
      "name": "Main Bot",
      "token": "$DISCORD_TOKEN_MAIN",
      "groupPolicy": "allowlist",
      "dmPolicy": "allowlist",
      "allowFrom": ["<YOUR_DISCORD_USER_ID>"],
      "guilds": {
        "<PRIVATE_GUILD_ID>": {
          "slug": "private",
          "requireMention": false
        }
      }
    },
    "sandbox": {
      "enabled": true,
      "name": "Sandbox Bot",
      "token": "$DISCORD_TOKEN_SANDBOX",
      "groupPolicy": "allowlist",
      "dmPolicy": "deny",
      "guilds": {
        "<SHARED_GUILD_ID>": {
          "slug": "shared",
          "requireMention": true
        }
      }
    }
  }
}
```

### Agent routing bindings

```json
"mappings": [
  {
    "agentId": "main-agent",
    "match": { "channel": "discord", "accountId": "default", "guildId": "<PRIVATE_GUILD_ID>" }
  },
  {
    "agentId": "sandbox",
    "match": { "channel": "discord", "accountId": "sandbox", "guildId": "<SHARED_GUILD_ID>" }
  }
]
```

**`requireMention: true` is non-negotiable** on shared guilds. Without it, two bots respond to each other = infinite loop + astronomical token bill.

## Step 6 — Tailscale

Install on all machines:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --ssh
```

The `--ssh` flag enables Tailscale SSH (identity-based auth, no keys to manage). For machines where you can't interactively authenticate:

```bash
# Generate auth key at https://login.tailscale.com → Settings → Keys
sudo tailscale up --authkey=tskey-auth-xxxxx --ssh
```

**Do NOT install Tailscale inside the container.** It requires `NET_ADMIN` capability, which defeats the sandbox purpose. Use socat bridges instead.

## Step 7 — Sandbox Workspace

Create minimal workspace files:

```bash
mkdir -p /path/to/workspace-sandbox
```

**SOUL.md** — Define agent identity and constraints.
**TOOLS.md** — Document SSH access: `ssh -o StrictHostKeyChecking=no root@172.17.0.1 -p 2222`

## Communication Patterns

```
# Main → Sandbox (same gateway)
sessions_send(label="sandbox", message="...")

# Sandbox → Main (same gateway)
sessions_send(label="main-agent", message="...")

# Agent A → Agent B (different gateways)
# Only via Discord @mention. No sessions_send across gateways.

# Async collaboration
# Both agents SSH to VPS /workspace and use files.
```

## Gotchas

1. **Container not using new image** — After rebuilding Docker image, stop and remove old containers. OpenClaw reuses running containers.
2. **Cross-context messaging** — Agent spawned from WhatsApp cannot write to Discord. First trigger must come from the right channel.
3. **MESSAGE CONTENT Intent** — Must be enabled in Discord Developer Portal or bot receives empty messages.
4. **Socat silent timeout** — If `ssh -p 2222` hangs with no error, check UFW rules on docker0.
5. **Agent ID rename** — Renaming an agent (e.g., `sandbox` → `spoke`) breaks active sessions that reference the old ID. Add the old ID to `agentToAgent.allow` until those sessions expire.
6. **sessions_send timeout** — `timeoutSeconds: 0` for fire-and-forget, `timeoutSeconds: 60` when waiting for a response. Timeout ≠ message not delivered.
7. **Bot token exposure** — Never post tokens in Discord channels. If exposed, reset immediately via Developer Portal.
