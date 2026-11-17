"""Import allowlisted stack tools in-process — no subprocess (SkillSpector-safe)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

ALLOWED_TOOLS: frozenset[str] = frozenset(
    {
        "haven_star_chart_gate.py",
        "haven_star_chart_feed.py",
    }
)


def load_tool(stack_root: Path, basename: str) -> ModuleType:
    if basename not in ALLOWED_TOOLS:
        raise ValueError(f"Tool not allowlisted: {basename}")
    path = (stack_root / "tools" / basename).resolve()
    expected = (stack_root / "tools" / basename).resolve()
    if path != expected or not path.is_file():
        raise FileNotFoundError(f"Missing stack tool: {basename}")
    spec = importlib.util.spec_from_file_location(f"lygo_hsc_{basename[:-3]}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {basename}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod