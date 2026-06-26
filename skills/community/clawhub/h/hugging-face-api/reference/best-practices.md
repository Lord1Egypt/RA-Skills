# Reference — Best Practices

Four pillars: discover for free, control cost, respect licensing, protect the token.

---

## 1. Discovery is free — use it first

- `hf_search_models`, `hf_model_info`, `hf_search_datasets`, and `hf_list_inference_models` are **free** (Hub + router list).
- Always discover and confirm support **before** spending on inference.
- Never hardcode a model id you have not confirmed is runnable.

## 2. Control cost

Inference (`hf_chat`, `hf_embeddings`) is **billed per provider**.

- Set `max_tokens` on every `hf_chat` call.
- Prefer smaller models when they meet quality needs.
- Batch embeddings: pass an array of `inputs`, not one call per item.
- Cache embeddings and deterministic completions.
- Track the `usage` returned by `hf_chat`.

## 3. Respect licensing

- Read the model card license via `hf_model_info` → `cardData.license` **before** downstream use.
- Honor restrictions: commercial use, redistribution, gated access, attribution.
- The same applies to datasets — check the dataset card.

## 4. Protect the token

- Never print, log, or echo the `hf_` token. The server redacts it; do not work around that.
- Use a least-privilege token (read for discovery; inference only where needed).
- Use placeholders (`your_hf_token`) in any shared config; inject the real value from secrets.
- Rotate the token periodically and on suspected exposure.

---

## Reproducibility

- Pin exact model ids (and revisions where available).
- Use the **same embedding model** for indexing and querying.
- Record the model id and `usage` with each result.

---

## Quick do/don't

| Do | Don't |
|----|-------|
| Confirm support before `hf_chat` | Call a model blind and hit `model_not_supported` |
| Batch embeddings | One call per item |
| Set `max_tokens` | Leave generation unbounded |
| Check the license | Ship a model with incompatible terms |
| Redact/never print the token | Log the token |
