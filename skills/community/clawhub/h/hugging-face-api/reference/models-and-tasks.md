# Reference — Models and Tasks

How to choose a model, what the common pipeline tasks are, and how to confirm a model is runnable through the router.

> Model availability via the router changes over time. **Always confirm with `hf_list_inference_models`** rather than assuming. The lists below are illustrative starting points.

---

## Popular chat / text-generation models

| Model id | Notes |
|----------|-------|
| `meta-llama/Llama-3.1-8B-Instruct` | General-purpose instruct model; gated license. |
| `meta-llama/Llama-3.2-3B-Instruct` | Smaller, cheaper. |
| `Qwen/Qwen2.5-7B-Instruct` | Strong multilingual instruct model. |
| `mistralai/Mistral-7B-Instruct-v0.3` | Compact instruct model. |

Use these with `hf_chat`. Confirm support first.

---

## Popular embedding (feature-extraction) models

| Model id | Notes |
|----------|-------|
| `sentence-transformers/all-MiniLM-L6-v2` | Default; small and fast (384-dim). |
| `BAAI/bge-small-en-v1.5` | Strong small English embedder. |
| `BAAI/bge-base-en-v1.5` | Larger, higher quality. |
| `intfloat/e5-small-v2` | Compact retrieval embedder. |

Use these with `hf_embeddings`. Pick one and use the **same** model for indexing and querying.

---

## Common pipeline tasks

| Pipeline tag | What it does | Tool |
|--------------|--------------|------|
| `text-generation` | Chat / completion | `hf_chat` (or `hf_request` router) |
| `feature-extraction` | Embeddings | `hf_embeddings` |
| `text-classification` | Labels for text | `hf_request` (router pipeline) |
| `summarization` | Summaries | `hf_request` |
| `translation` | Translate text | `hf_request` |
| `automatic-speech-recognition` | Speech to text | `hf_request` |

For tasks without a dedicated tool, use `hf_request` against the appropriate router pipeline path.

> Verification needed: confirm exact pipeline paths for non-chat/non-embedding tasks at https://huggingface.co/docs.

---

## How to find supported inference models

1. Run `hf_list_inference_models` — returns models currently runnable via the router.
2. Cross-check candidates from `hf_search_models` against that list.
3. Use `hf_model_info` to verify the `pipeline_tag` matches your task and to read the license.

If a desired model is **not** listed, you will get `model_not_supported` when you call it — either pick a listed model or enable an inference provider for it in your HF account.
