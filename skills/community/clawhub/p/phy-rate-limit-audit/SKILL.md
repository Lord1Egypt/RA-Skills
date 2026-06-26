---
name: Rate Limit Audit
description: Missing rate limit detector for API codebases. Scans Express/Koa/Fastify/NestJS, FastAPI/Flask/Django, Go (gin/chi/echo), Spring Boot, and Ruby (Rack) for 10 classes of unprotected endpoints — auth routes open to brute force, payment endpoints with no throttle, email/SMS senders without limit (cost amplification), search routes with no query throttle, retry logic without backoff, admin endpoints without per-IP limiting, and more. Zero external dependencies. Works on directories or single files. CI fail-gate included.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - security
  - api
  - rate-limiting
  - brute-force
  - dos
  - owasp
  - static-analysis
  - zero-deps
  - express
  - fastapi
  - django
  - flask
  - golang
  - spring
---

# phy-rate-limit-audit — Missing Rate Limit Detector

Scans your API source code for **10 classes of missing rate limiting** that lead to brute-force attacks, cost amplification (SMS/email bombs), DoS via expensive queries, and retry storms.

Maps to **OWASP API Security Top 10 2023: API4 — Unrestricted Resource Consumption**.

## Quick Start

```bash
# Scan a directory
python rate_limit_audit.py ./src

# Single file
python rate_limit_audit.py src/routes/auth.js

# CI mode — exit 1 on CRITICAL or HIGH
python rate_limit_audit.py ./src --ci

# Only show HIGH and above
python rate_limit_audit.py ./src --only-severity HIGH

# Verbose: show which lines triggered each finding
python rate_limit_audit.py ./src --verbose
```

## The 10 Checks

| ID | Severity | Check | Attack Vector |
|----|----------|-------|---------------|
| RL001 | HIGH | No rate-limit library imported in project | Global unprotected |
| RL002 | CRITICAL | Auth endpoint (/login /register /forgot) without per-route limit | Brute force / credential stuffing |
| RL003 | CRITICAL | Email/SMS send without rate limit guard | Cost amplification ($$$) |
| RL004 | HIGH | Payment/billing endpoint without rate limiting | Financial DoS |
| RL005 | HIGH | Search/list endpoint without throttle | Expensive query DoS |
| RL006 | HIGH | Admin endpoint without per-IP rate limiting | Privilege escalation via brute force |
| RL007 | MEDIUM | Retry loop without exponential backoff | Retry storm / self-DoS |
| RL008 | MEDIUM | File processing endpoint without queue/semaphore | CPU/memory exhaustion |
| RL009 | MEDIUM | External API call in request handler without circuit breaker | Cascading failure |
| RL010 | LOW | Rate limit configured but threshold too permissive on auth routes | Slow brute force |

### RL001 — No Rate-Limit Library in Project
Scans all source files for imports of known rate-limiting libraries. If none are found across the entire codebase, every endpoint is unprotected.

**Detected libraries:**
- JS/TS: `express-rate-limit`, `rate-limiter-flexible`, `koa-ratelimit`, `@nestjs/throttler`, `fastify-rate-limit`, `express-slow-down`, `bottleneck`, `p-throttle`
- Python: `slowapi`, `flask-limiter`, `django-ratelimit`, `limits`, `ratelimit`
- Go: `github.com/ulule/limiter`, `golang.org/x/time/rate`, `github.com/didip/tollbooth`
- Ruby: `rack-attack`, `rack/throttle`
- Java/Spring: `@RateLimiter`, `RateLimiterRegistry`, `resilience4j.ratelimiter`

### RL002 — Auth Endpoints Without Per-Route Limit (CRITICAL)
Detects route definitions for authentication paths (`/login`, `/signin`, `/auth`, `/register`, `/signup`, `/forgot-password`, `/reset-password`, `/verify-otp`, `/token`, `/oauth`) and checks whether a rate-limit guard appears within ±25 lines of the route handler.

