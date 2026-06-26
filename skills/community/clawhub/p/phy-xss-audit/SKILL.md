---
name: XSS Audit
description: Cross-Site Scripting (XSS) static vulnerability scanner (OWASP A03:2021). Detects reflected, stored, and DOM-based XSS in JavaScript/TypeScript, React, Vue, Angular, Python/Django/Jinja2, PHP, Ruby/ERB, and Go html/template. Zero external dependencies — pure Python stdlib only.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - security
  - xss
  - owasp
  - static-analysis
  - javascript
  - python
  - php
  - vulnerability
---

# phy-xss-audit — XSS Vulnerability Static Scanner

Scans source code for **Cross-Site Scripting (XSS)** vulnerabilities across 10 checks covering server-side rendering, client-side DOM manipulation, and framework-specific patterns. Maps to **OWASP A03:2021 — Injection** and **CWE-79**.

## Quick Start

```bash
# Scan entire project
python3 ~/.claude/skills/phy-xss-audit/scripts/xss_audit.py .

# Scan single file
python3 ~/.claude/skills/phy-xss-audit/scripts/xss_audit.py src/components/Post.tsx

# CI mode — exits 1 on any CRITICAL or HIGH finding
python3 ~/.claude/skills/phy-xss-audit/scripts/xss_audit.py . --ci

# JSON output (for SARIF pipelines)
python3 ~/.claude/skills/phy-xss-audit/scripts/xss_audit.py . --format json

# GitHub Actions annotations
python3 ~/.claude/skills/phy-xss-audit/scripts/xss_audit.py . --format github

# Run only one check
python3 ~/.claude/skills/phy-xss-audit/scripts/xss_audit.py . --check XV003
```

## The 10 Checks

| ID | Severity | Title | CWE | Languages |
|----|----------|-------|-----|-----------|
| XV001 | HIGH | innerHTML / outerHTML with user data | CWE-79 | JS/TS/Vue/HTML |
| XV002 | HIGH | document.write() with user data | CWE-79 | JS/TS/HTML |
| XV003 | **CRITICAL** | eval() / setTimeout(string) with user data | CWE-95 | JS/TS/Vue |
| XV004 | HIGH | dangerouslySetInnerHTML without DOMPurify | CWE-79 | React JSX/TSX |
| XV005 | **CRITICAL** | Django mark_safe() / autoescape off | CWE-79 | Python/HTML |
| XV006 | **CRITICAL** | Jinja2 \| safe filter or Markup() bypass | CWE-79 | Python/HTML |
| XV007 | HIGH | PHP echo/print without htmlspecialchars | CWE-79 | PHP |
| XV008 | HIGH | ERB raw / html_safe without sanitize | CWE-79 | Ruby/ERB |
| XV009 | HIGH | Vue v-html with dynamic expression | CWE-79 | Vue |
| XV010 | HIGH | Angular bypassSecurityTrust / Go template.HTML cast | CWE-79 | TS/Go |

## Pass / Partial / Fail Criteria

### XV001 — innerHTML / outerHTML with user data
- **FAIL (HIGH)**: `element.innerHTML =` or `.html()` (jQuery) where user-controlled data (`req.query`, `req.body`, `request.GET`, `location.search`, etc.) flows in within ±20 lines, and no `DOMPurify.sanitize()` guard nearby.
- **PASS**: Sanitized with `DOMPurify.sanitize(input)` before assignment, or data source is internal/static only.

### XV002 — document.write() with user data
- **FAIL (HIGH)**: `document.write()` or `document.writeln()` with user-controlled data in nearby lines.
- **PASS**: `document.write()` only writes developer-controlled static strings (no user input path).

### XV003 — eval() / setTimeout(string) with user data
- **FAIL (CRITICAL)**: `eval(userVar)`, `setTimeout(userVar + "...")`, or `new Function(...)` with user data in the argument. Skipped in test/spec files.
- **PASS**: `eval()` used only with static strings (JSON schemas, etc.), or user data passed via safe JSON.parse().

