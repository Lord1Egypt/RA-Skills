---
name: mongolian-ai
description: Use for Mongolian-language work through the Mongol Open Idea API, including Chinese, traditional Mongolian, and Cyrillic Mongolian translation; Mongolian chat or writing; TTS; ASR; OCR; and Word/PDF document translation. Trigger when the user asks about Mongolian text, Mongolian script conversion, Mongolian audio, Mongolian OCR, or document translation involving Mongolian.
---

# Mongolian AI

Use the Mongol Open Idea API directly from Codex. This is not the OpenAI API and does not use OpenClaw gateway commands.

Base URL: `https://mongol.open-idea.net/api/v1`

This skill is suitable for public distribution because it does not bundle API keys, executable API clients, or account-specific configuration. Each user must provide their own API key.

## Setup

Read the API key from `MONGOL_OPEN_IDEA_API_KEY`.

If the variable is missing, tell the user:

```text
MONGOL_OPEN_IDEA_API_KEY is not configured. Create an API key at https://mongol.open-idea.net, then set it in your local shell or Codex environment as MONGOL_OPEN_IDEA_API_KEY. Do not paste the key into chat.
```

Never ask the user to paste the key into the conversation. If the user already pasted a key, warn them to revoke it and create a new one. Do not echo the key.

Do not store API keys in this skill folder, examples, logs, screenshots, or generated artifacts.

## Route Each Request

Choose the endpoint every turn:

- Image input or "OCR": `POST /ocr`.
- Audio input or transcription: prefer async `POST /audio/async`, then poll `GET /audio/async/{jobId}` every 3-5 seconds until done.
- Read aloud, synthesize speech, or play audio: prefer async `POST /tts/async`, then poll `GET /tts/async/{jobId}`; use sync `POST /tts` only for very short text.
- Pure translation or script conversion, including "translate", "what does this mean", "Cyrillic to traditional Mongolian": `POST /translation`.
- Mongolian text plus a request to answer in Chinese: `POST /chat/completions` with a Chinese system message.
- Mongolian input without translation intent: `POST /chat/completions` with a Mongolian-only system message.
- Word/PDF document translation: use the matching document endpoint; read `references/api-reference.md` first.

For OCR -> translation or ASR -> translation chains, pass the prior response field by variable or structured data. Do not manually copy text from logs, terminal previews, or chat snippets into the next paid request.

## Cost Confirmation

Short translations and short chats can be called directly.

Before long text, batch jobs, Word/PDF translation, OCR, ASR, or TTS, estimate cost and ask for confirmation. See `references/behavior.md` for rates and retry rules.

Do not repeat a successful paid request just because the visible output looks odd or the user dislikes the result. Ask for explicit approval before any redo that may charge again.

## Output Contract

After a successful API call, final user-visible output must be:

1. Business content only, unless the user explicitly asks for billing details.
2. A localized billing summary only when the user requested billing details, cost details, or account-balance information.

Business content fields:

- `POST /translation`: `data.tgtText`; concatenate segments in order.
- `POST /chat/completions`: `choices[0].message.content`.
- `POST /ocr`, `POST /word/translation`, `POST /pdf/translation`: `data.text`.
- `POST /audio` and completed `POST /audio/async`: `data.text`.
- `POST /tts`: save/play the binary audio; do not print binary, base64, or full WAV content.
- Completed `POST /tts/async`: decode `audioBase64` to WAV; do not print base64.

Billing fields must be parsed for cost awareness and retry safety:

- Headers: `X-Mengguyu-Billing-Charged`, `X-Mengguyu-Billing-Balance`, `X-Mengguyu-Billing-Currency`.
- JSON: `billingCharged`, `billingBalance`, and any returned currency field.

Do not expose billing fields, account balance, or paid-operation metadata by default. If the user explicitly asks for billing details, summarize only the returned values in the user's language and locale. If multiple successful calls in one workflow include billing fields, summarize them in call order. If no billing fields are present, say that the API did not return billing details.

Do not expose request payloads, raw JSON, internal routing notes, model names, token usage, or code blocks in the final answer unless the user is debugging the integration.

Read these references only when needed:

- `references/api-reference.md`: endpoint payloads, language codes, TTS/ASR polling, chat token sizing.
- `references/behavior.md`: cost, retry, redo, and output self-check rules.
