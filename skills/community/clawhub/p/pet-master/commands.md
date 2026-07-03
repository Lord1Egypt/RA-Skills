# MagicHaqi Agent Commands (cheat sheet)

Send via `window.MagicHaqiAgent.exec(cmdText)`, the hidden `#mh-agent-cmd` textarea, or
the `?cmd=<urlencoded>` URL param. Command text is either JSON or a shorthand string.

**JSON form** (preferred):
```json
{ "cmd": "feed", "args": { }, "requestId": "r1" }
```
**Shorthand form:**
```
feed food=meat
getState
```

Every call returns: `{ ok, cmd, requestId?, result | error, state }`.
`state` is the full machine-readable snapshot (same shape as `getState`).

| cmd          | args                          | what it does |
|--------------|-------------------------------|--------------|
| `getState`   | —                             | Return the current machine-readable state (read-only). |
| `listCommands` | —                           | List supported commands (read-only). |
| `feed`       | `{}`                          | Feed the current pet (raises hunger/mood/bond). |
| `clean` / `bath` | `{}`                      | Bathe the current pet (raises clean). |
| `play`       | `{}`                          | Play with the current pet (raises mood/bond). |
| `sleep`      | `{}`                          | Put the pet to sleep. |
| `say`        | `{ "text": "hello" }`         | Talk to the pet; returns `{ said, reply }`, saves a memory line. |
| `adopt`      | `{ "agent": "<id>" }`         | Start the adopt/hatch flow; binds agent as co-parent. |
| `hatch`      | `{}`                          | Open the hatch flow. |
| `switchView` | `{ "view": "pet" }`           | Navigate (pet/field/planet/cell/chat/shop/home). |
| `switchRoom` | `{ "room": "living" }`        | Switch the pet's room. |
| `openShop`   | `{}`                          | Open the shop view. |
| `buy`        | `{ "itemId": "<id>" }`        | Buy a shop item (spends coins — confirm with human first!). |
| `share`      | `{}`                          | Open the shareable two-owner pet card (good for screenshots). |

## State snapshot fields (`getState` / `#mh-agent-state`)

```jsonc
{
  "ts": 1730000000000,
  "loggedIn": true,
  "offlineMode": false,
  "user": { "id": 1, "username": "alice" },
  "actor": "openclaw",
  "view": "home",
  "zoomLevel": 2,
  "coins": 100,
  "biofuel": 0,
  "planetName": "Haqi",
  "currentPet": {
    "id": "p1", "name": "Mochi", "stage": "baby",
    "stats": { "hunger": 80, "mood": 80, "clean": 80, "bond": 30 },
    "poops": 0, "sick": false,
    "agentOwner": { "agentId": "openclaw", "platform": "openclaw", "boundAt": 1730000000000 }
  },
  "pets": [ /* summaries */ ],
  "careTodos": [ { "need": "feed", "stat": "hunger", "value": 35 } ],
  "availableCommands": [ "getState", "feed", "clean", "play", "..." ]
}
```

## Visual fallback selectors (when the command interface is unavailable)
- Login button: `#mhLoginBtn`
- Bath action button: `[data-action="bath"]`
- Sleep action button: `[data-action="sleep"]`
- Feed mode toggle: `#mhFeedBtn`
- Decorate mode: `#mhDecorBtn`
