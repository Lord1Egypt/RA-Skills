# Model Providers

Source: https://docs.openclaw.ai/providers

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationOverviewModel ProvidersGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Model ProvidersModel Provider Quickstart
Model concepts
Models CLI
Configuration
Model ProvidersModel Failover
Providers
AnthropicOpenAIOpenRouterLitellmAmazon BedrockVercel AI GatewayMoonshot AIMiniMaxOpenCode ZenGLM ModelsZ.AISyntheticQianfan
On this page
- [Model Providers](#model-providers)
- [Highlight: Venice (Venice AI)](#highlight-venice-venice-ai)
- [Quick start](#quick-start)
- [Provider docs](#provider-docs)
- [Transcription providers](#transcription-providers)
- [Community tools](#community-tools)

​Model Providers
OpenClaw can use many LLM providers. Pick a provider, authenticate, then set the
default model as `provider/model`.
Looking for chat channel docs (WhatsApp/Telegram/Discord/Slack/Mattermost (plugin)/etc.)? See [Channels](/channels).
​Highlight: Venice (Venice AI)
Venice is our recommended Venice AI setup for privacy-first inference with an option to use Opus for hard tasks.

- Default: `venice/llama-3.3-70b`

- Best overall: `venice/claude-opus-45` (Opus remains the strongest)

See [Venice AI](/providers/venice).
​Quick start

- Authenticate with the provider (usually via `openclaw onboard`).

- Set the default model:

Copy```
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}

```

​Provider docs

- [OpenAI (API + Codex)](/providers/openai)

- [Anthropic (API + Claude Code CLI)](/providers/anthropic)

- [Qwen (OAuth)](/providers/qwen)

- [OpenRouter](/providers/openrouter)

- [LiteLLM (unified gateway)](/providers/litellm)

- [Vercel AI Gateway](/providers/vercel-ai-gateway)

- [Together AI](/providers/together)

- [Cloudflare AI Gateway](/providers/cloudflare-ai-gateway)

- [Moonshot AI (Kimi + Kimi Coding)](/providers/moonshot)

- [OpenCode Zen](/providers/opencode)

- [Amazon Bedrock](/providers/bedrock)

- [Z.AI](/providers/zai)

- [Xiaomi](/providers/xiaomi)

- [GLM models](/providers/glm)

- [MiniMax](/providers/minimax)

- [Venice (Venice AI, privacy-focused)](/providers/venice)

- [Hugging Face (Inference)](/providers/huggingface)

- [Ollama (local models)](/providers/ollama)

- [vLLM (local models)](/providers/vllm)

- [Qianfan](/providers/qianfan)

- [NVIDIA](/providers/nvidia)

​Transcription providers

- [Deepgram (audio transcription)](/providers/deepgram)

​Community tools

- [Claude Max API Proxy](/providers/claude-max-api-proxy) - Use Claude Max/Pro subscription as an OpenAI-compatible API endpoint

For the full provider catalog (xAI, Groq, Mistral, etc.) and advanced configuration,
see [Model providers](/concepts/model-providers).Model Provider Quickstart⌘I