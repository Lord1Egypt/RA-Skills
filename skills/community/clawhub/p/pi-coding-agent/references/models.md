# Pi Custom Models & Providers

File: `~/.pi/agent/models.json` (edits auto-reload on `/model`)

## Minimal Example (Ollama)

```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "models": [{ "id": "llama3.1:8b" }]
    }
  }
}
```

## Supported API Types

- `openai-completions` — OpenAI Chat Completions (broadest compatibility)
- `openai-responses` — OpenAI Responses API
- `anthropic-messages` — Anthropic Messages API
- `google-generative-ai` — Google Generative AI

## Full Model Configuration

```json
{
  "id": "model-id",
  "name": "Display Name",
  "api": "openai-completions",
  "reasoning": true,
  "thinkingLevelMap": { "off": null, "medium": "medium", "high": "high" },
  "input": ["text", "image"],
  "contextWindow": 128000,
  "maxTokens": 16384,
  "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
  "compat": { "supportsDeveloperRole": false }
}
```

## thinkingLevelMap

Maps Pi's 6 thinking levels to provider values:

| Value | Meaning |
|-------|---------|
| Omitted | Use provider default mapping |
| String | Send this value to provider |
| null | Level not supported (hidden in UI) |

## Overriding Built-in Providers

```json
{ "providers": { "anthropic": { "baseUrl": "https://my-proxy/v1" } } }
```
All built-in models are retained; only routing changes.

Merge semantics: built-in models retained, custom models upserted by id (same id replaces, new id adds).

## modelOverrides

Override specific built-in models (without replacing the entire provider model list):

```json
{ "providers": { "openrouter": { "modelOverrides": {
  "anthropic/claude-sonnet-4": { "name": "Claude 4 (Bedrock Route)", "compat": { "openRouterRouting": { "only": ["amazon-bedrock"] } } }
}}}}
```

## OpenAI Compat Options (compat)

| Field | Description |
|-------|-------------|
| `supportsDeveloperRole` | Use developer role (false → system role) |
| `supportsReasoningEffort` | Supports reasoning_effort |
| `supportsUsageInStreaming` | Supports stream_options.include_usage |
| `maxTokensField` | `max_completion_tokens` or `max_tokens` |
| `requiresToolResultName` | Tool result includes name |
| `thinkingFormat` | reasoning_effort/openrouter/deepseek/together/zai/qwen/qwen-chat-template |
| `openRouterRouting` | OpenRouter provider routing config |
| `vercelGatewayRouting` | Vercel AI Gateway routing |
| `cacheControlFormat` | `"anthropic"` — Anthropic-style prompt caching |

## Anthropic Compat Options

| Field | Description |
|-------|-------------|
| `supportsEagerToolInputStreaming` | eager_input_streaming (default true) |
| `supportsLongCacheRetention` | cache_control.ttl: "1h" (default true) |
| `sendSessionAffinityHeaders` | x-session-affinity (auto-detected) |
| `supportsCacheControlOnTools` | cache_control on tool definitions (default true) |
| `forceAdaptiveThinking` | adaptive thinking (thinking.type: "adaptive") |

## apiKey/headers Formats

- Literal: used directly
- Env var: `"MY_KEY"`
- Shell command: `"!op read 'op://vault/item'"` (resolved at request time, not cached)