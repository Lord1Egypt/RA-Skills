#!/usr/bin/env python3
"""Audit the source tree that is eligible for a v2.0 source release."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Set
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PARTS = {".git", ".agenthub-package-142", ".skill-scaffold", "__pycache__", "reports"}
FORBIDDEN_SUFFIXES = {".zip", ".pyc", ".pyo"}
PROVIDER_HOSTS = {
    "api64.ipify.org", "get.geojs.io", "rdap.org", "rdap-bootstrap.arin.net", "stat.ripe.net",
    "api.ipapi.is", "proxycheck.io", "ping0.cc", "www.ping0.cc", "ip.ping0.cc",
    "api.ipinfo.io", "api.abuseipdb.com", "www.abuseipdb.com", "ipinfo.io", "www.ipinfo.io",
    "ipqualityscore.com", "www.ipqualityscore.com", "scamalytics.com", "www.scamalytics.com",
    "ipdata.co", "www.ipdata.co", "img.shields.io", "python.org", "www.python.org",
}
METADATA_HOSTS = {"github.com", "www.github.com", "getipproxy.com", "www.getipproxy.com"}
TEXT_SUFFIXES = {
    ".md", ".py", ".yaml", ".yml", ".json", ".html", ".css", ".js", ".txt", ".toml",
}
SECRET_ASSIGNMENT = re.compile(
    r"(?i)(?:api[-_]?key|access[-_]?token|password|secret)\s*[:=]\s*['\"]([^'\"\r\n]{12,})['\"]"
)
SECRET_PREFIX = re.compile(r"(?i)\b(?:sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{20,})\b")
FORBIDDEN_OUTPUT_FIELD = re.compile(
    r"[\"'](?:raw|raw_response|raw_payload|provider_response|upstream_response|payload|"
    r"email|abuse_contacts?|contacts?|fn|reverse_dns|hostname|analysis)[\"']\s*:"
)
EMAIL_VALUE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PLACEHOLDER_SECRETS = {"secret-token", "super-secret", "test-secret", "example-secret"}


def tracked_files(root: Path) -> List[Path]:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            check=False, capture_output=True, text=False,
        )
    except OSError:
        completed = None
    if completed and completed.returncode == 0:
        return [root / item for item in completed.stdout.decode("utf-8").split("\0") if item]
    return [path for path in root.rglob("*") if path.is_file()]


def forbidden_path(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return any(part in FORBIDDEN_PARTS or part.startswith(".agenthub-package-")
               for part in relative.parts) or path.suffix.lower() in FORBIDDEN_SUFFIXES


def text_files(paths: Iterable[Path]) -> Iterable[tuple[Path, str]]:
    for path in paths:
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            yield path, path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue


def scan_production_sources(root: Path) -> List[str]:
    findings: List[str] = []
    source_paths: List[Path] = []
    for base in (root / "scripts", root / "assets", root / "agents", root / "references"):
        source_paths.extend(path for path in base.rglob("*") if path.is_file())
    source_paths.extend(
        root / name for name in ("README.md", "README.zh-CN.md", "SKILL.md", "COMPLIANCE.md")
        if (root / name).is_file()
    )
    for path, content in text_files(source_paths):
        relative = path.relative_to(root)
        for match in SECRET_ASSIGNMENT.finditer(content):
            if match.group(1).strip().casefold() not in PLACEHOLDER_SECRETS:
                findings.append(f"possible credential value in {relative}")
        if SECRET_PREFIX.search(content):
            findings.append(f"possible token prefix in {relative}")
        if FORBIDDEN_OUTPUT_FIELD.search(content):
            findings.append(f"forbidden output field in {relative}")
        if EMAIL_VALUE.search(content):
            findings.append(f"email-like value in {relative}")
        for match in re.finditer(r"https?://[^\s\"'`)>]+", content):
            parsed = urlsplit(match.group(0).rstrip(".,"))
            if parsed.scheme == "http":
                findings.append(f"plaintext HTTP URL in {relative}: {parsed.hostname or match.group(0)}")
            elif parsed.hostname and parsed.hostname.lower() not in PROVIDER_HOSTS | METADATA_HOSTS:
                findings.append(f"unapproved URL host in {relative}: {parsed.hostname}")
    return findings


def main() -> int:
    tracked = set(tracked_files(ROOT))
    paths = set(tracked)
    paths.update(path for path in ROOT.rglob("*") if path.is_file())
    findings: List[str] = []
    release_paths: Set[Path] = set()
    for path in paths:
        if not path.exists():
            continue
        if forbidden_path(path, ROOT):
            if path in tracked:
                findings.append(f"forbidden release artifact: {path.relative_to(ROOT)}")
        else:
            release_paths.add(path)
    findings.extend(scan_production_sources(ROOT))
    if not (ROOT / ".gitignore").exists():
        findings.append("missing .gitignore")
    if not (ROOT / "COMPLIANCE.md").exists():
        findings.append("missing COMPLIANCE.md")
    if findings:
        print("release audit failed:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1
    print(f"release audit passed: {len(release_paths)} eligible source files checked")
    print("archives, caches, reports, and package directories are excluded from release content")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
