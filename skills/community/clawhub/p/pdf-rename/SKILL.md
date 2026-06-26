---
name: pdf-rename
description: Rename academic PDF papers to a standardized format "[Year] [Venue] Title.pdf" using a three-stage pipeline (Extract → Verify → Rename). Use when the user asks to organize, batch-rename, or metadata-enrich PDF files in a folder. Activates on keywords like "rename PDFs", "organize papers", "batch rename PDFs", "rename papers by metadata", "pdf重命名", "文献整理".
---

# PDF Rename — Academic Paper Organizer

Rename academic PDFs to: `[Year] [Venue] Title.pdf`

**Three-stage pipeline (strict order):**

```
Extract → Verify → Rename
```

**Anti-error principle:** Never re-parse PDF content during Rename stage. The Manifest is the single source of truth.

---

## Quick Start

```bash
# Stage 1: Extract metadata → generate manifest
python scripts/extract.py "<folder_path>"

# Stage 2: Verify (manual or web search), then inject verified data
#   → Edit scripts/VERIFIED_DATA dict with web-verified values
python scripts/apply_verified.py "<folder_path>"

# Stage 3: Preview rename plan
python scripts/execute.py "<folder_path>" --preview

# Execute rename (with backup)
python scripts/execute.py "<folder_path>" --execute
```

---

## Workflow Details

### Stage 1: Extract

`scripts/extract.py` reads every PDF in the folder and generates `manifest.json`.

For each PDF it extracts:
- **Title**: from PDF first-page text (heuristic: first non-metadata line)
- **Year**: from filename prefix (most reliable) or PDF text (conference-year pattern)
- **Venue**: inferred from PDF text (NeurIPS, ICML, arXiv, etc.)
- **Status**: `needs_verification` (title/year from auto-extraction)

**Manifest schema** — see `references/manifest_spec.md`

> ⚠️ PDF text extraction is unreliable for titles. Expected quality: filename > PDF text for title. Always verify with web search before executing rename.

### Stage 2: Verify

Before running rename, manually or via web search verify:
1. Title is correct (filename is often sufficient, but multi-word titles may differ)
2. Year is correct (arXiv submission year ≠ conference year)
3. Venue is correct

Inject verified data via `scripts/apply_verified.py`:
- Key = original filename (exact match)
- Value = `{'title', 'year', 'venue', 'confirmed': True}`

Set `confirmed: False` or omit entry for files to skip.

### Stage 3: Rename

`scripts/execute.py` reads manifest and renames files:
- **Status must be `ready`** to execute
- Duplicate titles → append `(1)`, `(2)`, etc.
- Files with status `needs_verification` or `manual_review` are **skipped**
- Backup is created automatically at `<folder>/_backup_YYYYMMDD_HHMMSS/`

---

## Key Design Decisions

| Problem | Solution |
|---------|----------|
| PDF title extraction garbled/incomplete | Use filename as primary title source; PDF text only for venue/year hints |
| Wrong year from arXiv ID vs conference year | Verify with web search; inject corrected year in `VERIFIED_DATA` |
| Duplicate papers (same content, different filenames) | Detect via title similarity; rename both with `(1)`, `(2)` suffixes |
| Accidental data loss | Always create timestamped backup before renaming |

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/extract.py` | Stage 1: extract PDF metadata → manifest.json |
| `scripts/apply_verified.py` | Stage 2: inject verified data into manifest |
| `scripts/execute.py` | Stage 3: rename files from manifest (preview or execute) |
| `scripts/find_duplicates.py` | Utility: detect near-duplicate titles in manifest |

---

## References

- `references/manifest_spec.md` — Full manifest JSON schema
- `references/venue_abbrev.md` — Standard venue abbreviation map
- `references/anti_patterns.md` — Common mistakes and how to avoid them
