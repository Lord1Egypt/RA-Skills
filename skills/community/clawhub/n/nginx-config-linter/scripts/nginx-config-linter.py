#!/usr/bin/env python3
"""Nginx Config Linter — lint, validate, and audit nginx configurations."""

import sys
import os
import re
import json
import glob
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

    def __lt__(self, other):
        order = {Severity.ERROR: 0, Severity.WARNING: 1, Severity.INFO: 2}
        return order[self] < order[other]


@dataclass
class Issue:
    rule: str
    severity: Severity
    message: str
    line: int = 0
    category: str = "syntax"
    fix: str = ""


@dataclass
class LintResult:
    file: str
    issues: list = field(default_factory=list)
    errors: int = 0
    warnings: int = 0
    infos: int = 0


# ── Nginx parser (lightweight) ──────────────────────────────────────

def parse_nginx_tokens(content: str):
    """Tokenize nginx config into a list of (line_no, token) pairs."""
    tokens = []
    line_no = 1
    i = 0
    while i < len(content):
        c = content[i]
        if c == '\n':
            line_no += 1
            i += 1
        elif c == '#':
            while i < len(content) and content[i] != '\n':
                i += 1
        elif c in ' \t\r':
            i += 1
        elif c in '{};':
            tokens.append((line_no, c))
            i += 1
        elif c in ('"', "'"):
            quote = c
            j = i + 1
            while j < len(content) and content[j] != quote:
                if content[j] == '\\':
                    j += 1
                if content[j] == '\n':
                    line_no += 1
                j += 1
            if j < len(content):
                j += 1
            tokens.append((line_no, content[i:j]))
            i = j
        else:
            j = i
            while j < len(content) and content[j] not in ' \t\r\n{};#':
                j += 1
            tokens.append((line_no, content[i:j]))
            i = j
    return tokens


def parse_nginx_blocks(tokens):
    """Parse tokens into a tree of directives and blocks."""
    result = []
    i = 0
    while i < len(tokens):
        line_no, tok = tokens[i]
        if tok == '}':
            return result, i
        if tok == ';':
            i += 1
            continue
        # Collect directive args until { or ;
        args = [tok]
        arg_line = line_no
        i += 1
        while i < len(tokens) and tokens[i][1] not in ('{', ';', '}'):
            args.append(tokens[i][1])
            i += 1
        if i < len(tokens) and tokens[i][1] == '{':
            i += 1
            children, end = parse_nginx_blocks(tokens[i:])
            i += end + 1
            result.append({
                'directive': args[0],
                'args': args[1:],
                'line': arg_line,
                'block': children
            })
        else:
            if i < len(tokens) and tokens[i][1] == ';':
                i += 1
            result.append({
                'directive': args[0],
                'args': args[1:],
                'line': arg_line,
                'block': None
            })
    return result, i


def parse_config(content: str):
    """Parse nginx config string into directive tree."""
    tokens = parse_nginx_tokens(content)
    tree, _ = parse_nginx_blocks(tokens)
    return tree


def find_directives(tree, name, recursive=True):
    """Find all directives matching name in tree."""
    results = []
    for node in tree:
        if node['directive'] == name:
            results.append(node)
        if recursive and node.get('block'):
            results.extend(find_directives(node['block'], name, True))
    return results


def find_in_context(tree, context_name, directive_name):
    """Find directive_name inside context_name blocks."""
    results = []
    for node in tree:
        if node['directive'] == context_name and node.get('block'):
            results.extend(find_directives(node['block'], directive_name, True))
        if node.get('block'):
            results.extend(find_in_context(node['block'], context_name, directive_name))
    return results


def get_all_args_flat(tree, directive_name):
    """Get all args for a directive across the whole tree."""
    directives = find_directives(tree, directive_name)
    return [(d['args'], d['line']) for d in directives]


# ── Syntax rules ────────────────────────────────────────────────────

