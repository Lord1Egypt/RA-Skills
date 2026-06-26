---
name: hash
version: "3.0.1"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [hash, tool, utility]
description: "Generate MD5 and SHA checksums, verify integrity, and compare hash values. Use when computing checksums, verifying downloads, or comparing hash outputs."
---

# hash

Hash & Checksum Tool.

## Commands

### `md5`

Compute MD5 hash

```bash
scripts/script.sh md5 <file_or_text>
```

### `sha1`

Compute SHA-1 hash

```bash
scripts/script.sh sha1 <file_or_text>
```

### `sha256`

Compute SHA-256 hash

```bash
scripts/script.sh sha256 <file_or_text>
```

### `sha512`

Compute SHA-512 hash

```bash
scripts/script.sh sha512 <file_or_text>
```

### `verify`

Verify a file against a known hash

```bash
scripts/script.sh verify <file> <expected_hash>
```

### `compare`

Compare hashes of two files

```bash
scripts/script.sh compare <file1> <file2>
```

### `batch`

Hash every file in a directory (default: sha256)

```bash
scripts/script.sh batch <directory> [algo]
```

### `check`

Verify hashes listed in a checksum file

```bash
scripts/script.sh check <hashfile>
```

### `history`

Show recent hash operations

```bash
scripts/script.sh history
```

## Requirements

- bash 4.0+

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
