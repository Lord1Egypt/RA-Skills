from __future__ import annotations

import json
import os
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator

from openclaw_sec.data.secret_patterns import KEYWORD_ASSIGNMENT, SECRET_PATTERNS


MAX_SCAN_BYTES = 2 * 1024 * 1024
IGNORED_DIR_NAMES = {".git", "node_modules", "__pycache__", ".pytest_cache", "dist", "build"}


@dataclass(frozen=True, slots=True)
class SecretHit:
    pattern_name: str
    line_no: int
    masked_value: str


@dataclass(frozen=True, slots=True)
class CommandResult:
    ok: bool
    returncode: int
    stdout: str
    stderr: str
    command: list[str]


def expand_path(value: str | Path | None) -> Path | None:
    if value is None:
        return None
    return Path(value).expanduser().resolve(strict=False)


def read_text(path: Path, limit: int = MAX_SCAN_BYTES) -> str:
    if not path.exists() or not path.is_file():
        return ""
    try:
        if path.stat().st_size > limit:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def load_json(path: Path) -> Any:
    return json.loads(read_text(path))


def flatten_json(value: Any, prefix: str = "") -> Iterator[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, nested in value.items():
            next_prefix = f"{prefix}.{key}" if prefix else str(key)
            yield from flatten_json(nested, next_prefix)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            next_prefix = f"{prefix}[{index}]"
            yield from flatten_json(nested, next_prefix)
    else:
        yield prefix, value


def mask_secret(secret: str) -> str:
    secret = secret.strip()
    if secret.startswith("-----BEGIN ") and "PRIVATE KEY-----" in secret:
        return "-----BEGIN **** PRIVATE KEY-----"
    if len(secret) <= 8:
        return "*" * len(secret)
    if ":" in secret and len(secret.split(":", 1)[0]) <= 12:
        left, right = secret.split(":", 1)
        return f"{left}:****{right[-4:]}" if len(right) >= 4 else f"{left}:****"
    if secret.lower().startswith("bearer "):
        token = secret[7:]
        return f"Bearer ****{token[-4:]}" if len(token) >= 4 else "Bearer ****"
    return f"{secret[:4]}****{secret[-4:]}"


def find_secret_hits(text: str) -> list[SecretHit]:
    hits: list[SecretHit] = []
    seen: set[tuple[str, int, str]] = set()
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pattern in SECRET_PATTERNS:
            for match in pattern.regex.finditer(line):
                masked = mask_secret(match.group(0))
                key = (pattern.name, line_no, masked)
                if key not in seen:
                    seen.add(key)
                    hits.append(SecretHit(pattern.name, line_no, masked))
        for match in KEYWORD_ASSIGNMENT.finditer(line):
            masked = mask_secret(match.group(2))
            key = ("keyword_assignment", line_no, masked)
            if key not in seen:
                seen.add(key)
                hits.append(SecretHit("keyword_assignment", line_no, masked))
    return hits


def unique_preserve(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def iter_files(root: Path, max_depth: int = 6) -> Iterator[Path]:
    root = root.expanduser().resolve(strict=False)
    if not root.exists():
        return
    base_depth = len(root.parts)
    for current_root, dirnames, filenames in os.walk(root):
        current_path = Path(current_root)
        depth = len(current_path.parts) - base_depth
        dirnames[:] = [dirname for dirname in dirnames if dirname not in IGNORED_DIR_NAMES]
        if depth >= max_depth:
            dirnames[:] = []
        for filename in filenames:
            yield current_path / filename


def run_command(command: list[str], timeout: int = 5) -> CommandResult:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return CommandResult(
            ok=completed.returncode == 0,
            returncode=completed.returncode,
            stdout=completed.stdout.strip(),
            stderr=completed.stderr.strip(),
            command=command,
        )
    except (FileNotFoundError, subprocess.SubprocessError, OSError) as exc:
        return CommandResult(
            ok=False,
            returncode=127,
            stdout="",
            stderr=str(exc),
            command=command,
        )


def permission_bits(path: Path) -> int:
    return stat.S_IMODE(path.lstat().st_mode)


def permission_string(path: Path) -> str:
    return stat.filemode(path.lstat().st_mode)


def is_world_readable(mode: int) -> bool:
    return bool(mode & stat.S_IROTH)


def is_world_writable(mode: int) -> bool:
    return bool(mode & stat.S_IWOTH)


def is_group_readable(mode: int) -> bool:
    return bool(mode & stat.S_IRGRP)


def is_group_writable(mode: int) -> bool:
    return bool(mode & stat.S_IWGRP)


def path_outside_base(path: Path, base: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(base.resolve(strict=False))
        return False
    except ValueError:
        return True


def discover_named_files(roots: Iterable[Path], names: set[str]) -> list[Path]:
    found: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for path in iter_files(root):
            if path.name in names:
                found.append(path)
    return found


def discover_suffix_files(roots: Iterable[Path], suffixes: tuple[str, ...]) -> list[Path]:
    found: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for path in iter_files(root):
            if path.name.endswith(suffixes):
                found.append(path)
    return found
