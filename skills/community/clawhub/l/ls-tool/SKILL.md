---
name: ls-tool
description: List directory contents with detailed file information. Use for browsing files, checking permissions, and examining directory structure.
---
# LS - Directory Listing Utility

List files and directories with configurable detail levels including file size, permissions, ownership, and timestamps.

## Usage

```bash
ls-tool [options] [path...]
```

## Options

- `-l`: Long format (permissions, size, date)
- `-a`: Show hidden files (starting with .)
- `-h`: Human-readable file sizes
- `-R`: Recursive listing
- `-t`: Sort by modification time

## Examples

```bash
ls-tool -la
ls-tool -lh /home/user
ls-tool -R src/
```