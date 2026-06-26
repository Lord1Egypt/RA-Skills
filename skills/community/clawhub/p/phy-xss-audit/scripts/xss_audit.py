#!/usr/bin/env python3
"""
phy-xss-audit — XSS vulnerability static scanner (OWASP A03:2021)
Detects reflected, stored, and DOM-based XSS patterns in server-side
and client-side source code without any external dependencies.
"""
from __future__ import annotations
import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# ── Check IDs and metadata ────────────────────────────────────────────────────

CHECKS = {
    "XV001": ("innerHTML / outerHTML with user data",      "HIGH",     "CWE-79"),
    "XV002": ("document.write() with user data",           "HIGH",     "CWE-79"),
    "XV003": ("eval() / setTimeout(string) with user data","CRITICAL", "CWE-95"),
    "XV004": ("dangerouslySetInnerHTML without DOMPurify", "HIGH",     "CWE-79"),
    "XV005": ("Django mark_safe() / autoescape off",       "CRITICAL", "CWE-79"),
    "XV006": ("Jinja2 | safe filter or Markup() bypass",   "CRITICAL", "CWE-79"),
    "XV007": ("PHP echo/print without htmlspecialchars",   "HIGH",     "CWE-79"),
    "XV008": ("ERB raw / html_safe without sanitize",      "HIGH",     "CWE-79"),
    "XV009": ("Vue v-html with dynamic expression",        "HIGH",     "CWE-79"),
    "XV010": ("Angular bypassSecurityTrust / Go template.HTML cast", "HIGH", "CWE-79"),
}

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}

# ── Extensions to scan ────────────────────────────────────────────────────────

LANG_EXTENSIONS: dict[str, list[str]] = {
    "js_ts":  [".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"],
    "python": [".py"],
    "php":    [".php"],
    "ruby":   [".rb", ".erb"],
    "go":     [".go", ".html"],   # Go templates embedded in html
    "vue":    [".vue"],
    "java":   [".java", ".jsp", ".html"],
    "html":   [".html", ".htm"],
}

ALL_EXTENSIONS: set[str] = set(e for exts in LANG_EXTENSIONS.values() for e in exts)

# ── User-input source patterns (taint sources) ───────────────────────────────

USER_INPUT_RE = re.compile(
    r"req\.(query|body|params|headers)\b"
    r"|request\.(GET|POST|args|form|data|json|headers)\b"
    r"|params\[|query_params\[|\$_GET\[|\$_POST\[|\$_REQUEST\["
    r"|@query_params\.|request\.params\b"
    r"|c\.Query\(|c\.Param\(|r\.URL\.Query\("      # Go Gin / stdlib
    r"|ctx\.Query\(|ctx\.Param\("                  # Go Fiber / Echo
    r"|location\.(search|hash)\b|URLSearchParams\("
    r"|getParameter\(|getAttribute\("
    r"|window\.location\b",
    re.IGNORECASE,
)

# Sanitization guards — if present near a sink, suppress the finding
SANITIZE_RE = re.compile(
    r"DOMPurify\.sanitize\("
    r"|sanitize_html\("
    r"|bleach\.clean\("
    r"|xss\.filterXSS\("
    r"|htmlspecialchars\("
    r"|htmlentities\("
    r"|h\s*\("           # Rails h() / html_escape()
    r"|html_escape\("
    r"|escape\s*\("
    r"|sanitize\s*\("
    r"|markdownSanitizer"
    r"|purify\(",
    re.IGNORECASE,
)

# ── Per-check patterns ────────────────────────────────────────────────────────

# XV001 — innerHTML / outerHTML
INNER_HTML_SINK_RE = re.compile(
    r"\binnerHTML\s*[+]?=|outerHTML\s*[+]?=|insertAdjacentHTML\s*\(",
)
JQUERY_HTML_RE = re.compile(r"\$\([^)]+\)\.html\(")

# XV002 — document.write
DOC_WRITE_RE = re.compile(r"document\.write\s*\(|document\.writeln\s*\(")

# XV003 — eval / code execution with strings
EVAL_SINK_RE = re.compile(
    r"\beval\s*\(|\bFunction\s*\("
    r"|setTimeout\s*\(\s*['\"`]|setInterval\s*\(\s*['\"`]"
    r"|setTimeout\s*\(\s*\w+\s*\+|setInterval\s*\(\s*\w+\s*\+"
)

