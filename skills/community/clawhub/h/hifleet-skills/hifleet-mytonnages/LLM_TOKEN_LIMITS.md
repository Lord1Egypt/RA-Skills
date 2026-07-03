# LLM token limits (route A mail parse)

## Symptom

Parse fails with errors such as:

- `ValueError: LLM response did not contain a JSON object`
- Model output truncated / invalid JSON
- `finish_reason=length` in logs

Often caused by **input or output exceeding** the model token limit (long email body, large Excel/PDF attachments, many vessels in one table).

## What the skill does

1. **Before LLM**: **`desensitize_for_llm.py`** on mail text (privacy).  
2. **After LLM**: **`extract_contacts.py`** fills phone/IM from **original** body into SQLite.  
3. **On failure**: **`mail_parse_loop`** logs error; show user message via **`scripts/i18n_messages.py`** (`llm.json_parse_failed`, `llm.token_limit_hint`).

## What to tell the user (localized)

Use **`format_llm_parse_error_for_user()`** from **`scripts/llm_parse_errors.py`** — do not paste raw stack traces.

## Adjust limits

| Layer | Action |
|-------|--------|
| **Output** | Set env **`CHARTER_LLM_MAX_OUTPUT_TOKENS`** (default 65536 in charter_ai) |
| **Input** | Shorten attachment text; split large Excel batches (`CHARTER_EXCEL_ROWS_PER_BATCH`) |
| **Agent UI** | Increase max output tokens / context window in the LLM provider settings |
| **Retry** | Failed mail stays in queue; **`mail_parse_loop --once`** retries every 10 minutes |

## Agent rule

If parse fails, inform the user with the **localized** token hint above; suggest checking agent model limits — **do not** blame “bad email” without mentioning token limits.
