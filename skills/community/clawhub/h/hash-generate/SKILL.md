---
name: hash-generate
description: Hash, HMAC, encode/decode, UUID generation, and hash identification.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔐"
    homepage: https://hash.agentutil.net
    always: false
---

# hash-generate

Compute hashes (MD5, SHA-1, SHA-256, SHA-512, CRC32), HMACs, encode/decode (base64, hex, URL), generate UUIDs, and identify unknown hash algorithms.

## Data Handling

This skill sends user-provided input to an external API for processing. Do not send sensitive data (passwords, secrets, private keys) without explicit user consent. The service does not store or log input data beyond the immediate response.

## Endpoints

### Hash

```bash
curl -X POST https://hash.agentutil.net/v1/hash \
  -H "Content-Type: application/json" \
  -d '{"input": "hello world", "algorithm": "sha256"}'
```

Algorithms: md5, sha1, sha256, sha512, crc32. Optional `encoding`: hex (default) or base64.

### HMAC

```bash
curl -X POST https://hash.agentutil.net/v1/hmac \
  -H "Content-Type: application/json" \
  -d '{"input": "hello", "key": "secret", "algorithm": "sha256"}'
```

### Encode/Decode

```bash
curl -X POST https://hash.agentutil.net/v1/encode \
  -H "Content-Type: application/json" \
  -d '{"input": "hello", "operation": "encode", "format": "base64"}'
```

Formats: base64, hex, url, uuid (encode-only, generates random UUID).

### Identify Hash

```bash
curl -X POST https://hash.agentutil.net/v1/identify \
  -H "Content-Type: application/json" \
  -d '{"hash": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"}'
```

## Response Format

```json
{
  "hash": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
  "algorithm": "sha256",
  "encoding": "hex",
  "input_length": 11,
  "request_id": "abc-123",
  "service": "https://hash.agentutil.net"
}
```

## Pricing

- Free tier: 10 queries/day, no authentication required
- Paid tier: $0.001/query via x402 protocol (USDC on Base)

## Privacy

No authentication required for free tier. No personal data collected. Rate limiting uses IP hashing only.
