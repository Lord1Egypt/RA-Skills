---
name: nginx-config-linter
description: Lint, validate, and audit nginx configuration files for syntax errors, security issues, and performance problems.
version: 1.0.0
---

# Nginx Config Linter

Validate and audit nginx configuration files for syntax, security, and performance issues.

## Commands

### Lint a config file
```bash
python3 scripts/nginx-config-linter.py lint /etc/nginx/nginx.conf
```

### Security audit
```bash
python3 scripts/nginx-config-linter.py security /etc/nginx/nginx.conf
```

### Performance check
```bash
python3 scripts/nginx-config-linter.py performance /etc/nginx/nginx.conf
```

### Full audit (lint + security + performance)
```bash
python3 scripts/nginx-config-linter.py audit /etc/nginx/nginx.conf
```

### Scan directory of configs
```bash
python3 scripts/nginx-config-linter.py audit /etc/nginx/ --recursive
```

## Options

- `--format text|json|markdown` — Output format (default: text)
- `--severity error|warning|info` — Minimum severity to report (default: info)
- `--recursive` — Scan directories recursively for .conf files
- `--strict` — Exit code 1 on any warning or error (CI mode)

## What It Checks

### Syntax (12 rules)
- Unmatched braces, missing semicolons
- Invalid directives in wrong context
- Duplicate server_name, duplicate location
- Empty blocks, unreachable locations
- Invalid listen directives
- Conflicting try_files

### Security (15 rules)
- Missing security headers (X-Frame-Options, X-Content-Type-Options, CSP, etc.)
- Server tokens exposed (server_tokens on)
- Weak SSL/TLS (SSLv3, TLS 1.0/1.1, weak ciphers)
- Missing HSTS header
- Directory listing enabled (autoindex on)
- Missing rate limiting
- Permissive CORS (*) with credentials
- Default server block missing
- Root inside location block

### Performance (10 rules)
- Gzip not enabled or poorly configured
- Missing keepalive settings
- Buffer sizes too small/large
- Missing proxy cache settings
- No worker_connections tuning
- Missing client_max_body_size
- Large timeout values
- Missing access_log off for static assets

## Exit Codes
- 0: No errors or warnings
- 1: Errors or warnings found (or --strict with any findings)
- 2: File not found or parse error
