# pyright: reportMissingImports=false
from pathlib import Path

import pypdf

from constants import PDF_EXTENSIONS
from utils import require_file, resolve_path


def get_pdf_info(path_str: str) -> dict:
    """Return metadata and page count for a PDF file."""
    path = resolve_path(path_str)
    err = require_file(path, PDF_EXTENSIONS)
    if err:
        return {"error": err}

    try:
        reader = pypdf.PdfReader(str(path))
        meta = reader.metadata or {}

        def clean(val):
            if val is None:
                return None
            s = str(val).strip()
            return s if s else None

        return {
            "file": str(path),
            "pages": len(reader.pages),
            "title": clean(meta.get("/Title")),
            "author": clean(meta.get("/Author")),
            "subject": clean(meta.get("/Subject")),
            "creator": clean(meta.get("/Creator")),
            "producer": clean(meta.get("/Producer")),
            "creation_date": clean(meta.get("/CreationDate")),
            "mod_date": clean(meta.get("/ModDate")),
            "encrypted": reader.is_encrypted,
            "file_size_kb": round(path.stat().st_size / 1024, 1),
        }
    except Exception as exc:
        return {"error": f"Could not read PDF: {exc}"}
