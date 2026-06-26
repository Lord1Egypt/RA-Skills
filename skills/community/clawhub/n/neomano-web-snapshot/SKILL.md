---
name: neomano-web-snapshot
description: Take a screenshot (PNG) of any website in a headless way (no GUI) to verify it's rendering/working. Use when the user asks for a website screenshot, uptime visual check, or to confirm a page loads correctly.
metadata: {"clawdbot":{"emoji":"📸","requires":{"bins":["node","bun"],"npm":["playwright"]}}}
---

## Requirements

- **Node.js** (required)
- **bun** (required for the provided bootstrap/install flow)
- **Playwright (Node package)** (required)

This skill uses **Playwright + headless Chromium** (works without a GUI).

## One-time setup (headless)

This installs dependencies into **this skill folder** (`{baseDir}`):

```bash
bash {baseDir}/scripts/bootstrap.sh
```

Note: `node_modules/` is intentionally *not* shipped in the skill package; dependencies are installed locally by the bootstrap script.

If you installed Playwright elsewhere (global or in a different project folder), Node may not find it when running this skill.

## Take a screenshot

```bash
bash {baseDir}/scripts/snapshot.sh "https://example.com" --out ./snapshots/example.png
```

Options:
- `--full-page` to capture full scroll height.
- `--wait-ms 2000` to wait after load (useful for SPAs).
