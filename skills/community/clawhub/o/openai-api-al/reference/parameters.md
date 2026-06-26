# Reference — Common Parameters

Frequently used parameters for chat, responses, and embeddings. Set cost-capping params on **every** paid call.

## Chat (`openai_chat`)

| Param | Type | Default | Notes |
|-------|------|---------|-------|
| `model` | string | — | Required. e.g. `gpt-4o-mini`. |
| `messages` | array | — | Required. Role-tagged turns. |
| `max_tokens` | int | (model max) | **Always set** to cap cost. |
| `temperature` | number | 1 | 0–2. Lower = deterministic. |
| `top_p` | number | 1 | Nucleus sampling (alt to temperature). |
| `frequency_penalty` | number | 0 | -2..2, reduce repetition. |
| `presence_penalty` | number | 0 | -2..2, encourage new topics. |
| `stop` | string/array | — | Stop sequences. |
| `tools` / `tool_choice` | array/string | — | Function calling. |
| `response_format` | object | — | `{type:"json_object"}` or `json_schema`. |
| `seed` | int | — | Reproducibility (best-effort). |

## Responses (`openai_responses`)

| Param | Type | Notes |
|-------|------|-------|
| `model` | string | Required. e.g. `gpt-4.1-mini`, `o4-mini`. |
| `input` | string/array | Required. The user input. |
| `instructions` | string | System-level guidance. |
| `max_output_tokens` | int | **Always set** to cap cost. |
| `temperature` | number | 0–2. |
| `tools` / `tool_choice` | array/string | Built-in & function tools. |
| `text` | object | Output format incl. `json_schema` (structured output). |
| `reasoning` | object | Reasoning effort for o-series. |

## Embeddings (`openai_embeddings`)

| Param | Type | Notes |
|-------|------|-------|
| `model` | string | `text-embedding-3-small` (1536) / `-large` (3072). |
| `input` | string/array | **Batch** as an array to save overhead. |
| `dimensions` | int | Truncate output dims (3-series). |

## Images (`openai_image_generate`)

| Param | Type | Notes |
|-------|------|-------|
| `prompt` | string | Required. |
| `model` | string | Default `gpt-image-1`. |
| `size` | string | e.g. `1024x1024`. |
| `n` | int | Each image is billed. |

## Cost-relevant defaults to remember

- Set `max_tokens` / `max_output_tokens` on every text call.
- Default models: `gpt-4o-mini`, `text-embedding-3-small`.
- Lower `temperature` for repeatable output.

> Verification needed: confirm parameter names/ranges with <https://platform.openai.com/docs/api-reference>.
