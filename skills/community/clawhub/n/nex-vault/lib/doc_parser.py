"""
Nex Vault - Document text extraction and date parsing
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import re
import subprocess
import datetime as dt
from pathlib import Path
from config import (
    DATE_PATTERNS, AUTO_RENEWAL_KEYWORDS, TERMINATION_KEYWORDS,
    MAX_TEXT_LENGTH, CLAUSE_TYPES
)


def extract_text(file_path):
    """Extract text from PDF, DOCX, TXT, or scanned images."""
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()

    try:
        if suffix == '.pdf':
            return _extract_pdf(file_path)
        elif suffix == '.docx':
            return _extract_docx(file_path)
        elif suffix == '.txt':
            return _extract_txt(file_path)
        elif suffix in ['.jpg', '.jpeg', '.png']:
            return _extract_image(file_path)
        else:
            return ""
    except Exception as e:
        print(f"Warning: Could not extract text from {file_path}: {e}")
        return ""


def _extract_pdf(file_path):
    """Extract text from PDF using pdftotext."""
    try:
        result = subprocess.run(
            ['pdftotext', str(file_path), '-'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout[:MAX_TEXT_LENGTH]
        else:
            # Fallback to OCR for scanned PDFs
            return _extract_image(file_path)
    except FileNotFoundError:
        print("Warning: pdftotext not found. Install with: apt-get install poppler-utils")
        return ""
    except Exception:
        return ""


def _extract_docx(file_path):
    """Extract text from DOCX using python-docx or zipfile."""
    try:
        from docx import Document
        doc = Document(file_path)
        text = '\n'.join([p.text for p in doc.paragraphs])
        return text[:MAX_TEXT_LENGTH]
    except ImportError:
        # Fallback: DOCX is ZIP-based
        try:
            import zipfile
            import xml.etree.ElementTree as ET
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                xml_content = zip_ref.read('word/document.xml')
            root = ET.fromstring(xml_content)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            text = '\n'.join([
                t.text for t in root.findall('.//w:t', ns) if t.text
            ])
            return text[:MAX_TEXT_LENGTH]
        except Exception:
            return ""
    except Exception:
        return ""


def _extract_txt(file_path):
    """Extract text from plain text file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()[:MAX_TEXT_LENGTH]
    except Exception:
        return ""


