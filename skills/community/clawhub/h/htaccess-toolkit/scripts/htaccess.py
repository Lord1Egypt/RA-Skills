#!/usr/bin/env python3
"""htaccess Toolkit — Generate, validate, and lint Apache .htaccess files."""

import argparse
import json
import re
import sys

VERSION = "1.0.0"


# ─── Generators ──────────────────────────────────────────────

REDIRECT_TEMPLATE = "Redirect {status} {from_path} {to_url}"
REWRITE_TEMPLATES = {
    "www-to-non-www": [
        "RewriteEngine On",
        "RewriteCond %{HTTP_HOST} ^www\\.(.*)$ [NC]",
        "RewriteRule ^(.*)$ https://%1/$1 [R=301,L]",
    ],
    "non-www-to-www": [
        "RewriteEngine On",
        "RewriteCond %{HTTP_HOST} !^www\\. [NC]",
        "RewriteRule ^(.*)$ https://www.%{HTTP_HOST}/$1 [R=301,L]",
    ],
    "http-to-https": [
        "RewriteEngine On",
        "RewriteCond %{HTTPS} off",
        "RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]",
    ],
    "trailing-slash-add": [
        "RewriteEngine On",
        "RewriteCond %{REQUEST_FILENAME} !-f",
        "RewriteRule ^(.*[^/])$ /$1/ [R=301,L]",
    ],
    "trailing-slash-remove": [
        "RewriteEngine On",
        "RewriteCond %{REQUEST_FILENAME} !-d",
        "RewriteRule ^(.*)/$ /$1 [R=301,L]",
    ],
    "remove-extension": [
        "RewriteEngine On",
        "RewriteCond %{REQUEST_FILENAME} !-d",
        "RewriteCond %{REQUEST_FILENAME}.html -f",
        "RewriteRule ^(.*)$ $1.html [L]",
    ],
}

SECURITY_HEADERS = {
    "basic": [
        "# Security Headers",
        '<IfModule mod_headers.c>',
        '  Header set X-Content-Type-Options "nosniff"',
        '  Header set X-Frame-Options "SAMEORIGIN"',
        '  Header set X-XSS-Protection "1; mode=block"',
        '  Header set Referrer-Policy "strict-origin-when-cross-origin"',
        '</IfModule>',
    ],
    "strict": [
        "# Strict Security Headers",
        '<IfModule mod_headers.c>',
        '  Header set X-Content-Type-Options "nosniff"',
        '  Header set X-Frame-Options "DENY"',
        '  Header set X-XSS-Protection "1; mode=block"',
        '  Header set Referrer-Policy "strict-origin-when-cross-origin"',
        '  Header set Permissions-Policy "camera=(), microphone=(), geolocation=()"',
        '  Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"',
        '  Header set Content-Security-Policy "default-src \'self\'; script-src \'self\'; style-src \'self\' \'unsafe-inline\'"',
        '</IfModule>',
    ],
}

CACHING_RULES = {
    "standard": [
        "# Browser Caching",
        '<IfModule mod_expires.c>',
        '  ExpiresActive On',
        '  ExpiresByType image/jpeg "access plus 1 year"',
        '  ExpiresByType image/png "access plus 1 year"',
        '  ExpiresByType image/gif "access plus 1 year"',
        '  ExpiresByType image/webp "access plus 1 year"',
        '  ExpiresByType image/svg+xml "access plus 1 year"',
        '  ExpiresByType image/x-icon "access plus 1 year"',
        '  ExpiresByType text/css "access plus 1 month"',
        '  ExpiresByType application/javascript "access plus 1 month"',
        '  ExpiresByType application/font-woff2 "access plus 1 year"',
        '  ExpiresByType text/html "access plus 0 seconds"',
        '</IfModule>',
    ],
    "aggressive": [
        "# Aggressive Caching",
        '<IfModule mod_expires.c>',
        '  ExpiresActive On',
        '  ExpiresDefault "access plus 1 year"',
        '  ExpiresByType text/html "access plus 0 seconds"',
        '  ExpiresByType application/json "access plus 0 seconds"',
        '</IfModule>',
        '',
        '<IfModule mod_headers.c>',
        '  <FilesMatch "\\.(ico|pdf|flv|jpg|jpeg|png|gif|webp|js|css|swf|woff2)$">',
        '    Header set Cache-Control "max-age=31536000, public"',
        '  </FilesMatch>',
        '</IfModule>',
    ],
}

