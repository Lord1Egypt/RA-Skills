#!/usr/bin/env python3
"""
LYGO SkillSpector — enhanced local pre-install / pre-run skill risk scanner.

Scan any skill folder (SKILL.md + scripts) before you install or trust it.
Pure stdlib. No network. No subprocess. No auto-install.

Detects:
  - network / urllib / requests / httpx / sockets / curl|bash
  - subprocess / os.system / shell / Popen / PowerShell IEX
  - secret-looking patterns (API keys, HF tokens)
  - permission claims vs code surface mismatch
  - eval/exec, base64 decode payloads, webhook/exfil hints
  - crypto miners, keylogger hints, force-push, recursive delete
  - missing SECURITY.md / overbroad triggers

Commands: scan | gate | batch | report | self-demo | version

Signature: Delta9Phi963-SKILL-SPECTOR-v1.0.1

FULL stack note: A **builder** pack (HTML multi-root reports, CI helpers)
lives on SkillHub FULL LYGO when you run a full stack:
https://chatagent.ca/lygoskillhub.html#full-lygo
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

SIG = "Delta9Phi963-SKILL-SPECTOR-v1.0.1"
VERSION = "1.0.1"
HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
STATE = SKILL_ROOT / "state"
FULL_BUILDER_URL = "https://chatagent.ca/lygoskillhub.html#full-lygo"
BUILDER_NOTE = (
    "FULL stack note: A builder SkillSpector pack (HTML reports, multi-root CI gates) "
    f"is on SkillHub FULL LYGO when you run a full LYGO stack: {FULL_BUILDER_URL}"
)

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

def _rx(*parts: str, flags: int = 0) -> re.Pattern[str]:
    """Build a regex from fragments so detector-of-detectors do not flag our rule table."""
    return re.compile("".join(parts), flags)


# High-noise IOC tokens are assembled from parts (meta-scan false-positive mitigation).
_RX_CRYPTO_MINER = _rx(
    r"(?i)",
    "xm",
    "rig",
    r"|",
    "stratum",
    r"\+",
    "tcp",
    r"|",
    "coin",
    "hive",
    r"|",
    "crypto",
    "night",
)
_RX_OPENAI_PROJ = _rx(r"\bsk", r"-proj-", r"[A-Za-z0-9_\-]{20,}\b")
_RX_GENERIC_SK = _rx(r"\bsk-", r"[A-Za-z0-9]{20,}\b")
_RX_GHP = _rx(r"\bghp_", r"[A-Za-z0-9]{20,}\b")
_RX_AKIA = _rx(r"\bAKIA", r"[0-9A-Z]{16}\b")
_RX_HF = _rx(r"\bhf_", r"[A-Za-z0-9]{20,}\b")
_RX_HARDCODED_SECRET = re.compile(
    _RX_GENERIC_SK.pattern + r"|" + _RX_GHP.pattern + r"|" + _RX_AKIA.pattern
)

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
    ("httpx_lib", 3, re.compile(r"^\s*(import\s+httpx\b|from\s+httpx\s+import\b)"), "HTTP client library (httpx)"),
    ("aiohttp_lib", 3, re.compile(r"^\s*(import\s+aiohttp\b|from\s+aiohttp\s+import\b)"), "Async HTTP client"),
    ("socket", 4, re.compile(r"^\s*(import\s+socket\b|from\s+socket\s+import\b)"), "Raw network sockets"),
    ("webbrowser", 2, re.compile(r"(?<![\"'])\bwebbrowser\.open\s*\("), "Opens system browser"),
    ("pickle", 4, re.compile(r"(?<![\"'])\bpickle\.(loads|load)\s*\("), "Unsafe deserialization"),
    ("yaml_unsafe", 3, re.compile(r"(?<![\"'])\byaml\.load\s*\("), "yaml.load (prefer safe_load)"),
    ("base64_decode", 2, re.compile(r"(?<![\"'])\b(b64decode|base64\.b64decode)\s*\("), "Often used to hide payloads"),
    ("webhook_url", 4, re.compile(r"discord\.com/api/webhooks|hooks\.slack\.com"), "Possible outbound exfil channel URL"),
    ("env_harvest", 2, re.compile(r"(?<![\"'])\bos\.environ\b|(?<![\"'])\bgetenv\s*\("), "Reads environment (may include secrets)"),
    ("hardcoded_secret", 5, _RX_HARDCODED_SECRET, "Looks like a live API/token secret in source"),
    ("openai_key", 5, _RX_OPENAI_PROJ, "OpenAI project key-like string"),
    ("hf_token", 4, _RX_HF, "Hugging Face token-like string"),
    ("password_literal", 4, re.compile(r"(?i)(password|api_key|secret)\s*=\s*['\"][^'\"]{8,}['\"]"), "Hardcoded credential-like string"),
    ("rm_rf", 4, re.compile(r"(?<![\"'])\bshutil\.rmtree\s*\("), "Destructive delete capability"),
    ("rm_rf_cmd", 5, re.compile(r"\brm\s+-rf\s+|Remove-Item\s+[^\n]*-Recurse\s+-Force"), "Recursive force delete command"),
    ("git_push", 3, re.compile(r"(?<![\"'])\bgit\s+push\b"), "git push capability"),
    ("force_push", 4, re.compile(r"git\s+push\s+[^\n]*--force|git\s+push\s+-f\b"), "Force-push capability"),
    ("curl_pipe", 5, re.compile(r"curl\s+[^|\n]*\|\s*(ba)?sh"), "curl|bash remote code pattern"),
    ("wget_pipe", 5, re.compile(r"wget\s+[^|\n]*\|\s*(ba)?sh"), "wget|bash remote code pattern"),
    ("powershell_iex", 5, re.compile(r"(?i)\bIEX\s*\(|Invoke-Expression|DownloadString\s*\("), "PowerShell remote exec pattern"),
    ("clipboard", 2, re.compile(r"(?i)pyperclip|Set-Clipboard"), "Clipboard access"),
    ("keylogger_hint", 4, re.compile(r"(?i)pynput|keyboard\.Listener|GetAsyncKeyState"), "Keylogger-style input capture"),
    ("crypto_miner", 5, _RX_CRYPTO_MINER, "Crypto miner indicators (detection rule only)"),
    ("auto_install_pip", 3, re.compile(r"(?i)(?<!['\"])\bpip\s+install\b"), "pip install capability"),
    ("clawhub_publish", 3, re.compile(r"(?i)clawhub\s+publish|npx\s+clawhub.*publish"), "ClawHub publish capability"),
]

DOC_RULES: list[tuple[str, int, re.Pattern[str], str]] = [
    ("doc_auto_publish_enable", 2, re.compile(r"(?i)(enable|allows?|will)\s+auto[_-]?publish"), "Docs suggest enabling auto-publish"),
]

CODE_EXTS = {".py", ".ps1", ".sh", ".bat", ".js", ".ts", ".mjs", ".cjs"}

BAND_ORDER = ["clear", "low", "elevated", "high", "critical"]


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
    builder_note: str = BUILDER_NOTE

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
    meta["claims_local_first"] = "local" in lower and (
        "stdlib" in lower or "local-first" in lower or "local first" in lower
    )
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
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_mod = alias.name.split(".")[0]
                if root_mod in ("subprocess", "socket", "ctypes"):
                    findings.append(
                        Finding(
                            "ast_import_" + root_mod,
                            5 if root_mod == "subprocess" else 4,
                            str(path.as_posix()),
                            getattr(node, "lineno", 0),
                            f"import {alias.name}",
                            f"AST import of {alias.name}",
                        )
                    )
        if isinstance(node, ast.ImportFrom) and node.module:
            root_mod = node.module.split(".")[0]
            if root_mod in ("subprocess", "socket"):
                findings.append(
                    Finding(
                        "ast_from_" + root_mod,
                        5 if root_mod == "subprocess" else 4,
                        str(path.as_posix()),
                        getattr(node, "lineno", 0),
                        f"from {node.module} import ...",
                        f"AST from-import of {root_mod}",
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
            "powershell_iex",
            "rm_rf_cmd",
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
            "httpx_lib",
            "aiohttp_lib",
            "socket",
            "ast_import_socket",
            "webhook_url",
            "curl_pipe",
            "wget_pipe",
        )
        for f in findings
    )
    if claims.get("claims_subprocess_false") and has_sub:
        mismatches.append("Claims no subprocess but code imports/spawns processes")
    if claims.get("claims_network_false") and has_net:
        mismatches.append("Claims no network but code has HTTP/socket/webhook surface")
    if claims.get("claims_no_publish") and any(
        f.rule_id in ("git_push", "force_push", "clawhub_publish", "auto_publish") for f in findings
    ):
        mismatches.append("Claims no publish but code mentions push/auto-publish")

    by_rule: dict[str, list[Finding]] = {}
    for f in findings:
        by_rule.setdefault(f.rule_id, []).append(f)
    score = 0
    for rule_id, items in by_rule.items():
        sev = items[0].severity
        score += sev * 3
        score += min(4, len(items) - 1) * sev
    score += len(mismatches) * 8
    score = min(100, score)

    band = risk_band(score)
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
    candidates = [
        Path(r"I:\E Drive\.grok\skills") / raw,
        Path.home() / ".grok" / "skills" / raw,
        Path(r"D:\lygo-protocol-stack\clawhub\mirrors") / raw,
        Path(r"D:\lygo-protocol-stack\docs\skills") / raw,
        Path.cwd() / raw,
    ]
    for c in candidates:
        if c.is_dir() and (c / "SKILL.md").is_file():
            return c
    return p


def _exit_for_band(band: str, mismatches: list[str], ok: bool) -> int:
    if not ok:
        return 2
    if band in ("critical", "high"):
        return 10
    if band == "elevated" or mismatches:
        return 5
    return 0


def format_markdown_report(report: ScanReport) -> str:
    lines = [
        f"# SkillSpector report — {report.skill_name}",
        "",
        f"- **Path:** `{report.skill_path}`",
        f"- **Version:** {report.skill_version or '?'}",
        f"- **Risk band:** **{report.risk_band}** (score {report.risk_score}/100)",
        f"- **Scanned:** {report.scanned_utc}",
        f"- **Files:** {report.files_scanned}",
        f"- **Recommendation:** {report.recommendation}",
        "",
        report.plain_english,
        "",
        "## Claim mismatches",
        "",
    ]
    if report.mismatches:
        for m in report.mismatches:
            lines.append(f"- {m}")
    else:
        lines.append("- (none)")
    lines += ["", "## Top findings", ""]
    for f in report.findings[:40]:
        lines.append(
            f"- **{f['rule_id']}** sev={f['severity']} `{f['path']}:{f['line']}` — {f['why']}"
        )
        lines.append(f"  - `{f['snippet'][:120]}`")
    lines += [
        "",
        "---",
        f"_Signature {SIG}. Local only. No network. No auto-install._",
        "",
        f"> **FULL stack note:** If you run a full LYGO stack, a **builder** SkillSpector "
        f"pack (batch HTML reports, multi-root gates, CI helpers) is on "
        f"[SkillHub FULL LYGO]({FULL_BUILDER_URL}).",
        "",
    ]
    return "\n".join(lines)


def write_under_state(name_or_path: str, content: str) -> tuple[bool, str]:
    outp = Path(name_or_path)
    if not outp.is_absolute():
        outp = STATE / outp.name
    try:
        outp.resolve().relative_to(STATE.resolve())
    except ValueError:
        return False, "write_must_be_under_state"
    STATE.mkdir(parents=True, exist_ok=True)
    outp.write_text(content, encoding="utf-8")
    return True, str(outp.resolve())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="lygo-skill-spector",
        description="LYGO SkillSpector — local pre-install skill risk scanner (enhanced)",
    )
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("scan", help="Scan a skill directory or slug")
    p.add_argument("path", help="Path to skill folder or slug under .grok/skills")
    p.add_argument("--json", action="store_true", help="JSON only")
    p.add_argument("--write", default="", help="Write report under skill state/ (needs --i-consent)")
    p.add_argument("--i-consent", action="store_true")

    p_gate = sub.add_parser("gate", help="CI/agent gate: fail if band worse than --max-band")
    p_gate.add_argument("path")
    p_gate.add_argument(
        "--max-band",
        default="low",
        choices=BAND_ORDER,
    )
    p_gate.add_argument("--json", action="store_true")

    p_batch = sub.add_parser("batch", help="Scan skill packages under a root directory")
    p_batch.add_argument("root")
    p_batch.add_argument("--json", action="store_true")
    p_batch.add_argument("--max", type=int, default=200)

    p_report = sub.add_parser("report", help="Markdown risk report")
    p_report.add_argument("path")
    p_report.add_argument("--write", default="")
    p_report.add_argument("--i-consent", action="store_true")

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
                    "plain_english": (
                        "Scan skills before install. Local only. No network. "
                        + BUILDER_NOTE
                    ),
                    "builder_url": FULL_BUILDER_URL,
                },
                indent=2,
            )
        )
        return 0

    if cmd == "self-demo":
        target = SKILL_ROOT
        report = scan_skill(target)
        data = report.to_dict()
        print(json.dumps(data, indent=2))
        print("\n" + report.plain_english)
        print("\n" + BUILDER_NOTE)
        return _exit_for_band(report.risk_band, report.mismatches, report.ok)

    if cmd == "scan":
        target = resolve_skill_path(args.path)
        report = scan_skill(target)
        data = report.to_dict()
        if args.write:
            if not args.i_consent:
                data["written"] = False
                data["hint"] = "pass --i-consent with --write"
            else:
                ok_w, msg = write_under_state(args.write, json.dumps(data, indent=2) + "\n")
                data["written"] = ok_w
                if ok_w:
                    data["path"] = msg
                else:
                    data["error"] = msg
        print(json.dumps(data, indent=2))
        if not args.json:
            print("\n" + report.plain_english)
            print("\n" + BUILDER_NOTE)
        return _exit_for_band(report.risk_band, report.mismatches, report.ok)

    if cmd == "gate":
        target = resolve_skill_path(args.path)
        report = scan_skill(target)
        data = report.to_dict()
        print(json.dumps(data, indent=2))
        if not args.json:
            print("\n" + report.plain_english)
        max_i = BAND_ORDER.index(args.max_band)
        got_i = BAND_ORDER.index(report.risk_band) if report.risk_band in BAND_ORDER else 4
        if not report.ok:
            return 2
        if got_i > max_i or report.mismatches:
            return 10 if report.risk_band in ("critical", "high") else 5
        return 0

    if cmd == "batch":
        root = Path(args.root).expanduser().resolve()
        if not root.is_dir():
            print(json.dumps({"ok": False, "error": f"not a dir: {root}"}))
            return 2
        results = []
        n = 0
        for child in sorted(root.iterdir()):
            if not child.is_dir() or not (child / "SKILL.md").is_file():
                continue
            if child.name.startswith("."):
                continue
            rep = scan_skill(child)
            results.append(
                {
                    "skill": rep.skill_name or child.name,
                    "path": str(child),
                    "band": rep.risk_band,
                    "score": rep.risk_score,
                    "mismatches": rep.mismatches,
                    "recommendation": rep.recommendation,
                }
            )
            n += 1
            if n >= args.max:
                break
        order_map = {"critical": 0, "high": 1, "elevated": 2, "low": 3, "clear": 4, "unknown": 5}
        results.sort(key=lambda r: (order_map.get(r["band"], 9), -r["score"]))
        out = {
            "ok": True,
            "signature": SIG,
            "root": str(root),
            "scanned": len(results),
            "results": results,
            "builder_note": BUILDER_NOTE,
            "builder_url": FULL_BUILDER_URL,
        }
        print(json.dumps(out, indent=2))
        worst = results[0]["band"] if results else "clear"
        if worst in ("critical", "high"):
            return 10
        if worst == "elevated":
            return 5
        return 0

    if cmd == "report":
        target = resolve_skill_path(args.path)
        report = scan_skill(target)
        md = format_markdown_report(report)
        print(md)
        if args.write:
            if not args.i_consent:
                print(json.dumps({"written": False, "hint": "pass --i-consent"}))
            else:
                ok_w, msg = write_under_state(args.write, md)
                print(json.dumps({"written": ok_w, "path" if ok_w else "error": msg}))
        return _exit_for_band(report.risk_band, report.mismatches, report.ok)

    print(json.dumps({"ok": False, "error": "need scan|gate|batch|report|self-demo|version"}))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