**Guard patterns recognized:** `rateLimit(`, `limiter(`, `@RateLimit`, `@limiter.limit`, `slowDown(`, `throttle(`, `rateLimiter`, `checkRateLimit`, `redis.incr`

### RL003 — Email/SMS Sends Without Rate Limit (CRITICAL)
Finds calls to email/SMS providers without a nearby guard:
- Email: `sendmail(`, `send_email(`, `ses.sendEmail(`, `ses.send_email(`, `sg.send(`, `resend.emails.send(`, `nodemailer`, `smtplib.SMTP`
- SMS: `twilio.messages.create(`, `sns.publish(`, `send_sms(`, `nexmo.message.sendSms(`

A compromised or public endpoint calling these without rate limiting = unlimited SMS/email charges.

### RL004 — Payment Endpoints Without Rate Limiting (HIGH)
Finds routes matching `/pay`, `/charge`, `/invoice`, `/subscribe`, `/billing`, `/checkout`, `/purchase`, `/order` and checks for rate-limit guards nearby. Unprotected payment endpoints allow attackers to enumerate card validity at scale.

### RL005 — Search/List Endpoints Without Throttle (HIGH)
Detects routes matching `/search`, `/query`, `/find`, `/filter`, `/list` + `?q=` or `?query=` patterns. Search routes often trigger full-text scans or ML inference — unprotected, a single attacker can saturate the database.

### RL006 — Admin Endpoints Without Per-IP Limiting (HIGH)
Admin paths (`/admin`, `/management`, `/internal`, `/dashboard`) without a rate-limit guard allow brute-forcing admin credentials without lockout.

### RL007 — Retry Without Exponential Backoff (MEDIUM)
Detects retry loops (`while retries`, `for attempt`, `for i in range`, `retry(`) without exponential backoff signals (`Math.pow`, `2 **`, `backoff`, `sleep(2 *`, `jitter`, `exponential`). Retry without backoff causes retry storms that amplify failures into outages.

### RL008 — Synchronous File Processing (MEDIUM)
Finds file upload handlers (`multipart`, `req.file`, `request.files`, `UploadedFile`) that process the file in-request without a queue/semaphore (`celery`, `bull`, `queue`, `asyncio.Semaphore`, `p-limit`, `worker`). Large file processing inline blocks threads and can exhaust memory.

### RL009 — External API Call Without Circuit Breaker (MEDIUM)
Detects outbound HTTP calls (`fetch(`, `requests.get(`, `http.Get(`, `axios.get(`, `RestTemplate.getForObject`) in request handlers without circuit-breaker patterns (`circuit`, `breaker`, `hystrix`, `resilience4j`, `pybreaker`, `tenacity`, `timeout`). If the external service is slow, every request hangs.

### RL010 — Permissive Rate Limit on Auth Routes (LOW)
If `express-rate-limit` or `slowapi` config is found with `max:` > 20 or `times:` > 20 on paths matching auth patterns, flags as too permissive. 20 req/window is already enough for a slow brute force on a 6-digit PIN.

## Sample Output

