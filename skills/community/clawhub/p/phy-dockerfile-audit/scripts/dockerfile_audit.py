#!/usr/bin/env python3
"""
phy-dockerfile-audit — Dockerfile static security auditor
10 checks covering CIS Docker Benchmark + OWASP container security.
Zero external dependencies — pure Python stdlib only.
"""
from __future__ import annotations
import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

# ── Check registry ────────────────────────────────────────────────────────────

CHECKS = {
    "DF001": ("Running as root (no USER instruction)",        "CRITICAL", "CWE-250"),
    "DF002": ("Base image unpinned (latest / no tag)",        "HIGH",     "CWE-1395"),
    "DF003": ("Secret-like value in ENV instruction",         "CRITICAL", "CWE-312"),
    "DF004": ("ADD with remote URL (arbitrary fetch)",        "HIGH",     "CWE-494"),
    "DF005": ("Shell form ENTRYPOINT / CMD (no signal pass)", "MEDIUM",   "CWE-755"),
    "DF006": ("sudo installed in container",                  "HIGH",     "CWE-250"),
    "DF007": ("Missing .dockerignore alongside Dockerfile",   "MEDIUM",   "CWE-552"),
    "DF008": ("Privileged port exposed (< 1024)",             "MEDIUM",   "CWE-284"),
    "DF009": ("apt-get without --no-install-recommends",      "LOW",      "CWE-1395"),
    "DF010": ("Secret-like ARG with hardcoded default",       "CRITICAL", "CWE-312"),
}

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}

# ── Patterns ──────────────────────────────────────────────────────────────────

# Secret-like key names for ENV / ARG checks
SECRET_NAME_RE = re.compile(
    r"(?i)(password|passwd|secret|api[_\-]?key|access[_\-]?key|token|auth|credential"
    r"|private[_\-]?key|db[_\-]?pass|database[_\-]?url|connection[_\-]?string"
    r"|jwt[_\-]?secret|signing[_\-]?key|encryption[_\-]?key|smtp[_\-]?pass)",
)

# Base image line
FROM_RE = re.compile(r"^\s*FROM\s+(.+?)(\s+AS\s+\S+)?\s*$", re.IGNORECASE)

# ADD instruction
ADD_RE = re.compile(r"^\s*ADD\s+", re.IGNORECASE)
URL_RE = re.compile(r"https?://", re.IGNORECASE)

# EXPOSE
EXPOSE_RE = re.compile(r"^\s*EXPOSE\s+(.+)", re.IGNORECASE)

# ENTRYPOINT / CMD
ENTRYPOINT_CMD_RE = re.compile(r"^\s*(ENTRYPOINT|CMD)\s+(.+)", re.IGNORECASE)
EXEC_FORM_RE = re.compile(r"^\s*\[")  # exec form starts with [

# USER
USER_RE = re.compile(r"^\s*USER\s+(.+)", re.IGNORECASE)
ROOT_USER_RE = re.compile(r"^(root|0)$", re.IGNORECASE)

# RUN instructions
RUN_RE = re.compile(r"^\s*RUN\s+(.+)", re.IGNORECASE)

# ENV instruction
ENV_RE = re.compile(r"^\s*ENV\s+(.+)", re.IGNORECASE)

# ARG instruction
ARG_RE = re.compile(r"^\s*ARG\s+(.+)", re.IGNORECASE)

# apt-get install
APT_INSTALL_RE = re.compile(r"apt-get\s+install\b", re.IGNORECASE)
NO_INSTALL_RECOMMENDS_RE = re.compile(r"--no-install-recommends", re.IGNORECASE)

# sudo install
SUDO_INSTALL_RE = re.compile(r"\binstall\b.+\bsudo\b|\bsudo\b.+\binstall\b", re.IGNORECASE)
SUDO_APT_RE = re.compile(r"apt(?:-get)?\s+install\s+.*\bsudo\b", re.IGNORECASE)

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


