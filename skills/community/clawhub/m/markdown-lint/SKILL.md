---
name: markdown-lint
description: Check markdown files for common issues including heading structure, link validity, list formatting, trailing whitespace, and code block language tags. Use when reviewing documentation, README files, or any .md file for consistency and best practices.
metadata:
  openclaw:
    emoji: 📝
    requires:
      bins: []
---

# Markdown Lint Skill

Static analysis for markdown files. Detects structural issues, broken links,
and formatting inconsistencies before they become review comments.

## When to use it

- Reviewing a README or docs file before committing
- Auditing a docs directory for consistency
- CI gate for markdown quality
- Onboarding a new repo and wanting a quick health check

## Quick start

```bash
# Lint a single file
node /path/to/markdown-lint/scripts/lint.mjs README.md

# Lint a directory (recursive)
node /path/to/markdown-lint/scripts/lint.mjs ./docs/

# JSON output for automation
node /path/to/markdown-lint/scripts/lint.mjs README.md --format json

# Fix safe issues automatically
node /path/to/markdown-lint/scripts/lint.mjs README.md --fix
```

## What it checks

| Check | What it detects |
|---|---|
| `heading-order` | Skipped heading levels (e.g. h1 → h3) |
| `code-lang` | Fenced code blocks without a language tag |
| `trailing-ws` | Trailing whitespace on lines |
| `multiple-h1` | More than one top-level heading |
| `blank-lines` | Missing blank lines around headings/lists |
| `link-text` | Bare URLs without link text |
| `list-indent` | Inconsistent list indentation |
| `hr-style` | Mixed horizontal rule styles |

## Exit codes

- `0` — all checks passed
- `1` — lint errors found
- `2` — file not found or read error

## Output format

Text (default):

```
README.md
  12:3  error  heading-order    Expected h2, got h3 (skips h2)
  28:1  error  multiple-h1      Multiple H1 headings found
  35:0  warn   trailing-ws      Trailing whitespace

2 errors, 1 warning
```

JSON:

```json
{
  "file": "README.md",
  "errors": [
    {"line": 12, "col": 3, "rule": "heading-order", "message": "Expected h2, got h3"}
  ],
  "warnings": [
    {"line": 35, "col": 0, "rule": "trailing-ws", "message": "Trailing whitespace"}
  ],
  "summary": {"errors": 1, "warnings": 1}
}
```

## Fixable rules

`--fix` automatically resolves:

- `trailing-ws` — strips trailing whitespace
- `blank-lines` — inserts missing blank lines
- `list-indent` — normalizes list indentation to 2 spaces

Non-fixable rules (like `heading-order`, `multiple-h1`) are reported but
not auto-corrected.

## Adding custom rules

Create a file `rules.json` in the same directory as the script:

```json
{
  "maxLineLength": 120,
  "requiredHeadings": ["Installation", "Usage", "License"]
}
```

The script reads `rules.json` if present and applies additional checks.
