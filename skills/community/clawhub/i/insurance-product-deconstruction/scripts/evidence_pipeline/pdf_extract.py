"""Page-level PDF extraction with OCR fallback and provenance."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Callable, Iterable


def _default_page_provider(path: Path):
    import pdfplumber
    return pdfplumber.open(path)


def _default_ocr_page(path: Path, page_index: int, temp_dir: Path) -> list[dict]:
    import sys
    import pypdfium2 as pdfium

    # Try to find OCR tools from config, fallback to home/tools
    try:
        from scripts.config import get_ocr_tools_dir
        tools_dir = get_ocr_tools_dir()
    except ImportError:
        tools_dir = None
    if tools_dir is None:
        tools_dir = Path.home() / "tools" / "insurance-wiki"
    sys.path.insert(0, str(tools_dir))
    from ocr_manager import OCRManager

    pdf = pdfium.PdfDocument(str(path))
    page = pdf[page_index]
    image = page.render(scale=200 / 72).to_pil()
    image_path = temp_dir / f"page-{page_index + 1}.png"
    image.save(image_path)
    try:
        return OCRManager.get_instance().recognize(str(image_path))
    finally:
        pdf.close()


def _join_ocr(records: Iterable[dict]) -> tuple[str, float | None, list]:
    texts = []
    confidences = []
    boxes = []
    for record in records or []:
        text = str(record.get("text", "")).strip()
        if text:
            texts.append(text)
        confidence = record.get("confidence")
        if isinstance(confidence, (int, float)):
            confidences.append(float(confidence))
        if record.get("box") is not None:
            boxes.append(record["box"])
    average = sum(confidences) / len(confidences) if confidences else None
    return "\n".join(texts), average, boxes


def extract_pdf_pages(
    pdf_path: Path,
    *,
    page_provider: Callable[[Path], object] | None = None,
    ocr_page: Callable[[Path, int, Path], list[dict]] | None = None,
    min_chars: int = 50,
    enable_ocr: bool = False,
) -> list[dict]:
    pdf_path = Path(pdf_path).resolve()
    provider = page_provider or _default_page_provider
    ocr = ocr_page or _default_ocr_page
    records = []
    with provider(pdf_path) as pdf, tempfile.TemporaryDirectory(prefix="insurance-evidence-") as raw_tmp:
        temp_dir = Path(raw_tmp)
        for index, page in enumerate(pdf.pages):
            direct = (page.extract_text() or "").strip()
            if len(direct) >= min_chars or not enable_ocr:
                text, confidence, boxes, method = direct, None, [], "direct"
            else:
                text, confidence, boxes = _join_ocr(ocr(pdf_path, index, temp_dir))
                method = "ocr"
            records.append({
                "source": str(pdf_path),
                "page": index + 1,
                "method": method,
                "text": text,
                "confidence": confidence,
                "boxes": boxes,
            })
    return records
