---
name: md-toc
description: Generate a table of contents (TOC) for any Markdown file by extracting its ATX headings (# .. ######). Use when you need a navigable outline of a long README, notes file, or doc before summarizing or editing it.
metadata:
  {
    "openclaw":
      { "emoji": "📑", "requires": { "bins": ["bash"] } }
  }
---

# md-toc

Generates a Markdown table of contents from the ATX headings in a file.

## When to use

- Building a TOC for a README or long notes file.
- Getting a quick outline of a document before editing or summarizing.
- Verifying heading structure during a doc review.

## Prerequisites

- The target file must be UTF-8 text with ATX headings (`#`, `##`, ...).
- A POSIX shell (`bash`/`sh`) and `awk` must be available.

## Usage

```bash
bash scripts/md-toc.sh path/to/file.md
bash scripts/md-toc.sh path/to/file.md --max 3   # cap heading depth
```

Output is a Markdown list with relative anchor links, printed to stdout.

## Notes

- Headings inside fenced code blocks are skipped.
- The script exits non-zero if the file is missing or unreadable.
