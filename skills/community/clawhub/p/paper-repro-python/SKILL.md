---
name: paper-repro-python
description: This skill should be used when the user asks to "reproduce a paper", "implement paper methods in Python", "extract paper content to Markdown", or works on paper reproduction tasks. Use for TeX-first extraction, modular Python implementation, and bilingual documentation.
metadata:
  openclaw:
    emoji: "📄"
---

# Follow this workflow end-to-end unless the user explicitly asks to skip steps

## 1) Intake and scope

- Confirm input artifacts: TeX source path(s), PDF path, supplementary files, target repository, and expected outputs.
- State assumptions explicitly when information is missing.
- Keep approach adaptable to the specific paper; do not force a fixed dependency stack or rigid project template.
- Check whether the working folder already contains paper source files (`.tex`, `.bib`, style files, figures).
- Check whether the working folder contains user-preprocessed documents (`.md`, `.json`, images such as `.png`, `.jpg`, `.svg`).
- Source priority rule (read in order, stop when sufficient):
  1. **TeX sources** (preferred): If usable TeX source files (`.tex`, `.bib`, style files) are present, use them as the primary source.
  2. **User-preprocessed documents** (secondary): If TeX is absent or incomplete, read user-provided documents (`.md`, `.json`) and images (`.png`, `.jpg`, `.svg`) that may contain pre-extracted paper content.
  3. **PDF fallback** (last resort): Only when both TeX and user-preprocessed documents are unavailable or insufficient, fall back to PDF extraction.

## 2) Source extraction (TeX → preprocessed docs → PDF)

- TeX path (highest priority):
  - Parse and read the main TeX project structure first (`main.tex` or equivalent entry file and includes).
  - Preserve original scientific wording when converting relevant content to Markdown notes.
  - Resolve equations, theorem blocks, citations, and appendices from source files whenever possible.
  - Record unresolved include/bibliography issues explicitly; do not invent missing content.

- User-preprocessed documents path (secondary):
  - Read Markdown files (`.md`) that may contain paper content extracted by the user.
  - Read JSON files (`.json`) that may contain structured paper data (metadata, sections, references).
  - View images (`.png`, `.jpg`, `.svg`) that may contain paper figures, tables, or scanned pages.
  - Preserve original content; do not summarize or paraphrase.
  - Note the source of each piece of information (which file, which section).

- PDF fallback path (lowest priority, when all else fails):
  - Extract paper content page by page into Markdown, preserving the original wording.
  - Do not summarize, paraphrase, or rewrite scientific statements.
  - Preserve structure faithfully:
    - Title, authors, affiliations, abstract, sections, subsections.
    - Equations (LaTeX-friendly when possible), theorem/lemma/proposition blocks.
    - Tables, figure captions, references, appendices, footnotes.
  - If a PDF is scanned or partially unreadable:
    - Run OCR and mark uncertain spans clearly.
    - Never silently invent missing text.
  - Include image references/placeholders when figures cannot be represented as plain text.
  - Produce one primary output file such as `paper_fulltext.md`.

## 3) Extraction quality checks

- Validate completeness before moving to reproduction:
  - Section/headings coverage matches the TeX project or PDF source used.
  - Key equations and algorithm blocks are present.
  - References and appendices are included if present in the source.
- Report known extraction limitations and exact affected files/pages/segments.

## 4) Reproduction planning (paper-specific)

- Build a reproduction plan from the extracted source materials (TeX-derived notes and/or Markdown), not from memory.
- Identify:
  - Problem definition, notation, assumptions, and objective functions.
  - Algorithm steps and required components.
  - Dataset generation/loading, training/optimization, and evaluation protocol.
  - Baselines and ablations required for faithful reproduction.
- If details are missing or ambiguous, call out the gap and provide a conservative implementation choice with rationale.

## 5) Python implementation principles

- Implement with modular design and clear boundaries:
  - Separate concerns (data, models/algorithms, training/solver loop, evaluation, utils, config).
  - Prefer low coupling and high cohesion.
- Avoid monolithic scripts:
  - Split code into modules whenever responsibilities can be separated.
  - Prefer one clear responsibility per file.
