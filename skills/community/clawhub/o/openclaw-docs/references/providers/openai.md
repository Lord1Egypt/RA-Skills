# OpenAI

Source: https://docs.openclaw.ai/providers/openai

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationProvidersOpenAIGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Model ProvidersModel Provider Quickstart
Model concepts
Models CLI
Configuration
Model ProvidersModel Failover
Providers
AnthropicOpenAIOpenRouterLitellmAmazon BedrockVercel AI GatewayMoonshot AIMiniMaxOpenCode ZenGLM ModelsZ.AISyntheticQianfan
On this page
- [OpenAI](#openai)
- [Option A: OpenAI API key (OpenAI Platform)](#option-a-openai-api-key-openai-platform)
- [CLI setup](#cli-setup)
- [Config snippet](#config-snippet)
- [Option B: OpenAI Code (Codex) subscription](#option-b-openai-code-codex-subscription)
- [CLI setup (Codex OAuth)](#cli-setup-codex-oauth)
- [Config snippet (Codex subscription)](#config-snippet-codex-subscription)
- [Notes](#notes)

​OpenAI
OpenAI provides developer APIs for GPT models. Codex supports **ChatGPT sign-in** for subscription
access or **API key** sign-in for usage-based access. Codex cloud requires ChatGPT sign-in.
​Option A: OpenAI API key (OpenAI Platform)
**Best for:** direct API access and usage-based billing.
Get your API key from the OpenAI dashboard.
​CLI setup
Copy```
openclaw onboard --auth-choice openai-api-key
# or non-interactive
openclaw onboard --openai-api-key "$OPENAI_API_KEY"

```

​Config snippet
Copy```
{
  env: { OPENAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "openai/gpt-5.1-codex" } } },
}

```

​Option B: OpenAI Code (Codex) subscription
**Best for:** using ChatGPT/Codex subscription access instead of an API key.
Codex cloud requires ChatGPT sign-in, while the Codex CLI supports ChatGPT or API key sign-in.
​CLI setup (Codex OAuth)
Copy```
# Run Codex OAuth in the wizard
openclaw onboard --auth-choice openai-codex

# Or run OAuth directly
openclaw models auth login --provider openai-codex

```

​Config snippet (Codex subscription)
Copy```
{
  agents: { defaults: { model: { primary: "openai-codex/gpt-5.3-codex" } } },
}

```

​Notes

- Model refs always use `provider/model` (see [/concepts/models](/concepts/models)).

- Auth details + reuse rules are in [/concepts/oauth](/concepts/oauth).

AnthropicOpenRouter⌘I