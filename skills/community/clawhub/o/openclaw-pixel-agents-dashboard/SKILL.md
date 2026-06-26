---
name: pixel-agents
description: Real-time pixel art ops dashboard for OpenClaw deployments. Visualizes agent activity as character sprites in a shared office with live activity bubbles, hardware monitoring, service controls, and task spawning.
---

# Pixel Agents Dashboard

Real-time pixel art ops dashboard that visualizes OpenClaw agent activity as character sprites in a shared office.

## Setup (First Time)

```bash
npm install
bash skill/scripts/setup.sh
npm run build
npm start
```

The setup script auto-discovers your agents, detects your gateway, and generates the config.

Or just run `npm start` — if no config exists, the setup wizard opens in your browser.

## Configuration

See `dashboard.config.example.json` for all options:

| Field | Description |
|-------|-------------|
| `server.port` | Dashboard port (default: 5070) |
| `gateway.url` | OpenClaw gateway URL |
| `gateway.token` | Gateway auth token (use `${ENV_VAR}`) |
| `agents[]` | Agent definitions (id, name, emoji, palette) |
| `features.*` | Toggle interactive elements on/off |
| `remoteAgents[]` | SSH targets for remote agent monitoring |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Port in use | Change `server.port` or set `PIXEL_AGENTS_PORT` env var |
| No agents shown | Check `openclaw.agentsDir` path |
| Gateway errors | Verify `gateway.url` and `gateway.token` |
