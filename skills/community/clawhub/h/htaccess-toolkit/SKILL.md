---
name: htaccess-toolkit
description: Generate, validate, lint, and explain Apache .htaccess files. Use when asked to create htaccess rules, redirect URLs, set security headers, enable caching, configure CORS, protect files, or audit existing .htaccess configurations. Triggers on "htaccess", "apache redirect", "mod_rewrite", "URL rewrite", "apache config", "browser caching", "hotlinking protection".
---

# htaccess Toolkit

Generate, validate, lint, and explain Apache .htaccess files with security headers, caching, CORS, compression, and more.

## Generate

```bash
# HTTPS redirect + security headers + compression
python3 scripts/htaccess.py generate --rewrites http-to-https --security strict --compression

# Full production setup
python3 scripts/htaccess.py generate \
  --rewrites http-to-https www-to-non-www \
  --security strict \
  --caching standard \
  --compression \
  --protect directory-listing dotfiles sensitive-files \
  --error-pages 404 500 \
  -o .htaccess

# WordPress hardening
python3 scripts/htaccess.py generate --protect wp-config xmlrpc dotfiles --security strict

# CORS for specific domain
python3 scripts/htaccess.py generate --cors specific --domain example.com

# Custom redirects
python3 scripts/htaccess.py generate --redirects "/old-page -> /new-page" "/blog -> https://blog.example.com"

# Hotlinking protection
python3 scripts/htaccess.py generate --protect hotlinking --domain example.com
```

## Lint

```bash
# Basic lint
python3 scripts/htaccess.py lint .htaccess

# Strict mode (exit 1 on errors, CI-friendly)
python3 scripts/htaccess.py lint .htaccess --strict

# Filter by severity
python3 scripts/htaccess.py lint .htaccess --severity error warning

# JSON output
python3 scripts/htaccess.py lint .htaccess -f json
```

### Lint Checks (10 rules)
- `rewrite-no-engine` — RewriteRule without RewriteEngine On
- `duplicate-rewrite-engine` — Multiple RewriteEngine On
- `redirect-no-slash` — Redirect path not starting with /
- `missing-l-flag` — RewriteRule without [L] flag
- `mixed-redirect-rewrite` — Mixing Redirect and RewriteRule
- `unclosed-ifmodule` — Unclosed IfModule blocks
- `unclosed-files` — Unclosed Files/FilesMatch blocks
- `wildcard-cors` — Wildcard origin with credentials
- `no-hsts` — HTTPS without HSTS header
- `options-minus-indexes` — Directory listing not disabled

## Explain

```bash
# Human-readable explanation of each directive
python3 scripts/htaccess.py explain .htaccess
```

## List Presets

```bash
python3 scripts/htaccess.py presets
python3 scripts/htaccess.py presets -f json
```

## Available Presets

**Rewrites:** http-to-https, www-to-non-www, non-www-to-www, trailing-slash-add, trailing-slash-remove, remove-extension

**Security:** basic, strict

**Caching:** standard, aggressive

**CORS:** permissive, specific

**Protection:** directory-listing, dotfiles, sensitive-files, wp-config, xmlrpc, hotlinking

**Error Pages:** 404, 403, 500, 503
