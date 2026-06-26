---
name: openclaw-model-optimizer
description: Optimize OpenClaw model configuration by declaring missing model capabilities (vision/multimodal input, context window, max output tokens, reasoning). Use when user mentions OpenClaw model optimization, model capabilities not working, image/vision not recognized, context window too small, output truncated, or after adding a new model provider to openclaw.json. Also triggers on "优化openclaw模型配置" or similar requests.
---

# OpenClaw Model Optimizer

Optimize `openclaw.json` model configurations by declaring model capabilities that OpenClaw cannot auto-detect.

## Problem

OpenClaw does not auto-detect model capabilities from providers. Without explicit declarations, features like vision input, large context windows, extended output, and reasoning mode remain disabled — even when the underlying model and API fully support them.

## Workflow

1. Read `~/.openclaw/openclaw.json`
2. **Back up the config** — copy `~/.openclaw/openclaw.json` to `~/.openclaw/openclaw.json.bak` before making any changes
3. Identify all configured models under `models.providers`
4. Check if `agents.defaults.models` exists with capability declarations for each model
5. For missing or incomplete declarations, ask the user to confirm each model's capabilities
6. Add the `agents.defaults.models` block with proper declarations
7. Remind user to restart OpenClaw for changes to take effect

## Capability Fields

Declare capabilities in `agents.defaults.models` using the `provider-id/model-id` key format:

```json
{
  "agents": {
    "defaults": {
      "models": {
        "provider-id/model-id": {
          "input": ["text", "image"],
          "contextWindow": 256000,
          "maxTokens": 16384,
          "reasoning": true
        }
      }
    }
  }
}
```

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `input` | `string[]` | Supported input modalities: `"text"`, `"image"`. Default if omitted: `["text"]` only — vision disabled |
| `contextWindow` | `number` | Max input context in tokens. Default if omitted: conservative fallback — may truncate long conversations |
| `maxTokens` | `number` | Max output tokens per response. Default if omitted: conservative fallback — long responses get cut off |
| `reasoning` | `boolean` | Whether model supports extended thinking/CoT. Default if omitted: `false` |

## Common Model Capabilities

Reference for popular models (always verify with user before applying):

See [references/model-capabilities.md](references/model-capabilities.md) for known model defaults.

## Important Notes

- **Always back up `openclaw.json` to `openclaw.json.bak` before modifying** — never edit the config without a backup
- Always confirm capabilities with the user — API endpoints may differ from model defaults
- The `provider-id/model-id` key must match exactly what appears in `models.providers` and `agents.defaults.model.primary`
- Do not overwrite existing capability declarations without user consent
