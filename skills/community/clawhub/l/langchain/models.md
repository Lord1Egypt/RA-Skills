# Models — Initialization, Parameters, and Provider Differences

## init_chat_model

```python
from langchain.chat_models import init_chat_model
model = init_chat_model("openai:gpt-4.1-mini", temperature=0, timeout=30, max_retries=2)
```

- Provider-prefixed strings (`openai:`, `anthropic:`, `google_genai:`, `bedrock_converse:`, `ollama:`) avoid importing a partner class per branch — the clean way to honor `chat_provider` from config.
- The partner package must be installed anyway (`langchain-openai`, `langchain-anthropic`, …); `init_chat_model` only defers the import.
- `configurable_fields=("model", "temperature")` makes the model swappable at invoke time — pair with `configurable_alternatives` for A/B runs.
- Embeddings have the same door: `init_embeddings("openai:text-embedding-3-small")`.

## Parameters That Behave Differently Than Expected

| Parameter | Reality |
|---|---|
| `temperature=0` | Not determinism. Same prompt can still differ across requests, model revisions, and load-balanced backends — never assert exact strings in tests |
| `max_tokens` | Caps the OUTPUT only, and a truncated response comes back as a valid message with `finish_reason: length` — check it before parsing |
| `timeout` | Per HTTP request, not per chain. With `max_retries=2` the worst case is roughly 3× timeout plus backoff |
| `max_retries` | Client-level, retries transport errors and 429s with backoff — this is the layer to keep; `.with_retry` is for parse failures (SKILL.md Core Rule 4) |
| `streaming` | Some clients need it set to emit tokens; some emit usage only with `stream_usage=True` |
| `model_kwargs` | Escape hatch for provider params LangChain does not model; typos land at the provider as a 400, not at import |
| Reasoning-model params | Reasoning models often reject `temperature` and bill hidden reasoning tokens as output — read `usage_metadata`, not your own estimate |

## Messages and Content Blocks

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
```

- Tuple shorthand in templates: `("system", "…"), ("human", "{q}"), ("placeholder", "{history}")`.
- Multimodal input is a list of content parts on a `HumanMessage` — text plus an image part (URL or base64 data). Provider support and size limits differ; a rejected image usually arrives as a generic 400.
- LangChain 1.x exposes `.content_blocks` on messages: a provider-agnostic view with typed blocks (`text`, `reasoning`, `tool_call`, citations). Read `.content_blocks` instead of branching on each provider's raw `content` shape; raw `content` stays available for provider-specific work.
- `AIMessage.tool_calls` is the normalized list (`name`, `args`, `id`) — always prefer it over parsing the raw payload.
- `response_metadata` carries finish reason, model name, and provider ids; `usage_metadata` carries token counts.

## Provider Differences That Change Code

- **System messages**: some providers accept exactly one, at the start. Concatenate rather than emitting several, and never place one after a tool exchange.
- **Tool-call pairing**: every `tool_call` id must be answered by a `ToolMessage` with that id before the next model call (SKILL.md Core Rule 7).
- **JSON modes**: `json_mode` guarantees syntactic JSON, not your schema; `json_schema`/structured outputs enforce the schema where supported.
- **Parallel tool calls**: some providers emit several tool calls in one message and some clients expose a flag to disable that. Code that assumes one call per turn breaks the day the model batches two.
- **Token accounting**: streaming responses omit usage unless requested; Anthropic-style caching reports cache-read and cache-write tokens separately (`prompt-caching` covers the strategy).
- **Local models via Ollama**: the context window is a server-side setting, so silent truncation replaces the explicit context-length error you get from hosted APIs.

## Choosing Per Call, Not Per App

Model choice is a per-call decision: extraction and routing run fine on the small model, final synthesis often does not. Route explicitly with `configurable_alternatives` or two named chains — do not let one global `model` variable make the expensive choice everywhere by default (SKILL.md Cost Grows Quadratically In Agent Steps).

## Embeddings

- The embedding model is part of the index: querying with a different model than you indexed with returns nonsense with no error. Store the model name in the collection metadata and assert it at startup.
- Dimensions must match the store's configured vector size; mismatch is a store-level error at insert, or a silent accuracy collapse for stores that pad.
- `embed_documents` (batch) vs `embed_query` (single) exist because some models use different prefixes or instructions for each side — never substitute one for the other.
