#!/usr/bin/env python3
"""Extract text from academic papers (PDF, DOCX, TXT) with section detection."""

import sys
import os
import re
import json
from pathlib import Path

# Section detection patterns
SECTION_PATTERNS = {
    'abstract': r'(?:abstract|摘要)\s*[\n\r]+',
    'introduction': r'(?:introduction|intro|背景|引言)\s*[\n\r]+',
    'methods': r'(?:methods|methodology|materials?\s+and\s+methods|方法|材料与方法)\s*[\n\r]+',
    'results': r'(?:results|发现|结果)\s*[\n\r]+',
    'discussion': r'(?:discussion|讨论)\s*[\n\r]+',
    'conclusion': r'(?:conclusion|conclusions|结论)\s*[\n\r]+',
    'references': r'(?:references|bibliography|参考文献)\s*[\n\r]+',
    'acknowledgments': r'(?:acknowledgments?|acknowledgements?|致谢)\s*[\n\r]+',
    'supplementary': r'(?:supplementary|supporting|补充材料)\s*[\n\r]+',
}


def detect_sections(text):
    """Detect paper sections and return structured content."""
    sections = {}
    current_pos = 0
    
    # Find all section headers and their positions
    section_positions = []
    for section_name, pattern in SECTION_PATTERNS.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            section_positions.append((match.start(), match.end(), section_name))
    
    # Sort by position
    section_positions.sort()
    
    # Extract content between sections
    for i, (start, end, name) in enumerate(section_positions):
        if i + 1 < len(section_positions):
            next_start = section_positions[i + 1][0]
            sections[name] = text[end:next_start].strip()
        else:
            sections[name] = text[end:].strip()
    
    return sections


def extract_pdf(path):
    """Extract text from PDF using multiple methods."""
    text = ""
    errors = []
    
    # Method 1: pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text, None
    except ImportError:
        errors.append("pdfplumber not installed")
    except Exception as e:
        errors.append(f"pdfplumber failed: {e}")
    
    # Method 2: PyMuPDF
    try:
        import fitz
        doc = fitz.open(path)
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        if text.strip():
            return text, None
    except ImportError:
        errors.append("PyMuPDF not installed")
    except Exception as e:
        errors.append(f"PyMuPDF failed: {e}")
    
    # Method 3: OCR fallback
    try:
        from pdf2image import convert_from_path
        import pytesseract
        images = convert_from_path(path)
        for image in images:
            text += pytesseract.image_to_string(image, lang='chi_sim+eng') + "\n"
        if text.strip():
            return text, None
    except ImportError:
        errors.append("OCR tools not installed (pdf2image, pytesseract)")
    except Exception as e:
        errors.append(f"OCR failed: {e}")
    
    if text.strip():
        return text, "; ".join(errors) if errors else None
    return "[ERROR: Could not extract text from PDF]", "; ".join(errors)


def extract_docx(path):
    """Extract text from DOCX."""
    try:
        from docx import Document
        doc = Document(path)
        return "\n".join([para.text for para in doc.paragraphs]), None
    except ImportError:
        return "[ERROR: python-docx not installed]", "python-docx not installed"
    except Exception as e:
        return f"[ERROR: Could not read DOCX: {e}]", str(e)


def extract_txt(path):
    """Extract text from TXT."""
    encodings = ['utf-8', 'gbk', 'latin-1']
    errors = []
    for encoding in encodings:
        try:
            with open(path, 'r', encoding=encoding) as f:
                return f.read(), None
        except UnicodeDecodeError:
            errors.append(f"Failed with {encoding}")
        except Exception as e:
            errors.append(f"Error with {encoding}: {e}")
    return "[ERROR: Could not decode TXT file]", "; ".join(errors)


def extract(paper_path, structured=False):
    """Route to appropriate extractor based on file extension."""
    path = Path(paper_path)
    ext = path.suffix.lower()
    
    if ext == '.pdf':
        text, error = extract_pdf(path)
    elif ext == '.docx':
        text, error = extract_docx(path)
    elif ext == '.txt':
        text, error = extract_txt(path)
    else:
        return f"[ERROR: Unsupported file format: {ext}]"
    
    if structured and not text.startswith("[ERROR:"):
        sections = detect_sections(text)
        result = {
            'full_text': text,
            'sections': sections,
            'metadata': {
                'file': str(path),
                'format': ext.lstrip('.'),
                'size': path.stat().st_size,
                'extraction_error': error
            }
        }
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    return text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: extract_paper.py <paper_path> [--structured]", file=sys.stderr)
        sys.exit(1)
    
    paper_path = sys.argv[1]
    structured = '--structured' in sys.argv
    
    result = extract(paper_path, structured=structured)
    # Write to stdout with UTF-8 encoding to avoid Windows console issues
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(result)
