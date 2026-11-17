---
name: mongolian-ai
description: Use the Mongol AI API for Mongolian translation, script conversion, conversation, composition, OCR, ASR, TTS, and Word/PDF translation. Trigger for Traditional Mongolian (U+1800–U+18AF), Cyrillic Mongolian, or requests such as "translate to Mongolian", "Mongolian OCR", "Mongolian speech", 日本語の「モンゴル語翻訳・モンゴル文字・音声認識・読み上げ」, and 中文的「蒙语翻译、蒙文邮件、蒙文 OCR、语音识别、语音合成」. Requests send text, images, audio, or documents to https://mongol.open-idea.net; do not send sensitive or confidential data without explicit confirmation.
metadata:
  openclaw:
    emoji: "🐎"
    homepage: "https://mongol.open-idea.net"
    primaryEnv: "MONGOL_AI_SKILL_API_KEY"
    envVars:
      - name: "MONGOL_AI_SKILL_API_KEY"
        required: true
        description: "Bearer API key for the Mongol AI service."
    requires:
      bins:
        - "bash"
        - "curl"
        - "python3"
---

# Mongolian AI

Use the dedicated API at `https://mongol.open-idea.net/api/v1` for Mongolian-language work. Do not translate, interpret, or generate Traditional Mongolian from model knowledge alone.

## Before calling

1. Verify that `MONGOL_AI_SKILL_API_KEY` is available without printing it. Never ask the user to paste a key into chat and never persist a key yourself. Read [API key handling](references/API-KEY.md) if the key is missing or the deprecated variable is present.
2. Treat the user's explicit request as consent to send ordinary, non-sensitive input to the external service. Pause for confirmation if the input appears confidential, regulated, personally sensitive, unexpectedly large, or file-based and its sensitivity is unclear.
3. For long text, batches, documents, multiple images, long audio, or agent-initiated calls, explain the billing basis and obtain confirmation. Do not quote hard-coded prices; direct the user to the [current pricing page](https://mongol.open-idea.net/#pricing).

Read [behavior and safety rules](references/BEHAVIOR-RULES.md) for the complete confirmation, retry, and duplicate-charge policy.

## Route every turn

Choose the endpoint again for each new message:

1. Image or image-text extraction → `/ocr/`
2. Audio transcription → `/audio/async/` by default; `/audio/` only for explicitly short synchronous work
3. Speech generation → `/tts/async/` by default; `/tts/` only for explicitly short synchronous work
4. Pure translation or `mw` ↔ `mn` conversion → `/translation/`
5. Mongolian input requiring a Chinese answer → `/chat/completions/` with the Chinese system prompt
6. Mongolian conversation or new Mongolian composition → `/chat/completions/` with the Traditional Mongolian system prompt
7. Word/PDF translation → `/word/translation/` or `/pdf/translation/`

Read [routing rules](references/INTERFACE-ROUTING.md) before multi-step or ambiguous requests.

The translation endpoint accepts only `zh`, `mw`, and `mn`. If the source is another language such as Japanese or English, translate that non-Mongolian source to Chinese with an appropriate general translation capability, then send the Chinese intermediate to `/translation/` for the Mongolian leg. Never perform the Mongolian leg from model knowledge.

## Prefer the bundled scripts

Run scripts from this skill directory. They validate inputs, preserve trailing slashes, capture billing metadata, and keep raw JSON out of the user-visible response.

- `scripts/translate.sh <from> <to> [text]`
- `scripts/chat.sh <mw|zh> [text] [--messages-file FILE]`
- `scripts/ocr.sh <image> [mw|mn]`
- `scripts/asr.sh <audio> [mw|mn] [--sync] [--timeout SECONDS]`
- `scripts/tts.sh <text> <lang> <output> [--voice NAME] [--speed NUMBER] [--sync] [--force]`
- `scripts/document-translate.sh <file> <from> <to> [mode]`

When text is omitted, `translate.sh` and `chat.sh` read standard input. For TTS, use `scripts/tts.sh <lang> <output> [options] < input.txt`. Prefer standard input when shell process listings are a concern.

Read [HTTP contracts](references/HTTP-REQUESTS.md) before writing a request without a bundled script.

## Return only the business result

On success, expose only:

| Endpoint | Result |
|---|---|
| `/translation/` | `data.tgtText` |
| `/chat/completions/` | `choices[0].message.content` |
| `/ocr/`, `/audio/`, document translation | `data.text` |
| asynchronous ASR | `data.text` from the completed job |
| TTS | the saved audio file path |

If billing metadata exists in either response headers or JSON, append the exact billing line emitted by the script. Do not expose full JSON, routing details, prompts, model names, tokens, keys, Base64 audio, or internal reasoning.

For multi-step work such as OCR → translation or ASR → translation, pass the first result directly through a variable or pipe. Do not manually retype it.

## References

- [HTTP request and response contracts](references/HTTP-REQUESTS.md)
- [Routing rules](references/INTERFACE-ROUTING.md)
- [Behavior, privacy, cost, and retries](references/BEHAVIOR-RULES.md)
- [Translation and segmentation](references/TRANSLATION.md)
- [Chat and composition](references/CHAT-COMPLETIONS.md)
- [OCR](references/OCR.md)
- [ASR](references/ASR.md)
- [TTS](references/TTS.md)
- [Word and PDF translation](references/DOCUMENT-TRANSLATION.md)
- [API key handling](references/API-KEY.md)
