# ASR

Use asynchronous recognition by default:

1. `POST /audio/async/`
2. read `jobId` or `job_id`
3. poll `GET /audio/async/{jobId}/`
4. continue while the response is 202 or status is `pending`/`processing`
5. finish on 200 with status `done`/`completed`
6. treat 422 or status `failed` as terminal

Use `POST /audio/` only when short synchronous processing is intentional.

## Input

- File formats: `wav`, `mp3`, `m4a`, `aac`, `ogg`, `flac`, and `pcm`
- Language: `mw` by default; `mn` for Cyrillic
- Sample rate: 16,000 by default
- Maximum file size: 10 MiB

The bundled script submits a multipart file to both synchronous and asynchronous endpoints and polls every three seconds, with a configurable overall timeout.

## Response

Return `data.text`. For ASR → translation, pass the value directly into `/translation/`.