CORS_RULES = {
    "permissive": [
        "# CORS - Permissive",
        '<IfModule mod_headers.c>',
        '  Header set Access-Control-Allow-Origin "*"',
        '  Header set Access-Control-Allow-Methods "GET, POST, OPTIONS"',
        '  Header set Access-Control-Allow-Headers "Content-Type, Authorization"',
        '</IfModule>',
    ],
    "specific": [
        "# CORS - Specific Origin",
        '<IfModule mod_headers.c>',
        '  SetEnvIf Origin "https://(www\\.)?{domain}$" CORS_ORIGIN=$0',
        '  Header set Access-Control-Allow-Origin "%{CORS_ORIGIN}e" env=CORS_ORIGIN',
        '  Header set Access-Control-Allow-Methods "GET, POST, OPTIONS" env=CORS_ORIGIN',
        '  Header set Access-Control-Allow-Headers "Content-Type, Authorization" env=CORS_ORIGIN',
        '  Header set Access-Control-Allow-Credentials "true" env=CORS_ORIGIN',
        '</IfModule>',
    ],
}

PROTECTION_RULES = {
    "directory-listing": [
        "# Disable Directory Listing",
        "Options -Indexes",
    ],
    "dotfiles": [
        "# Block access to hidden files",
        '<FilesMatch "^\\..">',
        '  Require all denied',
        '</FilesMatch>',
    ],
    "sensitive-files": [
        "# Block sensitive files",
        '<FilesMatch "(^#.*#|\\.(bak|conf|dist|fla|in[ci]|log|orig|psd|sh|sql|sw[op])|~)$">',
        '  Require all denied',
        '</FilesMatch>',
    ],
    "wp-config": [
        "# Protect wp-config.php",
        '<Files wp-config.php>',
        '  Require all denied',
        '</Files>',
    ],
    "xmlrpc": [
        "# Block XML-RPC (WordPress brute force protection)",
        '<Files xmlrpc.php>',
        '  Require all denied',
        '</Files>',
    ],
    "hotlinking": [
        "# Prevent image hotlinking",
        "RewriteEngine On",
        'RewriteCond %{HTTP_REFERER} !^$',
        'RewriteCond %{HTTP_REFERER} !^https?://(www\\.)?{domain} [NC]',
        'RewriteRule \\.(jpg|jpeg|png|gif|webp|svg)$ - [F,NC,L]',
    ],
}

COMPRESSION_RULES = [
    "# Gzip Compression",
    '<IfModule mod_deflate.c>',
    '  AddOutputFilterByType DEFLATE text/html text/plain text/css',
    '  AddOutputFilterByType DEFLATE application/javascript application/json',
    '  AddOutputFilterByType DEFLATE application/xml text/xml',
    '  AddOutputFilterByType DEFLATE image/svg+xml',
    '  AddOutputFilterByType DEFLATE application/font-woff2',
    '</IfModule>',
]

ERROR_PAGES = {
    "404": 'ErrorDocument 404 /404.html',
    "403": 'ErrorDocument 403 /403.html',
    "500": 'ErrorDocument 500 /500.html',
    "503": 'ErrorDocument 503 /maintenance.html',
}


