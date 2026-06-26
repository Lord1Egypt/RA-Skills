# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MD to Share is a Markdown-to-long-image converter. It converts `.md` files to JPEG/PNG images using Playwright's bundled Chromium for rendering. Designed to be callable by AI Agents (OpenClaw, Claude Code).

## Commands

```bash
# Install dependencies (automatically installs Playwright Chromium)
npm install

# Convert markdown to image
node md2img.mjs <input.md> <output.jpg>

# With options
node md2img.mjs report.md report.jpg --preset=openclaw --theme=dark --timeout=60000

# Or use global command after npm link
npm link
md2img <input.md> <output.jpg>
```

## Architecture

Single-file architecture in `md2img.mjs`:
1. Reads markdown file → parses with `marked`
2. Wraps HTML in styled template with theme system (light/dark auto-detect)
3. Launches isolated Chromium via Playwright (bundled, no system Chrome needed)
4. Creates browser context with `deviceScaleFactor` for high-DPI rendering
5. Screenshots full page to JPEG/PNG
6. Auto-splits large images at semantic boundaries (h1/h2/hr)

**Key design**: Uses Playwright's bundled Chromium, completely independent of any system browser. This prevents conflicts when running alongside OpenClaw's Chrome MCP instance.

## Dependencies

- Node.js 18+
- playwright (bundles its own Chromium — no system browser required)
- marked (markdown parser)

## Environment Variables

- `CHROME_PATH` — Optional: override Playwright's bundled Chromium with a custom executable
- `MD2IMG_TIMEOUT` — Optional: override default 30s timeout (in ms)

## Exit Codes

AI agents should check these for error handling:
- 0: Success
- 1-3: Input errors (args, file not found, read error)
- 4: Browser not available (run `npx playwright install chromium`)
- 5: Browser launch failed
- 6-7: Render/screenshot errors
- 8: Output write error