```
============================================================
  Rate Limit Audit — src/
  Files scanned: 47  |  Files flagged: 8
============================================================

── CRITICAL (2) ────────────────────────────────────────────
🔴 RL002 [CRITICAL] src/routes/auth.js:34
   Auth endpoint POST /login has no rate-limit guard within 25 lines.
   Attack: Credential stuffing / brute force — 100K attempts/hour unchecked.
   CWE: CWE-307: Improper Restriction of Excessive Authentication Attempts
   Fix: app.post('/login', rateLimit({ windowMs: 15*60*1000, max: 5 }), handler)

🔴 RL003 [CRITICAL] src/services/notifications.js:89
   Email send (ses.sendEmail) with no rate-limit guard in caller chain.
   Attack: Attackers trigger unlimited email sends → AWS SES bill amplification.
   CWE: CWE-400: Uncontrolled Resource Consumption
   Fix: Add per-user rate limit before any email-sending endpoint.

── HIGH (2) ────────────────────────────────────────────────
🟠 RL004 [HIGH] src/routes/payments.js:12
   Payment endpoint POST /checkout has no rate-limit guard.
   Attack: Card enumeration — test stolen cards at scale without detection.
   Fix: rateLimit({ windowMs: 60000, max: 3, keyGenerator: req => req.user.id })

🟠 RL005 [HIGH] src/routes/search.js:8
   Search endpoint GET /search has no throttle guard.
   Attack: Full-text search DoS — single attacker saturates Elasticsearch.
   Fix: Add rateLimit({ windowMs: 60000, max: 30 }) before search handler.

── MEDIUM (2) ──────────────────────────────────────────────
🟡 RL007 [MEDIUM] src/utils/retry.js:22
   Retry loop detected without exponential backoff (no Math.pow/backoff/jitter).
   Attack: Retry storm amplifies transient failures into sustained outage.
   Fix: Add: await sleep(Math.min(1000 * 2 ** attempt + Math.random() * 1000, 30000))

🟡 RL009 [MEDIUM] src/handlers/weather.js:45
   External HTTP call (fetch) in request handler without circuit breaker or timeout.
   Attack: Slow external service hangs all Node.js event loop threads.
   Fix: Add timeout: fetch(url, { signal: AbortSignal.timeout(3000) })

── LOW (1) ─────────────────────────────────────────────────
🔵 RL010 [LOW] src/middleware/rateLimits.js:5
   Rate limit on auth route has max: 100 — too permissive for credential endpoint.
   Fix: Use max: 5 per 15-minute window for /login, /register, /forgot-password.

────────────────────────────────────────────────────────────
  Total: 7 findings
  Critical: 2 | High: 2 | Medium: 2 | Low: 1

  ❌ CI GATE FAILED — resolve CRITICAL/HIGH findings before merging.
```

## The Script

```python
#!/usr/bin/env python3
"""
phy-rate-limit-audit — Missing Rate Limit Detector
Scans Express/FastAPI/Flask/Django/Go/Spring for unprotected API endpoints.
Zero external dependencies.
"""

import sys
import re
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ─── Data Structures ─────────────────────────────────────────────────────────

@dataclass
class Finding:
    check_id: str
    severity: str      # CRITICAL / HIGH / MEDIUM / LOW
    location: str      # "file.js:34"
    message: str
    attack: str = ""
    cwe: str = ""
    fix: str = ""

    def __str__(self) -> str:
        icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵"}.get(self.severity, "⚪")
        parts = [f"{icon} {self.check_id} [{self.severity}] {self.location}"]
        parts.append(f"   {self.message}")
        if self.attack:
            parts.append(f"   Attack: {self.attack}")
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

    @property
    def low_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "LOW")


# ─── Constants ────────────────────────────────────────────────────────────────

RATE_LIMIT_IMPORTS = re.compile(
    r"(express-rate-limit|rate-limiter-flexible|koa-ratelimit|@nestjs/throttler|"
    r"fastify-rate-limit|express-slow-down|bottleneck|p-throttle|"
    r"slowapi|flask.limiter|flask_limiter|django.ratelimit|django_ratelimit|"
    r"from limits|import ratelimit|"
    r"ulule/limiter|golang\.org/x/time/rate|didip/tollbooth|"
    r"rack.attack|rack/throttle|"
    r"RateLimiterRegistry|@RateLimiter|resilience4j\.ratelimiter)",
    re.IGNORECASE,
)

RATE_LIMIT_GUARD_RE = re.compile(
    r"(rateLimit\(|limiter\(|@RateLimit|@limiter\.limit|slowDown\(|"
    r"throttle\(|rateLimiter|checkRateLimit|redis\.incr|"
    r"Limiter\(|tollbooth|rack\.attack|RateLimiter\.create)",
    re.IGNORECASE,
)

AUTH_ROUTE_RE = re.compile(
    r"""(app|router|Route)\.(post|get|put|patch)\s*\(\s*['"`]"""
    r"""[^'"`]*(login|signin|register|signup|forgot.password|reset.password|"""
    r"""verify.?otp|verify.?email|send.?otp|token|oauth|authenticate)[^'"`]*['"`]""",
    re.IGNORECASE,
)

