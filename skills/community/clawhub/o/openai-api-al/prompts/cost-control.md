# Prompt — Cost Control

## Purpose

Enforce cost discipline before and during OpenAI calls. Every chat/responses/embeddings/image call is **billed**.

## Reusable template

```
Before calling OpenAI for: {{task}}

1. Is OpenAI necessary, or can I use cache/local/heuristic? -> {{justification}}
2. Cheapest capable model: {{model}}   (default gpt-4o-mini / text-embedding-3-small)
3. Output cap: max_tokens={{max_tokens}}
4. Batchable inputs? {{batch_plan}}
5. Cacheable? key = {{cache_key}}
6. Loop guard: max {{max_calls}} calls, no uncontrolled retries
7. After call: read usage.total_tokens and report it

If any answer increases cost without value, stop and revise.
```

## Variables

| Variable | Meaning |
|----------|---------|
| `{{task}}` | The task. |
| `{{justification}}` | Why a paid call is needed. |
| `{{model}}` | Chosen cheapest model. |
| `{{max_tokens}}` | Output cap. |
| `{{batch_plan}}` | How inputs are batched. |
| `{{cache_key}}` | Cache identity. |
| `{{max_calls}}` | Hard call ceiling. |

## Example

```
Task: embed 500 FAQ chunks
1. Necessary? Yes, building a search index.
2. Model: text-embedding-3-small
3. Cap: N/A (embeddings)
4. Batch: send all 500 in one array input
5. Cache: key = sha256(chunk_text); skip already-embedded
6. Loop guard: 1 call (batched)
7. Report usage.total_tokens
```

## Bad

> Loop over 500 chunks calling `openai_embeddings` once per chunk with no cache. — 500 billed calls; massive overhead and cost.

## Good

> One batched `openai_embeddings` call with all 500 chunks; skip chunks already cached. Report total tokens.

## Bad

> `openai_chat` with no `max_tokens` on `gpt-5` to write a one-line label. — Unbounded, expensive output on an overpowered model.

## Good

> `openai_chat` on `gpt-4o-mini` with `max_tokens=10` for the label.

> Verification needed: confirm pricing/limits with <https://platform.openai.com/docs/api-reference>.
