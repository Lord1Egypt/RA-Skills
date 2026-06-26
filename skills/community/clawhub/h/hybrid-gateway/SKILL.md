---
name: hybrid-gateway
description: Set up and troubleshoot a hybrid OpenClaw architecture where the gateway runs on a cloud VPS and a local machine (Mac Mini, desktop, Raspberry Pi, etc.) acts as a node. Covers Tailscale networking, gateway bind modes, node pairing, LaunchAgent/systemd auto-start, exec routing, SSH fallback, and the common gotchas that break this setup. Use when connecting a local node to a remote gateway, debugging node connectivity, or planning a VPS + local hardware split.
metadata:
  openclaw:
    env:
      - name: OPENCLAW_GATEWAY_TOKEN
        description: Your existing gateway auth token (already configured on your VPS). The node needs this to authenticate with the gateway.
        scope: node-service
      - name: OPENCLAW_ALLOW_INSECURE_PRIVATE_WS
        description: Optional. Set to 1 to allow ws:// over Tailscale (safe — traffic is WireGuard-encrypted). Not needed if using wss:// via Tailscale Serve.
        scope: node-service
        required: false
---

# Hybrid Gateway — VPS + Local Node

Run your OpenClaw gateway on a cloud VPS for reliability, and connect a local machine as a node for hardware capabilities the VPS lacks: residential IP, GPU/ML inference, browser automation, local models, macOS-only tools, etc.

## Why this architecture?

| | VPS (Gateway) | Local Node |
|---|---|---|
| **Always online** | ✅ Static IP, no ISP outages | ❌ Power/network dependent |
| **Messaging** | ✅ Handles Telegram, Discord, etc. | ❌ Not its job |
| **Agent brain** | ✅ Runs models, routes tools | ❌ Peripheral only |
| **GPU / ML** | ❌ Most VPS have no GPU | ✅ Apple Silicon, NVIDIA, etc. |
| **Browser automation** | ⚠️ Headless only, cloud IP | ✅ Real browser, residential IP |
| **Local models** | ❌ No hardware for it | ✅ Ollama, whisper, etc. |
| **macOS tools** | ❌ Linux VPS | ✅ Native macOS (if using Mac) |

## Prerequisites

Before starting, you need:

