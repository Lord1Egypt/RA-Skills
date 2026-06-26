---
name: openclaw-vps-deploy
description: >
  Deploy a custom OpenClaw repo (official or forked) to a Hostinger VPS and make it accessible via
  the cloud. Use when setting up a new OpenClaw instance on a remote VPS, deploying a custom or
  forked OpenClaw build to a server, making OpenClaw accessible at a public URL, or setting up
  OpenClaw as a cloud-hosted service on Hostinger. Handles SSH connection, Node.js install,
  OpenClaw install (npm package or git clone+build), systemd service, firewall, and auth token
  generation.
---

# OpenClaw VPS Deploy

Deploy OpenClaw (official or custom fork) to a Hostinger VPS with full cloud access.

## Quick Deploy

```bash
# Official package (most common)
python3 scripts/deploy.py \
  --ip 187.124.84.25 \
  --key ~/.ssh/id_ed25519 \
  --name "Koda"

# Custom git fork
python3 scripts/deploy.py \
  --ip 187.124.84.25 \
  --key ~/.ssh/id_ed25519 \
  --repo https://github.com/your-org/openclaw \
  --name "Koda" \
  --gw-port 18789
```

The script auto-reads `ANTHROPIC_API_KEY` from the local OpenClaw vault (`~/.openclaw/secrets.json`) or environment. Pass `--anthropic` to override.

## What the Script Does

1. **Connects** via SSH (key auth — required, password auth often disabled on Hostinger)
2. **Installs Node.js 22** via nodesource apt repo
3. **Installs OpenClaw** — either `npm install -g <package>` or git clone + `pnpm build`
4. **Writes `openclaw.json`** with correct schema (see critical notes below)
5. **Installs systemd service** — auto-starts on reboot, restarts on crash
6. **Opens UFW ports** — SSH (22) + gateway port
7. **Saves auth token** to local vault as `OPENCLAW_VPS_<IP>_TOKEN`

## SSH Key on WSL2

The user's Windows SSH key is accessible at `/mnt/c/Users/<username>/.ssh/id_ed25519` in WSL2. Copy it with correct permissions before use:

```bash
cp /mnt/c/Users/charl/.ssh/id_ed25519 /tmp/vps_key
chmod 600 /tmp/vps_key
python3 scripts/deploy.py --ip 1.2.3.4 --key /tmp/vps_key
```

## Getting the Server IP

From the Hostinger tab in the Control dashboard (VPS Servers section), or via API:

```bash
mcporter call hostinger-api.VPS_getVirtualMachinesV1 2>&1 | \
  python3 -c "import json,sys; [print(v['id'], v['ipv4'][0]['address'], v['hostname']) for v in json.load(sys.stdin) if v.get('ipv4')]"
```

## Critical Notes (Read Before Manually Deploying)

See `references/gotchas.md` for full details on every failure mode. Key points:

1. **Never use `openclaw gateway start`** as ExecStart — use `openclaw gateway --bind lan --auth token --allow-unconfigured`
2. **Config schema**: use `agents.list[]` not `agents.default` (causes schema error)
3. **Set `gateway.mode`** — required, use `"remote"` for cloud access
4. **Set `XDG_RUNTIME_DIR=/run/user/0`** in systemd + `mkdir -p /run/user/0`
5. **Add public IP to `allowedOrigins`** — otherwise the UI blocks non-localhost connections
6. **Performance**: always set `OPENCLAW_NO_RESPAWN=1` and `NODE_COMPILE_CACHE`

## Correct openclaw.json Schema

```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "anthropic/claude-sonnet-4-6" }
    },
    "list": [
      { "id": "main", "default": true, "name": "Koda" }
    ]
  },
  "env": {
    "ANTHROPIC_API_KEY": "sk-ant-..."
  },
  "gateway": {
    "port": 18789,
    "bind": "lan",
    "mode": "remote",
    "auth": { "mode": "token", "token": "your-token" },
    "controlUi": {
      "allowedOrigins": [
        "http://localhost:18789",
        "http://127.0.0.1:18789",
        "http://YOUR.SERVER.IP:18789"
      ]
    }
  }
}
```

## Correct systemd Unit

```ini
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root
ExecStart=/usr/bin/openclaw gateway --bind lan --port 18789 --auth token --allow-unconfigured
Restart=always
RestartSec=5
Environment=HOME=/root
Environment=OPENCLAW_NO_RESPAWN=1
Environment=NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
Environment=XDG_RUNTIME_DIR=/run/user/0

[Install]
WantedBy=multi-user.target
```

## Managing a Live Instance

```bash
# Status
ssh root@SERVER_IP "systemctl status openclaw"

# Logs (live)
ssh root@SERVER_IP "journalctl -u openclaw -f"

# Restart
ssh root@SERVER_IP "systemctl restart openclaw"

# Update OpenClaw (npm)
ssh root@SERVER_IP "npm install -g openclaw && systemctl restart openclaw"

# Update custom fork (git)
ssh root@SERVER_IP "cd /opt/openclaw && git pull && pnpm install && pnpm build && systemctl restart openclaw"
```

## Accessing the UI

Navigate to `http://SERVER_IP:18789`. When prompted for an auth token, use the value stored in:
- Local vault: `OPENCLAW_VPS_<IP_WITH_UNDERSCORES>_TOKEN`
- Or retrieve: `python3 -c "import json; v=json.load(open('/home/charl/.openclaw/secrets.json')); [print(k,v[k]) for k in v if 'VPS' in k and 'TOKEN' in k]"`

## Multi-Agent VPS Setup

One VPS can run multiple isolated agents on separate ports, each with its own Cloudflare URL. No core OpenClaw changes needed — use `--config-dir` per agent.

See `references/multi-agent.md` for: port allocation, per-agent systemd services, provisioning script, resource planning, and Cloudflare tunnel integration.

```bash
# Each agent = separate gateway on a separate port
openclaw gateway --config-dir /root/agents/koda   --port 18789
openclaw gateway --config-dir /root/agents/alex   --port 18790
```

## Dependencies

- `paramiko` Python package (auto-installed by deploy.py if missing)
- SSH private key with access to the target VPS
- `ANTHROPIC_API_KEY` in vault or environment
