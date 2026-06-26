from __future__ import annotations

from pathlib import Path
from typing import Iterable

import img2pdf
from PIL import Image, ImageOps
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.pdfgen import canvas

from ..core.deps import require_bin
from ..core.exec import run_cmd

_PAGE_SIZES = {
    "A4": A4,
    "LETTER": LETTER,
}


def images_to_pdf(
    inputs: Iterable[Path],
    output_path: Path,
    page_size: str | None = None,
    margin: int = 0,
) -> None:
    images = [Path(p) for p in inputs]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if page_size is None:
        with output_path.open("wb") as f:
            f.write(img2pdf.convert([str(p) for p in images]))
        return

    size = _PAGE_SIZES.get(page_size.upper())
    if not size:
        raise ValueError(f"Unsupported page size: {page_size}. Use A4 or LETTER.")

    width, height = size
    c = canvas.Canvas(str(output_path), pagesize=size)
    for path in images:
        img = Image.open(path)
        img = ImageOps.exif_transpose(img)
        iw, ih = img.size
        max_w = width - 2 * margin
        max_h = height - 2 * margin
        scale = min(max_w / iw, max_h / ih)
        new_w = iw * scale
        new_h = ih * scale
        x = (width - new_w) / 2
        y = (height - new_h) / 2
        c.drawInlineImage(img, x, y, new_w, new_h)
        c.showPage()
    c.save()


def pdf_to_jpg(
    input_pdf: Path,
    output_dir: Path,
    dpi: int = 150,
    first_page: int | None = None,
    last_page: int | None = None,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = output_dir / input_pdf.stem

    pdftoppm = require_bin("pdftoppm", "Install poppler to enable PDF rendering")
    cmd = [pdftoppm, "-jpeg", "-r", str(dpi)]
    if first_page is not None:
        cmd.extend(["-f", str(first_page)])
    if last_page is not None:
        cmd.extend(["-l", str(last_page)])
    cmd.extend([str(input_pdf), str(prefix)])
    run_cmd(cmd)

    return sorted(output_dir.glob(f"{input_pdf.stem}-*.jpg"))
