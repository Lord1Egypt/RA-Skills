# Models and Providers

## Table of Contents

1. [How model selection works](#how-model-selection-works)
2. [Model ref format](#model-ref-format)
3. [Setting the primary model](#setting-the-primary-model)
4. [Fallback chains](#fallback-chains)
5. [Image, PDF, and generation models](#image-pdf-and-generation-models)
6. [Per-agent model overrides](#per-agent-model-overrides)
7. [Model allowlist](#model-allowlist)
8. [Switching models in chat](#switching-models-in-chat)
9. [Built-in providers](#built-in-providers)
10. [Adding a custom or third-party provider](#adding-a-custom-or-third-party-provider)
11. [Local models (Ollama, vLLM, LM Studio)](#local-models)
12. [Multi-key provider rotation](#multi-key-provider-rotation)
13. [Model failover and cooldowns](#model-failover-and-cooldowns)
14. [Sub-agent model config](#sub-agent-model-config)
15. [Scanning for free models](#scanning-for-free-models)
16. [Verifying your setup](#verifying-your-setup)

---

## How model selection works

OpenClaw selects models in this priority order for every agent run:

1. **Session override** (if the user ran `/model <ref>` in chat)
2. **Primary model** (`agents.defaults.model.primary` or `agents.defaults.model`)
3. **Fallbacks** in `agents.defaults.model.fallbacks` (in order)
4. **Provider failover** — within each candidate, OpenClaw tries additional configured keys before advancing to the next model

The key separation to understand:
- `agents.defaults.model` → **which model to use** (primary + fallback chain)
- `agents.defaults.models` → **allowlist and aliases** — if set, only listed models are available

---

## Model ref format

All model refs use `provider/model`:

```
anthropic/claude-opus-4-6
openai/gpt-5.4
google/gemini-3.1-pro-preview
openrouter/auto
ollama/llama3.3
moonshot/kimi-k2.5
```

Provider aliases normalize automatically: `z.ai/*` → `zai/*`, `openai-codex` is the provider id for the Codex login flow, etc.

For OpenRouter-style nested IDs (e.g. `moonshotai/kimi-k2`), always include the provider prefix: `openrouter/moonshotai/kimi-k2`.

---

## Setting the primary model

**Via CLI (recommended):**
```bash
openclaw models set anthropic/claude-opus-4-6
openclaw models set openai/gpt-5.4
openclaw models set openrouter/auto
```

**Via config (`~/.openclaw/openclaw.json`):**
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-6"
      }
    }
  }
}
```

Shorthand (model string directly, no primary/fallbacks object):
```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-6"
    }
  }
}
```

---

## Fallback chains

Fallbacks kick in when a model fails with a failover-worthy error (rate limit, auth exhaustion, overload). Non-retryable errors (bad request, context overflow) do **not** trigger fallback.

**Via CLI:**
```bash
openclaw models fallbacks list
openclaw models fallbacks add openrouter/anthropic/claude-opus-4-6
openclaw models fallbacks add openai/gpt-4o
openclaw models fallbacks remove openai/gpt-4o
openclaw models fallbacks clear
```

**Via config:**
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-6",
        "fallbacks": [
          "openrouter/anthropic/claude-opus-4-6",
          "openai/gpt-5.4",
          "openrouter/auto"
        ]
      }
    }
  }
}
```

**Fallback resolution rules:**
- Per-provider key rotation happens inside each candidate before advancing to the next.
- If the current run is on an override model not in the configured chain, OpenClaw appends the configured primary at the end so it can settle back to the default once earlier candidates are exhausted.
- If every candidate fails, a `FallbackSummaryError` is thrown with per-attempt detail and the soonest cooldown expiry.

**Recommended strategy:**
- Primary: best/strongest model you have access to.
- First fallback: same model on a proxy (e.g. OpenRouter) for redundancy.
- Second fallback: a faster/cheaper model as a cost backstop.
- Third fallback: `openrouter/auto` as a catch-all.

---

## Image, PDF, and generation models

```bash
openclaw models set-image openai/gpt-image-1     # vision model when primary can't accept images
openclaw models image-fallbacks add google/gemini-3.1-pro-preview

openclaw models set-image-generation openai/gpt-image-1   # image generation
```

Via config:
```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "anthropic/claude-opus-4-6" },
      "imageModel": { "primary": "openai/gpt-5.4", "fallbacks": ["google/gemini-3.1-pro-preview"] },
      "pdfModel": "anthropic/claude-sonnet-4-6",
      "imageGenerationModel": "openai/gpt-image-1"
    }
  }
}
```

- `imageModel` is used only when the primary model cannot accept image inputs.
- `pdfModel` is used by the pdf tool. Falls back to `imageModel`, then the resolved session model.
- `imageGenerationModel` is used by the `image_generate` capability.

---

## Per-agent model overrides

Each agent in `agents.list` can have its own model, independently of global defaults:

```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "anthropic/claude-sonnet-4-6" }
    },
    "list": [
      {
        "id": "main",
        "model": "anthropic/claude-opus-4-6"
      },
      {
        "id": "fast",
        "workspace": "~/.openclaw/workspace-fast",
        "model": "anthropic/claude-haiku-4-5"
      },
      {
        "id": "research",
        "workspace": "~/.openclaw/workspace-research",
        "model": {
          "primary": "anthropic/claude-opus-4-6",
          "fallbacks": ["openrouter/anthropic/claude-opus-4-6"]
        }
      }
    ]
  }
}
```

You can also set a per-agent default thinking level:
```json
{
  "id": "deep",
  "model": "anthropic/claude-opus-4-6",
  "thinkingDefault": "high"
}
```

---

## Model allowlist

If `agents.defaults.models` is set, it becomes an **allowlist** — only listed models are eligible for `/model` switching and session overrides. Users trying to pick an unlisted model see:

```
Model "provider/model" is not allowed. Use /model to list available models.
```

Use this to prevent unintended model drift in production setups.

```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "anthropic/claude-sonnet-4-6" },
      "models": {
        "anthropic/claude-sonnet-4-6": { "alias": "Sonnet" },
        "anthropic/claude-opus-4-6": { "alias": "Opus" },
        "anthropic/claude-haiku-4-5": { "alias": "Haiku" },
        "openrouter/auto": { "alias": "auto" }
      }
    }
  }
}
```

- Aliases let users pick models by short name in chat (`/model Sonnet`).
- An empty `models.defaults.models` object (omitted) means all configured models are available.
- Per-agent `agents.list[].skills` can override the global model list.

**Managing aliases via CLI:**
```bash
openclaw models aliases list
openclaw models aliases add Sonnet anthropic/claude-sonnet-4-6
openclaw models aliases remove Sonnet
```

---

## Switching models in chat

Users can switch models per-session without restarting:

```
/model                        # interactive picker
/model list                   # numbered list
/model 3                      # pick by number
/model openai/gpt-5.4         # pick by ref
/model Sonnet                 # pick by alias
/model status                 # detailed view: auth candidates, endpoint info
```

On Discord, `/model` and `/models` open an interactive picker with provider and model dropdowns.

**Live switch behavior:**
- If the agent is idle, the next run uses the new model immediately.
- If a run is already active, the switch is queued and takes effect at the next clean retry point.
- Once tool activity or reply output has started, the queued switch waits until the next user turn.

---

## Built-in providers

These require **no** `models.providers` config entry. Run `openclaw onboard` or set the relevant env var on the machine running OpenClaw, then pick a model ref.

| Provider | Provider ID | How OpenClaw connects | Example model | `--auth-choice` for onboard |
|---|---|---|---|---|
| Anthropic | `anthropic` | `ANTHROPIC_API_KEY` env var | `anthropic/claude-opus-4-6` | `anthropic-api-key` |
| OpenAI | `openai` | `OPENAI_API_KEY` env var | `openai/gpt-5.4` | `openai-api-key` |
| OpenAI Codex | `openai-codex` | device login flow via `openclaw models auth login` | `openai-codex/gpt-5.4` | `openai-codex` |
| Google Gemini | `google` | `GEMINI_API_KEY` env var | `google/gemini-3.1-pro-preview` | `gemini-api-key` |
| Google Vertex | `google-vertex` | gcloud login on the gateway host | `google-vertex/gemini-3.1-pro` | — |
| Google Gemini CLI | `google-gemini-cli` | device login flow via `openclaw models auth login` | `google-gemini-cli/gemini-3-flash-preview` | `google-gemini-cli` |
| OpenRouter | `openrouter` | `OPENROUTER_API_KEY` env var | `openrouter/auto` | `openrouter-api-key` |
| GitHub Copilot | `github-copilot` | device login flow via `openclaw models auth login-github-copilot` | `github-copilot/claude-sonnet-4-6` | `github-copilot` |
| OpenCode Zen | `opencode` | `OPENCODE_API_KEY` env var | `opencode/claude-opus-4-6` | `opencode-zen` |
| OpenCode Go | `opencode-go` | `OPENCODE_API_KEY` env var | `opencode-go/kimi-k2.5` | `opencode-go` |
| Mistral | `mistral` | `MISTRAL_API_KEY` env var | `mistral/mistral-large` | `mistral-api-key` |
| xAI (Grok) | `xai` | `XAI_API_KEY` env var | `xai/grok-3` | `xai-api-key` |
| DeepSeek | `deepseek` | `DEEPSEEK_API_KEY` env var | `deepseek/deepseek-r1` | `deepseek-api-key` |
| Z.AI (GLM) | `zai` | `ZAI_API_KEY` env var | `zai/glm-5.1` | `zai-api-key` |
| Kilo Gateway | `kilocode` | `KILOCODE_API_KEY` env var | `kilocode/kilo/auto` | `kilocode-api-key` |
| Vercel AI Gateway | `vercel-ai-gateway` | `AI_GATEWAY_API_KEY` env var | `vercel-ai-gateway/anthropic/claude-opus-4.6` | `ai-gateway-api-key` |
| Moonshot (Kimi) | `kimi` | `KIMI_API_KEY` env var | `kimi/kimi-k2.5` | `kimi-code-api-key` |
| MiniMax | `minimax` | device login or `MINIMAX_API_KEY` env var | `minimax/abab7-chat` | `minimax-global-api` |
| Qwen | `qwen` | device login or `QWEN_API_KEY` env var | `qwen/qwen-max` | `qwen-api-key` |
| Chutes | `chutes` | `CHUTES_API_KEY` env var | `chutes/deepseek-v3` | `chutes` |
| Venice | `venice` | `VENICE_API_KEY` env var | `venice/llama-3.3-70b` | `venice-api-key` |
| Together | `together` | `TOGETHER_API_KEY` env var | `together/llama-3.3-70b` | `together-api-key` |
| HuggingFace | `huggingface` | `HUGGINGFACE_HUB_TOKEN` env var | `huggingface/deepseek-ai/DeepSeek-R1` | `huggingface-api-key` |
| Ollama (local) | `ollama` | `OLLAMA_API_KEY` env var (any value enables auto-detection) | `ollama/llama3.3` | via plugin |
| vLLM (local) | `vllm` | `VLLM_API_KEY` env var (any value enables auto-detection) | `vllm/my-model` | via plugin |

**Connecting a provider via the onboard wizard:**
```bash
openclaw onboard                                      # interactive — picks up where you are
openclaw models auth login                            # add or re-authenticate any provider interactively
openclaw models auth login-github-copilot             # GitHub Copilot device login flow
openclaw models auth login --provider google-gemini-cli
openclaw models auth order set anthropic openrouter openai  # set provider priority order
```

---

## Adding a custom or third-party provider

Use `models.providers` in `openclaw.json` for any OpenAI-compatible or Anthropic-compatible API.

**When to use `models.providers`:**
- The provider is not in OpenClaw's built-in catalog
- You have a self-hosted inference server (vLLM, LiteLLM, LM Studio)
- You want to use a specific provider endpoint or relay
- You want to add models before official support arrives

**Config structure:**
```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "<provider-id>": {
        "baseUrl": "https://api.example.com/v1",
        "apiKey": "${MY_API_KEY}",
        "api": "openai-completions",
        "models": [
          { "id": "my-model-id", "name": "My Model", "contextWindow": 128000 }
        ]
      }
    }
  }
}
```

**Key fields:**

| Field | Values | Notes |
|---|---|---|
| `baseUrl` | URL string | Base API endpoint (no trailing `/chat/completions`) |
| `apiKey` | string or `${ENV_VAR}` | Use `${ENV_VAR}` to reference an env var |
| `api` | `openai-completions` or `anthropic-messages` | Use `openai-completions` for any `/v1/chat/completions` API |
| `models[].id` | string | The model id sent to the provider |
| `models[].name` | string | Display name |
| `models[].contextWindow` | number | Native context window (metadata) |
| `models[].contextTokens` | number | Effective runtime cap (overrides contextWindow) |

**Use `"mode": "merge"`** (default) — OpenClaw merges your providers into `models.json` alongside built-ins. Use `"replace"` only if you want to remove all built-in providers.

**OpenAI-compatible example (Moonshot / Kimi K2.5):**
```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "moonshot": {
        "baseUrl": "https://api.moonshot.ai/v1",
        "apiKey": "${MOONSHOT_API_KEY}",
        "api": "openai-completions",
        "models": [
          { "id": "kimi-k2.5", "name": "Kimi K2.5", "contextWindow": 131072 },
          { "id": "kimi-k2-thinking", "name": "Kimi K2 Thinking" }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": { "primary": "moonshot/kimi-k2.5" }
    }
  }
}
```

**LiteLLM proxy (OpenAI-compatible, multiple upstream providers):**
```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "litellm": {
        "baseUrl": "http://localhost:4000/v1",
        "apiKey": "${LITELLM_MASTER_KEY}",
        "api": "openai-completions",
        "models": [
          { "id": "claude-opus-4-6", "name": "Claude Opus via LiteLLM" },
          { "id": "gpt-5.4", "name": "GPT-5.4 via LiteLLM" }
        ]
      }
    }
  }
}
```

**Private vLLM server (openai-compatible):**
```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "my-vllm": {
        "baseUrl": "http://10.0.0.5:8000/v1",
        "apiKey": "token-from-vllm",
        "api": "openai-completions",
        "models": [
          { "id": "Qwen/Qwen2.5-72B-Instruct", "name": "Qwen 2.5 72B" }
        ]
      }
    }
  }
}
```

**After adding a custom provider, always add to allowlist and verify:**
```bash
openclaw config validate
openclaw models list --provider moonshot
openclaw models set moonshot/kimi-k2.5
openclaw gateway restart
openclaw models status
```

---

## Local models

### Ollama

Ollama is auto-detected at `http://127.0.0.1:11434`. Set any value for `OLLAMA_API_KEY` to opt in to auto-discovery:

```bash
export OLLAMA_API_KEY=ollama
openclaw plugins enable ollama   # if not already enabled
openclaw models list --local
openclaw models set ollama/llama3.3
```

Custom config (if Ollama runs on a different host/port):
```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "ollama": {
        "baseUrl": "http://10.0.0.10:11434/v1",
        "apiKey": "ollama",
        "api": "openai-completions",
        "models": [
          { "id": "qwen3.5:32b", "name": "Qwen 3.5 32B" },
          { "id": "llama3.3:latest", "name": "Llama 3.3" }
        ]
      }
    }
  }
}
```

**Ollama model management:**
```bash
ollama pull llama3.3        # pull a model before using it in OpenClaw
ollama list                 # list downloaded models
openclaw models scan --provider ollama --no-probe
```

### vLLM and SGLang

Default ports: vLLM `8000`, SGLang `30000`. Set `VLLM_API_KEY` (any value) to opt in:
```bash
export VLLM_API_KEY=any-value
openclaw models list --local
```

Or configure explicitly (see vLLM example above under custom providers).

### LM Studio

LM Studio exposes an OpenAI-compatible endpoint at `http://127.0.0.1:1234/v1`:
```json
{
  "models": {
    "providers": {
      "lmstudio": {
        "baseUrl": "http://127.0.0.1:1234/v1",
        "apiKey": "lm-studio",
        "api": "openai-completions",
        "models": [
          { "id": "loaded-model-name", "name": "My LM Studio Model" }
        ]
      }
    }
  }
}
```

---

## Multi-key provider rotation

OpenClaw can automatically rotate between multiple provider keys when one hits a rate limit (429, quota exceeded). This is configured on the machine running OpenClaw, not inside this skill. Non-rate-limit errors fail immediately without rotation.

**Environment variable naming patterns OpenClaw recognises:**

```bash
# Single key
ANTHROPIC_API_KEY="sk-ant-key1"

# Multiple keys (comma or semicolon separated)
ANTHROPIC_API_KEYS="sk-ant-key1,sk-ant-key2,sk-ant-key3"

# Numbered keys
ANTHROPIC_API_KEY_1="sk-ant-key1"
ANTHROPIC_API_KEY_2="sk-ant-key2"

# Single live override (highest priority)
OPENCLAW_LIVE_ANTHROPIC_KEY="sk-ant-override"
```

Same naming pattern applies to other providers: `OPENAI_API_KEYS`, `OPENROUTER_API_KEYS`, `GEMINI_API_KEYS`, etc.

**View and adjust provider priority:**
```bash
openclaw models auth order get
openclaw models auth order set anthropic openrouter openai
```

---

## How failover and cooldowns work

When a model run fails, OpenClaw works through its candidate chain automatically. This section describes that behaviour so you can configure it correctly.

**Sequence for a single run:**
1. Try primary model with the first configured key/profile for that provider.
2. On rate limit: try the next key/profile for the same provider.
3. When all profiles for that model are exhausted: advance to the next model in the fallback list.
4. Repeat until a model succeeds or every candidate fails.

**Cooldown behaviour:**
- Rate-limited profiles are cooled down with exponential backoff before retrying.
- Persistent failures (e.g. billing holds): backoff starts at 5 hours, doubles per failure, caps at 24 hours. Counter resets after 24 hours clean.
- Overloaded responses: one same-provider key rotation is tried before moving to the next fallback model.
- Cooldown state is stored in `~/.openclaw/agents/<agentId>/agent/auth-state.json` on the machine running OpenClaw.

**Inspect the current state:**
```bash
openclaw models status          # shows primary, fallbacks, and any provider warnings
openclaw models status --check  # non-zero exit if any provider is missing or expiring (CI use)
openclaw health --verbose       # broader gateway and provider health view
```

**Force a specific model for the current session:**
```
/model anthropic/claude-opus-4-6
```

---

## Sub-agent model config

Sub-agents inherit the calling agent's model by default. To use a cheaper model for background work:

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "model": "anthropic/claude-haiku-4-5",
        "thinking": "minimal"
      }
    }
  }
}
```

Per-agent override:
```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "subagents": {
          "model": "anthropic/claude-sonnet-4-6",
          "thinking": "low",
          "runTimeoutSeconds": 120
        }
      }
    ]
  }
}
```

A `model` passed directly in `sessions_spawn` always wins over these defaults.

---

## Scanning for free models

`openclaw models scan` inspects OpenRouter's free model catalog and ranks candidates for use as fallbacks:

```bash
openclaw models scan                         # interactive scan (requires OPENROUTER_API_KEY)
openclaw models scan --no-probe              # metadata only, no live probes
openclaw models scan --min-params 7          # filter to >=7B parameter models
openclaw models scan --max-age-days 60       # skip models older than 60 days
openclaw models scan --set-default           # set top result as primary
openclaw models scan --max-candidates 3 --yes  # non-interactive, accept top 3
```

Scan rankings: image support → tool latency → context size → parameter count.

---

## Verifying your setup

```bash
openclaw models list              # all configured models
openclaw models list --all        # full catalog including built-ins
openclaw models list --local      # local providers only
openclaw models status            # primary, fallbacks, image model, auth overview
openclaw models status --check    # CI-friendly: non-zero if auth missing or expiring
openclaw config validate          # validate the full config including models.providers
```

**Debug tip:** start minimal when adding a custom provider — `baseUrl`, `apiKey`, `api`, and one model. Verify with `openclaw models list --provider <id>`. Add more models and params only after the basic connection works. Never edit `~/.openclaw/agents/<agentId>/agent/models.json` directly — it is regenerated from `openclaw.json`.
