---
name: htaccess-gen
description: Generate .htaccess files for Apache web servers. Use when creating redirect rules, URL rewrites, security headers, HTTPS enforcement, IP blocking, caching rules, custom error pages, or hotlink protection. Covers common Apache configurations including mod_rewrite, mod_headers, mod_deflate, and mod_expires. Also use when converting nginx config concepts to Apache .htaccess format.
---

# htaccess-gen

Generate production-ready .htaccess configurations from the command line.

## Quick Start

```bash
# Generate HTTPS redirect + security headers + caching
python3 scripts/htaccess_gen.py generate --https --security-headers --caching

# Generate redirect rules
python3 scripts/htaccess_gen.py redirect --from /old-page --to /new-page --type 301

# Block IPs
python3 scripts/htaccess_gen.py generate --block-ip 192.168.1.100 --block-ip 10.0.0.0/24

# Full production config
python3 scripts/htaccess_gen.py generate --https --www --security-headers --caching --gzip --error-pages --hotlink-protection --output .htaccess
```

## Commands

### `generate`
Create a complete .htaccess file with selected features.

Options:
- `--https` — Force HTTPS redirect
- `--www` — Force www prefix (or `--no-www` to remove it)
- `--security-headers` — Add security headers (X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, HSTS)
- `--caching` — Add browser caching rules (mod_expires)
- `--gzip` — Enable gzip/deflate compression
- `--error-pages` — Add custom error page directives (403, 404, 500)
- `--hotlink-protection` — Prevent image hotlinking
- `--domain <domain>` — Your domain name (used for hotlink protection and www rules)
- `--block-ip <ip>` — Block an IP address or CIDR range (repeatable)
- `--cors` — Enable CORS headers
- `--cors-origin <origin>` — Specific allowed origin (default: `*`)
- `--index <file>` — Set directory index file
- `--output <file>` — Write to file instead of stdout

### `redirect`
Generate redirect rules.

Options:
- `--from <path>` — Source path (required)
- `--to <path>` — Destination path or URL (required)
- `--type <code>` — HTTP status code: 301 (permanent) or 302 (temporary). Default: 301.

### `rewrite`
Generate URL rewrite rules.

Options:
- `--pattern <regex>` — Regex pattern to match (required)
- `--target <path>` — Rewrite target (required)
- `--flags <flags>` — RewriteRule flags (default: `[L,QSA]`)
- `--condition <cond>` — RewriteCond to prepend (repeatable)

## Feature Details

### Security Headers
Adds these headers via `mod_headers`:
- `X-Frame-Options: SAMEORIGIN` — Prevents clickjacking
- `X-Content-Type-Options: nosniff` — Prevents MIME sniffing
- `X-XSS-Protection: 1; mode=block` — XSS filter
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains` (when --https)

### Caching Rules
Sets expiry times via `mod_expires`:
- Images: 1 month
- CSS/JS: 1 week
- HTML: 1 hour
- Fonts: 1 year
