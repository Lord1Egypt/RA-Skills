# Intiface Direct — Buttplug v4 Device Control

Control 750+ BLE intimate devices directly through Intiface Central.
No MCP bridges, no extra dependencies beyond Node.js.

## What you need
1. **Intiface Central** — free app from https://intiface.com/central/
2. **Node.js** — bundled with OpenClaw
3. **A BLE toy** — 700+ brands supported (Lovense, Satisfyer, Kiiroo, We-Vibe, etc.)

## Quick Start
```bash
# Install dependencies
npm install

# List devices
node connector.cjs list

# Single vibration
node connector.cjs vibrate 0 0 50

# Continuous vibration (resends every 3s — no timeout!)
node connector.cjs loop 0 0 50

# Stop
node connector.cjs stop 0
```

## CLI Commands
| Command | Description |
|---------|-------------|
| `list` | Show connected devices |
| `vibrate <d> <f> <v>` | Single vibration burst (exits after) |
| `loop <d> <f> <v> [sec]` | Continuous vibe, resends every `sec` seconds (default 3) |
| `stop <d>` | Stop device |

## Strength Guide (0–100)
- Gentle: 10–25
- Medium: 30–50
- Strong: 55–75
- Maximum: 80–100

## Custom Patterns
See the "Creating Custom Patterns" section in `SKILL.md` for building ramps, waves, pulses, and fade-outs with temporary Node.js scripts. The `ws` library is already available in `node_modules/`.

## Environment
- `INTIFACE_WS_URL` — WebSocket URL (default: `ws://localhost:12345`)
- Use a LAN IP like `ws://192.168.0.13:12345` for remote control
