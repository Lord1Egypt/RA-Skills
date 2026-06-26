# Vercel AI Gateway

Source: https://docs.openclaw.ai/providers/vercel-ai-gateway

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationProvidersVercel AI GatewayGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Model ProvidersModel Provider Quickstart
Model concepts
Models CLI
Configuration
Model ProvidersModel Failover
Providers
AnthropicOpenAIOpenRouterLitellmAmazon BedrockVercel AI GatewayMoonshot AIMiniMaxOpenCode ZenGLM ModelsZ.AISyntheticQianfan
On this page
- [Vercel AI Gateway](#vercel-ai-gateway)
- [Quick start](#quick-start)
- [Non-interactive example](#non-interactive-example)
- [Environment note](#environment-note)

​Vercel AI Gateway
The [Vercel AI Gateway](https://vercel.com/ai-gateway) provides a unified API to access hundreds of models through a single endpoint.

- Provider: `vercel-ai-gateway`

- Auth: `AI_GATEWAY_API_KEY`

- API: Anthropic Messages compatible

​Quick start

- Set the API key (recommended: store it for the Gateway):

Copy```
openclaw onboard --auth-choice ai-gateway-api-key

```

- Set a default model:

Copy```
{
  agents: {
    defaults: {
      model: { primary: "vercel-ai-gateway/anthropic/claude-opus-4.6" },
    },
  },
}

```

​Non-interactive example
Copy```
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice ai-gateway-api-key \
  --ai-gateway-api-key "$AI_GATEWAY_API_KEY"

```

​Environment note
If the Gateway runs as a daemon (launchd/systemd), make sure `AI_GATEWAY_API_KEY`
is available to that process (for example, in `~/.openclaw/.env` or via
`env.shellEnv`).Amazon BedrockMoonshot AI⌘I