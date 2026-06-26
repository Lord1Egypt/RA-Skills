---
name: Async Audit
description: Async/await error handling auditor. Scans JavaScript/TypeScript, Python, and Go code for unhandled async errors — floating promises (fire-and-forget with no .catch()), Express async route handlers without try/catch, Promise.all without error boundary, asyncio.create_task swallowing exceptions, goroutine error returns silently ignored, and missing unhandledRejection process listeners. Finds the silent crashes that only appear in production logs at 3am. Zero external dependencies. Zero competitors on ClawHub.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - async
  - javascript
  - typescript
  - python
  - go
  - error-handling
  - developer-tools
  - static-analysis
  - reliability
---

# phy-async-audit

**Async/await error handling auditor** — catches the silent async failures that crash production services with no stack trace, no log entry, and no alert. These bugs don't appear in unit tests because they only trigger on unexpected rejection paths.

Async errors are uniquely dangerous: an unhandled Promise rejection in Node.js used to terminate the process silently (pre-v15), now produces a warning that most teams never see. A forgotten `await` makes a function return `undefined` instead of throwing. A `Promise.all()` without a try/catch fails the entire batch when one item errors.

## What It Detects

| ID | Pattern | Severity | Impact |
|----|---------|----------|--------|
| AE001 | Floating promise — async call without `await` and without `.catch()` | HIGH | Exception silently swallowed |
| AE002 | Express/Fastify async route handler without try/catch | CRITICAL | Uncaught exception crashes request handler |
| AE003 | `Promise.all()` / `Promise.allSettled()` without error boundary | HIGH | One failure fails all; no partial result |
| AE004 | `new Promise()` constructor with missing `reject` call path | MEDIUM | Promise hangs forever on error branch |
| AE005 | `await` inside loop without per-iteration error handling | MEDIUM | First error aborts all remaining iterations |
| AE006 | `asyncio.create_task()` without done callback or await | HIGH | Exception logged to stderr only, not propagated |
| AE007 | `asyncio.gather()` without `return_exceptions=True` or try/except | HIGH | One failed coroutine kills all |
| AE008 | `async def` endpoint (FastAPI/aiohttp) without except clause | CRITICAL | Unhandled exception returns 500 with no logging |
| AE009 | Go goroutine ignoring error return values | HIGH | Errors silently discarded at concurrency boundary |
| AE010 | No `process.on('unhandledRejection')` in Node.js entry file | MEDIUM | Unhandled rejections produce warnings only |

## Trigger Phrases

```
/phy-async-audit
Check my codebase for unhandled async errors
```

```
/phy-async-audit
Find floating promises and missing try/catch in src/
```

```
/phy-async-audit
Why is my Express server silently dying on async routes?
```

```
/phy-async-audit
Audit async error handling before production deploy
```

---

## Implementation

When invoked, execute the following Python analysis.

