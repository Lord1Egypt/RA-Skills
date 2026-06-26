# Reference — APIs and Tools

Hugging Face is reached through two base URLs. Knowing which one a tool uses tells you whether it is free.

---

## Hub vs Router

| Family | Base URL | Purpose | Cost |
|--------|----------|---------|------|
| **Hub API** | `https://huggingface.co` | Search/inspect models, datasets, Spaces; whoami | **Free** |
| **Inference router** | `https://router.huggingface.co` | Chat completions, embeddings | **Billed** (per provider) |

Both use the same auth header: `Authorization: Bearer <HF_TOKEN>`.

---

## The 7 tools mapped to endpoints

| Tool | Family | Method + path | Cost |
|------|--------|---------------|------|
| `hf_chat` | Router | `POST /v1/chat/completions` | Billed |
| `hf_embeddings` | Router | `POST /hf-inference/models/{model}/pipeline/feature-extraction` | Billed |
| `hf_list_inference_models` | Router | `GET /v1/models` | Free |
| `hf_search_models` | Hub | `GET /api/models` | Free |
| `hf_model_info` | Hub | `GET /api/models/{id}` | Free |
| `hf_search_datasets` | Hub | `GET /api/datasets` | Free |
| `hf_request` | Both | any path on `hub` or `router` | Depends |

---

## `hf_request` — the generic escape hatch

Use it for any endpoint without a dedicated tool. Pick the base with `api`:

- `api: "hub"` → `https://huggingface.co`
- `api: "router"` → `https://router.huggingface.co`

Examples:

```json
{ "api": "hub", "path": "/api/whoami-v2" }
{ "api": "hub", "path": "/api/spaces?search=llm&limit=5" }
{ "api": "hub", "path": "/api/datasets/rajpurkar/squad" }
{ "api": "router", "method": "POST", "path": "/v1/chat/completions", "body": { "model": "Qwen/Qwen2.5-7B-Instruct", "messages": [{ "role": "user", "content": "Hi" }], "max_tokens": 16 } }
```

---

## Pointer to full API docs

For complete tool input schemas, output shapes, and example I/O, see the MCP tools reference: `../../mcp/docs/03-tools-reference.md`. For endpoint details beyond what the tools cover, consult https://huggingface.co/docs.
