# PoYo GPT-5.6 Responses API Reference

## Endpoint

- Responses API: `POST https://api.poyo.ai/v1/responses`
- Source docs: <https://docs.poyo.ai/api-manual/chat-series/responses>
- Model page: <https://poyo.ai/models/gpt-5-6>

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

- `gpt-5-6-sol`
- `gpt-5-6-terra`
- `gpt-5-6-luna`

Use an exact id listed on the current PoYo model page. Do not send `gpt-5-6` as an assumed alias.

## Request Schema

Common fields documented by the Responses API:

- `model` string, required
- `input` string or structured input array, required
- `instructions` string, optional
- `tools` array, optional
- `tool_choice` string or object, optional
- `max_output_tokens` integer, optional
- `stream` boolean, optional
- `reasoning` object, optional
- `text` object, optional
- `previous_response_id` string, optional
- `temperature` number, optional when supported by the selected model
- `top_p` number, optional when supported by the selected model

Always verify current field and tool support in the PoYo docs before relying on model-specific options.

## Basic Text Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/v1/responses" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gpt-5-6-luna",
    "instructions": "You are a concise senior backend reviewer. Return findings first.",
    "input": "Review an API rollout plan and list the three highest operational risks.",
    "max_output_tokens": 700
  }'
```

## Structured Input Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/v1/responses" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gpt-5-6-terra",
    "input": [
      {
        "role": "developer",
        "content": "Answer as a short implementation checklist."
      },
      {
        "role": "user",
        "content": "Plan a safe database migration for a high-traffic API."
      }
    ],
    "reasoning": {
      "effort": "medium"
    },
    "max_output_tokens": 900
  }'
```

## Streaming Example

Use streaming only when the client can consume SSE.

```bash
curl --fail-with-body --no-buffer --request POST \
  --url "https://api.poyo.ai/v1/responses" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gpt-5-6-sol",
    "input": "Draft five concise release-note titles for an AI API update.",
    "stream": true,
    "max_output_tokens": 180
  }'
```

## Typical Response Shape

```json
{
  "code": 200,
  "data": {
    "id": "resp_example",
    "object": "response",
    "status": "completed",
    "model": "gpt-5-6-luna",
    "output": [
      {
        "type": "message",
        "role": "assistant",
        "content": [
          {
            "type": "output_text",
            "text": "..."
          }
        ]
      }
    ],
    "usage": {
      "input_tokens": 42,
      "output_tokens": 180,
      "total_tokens": 222
    }
  }
}
```

## Practical Guidance

- Read assistant text from supported `data.output` message content blocks rather than assuming a Chat Completions `choices` array.
- Preserve `data.id` if a later call will use `previous_response_id`.
- Treat tool calls as untrusted model output until the application validates the tool name and arguments.
- Avoid logging private input, tool arguments, media content, API keys, or raw authorization headers.
