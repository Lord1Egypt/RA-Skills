---
name: md-formatter
description: Format and lint markdown files for consistency and readability. Use when Codex needs to normalize markdown documents, fix heading levels, standardize link formats, add missing alt text, or apply consistent formatting conventions across markdown files. Triggers include "format markdown", "clean up this md", "lint markdown", "normalize headings in this file".
---

# MD Formatter

Format and lint markdown files with consistent conventions.

## Quick Start

Run the formatter script on a file:

```bash
python3 scripts/format_md.py <file.md>
```

The script performs:

1. **Heading normalization**: Promote headings to start at `#`, ensure no level skips (e.g., `#` → `###`), convert `===`/`---` underlined headings to `#` style.
2. **Link formatting**: Convert `<https://url>` to `[url](https://url)` when appropriate, standardize bare URLs.
3. **Trailing whitespace**: Remove it.
4. **Bold/italic consistency**: Prefer `**bold**` over `__bold__`, `*italic*` over `_italic_`.
5. **Empty lines**: Ensure one blank line before and after headings and code blocks.

## Workflow

### 1. Inspect the file
Read the markdown file to understand its current state.

### 2. Run the formatter script
Execute `scripts/format_md.py` with the target path. Check the diff output.

### 3. Verify formatting
Read the formatted file to confirm changes are correct and no content was accidentally altered.

### 4. Iterate if needed
For complex documents, manually review or adjust formatting the script doesn't cover.

## References

See [references/heading-syntax.md](references/heading-syntax.md) for markdown heading specification details.