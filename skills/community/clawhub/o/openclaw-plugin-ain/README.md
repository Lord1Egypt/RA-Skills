# openclaw-plugin-ain

OpenClaw plugin that bridges [AIN](https://github.com/felipematos/ain) provider registry, intelligent routing, and execution into the OpenClaw ecosystem.

## Features

- **Provider bridging** — All AIN-configured providers are exposed to OpenClaw as `ain:<name>`
- **LLM tools** — `ain_run` (prompt execution) and `ain_classify` (task classification) available to agents
- **Routing hook** — `before_model_resolve` hook uses AIN's intelligent routing engine

## Installation

```bash
npm install openclaw-plugin-ain
```

## Configuration

In your OpenClaw config:

```json
{
  "plugins": {
    "ain": {
      "enableRouting": true,
      "routingPolicy": "default",
      "exposeTools": true
    }
  }
}
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `configPath` | string | `~/.ain/config.yaml` | Path to AIN config file |
| `enableRouting` | boolean | `true` | Enable the routing hook |
| `routingPolicy` | string | — | Named routing policy from AIN policies |
| `exposeTools` | boolean | `true` | Expose ain_run and ain_classify tools |

## Tools

### `ain_run`

Execute an LLM prompt through AIN.

**Parameters:** `prompt` (required), `provider`, `model`, `jsonMode`, `schema`, `system`, `temperature`

### `ain_classify`

Classify a prompt's task type and complexity.

**Parameters:** `prompt` (required)

**Returns:** `{ taskType, complexity }`

## License

MIT
