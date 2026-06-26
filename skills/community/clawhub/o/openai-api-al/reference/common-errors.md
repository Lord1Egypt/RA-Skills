# Reference — Common Errors

All errors use the envelope:

```json
{ "error": { "message": "...", "type": "...", "param": "...", "code": "..." } }
```

| HTTP | code | Cause | Correct reaction |
|------|------|-------|------------------|
| 401 | `invalid_api_key` | Missing/wrong/revoked key | Fix the key. **DO NOT retry.** |
| 429 | rate limit | Sending too fast | Back off exponentially; respect `Retry-After`; cap attempts. |
| 429 | `insufficient_quota` | No billing credit | Stop. Tell user to add credit. Retrying won't help. |
| 400 | `invalid_request_error` | Bad params | Fix params; don't blindly retry. |
| 400 | `context_length_exceeded` | Prompt too long | Trim/summarize input or use larger-context model. |
| 404 | `model_not_found` | Unknown/inaccessible model | Verify with `openai_models`; pick valid model. |
| 500/503 | `server_error` | Transient OpenAI issue | Retry with backoff (server auto-retries). |

## Decision rules

1. Branch on `error.code` first.
2. **Never loop-retry** `401` or `400` — they are deterministic.
3. For `429`, distinguish rate (slow down) vs. quota (stop) by reading `code`/`message`.
4. Surface `error.message` verbatim (already redacted).
5. For `context_length_exceeded`, reduce input before retrying.

## Retries

The MCP server auto-retries `429`/`5xx` up to `OPENAI_MAX_RETRIES` (default 3). It does NOT retry `401`/`400`. Set `OPENAI_MAX_RETRIES=0` to handle retries yourself.

> Verification needed: confirm error codes with <https://platform.openai.com/docs/api-reference>.
