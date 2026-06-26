# OpenCode Zen

Source: https://docs.openclaw.ai/providers/opencode

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationProvidersOpenCode ZenGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Model ProvidersModel Provider Quickstart
Model concepts
Models CLI
Configuration
Model ProvidersModel Failover
Providers
AnthropicOpenAIOpenRouterLitellmAmazon BedrockVercel AI GatewayMoonshot AIMiniMaxOpenCode ZenGLM ModelsZ.AISyntheticQianfan
On this page
- [OpenCode Zen](#opencode-zen)
- [CLI setup](#cli-setup)
- [Config snippet](#config-snippet)
- [Notes](#notes)

​OpenCode Zen
OpenCode Zen is a **curated list of models** recommended by the OpenCode team for coding agents.
It is an optional, hosted model access path that uses an API key and the `opencode` provider.
Zen is currently in beta.
​CLI setup
Copy```
openclaw onboard --auth-choice opencode-zen
# or non-interactive
openclaw onboard --opencode-zen-api-key "$OPENCODE_API_KEY"

```

​Config snippet
Copy```
{
  env: { OPENCODE_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-6" } } },
}

```

​Notes

- `OPENCODE_ZEN_API_KEY` is also supported.

- You sign in to Zen, add billing details, and copy your API key.

- OpenCode Zen bills per request; check the OpenCode dashboard for details.

MiniMaxGLM Models⌘I