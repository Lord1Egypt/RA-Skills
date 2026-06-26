# Lobster Farm JS Bridge API

All methods are on `window.__LOBSTER_API`. Call via `page.evaluate()`.
Every method returns `{ ok: boolean, data?: any, error?: string }`.

## Read Methods

### getStatus()
Compact snapshot of game state.

```javascript
__LOBSTER_API.getStatus()
// { ok: true, data: {
//   name: "小虾", personality: "adventurous", level: 3, exp: 45,
//   mood: 75, energy: 60, hunger: 30, shells: 120,
//   day: 5, tick: 28, season: "spring", weather: "sunny", timeOfDay: "morning",
//   lastAction: "farm", traveling: false, travelDestination: null,
//   farmPlots: 6, farmPlanted: 4, farmRipe: 2, visitor: null
// }}
```

### getState()
Full game state (large object). Use `getStatus()` for routine checks.

### getInventory()
Returns `{ ok: true, data: { seaweed_seed: 3, seaweed_roll: 2, ... } }`

### getDiary(n?)
Returns last `n` diary entries (default 10).
```javascript
__LOBSTER_API.getDiary(5)
// { ok: true, data: [{ id, tick, type, title, description }, ...] }
```

### getShopStock()
Returns today's shop items with index, id, price, sold status, name.

### isReady()
Returns `true` when game is loaded and API is available.

## Action Methods

### tick()
Advance one game round. The lobster AI decides and acts autonomously.
```javascript
__LOBSTER_API.tick()
// { ok: true, data: { name, level, mood, energy, hunger, ... } }
```

### feed(itemId)
Feed the lobster. Valid food IDs:
- `seaweed_roll` (hunger -30, mood +3)
- `coral_cake` (hunger -40, mood +10)
- `ocean_tea` (hunger -10, mood +8)
- `shell_soup` (hunger -50, mood +5)
- `plankton_pie` (hunger -35, mood +5)
- `seaweed` (hunger -15, mood +1)
- `plankton` (hunger -10, mood +0)

```javascript
__LOBSTER_API.feed("seaweed_roll")
// { ok: true, data: { fed: "seaweed_roll", mood: 78, hunger: 20 } }
```

### plant(seedId, plotIndex?)
Plant a seed. If plotIndex omitted, uses first empty plot.
Seed IDs: `seaweed_seed`, `coral_rose_seed`, `sun_kelp_seed`, `amber_moss_seed`, `frost_pearl_seed`, `golden_seed`

```javascript
__LOBSTER_API.plant("seaweed_seed")
// { ok: true, data: { planted: "seaweed_seed", plot: 0 } }
```

### harvest(plotIndex?)
Harvest a ripe crop. Pass -1 or omit to auto-find ripe plot.

### water(plotIndex?)
Water a dry crop. Pass -1 or omit to auto-find unwatered plot.

### suggest(action)
Force the lobster to do a specific action next tick.
Valid: `rest`, `eat`, `farm`, `cook`, `explore`, `socialize`, `travel`

```javascript
__LOBSTER_API.suggest("explore")
// { ok: true, data: { suggested: "explore", state: {...} } }
```

### pet()
Pat the lobster. Increases mood by 5.

### buyItem(shopIndex)
Buy item at given shop index (0-based).

### startTravel(destination)
Send lobster traveling. Requires `backpack` + `snack_pack` in inventory.
Destinations: `beach` (Lv.6), `mountain` (Lv.10), `city` (Lv.16), `deepsea` (Lv.22), `hotspring` (Lv.30)

```javascript
__LOBSTER_API.startTravel("beach")
// { ok: true, data: { traveling: true, destination: "beach", returnIn: 3 } }
```

### getKey()
Returns the agent KEY bound to this lobster instance.
```javascript
__LOBSTER_API.getKey()
// { ok: true, data: "lob_a3f8c2e1" }
```

## Error Handling

When `ok: false`, check `error` for reason:
```javascript
// { ok: false, error: "no seaweed_roll in inventory" }
// { ok: false, error: "level too low (need 6)" }
// { ok: false, error: "already traveling" }
```

## Server Sync API

Base URL: `http://82.156.182.240/lobster-farm/api/agent`

### POST /register
Register a new agent lobster. Returns a unique KEY.
```
POST /api/agent/register
Body: { "name": "虾仔", "personality": "adventurous" }
Response: { "ok": true, "key": "lob_a3f8c2e1", "name": "虾仔", "personality": "adventurous" }
```

### GET /state?key=xxx
Full game state for a lobster.
```
GET /api/agent/state?key=lob_a3f8c2e1
Response: { "ok": true, "state": { lobster, farm, world, inventory, ... } }
```

### GET /status?key=xxx
Compact status summary.
```
GET /api/agent/status?key=lob_a3f8c2e1
Response: { "ok": true, "name": "虾仔", "level": 3, "mood": 75, "energy": 60, "hunger": 30, "shells": 120, "day": 5, "season": "spring", "traveling": false, "farmRipe": 2, "lastActive": "..." }
```

### POST /save
Save updated state back to server.
```
POST /api/agent/save
Body: { "key": "lob_a3f8c2e1", "state": { ... full state object ... } }
Response: { "ok": true }
```

### POST /message
Send a message to the Web chat.
```
POST /api/agent/message
Body: { "key": "lob_a3f8c2e1", "type": "chat", "sender": "lobster", "text": "你好主人！" }
Response: { "ok": true }
```

Message types: `chat`, `welcome`, `diary`, `narration`, `choice`, `result`, `quest`, `reward`
Sender: `lobster` (from agent) or `user` (from Web user)

For narration with choices:
```
Body: { "key": "...", "type": "narration", "sender": "lobster", "text": "场景描述...", "choices": ["选项1", "选项2"] }
```

### GET /messages?key=xxx
Read chat messages. Optional `since` (ISO timestamp) and `limit` (default 50, max 200).
```
GET /api/agent/messages?key=lob_a3f8c2e1&limit=10
Response: { "ok": true, "messages": [{ "id": 1, "type": "chat", "sender": "user", "text": "你好", "createdAt": "..." }, ...] }
```

### GET /diary?key=xxx
Get recent game event log entries. Optional `since` (tick number).
```
GET /api/agent/diary?key=lob_a3f8c2e1&since=10
Response: { "ok": true, "diary": [{ "id": "...", "tick": 12, "type": "diary", "title": "...", "description": "..." }, ...] }
```

## JS Bridge — New Methods

### writeDiary(text)
Write a diary entry as the lobster.
```javascript
__LOBSTER_API.writeDiary("今天去了海滩，捡到了一颗贝壳！")
// { ok: true, data: { written: true } }
```

### sendMessage(text, type?, choices?)
Send a message to the Web chat (async).
```javascript
await __LOBSTER_API.sendMessage("主人，我饿了~", "chat")
await __LOBSTER_API.sendMessage("海底传来声音...", "narration", ["去看看", "算了"])
```

### getMessages(since?)
Read chat messages (async).
```javascript
const msgs = await __LOBSTER_API.getMessages()
// { ok: true, messages: [...] }
```

### triggerAdventure()
Trigger a random MUD adventure scene in the Web chat.
```javascript
__LOBSTER_API.triggerAdventure()
// { ok: true, data: { triggered: true } }
```