def cmd_generate(args):
    """Generate .htaccess rules."""
    sections = []

    if args.rewrites:
        for name in args.rewrites:
            if name in REWRITE_TEMPLATES:
                sections.append(REWRITE_TEMPLATES[name])
            else:
                print(f"Warning: Unknown rewrite '{name}'. Available: {', '.join(REWRITE_TEMPLATES.keys())}", file=sys.stderr)

    if args.security:
        level = args.security
        if level in SECURITY_HEADERS:
            sections.append(SECURITY_HEADERS[level])

    if args.caching:
        level = args.caching
        if level in CACHING_RULES:
            sections.append(CACHING_RULES[level])

    if args.cors:
        mode = args.cors
        if mode in CORS_RULES:
            rules = CORS_RULES[mode]
            if args.domain and mode == "specific":
                rules = [r.replace("{domain}", args.domain.replace(".", "\\.")) for r in rules]
            sections.append(rules)

    if args.protect:
        for name in args.protect:
            if name in PROTECTION_RULES:
                rules = PROTECTION_RULES[name]
                if args.domain:
                    rules = [r.replace("{domain}", args.domain.replace(".", "\\.")) for r in rules]
                sections.append(rules)
            else:
                print(f"Warning: Unknown protection '{name}'. Available: {', '.join(PROTECTION_RULES.keys())}", file=sys.stderr)

    if args.compression:
        sections.append(COMPRESSION_RULES)

    if args.error_pages:
        pages = []
        for code in args.error_pages:
            if code in ERROR_PAGES:
                pages.append(ERROR_PAGES[code])
        if pages:
            sections.append(["# Custom Error Pages"] + pages)

    if args.redirects:
        redirect_lines = ["# Redirects"]
        for spec in args.redirects:
            parts = spec.split("->")
            if len(parts) == 2:
                from_path = parts[0].strip()
                to_url = parts[1].strip()
                status = "301"
                redirect_lines.append(f"Redirect {status} {from_path} {to_url}")
        sections.append(redirect_lines)

    if not sections:
        print("No rules to generate. Use --help to see options.", file=sys.stderr)
        sys.exit(1)

    output = "\n\n".join("\n".join(s) for s in sections)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output + "\n")
        print(f"Written to {args.output}")
    else:
        print(output)


# ─── Validator / Linter ──────────────────────────────────────

LINT_RULES = [
    {
        "id": "rewrite-no-engine",
        "severity": "error",
        "check": lambda lines: (
            any("RewriteRule" in l or "RewriteCond" in l for l in lines)
            and not any("RewriteEngine On" in l for l in lines)
        ),
        "message": "RewriteRule/RewriteCond used without 'RewriteEngine On'",
    },
    {
        "id": "duplicate-rewrite-engine",
        "severity": "warning",
        "check": lambda lines: sum(1 for l in lines if "RewriteEngine On" in l) > 1,
        "message": "Multiple 'RewriteEngine On' declarations (only one needed)",
    },
    {
        "id": "redirect-no-slash",
        "severity": "warning",
        "check": lambda lines: any(
            re.match(r'^\s*Redirect\s+\d+\s+[^/]', l) for l in lines
        ),
        "message": "Redirect source path should start with /",
    },
    {
        "id": "missing-l-flag",
        "severity": "warning",
        "check": lambda lines: any(
            re.match(r'^\s*RewriteRule\s+\S+\s+\S+\s*$', l) for l in lines
        ),
        "message": "RewriteRule without [L] flag may cause unexpected behavior",
    },
    {
        "id": "mixed-redirect-rewrite",
        "severity": "info",
        "check": lambda lines: (
            any(re.match(r'^\s*Redirect\s', l) for l in lines)
            and any(re.match(r'^\s*RewriteRule\s', l) for l in lines)
        ),
        "message": "Mixing Redirect and RewriteRule directives (Redirect runs first regardless of order)",
    },
    {
        "id": "unclosed-ifmodule",
        "severity": "error",
        "check": lambda lines: (
            sum(1 for l in lines if re.match(r'^\s*<IfModule', l))
            != sum(1 for l in lines if re.match(r'^\s*</IfModule', l))
        ),
        "message": "Unclosed <IfModule> block",
    },
    {
        "id": "unclosed-files",
        "severity": "error",
        "check": lambda lines: (
            sum(1 for l in lines if re.match(r'^\s*<Files', l))
            != sum(1 for l in lines if re.match(r'^\s*</Files', l))
        ),
        "message": "Unclosed <Files> or <FilesMatch> block",
    },
    {
        "id": "wildcard-cors",
        "severity": "warning",
        "check": lambda lines: any(
            'Access-Control-Allow-Origin "*"' in l for l in lines
        ) and any(
            'Access-Control-Allow-Credentials "true"' in l for l in lines
        ),
        "message": "Wildcard CORS origin with credentials is invalid (browsers reject this)",
    },
    {
        "id": "no-hsts",
        "severity": "info",
        "check": lambda lines: (
            any("https" in l.lower() for l in lines)
            and not any("Strict-Transport-Security" in l for l in lines)
        ),
        "message": "HTTPS redirects without HSTS header (consider adding Strict-Transport-Security)",
    },
    {
        "id": "options-minus-indexes",
        "severity": "info",
        "check": lambda lines: not any(
            re.match(r'^\s*Options\s+.*-Indexes', l) for l in lines
        ),
        "message": "Directory listing not explicitly disabled (consider 'Options -Indexes')",
    },
]


