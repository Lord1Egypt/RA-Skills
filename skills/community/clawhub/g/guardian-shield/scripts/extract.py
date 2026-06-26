"""
Guardian Shield — Text Extraction

Extracts text from various formats for scanning:
  - Plain text
  - HTML content
  - PDF files (requires PyPDF2)

Chunking is applied for large documents to keep scans efficient.

(c) Fallen Angel Systems LLC — All rights reserved.
"""

import re
import logging
from typing import List, Optional

logger = logging.getLogger("guardian-shield.extract")

# Chunk settings
DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 100
MAX_TEXT_LENGTH = 500_000  # 500KB hard cap


def extract_text(content: str, content_type: str = "text") -> str:
    """
    Extract readable text from content.

    Args:
        content: Raw content string
        content_type: One of "text", "html", "pdf_path"

    Returns:
        Extracted plain text
    """
    if content_type == "text":
        return _clean_text(content)

    if content_type == "html":
        return _extract_html(content)

    if content_type == "pdf_path":
        return _extract_pdf(content)

    return _clean_text(content)


def chunk_text(text: str, chunk_size: int = DEFAULT_CHUNK_SIZE,
               overlap: int = DEFAULT_CHUNK_OVERLAP) -> List[str]:
    """
    Split text into overlapping chunks for scanning.

    Args:
        text: Input text
        chunk_size: Target characters per chunk
        overlap: Characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if not text:
        return []

    # Truncate extremely long text
    if len(text) > MAX_TEXT_LENGTH:
        text = text[:MAX_TEXT_LENGTH]
        logger.warning(f"Text truncated to {MAX_TEXT_LENGTH} chars")

    # Short text doesn't need chunking
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size

        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence end in the last 20% of the chunk
            search_start = end - int(chunk_size * 0.2)
            sentence_end = _find_sentence_boundary(text, search_start, end)
            if sentence_end > 0:
                end = sentence_end

        chunks.append(text[start:end].strip())
        start = end - overlap

    return [c for c in chunks if c]


def _clean_text(text: str) -> str:
    """Basic text cleanup."""
    if not text:
        return ""
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove null bytes
    text = text.replace('\x00', '')
    return text.strip()


def _strip_html_basic(html: str) -> str:
    """Basic HTML tag stripping (free tier - no beautifulsoup)."""
    # Remove script and style tags with content
    text = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    # Remove all HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Decode common entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
    return _clean_text(text)


def _extract_html(html: str) -> str:
    """Full HTML extraction using BeautifulSoup (home tier)."""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements
        for element in soup(['script', 'style', 'head']):
            element.decompose()

        text = soup.get_text(separator=' ')
        return _clean_text(text)
    except ImportError:
        logger.warning("beautifulsoup4 not installed, falling back to basic extraction")
        return _strip_html_basic(html)


def _extract_pdf(pdf_path: str) -> str:
    """Extract text from PDF file (home tier)."""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        return _clean_text(' '.join(text_parts))
    except ImportError:
        logger.warning("PyPDF2 not installed, PDF extraction unavailable")
        return ""
    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        return ""


def _find_sentence_boundary(text: str, start: int, end: int) -> int:
    """Find the best sentence boundary in a text range."""
    # Look for period/question/exclamation followed by space
    for i in range(end - 1, start, -1):
        if text[i] in '.!?' and i + 1 < len(text) and text[i + 1] in ' \n\t':
            return i + 1
    # Fall back to newline
    for i in range(end - 1, start, -1):
        if text[i] == '\n':
            return i + 1
    return -1
