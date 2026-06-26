---
name: hexdump-tool
description: Display file contents in hexadecimal and ASCII format. Use for binary file analysis, forensic examination, and low-level data inspection.
---
# Hex Dump - Binary File Viewer

Display file contents as hexadecimal bytes alongside their ASCII representation. Each line shows offset, raw bytes, and printable characters for complete binary inspection.

## Usage

```bash
hexdump-tool [options] <file>
```

## Features

- Side-by-side hex + ASCII display
- Configurable byte grouping
- Canonical format with offset markers
- Colorized output for readability

## Examples

```bash
# Standard hex dump
hexdump-tool binary.bin

# Canonical format
hexdump-tool -C data.bin

# Show first 256 bytes only
hexdump-tool -n 256 file.bin
```
