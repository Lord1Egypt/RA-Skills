---
name: manuscript-math-docx-qc
description: Portable agent skill/playbook for OpenClaw, Hermes, Claude, Codex, and other agents revising scientific manuscripts that will be exported to DOCX/PDF, especially when mathematical formulas, subscripted variables, tables, figures, Word rendering, Pandoc conversion, LibreOffice PDF checks, or submission-package visual QC may fail.
---

# Manuscript Math, DOCX, and Visual QC

Use this skill/playbook to turn manuscript source files into Word/PDF-safe submission artifacts. It is written to be usable by OpenClaw, Hermes, Claude, Codex, and other coding or research agents. The goal is not only correct content, but correct rendering in the actual files that authors, reviewers, or journal portals will inspect.

## Agent Compatibility

This file is the authoritative workflow. Agents that do not support formal skill metadata can ignore the YAML header and follow the Markdown instructions directly.

- OpenClaw / repository-aware agents: read `AGENTS.md` first, then this file for the full workflow.
- Hermes / Claude / chat agents: treat this file as the operating checklist for manuscript DOCX/PDF QC.
- Codex-compatible skill loaders: use the `name` and `description` metadata above.

Do not assume a specific agent runtime, memory format, tool wrapper, or repository layout. Use the available shell, document, image, and file-inspection tools in the current environment.

## Maintenance Rule

Treat this skill as a living checklist. When using it on a real manuscript and discovering a reusable failure mode, formula pattern, DOCX/PDF conversion issue, figure-layout fix, table-rendering fix, or submission-package synchronization problem, update this `SKILL.md` before finishing if the lesson is likely to recur.

Only add generalizable lessons. Do not add project-specific paths, manuscript titles, private author details, transient filenames, or one-off numerical results unless they describe a reusable workflow pattern.

Good additions:

- A formula syntax that renders correctly or incorrectly in Word/PDF.
- A reproducible QC command that catches stale figures, broken DOCX archives, or clipped pages.
- A common conversion artifact from Pandoc, LibreOffice, Word, or PDF rendering.
- A source-level fix pattern for figure/table overlap.

Bad additions:

- A single manuscript's scientific conclusion.
- A temporary upload zip name.
- A local path that applies only to one project.
- A subjective writing preference already covered elsewhere.

## Core Workflow

1. Identify the authoritative source.
   - Locate the real manuscript source (`manuscript.md`, `.tex`, `.docx`) and figure/table generation scripts.
   - Do not fix screenshots or exported DOCX by hand unless no source exists.
   - Prefer reproducible edits to source Markdown/scripts, then rebuild DOCX/PDF.

2. Check formula source before judging screenshots.
   - Screenshots can reflect stale DOCX output. Inspect the current manuscript source and then rebuild.
   - Search for formula-risk patterns:
     ```bash
     rg -n "\\$\\$|\\\\\\(|\\\\\\)|\\\\frac|\\\\sum|metric|SE_|Y_\\{|w_\\{|scores\\[|weights\\[" manuscript code
     ```

3. Fix formulas for Word/Pandoc/LibreOffice rendering.
   - Use inline math for scientific variables with subscripts: `$Y_{ij}$`, `$w_{ij}$`, `$x_i$`.
   - Do not use code spans for mathematical variables in prose when subscripts matter: avoid `` `Y_ij` `` unless referring to a literal column name.
   - For multi-letter quantities inside display math, use `\operatorname{}` or `\text{}` so Word does not space letters apart.
   - Good:
     ```tex
     $$\theta = \max\left(0, \min\left(1,
     \frac{|\operatorname{metric}_{\text{raw}} - \operatorname{metric}_{\text{processed}}|}
     {|\operatorname{metric}_{\text{raw}}|}\right)\right)$$
     ```
   - Risky for Word/PDF export:
     ```tex
     $$\mathrm{metricValue}_{\mathrm{raw}}$$
     ```
     This can render as spaced letters in some LibreOffice/PDF conversion paths.
   - For standard errors and named subscripts, use:
     ```tex
     $\text{SE}_{\text{raw}}$
     $|\operatorname{metric}_{\text{raw}}/t_{\text{raw}}|$
     ```
   - Avoid long code-style formulas in prose. If a formula is conceptually simple but visually fragile, replace code notation with a short sentence and a display equation.

