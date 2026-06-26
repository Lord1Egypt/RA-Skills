---
name: minecraft-server-admin
description: >
  Execute Minecraft Java Edition admin commands through the RCON remote console.
  Use for player moderation, whitelist management, item/state commands, world rules,
  broadcast messages, and recent log review on servers you control. Covers in-game
  command administration only. Does NOT handle full server lifecycle, filesystem
  backups, or plugin installation/update workflows; use a dedicated server-ops skill
  for those. Requires RCON enabled on the target server and is not for singleplayer worlds.
metadata:
  openclaw:
    emoji: "🖥️"
    requires:
      bins:
        - node
      env:
        - MC_RCON_HOST
        - MC_RCON_PORT
        - MC_RCON_PASSWORD
    install:
      - id: rcon-dep
        kind: node
        package: rcon-client
        label: "rcon-client — Minecraft RCON protocol"
    homepage: https://github.com/en1r0py1865/minecraft-skill
---

# Minecraft Server Admin

**Scope**: This skill is your **in-game remote control** for a Minecraft Java server.
It sends commands through the RCON protocol to manage players, world state, and
server communication in real time. It intentionally excludes server-infrastructure
operations such as process lifecycle management, filesystem backups, plugin jar
installation, and continuous uptime monitoring; use a dedicated PaperMC ops skill
for those. This skill does NOT require minecraft-bridge — it communicates directly
with the server's admin console over a separate TCP connection.

**Architecture**:
```
OpenClaw → RCON TCP (port 25575) → Minecraft Server Console
```

---

## Prerequisites

### Enable RCON on the Server

Edit `server.properties`:
```properties
enable-rcon=true
rcon.port=25575
rcon.password=STRONG_PASSWORD_HERE
broadcast-rcon-to-ops=false
```
Restart server after changing these values.

### Environment Variables

```
MC_RCON_HOST=localhost        # Server IP or hostname
MC_RCON_PORT=25575            # RCON port (must match server.properties)
MC_RCON_PASSWORD=yourpassword # RCON password (must match server.properties)
MC_SERVER_LOG=/path/to/server/logs/latest.log  # optional, for log analysis
```

### Verify Connection

```bash
node ~/.openclaw/skills/minecraft-server-admin/scripts/rcon.js "list"
# Expected: "There are N of a max of M players online: ..."
```

---

## Operation Categories

### PLAYER MANAGEMENT
For any player-related command, use: `scripts/rcon.js "<command>"`

**Listing & Checking**
- "who is online" → `/list` → parse player count and names
- "is [player] online" → `/list` then check if name appears

**Access Control** ⚠️ Requires confirmation before executing:
- kick: `/kick <player> [reason]`
- temp ban: `/ban <player> [reason]` + calendar note
- permanent ban: `/ban <player> [reason]`
- ban IP: `/ban-ip <player|ip> [reason]`
- unban: `/pardon <player>` or `/pardon-ip <ip>`
- whitelist add: `/whitelist add <player>`
- whitelist remove: `/whitelist remove <player>`
- op player: `/op <player>` ⚠️ HIGH PRIVILEGE — always confirm
- deop player: `/deop <player>`

**Item & State Management**
- give items: `/give <player> <item_id> [count]`
- clear inventory: `/clear <player> [item] [count]`
- set gamemode: `/gamemode <survival|creative|adventure|spectator> <player>`
- teleport: `/tp <player> <x> <y> <z>` or `/tp <player> <target_player>`
- set health/hunger: `/effect give <player> minecraft:regeneration ...`
- heal player: `/effect give <player> minecraft:instant_health 1 10`

### WORLD MANAGEMENT

**Time & Weather**
- day: `/time set day`
- night: `/time set midnight`  
- sunrise: `/time set 0`
- clear weather: `/weather clear [seconds]`
- rain: `/weather rain [seconds]`
- thunder: `/weather thunder [seconds]`

**World State**
- save world: `/save-all` (always do before maintenance)
- save-off (for backup): `/save-off` then backup then `/save-on`
- change difficulty: `/difficulty <peaceful|easy|normal|hard>`
- set game rule: `/gamerule <rule> <value>`
  - Examples: `keepInventory true`, `doDaylightCycle false`, `doFireTick false`
- find structure: `/locate structure minecraft:<structure_name>`
- fill area: `/fill <x1 y1 z1> <x2 y2 z2> <block>` ⚠️ Confirm range before running

**Entity Management**
- kill all mobs: `/kill @e[type=!player]` ⚠️ Confirm — kills all non-players
- kill specific type: `/kill @e[type=minecraft:zombie]`
- remove dropped items: `/kill @e[type=minecraft:item]`

### BROADCAST & COMMUNICATION

- server message: `/say <message>` (prefixed with [Server])
- title on screen: `/title @a title {"text":"<msg>","color":"gold","bold":true}`
- subtitle: `/title @a subtitle {"text":"<msg>"}`
- private message: `/msg <player> <message>`
- actionbar: `/title @a actionbar {"text":"<msg>"}`

### PERFORMANCE MONITORING

When asked about server performance:
1. Execute `/list` → check player count
2. Read `MC_SERVER_LOG` file (last 200 lines) if path set
3. Look for patterns in `references/log-patterns.md`
4. Report: TPS warnings, error frequency, player activity spikes

---

## Safety Protocols

**Confirmation required** for all destructive/high-privilege commands:

```
⚠️  Dangerous Operation
Command: /ban SomePlayer griefing and harassment
Server:  ${MC_RCON_HOST}:${MC_RCON_PORT}
Effect:  Permanently bans SomePlayer from server

Type 'confirm' to proceed, or 'cancel' to abort.
```

Operations requiring confirmation:
- `ban`, `ban-ip` — permanent account restriction
- `op` — grants admin privileges
- `fill` — large area modification
- `kill @e` — entity mass-removal
- `stop` — server shutdown
- `save-off` — pauses auto-save (dangerous if forgotten)

**Audit logging**: After each operation, append to OpenClaw Memory:
```
## Server Admin Log [ISO timestamp]
- Command: /ban PlayerX "repeated griefing"
- Executed by: [OpenClaw user]
- Result: success
```

---

## Response Formatting

### Player List (`/list` response)
Parse and present as:
```
👥 Players Online (3/20):
  • Steve — [show coords if available]
  • Alex
  • Notch
```

### Kicked/Banned confirmation
```
✅ Done: PlayerX has been banned
   Reason: griefing
   Effective immediately
   To undo: /pardon PlayerX
```

### Error Responses
- Connection refused → check RCON settings, server running?
- Authentication failure → wrong MC_RCON_PASSWORD
- Command returned empty → server may not have recognized command (check version)

---

## Log Analysis

When user asks about server health or player history:

1. Check `MC_SERVER_LOG` is set and file exists
2. Read the last N lines: `tail -500 <log_file>`
3. Apply patterns from `references/log-patterns.md`
4. Summarize findings:

```
📊 Server Log Summary (last 2 hours)
  Player logins: 14
  Player logouts: 12 (2 still online)
  Errors/Warnings: 3
    - [15:42] Can't keep up! Running 2500ms behind
    - [16:10] Saving chunks for level 'world'
  Suspicious activity: none detected
```

## Additional Resources
- `references/commands.md` — All vanilla commands with syntax and permission level
- `references/log-patterns.md` — Common log patterns and what they mean
- `scripts/rcon.js` — RCON client (used by all commands above)
- `scripts/log-analyzer.js` — Log parsing utilities
