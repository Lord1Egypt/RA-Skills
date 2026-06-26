---
title: Hugging Face Skill
featured: true
---

# Hugging Face Agent Skill

A playbook for agents that use the Hugging Face MCP server. Follow these steps in order. Discover for free first; run billed inference only against confirmed-supported models.

---

## 1. Name

**Hugging Face** — open-source model and dataset discovery plus OpenAI-compatible inference (chat and embeddings) across inference providers, via 7 MCP tools.

## 2. Purpose

Use this skill to find open-source models and datasets on the Hugging Face Hub, confirm which models are runnable through the Inference router, and run chat completions and embeddings — while controlling cost, respecting licenses, and keeping the access token secret.

## 3. When to use Hugging Face

Use it when the task involves:

- **Open-source models** (Llama, Qwen, Mistral, BGE, sentence-transformers, etc.).
- **Model or dataset discovery** — search/inspect the Hub catalog.
- **OpenAI-compatible inference across providers** — one interface, many providers.
- **Embeddings** — vectors for semantic search, RAG, clustering.

## 4. When NOT to use it

- If you need a **specific closed/proprietary model** (e.g. a vendor's flagship), call that vendor's provider directly.
- If the task needs no model at all (pure local computation), skip inference.
- If a cheaper or already-integrated tool already solves the task, use it.

## 5. Environment

Set one secret:

| Variable | Required | Notes |
|----------|----------|-------|
| `HF_TOKEN` | Yes | `hf_...`. Get it at https://huggingface.co/settings/tokens. Never expose it. |

Optional: `HF_HUB_BASE_URL`, `HF_ROUTER_BASE_URL`, `HF_TIMEOUT_MS`, `HF_MAX_RETRIES`, `LOG_LEVEL`.

## 6. Operations (the 7 tools)

| Tool | Use it to | Cost |
|------|-----------|------|
| `hf_search_models` | Search Hub models | Free |
| `hf_model_info` | Inspect one model (license, task) | Free |
| `hf_search_datasets` | Search Hub datasets | Free |
| `hf_list_inference_models` | List models runnable via router | Free |
| `hf_chat` | OpenAI-style chat completion | Billed |
| `hf_embeddings` | Embedding vectors | Billed |
| `hf_request` | Reach any other Hub/router endpoint | Depends |

## 7. Discovery workflow (FREE)

Do this first; it costs nothing.

1. `hf_search_models` — find candidates by task/author/popularity.
2. `hf_model_info` — check `pipeline_tag` and `cardData.license`.
3. `hf_search_datasets` — find data if needed.
4. `hf_list_inference_models` — confirm the chosen model is actually runnable.

## 8. Inference workflow (BILLED)

1. Choose a model that appears in `hf_list_inference_models`.
2. For chat: call `hf_chat` with OpenAI-style `messages` and a bounded `max_tokens`.
3. For vectors: call `hf_embeddings` with a **batch** of `inputs` (default model `sentence-transformers/all-MiniLM-L6-v2`).
4. Report the model id and the returned `usage`.

## 9. Cost control

- Hub discovery is **free** — use it liberally.
- Inference is **billed per provider** — always:
  - Set `max_tokens` on `hf_chat`.
  - Prefer smaller models when quality allows.
  - Batch embeddings (array `inputs`) instead of per-item calls.
  - Cache embeddings and deterministic completions.

## 10. Error handling

| Error | Reaction |
|-------|----------|
| `model_not_supported` (402/403) | Call `hf_list_inference_models`, pick a listed model, retry. |
| `401` invalid token | Stop. Fix `HF_TOKEN`. Do not retry blindly. |
| `402` credits | Stop. Add credits or use a cheaper/free model. |
| `429` rate limit | Back off (server retries); slow down, batch, cache. |

## 11. Security

- **Never** print, log, or echo the `hf_` token. The server redacts it; do not undo that.
- Use a least-privilege token (read for discovery; inference only where needed).
- Use placeholders (`your_hf_token`) in any shared config.

## 12. Reproducibility / model pinning

- Use **exact model ids** (and a revision/commit if available) so runs are repeatable.
- Use the **same embedding model** for indexing and querying in RAG.

## 13. Licensing

- Before downstream use, check the model card's **license** (`hf_model_info` → `cardData.license`).
- Respect usage restrictions (commercial use, redistribution, gated access).

## 14. Agent checklist

- [ ] Confirmed Hugging Face is the right tool (open-source / discovery / embeddings).
- [ ] Discovered model via `hf_search_models` / `hf_model_info` (free).
- [ ] Confirmed it is runnable via `hf_list_inference_models`.
- [ ] Checked the license.
- [ ] Set `max_tokens` (chat) / batched inputs (embeddings).
- [ ] Did not expose the token.
- [ ] Cited the exact model id and reported `usage`.

## 15. Example workflows

- **Find a model → run chat**: `hf_search_models` → `hf_model_info` → `hf_list_inference_models` → `hf_chat`. See `recipes/find-and-run-model.md`.
- **Build embeddings for RAG**: `hf_embeddings` (batch) → store → query. See `recipes/build-embeddings.md`.
- **Dataset lookup**: `hf_search_datasets` → `hf_request` for details. See `recipes/dataset-discovery.md`.

## 16. Common mistakes

- Calling `hf_chat` before confirming the model is supported (causes `model_not_supported`).
- One embedding call per item instead of a batch (slow and costly).
- Skipping the license check.
- Exposing the token in logs or output.
- Omitting `max_tokens`, leading to runaway generation cost.

## 17. Maintenance

- The runnable model list changes — re-run `hf_list_inference_models` rather than hardcoding ids.
- Re-check licenses when adopting a new model.
- Rotate `HF_TOKEN` periodically.
- Confirm endpoint/provider details against https://huggingface.co/docs when behavior changes.
