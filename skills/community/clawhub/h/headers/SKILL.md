---
name: security-headers
description: Audit HTTP security headers for any website — checks HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, COOP, CORP, and XSS-Protection. Grades sites A-F. Detects server info leakage (Server, X-Powered-By). Use when asked to check website security, audit headers, find missing security headers, or grade a site's HTTP security posture. Zero dependencies.
---

# security-headers 🔒

HTTP security headers auditor with grading and info leak detection.

## Commands

```bash
# Check one or more sites (auto-adds https://)
python3 scripts/headers.py github.com example.com

# JSON output
python3 scripts/headers.py --json example.com
```

## Checks (9 headers)
- 🔴 **High**: Strict-Transport-Security (HSTS), Content-Security-Policy (CSP)
- 🟡 **Medium**: X-Content-Type-Options, X-Frame-Options, Referrer-Policy
- 🟢 **Low**: Permissions-Policy, X-XSS-Protection, COOP, CORP

## Grading
- **A** (≥78%): 7+ headers present
- **B** (≥56%): 5-6 headers
- **C** (≥33%): 3-4 headers
- **D** (≥11%): 1-2 headers
- **F** (0%): No security headers

## Info Leak Detection
Flags Server, X-Powered-By, X-AspNet-Version, X-Generator headers that reveal technology stack.