### XV004 — dangerouslySetInnerHTML without DOMPurify
- **FAIL (HIGH)**: React component uses `dangerouslySetInnerHTML={{ __html: ... }}` without `DOMPurify.sanitize()` wrapping the value within 5 lines.
- **PASS**: Value is `DOMPurify.sanitize(html)` — pattern `DOMPurify.sanitize(` appears within ±5 lines.

### XV005 — Django mark_safe() / autoescape off
- **FAIL (CRITICAL)**: `mark_safe(user_data)` where user-controlled data flows in ±10 lines. Also fires on `{% autoescape off %}` in any template.
- **PASS**: `mark_safe()` only wraps developer-defined static HTML strings, or data is sanitized with `bleach.clean()` first.

### XV006 — Jinja2 | safe filter or Markup() bypass
- **FAIL (CRITICAL)**: Template variable piped through `| safe` or wrapped in `Markup()` when user-controlled data is nearby within ±10 lines.
- **PASS**: `| safe` used only on developer-controlled content (e.g., static site generator output with no user input).

### XV007 — PHP echo/print without htmlspecialchars
- **FAIL (HIGH)**: `echo $_GET['key']` or `echo $var` without `htmlspecialchars()` / `htmlentities()` / `strip_tags()` / `filter_input()` on the same line.
- **PASS**: All user input wrapped with `htmlspecialchars($var, ENT_QUOTES, 'UTF-8')` before output.

### XV008 — ERB raw / html_safe without sanitize
- **FAIL (HIGH)**: `<%== user_var %>`, `user_var.html_safe`, or `raw user_var` in ERB templates where user input flows in ±10 lines, with no `sanitize()` or `strip_tags()` guard nearby.
- **PASS**: Output uses `h(var)` / `escape_html()`, or `sanitize()` wraps the user value.

### XV009 — Vue v-html with dynamic expression
- **FAIL (HIGH)**: `v-html="someVar"` where the value is dynamic and no `DOMPurify.sanitize()` appears in the surrounding 10 lines.
- **PASS**: Value is computed through `DOMPurify.sanitize(rawHtml)` before being bound to `v-html`.

### XV010 — Angular bypassSecurityTrust / Go template.HTML cast
- **FAIL (HIGH)**: Angular `bypassSecurityTrustHtml(userVar)` or `bypassSecurityTrustScript(userVar)` where user data flows nearby. Go: `template.HTML(userStr)` or `template.JS(userStr)` cast with user-controlled input.
- **PASS**: Angular — no bypass called; use standard `[innerHTML]` binding. Go — let `html/template` handle escaping automatically (never cast user strings to `template.HTML`).

## XSS Types Covered

| XSS Type | Checks |
|----------|--------|
| **Reflected XSS** | XV001, XV002, XV005, XV006, XV007 |
| **Stored XSS** | XV001, XV004, XV008, XV009 |
| **DOM-based XSS** | XV001, XV002, XV003 |
| **Server-Side Template Injection → XSS** | XV005, XV006 |
| **Framework bypass XSS** | XV004, XV009, XV010 |

## Supported Languages and Frameworks

| Language | Framework | Checks |
|----------|-----------|--------|
| JavaScript / TypeScript | Vanilla, React, Vue, Angular | XV001–XV004, XV009, XV010 |
| Python | Django, Jinja2 (Flask/FastAPI) | XV005, XV006 |
| PHP | Vanilla, WordPress | XV007 |
| Ruby | Rails, Sinatra | XV008 |
| Go | html/template, Gin | XV010 |

## Taint Source Patterns (User-Controlled Data)

The scanner considers a value "user-controlled" if the surrounding ±15-20 lines contain:

```
req.query / req.body / req.params / req.headers       (Node.js/Express)
request.GET / request.POST / request.args / request.json  (Django/Flask)
params[ / query_params[ / @query_params               (Rails/FastAPI)
$_GET[ / $_POST[ / $_REQUEST[ / $_COOKIE[             (PHP)
location.search / location.hash / URLSearchParams(    (Browser DOM)
c.Query( / c.Param( / r.URL.Query(                    (Go Gin/stdlib)
```

