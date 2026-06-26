#!/usr/bin/env python3
# pyright: reportMissingImports=false

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pypdf",
#   "pdfplumber",
#   "reportlab",
#   "python-docx",
#   "edge-tts",
#   "pillow",
# ]
# ///
#
"""
PDF Toolkit - PDF manipulation, DOCX read/write, OCR, and text-to-speech.

Usage: main.py <command> [args...]
Run `main.py doctor` to see available commands and system tool status.
"""

import sys
from pathlib import Path

# Ensure sibling modules are importable regardless of the calling directory
sys.path.insert(0, str(Path(__file__).parent))

from service import dispatch, format_output


def main():
    """Entry point - dispatches to the appropriate command handler."""
    if len(sys.argv) < 2:
        print(
            "Usage: pdf-toolkit <command> [args...]\n"
            "\n"
            "Commands:\n"
            "  doctor          Show available tools and features\n"
            "  info            PDF metadata and page count\n"
            "  extract-text    Extract text from PDF\n"
            "  extract-tables  Extract tables from PDF\n"
            "  extract-images  Extract images from PDF\n"
            "  merge           Merge multiple PDFs\n"
            "  split           Split or slice a PDF\n"
            "  rotate          Rotate pages in a PDF\n"
            "  create-pdf      Create a PDF from text\n"
            "  read-docx       Read a DOCX file\n"
            "  write-docx      Write a DOCX file\n"
            "  ocr             OCR a scanned PDF (requires tesseract)\n"
            "  tts             Convert text/document to MP3 (requires ffmpeg)\n"
            "  convert         Convert document formats (requires pandoc/libreoffice)\n"
        )
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]
    result = dispatch(command, args)
    print(format_output(result))


if __name__ == "__main__":
    main()
