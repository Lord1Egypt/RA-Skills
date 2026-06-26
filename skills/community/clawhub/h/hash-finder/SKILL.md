---
name: Hash Finding Tool
description: Crack and identify hashes by attempting to match them against known hash databases and common plaintext values.
---

# Overview

The Hash Finding Tool is a security utility designed to identify the plaintext values behind cryptographic hashes. By leveraging extensive hash databases and intelligent matching algorithms, this tool helps security professionals, penetration testers, and incident responders quickly determine the original values of captured or discovered hashes.

This tool supports common hash types and performs rapid lookups against curated datasets of known hash-plaintext pairs. It is ideal for password auditing, forensic analysis, breach investigation, and general security research where hash identification is required.

Whether you're validating password strength in a security assessment or recovering plaintext from discovered hashes during an incident, the Hash Finding Tool provides fast, accurate results through a simple API interface.

## Usage

**Request Example:**

```json
{
  "hash": "5d41402abc4b2a76b9719d911017c592"
}
```

**Response Example:**

```json
{
  "hash": "5d41402abc4b2a76b9719d911017c592",
  "plaintext": "hello",
  "hash_type": "MD5",
  "found": true,
  "confidence": 0.99
}
```

## Endpoints

### POST /crack-hash

**Description:**  
Attempts to crack or identify a given hash by matching it against known hash databases and common plaintext values.

**Method:** `POST`  
**Path:** `/crack-hash`

**Request Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| hash | string | Yes | The hash value to crack. Accepts MD5, SHA-1, SHA-256, and other common hash formats. |

**Response Schema:**

The response returns a JSON object containing:

| Field | Type | Description |
|-------|------|-------------|
| hash | string | The input hash that was queried. |
| plaintext | string | The plaintext value if a match was found; `null` if not found. |
| hash_type | string | The detected or inferred hash algorithm type (e.g., "MD5", "SHA-1", "SHA-256"). |
| found | boolean | `true` if a match was located in the database; `false` otherwise. |
| confidence | number | A confidence score between 0 and 1 indicating the likelihood of an accurate match. |

**Status Codes:**

- `200 OK` — Hash lookup completed successfully.
- `422 Unprocessable Entity` — Validation error (e.g., missing or malformed hash parameter).

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

## About

ToolWeb.in — 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- 🌐 [toolweb.in](https://toolweb.in)
- 🔌 [portal.toolweb.in](https://portal.toolweb.in)
- 🤖 [hub.toolweb.in](https://hub.toolweb.in)
- 🐾 [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- 🚀 [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- 📺 [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- **Kong Route:** `https://api.mkkpro.com/security/hash-finder`
- **API Docs:** `https://api.mkkpro.com:8008/docs`
