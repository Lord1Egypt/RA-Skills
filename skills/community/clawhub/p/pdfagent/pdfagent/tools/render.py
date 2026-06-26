from __future__ import annotations

from pathlib import Path

from ..core.deps import require_bin
from ..core.exec import run_cmd


def render_pdf_to_images(
    input_pdf: Path,
    output_dir: Path,
    *,
    dpi: int = 150,
    fmt: str = "png",
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = output_dir / input_pdf.stem

    pdftoppm = require_bin("pdftoppm", "Install poppler to enable PDF rendering")

    if fmt not in {"png", "jpeg", "jpg"}:
        raise ValueError("fmt must be png or jpeg")

    if fmt in {"jpeg", "jpg"}:
        args = [pdftoppm, "-jpeg", "-r", str(dpi), str(input_pdf), str(prefix)]
        run_cmd(args)
        ext = "jpg"
    else:
        args = [pdftoppm, "-png", "-r", str(dpi), str(input_pdf), str(prefix)]
        run_cmd(args)
        ext = "png"

    return sorted(output_dir.glob(f"{input_pdf.stem}-*.{ext}"))
