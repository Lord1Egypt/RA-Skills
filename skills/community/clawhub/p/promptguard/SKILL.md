---
name: promptguard
description: Detect prompt injection attacks in text. Returns risk score and detected patterns.
version: 0.1.1
metadata:
  openclaw:
    requires:
      bins:
        - python
    install:
      - kind: uv
        packages: [fastapi, uvicorn, pydantic]
---

# PromptGuard

A security API that scans text for common prompt injection patterns and returns a risk score. Designed for AI agents that process untrusted text input from external sources.

## What It Detects

- Instruction override attempts
- HTML comment injection
- Zero-width unicode characters
- Delimiter-based attacks
- Role switching tokens
- System prompt extraction attempts

## Installation

```bash
pip install fastapi uvicorn pydantic
```

## Usage

Start the server:

```bash
uvicorn promptguard.app:app --port 8000
```

Then send a POST request:

```bash
curl -X POST http://localhost:8000/v1/scan \
  -H "Content-Type: application/json" \
  -d '{"text": "What is the weather in London today?"}'
```

Response (clean text):
```json
{
  "risk_score": "0",
  "patterns_detected": [],
  "input_length": 38
}
```

## Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | yes | Text to scan (1-100,000 chars) |

## Response

| Field | Type | Description |
|-------|------|-------------|
| `risk_score` | decimal | 0.0 (safe) to 1.0 (high risk) |
| `patterns_detected` | list | Names of detected patterns |
| `input_length` | integer | Length of input text |
