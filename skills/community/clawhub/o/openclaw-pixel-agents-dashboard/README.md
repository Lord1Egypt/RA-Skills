# Pixel Agents Dashboard

A pixel-art ops dashboard for [OpenClaw](https://openclaw.ai) deployments. Watch your AI agents work in real-time — each agent appears as a character sprite in a shared office, with live activity bubbles, tool usage indicators, and conversation previews.

![Screenshot](public/Screenshot.jpg)

## Features

- **Live agent activity** — Characters move, idle, and show speech bubbles based on real-time JSONL session parsing
- **Spawn agents** — Click `+ Agent` to spawn sub-agents (like research assistants or quick coders) with a mini-chat panel
- **Hardware monitor** — Server rack shows CPU, GPU, RAM, disk, and network stats
- **Service controls** — Breaker panel to start/stop/restart OpenClaw gateway services
- **Update checker** — Ham radio checks for OpenClaw updates
- **Day/night cycle** — Ambient lighting matches your local time
- **Conversation heat** — Agents glow based on recent activity
- **Touch/mobile support** — Pan, zoom, and tap on mobile devices

## Quick Start

### Option A: npm (recommended)

```bash
npm install -g openclaw-pixel-agents-dashboard
pixel-agents
```

### Option B: Clone from source

```bash
git clone https://github.com/jaffer1979/openclaw-pixel-agents-dashboard.git
cd openclaw-pixel-agents-dashboard
npm install
npm run build
npm start
```

### Set up via the wizard

Open `http://localhost:5070` — the **setup wizard** walks you through everything:
- Discovers your OpenClaw agents automatically
- Configures your gateway connection
- Lets you pick which features to enable
- Generates your config file — you're done!

> **Power users:** If you prefer manual config, copy `dashboard.config.example.json` to `dashboard.config.json` and edit it before starting. The wizard only runs when no config file is present. See [Configuration](#configuration) below for details.

### Development

```bash
npm run dev
```

Runs Vite dev server on port 5061 with hot reload. API requests proxy to the backend on your configured port.

## Configuration

The dashboard reads `dashboard.config.json` from:

1. Path in `PIXEL_AGENTS_CONFIG` environment variable
2. Current working directory (`./dashboard.config.json`)
3. `~/.config/pixel-agents/dashboard.config.json`

### Environment Variable Expansion

Use `${ENV_VAR}` in any string value to read from environment variables. This keeps secrets out of your config file:

```json
{
  "gateway": {
    "token": "${OPENCLAW_GATEWAY_TOKEN}"
  }
}
```

### Path Expansion

Use `~` as a shorthand for your home directory:

```json
{
  "openclaw": {
    "agentsDir": "~/.openclaw/agents"
  }
}
```

### Agent Configuration

Each agent needs:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Agent directory name (matches `~/.openclaw/agents/<id>/`) |
| `name` | string | Display name shown above the character |
| `emoji` | string | Emoji identifier |
| `palette` | number | Character skin (0-5, each is a different sprite) |
| `alwaysPresent` | boolean | `true` = always on map; `false` = appears only when active |

### Feature Toggles

Every interactive feature can be turned on/off:

| Feature | Default | Description |
|---------|---------|-------------|
| `fireAlarm` | true | Gateway restart controls |
| `breakerPanel` | true | Service start/stop/restart |
| `hamRadio` | true | OpenClaw update checker |
| `serverRack` | true | Hardware stats monitor |
| `nickDesk` | false | Decorative desk (Station House-specific) |
| `dayNightCycle` | true | Ambient lighting based on local time |
| `conversationHeat` | true | Activity glow on agents |
| `channelBadges` | true | Telegram/Discord icons on agent names |
| `sounds` | true | UI sound effects |
| `door` | true | Animated door for agent spawn/despawn |

### Remote Agents

If you have agents running on remote machines, add them to `remoteAgents`:

```json
{
  "remoteAgents": [
    {
      "id": "remote-agent",
      "host": "192.168.1.100",
      "user": "openclaw",
      "password": "${REMOTE_SSH_PASS}",
      "agentsDir": "/home/openclaw/.openclaw/agents"
    }
  ]
}
```

Remote agents are synced via SSH (rsync). Requires `sshpass` for password auth. SSH key auth is also supported via `keyPath`.

## Architecture

```
┌─────────────────┐     WebSocket      ┌──────────────────┐
│  React/Canvas    │◄──────────────────►│  Express Server  │
│  (browser)       │                    │  (Node.js)       │
└─────────────────┘                    └────────┬─────────┘
                                                │
                                    ┌───────────┴───────────┐
                                    │                       │
                              JSONL Watcher          Gateway API
                              (file tailing)         (/tools/invoke)
                                    │                       │
                              ┌─────┴─────┐          ┌─────┴─────┐
                              │ Agent     │          │ OpenClaw  │
                              │ Sessions  │          │ Gateway   │
                              └───────────┘          └───────────┘
```

- **Backend** tails JSONL session files and broadcasts parsed events via WebSocket
- **Frontend** renders a pixel-art canvas with agent sprites, UI overlays, and interactive controls
- **Spawner** uses the gateway's `/tools/invoke` API to create sub-agent sessions

## Sprite Assets

Character sprites, wall tiles, and floor tiles are from the [JIK-A-4 Metro City](https://github.com/pdlucca/pixel-agents) pack by Pablo De Lucca, licensed under MIT. See `public/assets/ASSET-LICENSE.md`.

## License

MIT
