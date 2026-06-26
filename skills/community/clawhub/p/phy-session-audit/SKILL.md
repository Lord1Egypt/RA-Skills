---
name: Session Audit
description: Session and cookie security auditor (OWASP A07:2021 — Identification and Authentication Failures). Scans Express/Koa/Fastify, Flask/Django/FastAPI, Go net/http, Spring Boot, and Rails source code for 10 session management weaknesses — missing HttpOnly/Secure/SameSite cookie flags, session token in URL, session fixation (no regenerate after login), missing CSRF protection, session data in localStorage, missing session timeout, weak session ID generation, and overly broad cookie domain scope. Zero external dependencies. CI fail-gate included.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - security
  - session
  - cookie
  - csrf
  - owasp
  - authentication
  - static-analysis
  - zero-deps
  - express
  - flask
  - django
  - spring
  - rails
---

# phy-session-audit — Session & Cookie Security Auditor

Scans source code for **10 session management vulnerabilities** that enable session hijacking, CSRF attacks, session fixation, and account takeover. Maps to **OWASP A07:2021 — Identification and Authentication Failures**.

## Quick Start

```bash
# Scan a directory
python session_audit.py ./src

# Single file
python session_audit.py src/middleware/session.js

# CI mode — exit 1 on CRITICAL or HIGH
python session_audit.py ./src --ci

# Only show CRITICAL findings
python session_audit.py ./src --only-severity CRITICAL
```

## The 10 Checks

| ID | Severity | Check | CWE |
|----|----------|-------|-----|
| SS001 | CRITICAL | Missing HttpOnly flag on session cookie | CWE-1004 |
| SS002 | HIGH | Missing Secure flag on session cookie | CWE-614 |
| SS003 | HIGH | Missing SameSite attribute on session cookie | CWE-352 |
| SS004 | CRITICAL | Session token / auth token in URL query string | CWE-598 |
| SS005 | CRITICAL | No session regeneration after login (session fixation) | CWE-384 |
| SS006 | HIGH | Missing CSRF protection on state-changing routes | CWE-352 |
| SS007 | HIGH | Session/auth data stored in localStorage | CWE-922 |
| SS008 | MEDIUM | Session timeout not configured (indefinite sessions) | CWE-613 |
| SS009 | MEDIUM | Weak session ID — not using cryptographically secure source | CWE-330 |
| SS010 | MEDIUM | Session cookie domain scope too broad (e.g., domain=.example.com) | CWE-565 |

### SS001 — Missing HttpOnly (CRITICAL)
Finds `Set-Cookie` headers and session configuration without `httpOnly: true` or `HttpOnly` flag. Without HttpOnly, any XSS vulnerability on any page can steal the session cookie via `document.cookie`.

**Detected patterns:** `res.cookie(name, val, {})` without `httpOnly: true`, `cookie_secure=False` in Django, `SESSION_COOKIE_HTTPONLY = False`, `set_cookie(key, value)` without `httponly=True`.

