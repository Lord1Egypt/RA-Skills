---
name: openrouter-paid-fallback
description: Set OpenClaw to use a paid OpenRouter model first and fall back to free models when quota is exhausted or rate-limited. Use when the user wants a paid OpenRouter model such as gpt-5.4-mini as the primary model with automatic free fallback.
---

# OpenRouter Paid Fallback

## Configure

1. Keep the OpenRouter API key present in config.
2. Set `agents.defaults.model.primary` to the requested paid model.
3. Set `agents.defaults.model.fallbacks` to:
   - `openrouter/free`
   - `nvidia/nemotron-3-nano-30b-a3b:free`
   - `qwen/qwen3-next-80b-a3b-instruct:free`
   - `stepfun/step-3.5-flash:free`
   - `arcee-ai/trinity-mini:free`
4. Restart the gateway.
5. Verify with `openclaw status` or `/status`.

## Defaults

- Primary: `openrouter/openai/gpt-5.4-mini`
- Keep the same fallback list unless the user asks otherwise.

## Rules

- Edit only the model-routing keys.
- Preserve unrelated config.
- If restart fails, check gateway status and remove stale config entries before retrying.
