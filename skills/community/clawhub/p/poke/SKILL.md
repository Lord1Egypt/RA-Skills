---
name: poke
description: Send SMS/iMessage to the user via Poke and process inbound Poke events. Use when the user asks to be texted, for SMS-based alerts, when processing events forwarded from Poke, or when helping a user set up external webhook triggers that route through Poke.
---

# Poke Bridge — OpenClaw Skill

Poke is the user's personal AI assistant on their phone (SMS/iMessage). OpenClaw agents connect to Poke for two-way communication and event routing.

## Architecture

```
User ←→ Poke (phone) ←→ Tunnel (relay) ←→ MCP Server ←→ OpenClaw (agent)
                                                ↑
External services (GitHub, Vercel, etc.) → webhooks → Poke → OpenClaw
```

**Poke owns:** triggers, schedules, condition monitoring, timing, user-facing UI
**OpenClaw owns:** execution — acting on events, running code, deploying, responding

Do NOT create OpenClaw cron jobs for things Poke can handle. Poke fires, you execute.

## Onboarding (Step by Step)

Follow these steps in order. Each step depends on the previous one.

### Step 1: Install openclaw-poke

```bash
npm install -g openclaw-poke
```

### Step 2: Run interactive setup

```bash
npx openclaw-poke setup
```

This auto-discovers your OpenClaw config and:
- Detects gateway port, auth tokens, hooks URL from `openclaw.json`
- Authenticates with Poke (runs `poke login` if needed)
- Prompts for Poke API key (or uses OAuth)
- Writes plugin config into `openclaw.json`
- Creates + starts systemd service for MCP server on :3210
- Installs agent skill
- Verifies the handshake

### Step 3: Authenticate with Poke

If not already logged in, setup will trigger `poke login`:

1. A **login code** appears in the terminal (e.g. `Q8CUQBXE`)
2. Open the URL: `https://poke.com/device?code=YOUR_CODE`
3. Enter the code and approve

**Important:** The login URL is `https://poke.com/device` — NOT `device.poke.com`.

### Step 4: Start the tunnel

The tunnel connects your local MCP server to Poke through an authenticated relay. No ports exposed, no public URLs, zero attack surface.

```bash
poke tunnel http://localhost:3210/mcp --name "OpenClaw"
```

The tunnel auto-registers with Poke — tools sync automatically.

**Make it persistent with systemd:**

```bash
cat > ~/.config/systemd/user/openclaw-poke-tunnel.service << 'EOF'
[Unit]
Description=OpenClaw Poke Tunnel
After=openclaw-poke-mcp.service
Requires=openclaw-poke-mcp.service

[Service]
Type=simple
ExecStart=/usr/local/bin/poke tunnel http://localhost:3210/mcp --name "OpenClaw"
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now openclaw-poke-tunnel
```

Adjust the `ExecStart` path to wherever `poke` is installed (`which poke`).

### Step 5: Verify

```bash
# Check MCP server health
curl -s http://localhost:3210/health

# Check tunnel status
systemctl --user status openclaw-poke-tunnel

# Send a test message
npx openclaw-poke test
```

### Known SDK Bug (poke ≤ 0.4.2)

`poke tunnel` may fail with "Server did not return a valid connection ID or tunnel URL." This is a Poke SDK bug — the API returns `serverUrl: null` for tunnel connections, but the SDK checks for it.

**Fix:** Patch the CLI binary:
```bash
# Find the error string and fix the check
POKE_BIN=$(which poke)
sed -i 's/this\.tunnelUrl=r\.serverUrl,!this\.connectionId||!this\.tunnelUrl/this.tunnelUrl=r.serverUrl||("https:\/\/tunnel.poke.com\/"+r.id),!this.connectionId/' "$POKE_BIN"
```

Also patch the library (variable name may differ — `r` vs `s`):
```bash
# Patch node_modules too (for programmatic usage)
SDK_DIR=$(node -e "console.log(require.resolve('poke').replace('/dist/index.mjs',''))")
sed -i 's/this\.tunnelUrl=s\.serverUrl,!this\.connectionId||!this\.tunnelUrl/this.tunnelUrl=s.serverUrl||("https:\/\/tunnel.poke.com\/"+s.id),!this.connectionId/' "$SDK_DIR/dist/index.mjs"
sed -i 's/this\.tunnelUrl=s\.serverUrl,!this\.connectionId||!this\.tunnelUrl/this.tunnelUrl=s.serverUrl||("https:\/\/tunnel.poke.com\/"+s.id),!this.connectionId/' "$SDK_DIR/dist/index.cjs"
```

### Alternative: Manual registration (no tunnel)

