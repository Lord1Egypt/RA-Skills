# API Recipes — LM Studio

LM Studio exposes OpenAI-compatible endpoints. Reuse existing clients by changing the base URL and replacing the model identifier with one from the local runtime.

Supported local endpoints include:
- `GET /v1/models`
- `POST /v1/responses`
- `POST /v1/chat/completions`
- `POST /v1/embeddings`
- `POST /v1/completions`

Assume port `1234` only until a reachability check proves it.

## 1. Python Client

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1")
```

Then keep the rest of the client mostly the same, but replace:
- Remote model names.
- Unsupported request fields.
- Assumptions that the local model supports every OpenAI feature.

## 2. TypeScript Client

```ts
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://localhost:1234/v1",
});
```

Before shipping, verify one real request with the intended local model id.

## 3. Chat Completions Smoke Test

```bash
curl -fsS http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "REPLACE_WITH_LOCAL_MODEL_ID",
    "messages": [
      {"role": "system", "content": "Be concise."},
      {"role": "user", "content": "Reply with READY."}
    ],
    "temperature": 0
  }' | jq .
```

Use this first when migrating an existing app from a cloud provider.

## 4. Responses Endpoint

LM Studio also supports the OpenAI-compatible `responses` endpoint, which matters for tools that expect it.

```bash
curl -fsS http://localhost:1234/v1/responses \
  -H "Content-Type: application/json" \
  -d '{
    "model": "REPLACE_WITH_LOCAL_MODEL_ID",
    "input": "Reply with READY."
  }' | jq .
```

Use this if the client, agent framework, or tool already depends on `responses`.

## 5. Embeddings Smoke Test

```bash
curl -fsS http://localhost:1234/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "REPLACE_WITH_LOCAL_EMBEDDING_MODEL_ID",
    "input": ["local embedding test"]
  }' | jq '.data[0].embedding | length'
```

Do not assume a chat model is also the correct embedding model.

## 6. Migration Checklist

When moving an existing OpenAI-based integration to LM Studio:
1. Change the base URL.
2. Replace the model name with a local identifier.
3. Remove unsupported request fields if the first request fails.
4. Verify the exact endpoint you plan to use.
5. Add a timeout and a friendly failure path for when the local server is down.

## 7. Failure Patterns

- `404` or `connection refused` -> wrong base URL or server not listening.
- `model not found` -> cloud model name still hardcoded.
- Empty or weak structured output -> wrong local model for the task, not necessarily wrong prompts.
- Slow requests after a machine sleep or heavy run -> re-check server readiness and loaded-model state.
