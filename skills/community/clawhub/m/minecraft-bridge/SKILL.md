---
name: minecraft-bridge
description: >
  Local HTTP bridge for Mineflayer-based live control of a Minecraft Java bot.
  Trigger when the user wants to connect a bot to their world, check bot
  status/inventory/position, or make the bot move, mine, craft, follow, or chat
  in-game. Examples: 'connect to my world', 'start the minecraft bot', 'what is in
  my inventory', 'go mine iron', 'craft a pickaxe', 'follow me', 'is minecraft bridge
  running'. Also use when another minecraft-* skill needs live game data. Do NOT
  trigger for Minecraft knowledge questions (use minecraft-wiki), server
  administration via RCON or server.properties (use minecraft-server-admin), or
  casual Minecraft mentions without a live-action request.
metadata:
  openclaw:
    emoji: "🎮"
    requires:
      bins:
        - node
      env:
        - MC_HOST
        - MC_PORT
        - MC_BOT_USERNAME
    install:
      - id: mineflayer
        kind: node
        package: mineflayer
        label: "Mineflayer — Minecraft bot API"
      - id: mineflayer-pathfinder
        kind: node
        package: mineflayer-pathfinder
        label: "Pathfinder — navigation plugin"
      - id: vec3
        kind: node
        package: vec3
        label: "Vec3 — 3D coordinate helper"
    homepage: https://github.com/en1r0py1865/minecraft-skill
---

# Minecraft Bridge

Persistent local HTTP service that bridges OpenClaw to a live Minecraft Java Edition
bot session. Exposes a REST API on `http://localhost:${MC_BRIDGE_PORT|3001}` for live
state reads and in-game bot actions.

**Boundary**:
- Use this skill for **live bot control** and **live game-state reads**
- Use `minecraft-wiki` for knowledge questions
- Use `minecraft-server-admin` for RCON, server.properties, whitelist/ban/op, and generic server administration

## Quick State Machine

```
UNSTARTED → run bridge-server.js → STARTING → bot spawns → CONNECTED
CONNECTED → game closes or kick → DISCONNECTED → auto-reconnect → CONNECTED
```

Check current state with: `GET http://localhost:3001/status`

---

## Setup (first time)

### 1. Environment variables
Set in `~/.openclaw/openclaw.json` or export in shell:
```
MC_HOST=localhost          # server IP (localhost for singleplayer LAN)
MC_PORT=25565              # game port
MC_BOT_USERNAME=ClawBot    # bot's in-game name (offline-mode servers)
MC_BRIDGE_PORT=3001        # bridge HTTP port (default 3001)
MC_VERSION=1.21.1          # Minecraft version string
```

### 2. Open Minecraft to LAN (singleplayer)
`ESC → Open to LAN → Allow Cheats ON → Start LAN World`
Note the port shown (e.g. 54321) — set `MC_PORT` to that value.

### 3. Start the bridge
```bash
node ~/.openclaw/skills/minecraft-bridge/bridge-server.js
```
Wait for: `🎮 Bridge ready at http://localhost:3001`

### 4. Verify
```bash
curl http://localhost:3001/status
```

---

## Runtime Operations

When user gives a live-game command:

1. **Check bridge health** — `GET /status`; if unreachable → show setup instructions above
2. **Execute action** — call appropriate endpoint (see API Reference below)
3. **Report result** — format response conversationally; include coordinates, item names, counts
4. **Persist context** — write significant events to OpenClaw memory (coordinates found, items collected, goals achieved)

### Interpreting /status response
```json
{
  "connected": true,
  "username": "ClawBot",
  "position": {"x": -142, "y": 64, "z": 88},
  "health": 18.0,
  "food": 14,
  "gameTime": 6000,
  "inventoryCount": 12,
  "biome": "plains"
}
```
- `gameTime` 0–6000 = morning, 6000–12000 = day, 12000–18000 = dusk/night
- `health` max 20.0; below 6 = danger
- `food` max 20; below 6 = can't sprint, below 1 = taking damage

---

## API Overview

See `references/api-spec.md` for the full schema.

Core endpoints:
- `GET /status` — bridge + bot connection state
- `GET /inventory`, `GET /position`, `GET /nearby` — live state reads
- `POST /move`, `POST /mine`, `POST /collect`, `POST /craft`, `POST /follow`, `POST /stop` — live bot actions
- `POST /chat` — send in-game chat
- `POST /command` — send arbitrary slash commands; use with caution

> **Security note**: `/command` forwards arbitrary slash commands. On servers where the bot has elevated permissions, this may include destructive or admin-level commands. Prefer `minecraft-server-admin` for server administration tasks.

---

## Dependent Skills

Dependent skills should health-check the bridge before using it.
See `references/dependency-guide.md` for the canonical dependency-check pattern and degradation behavior.

---

## Error Handling

| Error | Cause | Recovery |
|-------|-------|---------|
| `ECONNREFUSED` | Bridge not started | Run `node bridge-server.js` |
| `{"connected":false}` | Bridge up, bot offline | Open Minecraft, check MC_HOST/PORT |
| `{"error":"pathfinding failed"}` | Path blocked | Try `/stop` then retry with different coords |
| `{"error":"no crafting table"}` | Craft without workbench | Move near crafting table first |
| Bot stuck looping | Pathfinding bug | POST /stop, then resume |

Auto-reconnect is built in — bridge retries every 5 s after disconnect.

---

## Additional Resources
- `references/api-spec.md` — Full API schema with all request/response fields
- `references/dependency-guide.md` — How other skills should declare bridge dependency
- `references/troubleshooting.md` — Detailed error diagnosis
- `scripts/start.sh` / `scripts/stop.sh` — Convenience wrappers
