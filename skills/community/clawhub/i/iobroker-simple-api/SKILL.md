---
name: iobroker-simple-api
description: Full access to ioBroker via the iobroker simple-api adapter. Read states, objects, historical data, write to states, execute scripts, and more.
---

# 📊 ioBroker Simple-API Skill

> Production-ready ioBroker client for OpenClaw automation.

Full access to ioBroker via the simple-api adapter. Read states, objects, historical data, write to states, execute JavaScript, and monitor your smart home. The skill automatically handles caching, rate limiting, and circuit breaker protection. Use this skill to integrate OpenClaw with your ioBroker installation for full smart home control.

---

## 🚀 Quick Start

### Prerequisites

- ioBroker with [simple-api](https://github.com/ioBroker/ioBroker.simple-api) adapter installed
- Adapter running on a port (default 8087)

### Minimal Configuration

The skill auto-detects config on first run. Manual config in `openclaw.json`:

```json
{
  "entries": {
    "iobroker-simple-api": {
      "config": {
        "url": "http://CHANGE_ME_IP",
        "port": 8087,
        "username": "",
        "password": ""
      }
    }
  }
}
```

### Test Connection

```
health
```

Returns connection status, uptime, and state count.

---

## ⚙️ Configuration

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `url` | Yes | `http://CHANGE_ME_IP` | ioBroker simple-api base URL |
| `port` | Yes | `8087` | ioBroker simple-api port |
| `username` | No | (empty) | Basic Auth username |
| `password` | No | (empty) | Basic Auth password |

### Auto-Detection

The skill automatically detects the OpenClaw config path:
1. From environment variables (`OPENCLAW_HOME`, `OPENCLAW_STATE_DIR`)
2. From its own installation path (skill → workspace → .openclaw)
3. Creates default config on first run if missing

### Runtime Config

Change config at runtime:

```
config:baseUrl=http://CHANGE_ME_IP:8087
config:timeout=20000
```

---

## 📖 Read Operations

### Get State Value

```
getPlainValue:javascript.0.sensor.temperature
```

With JSON parsing:
```
getPlainValue:javascript.0.data?json
```

### Get State + Object

```
get:javascript.0.sensor.temperature
```

### Get Multiple States

```
getBulk:javascript.0.sensor.temperature,javascript.0.sensor.humidity
```

### List Objects/States

```
objects:*              # All objects
objects:javascript.0.*  # JavaScript adapter objects
states:*               # All states
states:humidity*       # States starting with humidity
```

### Search

```
search:temperature
search:livingroom
```

### Query History

```
query:javascript.0.sensor.temperature?dateFrom=-1h
query:system.host.*?dateFrom=-24h&aggregate=minmax
```

Supported time formats:
- `-1h`, `-30m`, `-7d` (relative)
- `today` (today at midnight)
- `2024-01-01` (absolute)

### CSV Export

```
csv:javascript.0.sensor.temperature?dateFrom=-24h
```

---

## 📤 Write Operations

### Set State

```
set:javascript.0.light?value=on
set:javascript.0.counter?value=42&type=number&ack=true
```

### Toggle

```
toggle:javascript.0.switch
```

### Set Multiple

```
setBulk:javascript.0.light1=on&javascript.0.light2=off
```

### Create/Delete State

```
create:javascript.0.myNewState?common={"type":"number","name":"My State"}
delete:javascript.0.myNewState
```

### Enable/Disable

```
enable:javascript.0.myNewState
disable:javascript.0.myNewState
```

---

## 💻 Script Execution

### Execute JavaScript

```
exec:$('javascript.0.sensor.temp').val(true)
eval:2+2
```

### List Scripts

```
scripts
jsinfo
```

---

## 🔌 System Commands

| Command | Description |
|---------|-------------|
| `health` | Connection status, uptime, state count |
| `cache` | Cache statistics (hits, misses, size) |
| `rate` | Rate limit status |
| `system` | Hosts, memory, CPU info |
| `runtime` | Uptime, CPU, memory, disk |
| `adapters` | List installed adapters |
| `instances` | Adapter instances with status |
| `status` | Full skill status |

---

## 🎬 Scenes & Snapshots

### Scenes

```
scene:mynight={"light.living":"on","light.bedroom":"off"}
scenes
activate:mynight
deletescene:mynight
```

### Snapshots

```
snapshot:backup=state1,state2
snapshots
diff:snap1 vs snap2
diff:snap1 vs current
```

---

## 📊 Groups & Enums

```
groups
groups:rooms
group:enum.rooms.living
```

---

## ⚡ Features

### Caching
- 30 second TTL for frequently accessed states
- Automatic cache invalidation on writes

### Rate Limiting
- 10 requests/second to prevent API flooding
- Queue management for burst requests

### Circuit Breaker
- Auto-recovery on failures
- Exponential backoff with jitter

### Batch Operations
- Efficient bulk get/set
- Parallel execution option

### Type Coercion
- Convert between boolean/number/string
- Automatic JSON parsing

### Historical Queries
- Multiple aggregation types (minmax, average, sum, count)
- Configurable time ranges

---

## 📋 API Reference

### Commands Summary

| Command | Description |
|---------|-------------|
| `getPlainValue:<id>` | Get state value |
| `get:<id>` | Get state + object |
| `getBulk:<ids>` | Multiple states |
| `objects:<pattern>` | List objects |
| `states:<pattern>` | List states |
| `search:<pattern>` | Search data |
| `query:<id>?dateFrom=...` | Query history |
| `set:<id>?value=...` | Set state |
| `toggle:<id>` | Toggle state |
| `setBulk:<id1>=<v1>&<id2>=<v2>` | Multiple writes |
| `create:<id>?common=...` | Create state |
| `delete:<id>` | Delete state |
| `exec:<js>` | Execute JS |
| `scene:name={...}` | Create scene |
| `snapshot:name=...` | Take snapshot |
| `groups` | List enums |
| `health` | Connection check |
| `cache` | Cache stats |
| `system` | System info |
| `runtime` | Runtime info |

---

## 📁 Resources

### Files

- `skill.js` - Main implementation
- `index.js` - Skill loader
- `LICENSE` - MIT No Attribution

---

## 🔗 External Links

- [ioBroker](https://www.iobroker.net/)
- [simple-api Adapter](https://github.com/ioBroker/ioBroker.simple-api)
- [ioBroker REST API Docs](https://www.iobroker.net/#en/adapters/adapterref/iobroker.simple-api/README.md)