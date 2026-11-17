# Miao Vision Plugin Installation

Current compatible plugin release: `v0.10.8` (`skill-v0.10.8`), with
`@miao-vision/cli@0.9.8`. Download the cross-host bundle from:

```text
https://github.com/miaoshou-dev/miao-vision/releases/latest/download/miao-vision-plugin.zip
```

The cross-host plugin bundle is the recommended installation. It contains the
same source skill for Codex, Claude Code, and OpenClaw:

- Codex: see `codex.md`
- Claude Code: see `claude.md`
- OpenClaw: see `openclaw.md`
- Pi: see `pi.md`

The standalone Skill ZIP remains a lightweight compatibility channel for one
release cycle.

Miao Vision uses the global `miao-viz` on PATH. The bundled
`node scripts/check-miao-viz.mjs --print-path` checks compatibility and returns
its absolute path. A compatible CLI is accepted even when its version differs
from the recommendation. If missing or incompatible, approve the bundled
installer, which runs `npm install -g @miao-vision/cli` at the fixed recommended
version. It does not use sudo or change shell configuration. Old binaries in
`~/.miao-vision/bin` remain untouched and are no longer selected automatically.

PNG/PDF export requires Playwright and matching Chromium. Run
`node scripts/setup-export.mjs --host cli` to check without installing;
after approval add `--install`. It reuses host dependencies first, then
`~/.miao-vision/playwright`, then workspace dependencies. Claude Code checks
project and user `.claude` directories; other hosts may specify their actual
root with `--host-root`. Downloads use the selected Playwright's own installer.
Business-project dependencies are never modified. No API key is required.

All ordinary source-data workflows stay local. Optional data-story image/video
generation requires Node.js 22+, `ai-cli`, `AI_GATEWAY_API_KEY`, remote upload
confirmation, and separate Gateway fees. It sends only the displayed prompt
and approved references; the original Node.js 20 workflows do not require it.
PDF browser dependencies are optional and are not downloaded with the plugin.
Remove the global CLI with `npm uninstall -g @miao-vision/cli`; plugin uninstall leaves it intact.

## Try It

After installation, attach your file or link and ask your agent:

- “Analyze this sales spreadsheet and create an HTML report with key metrics and charts.”
- “Export this report as a printable A4 PDF.”
- “Use this week’s new data to update last week’s report with the same metrics and layout.”
