# Reference — Common Errors

Two APIs, two error shapes. Recognize them and react correctly.

---

## Error shapes

**Router (object):**

```json
{ "error": { "message": "Model is not supported", "type": "invalid_request_error", "code": "model_not_supported" } }
```

**Hub (string):**

```json
{ "error": "Authorization header is invalid, use 'Bearer hf_...'" }
```

The MCP server preserves the status and message (token redacted).

---

## Status codes and reactions

| Status / code | Meaning | Retry? | Reaction |
|---------------|---------|--------|----------|
| `401` | Invalid/missing token | No | Fix `HF_TOKEN`; stop. |
| `402` | Out of credits | No | Add credits or use a cheaper/free model. |
| `403` / `model_not_supported` | No provider enabled for the model | No | `hf_list_inference_models` → pick a listed model. |
| `404` | Not found | No | Verify id/path with `hf_model_info` / `hf_search_models`. |
| `429` | Rate limited | Auto | Server backs off; slow down, batch, cache. |
| `5xx` | Transient server error | Auto | Server retries up to `HF_MAX_RETRIES`; then report. |

---

## Decision rule

```text
model_not_supported -> list models, pick supported, retry
401 / 402           -> STOP, human action needed (token / credits)
404                 -> verify the id or path
429 / 5xx           -> transient; let the server retry, then slow down
```

`401` and `402` are **not** retryable. Retrying them just wastes calls.
