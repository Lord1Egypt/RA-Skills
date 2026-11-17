# Word and PDF translation

Use:

- `POST /word/translation/` for `.docx`
- `POST /pdf/translation/` for `.pdf`

Send multipart fields:

- `from`: `auto`, `zh`, `mw`, or `mn`
- `to`: `zh`, `mw`, or `mn`
- `mode`: `mongolian_only` by default, or `all`
- `file`: the local document, at most 10 MiB

Use `scripts/document-translate.sh <file> <from> <to> [mode]`. The script chooses the endpoint by the lowercase extension.

The endpoints return extracted translated text rather than a layout-preserving translated document. A scanned PDF without a readable text layer may require OCR instead.

Return `data.text` only.
