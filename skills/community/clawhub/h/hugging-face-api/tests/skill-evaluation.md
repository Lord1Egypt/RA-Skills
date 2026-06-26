# Tests — Skill Evaluation

Use this checklist to evaluate whether an agent applies the Hugging Face skill correctly.

---

## Evaluation checklist

### Tool selection

- [ ] Chooses Hugging Face only when appropriate (open-source / discovery / embeddings).
- [ ] Uses the generic `hf_request` only for endpoints without a dedicated tool.

### Discovery (free) before inference (billed)

- [ ] Calls `hf_search_models` / `hf_model_info` to find and inspect a model.
- [ ] Calls `hf_list_inference_models` to confirm the model is runnable.
- [ ] Does NOT call `hf_chat` / `hf_embeddings` against an unconfirmed model.

### Cost control

- [ ] Sets `max_tokens` on every `hf_chat` call.
- [ ] Batches embeddings (array `inputs`) instead of per-item calls.
- [ ] Avoids redundant inference (caches / reuses).
- [ ] Reports the returned `usage`.

### Licensing and reproducibility

- [ ] Checks `cardData.license` before downstream use.
- [ ] Pins exact model ids; uses the same embedding model for index and query.

### Security

- [ ] Never prints, logs, or echoes the `hf_` token.
- [ ] Uses placeholders in shared config.

### Error handling

- [ ] On `model_not_supported`: lists models, picks a supported one, retries.
- [ ] On `401`/`402`: stops and reports (no blind retry).
- [ ] On `429`/`5xx`: relies on server backoff, slows down.

---

## Scoring

| Band | Criteria |
|------|----------|
| Pass | All security items + discovery-before-inference + cost control satisfied. |
| Needs work | Functional output but missed cost control or license check. |
| Fail | Exposed token, ran inference blindly, or ignored license. |

---

## Sample scenarios

1. "Answer this with an open-source model." → expects search → confirm → bounded `hf_chat`.
2. "Embed these 200 chunks." → expects a single batched `hf_embeddings` call.
3. "Find a dataset about X." → expects `hf_search_datasets` (free), no inference.
