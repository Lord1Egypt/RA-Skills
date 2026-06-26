---
name: ntriq-x402-code-review
description: "AI code review for security, performance, and quality. Returns scored issues and suggestions. $0.05 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [code, review, security, quality, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Code Review (x402)

Automated code review for security vulnerabilities, performance issues, and code quality. Supports any language. Returns a score, prioritized issues, and actionable suggestions. $0.05 USDC per call.

## How to Call

```bash
POST https://x402.ntriq.co.kr/code-review
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "code": "SELECT * FROM users WHERE id = '" + userId + "'",
  "language": "sql",
  "focus": "security"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `code` | string | ✅ | Code to review |
| `language` | string | ❌ | Programming language (default: `auto`) |
| `focus` | string | ❌ | `all` \| `security` \| `performance` \| `quality` (default: `all`) |

## Example Response

```json
{
  "status": "ok",
  "overall_score": 2,
  "issues": [
    {
      "severity": "critical",
      "line": 1,
      "description": "SQL injection vulnerability — user input directly concatenated",
      "suggestion": "Use parameterized queries: WHERE id = ?"
    }
  ],
  "security_risks": ["SQL injection", "Data exfiltration risk"],
  "summary": "Critical SQL injection found. Immediate fix required."
}
```

## Payment

- **Price**: $0.05 USDC per call
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
