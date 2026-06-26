---
name: browser-agent
description: Browser automation with Playwright for opening pages, taking screenshots, finding or clicking DOM elements, filling forms, extracting text, and managing cookies/session state. Use when Codex needs deterministic browser control against real web pages, smoke-testing a site, grabbing DOM evidence, or automating straightforward UI flows.
---

# Browser Agent

Use Playwright-backed browser control for reproducible page actions.

## Workflow

1. Run `index.js` with a target URL.
2. Use action flags to open, screenshot, extract title/text, click selectors, fill inputs, or save/load session state.
3. Keep selectors explicit when clicking or filling.
4. Save evidence (screenshots / extracted text) to `out/`.

## Supported actions
- page open
- screenshot
- title read
- text extraction by selector
- click by selector
- fill input/textarea by selector
- save cookies/storage state
- load cookies/storage state

## Example

```bash
node skills/browser-agent/index.js --url https://example.com --screenshot out/example.png --title --extract h1
```
