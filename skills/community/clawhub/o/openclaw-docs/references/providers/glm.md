# GLM Models

Source: https://docs.openclaw.ai/providers/glm

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationProvidersGLM ModelsGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Model ProvidersModel Provider Quickstart
Model concepts
Models CLI
Configuration
Model ProvidersModel Failover
Providers
AnthropicOpenAIOpenRouterLitellmAmazon BedrockVercel AI GatewayMoonshot AIMiniMaxOpenCode ZenGLM ModelsZ.AISyntheticQianfan
On this page
- [GLM models](#glm-models)
- [CLI setup](#cli-setup)
- [Config snippet](#config-snippet)
- [Notes](#notes)

​GLM models
GLM is a **model family** (not a company) available through the Z.AI platform. In OpenClaw, GLM
models are accessed via the `zai` provider and model IDs like `zai/glm-5`.
​CLI setup
Copy```
openclaw onboard --auth-choice zai-api-key

```

​Config snippet
Copy```
{
  env: { ZAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "zai/glm-5" } } },
}

```

​Notes

- GLM versions and availability can change; check Z.AI’s docs for the latest.

- Example model IDs include `glm-5`, `glm-4.7`, and `glm-4.6`.

- For provider details, see [/providers/zai](/providers/zai).

OpenCode ZenZ.AI⌘I