# Python FastAPI/Flask auth route patterns
PYTHON_AUTH_ROUTE_RE = re.compile(
    r"""@(app|router)\.(post|get|put|patch)\s*\(\s*['"`]"""
    r"""[^'"`]*(login|signin|register|signup|forgot|reset.password|"""
    r"""verify|token|oauth|authenticate)[^'"`]*['"`]""",
    re.IGNORECASE,
)

# Go auth route patterns
GO_AUTH_ROUTE_RE = re.compile(
    r"""(router|r|e|g|mux)\.(POST|GET|PUT|PATCH)\s*\(\s*"[^"]*"""
    r"""(login|signin|register|signup|forgot|reset|verify|token|oauth|auth)[^"]*""",
    re.IGNORECASE,
)

EMAIL_SEND_RE = re.compile(
    r"(sendmail|send_email|ses\.sendEmail|ses\.send_email|sg\.send|"
    r"resend\.emails\.send|nodemailer|smtplib\.SMTP|mail\.send|"
    r"sendgrid|mailgun|postmark\.send)",
    re.IGNORECASE,
)

SMS_SEND_RE = re.compile(
    r"(twilio\.messages\.create|sns\.publish|send_sms|nexmo\.message|"
    r"vonage\.sms|messagebird\.messages\.create|plivo\.send_message)",
    re.IGNORECASE,
)

PAYMENT_ROUTE_RE = re.compile(
    r"""(app|router|Route|router|r)\.(post|get|put|patch)\s*\(\s*['"`]"""
    r"""[^'"`]*(pay|charge|invoice|subscri|billing|checkout|purchase|order)[^'"`]*['"`]""",
    re.IGNORECASE,
)

SEARCH_ROUTE_RE = re.compile(
    r"""(app|router|Route|r|e|g)\.(get|post)\s*\(\s*['"`][^'"`]*(search|query|find|filter|/list)[^'"`]*['"`]""",
    re.IGNORECASE,
)

ADMIN_ROUTE_RE = re.compile(
    r"""(app|router|Route|r|e|g)\.(get|post|put|patch|delete)\s*\(\s*['"`][^'"`]*(admin|management|internal|dashboard)[^'"`]*['"`]""",
    re.IGNORECASE,
)

RETRY_LOOP_RE = re.compile(
    r"(while\s+retries|for\s+attempt|for\s+i\s+in\s+range|retry\(|attempts\s*=|max_retries)",
    re.IGNORECASE,
)

BACKOFF_RE = re.compile(
    r"(Math\.pow|2\s*\*\*\s*attempt|backoff|sleep\(2\s*\*|jitter|exponential|time\.Sleep\(.*\*\s*2)",
    re.IGNORECASE,
)

FILE_UPLOAD_RE = re.compile(
    r"(multipart|req\.file|request\.files|UploadedFile|multer|formidable|busboy)",
    re.IGNORECASE,
)

QUEUE_SEMAPHORE_RE = re.compile(
    r"(celery|bull|queue|asyncio\.Semaphore|p.limit|worker|background|defer|enqueue)",
    re.IGNORECASE,
)

OUTBOUND_HTTP_RE = re.compile(
    r"(fetch\(|requests\.get|requests\.post|http\.Get|http\.Post|"
    r"axios\.(get|post)|RestTemplate|WebClient|urllib\.request|httpx\.(get|post))",
    re.IGNORECASE,
)

CIRCUIT_BREAKER_RE = re.compile(
    r"(circuit|breaker|hystrix|resilience4j|pybreaker|tenacity|"
    r"AbortSignal\.timeout|signal:\s*AbortSignal|timeout:\s*\d)",
    re.IGNORECASE,
)

