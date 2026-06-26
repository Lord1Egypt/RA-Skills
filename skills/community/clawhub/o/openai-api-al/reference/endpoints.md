# Reference — Endpoints (Tools)

The OpenAI MCP server exposes 7 tools. Six are dedicated; one is a generic passthrough for full API coverage.

| Tool | HTTP | Billed? | Purpose |
|------|------|---------|---------|
| `openai_chat` | `POST /chat/completions` | Yes | Classic chat completion |
| `openai_responses` | `POST /responses` | Yes | Unified API (tools, structured output, reasoning) |
| `openai_embeddings` | `POST /embeddings` | Yes | Vectors for RAG/search |
| `openai_image_generate` | `POST /images/generations` | Yes | Image generation |
| `openai_moderations` | `POST /moderations` | **Free** | Content safety |
| `openai_models` | `GET /models[/{id}]` | Free | List/inspect models |
| `openai_request` | **any** | Depends | Generic passthrough |

Full schemas and I/O examples: [../../mcp/docs/03-tools-reference.md](../../mcp/docs/03-tools-reference.md).

## Generic passthrough catalog (`openai_request`)

Reach any endpoint by setting `path` (after `/v1`), optional `method`, optional `body`.

| Capability | method | path |
|------------|--------|------|
| Text-to-speech | POST | `/audio/speech` |
| Transcription | POST | `/audio/transcriptions` |
| Audio translation | POST | `/audio/translations` |
| List/delete files | GET/DELETE | `/files`, `/files/{id}` |
| Uploads | POST | `/uploads` |
| Fine-tuning jobs | POST/GET | `/fine_tuning/jobs` |
| Batches | POST/GET | `/batches`, `/batches/{id}` |
| Vector stores | POST/GET | `/vector_stores` |
| Assistants / threads | POST/GET | `/assistants`, `/threads` |
| Model details | GET | `/models/{id}` |

Anything in the official API reference is reachable. See the full API docs catalog at <https://platform.openai.com/docs/api-reference>.

## Choosing chat vs. responses

- `openai_chat` — broadly-compatible `messages` schema; simple flows.
- `openai_responses` — newer; reasoning models, structured output, built-in tools.

> Verification needed: confirm endpoint paths and bodies with <https://platform.openai.com/docs/api-reference>.
