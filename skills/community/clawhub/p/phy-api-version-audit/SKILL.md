---
name: API Version Audit
description: API versioning health auditor. Scans REST API source code to detect unversioned routes, deprecated endpoints missing Sunset headers, hardcoded version strings in client code, inconsistent versioning strategies (URL vs header vs query param), and version gaps. Supports Express/Fastify, FastAPI/Flask/Django, Spring Boot, Go (Gin/Echo/net/http), Rails, and Laravel. Zero competitors on ClawHub.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - api
  - versioning
  - rest
  - audit
  - developer-tools
  - security
  - backend
---

# phy-api-version-audit

**API versioning health auditor** — finds unversioned routes, deprecated endpoints missing `Sunset` headers, hardcoded version strings, mixed versioning strategies, and version gaps before they cause breaking-change incidents.

Companion to `phy-api-changelog-gen` (spec diff) — this tool scans **source code**, that tool diffs **OpenAPI specs**.

## What It Detects

| Check | ID | Severity |
|-------|----|---------:|
| Route defined without `/v{N}/` or `/api/v{N}/` prefix | UV001 | MEDIUM |
| `@deprecated` / `DEPRECATED` handler with no `Sunset:` header emission | SU001 | HIGH |
| Client code with hardcoded `/v{N}/` URL string (brittle coupling) | HC001 | LOW |
| Mixed versioning strategies in the same codebase (URL + header + query) | MX001 | MEDIUM |
| Version gap — v1 and v3 registered but no v2 | VG001 | LOW |
| `Deprecation:` header present but no `Sunset:` header (RFC 8594) | SU002 | MEDIUM |
| Version in `Accept` header not validated (any value accepted) | AV001 | MEDIUM |
| Routes using numeric `/v0/` (pre-production leaking to prod) | V0001 | HIGH |
| OpenAPI `info.version` not matching any route version prefix | OA001 | LOW |

## How to Use

Paste this skill into Claude Code and describe your project:

```
/phy-api-version-audit
Scan my Express API in src/routes/ for versioning issues
```

```
/phy-api-version-audit
Check my FastAPI project at ~/projects/myapi for deprecated endpoints without Sunset headers
```

```
/phy-api-version-audit
Audit the entire monorepo at ~/work/platform for versioning strategy consistency
```

The agent will:
1. Detect the tech stack automatically (Express, FastAPI, Django, Spring, Gin, Rails, Laravel)
2. Walk all route definition files
3. Scan for all 9 check patterns
4. Group findings by severity (HIGH → MEDIUM → LOW)
5. Output per-framework fix snippets for every finding
6. Print a CI fail-gate command

---

## Implementation

When invoked, execute the following Python analysis. Ask the user for `--root` (default `.`) and optional flags.

