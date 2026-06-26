---
name: md5-tool
description: Compute MD5 cryptographic hash values for files and text. Use for file integrity verification and checksum validation.
---
# MD5 - Message Digest Hash Calculator

Calculate 128-bit MD5 hash values for files or text input. Commonly used for file integrity checking and data fingerprinting.

## Usage
```bash
md5-tool [options] <file>
```
## Examples
```bash
md5-tool document.pdf
echo "data" | md5-tool
md5-tool --check checksums.md5
```