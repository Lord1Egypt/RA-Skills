---
name: openclaw-capture
description: Wrap a local openclaw_capture_workflow checkout as an OpenClaw/ClawHub skill that captures links, text, images, and videos, routes STT by platform, and fans results out to Telegram and Feishu.
---

# OpenClaw Capture

Use this skill when the user wants to send a link, pasted text, image, or video into the local `openclaw_capture_workflow` backend without modifying that repo, while choosing STT and notification modules by environment.

## Behavior

1. Normalize the request into the legacy payload contract:
   - `chat_id`
   - `reply_to_message_id`
   - `request_id`
   - `source_kind`
   - `source_url`
   - `raw_text`
   - `image_refs`
   - `platform_hint`
   - `requested_output_lang`
2. Immediately tell the user: `已收到，开始处理。`
3. Dispatch the payload through the wrapper runtime:

```bash
python3 scripts/dispatch_capture.py --payload-file /path/to/payload.json
```

You may also pipe JSON through stdin:

```bash
python3 scripts/dispatch_capture.py <<'JSON'
{"chat_id":"-1001","source_kind":"url","source_url":"https://example.com"}
JSON
```

## Routing Rules

- Keep the payload contract unchanged from the legacy workflow.
- For `mixed`, preserve URL, pasted text, and images together.
- STT profile resolves as:
  - macOS -> `mac_local_first`
  - non-macOS with `OPENCLAW_CAPTURE_LOCAL_STT_COMMAND` -> `local_cli_then_remote`
  - otherwise -> `remote_only`
- Output modules resolve from `OPENCLAW_CAPTURE_OUTPUTS`:
  - `telegram`
  - `feishu`

## Required Environment

- `OPENCLAW_CAPTURE_LEGACY_PROJECT_ROOT` should point to the local `openclaw_capture_workflow` checkout when this skill is not being run from the source repo.
- `OPENCLAW_CAPTURE_BACKEND_MODE=library|http`
- `OPENCLAW_CAPTURE_BACKEND_URL` when `BACKEND_MODE=http`
- `OPENCLAW_CAPTURE_STT_PROFILE=mac_local_first|local_cli_then_remote|remote_only` to override the default routing
- `OPENCLAW_CAPTURE_LOCAL_STT_COMMAND` for non-mac local CLI transcription fallback
- `OPENCLAW_CAPTURE_MODEL_PROFILE=openai_direct|aihubmix_gateway`
- `OPENCLAW_CAPTURE_MODEL_API_BASE_URL`
- `OPENCLAW_CAPTURE_MODEL_API_KEY`
- `OPENCLAW_CAPTURE_OUTPUTS=telegram,feishu`
- `OPENCLAW_CAPTURE_TELEGRAM_BOT_TOKEN`
- `OPENCLAW_CAPTURE_FEISHU_WEBHOOK`

## References

- Runtime profiles and environment matrix: [references/runtime-profiles.md](references/runtime-profiles.md)
- Module behavior and output fanout: [references/module-matrix.md](references/module-matrix.md)
- Legacy payload contract and mixed-input rules: [references/payload-contract.md](references/payload-contract.md)

Do not manually summarize after dispatch succeeds unless the user explicitly asks for an inline summary.

