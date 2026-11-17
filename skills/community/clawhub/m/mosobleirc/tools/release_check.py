#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_FILES = {
    "config/inventory.json",
    "config/runtime.json",
    "relay/yandex/inventory.json",
    ".env",
}

REQUIRED_FILES = {
    "LICENSE",
    "tests/fixtures/inventory.fixture.json",
    "scripts/direct_transport.py",
    "scripts/setup_runtime.py",
    "config/runtime.relay.example.json",
    "README.md",
    "SKILL.md",
    "ARCHITECTURE.md",
    "PRODUCTION.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "PUBLIC_RELEASE.md",
    "requirements.txt",
    "config/inventory.example.json",
    "config/runtime.example.json",
    "relay/yandex/index.py",
    "relay/yandex/inventory.example.json",
    "relay/yandex/runtime.env.example",
    ".github/workflows/ci.yml",
}

PATTERNS = [
    ("provider JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}")),
    ("provider token assignment", re.compile(r"(?:MOSOBLEIRC_TOKEN|X-Auth-Tenant-Token)\s*[=:]\s*['\"]?[A-Za-z0-9._~-]{20,}", re.I)),
    ("deployment URL", re.compile(r"https://functions\.yandexcloud\.net/[a-z0-9_-]{8,}", re.I)),
    ("private Yandex Function URL", re.compile(r"https://[a-z0-9-]{8,}\.functions\.yandexcloud\.net", re.I)),
    ("Yandex API key", re.compile(r"\bAQV[A-Za-z0-9_-]{20,}\b")),
    ("Yandex IAM token", re.compile(r"\bt1\.[A-Za-z0-9._~-]{20,}\b")),
    ("literal Api-Key credential", re.compile(r"\bApi-Key\s+[A-Za-z0-9._~-]{16,}\b", re.I)),
    ("URL with embedded credentials", re.compile(r"https?://[^\s/:@]+:[^\s/@]+@", re.I)),
    ("GitHub token", re.compile(r"\bgh[opusr]_[A-Za-z0-9_]{20,}\b")),
    ("generic bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}", re.I)),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("email address", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)),
    ("Russian phone number", re.compile(r"(?<!\d)(?:\+7|8)[\s()-]*\d{3}[\s()-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}(?!\d)")),
    ("private deployment path", re.compile(r"/(?:root|srv/agent|var/lib/openclaw)[/\w.-]*", re.I)),
]


def _is_forbidden_runtime_path(rel: Path) -> bool:
    posix = rel.as_posix()
    if posix in FORBIDDEN_FILES:
        return True
    name = rel.name.lower()
    if any(part.lower() in {"private", "production", "secrets", "backups", "reference-images", "reference-history"} for part in rel.parts):
        return True
    if name.startswith(("provider_token", "yandex_api_key")) or rel.suffix.lower() in {".db", ".sqlite", ".sqlite3", ".pem", ".key", ".token", ".zip", ".gz", ".bak"}:
        return True
    if name in {"runtime.json", "inventory.json", "runtime.env"}:
        return True
    if name.startswith(".env") and "example" not in name:
        return True
    if rel.parts and rel.parts[0] == "config":
        if ("runtime" in name or "inventory" in name) and "example" not in name:
            return True
    if len(rel.parts) >= 2 and rel.parts[:2] == ("relay", "yandex"):
        if ("runtime" in name or "inventory" in name) and "example" not in name:
            return True
    return False


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if ".git" in rel.parts or "__pycache__" in rel.parts or path.suffix == ".pyc":
            continue
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        if len(raw) > 2_000_000 or b"\x00" in raw:
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        yield path, rel, text


def scan_root(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in sorted(REQUIRED_FILES):
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if ".git" in rel.parts or "__pycache__" in rel.parts:
            continue
        if _is_forbidden_runtime_path(rel):
            errors.append(f"forbidden runtime file in release tree: {rel}")

    for _path, rel, text in iter_text_files(root):
        for label, pattern in PATTERNS:
            if pattern.search(text):
                errors.append(f"{rel}: matched {label}")
    return errors


def main() -> int:
    errors = scan_root(ROOT)
    if errors:
        print("RELEASE_CHECK_FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("RELEASE_CHECK_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
