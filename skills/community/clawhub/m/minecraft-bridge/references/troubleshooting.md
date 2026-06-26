# Minecraft Bridge Troubleshooting

## Quick Diagnosis

```text
1. curl http://localhost:3001/status
   ├─ ECONNREFUSED         -> service not running
   ├─ {"connected":false} -> bridge up, bot offline
   ├─ {"connected":true}  -> bridge connected; investigate the action itself
   └─ other errors         -> inspect logs and config
```

---

## A. Service Not Running (ECONNREFUSED)

Checks:
1. Verify Node.js is installed (`node --version`, ideally v18+)
2. Verify dependencies are installed
3. Start the bridge manually and watch output
4. Check whether the port is already occupied

Example:

```bash
MC_HOST=localhost MC_PORT=25565 node ~/.openclaw/skills/minecraft-bridge/bridge-server.js
lsof -i :3001
```

---

## B. Bridge Running, Bot Offline

Common causes:

### Minecraft is not running
Open Minecraft Java Edition and enter the target world/server.

### Wrong port (very common in singleplayer LAN)
When you use "Open to LAN", the port is random each time.
Update `MC_PORT` to the actual LAN port.

### Version mismatch
Make sure `MC_VERSION` matches the actual game/server version.

### Username collision
If another player already uses the same bot username, change `MC_BOT_USERNAME`.

### Auth mismatch
Public/authenticated servers may require Microsoft auth rather than offline mode.
Set `MC_AUTH=microsoft` when appropriate.

---

## C. Action Execution Fails

### `/move` -> `No path found`
- target is sealed off
- destination is too far for a reliable single pathing run
- use intermediate waypoints

### `/mine` -> mined < requested
- there are not enough matching blocks nearby
- move closer to the target area first

### `/craft` -> no recipe / missing crafting table
- required workbench not nearby
- recipe unavailable or materials missing

### bot appears stuck
1. send `POST /stop`
2. inspect `GET /status` and `currentAction`
3. restart the bridge if necessary

---

## D. Other Common Problems

### Dependency version mismatch
Reinstall dependencies cleanly if Mineflayer packages are out of sync.

### Firewall / exposure concern
The bridge is intended to listen only on `127.0.0.1`.
Do not expose it publicly.

### High memory usage
Mineflayer can use more memory when many chunks are loaded.
Lower view distance or reduce movement scope if needed.

---

## Useful Log Signals

Typical messages:

```text
[bridge] Bot online @ {"x":-142,"y":64,"z":88}
[bridge] Bot error: read ECONNRESET
[bridge] Bot disconnected (...), retrying...
[bridge] POST /move error: ...
```

For deeper debugging:

```bash
DEBUG=mineflayer:* node bridge-server.js
```
