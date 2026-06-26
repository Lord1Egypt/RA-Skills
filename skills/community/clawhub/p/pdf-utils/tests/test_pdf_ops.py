from pathlib import Path

import fitz

from scripts.pdf_ops import merge_pdfs, page_to_image, split_pdf


def _make_pdf(path: Path, pages: int) -> None:
    doc = fitz.open()
    for idx in range(pages):
        page = doc.new_page()
        page.insert_text((72, 72), f"page {idx + 1}")
    doc.save(path)
    doc.close()


def test_merge_split_render(tmp_path: Path):
    a = tmp_path / "a.pdf"
    b = tmp_path / "b.pdf"
    merged = tmp_path / "merged.pdf"
    split = tmp_path / "split.pdf"
    image = tmp_path / "page.png"

    _make_pdf(a, 1)
    _make_pdf(b, 2)

    merge_pdfs([str(a), str(b)], str(merged))
    merged_doc = fitz.open(merged)
    assert merged_doc.page_count == 3
    merged_doc.close()

    split_pdf(str(merged), 2, 3, str(split))
    split_doc = fitz.open(split)
    assert split_doc.page_count == 2
    split_doc.close()

    page_to_image(str(merged), 1, 2.0, str(image))
    assert image.exists()
    assert image.stat().st_size > 0
