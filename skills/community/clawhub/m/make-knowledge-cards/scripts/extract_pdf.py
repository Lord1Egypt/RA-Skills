#!/usr/bin/env python3
"""Extract text from a PDF file for knowledge card generation.

Usage:
    python extract_pdf.py <pdf_file_path>

Output:
    Extracted text printed to stdout. Page breaks are marked with
    a separator line (--- Page N ---).

Exit codes:
    0 - Success (text extracted)
    1 - Usage error (no file path provided)
    2 - File not found or not a PDF
    3 - PDF is encrypted and cannot be read
    4 - No text could be extracted (possibly a scanned/image PDF)
"""

import sys
from pathlib import Path

from pypdf import PdfReader


def extract_pdf_text(pdf_path: str) -> str:
    """Extract text from all pages of a PDF file.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Concatenated text from all pages.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a PDF or is encrypted.
        RuntimeError: If no text could be extracted.
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {pdf_path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Not a PDF file: {pdf_path}")

    reader = PdfReader(str(path))

    # Check for encryption
    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception:
            raise ValueError(
                "PDF is encrypted with a password. "
                "Please decrypt it first and try again."
            )

    pages = []
    total_chars = 0

    for i, page in enumerate(reader.pages, 1):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""

        if text.strip():
            pages.append(f"--- Page {i} ---\n{text.strip()}")
            total_chars += len(text.strip())

    if total_chars == 0:
        raise RuntimeError(
            "No text could be extracted from this PDF. "
            "It may be a scanned document (images only). "
            "Please use OCR software to extract text first."
        )

    return "\n\n".join(pages)


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf.py <pdf_file_path>", file=sys.stderr)
        sys.exit(1)

    pdf_path = sys.argv[1]

    try:
        text = extract_pdf_text(pdf_path)
        print(text)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(3)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(4)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
