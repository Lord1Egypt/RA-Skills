---
name: pdf-rename
description: Rename academic PDF papers to a standardized format "[Year] [Venue] Title.pdf" using a three-stage pipeline (Extract → Verify → Rename). Use when the user asks to organize, batch-rename, or metadata-enrich PDF files in a folder. Activates on keywords like "rename PDFs", "organize papers", "batch rename PDFs", "rename papers by metadata", "pdf重命名", "文献整理".
---

# PDF Rename — Academic Paper Organizer

Rename academic PDFs to: `[Year] [Venue] Title.pdf`

**Three-stage pipeline:**

```
Extract → Verify → Rename
```

**Anti-error principle:** Never re-parse PDF content during Rename. The Manifest is the single source of truth.

---

## Quick Start

```bash
# Stage 1: Extract raw text → manifest.json
python scripts/extract.py "<folder_path>"

# Stage 2: LLM parses raw_text → inject verified data → manifest_verified.json
#   (Agent reads manifest.json raw_text field and writes to scripts/VERIFIED_DATA_*.py)
python scripts/apply_verified.py "<folder_path>"

# Stage 3: Preview / Execute
python scripts/execute.py "<folder_path>" --preview
python scripts/execute.py "<folder_path>" --execute
```

---

## Stage 1: Extract

**What it does:**
- Reads first 3 pages of each PDF
- Stores raw text in `manifest.json` → `raw_text` field
- Extracts `year_hint` from filename prefix
- Detects potential duplicates by filename similarity

**Manifest schema** — see `references/manifest_spec.md`

---

## Stage 2: Verify

The agent reads `manifest.json`, parses each `raw_text` field, and writes verified metadata.

**Steps:**
1. Read `manifest.json`
2. For each entry, parse the `raw_text` to extract: title, authors, venue, year, abstract
3. Create or update `scripts/VERIFIED_DATA_*.py` with verified entries

**VERIFIED_DATA format:**

```python
VERIFIED_DATA = {
    "OriginalFilename.pdf": {
        "title": "Correct Paper Title",
        "year": "2024",
        "venue": "NeurIPS",
        "confirmed": True   # must be True to be renamed
    },
}
```

**Rules:**
- Key must **exactly match** the original filename
- `confirmed: True` → status becomes `ready` → will be renamed
- `confirmed: False` or omitted → **skipped**
- Multiple `VERIFIED_DATA_*.py` files are auto-merged
- **Prefer venue/conference year over filename year** (e.g., arXiv 2022 → NeurIPS 2024)

**⚠️ Key gotchas during parsing:**
- Multi-line titles: pypdf concatenates lines without spaces (e.g., `"Direct score maximization outperformsplanning loss"`) — use context to infer correct split
- Journal refs at top of page: `"Math. Program. (2012) 133..."` is NOT the title — read further
- arXiv papers: use conference year if published, otherwise use arXiv year
- Non-paper files (book chapters, lecture notes, loss curves): set `confirmed: False` and skip

Then run:
```bash
python scripts/apply_verified.py "<folder_path>"
```

---

## Stage 3: Rename

- Only `status == 'ready'` files are renamed
- Duplicate titles → `(1)`, `(2)` suffixes
- Backup created at `<folder>/_backup_YYYYMMDD_HHMMSS/`

```bash
python scripts/execute.py "<folder_path>" --preview   # dry run
python scripts/execute.py "<folder_path>" --execute   # rename
```

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/extract.py` | Stage 1: extract raw PDF text → manifest.json |
| `scripts/apply_verified.py` | Stage 2: inject verified metadata → manifest_verified.json |
| `scripts/execute.py` | Stage 3: rename files (preview or execute) |
| `scripts/llm_parse.py` | (Optional) programmatic LLM parsing via gateway API |

---

## Known Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `raw_text` empty | PDF is a scan | Skip (`confirmed: False`) or manually determine metadata |
| Title extracted without spaces | pypdf concatenates lines | LLM infers from context; use filename as hint |
| Wrong year (arXiv ≠ conference) | Used filename year | Use venue year from `raw_text`, not filename |
| DOI/journal ref at top of page | Metadata precedes title | Read past it — title is usually after |
| Middle-dot author lines misidentified | `·` separator in names | LLM handles via semantic understanding |
| Non-paper files renamed | No filter applied | Set `confirmed: False` for non-papers |
| Windows filename encoding garbled | Chinese/non-ASCII chars in PowerShell | Use Python scripts, not manual file ops |
| Ligature artifacts | PDF encoding (e.g., `ﬁ` → `fi`) | `clean_title_text()` in extract.py handles these |

---

## References

- `references/manifest_spec.md` — Full manifest JSON schema
- `references/venue_abbrev.md` — Standard venue abbreviation map