def check_syntax(content: str, tree) -> list:
    issues = []

    # Check brace matching
    open_count = content.count('{')
    close_count = content.count('}')
    if open_count != close_count:
        issues.append(Issue(
            rule="unmatched-braces",
            severity=Severity.ERROR,
            message=f"Unmatched braces: {open_count} opening, {close_count} closing",
            category="syntax"
        ))

    # Duplicate server_name
    server_blocks = find_directives(tree, 'server')
    server_names_seen = {}
    for sb in server_blocks:
        if sb.get('block'):
            names = find_directives(sb['block'], 'server_name', False)
            for n in names:
                for arg in n['args']:
                    if arg in server_names_seen:
                        issues.append(Issue(
                            rule="duplicate-server-name",
                            severity=Severity.WARNING,
                            message=f"Duplicate server_name '{arg}' (also at line {server_names_seen[arg]})",
                            line=n['line'],
                            category="syntax"
                        ))
                    else:
                        server_names_seen[arg] = n['line']

    # Duplicate location in same server
    for sb in server_blocks:
        if sb.get('block'):
            locations = find_directives(sb['block'], 'location', False)
            loc_seen = {}
            for loc in locations:
                key = ' '.join(loc['args'])
                if key in loc_seen:
                    issues.append(Issue(
                        rule="duplicate-location",
                        severity=Severity.WARNING,
                        message=f"Duplicate location '{key}' in same server block (also at line {loc_seen[key]})",
                        line=loc['line'],
                        category="syntax"
                    ))
                else:
                    loc_seen[key] = loc['line']

    # Empty blocks
    for node in _walk(tree):
        if node.get('block') is not None and len(node['block']) == 0:
            issues.append(Issue(
                rule="empty-block",
                severity=Severity.INFO,
                message=f"Empty '{node['directive']}' block",
                line=node['line'],
                category="syntax"
            ))

    # Invalid listen directive
    listens = find_directives(tree, 'listen')
    for l in listens:
        if l['args']:
            addr = l['args'][0]
            # Strip options like ssl, default_server, etc.
            port_part = addr.split(':')[-1] if ':' in addr else addr
            port_str = re.sub(r'[^0-9]', '', port_part)
            if port_str:
                port = int(port_str)
                if port < 1 or port > 65535:
                    issues.append(Issue(
                        rule="invalid-listen-port",
                        severity=Severity.ERROR,
                        message=f"Invalid listen port: {port}",
                        line=l['line'],
                        category="syntax"
                    ))

    # Root inside location
    for sb in server_blocks:
        if sb.get('block'):
            locs = find_directives(sb['block'], 'location', False)
            for loc in locs:
                if loc.get('block'):
                    roots = find_directives(loc['block'], 'root', False)
                    for r in roots:
                        issues.append(Issue(
                            rule="root-inside-location",
                            severity=Severity.WARNING,
                            message="'root' inside 'location' block — prefer 'root' at server level",
                            line=r['line'],
                            category="syntax",
                            fix="Move 'root' to server block level and use 'alias' in location if needed"
                        ))

    return issues


def _walk(tree):
    """Walk all nodes in the tree."""
    for node in tree:
        yield node
        if node.get('block'):
            yield from _walk(node['block'])


# ── Security rules ──────────────────────────────────────────────────

SECURITY_HEADERS = {
    'X-Frame-Options': 'DENY or SAMEORIGIN',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
}


