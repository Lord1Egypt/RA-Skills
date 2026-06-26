"""Extract references from PDF papers — enhanced regex + optional GROBID.

Extraction pipeline:
  1. Try GROBID (if --use-grobid and Docker service is running) → structured XML
  2. Fallback: enhanced regex extraction from raw PDF text (PyMuPDF)
  3. Resolve extracted references via multi-source resolver (S2, CrossRef, OpenAlex)
"""
import re
import sys
import logging
from typing import List, Optional
from xml.etree import ElementTree as ET

from schemas import Paper, RawReference

logger = logging.getLogger(__name__)

# ── GROBID support (optional) ────────────────────────────


GROBID_URL = "http://localhost:8070/api/processFulltextDocument"


def _grobid_available() -> bool:
    """Check if GROBID service is running."""
    try:
        import httpx
        resp = httpx.get("http://localhost:8070/api/isalive", timeout=3)
        return resp.status_code == 200
    except Exception:
        return False


def _extract_via_grobid(path: str) -> List[RawReference]:
    """Use GROBID to extract structured references from a PDF."""
    import httpx
    refs = []
    try:
        with open(path, "rb") as f:
            resp = httpx.post(
                GROBID_URL,
                files={"input": (path, f, "application/pdf")},
                data={"consolidateCitations": "1"},
                timeout=120,
            )
        if resp.status_code != 200:
            print(f"[pdf] GROBID returned {resp.status_code}", file=sys.stderr)
            return []

        # Parse TEI XML
        ns = {"tei": "http://www.tei-c.org/ns/1.0"}
        root = ET.fromstring(resp.text)

        for bib in root.findall(".//tei:listBibl/tei:biblStruct", ns):
            ref = _parse_bibl_struct(bib, ns)
            if ref:
                refs.append(ref)

        print(f"[pdf] GROBID extracted {len(refs)} references", file=sys.stderr)
    except Exception as e:
        print(f"[pdf] GROBID failed: {e}", file=sys.stderr)
    return refs


def _parse_bibl_struct(bib, ns) -> Optional[RawReference]:
    """Parse a single <biblStruct> element into a RawReference."""
    # Title
    title_el = bib.find(".//tei:analytic/tei:title", ns)
    if title_el is None:
        title_el = bib.find(".//tei:monogr/tei:title", ns)
    title = title_el.text.strip() if title_el is not None and title_el.text else None

    # Authors
    authors = []
    for author in bib.findall(".//tei:analytic/tei:author/tei:persName", ns):
        first = author.findtext("tei:forename", "", ns).strip()
        last = author.findtext("tei:surname", "", ns).strip()
        name = f"{first} {last}".strip()
        if name:
            authors.append(name)

    # Year
    year = None
    date_el = bib.find(".//tei:monogr/tei:imprint/tei:date[@when]", ns)
    if date_el is not None:
        try:
            year = int(date_el.get("when", "")[:4])
        except (ValueError, TypeError):
            pass

    # DOI
    doi = None
    for idno in bib.findall(".//tei:idno[@type='DOI']", ns):
        if idno.text:
            doi = idno.text.strip()

    # arXiv
    arxiv_id = None
    for idno in bib.findall(".//tei:idno[@type='arXiv']", ns):
        if idno.text:
            arxiv_id = idno.text.strip()

    # Raw text
    raw = f"{', '.join(authors)}. {title or '(untitled)'}. {year or ''}"

    if not title and not doi and not arxiv_id:
        return None

    return RawReference(
        raw_text=raw.strip(),
        title=title,
        authors=authors,
        year=year,
        doi=doi,
        arxiv_id=arxiv_id,
    )


# ── Enhanced regex extraction ─────────────────────────────


def _dehyphenate(text: str) -> str:
    """Fix hyphenated line breaks: 'correspon-\\ndence' → 'correspondence'."""
    return re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)


def _extract_via_regex(text: str) -> List[RawReference]:
    """Enhanced regex extraction of references from PDF text."""
    # Find the reference section
    ref_text = _find_reference_section(text)
    if not ref_text:
        print("[pdf] Could not locate reference section, scanning full text", file=sys.stderr)
        ref_text = text

    # Fix hyphenated line breaks before splitting
    ref_text = _dehyphenate(ref_text)

    # Split into individual reference entries
    entries = _split_references(ref_text)

    refs = []
    for entry in entries[:80]:  # cap at 80 references
        ref = _parse_reference_entry(entry)
        if ref:
            refs.append(ref)

    print(f"[pdf] Regex extracted {len(refs)} references", file=sys.stderr)
    return refs


