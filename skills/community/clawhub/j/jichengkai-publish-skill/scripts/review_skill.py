#!/usr/bin/env python3
"""Review a Codex skill folder for common pre-publish risks."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "vendor",
}

TEXT_EXTENSIONS = {
    "",
    ".bash",
    ".cjs",
    ".css",
    ".env",
    ".html",
    ".js",
    ".json",
    ".jsx",
    ".lock",
    ".md",
    ".mjs",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

SECRET_FILE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"(^|/)\.env($|\.)",
        r"(^|/)id_rsa$",
        r"(^|/)id_ed25519$",
        r"\.(pem|p12|pfx|key)$",
        r"credentials(\.json|\.yml|\.yaml|\.txt)?$",
        r"secrets?(\.json|\.yml|\.yaml|\.txt)?$",
    )
]

SECRET_CONTENT_PATTERNS = [
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("OpenAI API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("generic secret assignment", re.compile(r"(?i)\b(password|passwd|token|api[_-]?key|secret)\b\s*[:=]\s*['\"][^'\"\n]{8,}['\"]")),
]

SENSITIVE_PATH_PATTERNS = [
    ("SSH directory", re.compile(r"(?<![A-Za-z0-9_~/-])~?/\.ssh\b|/Users/[^/\s]+/\.ssh|/home/[^/\s]+/\.ssh")),
    ("cloud credentials", re.compile(r"(?<![A-Za-z0-9_~/-])~?/\.aws/credentials\b|~?/\.config/gcloud\b|~?/\.azure\b")),
    ("shell history", re.compile(r"(?<![A-Za-z0-9_~/-])~?/\.(zsh_history|bash_history)\b")),
    ("OS keychain", re.compile(r"\bkeychain\b|\bsecurity\s+find-(?:generic|internet)-password\b", re.IGNORECASE)),
]

NETWORK_PATTERNS = [
    ("curl or wget", re.compile(r"\b(curl|wget)\b")),
    ("HTTP client import", re.compile(r"\b(import|from)\s+(requests|httpx|aiohttp|urllib|socket)\b")),
    ("fetch call", re.compile(r"\bfetch\s*\(")),
    ("HTTP URL", re.compile(r"https?://")),
]

OBFUSCATION_PATTERNS = [
    ("dynamic eval", re.compile(r"\b(eval|exec)\s*\(")),
    ("base64 decode", re.compile(r"\b(base64|atob|b64decode)\b")),
    ("long encoded string", re.compile(r"['\"][A-Za-z0-9+/]{160,}={0,2}['\"]")),
    ("destructive broad delete", re.compile(r"\brm\s+-[^\n;]*r[^\n;]*f[^\n;]*(/|\$HOME|~|\*)")),
    ("global chmod", re.compile(r"\bchmod\s+-R\b")),
]


@dataclass
class Finding:
    severity: str
    file: str
    line: int | None
    title: str
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review a Codex skill folder for common pre-publish risks.")
    parser.add_argument("skill_path", help="Path to the skill folder to review")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    parser.add_argument("--fail-on-warn", action="store_true", help="Exit non-zero when warnings are present")
    parser.add_argument("--max-text-bytes", type=int, default=2_000_000, help="Maximum text file size to scan")
    return parser.parse_args()


def iter_files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name not in EXCLUDED_DIRS]
        for file_name in files:
            yield Path(current) / file_name


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_text_candidate(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS


def read_text(path: Path, max_bytes: int) -> tuple[str | None, str | None]:
    data = path.read_bytes()
    if b"\x00" in data:
        return None, "binary content"
    if len(data) > max_bytes:
        return None, f"text file larger than {max_bytes} bytes"
    try:
        return data.decode("utf-8"), None
    except UnicodeDecodeError:
        try:
            return data.decode("utf-8", errors="replace"), "non-UTF-8 bytes replaced"
        except Exception as exc:  # pragma: no cover
            return None, f"could not decode: {exc}"


def add_pattern_findings(
    findings: list[Finding],
    severity: str,
    rel_path: str,
    text: str,
    patterns: Iterable[tuple[str, re.Pattern[str]]],
) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        for title, pattern in patterns:
            if pattern.search(line):
                findings.append(Finding(severity, rel_path, line_number, title, "Matched risk pattern. Inspect manually."))


def review(root: Path, max_text_bytes: int) -> list[Finding]:
    findings: list[Finding] = []

    if not root.exists():
        return [Finding("ERROR", str(root), None, "missing path", "Skill path does not exist.")]
    if not root.is_dir():
        return [Finding("ERROR", str(root), None, "not a directory", "Skill path must be a directory.")]
    if not (root / "SKILL.md").is_file():
        findings.append(Finding("ERROR", ".", None, "missing SKILL.md", "Codex skills require a SKILL.md file."))

    for path in iter_files(root):
        rel_path = relative(path, root)
        lower_rel = rel_path.lower()

        for pattern in SECRET_FILE_PATTERNS:
            if pattern.search(lower_rel):
                findings.append(Finding("ERROR", rel_path, None, "sensitive filename", "Remove secret-like files before publishing."))

        size = path.stat().st_size
        if size > 5_000_000:
            findings.append(Finding("INFO", rel_path, None, "large file", f"File is {size} bytes; confirm it belongs in the skill."))

        if not is_text_candidate(path):
            text, note = read_text(path, max_text_bytes)
            if text is None:
                findings.append(Finding("INFO", rel_path, None, "skipped non-text file", note or "Not a text file."))
                continue
        else:
            text, note = read_text(path, max_text_bytes)
            if note:
                findings.append(Finding("INFO", rel_path, None, "text scan note", note))
            if text is None:
                continue

        add_pattern_findings(findings, "ERROR", rel_path, text, SECRET_CONTENT_PATTERNS)
        add_pattern_findings(findings, "WARN", rel_path, text, SENSITIVE_PATH_PATTERNS)
        add_pattern_findings(findings, "WARN", rel_path, text, NETWORK_PATTERNS)
        add_pattern_findings(findings, "WARN", rel_path, text, OBFUSCATION_PATTERNS)

    return findings


def print_text(findings: list[Finding]) -> None:
    if not findings:
        print("No common pre-publish risks found.")
        return

    for finding in findings:
        location = finding.file
        if finding.line is not None:
            location = f"{location}:{finding.line}"
        print(f"[{finding.severity}] {location} - {finding.title}: {finding.detail}")


def main() -> int:
    args = parse_args()
    root = Path(args.skill_path).expanduser().resolve()
    findings = review(root, args.max_text_bytes)

    if args.json:
        print(json.dumps([asdict(finding) for finding in findings], indent=2))
    else:
        print_text(findings)

    has_error = any(finding.severity == "ERROR" for finding in findings)
    has_warn = any(finding.severity == "WARN" for finding in findings)
    if has_error or (args.fail_on_warn and has_warn):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
