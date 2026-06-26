# pyright: reportMissingImports=false
import shutil
from constants import (
    BIN_FFMPEG,
    BIN_LIBREOFFICE,
    BIN_PANDOC,
    BIN_PDFIMAGES,
    BIN_PDFTOTEXT,
    BIN_TESSERACT,
    PYTHON_PACKAGES,
)
from utils import is_binary_available


def run_doctor() -> dict:
    """Check availability of all optional system binaries and Python packages."""
    system_tools = [
        {
            "binary": BIN_PDFTOTEXT,
            "label": "pdftotext (poppler)",
            "purpose": "Faster text extraction fallback",
            "install": "brew install poppler  /  apt install poppler-utils",
        },
        {
            "binary": BIN_PDFIMAGES,
            "label": "pdfimages (poppler)",
            "purpose": "Required for OCR — extracts page images",
            "install": "brew install poppler  /  apt install poppler-utils",
        },
        {
            "binary": BIN_TESSERACT,
            "label": "tesseract",
            "purpose": "Required for OCR command",
            "install": "brew install tesseract  /  apt install tesseract-ocr",
        },
        {
            "binary": BIN_FFMPEG,
            "label": "ffmpeg",
            "purpose": "Required for TTS → MP3 conversion",
            "install": "brew install ffmpeg  /  apt install ffmpeg",
        },
        {
            "binary": BIN_PANDOC,
            "label": "pandoc",
            "purpose": "Document format conversion",
            "install": "brew install pandoc  /  apt install pandoc",
        },
        {
            "binary": BIN_LIBREOFFICE,
            "label": "libreoffice",
            "purpose": "Document format conversion (alternative to pandoc)",
            "install": "brew install --cask libreoffice  /  apt install libreoffice",
        },
    ]

    python_status = []
    for pkg in PYTHON_PACKAGES:
        # Normalise package name to importable module name
        module = pkg.replace("-", "_").replace("python_", "").replace("_tts", "_tts")
        # Special cases
        module_map = {
            "pypdf": "pypdf",
            "pdfplumber": "pdfplumber",
            "reportlab": "reportlab",
            "python_docx": "docx",
            "edge_tts": "edge_tts",
            "pillow": "PIL",
        }
        mod_name = module_map.get(pkg.replace("-", "_"), pkg.replace("-", "_"))
        try:
            __import__(mod_name)
            available = True
        except ImportError:
            available = False
        python_status.append({"package": pkg, "available": available})

    system_status = []
    for tool in system_tools:
        path = shutil.which(tool["binary"])
        system_status.append(
            {
                "label": tool["label"],
                "binary": tool["binary"],
                "available": path is not None,
                "path": path or "",
                "purpose": tool["purpose"],
                "install": tool["install"],
            }
        )

    return {"python": python_status, "system": system_status}
