# Existing nano-gpt → OpenClaw Integration

Source: https://docs.nano-gpt.com/integrations/openclaw.md

## Current State (Manual JSON Config)
NanoGPT already works with OpenClaw via manual JSON config. Users add this to their `clawdbot.json`:

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "nanogpt": {
        "baseUrl": "https://nano-gpt.com/api/v1",
        "apiKey": "YOUR_KEY",
        "auth": "api-key",
        "api": "openai-completions",
        "headers": {},
        "authHeader": false,
        "models": [
          {
            "id": "anthropic/claude-opus-4.5",
            "name": "Claude Opus 4.5",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 200000,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

## What a Plugin Adds
The manual approach requires users to:
1. Know which models exist (hardcoded list goes stale)
2. Know model capabilities (context window, reasoning, vision, etc.)
3. Manually configure costs
4. No usage tracking

A proper plugin would:
- Fetch dynamic model list from `/api/v1/models?detailed=true`
- Auto-populate model capabilities (vision, reasoning, context window, pricing)
- Handle `NANOGPT_API_KEY` env var detection
- Provide `openclaw onboard --nano-gpt-api-key <key>` flow
- Support usage tracking via `/api/subscription/v1/usage`
- Balance checking via `/api/check-balance`
- Support all model families: OpenAI, Anthropic, Google, xAI, DeepSeek, Moonshot, Qwen, etc.

## Alternative Base URLs
- `https://nano-gpt.com/api/v1` (canonical)
- `https://nano-gpt.com/api/subscription/v1` (subscription-only routing)
- Alternative domains: `ai.bitcoin.com`, `bcashgpt.com`, `cake.nano-gpt.com`
