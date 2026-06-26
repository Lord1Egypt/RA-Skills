# Troubleshooting

## Healthy state

A good state usually means:

- `openclaw browser status` shows `running: true`
- `curl http://127.0.0.1:18800/json/version` returns JSON
- `openclaw browser tabs` works

## Common issues

### `running: false`

Usually means Chromium is not running or OpenClaw cannot attach.

Fix order:

1. Run `python3 scripts/configure-browser.py`
2. Restart gateway after config changes
3. Run `bash scripts/start-browser.sh`
4. Re-check `openclaw browser status`

### Chromium fails as root

Use `--no-sandbox`. This is already included by this skill.

### `browser: unknown` or `detectedBrowser: custom`

This is acceptable for a custom Chromium path. Treat it as healthy if CDP works and status is `running: true`.

### Port 18800 already occupied

Kill stale Chromium started with the same remote debugging port, then re-run `start-browser.sh`.

### OpenClaw launch times out

Prefer `attachOnly: true` and let Chromium be started manually.

## Recommended operator flow

For this machine, prefer:

1. configure
2. restart gateway
3. start browser
4. verify status
5. use browser naturally through OpenClaw
