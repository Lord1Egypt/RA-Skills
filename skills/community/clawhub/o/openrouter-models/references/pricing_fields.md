# OpenRouter pricing field reference

Every model exposes a `pricing` object whose fields are **strings representing
dollars per token** (small floats like `"0.000003"`). Three of them —
`web_search` in particular — are quoted as **per-call** rather than per-token
even though the API does not label the unit, so always sanity-check.

For human-friendly output, the analysis script multiplies by 1,000,000 to
display **$ / 1M tokens** (or **$ / 1M calls** for web search).

## Pricing fields

| Field | Unit | Applies to | Notes |
|---|---|---|---|
| `prompt` | $/token | Input tokens | Always present |
| `completion` | $/token | Output tokens | Always present |
| `input_cache_read` | $/token | Cached input tokens read back | ~90% off prompt for Anthropic / OpenAI / Google |
| `input_cache_write` | $/token | Cached input tokens written | Usually ≥ prompt price; write-once, read-many |
| `web_search` | $/call | Per search invocation (NOT per token) | Quoted as `"0.01"` = **$0.01 per call**, not per token |
| `internal_reasoning` | $/token | Hidden reasoning tokens | Some models charge the same as completion |
| `image` | $/token | Image input tokens | When priced separately from text |
| `audio` | $/token | Audio input tokens | When priced separately from text |

## Sentinel values

| Raw value | Meaning |
|---|---|
| `-1` | Variable / undetermined price (e.g. router/meta models like `openrouter/auto`) |
| `"0"` or `"0.0"` | Free tier (genuinely $0) |
| `"0.000000xxx"` | Real price per token |

The `analyze.py` script treats `-1` as "skip" and `"0"` as genuinely free.

## Architecture fields

```jsonc
"architecture": {
  "modality": "text->text",          // legacy shorthand, prefer the lists below
  "input_modalities": ["text", "image", "file", "audio", "video"],
  "output_modalities": ["text", "image", "audio"],
  "tokenizer": "Router" | "Claude" | "GPT" | "Gemini" | "Llama3" | ...,
  "instruct_type": null
}
```

`modality` is an older compact string (`"text+image->text"`); the
`input_modalities` / `output_modalities` lists are the canonical source.

## Top provider and limits

```jsonc
"top_provider": {
  "context_length": 200000,           // provider-specific override
  "max_completion_tokens": 8192,     // null = unlimited
  "is_moderated": true
}
```

The model's own `context_length` is the global max. `top_provider.context_length`
may be smaller for a specific provider endpoint.

## Other useful fields

| Field | Meaning |
|---|---|
| `canonical_slug` | The URL-friendly identifier, often identical to `id` |
| `hugging_face_id` | Upstream HF repo, when applicable |
| `supported_parameters` | Capabilities: `["tools", "tool_choice", "temperature", "top_p", ...]` |
| `per_request_limits` | `null` or `{"prompt_tokens": ..., "completion_tokens": ...}` |
| `default_parameters` | Provider defaults (temperature, top_p, penalties, etc.) |
| `knowledge_cutoff` | ISO date string or `null` |
| `expiration_date` | Unix timestamp; model deprecation date or `null` |
| `links.details` | Endpoint pricing URL (use `/api/v1/models/{id}/endpoints`) |

## Filtering recipes

| Goal | Flag combination |
|---|---|
| All Claude models | `--family anthropic/` |
| Vision-capable ≥ 1M ctx | `--has-image --min-ctx 1000000` |
| Free + image | `--free --has-image` |
| Cheapest cache-read | `--has-cache --sort input_cache_read --limit 10` |
| All router models | `--family openrouter/` (auto, fusion, bodybuilder, pareto-code) |
| Reasoning-priced models | `--has-reasoning-price` |
| Output-image generators | `--outputs-image` |