def cmd_lint(args):
    """Lint an .htaccess file."""
    try:
        with open(args.file) as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.", file=sys.stderr)
        sys.exit(1)

    lines = content.splitlines()
    issues = []

    for rule in LINT_RULES:
        if args.severity and rule["severity"] not in args.severity:
            continue
        try:
            if rule["check"](lines):
                issues.append({
                    "id": rule["id"],
                    "severity": rule["severity"],
                    "message": rule["message"],
                })
        except Exception:
            pass

    # Line-level checks
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Check for common typos
        if re.match(r'^\s*RewriteRule\s+.*\[.*R=30[^12]', stripped):
            issues.append({
                "id": "suspicious-redirect-code",
                "severity": "warning",
                "message": f"Line {i}: Unusual redirect status code (expected 301 or 302)",
                "line": i,
            })

    if args.format == "json":
        result = {
            "file": args.file,
            "lines": len(lines),
            "issues": issues,
            "errors": sum(1 for i in issues if i["severity"] == "error"),
            "warnings": sum(1 for i in issues if i["severity"] == "warning"),
            "info": sum(1 for i in issues if i["severity"] == "info"),
        }
        print(json.dumps(result, indent=2))
    elif args.format == "markdown":
        print(f"# Lint: {args.file}\n")
        if not issues:
            print("No issues found.")
        else:
            print(f"| Severity | ID | Message |")
            print(f"|----------|-----|---------|")
            for i in issues:
                icon = {"error": "🔴", "warning": "🟡", "info": "🔵"}[i["severity"]]
                print(f"| {icon} {i['severity']} | {i['id']} | {i['message']} |")
    else:
        if not issues:
            print(f"✅ {args.file}: No issues found.")
        else:
            icons = {"error": "✗", "warning": "!", "info": "i"}
            for i in issues:
                print(f"  [{icons[i['severity']]}] {i['id']}: {i['message']}")
            errors = sum(1 for i in issues if i["severity"] == "error")
            warnings = sum(1 for i in issues if i["severity"] == "warning")
            print(f"\n  {errors} error(s), {warnings} warning(s), {len(issues) - errors - warnings} info")

    if args.strict and any(i["severity"] == "error" for i in issues):
        sys.exit(1)


