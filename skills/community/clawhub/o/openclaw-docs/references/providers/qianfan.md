# Qianfan

Source: https://docs.openclaw.ai/providers/qianfan

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationProvidersQianfanGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Model ProvidersModel Provider Quickstart
Model concepts
Models CLI
Configuration
Model ProvidersModel Failover
Providers
AnthropicOpenAIOpenRouterLitellmAmazon BedrockVercel AI GatewayMoonshot AIMiniMaxOpenCode ZenGLM ModelsZ.AISyntheticQianfan
On this page
- [Qianfan Provider Guide](#qianfan-provider-guide)
- [Prerequisites](#prerequisites)
- [Getting Your API Key](#getting-your-api-key)
- [CLI setup](#cli-setup)
- [Related Documentation](#related-documentation)

​Qianfan Provider Guide
Qianfan is Baidu’s MaaS platform, provides a **unified API** that routes requests to many models behind a single
endpoint and API key. It is OpenAI-compatible, so most OpenAI SDKs work by switching the base URL.
​Prerequisites

- A Baidu Cloud account with Qianfan API access

- An API key from the Qianfan console

- OpenClaw installed on your system

​Getting Your API Key

- Visit the [Qianfan Console](https://console.bce.baidu.com/qianfan/ais/console/apiKey)

- Create a new application or select an existing one

- Generate an API key (format: `bce-v3/ALTAK-...`)

- Copy the API key for use with OpenClaw

​CLI setup
Copy```
openclaw onboard --auth-choice qianfan-api-key

```

​Related Documentation

- [OpenClaw Configuration](/gateway/configuration)

- [Model Providers](/concepts/model-providers)

- [Agent Setup](/concepts/agent)

- [Qianfan API Documentation](https://cloud.baidu.com/doc/qianfan-api/s/3m7of64lb)

Synthetic⌘I