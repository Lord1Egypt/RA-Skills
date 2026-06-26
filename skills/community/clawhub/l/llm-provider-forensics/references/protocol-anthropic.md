# Anthropic-Compatible Protocol Rules

## Common probe
- `POST /v1/messages`

## Required headers
- `x-api-key: <key>`
- `anthropic-version: 2023-06-01`

## Minimal body
```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 64,
  "messages": [{"role": "user", "content": "Reply with exactly OK"}]
}
```

## Notes
- Many Claude-compatible gateways do not expose a canonical model-list endpoint.
- If a gateway also supports OpenAI-compatible paths, probe both families.
- Record whether response shape matches Anthropic native schema or a wrapper.
