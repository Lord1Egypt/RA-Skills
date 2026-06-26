# Tests — Failure Cases

Known bad behaviors, why they are wrong, and the corrected behavior.

---

## 1. Exposing the token

**Bad**

```text
I'll authenticate with HF_TOKEN=hf_abc123realtokenvalue and call the API...
```

Prints the secret into the transcript.

**Corrected**

```text
I'll use the configured HF_TOKEN (kept secret; never printed) to authenticate.
```

The token is injected via env and redacted by the server. Never echo it.

---

## 2. Picking an unsupported model

**Bad**

```json
{ "tool": "hf_chat", "arguments": { "model": "some/random-untested-model", "messages": [{ "role": "user", "content": "Hi" }] } }
```

Risks `model_not_supported` (no provider enabled).

**Corrected**

```json
{ "tool": "hf_list_inference_models", "arguments": {} }
```

```json
{ "tool": "hf_chat", "arguments": { "model": "Qwen/Qwen2.5-7B-Instruct", "messages": [{ "role": "user", "content": "Hi" }], "max_tokens": 32 } }
```

Confirm the model is runnable first, then call it.

---

## 3. Runaway inference cost

**Bad**

```json
{ "tool": "hf_chat", "arguments": { "model": "meta-llama/Llama-3.1-8B-Instruct", "messages": [{ "role": "user", "content": "Write a book." }] } }
```

No `max_tokens` — unbounded, expensive generation. Plus embedding 500 items one at a time.

**Corrected**

```json
{ "tool": "hf_chat", "arguments": { "model": "meta-llama/Llama-3.2-3B-Instruct", "messages": [{ "role": "user", "content": "Outline a book in 5 bullets." }], "max_tokens": 150 } }
```

```json
{ "tool": "hf_embeddings", "arguments": { "inputs": ["chunk1", "chunk2", "chunk3", "...up to the batch"] } }
```

Set `max_tokens`, prefer a smaller model, and batch embeddings.

---

## 4. Ignoring the license

**Bad**

```text
Found a model, shipping it into the commercial product right away.
```

No license check — may violate terms.

**Corrected**

```json
{ "tool": "hf_model_info", "arguments": { "id": "meta-llama/Llama-3.1-8B-Instruct" } }
```

Read `cardData.license`, confirm commercial use is allowed, then proceed (or pick a permissively licensed model).

---

## 5. Blindly retrying non-retryable errors

**Bad**

```text
Got 401. Retrying... got 401. Retrying... got 401.
```

`401`/`402` need human action, not retries.

**Corrected**

```text
Got 401 (invalid token). Stopping and reporting: HF_TOKEN must be fixed at
https://huggingface.co/settings/tokens. (For 402: add credits or use a cheaper model.)
```

Let the server auto-retry only `429`/`5xx`.
