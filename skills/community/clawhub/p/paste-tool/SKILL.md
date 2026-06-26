---
name: paste-tool
description: Merge lines from multiple files side by side, creating columnar output. Use for combining data from separate sources into aligned tables.
---
# Paste - File Merging Utility

Merge corresponding lines from multiple files, separated by a configurable delimiter. Creates tabular output from separate data sources for comparison and combined analysis.

## Usage
```bash
paste-tool [options] <file1> <file2>...
```

## Options

- `-d sep`: Use custom delimiter (default: tab)
- `-s`: Serial merge (concatenate files sequentially instead of parallel)

## Examples

```bash
# Merge two files side by side
paste-tool names.txt scores.txt

# Use comma delimiter
paste-tool -d ',' col1.txt col2.txt col3.txt

# Serial merge
paste-tool -s file1.txt file2.txt
```