# XV004 — React dangerouslySetInnerHTML
DANGEROUS_RE = re.compile(r"dangerouslySetInnerHTML\s*=\s*\{")
DOMPURIFY_NEARBY_RE = re.compile(r"DOMPurify\.sanitize\(")

# XV005 — Django mark_safe / autoescape off
MARK_SAFE_RE = re.compile(r"\bmark_safe\s*\(")
AUTOESCAPE_OFF_RE = re.compile(r"\{%\s*autoescape\s+off\s*%\}")

# XV006 — Jinja2 | safe or Markup()
JINJA_SAFE_RE = re.compile(r"\|\s*safe\b")
MARKUP_RE = re.compile(r"\bMarkup\s*\(")

# XV007 — PHP echo/print without htmlspecialchars
PHP_ECHO_RE = re.compile(
    r"\becho\s+\$_(GET|POST|REQUEST|COOKIE)\["
    r"|\becho\s+\$\w+(?!\s*=)"   # echo $var (not assignment)
    r"|\bprint\s+\$_(GET|POST|REQUEST)\["
)

# XV008 — ERB raw / html_safe
ERB_RAW_RE = re.compile(r"<%==|\.html_safe\b|raw\s+@?\w+")
RAILS_SANITIZE_RE = re.compile(r"sanitize\s*\(|strip_tags\(")

# XV009 — Vue v-html
VHTML_RE = re.compile(r'v-html\s*=\s*["\']?\s*\w')

# XV010 — Angular bypassSecurityTrust / Go template.HTML cast
BYPASS_TRUST_RE = re.compile(
    r"bypassSecurityTrustHtml\s*\("
    r"|bypassSecurityTrustScript\s*\("
    r"|bypassSecurityTrustUrl\s*\("
    r"|bypassSecurityTrustStyle\s*\("
    r"|bypassSecurityTrustResourceUrl\s*\("
)
GO_TEMPLATE_HTML_RE = re.compile(r"template\.HTML\s*\(|template\.JS\s*\(|template\.URL\s*\(")

# ── Finding dataclass ─────────────────────────────────────────────────────────

@dataclass
class Finding:
    check_id: str
    severity: str
    cwe: str
    message: str
    file: str
    line: int
    snippet: str
    fix: str

# ── Helper: read lines safely ─────────────────────────────────────────────────

def read_lines(path: Path) -> list[str]:
    for enc in ("utf-8", "latin-1"):
        try:
            return path.read_text(encoding=enc).splitlines()
        except Exception:
            pass
    return []

def context_window(lines: list[str], center: int, radius: int = 15) -> str:
    """Return joined lines in [center-radius, center+radius]."""
    start = max(0, center - radius)
    end = min(len(lines), center + radius + 1)
    return "\n".join(lines[start:end])

def has_user_input_nearby(lines: list[str], center: int, radius: int = 20) -> bool:
    window = context_window(lines, center, radius)
    return bool(USER_INPUT_RE.search(window))

def has_sanitizer_nearby(lines: list[str], center: int, radius: int = 10) -> bool:
    window = context_window(lines, center, radius)
    return bool(SANITIZE_RE.search(window))

def is_test_file(path: Path) -> bool:
    name = path.name.lower()
    parents = {p.name.lower() for p in path.parents}
    return (
        "test" in name or "spec" in name or "mock" in name
        or "fixture" in name or "example" in name
        or "tests" in parents or "spec" in parents or "__tests__" in parents
    )

# ── Check implementations ─────────────────────────────────────────────────────

def check_xv001(path: Path, lines: list[str], findings: list[Finding]) -> None:
    """innerHTML / outerHTML / jQuery.html() with user data."""
    ext = path.suffix.lower()
    if ext not in (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".html"):
        return
    for i, line in enumerate(lines):
        if not (INNER_HTML_SINK_RE.search(line) or JQUERY_HTML_RE.search(line)):
            continue
        if not has_user_input_nearby(lines, i):
            continue
        if has_sanitizer_nearby(lines, i):
            continue
        sink = "jQuery .html()" if JQUERY_HTML_RE.search(line) else "innerHTML/outerHTML"
        findings.append(Finding(
            check_id="XV001", severity="HIGH", cwe="CWE-79",
            message=f"{sink} assignment with user-controlled data — reflected/stored XSS risk",
            file=str(path), line=i + 1,
            snippet=line.strip()[:120],
            fix="Sanitize with DOMPurify.sanitize(userInput) before assigning to innerHTML.",
        ))