def cmd_explain(args):
    """Explain directives in an .htaccess file."""
    try:
        with open(args.file) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.", file=sys.stderr)
        sys.exit(1)

    DIRECTIVE_EXPLANATIONS = {
        r'RewriteEngine\s+On': "Enables the URL rewriting engine (mod_rewrite)",
        r'RewriteCond\s+%\{HTTP_HOST\}': "Condition: matches against the requested hostname",
        r'RewriteCond\s+%\{HTTPS\}\s+off': "Condition: request is NOT using HTTPS",
        r'RewriteCond\s+%\{REQUEST_FILENAME\}\s+!-f': "Condition: requested file does not exist on disk",
        r'RewriteCond\s+%\{REQUEST_FILENAME\}\s+!-d': "Condition: requested path is not a directory",
        r'RewriteRule': "Rewrites URL based on pattern → substitution [flags]",
        r'Redirect\s+301': "Permanent redirect (301) — search engines update their index",
        r'Redirect\s+302': "Temporary redirect (302) — search engines keep original URL",
        r'Options\s+.*-Indexes': "Disables directory listing when no index file exists",
        r'Header\s+set\s+X-Content-Type-Options': "Prevents MIME-type sniffing (security)",
        r'Header\s+set\s+X-Frame-Options': "Controls whether page can be loaded in iframe (clickjacking protection)",
        r'Header\s+.*Strict-Transport-Security': "HSTS: forces HTTPS for specified duration",
        r'Header\s+set\s+Content-Security-Policy': "CSP: controls which resources the browser can load",
        r'Header\s+set\s+Access-Control-Allow-Origin': "CORS: specifies which origins can access resources",
        r'ExpiresActive\s+On': "Enables browser caching via mod_expires",
        r'ExpiresByType': "Sets cache duration for specific MIME types",
        r'ErrorDocument': "Custom error page for specific HTTP status code",
        r'AddOutputFilterByType\s+DEFLATE': "Enables gzip compression for specified content types",
        r'Require\s+all\s+denied': "Blocks all access to the matched file/directory",
        r'<IfModule': "Conditional block: only applies if the specified module is loaded",
        r'<Files': "Applies directives to matching filenames",
        r'<FilesMatch': "Applies directives to filenames matching regex pattern",
    }

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        explanation = None
        for pattern, desc in DIRECTIVE_EXPLANATIONS.items():
            if re.search(pattern, stripped):
                explanation = desc
                break

        if explanation:
            print(f"  L{i:3d}: {stripped}")
            print(f"        → {explanation}")
        elif stripped.startswith("</"):
            continue  # Skip closing tags
        else:
            print(f"  L{i:3d}: {stripped}")


def cmd_presets(args):
    """List available presets for generation."""
    categories = {
        "Rewrites": list(REWRITE_TEMPLATES.keys()),
        "Security": list(SECURITY_HEADERS.keys()),
        "Caching": list(CACHING_RULES.keys()),
        "CORS": list(CORS_RULES.keys()),
        "Protection": list(PROTECTION_RULES.keys()),
        "Error Pages": list(ERROR_PAGES.keys()),
    }

    if args.format == "json":
        print(json.dumps(categories, indent=2))
    else:
        for cat, items in categories.items():
            print(f"\n{cat}:")
            for item in items:
                print(f"  - {item}")


def main():
    parser = argparse.ArgumentParser(
        prog="htaccess",
        description="Generate, validate, and lint Apache .htaccess files.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    sub = parser.add_subparsers(dest="command", required=True)

    # generate
    p_gen = sub.add_parser("generate", help="Generate .htaccess rules")
    p_gen.add_argument("--rewrites", nargs="+", help="Rewrite rules (e.g., http-to-https www-to-non-www)")
    p_gen.add_argument("--security", choices=["basic", "strict"], help="Security headers level")
    p_gen.add_argument("--caching", choices=["standard", "aggressive"], help="Browser caching")
    p_gen.add_argument("--cors", choices=["permissive", "specific"], help="CORS rules")
    p_gen.add_argument("--protect", nargs="+", help="Protection rules")
    p_gen.add_argument("--compression", action="store_true", help="Add gzip compression")
    p_gen.add_argument("--error-pages", nargs="+", help="Custom error pages (e.g., 404 500)")
    p_gen.add_argument("--redirects", nargs="+", help="Redirects as 'from -> to' (e.g., '/old -> /new')")
    p_gen.add_argument("--domain", help="Domain for CORS/hotlinking rules")
    p_gen.add_argument("-o", "--output", help="Output file (default: stdout)")

    # lint
    p_lint = sub.add_parser("lint", help="Lint an .htaccess file")
    p_lint.add_argument("file", help=".htaccess file to lint")
    p_lint.add_argument("--severity", nargs="+", choices=["error", "warning", "info"])
    p_lint.add_argument("--strict", action="store_true", help="Exit 1 on errors")
    p_lint.add_argument("-f", "--format", choices=["text", "json", "markdown"], default="text")

    # explain
    p_explain = sub.add_parser("explain", help="Explain directives in .htaccess file")
    p_explain.add_argument("file", help=".htaccess file to explain")

    # presets
    p_presets = sub.add_parser("presets", help="List available presets")
    p_presets.add_argument("-f", "--format", choices=["text", "json"], default="text")

    args = parser.parse_args()

    commands = {
        "generate": cmd_generate,
        "lint": cmd_lint,
        "explain": cmd_explain,
        "presets": cmd_presets,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
