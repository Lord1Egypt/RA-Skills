# Minecraft Bridge API Specification

Base URL: `http://localhost:${MC_BRIDGE_PORT:-3001}`
Content-Type: `application/json`
Authentication: none (intended only for localhost on `127.0.0.1`)

---

## Response Format

### Success
```json
{"success": true, "...": "data"}
```

### Failure
```json
{"success": false, "error": "message"}
```

### Bot Offline (503)
```json
{"error": "Bot not connected", "hint": "Open Minecraft and check MC_HOST/MC_PORT"}
```

---

## GET /status

Check bridge health and bot connection state. This is the only endpoint that is expected to respond even when the bot is offline.

### Response fields

| Field | Type | Meaning |
|---|---|---|
| connected | boolean | Whether the bot is connected |
| username | string | Bot username |
| position | `{x,y,z}` or null | Current position |
| health | number or null | Health (0–20) |
| food | number or null | Hunger (0–20) |
| saturation | number or null | Food saturation |
| gameTime | number or null | In-game time (0–24000) |
| isDay | boolean | Convenience day/night flag |
| inventoryCount | number | Count of non-empty inventory stacks |
| currentAction | string or null | Current action |
| bridgeVersion | string | Bridge version |

---

## GET /inventory

Return all carried items.

Example:
```json
{
  "success": true,
  "items": [
    {
      "name": "iron_ore",
      "displayName": "Iron Ore",
      "count": 24,
      "slot": 36,
      "durability": null
    }
  ],
  "totalStacks": 3
}
```

---

## GET /position

Return position and facing.

Example:
```json
{
  "success": true,
  "x": -142,
  "y": 64,
  "z": 88,
  "yaw": 1.57,
  "pitch": 0.0
}
```

---

## GET /health

Return health and hunger state.

Example:
```json
{
  "success": true,
  "health": 18.0,
  "food": 14,
  "saturation": 5.0,
  "isDead": false
}
```

---

## GET /nearby?radius=16

Return nearby entities.

Parameters:
- `radius`: detection radius in blocks, default 16, practical upper bound ~32

Example:
```json
{
  "success": true,
  "entities": [
    {
      "name": "Zombie",
      "type": "mob",
      "distance": 8,
      "position": {"x": -150, "y": 64, "z": 88}
    }
  ],
  "radius": 16
}
```

---

## POST /chat

Send an in-game chat message.

Request:
```json
{"message": "Hello world!"}
```

Response:
```json
{"success": true, "sent": "Hello world!"}
```

---

## POST /command

Send a slash command through the bot.

Request:
```json
{"command": "give ClawBot diamond 64"}
```

Notes:
- Leading `/` is optional
- This is potentially high risk if the bot has elevated permissions
- Prefer `minecraft-server-admin` for server-administration tasks

---

## POST /move

Pathfind to target coordinates.

Request:
```json
{"x": -100, "y": 64, "z": 200}
```

If `y` is omitted, the bridge uses an XZ goal and lets the pathfinder determine height.

Success example:
```json
{"success": true, "arrived": {"x": -100, "y": 64, "z": 200}}
```

Failure example:
```json
{"success": false, "error": "No path found"}
```

---

## POST /mine

Mine the nearest matching block(s).

Request:
```json
{"blockName": "iron_ore", "count": 5}
```

Response:
```json
{"success": true, "blockName": "iron_ore", "requested": 5, "mined": 4}
```

`mined` may be lower than `requested` if there are not enough matching blocks nearby.

---

## POST /collect

Collect dropped ground items.

Request:
```json
{"itemName": "iron_ingot", "count": 10}
```

---

## POST /craft

Craft an item, using a nearby crafting table when required.

Request:
```json
{"itemName": "iron_pickaxe", "count": 1}
```

Common failure reasons:
- no valid recipe
- missing crafting table
- missing materials

---

## POST /follow

Follow a player continuously until `/stop`.

Request:
```json
{"playerName": "Steve"}
```

---

## POST /stop

Cancel the current movement/mining/follow action.

Response:
```json
{"success": true, "stopped": true}
```

---

## Common `blockName` Values

| Block | `blockName` |
|---|---|
| Stone | `stone` |
| Cobblestone | `cobblestone` |
| Dirt | `dirt` |
| Sand | `sand` |
| Gravel | `gravel` |
| Oak Log | `oak_log` |
| Coal Ore | `coal_ore` |
| Iron Ore | `iron_ore` |
| Gold Ore | `gold_ore` |
| Diamond Ore | `diamond_ore` |
| Deepslate Diamond Ore | `deepslate_diamond_ore` |
| Redstone Ore | `redstone_ore` |
| Crafting Table | `crafting_table` |
| Furnace | `furnace` |
| Chest | `chest` |
