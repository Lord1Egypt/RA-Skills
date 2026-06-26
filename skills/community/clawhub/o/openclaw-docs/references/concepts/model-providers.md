# Model Providers

Source: https://docs.openclaw.ai/concepts/model-providers

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationConfigurationModel ProvidersGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Model ProvidersModel Provider Quickstart
Model concepts
Models CLI
Configuration
Model ProvidersModel Failover
Providers
AnthropicOpenAIOpenRouterLitellmAmazon BedrockVercel AI GatewayMoonshot AIMiniMaxOpenCode ZenGLM ModelsZ.AISyntheticQianfan
On this page
- [Model providers](#model-providers)
- [Quick rules](#quick-rules)
- [Built-in providers (pi-ai catalog)](#built-in-providers-pi-ai-catalog)
- [OpenAI](#openai)
- [Anthropic](#anthropic)
- [OpenAI Code (Codex)](#openai-code-codex)
- [OpenCode Zen](#opencode-zen)
- [Google Gemini (API key)](#google-gemini-api-key)
- [Google Vertex, Antigravity, and Gemini CLI](#google-vertex-antigravity-and-gemini-cli)
- [Z.AI (GLM)](#z-ai-glm)
- [Vercel AI Gateway](#vercel-ai-gateway)
- [Other built-in providers](#other-built-in-providers)
- [Providers via models.providers (custom/base URL)](#providers-via-models-providers-custom%2Fbase-url)
- [Moonshot AI (Kimi)](#moonshot-ai-kimi)
- [Kimi Coding](#kimi-coding)
- [Qwen OAuth (free tier)](#qwen-oauth-free-tier)
- [Synthetic](#synthetic)
- [MiniMax](#minimax)
- [Ollama](#ollama)
- [vLLM](#vllm)
- [Local proxies (LM Studio, vLLM, LiteLLM, etc.)](#local-proxies-lm-studio-vllm-litellm-etc)
- [CLI examples](#cli-examples)

​Model providers
This page covers **LLM/model providers** (not chat channels like WhatsApp/Telegram).
For model selection rules, see [/concepts/models](/concepts/models).
​Quick rules

- Model refs use `provider/model` (example: `opencode/claude-opus-4-6`).

- If you set `agents.defaults.models`, it becomes the allowlist.

- CLI helpers: `openclaw onboard`, `openclaw models list`, `openclaw models set <provider/model>`.

​Built-in providers (pi-ai catalog)
OpenClaw ships with the pi‑ai catalog. These providers require **no**
`models.providers` config; just set auth + pick a model.
​OpenAI

- Provider: `openai`

- Auth: `OPENAI_API_KEY`

- Example model: `openai/gpt-5.1-codex`

- CLI: `openclaw onboard --auth-choice openai-api-key`

Copy```
{
  agents: { defaults: { model: { primary: "openai/gpt-5.1-codex" } } },
}

```

​Anthropic

- Provider: `anthropic`

- Auth: `ANTHROPIC_API_KEY` or `claude setup-token`

- Example model: `anthropic/claude-opus-4-6`

- CLI: `openclaw onboard --auth-choice token` (paste setup-token) or `openclaw models auth paste-token --provider anthropic`

Copy```
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}

```

​OpenAI Code (Codex)

- Provider: `openai-codex`

- Auth: OAuth (ChatGPT)

- Example model: `openai-codex/gpt-5.3-codex`

- CLI: `openclaw onboard --auth-choice openai-codex` or `openclaw models auth login --provider openai-codex`

Copy```
{
  agents: { defaults: { model: { primary: "openai-codex/gpt-5.3-codex" } } },
}

```

​OpenCode Zen

- Provider: `opencode`

- Auth: `OPENCODE_API_KEY` (or `OPENCODE_ZEN_API_KEY`)

- Example model: `opencode/claude-opus-4-6`

- CLI: `openclaw onboard --auth-choice opencode-zen`

Copy```
{
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-6" } } },
}

```

​Google Gemini (API key)

- Provider: `google`

- Auth: `GEMINI_API_KEY`

- Example model: `google/gemini-3-pro-preview`

- CLI: `openclaw onboard --auth-choice gemini-api-key`

​Google Vertex, Antigravity, and Gemini CLI

- Providers: `google-vertex`, `google-antigravity`, `google-gemini-cli`

- Auth: Vertex uses gcloud ADC; Antigravity/Gemini CLI use their respective auth flows

Antigravity OAuth is shipped as a bundled plugin (`google-antigravity-auth`, disabled by default).

- Enable: `openclaw plugins enable google-antigravity-auth`

- Login: `openclaw models auth login --provider google-antigravity --set-default`

Gemini CLI OAuth is shipped as a bundled plugin (`google-gemini-cli-auth`, disabled by default).

- Enable: `openclaw plugins enable google-gemini-cli-auth`

- Login: `openclaw models auth login --provider google-gemini-cli --set-default`

- Note: you do **not** paste a client id or secret into `openclaw.json`. The CLI login flow stores
tokens in auth profiles on the gateway host.

​Z.AI (GLM)

- Provider: `zai`

- Auth: `ZAI_API_KEY`

- Example model: `zai/glm-4.7`

CLI: `openclaw onboard --auth-choice zai-api-key`

- Aliases: `z.ai/*` and `z-ai/*` normalize to `zai/*`

​Vercel AI Gateway

- Provider: `vercel-ai-gateway`

- Auth: `AI_GATEWAY_API_KEY`

- Example model: `vercel-ai-gateway/anthropic/claude-opus-4.6`

- CLI: `openclaw onboard --auth-choice ai-gateway-api-key`

​Other built-in providers

- OpenRouter: `openrouter` (`OPENROUTER_API_KEY`)

- Example model: `openrouter/anthropic/claude-sonnet-4-5`

- xAI: `xai` (`XAI_API_KEY`)

- Groq: `groq` (`GROQ_API_KEY`)

Cerebras: `cerebras` (`CEREBRAS_API_KEY`)

- GLM models on Cerebras use ids `zai-glm-4.7` and `zai-glm-4.6`.

- OpenAI-compatible base URL: `https://api.cerebras.ai/v1`.

- Mistral: `mistral` (`MISTRAL_API_KEY`)

- GitHub Copilot: `github-copilot` (`COPILOT_GITHUB_TOKEN` / `GH_TOKEN` / `GITHUB_TOKEN`)

- Hugging Face Inference: `huggingface` (`HUGGINGFACE_HUB_TOKEN` or `HF_TOKEN`) — OpenAI-compatible router; example model: `huggingface/deepseek-ai/DeepSeek-R1`; CLI: `openclaw onboard --auth-choice huggingface-api-key`. See [Hugging Face (Inference)](/providers/huggingface).

​Providers via `models.providers` (custom/base URL)
Use `models.providers` (or `models.json`) to add **custom** providers or
OpenAI/Anthropic‑compatible proxies.
​Moonshot AI (Kimi)
Moonshot uses OpenAI-compatible endpoints, so configure it as a custom provider:

- Provider: `moonshot`

- Auth: `MOONSHOT_API_KEY`

- Example model: `moonshot/kimi-k2.5`

Kimi K2 model IDs:

- `moonshot/kimi-k2.5`

- `moonshot/kimi-k2-0905-preview`

- `moonshot/kimi-k2-turbo-preview`

- `moonshot/kimi-k2-thinking`

- `moonshot/kimi-k2-thinking-turbo`

Copy```
{
  agents: {
    defaults: { model: { primary: "moonshot/kimi-k2.5" } },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [{ id: "kimi-k2.5", name: "Kimi K2.5" }],
      },
    },
  },
}

```

​Kimi Coding
Kimi Coding uses Moonshot AI’s Anthropic-compatible endpoint:

- Provider: `kimi-coding`

- Auth: `KIMI_API_KEY`

- Example model: `kimi-coding/k2p5`

Copy```
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: { model: { primary: "kimi-coding/k2p5" } },
  },
}

```

​Qwen OAuth (free tier)
Qwen provides OAuth access to Qwen Coder + Vision via a device-code flow.
Enable the bundled plugin, then log in:
Copy```
openclaw plugins enable qwen-portal-auth
openclaw models auth login --provider qwen-portal --set-default

```

Model refs:

- `qwen-portal/coder-model`

- `qwen-portal/vision-model`

See [/providers/qwen](/providers/qwen) for setup details and notes.
​Synthetic
Synthetic provides Anthropic-compatible models behind the `synthetic` provider:

- Provider: `synthetic`

- Auth: `SYNTHETIC_API_KEY`

- Example model: `synthetic/hf:MiniMaxAI/MiniMax-M2.1`

- CLI: `openclaw onboard --auth-choice synthetic-api-key`

Copy```
{
  agents: {
    defaults: { model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.1" } },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [{ id: "hf:MiniMaxAI/MiniMax-M2.1", name: "MiniMax M2.1" }],
      },
    },
  },
}

```

​MiniMax
MiniMax is configured via `models.providers` because it uses custom endpoints:

- MiniMax (Anthropic‑compatible): `--auth-choice minimax-api`

- Auth: `MINIMAX_API_KEY`

See [/providers/minimax](/providers/minimax) for setup details, model options, and config snippets.
​Ollama
Ollama is a local LLM runtime that provides an OpenAI-compatible API:

- Provider: `ollama`

- Auth: None required (local server)

- Example model: `ollama/llama3.3`

- Installation: [https://ollama.ai](https://ollama.ai)

Copy```
# Install Ollama, then pull a model:
ollama pull llama3.3

```

Copy```
{
  agents: {
    defaults: { model: { primary: "ollama/llama3.3" } },
  },
}

```

Ollama is automatically detected when running locally at `http://127.0.0.1:11434/v1`. See [/providers/ollama](/providers/ollama) for model recommendations and custom configuration.
​vLLM
vLLM is a local (or self-hosted) OpenAI-compatible server:

- Provider: `vllm`

- Auth: Optional (depends on your server)

- Default base URL: `http://127.0.0.1:8000/v1`

To opt in to auto-discovery locally (any value works if your server doesn’t enforce auth):
Copy```
export VLLM_API_KEY="vllm-local"

```

Then set a model (replace with one of the IDs returned by `/v1/models`):
Copy```
{
  agents: {
    defaults: { model: { primary: "vllm/your-model-id" } },
  },
}

```

See [/providers/vllm](/providers/vllm) for details.
​Local proxies (LM Studio, vLLM, LiteLLM, etc.)
Example (OpenAI‑compatible):
Copy```
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/minimax-m2.1-gs32" },
      models: { "lmstudio/minimax-m2.1-gs32": { alias: "Minimax" } },
    },
  },
  models: {
    providers: {
      lmstudio: {
        baseUrl: "http://localhost:1234/v1",
        apiKey: "LMSTUDIO_KEY",
        api: "openai-completions",
        models: [
          {
            id: "minimax-m2.1-gs32",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}

```

Notes:

For custom providers, `reasoning`, `input`, `cost`, `contextWindow`, and `maxTokens` are optional.
When omitted, OpenClaw defaults to:

- `reasoning: false`

- `input: ["text"]`

- `cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 }`

- `contextWindow: 200000`

- `maxTokens: 8192`

- Recommended: set explicit values that match your proxy/model limits.

​CLI examples
Copy```
openclaw onboard --auth-choice opencode-zen
openclaw models set opencode/claude-opus-4-6
openclaw models list

```

See also: [/gateway/configuration](/gateway/configuration) for full configuration examples.Models CLIModel Failover⌘I