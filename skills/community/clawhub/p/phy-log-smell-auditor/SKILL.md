---
name: Log Smell Auditor
description: Application logging quality auditor. Scans source files for logging anti-patterns — debug/print statements left in production paths, log level mismatches (errors logged as info, warnings swallowed), PII exposure risk (email, token, password appearing in log strings), missing structured context fields (no request_id/trace_id in web handler log calls), and noisy debug flooding in tight loops. Supports JavaScript/TypeScript (console.log, winston, pino), Python (logging, structlog, print), Go (log, zap, logrus), Java (SLF4J, Log4j), and Ruby (Rails logger). Reports by severity with file and line citations. Generates a one-command fix for the most common issues. Zero external API — pure static file analysis. Triggers on "logging audit", "bad logs", "debug left in code", "PII in logs", "log level wrong", "missing trace id", "/log-audit".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - logging
    - observability
    - security
    - developer-tools
    - static-analysis
    - javascript
    - python
    - go
    - pii
    - structured-logging
---

# Log Smell Auditor

You wake up at 3am. The alert fired. You open the logs.

`DEBUG processing request`
`console.log("here")`
`INFO user password: hunter2`

No trace ID. No request context. Just noise and a PII leak.

This skill scans your codebase before that moment happens — finds the print statements, the wrong log levels, the PII exposures, and the missing structured context fields.

**Supports JS/TS, Python, Go, Java, Ruby. Zero external API.**

---

## Trigger Phrases

- "logging audit", "bad logs", "logging quality"
- "debug left in code", "console.log in production"
- "PII in logs", "password in logs", "sensitive data logged"
- "log level wrong", "error logged as info"
- "missing trace id", "missing request id"
- "structured logging check", "log noise"
- "/log-audit"

---

## How to Provide Input

```bash
# Option 1: Audit entire project
/log-audit

# Option 2: Specific directory
/log-audit src/
/log-audit app/

# Option 3: Focus on a specific smell
/log-audit --check debug-leaks      # print/console.log in prod paths
/log-audit --check pii              # sensitive data in log strings
/log-audit --check levels           # wrong log levels
/log-audit --check structure        # missing trace/request IDs

# Option 4: Generate fix script
/log-audit --fix-debug-leaks        # outputs sed commands to remove debug prints

# Option 5: CI mode (exit 1 if issues found above threshold)
/log-audit --ci --max-errors 0 --max-warnings 10
```

---

## Step 1: Detect Logging Framework

```bash
python3 -c "
import os, json
from pathlib import Path

frameworks = {}

# Node.js
if os.path.exists('package.json'):
    pkg = json.loads(Path('package.json').read_text())
    deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
    for lib in ['winston', 'pino', 'bunyan', 'morgan', 'loglevel', 'debug', 'log4js']:
        if lib in deps:
            frameworks.setdefault('javascript', []).append(lib)

# Python
for f in ['requirements.txt', 'Pipfile', 'pyproject.toml']:
    if os.path.exists(f):
        content = Path(f).read_text()
        for lib in ['structlog', 'loguru', 'python-json-logger']:
            if lib in content:
                frameworks.setdefault('python', []).append(lib)

# Go
if os.path.exists('go.mod'):
    content = Path('go.mod').read_text()
    for lib in ['zap', 'logrus', 'zerolog', 'slog']:
        if lib in content:
            frameworks.setdefault('go', []).append(lib)

if frameworks:
    for lang, libs in frameworks.items():
        print(f'{lang}: {libs}')
else:
    print('No logging framework detected — scanning for stdlib logging patterns')
"
```

---

## Step 2: Detect Debug/Print Leaks

```python
import re
import glob
from pathlib import Path

# Language-specific debug print patterns
DEBUG_LEAK_PATTERNS = {
    'js_ts': [
        (re.compile(r'^\s*console\.(log|debug|warn|error|info|trace)\s*\('), 'console.log — should use structured logger'),
        (re.compile(r'^\s*debugger\s*;?$'), 'debugger statement — remove before production'),
    ],
    'python': [
        (re.compile(r'^\s*print\s*\('), 'print() — should use logging module'),
        (re.compile(r'^\s*import\s+pdb\b|^\s*pdb\.set_trace\(\)'), 'pdb debugger — remove before production'),
        (re.compile(r'^\s*breakpoint\(\)'), 'breakpoint() — remove before production'),
    ],
    'go': [
        (re.compile(r'^\s*fmt\.Print(ln|f)?\s*\('), 'fmt.Print — use structured logger (zap/slog) instead'),
        (re.compile(r'^\s*log\.Print(ln|f)?\s*\('), 'stdlib log.Print — consider structured logger'),
    ],
    'java': [
        (re.compile(r'^\s*System\.out\.print'), 'System.out.print — use SLF4J logger'),
        (re.compile(r'^\s*e\.printStackTrace\(\)'), 'printStackTrace() — log with logger.error instead'),
    ],
    'ruby': [
        (re.compile(r'^\s*puts\s+'), 'puts — use Rails logger instead'),
        (re.compile(r'^\s*pp\s+'), 'pp — remove debug output'),
        (re.compile(r'^\s*binding\.pry'), 'binding.pry — remove before production'),
    ],
}

EXT_TO_LANG = {
    '.js': 'js_ts', '.jsx': 'js_ts', '.ts': 'js_ts', '.tsx': 'js_ts', '.mjs': 'js_ts',
    '.py': 'python',
    '.go': 'go',
    '.java': 'java',
    '.rb': 'ruby',
}

SKIP_DIRS = {'node_modules', '.git', 'dist', 'build', '__pycache__', '.next', 'vendor', 'venv', '.venv'}


def find_debug_leaks(src_dir='.'):
    findings = []
    for ext, lang in EXT_TO_LANG.items():
        for fpath in glob.glob(f'{src_dir}/**/*{ext}', recursive=True):
            if any(skip in fpath for skip in SKIP_DIRS):
                continue
            # Skip test files — print/console is acceptable in tests
            if any(t in fpath for t in ['test', 'spec', '__tests__']):
                continue
            try:
                lines = Path(fpath).read_text(errors='replace').splitlines()
            except Exception:
                continue
            for i, line in enumerate(lines, 1):
                for pattern, message in DEBUG_LEAK_PATTERNS[lang]:
                    if pattern.search(line):
                        findings.append({
                            'file': fpath,
                            'line': i,
                            'code': line.strip(),
                            'smell': 'DEBUG_LEAK',
                            'message': message,
                            'severity': 'MEDIUM',
                        })
    return findings
```

