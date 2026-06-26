---
name: hash-tool
description: Compute cryptographic hash values of files and text. Use for verifying file integrity, checksums, and data validation.
---
# Hash - Checksum Calculator
Calculate cryptographic hash values using algorithms like MD5, SHA-1, SHA-256, and SHA-512. Essential for file integrity verification.
## Usage
```bash
hash-tool [options] <algorithm> <file>
```
## Algorithms
- md5, sha1, sha256, sha512
## Examples
```bash
hash-tool sha256 file.txt
hash-tool md5 document.pdf
echo "data" | hash-tool sha256
```