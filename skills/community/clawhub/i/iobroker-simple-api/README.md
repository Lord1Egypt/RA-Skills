# ioBroker Simple-API Skill for OpenClaw

> Production-ready ioBroker client with caching, rate limiting, and circuit breaker protection.

## Features

- 📊 **Full Read Access** - States, objects, historical data, search
- 📤 **Write Operations** - Set, toggle, setBulk, create, delete states
- 💻 **Script Execution** - Execute JavaScript in ioBroker
- ⚡ **Caching** - 30s TTL for frequently accessed states
- 🚦 **Rate Limiting** - 10 req/sec to prevent API flooding
- 🔒 **Circuit Breaker** - Auto-recovery on failures
- 🔄 **Batch Operations** - Efficient bulk get/set
- 📈 **Historical Queries** - With aggregation options
- 📋 **Scenes & Snapshots** - Save and restore state groups

## Quick Start

1. Install [simple-api](https://github.com/ioBroker/ioBroker.simple-api) adapter in ioBroker
2. Configure the skill (auto-detected on first run):

```json
{
  "entries": {
    "iobroker-simple-api": {
      "config": {
        "url": "http://iobroker.local",
        "port": 8087,
        "username": "",
        "password": ""
      }
    }
  }
}
```

3. Test connection:

```
health
```

## Commands

### Read Operations

| Command | Description |
|---------|-------------|
| `getPlainValue:<id>` | Get state value |
| `get:<id>` | Get state + object |
| `getBulk:<ids>` | Multiple states |
| `objects:<pattern>` | List objects |
| `states:<pattern>` | List states |
| `search:<pattern>` | Search data |
| `query:<id>?dateFrom=-1h` | Query history |
| `csv:<id>?dateFrom=-24h` | Export CSV |

### Write Operations

| Command | Description |
|---------|-------------|
| `set:<id>?value=...` | Set state |
| `toggle:<id>` | Toggle state |
| `setBulk:<id1>=<v1>&<id2>=<v2>` | Multiple writes |
| `create:<id>?common={...}` | Create state |
| `delete:<id>` | Delete state |

### System

| Command | Description |
|---------|-------------|
| `health` | Connection status |
| `cache` | Cache statistics |
| `system` | System info |
| `runtime` | Runtime info |
| `status` | Full status |

### Advanced

| Command | Description |
|---------|-------------|
| `exec:<js>` | Execute JavaScript |
| `scene:name={...}` | Create scene |
| `snapshot:name=...` | Take snapshot |
| `groups` | List enums |

## Examples

```bash
# Read temperature
getPlainValue:javascript.0.sensor.temperature

# Set light on
set:javascript.0.light?value=on

# Query last hour
query:system.host.*?dateFrom=-1h&aggregate=minmax

# Toggle switch
toggle:javascript.0.switch
```

## Configuration

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `url` | Yes | `http://iobroker.local` | ioBroker URL |
| `port` | Yes | `8087` | simple-api port |
| `username` | No | (empty) | Basic Auth |
| `password` | No | (empty) | Basic Auth |

Auto-detected from skill location on first run.

## Resources

- `skill.js` - Main implementation
- `index.js` - Skill loader
- `SKILL.md` - Full documentation
- `LICENSE` - MIT No Attribution

## License

MIT-0 (No Attribution Required) - See [LICENSE](LICENSE) for full text.

## Links

- [ioBroker](https://www.iobroker.net/)
- [simple-api Adapter](https://github.com/ioBroker/ioBroker.simple-api)
- [ioBroker REST API Docs](https://www.iobroker.net/#en/adapters/adapterref/iobroker.simple-api/README.md)