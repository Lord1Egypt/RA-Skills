---
name: openrouter
version: 1.2.3
updated: 2026-03-07
description: "OpenRouter API gateway skill. Access 300+ AI models from 60+ providers through a single OpenAI-compatible API. Unified billing, automatic fallbacks, provider routing, and BYOK support."
homepage: https://openrouter.ai
api_base: https://openrouter.ai/api/v1
credentials: [OPENROUTER_API_KEY]
metadata: {"openclaw":{"requires":{"env":["OPENROUTER_API_KEY"]},"primaryEnv":"OPENROUTER_API_KEY"}}
---

# OpenRouter — One API Key, Hundreds of AI Models

OpenRouter is a unified API gateway that gives you access to **300+ AI models** from
**60+ providers** — Anthropic, OpenAI, Google, DeepSeek, Meta, Mistral, xAI, and more —
through a single, **OpenAI-compatible API endpoint**.

Instead of managing separate accounts, API keys, and billing for each provider, you use
one API key and one credit balance. Switch models by changing a single parameter — no
code changes needed.

OpenRouter powers **250,000+ apps** with **4.2M+ users globally**.

**Base URL:** `https://openrouter.ai/api/v1`

---

## Why Use OpenRouter

| Benefit | Details |
|---------|---------|
| **One API, all models** | Access Claude, GPT, Gemini, DeepSeek, Llama, Grok, and hundreds more through a single endpoint |
| **OpenAI-compatible** | Drop-in replacement — change the base URL and API key, everything else works unchanged |
| **No markup** | Provider pricing is passed through at cost |
| **Automatic fallbacks** | If a provider goes down, requests route to another provider automatically |
| **Edge routing** | ~25–40ms of added latency between you and inference |
| **Privacy controls** | Fine-grained data policies — choose which providers can see your prompts |
| **BYOK support** | Bring your own provider API keys and still get OpenRouter's routing and analytics |

---

## Quick Start

### 1. Create an Account

Sign up at [openrouter.ai](https://openrouter.ai) and add credits on the Credits page.
Credits work with any model or provider. There is no minimum purchase and credits
don't expire.

### 2. Create an API Key

Go to Settings > API Keys and create a key. Store it securely as an environment
variable:

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

### 3. Make a Request

OpenRouter is fully OpenAI-compatible. Here's a basic example:

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-4-20250514",
    "messages": [
      {"role": "user", "content": "Hello, what can you help me with?"}
    ]
  }'
```

To switch models, just change the `model` field — no other code changes needed.

### 4. Using the OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-v1-..."
)

response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

---

## Pricing

OpenRouter passes through provider pricing at cost — no markup.

| Plan | How It Works |
|------|-------------|
| **Free models** | Dozens of models at $0/token. Rate-limited to 20 req/min, 200 req/day (or 1,000/day with $10+ in credits) |
| **Pay-as-you-go** | Buy credits, use them with any model. Billed per token at posted rates. Auto top-up available |
| **BYOK** | Use your own provider API keys. First 1M BYOK requests/month are free, then 5% of upstream cost |
| **Enterprise** | Volume discounts, prepayment credits, annual commits, invoicing/POs, SSO (SAML) |

Input and output tokens are billed separately per model. You're only charged for
successful completions — failed requests and fallback attempts don't cost you.

### Sample Model Pricing (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| DeepSeek V3.2 | $0.25 | $0.38 |
| Gemini 3.1 Flash Lite | $0.25 | $1.50 |
| Llama 3.3 70B | Free | Free |
| GPT-5.4 | $2.50 | $15.00 |
| Claude Sonnet 4.6 | ~$3.00 | ~$15.00 |
| GPT-5.4 Pro | $30.00 | $180.00 |

*Prices change as providers update. Check [openrouter.ai/models](https://openrouter.ai/models)
for current rates.*

---

## Key Features

### Model Routing & Fallbacks

OpenRouter automatically routes requests to the best available provider. If one
provider goes down or errors, the request falls back to another — you're only billed
for the successful run.

You can also control routing explicitly:

- **Provider ordering** — Prioritize specific providers for a model
- **Provider ignoring** — Exclude providers you don't trust
- **Performance thresholds** — Set latency or throughput minimums
- **Regional routing** — Pin requests to specific regions (Enterprise / Pay-as-you-go)
- **`:nitro` variant** — Append `:nitro` to a model slug for speed-optimized routing

### Bring Your Own Key (BYOK)

Use your existing API keys from OpenAI, Anthropic, Google Cloud, AWS Bedrock,
Azure AI, and other providers while still getting OpenRouter's unified interface,
fallback routing, and analytics.

- First **1M BYOK requests per month are free**
- 5% fee on subsequent usage (based on upstream provider cost)
- BYOK keys are automatically prioritized during routing
- Supports: OpenAI, Anthropic, Google Vertex, AWS Bedrock, Azure, and more

### Tool Calling & Structured Outputs

If the underlying model supports function calling / tool use, you can use it through
the same API. Structured output formats (JSON mode) are also supported for
compatible models.

### Web Search

Append `:online` to any model slug to enable web search (powered by Exa.ai). Search
results are injected into the context with citations. Pricing is per result returned.

### Multimodal

OpenRouter supports images, audio, and PDFs across models that handle them. Send
images as URLs or base64, and PDFs work the same way.

### Prompt Caching

Most major providers now support context caching through OpenRouter. Gemini offers
a 90% discount on cached tokens.

### Zero Completion Insurance

Every request includes Zero Completion Insurance — if a model returns an empty or
failed completion, you're not charged.

### Zero Data Retention (ZDR)

For sensitive workloads, enable ZDR to ensure providers don't retain your prompts
or completions.

---

## API Reference

All endpoints use `Authorization: Bearer <OPENROUTER_API_KEY>`.

Base URL: `https://openrouter.ai/api/v1`

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat/completions` | Chat completion (OpenAI-compatible) |
| POST | `/completions` | Text completion (OpenAI-compatible) |
| GET | `/models` | List all available models with pricing |
| GET | `/models/{model_id}` | Get details for a specific model |
| POST | `/embeddings` | Generate embeddings (model-dependent) |

### Key Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/keys` | Create a new API key (requires Provisioning key) |
| GET | `/keys` | List API keys |
| DELETE | `/keys/{key_id}` | Delete an API key |