```python
#!/usr/bin/env python3
"""
phy-async-audit — Async/await error handling scanner
Detects AE001–AE010 in JavaScript/TypeScript, Python, and Go.
Zero external dependencies.
"""
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# ─────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────

SKIP_DIRS = {
    '__pycache__', '.git', 'node_modules', 'vendor', '.venv', 'venv',
    'dist', 'build', '.next', 'coverage',
}

SEVERITY_ORDER = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
SEVERITY_EMOJI = {'CRITICAL': '💀', 'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🔵'}

CI_MODE = '--ci' in sys.argv
MIN_SEVERITY = next(
    (sys.argv[sys.argv.index('--min-severity') + 1]
     for _ in ['x'] if '--min-severity' in sys.argv),
    'LOW'
)

JS_EXTS = {'.js', '.ts', '.mjs', '.cjs', '.jsx', '.tsx'}
PY_EXTS = {'.py'}
GO_EXTS = {'.go'}
ALL_EXTS = JS_EXTS | PY_EXTS | GO_EXTS


# ─────────────────────────────────────────────────────
# Data model
# ─────────────────────────────────────────────────────

@dataclass
class Finding:
    check_id: str
    file: str
    line: int
    severity: str
    description: str
    matched_text: str
    fix: str


# ─────────────────────────────────────────────────────
# File walker
# ─────────────────────────────────────────────────────

def walk_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS and not d.startswith('.')]
        for fname in filenames:
            fpath = Path(dirpath) / fname
            if fpath.suffix.lower() not in ALL_EXTS:
                continue
            # Skip test files — async errors in tests are expected
            name_lower = fpath.name.lower()
            if any(x in name_lower for x in
                   ('test', 'spec', '.test.', '.spec.', '_test', 'mock', 'fixture')):
                continue
            try:
                content = fpath.read_text(errors='ignore')
                yield fpath, content
            except Exception:
                continue


def _is_js(fpath: Path) -> bool:
    return fpath.suffix.lower() in JS_EXTS

def _is_py(fpath: Path) -> bool:
    return fpath.suffix.lower() in PY_EXTS

def _is_go(fpath: Path) -> bool:
    return fpath.suffix.lower() in GO_EXTS


# ─────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────

def _has_nearby(lines: list[str], line_idx: int, patterns: list[re.Pattern],
                before: int = 5, after: int = 20) -> bool:
    start = max(0, line_idx - before)
    end = min(len(lines), line_idx + after)
    window = '\n'.join(lines[start:end])
    return any(p.search(window) for p in patterns)


# ─────────────────────────────────────────────────────
# AE001 — Floating promise (JS/TS)
# ─────────────────────────────────────────────────────

# Async function call patterns: someAsync(), this.service.fetch(), await-less
ASYNC_CALL_RE = re.compile(
    r"""^(?P<indent>\s*)
        (?!(?:const|let|var|return|throw|await|if|else|while|for|=)\s)
        (?!\/\/)
        (?P<call>
            (?:\w+\.)*\w+\s*\([^)]*\)   # method or function call
        )
        \s*;?\s*$""",
    re.VERBOSE | re.MULTILINE
)

# Indicators that a call is async (returns a Promise)
ASYNC_INDICATOR_RE = re.compile(
    r"""async\s+function|
        \.then\s*\(|
        Promise\.|
        fetch\s*\(|
        axios\.|
        \.send\s*\(|
        \.save\s*\(|
        \.create\s*\(|
        \.update\s*\(|
        \.delete\s*\(|
        \.findOne\s*\(|
        \.findAll\s*\(|
        readFile|writeFile|
        setTimeout|setInterval|
        emit\s*\(""",
    re.IGNORECASE | re.VERBOSE
)

# Patterns that indicate the call IS handled
FLOATING_HANDLED_RE = [
    re.compile(r'\.catch\s*\('),
    re.compile(r'await\s+'),
    re.compile(r'\.then\s*\('),
    re.compile(r'try\s*\{'),
]

# Explicitly async function names (conservative list to reduce false positives)
KNOWN_ASYNC_PREFIXES = re.compile(
    r"""^(?:
        send|fetch|post|get|put|patch|delete|
        save|create|update|destroy|remove|
        load|download|upload|
        connect|disconnect|
        emit|dispatch|publish|
        notify|alert|
        log\w*|track\w*|
        refresh|sync|
        execute|run|process|handle
    )\w*\s*\(""",
    re.IGNORECASE | re.VERBOSE
)


def check_ae001_floating_promise(fpath: Path, content: str) -> list[Finding]:
    """Detect floating async calls — called without await and without .catch()"""
    findings = []
    lines = content.split('\n')

    # Only process files that have async code
    if 'async ' not in content and 'Promise' not in content:
        return []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith('//') or stripped.startswith('*'):
            continue

        # Look for standalone function calls that look async (no await, no assignment)
        # Pattern: line is just a function call, no assignment
        if not re.match(r'^\s*\w[\w.]*\s*\(', line):
            continue
        # Must not be an assignment
        if '=' in line.split('(')[0]:
            continue
        # Must not already have await
        if 'await' in line:
            continue
        # Must not be a return statement
        if stripped.startswith('return '):
            continue
        # Must look like an async operation
        if not KNOWN_ASYNC_PREFIXES.search(stripped):
            continue
        # Check for .catch() on the same line
        if '.catch(' in line:
            continue
        # Check for try/catch in surrounding context
        window_before = '\n'.join(lines[max(0, i-3):i])
        window_after = '\n'.join(lines[i:min(len(lines), i+3)])
        if 'try {' in window_before or '.catch(' in window_after:
            continue

        # Check if we're inside an async function context
        # Look up to find containing function
        context_start = max(0, i - 30)
        context = '\n'.join(lines[context_start:i + 1])
        if 'async ' not in context:
            continue

        findings.append(Finding(
            check_id='AE001',
            file=str(fpath),
            line=i + 1,
            severity='HIGH',
            description=(
                f'Floating promise — `{stripped[:60]}` called without `await` '
                f'and without `.catch()`. Errors are silently swallowed.'
            ),
            matched_text=stripped[:120],
            fix=(
                '// Option 1: await it (preferred if you care about the result)\n'
                'await someAsyncFn();\n\n'
                '// Option 2: attach .catch() for fire-and-forget\n'
                'someAsyncFn().catch(err => logger.error("Failed:", err));\n\n'
                '// Option 3: void operator to signal intentional fire-and-forget\n'
                'void someAsyncFn(); // explicit — but still add monitoring'
            ),
        ))
    return findings


# ─────────────────────────────────────────────────────
# AE002 — Express/Fastify async handler without try/catch
# ─────────────────────────────────────────────────────

# Route handler patterns: app.get('/path', async (req, res) => {
EXPRESS_ROUTE_RE = re.compile(
    r"""(?:app|router|fastify|server)\s*\.\s*
        (?:get|post|put|patch|delete|use|all)\s*\(
        [^,)]+,\s*
        async\s*(?:\([^)]*\)|[^=]+=>)""",
    re.VERBOSE | re.IGNORECASE
)

TRYCATCH_NEARBY_RE = [
    re.compile(r'\btry\s*\{'),
    re.compile(r'\.catch\s*\('),
    re.compile(r'asyncHandler\s*\('),
    re.compile(r'catchAsync\s*\('),
    re.compile(r'wrapAsync\s*\('),
    re.compile(r'express-async-handler'),
    re.compile(r'express-async-errors'),
]


def check_ae002_express_async(fpath: Path, content: str) -> list[Finding]:
    if not _is_js(fpath):
        return []
    if 'express' not in content.lower() and 'fastify' not in content.lower():
        return []

    findings = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if not EXPRESS_ROUTE_RE.search(line):
            continue
        # Check next 30 lines for try/catch or error wrapper
        if _has_nearby(lines, i, TRYCATCH_NEARBY_RE, before=0, after=30):
            continue
        findings.append(Finding(
            check_id='AE002',
            file=str(fpath),
            line=i + 1,
            severity='CRITICAL',
            description=(
                'Express async route handler without try/catch. '
                'If the async function throws, Express receives an unhandled rejection '
                '— the request hangs or the process crashes (Node < v15).'
            ),
            matched_text=line.strip()[:120],
            fix=(
                '// Option 1: Wrap with try/catch\n'
                'app.get("/path", async (req, res, next) => {\n'
                '    try {\n'
                '        const data = await service.getData();\n'
                '        res.json(data);\n'
                '    } catch (err) {\n'
                '        next(err);  // passes to Express error handler\n'
                '    }\n'
                '});\n\n'
                '// Option 2: Use express-async-errors (wraps automatically)\n'
                "require('express-async-errors');  // at top of entry file"
            ),
        ))
    return findings


# ─────────────────────────────────────────────────────
# AE003 — Promise.all without error boundary
# ─────────────────────────────────────────────────────

PROMISE_ALL_RE = re.compile(
    r'Promise\s*\.\s*(?:all|race|any)\s*\(',
    re.IGNORECASE
)

PROMISE_ALL_GUARDED_RE = [
    re.compile(r'\btry\s*\{'),
    re.compile(r'\.catch\s*\('),
    re.compile(r'allSettled\s*\('),
]


def check_ae003_promise_all(fpath: Path, content: str) -> list[Finding]:
    if not _is_js(fpath):
        return []

    findings = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if not PROMISE_ALL_RE.search(line):
            continue
        # Check: is it wrapped in try/catch or followed by .catch()?
        if _has_nearby(lines, i, PROMISE_ALL_GUARDED_RE, before=5, after=5):
            continue
        match = PROMISE_ALL_RE.search(line)
        method = match.group(0).split('.')[-1].split('(')[0].strip()
        findings.append(Finding(
            check_id='AE003',
            file=str(fpath),
            line=i + 1,
            severity='HIGH',
            description=(
                f'`Promise.{method}()` without error boundary. '
                f'`Promise.all` rejects immediately when ANY promise rejects — '
                f'all other results are lost, and the rejection may be unhandled.'
            ),
            matched_text=line.strip()[:120],
            fix=(
                '// Option 1: try/catch\n'
                'try {\n'
                '    const results = await Promise.all([p1, p2, p3]);\n'
                '} catch (err) {\n'
                '    logger.error("One of the promises failed:", err);\n'
                '}\n\n'
                '// Option 2: use allSettled if partial results are acceptable\n'
                'const results = await Promise.allSettled([p1, p2, p3]);\n'
                'const failed = results.filter(r => r.status === "rejected");\n'
                'if (failed.length) logger.error("Some failed:", failed);'
            ),
        ))
    return findings


# ─────────────────────────────────────────────────────
# AE004 — new Promise() with missing reject path
# ─────────────────────────────────────────────────────

NEW_PROMISE_RE = re.compile(
    r'new\s+Promise\s*\(\s*(?:function\s*)?\(\s*(?:resolve\s*,\s*reject|res\s*,\s*rej)\s*\)'
)


def check_ae004_promise_constructor(fpath: Path, content: str) -> list[Finding]:
    if not _is_js(fpath):
        return []

    findings = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if not NEW_PROMISE_RE.search(line):
            continue

        # Find the Promise body (next ~30 lines)
        end = min(len(lines), i + 30)
        body = '\n'.join(lines[i:end])

        # Check if reject/rej is actually called in the body
        reject_called = re.search(r'\b(?:reject|rej)\s*\(', body)
        if reject_called:
            continue

        findings.append(Finding(
            check_id='AE004',
            file=str(fpath),
            line=i + 1,
            severity='MEDIUM',
            description=(
                '`new Promise()` constructor where `reject` appears never called. '
                'If an error occurs in the callback, the Promise hangs forever instead of failing fast.'
            ),
            matched_text=line.strip()[:120],
            fix=(
                'new Promise((resolve, reject) => {\n'
                '    try {\n'
                '        // your async operation\n'
                '        resolve(result);\n'
                '    } catch (err) {\n'
                '        reject(err);  // always handle the error path\n'
                '    }\n'
                '});'
            ),
        ))
    return findings


# ─────────────────────────────────────────────────────
# AE005 — await inside loop without per-iteration error handling
# ─────────────────────────────────────────────────────

LOOP_START_RE = re.compile(
    r'^\s*(?:for|while)\s*[\(\s]'
)

AWAIT_IN_LOOP_RE = re.compile(r'\bawait\b')

LOOP_TRY_CATCH_RE = [re.compile(r'\btry\s*\{')]


def check_ae005_await_in_loop(fpath: Path, content: str) -> list[Finding]:
    if not _is_js(fpath):
        return []

    findings = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if not LOOP_START_RE.match(line):
            continue

        # Find loop body (next ~20 lines)
        end = min(len(lines), i + 20)
        body_lines = lines[i:end]
        body = '\n'.join(body_lines)

        if not AWAIT_IN_LOOP_RE.search(body):
            continue

        # Good if loop body has its own try/catch
        if re.search(r'\btry\s*\{', body):
            continue

        # Find the await line
        for j, bline in enumerate(body_lines[1:], 1):
            if AWAIT_IN_LOOP_RE.search(bline):
                findings.append(Finding(
                    check_id='AE005',
                    file=str(fpath),
                    line=i + j + 1,
                    severity='MEDIUM',
                    description=(
                        '`await` inside a loop without per-iteration try/catch. '
                        'If one iteration fails, the entire loop aborts and remaining items are skipped.'
                    ),
                    matched_text=bline.strip()[:120],
                    fix=(
                        '// Wrap each iteration in try/catch:\n'
                        'for (const item of items) {\n'
                        '    try {\n'
                        '        await processItem(item);\n'
                        '    } catch (err) {\n'
                        '        logger.error(`Failed for item ${item.id}:`, err);\n'
                        '        // continue loop or collect failures\n'
                        '    }\n'
                        '}\n\n'
                        '// Or use allSettled for batch processing:\n'
                        'const results = await Promise.allSettled(items.map(processItem));'
                    ),
                ))
                break  # one finding per loop
    return findings


# ─────────────────────────────────────────────────────
# AE006 — asyncio.create_task without error handling (Python)
# ─────────────────────────────────────────────────────

CREATE_TASK_RE = re.compile(r'asyncio\.create_task\s*\(')

TASK_ERROR_HANDLED_RE = [
    re.compile(r'add_done_callback'),
    re.compile(r'\.result\s*\(\)'),
    re.compile(r'await\s+\w+'),  # task is awaited
    re.compile(r'tasks\.append'),  # collected for later gathering
    re.compile(r'asyncio\.gather'),
]


def check_ae006_create_task(fpath: Path, content: str) -> list[Finding]:
    if not _is_py(fpath):
        return []

    findings = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if not CREATE_TASK_RE.search(line):
            continue

        # Check if the task variable is used for error handling
        # Look at next 15 lines
        if _has_nearby(lines, i, TASK_ERROR_HANDLED_RE, before=0, after=15):
            continue

        # Check if the return value is assigned
        has_assignment = '=' in line.split('create_task')[0]
        if not has_assignment:
            findings.append(Finding(
                check_id='AE006',
                file=str(fpath),
                line=i + 1,
                severity='HIGH',
                description=(
                    '`asyncio.create_task()` result not awaited or assigned to a variable. '
                    'Exceptions in the task are logged to stderr only — not propagated to the caller.'
                ),
                matched_text=line.strip()[:120],
                fix=(
                    '# Option 1: await the task directly (sequential)\n'
                    'await asyncio.create_task(my_coroutine())\n\n'
                    '# Option 2: add done callback for fire-and-forget with error reporting\n'
                    'def handle_exception(task):\n'
                    '    if not task.cancelled() and task.exception():\n'
                    '        logger.error("Task failed:", exc_info=task.exception())\n'
                    'task = asyncio.create_task(my_coroutine())\n'
                    'task.add_done_callback(handle_exception)\n\n'
                    '# Option 3: collect tasks for gather\n'
                    'tasks = [asyncio.create_task(c) for c in coroutines]\n'
                    'results = await asyncio.gather(*tasks, return_exceptions=True)'
                ),
            ))
    return findings


# ─────────────────────────────────────────────────────
# AE007 — asyncio.gather without return_exceptions (Python)
# ─────────────────────────────────────────────────────

GATHER_RE = re.compile(r'asyncio\.gather\s*\(')
GATHER_SAFE_RE = [
    re.compile(r'return_exceptions\s*=\s*True'),
    re.compile(r'try\s*:'),
    re.compile(r'except\s+'),
]


def check_ae007_gather(fpath: Path, content: str) -> list[Finding]:
    if not _is_py(fpath):
        return []

    findings = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if not GATHER_RE.search(line):
            continue
        if _has_nearby(lines, i, GATHER_SAFE_RE, before=3, after=10):
            continue
        findings.append(Finding(
            check_id='AE007',
            file=str(fpath),
            line=i + 1,
            severity='HIGH',
            description=(
                '`asyncio.gather()` without `return_exceptions=True` or try/except. '
                'If any coroutine raises, gather raises immediately and cancels others.'
            ),
            matched_text=line.strip()[:120],
            fix=(
                '# Option 1: return_exceptions=True (gather all results)\n'
                'results = await asyncio.gather(*tasks, return_exceptions=True)\n'
                'errors = [r for r in results if isinstance(r, Exception)]\n'
                'if errors:\n'
                '    for e in errors:\n'
                '        logger.error("Task failed:", exc_info=e)\n\n'
                '# Option 2: wrap in try/except (stops on first failure)\n'
                'try:\n'
                '    results = await asyncio.gather(*tasks)\n'
                'except Exception as e:\n'
                '    logger.error("Gather failed:", e)'
            ),
        ))
    return findings


# ─────────────────────────────────────────────────────
# AE008 — FastAPI/aiohttp async handler without except (Python)
# ─────────────────────────────────────────────────────

FASTAPI_HANDLER_RE = re.compile(
    r"""@(?:app|router|api_router)\s*\.\s*
        (?:get|post|put|patch|delete|websocket)\s*\([^)]*\)\s*\n
        \s*async\s+def\s+\w+\s*\(""",
    re.VERBOSE | re.MULTILINE
)

AIOHTTP_HANDLER_RE = re.compile(
    r'async\s+def\s+\w+\s*\(\s*request\s*:\s*(?:web\.)?Request\s*\)'
)

ASYNC_DEF_WITH_AWAIT_RE = re.compile(r'async\s+def\s+(\w+)\s*\(')
EXCEPT_RE = re.compile(r'\bexcept\b')
AWAIT_IN_BODY_RE = re.compile(r'\bawait\b')


def check_ae008_async_handler(fpath: Path, content: str) -> list[Finding]:
    if not _is_py(fpath):
        return []
    if 'fastapi' not in content.lower() and 'aiohttp' not in content.lower():
        return []

    findings = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        # Check for FastAPI route decorator followed by async def
        if not (line.strip().startswith('@') and
                re.search(r'\.(get|post|put|patch|delete)\s*\(', line)):
            continue

        # Find the async def on next non-blank line
        handler_line = i + 1
        while handler_line < len(lines) and not lines[handler_line].strip():
            handler_line += 1
        if handler_line >= len(lines):
            continue
        if not re.match(r'\s*async\s+def\s+', lines[handler_line]):
            continue

        # Find function body (next ~40 lines until same/lower indent)
        base_indent = len(lines[handler_line]) - len(lines[handler_line].lstrip())
        end_line = handler_line + 1
        for j in range(handler_line + 1, min(len(lines), handler_line + 50)):
            l = lines[j]
            if l.strip() and (len(l) - len(l.lstrip())) <= base_indent:
                end_line = j
                break
        else:
            end_line = min(len(lines), handler_line + 50)

        body = '\n'.join(lines[handler_line:end_line])

        # Must have await to be a real async handler
        if not AWAIT_IN_BODY_RE.search(body):
            continue
        # Skip if already has except
        if EXCEPT_RE.search(body):
            continue

        fn_name_m = re.search(r'async\s+def\s+(\w+)', lines[handler_line])
        fn_name = fn_name_m.group(1) if fn_name_m else '<handler>'

        findings.append(Finding(
            check_id='AE008',
            file=str(fpath),
            line=handler_line + 1,
            severity='CRITICAL',
            description=(
                f'FastAPI async handler `{fn_name}` has `await` calls but no `except` clause. '
                f'An unhandled exception returns 500 with no structured error response or logging.'
            ),
            matched_text=lines[handler_line].strip()[:120],
            fix=(
                '@app.get("/items/{item_id}")\n'
                'async def get_item(item_id: int):\n'
                '    try:\n'
                '        item = await db.get_item(item_id)\n'
                '        if not item:\n'
                '            raise HTTPException(status_code=404, detail="Not found")\n'
                '        return item\n'
                '    except HTTPException:\n'
                '        raise  # re-raise HTTP exceptions\n'
                '    except Exception as e:\n'
                '        logger.error("Unexpected error in get_item:", exc_info=True)\n'
                '        raise HTTPException(status_code=500, detail="Internal error")'
            ),
        ))
    return findings


# ─────────────────────────────────────────────────────
# AE009 — Go goroutine ignoring error returns
# ─────────────────────────────────────────────────────

GO_GOROUTINE_RE = re.compile(r'\bgo\s+func\s*\(')
GO_IGNORED_ERROR_RE = re.compile(
    r"""^\s*
        (?:\w+\.)*\w+\s*\([^)]*\)\s*$  # func call with no assignment
    """,
    re.VERBOSE
)
# Functions that commonly return errors
GO_ERROR_RETURNING_RE = re.compile(
    r"""(?:
        \.Write\s*\(|
        \.Read\s*\(|
        \.Close\s*\(|
        \.Exec\s*\(|
        \.Query\s*\(|
        \.Scan\s*\(|
        \.Decode\s*\(|
        \.Encode\s*\(|
        json\.Marshal\s*\(|
        json\.Unmarshal\s*\(|
        os\.Open\s*\(|
        os\.Create\s*\(|
        ioutil\.ReadFile\s*\(|
        http\.Get\s*\(|
        http\.Post\s*\(
    )""",
    re.VERBOSE
)

GO_ERROR_CHECK_RE = re.compile(r'if\s+err\s*!=\s*nil|log\.\w*\s*\(.*err|panic\s*\(')


def check_ae009_goroutine_errors(fpath: Path, content: str) -> list[Finding]:
    if not _is_go(fpath):
        return []

    findings = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if not GO_GOROUTINE_RE.search(line):
            continue

        # Find goroutine body (next ~30 lines)
        end = min(len(lines), i + 30)
        body_lines = lines[i:end]
        body = '\n'.join(body_lines)

        # Check if there's error handling in the goroutine
        if GO_ERROR_CHECK_RE.search(body):
            continue
        # Check if error-returning functions are called
        if not GO_ERROR_RETURNING_RE.search(body):
            continue

        findings.append(Finding(
            check_id='AE009',
            file=str(fpath),
            line=i + 1,
            severity='HIGH',
            description=(
                'Goroutine calls error-returning functions without checking errors. '
                'Errors inside goroutines do not propagate to the caller — they are silently ignored.'
            ),
            matched_text=line.strip()[:120],
            fix=(
                'go func() {\n'
                '    defer func() {\n'
                '        if r := recover(); r != nil {\n'
                '            log.Printf("goroutine panic: %v", r)\n'
                '        }\n'
                '    }()\n'
                '    if err := db.Exec(query); err != nil {\n'
                '        log.Printf("goroutine error: %v", err)\n'
                '        // optionally send to errChan\n'
                '    }\n'
                '}()'
            ),
        ))
    return findings


# ─────────────────────────────────────────────────────
# AE010 — Missing unhandledRejection handler (Node.js entry files)
# ─────────────────────────────────────────────────────

UNHANDLED_REJECTION_RE = re.compile(
    r"""process\.on\s*\(\s*['"]unhandledRejection['"]|
        process\.on\s*\(\s*['"]uncaughtException['"]""",
    re.VERBOSE
)

# Entry file heuristics
ENTRY_FILE_INDICATORS = re.compile(
    r"""app\.listen\s*\(|
        server\.listen\s*\(|
        fastify\.listen\s*\(|
        createServer\s*\(|
        http\.createServer|
        https\.createServer""",
    re.VERBOSE | re.IGNORECASE
)


def check_ae010_unhandled_rejection(fpath: Path, content: str) -> list[Finding]:
    if not _is_js(fpath):
        return []

    # Only check entry files (files with server.listen or similar)
    if not ENTRY_FILE_INDICATORS.search(content):
        return []

    # If already has unhandledRejection handler, fine
    if UNHANDLED_REJECTION_RE.search(content):
        return []

    return [Finding(
        check_id='AE010',
        file=str(fpath),
        line=1,
        severity='MEDIUM',
        description=(
            'Node.js entry file without `process.on("unhandledRejection")` handler. '
            'Unhandled Promise rejections produce a deprecation warning in Node v15+ '
            'and terminated the process in earlier versions.'
        ),
        matched_text=fpath.name,
        fix=(
            '// Add at the top of your entry file (index.js / app.js / server.js):\n'
            'process.on("unhandledRejection", (reason, promise) => {\n'
            '    logger.error("Unhandled Promise Rejection:", reason);\n'
            '    // Optionally: process.exit(1) for strict mode\n'
            '});\n\n'
            'process.on("uncaughtException", (err) => {\n'
            '    logger.error("Uncaught Exception:", err);\n'
            '    process.exit(1);  // Always exit on uncaught exceptions\n'
            '});'
        ),
    )]


# ─────────────────────────────────────────────────────
# Main runner
# ─────────────────────────────────────────────────────

ALL_CHECKS = [
    check_ae001_floating_promise,
    check_ae002_express_async,
    check_ae003_promise_all,
    check_ae004_promise_constructor,
    check_ae005_await_in_loop,
    check_ae006_create_task,
    check_ae007_gather,
    check_ae008_async_handler,
    check_ae009_goroutine_errors,
    check_ae010_unhandled_rejection,
]


def deduplicate(findings: list[Finding]) -> list[Finding]:
    seen: set[tuple] = set()
    result = []
    for f in findings:
        key = (f.check_id, f.file, f.line)
        if key not in seen:
            seen.add(key)
            result.append(f)
    return result


def run_audit(root: Path) -> int:
    print(f"\n🔍  phy-async-audit — scanning {root}\n{'─'*60}")

    all_findings: list[Finding] = []
    severity_threshold = SEVERITY_ORDER.get(MIN_SEVERITY, 3)

    for fpath, content in walk_files(root):
        for check in ALL_CHECKS:
            try:
                results = check(fpath, content)
                all_findings.extend(results)
            except Exception:
                pass

    all_findings = deduplicate(all_findings)
    all_findings = [f for f in all_findings
                    if SEVERITY_ORDER.get(f.severity, 3) <= severity_threshold]
    all_findings.sort(key=lambda f: (SEVERITY_ORDER.get(f.severity, 3), f.file, f.line))

    if not all_findings:
        print("✅  No async error handling issues found.")
        return 0

    critical = sum(1 for f in all_findings if f.severity == 'CRITICAL')
    high = sum(1 for f in all_findings if f.severity == 'HIGH')
    med = sum(1 for f in all_findings if f.severity == 'MEDIUM')
    low = sum(1 for f in all_findings if f.severity == 'LOW')

    print(f"Found {len(all_findings)} issue(s): "
          f"💀 CRITICAL={critical}  🔴 HIGH={high}  🟡 MEDIUM={med}  🔵 LOW={low}\n")

    current_severity = None
    for f in all_findings:
        if f.severity != current_severity:
            current_severity = f.severity
            emoji = SEVERITY_EMOJI.get(f.severity, '⚪')
            print(f"\n{emoji} {f.severity}\n{'─'*50}")

        print(f"\n[{f.check_id}] {f.file}:{f.line}")
        print(f"  {f.description}")
        print(f"  Matched: {f.matched_text}")
        print(f"  Fix:")
        for fix_line in f.fix.split('\n'):
            print(f"    {fix_line}")

    # Breakdown by check
    from collections import Counter
    counts = Counter(f.check_id for f in all_findings)
    print(f"\n{'═'*60}")
    print("Breakdown:")
    for check_id, count in sorted(counts.items(), key=lambda x: -x[1]):
        label = {
            'AE001': 'Floating promise',
            'AE002': 'Express async without try/catch',
            'AE003': 'Promise.all without boundary',
            'AE004': 'Promise constructor missing reject',
            'AE005': 'await in loop without error handling',
            'AE006': 'asyncio.create_task no callback',
            'AE007': 'asyncio.gather no return_exceptions',
            'AE008': 'FastAPI handler no except',
            'AE009': 'Goroutine ignoring errors',
            'AE010': 'Missing unhandledRejection handler',
        }.get(check_id, check_id)
        print(f"  {check_id}: {count}  — {label}")

    print(f"\nCI fail-gate (fails on CRITICAL or HIGH):")
    print(f"  python async_audit.py --root . --ci --min-severity HIGH")

    if CI_MODE and (critical + high) > 0:
        print(f"\n[CI] Exit 1 — {critical + high} CRITICAL/HIGH async errors found.")
        return 1
    return 0


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Async/await error handling auditor')
    parser.add_argument('--root', default='.', help='Root directory to scan')
    parser.add_argument('--ci', action='store_true', help='Exit 1 on CRITICAL or HIGH')
    parser.add_argument('--min-severity', choices=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
                        default='LOW')
    args = parser.parse_args()
    CI_MODE = args.ci
    MIN_SEVERITY = args.min_severity
    sys.exit(run_audit(Path(args.root)))
```

