#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dependency detection and installation utilities.
"""

import importlib.util
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


IS_WIN = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"
PY = Path(__file__).parent.parent.parent / ".venv" / "Scripts" / "python.exe"
if not PY.exists():
    import sys
    PY = Path(sys.executable)


def pip_install(package: str) -> bool:
    """Install a Python package using pip."""
    python = Path(sys.executable)
    try:
        subprocess.run(
            [str(python), "-m", "pip", "install", package],
            check=True, capture_output=True, timeout=120
        )
        return True
    except Exception:
        return False


def is_pandoc() -> bool:
    """Check if pandoc is installed."""
    if shutil.which("pandoc"):
        return True
    if IS_WIN and Path(r"C:\Program Files\Pandoc\pandoc.EXE").exists():
        return True
    if IS_MAC and Path("/usr/local/bin/pandoc").exists():
        return True
    return False


def is_markitdown_class() -> bool:
    """Check if markitdown Python class is available."""
    try:
        from markitdown import MarkItDown
        return True
    except Exception:
        return False


def is_mammoth() -> bool:
    """Check if mammoth is installed."""
    return importlib.util.find_spec("mammoth") is not None


def is_latexocr() -> bool:
    """Check if pix2tex (LaTeX-OCR) is installed."""
    return importlib.util.find_spec("pix2tex") is not None


def is_rapidocr() -> bool:
    """Check if RapidOCR is installed."""
    return importlib.util.find_spec("rapidocr_onnxruntime") is not None


def is_pdf2image() -> bool:
    """Check if pdf2image is installed."""
    return importlib.util.find_spec("pdf2image") is not None


def is_markitdown_cli() -> bool:
    """Check if markitdown CLI is available."""
    if shutil.which("markitdown"):
        return True
    if IS_WIN:
        scripts_dir = Path(PY).parent / "Scripts"
        if (scripts_dir / "markitdown.exe").exists():
            return True
        if (scripts_dir / "markitdown.cmd").exists():
            return True
    return False


def is_beautifulsoup() -> bool:
    """Check if beautifulsoup4 is installed."""
    return importlib.util.find_spec("bs4") is not None


def find_poppler() -> Optional[str]:
    """Find poppler installation path on Windows."""
    if not IS_WIN:
        return None
    
    candidates = [
        Path(r"C:\Program Files\poppler\Library\bin"),
        Path(r"C:\Program Files (x86)\poppler\Library\bin"),
        Path(r"C:\poppler\Library\bin"),
        Path.home() / "scoop" / "apps" / "poppler" / "current" / "Library" / "bin",
    ]
    
    for p in candidates:
        if (p / "pdftoppm.exe").exists():
            return str(p)
    
    return None