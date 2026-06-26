# Configuration Guide

## Quick Start

1. Copy `.env.example` to `.env`.
2. Fill in your `API_BASE_URL` and `API_KEY`.
3. Run the scripts from the repository root.

## Environment Variable Groups

### Global API Config

All image/video generation scripts share one API address and key:

- `API_BASE_URL` (required) — API gateway base URL, e.g. `https://chat.aifast.site`
- `API_KEY` (required) — Bearer token / API key

### LibTV Session Mode

- `LIBTV_ACCESS_KEY` (required)
- `OPENAPI_IM_BASE` (optional, default `https://im.liblib.tv`)
- `IM_BASE_URL` (optional alias)

### Gemini Image Mode

Uses `API_BASE_URL` / `API_KEY` from Global API Config.

- `GEMINI_MODEL` (optional)

### Unified Video Mode

Uses `API_BASE_URL` / `API_KEY` from Global API Config.

The project supports multiple providers through shared scripts:

- Multipart path (`POST /v1/videos`): Sora, Veo, Grok, Doubao
- JSON path (`POST /v1/video/generations`): Vidu

Provider-specific model parameters (optional):

- `SORA_MODEL`, `SORA_SIZE`, `SORA_SECONDS`
- `VEO_MODEL`, `VEO_SIZE`, `VEO_SECONDS`
- `GROK_MODEL`, `GROK_SIZE`, `GROK_SECONDS`, `GROK_ASPECT_RATIO`
- `DOUBAO_MODEL`, `DOUBAO_SIZE`, `DOUBAO_SECONDS`
- `VIDU_MODEL`, `VIDU_SIZE`, `VIDU_DURATION`, `VIDU_ASPECT_RATIO`

## Recommended Validation Commands

```bash
python scripts/sora_generate_video.py "test prompt" --model sora-2 --raw
python scripts/veo_generate_video.py "test prompt" --raw
python scripts/grok_generate_video.py "test prompt" --raw
python scripts/doubao_generate_video.py "test prompt" --raw
python scripts/vidu_generate_video.py "test prompt" --raw
```

## Notes

- Do not commit real API keys.
- Keep `.env` local and use `.env.example` for sharing.
- If a provider returns `model_not_found`, the gateway channel is not available for that model.
