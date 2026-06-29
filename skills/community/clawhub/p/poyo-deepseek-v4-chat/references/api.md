# PoYo DeepSeek V4 Chat API Reference

## Endpoint

- Chat completions: `POST https://api.poyo.ai/v1/chat/completions`
- Source docs: <https://docs.poyo.ai/api-manual/chat-series/chat-completions>
- Flash model page: <https://poyo.ai/models/deepseek-v4-flash>
- Pro model page: <https://poyo.ai/models/deepseek-v4-pro>

## Auth

Send:

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Get API keys from <https://poyo.ai/dashboard/api-key>.

Recommended skill env var:

- `POYO_API_KEY`

## Models

- `deepseek-v4-flash`: DeepSeek V4 Flash chat model on PoYo.
- `deepseek-v4-pro`: DeepSeek V4 Pro chat model on PoYo.

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

## Flash Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/v1/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "deepseek-v4-flash",
    "messages": [
      {
        "role": "system",
        "content": "You are a concise coding assistant. Reply with direct steps."
      },
      {
        "role": "user",
        "content": "Explain how to add request validation to this API endpoint."
      }
    ],
    "temperature": 0.3,
    "max_tokens": 500
  }'
```

## Pro Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/v1/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "deepseek-v4-pro",
    "messages": [
      {
        "role": "system",
        "content": "You are a careful analysis assistant. Separate facts, assumptions, and risks."
      },
      {
        "role": "user",
        "content": "Analyze this migration plan and identify the highest-risk dependencies."
      }
    ],
    "temperature": 0.2,
    "max_tokens": 900
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
    "model": "deepseek-v4-flash",
    "messages": [
      {
        "role": "user",
        "content": "Draft five short support reply templates."
      }
    ],
    "stream": true,
    "max_tokens": 220
  }'
```

## Typical Response

```json
{
  "code": 200,
  "data": {
    "id": "chatcmpl_example",
    "object": "chat.completion",
    "model": "deepseek-v4-flash",
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

- Use Flash when the workflow prioritizes lighter chat, coding help, or high-throughput text handling.
- Use Pro when the workflow needs more careful reasoning, code review, or long-context analysis.
- Set `max_tokens` to control response length.
- Use a system prompt for role, format, and safety boundaries.
- Avoid logging private user messages, API keys, or raw authorization headers.
