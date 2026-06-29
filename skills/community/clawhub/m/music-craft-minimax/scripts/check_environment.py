#!/usr/bin/env python3
"""Lightweight environment check for the OpenClaw MiniMax workflow.

This script is intentionally standard-library only and avoids importing any
heavy audio dependencies. Optional Python packages are checked with
importlib.util.find_spec so the script remains fast and safe to run in minimal
environments.
"""

from __future__ import annotations

import importlib.util
import os
import platform
import shutil
import subprocess
import sys


REQUIRED_PYTHON = (3, 9)
REQUIRED_ENV_VAR = "MINIMAX_API_KEY"
PATH_EXECUTABLES = ("ffmpeg", "mmx")
OPTIONAL_IMPORTS = (
    "librosa",
    "numpy",
    "scipy",
    "parselmouth",
    "demucs",
    "torch",
    "transformers",
)


def _status(ok: bool) -> str:
    return "OK" if ok else "MISSING"


def _print_group(title: str) -> None:
    print(f"\n{title}")
    print("-" * len(title))


def _check_python_version() -> tuple[bool, str]:
    current = sys.version_info[:3]
    ok = current >= REQUIRED_PYTHON
    details = f"Python {current[0]}.{current[1]}.{current[2]}"
    if not ok:
        details += f" (requires >= {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]})"
    return ok, details


def _check_env_var(name: str) -> tuple[bool, str]:
    present = bool(os.environ.get(name))
    return present, f"{name}: {_status(present)}"


def _check_executable(name: str) -> tuple[bool, str]:
    path = shutil.which(name)
    if path:
        return True, f"{name}: OK ({path})"
    return False, f"{name}: MISSING"


def _probe_mmx_version() -> str:
    mmx_path = shutil.which("mmx")
    if not mmx_path:
        return "mmx version: unavailable (mmx missing)"

    probes = (
        [mmx_path, "--version"],
        [mmx_path, "-v"],
        [mmx_path, "version"],
    )
    for probe in probes:
        try:
            result = subprocess.run(
                probe,
                text=True,
                capture_output=True,
                timeout=5,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        text = (result.stdout or result.stderr).strip()
        if result.returncode == 0 and text:
            return f"mmx version: {text.splitlines()[0]}"
    return f"mmx version: unknown (path: {mmx_path})"


def _check_import(name: str) -> tuple[bool, str]:
    available = importlib.util.find_spec(name) is not None
    return available, f"{name}: {_status(available)}"


def main() -> int:
    system = platform.system() or "Unknown"
    release = platform.release() or "Unknown"
    python_ok, python_details = _check_python_version()
    key_ok, key_details = _check_env_var(REQUIRED_ENV_VAR)

    print("OpenClaw MiniMax environment check")
    print(f"Platform: {system} {release}")
    print(f"Interpreter: {sys.executable}")

    _print_group("Required")
    print(python_details)
    print(key_details)
    if system.lower() == "windows":
        print("Windows hint: open a new terminal after setting environment variables.")
        print("Windows hint: use `Get-Command ffmpeg, mmx` in PowerShell to verify PATH.")

    _print_group("Recommended")
    for executable in PATH_EXECUTABLES:
        ok, details = _check_executable(executable)
        print(details)
        if system.lower() == "windows" and not ok:
            if executable == "ffmpeg":
                print("  Hint: install via `winget install Gyan.FFmpeg` or add FFmpeg to PATH.")
            elif executable == "mmx":
                print("  Hint: install the MiniMax CLI and restart the terminal so PATH updates apply.")
    print(_probe_mmx_version())

    _print_group("Optional advanced")
    for package in OPTIONAL_IMPORTS:
        ok, details = _check_import(package)
        print(details)

    print("\nSummary")
    print("-------")
    print(f"Required basics: {_status(python_ok and key_ok)}")
    if not python_ok:
        print("Python version is too old. Upgrade to Python 3.9 or newer.")
    if not key_ok:
        print("MINIMAX_API_KEY is missing. Export it before using MiniMax features.")

    return 0 if python_ok and key_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
