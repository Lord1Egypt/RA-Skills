from __future__ import annotations

from pathlib import Path
from typing import Iterable
import difflib

from pypdf import PdfReader
from reportlab.pdfgen import canvas


class CompareResult:
    def __init__(self, summary_path: Path, report_pdf: Path | None = None) -> None:
        self.summary_path = summary_path
        self.report_pdf = report_pdf


def compare_pdfs(
    left: Path,
    right: Path,
    output_dir: Path,
    *,
    report_pdf: bool = True,
) -> CompareResult:
    output_dir.mkdir(parents=True, exist_ok=True)

    left_text = _extract_text(left)
    right_text = _extract_text(right)

    diff = list(difflib.unified_diff(
        left_text.splitlines(),
        right_text.splitlines(),
        fromfile=left.name,
        tofile=right.name,
        lineterm="",
    ))

    summary_path = output_dir / "diff.txt"
    summary_path.write_text("\n".join(diff), encoding="utf-8")

    report_path = None
    if report_pdf:
        report_path = output_dir / "diff.pdf"
        _render_diff_pdf(report_path, diff)

    return CompareResult(summary_path=summary_path, report_pdf=report_path)


def _extract_text(path: Path) -> str:
    reader = PdfReader(str(path))
    parts: list[str] = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)


def _render_diff_pdf(output_path: Path, diff_lines: Iterable[str]) -> None:
    c = canvas.Canvas(str(output_path))
    y = 800
    for line in diff_lines:
        if y < 40:
            c.showPage()
            y = 800
        c.setFont("Helvetica", 9)
        c.drawString(40, y, line[:120])
        y -= 12
    c.save()