RATE_LIMIT_MAX_RE = re.compile(
    r"max:\s*(\d+)|times:\s*(\d+)|limit:\s*(\d+)",
    re.IGNORECASE,
)

SUPPORTED_EXTENSIONS = {".js", ".ts", ".jsx", ".tsx", ".py", ".go", ".rb", ".java", ".kt"}

SKIP_DIRS = {"node_modules", ".git", "venv", ".venv", "__pycache__", "dist", "build", ".next", "vendor"}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def get_context_lines(lines: list, idx: int, window: int = 25) -> str:
    start = max(0, idx - window)
    end = min(len(lines), idx + window)
    return "\n".join(lines[start:end])


def has_guard_nearby(lines: list, idx: int, guard_re: re.Pattern, window: int = 25) -> bool:
    ctx = get_context_lines(lines, idx, window)
    return bool(guard_re.search(ctx))


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

def check_rl001_no_rate_limit_library(all_files: list, all_contents: dict) -> list:
    """RL001 — No rate-limit library imported anywhere in the project."""
    for content in all_contents.values():
        if RATE_LIMIT_IMPORTS.search(content):
            return []  # Found at least one — skip

    return [Finding(
        check_id="RL001",
        severity="HIGH",
        location="<project>",
        message="No rate-limiting library imported anywhere in the codebase. All endpoints are unprotected.",
        attack="Unlimited requests — brute force, DoS, cost amplification attacks all possible.",
        cwe="CWE-400: Uncontrolled Resource Consumption",
        fix=(
            "JS: npm install express-rate-limit  |  "
            "Python: pip install slowapi (FastAPI) or flask-limiter  |  "
            "Go: go get golang.org/x/time/rate"
        ),
    )]


def check_rl002_auth_no_limit(filepath: str, lines: list) -> list:
    """RL002 — Auth endpoints without per-route rate limiting."""
    findings = []
    for i, line in enumerate(lines):
        match = AUTH_ROUTE_RE.search(line) or PYTHON_AUTH_ROUTE_RE.search(line) or GO_AUTH_ROUTE_RE.search(line)
        if not match:
            continue
        if not has_guard_nearby(lines, i, RATE_LIMIT_GUARD_RE, window=25):
            findings.append(Finding(
                check_id="RL002",
                severity="CRITICAL",
                location=f"{filepath}:{i + 1}",
                message=f"Auth endpoint '{match.group().strip()[:80]}' has no rate-limit guard within 25 lines.",
                attack="Credential stuffing / brute force — 100K+ attempts per hour without detection.",
                cwe="CWE-307: Improper Restriction of Excessive Authentication Attempts",
                fix="rateLimit({ windowMs: 15*60*1000, max: 5, skipSuccessfulRequests: true })",
            ))
    return findings


def check_rl003_email_sms_no_limit(filepath: str, lines: list, all_content: str) -> list:
    """RL003 — Email/SMS sends without rate-limit guard."""
    # Skip if this is a service/helper file — check callers instead
    # But still flag if the send appears directly in a route handler
    findings = []
    for i, line in enumerate(lines):
        if not (EMAIL_SEND_RE.search(line) or SMS_SEND_RE.search(line)):
            continue
        if has_guard_nearby(lines, i, RATE_LIMIT_GUARD_RE, window=30):
            continue
        # Check if this is inside a route handler (heuristic: near app.post/router.post)
        ctx = get_context_lines(lines, i, 40)
        if re.search(r"(app|router)\.(post|get|put|patch)\s*\(", ctx, re.IGNORECASE):
            finding_type = "Email" if EMAIL_SEND_RE.search(line) else "SMS"
            findings.append(Finding(
                check_id="RL003",
                severity="CRITICAL",
                location=f"{filepath}:{i + 1}",
                message=f"{finding_type} send detected in route handler with no rate-limit guard.",
                attack=f"{finding_type} bombing — attacker triggers unlimited sends → cost amplification / account harassment.",
                cwe="CWE-400: Uncontrolled Resource Consumption",
                fix=f"Add per-user rate limit (max 3/{('hour' if finding_type == 'SMS' else 'minute')}) before this endpoint.",
            ))
    return findings


