**English** | [中文](README_zh.md)

# Paper to Slides

An AI skill that deep-reads academic papers and turns them into polished HTML presentations — give it a PDF or arXiv link, get back a structured research report and a ready-to-present slide deck.

**Philosophy:** Reading a paper should produce reusable artifacts, not just understanding. A single command gives you both a deep analysis and presentation-ready output.

## What You Get

Give the skill a paper (local PDF, arXiv link, or any PDF URL), and it produces:

- **Research Report** — A dual-mode deep-read: Part A is a full academic analysis (structured abstract → methodology → results → discussion), Part B distills the core logic chain into a one-line summary
- **HTML Slide Deck** — A zero-dependency, animated presentation with 10 style presets, browser-based inline editing, and responsive design that works on any screen

You can request either output alone or both together.

## Quick Start

1. Install the skill in your agent (OpenClaw or Claude Code)
2. Say "read this paper and make slides" with a PDF path or arXiv link
3. The agent handles everything — extraction, analysis, style selection, generation

```
解析 https://arxiv.org/abs/2603.02096，组会汇报，亮色，15页左右
```

```
Deep-read /path/to/paper.pdf, generate report and slides, dark theme
```

The agent will ask about slide preferences (length, theme, editing) if not specified. Or provide them upfront to skip the questions.

## Style Gallery

10 built-in style presets. [Open live preview →](style-preview.html)

### Light Themes

| Swiss Modern ⭐ | Notebook Tabs | Pastel Geometry |
|:---:|:---:|:---:|
| ![Swiss Modern](style-examples/swiss-modern.png) | ![Notebook Tabs](style-examples/notebook-tabs.png) | ![Pastel Geometry](style-examples/pastel-geometry.png) |
| Clean, precise, academic | Editorial, organized, tactile | Friendly, approachable |

| Split Pastel | Vintage Editorial | Paper & Ink |
|:---:|:---:|:---:|
| ![Split Pastel](style-examples/split-pastel.png) | ![Vintage Editorial](style-examples/vintage-editorial.png) | ![Paper & Ink](style-examples/paper-ink.png) |
| Playful, creative, dual-tone | Witty, confident, retro | Literary, thoughtful |

### Dark Themes

| Bold Signal | Neon Cyber | Dark Botanical | Terminal Green |
|:---:|:---:|:---:|:---:|
| ![Bold Signal](style-examples/bold-signal.png) | ![Neon Cyber](style-examples/neon-cyber.png) | ![Dark Botanical](style-examples/dark-botanical.png) | ![Terminal Green](style-examples/terminal-green.png) |
| High-impact, bold | Futuristic, techy | Elegant, artistic | Hacker aesthetic |

## Installation

### OpenClaw

```bash
# From ClawHub (coming soon)
clawhub install paper-to-slides

# Or manually
git clone https://github.com/zhangguanghao523/paper-to-slides.git ~/.openclaw/skills/paper-to-slides
```

### Claude Code

```bash
git clone https://github.com/zhangguanghao523/paper-to-slides.git ~/.claude/skills/paper-to-slides
```

### System Dependency

The skill needs `pdftotext` for PDF text extraction:

```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt install poppler-utils
```

That's it. No Python packages, no npm, no build tools. Generated slides are pure HTML with inline CSS/JS.

## Architecture

This skill uses **progressive disclosure** — the main `SKILL.md` is a concise workflow map, with supporting files loaded on-demand only when needed:

| File | Purpose | Loaded When |
|------|---------|-------------|
| `SKILL.md` | Core two-phase workflow | Always (skill invocation) |
| `prompts/part-a-template.md` | Part A deep academic report template | Phase 1 (report writing) |
| `prompts/part-b-template.md` | Part B core logic extraction template | Phase 1 (report writing) |
| `prompts/slide-styles.md` | 10 curated visual presets | Phase 2 (style selection) |
| `prompts/slide-template.md` | HTML architecture, viewport CSS, JS controller | Phase 2 (generation) |

## Built On

| Component | Role |
|-----------|------|
| [paper-parse](https://clawhub.com) | Dual-mode report templates (Part A + Part B) |
| [frontend-slides](https://github.com/zarazhangrui/frontend-slides) | Zero-dependency HTML presentation framework |
| [poppler](https://poppler.freedesktop.org/) | PDF text & figure extraction (pdftotext / pdftoppm) |

## Requirements

- An AI agent (OpenClaw, Claude Code, or similar)
- `pdftotext` (from poppler) — for PDF text extraction
- Internet connection (for arXiv downloads and Google Fonts in generated slides)

## Credits

Built with [OpenClaw](https://github.com/openclaw/openclaw). Presentation engine adapted from [frontend-slides](https://github.com/zarazhangrui/frontend-slides) by [@zarazhangrui](https://github.com/zarazhangrui). Report templates adapted from [paper-parse](https://clawhub.com).

## License

MIT — Use it, modify it, share it.
