---
name: massat-security-audit
display_name: MASSAT Security Audit — OWASP ASI01-ASI10 for multi-agent systems
version: 1.1.0
author: Craig M. Brown
homepage: https://craigmbrown.com/blindoracle/listings/
license: MIT-0
category: security
tags:
  - security-audit
  - owasp-asi
  - multi-agent
  - mcp
  - x402
---

# MASSAT security audit — check an agent or MCP server before you trust it

**What this skill does:** it buys a security audit of an AI agent or MCP server from
BlindOracle's public API (`https://api.craigmbrown.com`). The audit covers OWASP
Agentic Security ASI01–ASI10. Findings are Merkle-committed and the report is signed,
so you can check it without trusting us.

**What it does not do:** it never holds your wallet, never signs for you, and never
moves funds on its own. You pay each call yourself, with your own x402 wallet (USDC on
Base) or a BlindOracle starter-credit note. MASSAT scores are self-assessed tooling, not
a certification. An accredited assessor makes any compliance determination.

> **Changed in 1.1.0 (2026-11-15).** Version 1.0.0 pointed at
> `craigmbrown.com/api/v1/massat/audit` and listed $50 / $99-a-month plans and a free
> quick scan. That endpoint now answers 401 and those plans do not exist. Use the routes
> and prices below.

## Price

| Call | Price | What you get |
|---|---|---|
| `security.massat-audit` | **$5.00** per audit | full ASI01–ASI10 audit, signed report |
| `security.massat-conformance` | $0.25 | checks an agent's stated security claims against MASSAT's requirements |
| `security.injection-resilience` | $0.50 | scans text you supply (prompt, tool descriptions, manifest) for injection patterns |
| `bundle.massat-ladder` | $4.734 | track record → pre-hire check → the $5 audit only if the check is not AVOID; unexecuted steps refunded |

Live prices: `GET https://api.craigmbrown.com/v1/services` (free, no key). There is no
free audit. An audit of a subject with no code returns `insufficient_subject` and is
**not charged**.

## How to call it

### Over MCP (recommended)

Add the remote MCP server `https://api.craigmbrown.com/v1/mcp` (streamable HTTP).
Call `list_services` first (free) to see prices, then the tool `security_massat-audit`.
An unpaid call returns a payment-required result with the exact x402 quote; pay it
from your own wallet, or pass a starter-credit note in `_meta["bo/x402-payment"]`.

### Over HTTP (x402)

```bash
curl -X POST https://api.craigmbrown.com/v1/services/security.massat-audit \
  -H 'Content-Type: application/json' \
  -d '{"target": "https://github.com/your-org/your-agent", "scope": "full"}'
# -> HTTP 402 with the x402 quote; retry with your signed payment header.
```

## Inputs

| Field | Required | Meaning |
|---|---|---|
| `target` | yes | a git repo URL, an agent manifest URL, or a code path |
| `scope` | no | `quick` or `full` (default `full`) |
| `owner` | no | owner or agent id, for attribution |
| `anchor` | no | `true` to anchor the proof on Base |
| `subject` | no | for an agent whose code is not public: a `{path: sha256}` manifest plus declared tools, collected with `blindoracle-sdk` `AuditAPI.collect(paths)`. Your source never leaves your machine. |

## Verify a result

Every paid call returns a settlement reference. Check it with no key at
`https://api.craigmbrown.com/v1/proofs/settlement/<ref>`, and the payment itself on
Basescan.

## Terms

Paying for a call accepts BlindOracle's terms: https://craigmbrown.com/blindoracle/terms.html
