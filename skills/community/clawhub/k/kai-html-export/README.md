# kai-html-export

English | [简体中文](README.zh-CN.md)

> Export any HTML file to PPTX or PNG, or publish it to a public URL — works with kai-slide-creator, kai-report-creator, or any self-contained HTML.

A Claude Code skill that converts HTML files into portable formats using a headless browser. PPTX/PNG export needs no Node.js and uses your existing system Chrome; the optional URL-sharing helper uses Cloudflare Pages by default and keeps Vercel as a fallback.

**v1.2.0** — Added a unified `share-html.py` entrypoint, made Cloudflare Pages the default share target, kept Vercel as a fallback, and disabled automatic sharing in hosted cloud sandboxes with manual-share guidance. **v1.1.7** — Two native mode image fixes: (1) images wrapped in transparent-background animation divs (e.g. `kd-reveal`, fade-in wrappers) were silently skipped by the decorative-blob filter — fixed by checking for child raster elements before skipping; (2) `object-fit: contain` and `fill` images were falling back to the Playwright screenshot path (which failed silently) — fixed by handling them directly in `_download_img_direct` without cropping. Both issues caused content images to disappear from native PPTX exports when slides used CSS animation wrappers around `<img>` elements. **v1.1.6** — Four improvements borrowed from the Anthropic PPTX skill: post-export preview grid; structural PPTX validation; sandbox-safe browser launch; QA process documented.

---

## Install

### Claude Code

```bash
git clone https://github.com/kaisersong/kai-html-export ~/.claude/skills/kai-html-export
pip install playwright python-pptx beautifulsoup4 lxml
```

### OpenClaw / ClawHub

```bash
clawhub install kai-html-export
```

> ClawHub page: https://clawhub.ai/skills/kai-html-export

Dependencies are installed automatically by OpenClaw on first use.

---

## Usage

```
/kai-html-export [file.html]                    # PPTX (image mode, default)
/kai-html-export --pptx [file.html]             # Explicit PPTX export
/kai-html-export --pptx --mode native [file]    # Editable PPTX (native mode)
/kai-html-export --png [file.html]              # Full-page screenshot to PNG
/kai-html-export --png --scale 2                # 2× retina-quality PNG
python scripts/share-html.py [file.html|folder]     # Optional: Share HTML to URL (Cloudflare default)
python scripts/share-html.py --provider vercel [file.html|folder]
```

If no file is specified, the most recently modified `.html` in the current directory is used.

---

## Export Modes

### Image Mode (default)

Captures each slide as a pixel-perfect screenshot and assembles them into a PowerPoint file. Text is rasterized — not editable, but visually identical to the browser.

```bash
/kai-html-export presentation.html
# → presentation.pptx  (16:9, 1440×900)
```

| | Image Mode |
|--|--|
| Visual fidelity | ⭐⭐⭐⭐⭐ pixel-perfect |
| Text editable | ❌ rasterized |
| Best for | sharing, archiving final decks |

---

### Native Mode — Editable PPTX

Reconstructs each slide as real PowerPoint shapes, text boxes, and tables. Text is fully editable in Keynote and PowerPoint.

```bash
/kai-html-export --pptx --mode native presentation.html
# → presentation.pptx  (editable text, shapes, tables)
```

| | Native Mode |
|--|--|
| Visual fidelity | ⭐⭐⭐ simplified |
| Text editable | ✅ full text editing |
| Best for | editing content, translating, repurposing slides |

#### What native mode renders

| Element | Support |
|---------|---------|
| Headings, paragraphs, lists | ✅ with font size, color, bold, alignment |
| Inline text styles | ✅ bold, italic, strikethrough, color |
| Inline background highlights | ✅ `<span style="background:…">` → colored shape behind text |
| Solid-color shapes (div with background) | ✅ rectangles with fill |
| Tables | ✅ editable cells with borders |
| Images (`<img>`, `canvas`, CSS `background-image`) | ✅ inserted as raster layers |
| SVG graphics | ✅ rasterized to PNG and embedded |
| Grid / dot / noise backgrounds | ✅ auto-detected and rendered |
| `position:fixed` nav dots + progress bars | ✅ per-slide state computed from slide index; set `data-export-progress="false"` on `<body>` to suppress both |

#### What native mode approximates or skips

