---
name: hash-toolkit
description: Hash generator and verifier supporting MD5, SHA1, SHA256, SHA512, CRC32, HMAC, and BLAKE2. Hash files, strings, or verify integrity. Pure Python, zero dependencies. GitHub: https://github.com/darbling/clawhub-skills 当用户需要计算哈希值、校验文件完整性、MD5校验、SHA256验证、HMAC签名时触发。
---

# 🔐 Hash Toolkit

**Author: Lin Hui** | [GitHub](https://github.com/darbling/clawhub-skills) | MIT License | v1.0.0

Compute and verify hashes for strings, files, and data. Supports MD5, SHA1, SHA256, SHA512, CRC32, HMAC, and BLAKE2.

## ✨ Features

- **String hashing** — Hash any text with your choice of algorithm
- **File hashing** — Compute hash of any file (streaming for large files)
- **Verify** — Compare a hash against expected value (pass/fail)
- **Batch** — Hash multiple files at once
- **HMAC** — Keyed-hash message authentication codes
- **CRC32** — Quick checksums for data integrity
- **BLAKE2** — Modern, fast, secure hash algorithm

## 🚀 Usage

```
Calculate the SHA256 hash of the string "hello world"
```
```
Compute the MD5 hash of the file /path/to/file.zip
```
```
Verify that the SHA256 hash of download.iso matches abc123def...
```
```
Generate HMAC-SHA256 signature for "message" with key "secret"
```
```
Calculate CRC32 checksum for data.bin
```

## ⚙️ Technical Details

- **Runtime**: Python 3.6+
- **Dependencies**: Zero (stdlib only: hashlib, hmac, zlib, binascii)
- **Algorithms**: MD5, SHA1, SHA224, SHA256, SHA384, SHA512, BLAKE2b, BLAKE2s, CRC32
- **Large files**: Streaming with 8MB chunks