## Sanitization Guards (Auto-Suppression)

These patterns near a sink suppress the finding:

| Guard | Context |
|-------|---------|
| `DOMPurify.sanitize(` | DOM XSS in JS/TS/Vue |
| `sanitize_html(` | Python bleach-based |
| `bleach.clean(` | Python Django |
| `htmlspecialchars(` | PHP |
| `htmlentities(` | PHP |
| `h(` / `html_escape(` | Rails ERB |
| `sanitize(` | Rails, Vue |
| `xss.filterXSS(` | Node.js xss library |
| `escape(` | Various |
| `strip_tags(` | PHP / Rails |

## CI Integration

```yaml
# GitHub Actions
- name: XSS audit
  run: python3 scripts/xss_audit.py . --format github --ci

# GitLab CI
xss-audit:
  script:
    - python3 scripts/xss_audit.py . --ci
  allow_failure: false
```

```bash
# Pre-commit hook
#!/bin/sh
python3 ~/.claude/skills/phy-xss-audit/scripts/xss_audit.py . --ci
```

## Example Output

```
======================================================================
  phy-xss-audit — XSS Vulnerability Report
======================================================================
  Total: 3  |  Critical: 1  |  High: 2
======================================================================

🔴 [XV005] CRITICAL — Django mark_safe() / autoescape off (CWE-79)
   File : app/views.py:47
   Code : return mark_safe(request.GET.get('content', ''))
   Fix  : Never call mark_safe() on user input. Use bleach.clean() first.

🟠 [XV001] HIGH — innerHTML / outerHTML with user data (CWE-79)
   File : src/components/Comment.tsx:23
   Code : el.innerHTML = comment.body
   Fix  : Sanitize with DOMPurify.sanitize(userInput) before innerHTML.

🟠 [XV004] HIGH — dangerouslySetInnerHTML without DOMPurify (CWE-79)
   File : src/components/Post.jsx:61
   Code : dangerouslySetInnerHTML={{ __html: post.content }}
   Fix  : dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(post.content) }}
```

## OWASP Coverage

This skill covers **OWASP A03:2021 — Injection** (XSS vector).

| OWASP ID | Description | Checks |
|----------|-------------|--------|
| A03:2021 | Injection — Cross-Site Scripting | XV001–XV010 |

**phy- suite OWASP coverage after this skill:**
- A01 — phy-path-traversal-audit ✅
- A02 — phy-crypto-audit ✅
- A03 — **phy-xss-audit** ✅ ← this skill
- A04 — phy-cors-audit ✅
- A05 — phy-security-headers ✅
- A06 — phy-dep-upgrade ✅
- A07 — phy-session-audit ✅
- A08 — phy-deserialization-audit ✅
- A09 — phy-otel-audit ✅ (observability/logging)
- A10 — phy-ssrf-audit ✅

**Full OWASP Top 10 coverage achieved.**

## Companion Skills

| Skill | Relationship |
|-------|-------------|
| `phy-cors-audit` | CORS misconfig → OWASP A04 |
| `phy-session-audit` | Cookie/session security → OWASP A07 |
| `phy-ssrf-audit` | Server-side request forgery → OWASP A10 |
| `phy-crypto-audit` | Weak cryptography → OWASP A02 |
| `phy-security-headers` | Missing CSP headers that mitigate XSS |

## Technical Notes

- **Zero external dependencies** — pure Python 3 stdlib (`re`, `pathlib`, `argparse`, `json`)
- **Skips**: `.git/`, `node_modules/`, `__pycache__/`, `dist/`, `build/`, `.venv/`
- **Encodings**: tries `utf-8` first, falls back to `latin-1`
- **XV003** (eval) skips files named `*.test.js` / `*.spec.ts` to reduce test utility false positives
- **Proximity window**: user input must be within ±10–20 lines of the dangerous sink (configurable per check)
- **False positive mitigation**: sanitizer guards auto-suppress findings when detected near the sink

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
