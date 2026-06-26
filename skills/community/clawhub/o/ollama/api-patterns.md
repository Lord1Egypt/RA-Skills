# API Patterns

## Base URLs

- Native local API: `http://127.0.0.1:11434/api`
- OpenAI-compatible local API: `http://127.0.0.1:11434/v1`
- Optional cloud API: `https://ollama.com/api` or `https://ollama.com/v1` only when the user explicitly chooses cloud execution

## Health Checks

Use the native API for fast factual checks:

```bash
curl -s http://127.0.0.1:11434/api/tags | jq '.models[].name'
curl -s http://127.0.0.1:11434/api/ps | jq '.models[].name'
```

Inspect a specific model before promising capabilities:

```bash
curl -s http://127.0.0.1:11434/api/show -d '{
  "model": "MODEL:TAG"
}' | jq '{capabilities, details, model_info}'
```

## Chat Request

Prefer non-streaming when the next step needs deterministic parsing:

```bash
curl -s http://127.0.0.1:11434/api/chat -d '{
  "model": "MODEL:TAG",
  "messages": [
    {"role": "system", "content": "Return one short answer."},
    {"role": "user", "content": "Say hello."}
  ],
  "stream": false
}' | jq -r '.message.content'
```

## Structured JSON

Use `format: "json"` or a full schema and validate before acting:

```bash
curl -s http://127.0.0.1:11434/api/chat -d '{
  "model": "MODEL:TAG",
  "messages": [
    {"role": "user", "content": "Classify this ticket as bug, feature, or support."}
  ],
  "format": "json",
  "options": {"temperature": 0},
  "stream": false
}' | jq -r '.message.content' | jq
```

## OpenAI-Compatible Clients

For tools that expect OpenAI model names, map a pulled model to the expected name:

```bash
ollama cp MODEL:TAG gpt-3.5-turbo
```

Then point the client at `http://127.0.0.1:11434/v1`.
Verify feature support before assuming tool calling, JSON schema, or vision works the same as a cloud provider.
