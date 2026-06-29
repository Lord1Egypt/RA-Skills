# md-pdf-report

> **English** | **[简体中文](./README.zh-CN.md)**

Convert Markdown research reports into styled PDFs, with auto-delivery to chat.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](md2pdf.py)
[![weasyprint](https://img.shields.io/badge/engine-weasyprint-purple.svg)](references/pdf-engine-comparison.md)
[![CJK](https://img.shields.io/badge/CJK-native%20support-red.svg)](references/macos-cjk-fonts.md)
[![Skill](https://img.shields.io/badge/Agent-Skill-orange.svg)](./SKILL.md)

---

## What It Does

Stops the loop where an AI agent writes a long Markdown report, then can't actually get a PDF to the user on a different device.

**md-pdf-report** turns a single `.md` file into:

1. **`.pdf`** — styled, paginated, with native CJK fonts (no garbled boxes)
2. **Both files sent to your chat** via the `MEDIA:` protocol, so you can download on phone, tablet, or any other device

The Markdown stays editable and the PDF is auto-generated. No content drift between the two.

```bash
# One-liner
python3 md2pdf.py report.md
# → report.pdf
# → + MEDIA: report.pdf  + MEDIA: report.md  (auto-sent to your chat)
```

---

## Why Use It

| | Without md-pdf-report | With md-pdf-report |
|---|---|---|
| **Source of truth** | Agent has only local `.md` | Single `.md`, PDF derived |
| **PDF generation** | Manual screenshot, base64 paste, or "file is at `/tmp/x.pdf`" (you can't open it) | One command, both files delivered |
| **Cross-device** | ❌ Local paths don't work on your phone | ✅ Chat attachment, downloadable anywhere |
| **Chinese fonts** | Garbled boxes / `libgobject` errors | Native CJK rendering, auto-bootstrap |
| **File size** | 5-15 MB if LaTeX path | 2-3 MB/page (weasyprint) |
| **Style control** | ✍️ ParagraphStyle API hell | Clean CSS, easy to customize |

---

## Use Cases

| Scenario | Fit | Why |
|----------|-----|-----|
| Research / fact-check / investigation report | ✅ Perfect | Long-form analysis with tables, sources, callouts |
| Scheme / plan / technical proposal | ✅ Perfect | Multi-section structure with warnings and notes |
| Investment memo / on-chain research | ✅ Perfect | Mixed CJK + English, source links |
| 调研报告 / 方案 / 链上分析 | ✅ Perfect | 原生中文，CJK 字体无需配置 |
| Resume / portfolio / one-pager | ❌ Use `kami` | Branded design, single-page layout |
| Slides / PPT / deck | ❌ Use `kami` | Different output format |
| Short message / notification | ❌ Don't | Just text is fine |
| PNG / image export | ❌ Different | Use image generation tools |

---

## Trigger Keywords

The skill fires automatically on natural user intent. No need to say the skill name.

**English:** `output as PDF`, `convert to PDF`, `save as PDF`, `export PDF`, `PDF version`, `give me a PDF`, `make a PDF`, `as a PDF`

**中文:** `输出 PDF`, `导出 PDF`, `转成 PDF`, `转为 PDF`, `转换成 PDF`, `做成 PDF`, `弄个 PDF`, `做个 PDF`, `整理成 PDF`, `保存成 PDF`, `存为 PDF`, `以 PDF 格式输出`, `以 PDF 格式`, `PDF 格式`, `PDF 版本`, `给我 PDF`, `给个 PDF`, `整个 PDF`, `来个 PDF`

**Strong triggers** (always fires): any of the above alone, or any of them paired with content types like `调研`, `报告`, `方案`, `fact-check`, `事实核查`, `链上调研`, `投资分析`, `对比分析`.

---

## Quick Start

### Install

```bash
# Option 1: clawhub (recommended)
npx clawhub@latest install 0xcjl/md-pdf-report

# Option 2: manual
git clone https://github.com/0xcjl/md-pdf-report.git
ln -sf $(pwd)/md-pdf-report ~/.hermes/skills/md-pdf-report  # or ~/.openclaw/skills/
pip install weasyprint markdown
```

### One-time macOS setup (weasyprint C dependencies)

```bash
brew install pango
```

`md2pdf.py` auto-bootstraps the library path on import. No env vars to set.

### Use

In your agent chat, say **"输出 PDF"** or **"convert to PDF"** with your report. Done.

Or as a CLI:

```bash
python3 md2pdf.py report.md              # → report.pdf
python3 md2pdf.py report.md -o out.pdf   # custom output
python3 md2pdf.py report.md --keep-html  # debug: also save report.html
```

---

## Example: MD in, PDF + Chat out

**Input** — a Markdown file with table, callout, and Chinese text:

```markdown
# 调研报告：某项目

## 核心结论

<div class="callout">

**关键发现：** 该项目 30 天活跃用户下降 47%。

</div>

| 指标 | Q1 | Q2 | 变化 |
|------|----|----|------|
| DAU  | 12k | 6.3k | -47% |
| 留存 | 68% | 41% | -27pp |
```

**Output** — a 3-page styled PDF, with:
- Centered title
- Red-bordered callout box for the key finding
- Striped table
- Page footer with `1 / 3` pagination
- Native Chinese rendering (no boxes)

**Delivery** — your agent automatically sends:

```
✅ PDF:  MEDIA:/path/to/report.pdf
✅ MD:   MEDIA:/path/to/report.md
```

You can download both on phone, tablet, or desktop.

---

## Architecture

```
md-pdf-report/
├── SKILL.md                          # Skill definition (Chinese, for agent)
├── README.md                         # English (this file)
├── README.zh-CN.md                   # Chinese
├── md2pdf.py                         # Main module — weasyprint + bootstrap
├── references/
│   ├── pdf-engine-comparison.md      # Why weasyprint over reportlab/pandoc
│   ├── macos-cjk-fonts.md            # .ttc vs .ttf, working font paths
│   └── weasyprint-bootstrap.md       # Fix for "cannot load libgobject"
├── templates/
│   ├── fact-check.md                 # Claim → verification → context scaffold
│   ├── research-report.md            # Analytical report scaffold
│   └── scheme.md                     # Proposal / plan scaffold
├── examples/
│   ├── test_report.md                # Minimal feature test
│   └── Mike_Lynch_FactCheck.md       # Real 7-page fact-check example
├── LICENSE                           # MIT
└── .gitignore
```

See [references/pdf-engine-comparison.md](references/pdf-engine-comparison.md) for the full engine decision matrix. See [references/macos-cjk-fonts.md](references/macos-cjk-fonts.md) for the macOS font path saga.

---

## Custom Markdown Extensions

Standard GitHub-flavored Markdown works out of the box. Three custom `<div>` classes add styled callouts:

```html
<div class="callout">  <!-- red border, light red bg, key conclusions -->
<div class="note">     <!-- gray border, light gray bg, supplementary info -->
<div class="warn">     <!-- yellow border, light yellow bg, caution -->
```

See `templates/` for ready-to-use scaffolds (fact-check, research-report, scheme).

---

## Verified Output

The `examples/Mike_Lynch_FactCheck.md` (14 KB Markdown) produces a 7-page A4 PDF with 1,951 correctly-rendered Chinese characters, 36 source links, and 5 styled callout boxes. Final size 2.4 MB.

```bash
python3 md2pdf.py examples/Mike_Lynch_FactCheck.md
# → examples/Mike_Lynch_FactCheck.pdf (7 pages, 2.4 MB)
```

---

## Customization

### Custom CSS

```python
from md2pdf import md_to_pdf, DEFAULT_CSS
md_to_pdf("report.md", css=DEFAULT_CSS + """
    h1 { color: #B91C1C; }  /* brand red */
    .callout { background: #FEFCE8; border-color: #FACC15; }
""")
```

### Custom fonts

Edit `md2pdf.py` top-of-file `FONT_BODY` / `FONT_HEADING` / `FONT_KAITI` constants. See `references/macos-cjk-fonts.md` for the verified macOS font paths.

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `cannot load library 'libgobject-2.0-0'` | pango not installed | `brew install pango` |
| Garbled Chinese (boxes) | Wrong font path | `find /System/Library/AssetsV2 -name "STXIHEI.ttf"` |
| `TTFError: postscript outlines are not supported` | Trying to use `.ttc` | Use `.ttf` paths from `references/macos-cjk-fonts.md` |
| PDF > 5 MB | Full fonts embedded | Use `pyftsubset` to subset fonts (advanced) |

Full troubleshooting in `references/weasyprint-bootstrap.md`.

---

## Credits

- **Concept & implementation**: [0xcjl](https://github.com/0xcjl)
- **CJK font discovery**: macOS `.ttc` files have PostScript outlines that Python font libraries can't load → `.ttf` files in `/System/Library/AssetsV2/` work. Documented in `references/macos-cjk-fonts.md`.
- **weasyprint bootstrap pattern**: Common need across CJK-on-macOS projects. `md2pdf.py` does it transparently.
- **Trigger keyword design**: Natural-language-first philosophy, inspired by [`kami`](https://github.com/0xcjl/kami) skill (also by 0xcjl).
- **Real-world test case**: Mike Lynch / Bayesian yacht fact-check report (2026-06-11), published in Hermes DM channel as full MD → PDF → chat-delivery pipeline demo.

---

## License

MIT
