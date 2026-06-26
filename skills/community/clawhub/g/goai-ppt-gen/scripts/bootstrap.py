from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def _resolved(path: str | Path) -> Path | None:
    try:
        return Path(path).resolve()
    except OSError:
        return None


def _uv_install_hint() -> str:
    if sys.platform == "darwin":
        return (
            "uv is required to run this skill. Install it with: brew install uv. "
            "After uv is installed, rerun the skill; uv will prepare Python and dependencies automatically."
        )
    if sys.platform == "win32":
        return (
            "uv is required to run this skill. Install it with: winget install astral-sh.uv. "
            "After uv is installed, rerun the skill; uv will prepare Python and dependencies automatically."
        )
    return (
        "uv is required to run this skill. Install uv and rerun this command. "
        "After uv is installed, it will prepare Python and dependencies automatically."
    )


def ensure_uv_runtime(entrypoint: str | Path) -> None:
    script_path = Path(entrypoint).resolve()
    skill_dir = script_path.parent.parent
    expected_venv = _resolved(skill_dir / ".venv")
    prefix = _resolved(sys.prefix)
    virtual_env = _resolved(os.environ["VIRTUAL_ENV"]) if "VIRTUAL_ENV" in os.environ else None

    if os.environ.get("UV_RUN_RECURSION_DEPTH"):
        return
    if expected_venv is not None and (prefix == expected_venv or virtual_env == expected_venv):
        return

    uv_bin = shutil.which("uv")
    if uv_bin is None:
        print(_uv_install_hint(), file=sys.stderr)
        raise SystemExit(1)

    os.execvpe(
        uv_bin,
        [
            uv_bin,
            "run",
            "--project",
            str(skill_dir),
            "python",
            str(script_path),
            *sys.argv[1:],
        ],
        os.environ.copy(),
    )
