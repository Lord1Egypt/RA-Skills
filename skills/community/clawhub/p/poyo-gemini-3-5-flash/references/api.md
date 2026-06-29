# PoYo Gemini 3.5 Flash API Reference

## Endpoints

- OpenAI-compatible chat: `POST https://api.poyo.ai/v1/chat/completions`
- Gemini Native Format: `POST https://api.poyo.ai/v1beta/models/gemini-3.5-flash:generateContent`
- Gemini Native streaming: `POST https://api.poyo.ai/v1beta/models/gemini-3.5-flash:streamGenerateContent`
- Chat source docs: <https://docs.poyo.ai/api-manual/chat-series/chat-completions>
- Gemini source docs: <https://docs.poyo.ai/api-manual/chat-series/gemini-native-format>
- Model page: <https://poyo.ai/models/gemini-3-5-flash>

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

- `gemini-3.5-flash`: Gemini 3.5 Flash chat model on PoYo.

## OpenAI-Compatible Request Fields

Common fields:

- `model` string, required
- `messages` array, required
- `temperature` number, optional
- `max_tokens` integer, optional
- `stream` boolean, optional
- `top_p` number, optional
- `stop` string or array, optional
- `n` integer, optional

Each message usually includes:

- `role`: `system`, `user`, or `assistant`
- `content`: message text or supported content structure

## Gemini Native Request Fields

Common fields:

- `contents` array, required
- `generationConfig` object, optional
- `safetySettings` array, optional

Each content item usually includes:

- `role`: `user` or `model`
- `parts`: array containing text or inline data parts

Always verify current field support in the PoYo docs before relying on optional parameters.

## OpenAI-Compatible Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/v1/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gemini-3.5-flash",
    "messages": [
      {
        "role": "system",
        "content": "You are a concise engineering planning assistant. Reply with a short checklist."
      },
      {
        "role": "user",
        "content": "Plan a safe rollout for a new chat model endpoint."
      }
    ],
    "temperature": 0.4,
    "max_tokens": 500
  }'
```

## Gemini Native Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/v1beta/models/gemini-3.5-flash:generateContent" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "contents": [
      {
        "role": "user",
        "parts": [
          {
            "text": "Summarize the API launch risks in three bullets."
          }
        ]
      }
    ],
    "generationConfig": {
      "temperature": 0.4,
      "maxOutputTokens": 500
    }
  }'
```

## Streaming Example

Use streaming only when the client can consume streaming responses.

```bash
curl --fail-with-body --no-buffer --request POST \
  --url "https://api.poyo.ai/v1/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gemini-3.5-flash",
    "messages": [
      {
        "role": "user",
        "content": "Generate five short release note titles."
      }
    ],
    "stream": true,
    "max_tokens": 160
  }'
```

## Typical Chat Response

```json
{
  "code": 200,
  "data": {
    "id": "chatcmpl_example",
    "object": "chat.completion",
    "model": "gemini-3.5-flash",
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

- Use `/v1/chat/completions` for OpenAI-style chat clients.
- Use Gemini Native Format when the integration already expects Gemini `contents` and `parts`.
- Set token limits to control response length.
- Use a system prompt for role, format, and safety boundaries.
- Avoid logging private user messages, inline media data, API keys, or raw authorization headers.
