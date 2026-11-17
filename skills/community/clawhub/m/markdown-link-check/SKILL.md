---
name: markdown-link-check
description: >
  Scan markdown files and verify that all hyperlinks (both local files and remote URLs) resolve correctly.
  Use when you need to: (1) verify documentation before publishing, (2) check a repo README or wiki links,
  (3) audit markdown files for broken links before generating static sites or releasing content,
  (4) validate links in collected digital assets before archiving.
---

# Markdown Link Check

Scan one or many markdown files and report every broken hyperlink with line numbers and diagnostic reasons.

## Quick Start

```bash
python3 scripts/check_links.py <file-or-directory>
```

Examples:
- Single file: `python3 scripts/check_links.py README.md`
- Whole directory: `python3 scripts/check_links.py ./docs --timeout 15`
- Verbose mode (shows healthy links too): `python3 scripts/check_links.py . -v`

## What It Checks

| Link type | Behavior |
|-----------|----------|
| Remote URLs (`http://`, `https://`) | Sends HEAD request, reports HTTP status or connection error |
| Local relative paths | Verifies file exists relative to the markdown file's directory |
| Anchors (`#section`) | Skipped (intra-file anchors are out of scope) |
| Image links (`![alt](url)`) | Skipped (use a dedicated asset checker for those) |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All links resolved successfully |
| 1 | Broken links found (details printed to stdout) |
| 2 | File/directory argument invalid or unreadable |

## Script Reference

`scripts/check_links.py` is a standalone Python 3 script with no external dependencies. It uses only the standard library (`urllib`, `pathlib`, `concurrent.futures`).

Key options:
- `--timeout N` — HTTP timeout per request in seconds (default 10)
- `-v, --verbose` — Print healthy link summary in addition to broken ones
