---
name: head-tool
description: Display the first lines of files. Use for quickly previewing file contents, checking headers, or sampling data.
---

# File Header Viewer

Output the beginning of files, defaulting to the first 10 lines. Essential for previewing log files, CSV headers, and large text files without loading them entirely.

## Usage

```bash
head-tool [options] [file...]
```

## Options

- `-n N`: Show first N lines (default: 10)
- `-c N`: Show first N bytes instead of lines
- `-q`: Quiet mode (suppress filename headers)
- Read from stdin when no file specified

## Examples

```bash
# Show first 10 lines
head-tool data.csv

# Show first 20 lines
head-tool -n 20 log.txt

# Show first 100 bytes
head-tool -c 100 config.yaml
```