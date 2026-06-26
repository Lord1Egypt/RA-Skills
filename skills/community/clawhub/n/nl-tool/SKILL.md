---
name: nl-tool
description: Number lines of text files, showing line numbers alongside content. Use for reference, indexing, and code line numbering.
---
# NL - Line Numbering Utility

Add line numbers to text files. Supports configurable number formats, starting values, and numbering schemes. Useful for code review, document reference, and log analysis.

## Usage
```bash
nl-tool [options] <file>
```

## Options

- `-ba`: Number all lines (including blank)
- `-bt`: Number non-empty lines only (default)
- `-v N`: Start numbering from N
- `-i N`: Increment by N for each line

## Examples

```bash
# Number all lines including blanks
nl-tool -ba script.sh

# Start from 100
nl-tool -v 100 data.txt
```