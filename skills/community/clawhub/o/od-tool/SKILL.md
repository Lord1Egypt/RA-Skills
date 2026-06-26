---
name: od-tool
description: Dump file contents in octal, decimal, hexadecimal, and ASCII formats. Use for binary data inspection and low-level file analysis.
---
# OD - Octal Dump Utility

Display file contents in multiple formats including octal, hexadecimal, decimal, and ASCII. Essential for binary analysis, debugging, and examining raw file data at byte level.

## Usage
```bash
od-tool [options] <file>
```

## Format Options

- Default: Octal bytes
- `-x`: Hexadecimal output
- `-d`: Decimal output
- `-c`: ASCII character display
- `-A`: Select address base (d=decimal, x=hex, o=octal, n=none)

## Examples

```bash
# Hex dump
od-tool -x file.bin

# Show ASCII representation
od-tool -c data.txt

# Hex with decimal addresses
od-tool -A d -x binary.dat
```