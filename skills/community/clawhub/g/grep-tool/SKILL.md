---
name: grep-tool
description: Search text files for lines matching a pattern using regular expressions. Use for log analysis, code searching, and data filtering.
---

# Pattern Search Utility

Search through files and output lines matching a given pattern. Supports basic, extended, and Perl-compatible regular expressions.

## Usage

```bash
grep-tool [options] <pattern> [file...]
```

## Common Options

- `-i`: Case-insensitive search
- `-r`: Recursive directory search
- `-n`: Show line numbers
- `-v`: Invert match (show non-matching lines)
- `-c`: Count matches instead of showing lines

## Examples

```bash
# Case-insensitive search
grep-tool -i "error" log.txt

# Recursive search
grep-tool -r "function" ./src

# Count matches
grep-tool -c "TODO" *.py
```