---

## Example Output

```
🔍  phy-async-audit — scanning /home/user/myapi
────────────────────────────────────────────────────────────
Found 6 issue(s): 💀 CRITICAL=2  🔴 HIGH=3  🟡 MEDIUM=1  🔵 LOW=0

💀 CRITICAL
──────────────────────────────────────────────────────

[AE002] src/routes/users.js:34
  Express async route handler without try/catch.
  If the async function throws, Express receives an unhandled rejection —
  the request hangs or the process crashes (Node < v15).
  Matched: app.get('/users/:id', async (req, res) => {
  Fix:
    app.get("/users/:id", async (req, res, next) => {
        try {
            const user = await User.findById(req.params.id);
            res.json(user);
        } catch (err) {
            next(err);
        }
    });

[AE008] src/api/payments.py:89
  FastAPI async handler `process_payment` has await calls but no except clause.
  Fix:
    try:
        result = await payment_service.charge(amount)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Unexpected error:", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal error")

🔴 HIGH
──────────────────────────────────────────────────────

[AE003] src/services/data.js:67
  Promise.all() without error boundary. One failure kills all.
  Matched: const [users, orders] = await Promise.all([getUsers(), getOrders()]);
  Fix:
    const results = await Promise.allSettled([getUsers(), getOrders()]);

════════════════════════════════════════════════════════════
Breakdown:
  AE002: 2  — Express async without try/catch
  AE008: 1  — FastAPI handler no except
  AE003: 1  — Promise.all without boundary
  AE006: 1  — asyncio.create_task no callback
  AE010: 1  — Missing unhandledRejection handler

CI fail-gate (fails on CRITICAL or HIGH):
  python async_audit.py --root . --ci --min-severity HIGH
```

---

## Why Async Errors Are Different

Async errors are **structurally silent**: unlike synchronous exceptions that propagate up the call stack and crash with a stack trace, async errors in the wrong context:

1. **Node.js**: An unhandled Promise rejection from 2018–2020 code produces only `(node:12345) UnhandledPromiseRejectionWarning` — no crash, no alert, customers just see broken behavior
2. **Python asyncio**: `asyncio.create_task()` exceptions are logged to `sys.stderr` with "Task exception was never retrieved" — invisible in production logs that only capture `stdout`
3. **Go goroutines**: There is no automatic panic propagation out of goroutines — each goroutine needs its own `defer/recover`

## Relationship to Other phy- Skills

| Skill | What It Finds |
|-------|---------------|
| `phy-async-audit` (this) | Unhandled async errors, floating promises, silent async failures |
| `phy-concurrency-audit` | Race conditions, data races, TOCTOU bugs |
| `phy-code-smell` | Structural quality — long functions, god classes |
| `phy-regex-audit` | ReDoS vulnerabilities in regex |

`phy-async-audit` and `phy-concurrency-audit` together cover the full concurrent programming risk surface: async-audit covers error propagation, concurrency-audit covers shared state.

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