### Analytics & Account

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/credits` | Check credit balance |
| GET | `/activity` | View usage activity and costs |

---

## Security & Privacy

- **No training on your data.** OpenRouter does not train on prompts or completions.
- **Provider logging controls.** Providers that log prompts are flagged. You can
  restrict routing to non-logging providers in your privacy settings.
- **Fine-grained data policies.** Ensure prompts only go to providers you trust.
- **SOC 2 Type I** compliance indicated (verify current status for compliance-critical
  deployments).
- **ZDR (Zero Data Retention)** available per-request or account-wide.
- **API key spending limits** — Set per-key caps with daily, weekly, or monthly resets.

---

## Framework Integrations

OpenRouter works with popular frameworks out of the box:

- **OpenAI SDK** (Python & TypeScript) — change the base URL
- **LangChain** / **LangGraph**
- **Vercel AI SDK**
- **Langfuse** (observability)
- **Mastra**
- **MCP Servers**
- Any framework that supports the OpenAI API format

---

## Organizations & Enterprise

For teams, OpenRouter offers organizations with:

- Shared credit pools and centralized billing
- Role-based access control (Admin / Member)
- Organization-wide activity tracking and CSV/PDF exports
- Guardrails — spending limits, model/provider allowlists, ZDR enforcement
- Programmatic key provisioning and rotation via Management API
- SSO (SAML) on Enterprise plans
- Broadcast / observability integrations (up to 5 destinations)

---

## Free Models

OpenRouter offers dozens of models at zero cost, including DeepSeek R1, Llama 3.3 70B,
Gemma 3, and others. Free models are rate-limited (20 req/min, 200 req/day for
accounts without credits; 1,000/day with $10+ credits) but require no payment to use.

A dedicated **free model router** (`openrouter/free`) automatically selects the best
available free model for your request.

---

## Contact & Support

| Need | Channel |
|------|---------|
| Technical support | [Discord](https://discord.gg/openrouter) — #help forum |
| Billing & account | support@openrouter.ai |
| Enterprise sales | [Enterprise form](https://openrouter.ai/contact) |
| Status page | [status.openrouter.ai](https://status.openrouter.ai) |
| Documentation | [openrouter.ai/docs](https://openrouter.ai/docs) |

---

## Important Notes

- **Save your API key on creation.** Store it in your platform's secrets manager or
  as `OPENROUTER_API_KEY` in your environment.
- **Never send your OpenRouter API key to any domain other than `openrouter.ai`.**
  Your key grants access to your credit balance and all enabled models.
- **Model availability can change.** Models can be deprecated or have pricing updates
  at any time. Pin specific model IDs/versions in production to avoid surprises.
- **Free model rate limits apply.** Free-tier usage is subject to rate limiting,
  especially during peak times. Failed attempts still count toward daily quotas.
- **BYOK is not free after 1M requests.** The first million BYOK requests per month
  are free, then a 5% fee applies based on upstream cost.
- **OpenRouter is a proxy, not a provider.** It routes your requests to the underlying
  model provider. Latency, output quality, and capabilities depend on the model and
  provider, not OpenRouter itself.
