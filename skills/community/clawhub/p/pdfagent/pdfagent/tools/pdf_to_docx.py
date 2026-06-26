from __future__ import annotations

from pathlib import Path


def pdf_to_docx(input_path: Path, output_path: Path, start: int | None = None, end: int | None = None) -> None:
    try:
        from pdf2docx import Converter
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("pdf2docx is required. Install with: pip install 'pdfagent[docx]'") from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    converter = Converter(str(input_path))
    try:
        if start is None and end is None:
            converter.convert(str(output_path))
        elif end is None:
            converter.convert(str(output_path), start=start)
        else:
            converter.convert(str(output_path), start=start, end=end)
    finally:
        converter.close()
