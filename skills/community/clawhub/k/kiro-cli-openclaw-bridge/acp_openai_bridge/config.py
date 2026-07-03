"""Configuration module for ACP-to-OpenAI Bridge.

Handles command-line arguments, environment variables, and default settings.
Provides BridgeConfig dataclass, kiro-cli path discovery, and platform detection.
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BridgeConfig:
    """Bridge service configuration.

    Fields can be set via command-line arguments, environment variables,
    or left at their defaults.
    """

    host: str = "127.0.0.1"
    port: int = 18788
    kiro_cli_path: str | None = None  # None means auto-find
    cwd: str | None = None  # None means use current directory
    request_timeout: float = 300.0  # seconds
    model: str | None = None  # None means use kiro-cli default

    @classmethod
    def from_args_and_env(cls) -> BridgeConfig:
        """Build a BridgeConfig from command-line arguments and environment variables.

        Priority (highest → lowest):
        1. Command-line arguments (if explicitly provided)
        2. Environment variables
        3. Dataclass defaults
        """
        parser = argparse.ArgumentParser(
            description="ACP-to-OpenAI Bridge: local proxy translating OpenAI requests to ACP JSON-RPC",
        )
        parser.add_argument("--host", type=str, default=None, help="Host to bind (default: 127.0.0.1)")
        parser.add_argument("--port", type=int, default=None, help="Port to listen on (default: 18788)")
        parser.add_argument("--kiro-cli-path", type=str, default=None, help="Path to kiro-cli executable")
        parser.add_argument("--cwd", type=str, default=None, help="Working directory for ACP session")
        parser.add_argument("--timeout", type=float, default=None, help="Request timeout in seconds (default: 300)")
        parser.add_argument("--model", type=str, default=None, help="Model ID for kiro-cli acp (e.g. claude-opus-4.6)")

        args = parser.parse_args()

        # Resolve each field: CLI arg → env var → default
        defaults = cls()

        host = args.host or os.environ.get("ACP_BRIDGE_HOST") or defaults.host

        port_env = os.environ.get("ACP_BRIDGE_PORT")
        port = args.port if args.port is not None else (int(port_env) if port_env else defaults.port)

        kiro_cli_path = args.kiro_cli_path or os.environ.get("ACP_BRIDGE_KIRO_CLI_PATH") or defaults.kiro_cli_path

        cwd = args.cwd or os.environ.get("ACP_BRIDGE_CWD") or defaults.cwd

        timeout_env = os.environ.get("ACP_BRIDGE_TIMEOUT")
        request_timeout = (
            args.timeout
            if args.timeout is not None
            else (float(timeout_env) if timeout_env else defaults.request_timeout)
        )

        model = args.model or os.environ.get("ACP_BRIDGE_MODEL") or defaults.model

        return cls(
            host=host,
            port=port,
            kiro_cli_path=kiro_cli_path,
            cwd=cwd,
            request_timeout=request_timeout,
            model=model,
        )


def find_kiro_cli() -> str:
    """Auto-find the kiro-cli executable path.

    Search order:
    1. shutil.which("kiro-cli")  — honours PATH
    2. ~/.local/bin/kiro-cli     — common Linux / WSL location
    3. /opt/homebrew/bin/kiro-cli — macOS ARM (Homebrew)
    4. /usr/local/bin/kiro-cli   — macOS Intel (Homebrew)

    Returns:
        Absolute path to the kiro-cli executable.

    Raises:
        FileNotFoundError: If kiro-cli cannot be found in any known location.
    """
    # 1. PATH lookup
    which_result = shutil.which("kiro-cli")
    if which_result is not None:
        return str(Path(which_result).resolve())

    # 2-4. Well-known fallback paths
    fallback_paths = [
        Path.home() / ".local" / "bin" / "kiro-cli",
        Path("/opt/homebrew/bin/kiro-cli"),
        Path("/usr/local/bin/kiro-cli"),
    ]

    for candidate in fallback_paths:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate.resolve())

    raise FileNotFoundError(
        "kiro-cli executable not found. "
        "Please install kiro-cli or specify its path via --kiro-cli-path or ACP_BRIDGE_KIRO_CLI_PATH."
    )


def detect_platform() -> dict:
    """Detect current platform information.

    Returns:
        A dict with keys:
        - system:  platform.system() result (e.g. "Linux", "Darwin")
        - is_wsl:  True if running inside WSL (Windows Subsystem for Linux)
        - machine: platform.machine() result (e.g. "x86_64", "arm64")
    """
    system = platform.system()
    machine = platform.machine()

    is_wsl = False
    if system == "Linux":
        try:
            proc_version = Path("/proc/version").read_text()
            # WSL kernels contain "microsoft" or "WSL" in /proc/version
            lower = proc_version.lower()
            if "microsoft" in lower or "wsl" in lower:
                is_wsl = True
        except OSError:
            pass

    return {
        "system": system,
        "is_wsl": is_wsl,
        "machine": machine,
    }