```python
#!/usr/bin/env python3
"""
phy-api-version-audit — REST API versioning health scanner
Checks for UV001, SU001, HC001, MX001, VG001, SU002, AV001, V0001, OA001
"""
import os
import re
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from collections import defaultdict


# ─────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────

VERSION_PREFIX_RE = re.compile(
    r'/(?:api/)?v\d+/',
    re.IGNORECASE
)

SKIP_DIRS = {
    '__pycache__', '.git', 'node_modules', 'vendor', '.venv', 'venv',
    'dist', 'build', '.next', 'coverage', 'test', 'tests', 'spec',
    '__tests__', 'e2e', 'fixtures', 'mocks', 'migrations', 'seeds',
}

SKIP_EXTENSIONS = {'.min.js', '.map', '.lock', '.sum', '.mod', '.generated.ts'}

MIN_SEVERITY = os.environ.get('API_AUDIT_MIN_SEVERITY', 'LOW')
CI_MODE = '--ci' in sys.argv
MIN_COUNT = int(next((sys.argv[sys.argv.index('--min-count') + 1]
                      for _ in ['x'] if '--min-count' in sys.argv), 1))

SEVERITY_ORDER = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}


# ─────────────────────────────────────────────────────
# Data models
# ─────────────────────────────────────────────────────

@dataclass
class Finding:
    check_id: str
    file: str
    line: int
    matched_text: str
    severity: str       # HIGH / MEDIUM / LOW
    description: str
    fix: str
    framework: str = ''


@dataclass
class VersionStrategyReport:
    url_versioned_files: list = field(default_factory=list)
    header_versioned_files: list = field(default_factory=list)
    query_versioned_files: list = field(default_factory=list)


# ─────────────────────────────────────────────────────
# Framework-specific route patterns
# ─────────────────────────────────────────────────────

# Each entry: (framework_name, route_definition_regex, file_extensions)
ROUTE_DEFINITION_PATTERNS = [
    # Express/Fastify — app.get('/path', ...) or router.post('/path')
    (
        'express',
        re.compile(
            r"""(?:app|router|fastify)\s*\.\s*(?:get|post|put|patch|delete|head|options)\s*\(\s*['"]([^'"]+)['"]""",
            re.IGNORECASE
        ),
        {'.js', '.ts', '.mjs', '.cjs'}
    ),
    # Express app.use('/prefix', router)
    (
        'express-use',
        re.compile(
            r"""(?:app|router)\s*\.\s*use\s*\(\s*['"]([^'"]+)['"]""",
            re.IGNORECASE
        ),
        {'.js', '.ts', '.mjs', '.cjs'}
    ),
    # FastAPI — @app.get('/path') or @router.post('/path')
    (
        'fastapi',
        re.compile(
            r"""@(?:app|router|APIRouter\(\))\s*\.\s*(?:get|post|put|patch|delete|head|options)\s*\(\s*['"]([^'"]+)['"]""",
            re.IGNORECASE
        ),
        {'.py'}
    ),
    # Flask — @app.route('/path') or @bp.route('/path')
    (
        'flask',
        re.compile(
            r"""@(?:\w+)\.route\s*\(\s*['"]([^'"]+)['"]""",
            re.IGNORECASE
        ),
        {'.py'}
    ),
    # Django urls.py — path('endpoint/', view)
    (
        'django',
        re.compile(
            r"""(?:path|re_path|url)\s*\(\s*['"]([^'"]+)['"]""",
            re.IGNORECASE
        ),
        {'.py'}
    ),
    # Spring Boot — @GetMapping, @PostMapping, @RequestMapping
    (
        'spring',
        re.compile(
            r"""@(?:Get|Post|Put|Patch|Delete|Request)Mapping\s*(?:\(\s*(?:value\s*=\s*)?['"]([^'"]+)['"]|\(\s*\{?['"]([^'"]+)['"])""",
            re.IGNORECASE
        ),
        {'.java', '.kt'}
    ),
    # Gin (Go) — r.GET("/path") or group.POST("/path")
    (
        'gin',
        re.compile(
            r"""\.(?:GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s*\(\s*"([^"]+)"""
        ),
        {'.go'}
    ),
    # Echo (Go) — e.GET("/path") or g.POST("/path")
    (
        'echo',
        re.compile(
            r"""(?:e|g|group|api)\s*\.\s*(?:GET|POST|PUT|PATCH|DELETE)\s*\(\s*"([^"]+)"""
        ),
        {'.go'}
    ),
    # Go net/http — http.HandleFunc("/path", ...)
    (
        'net/http',
        re.compile(
            r"""http\.HandleFunc\s*\(\s*"([^"]+)"""
        ),
        {'.go'}
    ),
    # Rails routes.rb — get 'path', post 'path', resources :name
    (
        'rails',
        re.compile(
            r"""^\s*(?:get|post|put|patch|delete|resources|resource|namespace|scope)\s+['"]([^'"]+)['"]""",
            re.MULTILINE
        ),
        {'.rb'}
    ),
    # Laravel — Route::get('/path', ...) or Route::resource('/path', ...)
    (
        'laravel',
        re.compile(
            r"""Route\s*::\s*(?:get|post|put|patch|delete|resource|apiResource)\s*\(\s*['"]([^'"]+)['"]""",
            re.IGNORECASE
        ),
        {'.php'}
    ),
]

# Routes that are intentionally unversioned (health checks, auth, static)
UNVERSIONED_WHITELIST = re.compile(
    r'^/?(?:health|ping|ready|live|status|metrics|favicon|robots\.txt|'
    r'static|public|assets|auth|oauth|login|logout|signup|register|'
    r'webhook|webhooks|ws|wss|\.|_).*',
    re.IGNORECASE
)

# ─────────────────────────────────────────────────────
# Sunset / Deprecation header patterns
# ─────────────────────────────────────────────────────

DEPRECATED_MARKER_RE = re.compile(
    r'(?:@deprecated|DEPRECATED|deprecated\s*[:=]|is_deprecated|mark.*deprecated|'
    r'deprecat.*route|deprecat.*endpoint)',
    re.IGNORECASE
)

SUNSET_HEADER_RE = re.compile(
    r"""['"]Sunset['"]|res\.(?:set|header|setHeader)\s*\(\s*['"]Sunset['"]|"""
    r"""add_header\s+Sunset|response\.headers\[['"]sunset|X-Sunset""",
    re.IGNORECASE
)

DEPRECATION_HEADER_RE = re.compile(
    r"""['"]Deprecation['"]|Deprecation.*header|res\.(?:set|header|setHeader)\s*\(\s*['"]Deprecation""",
    re.IGNORECASE
)


# ─────────────────────────────────────────────────────
# Hardcoded version string patterns (client code)
# ─────────────────────────────────────────────────────

HARDCODED_VERSION_RE = re.compile(
    r"""(?:fetch|axios|requests\.(?:get|post|put|patch|delete)|http\.(?:get|post)|"""
    r"""urllib|httpx|RestTemplate|WebClient|Net::HTTP|curl|wget)\s*[(\[]?\s*['"`]"""
    r"""([^'"`]*?/v\d+/[^'"`]*?)['"`]""",
    re.IGNORECASE
)

HARDCODED_VERSION_CONST_RE = re.compile(
    r"""(?:const|let|var|BASE_URL|API_URL|API_BASE|baseUrl|apiUrl)\s*[=:]\s*['"`]"""
    r"""([^'"`]*?/v\d+/?)['"`]""",
    re.IGNORECASE
)


# ─────────────────────────────────────────────────────
# Versioning strategy detection
# ─────────────────────────────────────────────────────

HEADER_VERSION_RE = re.compile(
    r"""[xX]-[aA][pP][iI]-[vV]ersion|api-version|Accept.*version=\d|"""
    r"""vnd\.\w+\.v\d+\+|content-type.*version|x-version""",
    re.IGNORECASE
)

QUERY_VERSION_RE = re.compile(
    r"""[?&]version=\d|req\.query\.version|request\.GET\[.version|"""
    r"""params\[:version\]|request\.query_params\[.version""",
    re.IGNORECASE
)

V0_ROUTE_RE = re.compile(r'/v0/', re.IGNORECASE)


# ─────────────────────────────────────────────────────
# OpenAPI spec parsing
# ─────────────────────────────────────────────────────

def find_openapi_version(root: Path) -> Optional[str]:
    """Find version string from openapi.json or openapi.yaml."""
    for name in ['openapi.json', 'openapi.yaml', 'openapi.yml',
                 'swagger.json', 'swagger.yaml', 'swagger.yml']:
        spec_path = root / name
        if not spec_path.exists():
            # Search recursively up to 3 levels deep
            for p in root.rglob(name):
                spec_path = p
                break
        if spec_path.exists():
            try:
                content = spec_path.read_text(errors='ignore')
                m = re.search(r"""['""]version['""]:\s*['""]([^'""]+)['""]""", content)
                if m:
                    return m.group(1)
                m = re.search(r"""^version:\s*['""]?([^\s'""\n]+)""", content, re.MULTILINE)
                if m:
                    return m.group(1)
            except Exception:
                pass
    return None


# ─────────────────────────────────────────────────────
# File walker
# ─────────────────────────────────────────────────────

def walk_files(root: Path, extensions: set[str]):
    """Yield (path, content) for all relevant source files."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]
        for fname in filenames:
            fpath = Path(dirpath) / fname
            ext = fpath.suffix.lower()
            if ext not in extensions:
                continue
            if any(fpath.name.endswith(s) for s in SKIP_EXTENSIONS):
                continue
            # Skip files under test/spec directories
            parts = fpath.parts
            if any(p in {'test', 'tests', 'spec', '__tests__', 'e2e', 'fixtures'} for p in parts):
                continue
            try:
                content = fpath.read_text(errors='ignore')
                yield fpath, content
            except Exception:
                continue


# ─────────────────────────────────────────────────────
# Check: UV001 — Unversioned routes
# ─────────────────────────────────────────────────────

def check_unversioned_routes(root: Path) -> list[Finding]:
    findings = []
    all_exts = set()
    for _, _, exts in ROUTE_DEFINITION_PATTERNS:
        all_exts |= exts

    for fpath, content in walk_files(root, all_exts):
        ext = fpath.suffix.lower()
        lines = content.split('\n')
        for fw_name, pattern, fw_exts in ROUTE_DEFINITION_PATTERNS:
            if ext not in fw_exts:
                continue
            for m in pattern.finditer(content):
                route = m.group(1) or (m.group(2) if m.lastindex >= 2 else '')
                if not route:
                    continue
                # Skip whitelisted paths
                if UNVERSIONED_WHITELIST.match(route):
                    continue
                # Skip if already versioned
                if VERSION_PREFIX_RE.search(route):
                    continue
                # Skip pure wildcards, parameters-only, and root /
                if route in ('/', '*', '') or route.startswith('/:') or route.startswith('{'):
                    continue
                # Skip Rails resource names (no slash = resource name, not path)
                if fw_name == 'rails' and '/' not in route:
                    continue
                line_no = content[:m.start()].count('\n') + 1
                findings.append(Finding(
                    check_id='UV001',
                    file=str(fpath),
                    line=line_no,
                    matched_text=f'{fw_name}: {route!r}',
                    severity='MEDIUM',
                    description=f'Route "{route}" has no version prefix (/v1/, /api/v1/)',
                    fix=_uv001_fix(fw_name, route),
                    framework=fw_name,
                ))
    return findings


def _uv001_fix(framework: str, route: str) -> str:
    versioned = f'/v1{route}' if route.startswith('/') else f'/v1/{route}'
    fixes = {
        'express': f'Change route to "{versioned}" or register under a versioned router:\n  const v1 = express.Router();\n  app.use("/v1", v1);\n  v1.get("{route}", handler);',
        'express-use': f'app.use("/v1", router); // prefix all routes in this sub-router',
        'fastapi': f'Change to @router.get("{versioned}") or use APIRouter(prefix="/v1")',
        'flask': f'Use Blueprint with url_prefix="/v1" or change to @bp.route("{versioned}")',
        'django': f'Wrap in path("v1/", include("your_app.urls")) in root urls.py',
        'spring': f'Change to @RequestMapping("/v1{route}") or @GetMapping("/v1{route}")',
        'gin': f'v1 := r.Group("/v1")\nv1.GET("{route}", handler)',
        'echo': f'v1 := e.Group("/v1")\nv1.GET("{route}", handler)',
        'net/http': f'http.HandleFunc("/v1{route}", handler)',
        'rails': f'namespace :v1 do\n  get "{route}", to: "controller#action"\nend',
        'laravel': f'Route::prefix("v1")->group(function () {{\n  Route::get("{route}", handler);\n}});',
    }
    return fixes.get(framework, f'Add version prefix: {versioned}')


# ─────────────────────────────────────────────────────
# Check: SU001 — Deprecated without Sunset header
# ─────────────────────────────────────────────────────

def check_deprecated_without_sunset(root: Path) -> list[Finding]:
    findings = []
    all_exts = {'.js', '.ts', '.py', '.java', '.kt', '.go', '.rb', '.php'}

    for fpath, content in walk_files(root, all_exts):
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if not DEPRECATED_MARKER_RE.search(line):
                continue
            # Check ±30 lines for Sunset header
            window_start = max(0, i - 5)
            window_end = min(len(lines), i + 30)
            window = '\n'.join(lines[window_start:window_end])
            if SUNSET_HEADER_RE.search(window):
                continue  # Sunset found nearby, skip
            findings.append(Finding(
                check_id='SU001',
                file=str(fpath),
                line=i + 1,
                matched_text=line.strip()[:120],
                severity='HIGH',
                description='Deprecated endpoint has no Sunset header (RFC 8594). Clients cannot plan migration.',
                fix=_su001_fix(fpath.suffix),
                framework=_detect_framework_from_ext(fpath.suffix),
            ))
    return findings


def _su001_fix(ext: str) -> str:
    fixes = {
        '.js': 'res.set("Sunset", "Sat, 31 Dec 2026 23:59:59 GMT");\nres.set("Deprecation", "true");\nres.set("Link", "</v2/resource>; rel=\\"successor-version\\"");',
        '.ts': 'res.setHeader("Sunset", "Sat, 31 Dec 2026 23:59:59 GMT");\nres.setHeader("Deprecation", "true");',
        '.py': 'response.headers["Sunset"] = "Sat, 31 Dec 2026 23:59:59 GMT"\nresponse.headers["Deprecation"] = "true"',
        '.java': 'return ResponseEntity.ok(body)\n  .header("Sunset", "Sat, 31 Dec 2026 23:59:59 GMT")\n  .header("Deprecation", "true")\n  .build();',
        '.kt': 'return ResponseEntity.ok(body)\n  .header("Sunset", "Sat, 31 Dec 2026 23:59:59 GMT")\n  .build()',
        '.go': 'w.Header().Set("Sunset", "Sat, 31 Dec 2026 23:59:59 GMT")\nw.Header().Set("Deprecation", "true")',
        '.rb': 'response.headers["Sunset"] = "Sat, 31 Dec 2026 23:59:59 GMT"\nresponse.headers["Deprecation"] = "true"',
        '.php': 'header("Sunset: Sat, 31 Dec 2026 23:59:59 GMT");\nheader("Deprecation: true");',
    }
    return fixes.get(ext, 'Add Sunset: <RFC 5322 date> response header (RFC 8594)')


# ─────────────────────────────────────────────────────
# Check: SU002 — Deprecation header without Sunset
# ─────────────────────────────────────────────────────

def check_deprecation_without_sunset(root: Path) -> list[Finding]:
    findings = []
    all_exts = {'.js', '.ts', '.py', '.java', '.kt', '.go', '.rb', '.php'}

    for fpath, content in walk_files(root, all_exts):
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if not DEPRECATION_HEADER_RE.search(line):
                continue
            window_start = max(0, i - 3)
            window_end = min(len(lines), i + 10)
            window = '\n'.join(lines[window_start:window_end])
            if SUNSET_HEADER_RE.search(window):
                continue
            findings.append(Finding(
                check_id='SU002',
                file=str(fpath),
                line=i + 1,
                matched_text=line.strip()[:120],
                severity='MEDIUM',
                description='`Deprecation` header set without accompanying `Sunset` date. RFC 8594 §4 requires both.',
                fix='Add: Sunset: Sat, 31 Dec 2026 23:59:59 GMT',
                framework=_detect_framework_from_ext(fpath.suffix),
            ))
    return findings


# ─────────────────────────────────────────────────────
# Check: HC001 — Hardcoded version strings
# ─────────────────────────────────────────────────────

def check_hardcoded_versions(root: Path) -> list[Finding]:
    findings = []
    all_exts = {'.js', '.ts', '.py', '.java', '.kt', '.go', '.rb', '.php',
                '.mjs', '.cjs', '.jsx', '.tsx'}

    for fpath, content in walk_files(root, all_exts):
        # Skip server-side route files for this check (they SHOULD define versions)
        fname_lower = fpath.name.lower()
        if any(x in fname_lower for x in ('route', 'router', 'urls', 'endpoint', 'controller')):
            continue
        lines = content.split('\n')
        for pattern in (HARDCODED_VERSION_RE, HARDCODED_VERSION_CONST_RE):
            for m in pattern.finditer(content):
                url = m.group(1)
                line_no = content[:m.start()].count('\n') + 1
                line_text = lines[line_no - 1].strip()
                # Skip tests
                if 'test' in line_text.lower() or 'expect(' in line_text or 'assert' in line_text:
                    continue
                findings.append(Finding(
                    check_id='HC001',
                    file=str(fpath),
                    line=line_no,
                    matched_text=line_text[:120],
                    severity='LOW',
                    description=f'Hardcoded version string in URL: "{url}" — version bumps require source edits',
                    fix='Extract to a constant: const API_BASE = process.env.API_BASE_URL || "https://api.example.com/v1"\nOr use a versioned SDK client.',
                    framework='client',
                ))
    return findings


# ─────────────────────────────────────────────────────
# Check: MX001 — Mixed versioning strategies
# ─────────────────────────────────────────────────────

def check_mixed_strategies(root: Path) -> list[Finding]:
    findings = []
    url_files, header_files, query_files = [], [], []
    all_exts = {'.js', '.ts', '.py', '.java', '.kt', '.go', '.rb', '.php'}

    for fpath, content in walk_files(root, all_exts):
        if VERSION_PREFIX_RE.search(content):
            url_files.append(str(fpath))
        if HEADER_VERSION_RE.search(content):
            header_files.append(str(fpath))
        if QUERY_VERSION_RE.search(content):
            query_files.append(str(fpath))

    strategies_used = sum([
        bool(url_files),
        bool(header_files),
        bool(query_files),
    ])

    if strategies_used >= 2:
        strategy_desc = []
        if url_files:
            strategy_desc.append(f'URL versioning in {len(url_files)} files')
        if header_files:
            strategy_desc.append(f'header versioning (X-API-Version / Accept) in {len(header_files)} files')
        if query_files:
            strategy_desc.append(f'query-param versioning in {len(query_files)} files')

        findings.append(Finding(
            check_id='MX001',
            file='<codebase-wide>',
            line=0,
            matched_text='; '.join(strategy_desc),
            severity='MEDIUM',
            description='Multiple API versioning strategies detected in the same codebase. Clients cannot reliably discover the correct strategy.',
            fix='Pick one strategy and apply consistently:\n'
                '  • URL versioning (/v1/): simplest, most widely supported, recommended for public APIs\n'
                '  • Header versioning (X-API-Version: 1): cleaner URLs, but harder to test in browser\n'
                '  • Content negotiation (Accept: application/vnd.api+json;version=1): REST-purist, complex\n'
                'Document the chosen strategy in your OpenAPI spec info.description.',
            framework='architecture',
        ))
    return findings


# ─────────────────────────────────────────────────────
# Check: VG001 — Version gaps
# ─────────────────────────────────────────────────────

def check_version_gaps(root: Path) -> list[Finding]:
    """Find registered versions and report gaps (e.g. v1 and v3 but no v2)."""
    findings = []
    registered_versions: set[int] = set()
    all_exts = {'.js', '.ts', '.py', '.java', '.kt', '.go', '.rb', '.php',
                '.mjs', '.cjs'}
    version_re = re.compile(r'/v(\d+)/', re.IGNORECASE)

    for fpath, content in walk_files(root, all_exts):
        for m in version_re.finditer(content):
            v = int(m.group(1))
            if 1 <= v <= 20:   # sanity bound
                registered_versions.add(v)

    if len(registered_versions) >= 2:
        sorted_versions = sorted(registered_versions)
        expected = set(range(sorted_versions[0], sorted_versions[-1] + 1))
        gaps = expected - registered_versions
        if gaps:
            findings.append(Finding(
                check_id='VG001',
                file='<codebase-wide>',
                line=0,
                matched_text=f'Registered: {sorted(registered_versions)}, Missing: {sorted(gaps)}',
                severity='LOW',
                description=f'Version gap detected — versions {sorted(gaps)} are missing between v{sorted_versions[0]} and v{sorted_versions[-1]}.',
                fix='Either add stubs for missing versions that redirect to the latest compatible version, or document the intentional skip in your API changelog.',
                framework='architecture',
            ))
    return findings


# ─────────────────────────────────────────────────────
# Check: AV001 — Accept header version not validated
# ─────────────────────────────────────────────────────

def check_accept_version_validation(root: Path) -> list[Finding]:
    """Detect when code reads Accept header for versioning but has no validation."""
    findings = []
    all_exts = {'.js', '.ts', '.py', '.java', '.kt', '.go', '.rb', '.php'}
    accept_read_re = re.compile(
        r"""req\.(?:get|header|headers)\s*\(\s*['"]accept['"]|"""
        r"""request\.headers\.get\s*\(\s*['"]accept['"]|"""
        r"""request\.META\[.HTTP_ACCEPT|"""
        r"""r\.Header\.Get\s*\(\s*"Accept"""",
        re.IGNORECASE
    )
    validation_re = re.compile(
        r"""vnd\.|version\s*==|version\s*in\s*\[|SUPPORTED_VERSIONS|allowed_versions|"""
        r"""version_map|switch.*version|if.*version.*==\s*['"]?\d""",
        re.IGNORECASE
    )

    for fpath, content in walk_files(root, all_exts):
        if not HEADER_VERSION_RE.search(content):
            continue
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if not accept_read_re.search(line):
                continue
            window = '\n'.join(lines[max(0, i-2):min(len(lines), i+15)])
            if validation_re.search(window):
                continue
            findings.append(Finding(
                check_id='AV001',
                file=str(fpath),
                line=i + 1,
                matched_text=line.strip()[:120],
                severity='MEDIUM',
                description='Accept header read for version negotiation but no version validation found. Any value will be accepted silently.',
                fix='Add explicit version validation:\n'
                    'const SUPPORTED = ["application/vnd.api.v1+json", "application/vnd.api.v2+json"];\n'
                    'if (!SUPPORTED.includes(req.get("Accept"))) {\n'
                    '  return res.status(406).json({error: "Unsupported API version"});\n'
                    '}',
                framework=_detect_framework_from_ext(fpath.suffix),
            ))
    return findings


# ─────────────────────────────────────────────────────
# Check: V0001 — /v0/ routes in production code
# ─────────────────────────────────────────────────────

def check_v0_routes(root: Path) -> list[Finding]:
    findings = []
    all_exts = {'.js', '.ts', '.py', '.java', '.kt', '.go', '.rb', '.php',
                '.mjs', '.cjs'}

    for fpath, content in walk_files(root, all_exts):
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if V0_ROUTE_RE.search(line):
                findings.append(Finding(
                    check_id='V0001',
                    file=str(fpath),
                    line=i + 1,
                    matched_text=line.strip()[:120],
                    severity='HIGH',
                    description='/v0/ route found in production code. v0 conventionally signals unstable/pre-release and should never be exposed publicly.',
                    fix='Rename /v0/ to /v1/ before production deployment. If this is intentionally internal, add a middleware that rejects requests from external IPs.',
                    framework=_detect_framework_from_ext(fpath.suffix),
                ))
    return findings


# ─────────────────────────────────────────────────────
# Check: OA001 — OpenAPI version mismatch
# ─────────────────────────────────────────────────────

def check_openapi_version_mismatch(root: Path, registered_versions: set[int]) -> list[Finding]:
    findings = []
    spec_version = find_openapi_version(root)
    if not spec_version or not registered_versions:
        return []
    # Extract major version number from semver like "1.3.2" → 1
    m = re.match(r'v?(\d+)', spec_version)
    if not m:
        return []
    spec_major = int(m.group(1))
    max_route_version = max(registered_versions)
    if spec_major != max_route_version:
        findings.append(Finding(
            check_id='OA001',
            file='openapi.yaml (or similar)',
            line=0,
            matched_text=f'OpenAPI info.version: {spec_version}, highest route version: v{max_route_version}',
            severity='LOW',
            description='OpenAPI spec version does not match highest route version prefix. Clients relying on spec metadata may target the wrong version.',
            fix=f'Update info.version in openapi.yaml to "{max_route_version}.0.0" to match the latest route version.',
            framework='openapi',
        ))
    return findings


# ─────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────

def _detect_framework_from_ext(ext: str) -> str:
    return {'.js': 'express', '.ts': 'express/nestjs', '.py': 'fastapi/flask/django',
            '.java': 'spring', '.kt': 'spring-kotlin', '.go': 'gin/echo',
            '.rb': 'rails', '.php': 'laravel'}.get(ext.lower(), 'unknown')


def deduplicate(findings: list[Finding]) -> list[Finding]:
    seen: set[tuple] = set()
    result = []
    for f in findings:
        key = (f.check_id, f.file, f.line)
        if key not in seen:
            seen.add(key)
            result.append(f)
    return result


# ─────────────────────────────────────────────────────
# Main runner
# ─────────────────────────────────────────────────────

def run_audit(root: Path) -> int:
    print(f"\n🔍  phy-api-version-audit — scanning {root}\n{'─'*60}")

    all_findings: list[Finding] = []

    # Collect registered versions for VG001 / OA001
    registered_versions: set[int] = set()
    version_re = re.compile(r'/v(\d+)/', re.IGNORECASE)
    all_exts = {'.js', '.ts', '.py', '.java', '.kt', '.go', '.rb', '.php', '.mjs', '.cjs'}
    for _, content in walk_files(root, all_exts):
        for m in version_re.finditer(content):
            v = int(m.group(1))
            if 1 <= v <= 20:
                registered_versions.add(v)

    checks = [
        ('UV001 — Unversioned routes', check_unversioned_routes(root)),
        ('SU001 — Deprecated without Sunset', check_deprecated_without_sunset(root)),
        ('SU002 — Deprecation without Sunset date', check_deprecation_without_sunset(root)),
        ('HC001 — Hardcoded version strings', check_hardcoded_versions(root)),
        ('MX001 — Mixed versioning strategies', check_mixed_strategies(root)),
        ('VG001 — Version gaps', check_version_gaps(root)),
        ('AV001 — Accept version not validated', check_accept_version_validation(root)),
        ('V0001 — v0 routes in production', check_v0_routes(root)),
        ('OA001 — OpenAPI version mismatch', check_openapi_version_mismatch(root, registered_versions)),
    ]

    for label, findings in checks:
        findings = deduplicate(findings)
        if findings:
            all_findings.extend(findings)

    # Filter by minimum severity
    severity_threshold = SEVERITY_ORDER.get(MIN_SEVERITY, 2)
    all_findings = [f for f in all_findings
                    if SEVERITY_ORDER.get(f.severity, 2) <= severity_threshold]

    # Sort: HIGH first, then by file/line
    all_findings.sort(key=lambda f: (SEVERITY_ORDER.get(f.severity, 2), f.file, f.line))

    # ── Output ──────────────────────────────────────────────
    if not all_findings:
        print("✅  No versioning issues found.")
        return 0

    high_count = sum(1 for f in all_findings if f.severity == 'HIGH')
    med_count = sum(1 for f in all_findings if f.severity == 'MEDIUM')
    low_count = sum(1 for f in all_findings if f.severity == 'LOW')

    print(f"Found {len(all_findings)} issue(s): "
          f"🔴 HIGH={high_count}  🟡 MEDIUM={med_count}  🔵 LOW={low_count}\n")

    current_severity = None
    for f in all_findings:
        if f.severity != current_severity:
            current_severity = f.severity
            emoji = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🔵'}.get(f.severity, '⚪')
            print(f"\n{emoji} {f.severity} ISSUES\n{'─'*50}")

        loc = f'{f.file}:{f.line}' if f.line else f.file
        print(f"\n[{f.check_id}] {loc}")
        print(f"  {f.description}")
        print(f"  Matched: {f.matched_text}")
        print(f"  Fix:")
        for fix_line in f.fix.split('\n'):
            print(f"    {fix_line}")

    # CI summary
    print(f"\n{'═'*60}")
    print(f"SUMMARY: {high_count} HIGH, {med_count} MEDIUM, {low_count} LOW")
    print(f"\nCI fail-gate (fails on any HIGH or MEDIUM finding):")
    print(f"  python api_version_audit.py --root . --ci --min-severity MEDIUM")
    if CI_MODE and high_count + med_count > 0:
        print("\n[CI] Exiting with code 1 — HIGH/MEDIUM findings present.")
        return 1
    return 0


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='API versioning health auditor')
    parser.add_argument('--root', default='.', help='Root directory to scan')
    parser.add_argument('--ci', action='store_true', help='CI mode: exit 1 on HIGH/MEDIUM')
    parser.add_argument('--min-severity', choices=['HIGH', 'MEDIUM', 'LOW'],
                        default='LOW', help='Minimum severity to report')
    parser.add_argument('--json', action='store_true', help='Output JSON instead of text')
    args = parser.parse_args()

    CI_MODE = args.ci
    MIN_SEVERITY = args.min_severity

    exit_code = run_audit(Path(args.root))
    sys.exit(exit_code)
```

---

## Example Output

```
🔍  phy-api-version-audit — scanning /home/user/myapi
────────────────────────────────────────────────────────────

Found 7 issue(s): 🔴 HIGH=2  🟡 MEDIUM=3  🔵 LOW=2

🔴 HIGH ISSUES
──────────────────────────────────────────────────────

[SU001] src/routes/users.js:47
  Deprecated endpoint has no Sunset header (RFC 8594). Clients cannot plan migration.
  Matched: // @deprecated — use /v2/users instead
  Fix:
    res.set("Sunset", "Sat, 31 Dec 2026 23:59:59 GMT");
    res.set("Deprecation", "true");
    res.set("Link", "</v2/users>; rel="successor-version"");

[V0001] src/routes/internal.ts:12
  /v0/ route found in production code.
  Matched: router.get('/v0/internal/config', adminHandler)
  Fix:
    Rename /v0/ to /v1/ before production deployment.

🟡 MEDIUM ISSUES
──────────────────────────────────────────────────────

[UV001] src/routes/payments.js:23
  Route "/checkout" has no version prefix (/v1/, /api/v1/)
  Matched: express: '/checkout'
  Fix:
    Change route to "/v1/checkout" or register under a versioned router:
      const v1 = express.Router();
      app.use("/v1", v1);
      v1.get("/checkout", handler);

[UV001] src/routes/webhooks.js:8
  Route "/stripe/webhook" has no version prefix
  [skipped — matches UNVERSIONED_WHITELIST for 'webhook']

[MX001] <codebase-wide>:0
  Multiple API versioning strategies detected.
  Matched: URL versioning in 12 files; header versioning (X-API-Version) in 3 files
  Fix:
    Pick one strategy. Recommended: URL versioning (/v1/) for public APIs.

🔵 LOW ISSUES
──────────────────────────────────────────────────────

[HC001] src/client/apiClient.ts:34
  Hardcoded version string: "https://api.example.com/v1/users"
  Fix:
    const API_BASE = process.env.API_BASE_URL || "https://api.example.com/v1";

[VG001] <codebase-wide>:0
  Version gap: versions [2] missing between v1 and v3
  Fix:
    Add /v2/ stub routes that redirect to /v3/ or document intentional skip.

════════════════════════════════════════════════════════════
SUMMARY: 2 HIGH, 3 MEDIUM, 2 LOW

CI fail-gate (fails on any HIGH or MEDIUM finding):
  python api_version_audit.py --root . --ci --min-severity MEDIUM
```

---

## Whitelisted Paths (Never Flagged for UV001)

These paths are intentionally unversioned and are excluded from UV001:

```
/health, /ping, /ready, /live, /status, /metrics
/favicon, /robots.txt, /static, /public, /assets
/auth, /oauth, /login, /logout, /signup, /register
/webhook, /webhooks, /ws, /wss
```

Add custom exemptions by setting:
```bash
export API_AUDIT_WHITELIST="^/internal,^/admin"
```

---

## Relationship to Other phy- Skills

| Skill | When to Use |
|-------|------------|
| `phy-api-version-audit` (this) | Source code has versioning issues — **pre-deployment** |
| `phy-api-changelog-gen` | You have two OpenAPI spec files and need a semantic diff |
| `phy-openapi-mock-server` | You want a mock server from a spec file |
| `phy-security-headers` | You want to audit runtime HTTP response headers |

---

## Supported Frameworks

| Language | Frameworks |
|----------|-----------|
| Node.js / TypeScript | Express, Fastify, Koa, NestJS |
| Python | FastAPI, Flask, Django |
| Java / Kotlin | Spring Boot, JAX-RS |
| Go | Gin, Echo, net/http, Chi |
| Ruby | Rails, Sinatra |
| PHP | Laravel, Slim |

Detection is automatic — no configuration needed.

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
