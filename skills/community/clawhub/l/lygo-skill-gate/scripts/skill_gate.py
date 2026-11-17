#!/usr/bin/env python3
"""
LYGO Skill Gate — local pre-install / pre-run skill risk scanner.

Scan any skill folder (SKILL.md + scripts) before you install or trust it.
Pure stdlib. No network. No subprocess. No auto-install.

Detects:
  - network / urllib / requests / sockets
  - subprocess / os.system / shell / Popen
  - secret-looking patterns in code
  - permission claims vs code surface mismatch
  - eval/exec, base64 decode payloads, webhook/exfil hints
  - missing SECURITY.md / overbroad triggers

Signature: Delta9Phi963-SKILL-GATE-v1.0.0
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIG = "Delta9Phi963-SKILL-GATE-v1.0.0"
VERSION = "1.0.0"
HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
STATE = SKILL_ROOT / "state"

SKIP_DIRS = {
    "__pycache__",
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "ollama_results",
    "results",
    "logs",
    "workspace",
}
TEXT_EXTS = {
    ".py",
    ".md",
    ".json",
    ".txt",
    ".yml",
    ".yaml",
    ".ps1",
    ".sh",
    ".bat",
    ".js",
    ".ts",
    ".toml",
    ".cfg",
    ".ini",
}

# (id, severity 1-5, regex, why) — match *code use*, not documentation strings
CODE_RULES: list[tuple[str, int, re.Pattern[str], str]] = [
    ("subprocess_import", 5, re.compile(r"^\s*(import\s+subprocess\b|from\s+subprocess\s+import\b)"), "Can spawn OS processes"),
    ("os_system", 5, re.compile(r"(?<![\"'])\bos\.system\s*\("), "Shell execution via os.system"),
    ("popen", 5, re.compile(r"(?<![\"'])\bsubprocess\.(Popen|run|call|check_output)\s*\("), "Subprocess launch"),
    ("shell_true", 4, re.compile(r"(?<![\"'])shell\s*=\s*True"), "Shell=True expands injection risk"),
    ("eval_exec", 5, re.compile(r"(?<![\w\"'])\b(eval|exec)\s*\("), "Dynamic code execution"),
    ("urllib", 3, re.compile(r"^\s*(import\s+urllib|from\s+urllib\s+import|from\s+urllib\.)"), "HTTP via urllib import"),
    ("urlopen_call", 3, re.compile(r"(?<![\"'])\burlopen\s*\("), "HTTP urlopen call"),
    ("requests_lib", 3, re.compile(r"^\s*(import\s+requests\b|from\s+requests\s+import\b)"), "HTTP client library"),
    ("requests_call", 3, re.compile(r"(?<![\"'])\brequests\.(get|post|put|delete)\s*\("), "HTTP requests call"),
    ("socket", 4, re.compile(r"^\s*(import\s+socket\b|from\s+socket\s+import\b)"), "Raw network sockets"),
    ("webbrowser", 2, re.compile(r"(?<![\"'])\bwebbrowser\.open\s*\("), "Opens system browser"),
    ("pickle", 4, re.compile(r"(?<![\"'])\bpickle\.(loads|load)\s*\("), "Unsafe deserialization"),
    ("yaml_unsafe", 3, re.compile(r"(?<![\"'])\byaml\.load\s*\("), "yaml.load (prefer safe_load)"),
    ("base64_decode", 2, re.compile(r"(?<![\"'])\b(b64decode|base64\.b64decode)\s*\("), "Often used to hide payloads"),
    ("webhook_url", 4, re.compile(r"discord\.com/api/webhooks|hooks\.slack\.com"), "Possible outbound exfil channel URL"),
    ("env_harvest", 2, re.compile(r"(?<![\"'])\bos\.environ\b|(?<![\"'])\bgetenv\s*\("), "Reads environment (may include secrets)"),
    ("hardcoded_secret", 5, re.compile(r"\bsk-[A-Za-z0-9]{20,}\b|\bghp_[A-Za-z0-9]{20,}\b|\bAKIA[0-9A-Z]{16}\b"), "Looks like a live API/token secret in source"),
    ("password_literal", 4, re.compile(r"(?i)(password|api_key|secret)\s*=\s*['\"][^'\"]{8,}['\"]"), "Hardcoded credential-like string"),
    ("rm_rf", 4, re.compile(r"(?<![\"'])\bshutil\.rmtree\s*\("), "Destructive delete capability"),
    ("git_push", 3, re.compile(r"(?<![\"'])\bgit\s+push\b"), "git push capability"),
]

# Docs/markdown only — softer signals
DOC_RULES: list[tuple[str, int, re.Pattern[str], str]] = [
    # Only flag affirmative enablement language, not "no auto-publish" denials
    ("doc_auto_publish_enable", 2, re.compile(r"(?i)(enable|allows?|will)\s+auto[_-]?publish"), "Docs suggest enabling auto-publish"),
]

CODE_EXTS = {".py", ".ps1", ".sh", ".bat", ".js", ".ts", ".mjs", ".cjs"}

FRONTMATTER_CLAIM_KEYS = (
    "network",
    "subprocess",
    "shell",
    "filesystem",
    "publish",
    "permissions",
)


@dataclass
class Finding:
    rule_id: str
    severity: int
    path: str
    line: int
    snippet: str
    why: str


@dataclass
class ScanReport:
    ok: bool
    signature: str = SIG
    version: str = VERSION
    scanned_utc: str = ""
    skill_path: str = ""
    skill_name: str = ""
    skill_version: str = ""
    files_scanned: int = 0
    risk_score: int = 0
    risk_band: str = "unknown"
    findings: list[dict[str, Any]] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)
    claims: dict[str, Any] = field(default_factory=dict)
    mismatches: list[str] = field(default_factory=list)
    plain_english: str = ""
    recommendation: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_frontmatter(skill_md: str) -> dict[str, Any]:
    if not skill_md.startswith("---"):
        return {}
    parts = skill_md.split("---", 2)
    if len(parts) < 3:
        return {}
    meta: dict[str, Any] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k in ("name", "description", "version", "license"):
            meta[k] = v
        if k == "description":
            meta["description"] = v
    # crude permissions block detection
    lower = skill_md.lower()
    meta["claims_network_false"] = bool(
        re.search(r"network:\s*false|permissions:[\s\S]{0,200}network:\s*false", lower)
    )
    meta["claims_subprocess_false"] = bool(
        re.search(r"subprocess:\s*false|no subprocess", lower)
    )
    meta["claims_no_publish"] = bool(
        re.search(r"publish:\s*false|no auto.?publish|no_auto_publish", lower)
    )
    meta["claims_local_first"] = "local" in lower and ("stdlib" in lower or "local-first" in lower or "local first" in lower)
    return meta


def iter_skill_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() not in TEXT_EXTS and p.name not in ("SKILL.md", "claw.json", "LICENSE"):
            continue
        # skip huge
        try:
            if p.stat().st_size > 2_000_000:
                continue
        except OSError:
            continue
        files.append(p)
    return files


def _is_comment_or_doc_noise(line: str, ext: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if ext == ".py":
        if s.startswith("#"):
            return True
        # skip pure string / pattern table rows in scanners
        if s.startswith(("r\"", "r'", "\"", "'", "(", "re.compile")):
            return True
    if ext in {".ps1"} and s.startswith("#"):
        return True
    if ext in {".sh"} and s.startswith("#"):
        return True
    return False


def scan_text(path: Path, text: str, findings: list[Finding], *, code: bool) -> None:
    ext = path.suffix.lower()
    rules = CODE_RULES if code else DOC_RULES
    for i, line in enumerate(text.splitlines(), 1):
        if code and _is_comment_or_doc_noise(line, ext):
            continue
        for rule_id, sev, rx, why in rules:
            if rx.search(line):
                findings.append(
                    Finding(
                        rule_id=rule_id,
                        severity=sev,
                        path=str(path.as_posix()),
                        line=i,
                        snippet=line.strip()[:160],
                        why=why,
                    )
                )


def scan_python_ast(path: Path, text: str, findings: list[Finding]) -> None:
    """Extra AST checks for import subprocess / eval."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in ("subprocess", "socket", "ctypes"):
                    findings.append(
                        Finding(
                            "ast_import_" + alias.name.split(".")[0],
                            5 if alias.name.startswith("subprocess") else 4,
                            str(path.as_posix()),
                            getattr(node, "lineno", 0),
                            f"import {alias.name}",
                            f"AST import of {alias.name}",
                        )
                    )
        if isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split(".")[0]
            if root in ("subprocess", "socket"):
                findings.append(
                    Finding(
                        "ast_from_" + root,
                        5 if root == "subprocess" else 4,
                        str(path.as_posix()),
                        getattr(node, "lineno", 0),
                        f"from {node.module} import ...",
                        f"AST from-import of {root}",
                    )
                )
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
            findings.append(
                Finding(
                    "ast_eval_exec",
                    5,
                    str(path.as_posix()),
                    getattr(node, "lineno", 0),
                    node.func.id + "(...)",
                    "AST eval/exec call",
                )
            )


