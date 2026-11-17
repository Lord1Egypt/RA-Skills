"""Bounded, non-installing environment diagnosis."""

from __future__ import annotations

import os
from pathlib import Path
import platform
import shutil
import socket
import sys
import tempfile
from typing import Any, Iterable

from .config import DASHBOARD_DIR, INTERNAL_DIR, KNOWLEDGE_DIR, normalized
from .result import make_result


SKIP_DIRS = {
    ".git",
    INTERNAL_DIR,
    KNOWLEDGE_DIR,
    DASHBOARD_DIR,
    "node_modules",
    "__pycache__",
}


def python_runtime_info(version: tuple[int, int, int] | None = None) -> dict[str, Any]:
    version = version or (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    return {
        "executable": sys.executable,
        "version": ".".join(str(value) for value in version),
        "supported": version >= (3, 10, 0),
        "minimum": "3.10.0",
    }


def probe_writable(path: Path) -> tuple[bool, str | None]:
    path = normalized(path)
    if not path.is_dir():
        return False, "directory does not exist"
    probe: Path | None = None
    try:
        descriptor, name = tempfile.mkstemp(prefix=".ai-workbench-write-probe-", dir=path)
        os.close(descriptor)
        probe = Path(name)
        probe.unlink()
        return True, None
    except OSError as exc:
        if probe:
            probe.unlink(missing_ok=True)
        return False, str(exc)


def port_is_available(port: int, host: str = "127.0.0.1") -> bool:
    if not 1 <= port <= 65535:
        return False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
        except OSError:
            return False
    return True


def choose_port(preferred: int = 8765, host: str = "127.0.0.1") -> tuple[int, bool]:
    if preferred and port_is_available(preferred, host):
        return preferred, True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return int(sock.getsockname()[1]), False


def find_vaults(roots: Iterable[Path], max_depth: int = 3) -> list[Path]:
    """Find Obsidian-shaped directories under explicitly supplied roots only."""

    candidates: set[Path] = set()
    for supplied_root in roots:
        root = normalized(supplied_root)
        if not root.is_dir():
            continue
        for current_text, dirnames, _filenames in os.walk(root):
            current = Path(current_text)
            try:
                depth = len(current.relative_to(root).parts)
            except ValueError:
                dirnames[:] = []
                continue
            if depth > max_depth:
                dirnames[:] = []
                continue
            if ".obsidian" in dirnames:
                candidates.add(current.resolve(strict=False))
            dirnames[:] = [
                name
                for name in dirnames
                if name == ".obsidian" or (not name.startswith(".") and name not in SKIP_DIRS)
            ]
            if ".obsidian" in dirnames:
                dirnames.remove(".obsidian")
    return sorted(candidates, key=lambda value: str(value).casefold())


def obsidian_installation() -> dict[str, Any]:
    system = platform.system().lower()
    app_candidates: list[Path] = []
    if system == "darwin":
        app_candidates = [Path("/Applications/Obsidian.app"), Path.home() / "Applications/Obsidian.app"]
    elif system == "windows":
        for key in ("LOCALAPPDATA", "PROGRAMFILES"):
            base = os.environ.get(key)
            if base:
                app_candidates.append(Path(base) / "Obsidian" / "Obsidian.exe")
    existing = [str(path) for path in app_candidates if path.exists()]
    cli = shutil.which("obsidian")
    return {
        "application_detected": bool(existing),
        "application_paths": existing,
        "cli_detected": bool(cli),
        "cli_path": cli,
    }


def diagnose(
    *,
    workspace: Path,
    sources: list[Path],
    preferred_port: int = 8765,
    max_vault_depth: int = 3,
) -> tuple[dict[str, Any], int]:
    workspace = normalized(workspace)
    sources = [normalized(path) for path in sources]
    missing_sources = [str(path) for path in sources if not path.is_dir()]
    if not workspace.is_dir():
        return make_result(
            status="error",
            code="WORKSPACE_NOT_FOUND",
            message="The selected workspace directory does not exist.",
            next_actions=[{"action": "select_workspace", "path": str(workspace)}],
        ), 1
    if missing_sources:
        return make_result(
            status="error",
            code="SOURCE_NOT_FOUND",
            message="One or more selected source directories do not exist.",
            next_actions=[{"action": "select_sources", "missing": missing_sources}],
            data={"missing_sources": missing_sources},
        ), 1

    writable, write_error = probe_writable(workspace)
    python_info = python_runtime_info()
    vaults = find_vaults(sources, max_depth=max_vault_depth)
    obsidian = obsidian_installation()
    selected_port, preferred_available = choose_port(preferred_port)
    system = platform.system().lower() or "unknown"
    gates: list[dict[str, Any]] = []

    if not python_info["supported"]:
        gates.append(
            {
                "gate": "python_runtime",
                "reason": "Python 3.10 or newer is required.",
                "requested_action": "install_or_select_python",
            }
        )
    if not writable:
        gates.append(
            {
                "gate": "workspace_write_access",
                "reason": write_error or "workspace is not writable",
                "requested_action": "select_or_authorize_workspace",
            }
        )
    if len(vaults) > 1:
        gates.append(
            {
                "gate": "vault_selection",
                "reason": "Multiple Obsidian-shaped vaults were found in the bounded source roots.",
                "choices": [str(path) for path in vaults],
                "requested_action": "select_vault_or_markdown_mode",
            }
        )

    if len(vaults) == 1:
        recommended_mode = "obsidian"
    else:
        recommended_mode = "markdown"

    data = {
        "workspace": str(workspace),
        "sources": [str(path) for path in sources],
        "platform": {
            "system": system,
            "release": platform.release(),
            "machine": platform.machine(),
            "shell": os.environ.get("SHELL") or os.environ.get("COMSPEC"),
            "non_ascii_workspace": not str(workspace).isascii(),
        },
        "python": python_info,
        "workspace_writable": writable,
        "obsidian": {
            **obsidian,
            "vault_candidates": [str(path) for path in vaults],
            "vault_count": len(vaults),
            "cli_optional": True,
        },
        "browser": {"python_webbrowser_available": True},
        "server": {
            "host": "127.0.0.1",
            "selected_port": selected_port,
            "preferred_port": preferred_port,
            "preferred_port_available": preferred_available,
        },
        "host_capability": {
            "level": "H2-inferred",
            "background_capability": "unknown",
            "background_adapter_available": system in {"darwin", "windows", "linux"},
        },
        "recommended_mode": recommended_mode,
        "installation_performed": False,
    }

    if gates:
        if any(gate["gate"] == "python_runtime" for gate in gates):
            code = "PYTHON_UNSUPPORTED"
        elif any(gate["gate"] == "workspace_write_access" for gate in gates):
            code = "WORKSPACE_NOT_WRITABLE"
        else:
            code = "MULTIPLE_VAULTS"
        return make_result(
            status="needs_user_input",
            code=code,
            message="Environment diagnosis completed with one or more user gates.",
            next_actions=[{"action": "resolve_gates_then_resume", "command": "doctor"}],
            needs_user_input=gates,
            data=data,
        ), 3

    return make_result(
        status="ok",
        code="DOCTOR_OK",
        message="Environment diagnosis completed without a blocking gate.",
        next_actions=[{"action": "initialize", "command": "init"}],
        data=data,
    ), 0