def severity_icon(s: str) -> str:
    return {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵"}.get(s, "⚪")


# ── Dockerfile parser ─────────────────────────────────────────────────────────

def parse_dockerfile(text: str) -> list[tuple[int, str]]:
    """
    Returns list of (line_number, instruction) tuples with
    line continuations joined. Comments stripped.
    line_number is the 1-based number of the FIRST physical line.
    """
    raw = text.splitlines()
    result: list[tuple[int, str]] = []
    i = 0
    while i < len(raw):
        line = raw[i].rstrip()
        first_lineno = i + 1
        # Skip comments and blanks
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        # Join line continuations
        while line.endswith("\\"):
            line = line[:-1]
            i += 1
            if i < len(raw):
                line = line + " " + raw[i].strip()
        result.append((first_lineno, line.strip()))
        i += 1
    return result


def read_dockerfile(path: Path) -> Optional[list[tuple[int, str]]]:
    for enc in ("utf-8", "latin-1"):
        try:
            text = path.read_text(encoding=enc)
            return parse_dockerfile(text)
        except Exception:
            pass
    return None


# ── Per-check implementations ─────────────────────────────────────────────────

def check_df001(instructions: list[tuple[int, str]], file: str) -> list[Finding]:
    """No USER instruction, or USER root."""
    findings = []
    user_lines = [(ln, inst) for ln, inst in instructions if USER_RE.match(inst)]
    if not user_lines:
        # Only fire if there's at least one FROM (it's a real Dockerfile)
        if any(FROM_RE.match(inst) for _, inst in instructions):
            findings.append(Finding(
                check_id="DF001", severity="CRITICAL", cwe="CWE-250",
                message="No USER instruction found — container runs as root by default",
                file=file, line=0,
                snippet="(no USER directive in file)",
                fix="Add 'USER nonroot' or create a non-root user: RUN useradd -r -u 1001 appuser && USER appuser",
            ))
    else:
        for ln, inst in user_lines:
            m = USER_RE.match(inst)
            if m and ROOT_USER_RE.match(m.group(1).strip()):
                findings.append(Finding(
                    check_id="DF001", severity="CRITICAL", cwe="CWE-250",
                    message=f"USER set to root explicitly",
                    file=file, line=ln,
                    snippet=inst[:120],
                    fix="Replace 'USER root' with a non-root user. Only use USER root temporarily during build steps.",
                ))
    return findings


def check_df002(instructions: list[tuple[int, str]], file: str) -> list[Finding]:
    """Base image unpinned (latest or no digest/tag)."""
    findings = []
    for ln, inst in instructions:
        m = FROM_RE.match(inst)
        if not m:
            continue
        image = m.group(1).strip()
        # scratch is ok
        if image.lower() == "scratch":
            continue
        # Must have a tag or digest
        if "@sha256:" in image:
            continue  # pinned by digest
        if ":" in image.split("/")[-1]:
            tag = image.split(":")[-1]
            if tag.lower() == "latest":
                findings.append(Finding(
                    check_id="DF002", severity="HIGH", cwe="CWE-1395",
                    message=f"Base image uses ':latest' tag — non-reproducible builds, silent upstream changes",
                    file=file, line=ln,
                    snippet=inst[:120],
                    fix=f"Pin to a specific version: {image.replace(':latest', ':' + '<version>')} or use a SHA digest.",
                ))
        else:
            # No tag at all — implicitly latest
            findings.append(Finding(
                check_id="DF002", severity="HIGH", cwe="CWE-1395",
                message=f"Base image has no tag — implicitly pulls ':latest'",
                file=file, line=ln,
                snippet=inst[:120],
                fix=f"Add a specific version tag: {image}:<version>, e.g. {image}:3.12-slim",
            ))
    return findings


def check_df003(instructions: list[tuple[int, str]], file: str) -> list[Finding]:
    """Secret-like value in ENV instruction."""
    findings = []
    for ln, inst in instructions:
        m = ENV_RE.match(inst)
        if not m:
            continue
        env_body = m.group(1)
        # ENV can be: KEY=value KEY2=value2   OR legacy: KEY value
        # Split on spaces or =
        pairs = re.findall(r'(\w+)(?:\s*=\s*|\s+)(\S+)', env_body)
        for key, value in pairs:
            if not SECRET_NAME_RE.search(key):
                continue
            # Skip obvious placeholders and empty values
            if value in ("", '""', "''", "none", "null", "undefined", "changeme",
                         "placeholder", "your_value_here"):
                continue
            # Skip if value looks like a build-arg reference
            if value.startswith("${") or value.startswith("$"):
                continue
            findings.append(Finding(
                check_id="DF003", severity="CRITICAL", cwe="CWE-312",
                message=f"Potential secret in ENV '{key}' — baked into image layer, visible in 'docker inspect'",
                file=file, line=ln,
                snippet=inst[:120],
                fix="Pass secrets at runtime via --env-file or Docker secrets. Use ARG for build-time only (but ARG values also appear in layer history).",
            ))
    return findings


def check_df004(instructions: list[tuple[int, str]], file: str) -> list[Finding]:
    """ADD with remote URL."""
    findings = []
    for ln, inst in instructions:
        if not ADD_RE.match(inst):
            continue
        if URL_RE.search(inst):
            findings.append(Finding(
                check_id="DF004", severity="HIGH", cwe="CWE-494",
                message="ADD fetches a remote URL — no integrity check, MITM risk",
                file=file, line=ln,
                snippet=inst[:120],
                fix="Use RUN curl -fsSL <url> | sha256sum -c <expected-hash> instead, or use COPY with a pre-downloaded file.",
            ))
    return findings


def check_df005(instructions: list[tuple[int, str]], file: str) -> list[Finding]:
    """Shell form ENTRYPOINT / CMD — no signal propagation."""
    findings = []
    for ln, inst in instructions:
        m = ENTRYPOINT_CMD_RE.match(inst)
        if not m:
            continue
        body = m.group(2).strip()
        if EXEC_FORM_RE.match(body):
            continue  # exec form is correct
        findings.append(Finding(
            check_id="DF005", severity="MEDIUM", cwe="CWE-755",
            message=f"Shell form {m.group(1).upper()} — runs via /bin/sh -c, PID 1 won't receive SIGTERM properly",
            file=file, line=ln,
            snippet=inst[:120],
            fix=f'Use exec form: {m.group(1).upper()} ["executable", "arg1"]. This ensures signals reach your process.',
        ))
    return findings


def check_df006(instructions: list[tuple[int, str]], file: str) -> list[Finding]:
    """sudo installed in container."""
    findings = []
    for ln, inst in instructions:
        m = RUN_RE.match(inst)
        if not m:
            continue
        cmd = m.group(1)
        if SUDO_APT_RE.search(cmd) or re.search(r'\binstall\b[^|;\n]*\bsudo\b', cmd, re.IGNORECASE):
            findings.append(Finding(
                check_id="DF006", severity="HIGH", cwe="CWE-250",
                message="sudo installed in container — privilege escalation risk if process is compromised",
                file=file, line=ln,
                snippet=inst[:120],
                fix="Remove sudo from the container. If specific commands need elevated privileges, use gosu or setuid wrapper instead.",
            ))
    return findings


def check_df007(path: Path, file: str) -> list[Finding]:
    """Missing .dockerignore in the same directory."""
    dockerignore = path.parent / ".dockerignore"
    if not dockerignore.exists():
        return [Finding(
            check_id="DF007", severity="MEDIUM", cwe="CWE-552",
            message="No .dockerignore file found — .git, .env, node_modules, secrets may be sent to build context",
            file=file, line=0,
            snippet="(no .dockerignore in " + str(path.parent) + ")",
            fix="Create .dockerignore with: .git\\n.env*\\nnode_modules\\n*.log\\n**/.DS_Store\\ncoverage/",
        )]
    return []


def check_df008(instructions: list[tuple[int, str]], file: str) -> list[Finding]:
    """Privileged port EXPOSE < 1024."""
    findings = []
    for ln, inst in instructions:
        m = EXPOSE_RE.match(inst)
        if not m:
            continue
        ports_str = m.group(1)
        # Extract all port numbers (may be range: 80-90 or proto: 80/tcp)
        for port_token in ports_str.split():
            port_str = port_token.split("/")[0].split("-")[0]
            try:
                port = int(port_str)
                if port < 1024:
                    findings.append(Finding(
                        check_id="DF008", severity="MEDIUM", cwe="CWE-284",
                        message=f"Privileged port {port} exposed — requires root or CAP_NET_BIND_SERVICE to bind",
                        file=file, line=ln,
                        snippet=inst[:120],
                        fix=f"Use an unprivileged port (>= 1024) and remap at the host: -p 80:{port + 7000}. Or add CAP_NET_BIND_SERVICE capability explicitly.",
                    ))
            except ValueError:
                pass
    return findings


def check_df009(instructions: list[tuple[int, str]], file: str) -> list[Finding]:
    """apt-get install without --no-install-recommends."""
    findings = []
    for ln, inst in instructions:
        m = RUN_RE.match(inst)
        if not m:
            continue
        cmd = m.group(1)
        if not APT_INSTALL_RE.search(cmd):
            continue
        if NO_INSTALL_RECOMMENDS_RE.search(cmd):
            continue
        findings.append(Finding(
            check_id="DF009", severity="LOW", cwe="CWE-1395",
            message="apt-get install without --no-install-recommends — installs unnecessary packages, bloats image",
            file=file, line=ln,
            snippet=inst[:120],
            fix="Use: apt-get install -y --no-install-recommends <packages> && rm -rf /var/lib/apt/lists/*",
        ))
    return findings


def check_df010(instructions: list[tuple[int, str]], file: str) -> list[Finding]:
    """Secret-like ARG with hardcoded default value."""
    findings = []
    for ln, inst in instructions:
        m = ARG_RE.match(inst)
        if not m:
            continue
        arg_body = m.group(1).strip()
        # ARG KEY=value
        kv = re.match(r'(\w+)\s*=\s*(\S+)', arg_body)
        if not kv:
            continue
        key, value = kv.group(1), kv.group(2).strip('"\'')
        if not SECRET_NAME_RE.search(key):
            continue
        # Skip empty / placeholder defaults
        if not value or value.lower() in ("", "none", "null", '""', "''"):
            continue
        findings.append(Finding(
            check_id="DF010", severity="CRITICAL", cwe="CWE-312",
            message=f"ARG '{key}' has a hardcoded secret default — visible in docker history even if overridden at build time",
            file=file, line=ln,
            snippet=inst[:120],
            fix="Remove the default value: ARG " + key + " (no =). Pass the value via --build-arg at build time. Never store secrets in ARG defaults.",
        ))
    return findings


# ── Orchestrator ──────────────────────────────────────────────────────────────

def scan_dockerfile(path: Path) -> list[Finding]:
    instructions = read_dockerfile(path)
    if instructions is None:
        return []

    file_str = str(path)
    findings: list[Finding] = []
    findings.extend(check_df001(instructions, file_str))
    findings.extend(check_df002(instructions, file_str))
    findings.extend(check_df003(instructions, file_str))
    findings.extend(check_df004(instructions, file_str))
    findings.extend(check_df005(instructions, file_str))
    findings.extend(check_df006(instructions, file_str))
    findings.extend(check_df007(path, file_str))
    findings.extend(check_df008(instructions, file_str))
    findings.extend(check_df009(instructions, file_str))
    findings.extend(check_df010(instructions, file_str))
    return findings


def is_dockerfile(path: Path) -> bool:
    """True if the path looks like a Dockerfile."""
    name = path.name.lower()
    return (
        name == "dockerfile"
        or name.startswith("dockerfile.")
        or name.endswith(".dockerfile")
    )


def scan_directory(root: Path) -> list[Finding]:
    SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__",
                 "dist", "build", ".next", "vendor"}
    findings: list[Finding] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(p in SKIP_DIRS for p in path.parts):
            continue
        if is_dockerfile(path):
            findings.extend(scan_dockerfile(path))
    return findings


