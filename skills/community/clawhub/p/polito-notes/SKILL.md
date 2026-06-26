---
name: polito-notes
dependencies:
  - pdftotext (poppler-utils) — for PDF text extraction
  - python3 — for note generation
  - ~/.local/share/local-rag/venv/ — for pdfminer.six fallback
description: >
  Convert PDF lecture slides into comprehensive bilingual (IT+EN) markdown notes
  for Polito university courses. Use when the user sends a PDF and specifies a
  course — or asks to process lecture material into notes.
  Triggers on "appunti", "notes", "processa questo pdf", "materia", "lezione".
---

# Polito Notes Pipeline

Convert a PDF into **two** markdown files: Italian (`notes.md`) and English (`notes-en.md`), placed in the correct course folder.

## Repository Structure

```
~/Documenti/github/polito/
├── first-year/
│   ├── first-semester/<course>/notes/
│   └── second-semester/<course>/notes/
├── second-year/
│   └── first-semester/<course>/notes/
```

Existing courses (check with `ls` — new ones may exist):
- **1st year 1st sem:** architetture-dei-sistemi-di-elaborazione, big-data-processing-and-analytics, computer-network-technologies-and-services, data-science-and-database-technology
- **1st year 2nd sem:** machine-learning-and-pattern-recognition, programmazione-di-sistema, software-engineering, web-applications-1
- **2nd year 1st sem:** advanced-machine-learning, deep-natural-language-processing, large-language-models, robot-learning

## Input

The user provides:
1. A PDF file (via file send or local path)
2. The **course name** (in Italian or English)
3. Optionally: lecture number and/or date

## Output

Two files in `<course>/notes/<N-kebab-title>/`:
- `notes.md` — Italian
- `notes-en.md` — English translation (not a literal translation: adapt phrasing to natural academic English while preserving identical structure and technical accuracy)

### Folder Naming

`N-titolo-in-kebab-case` — N is the lecture number (provided by user or inferred from content/prior folders).

## Template

Both files follow this exact structure:

```markdown
# [Title]

> **Course:** Course Name  
> **Lecture:** N  
> **Date:** YYYY-MM-DD  
> **Source:** original-filename.pdf

## Overview

[2-3 sentences: what this lecture covers and how it connects to previous topics]

## Content

### [Section 1 — Name]

[Fluid narrative prose. NOT bullet-list dumps. Explain each concept with
connecting logic, context, and motivation before diving into details.]

[Formulas in LaTeX inline/block, each symbol explained verbally right after.]

[When a comparison, taxonomy, or parameter set appears → **table**]

[When a process, pipeline, architecture, or relationship between concepts
appears → **Mermaid diagram**]

### [Section 2 — Name]
...

## Key Concepts

| Concept | Definition | Formula / Note |
|---------|-----------|----------------|
| ...     | ...       | ...            |

[Only at the end, as quick-reference. Does NOT replace the full explanations.]

## Connections

[Links to other lectures or courses when relevant.]
```

## Rules

1. **Zero information loss** — every definition, formula, example, use case, caveat, and technical detail from the PDF must appear in the output. Nothing gets skipped.
2. **Narrative flow** — write in continuous prose, not mechanical lists. Bullet points only when genuinely natural (e.g., listing properties). Prefer "The key idea behind X is..." over "• X is...".
3. **Visual reconstruction** — every diagram, schema, or figure in the PDF becomes a **Mermaid diagram** when possible (flowcharts, sequences, hierarchies). For complex visual layouts (matrices, heatmaps, scatter plots, mathematical plots), use a **descriptive paragraph** explaining what the figure shows instead of forcing an inaccurate Mermaid diagram.
4. **Formulas** — LaTeX `$$block$$` or `$inline$`. After each formula, explain every symbol in words.
5. **Terminology** — first occurrence of a technical term: **bold**. Standard English terms stay in English even in the Italian version (with Italian explanation on first use).
6. **Update vs create** — if the PDF covers topics already in an existing notes file, integrate the new content into the existing file. Don't duplicate.
7. **Both files must be structurally identical** — same sections, same tables, same diagrams. Only language differs.
8. **Backup** — before overwriting an existing notes file, copy it to `<filename>.bak` (e.g., `notes.md.bak`, `notes-en.md.bak`).
9. **Sensitive data warning** — PDFs may contain sensitive or personal data. All content from the PDF will be preserved verbatim in the generated markdown notes. Ensure notes are stored securely and not shared publicly.

## Workflow

1. Extract text from PDF (use `pdftotext` or python script)
2. Identify the course and resolve the target folder
3. Check existing folders to determine lecture number
4. Generate `notes.md` (Italian) following the template
5. Generate `notes-en.md` (English) — same structure, natural academic English
6. Write both files to the target folder
7. Confirm to the user with: course, lecture number, folder path, and a brief summary of what was covered

## RAG Integration

After generating notes, the new markdown files will be automatically picked up by the **local-rag** skill during the next indexing run (daily cron at 9 AM). No manual action needed.

To search across all notes immediately:

```bash
~/.local/share/local-rag/venv/bin/python ~/.openclaw/workspace/skills/lookupmark-local-rag/scripts/query.py "attention mechanism in transformers" --top-n 5
```

## Example Output Structure

```
polito/second-year/first-semester/large-language-models/notes/
├── 01-introduction-to-llms/
│   ├── notes.md          # Italian
│   └── notes-en.md       # English
├── 02-transformer-architecture/
│   ├── notes.md
│   └── notes-en.md
└── ...
```
