# Linux Guide

## Requirements

- `openclaw` in PATH
- `node` in PATH
- `npm` in PATH
- `curl` in PATH
- `bash`

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

## Permission notes (common on Linux)

`--apply` uses global npm install (`npm install -g`). Depending on your Node setup:

- With `nvm`/user-local Node: usually no sudo needed
- With system Node: you may need sudo or a writable global prefix

Examples:

```bash
# preferred: user-local Node toolchain
npm config get prefix

# if policy allows and system npm requires it
sudo bash scripts/openclaw-safe-update.sh --apply
```

## Troubleshooting

- Port conflict: usually not needed (script auto-selects free port >= 18000)
- Optional manual override: `--port 18895`
- Slow startup: set env `SIDECAR_MAX_WAIT=180`
- Check logs at: `~/.openclaw/logs/openclaw-sidecar-verify.log`
