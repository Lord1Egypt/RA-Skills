---
name: kai-html-export
description: >-
  Export any HTML file to PPTX or PNG, or publish HTML to a public share URL. Use when the user wants to convert an
  HTML presentation to PowerPoint, screenshot a web page, export an HTML
  report as an image, or share HTML online. Triggers: /kai-html-export, --pptx, --png,
  "export to pptx", "screenshot html", "convert html to powerpoint",
  "导出为ppt", "导出ppt", "生成ppt", "转成ppt", "导出幻灯片",
  "html转ppt", "保存为ppt", "可编辑的ppt", "native模式", "导出为可编辑",
  "share html", "deploy html", "share slides", "发布 html".
version: 1.2.0
metadata:
  openclaw:
    emoji: "📤"
    os:
      - darwin
      - linux
      - windows
    requires:
      bins:
        - python3
    install:
      - id: python-pptx
        kind: uv
        package: python-pptx
        label: "python-pptx (PPTX assembly)"
      - id: playwright
        kind: uv
        package: playwright
        label: "Playwright (headless browser for screenshots)"
      - id: beautifulsoup4
        kind: uv
        package: beautifulsoup4
        label: "BeautifulSoup4 (HTML parsing for native export)"
      - id: lxml
        kind: uv
        package: lxml
        label: "lxml (HTML parser backend)"
---

# kai-html-export

Export any HTML file to PPTX or PNG using a headless browser, or publish it to a public URL. PPTX and PNG export need no Node.js; the optional share helper uses Cloudflare Pages by default and Vercel as a fallback. In hosted cloud sandboxes, automatic sharing is disabled and the helper prints manual-share guidance instead of starting a deploy flow.

## Commands

| Command | What it does |
|---------|-------------|
| `/kai-html-export [file.html]` | Export HTML presentation to PPTX (auto-detects slides) |
| `/kai-html-export --pptx [file.html]` | Explicit PPTX export |
| `/kai-html-export --png [file.html]` | Full-page screenshot to PNG |
| `/kai-html-export --png --scale 2 [file.html]` | 2× resolution screenshot |
| `python3 <skill-path>/scripts/share-html.py [file.html|folder]` | Publish HTML to a public URL (Cloudflare default) |
| `python3 <skill-path>/scripts/share-html.py --provider vercel [file.html|folder]` | Publish HTML to a public URL with Vercel |

If no file is specified, use the most recently modified `.html` file in the current directory.

## Export to PPTX

Run the bundled script:

```bash
python3 <skill-path>/scripts/export-pptx.py <file.html> [output.pptx] [--mode image|native] [--width 1440] [--height 900]
```

### Export Modes

**`--mode image`** (default):
- Pixel-perfect screenshots of each slide
- Visual fidelity: ⭐⭐⭐⭐⭐
- Editability: ❌ None (text is rasterized)
- Best for: archiving, sharing final presentations

**`--mode native`** (new):
- Editable text, shapes, and tables
- Visual fidelity: ⭐⭐⭐ (simplified gradients, no shadows)
- Editability: ✅ Full text editing
- Best for: collaborative editing, content reuse

Supported in native mode:
- Text (h1-h6, p): font size, color, bold, alignment
- Lists (ul, ol): bullet points
- Tables: editable cells
- Shapes (div with solid background): rectangles
- Images: native insertion

Not supported in native mode (fall back to image):
- CSS gradients → solid color approximation
- Box shadows → omitted
- Custom web fonts → system fonts
- SVG graphics → rasterize to PNG

## Export to PNG

Run the bundled script:

```bash
python3 <skill-path>/scripts/screenshot.py <file.html> [output.png] [--width 1440] [--scale 2]
```

- Captures the full page at the specified width
- `--scale 2` produces a 2× retina-quality image
- Useful for sharing reports or single-page HTML as images

## Share HTML to a public URL

Run the bundled helper:

```bash
python3 <skill-path>/scripts/share-html.py <file.html|folder>
python3 <skill-path>/scripts/share-html.py --provider vercel <file.html|folder>
```

- Accepts either a single HTML file or a folder containing `index.html`
- Copies common relative assets automatically when starting from a single file
- Uses Cloudflare Pages by default and keeps Vercel as an optional fallback
- Cloudflare is the recommended default for China-facing links
- Automatic sharing is disabled in hosted cloud sandboxes; the helper tells the user to share manually from a local machine instead
- Cloudflare requires `wrangler login` before first local use
- Vercel requires `npx vercel login` before first local use

## Dependencies

| Package | Purpose | Install |
|---------|---------|---------|
| `playwright` | Headless browser screenshots | `pip install playwright` |
| `python-pptx` | Assemble screenshots into PPTX | `pip install python-pptx` |
| Node.js + Wrangler / Vercel CLI | Optional live URL publishing | `wrangler login` or `npx vercel login` |

No browser download needed if Chrome, Edge, or Brave is already installed. URL publishing is optional and separate from export.

## QA Process

After every native-mode export, assume something looks wrong until proven otherwise:

1. **Preview grid** — the export automatically saves `{name}-preview.png` with thumbnails of slide 1, ~1/3, ~2/3, and last. Open it immediately: `open {name}-preview.png`
2. **Structural check** — if slide count mismatches or any slide is unreadable, the script prints `⚠` warnings
3. **Open PPTX** — for image issues or layout problems, open the PPTX in Keynote/PowerPoint to verify the render
4. **Re-export** — if visual quality is wrong, diagnose the root cause in the HTML before re-running

## Works with any HTML

Designed to work with output from:
- **kai-slide-creator** — HTML presentations with `.slide` elements
- **kai-report-creator** — Single-page HTML reports
- Any self-contained HTML file