def check_security(content: str, tree) -> list:
    issues = []

    # server_tokens
    st = find_directives(tree, 'server_tokens')
    if not st:
        issues.append(Issue(
            rule="server-tokens-exposed",
            severity=Severity.WARNING,
            message="server_tokens not explicitly set — nginx version exposed by default",
            category="security",
            fix="Add 'server_tokens off;' in http block"
        ))
    else:
        for s in st:
            if s['args'] and s['args'][0].lower() == 'on':
                issues.append(Issue(
                    rule="server-tokens-on",
                    severity=Severity.WARNING,
                    message="server_tokens is on — exposes nginx version",
                    line=s['line'],
                    category="security",
                    fix="Set 'server_tokens off;'"
                ))

    # SSL/TLS checks
    ssl_protocols = find_directives(tree, 'ssl_protocols')
    for sp in ssl_protocols:
        for arg in sp['args']:
            if arg.lower() in ('sslv2', 'sslv3'):
                issues.append(Issue(
                    rule="weak-ssl-protocol",
                    severity=Severity.ERROR,
                    message=f"Weak SSL protocol: {arg} — vulnerable to known attacks",
                    line=sp['line'],
                    category="security",
                    fix="Remove SSLv2/SSLv3, use 'TLSv1.2 TLSv1.3'"
                ))
            elif arg.lower() == 'tlsv1':
                issues.append(Issue(
                    rule="deprecated-tls-protocol",
                    severity=Severity.WARNING,
                    message="TLSv1.0 is deprecated — most browsers no longer support it",
                    line=sp['line'],
                    category="security",
                    fix="Use 'TLSv1.2 TLSv1.3'"
                ))
            elif arg.lower() == 'tlsv1.1':
                issues.append(Issue(
                    rule="deprecated-tls-protocol",
                    severity=Severity.WARNING,
                    message="TLSv1.1 is deprecated",
                    line=sp['line'],
                    category="security",
                    fix="Use 'TLSv1.2 TLSv1.3'"
                ))

    # autoindex
    autoindex = find_directives(tree, 'autoindex')
    for ai in autoindex:
        if ai['args'] and ai['args'][0].lower() == 'on':
            issues.append(Issue(
                rule="directory-listing",
                severity=Severity.WARNING,
                message="Directory listing enabled (autoindex on)",
                line=ai['line'],
                category="security",
                fix="Set 'autoindex off;' unless intentionally serving file listings"
            ))

    # Check for security headers via add_header
    add_headers = find_directives(tree, 'add_header')
    found_headers = set()
    for ah in add_headers:
        if ah['args']:
            found_headers.add(ah['args'][0].lower())

    for header, value in SECURITY_HEADERS.items():
        if header.lower() not in found_headers:
            issues.append(Issue(
                rule="missing-security-header",
                severity=Severity.WARNING,
                message=f"Missing security header: {header}",
                category="security",
                fix=f"Add: add_header {header} \"{value}\";"
            ))

    # HSTS
    hsts_found = False
    for ah in add_headers:
        if ah['args'] and ah['args'][0].lower() == 'strict-transport-security':
            hsts_found = True
            if len(ah['args']) > 1:
                val = ' '.join(ah['args'][1:]).strip('"').strip("'")
                match = re.search(r'max-age=(\d+)', val)
                if match and int(match.group(1)) < 31536000:
                    issues.append(Issue(
                        rule="weak-hsts",
                        severity=Severity.WARNING,
                        message=f"HSTS max-age too short ({match.group(1)}s) — recommend >= 31536000 (1 year)",
                        line=ah['line'],
                        category="security",
                        fix='add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";'
                    ))

    ssl_certs = find_directives(tree, 'ssl_certificate')
    if ssl_certs and not hsts_found:
        issues.append(Issue(
            rule="missing-hsts",
            severity=Severity.WARNING,
            message="SSL configured but HSTS header missing",
            category="security",
            fix='add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";'
        ))

    # CORS wildcard with credentials
    for ah in add_headers:
        if ah['args'] and ah['args'][0].lower() == 'access-control-allow-origin':
            if len(ah['args']) > 1 and ah['args'][1].strip('"').strip("'") == '*':
                # Check if credentials also set
                for ah2 in add_headers:
                    if (ah2['args'] and
                        ah2['args'][0].lower() == 'access-control-allow-credentials' and
                        len(ah2['args']) > 1 and ah2['args'][1].strip('"').strip("'").lower() == 'true'):
                        issues.append(Issue(
                            rule="cors-wildcard-credentials",
                            severity=Severity.ERROR,
                            message="CORS wildcard (*) with credentials — browsers will reject this",
                            line=ah['line'],
                            category="security",
                            fix="Use specific origin instead of * when credentials are enabled"
                        ))

    # Default server block check
    server_blocks = find_directives(tree, 'server')
    has_default = False
    for sb in server_blocks:
        if sb.get('block'):
            listens = find_directives(sb['block'], 'listen', False)
            for l in listens:
                if 'default_server' in l['args'] or 'default' in l['args']:
                    has_default = True
    if server_blocks and not has_default:
        issues.append(Issue(
            rule="no-default-server",
            severity=Severity.INFO,
            message="No default_server defined — first server block will handle unmatched requests",
            category="security",
            fix="Add 'listen 80 default_server;' to a catch-all server block that returns 444"
        ))

    return issues