def risk_band(score: int) -> str:
    if score >= 40:
        return "critical"
    if score >= 25:
        return "high"
    if score >= 12:
        return "elevated"
    if score >= 5:
        return "low"
    return "clear"


def recommendation(band: str, mismatches: list[str]) -> str:
    if band in ("critical", "high"):
        return "DO_NOT_INSTALL — review findings; sandbox only if you fully understand every hit"
    if band == "elevated" or mismatches:
        return "REVIEW_FIRST — read flagged files; enable only features you need"
    if band == "low":
        return "PROCEED_WITH_EYES_OPEN — minor signals; still skim SECURITY.md"
    return "LOOKS_CLEAN — still treat third-party skills as untrusted code"


def scan_skill(path: str | Path) -> ScanReport:
    root = Path(path).expanduser().resolve()
    report = ScanReport(ok=False, scanned_utc=utc_now(), skill_path=str(root))
    if not root.is_dir():
        report.plain_english = f"Not a directory: {root}"
        report.recommendation = "NEED_SKILL_DIR"
        return report

    skill_md_path = root / "SKILL.md"
    if not skill_md_path.is_file():
        report.plain_english = "No SKILL.md — not a valid skill package root"
        report.recommendation = "NEED_SKILL_MD"
        report.risk_score = 15
        report.risk_band = "elevated"
        return report

    skill_text = skill_md_path.read_text(encoding="utf-8", errors="replace")
    claims = parse_frontmatter(skill_text)
    report.claims = claims
    report.skill_name = claims.get("name") or root.name
    report.skill_version = claims.get("version") or ""

    findings: list[Finding] = []
    files = iter_skill_files(root)
    report.files_scanned = len(files)

    for fp in files:
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = fp.relative_to(root)
        is_code = fp.suffix.lower() in CODE_EXTS
        scan_text(rel, text, findings, code=is_code)
        if fp.suffix == ".py":
            scan_python_ast(rel, text, findings)

    # structural checks
    if not (root / "references" / "SECURITY.md").is_file() and not (root / "SECURITY.md").is_file():
        findings.append(
            Finding(
                "missing_security_md",
                2,
                "references/SECURITY.md",
                0,
                "(missing)",
                "No SECURITY.md — weaker operator disclosure",
            )
        )

    # claim vs code mismatches
    mismatches: list[str] = []
    has_sub = any(
        f.rule_id
        in (
            "subprocess_import",
            "os_system",
            "popen",
            "shell_true",
            "ast_import_subprocess",
            "ast_from_subprocess",
        )
        for f in findings
    )
    has_net = any(
        f.rule_id
        in (
            "urllib",
            "urlopen_call",
            "requests_lib",
            "requests_call",
            "socket",
            "ast_import_socket",
            "webhook_url",
        )
        for f in findings
    )
    if claims.get("claims_subprocess_false") and has_sub:
        mismatches.append("Claims no subprocess but code imports/spawns processes")
    if claims.get("claims_network_false") and has_net:
        mismatches.append("Claims no network but code has HTTP/socket/webhook surface")
    if claims.get("claims_no_publish") and any(f.rule_id in ("git_push", "auto_publish") for f in findings):
        mismatches.append("Claims no publish but code mentions push/auto-publish")

    # score (cap multi-hits per rule)
    by_rule: dict[str, list[Finding]] = {}
    for f in findings:
        by_rule.setdefault(f.rule_id, []).append(f)
    score = 0
    for rule_id, items in by_rule.items():
        sev = items[0].severity
        # first hit full, extras discounted
        score += sev * 3
        score += min(4, len(items) - 1) * sev
    score += len(mismatches) * 8
    score = min(100, score)

    band = risk_band(score)
    # unique findings for report (limit noise)
    finding_dicts = []
    seen_keys: set[str] = set()
    for f in sorted(findings, key=lambda x: (-x.severity, x.path, x.line)):
        key = f"{f.rule_id}:{f.path}:{f.line}"
        if key in seen_keys:
            continue
        seen_keys.add(key)
        finding_dicts.append(asdict(f))
        if len(finding_dicts) >= 80:
            break

    counts: dict[str, int] = {}
    for f in findings:
        counts[f.rule_id] = counts.get(f.rule_id, 0) + 1

    report.ok = True
    report.risk_score = score
    report.risk_band = band
    report.findings = finding_dicts
    report.summary = {
        "finding_count": len(findings),
        "unique_rules": len(counts),
        "rule_counts": dict(sorted(counts.items(), key=lambda kv: -kv[1])[:20]),
        "has_subprocess_signals": has_sub,
        "has_network_signals": has_net,
        "mismatches": len(mismatches),
    }
    report.mismatches = mismatches
    report.recommendation = recommendation(band, mismatches)
    report.plain_english = (
        f"Skill **{report.skill_name}** v{report.skill_version or '?'} — "
        f"risk **{band}** (score {score}/100), {len(findings)} signals across {len(files)} files. "
        + (
            f"Claim mismatches: {'; '.join(mismatches)}. "
            if mismatches
            else "No permission-claim mismatches detected. "
        )
        + f"Recommendation: {report.recommendation}."
    )
    return report


