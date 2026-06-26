---
name: less-tool
description: View file contents with interactive scrolling and search. Use for reading log files, code, and large text documents with pagination.
---
# Less - Interactive File Viewer

View file contents with forward and backward scrolling, search functionality, and line number navigation. Supports large files by loading only the viewed portion into memory.

## Usage

```bash
less-tool [options] <file>
```

## Navigation

- `Space`: Forward one page
- `b`: Back one page
- `j/k`: Scroll up/down one line
- `/pattern`: Search forward
- `?pattern`: Search backward
- `n`: Next match
- `q`: Quit

## Examples

```bash
less-tool large_log.txt
less-tool -N script.py
```