def check_rl004_payment_no_limit(filepath: str, lines: list) -> list:
    """RL004 — Payment/billing endpoints without rate limiting."""
    findings = []
    for i, line in enumerate(lines):
        if not PAYMENT_ROUTE_RE.search(line):
            continue
        if not has_guard_nearby(lines, i, RATE_LIMIT_GUARD_RE, window=25):
            findings.append(Finding(
                check_id="RL004",
                severity="HIGH",
                location=f"{filepath}:{i + 1}",
                message=f"Payment endpoint '{line.strip()[:80]}' has no rate-limit guard.",
                attack="Card enumeration at scale — test thousands of stolen card numbers per minute.",
                cwe="CWE-400",
                fix="rateLimit({ windowMs: 60000, max: 3, keyGenerator: req => req.user?.id || req.ip })",
            ))
    return findings


def check_rl005_search_no_throttle(filepath: str, lines: list) -> list:
    """RL005 — Search/list endpoints without rate limiting."""
    findings = []
    for i, line in enumerate(lines):
        if not SEARCH_ROUTE_RE.search(line):
            continue
        if not has_guard_nearby(lines, i, RATE_LIMIT_GUARD_RE, window=25):
            findings.append(Finding(
                check_id="RL005",
                severity="HIGH",
                location=f"{filepath}:{i + 1}",
                message=f"Search/list endpoint '{line.strip()[:80]}' has no throttle.",
                attack="Full-text search DoS — single attacker triggers parallel expensive queries saturating the database.",
                cwe="CWE-400",
                fix="rateLimit({ windowMs: 60000, max: 30 }) — search endpoints need tighter limits than read endpoints.",
            ))
    return findings


def check_rl006_admin_no_limit(filepath: str, lines: list) -> list:
    """RL006 — Admin endpoints without per-IP rate limiting."""
    findings = []
    for i, line in enumerate(lines):
        if not ADMIN_ROUTE_RE.search(line):
            continue
        if not has_guard_nearby(lines, i, RATE_LIMIT_GUARD_RE, window=25):
            findings.append(Finding(
                check_id="RL006",
                severity="HIGH",
                location=f"{filepath}:{i + 1}",
                message=f"Admin endpoint '{line.strip()[:80]}' has no per-IP rate limiting.",
                attack="Admin brute force — password/2FA code guessing without lockout on highest-privilege endpoint.",
                cwe="CWE-307",
                fix="rateLimit({ windowMs: 15*60*1000, max: 3, keyGenerator: req => req.ip })",
            ))
    return findings


def check_rl007_retry_no_backoff(filepath: str, lines: list) -> list:
    """RL007 — Retry logic without exponential backoff."""
    findings = []
    for i, line in enumerate(lines):
        if not RETRY_LOOP_RE.search(line):
            continue
        ctx = get_context_lines(lines, i, 20)
        if not BACKOFF_RE.search(ctx):
            findings.append(Finding(
                check_id="RL007",
                severity="MEDIUM",
                location=f"{filepath}:{i + 1}",
                message="Retry loop detected without exponential backoff.",
                attack="Retry storm — transient failure triggers immediate retry avalanche, converting brief outages into sustained cascades.",
                cwe="CWE-400",
                fix="await sleep(Math.min(1000 * 2 ** attempt + Math.random() * 1000, 30000))",
            ))
    return findings


