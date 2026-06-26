---
name: markdown-linter
description: Lint Markdown files for formatting issues, broken links, and style consistency.
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
      python:
        - markdown
        - requests
---

# Markdown Linter

## What This Does

A CLI tool to lint Markdown files for common formatting issues, style consistency, and broken links. Helps maintain documentation quality by catching errors before publication.

Key features:
- **Header hierarchy validation** - ensure proper nesting (no skipped levels)
- **Image alt text checking** - flag images without descriptive alt text
- **Internal link validation** - check that internal links (within same doc) point to existing anchors
- **Line length checking** - warn about lines exceeding configurable length (default 80 chars)
- **Trailing whitespace detection** - find and report trailing spaces/tabs
- **List consistency** - ensure consistent list markers (-, *, +) within same document
- **Code block language** - recommend adding language specification to code blocks
- **Empty link detection** - flag links with empty text or URLs
- **Duplicate headers** - warn about duplicate header text within same file
- **External link checking** - optionally validate external URLs (requires network)

## How To Use

Run the skill with:
```bash
./scripts/main.py run --input path/to/file.md
```

Or lint multiple files:
```bash
./scripts/main.py run --input "*.md"
```

### Options

- `--input`: Path to Markdown file(s) (supports glob patterns)
- `--max-line-length`: Maximum allowed line length (default: 80)
- `--check-external-links`: Enable external URL validation (default: false)
- `--ignore-rules`: Comma-separated list of rule IDs to ignore

### Output

Returns JSON with linting results:
```json
{
  "file": "example.md",
  "issues": [
    {
      "line": 10,
      "column": 1,
      "rule": "MD001",
      "severity": "warning",
      "message": "Header levels should only increment by one level at a time",
      "fix": "Change ## to #"
    }
  ],
  "summary": {
    "total_issues": 5,
    "errors": 2,
    "warnings": 3
  }
}
```

## Limitations

- External link checking requires network connectivity and may be slow
- Readability scores are not currently implemented
- Some Markdown extensions (tables, footnotes) may not be fully validated
- Large files (>10k lines) may take longer to process
- Anchor detection for internal links works only for simple anchor patterns

## Examples

Basic linting:
```bash
./scripts/main.py run --input README.md
```

With custom line length:
```bash
./scripts/main.py run --input docs/*.md --max-line-length 100
```

With external link validation:
```bash
./scripts/main.py run --input "**/*.md" --check-external-links
```

## Rule Reference

- **MD001**: Header hierarchy violation
- **MD002**: Missing image alt text
- **MD003**: Broken internal link
- **MD004**: Line too long
- **MD005**: Trailing whitespace
- **MD006**: Inconsistent list markers
- **MD007**: Code block missing language
- **MD008**: Empty link
- **MD009**: Duplicate header
- **MD010**: Broken external link (if enabled)