#!/usr/bin/env python3
"""
Stage 1: Extract raw text from PDF first pages → manifest with raw_text field.
The LLM (or human) then reads raw_text to identify title/author/venue/year/abstract.
"""
from pypdf import PdfReader
import os, re, json

MANIFEST_PATH = os.path.join(os.path.dirname(__file__), 'manifest.json')


def sanitize(name):
    return re.sub(r'[<>:"/\\|?*]', ' ', name).strip()


def extract_pages_text(path, max_pages=3, max_chars_per_page=3000):
    """Extract text from first max_pages pages, concatenated."""
    try:
        reader = PdfReader(path)
        pages = reader.pages[:max_pages]
        texts = []
        for page in pages:
            text = page.extract_text() or ""
            texts.append(text[:max_chars_per_page])
        return "\n".join(texts)
    except Exception as e:
        return f"[ERROR reading PDF: {e}]"


def run(folder):
    pdfs = sorted([f for f in os.listdir(folder) if f.lower().endswith('.pdf')])
    manifest = []

    for fname in pdfs:
        path = os.path.join(folder, fname)
        raw_text = extract_pages_text(path)

        # Also try to extract filename year as hint
        fn_year = re.search(r'^(19\d{2}|20\d{2})(?=[A-Z(])', fname)
        year_hint = fn_year.group(1) if fn_year else None

        manifest.append({
            "filename": fname,
            "filepath": path,
            "year_hint": year_hint,
            "status": "needs_llm_review",
            "raw_text": raw_text,
            "is_duplicate": False,
            "duplicate_group": None,
            "title": None,
            "title_source": None,
            "year": year_hint,
            "year_source": "filename",
            "venue": None,
            "venue_source": None,
            "notes": "",
        })

    # Mark duplicates by normalized title (using filename as proxy)
    title_idx = {}
    for i, m in enumerate(manifest):
        # Use filename without year prefix as title proxy for dup detection
        fn = m["filename"]
        fn_without_year = re.sub(r'^(19|20)\d{2}\s*', '', fn).lower()
        norm = re.sub(r'[^a-z0-9]', '', fn_without_year.replace(".pdf",""))
        if norm:
            if norm not in title_idx:
                title_idx[norm] = []
            title_idx[norm].append(i)
    for indices in title_idx.values():
        if len(indices) > 1:
            grp = str(indices)
            for idx in indices:
                manifest[idx]["is_duplicate"] = True
                manifest[idx]["duplicate_group"] = grp

    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f'[OK] {len(manifest)} files -> {MANIFEST_PATH}')
    for m in manifest:
        preview = (m["raw_text"] or "")[:80].replace("\n", " ")
        print(f'  {m["filename"]}')
        print(f'    raw_text: {preview}...')

    return manifest


if __name__ == '__main__':
    import sys
    folder = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    run(folder)
