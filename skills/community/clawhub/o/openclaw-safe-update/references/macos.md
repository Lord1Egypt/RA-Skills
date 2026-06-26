# macOS Guide

## Requirements

- `openclaw` in PATH
- `node` in PATH
- `npm` in PATH
- `curl` in PATH
- `bash` (macOS default)

Quick check:

```bash
command -v openclaw node npm curl bash
```

## Verify-only (recommended default)

```bash
bash scripts/openclaw-safe-update.sh
```

Pin a target version:

```bash
bash scripts/openclaw-safe-update.sh --target 2026.3.2
```

## Apply upgrade (explicit)

```bash
bash scripts/openclaw-safe-update.sh --apply
```

If your global npm path requires permission, use your preferred Node toolchain (nvm/mise) or run with elevated privileges according to your system policy.

## Troubleshooting

- Port conflict: usually not needed (script auto-selects free port >= 18000)
- Optional manual override: `--port 18895`
- Slow startup: set env `SIDECAR_MAX_WAIT=180`
- Check logs at: `~/.openclaw/logs/openclaw-sidecar-verify.log`