def _find_reference_section(text: str) -> Optional[str]:
    """Locate the reference section in the text."""
    # Case-insensitive single pass with all header variants
    pattern = re.compile(
        r'\n\s*(?:'
        r'References?|REFERENCES?|'
        r'Bibliography|BIBLIOGRAPHY|'
        r'Works?\s+Cited|WORKS?\s+CITED|'
        r'Cited\s+Literature|CITED\s+LITERATURE|'
        r'Literature\s+Cited|LITERATURE\s+CITED|'
        r'Cited\s+References?|CITED\s+REFERENCES?|'
        r'R\s*[eé]\s*f\s*[eé]\s*r\s*e\s*n\s*c\s*e\s*s?'  # spaced-out "References"
        r')\s*\n'
    )
    best_pos = None
    for match in pattern.finditer(text):
        pos = match.end()
        # Prefer the LAST occurrence (references are at the end)
        best_pos = pos

    if best_pos is not None:
        return text[best_pos:]
    return None


def _split_references(ref_text: str) -> List[str]:
    """Split reference section into individual entries.

    Tries multiple strategies in order:
      1. Bracketed numbers: [1] ... [2] ...
      2. Dot numbers: 1. ... 2. ...
      3. Author-year (ACL/NLP style): Name, ... Year. Title ...
      4. Blank-line separated paragraphs
    """
    MIN_ENTRIES = 3   # need at least this many to accept a strategy
    MIN_CHARS = 20    # ignore entries shorter than this

    def _clean(entries):
        return [e.strip() for e in entries if e.strip() and len(e.strip()) >= MIN_CHARS]

    # Strategy 1: Bracketed numbers  [1] ... [2] ...
    bracket_entries = re.split(r'\n\s*\[\d+\]\s*', ref_text)
    cleaned = _clean(bracket_entries)
    if len(cleaned) >= MIN_ENTRIES:
        return cleaned

    # Strategy 2: Dot numbers  1. Author ... 2. Author ...
    dot_entries = re.split(r'\n\s*(\d{1,3})\.\s+(?=[A-Z])', ref_text)
    if len(dot_entries) > MIN_ENTRIES:
        merged = []
        for i in range(1, len(dot_entries) - 1, 2):
            if i + 1 < len(dot_entries):
                merged.append(dot_entries[i + 1].strip())
        cleaned = _clean(merged)
        if len(cleaned) >= MIN_ENTRIES:
            return cleaned

    # Strategy 3: Author-year format (ACL/NLP style)
    # Pattern: a new reference starts when a line begins with an uppercase
    # letter (author surname) AND the previous reference contained a year.
    # Detect: "Surname, First" or "Surname and" at start of a new line,
    # which is NOT a continuation of the previous line.
    author_year = _split_author_year(ref_text)
    if len(author_year) >= MIN_ENTRIES:
        return _clean(author_year)

    # Strategy 4: Blank-line separated paragraphs
    para_entries = re.split(r'\n\s*\n', ref_text)
    cleaned = _clean(para_entries)
    if len(cleaned) >= MIN_ENTRIES:
        return cleaned

    # Last resort: treat entire ref_text as one entry (will likely fail)
    return _clean([ref_text])


