from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable, Sequence


class ExternalCommandError(RuntimeError):
    pass


def run_cmd(
    cmd: Sequence[str],
    *,
    cwd: Path | None = None,
    input_text: str | None = None,
    timeout: int | None = None,
    env: dict[str, str] | None = None,
) -> str:
    try:
        result = subprocess.run(
            list(cmd),
            cwd=str(cwd) if cwd else None,
            input=input_text,
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
            check=False,
        )
    except FileNotFoundError as exc:
        raise ExternalCommandError(f"Command not found: {cmd[0]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise ExternalCommandError(f"Command timed out: {' '.join(cmd)}") from exc

    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        details = stderr or stdout or f"Exit code {result.returncode}"
        raise ExternalCommandError(f"Command failed: {' '.join(cmd)} -> {details}")

    return result.stdout
