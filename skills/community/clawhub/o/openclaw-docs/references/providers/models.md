# Model Provider Quickstart

Source: https://docs.openclaw.ai/providers/models

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationOverviewModel Provider QuickstartGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
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
- [Quick start (two steps)](#quick-start-two-steps)
- [Supported providers (starter set)](#supported-providers-starter-set)

​Model Providers
OpenClaw can use many LLM providers. Pick one, authenticate, then set the default
model as `provider/model`.
​Highlight: Venice (Venice AI)
Venice is our recommended Venice AI setup for privacy-first inference with an option to use Opus for the hardest tasks.

- Default: `venice/llama-3.3-70b`

- Best overall: `venice/claude-opus-45` (Opus remains the strongest)

See [Venice AI](/providers/venice).
​Quick start (two steps)

- Authenticate with the provider (usually via `openclaw onboard`).

- Set the default model:

Copy```
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-6" } } },
}

```

​Supported providers (starter set)

- [OpenAI (API + Codex)](/providers/openai)

- [Anthropic (API + Claude Code CLI)](/providers/anthropic)

- [OpenRouter](/providers/openrouter)

- [Vercel AI Gateway](/providers/vercel-ai-gateway)

- [Cloudflare AI Gateway](/providers/cloudflare-ai-gateway)

- [Moonshot AI (Kimi + Kimi Coding)](/providers/moonshot)

- [Synthetic](/providers/synthetic)

- [OpenCode Zen](/providers/opencode)

- [Z.AI](/providers/zai)

- [GLM models](/providers/glm)

- [MiniMax](/providers/minimax)

- [Venice (Venice AI)](/providers/venice)

- [Amazon Bedrock](/providers/bedrock)

- [Qianfan](/providers/qianfan)

For the full provider catalog (xAI, Groq, Mistral, etc.) and advanced configuration,
see [Model providers](/concepts/model-providers).Model ProvidersModels CLI⌘I