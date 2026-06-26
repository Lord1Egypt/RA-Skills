---
name: local-voice-reply
description: Local OPUS/Ogg voice-reply pipeline for Feishu/Discord with structured voice customization. Default voice is Juno (`voice/juno_ref.wav`), with support for registered custom voices via API. Includes FastAPI server + scripts for stable generation/sending. Requires ffmpeg on PATH and Python deps (torch/torchaudio/chatterbox-tts/fastapi/uvicorn). Activate for /voice_mode_on or any user request for voice/audio reply.
---

# Local Voice Reply

Use this skill to turn text into a cloned/custom-voice audio reply and deliver it reliably to Feishu or Discord.

## Structured skill definition

- Purpose: local low-latency voice replies in Opus/Ogg.
- Channels: Feishu + Discord.
- Default voice: `juno` (reference file: `voice/juno_ref.wav`).
- Custom voice modes:
  1) File-based: replace/update `voice/juno_ref.wav`.
  2) Registry-based: upload/register voices via `POST /voice/register`, then call by `voice_name`.
- Output: `.opus` (Ogg container) under `.openclaw/media/outbound/voice-server-v3/` (or `TARVIS_VOICE_OUTPUT_DIR`).
- Control scripts:
  - `scripts/send_voice_reply.ps1` (server API path)
  - `scripts/generate_cuda_voice.ps1` (stable local CUDA generation path)

Server implementation is kept with the skill (not workspace root):
- `server/voice_server_v3.py` (FastAPI routes)
- `server/voice_engine.py` (generation and cache engine)

Voice assets are also colocated with the skill:
- `voice/`

## Runtime requirements

- `ffmpeg` must be installed and available on `PATH` (required for Opus encoding).
- Python packages required by the server:
  - `fastapi`
  - `uvicorn`
  - `python-multipart`
  - `chatterbox-tts`
  - `torch`
  - `torchaudio`
  - `numpy`
- On first startup, `ChatterboxTTS.from_pretrained()` may download model assets, so initial run can require network access and additional disk.
- Optional env vars:
  - `TARVIS_VOICE_OUTPUT_DIR` to override where generated Opus files are written.
  - `TARVIS_VOICE_DEVICE` to force device selection (`cuda`/`gpu`, `mps`, or `cpu`).

## Persistence behavior

- Uploaded voice samples from `POST /voice/register` are persisted under `server/voices/`.
- Cache and registry data are persisted under `server/voice_cache/`.
- Generated Opus outputs are written under `.openclaw/media/outbound/voice-server-v3/` by default (or `TARVIS_VOICE_OUTPUT_DIR` when set).
- `POST /output/cleanup` only deletes staged `.opus` files inside the configured output directory and their `.json` sidecar files.

## Use this workflow

1. Ensure local **v3.3** TTS server is running from this skill folder:
   - `python -m uvicorn --app-dir server voice_server_v3:app --host 127.0.0.1 --port 8000`
2. Call `/speak` with `text` (and optional `speed`, `exaggeration`, `cfg`).
   - `voice_name` defaults to `juno`.
3. Receive **Opus directly** from server (`audio/ogg`) in Juno voice.
4. Save final media into allowed path:
   - `C:\Users\hanli\.openclaw\media\outbound\`
5. Send with `message` tool:
   - `action=send`
   - `filePath=<allowed-path>`
   - `asVoice=true`
   - For Feishu: `channel=feishu`
   - For Discord: `channel=discord`

## Voice customization guide

### A) Replace default Juno reference

1. Replace `voice/juno_ref.wav` with your target reference voice sample.
2. Keep sample clean (single speaker, low noise, clear pronunciation).
3. Restart server and test with `voice_name=juno`.

### B) Register additional named voices

1. Call `POST /voice/register` with a reference sample and target `voice_name`.
2. Confirm registration under `server/voices/`.
3. Generate with that `voice_name` in `/speak` or `/speak_stream`.

## Defaults

- `voice_name`: `juno`
- `speed`: `1.2`
- Output format: Opus in Ogg container from server `/speak` (no post-conversion)
- Discord compatibility: Ogg/Opus is supported and can be sent as voice/audio with `asVoice=true`

## Speed Improvements In This Version

- Caches model capability lookups once at startup.
- Uses `torch.inference_mode()` during synthesis to reduce overhead.
- Reuses phrase cache for both `/speak` and `/speak_stream`.
- Improves chunking behavior for long CJK text to avoid oversized chunks.
- Keeps latency metrics for benchmarking and tuning.

## Common failure and fix

- Error: `LocalMediaAccessError ... path-not-allowed`
- Fix: copy the file into `.openclaw/media/outbound` before sending.

## Script

Use `scripts/send_voice_reply.ps1` to generate Opus directly with defaults (`voice_name=juno`, `speed=1.2`).
It auto-selects `/speak_stream` for longer text (or when `-Stream` is passed) for better throughput.

For stable CUDA generation command patterns under stricter exec approval policies, use:
- `scripts/generate_cuda_voice.ps1 -Text "..."`
This keeps the outer command shape fixed so `allow-always` is more reusable.
