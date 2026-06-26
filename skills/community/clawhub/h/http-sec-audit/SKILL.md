---
name: http-sec-audit
description: Audit HTTP security headers for any website. Use when a user asks to check security headers, harden a web server, audit HSTS/CSP/X-Frame-Options compliance, find information leaks (Server, X-Powered-By), or assess a website's security posture. Checks 10 security headers and grades A–F. Supports multiple URLs and JSON output.
---

# HTTP Security Headers Audit

Scan any URL for missing or misconfigured security headers and get an actionable report with grades, fix recommendations, and info-leak detection.

## Quick Start

```bash
python3 scripts/sec_headers.py https://example.com
```

## Commands

```bash
# Single URL audit
python3 scripts/sec_headers.py https://example.com

# Multiple URLs
python3 scripts/sec_headers.py https://example.com https://google.com https://github.com

# JSON output (for programmatic use)
python3 scripts/sec_headers.py https://example.com --json

# Custom timeout
python3 scripts/sec_headers.py https://example.com --timeout 5
```

## What It Checks

**Security headers** (graded by severity):
- `Strict-Transport-Security` (HSTS) — HIGH
- `Content-Security-Policy` (CSP) — HIGH
- `X-Content-Type-Options` — MEDIUM
- `X-Frame-Options` — MEDIUM
- `Referrer-Policy` — MEDIUM
- `Permissions-Policy` — MEDIUM
- `X-XSS-Protection` — LOW
- `Cross-Origin-Opener-Policy` (COOP) — LOW
- `Cross-Origin-Resource-Policy` (CORP) — LOW
- `Cross-Origin-Embedder-Policy` (COEP) — LOW

**Info leak detection:**
- `Server` header (software version disclosure)
- `X-Powered-By` (technology stack leak)
- `X-AspNet-Version` (framework version leak)

## Grading

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 90–100 | Excellent — all critical headers present |
| B | 75–89 | Good — minor gaps |
| C | 50–74 | Fair — important headers missing |
| D | 25–49 | Poor — significant exposure |
| F | 0–24 | Failing — most headers absent |

## Dependencies

```bash
pip install requests
```
