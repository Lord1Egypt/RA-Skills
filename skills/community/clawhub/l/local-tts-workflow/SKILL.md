---
name: local-tts-workflow
description: OpenClaw text-to-speech workflow for an OpenAI-compatible TTS server, including remote/self-hosted deployments such as vLLM Omni. Use when configuring, testing, debugging, or validating `/v1/audio/speech`, single-reply `[[tts:...]]` overrides, custom voice behavior, streaming vs non-streaming behavior, mode selection (base speaker, base clone, custom voice, voice design), local model-path fallback, and OpenClaw TTS integration. Also use when preparing text for speech output so numbers are normalized into spoken words instead of raw Arabic digits.
---

# Local TTS Workflow

Use this skill to debug the **actual speech pipeline** and to prepare text so the model reads it sanely.

Do **not** hardcode `127.0.0.1` blindly. Read the active OpenClaw config first and use the current `messages.tts.openai.baseUrl` as the source of truth.

Current known deployment in this workspace: `http://127.0.0.1:8000/v1`.

Current local model-path fallback worth remembering: if the server did not pull a model by registry name, it may be loading directly from a local path such as `./models/qwen3-tts-0.6b-mlx`.

When exact route shape matters, the local OpenAPI document is available at:

- `http://localhost:8000/openapi.json`

Use this OpenAPI doc as a schema/reference source to compare this local `mlx-audio` server against OpenAI’s API. Do not treat it as a health check.

## Core rule: normalize numbers before synthesis

If text is meant to be **spoken aloud**, do **not** leave Arabic numerals in the final TTS input.

Convert them into words first.

Examples:

- Chinese output: write `一 二 三`, not `123`
- English output: write `one two three`, not `123`

This rule matters because the TTS model can go weird or read digits badly when fed raw numerals.

When preparing spoken text, normalize:

- dates
- times
- counts
- version-like strings if they will be read aloud
- mixed Chinese/English numeric snippets

If preserving exact machine-readable formatting matters, keep one copy for display and a separate normalized copy for TTS.

## Workflow

### 1. Verify the server before touching OpenClaw

Read `~/.openclaw/openclaw.json` first and extract:

- `messages.tts.provider`
- `messages.tts.openai.baseUrl`
- `messages.tts.openai.model`
- `messages.tts.openai.voice`

Check the basics against the **actual configured host**:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/v1/models
```

Confirm that the intended TTS model exists.

If the model does not appear by pulled registry name, do not assume TTS is broken — this server may be loading a local-path model such as `./models/qwen3-tts-0.6b-mlx`.

If the server is task-gated, ensure TTS is enabled:

```bash
MLX_AUDIO_SERVER_TASKS=tts uv run python server.py
```

## 2. Prove the raw TTS endpoint works

Always isolate the server from the client stack.

Minimal non-streaming test:

```bash
curl http://127.0.0.1:8000/v1/audio/speech \
 -X POST \
 -H 'Content-Type: application/json' \
 -d '{
 "model": "/models/lj-qwen3-tts/",
 "voice": "lj",
 "input": "你好，这是一次性返回完整音频的测试。",
 "response_format": "wav",
 "stream": false
 }' \
 --output sample.wav
```

Basic streaming test:

```bash
curl http://127.0.0.1:8000/v1/audio/speech \
 -H 'Content-Type: application/json' \
 -X POST \
 -d '{
 "model": "/models/lj-qwen3-tts/",
 "voice": "lj",
 "input": "你好，这是实时流式语音合成测试。",
 "response_format": "wav",
 "stream": true,
 "streaming_interval": 2.0
 }' \
 | ffplay -i -
