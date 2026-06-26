# Z.AI

Source: https://docs.openclaw.ai/providers/zai

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationProvidersZ.AIGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Model ProvidersModel Provider Quickstart
Model concepts
Models CLI
Configuration
Model ProvidersModel Failover
Providers
AnthropicOpenAIOpenRouterLitellmAmazon BedrockVercel AI GatewayMoonshot AIMiniMaxOpenCode ZenGLM ModelsZ.AISyntheticQianfan
On this page
- [Z.AI](#z-ai)
- [CLI setup](#cli-setup)
- [Config snippet](#config-snippet)
- [Notes](#notes)

​Z.AI
Z.AI is the API platform for **GLM** models. It provides REST APIs for GLM and uses API keys
for authentication. Create your API key in the Z.AI console. OpenClaw uses the `zai` provider
with a Z.AI API key.
​CLI setup
Copy```
openclaw onboard --auth-choice zai-api-key
# or non-interactive
openclaw onboard --zai-api-key "$ZAI_API_KEY"

```

​Config snippet
Copy```
{
  env: { ZAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "zai/glm-5" } } },
}

```

​Notes

- GLM models are available as `zai/<model>` (example: `zai/glm-5`).

- See [/providers/glm](/providers/glm) for the model family overview.

- Z.AI uses Bearer auth with your API key.

GLM ModelsSynthetic⌘I