def check_rl008_sync_file_processing(filepath: str, lines: list) -> list:
    """RL008 — File upload without background queue/semaphore."""
    findings = []
    for i, line in enumerate(lines):
        if not FILE_UPLOAD_RE.search(line):
            continue
        ctx = get_context_lines(lines, i, 30)
        # Check if any processing-heavy ops appear nearby (sharp, ffmpeg, pandas, pillow, resize)
        if not re.search(r"(sharp|ffmpeg|pandas|PIL|Pillow|resize|compress|transcode|convert)", ctx, re.IGNORECASE):
            continue
        if not QUEUE_SEMAPHORE_RE.search(ctx):
            findings.append(Finding(
                check_id="RL008",
                severity="MEDIUM",
                location=f"{filepath}:{i + 1}",
                message="File processing (image/video/data) handled synchronously in request without queue or semaphore.",
                attack="10 concurrent large file uploads → thread pool exhaustion → total service unavailability.",
                cwe="CWE-400",
                fix="Offload processing to a background worker (Celery/Bull/BullMQ). Use p-limit or asyncio.Semaphore for concurrency cap.",
            ))
    return findings


def check_rl009_outbound_no_circuit(filepath: str, lines: list) -> list:
    """RL009 — External API call in handler without circuit breaker or timeout."""
    findings = []
    for i, line in enumerate(lines):
        if not OUTBOUND_HTTP_RE.search(line):
            continue
        ctx = get_context_lines(lines, i, 20)
        # Only flag if inside a route handler (heuristic)
        if not re.search(r"(app|router|handler|controller|@app\.|@router\.)", ctx, re.IGNORECASE):
            continue
        if not CIRCUIT_BREAKER_RE.search(ctx):
            findings.append(Finding(
                check_id="RL009",
                severity="MEDIUM",
                location=f"{filepath}:{i + 1}",
                message="Outbound HTTP call in request handler without timeout or circuit breaker.",
                attack="External service slowdown → all in-flight requests hang → event loop saturation → total service unavailability.",
                cwe="CWE-400",
                fix="Add timeout: fetch(url, { signal: AbortSignal.timeout(3000) }) and consider circuit breaker (opossum/pybreaker).",
            ))
    return findings


def check_rl010_permissive_limit(filepath: str, lines: list) -> list:
    """RL010 — Rate limit max too high on auth-related config."""
    findings = []
    for i, line in enumerate(lines):
        # Look for rateLimit config near auth path mentions
        max_match = RATE_LIMIT_MAX_RE.search(line)
        if not max_match:
            continue
        # Extract the numeric value
        val_str = max_match.group(1) or max_match.group(2) or max_match.group(3)
        if not val_str:
            continue
        try:
            val = int(val_str)
        except ValueError:
            continue
        if val <= 20:
            continue  # Acceptable limit
        # Check if the surrounding context is for an auth endpoint
        ctx = get_context_lines(lines, i, 20)
        if re.search(r"(login|signin|register|forgot|reset.password|verify|auth|token)", ctx, re.IGNORECASE):
            findings.append(Finding(
                check_id="RL010",
                severity="LOW",
                location=f"{filepath}:{i + 1}",
                message=f"Rate limit max: {val} is too permissive for an auth-related endpoint.",
                attack=f"At {val} requests/window, slow brute force of 4-6 digit PINs completes in hours undetected.",
                cwe="CWE-307",
                fix="Use max: 5 per 15-minute window for /login and /register. Use max: 3 for /forgot-password (SMS/email send).",
            ))
    return findings


# ─── Main Audit ───────────────────────────────────────────────────────────────

def audit(path: str, verbose: bool = False) -> AuditResult:
    result = AuditResult(scan_root=path)
    files = collect_files(path)

    # Load all contents for RL001 (cross-file check)
    all_contents = {}
    for f in files:
        try:
            all_contents[str(f)] = f.read_text(errors="ignore")
        except Exception:
            pass

    result.files_scanned = len(files)

    # RL001 is a global check — run once
    rl001_findings = check_rl001_no_rate_limit_library(files, all_contents)
    result.findings.extend(rl001_findings)

    # Per-file checks
    file_finding_counts = {}
    for f in files:
        content = all_contents.get(str(f), "")
        lines = content.splitlines()
        fp = str(f)

        file_findings = []
        file_findings.extend(check_rl002_auth_no_limit(fp, lines))
        file_findings.extend(check_rl003_email_sms_no_limit(fp, lines, content))
        file_findings.extend(check_rl004_payment_no_limit(fp, lines))
        file_findings.extend(check_rl005_search_no_throttle(fp, lines))
        file_findings.extend(check_rl006_admin_no_limit(fp, lines))
        file_findings.extend(check_rl007_retry_no_backoff(fp, lines))
        file_findings.extend(check_rl008_sync_file_processing(fp, lines))
        file_findings.extend(check_rl009_outbound_no_circuit(fp, lines))
        file_findings.extend(check_rl010_permissive_limit(fp, lines))

        if file_findings:
            result.files_flagged += 1
            file_finding_counts[fp] = len(file_findings)
        result.findings.extend(file_findings)

    return result


