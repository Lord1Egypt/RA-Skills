# PoYo GPT-5.2 Chat Completions API Reference

## Endpoint

- Chat completions: `POST https://api.poyo.ai/v1/chat/completions`
- Source docs: <https://docs.poyo.ai/api-manual/chat-series/chat-completions>

## Auth

Send:

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Get API keys from <https://poyo.ai/dashboard/api-key>.

Recommended skill env var:

- `POYO_API_KEY`

## Model

- `gpt-5.2`: OpenAI-compatible chat completion model on PoYo.

## Request Schema

Common fields:

- `model` string, required
- `messages` array, required
- `temperature` number, optional
- `max_tokens` integer, optional
- `stream` boolean, optional
- `top_p` number, optional
- `frequency_penalty` number, optional
- `presence_penalty` number, optional
- `stop` string or array, optional
- `n` integer, optional

Each message usually includes:

- `role`: `system`, `user`, or `assistant`
- `content`: message text or supported content structure

Always verify current field support in the PoYo docs before relying on optional parameters.

## Basic Chat Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/v1/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gpt-5.2",
    "messages": [
      {
        "role": "system",
        "content": "You are a concise API launch advisor. Reply with a short checklist."
      },
      {
        "role": "user",
        "content": "Give me a production checklist for launching an AI media generation endpoint."
      }
    ],
    "temperature": 0.4,
    "max_tokens": 400
  }'
```

## Streaming Example

Use streaming only when the client can consume SSE.

```bash
curl --fail-with-body --no-buffer --request POST \
  --url "https://api.poyo.ai/v1/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gpt-5.2",
    "messages": [
      {
        "role": "user",
        "content": "Generate 5 short titles about AI video generation."
      }
    ],
    "stream": true,
    "max_tokens": 160
  }'
```

## Typical Response

```json
{
  "code": 200,
  "data": {
    "id": "chatcmpl_example",
    "object": "chat.completion",
    "model": "gpt-5.2",
    "choices": [
      {
        "index": 0,
        "message": {
          "role": "assistant",
          "content": "..."
        },
        "finish_reason": "stop"
      }
    ],
    "usage": {
      "prompt_tokens": 28,
      "completion_tokens": 120,
      "total_tokens": 148
    }
  }
}
```

## Practical Guidance

- Use `/v1/chat/completions` for synchronous chat.
- Use `/api/generate/submit` for async image, video, music, and 3D generation instead.
- Set `max_tokens` to control response length.
- Use a system prompt for role, format, and safety boundaries.
- Avoid logging private user messages, API keys, or raw authorization headers.
