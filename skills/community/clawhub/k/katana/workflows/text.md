# Text / LLM Chat Workflow

**Load this file when the user requests text generation, LLM chat, or E2EE private model usage.**

---

## Model Selection

Check `{baseDir}/models.md` for full catalogue with pricing and capabilities.

### Text Model Aliases

See `{baseDir}/SKILL.md` quick reference or `{baseDir}/models.md` for the full alias table.

If the user specifies an exact model ID (e.g. `grok-4-20-multi-agent`), pass it through directly.

### Cost Reference

See `{baseDir}/models.md` for detailed pricing per model.

### Cache Write Costs

See `{baseDir}/models.md` for the full cache cost column.

---

## Endpoint & Authentication

- **Endpoint:** `POST /v1/chat/completions` (OpenAI-compatible)
- **Auth:** `Authorization: Bearer <api_key>:<api_secret>` (different from image/video which use separate X-API-Key/X-API-Secret headers)

---

## Workflow

### Submission

Build the JSON payload in a temp file:

> **Default max_tokens:** If not supplied, the API defaults to 16,000 output tokens. Always set `max_tokens` explicitly to control cost.

```python
import json, tempfile
payload = {"model": "grok-4-3", "messages": [{"role": "user", "content": "Hello"}], "max_tokens": 16000}
with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
    json.dump(payload, f)
    tmpfile = f.name
print(tmpfile)
```

Submit using the secure header pattern:
```bash
. "${KATANA_SECRETS_FILE:-$HOME/.openclaw/secrets/katana.env}" && _H=$(mktemp) && chmod 600 "$_H" && printf 'Content-Type: application/json\nAuthorization: Bearer %s:%s\n' "$KATANA_API_KEY" "$KATANA_API_SECRET" > "$_H" && curl -s -X POST 'https://kat.imgnai.com/v1/chat/completions' -H @"$_H" -d @"$tmpfile" && rm -f "$_H" && rm -f "$tmpfile"
```

---

## Text Parameters

- `model`: Model ID (see aliases above or use exact ID)
- `messages`: Array of `{"role": "user"|"assistant"|"system", "content": "..."}` objects
- `max_tokens`: Default `16000`. Check `models.md` for per-model max output limits. `max_completion_tokens` is accepted as an alias.
- `temperature`, `top_p`: Standard OpenAI-compatible parameters
- `top_k`: Integer (e.g. 40) — top-K sampling
- `min_p`: Float (e.g. 0.05) — minimum probability threshold
- `repeat_penalty`: Float (e.g. 1.1) — repetition penalty
- `presence_penalty`: Float (e.g. 0.0) — presence penalty
- `files`: Array of `{"url": "https://..."}` objects for document/file input (models with "file" input type only)
- **Single `prompt` string:** For clients that send a single string `prompt` (instead of `messages` array), the API converts it into one user message when `messages` is omitted. This skill always uses the `messages` array format.

---

## Response Handling

OpenAI-compatible format:
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "..."
      }
    }
  ],
  "usage": { ... }
}
```

Extract `choices[0].message.content` from response and return it.

### reasoning_content

When the model produces reasoning/thinking output:
- **Non-streaming chat:** `choices[].message.reasoning_content`
- **Polled text completions:** `responses[].output_assets[].reasoning_content`

This field may be absent for models that do not produce reasoning traces.

### Text Response Billing Fields

The response includes `usage.imgnai` with:
- `credits_reserved`: credits held before inference
- `credits_charged`: actual final cost
- `credits_refunded`: difference refunded if cost < reserve
- `privacy_mode`: `Anonymized` or `E2EE Private`
- `billing_source`: where the charge came from

**Billing reserve mechanics:**
- Normal minimum reserve is 10 credits
- Large `max_tokens`/`max_completion_tokens` can reserve more
- API pre-charges the reserve, then refunds unused after actual usage is known
- Every call has a minimum 0.1 credit charge, rounded up to the nearest 0.1

---

## Streaming

The API supports SSE streaming for text/LLM calls with API-key billing:

```json
{
  "model": "grok-4-3",
  "messages": [{"role": "user", "content": "Hello"}],
  "max_tokens": 16000,
  "stream": true,
  "stream_options": {"include_usage": true}
}
```

**Response format:** Server-Sent Events (SSE) — chunks arrive as `data: {json}` lines, model name is rewritten to public name, usage included in final chunk, then `data: [DONE]`.

**Restrictions:**
- Streaming is only available with API-key billing
- x402 text calls must be non-streaming (omit `stream` or send `stream: false`)

**This skill defaults to non-streaming.** Set `stream: true` only when explicitly requested.

**⚠️ Streaming cost caveat:** If a streaming provider does not return usage in the stream, imgnAI keeps the full reserve instead of refunding based on an unknown cost. Always set `max_tokens` or `max_completion_tokens` to keep the reserve predictable. This applies to API-key billing only.

---

## Multimodal / Vision

Vision-capable text models accept image inputs using the OpenAI-compatible content array format. Supported by models with "image" in their input types (check `models.md`).

**Format:** Send `image_url` objects in the message content array:

```json
{
  "model": "grok-4-3",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Describe this image."},
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,<BASE64_ENCODED_IMAGE_BYTES>"
          }
        }
      ]
    }
  ],
  "max_tokens": 16000
}
```

**Accepted image formats:** HTTPS URLs, full `data:image/...;base64,...` data URLs, or raw base64 strings in `image_url.url`. Do NOT send local file paths or `file://` URLs.

