---
slug: hash-generator-tool
name: Hash Toolkit
description: "Multi-purpose hash tool: MD5, SHA-1, SHA-256, SHA-512, BLAKE2b, Base64 encode/decode, UUID generation, HMAC signing. Pure Python standard library, no API key required."
keywords: hash, md5, sha256, sha512, blake2, base64, uuid, hmac, checksum, cryptography
version: "1.0.0"
author: Qiance
language: en
---

# Hash Toolkit

All-in-one hash utility supporting multiple algorithms, Base64 encoding/decoding, UUID generation, and HMAC signing. Pure Python standard library, works offline.

## Features

- **Hash Algorithms**: MD5, SHA-1, SHA-256, SHA-512, BLAKE2b
- **Base64**: Encode and decode
- **UUID**: Generate random UUIDs
- **HMAC**: Sign messages with secret keys
- **Pure standard library**: Zero dependencies, works offline

## Usage

### Hash Generation

```bash
# SHA-256 (default)
python3 scripts/hash_toolkit.py "Hello World"

# MD5
python3 scripts/hash_toolkit.py "Hello World" --algo md5

# SHA-512
python3 scripts/hash_toolkit.py "Hello World" --algo sha512

# BLAKE2b
python3 scripts/hash_toolkit.py "Hello World" --algo blake2
```

### Base64

```bash
# Encode
python3 scripts/hash_toolkit.py "Hello World" --encode64

# Decode
python3 scripts/hash_toolkit.py "SGVsbG8gV29ybGQ=" --decode
```

### UUID

```bash
# Generate one UUID
python3 scripts/hash_toolkit.py --uuid

# Generate 5 UUIDs
python3 scripts/hash_toolkit.py --uuid --count 5
```

### HMAC

```bash
# HMAC-SHA256
python3 scripts/hash_toolkit.py "message" --hmac "secret-key"

# HMAC with different algorithm
python3 scripts/hash_toolkit.py "message" --hmac "secret-key" --algo sha512
```

## Options

| Option | Description |
|--------|-------------|
| `TEXT` | Text to hash/encode |
| `--algo` | Algorithm: md5, sha1, sha256, sha512, blake2 (default: sha256) |
| `--encode64` | Base64 encode |
| `--decode` | Base64 decode |
| `--uuid` | Generate UUID |
| `--hmac KEY` | HMAC signing with key |
| `--upper` | Output uppercase |
| `--count N` | Number of UUIDs to generate |

## Security Notes

- **MD5 & SHA-1**: Not recommended for security purposes (collision vulnerabilities)
- **SHA-256/SHA-512/BLAKE2b**: Suitable for security applications
- **Password storage**: Use bcrypt/argon2 instead of simple hashing
- **HMAC**: Suitable for message authentication

---

## 中文说明

多功能Hash工具，支持多种哈希算法、Base64编解码、UUID生成、HMAC签名。纯Python标准库，无需API Key。