```

If direct `curl` works but OpenClaw does not, the bug is probably in the **TTS integration or provider selection layer**, not the TTS backend.

## 3. Distinguish server failure from integration failure

Use this rule:

- **Direct curl fails** → fix the local TTS server first
- **Direct curl works, but OpenClaw sounds wrong or falls back** → inspect OpenClaw provider selection, fallback, and request shape
- **OpenClaw sends requests but voice/mode is wrong** → inspect fields like `model`, `voice`, `instructions`, `ref_audio`, `ref_text`, and streaming flags

## 4. Know the four TTS modes

Use the right request shape for the right model type.

### Base speaker

Use built-in speaker playback.

Typical shape:

- model type: `base`
- no full `ref_audio + ref_text`
- `voice.id` means built-in speaker name

### Base clone

Use clone-style synthesis.

Typical shape:

- model type: `base`
- must provide both `ref_audio` and `ref_text`, or supply a consent voice identity that resolves to both

Hard rule: **do not attempt clone with only `ref_audio`**.

### CustomVoice

Use a model with prebuilt custom speakers.

Typical shape:

- model type: `custom_voice`
- `voice` may be accepted either as a plain string or as `{"id":"..."}` depending on the server
- for this workspace, `lj-qwen3-tts` / `/models/lj-qwen3-tts/` must use speaker/voice `lj`
- do not send clone payloads

### VoiceDesign

Use style-description-driven synthesis.

Typical shape:

- model type: `voice_design`
- must provide `instructions`
- do not send `voice`, `ref_audio`, or `ref_text`

## 5. Treat streaming as a real transport choice

This server supports real incremental generation, not fake post-hoc slicing.

Important behavior:

- Current OpenAPI says `stream` defaults to `false`
- `response_format` defaults to `mp3`
- `streaming_interval` defaults to `2.0`
- Required fields are only `model` and `input`
- Extra optional fields exposed by this local server include `instruct`, `voice`, `speed`, `gender`, `pitch`, `lang_code`, `ref_audio`, `ref_text`, `temperature`, `top_p`, `top_k`, `repetition_penalty`, `response_format`, `stream`, `streaming_interval`, `max_tokens`, and `verbose`

Do not assume OpenAI parity on names or defaults — check the local OpenAPI schema first.

## 6. Use consent uploads properly

For consent-based clone flows, upload voice material through `/v1/audio/voice_consents`.

Use `ref_text` with the recording. That is not optional in spirit, even if a workflow tries to pretend otherwise.

If later synthesis depends on stored consent voices, verify that the saved identity actually maps to both:

- reference audio
- reference text

## 7. OpenClaw-specific debugging pattern

When OpenClaw TTS appears broken:

1. Confirm `messages.tts` points at the actual configured endpoint in `openclaw.json`
2. Confirm the intended model exists in `/v1/models` or is otherwise accepted by the server; if not, check whether it is a local-path-backed deployment such as `./models/qwen3-tts-0.6b-mlx`
3. Confirm the selected provider is really the OpenAI-compatible path and not Microsoft fallback
4. Test direct `curl` with the same effective model/voice/mode assumptions
5. Inspect whether OpenClaw is falling back to another provider
6. If using `[[tts:...]]`, verify whether single-reply override keys (`model`, `voice`, maybe `provider`) are enabled and are being honored
7. If needed, compare raw request shape with a dump proxy

If OpenClaw reaches the server successfully, the next question is usually **which mode did it actually request**.

## 8. Preferred test ladder

Use this order:

1. `GET /health`
2. `GET /v1/models`
3. direct non-streaming TTS test
4. direct streaming TTS test
5. consent upload test if clone is involved
6. OpenAI client compatibility test if relevant
7. OpenClaw integration test
8. dump-proxy / log inspection only if still ambiguous

## 9. Common conclusions

### Server good, integration bad

Typical signs:

- manual `curl` returns playable audio
- OpenClaw output sounds like fallback voice or wrong mode
- provider selection is inconsistent

Conclusion: fix integration, not inference.

### Text normalization bug

Typical signs:

- synthesis succeeds technically
- numbers are read awkwardly, skipped, or glitched

Conclusion: normalize the spoken text first. Do not blame the transport layer for a prompt-content problem.

### Mode mismatch

Typical signs:

- clone request sent to CustomVoice
- VoiceDesign called without `instructions`
- only `ref_audio` present for Base clone

Conclusion: wrong request semantics for the chosen model type.

## 10. Use the reference doc when exact fields matter

Read `references/tts-api.md` when you need exact behavior for:

- `/v1/audio/speech`
- `/v1/audio/voice_consents`
- streaming vs non-streaming
- `stream_format="audio"` vs `stream_format="event"`
- mode selection and response headers
- consent storage semantics
- exact model/request mismatch errors

Do **not** assume generic OpenAI TTS docs fully match this local server.

## Resources

### references/

- `references/tts-api.md` — exact local API behavior, streaming semantics, mode rules, consent upload flow, and common error conditions