**Image processing:** Base64 inputs are converted to JPEG, capped at 4096px max side, original aspect ratio preserved.

**Pricing:** Image tokens are counted in input token pricing. No separate vision surcharge.

### Audio Input

Some text models support audio input (check `models.md` for models listing "audio" in input types):
- `gemini-3-1-flash-lite-preview` — text, image, video, file, audio
- `gemini-3-1-pro-preview` — text, image, video, file, audio
- `gemini-3-flash-preview` — text, image, file, audio, video

**Format:** Same OpenAI content array pattern with audio content type:

```json
{
  "role": "user",
  "content": [
    {"type": "text", "text": "Transcribe this audio."},
    {"type": "input_audio", "input_audio": {"data": "<base64_encoded_audio>", "format": "mp3"}}
  ]
}
```

---

## x402 Streaming Restriction

**x402 text calls must be non-streaming** (omit `stream` or send `stream: false`). Streaming is only available with API-key billing.

---

## Text Polling (Long-Running Models)

Some text models publish `recommended_polling` (check `GET /v1/models`). For these models, use async polling instead of synchronous completions:

1. **Submit:** `POST /v1/chat/completions?wait=false` with the normal payload
2. **Poll:** `GET /v1/generation-requests/{request_id}` (same endpoint as image/video polling)
3. **Extract response:** Completed assistant text is in `responses[].output_assets[].content`
4. **Token usage:** `responses[].output_assets[].metadata.usage`
5. **Reasoning content:** `responses[].output_assets[].reasoning_content`
6. **Timeout:** Use the model's `request_timeout_seconds` from `GET /v1/models` as the deadline. For `q-naifu-a3b`, allow at least 600 seconds.

**Polling pattern:** Follow the same polling pattern as image/video (extract `poll_after_seconds`, use as interval). Apply the 10-minute guard for text polling (600s API timeout).

---

## Assistant Prefill

Some models (e.g. `q-naifu-a3b`) support assistant response prefill — making the completion begin with specific text. To use:

1. Add the desired prefix as the **final assistant message** in the messages array
2. The prefill content **must not end with trailing whitespace**

Example:
```json
{
  "model": "q-naifu-a3b",
  "messages": [
    {"role": "user", "content": "Write a haiku about APIs."},
    {"role": "assistant", "content": "Here is your haiku:"}
  ],
  "max_tokens": 16000
}
```

---

## File Input

Models with "file" in their input types accept file attachments via the `files` array parameter:

```json
{
  "files": [{ "url": "https://example.com/document.pdf" }]
}
```

### `q-naifu-a3b` Supported File Formats

- **Image formats:** JPEG/JPG, PNG, WebP, GIF, AVIF, TIFF/TIF, BMP, HEIC/HEIF
- **Document formats:** .pdf, .docx
- **Code/text formats:** .txt, .md, .json, .yaml, .yml, .csv, .tsv, .xml, .html, .css, .js, .ts, .tsx, .jsx, .py, .rs, .go, .java, .kt, .c, .cpp, .h, .cs, .sh, .ps1, .toml, .ini, .cfg, .log, .sql
- **Blocked:** video, audio, archives, executables, old Office formats
- **Max size:** 40 MB per file
- Unknown extensions allowed when content is detected as image or text

---

## Delivery

**Model features:** Text models support varying capabilities including Tool calling, Structured output, Long context, Vision, Video input, Audio input, and File input. Check `models.md` for per-model feature flags.

**Return the model's response VERBATIM.** Do not summarise, rephrase, paraphrase, or editorialise the LLM's output. Present it exactly as returned, unless the user explicitly asks you to summarise or reformat.

Follow the delivery pattern defined in `{baseDir}/SKILL.md`.

---

## Private & E2EE Private Models

Three privacy tiers exist for text models:

1. **Anonymized:** Customer account identity is not sent with the inference request. The model operator may process prompt content.
2. **Private:** The request is handled through a **private in-house model path**. No E2EE/hardware attestation — imgnAI can see the content but it stays in-house.
3. **E2EE Private:** The request is handled through a **hardware-protected confidential-compute model path**. The user's prompts and model responses are encrypted end-to-end — imgnAI cannot read them.

**Available private models** (check `models.md` for current list):
- `q-naifu-a3b` (Private — in-house, no attestation)
- `kimi-k2-6-private`, `qwen3-coder-next-private`, `glm-5-1-private` (E2EE Private)
- `mimo-v2-flash-private`, `qwen3-5-27b-private`, `qwen3-5-397b-a17b-private` (E2EE Private)
- `minimax-m2-5-private`, `glm-5-private`, `kimi-k2-5-private` (E2EE Private)
- `deepseek-v3-2-private`, `qwen3-coder-480b-a35b-private` (E2EE Private)
- `qwen3-vl-30b-a3b-instruct-private`, `gemma-3-27b-private` (E2EE Private)

Usage is identical to regular models — just use the model ID. Privacy is handled transparently by the API.

### Privacy Attestation (E2EE Private only)

**Attestation only applies to E2EE Private models, not Private models.** Verify E2EE claims for E2EE Private models:

```
GET /v1/text/attestation?model=<private_model>&nonce=<64_hex_nonce>
```

Returns a privacy proof for the E2EE model. Uses Intel TDX and NVIDIA Confidential Computing where applicable. The `nonce` must be a 64-character hex string.

---

## Error Handling

Follow the error handling protocol defined in `{baseDir}/SKILL.md`.

---

*Part of the Katana skill. See SKILL.md for routing, general configuration, and llms.txt freshness checks.*