Only use this if you already have a publicly reachable URL (VPS, Tailscale Funnel, ngrok). Less secure — anyone with the URL can reach the endpoint.

```bash
# 1. Expose the MCP server port publicly
tailscale funnel localhost:3210 /poke

# 2. Register with Poke
poke mcp add https://myhost.example.com/poke/mcp --name "OpenClaw"
```

## What Gets Configured

| Component | Value | Source |
|-----------|-------|--------|
| MCP endpoint | `http://localhost:3210/mcp` | MCP server |
| Hooks URL | `http://localhost:{port}/hooks/agent` | Auto-detected from gateway config |
| Hooks token | Bearer token | Auto-detected from `openclaw.json` |
| Poke API key | JWT | User provides or OAuth |
| Gateway port | 18789 (default) | Auto-detected |

## Sending Messages (OpenClaw → User)

Use the `poke_send` tool. It sends SMS/iMessage through Poke to the user's phone.

### When to Use Poke vs Chat Channel

| Scenario | Use |
|----------|-----|
| Normal conversation | Telegram/WhatsApp (default channel) |
| User explicitly says "text me" | Poke |
| Critical alert (deploy failure, outage) | Poke (SMS gets through) |
| Proactive daily briefing | Chat channel (less intrusive) |
| Responding to a Poke-sourced request | Poke (respond where request came from) |

## Handling Inbound Events (Poke → OpenClaw)

**ALL messages from Poke arrive prefixed with `[Poke→OpenClaw]`.** This is how you identify the source.

### Critical Rule: Route Responses Back to Poke

When you see `[Poke→OpenClaw]` in a hook/system message:
1. **The request came from Poke**, not from the user's chat channel
2. **Respond via `poke_send`**, NOT in the current chat session
3. **Never dump Poke responses into Telegram/WhatsApp** — Poke asked, Poke gets the answer

### Critical Rule: Tell Poke to Target Your Main Session

When sending instructions to Poke, **always tell Poke to use session targeting**:
- Poke should call `list_sessions` to discover active sessions and their keys
- Then use `send_to_agent` with `session_key` set to your main session (`kind: "direct"`, ends with `:main`)
- Discover the key via `list_sessions` — don't hardcode it
- Without `session_key`, messages land in a throwaway hook session with NO context

### Inbound Event Format

```
System: [timestamp] Hook Hook: [Poke→OpenClaw] <message content>
```

## Webhook Triggers (Post-Setup)

After the handshake is established, wire up external services to route through Poke.

### Creating Triggers

```bash
# Via tool
poke_webhook(condition="when a Vercel deploy fails")

# Via CLI
npx openclaw-poke webhook "when a Vercel deploy fails"
```

Or text Poke directly: "Create a trigger: when GitHub Actions fails, send details to my OpenClaw agent"

### Common Patterns

- **GitHub CI failures** → `workflow_run` events
- **Vercel deploy errors** → deployment events
- **Stripe payment failures** → `payment_intent.payment_failed`
- **Uptime monitoring** → webhook on downtime
- **Calendar events** → Google Calendar push notifications

## Available Tools

| Tool | Purpose |
|------|---------|
| `poke_send` | Send SMS/iMessage to user |
| `poke_sessions` | List active OpenClaw sessions |
| `poke_session_send` | Send message to specific session |
| `poke_webhook` | Create Poke trigger/webhook |

## MCP Server Tools (exposed to Poke)

| Tool | Purpose |
|------|---------|
| `send_to_agent` | Send message to OpenClaw (with session targeting) |
| `list_sessions` | List active OpenClaw sessions and their keys |
| `check_agent_status` | Health check |
| `create_reminder` | Set a reminder via OpenClaw |
| `send_media` | Send media to agent |
| `get_logs` | Get recent agent logs |
| `read_file` | Read a file from agent workspace |
| `create_trigger` | Create a trigger on OpenClaw side |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Missing Poke API key" | Run `npx openclaw-poke setup` or set `POKE_API_KEY` |
| "Server did not return a valid connection ID" | Poke SDK bug — apply the sed patch above |
| Tunnel won't start | Check `poke whoami` — may need `poke login` |
| Login URL not found | URL is `https://poke.com/device?code=CODE` (not device.poke.com) |
| Message not delivered | Check Poke app, verify phone number |
| Agent responds in wrong channel | Check for `[Poke→OpenClaw]` prefix; respond via `poke_send` |
| Poke responses land in wrong session | Poke isn't using session targeting; remind it to call `list_sessions` |
| Tools show 0 after registration | Normal; tools sync on first use |
| "clearhistory" | If Poke calls wrong MCP after renaming, text "clearhistory" to Poke |
| Tunnel disconnects | systemd auto-restarts; check `journalctl --user -u openclaw-poke-tunnel` |
