---
name: html-to-pdf
description: >
  Convert an HTML file to a PDF using headless Chrome (Puppeteer) — the same approach
  atypica uses for its AI-generated research reports.
  Use this skill whenever the user wants to export an HTML file, report, or webpage snapshot
  to PDF. Trigger on phrases like "convert to PDF", "export as PDF", "save report as PDF",
  "html to pdf", "generate PDF from HTML", or when a user hands you an .html file and
  asks for a downloadable document. Even if the user just says "make a PDF of this",
  use this skill if the source is HTML.
---

## Overview

This skill converts an HTML file to PDF using **Puppeteer** (headless Chromium), exactly
how atypica exports its AI research reports. Two modes are supported:

| Mode | When to use |
|------|-------------|
| **Single-page** (default) | Design/report pages meant to look like one tall poster — no page breaks. Full-width at 1440 px. |
| **Paginated** | Documents meant to be printed or read page-by-page (A4, Letter, etc.). |

## Quickstart (3 steps)

```bash
# 1. Copy the bundled scripts to a working directory
cp <skill-dir>/scripts/html-to-pdf.js ./
cp <skill-dir>/scripts/package.json ./

# 2. Install the only dependency (downloads Chromium automatically, ~170 MB, one-time)
npm install

# 3. Run
node html-to-pdf.js report.html report.pdf
```

`<skill-dir>` is the directory that contains this SKILL.md file.

> **Note:** `npm install puppeteer` (~170 MB) downloads a pinned Chromium binary.
> This is the only install step — no system Chrome, no wkhtmltopdf, no separate server needed.
> If the environment already has Puppeteer installed, skip step 2.

---

## Command reference

```
node html-to-pdf.js <input.html> <output.pdf> [options]

Options:
  --paginated         A4-paginated mode (respects @media print, page-breaks)
  --format <fmt>      Page format: A4 (default), A3, Letter, Legal
  --width <px>        Viewport width for single-page mode (default: 1440)
  --wait <ms>         Extra milliseconds to wait after page load (for JS-rendered content)
  --header-footer     Add page-number footer in paginated mode
```

### Examples

```bash
# Single-page full-height (atypica report style)
node html-to-pdf.js report.html report.pdf

# A4 paginated document
node html-to-pdf.js document.html document.pdf --paginated

# A4 with page numbers
node html-to-pdf.js document.html document.pdf --paginated --header-footer

# Narrower single-page layout
node html-to-pdf.js report.html report.pdf --width 1280

# Wait 2 s for JavaScript-rendered charts
node html-to-pdf.js dashboard.html dashboard.pdf --wait 2000
```

---

## How it works (mirrors atypica's browser service)

1. **Launches headless Chromium** via Puppeteer with sandbox disabled and CJK font hints enabled.
2. **Loads the HTML** from a `file://` URL so relative assets (images, local CSS) resolve correctly.
3. **Injects system-font CSS** to ensure Chinese/Japanese/Korean characters render on any OS.
4. **Single-page mode**: measures `document.body.scrollHeight`, sets viewport to that height, and generates a single-page PDF at that exact size — no clipping, no page breaks.
5. **Paginated mode**: injects `@media print` CSS for clean page-breaks, then generates a standard-format paginated PDF.
6. Writes the PDF buffer to the output path.

---

## Handling common issues

| Problem | Fix |
|---------|-----|
| Chromium not found after `npm install puppeteer` | Run `npx puppeteer browsers install chrome` |
| Missing system fonts / boxes instead of CJK chars | Inject works for most cases; for guaranteed rendering install `fonts-noto-cjk` (Linux) or ensure macOS system fonts are accessible |
| JavaScript-rendered content missing | Add `--wait 2000` (or more) to let JS execute after load |
| Images not loading | Make sure image `src` paths are relative to the HTML file location |
| PDF cut off at bottom | The script auto-measures height; if content loads lazily add `--wait` |
| `--no-sandbox` error in strict container | Puppeteer requires `--no-sandbox` in Docker/CI; this flag is already set |

---

## Dependency notes

- **Node.js ≥ 18** required (≥ 20 recommended)
- `puppeteer` is the only `npm` dependency — it self-contains Chromium
- No global Chrome installation needed
- Works on macOS, Linux, and Windows (WSL)
- In CI/Docker, add `--disable-dev-shm-usage` (already included in the script)