### SS002 — Missing Secure Flag (HIGH)
Session cookies without `Secure` flag are sent over plain HTTP connections (if the browser is redirected or the user types http://). Attacker on same network can intercept with passive MITM.

### SS003 — Missing SameSite (HIGH)
Without `SameSite=Strict` or `SameSite=Lax`, the browser sends session cookies on cross-origin requests — enabling CSRF attacks even if a CSRF token library is used but misconfigured. Default before Chrome 80 was `SameSite=None`.

### SS004 — Session Token in URL (CRITICAL)
Finds `req.query.token`, `request.args.get('session_id')`, `?auth=`, `?session=`, `?token=` used as authentication. URL tokens appear in server logs, browser history, Referer headers, and CDN access logs.

### SS005 — Session Fixation (CRITICAL)
After successful login (`password.check()`, `authenticate()`, `login(user)`, `bcrypt.compare()`), the session ID must be regenerated. Finds login success paths without `req.session.regenerate()`, `session.cycle_key()`, `request.session.flush()`, `session.save()` after a fresh session create. Session fixation lets an attacker pre-set a known session ID and hijack the session post-login.

### SS006 — Missing CSRF Protection (HIGH)
Finds POST/PUT/PATCH/DELETE route definitions without CSRF middleware or token validation nearby. Detects framework-specific CSRF patterns: `csurf`, `csrf_token`, `CsrfViewMiddleware`, `@csrf_protect`, `protect_from_forgery`, `_token` verification.

### SS007 — Auth in localStorage (HIGH)
Finds `localStorage.setItem('token'`, `localStorage.setItem('session'`, `localStorage.setItem('auth'`. localStorage is accessible to JavaScript from any script on the page — a single XSS vulnerability exposes every stored credential. Use HttpOnly cookies instead.

### SS008 — No Session Timeout (MEDIUM)
Finds session configuration without `maxAge`, `expires`, `cookie_age`, `SESSION_COOKIE_AGE`, `MaxInactiveInterval`. Indefinite sessions mean a stolen session token is valid forever.

### SS009 — Weak Session ID Source (MEDIUM)
Finds session ID generation using `random.random()`, `Math.random()`, `uuid.uuid4()` without `secrets` module, `str(time.time())`, or sequential IDs. Session IDs must use a cryptographically secure source.

### SS010 — Overly Broad Cookie Domain (MEDIUM)
Finds `domain: '.example.com'` (leading dot) — this shares the cookie across all subdomains including potentially compromised ones (e.g., user-uploaded content on `uploads.example.com`).

## Sample Output

```
============================================================
  Session Audit — src/
  Files scanned: 31  |  Files flagged: 5
============================================================

── CRITICAL (3) ────────────────────────────────────────────
🔴 SS001 [CRITICAL] src/middleware/session.js:12
   Session cookie set without httpOnly: true. XSS → instant session theft via document.cookie.
   CWE: CWE-1004: Sensitive Cookie Without 'HttpOnly' Flag
   Fix: res.cookie('session', token, { httpOnly: true, secure: true, sameSite: 'Strict' })

🔴 SS004 [CRITICAL] src/routes/auth.js:45
   Auth token in URL query string: req.query.token used for authentication.
   CWE: CWE-598: Token Exposed in URL
   Fix: Move token to Authorization: Bearer header. Never authenticate via query string.

🔴 SS005 [CRITICAL] src/routes/login.js:78
   Login success (bcrypt.compare) with no session regeneration nearby.
   CWE: CWE-384: Session Fixation
   Fix: req.session.regenerate((err) => { req.session.userId = user.id; res.redirect('/dashboard'); })

── HIGH (2) ────────────────────────────────────────────────
🟠 SS003 [HIGH] src/app.js:23
   Session cookie has no SameSite attribute. CSRF attacks work even if CSRF token is missing.
   CWE: CWE-352: Cross-Site Request Forgery
   Fix: app.use(session({ cookie: { sameSite: 'Strict' } }))

🟠 SS007 [HIGH] src/utils/auth.js:91
   JWT stored in localStorage: localStorage.setItem('token', jwt).
   CWE: CWE-922: Insecure Storage of Sensitive Information
   Fix: Store JWT in HttpOnly cookie. If SPA: use memory variable (lost on refresh) + refresh token in HttpOnly cookie.

── MEDIUM (1) ──────────────────────────────────────────────
🟡 SS008 [MEDIUM] src/app.js:18
   Session configured without maxAge/expires. Sessions never expire — stolen tokens valid forever.
   CWE: CWE-613: Insufficient Session Expiration
   Fix: cookie: { maxAge: 8 * 60 * 60 * 1000 }  (8 hours — adjust to your security requirements)

────────────────────────────────────────────────────────────
  Total: 6 findings
  Critical: 3 | High: 2 | Medium: 1

  ❌ CI GATE FAILED — resolve CRITICAL/HIGH findings before merging.
```

## The Script

```python
#!/usr/bin/env python3
"""
phy-session-audit — Session & Cookie Security Auditor
OWASP A07:2021 — Identification and Authentication Failures
Scans Express/Flask/Django/Go/Spring/Rails for session management vulnerabilities.
Zero external dependencies.
"""

import sys
import re
from dataclasses import dataclass, field
from pathlib import Path


# ─── Data Structures ─────────────────────────────────────────────────────────

@dataclass
class Finding:
    check_id: str
    severity: str      # CRITICAL / HIGH / MEDIUM
    location: str
    message: str
    cwe: str = ""
    fix: str = ""

    def __str__(self) -> str:
        icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}.get(self.severity, "⚪")
        parts = [f"{icon} {self.check_id} [{self.severity}] {self.location}"]
        parts.append(f"   {self.message}")
        if self.cwe:
            parts.append(f"   CWE: {self.cwe}")
        if self.fix:
            parts.append(f"   Fix: {self.fix}")
        return "\n".join(parts)


@dataclass
class AuditResult:
    scan_root: str
    files_scanned: int = 0
    files_flagged: int = 0
    findings: list = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "CRITICAL")

    @property
    def high_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "HIGH")

    @property
    def medium_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "MEDIUM")


# ─── Constants ────────────────────────────────────────────────────────────────

# SS001 — Missing HttpOnly
COOKIE_SET_RE = re.compile(
    r"(res\.cookie\s*\(|response\.set_cookie\s*\(|set_cookie\s*\(|"
    r"cookie\s*\(\s*['\"]|SESSION_COOKIE_HTTPONLY\s*=|"
    r"cookie_httponly\s*=|setcookie\s*\()",
    re.IGNORECASE,
)

HTTPONLY_PRESENT_RE = re.compile(
    r"(httpOnly\s*:\s*true|httponly\s*=\s*True|HttpOnly|http_only\s*=\s*True|"
    r"SESSION_COOKIE_HTTPONLY\s*=\s*True)",
    re.IGNORECASE,
)

HTTPONLY_DISABLED_RE = re.compile(
    r"(httpOnly\s*:\s*false|httponly\s*=\s*False|SESSION_COOKIE_HTTPONLY\s*=\s*False)",
    re.IGNORECASE,
)

# SS002 — Missing Secure flag
SECURE_PRESENT_RE = re.compile(
    r"(secure\s*:\s*true|secure\s*=\s*True|;\s*Secure|"
    r"SESSION_COOKIE_SECURE\s*=\s*True|cookie_secure\s*=\s*True)",
    re.IGNORECASE,
)

SECURE_DISABLED_RE = re.compile(
    r"(secure\s*:\s*false|secure\s*=\s*False|SESSION_COOKIE_SECURE\s*=\s*False)",
    re.IGNORECASE,
)

# SS003 — Missing SameSite
SAMESITE_PRESENT_RE = re.compile(
    r"(sameSite|samesite|SameSite|same_site)",
    re.IGNORECASE,
)

SAMESITE_NONE_RE = re.compile(
    r"(sameSite\s*:\s*['\"]none['\"]|samesite\s*=\s*['\"]?none['\"]?)",
    re.IGNORECASE,
)

# SS004 — Token in URL
URL_TOKEN_RE = re.compile(
    r"(req\.query\.(token|session_id|auth|session|access_token|api_key)|"
    r"request\.args\.get\s*\(\s*['\"](?:token|session_id|auth|session|access_token)['\"]|"
    r"c\.Query\s*\(\s*['\"](?:token|session|auth)['\"]|"
    r"request\.getParameter\s*\(\s*['\"](?:token|session|auth)['\"]|"
    r"\?token=|\?session=|\?auth=|\?access_token=)",
    re.IGNORECASE,
)

# SS005 — Session fixation (no regenerate after login)
LOGIN_SUCCESS_RE = re.compile(
    r"(bcrypt\.compare|bcrypt\.check|password_verify|"
    r"authenticate\s*\(|login\s*\(user|checkpw\s*\(|"
    r"verify_password\s*\(|checkCredentials|validateLogin)",
    re.IGNORECASE,
)

SESSION_REGENERATE_RE = re.compile(
    r"(req\.session\.regenerate|session\.regenerate|"
    r"session\.cycle_key\(\)|request\.session\.flush\(\)|"
    r"session\.invalidate\(\)|SecurityContextHolder\.clearContext|"
    r"reset_session\(\)|request\.change_session_id)",
    re.IGNORECASE,
)

# SS006 — CSRF protection
POST_ROUTE_RE = re.compile(
    r"""(app|router)\.(post|put|patch|delete)\s*\(\s*['"`]""",
    re.IGNORECASE,
)

PYTHON_POST_ROUTE_RE = re.compile(
    r"""@(app|router|blueprint)\.(post|put|patch|delete)\s*\(""",
    re.IGNORECASE,
)

CSRF_GUARD_RE = re.compile(
    r"(csurf|csrf_token|CsrfViewMiddleware|@csrf_protect|"
    r"protect_from_forgery|_token|csrf\.protect|"
    r"validateCsrfToken|verify_csrf_token|X-CSRF-Token|"
    r"CsrfTokenRepository|@EnableWebSecurity)",
    re.IGNORECASE,
)

# SS007 — Auth in localStorage
LOCALSTORAGE_AUTH_RE = re.compile(
    r"localStorage\.setItem\s*\(\s*['\"](?:token|session|auth|jwt|access_token|"
    r"refresh_token|bearer|user_token|authToken|sessionToken)['\"]",
    re.IGNORECASE,
)

# SS008 — No session timeout
SESSION_CONFIG_RE = re.compile(
    r"(app\.use\s*\(\s*session\s*\(|SessionMiddleware\s*\(|"
    r"SESSION_COOKIE_AGE|session\.permanent|"
    r"setMaxInactiveInterval|gorilla/sessions\.NewCookieStore)",
    re.IGNORECASE,
)

TIMEOUT_PRESENT_RE = re.compile(
    r"(maxAge|max_age|expires|SESSION_COOKIE_AGE|"
    r"MaxInactiveInterval|cookie_age|session\.permanent\s*=\s*True)",
    re.IGNORECASE,
)

# SS009 — Weak session ID
WEAK_SESSION_ID_RE = re.compile(
    r"(random\.random\s*\(\)|random\.randint\s*\(|Math\.random\s*\(\)|"
    r"str\s*\(\s*time\.time\s*\(\)\s*\)|time\.time\s*\(\)\s*\.hex|"
    r"session_id\s*=\s*str\s*\(\s*\d|uuid\.uuid4\s*\(\)\s*\.hex)",
    re.IGNORECASE,
)

# SS010 — Broad cookie domain
BROAD_DOMAIN_RE = re.compile(
    r"(domain\s*:\s*['\"]\.[\w.-]+['\"]|"
    r"domain\s*=\s*['\"]\.[\w.-]+['\"]|"
    r"SESSION_COOKIE_DOMAIN\s*=\s*['\"]\.[\w.-]+['\"])",
    re.IGNORECASE,
)

SUPPORTED_EXTENSIONS = {".js", ".ts", ".jsx", ".tsx", ".py", ".go", ".java", ".kt", ".rb", ".php"}
SKIP_DIRS = {"node_modules", ".git", "venv", ".venv", "__pycache__", "dist", "build", ".next", "vendor", "test", "tests", "__tests__", "migrations"}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def get_context(lines: list, idx: int, window: int = 20) -> str:
    start = max(0, idx - window)
    end = min(len(lines), idx + window)
    return "\n".join(lines[start:end])


def collect_files(path: str) -> list:
    p = Path(path)
    if p.is_file():
        return [p] if p.suffix in SUPPORTED_EXTENSIONS else []
    files = []
    for f in p.rglob("*"):
        if any(skip in f.parts for skip in SKIP_DIRS):
            continue
        if f.is_file() and f.suffix in SUPPORTED_EXTENSIONS:
            files.append(f)
    return files


# ─── Checks ──────────────────────────────────────────────────────────────────

def check_ss001_missing_httponly(filepath: str, lines: list) -> list:
    """SS001 — Session cookie without HttpOnly flag."""
    findings = []
    for i, line in enumerate(lines):
        if not COOKIE_SET_RE.search(line):
            continue
        ctx = get_context(lines, i, 10)
        if HTTPONLY_DISABLED_RE.search(ctx):
            findings.append(Finding(
                check_id="SS001",
                severity="CRITICAL",
                location=f"{filepath}:{i + 1}",
                message="HttpOnly explicitly disabled on cookie. Any XSS can steal session via document.cookie.",
                cwe="CWE-1004: Sensitive Cookie Without 'HttpOnly' Flag",
                fix="Set httpOnly: true on all authentication cookies.",
            ))
        elif not HTTPONLY_PRESENT_RE.search(ctx):
            # Session-related cookie without explicit httpOnly
            if re.search(r"(session|auth|token|jwt)", ctx, re.IGNORECASE):
                findings.append(Finding(
                    check_id="SS001",
                    severity="CRITICAL",
                    location=f"{filepath}:{i + 1}",
                    message="Session/auth cookie set without explicit HttpOnly flag — defaults to false in most frameworks.",
                    cwe="CWE-1004: Sensitive Cookie Without 'HttpOnly' Flag",
                    fix="res.cookie('session', token, { httpOnly: true, secure: true, sameSite: 'Strict' })",
                ))
    return findings


def check_ss002_missing_secure(filepath: str, lines: list) -> list:
    """SS002 — Session cookie without Secure flag."""
    findings = []
    for i, line in enumerate(lines):
        if not COOKIE_SET_RE.search(line):
            continue
        ctx = get_context(lines, i, 10)
        if SECURE_DISABLED_RE.search(ctx):
            findings.append(Finding(
                check_id="SS002",
                severity="HIGH",
                location=f"{filepath}:{i + 1}",
                message="Secure flag explicitly disabled — cookie sent over HTTP. Passive MITM on same network intercepts session.",
                cwe="CWE-614: Sensitive Cookie in HTTPS Session Without 'Secure' Attribute",
                fix="Set secure: true (only disable in development, never production).",
            ))
        elif not SECURE_PRESENT_RE.search(ctx):
            if re.search(r"(session|auth|token|jwt)", ctx, re.IGNORECASE):
                findings.append(Finding(
                    check_id="SS002",
                    severity="HIGH",
                    location=f"{filepath}:{i + 1}",
                    message="Session/auth cookie missing Secure flag — sent over plain HTTP connections.",
                    cwe="CWE-614",
                    fix="Add secure: true to cookie options. Use SESSION_COOKIE_SECURE=True in Django.",
                ))
    return findings


def check_ss003_missing_samesite(filepath: str, lines: list) -> list:
    """SS003 — Session cookie without SameSite attribute."""
    findings = []
    for i, line in enumerate(lines):
        if not COOKIE_SET_RE.search(line):
            continue
        ctx = get_context(lines, i, 10)
        if not SAMESITE_PRESENT_RE.search(ctx):
            if re.search(r"(session|auth|token|jwt)", ctx, re.IGNORECASE):
                findings.append(Finding(
                    check_id="SS003",
                    severity="HIGH",
                    location=f"{filepath}:{i + 1}",
                    message="Session cookie missing SameSite attribute. Browser sends cookie on cross-origin requests — CSRF possible.",
                    cwe="CWE-352: Cross-Site Request Forgery",
                    fix="Add sameSite: 'Strict' (forms) or sameSite: 'Lax' (external links). Avoid sameSite: 'None' unless required.",
                ))
        elif SAMESITE_NONE_RE.search(ctx):
            findings.append(Finding(
                check_id="SS003",
                severity="HIGH",
                location=f"{filepath}:{i + 1}",
                message="SameSite=None: cookie sent on ALL cross-origin requests. Combined with Secure, but CSRF still possible on some flows.",
                cwe="CWE-352",
                fix="Use sameSite: 'Strict' or 'Lax' unless cross-site cookie sharing is explicitly required (e.g., embedded iframe).",
            ))
    return findings


def check_ss004_token_in_url(filepath: str, lines: list) -> list:
    """SS004 — Auth token passed in URL query string."""
    findings = []
    for i, line in enumerate(lines):
        m = URL_TOKEN_RE.search(line)
        if m:
            findings.append(Finding(
                check_id="SS004",
                severity="CRITICAL",
                location=f"{filepath}:{i + 1}",
                message=f"Auth token in URL query string: '{line.strip()[:70]}'. Tokens in URLs appear in server logs, browser history, and Referer headers.",
                cwe="CWE-598: Token Exposed in URL",
                fix="Use Authorization: Bearer <token> header. For redirect flows, use short-lived one-time codes, not long-lived tokens.",
            ))
    return findings


def check_ss005_session_fixation(filepath: str, lines: list) -> list:
    """SS005 — No session regeneration after login (session fixation)."""
    findings = []
    for i, line in enumerate(lines):
        if not LOGIN_SUCCESS_RE.search(line):
            continue
        ctx = get_context(lines, i, 25)
        # Only flag if this looks like a login handler (has response/redirect)
        if not re.search(r"(res\.|response\.|redirect|return|render|send)", ctx, re.IGNORECASE):
            continue
        if not SESSION_REGENERATE_RE.search(ctx):
            findings.append(Finding(
                check_id="SS005",
                severity="CRITICAL",
                location=f"{filepath}:{i + 1}",
                message="Login success without session regeneration. Attacker can fix a known session ID pre-login and hijack post-login.",
                cwe="CWE-384: Session Fixation",
                fix="req.session.regenerate((err) => { req.session.userId = user.id; res.redirect('/dashboard'); })",
            ))
    return findings


def check_ss006_missing_csrf(filepath: str, lines: list, all_content: str) -> list:
    """SS006 — State-changing route without CSRF protection."""
    # If CSRF middleware is globally configured, skip per-route checks
    if CSRF_GUARD_RE.search(all_content):
        return []

    findings = []
    for i, line in enumerate(lines):
        if not (POST_ROUTE_RE.search(line) or PYTHON_POST_ROUTE_RE.search(line)):
            continue
        if re.search(r"(webhook|health|api/|/api|grpc|rest)", line, re.IGNORECASE):
            continue  # Skip API-only or webhook endpoints
        findings.append(Finding(
            check_id="SS006",
            severity="HIGH",
            location=f"{filepath}:{i + 1}",
            message=f"State-changing route '{line.strip()[:70]}' with no CSRF protection found in project.",
            cwe="CWE-352: Cross-Site Request Forgery",
            fix=(
                "Express: npm install csurf; app.use(csrf())\n"
                "   Django: ensure CsrfViewMiddleware is in MIDDLEWARE\n"
                "   Rails: protect_from_forgery with: :exception"
            ),
        ))
        if len(findings) >= 3:
            break  # Cap at 3 to avoid noise (global fix applies to all)
    return findings


def check_ss007_localstorage_auth(filepath: str, lines: list) -> list:
    """SS007 — Auth/session data stored in localStorage."""
    findings = []
    for i, line in enumerate(lines):
        if LOCALSTORAGE_AUTH_RE.search(line):
            findings.append(Finding(
                check_id="SS007",
                severity="HIGH",
                location=f"{filepath}:{i + 1}",
                message=f"Auth token stored in localStorage: '{line.strip()[:70]}'. Accessible to any JS on the page — XSS = full credential theft.",
                cwe="CWE-922: Insecure Storage of Sensitive Information",
                fix=(
                    "Store JWT in HttpOnly cookie: res.cookie('token', jwt, { httpOnly: true, secure: true })\n"
                    "   If SPA: store access token in memory + refresh token in HttpOnly cookie."
                ),
            ))
    return findings


def check_ss008_no_session_timeout(filepath: str, lines: list) -> list:
    """SS008 — Session configured without timeout."""
    findings = []
    for i, line in enumerate(lines):
        if not SESSION_CONFIG_RE.search(line):
            continue
        ctx = get_context(lines, i, 15)
        if not TIMEOUT_PRESENT_RE.search(ctx):
            findings.append(Finding(
                check_id="SS008",
                severity="MEDIUM",
                location=f"{filepath}:{i + 1}",
                message="Session configured without maxAge/expires. Sessions never expire — stolen tokens remain valid indefinitely.",
                cwe="CWE-613: Insufficient Session Expiration",
                fix="cookie: { maxAge: 8 * 60 * 60 * 1000 }  (8 hours). For high-security: 15-30 minutes with sliding window.",
            ))
    return findings


def check_ss009_weak_session_id(filepath: str, lines: list) -> list:
    """SS009 — Weak (predictable) session ID generation."""
    findings = []
    for i, line in enumerate(lines):
        if WEAK_SESSION_ID_RE.search(line):
            # Check if this is actually being used as a session ID
            ctx = get_context(lines, i, 5)
            if re.search(r"(session|token|id|key|nonce)", ctx, re.IGNORECASE):
                findings.append(Finding(
                    check_id="SS009",
                    severity="MEDIUM",
                    location=f"{filepath}:{i + 1}",
                    message=f"Session ID generated with predictable source: '{line.strip()[:70]}'",
                    cwe="CWE-330: Use of Insufficiently Random Values",
                    fix=(
                        "Python: import secrets; session_id = secrets.token_urlsafe(32)\n"
                        "   Node.js: require('crypto').randomBytes(32).toString('hex')\n"
                        "   Use a battle-tested session library instead of rolling your own."
                    ),
                ))
    return findings


def check_ss010_broad_cookie_domain(filepath: str, lines: list) -> list:
    """SS010 — Cookie domain too broad (leading dot = all subdomains)."""
    findings = []
    for i, line in enumerate(lines):
        m = BROAD_DOMAIN_RE.search(line)
        if m:
            findings.append(Finding(
                check_id="SS010",
                severity="MEDIUM",
                location=f"{filepath}:{i + 1}",
                message=f"Cookie domain with leading dot shares across ALL subdomains: '{m.group()}'",
                cwe="CWE-565: Reliance on Cookies Without Validation and Integrity Checking",
                fix=(
                    "Use exact domain (no leading dot): domain: 'app.example.com'\n"
                    "   Leading dot .example.com shares cookie to uploads.example.com, static.example.com — attack surface."
                ),
            ))
    return findings


# ─── Main Audit ───────────────────────────────────────────────────────────────

def audit(path: str) -> AuditResult:
    result = AuditResult(scan_root=path)
    files = collect_files(path)
    result.files_scanned = len(files)

    all_contents = {}
    for f in files:
        try:
            all_contents[str(f)] = f.read_text(errors="ignore")
        except Exception:
            pass

    for f in files:
        content = all_contents.get(str(f), "")
        lines = content.splitlines()
        fp = str(f)

        file_findings = []
        file_findings.extend(check_ss001_missing_httponly(fp, lines))
        file_findings.extend(check_ss002_missing_secure(fp, lines))
        file_findings.extend(check_ss003_missing_samesite(fp, lines))
        file_findings.extend(check_ss004_token_in_url(fp, lines))
        file_findings.extend(check_ss005_session_fixation(fp, lines))
        file_findings.extend(check_ss006_missing_csrf(fp, lines, content))
        file_findings.extend(check_ss007_localstorage_auth(fp, lines))
        file_findings.extend(check_ss008_no_session_timeout(fp, lines))
        file_findings.extend(check_ss009_weak_session_id(fp, lines))
        file_findings.extend(check_ss010_broad_cookie_domain(fp, lines))

        if file_findings:
            result.files_flagged += 1
        result.findings.extend(file_findings)

    return result


def format_report(result: AuditResult, ci_mode: bool = False) -> str:
    out = []
    out.append(f"\n{'='*60}")
    out.append(f"  Session Audit — {result.scan_root}")
    out.append(f"  Files scanned: {result.files_scanned}  |  Files flagged: {result.files_flagged}")
    out.append(f"{'='*60}")

    if not result.findings:
        out.append("✅ No session management vulnerabilities detected.")
        return "\n".join(out)

    for severity in ("CRITICAL", "HIGH", "MEDIUM"):
        sev = [f for f in result.findings if f.severity == severity]
        if sev:
            out.append(f"\n── {severity} ({len(sev)}) {'─'*40}")
            for finding in sev:
                out.append(str(finding))

    out.append(f"\n{'─'*60}")
    out.append(
        f"  Total: {len(result.findings)} findings  |  "
        f"Critical: {result.critical_count}  High: {result.high_count}  Medium: {result.medium_count}"
    )
    if ci_mode and (result.critical_count > 0 or result.high_count > 0):
        out.append("\n  ❌ CI GATE FAILED — resolve CRITICAL/HIGH findings before merging.")
    return "\n".join(out)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="phy-session-audit — Session & Cookie Security Auditor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python session_audit.py ./src
  python session_audit.py src/middleware/session.js
  python session_audit.py ./src --ci
  python session_audit.py ./src --only-severity CRITICAL
        """,
    )
    parser.add_argument("path", help="Directory or file to audit")
    parser.add_argument("--ci", action="store_true", help="Exit 1 on CRITICAL or HIGH findings")
    parser.add_argument(
        "--only-severity",
        choices=["CRITICAL", "HIGH", "MEDIUM"],
        help="Filter to this severity and above",
    )
    args = parser.parse_args()

    result = audit(args.path)

    sev_order = ["CRITICAL", "HIGH", "MEDIUM"]
    if args.only_severity:
        cutoff = sev_order.index(args.only_severity)
        result.findings = [f for f in result.findings if sev_order.index(f.severity) <= cutoff]

    print(format_report(result, ci_mode=args.ci))

    if args.ci and (result.critical_count > 0 or result.high_count > 0):
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## CI Integration

