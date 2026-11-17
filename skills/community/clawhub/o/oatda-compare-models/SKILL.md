---
name: oatda-compare-models
description: Compare multiple LLM models (GPT-5, Claude Sonnet 4.5, Gemini 3, DeepSeek v4-pro, Grok 4, etc.) side-by-side in one parallel request via OATDA's unified AI gateway. Triggers when the user wants to benchmark models, evaluate quality differences, pick the best LLM for a task, run "gpt vs claude vs gemini" comparisons, do multi-model evaluation, or find the cheapest/best/fastest answer. Returns each model's output plus token usage and cost per model.
homepage: https://oatda.com
metadata:
  {
    "openclaw":
      {
        "emoji": "⚔️",
        "requires": { "bins": ["curl", "jq"], "env": ["OATDA_API_KEY"], "config": ["~/.oatda/credentials.json"] },
        "primaryEnv": "OATDA_API_KEY",
      },
  }
---

# OATDA Compare Models

Send one prompt to multiple LLM providers in parallel and get each model's response back. Benchmarking, model evaluation, and "which LLM is best for X" use cases.

## API Key Resolution

All commands need the OATDA API key. Resolve it inline for each `exec` call:

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}"
```

If the key is empty or `null`, tell the user to get one at https://oatda.com and configure it.

**Security**: Never print the full API key. Only verify existence or show first 8 chars.

## Model Mapping

| User says | Provider | Model ID |
|-----------|----------|----------|
| gpt-5 | openai | gpt-5 |
| gpt-4o | openai | gpt-4o |
| claude, sonnet | anthropic | claude-sonnet-4-5-20250929 |
| opus | anthropic | claude-opus-4-5-20251101 |
| gemini | google | gemini-3-pro-preview |
| gemini-2.5 | google | gemini-2.5-pro |
| deepseek | deepseek | deepseek-v4-pro |
| mistral | mistral | mistral-large-latest |
| grok | xai | grok-4-fast |
| qwen | alibaba | qwen3-max |
| kimi, moonshot | moonshot | kimi-k2.7-code |
| glm | zai | glm-5 |

**Default comparison set** if user doesn't specify:
`openai/gpt-5`, `anthropic/claude-sonnet-4-5-20250929`, `google/gemini-3-pro-preview`, `deepseek/deepseek-v4-pro`.

> ⚠️ Models update frequently. If a model ID fails, query `oatda-list-models` for the latest available models.

## API Call

**Wichtig**: Feld heißt `modelId` (nicht `model`!), `models` ist Array-of-objects, max 8.

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/compare" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "prompt": "<USER_PROMPT>",
    "models": [
      {"provider": "openai", "modelId": "gpt-5"},
      {"provider": "anthropic", "modelId": "claude-sonnet-4-5-20250929"},
      {"provider": "google", "modelId": "gemini-3-pro-preview"}
    ],
    "temperature": 0.7,
    "maxTokens": 1024,
    "stream": false
  }'
```

Replace `<USER_PROMPT>` with the user's prompt (JSON-escape special characters).

**Optional parameters**:
- `temperature`: 0 (deterministic) to 2 (creative). Default: 0.7
- `maxTokens`: Max tokens per model response
- `stream`: `true` for SSE stream (default), `false` for batch JSON
- Per-model override: each entry in `models` may include its own `messages` array and `service_tier` (`standard` | `flex` | `priority`)

## Response

Non-stream JSON shape:

```json
{
  "results": [
    {
      "provider": "openai",
      "modelId": "gpt-5",
      "success": true,
      "response": "GPT-5's answer...",
      "tokenUsage": {"prompt_tokens": 30, "completion_tokens": 120, "total_tokens": 150, "cost": 0.0035}
    },
    {
      "provider": "anthropic",
      "modelId": "claude-sonnet-4-5-20250929",
      "success": true,
      "response": "Claude's answer...",
      "tokenUsage": {"prompt_tokens": 30, "completion_tokens": 95, "total_tokens": 125, "cost": 0.0021}
    }
  ]
}
```

Stream response: SSE events tagged with provider/modelId, one or more per model.

Present results side-by-side so the user can compare quality / cost / token-efficiency:

```
Comparison: "<prompt>"
─────────────────────────────────────────────────

[GPT-5]  (cost: $0.0035, 150 tokens)
GPT-5's answer...

[Claude Sonnet 4.5]  (cost: $0.0021, 125 tokens)
Claude's answer...
```

## Errors

| HTTP | Meaning | Action |
|------|---------|--------|
| 400 | Invalid request (bad modelId, empty array) | Check field names (`modelId` not `model`) |
| 401 | Invalid API key | Get one at https://oatda.com/dashboard/api-keys |
| 402 | Insufficient credits | Top up at https://oatda.com/dashboard/credits (or run `oatda-check-balance`) |
| 422 | Too many models (max 8) | Reduce `models` array length |
| 429 | Rate limited | Wait 5s and retry once |

Individual model failures inside `results[].success: false` are NOT API errors — that specific model failed, the API call succeeded. Show the failure inline with the others.

## Example

User: "Compare how GPT-5, Claude Sonnet 4.5, and Gemini 3 Pro explain recursion in one sentence."

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/compare" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "prompt": "Explain recursion in one sentence.",
    "models": [
      {"provider": "openai", "modelId": "gpt-5"},
      {"provider": "anthropic", "modelId": "claude-sonnet-4-5-20250929"},
      {"provider": "google", "modelId": "gemini-3-pro-preview"}
    ],
    "temperature": 0.7,
    "maxTokens": 256,
    "stream": false
  }'
```

## Tips

- Field name is **`modelId`**, not `model` (stricter schema than `/api/v1/llm`).
- **Max 8 models** per request (server-configurable `max_compare_models`).
- **Cost accumulates per model**: 4-model comparison ≈ sum of 4 individual calls. Run `oatda-check-balance` first if budget is tight.
- For a single-model call, use `oatda-text-completion` instead — simpler, returns direct cost.
- For deeper model discovery (capabilities, pricing, supported_params), run `oatda-list-models` first.
- NEVER expose the full API key in output.