def _split_author_year(ref_text: str) -> List[str]:
    """Split author-year formatted references (ACL/NeurIPS/EMNLP style).

    These references look like (after dehyphenation, lines joined):
        Alan Akbik, Duncan Blythe, and Roland Vollgraf.
        2018. Contextual string embeddings for sequence
        labeling. In Proceedings of the 27th ...
        Rami Al-Rfou, Dokook Choe, Noah Constant, ...
        2018. Character-level language ...

    Strategy: detect "Author. Year." boundaries using a regex that finds
    the pattern: sentence-ending punctuation, then a name-like token,
    then eventually a year followed by period.
    """
    # Join lines but keep newlines for boundary detection
    # First, try to detect the "Name. Year." pattern
    # We look for: (end of previous ref) (start of new ref = Author name)
    # Pattern: ".  Firstname Lastname" or similar at start of new ref

    # Approach: find all positions where "YEAR[a-z]?." appears,
    # then the text between consecutive year-markers is one reference.
    # But we need to handle the author block before the year.

    # Better approach: use a regex to find boundaries.
    # A boundary is where text like "1638–1649.\n" is followed by "Author Name"
    # Or: previous ref ends, new author name starts.

    # Most reliable: find all "YEAR." patterns and use them as anchors.
    # Each reference contains exactly one "YEAR. Title" pattern.

    # Split on the pattern: looks like end-of-ref followed by start-of-author
    # ".\nAuthorname" where the previous line ended a reference

    # Use a combined text approach
    combined = re.sub(r'\n', ' ', ref_text)
    combined = re.sub(r'\s+', ' ', combined).strip()

    # Find all "year." positions — these are key anchors
    year_positions = [(m.start(), m.end()) for m in
                      re.finditer(r'\b(19|20)\d{2}[a-z]?\.\s', combined)]

    if len(year_positions) < 2:
        return []

    # For each year position, we know "Author(s). Year. Title. Venue."
    # The author block is BEFORE the year. Find where each author block starts.
    # Strategy: for each year position, look backwards for the start of the
    # author block. The author block starts after the end of the previous reference.

    entries = []
    for i, (yr_start, yr_end) in enumerate(year_positions):
        # Find author block start: search backwards from yr_start for
        # the beginning of author names. The author block ends with ". Year."
        # and starts either at the beginning or after the previous ref's venue info.

        # Look for the last period-space before the author names
        # Authors are like: "Surname, First, Surname, First, and Surname, First."
        # So find the text segment: from after previous entry to current year.

        # For the first entry, start from the beginning
        if i == 0:
            entry_start = 0
        else:
            # Start from after the previous year's title+venue section
            # The previous entry ends somewhere before this entry's authors start
            # Heuristic: find the last ". " before the author block that looks
            # like end-of-venue (page numbers, publisher name, etc.)
            prev_yr_end = year_positions[i-1][1]
            # Search between prev_year_end and current yr_start for the boundary
            between = combined[prev_yr_end:yr_start]

            # The boundary is the last place where a venue/page-range ends
            # and author names begin. Look for patterns like:
            # "...pages 1234–5678. Author Name" or "...Linguistics. Author Name"
            # Find the last ". CapitalLetter" that starts an author name
            boundary_matches = list(re.finditer(
                r'\.\s+(?=[A-Z][a-z\u00c0-\u024f]+[\s,])', between))
            if boundary_matches:
                # Use the last boundary found
                entry_start = prev_yr_end + boundary_matches[-1].start() + 2  # skip ". "
            else:
                entry_start = prev_yr_end

        # Entry end: find the end of this reference's venue section
        # It's the text from yr_end to the start of the next author block
        if i < len(year_positions) - 1:
            next_yr_start = year_positions[i+1][0]
            # Find where next author block starts (similar logic)
            remaining = combined[yr_end:next_yr_start]
            boundary_matches = list(re.finditer(
                r'\.\s+(?=[A-Z][a-z\u00c0-\u024f]+[\s,])', remaining))
            if boundary_matches:
                entry_end = yr_end + boundary_matches[-1].start() + 1
            else:
                entry_end = next_yr_start
        else:
            entry_end = len(combined)

        entry = combined[entry_start:entry_end].strip()
        if len(entry) > 20:
            entries.append(entry)

    return entries


def _parse_reference_entry(entry: str) -> Optional[RawReference]:
    """Parse a single reference entry into a RawReference."""
    # Fix hyphenated line breaks BEFORE collapsing whitespace
    # "Neural Net-\nworks" → "Neural Networks"
    entry = re.sub(r'-\s*\n\s*', '', entry)
    # Collapse remaining whitespace
    entry = re.sub(r'\s+', ' ', entry).strip()
    if len(entry) < 15:
        return None

    # Extract DOI
    doi = None
    doi_match = re.search(r'10\.\d{4,}/[^\s,\]}>]+', entry)
    if doi_match:
        doi = doi_match.group().rstrip('.')

    # Extract arXiv ID
    arxiv_id = None
    arxiv_match = re.search(r'arXiv[:\s]*(\d{4}\.\d{4,5}(?:v\d+)?)', entry, re.IGNORECASE)
    if arxiv_match:
        arxiv_id = arxiv_match.group(1)

    # Extract year (4-digit number between 1900-2030)
    year = None
    year_matches = re.findall(r'\b(19\d{2}|20[0-3]\d)\b', entry)
    if year_matches:
        # Take the first year found (usually publication year in author-year format)
        year = int(year_matches[0])

    # Extract title — heuristic: text in quotes, or after authors before journal/venue
    title = _extract_title(entry, year)

    # Extract authors — text before the year or title
    authors = _extract_authors(entry, year)

    if not title and not doi and not arxiv_id:
        return None

    return RawReference(
        raw_text=entry[:300],
        title=title,
        authors=authors,
        year=year,
        doi=doi,
        arxiv_id=arxiv_id,
    )


