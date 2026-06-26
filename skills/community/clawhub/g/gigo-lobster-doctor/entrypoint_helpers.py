#!/usr/bin/env python3

from __future__ import annotations

import os
import json
import sys
from pathlib import Path


def _has_output_dir_override(argv: list[str]) -> bool:
    return any(item == "--output-dir" or item.startswith("--output-dir=") for item in argv)


def _workspace_output_dir(skill_root: Path, output_slug: str) -> str | None:
    if skill_root.parent.name == "skills" and skill_root.parent.parent.name == "workspace":
        workspace_root = skill_root.parent.parent
        return str((workspace_root / "outputs" / output_slug).resolve())
    return None


def _candidate_secret_files(skill_root: Path) -> list[Path]:
    candidates: list[Path] = []
    openclaw_root = os.environ.get("OPENCLAW_ROOT", "").strip()
    if openclaw_root:
        candidates.append(Path(openclaw_root) / "secrets.env")
    openclaw_workspace = os.environ.get("OPENCLAW_WORKSPACE", "").strip()
    if openclaw_workspace:
        candidates.append(Path(openclaw_workspace).parent / "secrets.env")
    if skill_root.parent.name == "skills" and skill_root.parent.parent.name == "workspace":
        candidates.append(skill_root.parent.parent.parent / "secrets.env")
    return candidates


def _load_optional_env_file(skill_root: Path) -> None:
    for candidate in _candidate_secret_files(skill_root):
        if not candidate.is_file():
            continue
        for raw_line in candidate.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if not key or key in os.environ:
                continue
            value = value.strip().strip("'\"")
            os.environ[key] = value
        return


def run_profile(*, active_skill: str, default_args: list[str], output_slug: str | None = None) -> int:
    skill_root = Path(__file__).resolve().parent
    _load_optional_env_file(skill_root)
    user_args = sys.argv[1:]
    merged_args = list(default_args)

    if output_slug and not _has_output_dir_override(user_args):
        workspace_output = _workspace_output_dir(skill_root, output_slug)
        if workspace_output:
            merged_args.extend(["--output-dir", workspace_output])

    if str(skill_root) not in sys.path:
        sys.path.insert(0, str(skill_root))

    os.environ.setdefault("GIGO_ACTIVE_SKILL", active_skill)
    os.environ.setdefault("PYTHONUNBUFFERED", "1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["GIGO_PROFILE_ARGV"] = json.dumps(merged_args + user_args, ensure_ascii=False)

    import main as runtime_main

    return runtime_main.main(merged_args + user_args)
