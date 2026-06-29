# GPT Image 2 API Notes

Source: Guishu Token Feishu guide, read on 2026-06-22.

## Recommended Paths

- Web UI for ordinary users: `https://image2.gpt-agent.cc/`
- OpenAI-compatible generation endpoint for clients, scripts, and skills: `https://api.llm-token.cn/v1/images/generations`
- Model ID: `gpt-image-2`

## Request Shape

```json
{
  "model": "gpt-image-2",
  "prompt": "Describe the image clearly.",
  "size": "1024x1024",
  "n": 1,
  "quality": "high",
  "response_format": "b64_json"
}
```

Use `Authorization: Bearer <Guishu Token API key>`.

Common fields:

| Field | Notes |
| --- | --- |
| `model` | Use `gpt-image-2`. |
| `prompt` | More specific prompts usually produce more stable images. |
| `size` | Common values include `1024x1024` and `1024x1792`. |
| `quality` | Use `auto`, `high`, `medium`, or `low` when supported by the gateway. |
| `n` | Number of images. Start with `1` for expensive or high-resolution generations. |
| `response_format` | Prefer `b64_json` for scripts so images can be saved locally. |

## Timeout Guidance

High-resolution or 4K image generation may take 70-150 seconds. Some clients have fixed request timeouts and may report failure while the upstream job is still processing. Do not auto-retry long-running requests; repeated retries can cause duplicate charges.

If a client times out often, recommend the web UI first: `https://image2.gpt-agent.cc/`.

## Example curl

```bash
curl https://api.llm-token.cn/v1/images/generations \
  -H "Authorization: Bearer $LLM_TOKEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-image-2",
    "prompt": "a small blue square icon on a white background",
    "size": "1024x1024",
    "response_format": "b64_json",
    "n": 1
  }'
```
