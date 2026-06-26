# Module Matrix

## Core

- Always required.
- Normalizes the legacy ingest payload.
- Chooses backend mode.
- Builds one shared result envelope for every output channel.

## `mac-local`

- Enabled automatically when the host platform is macOS and no explicit STT profile overrides it.
- Relies on the legacy Apple local speech path plus local OCR already provided by `openclaw_capture_workflow`.

## `cloud-stt`

- Enabled automatically for non-macOS paths.
- If `OPENCLAW_CAPTURE_LOCAL_STT_COMMAND` is set, the wrapper tries local CLI transcription first.
- Otherwise it uses the legacy remote transcription path.

## `telegram`

- Enabled when `telegram` is present in `OPENCLAW_CAPTURE_OUTPUTS`.
- Reuses the legacy Telegram message builder so Telegram and Feishu receive the same summary envelope.

## `feishu`

- Enabled when `feishu` is present in `OPENCLAW_CAPTURE_OUTPUTS`.
- Sends the shared text envelope to a Feishu webhook as a plain text robot message.