def _extract_image(file_path):
    """Extract text from image using OCR (tesseract)."""
    try:
        result = subprocess.run(
            ['tesseract', str(file_path), 'stdout'],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return result.stdout[:MAX_TEXT_LENGTH]
    except FileNotFoundError:
        print("Warning: tesseract not found. Install with: apt-get install tesseract-ocr")
    except Exception:
        pass
    return ""


def parse_dates(text):
    """Find all dates in text with context. Returns list of {date, context, type}."""
    dates_found = []

    for pattern in DATE_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            date_str = match.group(0)
            # Try to parse the date
            parsed_date = _parse_date_string(date_str)
            if parsed_date:
                # Get surrounding context (50 chars before and after)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()

                # Guess date type based on context
                date_type = _guess_date_type(context, text, match.start())

                dates_found.append({
                    'date': parsed_date.isoformat(),
                    'context': context,
                    'type': date_type,
                })

    # Remove duplicates
    seen = set()
    unique_dates = []
    for d in dates_found:
        key = (d['date'], d['type'])
        if key not in seen:
            seen.add(key)
            unique_dates.append(d)

    return sorted(unique_dates, key=lambda x: x['date'])


def detect_auto_renewal(text):
    """Detect auto-renewal clauses."""
    text_lower = text.lower()

    for keyword in AUTO_RENEWAL_KEYWORDS:
        if keyword in text_lower:
            # Find the clause text around the keyword
            idx = text_lower.find(keyword)
            start = max(0, idx - 100)
            end = min(len(text), idx + 300)
            clause_text = text[start:end]

            # Try to extract renewal period
            renewal_period = _extract_renewal_period(clause_text)

            return {
                'has_auto_renewal': True,
                'clause_text': clause_text,
                'renewal_period': renewal_period,
            }

    return {
        'has_auto_renewal': False,
        'clause_text': None,
        'renewal_period': None,
    }


def detect_termination_notice(text):
    """Find termination notice period required."""
    text_lower = text.lower()

    for keyword in TERMINATION_KEYWORDS:
        if keyword in text_lower:
            idx = text_lower.find(keyword)
            start = max(0, idx - 100)
            end = min(len(text), idx + 300)
            clause_text = text[start:end]

            # Try to extract number of days
            notice_days = _extract_notice_days(clause_text)

            if notice_days:
                return {
                    'notice_days': notice_days,
                    'clause_text': clause_text,
                }

    return {
        'notice_days': None,
        'clause_text': None,
    }


def extract_parties(text):
    """Extract party names from contract headers."""
    parties = []

    # Common patterns in contracts
    patterns = [
        r"between\s+([A-Z][A-Za-z\s&,]+?)\s+and\s+([A-Z][A-Za-z\s&,]+?)\s*(?:agreement|contract|agreement|hereby)",
        r"tussen\s+([A-Z][A-Za-z\s&,]+?)\s+en\s+([A-Z][A-Za-z\s&,]+?)\s*(?:overeenkomst|contract|partijen)",
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            for i in range(1, len(match.groups()) + 1):
                party = match.group(i).strip()
                if party and len(party) < 100:
                    parties.append(party)

    # Also look for company names (CAPS pattern)
    caps_pattern = r"\b([A-Z][A-Z\s&,]{2,}(?:Inc|Ltd|GmbH|NV|BVBA|BV|LLC|Corp|Company|AG))\b"
    matches = re.finditer(caps_pattern, text)
    for match in matches:
        party = match.group(1).strip()
        if party not in parties and len(party) < 100:
            parties.append(party)

    return list(set(parties))[:10]  # Return top 10 unique parties


def extract_key_clauses(text):
    """Find and extract important clauses."""
    clauses = []

    # Simple keyword matching for different clause types
    clause_patterns = {
        'termination': [
            r"(?:termination|terminating|terminate|terminated|opzeg|beëindig)[^.!?]{20,300}(?:\.|!|\?)",
        ],
        'renewal': [
            r"(?:renewal|renew|renewed|verlenging|vernieuwd)[^.!?]{20,300}(?:\.|!|\?)",
        ],
        'payment': [
            r"(?:payment|fee|charge|price|cost|betaling|prijs|tarief)[^.!?]{20,300}(?:\.|!|\?)",
        ],
        'liability': [
            r"(?:liability|liable|liable for|aansprakelijkheid)[^.!?]{20,300}(?:\.|!|\?)",
        ],
        'confidentiality': [
            r"(?:confidential|confidentiality|geheim|vertrouwelijk)[^.!?]{20,300}(?:\.|!|\?)",
        ],
    }

    for clause_type, patterns in clause_patterns.items():
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                clause_text = match.group(0).strip()
                if len(clause_text) > 50:
                    clauses.append({
                        'type': clause_type,
                        'text': clause_text[:500],
                    })

    return clauses


def calculate_notice_deadline(end_date, notice_days):
    """Calculate when you must give notice (end_date - notice_days)."""
    if not end_date or not notice_days:
        return None

    try:
        end = dt.datetime.fromisoformat(end_date).date()
        deadline = end - dt.timedelta(days=notice_days)
        return deadline.isoformat()
    except (ValueError, TypeError):
        return None


def _parse_date_string(date_str):
    """Parse a date string in various formats."""
    date_str = date_str.strip()

    # Try ISO format
    try:
        return dt.datetime.fromisoformat(date_str).date()
    except ValueError:
        pass

    # Try DD/MM/YYYY or DD-MM-YYYY
    for sep in ['/', '-']:
        parts = date_str.split(sep)
        if len(parts) == 3:
            try:
                day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
                if 1 <= day <= 31 and 1 <= month <= 12 and year >= 1900:
                    return dt.date(year, month, day)
            except ValueError:
                pass

    # Try YYYY/MM/DD or YYYY-MM-DD
    for sep in ['/', '-']:
        parts = date_str.split(sep)
        if len(parts) == 3:
            try:
                year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                if 1 <= day <= 31 and 1 <= month <= 12 and year >= 1900:
                    return dt.date(year, month, day)
            except ValueError:
                pass

    return None


def _guess_date_type(context, full_text, position):
    """Guess if a date is start, end, renewal, or termination."""
    context_lower = context.lower()

    if any(w in context_lower for w in ['start', 'from', 'beginning', 'van', 'per']):
        return 'start'
    elif any(w in context_lower for w in ['end', 'until', 'through', 'tot', 'tot en met', 'expir']):
        return 'end'
    elif any(w in context_lower for w in ['renew', 'renewal', 'extend', 'verlenging', 'extension']):
        return 'renewal'
    elif any(w in context_lower for w in ['terminat', 'notice', 'opzeg']):
        return 'termination'
    else:
        return 'unknown'


def _extract_renewal_period(text):
    """Extract renewal period like '1 year', '12 months', etc."""
    pattern = r"(\d+)\s*(?:year|month|day|week|jaar|maand|dag|week)s?"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(0)
    return None


def _extract_notice_days(text):
    """Extract number of days from termination notice text."""
    # Look for "X days" pattern
    match = re.search(r"(\d+)\s*(?:days?|dag|dagen)", text, re.IGNORECASE)
    if match:
        return int(match.group(1))

    # Look for "X months" pattern (convert to days)
    match = re.search(r"(\d+)\s*(?:month|maand)s?", text, re.IGNORECASE)
    if match:
        return int(match.group(1)) * 30

    return None
