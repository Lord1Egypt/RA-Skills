# CLI vs SDK Routing Guide

Decide whether to run `gladia transcribe` or escalate to SDK skills.

## Default rule

**Use CLI** when the feature has a CLI flag and the user wants a terminal workflow.

**Escalate to SDK** for everything else — follow the skill links below.

## Transcription modes

**CLI (`gladia transcribe`):**

- Pre-recorded local file or `http(s)` URL

**SDK only — escalate:**

- Live / real-time streaming → [gladia-live-transcription](../gladia-live-transcription/SKILL.md)
- Pre-recorded via application code → [gladia-pre-recorded-transcription](../gladia-pre-recorded-transcription/SKILL.md)
- Batch jobs with webhooks → SDK `transcribe()` + `callback_url`
- Job management (list, get, delete) → SDK `get()`, `list()`, `delete()`

## CLI-supported flags

These map directly to `gladia transcribe` flags:

- **Basic transcription** — default (no flag)
- **Speaker diarization** — `--diarize`
- **Language hints** — `--language en,fr` (comma-separated; constrains detection, does not enable code switching)
- **Code switching** — `--code-switching`
- **Model selection** — `--model solaria-1` or `--model solaria-3`

For advanced diarization (exact speaker count, min/max speakers), escalate to [gladia-audio-intelligence](../gladia-audio-intelligence/SKILL.md) — `diarization_config`.

## SDK-only audio intelligence

No CLI flags exist for these. Use [gladia-audio-intelligence](../gladia-audio-intelligence/SKILL.md):

- Translation — `translation`
- API summarization addon — `summarization` (not the same as the agent summarizing `-o text` output in conversation)
- Named entity recognition — `named_entity_recognition`
- PII redaction — `pii_redaction`
- Sentiment analysis — `sentiment_analysis`
- Audio-to-LLM — `audio_to_llm`
- Custom vocabulary — `custom_vocabulary`


## Output formats

**CLI (`-o` / `--output`):**

- Plain text transcript — `text` (default)
- Utterances with timestamps — `json`
- Full API response — `json-full`
- SRT subtitles — `srt` (add `--diarize` for speaker labels)
- VTT subtitles — `vtt` (add `--diarize` for speaker labels)

**SDK equivalents:**

- Plain text — `result.transcription.full_transcript`
- Utterances — `result.transcription.utterances`
- Full response — `get()` / `transcribe()` response
- Subtitles — `subtitles` addon or format from utterances

## When to escalate

Escalate from CLI to SDK skills when:

1. User requests a feature with **no CLI flag** (see SDK-only sections above)
2. User is building an **application**, not a one-off terminal task
3. User needs **advanced diarization config** beyond `--diarize`
4. User needs **async delivery** (webhooks, job polling in code)
5. `gladia` CLI is **not installed** and user does not want to install it

For setup and SDK vs raw API decisions, start with [gladia-sdk-integration](../gladia-sdk-integration/SKILL.md).