# ── Performance rules ───────────────────────────────────────────────

def check_performance(content: str, tree) -> list:
    issues = []

    # Gzip
    gzip_dirs = find_directives(tree, 'gzip')
    gzip_on = any(d['args'] and d['args'][0].lower() == 'on' for d in gzip_dirs)
    if not gzip_on:
        issues.append(Issue(
            rule="gzip-disabled",
            severity=Severity.WARNING,
            message="Gzip compression not enabled",
            category="performance",
            fix="Add 'gzip on; gzip_types text/plain text/css application/json application/javascript;'"
        ))
    else:
        gzip_types = find_directives(tree, 'gzip_types')
        if not gzip_types:
            issues.append(Issue(
                rule="gzip-no-types",
                severity=Severity.INFO,
                message="Gzip enabled but gzip_types not specified — only text/html compressed by default",
                category="performance",
                fix="Add 'gzip_types text/plain text/css application/json application/javascript text/xml;'"
            ))

    # Keepalive
    keepalive = find_directives(tree, 'keepalive_timeout')
    if not keepalive:
        issues.append(Issue(
            rule="no-keepalive-timeout",
            severity=Severity.INFO,
            message="keepalive_timeout not explicitly set (default: 75s)",
            category="performance"
        ))

    # Worker connections
    events_blocks = find_directives(tree, 'events')
    if events_blocks:
        for eb in events_blocks:
            if eb.get('block'):
                wc = find_directives(eb['block'], 'worker_connections', False)
                if not wc:
                    issues.append(Issue(
                        rule="no-worker-connections",
                        severity=Severity.INFO,
                        message="worker_connections not set in events block (default: 512)",
                        category="performance",
                        fix="Add 'worker_connections 1024;' or higher in events block"
                    ))
                else:
                    for w in wc:
                        if w['args'] and w['args'][0].isdigit() and int(w['args'][0]) < 256:
                            issues.append(Issue(
                                rule="low-worker-connections",
                                severity=Severity.WARNING,
                                message=f"worker_connections is {w['args'][0]} — may limit concurrent connections",
                                line=w['line'],
                                category="performance",
                                fix="Increase worker_connections to at least 1024"
                            ))

    # client_max_body_size
    cmbs = find_directives(tree, 'client_max_body_size')
    if not cmbs:
        issues.append(Issue(
            rule="no-client-max-body-size",
            severity=Severity.INFO,
            message="client_max_body_size not set (default: 1m) — may be too small for file uploads",
            category="performance",
            fix="Add 'client_max_body_size 10m;' or appropriate value"
        ))

    # Large timeouts
    for timeout_dir in ('proxy_read_timeout', 'proxy_connect_timeout', 'proxy_send_timeout'):
        timeouts = find_directives(tree, timeout_dir)
        for t in timeouts:
            if t['args']:
                val = t['args'][0].rstrip('s')
                if val.isdigit() and int(val) > 300:
                    issues.append(Issue(
                        rule="large-timeout",
                        severity=Severity.INFO,
                        message=f"{timeout_dir} is {t['args'][0]} — consider if this is intentional",
                        line=t['line'],
                        category="performance"
                    ))

    # Buffering
    proxy_buffering = find_directives(tree, 'proxy_buffering')
    for pb in proxy_buffering:
        if pb['args'] and pb['args'][0].lower() == 'off':
            issues.append(Issue(
                rule="proxy-buffering-off",
                severity=Severity.INFO,
                message="proxy_buffering off — responses sent directly to client, higher memory per connection",
                line=pb['line'],
                category="performance"
            ))

    # access_log for static assets
    location_blocks = find_directives(tree, 'location')
    static_patterns = [r'\.(css|js|ico|gif|png|jpg|jpeg|svg|woff|woff2|ttf|eot)$',
                       r'^/static/', r'^/assets/', r'^/images/']
    for loc in location_blocks:
        loc_path = ' '.join(loc['args'])
        is_static = any(p in loc_path for p in ['.css', '.js', '.ico', '.png', '.jpg',
                                                  'static', 'assets', 'images', 'fonts'])
        if is_static and loc.get('block'):
            has_log_off = False
            for d in loc['block']:
                if d['directive'] == 'access_log' and d['args'] and d['args'][0] == 'off':
                    has_log_off = True
            if not has_log_off:
                issues.append(Issue(
                    rule="static-asset-logging",
                    severity=Severity.INFO,
                    message=f"Static asset location '{loc_path}' — consider 'access_log off;' to reduce I/O",
                    line=loc['line'],
                    category="performance"
                ))

    return issues


