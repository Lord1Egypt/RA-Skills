# http-security-headers — Status

**Price:** $59
**Status:** Ready
**Created:** 2026-04-01

## Description
Analyze HTTP security headers for any URL. Grade websites A-F with 15 security header checks, CSP/HSTS deep analysis, information disclosure detection, and server-specific fix recommendations (Nginx, Apache, Cloudflare).

## Features
- 15 security header checks (HSTS, CSP, X-Frame-Options, etc.)
- Deep HSTS analysis (max-age, includeSubDomains, preload)
- Deep CSP analysis (unsafe-inline, unsafe-eval, wildcards, directive coverage)
- 5 information disclosure checks (Server, X-Powered-By, etc.)
- A-F grading with weighted scoring
- 3 output formats (text, JSON, markdown)
- CI-friendly exit codes + --min-grade flag
- Fix snippets for Nginx, Apache, Cloudflare
- Batch URL scanning
- Pure Python stdlib (no dependencies)

## Tested Against
- google.com (Grade F — few security headers)
- github.com (Grade D — good CSP but missing COOP/CORP/COEP)
- cloudflare.com (Grade D — no CSP, good basic headers)
- JSON + Markdown output verified
- CI exit codes verified
