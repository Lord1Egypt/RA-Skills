#!/usr/bin/env python3
"""
PDF text extraction using PyMuPDF + pdfplumber.
Handles both text-based PDFs and scanned PDFs (detected by absence of text layer).
"""

import io
import os
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Any

import fitz  # PyMuPDF
import pdfplumber


@dataclass
class PDFExtractResult:
    """Result of PDF text extraction."""
    full_text: str
    tables: List[List[List[str]]]  # List of tables, each table is list of rows
    page_count: int
    is_scanned: bool  # True if no text layer found (needs OCR)
    page_texts: List[str]  # Text per page
    metadata: Dict[str, Any]  # PDF metadata


def extract_pdf_text(pdf_path: str, password: Optional[str] = None) -> PDFExtractResult:
    """
    Extract text and tables from a PDF file.

    Uses PyMuPDF for fast text extraction and pdfplumber for table extraction.
    Automatically detects if a PDF is scanned (no text layer).

    Args:
        pdf_path: Path to the PDF file.
        password: Optional password for encrypted PDFs.

    Returns:
        PDFExtractResult with full_text, tables, page_count, is_scanned, page_texts, metadata.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Step 1: Try PyMuPDF for text extraction
    page_texts = []
    full_text_parts = []
    metadata = {}

    try:
        doc = fitz.open(pdf_path)
        if doc.is_encrypted and password:
            doc.authenticate(password)

        metadata = {
            "title": doc.metadata.get("title", ""),
            "author": doc.metadata.get("author", ""),
            "subject": doc.metadata.get("subject", ""),
            "creator": doc.metadata.get("creator", ""),
            "producer": doc.metadata.get("producer", ""),
            "creation_date": doc.metadata.get("creationDate", ""),
        }

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            page_texts.append(text)
            full_text_parts.append(text)

        doc.close()

    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF with PyMuPDF: {e}")

    full_text = "\n".join(full_text_parts)

    # Step 2: Detect if scanned (no text layer)
    is_scanned = len(full_text.strip()) < 50  # Very little text = likely scanned

    # Step 3: Extract tables with pdfplumber
    tables = []
    try:
        with pdfplumber.open(pdf_path, password=password or "") as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                if page_tables:
                    # pdfplumber returns list of tables per page
                    for table in page_tables:
                        if table:
                            tables.append(table)
    except Exception as e:
        # Table extraction failure is non-fatal
        pass

    result = PDFExtractResult(
        full_text=full_text,
        tables=tables,
        page_count=len(page_texts),
        is_scanned=is_scanned,
        page_texts=page_texts,
        metadata=metadata,
    )

    return result


def extract_page_text(pdf_path: str, page_num: int, password: Optional[str] = None) -> str:
    """
    Extract text from a specific page of a PDF.

    Args:
        pdf_path: Path to the PDF file.
        page_num: 0-based page number.
        password: Optional password for encrypted PDFs.

    Returns:
        Text content of the specified page.
    """
    try:
        doc = fitz.open(pdf_path)
        if doc.is_encrypted and password:
            doc.authenticate(password)

        if page_num < 0 or page_num >= len(doc):
            raise IndexError(f"Page {page_num} out of range (0-{len(doc)-1})")

        page = doc[page_num]
        text = page.get_text()
        doc.close()
        return text

    except Exception as e:
        raise RuntimeError(f"Failed to extract page {page_num}: {e}")


def extract_tables_from_page(pdf_path: str, page_num: int, password: Optional[str] = None) -> List[List[List[str]]]:
    """
    Extract tables from a specific page of a PDF.

    Args:
        pdf_path: Path to the PDF file.
        page_num: 0-based page number.
        password: Optional password for encrypted PDFs.

    Returns:
        List of tables, each table is a list of rows (each row is a list of cell strings).
    """
    tables = []
    try:
        with pdfplumber.open(pdf_path, password=password or "") as pdf:
            if page_num < 0 or page_num >= len(pdf.pages):
                raise IndexError(f"Page {page_num} out of range")

            page = pdf.pages[page_num]
            page_tables = page.extract_tables()
            if page_tables:
                tables = [t for t in page_tables if t]
    except Exception as e:
        raise RuntimeError(f"Failed to extract tables from page {page_num}: {e}")

    return tables


def get_pdf_info(pdf_path: str) -> Dict[str, Any]:
    """
    Get basic PDF information without full text extraction.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Dictionary with page_count, is_encrypted, metadata.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    info = {
        "page_count": len(doc),
        "is_encrypted": doc.is_encrypted,
        "metadata": dict(doc.metadata),
    }
    doc.close()
    return info


def render_page_as_image(pdf_path: str, page_num: int, dpi: int = 300) -> bytes:
    """
    Render a PDF page as an image (for OCR processing).

    Args:
        pdf_path: Path to the PDF file.
        page_num: 0-based page number.
        dpi: Resolution for rendering (default 300 DPI for OCR).

    Returns:
        PNG image data as bytes.
    """
    try:
        doc = fitz.open(pdf_path)
        if page_num < 0 or page_num >= len(doc):
            raise IndexError(f"Page {page_num} out of range")

        page = doc[page_num]
        mat = fitz.Matrix(dpi / 72, dpi / 72)  # Scale for DPI
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img_data = pix.tobytes("png")
        doc.close()
        return img_data

    except Exception as e:
        raise RuntimeError(f"Failed to render page {page_num} as image: {e}")


def save_page_as_image(pdf_path: str, page_num: int, output_path: str, dpi: int = 300) -> None:
    """
    Render a PDF page as an image file.

    Args:
        pdf_path: Path to the PDF file.
        page_num: 0-based page number.
        output_path: Path to save the output image.
        dpi: Resolution for rendering.
    """
    img_data = render_page_as_image(pdf_path, page_num, dpi)
    with open(output_path, "wb") as f:
        f.write(img_data)
