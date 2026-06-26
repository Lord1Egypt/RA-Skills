from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image, ImageEnhance, ImageOps

from .images import images_to_pdf
from .ocr import ocr_pdf


def scan_to_pdf(
    inputs: Iterable[Path],
    output_path: Path,
    *,
    enhance: bool = False,
    grayscale: bool = False,
    ocr: bool = False,
    ocr_lang: str = "eng",
) -> None:
    processed: list[Path] = []
    temp_dir = output_path.parent / f".{output_path.stem}_scan"
    temp_dir.mkdir(parents=True, exist_ok=True)

    for idx, path in enumerate(inputs, start=1):
        img = Image.open(path)
        img = ImageOps.exif_transpose(img)
        if grayscale:
            img = img.convert("L")
        if enhance:
            img = ImageEnhance.Contrast(img).enhance(1.3)
        out_path = temp_dir / f"scan_{idx}.png"
        img.save(out_path)
        processed.append(out_path)

    images_to_pdf(processed, output_path)

    if ocr:
        ocr_output = output_path.parent / f"{output_path.stem}_ocr.pdf"
        ocr_pdf(output_path, ocr_output, languages=ocr_lang)
        ocr_output.replace(output_path)