---

## Step 3: Detect PII Exposure

```python
# PII-sensitive field patterns in log strings
PII_PATTERNS = [
    (re.compile(r'(password|passwd|pwd|secret|token|api.?key|auth.?token)', re.I),
     'CRITICAL', 'Credential/secret in log string'),
    (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z]{2,}\b', re.I),
     'HIGH', 'Email address literal in log'),
    (re.compile(r'(credit.?card|card.?number|ccn|cvv|ssn|social.?security)', re.I),
     'CRITICAL', 'Financial/identity data in log string'),
    (re.compile(r'(phone|mobile|cell).*(=|:|\+)\s*[\d\s\-\(\)]{7,}', re.I),
     'HIGH', 'Phone number in log string'),
    (re.compile(r'(user.?id|userid|user_id)\s*[:=]\s*["\']?\d+', re.I),
     'LOW', 'User ID in log — consider pseudonymizing'),
    (re.compile(r'(ip.?addr|x.?forwarded|remote.?addr)\s*[:=]\s*["\']?\d{1,3}\.\d', re.I),
     'MEDIUM', 'IP address in log — GDPR sensitive'),
    (re.compile(r'Bearer\s+[A-Za-z0-9\-._~+/]+=*', re.I),
     'CRITICAL', 'Bearer token literal in log'),
]

LOG_CALL_PATTERN = re.compile(
    r'(console\.|logger\.|log\.|logging\.|fmt\.|System\.out\.|puts\s)',
    re.I
)

def find_pii_in_logs(src_dir='.'):
    findings = []
    for ext in EXT_TO_LANG:
        for fpath in glob.glob(f'{src_dir}/**/*{ext}', recursive=True):
            if any(skip in fpath for skip in SKIP_DIRS):
                continue
            try:
                lines = Path(fpath).read_text(errors='replace').splitlines()
            except Exception:
                continue
            for i, line in enumerate(lines, 1):
                # Only check lines that contain a log call
                if not LOG_CALL_PATTERN.search(line):
                    continue
                for pattern, severity, message in PII_PATTERNS:
                    if pattern.search(line):
                        findings.append({
                            'file': fpath,
                            'line': i,
                            'code': line.strip()[:100],
                            'smell': 'PII_EXPOSURE',
                            'message': message,
                            'severity': severity,
                        })
    return findings
```

---

## Step 4: Detect Missing Structured Context

```python
# Web handler patterns — these should always have structured context in logs
HANDLER_PATTERNS = [
    re.compile(r'(app\.(get|post|put|delete|patch)|router\.|@app\.route|@router\.|func.*Handler)', re.I),
    re.compile(r'(express|fastapi|flask|gin|echo|koa|fiber)\b', re.I),
    re.compile(r'def\s+(get|post|put|delete|patch|handle)\b', re.I),
]

# Structured context fields that should be present in handler logs
REQUIRED_CONTEXT_FIELDS = [
    ('request_id', re.compile(r'request.?id|req.?id|trace.?id|correlation.?id|x.?request.?id', re.I)),
    ('user_id', re.compile(r'user.?id|userid|actor.?id|subject', re.I)),
    ('method_path', re.compile(r'method|path|url|endpoint|route', re.I)),
]

def find_missing_structured_context(src_dir='.'):
    findings = []

    for ext in ['.ts', '.js', '.py', '.go']:
        for fpath in glob.glob(f'{src_dir}/**/*{ext}', recursive=True):
            if any(skip in fpath for skip in SKIP_DIRS):
                continue
            try:
                content = Path(fpath).read_text(errors='replace')
                lines = content.splitlines()
            except Exception:
                continue

            # Check if file contains web handlers
            if not any(p.search(content) for p in HANDLER_PATTERNS):
                continue

            # Find log calls in this file
            for i, line in enumerate(lines, 1):
                if not LOG_CALL_PATTERN.search(line):
                    continue

                # Check if nearby context (±5 lines) has structured fields
                context_window = '\n'.join(lines[max(0, i-5):i+5])
                missing_fields = []
                for field_name, field_pattern in REQUIRED_CONTEXT_FIELDS:
                    if not field_pattern.search(context_window):
                        missing_fields.append(field_name)

                if len(missing_fields) >= 2:  # Missing 2+ required fields
                    findings.append({
                        'file': fpath,
                        'line': i,
                        'code': line.strip()[:100],
                        'smell': 'MISSING_STRUCTURED_CONTEXT',
                        'message': f'Log in web handler missing: {", ".join(missing_fields)}',
                        'severity': 'MEDIUM',
                    })

    return findings
```

