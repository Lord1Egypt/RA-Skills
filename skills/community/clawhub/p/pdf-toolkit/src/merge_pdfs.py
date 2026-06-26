# pyright: reportMissingImports=false
from pathlib import Path

import pypdf

from constants import PDF_EXTENSIONS, VALID_ROTATIONS
from utils import (
    ensure_output_dir,
    parse_page_ranges,
    require_file,
    resolve_path,
)


def merge_pdfs(input_paths: list[str], output_str: str) -> dict:
    """Merge two or more PDFs into a single output file."""
    if len(input_paths) < 2:
        return {"error": "merge requires at least two input PDF files"}

    paths = []
    for p in input_paths:
        path = resolve_path(p)
        err = require_file(path, PDF_EXTENSIONS)
        if err:
            return {"error": err}
        paths.append(path)

    output = resolve_path(output_str)
    err = ensure_output_dir(output)
    if err:
        return {"error": err}

    try:
        writer = pypdf.PdfWriter()
        total_pages = 0
        for path in paths:
            reader = pypdf.PdfReader(str(path))
            for page in reader.pages:
                writer.add_page(page)
            total_pages += len(reader.pages)

        with open(output, "wb") as f:
            writer.write(f)

        return {
            "inputs": [str(p) for p in paths],
            "output": str(output),
            "total_pages": total_pages,
        }
    except Exception as exc:
        return {"error": f"Could not merge PDFs: {exc}"}


def split_pdf(
    path_str: str,
    output_dir_str: str | None,
    pages_spec: str | None,
    output_str: str | None,
) -> dict:
    """Split a PDF into individual pages or extract a page range."""
    path = resolve_path(path_str)
    err = require_file(path, PDF_EXTENSIONS)
    if err:
        return {"error": err}

    try:
        reader = pypdf.PdfReader(str(path))
        total = len(reader.pages)

        if pages_spec:
            # Extract a range into a single output file
            indices = parse_page_ranges(pages_spec, total)
            if isinstance(indices, str):
                return {"error": indices}

            output = (
                resolve_path(output_str)
                if output_str
                else path.parent / f"{path.stem}_extracted.pdf"
            )
            err = ensure_output_dir(output)
            if err:
                return {"error": err}

            writer = pypdf.PdfWriter()
            for idx in indices:
                writer.add_page(reader.pages[idx])
            with open(output, "wb") as f:
                writer.write(f)

            return {
                "file": str(path),
                "pages_extracted": [i + 1 for i in indices],
                "output": str(output),
            }
        else:
            # Split into individual page files
            out_dir = (
                resolve_path(output_dir_str)
                if output_dir_str
                else path.parent / f"{path.stem}_pages"
            )
            try:
                out_dir.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                return {"error": f"Cannot create output directory: {exc}"}

            saved = []
            for idx in range(total):
                writer = pypdf.PdfWriter()
                writer.add_page(reader.pages[idx])
                out_file = out_dir / f"{path.stem}_page{idx + 1:04d}.pdf"
                with open(out_file, "wb") as f:
                    writer.write(f)
                saved.append(str(out_file))

            return {
                "file": str(path),
                "total_pages": total,
                "output_dir": str(out_dir),
                "files": saved,
            }
    except Exception as exc:
        return {"error": f"Could not split PDF: {exc}"}


def rotate_pdf(
    path_str: str, degrees: int, output_str: str, pages_spec: str | None = None
) -> dict:
    """Rotate pages in a PDF by 90, 180, or 270 degrees."""
    if degrees not in VALID_ROTATIONS:
        return {"error": f"Invalid rotation. Must be one of: {sorted(VALID_ROTATIONS)}"}

    path = resolve_path(path_str)
    err = require_file(path, PDF_EXTENSIONS)
    if err:
        return {"error": err}

    output = resolve_path(output_str)
    err = ensure_output_dir(output)
    if err:
        return {"error": err}

    try:
        reader = pypdf.PdfReader(str(path))
        total = len(reader.pages)

        if pages_spec:
            indices = parse_page_ranges(pages_spec, total)
            if isinstance(indices, str):
                return {"error": indices}
            rotate_set = set(indices)
        else:
            rotate_set = set(range(total))

        writer = pypdf.PdfWriter()
        for idx, page in enumerate(reader.pages):
            if idx in rotate_set:
                page.rotate(degrees)
            writer.add_page(page)

        with open(output, "wb") as f:
            writer.write(f)

        return {
            "file": str(path),
            "degrees": degrees,
            "pages_rotated": sorted(i + 1 for i in rotate_set),
            "output": str(output),
        }
    except Exception as exc:
        return {"error": f"Could not rotate PDF: {exc}"}
