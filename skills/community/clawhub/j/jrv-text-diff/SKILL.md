---
name: jrv-text-diff
description: Compare two text files or strings side-by-side or unified. Highlights additions, deletions, and changes with color. Supports word-level diff, ignore-whitespace, and JSON/YAML structural diff modes.
---

# jrv-text-diff

Compare two texts, files, or code snippets and show exactly what changed. Supports unified diff, side-by-side view, word-level highlighting, and structural diff for JSON/YAML.

## Quick Start

```bash
# Compare two files
python3 scripts/text_diff.py file1.txt file2.txt

# Compare inline strings
python3 scripts/text_diff.py --text "hello world" --text2 "hello there"

# Unified diff (patch format)
python3 scripts/text_diff.py file1.txt file2.txt --format unified

# Side-by-side comparison
python3 scripts/text_diff.py file1.txt file2.txt --format side-by-side

# Word-level diff
python3 scripts/text_diff.py file1.txt file2.txt --word-diff

# Ignore whitespace
python3 scripts/text_diff.py file1.txt file2.txt --ignore-whitespace

# JSON structural diff
python3 scripts/text_diff.py data1.json data2.json --format json

# YAML structural diff
python3 scripts/text_diff.py config1.yaml config2.yaml --format yaml

# Output diff as JSON report
python3 scripts/text_diff.py file1.txt file2.txt --output-json
```

## Commands

| Command | Description |
|---------|-------------|
| `text_diff.py <file1> <file2>` | Compare two files (default: unified diff) |
| `--text <str> --text2 <str>` | Compare two inline strings |
| `--format unified` | Unified patch-style diff output |
| `--format side-by-side` | Two-column comparison |
| `--format context` | Context diff (like diff -c) |
| `--format json` | Structural JSON diff |
| `--format yaml` | Structural YAML diff |
| `--word-diff` | Highlight word-level changes within lines |
| `--ignore-whitespace` | Ignore leading/trailing whitespace |
| `--ignore-case` | Case-insensitive comparison |
| `--context N` | Lines of context (default: 3) |
| `--output-json` | Output diff stats as JSON |
| `--no-color` | Disable ANSI color output |

## Use Cases

- **Code review**: See exactly what changed between two versions of a config or script
- **Config auditing**: Spot differences between prod and staging configs
- **JSON/YAML diffs**: Structural comparison ignoring key ordering
- **Copy editing**: Word-level diff for prose documents
- **CI pipelines**: JSON output for programmatic diff analysis

## Exit Codes

- `0` — Files are identical
- `1` — Files differ
- `2` — Error (file not found, parse error, etc.)
