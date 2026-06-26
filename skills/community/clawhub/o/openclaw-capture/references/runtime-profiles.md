# Runtime Profiles

## Backend Mode

- `OPENCLAW_CAPTURE_BACKEND_MODE=library`
  - Imports the local `openclaw_capture_workflow` package and runs extraction, summary, and note writing in-process.
  - The wrapper owns notification fanout.
- `OPENCLAW_CAPTURE_BACKEND_MODE=http`
  - Sends the payload to `OPENCLAW_CAPTURE_BACKEND_URL`.
  - Polls `/jobs/<id>` until completion.
  - Treats Telegram as legacy-owned to avoid duplicate sends and adds Feishu fanout locally.

## STT Profile

- `mac_local_first`
  - Uses the legacy `video_audio_asr.py` bridge with Apple local speech first and remote fallback.
- `local_cli_then_remote`
  - Runs `OPENCLAW_CAPTURE_LOCAL_STT_COMMAND` first.
  - If the local CLI fails or returns empty output, falls back to the legacy remote audio path.
- `remote_only`
  - Uses the legacy remote audio path directly.

## Model Profile

- `openai_direct`
  - Default base URL: `https://api.openai.com/v1`
- `aihubmix_gateway`
  - Default base URL: `https://aihubmix.com/v1`

Override either profile with `OPENCLAW_CAPTURE_MODEL_API_BASE_URL`.