# ── Output ────────────────────────────────────────────────────────────────────

def print_findings(findings: list[Finding], fmt: str, ci: bool) -> int:
    findings.sort(key=lambda f: (SEVERITY_ORDER.get(f.severity, 9), f.file, f.line))
    criticals = sum(1 for f in findings if f.severity == "CRITICAL")
    highs     = sum(1 for f in findings if f.severity == "HIGH")

    if fmt == "json":
        print(json.dumps({
            "total": len(findings), "criticals": criticals, "highs": highs,
            "findings": [
                {"check": f.check_id, "severity": f.severity, "cwe": f.cwe,
                 "message": f.message, "file": f.file, "line": f.line,
                 "snippet": f.snippet, "fix": f.fix}
                for f in findings
            ],
        }, indent=2))
    elif fmt == "github":
        for f in findings:
            lvl = "error" if f.severity in ("CRITICAL", "HIGH") else "warning"
            loc = f",line={f.line}" if f.line else ""
            print(f"::{lvl} file={f.file}{loc},title={f.check_id} {f.severity}::{f.message}")
    else:
        if not findings:
            print("✅  No Dockerfile security issues detected.")
        else:
            print(f"\n{'='*70}")
            print(f"  phy-dockerfile-audit — Dockerfile Security Report")
            print(f"{'='*70}")
            print(f"  Total: {len(findings)}  |  Critical: {criticals}  |  High: {highs}")
            print(f"{'='*70}\n")
            for f in findings:
                icon = severity_icon(f.severity)
                name, _, cwe = CHECKS.get(f.check_id, (f.message, "", f.cwe))
                print(f"{icon} [{f.check_id}] {f.severity} — {name} ({cwe})")
                if f.line:
                    print(f"   File : {f.file}:{f.line}")
                else:
                    print(f"   File : {f.file}")
                print(f"   Code : {f.snippet}")
                print(f"   Fix  : {f.fix}\n")

    if ci and (criticals > 0 or highs > 0):
        return 1
    return 0


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        description="phy-dockerfile-audit — Dockerfile static security auditor",
    )
    ap.add_argument("target", nargs="?", default=".",
                    help="Dockerfile path or directory to scan (default: current dir)")
    ap.add_argument("--format", choices=["text", "json", "github"], default="text",
                    help="Output format")
    ap.add_argument("--ci", action="store_true",
                    help="Exit 1 if any CRITICAL or HIGH finding exists")
    ap.add_argument("--check", metavar="ID",
                    help="Run only this check ID (e.g. DF001)")
    args = ap.parse_args()

    target = Path(args.target).resolve()
    if not target.exists():
        print(f"Error: not found: {target}", file=sys.stderr)
        sys.exit(2)

    if target.is_file():
        findings = scan_dockerfile(target)
    else:
        findings = scan_directory(target)

    if args.check:
        findings = [f for f in findings if f.check_id == args.check.upper()]

    rc = print_findings(findings, args.format, args.ci)
    sys.exit(rc)


if __name__ == "__main__":
    main()
