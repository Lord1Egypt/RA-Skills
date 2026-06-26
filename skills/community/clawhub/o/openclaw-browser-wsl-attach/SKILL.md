---
name: openclaw-browser-wsl-attach
description: Automatically prepare, repair, and attach an OpenClaw-controlled Chromium browser in WSL or Linux environments where OpenClaw runs as root or in a headless session. Use when the user asks to configure browser control, fix browser startup failures, enable OpenClaw browser automation, repair CDP/browser issues, or start a reusable attachOnly Chromium session for screenshots, web automation, login flows, clicking, typing, or page extraction.
---

# OpenClaw Browser WSL Attach

Prepare a stable OpenClaw browser session by using Chromium in `attachOnly` mode with remote debugging enabled. Prefer this workflow in WSL, headless Linux, or root-run OpenClaw environments where direct browser launch is flaky.

## Workflow

1. Check browser readiness before changing anything.
2. If OpenClaw browser is already attached and healthy, reuse it.
3. If Chromium exists but OpenClaw launch is unstable, switch to `attachOnly` mode.
4. Run `python3 scripts/configure-browser.py` and restart the gateway.
5. Start Chromium manually with CDP on port `18800`.
6. Verify `curl http://127.0.0.1:18800/json/version` and `openclaw browser status`.
7. Then use normal browser actions through OpenClaw.

## Quick checks

Run these checks first:

```bash
openclaw browser status
command -v chromium || command -v chromium-browser || command -v google-chrome
curl -s http://127.0.0.1:18800/json/version
```

Interpretation:

- If `openclaw browser status` shows `running: true`, the browser is ready.
- If CDP JSON returns but OpenClaw still fails to launch browser itself, prefer `attachOnly`.
- If Chromium is missing, install or point `browser.executablePath` to a valid Chromium-based browser.

## Preferred configuration

Use this browser config in `~/.openclaw/openclaw.json` for WSL/root/headless Linux:

```json
"browser": {
  "enabled": true,
  "executablePath": "/usr/bin/chromium",
  "headless": true,
  "noSandbox": true,
  "attachOnly": true
}
```

Notes:

- Use `noSandbox: true` when Chromium runs as root.
- Use `attachOnly: true` when OpenClaw-managed launch times out or is unreliable.
- `browser: unknown` and `detectedBrowser: custom` are acceptable if `running: true` and CDP works.

## Start Chromium manually

Use the bundled scripts in this order:

```bash
python3 scripts/configure-browser.py
# restart gateway after config changes
bash scripts/start-browser.sh
bash scripts/healthcheck.sh
```

What each script does:

- `configure-browser.py`: updates `~/.openclaw/openclaw.json` for WSL/root/headless attachOnly mode and writes a timestamped backup
- `start-browser.sh`: creates the OpenClaw browser profile directory, kills stale Chromium on port `18800` when needed, starts headless Chromium, and prints verification output
- `healthcheck.sh`: shows binary, status, CDP, process, and environment diagnostics

## Verify success

Healthy state usually looks like:

- `curl http://127.0.0.1:18800/json/version` returns JSON
- `openclaw browser status` shows `running: true`
- `openclaw browser tabs` works

Once healthy, continue with OpenClaw browser tooling normally.

## Repair workflow

If browser control breaks later:

1. Re-run `openclaw browser status`
2. Re-run `bash scripts/start-browser.sh`
3. Run `bash scripts/healthcheck.sh`
4. If needed, inspect `/tmp/openclaw-browser.log`
5. Confirm port `18800` is not blocked by another process
6. Restart gateway only after config changes

## User-facing guidance

After setup, the user can simply ask for browser tasks in natural language, for example:

- open a URL
- search a phrase
- log into a site
- click a button
- extract page content
- take a screenshot

Read `references/troubleshooting.md` when browser attach still fails after the standard workflow.

Prefer this skill whenever the task is about making OpenClaw browser automation reliable on this machine, not just using the browser tool once.
