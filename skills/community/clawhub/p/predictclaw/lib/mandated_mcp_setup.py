from __future__ import annotations

import os
import shlex
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from .config import MANDATED_MCP_COMMAND_DEFAULT


class MandatedMcpSetupError(RuntimeError):
    """Raised when mandated MCP setup fails."""


@dataclass(frozen=True)
class MandatedMcpSetupResult:
    status: str
    command: str | None
    installed: bool
    wrote_env: bool
    message: str


def _resolve_executable(
    command: str, process_env: Mapping[str, str] | None = None
) -> str | None:
    argv = shlex.split(command)
    if not argv:
        return None
    executable = argv[0]
    if "/" in executable:
        path = Path(executable).expanduser()
        if path.exists() and os.access(path, os.X_OK):
            return str(path)
        return None
    path_env = process_env.get("PATH") if process_env else None
    return shutil.which(executable, path=path_env)


def detect_mandated_mcp_command(
    process_env: Mapping[str, str] | None = None,
) -> tuple[str | None, str | None]:
    explicit = (process_env or {}).get("ERC_MANDATED_MCP_COMMAND")
    if explicit and _resolve_executable(explicit, process_env):
        return explicit, "configured"

    if _resolve_executable(MANDATED_MCP_COMMAND_DEFAULT, process_env):
        return MANDATED_MCP_COMMAND_DEFAULT, "default"

    return None, None


def configure_mandated_mcp(
    *,
    skill_dir: Path,
    process_env: Mapping[str, str] | None = None,
) -> MandatedMcpSetupResult:
    command, source = detect_mandated_mcp_command(process_env)

    if command is None:
        return MandatedMcpSetupResult(
            status="missing",
            command=None,
            installed=False,
            wrote_env=False,
            message=(
                "No mandated-vault MCP launcher was found. Install the external erc-mandated-mcp runtime yourself, "
                "then set ERC_MANDATED_MCP_COMMAND in your local .env manually."
            ),
        )

    source_label = (
        "configured command" if source == "configured" else "default launcher"
    )
    return MandatedMcpSetupResult(
        status="ready",
        command=command,
        installed=False,
        wrote_env=False,
        message=f"Mandated MCP is ready via {source_label}: {command}.",
    )
