---
name: paper-to-slides
description: End-to-end academic paper analysis and presentation generation. Use when a user provides a PDF paper (local path or arXiv URL) and wants (1) a deep research report (dual-mode Part A + Part B), (2) an HTML slide deck for group meeting / seminar / conference talk, or (3) both. Triggers on "read this paper and make slides", "parse this paper into a presentation", "论文研读+做PPT", "解析论文做成slides", or any request combining paper analysis with presentation output. Supports arXiv links (abs/pdf), DOI URLs, and direct PDF URLs.
---

# Paper to Slides

Two-phase pipeline: **Phase 1** deep-reads an academic paper into a structured dual-mode report, **Phase 2** transforms the report into a polished, zero-dependency HTML presentation.

## Dependencies

- `pdftotext` (from poppler) — install via `brew install poppler` or `apt install poppler-utils` if missing
- Google Fonts (loaded via CDN in the generated HTML)

## Phase 1: Paper Deep-Read

### Step 1.0 — Resolve input source

Determine the input type and obtain a local PDF:

| Input | Action |
|-------|--------|
| Local path (`/path/to/paper.pdf`) | Use directly |
| arXiv abs URL (`https://arxiv.org/abs/2603.02096`) | Convert to `https://arxiv.org/pdf/2603.02096` and download |
| arXiv PDF URL (`https://arxiv.org/pdf/2603.02096`) | Download directly |
| Other PDF URL | Download directly |

**Download command:**
```bash
curl -L -o /tmp/paper.pdf "<pdf_url>"
```

Use the arXiv ID or paper title as the filename when possible (e.g., `/tmp/2603.02096_FluxMem.pdf`).

### Step 1.1 — Extract full text

```bash
pdftotext "<paper.pdf>" /tmp/paper_text.txt
```

Read the extracted text completely. For papers with critical figures, try extracting key pages as images via `pdftoppm` and analyzing them with the image tool.

### Step 1.2 — Comprehensive analysis

Create `temp_analysis.md` extracting:

- Research question, hypotheses, methodology, data sources
- Core findings with key quantitative results
- Theoretical contributions and practical implications
- The paper's fundamental contradiction/gap, novel angle, and method innovation

This step is mandatory — it ensures report quality through structured thinking.

### Step 1.3 — Write dual-mode report

Generate `[PaperName]_研读报告.md` containing both parts separated by `---`:

- **Part A** — Read [part-a-template.md](prompts/part-a-template.md) before writing. Deep academic report: structured abstract → introduction → methodology → results → discussion → conclusion → core references.
- **Part B** — Read [part-b-template.md](prompts/part-b-template.md) before writing. Core logic extraction: four key elements table → method formula → one-line summary (expert + layperson versions).

**Writing standards**: Use complete paragraphs over bullet lists. Provide bilingual terms (中英) on first mention. Support every claim with specific data from the paper.

### Step 1.4 — Deliver report

Present the report file and briefly summarize the paper's core innovation, key findings, and theoretical value.

## Phase 2: Slides Generation

If the user only requested a report, stop after Phase 1.

### Step 2.0 — Confirm parameters

Ask the user (all at once):

1. **Purpose**: 组会汇报 / 学术会议 / 教学 / 其他
2. **Length**: Short (5-10) / Medium (10-20) / Long (20+)
3. **Theme**: 亮色 / 暗色 / 偏好的风格
4. **Editing**: 是否需要浏览器内编辑功能

If the user already specified these in the initial request, skip asking and proceed.

### Step 2.1 — Choose style

Select an appropriate style based on user preferences. Read [slide-styles.md](prompts/slide-styles.md) for available presets and CSS specifications. Academic presentations generally suit Swiss Modern (light), Notebook Tabs (light), or Bold Signal (dark).

### Step 2.2 — Plan slide outline

Map the report content to a slide structure. Typical academic paper outline (15-19 slides):

| Section | Slides | Content |
|---------|--------|---------|
| Title | 1 | Paper title, authors, affiliations, date |
| Problem | 1-2 | Background, existing gaps, key insight |
| Method (divider) | 1 | Section divider slide |
| Method details | 3-5 | Core modules, formulas, architecture |
| Results (divider) | 1 | Section divider slide |
| Quantitative results | 2-3 | Main results tables, metrics, comparisons |
| Efficiency / Ablation | 1-2 | Efficiency gains, ablation studies |
| Discussion (divider) | 1 | Section divider slide |
| Advantages & Limitations | 1-2 | Key properties, future directions |
| Summary | 1 | One-line takeaway |
| Thanks | 1 | Links, navigation hints |

### Step 2.3 — Generate HTML

Read [slide-template.md](prompts/slide-template.md) for the mandatory HTML architecture, viewport CSS, JS controller, and inline editing implementation.

**Non-negotiable rules**:
- Single self-contained HTML file, all CSS/JS inline
- Every `.slide` must have `height: 100vh; height: 100dvh; overflow: hidden`
- ALL font sizes and spacing must use `clamp()` — never fixed px/rem
- Load fonts from Google Fonts or Fontshare — never system fonts
- Include `prefers-reduced-motion` support
- Max content per slide: 1 heading + 4-6 bullets OR 1 heading + 2 paragraphs. Overflow → split slides.

**If inline editing is enabled**, implement via `contentEditable` API + `localStorage` persistence. Use JS-based hover with 400ms delay for the edit button (not CSS `~` sibling selector — it breaks due to pointer-events). See the template for the complete implementation.

### Step 2.4 — Open and deliver

```bash
open [filename].html
```

Tell the user: file location, slide count, navigation (arrow keys / space / dots), and editing instructions (press E) if enabled.

## Both Phases Together

When the user requests both report and slides, run Phase 1 fully first, then Phase 2. The report serves as the structured source for slide content — do not re-analyze the paper.