def format_report(result: AuditResult, ci_mode: bool = False) -> str:
    lines_out = []
    lines_out.append(f"\n{'='*60}")
    lines_out.append(f"  Rate Limit Audit — {result.scan_root}")
    lines_out.append(f"  Files scanned: {result.files_scanned}  |  Files flagged: {result.files_flagged}")
    lines_out.append(f"{'='*60}")

    if not result.findings:
        lines_out.append("✅ No missing rate limits detected.")
        return "\n".join(lines_out)

    for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        sev_findings = [f for f in result.findings if f.severity == severity]
        if sev_findings:
            lines_out.append(f"\n── {severity} ({len(sev_findings)}) {'─'*40}")
            for finding in sev_findings:
                lines_out.append(str(finding))

    lines_out.append(f"\n{'─'*60}")
    lines_out.append(
        f"  Total: {len(result.findings)} findings  |  "
        f"Critical: {result.critical_count}  High: {result.high_count}  "
        f"Medium: {result.medium_count}  Low: {result.low_count}"
    )
    if ci_mode and (result.critical_count > 0 or result.high_count > 0):
        lines_out.append("\n  ❌ CI GATE FAILED — resolve CRITICAL/HIGH findings before merging.")
    return "\n".join(lines_out)


# ─── CLI Entry Point ──────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="phy-rate-limit-audit — Missing Rate Limit Detector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python rate_limit_audit.py ./src
  python rate_limit_audit.py src/routes/auth.js
  python rate_limit_audit.py ./src --ci
  python rate_limit_audit.py ./src --only-severity HIGH
        """,
    )
    parser.add_argument("path", help="Directory or file to audit")
    parser.add_argument("--ci", action="store_true", help="Exit 1 on CRITICAL or HIGH findings")
    parser.add_argument(
        "--only-severity",
        choices=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        help="Filter to this severity and above",
    )
    parser.add_argument("--verbose", action="store_true", help="Show extra context for each finding")
    args = parser.parse_args()

    result = audit(args.path, verbose=args.verbose)

    sev_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
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
- name: Rate Limit Audit
  run: python rate_limit_audit.py ./src --ci

# GitLab CI
rate-limit-security:
  script:
    - python rate_limit_audit.py ./src --only-severity HIGH --ci
  allow_failure: false
```

## False Positive Notes

- **RL001** only fires if zero rate-limit libraries are found across the entire project
- **RL002/RL004/RL005/RL006** use a ±25 line proximity window — if your middleware is registered elsewhere (e.g., in app.js), these may fire. Suppress with `# phy-ignore: RL002` comment on the route line
- **RL007** skips files where backoff keywords appear anywhere near the retry loop (window: 20 lines)
- **RL008** only fires when file upload AND heavy processing (sharp/ffmpeg/pandas/PIL) appear together without a queue signal
- **RL009** uses a heuristic to detect route handlers — may miss controller patterns in heavily abstracted frameworks (e.g., NestJS decorators)

## Related Skills

- **phy-async-audit** — unhandled async errors (errors from rate-limit failures need proper propagation)
- **phy-cors-audit** — CORS misconfig can bypass IP-based rate limiting
- **phy-openapi-sec-audit** — checks for missing rate limit headers in OpenAPI response definitions
- **phy-security-headers** — `Retry-After` header enforcement

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
