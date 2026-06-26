from __future__ import annotations

from pathlib import Path
from typing import Optional

from pypdf import PdfReader


def count_pages(path: Path) -> int:
    reader = PdfReader(str(path))
    return len(reader.pages)


def count_pages_safe(path: Path) -> Optional[int]:
    try:
        return count_pages(path)
    except Exception:
        return None
