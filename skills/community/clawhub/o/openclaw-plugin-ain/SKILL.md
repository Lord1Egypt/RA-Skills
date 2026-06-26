# AIN — AI Node Plugin for OpenClaw

Bridges the [AIN](https://github.com/felipematos/ain) provider registry, intelligent routing engine, and execution layer into the OpenClaw ecosystem.

## What it does

- **Provider bridging** — All AIN-configured providers (LM Studio, Ollama, OpenAI, vLLM, etc.) are automatically exposed to OpenClaw as `ain:<name>` providers
- **LLM tools** — Two agent tools: `ain_run` (prompt execution with routing, structured output, fallback chains) and `ain_classify` (task type and complexity classification)
- **Routing hook** — `before_model_resolve` hook uses AIN's intelligent routing engine to automatically select the best model for each task based on policies and task classification

## Installation

```bash
npm install openclaw-plugin-ain
```

Requires [@felipematos/ain-cli](https://www.npmjs.com/package/@felipematos/ain-cli) (installed as a dependency).

## Configuration

In your OpenClaw config:

```json
{
  "plugins": {
    "ain": {
      "enableRouting": true,
      "routingPolicy": "local-first",
      "exposeTools": true
    }
  }
}
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `configPath` | string | `~/.ain/config.yaml` | Path to AIN config file |
| `enableRouting` | boolean | `true` | Enable intelligent model routing |
| `routingPolicy` | string | — | Named routing policy from AIN policies.yaml |
| `exposeTools` | boolean | `true` | Expose ain_run and ain_classify tools to agents |

## Tools

### `ain_run`

Execute an LLM prompt through AIN's execution engine with full support for routing, structured output, and fallback chains.

**Parameters:**
- `prompt` (string, required) — The prompt to execute
- `provider` (string) — Provider name
- `model` (string) — Model ID or alias
- `jsonMode` (boolean) — Request JSON output
- `schema` (object) — JSON Schema for output validation
- `system` (string) — System prompt
- `temperature` (number) — Sampling temperature

**Returns:** `{ output, provider, model, usage, parsedOutput }`

### `ain_classify`

Classify a prompt's task type and estimate its complexity.

**Parameters:**
- `prompt` (string, required) — The prompt to classify

**Returns:** `{ taskType, complexity }`

Task types: `classification`, `extraction`, `generation`, `reasoning`, `unknown`
Complexity: `low`, `medium`, `high`

## Routing

When `enableRouting` is true, the plugin registers a `before_model_resolve` hook that analyzes incoming prompts and selects the optimal model based on:

- Task classification (classification/extraction → fast tier, generation → general tier, reasoning → reasoning tier)
- Routing policies defined in `~/.ain/policies.yaml`
- Model tags and tier configuration

## Requirements

- Node.js >= 18
- AIN configured with at least one provider (`ain config init && ain providers add ...`)
- OpenClaw >= 1.0.0

## License

MIT
