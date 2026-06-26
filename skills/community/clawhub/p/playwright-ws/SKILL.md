---
name: playwright-ws
description: Browser automation via remote Playwright WebSocket server for screenshots, PDFs and testing.
metadata: {"clawdbot":{"emoji":"🎭","requires":{"bins":["node"],"env":["PLAYWRIGHT_WS"]},"primaryEnv":"PLAYWRIGHT_WS"}}
---

# Playwright Skill

Remote browser automation via Playwright WebSocket server. No local browser installation required.

> **Privacy notice:** The configured WebSocket server can observe all requested URLs, page contents, screenshots, and test interactions. Use only a Playwright server you control or fully trust, and avoid routing sensitive sites through untrusted infrastructure.

## Use Cases

| Task | Script | Description |
|------|--------|-------------|
| Screenshot | `scripts/screenshot.js` | Capture screenshots of web pages |
| PDF | `scripts/pdf-export.js` | Generate PDFs from URLs |
| Test | `scripts/test-runner.js` | Run Playwright tests remotely |

## Installation

```bash
cd playwright-skill
npm install
export PLAYWRIGHT_WS=ws://your-server:3000
```

## Quick Start

```bash
# Screenshot
node scripts/screenshot.js https://example.com screenshot.png --full-page

# PDF
node scripts/pdf-export.js https://example.com page.pdf
```

## Configuration

Set `PLAYWRIGHT_WS` environment variable to your Playwright WebSocket URL:

```bash
export PLAYWRIGHT_WS=ws://your-playwright-server:3000
```

## Scripts

- `screenshot.js` - Take screenshots with options
- `pdf-export.js` - Generate PDFs
- `test-runner.js` - Run remote tests

## References

- `references/selectors.md` - Selector strategies
- `references/api-reference.md` - API documentation