# 📜 Papyrus

> Turn arXiv papers into bilingual, beautifully formatted, annotation-rich PDFs.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green)](https://python.org)
[![Version](https://img.shields.io/badge/version-v0.2.1-lightgrey)](https://github.com/ZaneChen76/papyrus/releases)
[![Platforms](https://img.shields.io/badge/platforms-OpenClaw%20%7C%20Claude%20Code%20%7C%20Codex%20%7C%20Hermes%20%7C%20Open%20Code-green)]()

Papyrus (莎草纸) transforms academic papers into deep-read study documents. Given a paper URL, it produces a single PDF containing the original English text, paragraph-by-paragraph Chinese translation, expert commentary, all figures and formulas — typeset with professional Kami-inspired design.

---

## ✨ What You Get

| Feature | Description |
|---------|-------------|
| Original text preserved | Exact English wording, figures, tables, equations |
| Chinese translation | Paragraph-by-paragraph, accurate and idiomatic |
| Expert commentary | Technical insights, historical context, design rationale |
| Crisp formulas | LaTeX rendered at 150 DPI via codecogs, zero blur |
| Visible formula wireframes | Clean border + background for each equation block |
| Professional typesetting | Kami design system — 10pt MingLiU + Times New Roman |
| Appendix figures | All attention visualizations and supplementary charts |

## 🚀 Quick Start

```bash
# CLI entry point
./SCRIPTS/run.sh --paper https://arxiv.org/abs/1706.03762 \
    --title "Attention Is All You Need — 逐段精读"
```

The pipeline:
1. **Fetch** — Downloads arXiv LaTeX source
2. **Render** — Converts LaTeX formulas to PNG via codecogs.com
3. **Build** — Constructs annotated bilingual HTML (LLM-assisted)
4. **Export** — WeasyPrint HTML → PDF

> ⚠️ Steps 2 (formula identification) and 3 (translation/commentary) require LLM assistance. Papyrus provides the scaffolding; the LLM fills in content following `SOP.md`.

## 🤖 Agent Platform Support

Papyrus v0.2.0 ships with adapters for major AI coding agents:

| Platform | Config | How to Install |
|----------|--------|---------------|
| **OpenClaw** | `SKILL.md` (auto-loaded) | Already installed at `~/.openclaw/skills/papyrus/` |
| **Claude Code** | `platforms/claude-code/papyrus-skill.md` | Copy to `.claude/skills/` |
| **Codex** | `platforms/codex/papyrus-tool.yaml` | Copy to `.codex/tools/` |
| **Hermes** | `platforms/hermes/papyrus-tool.py` | Copy to `hermes/tools/` |
| **Open Code** | `platforms/open-code/papyrus-config.yaml` | Copy to `.open-code/` |

All platforms invoke the same unified CLI (`SCRIPTS/papyrus`) with four commands: `fetch`, `figures`, `formulas`, `pdf`.

## 📁 Structure

```
papyrus/
├── SKILL.md              # Skill definition and design decisions
├── SOP.md                # Standard Operating Procedure (mandatory)
├── README.md             # You are here
├── LICENSE               # MIT
├── SCRIPTS/
│   ├── run.sh            # Main entry point
│   ├── fetch_arxiv.sh    # Download arXiv LaTeX source
│   ├── render_formulas.sh # Render LaTeX → PNG
│   ├── build_html.py     # Build annotated HTML skeleton
│   └── build_pdf.sh      # HTML → PDF via WeasyPrint
├── TEMPLATES/
│   └── paper.html        # Kami-styled HTML template
└── PROMPTS/
    └── qc_checklist.md    # Three-round quality control
```

## 🔧 Dependencies

- **Python 3.10+** — `weasyprint`, `pypdf`, `Pillow`, `requests`
- **bash** — standard Unix tools
- **Option A** (recommended): local LaTeX engine (`pdflatex` from texlive or basictex)
- **Option B** (backup): internet access for codecogs.com formula rendering

Install Python dependencies:
```bash
pip3 install weasyprint pypdf Pillow requests
```

For best results, install a lightweight LaTeX distribution:
```bash
# macOS
brew install --cask basictex

# Ubuntu/Debian
apt install texlive-latex-base texlive-latex-extra
```

## 🎨 Design Philosophy

- **No scaling, no blur.** Formula images use native 150 DPI resolution with `max-width:100%; height:auto`. Never upscale.
- **Visible structure.** Formula blocks have a wireframe box to visually separate math from text.
- **Three-layer depth.** Each paragraph: original English → Chinese translation → expert commentary.
- **Defensive figure mapping.** Always verify figure-to-file mapping from arXiv HTML source. Never guess.

## 📚 Example Output

See `examples/` for a complete output: "Attention Is All You Need — Annotated Deep-Read" (38 pages, bilingual, 7 formulas, 5 figures).

## 🤝 Contributing

Found a rendering bug? Have a paper that Papyrus struggles with? Open an issue with:
1. The paper URL
2. A description of the problem
3. Screenshots of the issue

## 📄 License

MIT — see [LICENSE](LICENSE).

---

*Papyrus was born from the observation that reading academic papers shouldn't require fighting with layout engines. One session with "Attention Is All You Need" produced enough learnings to codify the entire pipeline.*

---

## 🎨 Credits

The visual design system (warm parchment background, ink-blue accent, serif-led typographic scale) is adapted from the **[Kami](https://docs.openclaw.ai)** design language, part of the OpenClaw skills ecosystem.

Kami's design tokens (colors, spacing, font stacks, wireframe patterns) are used under the same MIT license.