def resolve_skill_path(raw: str) -> Path:
    p = Path(raw).expanduser()
    if p.is_dir():
        return p
    # try common roots
    candidates = [
        Path(r"I:\E Drive\.grok\skills") / raw,
        Path.home() / ".grok" / "skills" / raw,
        Path(r"D:\lygo-protocol-stack\clawhub\mirrors") / raw,
        Path.cwd() / raw,
    ]
    for c in candidates:
        if c.is_dir() and (c / "SKILL.md").is_file():
            return c
    return p


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="lygo-skill-gate",
        description="LYGO Skill Gate — local pre-install skill risk scanner",
    )
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("scan", help="Scan a skill directory or slug")
    p.add_argument("path", help="Path to skill folder or slug under .grok/skills")
    p.add_argument("--json", action="store_true", help="JSON only")
    p.add_argument("--write", default="", help="Write report under skill state/ (needs --i-consent)")
    p.add_argument("--i-consent", action="store_true")

    sub.add_parser("version")
    sub.add_parser("self-demo", help="Scan this skill package (self)")

    args = ap.parse_args(argv)
    cmd = args.cmd or "version"

    if cmd == "version":
        print(
            json.dumps(
                {
                    "ok": True,
                    "signature": SIG,
                    "version": VERSION,
                    "plain_english": "Scan skills before install. Local only. No network.",
                },
                indent=2,
            )
        )
        return 0

    if cmd == "self-demo":
        target = SKILL_ROOT
    elif cmd == "scan":
        target = resolve_skill_path(args.path)
    else:
        print(json.dumps({"ok": False, "error": "need scan|self-demo|version"}))
        return 2

    report = scan_skill(target)
    data = report.to_dict()

    if cmd == "scan" and args.write:
        if not args.i_consent:
            data["written"] = False
            data["hint"] = "pass --i-consent with --write"
        else:
            outp = Path(args.write)
            if not outp.is_absolute():
                outp = STATE / outp.name
            try:
                outp.resolve().relative_to(STATE.resolve())
            except ValueError:
                data["written"] = False
                data["error"] = "write_must_be_under_skill_state"
            else:
                STATE.mkdir(parents=True, exist_ok=True)
                outp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
                data["written"] = True
                data["path"] = str(outp.resolve())

    print(json.dumps(data, indent=2))
    # human footer
    if not (cmd == "scan" and args.json):
        print("\n" + report.plain_english)

    if report.risk_band in ("critical", "high"):
        return 10
    if report.risk_band == "elevated" or report.mismatches:
        return 5
    if not report.ok:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
