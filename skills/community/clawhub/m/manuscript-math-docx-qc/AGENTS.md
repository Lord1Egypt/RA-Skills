# AGENTS.md - Manuscript Math, DOCX, and Visual QC

This repository contains a portable agent skill/playbook for manuscript rendering QC. It is intended for OpenClaw, Hermes, Claude, Codex, and other agents that can inspect files and run local commands.

## Primary Instruction

Follow `SKILL.md` as the authoritative workflow. Use it to check manuscripts that will be exported to DOCX/PDF, especially when formulas, subscripted variables, figures, tables, Word rendering, Pandoc conversion, LibreOffice PDF checks, or upload-package synchronization may fail.

## Runtime Expectations

- Work from source files whenever possible. Prefer fixing Markdown, TeX, scripts, or DOCX-generation code over manually editing exported artifacts.
- Rebuild the real DOCX/PDF artifacts before judging screenshots or old exports.
- Validate generated DOCX files with `unzip -t`.
- Convert DOCX to PDF with LibreOffice when available.
- Render PDF pages to images and visually inspect formula, figure, and table pages.
- Keep examples and future edits generic. Do not add private paths, manuscript titles, author details, unpublished findings, or project-specific upload names.

## Useful Commands

```bash
rg -n "\\$\\$|\\\\\\(|\\\\\\)|\\\\frac|\\\\sum|metric|SE_|Y_\\{|w_\\{|scores\\[|weights\\[" manuscript code
pandoc manuscript/manuscript.md -o build/manuscript.docx
unzip -t build/manuscript.docx | tail -5
soffice --headless --convert-to pdf --outdir build/pdf_check build/manuscript.docx
pdfinfo build/pdf_check/manuscript.pdf | rg 'Pages|Page size|File size'
pdftoppm -png -r 130 build/pdf_check/manuscript.pdf build/pdf_check/pages/page
```

## Minimal Self-Test

Run this from the repository root:

```bash
bash -n examples/minimal/qc_commands.sh
./examples/minimal/qc_commands.sh
```

Expected result: the script creates a DOCX, validates it, converts it to PDF, renders one page image, and leaves only `build/` as ignored output.
