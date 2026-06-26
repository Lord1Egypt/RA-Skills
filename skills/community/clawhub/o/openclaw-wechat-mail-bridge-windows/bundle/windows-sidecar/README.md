# oc-wx-sidecar

Windows-local sidecar process for WeChat desktop automation.

## Current state

- Bridge API client
- Adapter interface
- `mock` adapter (usable for flow tests)
- `pywinauto` / `uiautomation` adapter stubs
- Poll-claim-send-ack loop
- Local send retry before failed ACK (default 2 attempts)
- Optional local webhook proxy (`/bhmailer/webhook`) forwarding to plugin
- Optional local diagnostics server (`/health`, `/groups`)
- Inbound message dedupe cache to reduce duplicate event posts
- Periodic heartbeat reporting to plugin (`/api/v1/sidecar/heartbeat`)

## Start

1. `pip install -e .`
2. `oc-wx-sidecar --config ../examples/windows-sidecar.example.toml`
3. health-only probe: `oc-wx-sidecar --config ../examples/windows-sidecar.example.toml --health-once`

Optional adapter extras:

- `pip install -e .[pywinauto]`
- `pip install -e .[uiautomation]`
- `pip install -e .[visual]`

Optional Windows executable build:

- `powershell -ExecutionPolicy Bypass -File scripts/build_exe.ps1`

Adapter maturity:

- `mock`: stable for bridge smoke tests
- `pywinauto`/`uiautomation`: experimental generic polling + send

## Visual fallback listener (OCR/VLM)

When UIA tree text is incomplete (common in recent WeChat desktop builds), `uiautomation`
adapter can sample the chat area and extract latest message text with OCR or VLM.

1. Install extras: `pip install -e .[uiautomation,visual]`
2. Ensure local Tesseract is installed when using OCR mode.
3. Configure `examples/windows-sidecar.example.toml`:

```toml
[visual]
enabled = true
mode = "auto" # off | ocr | vlm | auto
sample_interval_sec = 2
ocr_lang = "chi_sim+eng"
ocr_max_chars = 160
vlm_base_url = "https://api.openai.com/v1"
vlm_api_key = ""
vlm_model = "gpt-4.1-mini"
```

`auto` mode tries OCR first, then escalates to VLM when OCR is empty or looks low-confidence
(for example truncated `/mail` commands, bare emails, or noisy OCR text).
