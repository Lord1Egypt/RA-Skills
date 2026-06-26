---
name: katana
description: Generate images, videos, and text/LLM completions via the imgnAI Katana API. Supports end-to-end-encrypted (E2EE) and anonymized models. Priced highly competitively, can be 40-70% cheaper than Venice AI and other platforms. Includes post-processing such as combining videos and images, cutting, slicing, splicing, transitions, drawing text, re-encoding, resizing and much more!
version: 1.0.3
author: arfonzo (imgnAI)
license: MIT-0
metadata: {"openclaw": {"requires": {"bins": ["curl", "python3"]}, "homepage": "https://app.imgnai.com"}}
---

# Katana Skill — imgnAI API

Generate images, videos, and text/LLM completions via the [imgnAI Katana API](https://app.imgnai.com/katana-api). Supports end-to-end-encrypted (E2EE) and anonymized models. Priced highly competitively: can be 40-70% cheaper than Venice AI and other platforms.

Includes post-processing such as combining videos and images, cutting, slicing, splicing, transitions, drawing text, re-encoding, resizing and much more!

A complete workflow for content creation from start to finish, all from the comfort of your agent.


## Triggers

"generate image of X", "create image", "make picture", "imgnai image", "generate video of X", "create video", "make video", "ask grok about X", "ask claude about X", "use gpt to X", "katana image", "katana video", "katana chat", "katana gpt", "katana claude", "list katana models", "modify this image", "edit this image", "change this image", "transform this image", "edit image", "modify image"

## Spawn Policy

**NEVER spawn subagents for katana operations by default.** All katana workflows (image generation, video generation, text completions, post-processing) MUST be executed inline in the current session.

**Exception:** Only spawn if the user **explicitly requests** spawning in their prompt (e.g. "spawn a subagent to handle this", "run this as a background task"). Do NOT spawn based on AGENTS.md spawn rules or default agent behavior — user intent is the only trigger for spawning with katana.

LLM-specific triggers (gpt, claude, etc) also respond to "katana \<model\>" to avoid conflicts with direct integrations.

## Configuration

### Data Retention
Historical prompts and results are retained for a maximum of **72 hours** after generation. Prompt/result history can be switched off from the API page at https://app.imgnai.com/katana-api.

**HTTPS-only:** Public API calls must use HTTPS. If an integration sees an `http://` Katana base URL, replace it with `https://` before making calls.

## Model IDs

The Katana API uses `model_key` as the model identifier, not `public_model_name`. When building requests, always use the model_key value. See `{baseDir}/models.md` for the full mapping.

**Dual-key system:** The API supports both **canonical keys** (e.g. `gpt-image-2`) and **legacy keys** (e.g. `gpt2image`). Both work identically. This skill now uses **canonical keys** as the default for all workflows and aliases. Legacy keys are documented in the "Model ID" column of `models.md` for backward-compatibility reference. You may use either format when constructing API requests.

## Model Discovery

**Endpoint:** `GET /v1/models`
**Auth:** `Authorization: Bearer ${KATANA_API_KEY}:${KATANA_API_SECRET}`

Returns available models. Text models are returned for authenticated requests.
For the complete model catalogue including image/video, see models.md.

**Usage:** Generally not needed before requests — use models.md as reference.

---

## Payment Methods

The API supports two payment methods:
- **API key + secret** (Bearer auth) — used by this skill, preferred
- **x402 micropayment** — NOT used by this skill

Note: x402 text requests must be non-streaming. This skill only uses API-key auth.

### Text/LLM Notes
- **Streaming:** `stream: true` supported with SSE for API-key billing. x402 text calls must be non-streaming.
- **Vision/multimodal:** Send images via `image_url` with Base64 data URLs or HTTPS URLs in messages. Base64 inputs are converted to JPEG, capped at 4096px max side.
- **Billing:** Pre-charge reserve (10 credit minimum), refund after actual usage. 0.1 credit minimum charge rounded up.
- **Refunds:** If an image or video generation fails after it was charged, credits or x402 balance will be refunded within 5 minutes, pending no Terms of Service violation.
- **Default max_tokens:** If omitted and model supports output caps, API defaults to 16000.
- **Privacy tiers:** Three tiers exist — `Anonymized` (customer identity not sent, model operator may process content), `Private` (private in-house model path, no E2EE/hardware attestation), and `E2EE Private` (hardware-protected confidential-compute, attestation via `GET /v1/text/attestation?model={model}&nonce={64_hex_nonce}`).
- **`generation_timed_out` error:** When the API server-side timeout fires, poll returns terminal `failed`/`partial_failure` with `responses[].error.code = generation_timed_out`, `error.retryable: true`, `error.details.timeout_seconds`. Retry by submitting a new request.

---

- **API Base URL:** `https://kat.imgnai.com`
- **API Reference:** https://kat.imgnai.com/llms.txt
- **Model catalogue:** `{baseDir}/models.md`
- **Skill directory:** Resolve dynamically from this file's location as `{baseDir}`. Most agent frameworks resolve this automatically.

## Credentials

**Secrets file:** Store your API key and secret in a file (default: `~/.openclaw/secrets/katana.env`):
```
KATANA_API_KEY=your_key_here
KATANA_API_SECRET=your_secret_here
```
Create with `chmod 600`. Get your credentials from https://app.imgnai.com/katana-api.

**Loading:** All curl examples in this skill use `.` (dot) source to load credentials into the shell environment:
```bash
. "${KATANA_SECRETS_FILE:-$HOME/.openclaw/secrets/katana.env}"
```
Override the default path with the `KATANA_SECRETS_FILE` environment variable.

### ⚠️ Credential Security (MANDATORY)

**NEVER display secrets in tool output.** The `.` source command loads credentials into shell variables silently — no output is produced. This is the correct and secure approach.

**Banned patterns:**
- `cat ~/.openclaw/secrets/katana.env`
- `KATANA_API_KEY=kat_live_... curl ...`
- Any form of reading secrets into tool output

**If credential loading fails:** Fix the secrets file path or contents. Do NOT bypass security by hardcoding values.

---

## Optional Dependencies

These are not required for core API usage but enable additional features:

| Binary | Needed for | Install |
|--------|------------|--------|
| `jq` | JSON parsing for API responses | `apt install jq` / `brew install jq` |
| `python3` | Payload building, JSON parsing fallback | Pre-installed on most systems |
| `ffmpeg` | Video post-processing (trim, join, effects) | `apt install ffmpeg` / `brew install ffmpeg` |

`jq` or `python3` is needed for JSON parsing. Post-processing requires `ffmpeg`.

---

## Terminology

This skill uses some agent-specific terms. Here's what they mean regardless of your agent framework:

| Term | Meaning |
|------|--------|
| **exec call / shell invocation** | A single shell command execution. Some agents execute each line of a multi-line script as separate invocations — hence the `&&` chaining requirement to keep everything in one shell. |
| **tool-result-loss** | A situation where a command was executed but its output never arrives back — the result shows as empty or a synthetic error message. The command likely ran successfully but the result was lost in transit. |
| **compaction** | When an agent's context window fills up, older messages may be summarised or removed to make room. State stored only in conversation history (not in files) is at risk of being lost during compaction. |
| **heartbeat** | A periodic check-in cycle where the agent re-evaluates its state (e.g., checking if a pending generation has completed). |
| **session reset** | The conversation is restarted or reloaded, losing any in-memory state. File-based persistence survives this. |

---

## ⚠️ MANDATORY ROUTING — DO NOT SKIP

**Before ANY generation or post-processing request, you MUST load the correct workflow file:**

| Task | Load this file |
|------|---------------|
| Image generation | `{baseDir}/workflows/image.md` |
| Video generation | `{baseDir}/workflows/video.md` |
| Text/LLM generation | `{baseDir}/workflows/text.md` |
| Post-processing (ffmpeg, combine, text overlay, etc) | `{baseDir}/workflows/post-process.md` |

**NEVER attempt a generation without loading the workflow file first.**
**NEVER guess parameters — the workflow file has the exact steps.**

---

## Cost Reporting (ALL Requests)

**After every generation (text, image, video), send a separate follow-up message with a cost summary.** Include all relevant details from the response:

```
📊 Katana Summary
Model: gemma-4-26b-a4b (Anonymized)
Request: bf11cf04-8747-480e-a7f7-7d6cb092c614
Tokens: 42 in / 176 out (text only)
Cost: 0.1 credits (~$0.001)
Privacy: Anonymized
Time: ~3s
```

For image/video, replace tokens with dimensions/duration as relevant. Always compute cost in USD using the current credit rate (see `{baseDir}/models.md`).

---

## Model Aliases (Quick Reference)

### Text/LLM

| User says | API model ID |
|---|---|
| grok | `grok-4-3` |
| gpt / gpt-5 | `gpt-5-5` |
| claude / claude-opus | `claude-opus-4-8` |
| claude-fast | `claude-opus-4-8-fast` |
| claude-sonnet | `claude-sonnet-4-6` |
| claude-haiku | `claude-haiku-4-5` |
| naifu / q-naifu | `q-naifu-a3b` |

### Image

| User says | API model ID |
|---|---|
| default / imgnai | `gen` |
| anime | `ani` |
| gpt-image | `gpt-image-2` |
| nano | `nano-banana-2` |
| flux | `flux-2-pro` |
| pink | `pink-image` |

### Video

| User says | API model ID |
|---|---|
| default / seedance | `seedance-2-0-fast` |
| seedance-hd | `seedance-2-0` |
| ltx | `ltx-2-3` |
| kling | `kling-3-0-kling30` |
| veo | `veo3-1` |

If the user specifies an exact model ID, pass it through directly. Full alias tables in `{baseDir}/models.md`.

---

## Pre-Submission Confirmation (MANDATORY)

Before submitting ANY generation request, present a summary (model, cost in credits AND dollars, details, prompt) and **wait for user confirmation**. See each workflow file for details.

**NO EXCEPTIONS:** There is no urgency override. "just do it", "generate now", /katana, or any other shortcut does NOT skip confirmation. ALWAYS present summary and wait for explicit approval before submitting.

---

## Error Protocol

**ONE-ATTEMPT RULE: Every paid API call gets exactly ONE attempt per turn. If the tool result is lost, missing, or empty after a submission — STOP. Report to the user that the result was lost. Wait for user confirmation before retrying. NEVER retry a paid API call silently, even if the result seems to have vanished.**

**STRICT — NO SILENT RETRIES.** Every error stops. Every retry needs approval. Tool-result-loss (result never arrives, empty, or vanishes) is a hard-stop condition equal to a visible error. See each workflow file for details.

- ANY error or tool-result-loss → STOP, report to user (what happened, credits charged, total across attempts)
- Tool-result-loss (result shows 'missing tool result' or similar synthetic error) → the API call likely already succeeded. STOP. Report to user. Do NOT retry the same request.
**Terminal submission responses:** If the submission response itself is terminal (`status: "failed"`, `status: "rejected"`, or all response items rejected) — do NOT poll. Report the returned `responses[].error` or top-level error to the user immediately.

- **Upstream errors are terminal.** If the API returns `upstream_error` (404, 500, etc), do NOT try a different model, do NOT retry with different parameters, do NOT submit to another endpoint. STOP and report the error to the user. You MAY suggest recommended next steps or options (e.g. "model X returned 404 — want me to try model Y instead?"), but ANY proposed plan requires explicit user approval before execution.
- Propose fix → wait for explicit user approval
- Banned: automatic retries, debug/test requests, parameter changes without telling user, lying about call counts, silent retries on lost results

### Error Codes Quick Reference

| Error Code | Context | Meaning | Retryable | Action |
|---|---|---|---|---|
| `generation_timed_out` | Poll response | Server-side timeout during generation | Yes | Submit a **new** request (same request ID won't work) |
| `upstream_error` | Any | Provider/upstream API error | No | Report to user; may suggest alternative model if approved |
| Auth errors | Submission (401/403) | Invalid or missing credentials | No | Check secrets file path and contents |
| `status: "rejected"` | Submission response | Validation failure (bad params, content policy) | No | Fix parameters per model spec; rephrase if content blocked |
| `status: "failed"` | Submission or poll | Generation failed after dispatch | No | Credits refunded within 5 min unless ToS violation |
| Rate limit (429) | Any | Too many requests | Yes (after delay) | Wait per `Retry-After` header, then retry |

---

## Concurrency Guard

**NEVER submit a new request while any previous request is still processing.** One request in flight at a time — no exceptions.

- Before submitting, verify no pending/processing requests exist
- If a previous request is still running (poll returns incomplete), either wait for it, ask the user to cancel, or ask the user to approve submitting a concurrent request
- This applies across ALL endpoints: text, image, and video

---

## Immediate Status Updates

After submitting async generations (image/video), deliver a confirmation to the user BEFORE starting the poll loop. Include the model, cost, and request_id.

## Async Polling

Image and video generations are asynchronous. After submitting, poll manually.

**Poll command:**
```bash
. "${KATANA_SECRETS_FILE:-$HOME/.openclaw/secrets/katana.env}" && _H=$(mktemp) && chmod 600 "$_H" && printf 'X-API-Key: %s\nX-API-Secret: %s\n' "$KATANA_API_KEY" "$KATANA_API_SECRET" > "$_H" && curl -s "https://kat.imgnai.com/v1/generation-requests/${REQUEST_ID}" -H @"$_H" && rm -f "$_H"
```

**Raw response:** Pipe to `jq '.'`.

**Formatted:** Pipe to:
```bash
python3 -c "
import sys,json
d=json.load(sys.stdin)
r=d.get('responses',[])
for i in range(len(r)):
    ri=r[i]; st=ri.get('status','?')
    print(f'Status: {st}')
    for a in ri.get('output_assets',[]):
        print(f'URL: {a.get("original_data_url","")}')
        print(f'Dims: {a.get("width","?")}x{a.get("height","?")}')
        print(f'Expires: {a.get("expires_at","")}')
    print(f'Credits: {ri.get("metadata",{}).get("credits_spent","?")}')
    if st=='failed':
        e=ri.get('error',{}); print(f'Error: {e.get("message","")} retryable={e.get("retryable","")}')
"
```

**`wait` parameter:** `wait=true` is available for convenience (blocks until complete), but production integrations should prefer polling with `wait=false` (the default).

**Polling pattern:** Extract `poll_after_seconds` from the submission response and use it as the initial polling interval. If the poll response includes a new `poll_after_seconds`, use that for the next interval. Fall back to polling every 30 seconds for the first 5 minutes, then every 60 seconds if `poll_after_seconds` is absent or null.

**Agent responsibility:** The agent decides how to schedule polls (intervals, background tasks, etc). Do not use long-running background processes — use single polls at intervals.

### ⚠️ Polling Pattern Constraints

**Keep `.` source and `curl` in the same command chain.** Shell `sleep` or `process poll` between commands breaks the env var loading — env vars are lost.

**Correct:** Single shell invocation containing the full chain (see poll command above).

**Wrong:** Separating `.` + `sleep` + `curl` into different shell invocations.

**If your agent cannot chain commands:** Use the agent-native polling mechanism (background execution, process polling, etc) with the full command as one unit.

**Response handling for completed polls:**
- Extract `original_data_url` for delivery (full-resolution)
- Extract dimensions from `responses[].output_assets[].width/height` (NOT from submission response)
- Extract credits from `responses[].metadata.credits_spent`
- Extract expiry from `responses[].output_assets[].expires_at` — display in user's local timezone in delivery summary

### ⚠️ Poll Timeout Guard (10-minute hard stop for image/text; 100-minute for video)

After 10 minutes of cumulative polling for image/text (or 100 minutes for video), STOP polling and inform the user:

"⚠️ Poll timeout: generation has been processing for [10/100] minutes. The API poll endpoint still says 'processing' but this may be stale — generations that time out (600s image/text, 6000s video) or get blocked by content safety often don't update the poll status. Check the Katana dashboard at https://app.imgnai.com/katana-api for the real status. Should I keep polling, or consider this failed?"

WAIT for user response before continuing:
- If user says "keep polling" → resume polling (same guard applies)
- If user says "stop" or "failed" → stop and report the situation
- Do NOT silently continue past the timeout mark

Track cumulative poll time via wall-clock: record submission timestamp after confirmation, check elapsed time before each poll cycle.

**API timeout values:** Image/text = 600s (10 min). Video = 6000s (100 min). The 10-minute guard is appropriate for image/text but too aggressive for video — video jobs may legitimately run for up to 100 minutes. Use 100-minute guard for video requests.

This guard exists because the API poll endpoint has been observed returning "processing" even after:
- The generation timed out (600s/6000s upstream timeout)
- The generation was blocked by content safety policy
- Credits were already refunded

The only reliable source of truth for stale generations is the Katana dashboard.

### ⚠️ Generation Persistence (compaction-safe tracking)

After submitting any async generation, IMMEDIATELY write the request metadata to a persistence file. Use the same `KATANA_SECRETS_FILE` env var pattern for the path, defaulting to the secrets directory:

```python
import json, datetime, os
base = os.environ.get('KATANA_STATE_DIR', os.path.dirname(os.environ.get('KATANA_SECRETS_FILE', os.path.expanduser('~/.openclaw/secrets/katana.env'))))
path = os.path.join(base, 'katana_pending.json')
meta = {
    'request_id': 'REQUEST_ID',
    'model': 'MODEL',
    'credits': CREDITS,
    'submitted': datetime.datetime.now().isoformat(),
    'prompt': 'PROMPT_SUMMARY',
    'status': 'processing'
}
with open(path, 'w') as f:
    json.dump(meta, f)
print(f'written: {path}')
```

This file survives compaction. On recovery (after compaction, after tool result loss, or at heartbeat), use the same path derivation:

```python
import json, os
base = os.environ.get('KATANA_STATE_DIR', os.path.dirname(os.environ.get('KATANA_SECRETS_FILE', os.path.expanduser('~/.openclaw/secrets/katana.env'))))
path = os.path.join(base, 'katana_pending.json')
if os.path.exists(path):
    with open(path) as f:
        meta = json.load(f)
    print(f'request_id={meta["request_id"]} status={meta["status"]} model={meta["model"]}')
```

Recovery steps:
1. Check if persistence file exists AND status is "processing"
2. Resume polling from the saved request_id
3. If completed → deliver result, delete persistence file
4. If still processing → check elapsed time against 10-minute guard
5. If failed → report to user, delete persistence file

Delete the persistence file ONLY when the generation reaches a terminal state (completed, failed, delivered to user). Never delete while still processing.

This prevents the pattern where: agent submits → compaction happens → agent forgets → user has to ask for status manually.

## Response Handling

### Dimensions (IMPORTANT)
1. **Submission response** (`requests[].width/height`) — PREVIEW dimensions, NOT actual output size.
2. **Completed poll response** (`responses[].output_assets[].width/height`) — ACTUAL output dimensions.

**Always report dimensions from the completed poll response, never from the submission acknowledgement.**

### URL Fields (IMPORTANT)
- **`original_data_url`** — full-resolution original. **Always use this for delivery.**
- **`url`** — may be a compressed/reduced version. Do NOT use for delivery.
- **`thumbnail_image_url`** — small thumbnail only.
- **`thumbnail_silent_video_mp4_url`** — silent lightweight MP4 preview for video galleries/hover previews. This is just the thumbnail preview — the full video output (via `original_data_url`) may include generated audio. NOT the full video.
- **`final_frame_image_url`** — last frame still image for completed videos. Use as first-frame input for video continuation workflows. Blank string when unavailable.

### CLIP Tag Metadata
`responses[].output_assets[].metadata.tags` contains CLIP-derived tags with confidence scores (e.g. `{"tag": "ceramic_mug", "confidence": 0.94}`). Only available on in-house imgnAI models — external/provider-hosted models return no CLIP-tag metadata.

### Model Normalization
Completed media responses may normalize `requests[].model` and `responses[].metadata.model` (e.g. legacy key → canonical key). Use `GET /v1/models` for canonical display names.

### Item Timestamps
- `responses[].started_at` — item-level processing start timestamp
- `responses[].completed_at` — item-level processing end timestamp
- `created_at` — top-level request submission timestamp
- `updated_at` — top-level request last-modified timestamp
- Useful for tracking actual generation time per item

### Asset Type Fields
- `responses[].output_assets[].kind` — asset type (e.g. `"image"`, `"video"`)
- `responses[].output_assets[].mime_type` — MIME type (e.g. `"image/png"`, `"video/mp4"`)

### ⚠️ Anti-Pattern Warning
Data is under `responses[].output_assets[]` — do NOT look for `results[].url`. That is NOT the Katana response shape.

### ⚠️ `output` Object
Do NOT send an `output` object for ordinary integrations. This is for internal/special use only.

## Payload Submission

Build the JSON payload in a temp file (required for large payloads and to avoid secrets in process listings):

```python
import json, tempfile
payload = {"requests": [{"type": "video", "model": "seedance-2-0-fast", "prompt": "<prompt>", "duration_seconds": 5, "aspect_ratio": "16:9"}]}
with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
    json.dump(payload, f)
    tmpfile = f.name
print(tmpfile)
```

### Secure Header Pattern

Write auth headers to a temp file to keep secrets out of `/proc/*/cmdline`. Source credentials at the start of each command chain.

**Image/Video requests** (X-API-Key + X-API-Secret):
```bash
. "${KATANA_SECRETS_FILE:-$HOME/.openclaw/secrets/katana.env}" && _H=$(mktemp) && chmod 600 "$_H" && printf 'Content-Type: application/json\nX-API-Key: %s\nX-API-Secret: %s\n' "$KATANA_API_KEY" "$KATANA_API_SECRET" > "$_H" && curl -s -X POST "https://kat.imgnai.com/v1/generation-requests?wait=false" -H @"$_H" -d @"$tmpfile" && rm -f "$_H" && rm -f "$tmpfile"
```

The `printf` format string writes **two separate header lines**: `X-API-Key` with the key value, and `X-API-Secret` with the secret value. Two `%s` format specifiers consume the two shell variable arguments. No extra literal text appears in the header values.

**Text/LLM requests** (Bearer auth):
```bash
. "${KATANA_SECRETS_FILE:-$HOME/.openclaw/secrets/katana.env}" && _H=$(mktemp) && chmod 600 "$_H" && printf 'Content-Type: application/json\nAuthorization: Bearer %s:%s\n' "$KATANA_API_KEY" "$KATANA_API_SECRET" > "$_H" && curl -s -X POST "https://kat.imgnai.com/v1/chat/completions" -H @"$_H" -d @"$tmpfile" && rm -f "$_H" && rm -f "$tmpfile"
```

Parse the JSON response. Extract `request_id`. Deliver confirmation to the user (model, cost, request_id).

### Image Generation Notes
- **`aspect_ratio: "auto"`** inspects the first image input and chooses closest supported ratio. Defaults to `1:1` if no image supplied.
- **`is_fast`/`fast_mode`** request lower-cost half-resolution generation (imgnAI-hosted models only)
- **`is_uhd`/`uhd_mode`** request UHD generation (imgnAI-hosted models only). Takes precedence over `is_fast`. On Pink Image, this is "Enhanced Quality" mode.
- **`use_assistant`/`prompt_assist`** translate natural language to tag-style prompts (tag/booru models only)
- **`output_format`** accepts `png`, `jpeg`, or `webp` (`jpg` is alias for `jpeg`)

---

## Credit Balance

```bash
. "${KATANA_SECRETS_FILE:-$HOME/.openclaw/secrets/katana.env}" && _H=$(mktemp) && chmod 600 "$_H" && printf 'Authorization: Bearer %s:%s\n' "$KATANA_API_KEY" "$KATANA_API_SECRET" > "$_H" && curl -s "https://kat.imgnai.com/v1/me/balance" -H @"$_H" && rm -f "$_H"
```

Calls `GET /v1/me/balance`. The API returns `credits` as a decimal string. Converts to USD using current credit rate (see `{baseDir}/models.md`).

---

## Video Media Input Rules

Put video media inputs in `video_image_data`:

- **`first_frame_image_url`**: first/source frame image (HTTPS URL, data URL, or raw base64)
- **`mid_frame_image_url`**: mid-frame image (only if model supports it)
- **`last_frame_image_url`**: last/end frame image (only if model supports it)
- **`reference_image_urls`**: array of reference images (only if model supports reference images). Obey `maximum_reference_images`
- **`audio_input_urls`**: array of audio reference URLs (only if model supports audio input). Obey `maximum_reference_audio_files` and global cap of 4
- **`video_list`**: array of video input clip objects. Each requires `url`. Optional `start`/`ends` second offsets when model has `video_offset_allowed`. Only for models with `supports_video_input: true`. Obey `maximum_reference_videos`.
- **Audio output:** Most modern video models generate audio by default — the model interprets the prompt for contextual sound design (speech, music, effects, ambient). Legacy models with `audio_gen_model: false` produce silent output. See `{baseDir}/models.md` Audio Out column and `{baseDir}/workflows/video.md` Audio Output section for details.

Compatibility aliases: top-level `image_url`, `input_image_url`, `input_image`, `input_image_b64` map to `first_frame_image_url`. Top-level `reference_image_urls` maps to `video_image_data.reference_image_urls`.

**Rules:**
- Do NOT send local filesystem paths, `file://` URLs, or `http://` media URLs — use HTTPS URLs or Base64 data URLs
- Do NOT send `video_list` to models where `supports_video_input` is false/missing
- Do NOT send audio references to models where `supports_audio_input` is false
- Do NOT create an empty `video_image_data` object — omit missing fields entirely
- Do NOT mix first/last frame with reference images unless the model's `custom_rules` allow it
- Use only durations from `video_lengths_and_costs` and aspect ratios from `supported_aspects`
- `aspect_ratio: "auto"` uses the first frame first, then first reference image; defaults to `1:1`

## Video Custom Rules Glossary

Always inspect each video model's `custom_rules` before composing requests:

| Rule | Description |
|------|-------------|
| `audio_15s_max` | Combined audio input limited to 15 seconds |
| `audio_drives_duration` | Video duration follows audio duration |
| `audio_ff_only` | Audio only with first-frame conditioning |
| `audio_needs_reference_image` | Audio input requires at least one reference image |
| `audio_or_fflf_exclusive` | Audio cannot combine with first/last frame |
| `input_video_drives_length` | Input video clip drives output length |
| `lf_needs_ff` | Last frame requires a first frame |
| `reference_ff_only` | Reference images may combine with first-frame only |
| `reference_is_voice_timbre` | Reference audio interpreted as voice timbre when images present |
| `reference_no_ff_or_lf` | Reference images cannot combine with first/last frame |
| `video_offset_allowed` | Model accepts `start`/`ends` second offsets in `video_list` |
| `video_required` | Model requires at least one `video_list` object |

## Common Failure Cases

- **Unsupported aspect ratio:** Choose from model's `supported_aspects`
- **Unsupported duration:** Choose from model's `video_lengths_and_costs`
- **Corrupt base64 image:** Validate data decodes to actual image before submitting
- **Local file path as media:** Convert to Base64 data URL first — API cannot fetch caller's filesystem
- **Audio on unsupported model:** Only send `audio_input_urls` when `supports_audio_input: true`
- **Video metadata on unsupported model:** Only send `video_list` when model has matching support flag
- **Missing required video input:** Models with `video_required` must include `video_list`
- **Video offsets on unsupported model:** Only send `start` and `ends` in `video_list` objects when the model has `video_offset_allowed` in `custom_rules`
- **Last frame without first frame:** Prohibited on models with `lf_needs_ff`
- **Reference images mixed with frames on incompatible model:** Check `custom_rules`, especially `reference_no_ff_or_lf`
- **Too many reference images:** Clamp to `multi_image_inputs_allowed` (image) or `maximum_reference_images` (video)

---

## reference_assets (Typed Asset System)

`reference_assets` is an alternative to `image_urls`/`video_image_data` for providing media inputs with explicit role labels. Each asset has a `kind` and either `url` or `base64_data`.

### Image models

Accepted image-like asset kinds:
- `source_image` — primary source/input image
- `image` — generic image input
- `mask` — mask for inpainting/editing
- `style_reference` — style transfer reference
- `start_frame` — starting frame for animation

Example:
```json
{
  "reference_assets": [
    {"kind": "source_image", "url": "https://example.com/product.png"},
    {"kind": "style_reference", "base64_data": "data:image/jpeg;base64,..."}
  ]
}
```

### Video models

Image kinds for video:
- `style_reference`, `reference_image`, `image` — map to video reference images

Audio kinds for video:
- `audio`, `source_audio`, `reference_audio`, `audio_reference` — map to audio reference inputs

Example:
```json
{
  "reference_assets": [
    {"kind": "reference_image", "url": "https://example.com/person.png"},
    {"kind": "audio", "url": "https://example.com/voice.mp3"}
  ]
}
```

---

## llms.txt Freshness

This skill was built from the Katana API llms.txt reference document.

**Last synced:** 2026-06-08
**llms.txt URL:** https://kat.imgnai.com/llms.txt
**Stored checksum:** `09a695f3958a6d9f17d4139179e2323600292c929be5c494253ae7df9d1410b3`

### Pre-generation check

Before submitting ANY generation request, check if the llms.txt checksum has been verified in the last 24 hours. If stale:

1. Fetch: `curl -s https://kat.imgnai.com/llms.txt`
2. Compute SHA256: `sha256sum` (Linux) or `shasum -a 256` (macOS)
3. Compare to stored checksum
4. If CHANGED → tell the user: "The Katana API model list has been updated since this skill was last synced. This may include new models, pricing changes, or removed models. Would you like me to check for changes and update the skill?"
5. If user says YES → parse new llms.txt, update models.md, update checksum and date
6. If user says NO → proceed with current models
7. Update last-checked date regardless

### llms.txt update process

When llms.txt changes, compare old vs new **holistically**. Diff the full documents — do not limit the review to a predefined checklist. Document ALL changes found and update all affected skill files accordingly: `models.md`, `SKILL.md`, workflow files.

**DO NOT auto-update without user confirmation.**

**Explicit approval rule:** During the llms.txt update process, always summarise ALL changes found and ask the user for explicit permission before updating any skill files (models.md, SKILL.md, workflow files). Do not auto-update without confirmation.

---

## Delivery Patterns

Deliver the generated media to the user via your agent's messaging/file capability. Include: model name, resolution/dimensions, credits, dollar cost, description, and the full-res URL (`original_data_url`).

### ⚠️ URL Display (MANDATORY)

ALL image and video deliveries MUST include the **full download URL** (`original_data_url`) as clickable text in the delivery message — not just the inline media attachment.

Users need the URL to:
- Download the full-resolution file
- Share it externally
- Archive it before expiry

**Include ALL URLs returned** — `original_data_url`, `thumbnail_image_url`, `final_frame_image_url`, `thumbnail_silent_video_mp4_url` — any URL the API returns for the asset. Do not assume the user only wants one.

Example:
```
MEDIA:https://k.imgnai.com/abc123.mp4

🔗 Full-res: https://k.imgnai.com/abc123.mp4
🖼️ Thumbnail: https://k.imgnai.com/def456.jpg
🎞️ Silent preview: https://k.imgnai.com/ghi789.mp4
⏰ Expires: Fri 16 May 2026, 14:00 BST
```

### ⚠️ Expiry Warning (MANDATORY)

ALL image and video generation summaries MUST include:
1. The **expiry timestamp** extracted from `responses[].output_assets[].expires_at` in the completed poll response — convert to user's local timezone for display
2. A clear warning that content must be downloaded before expiry if the user wishes to keep it

Example format:
```
⏰ Expires: Fri 16 May 2026, 14:00 BST — download before expiry if you need it long-term.
```

**Do NOT calculate expiry manually.** The API provides `expires_at` in the poll response. Use it directly. The 72h retention window may change server-side; `expires_at` is always authoritative.

For text/LLM: return the model's response verbatim. Then send a separate follow-up message with a cost summary per the "Cost Reporting" section above. Text completions do not require an expiry warning (no media URL to expire).

---

