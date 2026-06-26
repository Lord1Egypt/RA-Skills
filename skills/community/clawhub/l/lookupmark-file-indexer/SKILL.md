---
name: file-indexer
description: >
  Fast filesystem catalog for finding files by name, date, type, or size.
  Indexes metadata only (no content). Uses SQLite for instant lookups.
  Triggers on "find file", "where is", "dov'è il file", "search file",
  "trova documento", "file più grandi", "recent files", "file modificati".
  NOT for: content-based search (use local-rag), sending files (use file-sender).
---

# File Indexer

Fast metadata-based file catalog. No content indexed — only filenames, sizes, dates, and extensions.

## Usage

```bash
# Build/rebuild the index (run once, or periodically)
python3 scripts/indexer.py --rebuild

# Update incrementally (fast — adds new, removes deleted)
python3 scripts/indexer.py --update

# Search by filename
python3 scripts/indexer.py --search "budget"

# Filter by extension
python3 scripts/indexer.py --search "report" --ext .pdf

# Filter by size
python3 scripts/indexer.py --search "" --min-size 10485760   # > 10MB

# Filter by date
python3 scripts/indexer.py --search "" --after 2026-03-01

# Index statistics
python3 scripts/indexer.py --stats
```

## Security

- **ALLOWED_ROOTS**: Only `~/Documenti` and `~/Scaricati` — same as RAG
- **BLOCKED_DIRS**: `.ssh`, `.gnupg`, `.config`, `credentials`, `.local`, `.cache`, `.Trash`
- **Zero content**: Only metadata (name, size, date, extension) — never reads file contents
- **No secrets**: Paths to sensitive dirs are never indexed
- **Local only**: SQLite DB at `~/.local/share/file-indexer/catalog.db`

## What Gets Indexed

| Yes | No |
|-----|-----|
| Filename | File contents |
| Extension | Full text |
| Size | Embeddings |
| Modified date | Preview |
| Directory path | Thumbnails |

## Automation

Add to cron or heartbeat for periodic updates:
```bash
python3 scripts/indexer.py --update
```

Works well alongside local-rag: use this for "where is that file?" and RAG for "what does that file say?"
