# Litellm

Source: https://docs.openclaw.ai/providers/litellm

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Model ProvidersModel Provider Quickstart
Model concepts
Models CLI
Configuration
Model ProvidersModel Failover
Providers
AnthropicOpenAIOpenRouterLitellmAmazon BedrockVercel AI GatewayMoonshot AIMiniMaxOpenCode ZenGLM ModelsZ.AISyntheticQianfan
On this page
- [LiteLLM](#litellm)
- [Why use LiteLLM with OpenClaw?](#why-use-litellm-with-openclaw)
- [Quick start](#quick-start)
- [Via onboarding](#via-onboarding)
- [Manual setup](#manual-setup)
- [Configuration](#configuration)
- [Environment variables](#environment-variables)
- [Config file](#config-file)
- [Virtual keys](#virtual-keys)
- [Model routing](#model-routing)
- [Viewing usage](#viewing-usage)
- [Notes](#notes)
- [See also](#see-also)

​LiteLLM
[LiteLLM](https://litellm.ai) is an open-source LLM gateway that provides a unified API to 100+ model providers. Route OpenClaw through LiteLLM to get centralized cost tracking, logging, and the flexibility to switch backends without changing your OpenClaw config.
​Why use LiteLLM with OpenClaw?

- **Cost tracking** — See exactly what OpenClaw spends across all models

- **Model routing** — Switch between Claude, GPT-4, Gemini, Bedrock without config changes

- **Virtual keys** — Create keys with spend limits for OpenClaw

- **Logging** — Full request/response logs for debugging

- **Fallbacks** — Automatic failover if your primary provider is down

​Quick start
​Via onboarding
Copy```
openclaw onboard --auth-choice litellm-api-key

```

​Manual setup

- Start LiteLLM Proxy:

Copy```
pip install &#x27;litellm[proxy]&#x27;
litellm --model claude-opus-4-6

```

- Point OpenClaw to LiteLLM:

Copy```
export LITELLM_API_KEY="your-litellm-key"

openclaw

```

That’s it. OpenClaw now routes through LiteLLM.
​Configuration
​Environment variables
Copy```
export LITELLM_API_KEY="sk-litellm-key"

```

​Config file
Copy```
{
  models: {
    providers: {
      litellm: {
        baseUrl: "http://localhost:4000",
        apiKey: "${LITELLM_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "claude-opus-4-6",
            name: "Claude Opus 4.6",
            reasoning: true,
            input: ["text", "image"],
            contextWindow: 200000,
            maxTokens: 64000,
          },
          {
            id: "gpt-4o",
            name: "GPT-4o",
            reasoning: false,
            input: ["text", "image"],
            contextWindow: 128000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
  agents: {
    defaults: {
      model: { primary: "litellm/claude-opus-4-6" },
    },
  },
}

```

​Virtual keys
Create a dedicated key for OpenClaw with spend limits:
Copy```
curl -X POST "http://localhost:4000/key/generate" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d &#x27;{
    "key_alias": "openclaw",
    "max_budget": 50.00,
    "budget_duration": "monthly"
  }&#x27;

```

Use the generated key as `LITELLM_API_KEY`.
​Model routing
LiteLLM can route model requests to different backends. Configure in your LiteLLM `config.yaml`:
Copy```
model_list:
  - model_name: claude-opus-4-6
    litellm_params:
      model: claude-opus-4-6
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: gpt-4o
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

```

OpenClaw keeps requesting `claude-opus-4-6` — LiteLLM handles the routing.
​Viewing usage
Check LiteLLM’s dashboard or API:
Copy```
# Key info
curl "http://localhost:4000/key/info" \
  -H "Authorization: Bearer sk-litellm-key"

# Spend logs
curl "http://localhost:4000/spend/logs" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY"

```

​Notes

- LiteLLM runs on `http://localhost:4000` by default

- OpenClaw connects via the OpenAI-compatible `/v1/chat/completions` endpoint

- All OpenClaw features work through LiteLLM — no limitations

​See also

- [LiteLLM Docs](https://docs.litellm.ai)

- [Model Providers](/concepts/model-providers)

OpenRouterAmazon Bedrock⌘I