| Element | Behavior |
|---------|---------|
| CSS gradients | → solid color (average of gradient stops) |
| Box shadows | → omitted |
| Custom web fonts (e.g. Barlow, Inter) | → nearest system font |
| Unsupported DOM / CSS edge cases | → skipped safely instead of crashing the export |

#### CJK (Chinese / Japanese / Korean) compensation

PingFang SC and other CJK fonts render ~15% wider and ~30% taller in Keynote/PowerPoint than in Chrome. Native mode automatically compensates:

- Text boxes with CJK content are widened by ×1.15
- Condensed font containers (Barlow Condensed, etc.) are widened by ×1.30
- Width expansion only applies to boxes narrower than 3 inches (prevents wide containers from overflowing)
- CJK system font mapping prefers Microsoft YaHei on Windows so exported PPTs do not fall back to Calibri
- Inline background shapes use PPTX coordinate system (not Chrome coordinates) to stay aligned with text

---

## Export to PNG

Captures the full rendered page as a PNG — useful for sharing reports or single-page HTML as images.

```bash
/kai-html-export --png report.html
# → report.png

# 2× resolution for retina / messaging apps
/kai-html-export --png report.html --scale 2
```

---

## Share HTML to URL

Publish a generated deck or report and get back a live URL:

```bash
python scripts/share-html.py presentation.html
python scripts/share-html.py ./my-html-folder
python scripts/share-html.py --provider vercel presentation.html
```

- Accepts a single HTML file or a folder with `index.html`
- Copies common relative assets automatically when starting from one file
- Defaults to Cloudflare Pages because Cloudflare is generally more reachable from China
- Keeps Vercel as an optional fallback provider
- Uses runtime CLIs only; the repo does not add new install-time dependencies
- In hosted cloud sandboxes, automatic sharing is disabled and the helper prints manual-share guidance instead of starting login or deploy flows

For local Cloudflare publishing:

```bash
wrangler login
```

For local Vercel publishing:

```bash
npx vercel login
```

---

## Requirements

| Dependency | Purpose | Auto-installed (OpenClaw) |
|-----------|---------|--------------------------|
| Python 3 + `playwright` | Headless browser screenshots | ✅ via uv |
| Python 3 + `python-pptx` | Assemble PPTX | ✅ via uv |
| `beautifulsoup4` + `lxml` | HTML parsing (native mode) | ✅ via uv |
| Node.js + Wrangler / Vercel CLI | Optional live URL publishing | ❌ manual |

**Browser:** Uses system Chrome, Edge, or Brave first — no 300MB Chromium download. Falls back to Playwright Chromium if no system browser is found.

**Claude Code users** — install manually:
```bash
pip install playwright python-pptx beautifulsoup4 lxml
```

For optional URL publishing with Cloudflare:
```bash
wrangler login
```

For optional URL publishing with Vercel:
```bash
npx vercel login
```

---

## Use Case: Brand Style Migration

Migrate an existing `.pptx` to a custom brand design system — get both a pixel-perfect archive and an editable version in one workflow.

**Setup:** Create `themes/your-brand/` with a `reference.md` describing colors, fonts, and layouts (and optionally a `starter.html` for complex visual systems).

```bash
# Step 1 — re-style: slide-creator reads the PPTX and migrates to your brand theme
/slide-creator --plan "migrate company-deck.pptx to our brand style"
# review PLANNING.md, then:
/slide-creator --generate
# → branded-deck.html

# Step 2 — export both modes
/kai-html-export branded-deck.html
# → branded-deck.pptx  (pixel-perfect, for sharing)

/kai-html-export --pptx --mode native branded-deck.html
# → branded-deck.pptx  (editable text, for editing)
```

This workflow is especially useful when an internal template or brand guidelines exist as a `starter.html` — slide-creator uses it as the base and fills in content from the source PPTX.

---

## Works With

| Skill | Output | Export format |
|-------|--------|--------------|
| [kai-slide-creator](https://github.com/kaisersong/slide-creator) | HTML presentation with `.slide` elements | PPTX (slide-by-slide) |
| [kai-report-creator](https://github.com/kaisersong/kai-report-creator) | Single-page HTML report | PNG (full page) |
| Any HTML file | Self-contained HTML | PPTX or PNG |

---

## Compatibility

| Platform | Version | Install path |
|---------|---------|-------------|
| Claude Code | any | `~/.claude/skills/kai-html-export/` |
| OpenClaw | ≥ 0.9 | `~/.openclaw/skills/kai-html-export/` |

---

## License

MIT
