"""Parse BibTeX (.bib) files and Zotero exports into Paper objects.

Supports:
- Standard .bib files
- Zotero BibTeX export
- Zotero CSL-JSON export (.json)

Field mapping:
  title    -> Paper.title
  author   -> Paper.authors (split on " and ")
  year     -> Paper.year
  doi      -> Paper.doi
  url      -> Paper.url
  abstract -> Paper.abstract
  eprint/arxivid -> Paper.arxiv_id
"""

import json
import re
import sys
from typing import List, Optional, Tuple

from schemas import Paper


# ---------------------------------------------------------------------------
# BibTeX parsing (no external dependency)
# ---------------------------------------------------------------------------

def _parse_bibtex_entries(text: str) -> List[dict]:
    """Parse BibTeX text into a list of entry dicts."""
    entries = []
    # Match @type{key, ... }
    # We need to handle nested braces
    pattern = re.compile(r'@(\w+)\s*\{([^,]*),', re.IGNORECASE)
    pos = 0
    while pos < len(text):
        m = pattern.search(text, pos)
        if not m:
            break
        entry_type = m.group(1).lower()
        entry_key = m.group(2).strip()
        # Find the matching closing brace
        start = m.end()
        depth = 1
        i = start
        while i < len(text) and depth > 0:
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
            i += 1
        body = text[start:i - 1] if depth == 0 else text[start:]
        # Parse fields
        fields = _parse_bibtex_fields(body)
        fields['_type'] = entry_type
        fields['_key'] = entry_key
        entries.append(fields)
        pos = i

    return entries


def _parse_bibtex_fields(body: str) -> dict:
    """Extract key=value pairs from a BibTeX entry body."""
    fields = {}
    # Match field = {value} or field = "value" or field = number
    i = 0
    while i < len(body):
        # Skip whitespace and commas
        while i < len(body) and body[i] in ' \t\n\r,':
            i += 1
        if i >= len(body):
            break
        # Find field name
        match = re.match(r'(\w+)\s*=\s*', body[i:])
        if not match:
            i += 1
            continue
        field_name = match.group(1).lower()
        i += match.end()
        if i >= len(body):
            break
        # Parse value
        value, consumed = _parse_bibtex_value(body[i:])
        fields[field_name] = value
        i += consumed
    return fields


def _parse_bibtex_value(text: str) -> Tuple[str, int]:
    """Parse a BibTeX value starting at the current position.
    Returns (value_string, chars_consumed)."""
    text = text.lstrip()
    if not text:
        return "", 0
    offset = len(text) - len(text.lstrip())

    if text[0] == '{':
        # Brace-delimited value
        depth = 1
        i = 1
        while i < len(text) and depth > 0:
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
            i += 1
        value = text[1:i - 1] if depth == 0 else text[1:]
        return _clean_bibtex_value(value), i
    elif text[0] == '"':
        # Quote-delimited value
        i = 1
        while i < len(text) and text[i] != '"':
            if text[i] == '\\':
                i += 1  # skip escaped char
            i += 1
        value = text[1:i]
        return _clean_bibtex_value(value), i + 1
    else:
        # Bare number or string
        m = re.match(r'(\S+)', text)
        if m:
            return m.group(1).strip(','), m.end()
        return "", 0


def _clean_bibtex_value(value: str) -> str:
    """Clean up a BibTeX value: remove extra braces, LaTeX commands."""
    # Remove nested braces (common in titles)
    value = re.sub(r'\{([^{}]*)\}', r'\1', value)
    # Remove common LaTeX commands
    value = re.sub(r'\\textit\{([^}]*)\}', r'\1', value)
    value = re.sub(r'\\textbf\{([^}]*)\}', r'\1', value)
    value = re.sub(r'\\emph\{([^}]*)\}', r'\1', value)
    value = re.sub(r'\\[a-zA-Z]+\s*', '', value)  # remove remaining commands
    # Clean up whitespace
    value = re.sub(r'\s+', ' ', value).strip()
    return value


