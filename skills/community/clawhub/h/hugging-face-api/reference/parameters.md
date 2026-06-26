# Reference — Parameters

Parameters for the chat and search tools, with guidance on sensible values.

---

## `hf_chat` parameters

| Field | Type | Required | Guidance |
|-------|------|----------|----------|
| `model` | string | Yes | Exact model id from `hf_list_inference_models`. Pin it. |
| `messages` | array of `{role, content}` | Yes | Roles: `system`, `user`, `assistant`. |
| `max_tokens` | integer | No | **Always set this** to bound cost. Use the smallest value that fits the answer. |
| `temperature` | number | No | 0 for deterministic/factual; 0.7+ for creative. |
| `top_p` | number | No | Nucleus sampling; usually leave default or use one of temperature/top_p. |
| `stream` | boolean | No | Stream tokens if the client and provider support it. |

Example:

```json
{
  "model": "Qwen/Qwen2.5-7B-Instruct",
  "messages": [
    { "role": "system", "content": "Answer in one sentence." },
    { "role": "user", "content": "What is RAG?" }
  ],
  "max_tokens": 60,
  "temperature": 0.2
}
```

---

## `hf_embeddings` parameters

| Field | Type | Required | Guidance |
|-------|------|----------|----------|
| `model` | string | No | Defaults to `sentence-transformers/all-MiniLM-L6-v2`. Pin for reproducibility. |
| `inputs` | string \| string[] | Yes | Prefer a **batch** (array) over many single calls. |

---

## `hf_search_models` parameters

| Field | Type | Required | Guidance |
|-------|------|----------|----------|
| `search` | string | No | Free-text query. |
| `author` | string | No | Org/user, e.g. `meta-llama`, `BAAI`. |
| `filter` | string | No | Tag/task, e.g. `text-generation`, `feature-extraction`. |
| `sort` | string | No | `downloads`, `likes`, `lastModified`. |
| `direction` | string\|number | No | `-1` for descending. |
| `limit` | integer | No | Keep small (e.g. 3-10) for focused results. |

---

## `hf_search_datasets` parameters

| Field | Type | Required | Guidance |
|-------|------|----------|----------|
| `search` | string | No | Free-text query. |
| `limit` | integer | No | Keep small for focused results. |

---

## `hf_request` parameters

| Field | Type | Required | Guidance |
|-------|------|----------|----------|
| `api` | `"hub"`\|`"router"` | No | `hub` (free) is default; `router` for inference. |
| `method` | string | No | Defaults `GET`. |
| `path` | string | Yes | Include query string if needed. |
| `body` | object | No | JSON body for POST/PUT. |
