# CLI Options

Use these defaults unless the user requests something more specific.

## Input Selection

- `ppx parse <file> -o <dir>`: Parse one PDF or image.
- `ppx parse <dir> -o <dir>`: Batch-parse a directory.
- `--pages "1-5,10,15-20"`: Restrict parsing to selected pages.

## OCR

- `--ocr auto`: Default. Works for mixed native/scanned documents.
- `--ocr yes`: Force OCR for scanned PDFs and raster-heavy pages.
- `--ocr no`: Skip OCR for native PDFs with selectable text.

## Tables

- `--table auto`: Default.
- `--table wbk`: White-background tables in ordinary documents.
- `--table ybk`: Colored or dark-background tables.
- `--table llm`: Highest table fidelity when an LLM backend is configured.
- `--table no`: Skip table extraction.

## Other Useful Flags

- `--mode page|tree|ppt`: Select parse mode. Use `page` unless a different downstream structure is required.
- `--workers N`: Parallelize directory parsing.
- `--html`: Emit `doc.html` in the output directory for HTML preview/export.
- `--json`: Emit JSON-focused output.
- `--cpu`: Force CPU mode.
- `--debug` or `-x`: Keep extra debug output.
- `--dev`: Save intermediate results for investigation.
