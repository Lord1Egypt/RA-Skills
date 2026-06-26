---
name: pixel-agents
description: Install, configure, and manage the Pixel Agents Dashboard — a real-time pixel art ops dashboard for OpenClaw deployments. Use when the user wants to set up, start, stop, configure, or troubleshoot the pixel agents dashboard. Handles auto-discovery of local agents, gateway connection, config generation, and service management.
---

# Pixel Agents Dashboard

Real-time pixel art ops dashboard that visualizes OpenClaw agent activity as character sprites in a shared office.

## Setup (First Time)

Run the auto-config script to discover agents and generate config:

```bash
bash scripts/setup.sh
```

This will:
1. Find your OpenClaw agents directory (`~/.openclaw/agents/`)
2. Detect the gateway URL and port
3. Discover all configured agents
4. Generate `dashboard.config.json`
5. Install dependencies and build

If agents or gateway can't be auto-discovered, the script generates a config from defaults and the setup wizard handles the rest.

## Start / Stop

```bash
# Start the dashboard
cd <project-dir> && npm start

# Or if installed globally
pixel-agents
```

Default port: 5070. Override with `PIXEL_AGENTS_PORT` env var.

## Configuration

Config file: `dashboard.config.json` (in project root or `~/.config/pixel-agents/`)

Key settings:
- `gateway.url` — OpenClaw gateway (default: `http://localhost:18789`)
- `gateway.token` — Use `${OPENCLAW_GATEWAY_TOKEN}` for env var
- `agents[]` — Array of `{id, name, emoji, palette, alwaysPresent}`
- `features` — Toggle components: serverRack, breakerPanel, hamRadio, fireAlarm, etc.

See `dashboard.config.example.json` for full reference.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port in use | Set `PIXEL_AGENTS_PORT=5071` or change `server.port` in config |
| No agents found | Check `openclaw.agentsDir` points to correct path |
| Gateway unreachable | Verify gateway is running: `curl http://localhost:18789/v1/models` |
| Sprites missing | Run `npm run build` — assets are in `public/assets/` |
