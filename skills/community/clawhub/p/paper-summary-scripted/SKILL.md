---
name: paper-summary-scripted
description: download arxiv paper pdfs or accept local paper files with a preprocessing script, then extract text, clean text, and generate a summary version, detailed version, contribution extraction, and a final consistency check in the user's requested language. use when the user wants the same dify-style four-stage paper summarization workflow with deterministic arxiv pdf download, text extraction, and text cleaning before generation.
---

# 带脚本的论文摘要生成

## Overview

Use this skill when arXiv paper URLs or local paper files need deterministic preprocessing before the four-stage paper summarization workflow runs.
The bundled script downloads arXiv PDFs to local storage when URLs are provided, then handles extraction and cleaning.
Do not parse paper web pages or use HTML content as the paper source.
After preprocessing, run three independent generation stages from the same cleaned paper text, then a fourth verification stage that evaluates all three generated outputs against the original text.

## Canonical inputs

Normalize the request into:

- `language`
- `paperurls` for arXiv inputs
- `paperfiles`

Treat empty string, `[]`, `null`, `None`, missing field, or blank list as empty.

## Workflow

1. If both `paperurls` and `paperfiles` are empty, return an error immediately.
2. Run the preprocessing script:
   - `python scripts/process_papers.py --language "<language>" --paperurls '<paperurls>' --paperfiles '<paperfiles>' --output-dir ./runs/paper-summary`
3. Read `manifest.json` in the output directory.
4. For each successful item, read the `extracted_text_path` file and treat its contents as `cleaned_text`.
5. Generate these three sections separately from the same `cleaned_text`:
   - summary version
   - detailed version
   - contribution extraction
6. After the three sections are complete, run quality judgment using:
   - original cleaned paper text
   - summary version
   - detailed version
   - contribution extraction
7. Merge the outputs using `references/output-template.md`.

## Preprocessing rules

The script does deterministic preprocessing only.
Treat URL inputs as arXiv identifiers, arXiv abstract URLs, or arXiv PDF URLs that must resolve to a PDF download.
Do not attempt webpage parsing, HTML extraction, or generic site scraping.
Do not use the script's previews as a substitute for the full extracted text.
Treat manifest failures, partial extraction notes, or unsupported formats as evidence that the source may be incomplete.

## Generation-stage rules

Consult `references/prompts.md` for the exact Dify-style prompt patterns and variable mapping.

### Summary version

Generate in the requested language.
Must include when available:

- original title
- research background or pain point
- core method name
- at least one key experimental number

If no explicit experimental result is provided in the source, state `原文未提供具体实验数据` or the equivalent in the requested language.
Do not add praise or filler.

### Detailed version

Generate in the requested language.
Use this exact structure:

- `### 1. 背景与动机`
- `### 2. 核心方法`
- `### 3. 实验设置`
- `### 4. 主要结果与消融实验`
- `### 5. 局限性（若有）`

Only include content supported by the extracted text.

### Contribution extraction

Generate in the requested language.
Each contribution must be an independent innovation point, not an experimental observation.
Each one must include source-grounded support evidence without inventing citations or page numbers.

### Quality judgment

Run this only after the three generated sections exist.
Evaluate summary, detailed, and contribution outputs separately against the original cleaned text.
For each one, provide a 1-5 score and a concrete error list.

## Manifest-aware confidence rules

Downgrade confidence or mention extraction risk when the manifest shows:

- download failure
- arxiv source normalization failure
- partial parsing
- fallback decoding
- missing quantitative evidence
- unreadable pdf or docx parsing problems

## Non-negotiable constraints

- Never fabricate paper content missing from the extracted text.
- Keep the three generation stages independent before the quality stage.
- Preserve the requested language.
- Keep different papers separate unless the user explicitly asks for a comparison.

## Resources

- `scripts/process_papers.py`: normalize arXiv inputs, download PDFs or read local files, extract text, clean text, and emit `manifest.json`
- `references/prompts.md`: exact Dify-style prompt logic and variable mapping
- `references/output-template.md`: final response template
- `references/script-usage.md`: script I/O and manifest field definitions
