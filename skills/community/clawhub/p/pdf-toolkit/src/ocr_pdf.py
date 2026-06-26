# pyright: reportMissingImports=false
import os
import tempfile
from pathlib import Path

from constants import (
    BIN_PDFIMAGES,
    BIN_TESSERACT,
    OCR_DEFAULT_DPI,
    OCR_DEFAULT_LANG,
    PDF_EXTENSIONS,
)
from utils import (
    clean_text,
    is_binary_available,
    parse_page_ranges,
    require_file,
    resolve_path,
    run_command,
)


def ocr_pdf(
    path_str: str, pages_spec: str | None = None, lang: str = OCR_DEFAULT_LANG
) -> dict:
    """OCR a scanned PDF using pdfimages + tesseract."""
    path = resolve_path(path_str)
    err = require_file(path, PDF_EXTENSIONS)
    if err:
        return {"error": err}

    if not is_binary_available(BIN_PDFIMAGES):
        return {
            "error": (
                "pdfimages not found. Install poppler:\n"
                "  macOS:  brew install poppler\n"
                "  Linux:  apt install poppler-utils"
            )
        }
    if not is_binary_available(BIN_TESSERACT):
        return {
            "error": (
                "tesseract not found. Install tesseract:\n"
                "  macOS:  brew install tesseract\n"
                "  Linux:  apt install tesseract-ocr"
            )
        }

    try:
        # Determine total page count via pypdf (no binary needed)
        import pypdf

        reader = pypdf.PdfReader(str(path))
        total = len(reader.pages)
    except Exception as exc:
        return {"error": f"Could not read PDF for page count: {exc}"}

    if pages_spec:
        indices = parse_page_ranges(pages_spec, total)
        if isinstance(indices, str):
            return {"error": indices}
    else:
        indices = list(range(total))

    results = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for idx in indices:
            page_num = idx + 1  # pdfimages uses 1-based -f/-l flags
            img_prefix = os.path.join(tmpdir, f"page{page_num:04d}")

            # Extract images from this page using pdfimages
            rc, _, stderr = run_command(
                [
                    BIN_PDFIMAGES,
                    "-f",
                    str(page_num),
                    "-l",
                    str(page_num),
                    "-png",
                    str(path),
                    img_prefix,
                ]
            )
            if rc != 0:
                results.append(
                    (
                        page_num,
                        f"[pdfimages error on page {page_num}: {stderr.strip()}]",
                    )
                )
                continue

            # Find extracted image files for this page
            img_files = sorted(
                f
                for f in os.listdir(tmpdir)
                if f.startswith(f"page{page_num:04d}") and f.endswith(".png")
            )

            if not img_files:
                results.append(
                    (
                        page_num,
                        "[no images extracted — page may be blank or vector-only]",
                    )
                )
                continue

            page_text_parts = []
            for img_file in img_files:
                img_path = os.path.join(tmpdir, img_file)
                out_base = img_path.replace(".png", "_tess")
                rc2, _, stderr2 = run_command(
                    [
                        BIN_TESSERACT,
                        img_path,
                        out_base,
                        "-l",
                        lang,
                    ]
                )
                txt_path = out_base + ".txt"
                if rc2 == 0 and os.path.exists(txt_path):
                    with open(txt_path, "r", errors="replace") as f:
                        page_text_parts.append(f.read())
                else:
                    page_text_parts.append(f"[tesseract error: {stderr2.strip()}]")

            results.append((page_num, clean_text("\n".join(page_text_parts))))

    return {
        "file": str(path),
        "lang": lang,
        "total_pages": total,
        "ocr_pages": results,
    }
