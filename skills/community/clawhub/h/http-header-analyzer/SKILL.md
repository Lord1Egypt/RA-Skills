---
name: http-header-analyzer
description: Analyze HTTP security headers and TLS configuration. Find missing headers, weak ciphers, and misconfigurations in web applications.
metadata: {"openclaw":{"emoji":"🔒","requires":{"bins":["curl"]}}}
---

# HTTP Header Analyzer

Check HTTP security headers and TLS configuration. Find missing protections and misconfigurations.

## Quick Start

```bash
# Analyze a single URL
python3 {baseDir}/scripts/analyze-headers.py https://example.com

# Check multiple targets
python3 {baseDir}/scripts/analyze-headers.py -f urls.txt

# JSON output
python3 {baseDir}/scripts/analyze-headers.py https://example.com --json
```

## Headers Checked

| Header | Purpose | Risk if Missing |
|--------|---------|-----------------|
| `Strict-Transport-Security` | Forces HTTPS | Medium |
| `Content-Security-Policy` | XSS protection | Medium-High |
| `X-Frame-Options` | Clickjacking protection | Medium |
| `X-Content-Type-Options` | MIME sniffing protection | Low |
| `X-XSS-Protection` | XSS filter (legacy) | Low |
| `Referrer-Policy` | Controls referrer leakage | Low |
| `Permissions-Policy` | Feature restrictions | Low |
| `Cross-Origin-Opener-Policy` | Cross-origin isolation | Low |
| `Cross-Origin-Embedder-Policy` | Cross-origin isolation | Low |
| `Cross-Origin-Resource-Policy` | Cross-origin protection | Low |

## Options

- `URL` — Target URL(s) to analyze
- `-f FILE` — File with URLs (one per line)
- `--json` — JSON output
- `--follow` — Follow redirects (default: yes)
- `--timeout SECS` — Request timeout (default: 10)
- `--user-agent UA` — Custom User-Agent
- `--check-tls` — Also check TLS certificate info
- `--severity LEVEL` — Minimum severity to report: `low`, `medium`, `high`

## Output

```
=== https://example.com ===
✅ Strict-Transport-Security: max-age=31536000; includeSubDomains
✅ Content-Security-Policy: default-src 'self'
❌ X-Frame-Options: MISSING (clickjacking risk)
✅ X-Content-Type-Options: nosniff
❌ Referrer-Policy: MISSING
⚠️  Server: nginx/1.18.0 (version exposed)

Score: 3/6 security headers present
Risk: MEDIUM
```
