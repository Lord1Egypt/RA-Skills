"""Audit the built-in Novel Core without inspecting user-installed engines.

The audit intentionally scans only the built-in Core surface. Optional detectors
and user engines are extension data, so their vocabulary must not make the Core
itself fail validation.
"""

from pathlib import Path
from typing import Union


_MARKERS = (
    ("author", "\u732b\u817b"),
    ("work", "\u5e86\u4f59\u5e74"),
    ("work", "\u5c06\u591c"),
    ("character", "\u8303\u95f2"),
    ("character", "\u5b81\u7f3a"),
    ("character", "\u6851\u6851"),
    ("style", "\u6c89\u9ed8\u89c1\u8bc1\u8005"),
    ("project", "\u5929\u5143\u9274"),
)

_CORE_FILES = ("SKILL.md", "novelforge.md")
_CORE_DIRECTORIES = ("agents", "references")


def _core_paths(skill_root: Path):
    for name in _CORE_FILES:
        path = skill_root / name
        if path.is_file():
            yield path
    for directory in _CORE_DIRECTORIES:
        root = skill_root / directory
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            yield path


def audit_builtin_core(skill_root: Union[Path, str]) -> dict:
    root = Path(skill_root).resolve()
    matches = []
    for path in _core_paths(root):
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for category, marker in _MARKERS:
                if marker in line:
                    matches.append(
                        {
                            "category": category,
                            "marker": marker,
                            "path": str(path.relative_to(root)),
                            "line": line_number,
                        }
                    )
    return {
        "status": "FAIL" if matches else "PASS",
        "matches": matches,
        "scanned": [str(path.relative_to(root)) for path in _core_paths(root)],
    }
