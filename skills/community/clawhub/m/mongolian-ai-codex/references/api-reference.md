# API Reference

Base URL: `https://mongol.open-idea.net/api/v1`

Use `Authorization: Bearer $MONGOL_OPEN_IDEA_API_KEY` for every request.

This API is not compatible with OpenAI API paths or model names.

## Translation

Endpoint: `POST /translation`

Payload:

```json
{ "from": "zh", "to": "mw", "content": "待翻译文本" }
```

Language codes:

- `zh`: Chinese.
- `mw`: traditional Mongolian.
- `mn`: Cyrillic Mongolian.

Mongolian-to-Mongolian conversion should call `/translation` once; the service handles the intermediate route.

Return field: `data.tgtText`.

## Chat

Endpoint: `POST /chat/completions`

Model: `gpt-5-mw`

For Mongolian output:

```json
{
  "model": "gpt-5-mw",
  "messages": [
    { "role": "system", "content": "请只用纯传统蒙古文回答，不要包含任何中文汉字。" },
    { "role": "user", "content": "<user request>" }
  ],
  "temperature": 0.5,
  "max_tokens": 768
}
```

For Chinese output:

```json
{
  "model": "gpt-5-mw",
  "messages": [
    { "role": "system", "content": "请使用简体中文回答。若用户输入包含传统蒙古文，请先理解原文语义，再直接给出针对用户请求的中文回复正文。只输出最终中文回复正文；禁止添加问候、自我介绍、解释过程、标题、原文复述或无关补充。若用户明确要求翻译，请不要使用本模板，应改用 POST /translation。" },
    { "role": "user", "content": "<user request>" }
  ],
  "temperature": 0.5,
  "max_tokens": 768
}
```

Set `max_tokens` by Unicode code point length of the final user message:

- `L <= 50`: `256`.
- `51 <= L <= 200`: `768`.
- `201 <= L <= 1000`: `3072`.
- `L > 1000`: `8192`, or `6144` when the expected answer is not long.

Count code points correctly. In JavaScript use `Array.from(content).length`; avoid UTF-16 `string.length`.

Return field: `choices[0].message.content`.

## OCR

Endpoint: `POST /ocr`

Use when the user provides an image containing Mongolian or asks to extract image text. Return field: `data.text`.

When chaining OCR into translation, pass `data.text` directly as a variable to the translation request. Do not manually transcribe from previews or logs.

## TTS

Prefer async TTS for almost all use.

Before triggering TTS, ask the user to choose a voice from the full list unless they already chose one:

`Kore`, `Puck`, `Zephyr`, `Charon`, `Fenrir`, `Aoede`, `Leda`, `Orus`, `Iapetus`, `Sulafat`, `Achird`, `Achernar`.

If the user says "any", "you choose", or moves on, choose by content:

- Formal/default: `Kore`.
- News: `Iapetus`.
- Children: `Leda`.
- Emotional: `Sulafat`.

Do not volunteer numeric speed values. Say the default is normal speed. If the user explicitly asks for speed changes, map "faster" to `"speed": 1.2` and "slower" to `"speed": 0.8`; otherwise omit `speed`.

Async endpoint: `POST /tts/async`

Payload:

```json
{ "text": "ᠰᠠᠢᠨ ᠪᠠᠢᠨ᠎ᠠ ᠤᠤ", "lang": "mn-Mong", "voice": "Kore" }
```

Language codes:

- `mn-Mong`: traditional Mongolian.
- `mn-Cyrl`: Cyrillic Mongolian.
- `zh-Hans`: Chinese.
- `en`: English.

Poll `GET /tts/async/{jobId}` every 3-5 seconds until HTTP 200 and `status: done`. Decode JSON field `audioBase64` to a `.wav` file. Do not print base64, binary, or full WAV content.

Do not use removed SSE endpoint `POST /tts/stream`.

## ASR

Prefer async ASR.

Endpoint: `POST /audio/async`

Use `multipart/form-data` with:

- `file`: audio file.
- `language`: recognition language.
- `sample_rate`: optional.

Poll `GET /audio/async/{jobId}` every 3-5 seconds. `processing` or `pending` may return HTTP 202; completion returns HTTP 200 with `data.text`.

For extremely short audio, sync `POST /audio` may be used, but long audio should not rely on a single synchronous request.

## Documents

Use document translation endpoints for Word/PDF requests:

- `POST /word/translation`: Word document translation, return `data.text`.
- `POST /pdf/translation`: PDF document translation, return `data.text`.

Treat documents as higher-cost tasks. Estimate cost and confirm before calling.