1. **OpenClaw installed on both machines** — VPS (gateway) and local machine (node)
2. **Tailscale installed on both machines** — this is how they talk to each other
   - [Download Tailscale](https://tailscale.com/download)
   - Sign in on both machines with the same Tailscale account
   - Verify connectivity: `tailscale status` on either machine should show both devices
3. **Gateway already running on the VPS** — `openclaw gateway status` should show running
4. **Gateway auth token configured** — required for non-loopback connections

If you don't have Tailscale set up yet, do that first. The rest of this guide assumes both machines are on the same tailnet.

## Step 1 — Configure gateway bind mode

By default, the gateway binds to `loopback` (127.0.0.1 only). Your node can't reach that from another machine.

**Recommended: `lan` bind (listens on all interfaces)**

```bash
# On the VPS
openclaw config set gateway.bind lan
```

This listens on `0.0.0.0` — both `127.0.0.1` (local agents) and your Tailscale IP (remote node) will work.

**Alternative: `tailnet` bind (Tailscale IP only)**

```bash
openclaw config set gateway.bind tailnet
```

⚠️ **Warning:** `tailnet` bind breaks local agent-to-agent sessions. Local tools try `ws://127.0.0.1:18789` but the gateway only listens on the Tailscale IP. If you use multi-agent workflows, use `lan` instead.

**Ensure auth is configured** (required for any non-loopback bind):

```bash
# Check current auth
openclaw config get gateway.auth.mode
openclaw config get gateway.auth.token

# Set token auth if not configured
openclaw config set gateway.auth.mode token
openclaw config set gateway.auth.token "<your-token>"

# Add rate limiting (recommended)
openclaw config set gateway.auth.rateLimit.maxAttempts 10
openclaw config set gateway.auth.rateLimit.windowMs 60000
openclaw config set gateway.auth.rateLimit.lockoutMs 300000
```

Restart the gateway after config changes:

```bash
openclaw gateway restart
```

Verify:

```bash
openclaw gateway status
# Should show: bind=lan (0.0.0.0) and RPC probe: ok
```

## Step 2 — Start the node on your local machine

On the local machine (Mac Mini, desktop, etc.):

```bash
# Get your VPS Tailscale IP (run on VPS)
tailscale ip -4
# Example output: 100.x.y.z

# On the local machine, set the gateway token
export OPENCLAW_GATEWAY_TOKEN="<your-token>"

# Start the node (foreground, for testing)
openclaw node run --host <VPS_TAILSCALE_IP> --port 18789 --display-name "My Node"
```

If it connects, you'll see it register. If not, see Troubleshooting below.

## Step 3 — Approve the device pairing

On the VPS:

```bash
openclaw devices list
# Find the pending request from your node
openclaw devices approve <requestId>

# Verify
openclaw nodes status
# Should show your node as paired and connected
```

## Step 4 — Install as a service (auto-start)

You want the node to survive reboots and run headless.

### macOS (LaunchAgent)

```bash
openclaw node install --host <VPS_TAILSCALE_IP> --port 18789 --display-name "My Node"
```

This creates a LaunchAgent plist that auto-starts on login.

**Important:** If the gateway requires `ws://` over a private network (not `wss://`), you may need to set an environment variable in the LaunchAgent plist:

Add these environment variables to the plist's `EnvironmentVariables` dict:

- `OPENCLAW_GATEWAY_TOKEN` — your existing gateway auth token (the same one from `openclaw config get gateway.auth.token` on the VPS)
- `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS` = `1` — allows `ws://` over Tailscale (safe — traffic is WireGuard-encrypted at the network layer)

See the [OpenClaw node host docs](https://docs.openclaw.ai/nodes/) for the full plist reference.

The insecure WS override is only needed because OpenClaw blocks plaintext `ws://` to non-loopback addresses by default. On Tailscale this is safe since all traffic is encrypted by WireGuard.

The LaunchAgent plist location: `~/Library/LaunchAgents/ai.openclaw.node.plist`

Load/unload manually:

```bash
launchctl load ~/Library/LaunchAgents/ai.openclaw.node.plist
launchctl unload ~/Library/LaunchAgents/ai.openclaw.node.plist
```

Check logs: `~/.openclaw/logs/node.log`

### Linux (systemd)

```bash
openclaw node install --host <VPS_TAILSCALE_IP> --port 18789 --display-name "My Node"
```

Or create a systemd user service manually:

In the systemd service `[Service]` section, add:

- `Environment=OPENCLAW_GATEWAY_TOKEN=<your-gateway-token>` — same token from your VPS gateway config
- `Environment=OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` — only if not using `wss://` via Tailscale Serve

See the [OpenClaw node host docs](https://docs.openclaw.ai/nodes/) for the full service file reference.

```bash
systemctl --user daemon-reload
systemctl --user enable openclaw-node
systemctl --user start openclaw-node
```

## Step 5 — Configure exec routing

Tell the gateway to route `exec host=node` commands to your node:

```bash
# On the VPS
openclaw config set tools.exec.node "My Node"
```

Now agents can run commands on your local machine:

```
exec host=node command="uname -a"
```

### Set up exec approvals on the node

The node enforces its own allowlist. Add commands you want to permit:

```bash
# On the VPS (manages node approvals remotely)
openclaw approvals allowlist add --node "My Node" "/usr/bin/uname"
openclaw approvals allowlist add --node "My Node" "/bin/bash"
openclaw approvals allowlist add --node "My Node" "/usr/local/bin/node"
```

Or edit `~/.openclaw/exec-approvals.json` on the node directly.

## Step 6 — Set up SSH fallback (optional but recommended)

The node protocol handles command execution, but SSH is still needed for:
- **File transfers** (scp/rsync between VPS and node)
- **Full shell environment** (commands needing `.bashrc`/`.zshrc` — nvm, homebrew PATH, env vars)
- **Fallback** when the node disconnects

### Set up SSH key access

```bash
Set up SSH key-based access between the VPS and the node:

1. Generate an ed25519 key pair on the VPS
2. Copy the public key to the node's `authorized_keys`
3. Create an SSH config alias (e.g. `Host my-node`) pointing to the node's Tailscale IP
4. Test with `ssh my-node` to confirm passwordless access

See the [GitHub SSH key guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) for detailed steps — the same process applies to any SSH host.
```

### When to use which transport

| Task | Use |
|---|---|
| Run a command | `exec host=node` (node protocol) |
| Transfer files | `scp my-node:/path/to/file .` (SSH) |
| Commands needing shell env | `ssh my-node "source ~/.zshrc; command"` (SSH) |
| Node disconnected | SSH fallback for everything |

## Troubleshooting

### "SECURITY ERROR: Cannot connect over plaintext ws://"

The node is trying to connect via `ws://` (not `wss://`) to a non-loopback address. This is blocked by default.

**Fix:** Set `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` in the node's environment. This is safe on Tailscale (WireGuard-encrypted). Add it to your LaunchAgent plist or systemd service.

**Better fix (long-term):** Use [Tailscale Serve](https://tailscale.com/kb/1242/tailscale-serve) to get proper `wss://` on the gateway. Then you don't need the env override.

### Local agent sessions fail after changing gateway.bind

If you changed `gateway.bind` from `loopback` to `tailnet`, local agent-to-agent communication breaks. Local sessions try `ws://127.0.0.1` but the gateway only listens on the Tailscale IP.

**Fix:** Use `gateway.bind: "lan"` instead. This listens on `0.0.0.0` — both loopback and Tailscale interfaces.

### Node shows "pairing required"

Network route is working, auth is fine, but the device hasn't been approved yet.

```bash
# On the VPS
openclaw devices list
openclaw devices approve <requestId>
```

### Node shows "bootstrap token invalid or expired"

The setup code or pairing token is stale.

**Fix:** Generate a fresh one and reconnect:
```bash
openclaw qr --json
```

### Node connects but exec host=node doesn't work

1. Check the node is actually paired and connected:
   ```bash
   openclaw nodes status
   ```
2. Check `tools.exec.node` points to the right node:
   ```bash
   openclaw config get tools.exec.node
   ```
3. Check exec approvals on the node allow the command you're running.

### Node disconnects frequently

- Ensure the node machine doesn't sleep (macOS: System Settings → Energy → Prevent automatic sleeping)
- Check Tailscale stays connected: `tailscale status`
- Check node logs: `~/.openclaw/logs/node.log`
- If on Wi-Fi, prefer ethernet for the node machine

### Commands fail with "command not found" on node

Node `system.run` uses a minimal PATH. Homebrew, nvm, and other tools that modify PATH via shell config won't be available.

**Fix:** Use full binary paths:
```bash
exec host=node command="/opt/homebrew/bin/ollama run llama3"
```

Or fall back to SSH when you need the full shell environment:
```bash
ssh my-node "source ~/.zshrc; ollama run llama3"
```

## Architecture diagram

```
┌─────────────────────────────────────────────┐
│                CLOUD VPS                     │
│                                              │
│  ┌──────────────────────────────────┐       │
│  │     OpenClaw Gateway             │       │
│  │     (bind: lan / 0.0.0.0)       │       │
│  │     port: 18789                  │       │
│  │                                  │       │
│  │  ┌─────────┐  ┌──────────────┐  │       │
│  │  │ Telegram │  │   Discord    │  │       │
│  │  │  Bot     │  │   Bot       │  │       │
│  │  └─────────┘  └──────────────┘  │       │
│  │                                  │       │
│  │  ┌─────────┐  ┌──────────────┐  │       │
│  │  │ Agents  │  │   Models     │  │       │
│  │  │ (main,  │  │   (API)     │  │       │
│  │  │ workers)│  │              │  │       │
│  │  └─────────┘  └──────────────┘  │       │
│  └──────────────────────────────────┘       │
│                    │                         │
│              Tailscale VPN                   │
│           (WireGuard encrypted)              │
└────────────────────┼────────────────────────┘
                     │
                     │  ws:// (safe — encrypted by Tailscale)
                     │
┌────────────────────┼────────────────────────┐
│             LOCAL NODE                       │
│                                              │
│  ┌──────────────────────────────────┐       │
│  │     OpenClaw Node                │       │
│  │     (LaunchAgent / systemd)      │       │
│  │                                  │       │
│  │  exec host=node → system.run    │       │
│  │                                  │       │
│  │  ┌─────────┐  ┌──────────────┐  │       │
│  │  │ Ollama  │  │  Lighthouse  │  │       │
│  │  │ (local  │  │  (browser    │  │       │
│  │  │ models) │  │  automation) │  │       │
│  │  └─────────┘  └──────────────┘  │       │
│  │                                  │       │
│  │  ┌─────────┐  ┌──────────────┐  │       │
│  │  │ Whisper │  │  Playwright  │  │       │
│  │  │ (speech │  │  (headless   │  │       │
│  │  │ to text)│  │  browser)    │  │       │
│  │  └─────────┘  └──────────────┘  │       │
│  └──────────────────────────────────┘       │
│                                              │
│  Also accessible via SSH (file transfer,     │
│  full shell env, fallback)                   │
└──────────────────────────────────────────────┘
```

## Quick reference

| Task | Command |
|---|---|
| Check gateway bind | `openclaw config get gateway.bind` |
| Check node status | `openclaw nodes status` |
| List pending pairings | `openclaw devices list` |
| Approve a node | `openclaw devices approve <id>` |
| Run command on node | `exec host=node command="..."` |
| Check Tailscale | `tailscale status` |
| Restart gateway | `openclaw gateway restart` |
| Node logs | `~/.openclaw/logs/node.log` |

## Tested with

- OpenClaw 2026.4.x
- Tailscale 1.x
- macOS 15 (Sequoia) + Ubuntu 24.04 VPS
- Mac Mini M4 as node, Hostinger VPS as gateway

Should work with any VPS provider and any local machine that can run OpenClaw + Tailscale.

## License

MIT
