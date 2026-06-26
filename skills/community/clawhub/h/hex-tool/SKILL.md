---
name: hex-tool
description: Convert data between hexadecimal and other formats. Use for debugging binary data, examining file headers, and working with hex dumps.
---
# Hex - Hexadecimal Conversion Tool

Convert between hexadecimal, decimal, binary, and ASCII representations. Essential for low-level debugging, binary protocol analysis, and byte-level data inspection.

## Usage

```bash
hex-tool [options] <value>
```

## Operations

- Encode text or numbers to hexadecimal
- Decode hexadecimal back to readable text
- Convert between hex, decimal, and binary bases

## Examples

```bash
# Encode text to hex
hex-tool --encode "Hello World"

# Decode hex to text
hex-tool --decode "48656c6c6f"

# Convert decimal to hex
hex-tool --from dec --to hex 255
```
