#!/usr/bin/env python3
"""Per-skill virtual environment bootstrap helpers."""

import os
import subprocess
import sys
import shutil
from pathlib import Path
from typing import List, Optional, Tuple

MIN_PYTHON = (3, 9)
VENV_DIRNAME = ".venv"
VENV_ACTIVE_FLAG = "OPENCODE_ACP_VENV_ACTIVE"


def _venv_python_path(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def _is_running_in_target_venv(venv_dir: Path) -> bool:
    try:
        return Path(sys.prefix).resolve() == venv_dir.resolve()
    except Exception:
        return False


def _candidate_python_commands() -> List[List[str]]:
    commands: List[List[str]] = []

    configured = os.environ.get("OPENCODE_ACP_PYTHON")
    if configured:
        commands.append([configured])

    commands.append([sys.executable])

    for minor in (12, 11, 10, 9):
        commands.append([f"python3.{minor}"])

    commands.extend([
        ["python3"],
        ["python"],
    ])

    if os.name == "nt":
        for minor in (12, 11, 10, 9):
            commands.append(["py", f"-3.{minor}"])
        commands.append(["py", "-3"])

    # Keep order while deduplicating
    deduped: List[List[str]] = []
    seen = set()
    for cmd in commands:
        key = tuple(cmd)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(cmd)
    return deduped


def _resolve_python_command(command: List[str]) -> Optional[List[str]]:
    binary = command[0]
    if os.path.isabs(binary):
        return command if Path(binary).exists() else None

    resolved = shutil.which(binary)
    if not resolved:
        return None
    return [resolved] + command[1:]


def _python_version(command: List[str]) -> Optional[Tuple[int, int]]:
    try:
        check = subprocess.run(
            command + ["-c", "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')"],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
    except Exception:
        return None

    raw = check.stdout.strip()
    if not raw:
        return None
    parts = raw.split(".")
    if len(parts) != 2:
        return None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None


def _select_python_for_venv() -> Optional[List[str]]:
    for candidate in _candidate_python_commands():
        resolved = _resolve_python_command(candidate)
        if not resolved:
            continue
        version = _python_version(resolved)
        if not version:
            continue
        if version >= MIN_PYTHON:
            return resolved
    return None


def ensure_local_skill_venv(argv: Optional[List[str]] = None, skill_dir: Optional[Path] = None) -> None:
    """Ensure script runs inside per-skill .venv, creating it on first run."""
    if os.environ.get(VENV_ACTIVE_FLAG) == "1":
        return

    python_for_venv = _select_python_for_venv()
    if not python_for_venv:
        min_version = f"{MIN_PYTHON[0]}.{MIN_PYTHON[1]}"
        current = f"{sys.version_info[0]}.{sys.version_info[1]}"
        raise RuntimeError(
            f"Python {min_version}+ required to bootstrap .venv; current interpreter is {current}"
        )

    base_dir = Path(skill_dir) if skill_dir is not None else Path(__file__).resolve().parent
    venv_dir = base_dir / VENV_DIRNAME

    if _is_running_in_target_venv(venv_dir):
        return

    venv_python = _venv_python_path(venv_dir)
    if not venv_python.exists():
        subprocess.run(python_for_venv + ["-m", "venv", str(venv_dir)], check=True)

    env = os.environ.copy()
    env[VENV_ACTIVE_FLAG] = "1"
    exec_argv = [str(venv_python)] + (argv if argv is not None else sys.argv)
    os.execvpe(str(venv_python), exec_argv, env)
