---
name: oatda-text-completion
description: Generate text using OATDA's unified LLM API. Triggers when the user wants to generate, write, or complete text using a specific LLM provider (OpenAI, Anthropic, Google, Deepseek, Mistral, xAI, Alibaba, MiniMax, ZAI, Moonshot) through the OATDA API. Also use when comparing outputs across models or using model aliases like "gpt-4o", "claude", "gemini", "deepseek", "grok", "qwen", "mistral".
homepage: https://oatda.com
metadata:
  {
    "openclaw":
      {
        "emoji": "💬",
        "requires": { "bins": ["curl", "jq"], "env": ["OATDA_API_KEY"], "config": ["~/.oatda/credentials.json"] },
        "primaryEnv": "OATDA_API_KEY",
      },
  }
---

# OATDA Text Completion

Generate text from 10+ LLM providers through OATDA's unified API.

## API Key Resolution

All commands need the OATDA API key. Resolve it inline for each `exec` call:

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}"
```

If the key is empty or `null`, tell the user to get one at https://oatda.com and configure it.

**Security**: Never print the full API key. Only verify existence or show first 8 chars.

## Model Mapping

| User says | Provider | Model |
|-----------|----------|-------|
| gpt-4o | openai | gpt-4o |
| gpt-4o-mini | openai | gpt-4o-mini |
| o1 | openai | o1 |
| claude, sonnet | anthropic | claude-3-5-sonnet |
| haiku | anthropic | claude-3-5-haiku |
| opus | anthropic | claude-3-opus |
| gemini | google | gemini-2.0-flash |
| gemini-1.5 | google | gemini-1.5-pro |
| deepseek | deepseek | deepseek-chat |
| mistral | mistral | mistral-large |
| grok | xai | grok-2 |
| qwen | alibaba | qwen-max |

**Default**: `openai` / `gpt-4o` if no model specified. If user provides `provider/model` format, split on `/`.

> ⚠️ Models update frequently. If a model ID fails, query `oatda-list-models` for the latest available models.

## API Call

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "provider": "<PROVIDER>",
    "model": "<MODEL>",
    "prompt": "<USER_PROMPT>",
    "temperature": 0.7,
    "maxTokens": 4096
  }'
```

### Optional Parameters

- `temperature`: 0 (deterministic) to 2 (creative). Default: 0.7
- `maxTokens`: Max tokens to generate. Default: 4096 (max 128000 for some models)
- `stream`: Set to `true` for streaming (not recommended via curl)

## Response Format

```json
{
  "success": true,
  "provider": "openai",
  "model": "gpt-4o",
  "response": "The generated text content...",
  "tokenUsage": {
    "prompt_tokens": 25,
    "completion_tokens": 150,
    "total_tokens": 175,
    "cost": 0.001375
  }
}
```

Present the `response` field to the user. Optionally mention token usage and cost.

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 401 | Invalid API key | Tell user to check key at https://oatda.com/dashboard/api-keys |
| 402 | Insufficient credits | Tell user to check balance at https://oatda.com/dashboard/usage |
| 429 | Rate limited | Wait 5 seconds and retry once |
| 400 | Bad request / model not found | Check model format, suggest `oatda-list-models` |

## Example

User: "Write a haiku about code using claude"

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X POST "https://oatda.com/api/v1/llm" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OATDA_API_KEY" \
  -d '{
    "provider": "anthropic",
    "model": "claude-3-5-sonnet",
    "prompt": "Write a haiku about code",
    "temperature": 0.7,
    "maxTokens": 256
  }'
```

## Notes

- The API expects `prompt` as a plain string, NOT a `messages` array
- Split `provider/model` into separate JSON fields
- For long-form content, increase `maxTokens`
- Use `oatda-list-models` to see all available models
- Use `oatda-vision-analysis` for image analysis tasks
