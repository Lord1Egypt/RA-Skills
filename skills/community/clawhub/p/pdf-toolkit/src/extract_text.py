# pyright: reportMissingImports=false
import io
import os
from pathlib import Path

import pdfplumber
import pypdf

from constants import PDF_EXTENSIONS, TABLE_CELL_SEP, TABLE_ROW_SEP
from utils import clean_text, parse_page_ranges, require_file, resolve_path


def extract_text(path_str: str, pages_spec: str | None = None) -> dict:
    """Extract plain text from a PDF, optionally limited to a page range."""
    path = resolve_path(path_str)
    err = require_file(path, PDF_EXTENSIONS)
    if err:
        return {"error": err}

    try:
        reader = pypdf.PdfReader(str(path))
        total = len(reader.pages)

        if pages_spec:
            indices = parse_page_ranges(pages_spec, total)
            if isinstance(indices, str):
                return {"error": indices}
        else:
            indices = list(range(total))

        parts = []
        for idx in indices:
            page = reader.pages[idx]
            text = page.extract_text() or ""
            parts.append((idx + 1, text))

        return {"file": str(path), "total_pages": total, "extracted_pages": parts}
    except Exception as exc:
        return {"error": f"Could not extract text: {exc}"}


def extract_tables(path_str: str, pages_spec: str | None = None) -> dict:
    """Extract tables from a PDF using pdfplumber."""
    path = resolve_path(path_str)
    err = require_file(path, PDF_EXTENSIONS)
    if err:
        return {"error": err}

    try:
        with pdfplumber.open(str(path)) as pdf:
            total = len(pdf.pages)

            if pages_spec:
                indices = parse_page_ranges(pages_spec, total)
                if isinstance(indices, str):
                    return {"error": indices}
            else:
                indices = list(range(total))

            all_tables = []
            for idx in indices:
                page = pdf.pages[idx]
                tables = page.extract_tables()
                for table in tables:
                    all_tables.append({"page": idx + 1, "rows": table})

        return {"file": str(path), "total_pages": total, "tables": all_tables}
    except Exception as exc:
        return {"error": f"Could not extract tables: {exc}"}


def extract_images(path_str: str, output_dir_str: str | None = None) -> dict:
    """Extract embedded images from a PDF using pypdf."""
    path = resolve_path(path_str)
    err = require_file(path, PDF_EXTENSIONS)
    if err:
        return {"error": err}

    output_dir = resolve_path(output_dir_str) if output_dir_str else path.parent
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return {"error": f"Cannot create output directory: {exc}"}

    try:
        reader = pypdf.PdfReader(str(path))
        saved = []
        count = 0
        for page_idx, page in enumerate(reader.pages):
            for img_obj in page.images:
                stem = path.stem
                ext = img_obj.name.split(".")[-1] if "." in img_obj.name else "png"
                filename = f"{stem}_p{page_idx + 1}_{count + 1}.{ext}"
                out_path = output_dir / filename
                out_path.write_bytes(img_obj.data)
                saved.append(str(out_path))
                count += 1

        return {
            "file": str(path),
            "images_extracted": count,
            "output_dir": str(output_dir),
            "files": saved,
        }
    except Exception as exc:
        return {"error": f"Could not extract images: {exc}"}
