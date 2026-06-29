# @earendil-works/pi-ai

Unified multi-provider LLM API, supporting OpenAI, Anthropic, Google, and more.

## getModel()

```ts
import { getModel } from "@earendil-works/pi-ai";

const model = getModel("anthropic", "claude-sonnet-4-20250514");
const model2 = getModel("openai", "gpt-4o");
const model3 = getModel("google", "gemini-2.5-pro");
```

## Supported Providers

- **Anthropic** — Full Claude series, supports OAuth subscription and API key
- **OpenAI** — Full GPT series, supports OAuth (ChatGPT Plus/Pro) and API key, Codex models
- **Google** — Full Gemini series + Vertex AI
- **Azure OpenAI** — Azure-hosted OpenAI models
- **Amazon Bedrock** — AWS-hosted models
- **Mistral** — Mistral series models
- **Groq** — High-speed inference
- **Cerebras** — High-speed inference
- **Cloudflare** — AI Gateway + Workers AI
- **xAI** — Grok series
- **OpenRouter** — Unified API gateway
- **Vercel AI Gateway**
- **ZAI** / **OpenCode Zen** / **OpenCode Go**
- **Hugging Face** — Open-source model inference
- **Fireworks** / **Together AI**
- **Kimi For Coding** — Coding-specific model
- **MiniMax** — M2.5 and other models
- **Xiaomi MiMo** — Includes China/Amsterdam/Singapore Token Plans
- **Ollama** — Local models
- **DeepSeek** — DeepSeek V3/R1

## Custom Providers

Add custom providers in `~/.pi/agent/models.json` (must be compatible with OpenAI/Anthropic/Google API format):

```json
{
  "providers": {
    "my-provider": {
      "baseURL": "https://api.example.com/v1",
      "apiKey": "${MY_API_KEY}",
      "models": ["model-a", "model-b"]
    }
  }
}
```

Custom OAuth providers or other API formats require an Extension.

## streamProxy

Browser-side proxy stream function, forwards LLM requests through a backend to avoid CORS:

```ts
import { streamProxy } from "@earendil-works/pi-ai";
import { Agent } from "@earendil-works/pi-agent-core";

const agent = new Agent({
  streamFn: (model, context, options) =>
    streamProxy(model, context, { ...options, authToken, proxyUrl }),
});
```