def check_xv002(path: Path, lines: list[str], findings: list[Finding]) -> None:
    """document.write() with user data."""
    ext = path.suffix.lower()
    if ext not in (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".html"):
        return
    for i, line in enumerate(lines):
        if not DOC_WRITE_RE.search(line):
            continue
        if not has_user_input_nearby(lines, i, radius=15):
            continue
        findings.append(Finding(
            check_id="XV002", severity="HIGH", cwe="CWE-79",
            message="document.write() called with user-controlled data — DOM XSS risk",
            file=str(path), line=i + 1,
            snippet=line.strip()[:120],
            fix="Never pass user data to document.write(). Use textContent or DOMPurify instead.",
        ))

def check_xv003(path: Path, lines: list[str], findings: list[Finding]) -> None:
    """eval() / setTimeout(string) with user data — code injection."""
    ext = path.suffix.lower()
    if ext not in (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue"):
        return
    if is_test_file(path):
        return
    for i, line in enumerate(lines):
        if not EVAL_SINK_RE.search(line):
            continue
        if not has_user_input_nearby(lines, i, radius=10):
            continue
        findings.append(Finding(
            check_id="XV003", severity="CRITICAL", cwe="CWE-95",
            message="eval() or setTimeout(string) with user-controlled data — arbitrary code execution",
            file=str(path), line=i + 1,
            snippet=line.strip()[:120],
            fix="Never pass user data to eval(). Use JSON.parse() for data, or pass a function reference to setTimeout.",
        ))

def check_xv004(path: Path, lines: list[str], findings: list[Finding]) -> None:
    """React dangerouslySetInnerHTML without DOMPurify."""
    ext = path.suffix.lower()
    if ext not in (".js", ".jsx", ".ts", ".tsx"):
        return
    for i, line in enumerate(lines):
        if not DANGEROUS_RE.search(line):
            continue
        # Check if DOMPurify is used nearby
        if DOMPURIFY_NEARBY_RE.search(context_window(lines, i, radius=5)):
            continue
        findings.append(Finding(
            check_id="XV004", severity="HIGH", cwe="CWE-79",
            message="dangerouslySetInnerHTML used without DOMPurify.sanitize() guard",
            file=str(path), line=i + 1,
            snippet=line.strip()[:120],
            fix="Wrap the value: dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userHtml) }}",
        ))

def check_xv005(path: Path, lines: list[str], findings: list[Finding]) -> None:
    """Django mark_safe() / autoescape off with user data."""
    ext = path.suffix.lower()
    if ext not in (".py", ".html"):
        return
    for i, line in enumerate(lines):
        if MARK_SAFE_RE.search(line):
            if has_user_input_nearby(lines, i, radius=10):
                findings.append(Finding(
                    check_id="XV005", severity="CRITICAL", cwe="CWE-79",
                    message="Django mark_safe() wraps user-controlled data — stored/reflected XSS",
                    file=str(path), line=i + 1,
                    snippet=line.strip()[:120],
                    fix="Never call mark_safe() on user input. Use Django's template auto-escaping or bleach.clean().",
                ))
        if AUTOESCAPE_OFF_RE.search(line):
            findings.append(Finding(
                check_id="XV005", severity="CRITICAL", cwe="CWE-79",
                message="{% autoescape off %} disables Django's XSS protection for this template block",
                file=str(path), line=i + 1,
                snippet=line.strip()[:120],
                fix="Remove autoescape off. If rich HTML is required, sanitize with bleach before rendering.",
            ))

def check_xv006(path: Path, lines: list[str], findings: list[Finding]) -> None:
    """Jinja2 | safe filter or Markup() wrapping user input."""
    ext = path.suffix.lower()
    if ext not in (".py", ".html", ".jinja", ".jinja2", ".j2"):
        return
    for i, line in enumerate(lines):
        if JINJA_SAFE_RE.search(line):
            if has_user_input_nearby(lines, i, radius=10):
                findings.append(Finding(
                    check_id="XV006", severity="CRITICAL", cwe="CWE-79",
                    message="Jinja2 | safe filter applied to user-controlled variable — disables auto-escaping",
                    file=str(path), line=i + 1,
                    snippet=line.strip()[:120],
                    fix="Remove | safe. Jinja2's auto-escaping handles HTML encoding. Use bleach if rich HTML is needed.",
                ))
        if MARKUP_RE.search(line):
            if has_user_input_nearby(lines, i, radius=10):
                findings.append(Finding(
                    check_id="XV006", severity="CRITICAL", cwe="CWE-79",
                    message="Jinja2 Markup() wraps user input — treats content as safe HTML",
                    file=str(path), line=i + 1,
                    snippet=line.strip()[:120],
                    fix="Do not wrap user input in Markup(). Only use Markup() for trusted, developer-controlled strings.",
                ))

def check_xv007(path: Path, lines: list[str], findings: list[Finding]) -> None:
    """PHP echo/print without htmlspecialchars."""
    if path.suffix.lower() != ".php":
        return
    for i, line in enumerate(lines):
        if not re.search(r"\becho\b|\bprint\b", line):
            continue
        # Skip if line has htmlspecialchars / htmlentities
        if re.search(r"htmlspecialchars|htmlentities|strip_tags|filter_input", line):
            continue
        # Must contain a $_GET/$_POST/$_REQUEST or dynamic variable
        if not re.search(r"\$_(GET|POST|REQUEST|COOKIE)\[|\$\w+", line):
            continue
        # Check for user input in the echo target
        if re.search(r"\$_(GET|POST|REQUEST|COOKIE)\[", line) or has_user_input_nearby(lines, i, radius=5):
            findings.append(Finding(
                check_id="XV007", severity="HIGH", cwe="CWE-79",
                message="PHP echo/print outputs user-controlled data without htmlspecialchars()",
                file=str(path), line=i + 1,
                snippet=line.strip()[:120],
                fix="Wrap output: echo htmlspecialchars($var, ENT_QUOTES, 'UTF-8'); or use a templating engine.",
            ))

def check_xv008(path: Path, lines: list[str], findings: list[Finding]) -> None:
    """ERB raw / html_safe without Rails sanitize()."""
    ext = path.suffix.lower()
    if ext not in (".rb", ".erb", ".html"):
        return
    for i, line in enumerate(lines):
        if not ERB_RAW_RE.search(line):
            continue
        if RAILS_SANITIZE_RE.search(context_window(lines, i, radius=5)):
            continue
        if has_user_input_nearby(lines, i, radius=10):
            findings.append(Finding(
                check_id="XV008", severity="HIGH", cwe="CWE-79",
                message="ERB raw / html_safe outputs user-controlled data without sanitize()",
                file=str(path), line=i + 1,
                snippet=line.strip()[:120],
                fix="Use sanitize(user_html) or h(var) instead of raw/html_safe with user input.",
            ))

def check_xv009(path: Path, lines: list[str], findings: list[Finding]) -> None:
    """Vue v-html with dynamic expression."""
    ext = path.suffix.lower()
    if ext not in (".vue", ".html"):
        return
    for i, line in enumerate(lines):
        if not VHTML_RE.search(line):
            continue
        # Flag all dynamic v-html as suspicious; DOMPurify check nearby suppresses
        if has_sanitizer_nearby(lines, i, radius=10):
            continue
        findings.append(Finding(
            check_id="XV009", severity="HIGH", cwe="CWE-79",
            message="Vue v-html directive with dynamic expression — XSS if data contains user input",
            file=str(path), line=i + 1,
            snippet=line.strip()[:120],
            fix="Sanitize with DOMPurify.sanitize() in the computed property / method feeding v-html.",
        ))

def check_xv010(path: Path, lines: list[str], findings: list[Finding]) -> None:
    """Angular bypassSecurityTrust / Go template.HTML() cast."""
    ext = path.suffix.lower()
    is_go = ext == ".go"
    is_angular = ext in (".ts", ".js")
    if not (is_go or is_angular):
        return
    for i, line in enumerate(lines):
        if BYPASS_TRUST_RE.search(line):
            if has_user_input_nearby(lines, i, radius=10):
                findings.append(Finding(
                    check_id="XV010", severity="HIGH", cwe="CWE-79",
                    message="Angular bypassSecurityTrust* called with user-controlled data — disables Angular's XSS sanitization",
                    file=str(path), line=i + 1,
                    snippet=line.strip()[:120],
                    fix="Never pass user input to bypassSecurityTrust*. Use Angular's built-in [innerHTML] binding which auto-sanitizes.",
                ))
        if is_go and GO_TEMPLATE_HTML_RE.search(line):
            if has_user_input_nearby(lines, i, radius=10):
                findings.append(Finding(
                    check_id="XV010", severity="HIGH", cwe="CWE-79",
                    message="Go template.HTML()/template.JS()/template.URL() cast with user data — bypasses html/template auto-escaping",
                    file=str(path), line=i + 1,
                    snippet=line.strip()[:120],
                    fix="Do not cast user data to template.HTML. Let html/template handle escaping automatically.",
                ))

# ── File dispatcher ───────────────────────────────────────────────────────────

ALL_CHECK_FUNS = [
    check_xv001, check_xv002, check_xv003, check_xv004,
    check_xv005, check_xv006, check_xv007, check_xv008,
    check_xv009, check_xv010,
]

def scan_file(path: Path) -> list[Finding]:
    if path.suffix.lower() not in ALL_EXTENSIONS:
        return []
    lines = read_lines(path)
    if not lines:
        return []
    findings: list[Finding] = []
    for fn in ALL_CHECK_FUNS:
        fn(path, lines, findings)
    return findings

def scan_directory(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__",
                 "dist", "build", ".next", "vendor", "coverage"}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(p in SKIP_DIRS for p in path.parts):
            continue
        findings.extend(scan_file(path))
    return findings

# ── Output formatting ─────────────────────────────────────────────────────────

def severity_icon(s: str) -> str:
    return {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵"}.get(s, "⚪")

def print_findings(findings: list[Finding], fmt: str, ci: bool) -> int:
    findings.sort(key=lambda f: (SEVERITY_ORDER.get(f.severity, 9), f.file, f.line))

    criticals = sum(1 for f in findings if f.severity == "CRITICAL")
    highs     = sum(1 for f in findings if f.severity == "HIGH")

    if fmt == "json":
        out = {
            "total": len(findings),
            "criticals": criticals,
            "highs": highs,
            "findings": [
                {"check": f.check_id, "severity": f.severity, "cwe": f.cwe,
                 "message": f.message, "file": f.file, "line": f.line,
                 "snippet": f.snippet, "fix": f.fix}
                for f in findings
            ],
        }
        print(json.dumps(out, indent=2))
    elif fmt == "github":
        for f in findings:
            lvl = "error" if f.severity in ("CRITICAL", "HIGH") else "warning"
            print(f"::{lvl} file={f.file},line={f.line},title={f.check_id} {f.severity}::"
                  f"{f.message} | Fix: {f.fix}")
    else:
        if not findings:
            print("✅  No XSS vulnerabilities detected.")
        else:
            print(f"\n{'='*70}")
            print(f"  phy-xss-audit — XSS Vulnerability Report")
            print(f"{'='*70}")
            print(f"  Total: {len(findings)}  |  Critical: {criticals}  |  High: {highs}")
            print(f"{'='*70}\n")
            for f in findings:
                icon = severity_icon(f.severity)
                name, _, cwe = CHECKS.get(f.check_id, (f.message, "", f.cwe))
                print(f"{icon} [{f.check_id}] {f.severity} — {name} ({cwe})")
                print(f"   File : {f.file}:{f.line}")
                print(f"   Code : {f.snippet}")
                print(f"   Fix  : {f.fix}\n")

    if ci and (criticals > 0 or highs > 0):
        return 1
    return 0

# ── CLI entry point ───────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        description="phy-xss-audit — XSS vulnerability static scanner (OWASP A03:2021)",
    )
    ap.add_argument("target", nargs="?", default=".",
                    help="File or directory to scan (default: current directory)")
    ap.add_argument("--format", choices=["text", "json", "github"], default="text",
                    help="Output format")
    ap.add_argument("--ci", action="store_true",
                    help="Exit 1 if any CRITICAL or HIGH finding is found")
    ap.add_argument("--check", metavar="ID",
                    help="Run only this check ID (e.g. XV003)")
    args = ap.parse_args()

    target = Path(args.target).resolve()
    if not target.exists():
        print(f"Error: path not found: {target}", file=sys.stderr)
        sys.exit(2)

    if args.check:
        cid = args.check.upper()
        idx_map = {
            "XV001": 0, "XV002": 1, "XV003": 2, "XV004": 3, "XV005": 4,
            "XV006": 5, "XV007": 6, "XV008": 7, "XV009": 8, "XV010": 9,
        }
        if cid not in idx_map:
            print(f"Unknown check ID: {cid}. Valid IDs: {', '.join(idx_map)}", file=sys.stderr)
            sys.exit(2)

    findings = scan_file(target) if target.is_file() else scan_directory(target)

    if args.check:
        findings = [f for f in findings if f.check_id == args.check.upper()]

    rc = print_findings(findings, args.format, args.ci)
    sys.exit(rc)


if __name__ == "__main__":
    main()
