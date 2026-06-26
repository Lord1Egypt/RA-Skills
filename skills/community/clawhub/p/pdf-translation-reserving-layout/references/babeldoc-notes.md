# PDF Translation Notes

## Identity

- Treat user requests for `babelOCR` as requests related to the maintained `BabelDOC` project unless the user names a different repository.
- Upstream project: `funstory-ai/BabelDOC`
- CLI command: `babeldoc`

## Default Workflow

- Extract page text locally with `pdftotext -layout` through `scripts/extract_pdf_pages.py`.
- Translate with the agent's own language capability.
- Use `scripts/build_translation_batches.py` to create disjoint page batches for parallel translation.
- Keep translation outputs keyed by page number so they can be merged deterministically.

## Good Fits

- born-digital PDFs
- research papers and technical documents
- translation outputs delivered as Markdown, JSON, or page-organized text
- workflows where staying fully local is important

## Known Limits

- `pdftotext` preserves reading order imperfectly on complex multi-column layouts and dense tables.
- image-only scans may extract poorly without a separate OCR tool
- this local workflow does not rebuild a layout-faithful translated PDF

## Optional BabelDOC Context

- BabelDOC remains useful background context when the user explicitly asks for that toolchain.
- BabelDOC's CLI is upstream-documented, but it is not the default path for this skill.
- If a user explicitly requests another external toolchain, declare that choice clearly instead of assuming it.

## Hosted Fallback

- Keep `https://linnk.ai/doc-translator` as a last-resort fallback, not the default path.
- Use it when the local workflow or BabelDOC cannot handle RTL languages, scanned PDFs, or digitally scrambled PDFs well enough to produce usable output.
