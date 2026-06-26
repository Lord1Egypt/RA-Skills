# Backends package
from backends.pandoc import convert_with_pandoc, install_pandoc, is_pandoc
from backends.markitdown import convert_with_markitdown, convert_pdf_with_ocr
from backends.mammoth import convert_with_mammoth

__all__ = [
    "convert_with_pandoc",
    "install_pandoc", 
    "is_pandoc",
    "convert_with_markitdown",
    "convert_pdf_with_ocr",
    "convert_with_mammoth",
]