4. Keep terminology distinct from math.
   - Treat literal software outputs as code: `metric_raw`, `metric_processed`, `qc_score`.
   - Treat mathematical quantities as math: $\operatorname{metric}_{\text{raw}}$.
   - In methods, define whether a formula is primary, revised, exploratory, diagnostic, or sensitivity-only. Do not let multiple estimands share one label without explicit mode naming.

5. Rebuild and inspect actual DOCX/PDF.
   - Rebuild DOCX from source, then validate ZIP integrity:
     ```bash
     pandoc manuscript/manuscript.md -o build/manuscript.docx
     unzip -t build/manuscript.docx | tail -5
     ```
   - Convert to PDF with LibreOffice:
     ```bash
     soffice --headless --convert-to pdf --outdir build/pdf_check build/manuscript.docx
     pdfinfo build/pdf_check/manuscript.pdf | rg 'Pages|Page size|File size'
     ```
   - Render pages for visual review:
     ```bash
     rm -rf build/pdf_check/pages
     mkdir -p build/pdf_check/pages
     pdftoppm -png -r 130 build/pdf_check/manuscript.pdf build/pdf_check/pages/page
     ```

6. Make contact sheets for fast visual QC.
   - Contact sheets are useful for finding figure clipping, label overlap, table overflow, blank pages, and stale figures.
   - Inspect formula pages at high resolution, not only the thumbnail sheet.
   - If the user points to a screenshot, compare the screenshot against regenerated page images.

7. Fix figures in source scripts, not in Word.
   - For overlapping labels, increase figure size, add `subplots_adjust`, reduce label density, wrap panel titles, move annotations into empty space, or remove nonessential callout boxes.
   - Keep publication images and DOCX-embedded images synchronized.
   - If a script writes only one image format but the DOCX uses another, patch the script to write both.
   - After regeneration, check image bounds/margins with PIL or a contact sheet.

8. Fix tables by DOCX postprocessing when needed.
   - Wide Markdown tables often render poorly in Word.
   - Postprocess the DOCX XML to set fixed table layout, smaller table font, narrower page margins, wrapping cells, and top vertical alignment.
   - Validate after repacking with `unzip -t`.

9. Sync upload packages after rebuilding.
   - Copy rebuilt manuscript, figures, scripts, and embedded image folders into the submission/upload directory.
   - Verify the upload directory is not stale by comparing file sizes/timestamps.
   - Rebuild and test the final zip:
     ```bash
     zip -r upload_package_qc.zip upload_package_dir
     unzip -t upload_package_qc.zip
     ```

## Formula Rendering Checklist

- [ ] Inline variables with subscripts use math mode, not code spans.
- [ ] Multi-letter variables in equations use `\operatorname{}` or `\text{}`.
- [ ] Literal table/code column names remain in backticks.
- [ ] Fractions are not too wide for the page.
- [ ] Greek letters, subscripts, and absolute-value bars survive DOCX/PDF export.
- [ ] Primary, revised, exploratory, and sensitivity formulas are clearly labeled as different estimands.
- [ ] The generated PDF page containing formulas has been visually inspected.

## Figure/Table Rendering Checklist

- [ ] Each figure source script regenerates the file used by DOCX and the file used by submission.
- [ ] No panel labels, legends, colorbars, annotations, or numeric labels overlap.
- [ ] No right/left edge clipping after PDF conversion.
- [ ] Figure captions follow the corresponding figure and are not split awkwardly when avoidable.
- [ ] Tables do not overflow the page, hide columns, or use unreadably tiny text.
- [ ] The final upload directory contains the regenerated assets, not stale originals.

## Common Failure Modes

- Screenshot shows malformed formula, but source already fixed: rebuild DOCX/PDF before editing again.
- `\mathrm{metricValue}` renders as spaced letters in PDF: replace with `\operatorname{metricValue}`.
- Prose says `Y_ij` instead of showing a subscript: replace code span with `$Y_{ij}$`.
- Figure looks fixed in `figures/` but wrong in DOCX: the embedded image was stale or missing.
- Upload zip still has old images: sync the upload directory after regeneration, then re-zip.
- Git commands fail due to unrelated repository issues: continue with file-level verification; do not block manuscript QC on git status.

## Final Response Pattern

When reporting back, give:

- The corrected DOCX path.
- The PDF/check image path.
- The final upload zip path if rebuilt.
- Exact validation performed: DOCX `unzip -t`, PDF conversion, page count, contact sheet or page inspection, zip `unzip -t`.
- Any remaining visual risk, especially dense supplementary figures or tables that are acceptable but not elegant.
