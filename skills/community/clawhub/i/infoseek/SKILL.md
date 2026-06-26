---
name: infoseek-en
description: >
  Deep web information search and archival skill for comprehensive research on persons,
  organizations, or products. Uses multiple search engines (Baidu, Tavily, Multi-Search-Engine)
  plus browser-based content extraction. Features URL-normalized deduplication with SQLite database,
  structured file storage with complete metadata, ad/content filtering, and customizable output
  formats (md/json/txt/csv/xlsx/html/docx). Automatically creates organized folders per subject.
  Enforces strict deletion policy (recycle bin only, user confirmation required).
  Use when: user needs comprehensive information gathering, background research, due diligence,
  media monitoring, competitive intelligence, or building information archives about specific subjects.
  Triggers: infoseek, deep search, information gathering, background check, media monitoring,
  archive search, research person, research company, competitive analysis, dossier building.
metadata:
  openclaw:
    requires:
      bins: [python3]
    primaryEnv: OPENCLAW_WORKSPACE
---

# InfoSeek - Deep Web Search & Archival

## Overview

InfoSeek performs comprehensive web research on any subject (person, organization, product) across multiple search engines, deduplicates results, extracts clean content, and archives everything with full metadata in organized folders.

## Prerequisites

Before executing a search task, verify these skills are installed:

```python
import os
from pathlib import Path

workspace = os.environ.get('OPENCLAW_WORKSPACE')
skills_dir = Path(workspace) / 'skills'

required = ['baidu-search', 'tavily', 'Multi-Search-Engine', 'agent-browser-clawdbot-0.1.0']
missing = [s for s in required if not (skills_dir / s).exists()]
```

If any are missing, instruct the user to install them:
```bash
openclaw skills install baidu-search
openclaw skills install tavily-search
openclaw skills install multi-search-engine
```

## Workflow

### Phase 0: Task Setup

1. **Confirm the search subject** — name, organization, or product
2. **Collect optional context** — background info, time range, output format (default: .md), special requirements
3. **Check dependencies** — run the prerequisite check above
4. **Create archive folder** — run:
   ```bash
   python scripts/infoseek_helper.py create-folder "<subject_name>"
   ```

### Phase 1: Multi-Engine Deep Search

Execute searches across all available engines. Each engine runs independently.

#### 1.1 Baidu Search (100+ pages)

Use the baidu-search skill:
- Query: `"<subject> <background_context>"`
- Depth: 100+ pages
- Record: URL, title, website name, publish date for each result

#### 1.2 Tavily Search

Use tavily_search tool:
```
query: "<subject> <background_context>"
search_depth: advanced
max_results: 50
```

#### 1.3 Multi-Search-Engine

Use the multi-search-engine skill across multiple engines simultaneously.

#### 1.4 Browser Deep-Crawl

For discovered URLs, use the browser tool to:
1. Open each page
2. Extract body content (filter ads, sidebars, comments)
3. Extract metadata: title, author, editor, date, website name

### Phase 2: Deduplication

Run URL deduplication on all collected results:
```bash
python scripts/infoseek_helper.py deduplicate "<temp_results_file>"
```

The script normalizes URLs (remove www, tracking params, unify http/https, remove trailing slashes) and checks against the SQLite database to skip duplicates.

### Phase 3: Content Extraction & Storage

For each unique URL:

1. **Extract content** using the browser tool — get title, body, metadata
2. **Filter content** — remove ads, sidebars, navigation, comments, related articles, footers
3. **Generate filename**:
   ```bash
   python scripts/infoseek_helper.py generate-filename \
     --date "<YYYYMMDD>" --title "<title>" --website "<site>" --format "<ext>"
   ```
   Format: `YYYYMMDD-title-website.ext`
4. **Save the file**:
   ```bash
   python scripts/infoseek_helper.py save-content \
     --folder "<archive_path>" --filename "<name>" --url "<url>" \
     --website "<site>" --source "<source>" --date "<date>" \
     --title "<title>" --author "<author>" --editor "<editor>" \
     --content "<body>" --task "<subject>"
   ```
5. **Record in database**:
   ```bash
   python scripts/infoseek_helper.py add-url \
     --url "<normalized_url>" --task "<subject>" --filename "<name>"
   ```

### Phase 4: Task Report

Output a summary when complete:
```
InfoSeek Task Report
====================
Subject: {query}
Engines used: {engines}
Total found: {total} | Duplicates skipped: {dupes} | New archived: {new}
Files saved: {count}
Location: {path}
Database records: {db_total}
```

## File Naming

Format: `YYYYMMDD-title-website.ext`

- Date: 8 digits (YYYYMMDD) from page metadata
- Title: page title (strip special chars `<>:"/\|?*`)
- Website: domain or media name
- Extension: md (default), json, txt, csv, xlsx, html, docx

If filename exists, append 8-char hash to prevent overwrites.

## Output Formats

All formats include full metadata (URL, website, source, date, title, author, editor) plus body content.

- **.md** — Markdown with metadata table
- **.json** — Structured JSON with metadata object and content field
- **.txt** — Plain text with header metadata
- **.csv** — One row per article, all metadata as columns
- **.xlsx** — Excel spreadsheet with metadata columns
- **.html** — Styled HTML page with metadata table
- **.docx** — Word document with metadata paragraph

## Storage Structure

```
{workspace}/
├── infoseek-archives/
│   ├── <subject_1>/
│   │   ├── 20260404-title-website.md
│   │   └── ...
│   └── <subject_2>/
└── infoseek/
    ├── infoseek.db          # SQLite dedup database
    ├── infoseek.log         # Operation log
    └── backups/
```

## Deletion Policy

**Strict data retention — no permanent deletes without confirmation.**

| Operation | Confirmation | Method |
|-----------|-------------|--------|
| Bulk folder delete | Required | Move to recycle bin |
| Single file delete | Required | Move to recycle bin |
| Dedup skip | Automatic | Skip only, no delete |
| Database cleanup | Required | Mark as deleted |

**Process:**
1. List files to delete (name, URL, date)
2. Ask user: "Confirm deletion? Files go to recycle bin and can be recovered."
3. On confirmation, move to recycle bin (Windows: PowerShell, Mac/Linux: system trash)
4. Update database, log the deletion, confirm to user

**Never:**
- Delete without user consent
- Permanently delete (bypass recycle bin)
- Delete without logging
- Delete without updating database

## Configuration

Override defaults in task instructions:
- **Search depth**: default 100 pages, specify e.g. "150 pages"
- **Time range**: default unlimited, specify e.g. "2020-01-01 to 2026-04-07"
- **Output format**: default md, specify e.g. "xlsx"
- **Storage path**: default `{workspace}/infoseek-archives/`, specify custom path

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Missing search skill | `openclaw skills install <name>` |
| Date extraction fails | Check page metadata; use `00000000` for unknown |
| Encoding errors | Ensure UTF-8; on Windows enable Unicode UTF-8 in region settings |
| Database corruption | `python scripts/infoseek_helper.py restore-backup` |

## Security & Privacy

- All searches use public channels only
- No personal data stored — only search results
- SQLite database is local, never uploaded
- Deletions use system recycle bin (recoverable)
- All operations logged and auditable
- No telemetry, no external data transmission

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 2.0.0 | 2026-04-07 | Full rewrite: SQLite dedup, URL normalization, HTML parsing, multi-engine integration |
| 1.0.0 | 2026-04-06 | Initial version (deprecated) |
