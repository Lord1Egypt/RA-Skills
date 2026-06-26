# GRU Gateway Model Catalog

All models below are served through `https://gru.huddle01.io` and must use the `hudl/` prefix in OpenClaw config.

## Supported Models

### OpenAI

| Model ID | Aliases (user might say) | Notes |
|---|---|---|
| `hudl/gpt-5.4` | gpt5, 5.4 | Latest GPT |
| `hudl/gpt-5.4-pro` | gpt5 pro, 5.4 pro | GPT-5.4 extended reasoning |
| `hudl/gpt-4.1` | gpt4.1, 4.1 | GPT-4.1 |
| `hudl/gpt-4.1-mini` | 4.1 mini | GPT-4.1 smaller, cheaper |
| `hudl/gpt-4.1-nano` | 4.1 nano | GPT-4.1 smallest, cheapest |
| `hudl/o3` | o3 | OpenAI reasoning model |
| `hudl/o4-mini` | o4, o4 mini | OpenAI reasoning model (small) |
| `hudl/gpt-4o-mini` | 4o mini | Legacy, fast and cheap |

### Anthropic

| Model ID | Aliases (user might say) | Notes |
|---|---|---|
| `hudl/claude-opus-4.6` | opus, claude, smart model, advanced, big model | Best reasoning, expensive |
| `hudl/claude-sonnet-4.6` | sonnet 4.6, new sonnet | Claude Sonnet 4.6 |
| `hudl/claude-sonnet-4.5` | sonnet 4.5 | Claude Sonnet 4.5 |
| `hudl/claude-haiku-4.5` | haiku | Fast, cheap Claude |
| `hudl/claude-sonnet-4` | sonnet 4 | Claude Sonnet 4 |

### Google

| Model ID | Aliases (user might say) | Notes |
|---|---|---|
| `hudl/gemini-3.1-pro` | gemini pro, gemini 3.1 | Latest Gemini Pro |
| `hudl/gemini-3.1-flash-lite` | gemini flash lite, flash lite | Ultra cheap Gemini |
| `hudl/gemini-2.5-pro` | gemini 2.5 pro | Gemini 2.5 Pro |
| `hudl/gemini-2.5-flash` | gemini flash, flash | Fast Gemini |

### DeepSeek

| Model ID | Aliases (user might say) | Notes |
|---|---|---|
| `hudl/deepseek-v3.2` | deepseek, deepseek v3, v3.2 | DeepSeek V3.2 |
| `hudl/deepseek-r1` | deepseek r1, r1 | DeepSeek reasoning model |

### xAI

| Model ID | Aliases (user might say) | Notes |
|---|---|---|
| `hudl/grok-4.1-fast` | grok, grok fast | Grok 4.1 Fast |
| `hudl/grok-3-mini` | grok mini, grok 3 | Grok 3 Mini |

### Qwen

| Model ID | Aliases (user might say) | Notes |
|---|---|---|
| `hudl/qwen3-235b` | qwen, qwen3 | Qwen3 235B |
| `hudl/qwen-2.5-coder-32b` | qwen coder | Qwen coding model |

### MiniMax

| Model ID | Aliases (user might say) | Notes |
|---|---|---|
| `hudl/minimax-m2.5` | minimax, m2.5, cheap model, fast model, default | Default model |

### Moonshot

| Model ID | Aliases (user might say) | Notes |
|---|---|---|
| `hudl/kimi-k2.5` | kimi, k2.5 | Kimi K2.5 |

### Meta

| Model ID | Aliases (user might say) | Notes |
|---|---|---|
| `hudl/llama-4-maverick` | llama, llama 4, maverick | Llama 4 Maverick |
| `hudl/llama-3.3-70b` | llama 3.3, llama 70b | Llama 3.3 70B |

### Mistral

| Model ID | Aliases (user might say) | Notes |
|---|---|---|
| `hudl/mistral-large` | mistral, mistral large | Mistral Large |
| `hudl/codestral` | codestral | Mistral coding model |

## Prefix rule

Every model served through GRU gets the `hudl/` prefix. This tells OpenClaw to route requests through the hudl provider config (which points at gru.huddle01.io). Without the prefix, OpenClaw won't know which provider to use.

Examples:
- User says "opus" -> config value: `hudl/claude-opus-4.6`
- User says "use grok" -> config value: `hudl/grok-4.1-fast`
- User says "switch to deepseek" -> config value: `hudl/deepseek-v3.2`

## Adding new models

When a new model is added to the GRU gateway:

1. Add a row to the appropriate provider table above.
2. The model ID in config must always be `hudl/<model-id-as-it-appears-on-gru>`.
3. Verify available models via: `curl -s https://gru.huddle01.io/v1/models -H "Authorization: Bearer $KEY" | jq '.data[].id'`