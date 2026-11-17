"""Resolve and validate lygo-protocol-stack root — SkillSpector-hardened."""

from __future__ import annotations

import os
import re
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
_STACK_MARKER = "tools/haven_star_chart_gate.py"
# Block traversal and wildcards; allow Windows drive colon (e.g. C:\)
_FORBIDDEN_PATH = re.compile(r"\.\.|[<>\"|?*]")

_REQUIRED_FILES = (
    "tools/haven_star_chart_gate.py",
    "tools/haven_star_chart_submit.py",
    "tools/haven_star_chart_feed.py",
    "docs/haven_star_chart/AGENT_PORTAL.md",
    "docs/haven_star_chart/submission_schema.json",
)


def _reject_unsafe_path(p: Path) -> None:
    s = str(p)
    if _FORBIDDEN_PATH.search(s):
        raise SystemExit(f"Unsafe path rejected: {p}")
    if len(s) > 512:
        raise SystemExit("Path too long")


def resolve_stack_root(explicit: str | None = None) -> Path:
    """Return validated stack root. LYGO_STACK_ROOT must point to a trusted user clone."""
    if explicit:
        p = Path(explicit).expanduser().resolve()
        _reject_unsafe_path(p)
        _assert_stack(p)
        return p
    env = os.environ.get("LYGO_STACK_ROOT", "").strip()
    if env:
        p = Path(env).expanduser().resolve()
        _reject_unsafe_path(p)
        _assert_stack(p)
        return p
    for anc in SKILL_ROOT.parents:
        if (anc / _STACK_MARKER).is_file():
            p = anc.resolve()
            _assert_stack(p)
            return p
    raise SystemExit(
        "Set LYGO_STACK_ROOT to your trusted lygo-protocol-stack clone (absolute path)."
    )


def validate_local_json_path(path: str | Path, *, stack: Path | None = None) -> Path:
    """Resolve submission JSON — must exist, be a file, no traversal."""
    p = Path(path).expanduser().resolve()
    _reject_unsafe_path(p)
    if not p.is_file():
        raise SystemExit(f"Not a file: {p}")
    if p.suffix.lower() != ".json":
        raise SystemExit("Submission path must be a .json file")
    if stack is not None:
        stack = stack.resolve()
        try:
            p.relative_to(stack)
        except ValueError:
            try:
                p.relative_to(Path.cwd().resolve())
            except ValueError:
                raise SystemExit(
                    "Submission JSON must live under LYGO_STACK_ROOT or current working directory"
                ) from None
    return p


def _assert_stack(p: Path) -> None:
    missing = [rel for rel in _REQUIRED_FILES if not (p / rel).is_file()]
    if missing:
        raise SystemExit(f"Invalid stack root {p}; missing: {missing}")