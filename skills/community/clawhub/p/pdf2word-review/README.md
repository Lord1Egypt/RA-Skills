# pdf2word-review (Agent Skill)

Convert PDF to editable Word **and automatically audit the conversion quality** — a four-way reconciliation (character count, table count, image count, table-cell count) that turns "did anything get dropped?" into evidence.

This is a **thin wrapper** skill around the open-source `pdf2word-review` engine (AGPL-3.0). It installs the engine, runs the conversion + reconciliation, and interprets the result for the user.

- **Engine repo:** https://github.com/xiyanjun/pdf-to-word-review
- **PyPI:** https://pypi.org/project/pdf2word-review/

## Why this skill

Most PDF→Word tools only convert. This one converts *and* verifies — it reconciles four dimensions and flags silent content loss, split/merged tables, and dropped images.

## Quick start

```bash
pip install git+https://github.com/xiyanjun/pdf-to-word-review.git
pdf2word input.pdf -o output.docx --verify --html
```

## Requirements

- Core: `pdf2docx`, `PyMuPDF`, `python-docx`, `lxml` (auto-installed)
- Optional OCR (scanned PDFs only): macOS Vision (`pyobjc-framework-Vision pyobjc-framework-Quartz`) or PaddleOCR (`paddleocr paddlepaddle`)
- Layout polish is macOS-only; use `--no-polish` elsewhere

## License

Engine: AGPL-3.0. This skill vendors no engine code.
