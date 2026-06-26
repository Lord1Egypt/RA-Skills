# Multi-Agent VPS Deployment

Run multiple isolated OpenClaw agents on a single VPS, each with its own port, workspace, identity, and public URL.

## Table of Contents
1. [Architecture](#architecture)
2. [Port Allocation](#port-allocation)
3. [Provisioning a New Agent](#provisioning-a-new-agent)
4. [Systemd Services](#systemd-services)
5. [Connecting Cloudflare Tunnels](#connecting-cloudflare-tunnels)
6. [Managing All Agents](#managing-all-agents)

---

## Architecture

Each agent is a fully isolated OpenClaw gateway process:

```
VPS (187.124.84.25)
├── /root/agents/
│   ├── koda/         ← config, workspace, sessions
│   ├── alex/
│   └── jordan/
│
├── openclaw-koda.service     → port 18789
├── openclaw-alex.service     → port 18790
├── openclaw-jordan.service   → port 18791
│
├── cloudflared-koda.service  → https://koda.yourdomain.com
├── cloudflared-alex.service  → https://alex.yourdomain.com
└── cloudflared-jordan.service → https://jordan.yourdomain.com
```

No core OpenClaw modifications required. Multi-gateway is a first-class feature via `--config-dir`.

---

## Port Allocation

Reserve a port range and track it:

| Port  | Agent   | Tunnel URL                    |
|-------|---------|-------------------------------|
| 18789 | koda    | koda.yourdomain.com           |
| 18790 | alex    | alex.yourdomain.com           |
| 18791 | jordan  | jordan.yourdomain.com         |
| 18792 | (next)  | ...                           |

Open all agent ports on UFW at once:
```bash
for port in 18789 18790 18791; do ufw allow $port/tcp; done
```

Or keep ports **closed** to the public and only expose them through Cloudflare Tunnel (recommended — Cloudflare handles the HTTPS, the raw port stays private).

---

## Provisioning a New Agent

Run this on the VPS (replace `alex` and `18790` with your values):

```bash
AGENT_NAME="alex"
AGENT_PORT=18790
AGENT_MODEL="anthropic/claude-sonnet-4-6"
AGENT_TOKEN=$(openssl rand -hex 24)
SERVER_IP=$(curl -s ifconfig.me)

# 1. Create config directory
mkdir -p /root/agents/${AGENT_NAME}/.openclaw/agents/main/sessions
chmod 700 /root/agents/${AGENT_NAME}/.openclaw

# 2. Write openclaw.json
cat > /root/agents/${AGENT_NAME}/.openclaw/openclaw.json << EOF
{
  "agents": {
    "defaults": {
      "model": { "primary": "${AGENT_MODEL}" }
    },
    "list": [
      {
        "id": "main",
        "default": true,
        "name": "${AGENT_NAME^}",
        "model": { "primary": "${AGENT_MODEL}" }
      }
    ]
  },
  "env": {
    "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
  },
  "gateway": {
    "port": ${AGENT_PORT},
    "bind": "lan",
    "mode": "remote",
    "auth": {
      "mode": "token",
      "token": "${AGENT_TOKEN}"
    },
    "controlUi": {
      "allowedOrigins": [
        "http://localhost:${AGENT_PORT}",
        "http://127.0.0.1:${AGENT_PORT}",
        "http://${SERVER_IP}:${AGENT_PORT}"
      ]
    }
  }
}
EOF

chmod 600 /root/agents/${AGENT_NAME}/.openclaw/openclaw.json

echo "Agent token for ${AGENT_NAME}: ${AGENT_TOKEN}"
```

---

## Systemd Services

### OpenClaw service per agent

Create `/etc/systemd/system/openclaw-${AGENT_NAME}.service`:

```ini
[Unit]
Description=OpenClaw Agent - alex
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/agents/alex
ExecStart=/usr/bin/openclaw gateway \
  --config-dir /root/agents/alex/.openclaw \
  --bind lan \
  --port 18790 \
  --auth token \
  --allow-unconfigured
Restart=always
RestartSec=5
Environment=HOME=/root/agents/alex
Environment=OPENCLAW_NO_RESPAWN=1
Environment=NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache-alex
Environment=XDG_RUNTIME_DIR=/run/user/0

[Install]
WantedBy=multi-user.target
```

**Note:** Set `HOME` to the agent dir so OpenClaw resolves workspace paths correctly. Set `NODE_COMPILE_CACHE` to a unique path per agent to avoid cache collisions.

Enable and start:
```bash
systemctl daemon-reload
systemctl enable openclaw-alex
systemctl start openclaw-alex
systemctl status openclaw-alex
```

---

## Connecting Cloudflare Tunnels

See the `cloudflare-agent-tunnel` skill for full setup. Short version:

### Quick tunnel (no account — temporary URL)
```bash
cloudflared tunnel --url http://localhost:18790
# Prints a random https://*.trycloudflare.com URL
# URL resets on restart — use for testing only
```

### Named tunnel (permanent URL, requires Cloudflare account)
```bash
# One-time: login + create tunnel
cloudflared login
cloudflared tunnel create alex

# Route to your domain
cloudflared tunnel route dns alex alex.yourdomain.com

# Config at /etc/cloudflared/alex.yml
# Service at /etc/systemd/system/cloudflared-alex.service
```

Full walkthrough in: `cloudflare-agent-tunnel` skill.

---

## Managing All Agents

```bash
# Status of all openclaw agents
systemctl list-units "openclaw-*" --no-pager

# Status of all tunnels
systemctl list-units "cloudflared-*" --no-pager

# Restart all agents
systemctl restart openclaw-koda openclaw-alex openclaw-jordan

# Logs for a specific agent
journalctl -u openclaw-alex -f

# List all agent ports in use
ss -tlnp | grep openclaw

# Add a new agent (next available port)
NEXT_PORT=$(ss -tlnp | grep -oP ':\K1878\d' | sort -n | tail -1 | xargs -I{} expr {} + 1)
echo "Next port: ${NEXT_PORT:-18789}"
```

---

## Resource Considerations (KVM 1 — 4GB RAM)

Each OpenClaw agent uses ~300-400MB RAM at idle. On a KVM 1 (4GB):

| Agents | Est. RAM | Headroom |
|--------|----------|----------|
| 1      | ~400MB   | ✅ Plenty |
| 2      | ~800MB   | ✅ Good   |
| 4      | ~1.6GB   | ✅ OK     |
| 8      | ~3.2GB   | ⚠️ Tight  |

For 4+ agents, upgrade to KVM 2 (8GB RAM). CPU is rarely the bottleneck — agents spend most time waiting on API responses.