# ── Output formatting ───────────────────────────────────────────────

def format_text(results: list, min_severity: Severity) -> str:
    lines = []
    total_e = total_w = total_i = 0
    for r in results:
        filtered = [i for i in r.issues if not (i.severity > min_severity)]
        if not filtered:
            lines.append(f"✅ {r.file}: No issues found")
            continue
        lines.append(f"\n📄 {r.file}")
        lines.append("─" * 60)
        for issue in filtered:
            icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}[issue.severity.value]
            loc = f"line {issue.line}" if issue.line else "global"
            lines.append(f"  {icon} [{issue.severity.value.upper()}] {issue.message}")
            lines.append(f"     Rule: {issue.rule} | {loc} | Category: {issue.category}")
            if issue.fix:
                lines.append(f"     Fix: {issue.fix}")
        e = sum(1 for i in filtered if i.severity == Severity.ERROR)
        w = sum(1 for i in filtered if i.severity == Severity.WARNING)
        inf = sum(1 for i in filtered if i.severity == Severity.INFO)
        total_e += e
        total_w += w
        total_i += inf
        lines.append(f"  Summary: {e} errors, {w} warnings, {inf} info")

    lines.append(f"\n{'═' * 60}")
    lines.append(f"Total: {total_e} errors, {total_w} warnings, {total_i} info across {len(results)} file(s)")

    grade = 'A'
    if total_e > 0:
        grade = 'F' if total_e > 5 else 'D' if total_e > 2 else 'C'
    elif total_w > 0:
        grade = 'C' if total_w > 10 else 'B' if total_w > 3 else 'B+'

    lines.append(f"Grade: {grade}")
    return '\n'.join(lines)


def format_json(results: list, min_severity: Severity) -> str:
    output = []
    for r in results:
        filtered = [i for i in r.issues if not (i.severity > min_severity)]
        output.append({
            'file': r.file,
            'issues': [{
                'rule': i.rule,
                'severity': i.severity.value,
                'message': i.message,
                'line': i.line,
                'category': i.category,
                'fix': i.fix
            } for i in filtered],
            'errors': sum(1 for i in filtered if i.severity == Severity.ERROR),
            'warnings': sum(1 for i in filtered if i.severity == Severity.WARNING),
            'infos': sum(1 for i in filtered if i.severity == Severity.INFO),
        })
    return json.dumps(output, indent=2)


def format_markdown(results: list, min_severity: Severity) -> str:
    lines = ["# Nginx Config Lint Report\n"]
    total_e = total_w = total_i = 0
    for r in results:
        filtered = [i for i in r.issues if not (i.severity > min_severity)]
        lines.append(f"## {r.file}\n")
        if not filtered:
            lines.append("No issues found.\n")
            continue
        lines.append("| Severity | Rule | Message | Line | Fix |")
        lines.append("|----------|------|---------|------|-----|")
        for i in filtered:
            fix = i.fix.replace('|', '\\|') if i.fix else '-'
            msg = i.message.replace('|', '\\|')
            lines.append(f"| {i.severity.value.upper()} | {i.rule} | {msg} | {i.line or '-'} | {fix} |")
        e = sum(1 for i in filtered if i.severity == Severity.ERROR)
        w = sum(1 for i in filtered if i.severity == Severity.WARNING)
        inf = sum(1 for i in filtered if i.severity == Severity.INFO)
        total_e += e
        total_w += w
        total_i += inf
        lines.append(f"\n**{e} errors, {w} warnings, {inf} info**\n")

    lines.append(f"---\n**Total: {total_e} errors, {total_w} warnings, {total_i} info across {len(results)} file(s)**")
    return '\n'.join(lines)


