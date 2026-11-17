# TTS

Use `POST /tts/async/` by default. Use `POST /tts/` only for intentionally short synchronous synthesis. Do not use `/tts/stream`.

## Parameters

- `text`: preserve the user's requested text exactly
- `lang`: `mn-Mong`, `mn-Cyrl`, `zh-Hans`, `en`, `ja`, `ko`, or `ru`
- `voice`: default `Kore`
- `speed`: default `1.0`, allowed range `0.5`–`2.0`

Available voices:

`Kore`, `Puck`, `Zephyr`, `Charon`, `Fenrir`, `Aoede`, `Leda`, `Orus`, `Iapetus`, `Sulafat`, `Achird`, `Achernar`

Do not interrupt a simple request merely to list every voice. Use `Kore` unless the user requests a particular voice or vocal style.

## Asynchronous flow

1. `POST /tts/async/` and read `jobId` or `job_id`.
2. Poll `GET /tts/async/{jobId}/` every three seconds.
3. Continue for 202 or `pending`/`processing`.
4. On `done`/`completed`, decode `audioBase64` to a WAV file.
5. Treat 422 or `failed` as terminal.

The script writes to a temporary sibling file, validates the audio signature, and atomically moves it to the requested output. It refuses to replace an existing output unless `--force` is explicit.

To keep text out of the process list, omit the text argument and pipe it to `scripts/tts.sh <lang> <output> [options]`.

## Response

Tell the user the saved file path. Never paste Base64, binary audio, or a WAV body into chat.