---

## Step 5: Output Report

```markdown
## Log Smell Audit
Project: my-api | Files scanned: 312 | Log calls found: 847

---

### Summary

| Smell | Count | Severity |
|-------|-------|---------|
| 🔴 PII Exposure | 3 | CRITICAL/HIGH |
| 🟠 Debug Leaks | 12 | MEDIUM |
| 🟡 Missing Structured Context | 8 | MEDIUM |
| ⚪ Noisy Debug in Loop | 2 | LOW |

---

### 🔴 CRITICAL — PII in Logs (3 findings)

**1. src/auth/login.ts:89**
```ts
logger.info(`User login: ${email} with password: ${password}`)
```
⚠️ **Password logged in plaintext.** This is a CRITICAL security and compliance issue.

Fix:
```ts
logger.info('User login attempt', { email: email, success: true })
// NEVER log password — not even hashed
```

**2. src/api/payments.ts:134**
```ts
console.log('Processing card', cardNumber, cvv)
```
⚠️ **Credit card number and CVV in log — PCI-DSS violation.**

Fix:
```ts
logger.info('Processing payment', { card_last4: cardNumber.slice(-4) })
```

**3. src/middleware/auth.ts:12**
```ts
log.debug(`Authorization: Bearer ${token}`)
```
⚠️ **Bearer token logged — enables credential theft from logs.**

Fix:
```ts
log.debug('Auth header present', { has_token: !!token })
```

---

### 🟠 Debug Leaks (12 console.log / print statements)

Top 5 production-path findings:

| File | Line | Code |
|------|------|------|
| src/services/user.ts | 23 | `console.log("processing user", userId)` |
| src/db/queries.ts | 67 | `console.log("query result:", rows)` |
| app/models/order.rb | 45 | `puts order.inspect` |
| handlers/webhook.go | 12 | `fmt.Println("webhook received", payload)` |
| src/utils/cache.ts | 89 | `console.log("cache miss for key:", key)` |

**Fix — replace with structured logger:**
```ts
// Before:
console.log("processing user", userId)

// After (pino/winston):
logger.debug({ userId }, 'Processing user')

// OR remove if not needed in production:
// (delete the line)
```

**One-command removal of all console.log in src/:**
```bash
# Preview (does not modify):
grep -rn "console\.log" src/ --include="*.ts" --include="*.js"

# Remove (careful — review first):
find src/ -name "*.ts" -o -name "*.js" | xargs sed -i '/console\.log/d'
```

---

### 🟡 Missing Structured Context (8 web handler logs)

These logs are in HTTP request handlers but are missing request_id and/or user_id:

**src/routes/orders.ts:45**
```ts
router.get('/orders', async (req, res) => {
    logger.info('Fetching orders')  // ← no request_id, no user_id
    const orders = await db.getOrders()
```

Fix:
```ts
logger.info('Fetching orders', {
    request_id: req.headers['x-request-id'],
    user_id: req.user?.id,
    method: req.method,
    path: req.path,
})
```

**Add request context middleware once, fix all handlers:**
```ts
// middleware/logging.ts
app.use((req, res, next) => {
    req.log = logger.child({
        request_id: req.headers['x-request-id'] || crypto.randomUUID(),
        method: req.method,
        path: req.path,
    })
    next()
})

// Now all handlers use: req.log.info('Fetching orders', { user_id: req.user?.id })
```

---

### CI Integration

```bash
# Fail CI if any CRITICAL log smells found
python3 -m log_smell_auditor --ci --max-critical 0 --max-pii 0 src/
# Exit 1 if violations found — add to pre-commit hook or CI pipeline
```
```

---

## Quick Mode Output

```
Log Audit: my-api (312 files, 847 log calls)

🔴 3 PII exposures — password logged plaintext (auth/login.ts:89), credit card (payments.ts:134), Bearer token (middleware/auth.ts:12)
🟠 12 debug leaks — console.log in production paths (src/services, src/db, handlers)
🟡 8 handler logs missing request_id/user_id context
⚪ 2 debug loops — logger.debug inside tight loop in cache.ts, queue.ts

Priority: Fix PII exposures IMMEDIATELY (compliance risk)
Quick win: Add request context middleware → fixes all 8 missing-context findings at once
```

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