# ── Main ────────────────────────────────────────────────────────────

def lint_file(filepath: str, mode: str = 'audit') -> LintResult:
    result = LintResult(file=filepath)
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception as e:
        result.issues.append(Issue(
            rule="file-error",
            severity=Severity.ERROR,
            message=str(e),
            category="syntax"
        ))
        result.errors = 1
        return result

    try:
        tree = parse_config(content)
    except Exception as e:
        result.issues.append(Issue(
            rule="parse-error",
            severity=Severity.ERROR,
            message=f"Failed to parse: {e}",
            category="syntax"
        ))
        result.errors = 1
        return result

    if mode in ('lint', 'audit'):
        result.issues.extend(check_syntax(content, tree))
    if mode in ('security', 'audit'):
        result.issues.extend(check_security(content, tree))
    if mode in ('performance', 'audit'):
        result.issues.extend(check_performance(content, tree))

    result.errors = sum(1 for i in result.issues if i.severity == Severity.ERROR)
    result.warnings = sum(1 for i in result.issues if i.severity == Severity.WARNING)
    result.infos = sum(1 for i in result.issues if i.severity == Severity.INFO)
    return result


def collect_files(path: str, recursive: bool) -> list:
    if os.path.isfile(path):
        return [path]
    if os.path.isdir(path):
        pattern = os.path.join(path, '**', '*.conf') if recursive else os.path.join(path, '*.conf')
        files = glob.glob(pattern, recursive=recursive)
        # Also check for nginx.conf without .conf pattern
        nginx_conf = os.path.join(path, 'nginx.conf')
        if os.path.isfile(nginx_conf) and nginx_conf not in files:
            files.append(nginx_conf)
        return sorted(files)
    return []


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print("Usage: nginx-config-linter.py <command> <path> [options]")
        print("\nCommands: lint, security, performance, audit")
        print("\nOptions:")
        print("  --format text|json|markdown  Output format (default: text)")
        print("  --severity error|warning|info  Minimum severity (default: info)")
        print("  --recursive  Scan directories recursively")
        print("  --strict  Exit 1 on any finding (CI mode)")
        sys.exit(0)

    command = args[0]
    if command not in ('lint', 'security', 'performance', 'audit'):
        print(f"Unknown command: {command}")
        print("Commands: lint, security, performance, audit")
        sys.exit(2)

    if len(args) < 2:
        print("Error: path required")
        sys.exit(2)

    path = args[1]
    fmt = 'text'
    min_sev = Severity.INFO
    recursive = False
    strict = False

    i = 2
    while i < len(args):
        if args[i] == '--format' and i + 1 < len(args):
            fmt = args[i + 1]
            i += 2
        elif args[i] == '--severity' and i + 1 < len(args):
            min_sev = Severity(args[i + 1])
            i += 2
        elif args[i] == '--recursive':
            recursive = True
            i += 1
        elif args[i] == '--strict':
            strict = True
            i += 1
        else:
            i += 1

    files = collect_files(path, recursive)
    if not files:
        print(f"No nginx config files found at: {path}")
        sys.exit(2)

    results = [lint_file(f, command) for f in files]

    if fmt == 'json':
        print(format_json(results, min_sev))
    elif fmt == 'markdown':
        print(format_markdown(results, min_sev))
    else:
        print(format_text(results, min_sev))

    total_errors = sum(r.errors for r in results)
    total_warnings = sum(r.warnings for r in results)

    if total_errors > 0:
        sys.exit(1)
    if strict and total_warnings > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
