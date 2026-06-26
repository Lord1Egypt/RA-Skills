#!/usr/bin/env python3
"""Shared command construction for wrapper entrypoints."""

import sys
from pathlib import Path
from typing import List, Optional


def build_client_command(
    project_dir: str,
    task: str,
    timeout: int,
    base_dir: Optional[Path] = None,
    python_executable: Optional[str] = None,
) -> List[str]:
    """Build a portable command to invoke opencode_acp_client.py."""
    script_base_dir = base_dir if base_dir is not None else Path(__file__).resolve().parent
    client_script = script_base_dir / "opencode_acp_client.py"
    interpreter = python_executable if python_executable is not None else sys.executable

    return [
        interpreter,
        str(client_script),
        "--project",
        project_dir,
        "--task",
        task,
        "--timeout",
        str(timeout),
    ]
