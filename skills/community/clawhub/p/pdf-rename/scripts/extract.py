#!/usr/bin/env python3
"""
Stage 1: Extract metadata from all PDFs in a folder → manifest.json
"""
from pypdf import PdfReader
import os, re, json

MANIFEST_PATH = os.path.join(os.path.dirname(__file__), 'manifest.json')


def sanitize(name):
    return re.sub(r'[<>:"/\\|?*]', ' ', name).strip()


def extract_first_page_text(path):
    try:
        reader = PdfReader(path)
        if reader.pages:
            return reader.pages[0].extract_text()[:4000] or None
    except:
        pass
    return None


def extract_title(text):
    """Extract title from PDF first page. Fallback: filename."""
    if not text:
        return None
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for line in lines[:6]:
        if len(line) < 15:
            continue
        if any(line.lower().startswith(x) for x in ['http', 'www', 'arxiv:', 'doi:', 'figure', 'abstract']):
            continue
        if re.match(r'^\d+\s*$', line):
            continue
        if sum(1 for c in line if c in '©§¶†') > 0:
            continue
        return line
    return None


def extract_year(text, filename):
    """Extract year: filename prefix (most reliable) > PDF text conference pattern."""
    # From filename prefix: 2018Title, 2020_Name
    fn_year = re.search(r'^(19\d{2}|20\d{2})(?=[A-Z(])', filename)
    if fn_year:
        y = int(fn_year.group(1))
        if 2000 <= y <= 2029:
            return fn_year.group(1), 'filename'
    # From PDF text: NeurIPS 2022, arXiv:2023
    if text:
        m = re.search(r'(NeurIPS|NIPS|ICML|ICLR|IJCAI|AAAI)\s+20(\d{2})', text, re.I)
        if m:
            return '20' + m.group(2), 'pdf_text'
        m2 = re.search(r'arXiv[:.\-]?(\d{4})', text, re.I)
        if m2:
            y = int(m2.group(1))
            if 2000 <= y <= 2029:
                return m2.group(1), 'pdf_text'
    return None, None


VENUE_KEYWORDS = {
    'NeurIPS': ['neurips', 'nips\n', 'neural information processing'],
    'ICML': ['icml\n', 'international conference on machine learning'],
    'ICLR': ['iclr\n', 'international conference on learning representations'],
    'AAAI': ['aaai\n', 'association for the advancement'],
    'IJCAI': ['ijcai\n', 'international joint conference on artificial intelligence'],
    'arXiv': ['arxiv'],
    'J. Theory Biol.': ['j. theory biol'],
    'J. Dyn. Games': ['dyn. games', 'j. dyn. games'],
    'Cambridge': ['cambridge university press'],
}


def extract_venue(text):
    if not text:
        return None
    t = text.lower()
    for venue, kws in VENUE_KEYWORDS.items():
        if any(k in t for k in kws):
            return venue
    return None


def run(folder):
    pdfs = sorted([f for f in os.listdir(folder) if f.lower().endswith('.pdf')])
    manifest = []
    for fname in pdfs:
        path = os.path.join(folder, fname)
        text = extract_first_page_text(path)
        title = extract_title(text)
        year, year_src = extract_year(text, fname)
        venue = extract_venue(text)

        notes = []
        if not title:
            notes.append('title=filename')
        if not year:
            notes.append('year=manual')
        if not venue:
            notes.append('venue=manual')

        status = 'needs_verification' if title else 'manual_review'

        manifest.append({
            'filename': fname,
            'filepath': path,
            'title': title,
            'title_source': 'pdf_text' if title else 'filename',
            'year': year,
            'year_source': year_src,
            'venue': venue,
            'venue_source': 'pdf_text' if venue else None,
            'status': status,
            'notes': '; '.join(notes),
            'is_duplicate': False,
            'duplicate_group': None,
        })

    # Mark duplicates by normalized title
    title_idx = {}
    for i, m in enumerate(manifest):
        norm = re.sub(r'[^a-z0-9]', '', m.get('title', '').lower())
        if norm:
            if norm not in title_idx:
                title_idx[norm] = []
            title_idx[norm].append(i)

    for indices in title_idx.values():
        if len(indices) > 1:
            grp = str(indices)
            for idx in indices:
                manifest[idx]['is_duplicate'] = True
                manifest[idx]['duplicate_group'] = grp

    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f'[OK] {len(manifest)} files processed → {MANIFEST_PATH}')
    for m in manifest:
        icon = '✅' if m['status'] == 'needs_verification' else '⚠️'
        dup = ' [DUP]' if m['is_duplicate'] else ''
        print(f'  {icon} {m["filename"]}')
        print(f'      title={m["title"] or "N/A"} year={m["year"] or "???"} venue={m["venue"] or "???"}{dup}')
    return manifest


if __name__ == '__main__':
    import sys
    folder = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    run(folder)
