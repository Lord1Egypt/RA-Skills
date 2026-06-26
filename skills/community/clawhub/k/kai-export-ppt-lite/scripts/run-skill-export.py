#!/usr/bin/env python3
"""
Tiny bootstrap for skill-based sandboxes.

Use this script as the stable execution surface for hosted skill runtimes.
If the sandbox only supports inline Python execution, inline this file instead
of the much larger `export-sandbox-pptx.py`.
"""

import argparse
import importlib.util
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

SKILL_NAME = "kai-export-ppt-lite"


def _candidate_skill_roots(
    script_file: Optional[str] = None,
    cwd: Optional[Path] = None,
    env: Optional[Dict[str, str]] = None,
) -> List[Path]:
    env = env or os.environ
    candidates: List[Path] = []

    def _add(path: Optional[Path]) -> None:
        if not path:
            return
        try:
            candidates.append(path.expanduser().resolve())
        except Exception:
            return

    if script_file:
        script_path = Path(script_file)
        _add(script_path.parent.parent)
        _add(script_path.parent)

    for env_key in (
        "KAI_EXPORT_PPT_LITE_ROOT",
        "CLAUDE_SKILL_DIR",
        "CODEX_SKILL_DIR",
        "OPENCLAW_SKILL_DIR",
    ):
        raw = env.get(env_key)
        if not raw:
            continue
        env_path = Path(raw)
        _add(env_path)
        _add(env_path.parent)
        _add(env_path.parent.parent)

    cwd_path = Path(cwd or Path.cwd())
    _add(cwd_path)
    for parent in cwd_path.parents:
        _add(parent)

    _add(Path.home() / "skills" / SKILL_NAME)
    _add(Path("/home/user/skills") / SKILL_NAME)
    return candidates


def _looks_like_skill_root(path: Path) -> bool:
    return (
        (path / "SKILL.md").exists() and
        (path / "scripts" / "export-sandbox-pptx.py").exists()
    )


def resolve_skill_root(
    explicit_root: Optional[str] = None,
    script_file: Optional[str] = None,
    cwd: Optional[Path] = None,
    env: Optional[Dict[str, str]] = None,
) -> Path:
    env = env or os.environ
    if explicit_root:
        root = Path(explicit_root).expanduser().resolve()
        if _looks_like_skill_root(root):
            return root
        raise FileNotFoundError(f"Skill root does not look valid: {root}")

    seen: Set[Path] = set()
    for candidate in _candidate_skill_roots(script_file, cwd, env):
        if candidate in seen:
            continue
        seen.add(candidate)
        if _looks_like_skill_root(candidate):
            return candidate
    raise FileNotFoundError(
        "Could not locate installed kai-export-ppt-lite skill root. "
        "Set KAI_EXPORT_PPT_LITE_ROOT or pass --skill-root."
    )


def load_exporter_module(skill_root: Path):
    script_path = skill_root / "scripts" / "export-sandbox-pptx.py"
    spec = importlib.util.spec_from_file_location(
        "kai_export_ppt_lite_exporter",
        script_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to create module spec for {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stable skill bootstrap for kai-export-ppt-lite",
    )
    parser.add_argument("html", help="Path to HTML file")
    parser.add_argument("output", nargs="?", help="Output .pptx path")
    parser.add_argument("--width", type=int, default=1440, help="Slide width in pixels (default: 1440)")
    parser.add_argument("--height", type=int, default=900, help="Slide height in pixels (default: 900)")
    parser.add_argument("--with-chrome", action="store_true", help="Add exporter-provided page counter and nav dots")
    parser.add_argument("--skill-root", help="Explicit installed skill root")
    args = parser.parse_args()

    skill_root = resolve_skill_root(
        explicit_root=args.skill_root,
        script_file=globals().get("__file__"),
    )
    module = load_exporter_module(skill_root)
    module.export_sandbox(
        args.html,
        args.output,
        args.width,
        args.height,
        add_chrome=args.with_chrome,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
