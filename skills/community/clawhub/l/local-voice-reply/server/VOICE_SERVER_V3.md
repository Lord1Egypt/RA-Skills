# Voice Server v3 (Chatterbox, Optimized)

## Layout

- `voice_server_v3.py`: API routes, request tracing middleware, and startup checks.
- `voice_engine.py`: synthesis engine, caching, timing metrics, and output handling.

## Install

```bash
python -m venv .venv
# mac/linux
source .venv/bin/activate
# windows powershell
# .\.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install fastapi uvicorn chatterbox-tts torch torchaudio python-multipart numpy
```

Also required:
- `ffmpeg` on `PATH` (Opus encoding).
- First startup may download Chatterbox model assets via `ChatterboxTTS.from_pretrained()`.

Optional env vars:
- `TARVIS_VOICE_OUTPUT_DIR` to override output directory (default: `~/.openclaw/media/outbound/voice-server-v3`).
- `TARVIS_VOICE_LOG_LEVEL` (`DEBUG`, `INFO`, etc.).
- `TARVIS_VOICE_PHRASE_RAM_CACHE_ITEMS` (default `24`) to tune in-memory phrase cache.
- `TARVIS_VOICE_FFMPEG_TIMEOUT_SEC` (default `60`) to avoid hung ffmpeg processes.

## Run

```bash
uvicorn voice_server_v3:app --host 127.0.0.1 --port 8000
```

Open Swagger docs at:
- http://127.0.0.1:8000/docs

## Endpoints

- `GET /health`
- `GET /benchmark`
- `POST /voice/register` (`voice_name`, `audio`) - voice name must match `[A-Za-z0-9][A-Za-z0-9_-]{0,63}`
- `POST /voice/warm` (`voice_name`)
- `POST /speak` (`text`, optional `voice_name`, `speed`, `exaggeration`, `cfg`) - returns `audio/ogg` (Opus)
- `POST /speak_stream` (same params as `/speak`) - chunked synthesis + Opus
- `POST /output/cleanup` (`path`) - delete staged `.opus` and sidecar `.json` only, constrained to output directory

## Performance Notes

- Method lookup for optional Chatterbox APIs is cached once on startup.
- `torch.inference_mode()` is used during generation.
- Phrase cache is shared by `/speak` and `/speak_stream`.
- A second in-memory phrase cache layer avoids repeated disk reads for hot phrases.
- Per-key synthesis locks avoid duplicate work under concurrent identical requests.
- Improved chunking handles CJK text without whitespace more efficiently.
- Stage latency metrics are tracked for tuning via `/benchmark`.
- Every request gets `X-Request-Id` / `X-Process-Ms`; synthesis responses include `X-Trace-Id`.
