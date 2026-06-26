# Windows Quick Install

This is the shortest path to a working local setup.

## 1. Prerequisites

Install these first:

- Windows 10 or 11
- Node.js 22+
- Python 3.11+
- WeChat desktop for Windows, already logged in
- Optional: Tesseract OCR if you want OCR mode in the visual fallback listener

## 2. Create local configs

Run:

```bat
scripts\init-local-configs.bat
```

That prepares:

- `plugin\.env`
- `runtime-config\openclaw.plugin.json`
- `runtime-config\windows-sidecar.toml`

## 3. Edit the local configs

Required edits:

- `plugin\.env`
  - set `BRIDGE_SHARED_SECRET`
  - set BHMailer-related values if you use the real backend
- `runtime-config\openclaw.plugin.json`
  - import or merge this into your local OpenClaw plugin config
- `runtime-config\windows-sidecar.toml`
  - set `adapter`
  - set `allow_groups`
  - keep `bridge.shared_secret` equal to `BRIDGE_SHARED_SECRET`

## 4. Start the plugin

```bat
scripts\start-plugin-dev.bat
```

## 5. Start the sidecar

```bat
scripts\start-sidecar-dev.bat
```

## 6. Optional health probe

```bat
scripts\probe-sidecar-health.bat
```

## Notes for real WeChat desktop use

- Prefer `adapter = "uiautomation"` in `runtime-config\windows-sidecar.toml`.
- Install the sidecar extras through the provided scripts; they already use `.[uiautomation,visual]`.
- If OCR quality is weak, keep `visual.mode = "auto"` and provide a VLM endpoint and API key.
- To build a standalone Windows executable for the sidecar, run:

```bat
scripts\build-sidecar-exe.bat
```
