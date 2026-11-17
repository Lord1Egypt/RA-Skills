---
name: "playwright-html-pdf-renderer"
description: "Render deterministic PDFs from HTML using local Playwright/Chromium."
---

# Playwright HTML → PDF Renderer

## Setup (one-time per environment)
- `npm install playwright`
- `npx playwright install chromium`

> The `npx playwright install chromium` step is bootstrap-only. Do not run it per request.

## Runtime (every render request)
1. Launch Playwright Chromium headless.
2. Load HTML (`file://...` or `setContent`).
3. Wait for readiness (`networkidle`, `document.fonts.ready`).
4. Export with `page.pdf({ printBackground: true, preferCSSPageSize: true })`.
5. Close browser and verify output file exists.

## API keys
- Local Playwright/Chromium: no API key required.
- Cloud browser provider: provider API key required.
