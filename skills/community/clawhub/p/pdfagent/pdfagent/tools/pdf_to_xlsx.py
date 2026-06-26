from __future__ import annotations

from pathlib import Path


def pdf_to_xlsx(
    input_path: Path,
    output_path: Path,
    pages: str = "1",
    flavor: str = "stream",
) -> None:
    try:
        import camelot
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("camelot-py is required. Install with: pip install 'pdfagent[tables]'") from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tables = camelot.read_pdf(str(input_path), pages=pages, flavor=flavor)
    if tables.n == 0:
        raise RuntimeError("No tables detected")

    tables.export(str(output_path), f="excel")
