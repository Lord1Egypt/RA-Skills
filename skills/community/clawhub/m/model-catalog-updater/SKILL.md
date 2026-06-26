---
name: model-catalog-updater
version: 1.2.0
description: Query available models from your configured providers and add them to OpenClaw config
homepage: https://github.com/openclaw/skills/model-catalog
metadata:
  model-catalog-updater:
    emoji: "📊"
    category: "developer-tools"
    config_path: "C:\\Users\\zebuM\\.openclaw\\openclaw.json"
    backup_name: "openclawworking.json"
    defaults:
      contextWindow: 128000
      maxTokens: 8192
      reasoningModelPatterns:
        - "deepseek-r1"
        - "qwq"
        - "o1"
        - "o3"
        - "reasoning"
        - "think"
commands:
  - name: model-catalog-updater
    description: Fetch and add models from a provider to your config
    options:
      - name: provider
        description: Select a provider to fetch models from
        type: string
        required: true
        choices:
          - name: qwen-portal
            value: qwen-portal
          - name: lmstudio
            value: lmstudio
          - name: minimax-portal
            value: minimax-portal
          - name: xai
            value: xai
          - name: openrouter
            value: openrouter
          - name: modal-direct
            value: modal-direct
          - name: minimax
            value: minimax
          - name: google
            value: google
          - name: openai-codex
            value: openai-codex
          - name: github-copilot
            value: github-copilot
          - name: groq
            value: groq
          - name: opencode
            value: opencode
          - name: zai
            value: zai
---

# Model Catalog Updater

Fetch available models from your configured API providers and add them to your OpenClaw config.

## How It Works

When invoked, this skill:

1. **Reads your config** → Loads providers from `openclaw.json`
2. **Presents choices** → Shows numbered list of your configured providers
3. **User selects provider** → Queries `/v1/models` from that provider
4. **Shows available models** → Lists models with IDs
5. **User picks models** → Select which to add (comma-separated or 'all')
6. **Creates backup** → Saves `openclawworking.json` before any edits
7. **Updates config** → Adds models to both:
   - `models.providers.{provider}.models[]` — model definitions
   - `agents.defaults.models.{provider/model-id}` — alias entries

## Usage

**Slash command:**
- `/model-catalog-updater provider:<dropdown>`

**Natural language:**
- "show me available models"
- "add models from openrouter"
- "what models are on lmstudio"

## Configuration

| Setting | Value |
|---------|-------|
| Config path | `C:\Users\zebuM\.openclaw\openclaw.json` |
| Backup file | `openclawworking.json` (same directory) |
| Default context window | 128000 |
| Default max tokens | 8192 |

## Reasoning Detection

Models are auto-detected as reasoning models if their ID contains:
- `deepseek-r1`
- `qwq`
- `o1`
- `o3`
- `reasoning`
- `think`

## Model Entry Format

Added to `models.providers.{provider}.models`:

```json
{
  "id": "model-id",
  "name": "Display Name",
  "reasoning": false,
  "input": ["text"],
  "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
  "contextWindow": 128000,
  "maxTokens": 8192
}
```

## Alias Entry Format

Added to `agents.defaults.models`:

```json
"provider/model-id": {}
```

(Empty object — user can add `"alias": "short-name"` manually if desired)

## Example Session

```
📊 Model Catalog

Your configured providers:
1. qwen-portal (https://portal.qwen.ai/v1)
2. lmstudio (http://192.168.56.1:1234/v1)
3. xai (https://api.x.ai/v1)
4. openrouter (https://openrouter.ai/api/v1)
5. modal-direct (https://api.us-west-2.modal.direct/v1)
6. cloudflare-ai-gateway
7. minimax

Select provider [1-7]: 3

Fetching models from xai...

Available models:
1. grok-4
2. grok-4-vision
3. grok-2-1212

Select models to add (comma-separated, or 'all'): 1,2

✅ Backup created: openclawworking.json
✅ Added to models.providers.xai.models:
   - grok-4
   - grok-4-vision
✅ Added to agents.defaults.models:
   - xai/grok-4
   - xai/grok-4-vision
```

## Notes

- Some providers don't expose `/v1/models` (e.g., Cloudflare AI Gateway)
- Vision models get `"input": ["text", "image"]` automatically if ID contains "vision" or "multimodal"
- Restart OpenClaw after adding models to apply changes
