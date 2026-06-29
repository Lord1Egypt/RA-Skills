# Pi Provider Authentication

## Subscription (OAuth)

`/login → select provider → complete OAuth in browser → auto-refresh token`

- ChatGPT Plus/Pro (Codex)
- Claude Pro/Max
- GitHub Copilot

## API Key (Environment Variables)

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

| Provider | Environment Variable |
|----------|---------------------|
| Anthropic | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Azure OpenAI | `AZURE_OPENAI_API_KEY` (+ `AZURE_OPENAI_BASE_URL`) |
| DeepSeek | `DEEPSEEK_API_KEY` |
| Google Gemini | `GEMINI_API_KEY` |
| Vertex AI | Application Default Credentials |
| Bedrock | `AWS_PROFILE` / `AWS_ACCESS_KEY_ID+SECRET` |
| Mistral | `MISTRAL_API_KEY` |
| Groq | `GROQ_API_KEY` |
| Cerebras | `CEREBRAS_API_KEY` |
| Cloudflare AI Gateway | `CLOUDFLARE_API_KEY` (+ ACCOUNT_ID, GATEWAY_ID) |
| Cloudflare Workers AI | `CLOUDFLARE_API_KEY` (+ ACCOUNT_ID) |
| xAI | `XAI_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| Vercel AI Gateway | `AI_GATEWAY_API_KEY` |
| Hugging Face | `HF_TOKEN` |
| Fireworks | `FIREWORKS_API_KEY` |
| Together AI | `TOGETHER_API_KEY` |
| Kimi For Coding | `KIMI_API_KEY` |
| MiniMax | `MINIMAX_API_KEY` |
| Xiaomi MiMo | `XIAOMI_API_KEY` (+ Token Plan CN/AMS/SGP) |

## Auth File

`~/.pi/agent/auth.json` (0600 permissions):

```json
{
  "anthropic": { "type": "api_key", "key": "sk-ant-..." },
  "openai": { "type": "api_key", "key": "!security find-generic-password -ws 'openai'" },
  "deepseek": { "type": "api_key", "key": "MY_DEEPSEEK_KEY" }
}
```

key supports three formats:
- Literal: used directly
- Env var: auto-detected without `$` prefix
- Shell command: `!command` executed and stdout captured (cached per process lifetime)

## Custom Providers

`~/.pi/agent/models.json`:

```json
{
  "providers": {
    "ollama": {
      "baseURL": "http://localhost:11434/v1",
      "apiKey": "ollama",
      "api": "openai-completions",
      "models": [
        { "id": "llama3", "name": "Llama 3", "reasoning": false, "input": ["text"],
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
          "contextWindow": 8192, "maxTokens": 4096 }
      ]
    }
  }
}
```

Custom OAuth requires an Extension.

## Priority

`--api-key flag` > `auth.json` > env vars > `models.json`

## Provider Parameters

- Azure: `AZURE_OPENAI_API_KEY` + `AZURE_OPENAI_BASE_URL` or `AZURE_OPENAI_RESOURCE_NAME`
- Bedrock: supports Profile, IAM Keys, Bearer Token, ECS IRSA
- Cloudflare: AIG routes OpenAI/Anthropic/Workers AI through different routes
- Vertex: requires `GOOGLE_CLOUD_PROJECT` + `GOOGLE_CLOUD_LOCATION`