def _extract_title(entry: str, year: Optional[int] = None) -> Optional[str]:
    """Try to extract the paper title from a reference entry.

    Handles multiple common citation styles:
      - Quoted title: "Title of the paper"
      - Author-year (ACL): Author. 2018. Title. In Venue ...
      - Numbered: [1] Author. Title. Venue, year.
      - Author (year): Author (2018). Title. Venue.
    """
    # Pattern 1: Title in quotes (IEEE, some CS styles)
    quoted = re.search(r'["\u201c]([^"\u201d]{10,250})["\u201d]', entry)
    if quoted:
        return quoted.group(1).strip()

    # Pattern 2: ACL/NLP style — "Author. Year. Title. In Venue" or "Author. Year. Title. arXiv"
    # e.g. "Jacob Devlin ... 2019. BERT: Pre-training of ... transformers. In Proceedings ..."
    if year:
        yr_str = str(year)
        # Match: year[a-z]?. Title (ends at "In ", "arXiv", "Proceedings", next period, etc.)
        acl_pat = re.compile(
            rf'{yr_str}[a-z]?\.\s+'           # "2018. " or "2018a. "
            r'([A-Z\d].+?)'                   # Title (non-greedy)
            r'(?:'
            r'\.\s+(?:In\s|Proceedings|arXiv|CoRR|Technical|Transactions|Journal|'
            r'(?:Ph\.?D\.?|Master\'?s?)\s+(?:thesis|dissertation)|'
            r'(?:ACL|EMNLP|NAACL|ICML|NeurIPS|ICLR|CVPR|AAAI|IJCAI|COLING|EACL|TACL|ACM|IEEE))'
            r'|$'                              # or end of string
            r')',
            re.IGNORECASE
        )
        m = acl_pat.search(entry)
        if m and len(m.group(1).strip()) >= 10:
            title = m.group(1).strip().rstrip('.')
            return title

    # Pattern 3: "Author (Year). Title." or "Author, Year. Title."
    paren_year = re.search(
        r'(?:\(\s*(?:19|20)\d{2}[a-z]?\s*\)|(?:19|20)\d{2}[a-z]?)[.)]*\s+'
        r'([A-Z\d][^.]{10,200})\.',
        entry
    )
    if paren_year:
        return paren_year.group(1).strip()

    # Pattern 4: After ". " — first sentence-like chunk starting with uppercase, > 10 chars
    sentences = re.findall(r'\.\s+([A-Z\d][^.]{10,200})\.', entry)
    if sentences:
        # Prefer the longest sentence as the likely title
        # But filter out venue-like strings (starting with "In ", "Proceedings")
        candidates = [s.strip() for s in sentences
                      if not re.match(r'^(?:In\s|Proceedings|pages?\s|pp\.)', s.strip())]
        if candidates:
            return max(candidates, key=len)
        return max(sentences, key=len).strip()

    # Pattern 5: Relaxed — any substantial text chunk between periods
    relaxed = re.findall(r'\.\s+([^.]{10,200})\.', entry)
    if relaxed:
        candidates = [s.strip() for s in relaxed if re.match(r'[A-Z\d]', s.strip())]
        if candidates:
            return max(candidates, key=len)

    return None


def _extract_authors(entry: str, year: Optional[int]) -> List[str]:
    """Try to extract author names from the beginning of a reference entry."""
    # Take text before the year
    if year:
        idx = entry.find(str(year))
        if idx > 0:
            author_text = entry[:idx].strip().rstrip('(,.')
        else:
            author_text = entry[:80]
    else:
        author_text = entry[:80]

    # Split by "and" or ","
    author_text = re.sub(r'\bet al\.?', '', author_text).strip()
    parts = re.split(r',\s*|\s+and\s+', author_text)
    authors = []
    for p in parts:
        p = p.strip().rstrip('.')
        # A name should have 2+ words, 3-40 chars
        if p and 3 <= len(p) <= 40 and ' ' in p and not any(c.isdigit() for c in p):
            authors.append(p)
    return authors[:10]


# ── Main entry point ──────────────────────────────────────


def extract_references(text: str) -> List[str]:
    """Legacy API — returns list of 'TYPE:value' strings."""
    refs = _extract_via_regex(text)
    result = []
    for ref in refs:
        if ref.doi:
            result.append(f"DOI:{ref.doi}")
        elif ref.arxiv_id:
            result.append(f"ARXIV:{ref.arxiv_id}")
        elif ref.title:
            result.append(f"TITLE:{ref.title}")
    return result


def parse_pdf(path: str, use_grobid: bool = False) -> dict:
    """Parse a PDF and extract + resolve references.

    Returns dict with raw_references, resolved_papers, unresolved_references,
    total_extracted, and resolve_rate.
    """
    import fitz
    doc = fitz.open(path)
    text = "".join(page.get_text() for page in doc)
    doc.close()

    # Extract references
    if use_grobid and _grobid_available():
        raw_refs = _extract_via_grobid(path)
    else:
        if use_grobid:
            print("[pdf] GROBID not available, falling back to regex", file=sys.stderr)
        raw_refs = _extract_via_regex(text)

    # Resolve via multi-source resolver
    from services.reference_resolver import resolve_references as multi_resolve
    resolved, unresolved = multi_resolve(raw_refs)

    total = len(raw_refs)
    return {
        "raw_references": [r.to_dict() for r in raw_refs],
        "resolved_papers": [p.to_dict() for p in resolved],
        "unresolved_references": unresolved,
        "total_extracted": total,
        "resolve_rate": len(resolved) / max(total, 1),
        "text_length": len(text),
    }
