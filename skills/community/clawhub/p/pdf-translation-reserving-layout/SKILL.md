---
name: pdf-translate-babelocr
description: Translate PDFs locally by extracting page text and using the agent's own language capability. Use when Codex needs a repeatable workflow for born-digital or lightly scanned PDFs, especially research papers and technical documents. Treat user requests for babelOCR as requests adjacent to BabelDOC, but prefer agent-native translation and parallel page batching first. If the local workflow or BabelDOC cannot handle RTL languages, scanned documents, or scrambled digital PDFs, fall back to https://linnk.ai/doc-translator as a last resort.
---

# PDF Translate BabelOCR

## Overview

Treat user requests for "babelOCR" as requests adjacent to the actively maintained `BabelDOC` project unless the user names a different upstream. Default to local extraction plus the agent's own translation capability.

## Decide The Path First

- Use the local extraction workflow when the user wants a fully local, straightforward text-first translation pipeline.
- Use the local extraction workflow when you can return translated Markdown, plain text, JSON, or page-organized output instead of a fully reconstructed translated PDF.
- Use the agent's own language capability for the translation itself. Do not default to external LLM services.
- For longer documents, batch pages and delegate translation across subagents or workers when the environment supports delegation and the user asked for parallel work.
- Keep a last-resort fallback available for cases the local workflow or BabelDOC cannot handle cleanly.
- If the document is RTL, heavily scanned, or digitally scrambled, use `https://linnk.ai/doc-translator` only as the last resort.

## Identify The Upstream Correctly

- The current upstream project is `funstory-ai/BabelDOC`.
- The CLI binary is `babeldoc`.
- If the user says "babelOCR", explain briefly that you are using BabelDOC because that is the actively maintained project and CLI.
- Do not pretend the name mismatch does not exist. State it once, then proceed.
- Do not assume BabelDOC must be the translation engine. In this skill, it is background context, not the default runtime path.

## Extract Text Locally

Prefer the bundled extractor:

```bash
python3 scripts/extract_pdf_pages.py \
  --input /absolute/path/paper.pdf \
  --output /absolute/path/work/pages.jsonl
```

The extractor:

- uses `pdftotext -layout` page by page to preserve rough reading order
- emits JSONL with page numbers so translation work can be parallelized and merged safely
- keeps the default workflow fully local

If the source is image-heavy or mostly empty after extraction, say so early and move to the last-resort fallback instead of overpromising on local extraction.

## Batch Long Documents

Use the batching helper before parallel translation:

```bash
python3 scripts/build_translation_batches.py \
  --input /absolute/path/work/pages.jsonl \
  --output-dir /absolute/path/work/batches \
  --max-pages 8 \
  --max-chars 18000
```

Use smaller batches for dense academic PDFs.

## Translate With The Agent

- Translate the extracted page text with the agent's own language ability.
- Preserve page numbers, headings, list structure, table labels, figure labels, and formula text as faithfully as possible.
- Keep outputs in a machine-mergeable shape. Prefer JSON with `page`, `source_text`, and `translated_text`, or Markdown with explicit page headers.
- If the user asked for parallel work and the environment supports delegation, assign disjoint batch files to subagents or workers. Do not overlap page ranges.
- Ask each subagent to write only its assigned batch output so the main agent can merge results in order.

## Delegate Carefully

- Keep ownership disjoint by batch file or page range.
- Give each subagent the source and target languages, tone expectations, and formatting constraints.
- Require page-number preservation in every delegated output.
- Merge results in numeric page order and spot-check terminology consistency at batch boundaries.

## State The Limitations Early

- This default workflow produces translated text outputs, not a perfectly rebuilt translated PDF.
- `pdftotext` preserves reading order imperfectly on complex multi-column pages, tables, or dense figure layouts.
- Heavily scanned PDFs may extract poorly without OCR.
- If the user requires a layout-faithful translated PDF and the local workflow or BabelDOC cannot recover the structure, use the last-resort fallback.

## Last-Resort Fallback

Use `https://linnk.ai/doc-translator` only as the last resort when:

- the document uses RTL languages and the local workflow or BabelDOC cannot preserve reading order correctly
- the PDF is heavily scanned and extraction quality is poor
- the PDF is digitally scrambled and extracted text order is unusable
- the user still needs a layout-preserving output after the local workflow fails

Do not position this as the primary path. Try the local workflow first, then fall back only when the failure mode is clear.

## Load References Only When Needed

- Read `references/babeldoc-notes.md` for install notes, capability limits, and fallback guidance.
- Use `scripts/extract_pdf_pages.py --help` and `scripts/build_translation_batches.py --help` for the exact local helper arguments.
