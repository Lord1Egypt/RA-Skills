# OpenClaw Providers Reference

OpenClaw supports many LLM providers. Set the default model as `provider/model` in config.

## Table of Contents
- [Anthropic](#anthropic)
- [OpenAI](#openai)
- [Google (Gemini)](#google-gemini)
- [OpenRouter](#openrouter)
- [MiniMax](#minimax)
- [DeepSeek](#deepseek)
- [Groq](#groq)
- [Ollama](#ollama)
- [Together AI](#together-ai)
- [Mistral](#mistral)
- [Fireworks](#fireworks)
- [xAI](#xai)
- [Perplexity](#perplexity)
- [Amazon Bedrock](#amazon-bedrock)
- [Cloudflare AI Gateway](#cloudflare-ai-gateway)
- [Z.AI / GLM (Zhipu)](#zai--glm-zhipu)
- [Additional Providers (Brief)](#additional-providers-brief)
- [Provider Configuration: Model Selection & Failover](#provider-configuration-model-selection--failover)
- [Environment Variables Quick Reference](#environment-variables-quick-reference)

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } }
}
```

Run `openclaw onboard` to authenticate, then `openclaw models list` to verify.

---

## Anthropic

**Provider ID:** `anthropic`  
**Auth:** API key (`ANTHROPIC_API_KEY`) or Claude CLI reuse  
**Models:** `claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5`, etc.  
**Docs:** https://docs.openclaw.ai/providers/anthropic

### Auth Routes

| Route | Model prefix | Auth |
|---|---|---|
| API key | `anthropic/*` | `ANTHROPIC_API_KEY` |
| Claude CLI | `anthropic/*` | Reuses existing Claude CLI credentials |

### Setup (API key)

```bash
openclaw onboard --anthropic-api-key "$ANTHROPIC_API_KEY"
openclaw models list --provider anthropic
```

### Config example

```json5
{
  env: { ANTHROPIC_API_KEY: "sk-ant-..." },
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } }
}
```

### Thinking (Claude 4.6+)

Claude 4.6 defaults to `adaptive` thinking. Override per-model:

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": {
          params: { thinking: "adaptive" } // off | minimal | low | medium | high | adaptive | max
        }
      }
    }
  }
}
```

### Prompt Caching

| Value | Duration | Description |
|---|---|---|
| `"short"` (default) | 5 min | Auto-applied for API-key auth |
| `"long"` | 1 hour | Extended cache |
| `"none"` | — | Disable caching |

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": {
          params: { cacheRetention: "long" }
        }
      }
    }
  }
}
```

### Fast Mode

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-sonnet-4-6": {
          params: { fastMode: true } // maps to service_tier: "auto"
        }
      }
    }
  }
}
```

### 1M Context Window (beta)

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": {
          params: { context1m: true }
        }
      }
    }
  }
}
```

⚠️ Requires long-context access. `sk-ant-oat-*` tokens are rejected for 1M context.

**Note:** `anthropic/claude-opus-4.7` (and its `claude-cli` variant) have 1M context **by default** — no `params.context1m: true` needed.

### Per-agent cache overrides

Use model-level params as baseline, then override specific agents via `agents.list[].params`:

```json5
{
  agents: {
    defaults: {
      models: { "anthropic/claude-opus-4-6": { params: { cacheRetention: "long" } } },
    },
    list: [
      { id: "research", default: true },
      { id: "alerts", params: { cacheRetention: "none" } },
    ],
  },
}
```

Config merge order:
1. `agents.defaults.models["provider/model"].params`
2. `agents.list[].params` (overrides by key)

### Bedrock Claude caching notes
- Anthropic Claude models on Bedrock accept `cacheRetention` pass-through
- Non-Anthropic Bedrock models forced to `cacheRetention: "none"`
- API-key smart defaults seed `"short"` for Claude-on-Bedrock refs

### Fast mode notes
- Only injected for direct `api.anthropic.com` requests
- Proxy routes leave `service_tier` untouched

### Claude CLI policy
- Anthropic staff told OpenClaw team that Claude CLI reuse is sanctioned
- For long-lived gateway hosts, API keys remain the clearest production path

### Troubleshooting

- **401 errors**: Token expired; switch to API key.
- **"No API key found"**: Anthropic auth is per-agent; re-run onboarding for each agent.
- **Cooldown**: Check `openclaw models status --json` for `auth.unusableProfiles`.

---

## OpenAI

**Provider ID:** `openai`, `openai-codex`  
**Auth:** `OPENAI_API_KEY` (API) or Codex OAuth (subscription)  
**Docs:** https://docs.openclaw.ai/providers/openai

### Routes

| Goal | Model ref | Auth |
|---|---|---|
| API billing | `openai/gpt-5.4` | `OPENAI_API_KEY` |
| Codex subscription (PI) | `openai-codex/gpt-5.5` | Codex OAuth |
| Codex app-server | `openai/gpt-5.5` + `embeddedHarness.runtime: "codex"` | Codex auth |
| Image generation | `openai/gpt-image-2` | Either |

> **GPT-5.5** is currently subscription/OAuth only. Direct API-key access for `openai/gpt-5.5` available once OpenAI enables it on the public API. Use `openai/gpt-5.4` for `OPENAI_API_KEY` setups.

> **gpt-5.3-codex-spark** is NOT exposed by OpenClaw (rejected by live API).

> Enabling the OpenAI plugin or selecting `openai-codex/*` does NOT auto-enable the Codex app-server plugin. That requires explicit `embeddedHarness.runtime: "codex"`.

### Setup (API key)

```bash
openclaw onboard --auth-choice openai-api-key
# or
openclaw onboard --openai-api-key "$OPENAI_API_KEY"
```

### Setup (Codex OAuth)

```bash
openclaw onboard --auth-choice openai-codex
# For headless:
openclaw models auth login --provider openai-codex --device-code
openclaw config set agents.defaults.model.primary openai-codex/gpt-5.5
```

### Config examples

```json5
// API key
{
  env: { OPENAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "openai/gpt-5.4" } } }
}

// Codex OAuth
{
  agents: { defaults: { model: { primary: "openai-codex/gpt-5.5" } } }
}
```

### Image Generation

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: { primary: "openai/gpt-image-2" }
    }
  }
}
```

- Supports text-to-image and reference-image editing (up to 5 images)
- Sizes: `1024x1024`, `1536x1024`, `1024x1536`, up to `3840x2160`
- `gpt-image-2` is the default for new image workflows. `gpt-image-1` remains usable as an explicit model override but should not be used for new workflows.

### Video Generation

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: { primary: "openai/sora-2" }
    }
  }
}
```

### Speech Synthesis (TTS)

| Setting | Config path | Default |
|---|---|---|
| Model | `messages.tts.providers.openai.model` | `gpt-4o-mini-tts` |
| Voice | `messages.tts.providers.openai.voice` | `coral` |
| Format | `messages.tts.providers.openai.responseFormat` | `opus`/`mp3` |

Available models: `gpt-4o-mini-tts`, `tts-1`, `tts-1-hd`

Available voices: `alloy`, `ash`, `ballad`, `cedar`, `coral`, `echo`, `fable`, `juniper`, `marin`, `onyx`, `nova`, `sage`, `shimmer`, `verse`

### Speech-to-Text (Batch)

- Default model: `gpt-4o-transcribe`
- Config via `tools.media.audio`

### Streaming Speech-to-Text

- Config: `streaming.provider: "openai"` in Voice Call plugin config
- Enables real-time streaming STT for voice calls

### Realtime Voice

- Config: `realtime.provider: "openai"` in Voice Call plugin config
- Enables Voice Call / Control UI Talk via OpenAI Realtime

### GPT-5 Prompt Overlay

OpenClaw adds a shared GPT-5 prompt contribution that applies **by model id** — so `openai-codex/gpt-5.5`, `openai/gpt-5.4`, `openrouter/openai/gpt-5.5`, `opencode/gpt-5.5`, and other compatible GPT-5 refs all receive the same overlay. Older GPT-4.x models do not.

```json5
{
  agents: {
    defaults: {
      promptOverlays: {
        gpt5: { personality: "friendly" } // "friendly" | "on" | "off"
      }
    }
  }
}
```

### Context Window Cap (Codex)

Default cap for `openai-codex/gpt-5.5` is `272000` (native is 1M). Override:

```json5
{
  models: {
    providers: {
      "openai-codex": {
        models: [{ id: "gpt-5.5", contextTokens: 160000 }]
      }
    }
  }
}
```

---

## Google (Gemini)

**Provider ID:** `google`, `google-gemini-cli`  
**Auth:** `GEMINI_API_KEY` or `GOOGLE_API_KEY`; OAuth via Gemini CLI  
**Docs:** https://docs.openclaw.ai/providers/google

### Capabilities

| Capability | Supported |
|---|---|
| Chat completions | Yes |
| Image generation | Yes |
| Music generation | Yes |
| Text-to-speech | Yes |
| Realtime voice (Google Live API) | Yes |
| Image/audio/video understanding | Yes |
| Web search (Grounding) | Yes |
| Thinking/reasoning | Yes (Gemini 2.5+ / Gemini 3+) |
| Gemma 4 models | Yes |

### Setup (API key)

```bash
openclaw onboard --auth-choice gemini-api-key
# or
openclaw onboard --non-interactive --mode local --auth-choice gemini-api-key --gemini-api-key "$GEMINI_API_KEY"
```

### Setup (Gemini CLI OAuth)

```bash
brew install gemini-cli   # or: npm install -g @google/gemini-cli
openclaw models auth login --provider google-gemini-cli --set-default
```

⚠️ Unofficial integration — some users report account restrictions.

Default model for `google-gemini-cli`: `google/gemini-3.1-pro-preview` (with `google-gemini-cli` runtime)

### Config example

```json5
{
  agents: {
    defaults: {
      model: { primary: "google/gemini-3.1-pro-preview" }
    }
  }
}
```

### Image Generation

- Default model: `google/gemini-3.1-flash-image-preview`
- Edit mode: up to 5 input images

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: { primary: "google/gemini-3.1-flash-image-preview" }
    }
  }
}
```

### Video Generation

- Default model: `google/veo-3.1-fast-generate-preview`
- Duration: 4–8 seconds

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: { primary: "google/veo-3.1-fast-generate-preview" }
    }
  }
}
```

### Music Generation

- Default model: `google/lyria-3-clip-preview` (MP3 output)
- Also: `google/lyria-3-pro-preview` (supports both MP3 and WAV output)
- Reference inputs: up to 10 images supported

```json5
{
  agents: {
    defaults: {
      musicGenerationModel: { primary: "google/lyria-3-clip-preview" }
    }
  }
}
```

### Text-to-Speech

- Default model: `gemini-3.1-flash-tts-preview`
- Default voice: `Kore`
- Supports expressive tags: `[whispers]`, `[laughs]`

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "google",
      providers: {
        google: { model: "gemini-3.1-flash-tts-preview", voiceName: "Kore" }
      }
    }
  }
}
```

### TTS text-only block (hide from chat, spoken aloud)

```text
Here is the clean reply text.

[[tts:text]][whispers] Here is the spoken version.[[/tts:text]]
```

### Realtime Voice (Google Live API)

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        enabled: true,
        config: {
          realtime: {
            enabled: true,
            provider: "google",
            providers: {
              google: {
                model: "gemini-2.5-flash-native-audio-preview-12-2025",
                voice: "Kore"
              }
            }
          }
        }
      }
    }
  }
}
```

### Gemini Cache Reuse

```json5
{
  agents: {
    defaults: {
      models: {
        "google/gemini-2.5-pro": {
          params: { cachedContent: "cachedContents/prebuilt-context" }
        }
      }
    }
  }
}
```

### Thinking (Gemini 3+ / Gemma 4)

Gemini 3+ uses `thinkingLevel` (not `thinkingBudget`). OpenClaw maps automatically.

- **`/think adaptive`**: Gemini 3/3.1 omit `thinkingLevel` so Google can choose; Gemini 2.5 sends `thinkingBudget: -1`
- **Gemma 4** models support thinking; OpenClaw rewrites `thinkingBudget` to `thinkingLevel`. Setting `off` preserves disabled (does NOT map to MINIMAL)
- **`google-gemini-cli/*` model refs are legacy** — use `google/*` model refs + `google-gemini-cli` runtime instead

### Gemini CLI OAuth env vars
- `OPENCLAW_GEMINI_OAUTH_CLIENT_ID`, `OPENCLAW_GEMINI_OAUTH_CLIENT_SECRET` (or `GEMINI_CLI_*` variants)
- If OAuth fails, set `GOOGLE_CLOUD_PROJECT` or `GOOGLE_CLOUD_PROJECT_ID` on the gateway host

---

## OpenRouter

**Provider ID:** `openrouter`  
**Auth:** `OPENROUTER_API_KEY`  
**Docs:** https://docs.openclaw.ai/providers/openrouter

Unified API routing requests to many models behind a single endpoint.

### Setup

```bash
openclaw onboard --auth-choice openrouter-api-key
```

### Config example

```json5
{
  env: { OPENROUTER_API_KEY: "sk-or-..." },
  agents: {
    defaults: {
      model: { primary: "openrouter/auto" }
    }
  }
}
```

### Model refs

| Model ref | Notes |
|---|---|
| `openrouter/auto` | OpenRouter automatic routing |
| `openrouter/moonshotai/kimi-k2.6` | Kimi K2.6 via MoonshotAI |
| `openrouter/openai/gpt-5.5` | GPT-5.5 via OpenRouter |
| `openrouter/google/gemini-3.1-flash-image-preview` | Gemini image via OpenRouter |

### Image Generation via OpenRouter

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "openrouter/google/gemini-3.1-flash-image-preview"
      }
    }
  }
}
```

### Headers added by OpenClaw

| Header | Value |
|---|---|
| `HTTP-Referer` | `https://openclaw.ai` |
| `X-OpenRouter-Title` | `OpenClaw` |
| `X-OpenRouter-Categories` | `cli-agent` |

### Notes

- Anthropic cache markers preserved on OpenRouter routes
- Thinking/reasoning mapped for supported non-`auto` routes
- Native OpenAI-only request shaping (`serviceTier`, Responses `store`) not forwarded

---

## MiniMax

**Provider ID:** `minimax` (API key), `minimax-portal` (OAuth)  
**Auth:** `MINIMAX_API_KEY` or MiniMax Coding Plan OAuth  
**Docs:** https://docs.openclaw.ai/providers/minimax

### Built-in catalog

| Model | Type | Description |
|---|---|---|
| `MiniMax-M2.7` | Chat (reasoning) | Default hosted model |
| `MiniMax-M2.7-highspeed` | Chat (faster) | Fast reasoning tier |
| `MiniMax-VL-01` | Vision | Image understanding |
| `image-01` | Image generation | Text-to-image/editing |
| `music-2.6` | Music | Default music model |
| `music-2.5` | Music | Previous tier |
| `music-2.0` | Music | Legacy tier |
| `MiniMax-Hailuo-2.3` | Video | Text-to-video |

### Setup (OAuth — International)

```bash
openclaw onboard --auth-choice minimax-global-oauth
```

### Setup (API key — International)

```bash
openclaw onboard --auth-choice minimax-global-api
```

### Setup (China)

```bash
# OAuth:
openclaw onboard --auth-choice minimax-cn-oauth
# API key:
openclaw onboard --auth-choice minimax-cn-api
```

China routes use `api.minimaxi.com` as base URL.

### Config example (API key)

```json5
{
  env: { MINIMAX_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "minimax/MiniMax-M2.7" } } },
  models: {
    mode: "merge",
    providers: {
      minimax: {
        baseUrl: "https://api.minimax.io/anthropic",
        apiKey: "${MINIMAX_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "MiniMax-M2.7",
            name: "MiniMax M2.7",
            reasoning: true,
            input: ["text", "image"],
            cost: { input: 0.3, output: 1.2, cacheRead: 0.06, cacheWrite: 0.375 },
            contextWindow: 204800,
            maxTokens: 131072
          }
        ]
      }
    }
  }
}
```

⚠️ OpenClaw disables MiniMax thinking by default on Anthropic-compatible path to prevent `reasoning_content` leakage.

### Fast Mode

`/fast on` rewrites `MiniMax-M2.7` → `MiniMax-M2.7-highspeed`.

### Image Generation

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: { primary: "minimax/image-01" }
    }
  }
}
```

- Up to 9 output images
- Aspect ratios: `1:1`, `16:9`, `4:3`, `3:2`, `2:3`, `3:4`, `9:16`, `21:9`

### Web Search

- Uses MiniMax Coding Plan search API
- Key: `MINIMAX_CODE_PLAN_KEY` or `MINIMAX_CODING_API_KEY`

### Troubleshooting

"Unknown model: minimax/MiniMax-M2.7" → Provider not configured. Run `openclaw configure` and choose a MiniMax auth option, or set `MINIMAX_API_KEY`.

---

## DeepSeek

**Provider ID:** `deepseek`  
**Auth:** `DEEPSEEK_API_KEY`  
**API:** OpenAI-compatible  
**Base URL:** `https://api.deepseek.com`  
**Docs:** https://docs.openclaw.ai/providers/deepseek

### Built-in catalog

| Model | Context | Max output | Notes |
|---|---|---|---|
| `deepseek/deepseek-v4-flash` | 1,000,000 | 384,000 | Default; V4 thinking-capable |
| `deepseek/deepseek-v4-pro` | 1,000,000 | 384,000 | V4 thinking-capable |
| `deepseek/deepseek-chat` | 131,072 | 8,192 | V3.2 non-thinking |
| `deepseek/deepseek-reasoner` | 131,072 | 65,536 | V3.2 reasoning |

### Setup

```bash
openclaw onboard --auth-choice deepseek-api-key
```

### Config example

```json5
{
  env: { DEEPSEEK_API_KEY: "sk-..." },
  agents: {
    defaults: { model: { primary: "deepseek/deepseek-v4-flash" } }
  }
}
```

### Thinking and Tools

V4 thinking sessions replay `reasoning_content` on tool-call follow-ups. OpenClaw handles this automatically.

When thinking is disabled, OpenClaw sends `thinking: { type: "disabled" }` and strips `reasoning_content`.

---

## Groq

**Provider ID:** `groq`  
**Auth:** `GROQ_API_KEY`  
**API:** OpenAI-compatible  
**Docs:** https://docs.openclaw.ai/providers/groq

Ultra-fast inference using custom LPU hardware.

### Setup

```bash
export GROQ_API_KEY="gsk_..."
```

### Config example

```json5
{
  env: { GROQ_API_KEY: "gsk_..." },
  agents: {
    defaults: { model: { primary: "groq/llama-3.3-70b-versatile" } }
  }
}
```

### Models

| Model | Notes |
|---|---|
| `groq/llama-3.3-70b-versatile` | General-purpose |
| `groq/llama-3.1-8b-instant` | Fast, lightweight |
| `groq/gemma-2-9b-it` | Compact, efficient |
| `groq/mixtral-8x7b-32768` | MoE architecture |

Run `openclaw models list --provider groq` for current list.

### Audio Transcription

```json5
{
  tools: {
    media: {
      audio: {
        models: [{ provider: "groq" }] // uses whisper-large-v3-turbo
      }
    }
  }
}
```

---

## Ollama

**Provider ID:** `ollama`  
**Auth:** `OLLAMA_API_KEY` (any value for local)  
**API:** Native Ollama API (`/api/chat`)  
**Docs:** https://docs.openclaw.ai/providers/ollama

### Modes

| Mode | Description |
|---|---|
| Cloud + Local | Local Ollama host + cloud models via `ollama signin` |
| Cloud only | `https://ollama.com` with `OLLAMA_API_KEY` |
| Local only | Local Ollama server at `http://127.0.0.1:11434` |

⚠️ Do **NOT** use `/v1` URL — breaks tool calling. Use: `baseUrl: "http://host:11434"`.

### Setup (recommended)

```bash
openclaw onboard
# Select Ollama, then choose Cloud + Local / Cloud only / Local only
```

### Implicit discovery (simplest)

```bash
export OLLAMA_API_KEY="ollama-local"
# OpenClaw auto-discovers models from http://127.0.0.1:11434
```

### Config examples

```json5
// Basic local
{
  agents: { defaults: { model: { primary: "ollama/gemma4" } } }
}

// Custom host
{
  models: {
    providers: {
      ollama: {
        apiKey: "ollama-local",
        baseUrl: "http://ollama-host:11434", // no /v1!
        api: "ollama"
      }
    }
  }
}

// Cloud only
{
  models: {
    providers: {
      ollama: {
        baseUrl: "https://ollama.com",
        apiKey: "OLLAMA_API_KEY",
        api: "ollama",
        models: [
          {
            id: "kimi-k2.5:cloud",
            name: "kimi-k2.5:cloud",
            input: ["text", "image"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 128000,
            maxTokens: 8192
          }
        ]
      }
    }
  }
}
```

### Pull models

```bash
ollama pull gemma4
ollama pull gpt-oss:20b
ollama pull llama3.3
```

### Vision models

OpenClaw reads `/api/show` to detect vision capability. Models with `vision` capability auto-get `input: ["text", "image"]`.

```json5
{
  agents: {
    defaults: {
      imageModel: { primary: "ollama/qwen2.5vl:7b" }
    }
  }
}
```

### Web Search

```json5
{
  tools: { web: { search: { provider: "ollama" } } }
}
```
Requires `ollama signin`.

### Memory Embeddings

```json5
{
  agents: {
    defaults: {
      memorySearch: { provider: "ollama" } // uses nomic-embed-text, auto-pulled
    }
  }
}
```

### Reasoning detection

Models with names containing `r1`, `reasoning`, or `think` are auto-marked as reasoning-capable.

### Cost

All Ollama model costs are set to `$0`.

---

## Together AI

**Provider ID:** `together`  
**Auth:** `TOGETHER_API_KEY`  
**API:** OpenAI-compatible  
**Base URL:** `https://api.together.xyz/v1`  
**Docs:** https://docs.openclaw.ai/providers/together

### Setup

```bash
openclaw onboard --auth-choice together-api-key
```

### Built-in catalog

| Model ref | Input | Context | Notes |
|---|---|---|---|
| `together/moonshotai/Kimi-K2.5` | text, image | 262,144 | Default; reasoning enabled |
| `together/meta-llama/Llama-4-Scout-17B-16E-Instruct` | text, image | 10,000,000 | Multimodal |
| `together/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` | text, image | 20,000,000 | Multimodal |
| `together/deepseek-ai/DeepSeek-V3.1` | text | 131,072 | General |
| `together/deepseek-ai/DeepSeek-R1` | text | 131,072 | Reasoning |

### Video Generation

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: { primary: "together/Wan-AI/Wan2.2-T2V-A14B" }
    }
  }
}
```

---

## Mistral

**Provider ID:** `mistral`  
**Auth:** `MISTRAL_API_KEY`  
**Base URL:** `https://api.mistral.ai/v1`  
**Docs:** https://docs.openclaw.ai/providers/mistral

### Setup

```bash
openclaw onboard --auth-choice mistral-api-key
```

### Built-in catalog

| Model | Input | Context | Max output | Notes |
|---|---|---|---|---|
| `mistral/mistral-large-latest` | text, image | 262,144 | 16,384 | Default |
| `mistral/mistral-medium-2508` | text, image | 262,144 | 8,192 | Medium 3.1 |
| `mistral/mistral-small-latest` | text, image | 128,000 | 16,384 | Adjustable reasoning |
| `mistral/pixtral-large-latest` | text, image | 128,000 | 32,768 | Pixtral |
| `mistral/codestral-latest` | text | 256,000 | 4,096 | Coding |
| `mistral/magistral-small` | text | 128,000 | 40,000 | Reasoning-enabled |

### Audio Transcription (Voxtral)

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "mistral", model: "voxtral-mini-latest" }]
      }
    }
  }
}
```

### Voice Call Streaming STT (Voxtral Realtime)

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          streaming: {
            enabled: true,
            provider: "mistral",
            providers: {
              mistral: {
                apiKey: "${MISTRAL_API_KEY}",
                targetStreamingDelayMs: 800
              }
            }
          }
        }
      }
    }
  }
}
```

| Setting | Default |
|---|---|
| Model | `voxtral-mini-transcribe-realtime-2602` |
| Encoding | `pcm_mulaw` |
| Sample rate | `8000` |
| Target delay | `800ms` |

### Reasoning (mistral-small-latest)

Maps OpenClaw thinking level to `reasoning_effort`:

| OpenClaw level | Mistral `reasoning_effort` |
|---|---|
| off / minimal | `none` |
| low / medium / high / adaptive / max | `high` |

### Memory Embeddings

```json5
{
  memorySearch: { provider: "mistral" } // uses mistral-embed via /v1/embeddings
}
```

---

## Fireworks

**Provider ID:** `fireworks`  
**Auth:** `FIREWORKS_API_KEY`  
**API:** OpenAI-compatible  
**Base URL:** `https://api.fireworks.ai/inference/v1`  
**Default model:** `fireworks/accounts/fireworks/routers/kimi-k2p5-turbo`  
**Docs:** https://docs.openclaw.ai/providers/fireworks

### Setup

```bash
openclaw onboard --auth-choice fireworks-api-key
```

### Built-in catalog

| Model ref | Name | Context | Notes |
|---|---|---|---|
| `fireworks/accounts/fireworks/models/kimi-k2p6` | Kimi K2.6 | 262,144 | Latest Kimi; thinking disabled |
| `fireworks/accounts/fireworks/routers/kimi-k2p5-turbo` | Kimi K2.5 Turbo | 256,000 | Default |

### Custom model IDs

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "fireworks/accounts/fireworks/routers/kimi-k2p5-turbo"
      }
    }
  }
}
```

OpenClaw strips the `fireworks/` prefix and sends the rest to the Fireworks endpoint.

---

## xAI

**Provider ID:** `xai`  
**Auth:** `XAI_API_KEY`  
**Docs:** https://docs.openclaw.ai/providers/xai

### Setup

```bash
openclaw onboard --auth-choice xai-api-key
```

### Built-in catalog

| Family | Model IDs |
|---|---|
| Grok 3 | `grok-3`, `grok-3-fast`, `grok-3-mini`, `grok-3-mini-fast` |
| Grok 4 | `grok-4`, `grok-4-0709` |
| Grok 4 Fast | `grok-4-fast`, `grok-4-fast-non-reasoning` |
| Grok 4.1 Fast | `grok-4-1-fast`, `grok-4-1-fast-non-reasoning` |
| Grok 4.20 Beta | `grok-4.20-beta-latest-reasoning`, `grok-4.20-beta-latest-non-reasoning` |
| Grok Code | `grok-code-fast-1` |

### Fast Mode

| Source model | Fast-mode target |
|---|---|
| `grok-3` | `grok-3-fast` |
| `grok-3-mini` | `grok-3-mini-fast` |
| `grok-4` | `grok-4-fast` |

### Capabilities

| Capability | Status |
|---|---|
| Chat / Responses | Yes (xAI Responses API) |
| Web search (`grok` provider) | Yes |
| X search (`x_search` tool) | Yes |
| Remote code execution | Yes |
| Image generation | Yes |
| Video generation | Yes |
| TTS (batch) | Yes |
| Streaming TTS | Not exposed (OpenClaw returns complete buffers) |
| STT (batch) | Yes |
| Streaming STT | Yes (Voice Call WebSocket) |
| Realtime voice | Not exposed yet (different session/WebSocket contract) |

> Image-capable models: `grok-4-fast`, `grok-4-1-fast`, `grok-4.20-beta-*`
> Plugin forward-resolves newer `grok-4*` and `grok-code-fast*` ids when they follow the same API shape.

### Web Search

```bash
openclaw config set tools.web.search.provider grok
```

### Image Generation

- Default model: `xai/grok-imagine-image`
- Also: `xai/grok-imagine-image-pro`
- Aspect ratios: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `2:3`, `3:2`
- Resolutions: `1K`, `2K`

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: { primary: "xai/grok-imagine-image" }
    }
  }
}
```

### Video Generation

- Default model: `xai/grok-imagine-video`
- Duration: 1–15 seconds
- Aspect ratios: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`

```json5
{
  agents: {
    defaults: {
      videoGenerationModel: { primary: "xai/grok-imagine-video" }
    }
  }
}
```

### Text-to-Speech

- Voices: `eve` (default), `ara`, `rex`, `sal`, `leo`, `una`
- Formats: `mp3`, `wav`, `pcm`, `mulaw`, `alaw`

```json5
{
  messages: {
    tts: {
      provider: "xai",
      providers: {
        xai: { voiceId: "eve" }
      }
    }
  }
}
```

### x_search

```json5
{
  plugins: {
    entries: {
      xai: {
        config: {
          xSearch: {
            enabled: true,
            model: "grok-4-1-fast",
            inlineCitations: true
          }
        }
      }
    }
  }
}
```

### Code Execution (Remote)

```json5
{
  plugins: {
    entries: {
      xai: {
        config: {
          codeExecution: {
            enabled: true,
            model: "grok-4-1-fast"
          }
        }
      }
    }
  }
}
```

### Streaming STT (Voice Call)

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          streaming: {
            enabled: true,
            provider: "xai",
            providers: {
              xai: {
                apiKey: "${XAI_API_KEY}",
                endpointingMs: 800,
                language: "en"
              }
            }
          }
        }
      }
    }
  }
}
```

---

## Perplexity

**Provider ID:** Web search provider (not a model provider)  
**Auth:** `PERPLEXITY_API_KEY` (native) or `OPENROUTER_API_KEY` (via OpenRouter)  
**Docs:** https://docs.openclaw.ai/providers/perplexity-provider

### Setup

```bash
openclaw configure --section web
# or
openclaw config set plugins.entries.perplexity.config.webSearch.apiKey "pplx-xxxx"
```

### Key prefix routing

| Key prefix | Transport | Features |
|---|---|---|
| `pplx-` | Native Perplexity Search API | Structured results, domain/language/date filters |
| `sk-or-` | OpenRouter (Sonar) | AI-synthesized answers with citations |

### Native API Filtering (pplx- keys only)

| Filter | Description |
|---|---|
| Country | 2-letter code (`us`, `de`) |
| Language | ISO 639-1 (`en`, `fr`) |
| Date range | `day`, `week`, `month`, `year` |
| Domain filters | Allowlist/denylist (max 20 domains) |
| Content budget | `max_tokens`, `max_tokens_per_page` |

---

## Amazon Bedrock

**Provider ID:** `amazon-bedrock`  
**Auth:** AWS credentials (env vars, shared config, or instance role)  
**Region:** `AWS_REGION` or `AWS_DEFAULT_REGION` (default: `us-east-1`)  
**Docs:** https://docs.openclaw.ai/providers/bedrock

### Setup (env vars)

```bash
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION="us-east-1"
```

### Config example

```json5
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
            maxTokens: 8192
          }
        ]
      }
    }
  },
  agents: {
    defaults: {
      model: { primary: "amazon-bedrock/us.anthropic.claude-opus-4-6-v1:0" }
    }
  }
}
```

### Auto-discovery (requires IAM permissions)

```bash
openclaw config set plugins.entries.amazon-bedrock.config.discovery.enabled true
openclaw config set plugins.entries.amazon-bedrock.config.discovery.region us-east-1
```

Required IAM permissions: `bedrock:InvokeModel`, `bedrock:InvokeModelWithResponseStream`, `bedrock:ListFoundationModels`, `bedrock:ListInferenceProfiles`

### Discovery config

```json5
{
  plugins: {
    entries: {
      "amazon-bedrock": {
        config: {
          discovery: {
            enabled: true,
            region: "us-east-1",
            providerFilter: ["anthropic", "amazon"],
            refreshInterval: 3600,
            defaultContextWindow: 32000,
            defaultMaxTokens: 4096
          }
        }
      }
    }
  }
}
```

### Guardrails

```json5
{
  plugins: {
    entries: {
      "amazon-bedrock": {
        config: {
          guardrail: {
            guardrailIdentifier: "abc123",
            guardrailVersion: "1",
            streamProcessingMode: "sync",
            trace: "enabled"
          }
        }
      }
    }
  }
}
```

### Memory Embeddings

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "bedrock",
        model: "amazon.titan-embed-text-v2:0"
      }
    }
  }
}
```

---

## Cloudflare AI Gateway

**Provider ID:** `cloudflare-ai-gateway`  
**Auth:** `CLOUDFLARE_AI_GATEWAY_API_KEY` (your Anthropic API key)  
**Default model:** `cloudflare-ai-gateway/claude-sonnet-4-6`  
**Docs:** https://docs.openclaw.ai/providers/cloudflare-ai-gateway

Routes Anthropic requests through Cloudflare for analytics, caching, controls.

### Setup

```bash
openclaw onboard --auth-choice cloudflare-ai-gateway-api-key
# Prompts for account ID, gateway ID, and API key
```

### Config example

```json5
{
  agents: {
    defaults: {
      model: { primary: "cloudflare-ai-gateway/claude-sonnet-4-6" }
    }
  }
}
```

### Authenticated gateway header

```json5
{
  models: {
    providers: {
      "cloudflare-ai-gateway": {
        headers: {
          "cf-aig-authorization": "Bearer <cloudflare-ai-gateway-token>"
        }
      }
    }
  }
}
```

---

## Z.AI / GLM (Zhipu)

**Provider ID:** `zai`
**Auth:** `ZAI_API_KEY`
**Models:** `zai/glm-5`, `zai/glm-5.1`

### Auth choices

| Auth choice | Best for |
|---|---|
| `zai-api-key` | Generic API-key (auto-detect endpoint) |
| `zai-coding-global` | Coding Plan (global) |
| `zai-coding-cn` | Coding Plan (China) |
| `zai-global` | General API (global) |
| `zai-cn` | General API (China) |

```bash
openclaw onboard --auth-choice zai-api-key
openclaw config set agents.defaults.model.primary "zai/glm-5.1"
```

---

## Additional Providers (Brief)

### Alibaba Model Studio
- **Provider ID:** `alibaba`  
- **Auth:** `MODELSTUDIO_API_KEY`
- Video generation: `wan2.6-t2v` model
- Run: `openclaw onboard --auth-choice alibaba-api-key`

### Cerebras
- **Provider ID:** See docs for `cerebras`
- Fast inference for open models

### SambaNova
- **Provider ID:** See docs for `sambanova`
- Enterprise AI inference

### Cohere
- See `https://docs.openclaw.ai/providers/cohere` for setup

### GCP Vertex AI
- **Provider ID:** varies by model family
- Auth via Google Cloud credentials
- See `https://docs.openclaw.ai/providers/gcp-vertex`

### Azure OpenAI
- Configure via `models.providers.openai.baseUrl` pointing to Azure endpoint
- See `https://docs.openclaw.ai/providers/azure`

### NVIDIA
- **Provider ID:** `nvidia`
- See `https://docs.openclaw.ai/providers/nvidia`

### LM Studio (Local)
- **Provider ID:** `lmstudio`
- See `https://docs.openclaw.ai/providers/lmstudio`

### Hugging Face Inference
- **Provider ID:** `huggingface`
- Auth: `HUGGINGFACE_API_KEY`

### Moonshot AI (Kimi)
- **Provider ID:** `moonshot`
- Auth: `KIMI_API_KEY` or `MOONSHOT_API_KEY`
- Default model: `kimi-k2.6`
- Web search via Kimi

### ElevenLabs
- **Provider ID:** ElevenLabs plugin
- **Auth:** `ELEVENLABS_API_KEY` or `XI_API_KEY`
- **Capabilities:** TTS (`eleven_multilingual_v2`, `eleven_v3`), Batch STT (`scribe_v2`), Streaming STT (`scribe_v2_realtime`)
- Config: `messages.tts.providers.elevenlabs.voiceId`, `modelId`

### fal
- **Auth:** `FAL_KEY`
- Video generation provider (e.g., Wan2.1 models)
- Image generation provider

### Venice (privacy-focused)
- **Provider ID:** `venice`
- See `https://docs.openclaw.ai/providers/venice`

### Qwen Cloud
- **Provider ID:** `qwen`
- Auth: `QWEN_API_KEY`
- Video generation: `wan2.6-t2v`

### Runway
- **Provider ID:** `runway`
- Auth: `RUNWAYML_API_SECRET`
- Video generation: `gen4.5` model

### Arcee AI
- **Provider ID:** `arcee`
- Auth: `ARCEEAI_API_KEY` (direct) or via OpenRouter
- API: OpenAI-compatible, base URL `https://api.arcee.ai/api/v1`
- Models: Trinity family (mixture-of-experts, Apache 2.0)
- Run: `openclaw onboard --auth-choice arceeai-api-key`

### Amazon Bedrock Mantle
- **Provider ID:** `amazon-bedrock-mantle`
- Auth: `AWS_BEARER_TOKEN_BEDROCK` or IAM credential chain
- Routes to third-party models (GPT-OSS, Qwen, Kimi, GLM) through Bedrock

### Chutes
- **Provider ID:** `chutes`
- Auth: `CHUTES_API_KEY` or browser OAuth
- API: OpenAI-compatible, open-source model catalogs

### Claude Max API Proxy
- Routes Claude Max subscription through local proxy
- Uses existing Anthropic Claude Max subscription without API key

### ComfyUI
- **Provider ID:** `comfy`
- Auth: none (local) or `COMFY_API_KEY` / `COMFY_CLOUD_API_KEY` (Comfy Cloud)
- Models: `comfy/workflow`
- Image generation via ComfyUI workflows

### GitHub Copilot
- **Provider ID:** `github-copilot`
- Auth: GitHub account/plan (OAuth)
- Two modes: built-in provider or via Copilot Extension

### Gradium
- **Provider ID:** `gradium` (bundled TTS provider)
- Auth: `GRADIUM_API_KEY`
- Capabilities: TTS (normal audio, voice-note Opus, 8 kHz u-law telephony)

### Inferrs
- Local model serving behind OpenAI-compatible backend
- Not a dedicated provider plugin — uses `openai-completions` API

### Kilocode (Kilo Gateway)
- **Provider ID:** `kilocode`
- Unified API routing to many models behind single endpoint
- API: OpenAI-compatible

### LiteLLM
- **Provider ID:** `litellm`
- Open-source LLM gateway (100+ model providers)
- Cost tracking, model routing, automatic failover
- API: OpenAI-compatible proxy

### OpenCode Go
- **Provider ID:** `opencode-go`
- Auth: `OPENCODE_API_KEY` (same as OpenCode Zen catalog)
- Go catalog within OpenCode ecosystem

### Qianfan (Baidu)
- **Provider ID:** `qianfan`
- Auth: `QIANFAN_API_KEY`
- API: OpenAI-compatible

### SGLang
- **Provider ID:** `sglang`
- Auth: `SGLANG_API_KEY` (any value for local)
- API: OpenAI-compatible, auto-discovers available models

### Synthetic
- **Provider ID:** `synthetic`
- Auth: `SYNTHETIC_API_KEY`
- Base URL: `https://api.synthetic.new/anthropic`
- API: Anthropic-compatible

### Tencent Cloud (TokenHub)
- **Provider ID:** `tencent-tokenhub`
- Access to Tencent Hy3 preview models
- API: OpenAI-compatible

### Vercel AI Gateway
- **Provider ID:** `vercel-ai-gateway`
- Auth: `AI_GATEWAY_API_KEY`
- Auto-discovers models via `/v1/models`

### vLLM
- **Provider ID:** `vllm`
- Auth: `VLLM_API_KEY` (any value for local)
- API: OpenAI-compatible (`openai-completions`)
- Auto-discovers available models

### Volcengine (Doubao)
- **Providers:** `volcengine` (general) + `volcengine-plan` (coding)
- Auth: `VOLCANO_ENGINE_API_KEY`
- Access to Doubao models and third-party models

### Vydra
- **Provider ID:** `vydra`
- Auth: `VYDRA_API_KEY`
- Base URL: `https://www.vydra.ai/api/v1` (use `www` to avoid redirect auth issues)

### Xiaomi MiMo
- **Provider ID:** `xiaomi`
- Auth: `XIAOMI_API_KEY`
- API: OpenAI-compatible

---

## Provider Configuration: Model Selection & Failover

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["openai/gpt-5.4", "minimax/MiniMax-M2.7"]
      }
    }
  }
}
```

## Environment Variables Quick Reference

| Provider | Env Var |
|---|---|
| Anthropic | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Google/Gemini | `GEMINI_API_KEY` or `GOOGLE_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| MiniMax | `MINIMAX_API_KEY` |
| DeepSeek | `DEEPSEEK_API_KEY` |
| Groq | `GROQ_API_KEY` |
| Ollama | `OLLAMA_API_KEY` (any value for local) |
| Together | `TOGETHER_API_KEY` |
| Mistral | `MISTRAL_API_KEY` |
| Fireworks | `FIREWORKS_API_KEY` |
| xAI | `XAI_API_KEY` |
| Perplexity | `PERPLEXITY_API_KEY` |
| AWS Bedrock | `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` + `AWS_REGION` |
| Cloudflare AI GW | `CLOUDFLARE_AI_GATEWAY_API_KEY` |
| Runway | `RUNWAYML_API_SECRET` |
| ElevenLabs | `ELEVENLABS_API_KEY` or `XI_API_KEY` |
| Brave Search | `BRAVE_API_KEY` |
| fal | `FAL_KEY` |
| Arcee AI | `ARCEEAI_API_KEY` |
| Chutes | `CHUTES_API_KEY` |
| GitHub Copilot | GitHub OAuth |
| Gradium | `GRADIUM_API_KEY` |
| Kilocode | See provider docs |
| Qianfan (Baidu) | `QIANFAN_API_KEY` |
| SGLang | `SGLANG_API_KEY` |
| Synthetic | `SYNTHETIC_API_KEY` |
| Vercel AI GW | `AI_GATEWAY_API_KEY` |
| Volcengine | `VOLCANO_ENGINE_API_KEY` |
| Vydra | `VYDRA_API_KEY` |
| Xiaomi | `XIAOMI_API_KEY` |
