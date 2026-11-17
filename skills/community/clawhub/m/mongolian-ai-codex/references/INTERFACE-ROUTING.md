# Interface routing

Choose a route independently for every user turn.

## Priority

1. Image or screenshot text extraction → `POST /ocr/`
2. Audio or recording transcription → `POST /audio/async/`; use `POST /audio/` only for deliberately short synchronous work
3. Read aloud or synthesize speech → `POST /tts/async/`; use `POST /tts/` only for deliberately short synchronous work
4. Pure translation or script conversion → `POST /translation/`
5. Mongolian input with an explicit Chinese-answer request → `POST /chat/completions/` using the Chinese prompt
6. Mongolian conversation or original Mongolian composition → `POST /chat/completions/` using the Traditional Mongolian prompt
7. `.docx` or `.pdf` translation → the matching document endpoint

An attachment does not override the user's actual goal. For example, “read this attached Mongolian text aloud” requires extraction first and TTS second.

## Language and intent

- Traditional Mongolian characters U+1800–U+18AF imply `mw`.
- Cyrillic Mongolian characters usually imply `mn`.
- A request to translate, convert scripts, or explain the literal meaning uses `/translation/`.
- A request to answer, compose, reply, summarize, or continue a conversation uses `/chat/completions/`.
- `mw` ↔ `mn` conversion is one `/translation/` request.
- When the user does not specify the target for Chinese source text, default to Traditional Mongolian (`zh` → `mw`).
- When the user provides Mongolian text and asks what it means, default to Chinese unless another target is explicit.
- The translation endpoint does not accept Japanese, English, or other source codes. For a non-Mongolian source outside `zh/mw/mn`, first translate that source to Chinese using an appropriate general translation capability, then call `/translation/` for `zh` → `mw` or `mn`. Keep the intermediate Chinese out of the final response unless requested.

## Multi-step work

- OCR → translation: capture `data.text`, then pass it as `/translation/` content.
- ASR → translation: capture the completed job's `data.text`, then pass it as `/translation/` content.
- Extracted text → TTS: verify the requested language and pass the exact text to TTS.
- Other language → Mongolian: non-Mongolian source → Chinese intermediate → `/translation/`; never generate the Mongolian leg directly.
- Scanned PDF: use OCR only when the document translation endpoint cannot read a text layer.

Perform privacy and cost confirmation before the first paid step. Do not expose intermediate raw JSON or manually retype intermediate text.

## Long inputs

Remove navigation or unrelated page chrome before translating a web page. Split text only on natural boundaries and preserve order. Do not replace deterministic translation with chat generation.
