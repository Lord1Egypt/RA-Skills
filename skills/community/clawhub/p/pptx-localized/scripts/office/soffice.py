"""
Helper for running LibreOffice (soffice) on Windows.

Windows notes:
  - AF_UNIX sockets are NOT blocked on Windows, so the LD_PRELOAD shim
    used on Linux sandboxes is NOT needed.
  - This script simply delegates to `soffice` (or `soffice.exe`) via subprocess.
  - Set `SOFFICE_PATH` env var if soffice is not on your PATH.

Usage:
    from office.soffice import run_soffice, get_soffice_env

    env = get_soffice_env()
    result = subprocess.run(["soffice", "--headless", ...], env=env)

    # Or use the helper directly:
    result = run_soffice(["--headless", "--convert-to", "pdf", "input.docx"])
"""

import os
import subprocess
import sys

def _find_soffice() -> str:
    """Find soffice executable."""
    # 1. Check env override
    env_path = os.environ.get("SOFFICE_PATH", "")
    if env_path and os.path.isfile(env_path):
        return env_path

    # 2. Try "soffice" / "soffice.exe" from PATH
    for name in ("soffice.exe", "soffice", "libreoffice.exe", "libreoffice"):
        try:
            subprocess.run(
                [name, "--version"],
                capture_output=True, timeout=10
            )
            return name
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    # 3. Common Windows install locations
    program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
    program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
    for base in (program_files, program_files_x86):
        for root in (base, os.path.join(base, "LibreOffice")):
            for version_dir in ("program", ""):
                candidate = os.path.join(root, version_dir, "soffice.exe")
                if os.path.isfile(candidate):
                    return candidate

    return "soffice"  # fallback; will fail with a clear error


_SOFFICE_CMD = _find_soffice()


def get_soffice_env() -> dict:
    """
    Return an env dict suitable for calling soffice.
    On Windows, no special LD_PRELOAD / SAL_USE_VCLPLUGIN tricks are needed.
    """
    env = os.environ.copy()
    # SAL_USE_VCLPLUGIN=svp can help on some headless Linux setups;
    # on Windows it is harmless but usually unnecessary. Keep for compatibility.
    env["SAL_USE_VCLPLUGIN"] = env.get("SAL_USE_VCLPLUGIN", "svp")
    return env


def run_soffice(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    """
    Run LibreOffice with the given arguments.
    Returns subprocess.CompletedProcess.
    """
    cmd = [_SOFFICE_CMD] + list(args)
    env = get_soffice_env()
    return subprocess.run(cmd, env=env, **kwargs)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python soffice.py [--headless] [--convert-to FORMAT] FILE ...",
            file=sys.stderr,
        )
        sys.exit(1)
    result = run_soffice(sys.argv[1:], capture_output=False)
    sys.exit(result.returncode)
