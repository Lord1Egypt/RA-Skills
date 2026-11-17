# Install Miao Vision Plugin for OpenClaw

OpenClaw consumes the same Codex-compatible Miao Vision bundle. Miao Vision
does not require a native OpenClaw runtime plugin.

## 1. Install and enable

```bash
openclaw plugins install ./miao-vision-plugin.zip
openclaw plugins enable miao-vision
openclaw gateway restart
```

For local development, replace the ZIP with the repository path and add
`--link`.

## 2. Verify

```bash
openclaw plugins inspect miao-vision --runtime --json
```

Confirm that `skills/miao-vision` is visible.

Miao Vision uses the global `miao-viz` on PATH. The bundled
`node scripts/check-miao-viz.mjs --print-path` checks compatibility and returns
its absolute path. A compatible CLI is accepted even when its version differs
from the recommendation. If missing or incompatible, approve the bundled
installer, which runs `npm install -g @miao-vision/cli` at the fixed recommended
version. It does not use sudo or change shell configuration. Old binaries in
`~/.miao-vision/bin` remain untouched and are no longer selected automatically.

PNG/PDF export requires Playwright and matching Chromium. Run
`node scripts/setup-export.mjs --host openclaw` to check without installing;
after approval add `--install`. It reuses host dependencies first, then
`~/.miao-vision/playwright`, then workspace dependencies. Claude Code checks
project and user `.claude` directories; other hosts may specify their actual
root with `--host-root`. Downloads use the selected Playwright's own installer.
Business-project dependencies are never modified. No API key is required.

Plugin uninstall leaves user artifacts, the global CLI, and browser cache intact.
