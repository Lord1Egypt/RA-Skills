---
name: http-security-headers
description: Analyze HTTP security headers for any URL. Check for HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, CORS, and more. Assign A-F security grades with OWASP-aligned recommendations. Use when asked to check security headers, audit HTTP headers, scan a website for security, check HSTS/CSP configuration, grade website security posture, or review HTTP response security. Triggers on "security headers", "check headers", "HSTS", "CSP audit", "website security scan", "header analysis", "security grade".
---

# HTTP Security Headers Analyzer

Analyze HTTP response headers for security best practices. Grade websites A-F with actionable recommendations.

## Quick Scan (Single URL)

```bash
python3 scripts/scan_headers.py <url>
```

## Batch Scan (Multiple URLs)

```bash
python3 scripts/scan_headers.py <url1> <url2> <url3>
```

## Output Formats

```bash
# Text (default)
python3 scripts/scan_headers.py <url>

# JSON
python3 scripts/scan_headers.py <url> --format json

# Markdown report
python3 scripts/scan_headers.py <url> --format markdown
```

## What It Checks

### Security Headers (15 checks)

| Header | Impact | Description |
|--------|--------|-------------|
| Strict-Transport-Security | Critical | HTTPS enforcement, preload, max-age |
| Content-Security-Policy | Critical | XSS/injection prevention, directive analysis |
| X-Frame-Options | High | Clickjacking protection |
| X-Content-Type-Options | High | MIME sniffing prevention |
| Referrer-Policy | Medium | Information leakage control |
| Permissions-Policy | Medium | Browser feature restrictions |
| X-XSS-Protection | Low | Legacy XSS filter (deprecated but checked) |
| Cross-Origin-Opener-Policy | Medium | Cross-origin isolation |
| Cross-Origin-Resource-Policy | Medium | Resource sharing control |
| Cross-Origin-Embedder-Policy | Medium | Embedding restrictions |
| Cache-Control | Medium | Sensitive data caching |
| X-Permitted-Cross-Domain-Policies | Low | Flash/PDF cross-domain |
| Clear-Site-Data | Info | Logout/session clearing |
| X-DNS-Prefetch-Control | Low | DNS prefetch control |
| Content-Type | High | Charset and MIME type |

### Negative Indicators (penalize)

- `Server` header revealing version info
- `X-Powered-By` header present
- `X-AspNet-Version` or similar tech disclosure

## Grading

- **A+** (100): All critical+high headers present with optimal config
- **A** (90-99): All critical headers, minor improvements possible
- **B** (75-89): Most headers present, some gaps
- **C** (60-74): Several missing headers
- **D** (40-59): Major security gaps
- **F** (<40): Critical headers missing

## CI Integration

Exit codes:
- `0` — Grade A or better
- `1` — Grade B-C (warnings)
- `2` — Grade D-F (failures)

Use `--min-grade B` to set custom threshold:
```bash
python3 scripts/scan_headers.py https://example.com --min-grade B
```

## Workflow

1. User provides URL(s) to scan
2. Run the scan script
3. Present the grade and findings
4. Highlight critical missing headers first
5. Provide specific fix recommendations (Nginx, Apache, Cloudflare snippets)
