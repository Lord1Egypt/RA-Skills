# PoYo Claude Fable 5 Messages API Reference

## Endpoint

- Messages API: `POST https://api.poyo.ai/v1/messages`
- Source docs: <https://docs.poyo.ai/api-manual/chat-series/claude-messages>
- Model page: <https://poyo.ai/models/claude-fable-5>

## Auth

Send:

```http
x-api-key: YOUR_API_KEY
anthropic-version: 2023-06-01
Content-Type: application/json
```

Get API keys from <https://poyo.ai/dashboard/api-key>.

Recommended skill env var:

- `POYO_API_KEY`

## Model

- `claude-fable-5`: Claude Messages-compatible model on PoYo.

## Request Schema

Common fields:

- `model` string, required
- `messages` array, required
- `max_tokens` integer, required by common Claude-compatible clients
- `system` string or supported content blocks, optional
- `stream` boolean, optional
- `stop_sequences` array, optional
- `metadata` object, optional
- `tools` array, optional
- `tool_choice` string or object, optional
- `cache_control` object, optional when supported
- `output_config` object, optional when supported

Each message usually includes:

- `role`: `user` or `assistant`
- `content`: text or documented content blocks

Always verify current field and content-block support in the PoYo docs before relying on optional parameters.

## Basic Messages Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/v1/messages" \
  --header "x-api-key: YOUR_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "claude-fable-5",
    "max_tokens": 900,
    "system": "You are a concise senior engineering reviewer. Return concrete findings first.",
    "messages": [
      {
        "role": "user",
        "content": "Review this rollout plan for hidden operational risks and list the top three."
      }
    ]
  }'
```

## Tool Use Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/v1/messages" \
  --header "x-api-key: YOUR_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "claude-fable-5",
    "max_tokens": 800,
    "tools": [
      {
        "name": "get_ticket",
        "description": "Fetch a support ticket by id",
        "input_schema": {
          "type": "object",
          "properties": {
            "ticket_id": {
              "type": "string"
            }
          },
          "required": ["ticket_id"]
        }
      }
    ],
    "tool_choice": "auto",
    "messages": [
      {
        "role": "user",
        "content": "Check ticket T-123 and summarize the customer impact."
      }
    ]
  }'
```

## Streaming Example

Use streaming only when the client can consume streaming responses.

```bash
curl --fail-with-body --no-buffer --request POST \
  --url "https://api.poyo.ai/v1/messages" \
  --header "x-api-key: YOUR_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "claude-fable-5",
    "max_tokens": 600,
    "stream": true,
    "messages": [
      {
        "role": "user",
        "content": "Draft a concise incident update for an internal engineering channel."
      }
    ]
  }'
```

## Typical Response Shape

```json
{
  "code": 200,
  "data": {
    "id": "msg_example",
    "type": "message",
    "role": "assistant",
    "content": [
      {
        "type": "text",
        "text": "..."
      }
    ],
    "model": "claude-fable-5",
    "stop_reason": "end_turn",
    "usage": {
      "input_tokens": 120,
      "output_tokens": 180
    }
  }
}
```

## Practical Guidance

- Use `system` for role, format, and policy constraints rather than adding a system role to `messages`.
- Use tools only when the application can validate and safely execute returned calls.
- Parse documented content blocks instead of assuming the response is a single string.
- Avoid logging private messages, image content, tool inputs, API keys, or raw API key headers.
