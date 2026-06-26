# Papyrus — Academic Paper Deep-Read Skill v0.2.1

> Turn arXiv papers into bilingual, beautifully formatted, annotation-rich PDFs.
> Now with support for OpenClaw, Claude Code, Codex, Hermes, and Open Code.

## Identity

**Papyrus** (莎草纸) transforms academic papers into deep-read study documents. Input a paper (arXiv URL or local PDF), output a PDF with:

- **Original text preserved** — exact English wording, figures, tables, equations
- **Chinese translation** — paragraph-by-paragraph, accurate and readable
- **Expert commentary** — technical insights, historical context, design rationale
- **Professional typesetting** — Kami-inspired design, visible formula wireframes, proper fonts

## Prerequisites

- Python 3.10+ with `weasyprint`, `pypdf`, `Pillow`, `requests`
- Node.js (for KaTeX fallback)
- Internet access (for codecogs.com formula rendering and arXiv downloads)

## Quick Start

```bash
# Unified CLI (works from any agent platform)
papyrus fetch https://arxiv.org/abs/1706.03762 /tmp/papyrus_work
papyrus figures /tmp/papyrus_work/figures /tmp/papyrus_work/figures_png
papyrus formulas /tmp/papyrus_work/formulas.txt /tmp/papyrus_work/formulas
papyrus pdf /tmp/papyrus_work/annotated.html output.pdf

# Agent platform integration: copy the appropriate config
cp platforms/claude-code/papyrus-skill.md .claude/skills/
cp platforms/codex/papyrus-tool.yaml .codex/tools/
cp platforms/hermes/papyrus-tool.py hermes/tools/
cp platforms/open-code/papyrus-config.yaml .open-code/

## Output

A single PDF containing:
1. Cover page with title, authors, abstract (bilingual)
2. Body text in bilingual blocks (English → Chinese → Commentary)
3. **Commentary enriched by web research**: LLM searches for quality paper interpretations (blog posts, lectures, citation papers, community discussions), synthesizes with its own understanding — delivering true "deep-read" quality, not surface-level translation
4. All original figures with translated captions
5. All formulas rendered as crisp LaTeX PNGs from codecogs
6. Tables with bilingual headers
7. Appendix figures (if any)
8. Epilogue with key takeaways

## Design System

- **Body**: 10pt MingLiU / Times New Roman
- **Accent**: #1B365D (ink blue), #f5f4ed (warm parchment)
- **Formula wireframe**: 1pt #d0dce9 border, rounded corners, light background
- **Page**: A4, 20mm margins

## Directory Structure

```
papyrus/
├── SKILL.md           ← You are here
├── SOP.md             ← Standard Operating Procedure (mandatory steps)
├── README.md          ← GitHub project README
├── SCRIPTS/
│   ├── run.sh         ← Main entry point
│   ├── fetch_arxiv.sh ← Download arXiv source (tar.gz)
│   ├── render_formulas.sh ← Render LaTeX → PNG (local TeX → codecogs)
│   ├── render_figures.sh  ← Convert PDF figures → PNG (PyMuPDF)
│   ├── build_html.py  ← Build annotated bilingual HTML
│   └── build_pdf.sh   ← HTML → WeasyPrint PDF
├── TEMPLATES/
│   └── paper.html     ← Base HTML template (Kami design system)
└── platforms/          ← Agent platform adapter configs
    ├── openclaw/       ← OpenClaw native config (auto-loaded)
    ├── claude-code/    ← Claude Code skill definition
    ├── codex/          ← OpenAI Codex YAML tool definition
    ├── hermes/         ← Hermes Python tool module
    └── open-code/      ← Google Open Code YAML config
└── PROMPTS/
    └── qc_checklist.md ← Three-round quality control checklist
```

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Formula rendering: local TeX → PNG, fallback to codecogs PNG @ `\dpi{150}` | Best quality when LaTeX available; internet-free fallback |
| Images: `max-width:100%; height:auto` | Never upscale; avoids blur from LANCZOS enlarging |
| Formula wireframe: visible border | User-requested: visually distinguishes formulas from text |
| Bilingual blocks: EN→CN→Commentary | Three-layer depth progressively builds understanding |
| Font: MingLiU for CN, Times New Roman for EN | Academic, readable, widely available on macOS/Windows |

## Known Limitations

- **Offline mode requires local LaTeX** — without `pdflatex`, formulas fall back to codecogs.com (internet required)
- **Vector PDF figures need PyMuPDF** — `fitz` rasterizes vector figures to PNG for WeasyPrint (auto-detected)
- **Commentary quality depends on LLM + web research** — deeper commentary requires iterative search across multiple sources
- Font availability varies by OS → fallback chain: MingLiU → LiSong Pro → SimSun → Songti SC
- arXiv source must be downloadable (no paywalled papers)
