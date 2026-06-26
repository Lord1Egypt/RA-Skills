# Papyrus — Academic Paper Deep-Read Skill

> Skill for Claude Code. Copy this file to `.claude/skills/papyrus.md`

## Description

Turn arXiv papers into bilingual, deeply annotated, professionally typeset PDFs. Papyrus fetches paper source, converts figures, renders formulas, and builds a Kami-styled PDF with English original + Chinese translation + expert commentary.

## When to Use

- User asks to "deep-read" or "annotate" an academic paper
- User provides an arXiv URL and wants a study guide
- User asks for a paper's content with translation and interpretation
- User mentions "papyrus", "paper deep-read", or "论文详读"

## How to Invoke

Papyrus is installed at `$PAPYRUS_HOME` (typically `~/.openclaw/skills/papyrus`). Use the unified CLI:

```bash
PAPYRUS_HOME="${PAPYRUS_HOME:-$HOME/.openclaw/skills/papyrus}"
PAPYRUS="$PAPYRUS_HOME/SCRIPTS/papyrus"
```

### Step-by-step pipeline:

1. **Fetch paper source:**
   ```bash
   $PAPYRUS fetch https://arxiv.org/abs/XXXX.NNNNN /tmp/papyrus_work
   ```

2. **Convert PDF figures to PNG:**
   ```bash
   $PAPYRUS figures /tmp/papyrus_work/figures /tmp/papyrus_work/png_figures
   ```

3. **Write formula definitions** to `/tmp/papyrus_work/formulas.txt`:
   ```
   @name=formula1
   \displaystyle \mathrm{Attention}(Q,K,V) = ...
   ```

4. **Render formulas:**
   ```bash
   $PAPYRUS formulas /tmp/papyrus_work/formulas.txt /tmp/papyrus_work/rendered_formulas
   ```

5. **Build annotated HTML** — use the template at `$PAPYRUS_HOME/TEMPLATES/paper.html`. Follow SOP at `$PAPYRUS_HOME/SOP.md` for figure mapping and commentary quality.

6. **Generate PDF:**
   ```bash
   $PAPYRUS pdf /tmp/papyrus_work/annotated.html /tmp/papyrus_work/output.pdf
   ```

## Dependencies

- Python: `weasyprint`, `pypdf`, `PyMuPDF`, `Pillow`, `requests`
- Optional: `pdflatex` for local formula rendering (falls back to codecogs.com)

## Key Rules

- **Never guess figure mapping** — always verify from arXiv HTML source
- **Never upscale formula images** — use `max-width:100%; height:auto` at native resolution
- **Commentary must be web-researched** — search for quality interpretations before writing
- **Three rounds of QC** — see `PROMPTS/qc_checklist.md`

## Output

A single PDF with:
- Bilingual cover page (title, authors, abstract)
- Body text: EN original → CN translation → expert commentary
- All figures with bilingual captions
- All formulas as crisp LaTeX-rendered PNGs
- Epilogue with key takeaways