- File size guideline:
  - Keep a single source file under ~200 lines whenever practical.
  - If a file grows beyond ~200 lines, refactor into submodules unless there is a clear reason not to.
- Keep dependencies minimal and paper-driven; choose tools based on the paper's actual needs.
- Avoid over-engineering early; start from the minimum reproducible core, then extend.
- Add tests/checks for critical math or pipeline steps where feasible.
- Preserve reproducibility:
  - deterministic seeds when applicable,
  - explicit config for key hyperparameters,
  - clear experiment entry points.

## 6) Logging and data persistence

- All reproduction experiments must save execution logs and output data:
  - **Logs**: Save console output, training progress, and error messages to timestamped log files (e.g., `logs/experiment_YYYYMMDD_HHMMSS.log`).
  - **Data**: Save all generated data (metrics, model checkpoints, intermediate results) to structured files (e.g., JSON, CSV, or pickle) in a dedicated `outputs/` or `results/` directory.
  - **Configuration snapshot**: Save the exact configuration/hyperparameters used for each run alongside the outputs.
- Logging should capture enough detail to:
  - Trace the execution flow for debugging.
  - Compare results across multiple runs.
  - Identify the exact conditions under which results were produced.

## 7) Result verification and comparison

- After running reproduction experiments, compare results against the paper's reported data:
  - Extract quantitative metrics (tables, figures) from the paper source.
  - Compute the same metrics from reproduction outputs.
  - Document both paper-reported values and reproduction values side by side.
- Identify discrepancies:
  - If reproduction results deviate significantly from paper results, investigate potential causes:
    - Implementation errors (algorithm bugs, missing steps).
    - Hyperparameter differences.
    - Random seed or initialization differences.
    - Dataset or preprocessing differences.
  - Document all findings and fixes applied.
- Validation criteria:
  - Define acceptable tolerance for numerical differences based on the paper's domain.
  - Flag results outside tolerance for further review.
- The goal of reproduction is accurate reconstruction of paper results; verification is mandatory, not optional.

## 8) README header requirements (paper metadata)

- Every reproduction project README must start with paper metadata before any other content:
  - **Paper title** (original title as published)
  - **Authors** (full names, affiliations, and email addresses if available)
  - **Abstract** (verbatim copy of the original abstract)
- For `README_zh-CN.md`:
  - Paper title: provide Chinese translation if original is in English; keep original if paper is in Chinese.
  - Authors: keep original names and affiliations; translate country/region names if needed.
  - Abstract: provide faithful Chinese translation of the abstract.
- Format example (English README):

  ```markdown
  # [Paper Title]

  **Authors:** Author Name¹, Co-Author Name²
  **Affiliations:**
  ¹ Department, University, Country (email@university.edu)
  ² Lab, Institution, Country (email@institution.edu)

  ## Abstract

  [Verbatim abstract text from the paper]

  ---

  [Then reproduction project content begins...]
  ```

## 9) README update requirements (bilingual + images)

- Generate and maintain two README files after code changes:
  - `README.md` (English original)
  - `README_zh-CN.md` (Chinese translation aligned with the English version)
- After the paper metadata header, ensure both files include:
  - paper citation and target claims to reproduce,
  - environment/setup commands,
  - project structure overview and module responsibilities,
  - how to run main experiments,
  - expected outputs/metrics and where artifacts are saved,
  - known deviations from the paper and why.
- Insert generated figures/images into both README files using valid relative Markdown image paths.
- Image output granularity rule: unless multi-panel comparison is explicitly needed, save one chart per image file (one figure per file).
- Keep both README files aligned with actual code paths and commands.
- Keep Chinese content as faithful translation of English technical content (no missing key steps).

## 10) Output contract

- Deliver:
  - source-derived extraction notes/file(s) (TeX-first, PDF fallback when needed),
  - implemented/updated Python code,
  - `README.md` and `README_zh-CN.md` with embedded generated images.
- Clearly separate:
  - exact extracted content (verbatim from source),
  - your implementation notes and engineering decisions.
- Report reproduction status:
  - which claims/experiments were successfully reproduced,
  - known gaps or deviations from paper results, with reasons.
