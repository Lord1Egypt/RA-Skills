# Research Notes — nano-gpt plugin

## What we know
- NanoGPT is a model aggregator with OpenAI-compatible API
- Base URL: https://nano-gpt.com/api/v1
- Auth: Bearer token (`sk-nano-<uuid>`) in `Authorization` header
- Model catalog: `GET /api/v1/models?detailed=true` (auth optional but gives user-specific pricing)
- Usage: `GET /api/subscription/v1/usage` (auth required)
- Balance: `POST /api/check-balance` (auth required)
- Existing OpenClaw integration is manual JSON config only (no plugin)
- 50+ model families: OpenAI, Anthropic, Google, xAI, Groq, DeepSeek, Moonshot, Qwen, etc.

## Model ID format in nano-gpt
- Format: `provider/model-id` e.g. `anthropic/claude-opus-4.6`, `openai/gpt-5.2`
- NanoGPT uses `/` in model IDs — OpenClaw provider format is `nano-gpt/anthropic/claude-opus-4.6`

## API compatibility
- Standard OpenAI `/v1/chat/completions` — compatible with `api: "openai-completions"`
- No special headers needed beyond `Authorization: Bearer`
- Streaming via SSE — same as OpenAI

## Capabilities from detailed model list
```
capabilities.vision              → input: ["text","image"]
capabilities.reasoning          → reasoning: true
pricing.prompt                  → cost.input ($/M tokens)
pricing.completion               → cost.output ($/M tokens)
context_length                  → contextWindow
max_output_tokens               → maxTokens
```

## Key SDK hooks needed
1. `catalog` (async) — fetch and map model list
2. `resolveDynamicModel` — accept arbitrary model refs
3. `resolveUsageAuth` — pass Bearer token
4. `fetchUsageSnapshot` — GET /api/subscription/v1/usage

## Alternative domains (good to know)
- ai.bitcoin.com
- bcashgpt.com
- cake.nano-gpt.com
(Only base URL changes, model IDs and endpoints the same)
