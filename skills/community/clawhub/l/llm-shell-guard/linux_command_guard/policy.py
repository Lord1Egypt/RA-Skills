from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

BASE_DIR = Path(__file__).resolve().parent
RULES_DIR = BASE_DIR / "rules"


@dataclass(frozen=True)
class Policy:
    allowlist: frozenset[str]
    blocked_binaries: frozenset[str]
    approval_required: frozenset[str]
    denylist: tuple[str, ...]
    regex_rules: tuple[str, ...]
    protected_paths: tuple[Path, ...]


def _read_lines(path: Path) -> list[str]:
    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return lines


def _read_paths(path: Path) -> tuple[Path, ...]:
    return tuple(Path(item).resolve() for item in _read_lines(path))


def load_policy() -> Policy:
    return Policy(
        allowlist=frozenset(_read_lines(RULES_DIR / "allowlist.txt")),
        blocked_binaries=frozenset(_read_lines(RULES_DIR / "blocked_binaries.txt")),
        approval_required=frozenset(_read_lines(RULES_DIR / "approval_required.txt")),
        denylist=tuple(_read_lines(RULES_DIR / "denylist.txt")),
        regex_rules=tuple(_read_lines(RULES_DIR / "regex_rules.txt")),
        protected_paths=_read_paths(RULES_DIR / "protected_paths.txt"),
    )


def starts_with_any(value: str, candidates: Iterable[str]) -> bool:
    return any(value == item or value.startswith(item + "/") for item in candidates)
