# Tests — Failure Cases

Known bad behaviors, why they're wrong, and the corrected version. Use these as negative tests.

## 1. Exposing the API key

**Bad**

> Agent prints `OPENAI_API_KEY=sk-...` or includes the `Authorization` header in output/logs.

**Why wrong:** leaks a secret that maps directly to spend; enables account abuse.

**Corrected**

> Never reference the key. It lives only in the environment; the MCP server redacts `Bearer`/`sk-` strings. Report results without secrets.

## 2. No `max_tokens` → runaway cost

**Bad**

```json
{ "tool": "openai_chat", "arguments": { "model": "gpt-4o", "messages": [{ "role": "user", "content": "Write about cats." }] } }
```

**Why wrong:** unbounded output; can generate thousands of billed tokens.

**Corrected**

```json
{ "tool": "openai_chat", "arguments": { "model": "gpt-4o-mini", "messages": [{ "role": "user", "content": "Write 3 sentences about cats." }], "max_tokens": 80 } }
```

## 3. Wrong / expensive model

**Bad**

> Using `gpt-5` or `o3` to classify a sentence into two categories.

**Why wrong:** pays frontier prices for a trivial task with no quality gain.

**Corrected**

> Use `gpt-4.1-nano` or `gpt-4o-mini` with a tiny `max_tokens`.

## 4. No moderation of untrusted input

**Bad**

> Forwarding arbitrary user/document text straight to a paid model without screening.

**Why wrong:** sends disallowed content, wastes paid calls, risks policy violations and prompt injection.

**Corrected**

> Call the free `openai_moderations` first; if `flagged`, refuse or sanitize before any paid call.

## 5. Retrying a 401

**Bad**

> Loop: call → `401 invalid_api_key` → retry → `401` → retry...

**Why wrong:** a 401 is deterministic; retrying never succeeds and wastes time.

**Corrected**

> Stop on `401`. Report that the key is missing/invalid and needs fixing. Do not retry.

## 6. Per-item embedding loop

**Bad**

> Calling `openai_embeddings` once per chunk for 1,000 chunks.

**Why wrong:** 1,000 billed calls with huge overhead; ignores batching.

**Corrected**

> Send chunks as a batched array `input` (chunked into reasonable batch sizes), cache vectors, re-embed only changes.

## 7. Ignoring usage / context limits

**Bad**

> Stuffing a 200k-token document into one chat call and ignoring `usage`.

**Why wrong:** triggers `context_length_exceeded` and/or large bills; no cost visibility.

**Corrected**

> Chunk/summarize input, set `max_tokens`, and report `usage.total_tokens` after each call.

> Verification needed: confirm behaviors with <https://platform.openai.com/docs/api-reference>.
