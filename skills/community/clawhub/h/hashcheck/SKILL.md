---
name: hashcheck
description: Calculate, verify, and compare file hashes using MD5, SHA-1, SHA-256, SHA-512, and BLAKE2b. Use when asked to checksum a file, verify a download hash, compare files for equality, or hash a text string. Supports all common algorithms, JSON output, and multi-algorithm display. Zero dependencies.
---

# hashcheck 🔒

File hash calculator, verifier, and comparator.

## Commands

```bash
# Calculate SHA-256 (default)
python3 scripts/hashcheck.py hash file.zip

# Specific algorithm
python3 scripts/hashcheck.py hash -a md5 file.iso

# Verify against expected hash
python3 scripts/hashcheck.py verify file.zip abc123def456...

# Compare two files
python3 scripts/hashcheck.py compare file1.txt file2.txt

# Hash a text string
python3 scripts/hashcheck.py text "hello world"

# Show all algorithms at once
python3 scripts/hashcheck.py all file.bin
```

## Algorithms
MD5, SHA-1, SHA-256, SHA-512, BLAKE2b