def parse_bibtex(text: str) -> List[Paper]:
    """Parse BibTeX text and return a list of Paper objects."""
    entries = _parse_bibtex_entries(text)
    papers = []
    for entry in entries:
        if entry.get('_type') in ('string', 'comment', 'preamble'):
            continue

        title = entry.get('title', '').strip()
        if not title:
            continue

        # Parse authors
        author_str = entry.get('author', '')
        authors = [a.strip() for a in author_str.split(' and ') if a.strip()] if author_str else []

        # Parse year
        year = None
        year_str = entry.get('year', '')
        if year_str:
            m = re.search(r'(\d{4})', year_str)
            if m:
                year = int(m.group(1))

        # Extract identifiers
        doi = entry.get('doi', '').strip() or None
        url = entry.get('url', '').strip() or None
        abstract = entry.get('abstract', '').strip() or None

        # arXiv ID
        arxiv_id = None
        eprint = entry.get('eprint', '') or entry.get('arxivid', '')
        if eprint:
            arxiv_id = eprint.strip()
        elif url and 'arxiv.org' in url:
            m = re.search(r'(\d{4}\.\d{4,5})', url)
            if m:
                arxiv_id = m.group(1)

        # Generate ID
        if arxiv_id:
            paper_id = f"ARXIV:{arxiv_id}"
        elif doi:
            paper_id = f"DOI:{doi}"
        else:
            paper_id = f"bib:{entry.get('_key', title[:30])}"

        papers.append(Paper(
            id=paper_id,
            title=title,
            authors=authors,
            year=year,
            doi=doi,
            url=url,
            abstract=abstract,
            arxiv_id=arxiv_id,
            source="bibtex",
            is_seed=True,
        ))

    print(f"[bibtex] Parsed {len(papers)} papers from BibTeX", file=sys.stderr)
    return papers


def parse_bibtex_file(path: str) -> List[Paper]:
    """Parse a .bib file and return Paper objects."""
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    return parse_bibtex(text)


# ---------------------------------------------------------------------------
# Zotero CSL-JSON parsing
# ---------------------------------------------------------------------------

def parse_csl_json(text: str) -> List[Paper]:
    """Parse Zotero CSL-JSON export and return Paper objects."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"[csl-json] Failed to parse JSON: {e}", file=sys.stderr)
        return []

    if isinstance(data, dict):
        # Some exports wrap items in a top-level object
        data = data.get('items', [data])

    papers = []
    for item in data:
        if not isinstance(item, dict):
            continue

        title = item.get('title', '').strip()
        if not title:
            continue

        # Authors
        authors = []
        for a in item.get('author', []):
            if isinstance(a, dict):
                parts = [a.get('given', ''), a.get('family', '')]
                name = ' '.join(p for p in parts if p).strip()
                if name:
                    authors.append(name)

        # Year
        year = None
        issued = item.get('issued', {})
        if isinstance(issued, dict):
            date_parts = issued.get('date-parts', [[]])
            if date_parts and date_parts[0]:
                try:
                    year = int(date_parts[0][0])
                except (ValueError, IndexError):
                    pass

        # Identifiers
        doi = item.get('DOI', '').strip() or None
        url = item.get('URL', '').strip() or None
        abstract = item.get('abstract', '').strip() or None

        arxiv_id = None
        if url and 'arxiv.org' in (url or ''):
            m = re.search(r'(\d{4}\.\d{4,5})', url)
            if m:
                arxiv_id = m.group(1)

        if arxiv_id:
            paper_id = f"ARXIV:{arxiv_id}"
        elif doi:
            paper_id = f"DOI:{doi}"
        else:
            paper_id = f"csl:{item.get('id', title[:30])}"

        papers.append(Paper(
            id=paper_id,
            title=title,
            authors=authors,
            year=year,
            doi=doi,
            url=url,
            abstract=abstract,
            arxiv_id=arxiv_id,
            source="zotero_csl",
            is_seed=True,
        ))

    print(f"[csl-json] Parsed {len(papers)} papers from CSL-JSON", file=sys.stderr)
    return papers


def parse_csl_json_file(path: str) -> List[Paper]:
    """Parse a Zotero CSL-JSON file and return Paper objects."""
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return parse_csl_json(text)


# ---------------------------------------------------------------------------
# Auto-detect and parse
# ---------------------------------------------------------------------------

def parse_file(path: str) -> List[Paper]:
    """Auto-detect file type and parse. Supports .bib and .json (CSL-JSON)."""
    lower = path.lower()
    if lower.endswith('.bib'):
        return parse_bibtex_file(path)
    elif lower.endswith('.json'):
        return parse_csl_json_file(path)
    else:
        # Try BibTeX first, then CSL-JSON
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()
        if text.lstrip().startswith('@') or '@article' in text.lower() or '@inproceedings' in text.lower():
            return parse_bibtex(text)
        else:
            return parse_csl_json(text)
