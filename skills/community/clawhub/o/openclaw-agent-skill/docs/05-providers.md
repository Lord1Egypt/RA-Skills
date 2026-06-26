# Model Providers

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 29

---

<!-- SOURCE: https://docs.openclaw.ai/providers -->

# Model Providers - OpenClaw

OpenClaw can use many LLM providers. Pick a provider, authenticate, then set the default model as `provider/model`. Looking for chat channel docs (WhatsApp/Telegram/Discord/Slack/Mattermost (plugin)/etc.)? See [Channels](https://docs.openclaw.ai/channels).

## Quick start

1.  Authenticate with the provider (usually via `openclaw onboard`).
2.  Set the default model:

```
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

## Provider docs

*   [Amazon Bedrock](https://docs.openclaw.ai/providers/bedrock)
*   [Anthropic (API + Claude Code CLI)](https://docs.openclaw.ai/providers/anthropic)
*   [Cloudflare AI Gateway](https://docs.openclaw.ai/providers/cloudflare-ai-gateway)
*   [GLM models](https://docs.openclaw.ai/providers/glm)
*   [Hugging Face (Inference)](https://docs.openclaw.ai/providers/huggingface)
*   [Kilocode](https://docs.openclaw.ai/providers/kilocode)
*   [LiteLLM (unified gateway)](https://docs.openclaw.ai/providers/litellm)
*   [MiniMax](https://docs.openclaw.ai/providers/minimax)
*   [Mistral](https://docs.openclaw.ai/providers/mistral)
*   [Moonshot AI (Kimi + Kimi Coding)](https://docs.openclaw.ai/providers/moonshot)
*   [NVIDIA](https://docs.openclaw.ai/providers/nvidia)
*   [Ollama (local models)](https://docs.openclaw.ai/providers/ollama)
*   [OpenAI (API + Codex)](https://docs.openclaw.ai/providers/openai)
*   [OpenCode Zen](https://docs.openclaw.ai/providers/opencode)
*   [OpenRouter](https://docs.openclaw.ai/providers/openrouter)
*   [Qianfan](https://docs.openclaw.ai/providers/qianfan)
*   [Qwen (OAuth)](https://docs.openclaw.ai/providers/qwen)
*   [Together AI](https://docs.openclaw.ai/providers/together)
*   [Vercel AI Gateway](https://docs.openclaw.ai/providers/vercel-ai-gateway)
*   [Venice (Venice AI, privacy-focused)](https://docs.openclaw.ai/providers/venice)
*   [vLLM (local models)](https://docs.openclaw.ai/providers/vllm)
*   [Xiaomi](https://docs.openclaw.ai/providers/xiaomi)
*   [Z.AI](https://docs.openclaw.ai/providers/zai)

## Transcription providers

*   [Deepgram (audio transcription)](https://docs.openclaw.ai/providers/deepgram)

*   [Claude Max API Proxy](https://docs.openclaw.ai/providers/claude-max-api-proxy) - Community proxy for Claude subscription credentials (verify Anthropic policy/terms before use)

For the full provider catalog (xAI, Groq, Mistral, etc.) and advanced configuration, see [Model providers](https://docs.openclaw.ai/concepts/model-providers).

---

<!-- SOURCE: https://docs.openclaw.ai/providers/models -->

# Model Provider Quickstart - OpenClaw

## Model Providers

OpenClaw can use many LLM providers. Pick one, authenticate, then set the default model as `provider/model`.

## Quick start (two steps)

1.  Authenticate with the provider (usually via `openclaw onboard`).
2.  Set the default model:

```
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

## Supported providers (starter set)

*   [OpenAI (API + Codex)](https://docs.openclaw.ai/providers/openai)
*   [Anthropic (API + Claude Code CLI)](https://docs.openclaw.ai/providers/anthropic)
*   [OpenRouter](https://docs.openclaw.ai/providers/openrouter)
*   [Vercel AI Gateway](https://docs.openclaw.ai/providers/vercel-ai-gateway)
*   [Cloudflare AI Gateway](https://docs.openclaw.ai/providers/cloudflare-ai-gateway)
*   [Moonshot AI (Kimi + Kimi Coding)](https://docs.openclaw.ai/providers/moonshot)
*   [Mistral](https://docs.openclaw.ai/providers/mistral)
*   [Synthetic](https://docs.openclaw.ai/providers/synthetic)
*   [OpenCode Zen](https://docs.openclaw.ai/providers/opencode)
*   [Z.AI](https://docs.openclaw.ai/providers/zai)
*   [GLM models](https://docs.openclaw.ai/providers/glm)
*   [MiniMax](https://docs.openclaw.ai/providers/minimax)
*   [Venice (Venice AI)](https://docs.openclaw.ai/providers/venice)
*   [Amazon Bedrock](https://docs.openclaw.ai/providers/bedrock)
*   [Qianfan](https://docs.openclaw.ai/providers/qianfan)

For the full provider catalog (xAI, Groq, Mistral, etc.) and advanced configuration, see [Model providers](https://docs.openclaw.ai/concepts/model-providers).

---

<!-- SOURCE: https://docs.openclaw.ai/providers/vercel-ai-gateway -->

# Vercel AI Gateway - OpenClaw

The [Vercel AI Gateway](https://vercel.com/ai-gateway) provides a unified API to access hundreds of models through a single endpoint.

*   Provider: `vercel-ai-gateway`
*   Auth: `AI_GATEWAY_API_KEY`
*   API: Anthropic Messages compatible
*   OpenClaw auto-discovers the Gateway `/v1/models` catalog, so `/models vercel-ai-gateway` includes current model refs such as `vercel-ai-gateway/openai/gpt-5.4`.

## Quick start

1.  Set the API key (recommended: store it for the Gateway):

```
openclaw onboard --auth-choice ai-gateway-api-key
```

2.  Set a default model:

```
{
  agents: {
    defaults: {
      model: { primary: "vercel-ai-gateway/anthropic/claude-opus-4.6" },
    },
  },
}
```

## Non-interactive example

```
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice ai-gateway-api-key \
  --ai-gateway-api-key "$AI_GATEWAY_API_KEY"
```

## Environment note

If the Gateway runs as a daemon (launchd/systemd), make sure `AI_GATEWAY_API_KEY` is available to that process (for example, in `~/.openclaw/.env` or via `env.shellEnv`).

## Model ID shorthand

OpenClaw accepts Vercel Claude shorthand model refs and normalizes them at runtime:

*   `vercel-ai-gateway/claude-opus-4.6` -> `vercel-ai-gateway/anthropic/claude-opus-4.6`
*   `vercel-ai-gateway/opus-4.6` -> `vercel-ai-gateway/anthropic/claude-opus-4-6`

---

<!-- SOURCE: https://docs.openclaw.ai/providers/venice -->

# Venice AI - OpenClaw

## Venice AI (Venice highlight)

**Venice** is our highlight Venice setup for privacy-first inference with optional anonymized access to proprietary models. Venice AI provides privacy-focused AI inference with support for uncensored models and access to major proprietary models through their anonymized proxy. All inference is private by default—no training on your data, no logging.

## Why Venice in OpenClaw

*   **Private inference** for open-source models (no logging).
*   **Uncensored models** when you need them.
*   **Anonymized access** to proprietary models (Opus/GPT/Gemini) when quality matters.
*   OpenAI-compatible `/v1` endpoints.

## Privacy Modes

Venice offers two privacy levels — understanding this is key to choosing your model:

| Mode | Description | Models |
| --- | --- | --- |
| **Private** | Fully private. Prompts/responses are **never stored or logged**. Ephemeral. | Llama, Qwen, DeepSeek, Kimi, MiniMax, Venice Uncensored, etc. |
| **Anonymized** | Proxied through Venice with metadata stripped. The underlying provider (OpenAI, Anthropic, Google, xAI) sees anonymized requests. | Claude, GPT, Gemini, Grok |

## Features

*   **Privacy-focused**: Choose between “private” (fully private) and “anonymized” (proxied) modes
*   **Uncensored models**: Access to models without content restrictions
*   **Major model access**: Use Claude, GPT, Gemini, and Grok via Venice’s anonymized proxy
*   **OpenAI-compatible API**: Standard `/v1` endpoints for easy integration
*   **Streaming**: ✅ Supported on all models
*   **Function calling**: ✅ Supported on select models (check model capabilities)
*   **Vision**: ✅ Supported on models with vision capability
*   **No hard rate limits**: Fair-use throttling may apply for extreme usage

## Setup

### 1\. Get API Key

1.  Sign up at [venice.ai](https://venice.ai/)
2.  Go to **Settings → API Keys → Create new key**
3.  Copy your API key (format: `vapi_xxxxxxxxxxxx`)

### 2\. Configure OpenClaw

**Option A: Environment Variable**

```
export VENICE_API_KEY="vapi_xxxxxxxxxxxx"
```

**Option B: Interactive Setup (Recommended)**

```
openclaw onboard --auth-choice venice-api-key
```

This will:

1.  Prompt for your API key (or use existing `VENICE_API_KEY`)
2.  Show all available Venice models
3.  Let you pick your default model
4.  Configure the provider automatically

**Option C: Non-interactive**

```
openclaw onboard --non-interactive \
  --auth-choice venice-api-key \
  --venice-api-key "vapi_xxxxxxxxxxxx"
```

### 3\. Verify Setup

```
openclaw agent --model venice/kimi-k2-5 --message "Hello, are you working?"
```

## Model Selection

After setup, OpenClaw shows all available Venice models. Pick based on your needs:

*   **Default model**: `venice/kimi-k2-5` for strong private reasoning plus vision.
*   **High-capability option**: `venice/claude-opus-4-6` for the strongest anonymized Venice path.
*   **Privacy**: Choose “private” models for fully private inference.
*   **Capability**: Choose “anonymized” models to access Claude, GPT, Gemini via Venice’s proxy.

Change your default model anytime:

```
openclaw models set venice/kimi-k2-5
openclaw models set venice/claude-opus-4-6
```

List all available models:

```
openclaw models list | grep venice
```

## Configure via `openclaw configure`

1.  Run `openclaw configure`
2.  Select **Model/auth**
3.  Choose **Venice AI**

## Which Model Should I Use?

| Use Case | Recommended Model | Why |
| --- | --- | --- |
| **General chat (default)** | `kimi-k2-5` | Strong private reasoning plus vision |
| **Best overall quality** | `claude-opus-4-6` | Strongest anonymized Venice option |
| **Privacy + coding** | `qwen3-coder-480b-a35b-instruct` | Private coding model with large context |
| **Private vision** | `kimi-k2-5` | Vision support without leaving private mode |
| **Fast + cheap** | `qwen3-4b` | Lightweight reasoning model |
| **Complex private tasks** | `deepseek-v3.2` | Strong reasoning, but no Venice tool support |
| **Uncensored** | `venice-uncensored` | No content restrictions |

## Available Models (41 Total)

### Private Models (26) — Fully Private, No Logging

| Model ID | Name | Context | Features |
| --- | --- | --- | --- |
| `kimi-k2-5` | Kimi K2.5 | 256k | Default, reasoning, vision |
| `kimi-k2-thinking` | Kimi K2 Thinking | 256k | Reasoning |
| `llama-3.3-70b` | Llama 3.3 70B | 128k | General |
| `llama-3.2-3b` | Llama 3.2 3B | 128k | General |
| `hermes-3-llama-3.1-405b` | Hermes 3 Llama 3.1 405B | 128k | General, tools disabled |
| `qwen3-235b-a22b-thinking-2507` | Qwen3 235B Thinking | 128k | Reasoning |
| `qwen3-235b-a22b-instruct-2507` | Qwen3 235B Instruct | 128k | General |
| `qwen3-coder-480b-a35b-instruct` | Qwen3 Coder 480B | 256k | Coding |
| `qwen3-coder-480b-a35b-instruct-turbo` | Qwen3 Coder 480B Turbo | 256k | Coding |
| `qwen3-5-35b-a3b` | Qwen3.5 35B A3B | 256k | Reasoning, vision |
| `qwen3-next-80b` | Qwen3 Next 80B | 256k | General |
| `qwen3-vl-235b-a22b` | Qwen3 VL 235B (Vision) | 256k | Vision |
| `qwen3-4b` | Venice Small (Qwen3 4B) | 32k | Fast, reasoning |
| `deepseek-v3.2` | DeepSeek V3.2 | 160k | Reasoning, tools disabled |
| `venice-uncensored` | Venice Uncensored (Dolphin-Mistral) | 32k | Uncensored, tools disabled |
| `mistral-31-24b` | Venice Medium (Mistral) | 128k | Vision |
| `google-gemma-3-27b-it` | Google Gemma 3 27B Instruct | 198k | Vision |
| `openai-gpt-oss-120b` | OpenAI GPT OSS 120B | 128k | General |
| `nvidia-nemotron-3-nano-30b-a3b` | NVIDIA Nemotron 3 Nano 30B | 128k | General |
| `olafangensan-glm-4.7-flash-heretic` | GLM 4.7 Flash Heretic | 128k | Reasoning |
| `zai-org-glm-4.6` | GLM 4.6 | 198k | General |
| `zai-org-glm-4.7` | GLM 4.7 | 198k | Reasoning |
| `zai-org-glm-4.7-flash` | GLM 4.7 Flash | 128k | Reasoning |
| `zai-org-glm-5` | GLM 5 | 198k | Reasoning |
| `minimax-m21` | MiniMax M2.1 | 198k | Reasoning |
| `minimax-m25` | MiniMax M2.5 | 198k | Reasoning |

### Anonymized Models (15) — Via Venice Proxy

| Model ID | Name | Context | Features |
| --- | --- | --- | --- |
| `claude-opus-4-6` | Claude Opus 4.6 (via Venice) | 1M  | Reasoning, vision |
| `claude-opus-4-5` | Claude Opus 4.5 (via Venice) | 198k | Reasoning, vision |
| `claude-sonnet-4-6` | Claude Sonnet 4.6 (via Venice) | 1M  | Reasoning, vision |
| `claude-sonnet-4-5` | Claude Sonnet 4.5 (via Venice) | 198k | Reasoning, vision |
| `openai-gpt-54` | GPT-5.4 (via Venice) | 1M  | Reasoning, vision |
| `openai-gpt-53-codex` | GPT-5.3 Codex (via Venice) | 400k | Reasoning, vision, coding |
| `openai-gpt-52` | GPT-5.2 (via Venice) | 256k | Reasoning |
| `openai-gpt-52-codex` | GPT-5.2 Codex (via Venice) | 256k | Reasoning, vision, coding |
| `openai-gpt-4o-2024-11-20` | GPT-4o (via Venice) | 128k | Vision |
| `openai-gpt-4o-mini-2024-07-18` | GPT-4o Mini (via Venice) | 128k | Vision |
| `gemini-3-1-pro-preview` | Gemini 3.1 Pro (via Venice) | 1M  | Reasoning, vision |
| `gemini-3-pro-preview` | Gemini 3 Pro (via Venice) | 198k | Reasoning, vision |
| `gemini-3-flash-preview` | Gemini 3 Flash (via Venice) | 256k | Reasoning, vision |
| `grok-41-fast` | Grok 4.1 Fast (via Venice) | 1M  | Reasoning, vision |
| `grok-code-fast-1` | Grok Code Fast 1 (via Venice) | 256k | Reasoning, coding |

## Model Discovery

OpenClaw automatically discovers models from the Venice API when `VENICE_API_KEY` is set. If the API is unreachable, it falls back to a static catalog. The `/models` endpoint is public (no auth needed for listing), but inference requires a valid API key.

| Feature | Support |
| --- | --- |
| **Streaming** | ✅ All models |
| **Function calling** | ✅ Most models (check `supportsFunctionCalling` in API) |
| **Vision/Images** | ✅ Models marked with “Vision” feature |
| **JSON mode** | ✅ Supported via `response_format` |

## Pricing

Venice uses a credit-based system. Check [venice.ai/pricing](https://venice.ai/pricing) for current rates:

*   **Private models**: Generally lower cost
*   **Anonymized models**: Similar to direct API pricing + small Venice fee

## Comparison: Venice vs Direct API

| Aspect | Venice (Anonymized) | Direct API |
| --- | --- | --- |
| **Privacy** | Metadata stripped, anonymized | Your account linked |
| **Latency** | +10-50ms (proxy) | Direct |
| **Features** | Most features supported | Full features |
| **Billing** | Venice credits | Provider billing |

## Usage Examples

```
# Use the default private model
openclaw agent --model venice/kimi-k2-5 --message "Quick health check"

# Use Claude Opus via Venice (anonymized)
openclaw agent --model venice/claude-opus-4-6 --message "Summarize this task"

# Use uncensored model
openclaw agent --model venice/venice-uncensored --message "Draft options"

# Use vision model with image
openclaw agent --model venice/qwen3-vl-235b-a22b --message "Review attached image"

# Use coding model
openclaw agent --model venice/qwen3-coder-480b-a35b-instruct --message "Refactor this function"
```

## Troubleshooting

### API key not recognized

```
echo $VENICE_API_KEY
openclaw models list | grep venice
```

Ensure the key starts with `vapi_`.

### Model not available

The Venice model catalog updates dynamically. Run `openclaw models list` to see currently available models. Some models may be temporarily offline.

### Connection issues

Venice API is at `https://api.venice.ai/api/v1`. Ensure your network allows HTTPS connections.

## Config file example

```
{
  env: { VENICE_API_KEY: "vapi_..." },
  agents: { defaults: { model: { primary: "venice/kimi-k2-5" } } },
  models: {
    mode: "merge",
    providers: {
      venice: {
        baseUrl: "https://api.venice.ai/api/v1",
        apiKey: "${VENICE_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "kimi-k2-5",
            name: "Kimi K2.5",
            reasoning: true,
            input: ["text", "image"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

## Links

*   [Venice AI](https://venice.ai/)
*   [API Documentation](https://docs.venice.ai/)
*   [Pricing](https://venice.ai/pricing)
*   [Status](https://status.venice.ai/)

---

<!-- SOURCE: https://docs.openclaw.ai/providers/xiaomi -->

# Xiaomi MiMo - OpenClaw

Xiaomi MiMo is the API platform for **MiMo** models. It provides REST APIs compatible with OpenAI and Anthropic formats and uses API keys for authentication. Create your API key in the [Xiaomi MiMo console](https://platform.xiaomimimo.com/#/console/api-keys). OpenClaw uses the `xiaomi` provider with a Xiaomi MiMo API key.

## Model overview

*   **mimo-v2-flash**: 262144-token context window, Anthropic Messages API compatible.
*   Base URL: `https://api.xiaomimimo.com/anthropic`
*   Authorization: `Bearer $XIAOMI_API_KEY`

## CLI setup

```
openclaw onboard --auth-choice xiaomi-api-key
# or non-interactive
openclaw onboard --auth-choice xiaomi-api-key --xiaomi-api-key "$XIAOMI_API_KEY"
```

## Config snippet

```
{
  env: { XIAOMI_API_KEY: "your-key" },
  agents: { defaults: { model: { primary: "xiaomi/mimo-v2-flash" } } },
  models: {
    mode: "merge",
    providers: {
      xiaomi: {
        baseUrl: "https://api.xiaomimimo.com/anthropic",
        api: "anthropic-messages",
        apiKey: "XIAOMI_API_KEY",
        models: [
          {
            id: "mimo-v2-flash",
            name: "Xiaomi MiMo V2 Flash",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 262144,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## Notes

*   Model ref: `xiaomi/mimo-v2-flash`.
*   The provider is injected automatically when `XIAOMI_API_KEY` is set (or an auth profile exists).
*   See [/concepts/model-providers](https://docs.openclaw.ai/concepts/model-providers) for provider rules.

---

<!-- SOURCE: https://docs.openclaw.ai/providers/zai -->

# Z.AI - OpenClaw

Z.AI is the API platform for **GLM** models. It provides REST APIs for GLM and uses API keys for authentication. Create your API key in the Z.AI console. OpenClaw uses the `zai` provider with a Z.AI API key.

## CLI setup

```
openclaw onboard --auth-choice zai-api-key
# or non-interactive
openclaw onboard --zai-api-key "$ZAI_API_KEY"
```

## Config snippet

```
{
  env: { ZAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "zai/glm-5" } } },
}
```

## Notes

*   GLM models are available as `zai/<model>` (example: `zai/glm-5`).
*   `tool_stream` is enabled by default for Z.AI tool-call streaming. Set `agents.defaults.models["zai/<model>"].params.tool_stream` to `false` to disable it.
*   See [/providers/glm](https://docs.openclaw.ai/providers/glm) for the model family overview.
*   Z.AI uses Bearer auth with your API key.

---

<!-- SOURCE: https://docs.openclaw.ai/providers/anthropic -->

# Anthropic - OpenClaw

## Anthropic (Claude)

Anthropic builds the **Claude** model family and provides access via an API. In OpenClaw you can authenticate with an API key or a **setup-token**.

## Option A: Anthropic API key

**Best for:** standard API access and usage-based billing. Create your API key in the Anthropic Console.

### CLI setup

```
openclaw onboard
# choose: Anthropic API key

# or non-interactive
openclaw onboard --anthropic-api-key "$ANTHROPIC_API_KEY"
```

### Config snippet

```
{
  env: { ANTHROPIC_API_KEY: "sk-ant-..." },
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

## Thinking defaults (Claude 4.6)

*   Anthropic Claude 4.6 models default to `adaptive` thinking in OpenClaw when no explicit thinking level is set.
*   You can override per-message (`/think:<level>`) or in model params: `agents.defaults.models["anthropic/<model>"].params.thinking`.
*   Related Anthropic docs:
    *   [Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking)
    *   [Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)

## Prompt caching (Anthropic API)

OpenClaw supports Anthropic’s prompt caching feature. This is **API-only**; subscription auth does not honor cache settings.

### Configuration

Use the `cacheRetention` parameter in your model config:

| Value | Cache Duration | Description |
| --- | --- | --- |
| `none` | No caching | Disable prompt caching |
| `short` | 5 minutes | Default for API Key auth |
| `long` | 1 hour | Extended cache (requires beta flag) |

```
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": {
          params: { cacheRetention: "long" },
        },
      },
    },
  },
}
```

### Defaults

When using Anthropic API Key authentication, OpenClaw automatically applies `cacheRetention: "short"` (5-minute cache) for all Anthropic models. You can override this by explicitly setting `cacheRetention` in your config.

### Per-agent cacheRetention overrides

Use model-level params as your baseline, then override specific agents via `agents.list[].params`.

```
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-opus-4-6" },
      models: {
        "anthropic/claude-opus-4-6": {
          params: { cacheRetention: "long" }, // baseline for most agents
        },
      },
    },
    list: [
      { id: "research", default: true },
      { id: "alerts", params: { cacheRetention: "none" } }, // override for this agent only
    ],
  },
}
```

Config merge order for cache-related params:

1.  `agents.defaults.models["provider/model"].params`
2.  `agents.list[].params` (matching `id`, overrides by key)

This lets one agent keep a long-lived cache while another agent on the same model disables caching to avoid write costs on bursty/low-reuse traffic.

### Bedrock Claude notes

*   Anthropic Claude models on Bedrock (`amazon-bedrock/*anthropic.claude*`) accept `cacheRetention` pass-through when configured.
*   Non-Anthropic Bedrock models are forced to `cacheRetention: "none"` at runtime.
*   Anthropic API-key smart defaults also seed `cacheRetention: "short"` for Claude-on-Bedrock model refs when no explicit value is set.

### Legacy parameter

The older `cacheControlTtl` parameter is still supported for backwards compatibility:

*   `"5m"` maps to `short`
*   `"1h"` maps to `long`

We recommend migrating to the new `cacheRetention` parameter. OpenClaw includes the `extended-cache-ttl-2025-04-11` beta flag for Anthropic API requests; keep it if you override provider headers (see [/gateway/configuration](https://docs.openclaw.ai/gateway/configuration)).

## 1M context window (Anthropic beta)

Anthropic’s 1M context window is beta-gated. In OpenClaw, enable it per model with `params.context1m: true` for supported Opus/Sonnet models.

```
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": {
          params: { context1m: true },
        },
      },
    },
  },
}
```

OpenClaw maps this to `anthropic-beta: context-1m-2025-08-07` on Anthropic requests. This only activates when `params.context1m` is explicitly set to `true` for that model. Requirement: Anthropic must allow long-context usage on that credential (typically API key billing, or a subscription account with Extra Usage enabled). Otherwise Anthropic returns: `HTTP 429: rate_limit_error: Extra usage is required for long context requests`. Note: Anthropic currently rejects `context-1m-*` beta requests when using OAuth/subscription tokens (`sk-ant-oat-*`). OpenClaw automatically skips the context1m beta header for OAuth auth and keeps the required OAuth betas.

## Option B: Claude setup-token

**Best for:** using your Claude subscription.

### Where to get a setup-token

Setup-tokens are created by the **Claude Code CLI**, not the Anthropic Console. You can run this on **any machine**:

Paste the token into OpenClaw (wizard: **Anthropic token (paste setup-token)**), or run it on the gateway host:

```
openclaw models auth setup-token --provider anthropic
```

If you generated the token on a different machine, paste it:

```
openclaw models auth paste-token --provider anthropic
```

### CLI setup (setup-token)

```
# Paste a setup-token during onboarding
openclaw onboard --auth-choice setup-token
```

### Config snippet (setup-token)

```
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}
```

## Notes

*   Generate the setup-token with `claude setup-token` and paste it, or run `openclaw models auth setup-token` on the gateway host.
*   If you see “OAuth token refresh failed …” on a Claude subscription, re-auth with a setup-token. See [/gateway/troubleshooting#oauth-token-refresh-failed-anthropic-claude-subscription](https://docs.openclaw.ai/gateway/troubleshooting#oauth-token-refresh-failed-anthropic-claude-subscription).
*   Auth details + reuse rules are in [/concepts/oauth](https://docs.openclaw.ai/concepts/oauth).

## Troubleshooting

**401 errors / token suddenly invalid**

*   Claude subscription auth can expire or be revoked. Re-run `claude setup-token` and paste it into the **gateway host**.
*   If the Claude CLI login lives on a different machine, use `openclaw models auth paste-token --provider anthropic` on the gateway host.

**No API key found for provider “anthropic”**

*   Auth is **per agent**. New agents don’t inherit the main agent’s keys.
*   Re-run onboarding for that agent, or paste a setup-token / API key on the gateway host, then verify with `openclaw models status`.

**No credentials found for profile `anthropic:default`**

*   Run `openclaw models status` to see which auth profile is active.
*   Re-run onboarding, or paste a setup-token / API key for that profile.

**No available auth profile (all in cooldown/unavailable)**

*   Check `openclaw models status --json` for `auth.unusableProfiles`.
*   Add another Anthropic profile or wait for cooldown.

More: [/gateway/troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting) and [/help/faq](https://docs.openclaw.ai/help/faq).

---

<!-- SOURCE: https://docs.openclaw.ai/providers/bedrock -->

# Amazon Bedrock - OpenClaw

OpenClaw can use **Amazon Bedrock** models via pi‑ai’s **Bedrock Converse** streaming provider. Bedrock auth uses the **AWS SDK default credential chain**, not an API key.

## What pi‑ai supports

*   Provider: `amazon-bedrock`
*   API: `bedrock-converse-stream`
*   Auth: AWS credentials (env vars, shared config, or instance role)
*   Region: `AWS_REGION` or `AWS_DEFAULT_REGION` (default: `us-east-1`)

## Automatic model discovery

If AWS credentials are detected, OpenClaw can automatically discover Bedrock models that support **streaming** and **text output**. Discovery uses `bedrock:ListFoundationModels` and is cached (default: 1 hour). Config options live under `models.bedrockDiscovery`:

```
{
  models: {
    bedrockDiscovery: {
      enabled: true,
      region: "us-east-1",
      providerFilter: ["anthropic", "amazon"],
      refreshInterval: 3600,
      defaultContextWindow: 32000,
      defaultMaxTokens: 4096,
    },
  },
}
```

Notes:

*   `enabled` defaults to `true` when AWS credentials are present.
*   `region` defaults to `AWS_REGION` or `AWS_DEFAULT_REGION`, then `us-east-1`.
*   `providerFilter` matches Bedrock provider names (for example `anthropic`).
*   `refreshInterval` is seconds; set to `0` to disable caching.
*   `defaultContextWindow` (default: `32000`) and `defaultMaxTokens` (default: `4096`) are used for discovered models (override if you know your model limits).

## Onboarding

1.  Ensure AWS credentials are available on the **gateway host**:

```
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION="us-east-1"
# Optional:
export AWS_SESSION_TOKEN="..."
export AWS_PROFILE="your-profile"
# Optional (Bedrock API key/bearer token):
export AWS_BEARER_TOKEN_BEDROCK="..."
```

2.  Add a Bedrock provider and model to your config (no `apiKey` required):

```
{
  models: {
    providers: {
      "amazon-bedrock": {
        baseUrl: "https://bedrock-runtime.us-east-1.amazonaws.com",
        api: "bedrock-converse-stream",
        auth: "aws-sdk",
        models: [
          {
            id: "us.anthropic.claude-opus-4-6-v1:0",
            name: "Claude Opus 4.6 (Bedrock)",
            reasoning: true,
            input: ["text", "image"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
  agents: {
    defaults: {
      model: { primary: "amazon-bedrock/us.anthropic.claude-opus-4-6-v1:0" },
    },
  },
}
```

## EC2 Instance Roles

When running OpenClaw on an EC2 instance with an IAM role attached, the AWS SDK will automatically use the instance metadata service (IMDS) for authentication. However, OpenClaw’s credential detection currently only checks for environment variables, not IMDS credentials. **Workaround:** Set `AWS_PROFILE=default` to signal that AWS credentials are available. The actual authentication still uses the instance role via IMDS.

```
# Add to ~/.bashrc or your shell profile
export AWS_PROFILE=default
export AWS_REGION=us-east-1
```

**Required IAM permissions** for the EC2 instance role:

*   `bedrock:InvokeModel`
*   `bedrock:InvokeModelWithResponseStream`
*   `bedrock:ListFoundationModels` (for automatic discovery)

Or attach the managed policy `AmazonBedrockFullAccess`.

## Quick setup (AWS path)

```
# 1. Create IAM role and instance profile
aws iam create-role --role-name EC2-Bedrock-Access \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy --role-name EC2-Bedrock-Access \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

aws iam create-instance-profile --instance-profile-name EC2-Bedrock-Access
aws iam add-role-to-instance-profile \
  --instance-profile-name EC2-Bedrock-Access \
  --role-name EC2-Bedrock-Access

# 2. Attach to your EC2 instance
aws ec2 associate-iam-instance-profile \
  --instance-id i-xxxxx \
  --iam-instance-profile Name=EC2-Bedrock-Access

# 3. On the EC2 instance, enable discovery
openclaw config set models.bedrockDiscovery.enabled true
openclaw config set models.bedrockDiscovery.region us-east-1

# 4. Set the workaround env vars
echo 'export AWS_PROFILE=default' >> ~/.bashrc
echo 'export AWS_REGION=us-east-1' >> ~/.bashrc
source ~/.bashrc

# 5. Verify models are discovered
openclaw models list
```

## Notes

*   Bedrock requires **model access** enabled in your AWS account/region.
*   Automatic discovery needs the `bedrock:ListFoundationModels` permission.
*   If you use profiles, set `AWS_PROFILE` on the gateway host.
*   OpenClaw surfaces the credential source in this order: `AWS_BEARER_TOKEN_BEDROCK`, then `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`, then `AWS_PROFILE`, then the default AWS SDK chain.
*   Reasoning support depends on the model; check the Bedrock model card for current capabilities.
*   If you prefer a managed key flow, you can also place an OpenAI‑compatible proxy in front of Bedrock and configure it as an OpenAI provider instead.

---

<!-- SOURCE: https://docs.openclaw.ai/providers/deepgram -->

# Deepgram - OpenClaw

## Deepgram (Audio Transcription)

Deepgram is a speech-to-text API. In OpenClaw it is used for **inbound audio/voice note transcription** via `tools.media.audio`. When enabled, OpenClaw uploads the audio file to Deepgram and injects the transcript into the reply pipeline (`{{Transcript}}` + `[Audio]` block). This is **not streaming**; it uses the pre-recorded transcription endpoint. Website: [https://deepgram.com](https://deepgram.com/)  
Docs: [https://developers.deepgram.com](https://developers.deepgram.com/)

## Quick start

1.  Set your API key:

2.  Enable the provider:

```
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "deepgram", model: "nova-3" }],
      },
    },
  },
}
```

## Options

*   `model`: Deepgram model id (default: `nova-3`)
*   `language`: language hint (optional)
*   `tools.media.audio.providerOptions.deepgram.detect_language`: enable language detection (optional)
*   `tools.media.audio.providerOptions.deepgram.punctuate`: enable punctuation (optional)
*   `tools.media.audio.providerOptions.deepgram.smart_format`: enable smart formatting (optional)

Example with language:

```
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "deepgram", model: "nova-3", language: "en" }],
      },
    },
  },
}
```

Example with Deepgram options:

```
{
  tools: {
    media: {
      audio: {
        enabled: true,
        providerOptions: {
          deepgram: {
            detect_language: true,
            punctuate: true,
            smart_format: true,
          },
        },
        models: [{ provider: "deepgram", model: "nova-3" }],
      },
    },
  },
}
```

## Notes

*   Authentication follows the standard provider auth order; `DEEPGRAM_API_KEY` is the simplest path.
*   Override endpoints or headers with `tools.media.audio.baseUrl` and `tools.media.audio.headers` when using a proxy.
*   Output follows the same audio rules as other providers (size caps, timeouts, transcript injection).

---

<!-- SOURCE: https://docs.openclaw.ai/providers/cloudflare-ai-gateway -->

# Cloudflare AI Gateway - OpenClaw

Cloudflare AI Gateway sits in front of provider APIs and lets you add analytics, caching, and controls. For Anthropic, OpenClaw uses the Anthropic Messages API through your Gateway endpoint.

*   Provider: `cloudflare-ai-gateway`
*   Base URL: `https://gateway.ai.cloudflare.com/v1/<account_id>/<gateway_id>/anthropic`
*   Default model: `cloudflare-ai-gateway/claude-sonnet-4-5`
*   API key: `CLOUDFLARE_AI_GATEWAY_API_KEY` (your provider API key for requests through the Gateway)

For Anthropic models, use your Anthropic API key.

## Quick start

1.  Set the provider API key and Gateway details:

```
openclaw onboard --auth-choice cloudflare-ai-gateway-api-key
```

2.  Set a default model:

```
{
  agents: {
    defaults: {
      model: { primary: "cloudflare-ai-gateway/claude-sonnet-4-5" },
    },
  },
}
```

## Non-interactive example

```
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice cloudflare-ai-gateway-api-key \
  --cloudflare-ai-gateway-account-id "your-account-id" \
  --cloudflare-ai-gateway-gateway-id "your-gateway-id" \
  --cloudflare-ai-gateway-api-key "$CLOUDFLARE_AI_GATEWAY_API_KEY"
```

## Authenticated gateways

If you enabled Gateway authentication in Cloudflare, add the `cf-aig-authorization` header (this is in addition to your provider API key).

```
{
  models: {
    providers: {
      "cloudflare-ai-gateway": {
        headers: {
          "cf-aig-authorization": "Bearer <cloudflare-ai-gateway-token>",
        },
      },
    },
  },
}
```

## Environment note

If the Gateway runs as a daemon (launchd/systemd), make sure `CLOUDFLARE_AI_GATEWAY_API_KEY` is available to that process (for example, in `~/.openclaw/.env` or via `env.shellEnv`).

---

<!-- SOURCE: https://docs.openclaw.ai/providers/kilocode -->

# Kilocode - OpenClaw

## Kilo Gateway

Kilo Gateway provides a **unified API** that routes requests to many models behind a single endpoint and API key. It is OpenAI-compatible, so most OpenAI SDKs work by switching the base URL.

## Getting an API key

1.  Go to [app.kilo.ai](https://app.kilo.ai/)
2.  Sign in or create an account
3.  Navigate to API Keys and generate a new key

## CLI setup

```
openclaw onboard --kilocode-api-key <key>
```

Or set the environment variable:

```
export KILOCODE_API_KEY="<your-kilocode-api-key>" # pragma: allowlist secret
```

## Config snippet

```
{
  env: { KILOCODE_API_KEY: "<your-kilocode-api-key>" }, // pragma: allowlist secret
  agents: {
    defaults: {
      model: { primary: "kilocode/kilo/auto" },
    },
  },
}
```

## Default model

The default model is `kilocode/kilo/auto`, a smart routing model that automatically selects the best underlying model based on the task:

*   Planning, debugging, and orchestration tasks route to Claude Opus
*   Code writing and exploration tasks route to Claude Sonnet

## Available models

OpenClaw dynamically discovers available models from the Kilo Gateway at startup. Use `/models kilocode` to see the full list of models available with your account. Any model available on the gateway can be used with the `kilocode/` prefix:

```
kilocode/kilo/auto              (default - smart routing)
kilocode/anthropic/claude-sonnet-4
kilocode/openai/gpt-5.2
kilocode/google/gemini-3-pro-preview
...and many more
```

## Notes

*   Model refs are `kilocode/<model-id>` (e.g., `kilocode/anthropic/claude-sonnet-4`).
*   Default model: `kilocode/kilo/auto`
*   Base URL: `https://api.kilo.ai/api/gateway/`
*   For more model/provider options, see [/concepts/model-providers](https://docs.openclaw.ai/concepts/model-providers).
*   Kilo Gateway uses a Bearer token with your API key under the hood.

---

<!-- SOURCE: https://docs.openclaw.ai/providers/github-copilot -->

# GitHub Copilot - OpenClaw

## What is GitHub Copilot?

GitHub Copilot is GitHub’s AI coding assistant. It provides access to Copilot models for your GitHub account and plan. OpenClaw can use Copilot as a model provider in two different ways.

## Two ways to use Copilot in OpenClaw

### 1) Built-in GitHub Copilot provider (`github-copilot`)

Use the native device-login flow to obtain a GitHub token, then exchange it for Copilot API tokens when OpenClaw runs. This is the **default** and simplest path because it does not require VS Code.

### 2) Copilot Proxy plugin (`copilot-proxy`)

Use the **Copilot Proxy** VS Code extension as a local bridge. OpenClaw talks to the proxy’s `/v1` endpoint and uses the model list you configure there. Choose this when you already run Copilot Proxy in VS Code or need to route through it. You must enable the plugin and keep the VS Code extension running. Use GitHub Copilot as a model provider (`github-copilot`). The login command runs the GitHub device flow, saves an auth profile, and updates your config to use that profile.

## CLI setup

```
openclaw models auth login-github-copilot
```

You’ll be prompted to visit a URL and enter a one-time code. Keep the terminal open until it completes.

### Optional flags

```
openclaw models auth login-github-copilot --profile-id github-copilot:work
openclaw models auth login-github-copilot --yes
```

## Set a default model

```
openclaw models set github-copilot/gpt-4o
```

### Config snippet

```
{
  agents: { defaults: { model: { primary: "github-copilot/gpt-4o" } } },
}
```

## Notes

*   Requires an interactive TTY; run it directly in a terminal.
*   Copilot model availability depends on your plan; if a model is rejected, try another ID (for example `github-copilot/gpt-4.1`).
*   The login stores a GitHub token in the auth profile store and exchanges it for a Copilot API token when OpenClaw runs.

---

<!-- SOURCE: https://docs.openclaw.ai/providers/huggingface -->

# Hugging Face (Inference) - OpenClaw

[Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers) offer OpenAI-compatible chat completions through a single router API. You get access to many models (DeepSeek, Llama, and more) with one token. OpenClaw uses the **OpenAI-compatible endpoint** (chat completions only); for text-to-image, embeddings, or speech use the [HF inference clients](https://huggingface.co/docs/api-inference/quicktour) directly.

*   Provider: `huggingface`
*   Auth: `HUGGINGFACE_HUB_TOKEN` or `HF_TOKEN` (fine-grained token with **Make calls to Inference Providers**)
*   API: OpenAI-compatible (`https://router.huggingface.co/v1`)
*   Billing: Single HF token; [pricing](https://huggingface.co/docs/inference-providers/pricing) follows provider rates with a free tier.

## Quick start

1.  Create a fine-grained token at [Hugging Face → Settings → Tokens](https://huggingface.co/settings/tokens/new?ownUserPermissions=inference.serverless.write&tokenType=fineGrained) with the **Make calls to Inference Providers** permission.
2.  Run onboarding and choose **Hugging Face** in the provider dropdown, then enter your API key when prompted:

```
openclaw onboard --auth-choice huggingface-api-key
```

3.  In the **Default Hugging Face model** dropdown, pick the model you want (the list is loaded from the Inference API when you have a valid token; otherwise a built-in list is shown). Your choice is saved as the default model.
4.  You can also set or change the default model later in config:

```
{
  agents: {
    defaults: {
      model: { primary: "huggingface/deepseek-ai/DeepSeek-R1" },
    },
  },
}
```

## Non-interactive example

```
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice huggingface-api-key \
  --huggingface-api-key "$HF_TOKEN"
```

This will set `huggingface/deepseek-ai/DeepSeek-R1` as the default model.

## Environment note

If the Gateway runs as a daemon (launchd/systemd), make sure `HUGGINGFACE_HUB_TOKEN` or `HF_TOKEN` is available to that process (for example, in `~/.openclaw/.env` or via `env.shellEnv`).

## Model discovery and onboarding dropdown

OpenClaw discovers models by calling the **Inference endpoint directly**:

```
GET https://router.huggingface.co/v1/models
```

(Optional: send `Authorization: Bearer $HUGGINGFACE_HUB_TOKEN` or `$HF_TOKEN` for the full list; some endpoints return a subset without auth.) The response is OpenAI-style `{ "object": "list", "data": [ { "id": "Qwen/Qwen3-8B", "owned_by": "Qwen", ... }, ... ] }`. When you configure a Hugging Face API key (via onboarding, `HUGGINGFACE_HUB_TOKEN`, or `HF_TOKEN`), OpenClaw uses this GET to discover available chat-completion models. During **interactive onboarding**, after you enter your token you see a **Default Hugging Face model** dropdown populated from that list (or the built-in catalog if the request fails). At runtime (e.g. Gateway startup), when a key is present, OpenClaw again calls **GET** `https://router.huggingface.co/v1/models` to refresh the catalog. The list is merged with a built-in catalog (for metadata like context window and cost). If the request fails or no key is set, only the built-in catalog is used.

## Model names and editable options

*   **Name from API:** The model display name is **hydrated from GET /v1/models** when the API returns `name`, `title`, or `display_name`; otherwise it is derived from the model id (e.g. `deepseek-ai/DeepSeek-R1` → “DeepSeek R1”).
*   **Override display name:** You can set a custom label per model in config so it appears the way you want in the CLI and UI:

```
{
  agents: {
    defaults: {
      models: {
        "huggingface/deepseek-ai/DeepSeek-R1": { alias: "DeepSeek R1 (fast)" },
        "huggingface/deepseek-ai/DeepSeek-R1:cheapest": { alias: "DeepSeek R1 (cheap)" },
      },
    },
  },
}
```

*   **Provider / policy selection:** Append a suffix to the **model id** to choose how the router picks the backend:
    
    *   **`:fastest`** — highest throughput (router picks; provider choice is **locked** — no interactive backend picker).
    *   **`:cheapest`** — lowest cost per output token (router picks; provider choice is **locked**).
    *   **`:provider`** — force a specific backend (e.g. `:sambanova`, `:together`).
    
    When you select **:cheapest** or **:fastest** (e.g. in the onboarding model dropdown), the provider is locked: the router decides by cost or speed and no optional “prefer specific backend” step is shown. You can add these as separate entries in `models.providers.huggingface.models` or set `model.primary` with the suffix. You can also set your default order in [Inference Provider settings](https://hf.co/settings/inference-providers) (no suffix = use that order).
*   **Config merge:** Existing entries in `models.providers.huggingface.models` (e.g. in `models.json`) are kept when config is merged. So any custom `name`, `alias`, or model options you set there are preserved.

## Model IDs and configuration examples

Model refs use the form `huggingface/<org>/<model>` (Hub-style IDs). The list below is from **GET** `https://router.huggingface.co/v1/models`; your catalog may include more. **Example IDs (from the inference endpoint):**

| Model | Ref (prefix with `huggingface/`) |
| --- | --- |
| DeepSeek R1 | `deepseek-ai/DeepSeek-R1` |
| DeepSeek V3.2 | `deepseek-ai/DeepSeek-V3.2` |
| Qwen3 8B | `Qwen/Qwen3-8B` |
| Qwen2.5 7B Instruct | `Qwen/Qwen2.5-7B-Instruct` |
| Qwen3 32B | `Qwen/Qwen3-32B` |
| Llama 3.3 70B Instruct | `meta-llama/Llama-3.3-70B-Instruct` |
| Llama 3.1 8B Instruct | `meta-llama/Llama-3.1-8B-Instruct` |
| GPT-OSS 120B | `openai/gpt-oss-120b` |
| GLM 4.7 | `zai-org/GLM-4.7` |
| Kimi K2.5 | `moonshotai/Kimi-K2.5` |

You can append `:fastest`, `:cheapest`, or `:provider` (e.g. `:together`, `:sambanova`) to the model id. Set your default order in [Inference Provider settings](https://hf.co/settings/inference-providers); see [Inference Providers](https://huggingface.co/docs/inference-providers) and **GET** `https://router.huggingface.co/v1/models` for the full list.

### Complete configuration examples

**Primary DeepSeek R1 with Qwen fallback:**

```
{
  agents: {
    defaults: {
      model: {
        primary: "huggingface/deepseek-ai/DeepSeek-R1",
        fallbacks: ["huggingface/Qwen/Qwen3-8B"],
      },
      models: {
        "huggingface/deepseek-ai/DeepSeek-R1": { alias: "DeepSeek R1" },
        "huggingface/Qwen/Qwen3-8B": { alias: "Qwen3 8B" },
      },
    },
  },
}
```

**Qwen as default, with :cheapest and :fastest variants:**

```
{
  agents: {
    defaults: {
      model: { primary: "huggingface/Qwen/Qwen3-8B" },
      models: {
        "huggingface/Qwen/Qwen3-8B": { alias: "Qwen3 8B" },
        "huggingface/Qwen/Qwen3-8B:cheapest": { alias: "Qwen3 8B (cheapest)" },
        "huggingface/Qwen/Qwen3-8B:fastest": { alias: "Qwen3 8B (fastest)" },
      },
    },
  },
}
```

**DeepSeek + Llama + GPT-OSS with aliases:**

```
{
  agents: {
    defaults: {
      model: {
        primary: "huggingface/deepseek-ai/DeepSeek-V3.2",
        fallbacks: [
          "huggingface/meta-llama/Llama-3.3-70B-Instruct",
          "huggingface/openai/gpt-oss-120b",
        ],
      },
      models: {
        "huggingface/deepseek-ai/DeepSeek-V3.2": { alias: "DeepSeek V3.2" },
        "huggingface/meta-llama/Llama-3.3-70B-Instruct": { alias: "Llama 3.3 70B" },
        "huggingface/openai/gpt-oss-120b": { alias: "GPT-OSS 120B" },
      },
    },
  },
}
```

**Force a specific backend with :provider:**

```
{
  agents: {
    defaults: {
      model: { primary: "huggingface/deepseek-ai/DeepSeek-R1:together" },
      models: {
        "huggingface/deepseek-ai/DeepSeek-R1:together": { alias: "DeepSeek R1 (Together)" },
      },
    },
  },
}
```

**Multiple Qwen and DeepSeek models with policy suffixes:**

```
{
  agents: {
    defaults: {
      model: { primary: "huggingface/Qwen/Qwen2.5-7B-Instruct:cheapest" },
      models: {
        "huggingface/Qwen/Qwen2.5-7B-Instruct": { alias: "Qwen2.5 7B" },
        "huggingface/Qwen/Qwen2.5-7B-Instruct:cheapest": { alias: "Qwen2.5 7B (cheap)" },
        "huggingface/deepseek-ai/DeepSeek-R1:fastest": { alias: "DeepSeek R1 (fast)" },
        "huggingface/meta-llama/Llama-3.1-8B-Instruct": { alias: "Llama 3.1 8B" },
      },
    },
  },
}
```

---

<!-- SOURCE: https://docs.openclaw.ai/providers/glm -->

# GLM Models - OpenClaw

GLM is a **model family** (not a company) available through the Z.AI platform. In OpenClaw, GLM models are accessed via the `zai` provider and model IDs like `zai/glm-5`.

## CLI setup

```
openclaw onboard --auth-choice zai-api-key
```

## Config snippet

```
{
  env: { ZAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "zai/glm-5" } } },
}
```

## Notes

*   GLM versions and availability can change; check Z.AI’s docs for the latest.
*   Example model IDs include `glm-5`, `glm-4.7`, and `glm-4.6`.
*   For provider details, see [/providers/zai](https://docs.openclaw.ai/providers/zai).

---

<!-- SOURCE: https://docs.openclaw.ai/providers/moonshot -->

# Moonshot AI - OpenClaw

## Moonshot AI (Kimi)

Moonshot provides the Kimi API with OpenAI-compatible endpoints. Configure the provider and set the default model to `moonshot/kimi-k2.5`, or use Kimi Coding with `kimi-coding/k2p5`. Current Kimi K2 model IDs:

*   `kimi-k2.5`
*   `kimi-k2-0905-preview`
*   `kimi-k2-turbo-preview`
*   `kimi-k2-thinking`
*   `kimi-k2-thinking-turbo`

```
openclaw onboard --auth-choice moonshot-api-key
```

Kimi Coding:

```
openclaw onboard --auth-choice kimi-code-api-key
```

Note: Moonshot and Kimi Coding are separate providers. Keys are not interchangeable, endpoints differ, and model refs differ (Moonshot uses `moonshot/...`, Kimi Coding uses `kimi-coding/...`).

## Config snippet (Moonshot API)

```
{
  env: { MOONSHOT_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "moonshot/kimi-k2.5" },
      models: {
        // moonshot-kimi-k2-aliases:start
        "moonshot/kimi-k2.5": { alias: "Kimi K2.5" },
        "moonshot/kimi-k2-0905-preview": { alias: "Kimi K2" },
        "moonshot/kimi-k2-turbo-preview": { alias: "Kimi K2 Turbo" },
        "moonshot/kimi-k2-thinking": { alias: "Kimi K2 Thinking" },
        "moonshot/kimi-k2-thinking-turbo": { alias: "Kimi K2 Thinking Turbo" },
        // moonshot-kimi-k2-aliases:end
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [
          // moonshot-kimi-k2-models:start
          {
            id: "kimi-k2.5",
            name: "Kimi K2.5",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-0905-preview",
            name: "Kimi K2 0905 Preview",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-turbo-preview",
            name: "Kimi K2 Turbo",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-thinking",
            name: "Kimi K2 Thinking",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-thinking-turbo",
            name: "Kimi K2 Thinking Turbo",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          // moonshot-kimi-k2-models:end
        ],
      },
    },
  },
}
```

## Kimi Coding

```
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "kimi-coding/k2p5" },
      models: {
        "kimi-coding/k2p5": { alias: "Kimi K2.5" },
      },
    },
  },
}
```

## Notes

*   Moonshot model refs use `moonshot/<modelId>`. Kimi Coding model refs use `kimi-coding/<modelId>`.
*   Override pricing and context metadata in `models.providers` if needed.
*   If Moonshot publishes different context limits for a model, adjust `contextWindow` accordingly.
*   Use `https://api.moonshot.ai/v1` for the international endpoint, and `https://api.moonshot.cn/v1` for the China endpoint.

---

<!-- SOURCE: https://docs.openclaw.ai/providers/nvidia -->

# NVIDIA - OpenClaw

NVIDIA provides an OpenAI-compatible API at `https://integrate.api.nvidia.com/v1` for Nemotron and NeMo models. Authenticate with an API key from [NVIDIA NGC](https://catalog.ngc.nvidia.com/).

## CLI setup

Export the key once, then run onboarding and set an NVIDIA model:

```
export NVIDIA_API_KEY="nvapi-..."
openclaw onboard --auth-choice skip
openclaw models set nvidia/nvidia/llama-3.1-nemotron-70b-instruct
```

If you still pass `--token`, remember it lands in shell history and `ps` output; prefer the env var when possible.

## Config snippet

```
{
  env: { NVIDIA_API_KEY: "nvapi-..." },
  models: {
    providers: {
      nvidia: {
        baseUrl: "https://integrate.api.nvidia.com/v1",
        api: "openai-completions",
      },
    },
  },
  agents: {
    defaults: {
      model: { primary: "nvidia/nvidia/llama-3.1-nemotron-70b-instruct" },
    },
  },
}
```

## Model IDs

*   `nvidia/llama-3.1-nemotron-70b-instruct` (default)
*   `meta/llama-3.3-70b-instruct`
*   `nvidia/mistral-nemo-minitron-8b-8k-instruct`

## Notes

*   OpenAI-compatible `/v1` endpoint; use an API key from NVIDIA NGC.
*   Provider auto-enables when `NVIDIA_API_KEY` is set; uses static defaults (131,072-token context window, 4,096 max tokens).

---

<!-- SOURCE: https://docs.openclaw.ai/providers/minimax -->

# MiniMax - OpenClaw

MiniMax is an AI company that builds the **M2/M2.5** model family. The current coding-focused release is **MiniMax M2.5** (December 23, 2025), built for real-world complex tasks. Source: [MiniMax M2.5 release note](https://www.minimax.io/news/minimax-m25)

## Model overview (M2.5)

MiniMax highlights these improvements in M2.5:

*   Stronger **multi-language coding** (Rust, Java, Go, C++, Kotlin, Objective-C, TS/JS).
*   Better **web/app development** and aesthetic output quality (including native mobile).
*   Improved **composite instruction** handling for office-style workflows, building on interleaved thinking and integrated constraint execution.
*   **More concise responses** with lower token usage and faster iteration loops.
*   Stronger **tool/agent framework** compatibility and context management (Claude Code, Droid/Factory AI, Cline, Kilo Code, Roo Code, BlackBox).
*   Higher-quality **dialogue and technical writing** outputs.

## MiniMax M2.5 vs MiniMax M2.5 Highspeed

*   **Speed:** `MiniMax-M2.5-highspeed` is the official fast tier in MiniMax docs.
*   **Cost:** MiniMax pricing lists the same input cost and a higher output cost for highspeed.
*   **Current model IDs:** use `MiniMax-M2.5` or `MiniMax-M2.5-highspeed`.

## Choose a setup

### MiniMax OAuth (Coding Plan) — recommended

**Best for:** quick setup with MiniMax Coding Plan via OAuth, no API key required. Enable the bundled OAuth plugin and authenticate:

```
openclaw plugins enable minimax-portal-auth  # skip if already loaded.
openclaw gateway restart  # restart if gateway is already running
openclaw onboard --auth-choice minimax-portal
```

You will be prompted to select an endpoint:

*   **Global** - International users (`api.minimax.io`)
*   **CN** - Users in China (`api.minimaxi.com`)

See [MiniMax OAuth plugin README](https://github.com/openclaw/openclaw/tree/main/extensions/minimax-portal-auth) for details.

### MiniMax M2.5 (API key)

**Best for:** hosted MiniMax with Anthropic-compatible API. Configure via CLI:

*   Run `openclaw configure`
*   Select **Model/auth**
*   Choose **MiniMax M2.5**

```
{
  env: { MINIMAX_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "minimax/MiniMax-M2.5" } } },
  models: {
    mode: "merge",
    providers: {
      minimax: {
        baseUrl: "https://api.minimax.io/anthropic",
        apiKey: "${MINIMAX_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "MiniMax-M2.5",
            name: "MiniMax M2.5",
            reasoning: true,
            input: ["text"],
            cost: { input: 0.3, output: 1.2, cacheRead: 0.03, cacheWrite: 0.12 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
          {
            id: "MiniMax-M2.5-highspeed",
            name: "MiniMax M2.5 Highspeed",
            reasoning: true,
            input: ["text"],
            cost: { input: 0.3, output: 1.2, cacheRead: 0.03, cacheWrite: 0.12 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

### MiniMax M2.5 as fallback (example)

**Best for:** keep your strongest latest-generation model as primary, fail over to MiniMax M2.5. Example below uses Opus as a concrete primary; swap to your preferred latest-gen primary model.

```
{
  env: { MINIMAX_API_KEY: "sk-..." },
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "primary" },
        "minimax/MiniMax-M2.5": { alias: "minimax" },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["minimax/MiniMax-M2.5"],
      },
    },
  },
}
```

### Optional: Local via LM Studio (manual)

**Best for:** local inference with LM Studio. We have seen strong results with MiniMax M2.5 on powerful hardware (e.g. a desktop/server) using LM Studio’s local server. Configure manually via `openclaw.json`:

```
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/minimax-m2.5-gs32" },
      models: { "lmstudio/minimax-m2.5-gs32": { alias: "Minimax" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [
          {
            id: "minimax-m2.5-gs32",
            name: "MiniMax M2.5 GS32",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 196608,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## Configure via `openclaw configure`

Use the interactive config wizard to set MiniMax without editing JSON:

1.  Run `openclaw configure`.
2.  Select **Model/auth**.
3.  Choose **MiniMax M2.5**.
4.  Pick your default model when prompted.

## Configuration options

*   `models.providers.minimax.baseUrl`: prefer `https://api.minimax.io/anthropic` (Anthropic-compatible); `https://api.minimax.io/v1` is optional for OpenAI-compatible payloads.
*   `models.providers.minimax.api`: prefer `anthropic-messages`; `openai-completions` is optional for OpenAI-compatible payloads.
*   `models.providers.minimax.apiKey`: MiniMax API key (`MINIMAX_API_KEY`).
*   `models.providers.minimax.models`: define `id`, `name`, `reasoning`, `contextWindow`, `maxTokens`, `cost`.
*   `agents.defaults.models`: alias models you want in the allowlist.
*   `models.mode`: keep `merge` if you want to add MiniMax alongside built-ins.

## Notes

*   Model refs are `minimax/<model>`.
*   Recommended model IDs: `MiniMax-M2.5` and `MiniMax-M2.5-highspeed`.
*   Coding Plan usage API: `https://api.minimaxi.com/v1/api/openplatform/coding_plan/remains` (requires a coding plan key).
*   Update pricing values in `models.json` if you need exact cost tracking.
*   Referral link for MiniMax Coding Plan (10% off): [https://platform.minimax.io/subscribe/coding-plan?code=DbXJTRClnb&source=link](https://platform.minimax.io/subscribe/coding-plan?code=DbXJTRClnb&source=link)
*   See [/concepts/model-providers](https://docs.openclaw.ai/concepts/model-providers) for provider rules.
*   Use `openclaw models list` and `openclaw models set minimax/MiniMax-M2.5` to switch.

## Troubleshooting

### “Unknown model: minimax/MiniMax-M2.5”

This usually means the **MiniMax provider isn’t configured** (no provider entry and no MiniMax auth profile/env key found). A fix for this detection is in **2026.1.12** (unreleased at the time of writing). Fix by:

*   Upgrading to **2026.1.12** (or run from source `main`), then restarting the gateway.
*   Running `openclaw configure` and selecting **MiniMax M2.5**, or
*   Adding the `models.providers.minimax` block manually, or
*   Setting `MINIMAX_API_KEY` (or a MiniMax auth profile) so the provider can be injected.

Make sure the model id is **case‑sensitive**:

*   `minimax/MiniMax-M2.5`
*   `minimax/MiniMax-M2.5-highspeed`

Then recheck with:

---

<!-- SOURCE: https://docs.openclaw.ai/providers/opencode -->

# OpenCode Zen - OpenClaw

OpenCode Zen is a **curated list of models** recommended by the OpenCode team for coding agents. It is an optional, hosted model access path that uses an API key and the `opencode` provider. Zen is currently in beta.

## CLI setup

```
openclaw onboard --auth-choice opencode-zen
# or non-interactive
openclaw onboard --opencode-zen-api-key "$OPENCODE_API_KEY"
```

## Config snippet

```
{
  env: { OPENCODE_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-6" } } },
}
```

## Notes

*   `OPENCODE_ZEN_API_KEY` is also supported.
*   You sign in to Zen, add billing details, and copy your API key.
*   OpenCode Zen bills per request; check the OpenCode dashboard for details.

---

<!-- SOURCE: https://docs.openclaw.ai/providers/openai -->

# OpenAI - OpenClaw

OpenAI provides developer APIs for GPT models. Codex supports **ChatGPT sign-in** for subscription access or **API key** sign-in for usage-based access. Codex cloud requires ChatGPT sign-in. OpenAI explicitly supports subscription OAuth usage in external tools/workflows like OpenClaw.

## Option A: OpenAI API key (OpenAI Platform)

**Best for:** direct API access and usage-based billing. Get your API key from the OpenAI dashboard.

### CLI setup

```
openclaw onboard --auth-choice openai-api-key
# or non-interactive
openclaw onboard --openai-api-key "$OPENAI_API_KEY"
```

### Config snippet

```
{
  env: { OPENAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "openai/gpt-5.4" } } },
}
```

OpenAI’s current API model docs list `gpt-5.4` and `gpt-5.4-pro` for direct OpenAI API usage. OpenClaw forwards both through the `openai/*` Responses path.

## Option B: OpenAI Code (Codex) subscription

**Best for:** using ChatGPT/Codex subscription access instead of an API key. Codex cloud requires ChatGPT sign-in, while the Codex CLI supports ChatGPT or API key sign-in.

### CLI setup (Codex OAuth)

```
# Run Codex OAuth in the wizard
openclaw onboard --auth-choice openai-codex

# Or run OAuth directly
openclaw models auth login --provider openai-codex
```

### Config snippet (Codex subscription)

```
{
  agents: { defaults: { model: { primary: "openai-codex/gpt-5.4" } } },
}
```

OpenAI’s current Codex docs list `gpt-5.4` as the current Codex model. OpenClaw maps that to `openai-codex/gpt-5.4` for ChatGPT/Codex OAuth usage.

### Transport default

OpenClaw uses `pi-ai` for model streaming. For both `openai/*` and `openai-codex/*`, default transport is `"auto"` (WebSocket-first, then SSE fallback). You can set `agents.defaults.models.<provider/model>.params.transport`:

*   `"sse"`: force SSE
*   `"websocket"`: force WebSocket
*   `"auto"`: try WebSocket, then fall back to SSE

For `openai/*` (Responses API), OpenClaw also enables WebSocket warm-up by default (`openaiWsWarmup: true`) when WebSocket transport is used. Related OpenAI docs:

*   [Realtime API with WebSocket](https://platform.openai.com/docs/guides/realtime-websocket)
*   [Streaming API responses (SSE)](https://platform.openai.com/docs/guides/streaming-responses)

```
{
  agents: {
    defaults: {
      model: { primary: "openai-codex/gpt-5.4" },
      models: {
        "openai-codex/gpt-5.4": {
          params: {
            transport: "auto",
          },
        },
      },
    },
  },
}
```

### OpenAI WebSocket warm-up

OpenAI docs describe warm-up as optional. OpenClaw enables it by default for `openai/*` to reduce first-turn latency when using WebSocket transport.

### Disable warm-up

```
{
  agents: {
    defaults: {
      models: {
        "openai/gpt-5.4": {
          params: {
            openaiWsWarmup: false,
          },
        },
      },
    },
  },
}
```

### Enable warm-up explicitly

```
{
  agents: {
    defaults: {
      models: {
        "openai/gpt-5.4": {
          params: {
            openaiWsWarmup: true,
          },
        },
      },
    },
  },
}
```

### OpenAI priority processing

OpenAI’s API exposes priority processing via `service_tier=priority`. In OpenClaw, set `agents.defaults.models["openai/<model>"].params.serviceTier` to pass that field through on direct `openai/*` Responses requests.

```
{
  agents: {
    defaults: {
      models: {
        "openai/gpt-5.4": {
          params: {
            serviceTier: "priority",
          },
        },
      },
    },
  },
}
```

Supported values are `auto`, `default`, `flex`, and `priority`.

### OpenAI Responses server-side compaction

For direct OpenAI Responses models (`openai/*` using `api: "openai-responses"` with `baseUrl` on `api.openai.com`), OpenClaw now auto-enables OpenAI server-side compaction payload hints:

*   Forces `store: true` (unless model compat sets `supportsStore: false`)
*   Injects `context_management: [{ type: "compaction", compact_threshold: ... }]`

By default, `compact_threshold` is `70%` of model `contextWindow` (or `80000` when unavailable).

### Enable server-side compaction explicitly

Use this when you want to force `context_management` injection on compatible Responses models (for example Azure OpenAI Responses):

```
{
  agents: {
    defaults: {
      models: {
        "azure-openai-responses/gpt-5.4": {
          params: {
            responsesServerCompaction: true,
          },
        },
      },
    },
  },
}
```

### Enable with a custom threshold

```
{
  agents: {
    defaults: {
      models: {
        "openai/gpt-5.4": {
          params: {
            responsesServerCompaction: true,
            responsesCompactThreshold: 120000,
          },
        },
      },
    },
  },
}
```

### Disable server-side compaction

```
{
  agents: {
    defaults: {
      models: {
        "openai/gpt-5.4": {
          params: {
            responsesServerCompaction: false,
          },
        },
      },
    },
  },
}
```

`responsesServerCompaction` only controls `context_management` injection. Direct OpenAI Responses models still force `store: true` unless compat sets `supportsStore: false`.

## Notes

*   Model refs always use `provider/model` (see [/concepts/models](https://docs.openclaw.ai/concepts/models)).
*   Auth details + reuse rules are in [/concepts/oauth](https://docs.openclaw.ai/concepts/oauth).

---

<!-- SOURCE: https://docs.openclaw.ai/providers/qianfan -->

# Qianfan - OpenClaw

## Qianfan Provider Guide

Qianfan is Baidu’s MaaS platform, provides a **unified API** that routes requests to many models behind a single endpoint and API key. It is OpenAI-compatible, so most OpenAI SDKs work by switching the base URL.

## Prerequisites

1.  A Baidu Cloud account with Qianfan API access
2.  An API key from the Qianfan console
3.  OpenClaw installed on your system

## Getting Your API Key

1.  Visit the [Qianfan Console](https://console.bce.baidu.com/qianfan/ais/console/apiKey)
2.  Create a new application or select an existing one
3.  Generate an API key (format: `bce-v3/ALTAK-...`)
4.  Copy the API key for use with OpenClaw

## CLI setup

```
openclaw onboard --auth-choice qianfan-api-key
```

*   [OpenClaw Configuration](https://docs.openclaw.ai/gateway/configuration)
*   [Model Providers](https://docs.openclaw.ai/concepts/model-providers)
*   [Agent Setup](https://docs.openclaw.ai/concepts/agent)
*   [Qianfan API Documentation](https://cloud.baidu.com/doc/qianfan-api/s/3m7of64lb)

---

<!-- SOURCE: https://docs.openclaw.ai/providers/vllm -->

# vLLM - OpenClaw

vLLM can serve open-source (and some custom) models via an **OpenAI-compatible** HTTP API. OpenClaw can connect to vLLM using the `openai-completions` API. OpenClaw can also **auto-discover** available models from vLLM when you opt in with `VLLM_API_KEY` (any value works if your server doesn’t enforce auth) and you do not define an explicit `models.providers.vllm` entry.

## Quick start

1.  Start vLLM with an OpenAI-compatible server.

Your base URL should expose `/v1` endpoints (e.g. `/v1/models`, `/v1/chat/completions`). vLLM commonly runs on:

*   `http://127.0.0.1:8000/v1`

2.  Opt in (any value works if no auth is configured):

```
export VLLM_API_KEY="vllm-local"
```

3.  Select a model (replace with one of your vLLM model IDs):

```
{
  agents: {
    defaults: {
      model: { primary: "vllm/your-model-id" },
    },
  },
}
```

## Model discovery (implicit provider)

When `VLLM_API_KEY` is set (or an auth profile exists) and you **do not** define `models.providers.vllm`, OpenClaw will query:

*   `GET http://127.0.0.1:8000/v1/models`

…and convert the returned IDs into model entries. If you set `models.providers.vllm` explicitly, auto-discovery is skipped and you must define models manually.

## Explicit configuration (manual models)

Use explicit config when:

*   vLLM runs on a different host/port.
*   You want to pin `contextWindow`/`maxTokens` values.
*   Your server requires a real API key (or you want to control headers).

```
{
  models: {
    providers: {
      vllm: {
        baseUrl: "http://127.0.0.1:8000/v1",
        apiKey: "${VLLM_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "your-model-id",
            name: "Local vLLM Model",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 128000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## Troubleshooting

*   Check the server is reachable:

```
curl http://127.0.0.1:8000/v1/models
```

*   If requests fail with auth errors, set a real `VLLM_API_KEY` that matches your server configuration, or configure the provider explicitly under `models.providers.vllm`.

---

<!-- SOURCE: https://docs.openclaw.ai/providers/synthetic -->

# Synthetic - OpenClaw

Synthetic exposes Anthropic-compatible endpoints. OpenClaw registers it as the `synthetic` provider and uses the Anthropic Messages API.

## Quick setup

1.  Set `SYNTHETIC_API_KEY` (or run the wizard below).
2.  Run onboarding:

```
openclaw onboard --auth-choice synthetic-api-key
```

The default model is set to:

```
synthetic/hf:MiniMaxAI/MiniMax-M2.5
```

## Config example

```
{
  env: { SYNTHETIC_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.5" },
      models: { "synthetic/hf:MiniMaxAI/MiniMax-M2.5": { alias: "MiniMax M2.5" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "hf:MiniMaxAI/MiniMax-M2.5",
            name: "MiniMax M2.5",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 192000,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

Note: OpenClaw’s Anthropic client appends `/v1` to the base URL, so use `https://api.synthetic.new/anthropic` (not `/anthropic/v1`). If Synthetic changes its base URL, override `models.providers.synthetic.baseUrl`.

## Model catalog

All models below use cost `0` (input/output/cache).

| Model ID | Context window | Max tokens | Reasoning | Input |
| --- | --- | --- | --- | --- |
| `hf:MiniMaxAI/MiniMax-M2.5` | 192000 | 65536 | false | text |
| `hf:moonshotai/Kimi-K2-Thinking` | 256000 | 8192 | true | text |
| `hf:zai-org/GLM-4.7` | 198000 | 128000 | false | text |
| `hf:deepseek-ai/DeepSeek-R1-0528` | 128000 | 8192 | false | text |
| `hf:deepseek-ai/DeepSeek-V3-0324` | 128000 | 8192 | false | text |
| `hf:deepseek-ai/DeepSeek-V3.1` | 128000 | 8192 | false | text |
| `hf:deepseek-ai/DeepSeek-V3.1-Terminus` | 128000 | 8192 | false | text |
| `hf:deepseek-ai/DeepSeek-V3.2` | 159000 | 8192 | false | text |
| `hf:meta-llama/Llama-3.3-70B-Instruct` | 128000 | 8192 | false | text |
| `hf:meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` | 524000 | 8192 | false | text |
| `hf:moonshotai/Kimi-K2-Instruct-0905` | 256000 | 8192 | false | text |
| `hf:openai/gpt-oss-120b` | 128000 | 8192 | false | text |
| `hf:Qwen/Qwen3-235B-A22B-Instruct-2507` | 256000 | 8192 | false | text |
| `hf:Qwen/Qwen3-Coder-480B-A35B-Instruct` | 256000 | 8192 | false | text |
| `hf:Qwen/Qwen3-VL-235B-A22B-Instruct` | 250000 | 8192 | false | text + image |
| `hf:zai-org/GLM-4.5` | 128000 | 128000 | false | text |
| `hf:zai-org/GLM-4.6` | 198000 | 128000 | false | text |
| `hf:deepseek-ai/DeepSeek-V3` | 128000 | 8192 | false | text |
| `hf:Qwen/Qwen3-235B-A22B-Thinking-2507` | 256000 | 8192 | true | text |

## Notes

*   Model refs use `synthetic/<modelId>`.
*   If you enable a model allowlist (`agents.defaults.models`), add every model you plan to use.
*   See [Model providers](https://docs.openclaw.ai/concepts/model-providers) for provider rules.

---

<!-- SOURCE: https://docs.openclaw.ai/providers/together -->

# Together - OpenClaw

The [Together AI](https://together.ai/) provides access to leading open-source models including Llama, DeepSeek, Kimi, and more through a unified API.

*   Provider: `together`
*   Auth: `TOGETHER_API_KEY`
*   API: OpenAI-compatible

## Quick start

1.  Set the API key (recommended: store it for the Gateway):

```
openclaw onboard --auth-choice together-api-key
```

2.  Set a default model:

```
{
  agents: {
    defaults: {
      model: { primary: "together/moonshotai/Kimi-K2.5" },
    },
  },
}
```

## Non-interactive example

```
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice together-api-key \
  --together-api-key "$TOGETHER_API_KEY"
```

This will set `together/moonshotai/Kimi-K2.5` as the default model.

## Environment note

If the Gateway runs as a daemon (launchd/systemd), make sure `TOGETHER_API_KEY` is available to that process (for example, in `~/.openclaw/.env` or via `env.shellEnv`).

## Available models

Together AI provides access to many popular open-source models:

*   **GLM 4.7 Fp8** - Default model with 200K context window
*   **Llama 3.3 70B Instruct Turbo** - Fast, efficient instruction following
*   **Llama 4 Scout** - Vision model with image understanding
*   **Llama 4 Maverick** - Advanced vision and reasoning
*   **DeepSeek V3.1** - Powerful coding and reasoning model
*   **DeepSeek R1** - Advanced reasoning model
*   **Kimi K2 Instruct** - High-performance model with 262K context window

All models support standard chat completions and are OpenAI API compatible.

---

<!-- SOURCE: https://docs.openclaw.ai/providers/mistral -->

# Mistral - OpenClaw

OpenClaw supports Mistral for both text/image model routing (`mistral/...`) and audio transcription via Voxtral in media understanding. Mistral can also be used for memory embeddings (`memorySearch.provider = "mistral"`).

## CLI setup

```
openclaw onboard --auth-choice mistral-api-key
# or non-interactive
openclaw onboard --mistral-api-key "$MISTRAL_API_KEY"
```

## Config snippet (LLM provider)

```
{
  env: { MISTRAL_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "mistral/mistral-large-latest" } } },
}
```

## Config snippet (audio transcription with Voxtral)

```
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "mistral", model: "voxtral-mini-latest" }],
      },
    },
  },
}
```

## Notes

*   Mistral auth uses `MISTRAL_API_KEY`.
*   Provider base URL defaults to `https://api.mistral.ai/v1`.
*   Onboarding default model is `mistral/mistral-large-latest`.
*   Media-understanding default audio model for Mistral is `voxtral-mini-latest`.
*   Media transcription path uses `/v1/audio/transcriptions`.
*   Memory embeddings path uses `/v1/embeddings` (default model: `mistral-embed`).

---

<!-- SOURCE: https://docs.openclaw.ai/providers/qwen -->

# Qwen - OpenClaw

Qwen provides a free-tier OAuth flow for Qwen Coder and Qwen Vision models (2,000 requests/day, subject to Qwen rate limits).

## Enable the plugin

```
openclaw plugins enable qwen-portal-auth
```

Restart the Gateway after enabling.

## Authenticate

```
openclaw models auth login --provider qwen-portal --set-default
```

This runs the Qwen device-code OAuth flow and writes a provider entry to your `models.json` (plus a `qwen` alias for quick switching).

## Model IDs

*   `qwen-portal/coder-model`
*   `qwen-portal/vision-model`

Switch models with:

```
openclaw models set qwen-portal/coder-model
```

## Reuse Qwen Code CLI login

If you already logged in with the Qwen Code CLI, OpenClaw will sync credentials from `~/.qwen/oauth_creds.json` when it loads the auth store. You still need a `models.providers.qwen-portal` entry (use the login command above to create one).

## Notes

*   Tokens auto-refresh; re-run the login command if refresh fails or access is revoked.
*   Default base URL: `https://portal.qwen.ai/v1` (override with `models.providers.qwen-portal.baseUrl` if Qwen provides a different endpoint).
*   See [Model providers](https://docs.openclaw.ai/concepts/model-providers) for provider-wide rules.

---

<!-- SOURCE: https://docs.openclaw.ai/providers/claude-max-api-proxy -->

# Claude Max API Proxy - OpenClaw

**claude-max-api-proxy** is a community tool that exposes your Claude Max/Pro subscription as an OpenAI-compatible API endpoint. This allows you to use your subscription with any tool that supports the OpenAI API format.

## Why Use This?

| Approach | Cost | Best For |
| --- | --- | --- |
| Anthropic API | Pay per token (~15/Minput,15/M input, 75/M output for Opus) | Production apps, high volume |
| Claude Max subscription | $200/month flat | Personal use, development, unlimited usage |

If you have a Claude Max subscription and want to use it with OpenAI-compatible tools, this proxy may reduce cost for some workflows. API keys remain the clearer policy path for production use.

## How It Works

```
Your App → claude-max-api-proxy → Claude Code CLI → Anthropic (via subscription)
     (OpenAI format)              (converts format)      (uses your login)
```

The proxy:

1.  Accepts OpenAI-format requests at `http://localhost:3456/v1/chat/completions`
2.  Converts them to Claude Code CLI commands
3.  Returns responses in OpenAI format (streaming supported)

## Installation

```
# Requires Node.js 20+ and Claude Code CLI
npm install -g claude-max-api-proxy

# Verify Claude CLI is authenticated
claude --version
```

## Usage

### Start the server

```
claude-max-api
# Server runs at http://localhost:3456
```

### Test it

```
# Health check
curl http://localhost:3456/health

# List models
curl http://localhost:3456/v1/models

# Chat completion
curl http://localhost:3456/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-opus-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### With OpenClaw

You can point OpenClaw at the proxy as a custom OpenAI-compatible endpoint:

```
{
  env: {
    OPENAI_API_KEY: "not-needed",
    OPENAI_BASE_URL: "http://localhost:3456/v1",
  },
  agents: {
    defaults: {
      model: { primary: "openai/claude-opus-4" },
    },
  },
}
```

## Available Models

| Model ID | Maps To |
| --- | --- |
| `claude-opus-4` | Claude Opus 4 |
| `claude-sonnet-4` | Claude Sonnet 4 |
| `claude-haiku-4` | Claude Haiku 4 |

## Auto-Start on macOS

Create a LaunchAgent to run the proxy automatically:

```
cat > ~/Library/LaunchAgents/com.claude-max-api.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.claude-max-api</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/node</string>
    <string>/usr/local/lib/node_modules/claude-max-api-proxy/dist/server/standalone.js</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/usr/local/bin:/opt/homebrew/bin:~/.local/bin:/usr/bin:/bin</string>
  </dict>
</dict>
</plist>
EOF

launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.claude-max-api.plist
```

## Links

*   **npm:** [https://www.npmjs.com/package/claude-max-api-proxy](https://www.npmjs.com/package/claude-max-api-proxy)
*   **GitHub:** [https://github.com/atalovesyou/claude-max-api-proxy](https://github.com/atalovesyou/claude-max-api-proxy)
*   **Issues:** [https://github.com/atalovesyou/claude-max-api-proxy/issues](https://github.com/atalovesyou/claude-max-api-proxy/issues)

## Notes

*   This is a **community tool**, not officially supported by Anthropic or OpenClaw
*   Requires an active Claude Max/Pro subscription with Claude Code CLI authenticated
*   The proxy runs locally and does not send data to any third-party servers
*   Streaming responses are fully supported

## See Also

*   [Anthropic provider](https://docs.openclaw.ai/providers/anthropic) - Native OpenClaw integration with Claude setup-token or API keys
*   [OpenAI provider](https://docs.openclaw.ai/providers/openai) - For OpenAI/Codex subscriptions

---

<!-- SOURCE: https://docs.openclaw.ai/providers/ollama -->

# Ollama - OpenClaw

Ollama is a local LLM runtime that makes it easy to run open-source models on your machine. OpenClaw integrates with Ollama’s native API (`/api/chat`), supporting streaming and tool calling, and can **auto-discover tool-capable models** when you opt in with `OLLAMA_API_KEY` (or an auth profile) and do not define an explicit `models.providers.ollama` entry.

## Quick start

1.  Install Ollama: [https://ollama.ai](https://ollama.ai/)
2.  Pull a model:

```
ollama pull gpt-oss:20b
# or
ollama pull llama3.3
# or
ollama pull qwen2.5-coder:32b
# or
ollama pull deepseek-r1:32b
```

3.  Enable Ollama for OpenClaw (any value works; Ollama doesn’t require a real key):

```
# Set environment variable
export OLLAMA_API_KEY="ollama-local"

# Or configure in your config file
openclaw config set models.providers.ollama.apiKey "ollama-local"
```

4.  Use Ollama models:

```
{
  agents: {
    defaults: {
      model: { primary: "ollama/gpt-oss:20b" },
    },
  },
}
```

## Model discovery (implicit provider)

When you set `OLLAMA_API_KEY` (or an auth profile) and **do not** define `models.providers.ollama`, OpenClaw discovers models from the local Ollama instance at `http://127.0.0.1:11434`:

*   Queries `/api/tags` and `/api/show`
*   Keeps only models that report `tools` capability
*   Marks `reasoning` when the model reports `thinking`
*   Reads `contextWindow` from `model_info["<arch>.context_length"]` when available
*   Sets `maxTokens` to 10× the context window
*   Sets all costs to `0`

This avoids manual model entries while keeping the catalog aligned with Ollama’s capabilities. To see what models are available:

```
ollama list
openclaw models list
```

To add a new model, simply pull it with Ollama:

The new model will be automatically discovered and available to use. If you set `models.providers.ollama` explicitly, auto-discovery is skipped and you must define models manually (see below).

## Configuration

### Basic setup (implicit discovery)

The simplest way to enable Ollama is via environment variable:

```
export OLLAMA_API_KEY="ollama-local"
```

### Explicit setup (manual models)

Use explicit config when:

*   Ollama runs on another host/port.
*   You want to force specific context windows or model lists.
*   You want to include models that do not report tool support.

```
{
  models: {
    providers: {
      ollama: {
        baseUrl: "http://ollama-host:11434",
        apiKey: "ollama-local",
        api: "ollama",
        models: [
          {
            id: "gpt-oss:20b",
            name: "GPT-OSS 20B",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 8192,
            maxTokens: 8192 * 10
          }
        ]
      }
    }
  }
}
```

If `OLLAMA_API_KEY` is set, you can omit `apiKey` in the provider entry and OpenClaw will fill it for availability checks.

### Custom base URL (explicit config)

If Ollama is running on a different host or port (explicit config disables auto-discovery, so define models manually):

```
{
  models: {
    providers: {
      ollama: {
        apiKey: "ollama-local",
        baseUrl: "http://ollama-host:11434", // No /v1 - use native Ollama API URL
        api: "ollama", // Set explicitly to guarantee native tool-calling behavior
      },
    },
  },
}
```

### Model selection

Once configured, all your Ollama models are available:

```
{
  agents: {
    defaults: {
      model: {
        primary: "ollama/gpt-oss:20b",
        fallbacks: ["ollama/llama3.3", "ollama/qwen2.5-coder:32b"],
      },
    },
  },
}
```

## Advanced

### Reasoning models

OpenClaw marks models as reasoning-capable when Ollama reports `thinking` in `/api/show`:

```
ollama pull deepseek-r1:32b
```

### Model Costs

Ollama is free and runs locally, so all model costs are set to $0.

### Streaming Configuration

OpenClaw’s Ollama integration uses the **native Ollama API** (`/api/chat`) by default, which fully supports streaming and tool calling simultaneously. No special configuration is needed.

#### Legacy OpenAI-Compatible Mode

If you need to use the OpenAI-compatible endpoint instead (e.g., behind a proxy that only supports OpenAI format), set `api: "openai-completions"` explicitly:

```
{
  models: {
    providers: {
      ollama: {
        baseUrl: "http://ollama-host:11434/v1",
        api: "openai-completions",
        injectNumCtxForOpenAICompat: true, // default: true
        apiKey: "ollama-local",
        models: [...]
      }
    }
  }
}
```

This mode may not support streaming + tool calling simultaneously. You may need to disable streaming with `params: { streaming: false }` in model config. When `api: "openai-completions"` is used with Ollama, OpenClaw injects `options.num_ctx` by default so Ollama does not silently fall back to a 4096 context window. If your proxy/upstream rejects unknown `options` fields, disable this behavior:

```
{
  models: {
    providers: {
      ollama: {
        baseUrl: "http://ollama-host:11434/v1",
        api: "openai-completions",
        injectNumCtxForOpenAICompat: false,
        apiKey: "ollama-local",
        models: [...]
      }
    }
  }
}
```

### Context windows

For auto-discovered models, OpenClaw uses the context window reported by Ollama when available, otherwise it defaults to `8192`. You can override `contextWindow` and `maxTokens` in explicit provider config.

## Troubleshooting

### Ollama not detected

Make sure Ollama is running and that you set `OLLAMA_API_KEY` (or an auth profile), and that you did **not** define an explicit `models.providers.ollama` entry:

And that the API is accessible:

```
curl http://localhost:11434/api/tags
```

### No models available

OpenClaw only auto-discovers models that report tool support. If your model isn’t listed, either:

*   Pull a tool-capable model, or
*   Define the model explicitly in `models.providers.ollama`.

To add models:

```
ollama list  # See what's installed
ollama pull gpt-oss:20b  # Pull a tool-capable model
ollama pull llama3.3     # Or another model
```

### Connection refused

Check that Ollama is running on the correct port:

```
# Check if Ollama is running
ps aux | grep ollama

# Or restart Ollama
ollama serve
```

## See Also

*   [Model Providers](https://docs.openclaw.ai/concepts/model-providers) - Overview of all providers
*   [Model Selection](https://docs.openclaw.ai/concepts/models) - How to choose models
*   [Configuration](https://docs.openclaw.ai/gateway/configuration) - Full config reference

---

<!-- SOURCE: https://docs.openclaw.ai/providers/litellm -->

# Litellm - OpenClaw

[LiteLLM](https://litellm.ai/) is an open-source LLM gateway that provides a unified API to 100+ model providers. Route OpenClaw through LiteLLM to get centralized cost tracking, logging, and the flexibility to switch backends without changing your OpenClaw config.

## Why use LiteLLM with OpenClaw?

*   **Cost tracking** — See exactly what OpenClaw spends across all models
*   **Model routing** — Switch between Claude, GPT-4, Gemini, Bedrock without config changes
*   **Virtual keys** — Create keys with spend limits for OpenClaw
*   **Logging** — Full request/response logs for debugging
*   **Fallbacks** — Automatic failover if your primary provider is down

## Quick start

### Via onboarding

```
openclaw onboard --auth-choice litellm-api-key
```

### Manual setup

1.  Start LiteLLM Proxy:

```
pip install 'litellm[proxy]'
litellm --model claude-opus-4-6
```

2.  Point OpenClaw to LiteLLM:

```
export LITELLM_API_KEY="your-litellm-key"

openclaw
```

That’s it. OpenClaw now routes through LiteLLM.

## Configuration

### Environment variables

```
export LITELLM_API_KEY="sk-litellm-key"
```

### Config file

```
{
  models: {
    providers: {
      litellm: {
        baseUrl: "http://localhost:4000",
        apiKey: "${LITELLM_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "claude-opus-4-6",
            name: "Claude Opus 4.6",
            reasoning: true,
            input: ["text", "image"],
            contextWindow: 200000,
            maxTokens: 64000,
          },
          {
            id: "gpt-4o",
            name: "GPT-4o",
            reasoning: false,
            input: ["text", "image"],
            contextWindow: 128000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
  agents: {
    defaults: {
      model: { primary: "litellm/claude-opus-4-6" },
    },
  },
}
```

## Virtual keys

Create a dedicated key for OpenClaw with spend limits:

```
curl -X POST "http://localhost:4000/key/generate" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "key_alias": "openclaw",
    "max_budget": 50.00,
    "budget_duration": "monthly"
  }'
```

Use the generated key as `LITELLM_API_KEY`.

## Model routing

LiteLLM can route model requests to different backends. Configure in your LiteLLM `config.yaml`:

```
model_list:
  - model_name: claude-opus-4-6
    litellm_params:
      model: claude-opus-4-6
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: gpt-4o
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY
```

OpenClaw keeps requesting `claude-opus-4-6` — LiteLLM handles the routing.

## Viewing usage

Check LiteLLM’s dashboard or API:

```
# Key info
curl "http://localhost:4000/key/info" \
  -H "Authorization: Bearer sk-litellm-key"

# Spend logs
curl "http://localhost:4000/spend/logs" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY"
```

## Notes

*   LiteLLM runs on `http://localhost:4000` by default
*   OpenClaw connects via the OpenAI-compatible `/v1/chat/completions` endpoint
*   All OpenClaw features work through LiteLLM — no limitations

## See also

*   [LiteLLM Docs](https://docs.litellm.ai/)
*   [Model Providers](https://docs.openclaw.ai/concepts/model-providers)

---

<!-- SOURCE: https://docs.openclaw.ai/providers/openrouter -->

# OpenRouter - OpenClaw

OpenRouter provides a **unified API** that routes requests to many models behind a single endpoint and API key. It is OpenAI-compatible, so most OpenAI SDKs work by switching the base URL.

## CLI setup

```
openclaw onboard --auth-choice apiKey --token-provider openrouter --token "$OPENROUTER_API_KEY"
```

## Config snippet

```
{
  env: { OPENROUTER_API_KEY: "sk-or-..." },
  agents: {
    defaults: {
      model: { primary: "openrouter/anthropic/claude-sonnet-4-5" },
    },
  },
}
```

## Notes

*   Model refs are `openrouter/<provider>/<model>`.
*   For more model/provider options, see [/concepts/model-providers](https://docs.openclaw.ai/concepts/model-providers).
*   OpenRouter uses a Bearer token with your API key under the hood.