```yaml
# GitHub Actions
- name: Session Security Audit
  run: python session_audit.py ./src --ci

# Only CRITICAL findings block the build
- name: Session Audit (critical only)
  run: python session_audit.py ./src --only-severity CRITICAL --ci
```

## False Positive Notes

- **SS001/SS002/SS003** — Only fire when a session/auth/token/jwt-related cookie is found without the flag. Pure analytics cookies won't trigger.
- **SS005** — Requires both a login-success signal AND a response nearby (25-line window). Utility functions that just check passwords won't fire.
- **SS006** — Skips if ANY CSRF guard pattern is found anywhere in the file. Also skips routes matching `webhook`, `health`, `/api/`, `/grpc` (typically stateless API routes using Bearer tokens instead of cookies). Caps at 3 findings (same global fix applies to all).
- **SS009** — `uuid.uuid4()` is flagged as MEDIUM when used as session ID — UUID4 uses OS entropy (`os.urandom`) and is fine, but using `.hex` and assigning it as a session ID without wrapping in `secrets` is technically weaker than `secrets.token_urlsafe()`. Suppress if your framework handles session ID generation internally.

## OWASP Coverage Map

| Check | OWASP A07:2021 Sub-Category |
|-------|-----------------------------|
| SS001 | Session token exposure via XSS |
| SS002 | Token transmission over cleartext |
| SS003 | CSRF protection gap |
| SS004 | Token exposure via URL |
| SS005 | Session fixation |
| SS006 | CSRF forgery |
| SS007 | Insecure client-side storage |
| SS008 | Infinite session lifetime |
| SS009 | Predictable session tokens |
| SS010 | Overly permissive cookie scope |

## Related Skills

- **phy-crypto-audit** — weak JWT signing, PRNG for tokens (complements SS009)
- **phy-jwt-auth-audit** — deep JWT token inspection, alg:none, scope audit
- **phy-cors-audit** — CORS misconfiguration that bypasses SameSite protection
- **phy-rate-limit-audit** — brute force protection for auth endpoints

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
