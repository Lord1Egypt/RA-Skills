"""Locate a separately installed Audiveris executable without modifying the host."""

from __future__ import annotations

import os
import shutil
from pathlib import Path


def find_audiveris() -> tuple[str | None, str | None]:
    """Return ``(path, installation_kind)`` for a conventional local install.

    The paths cover the official macOS app bundle and the official Windows MSI
    default location.  Other installations remain supported when their
    executable is available on PATH.  This function never launches a process.
    """
    for command in ("audiveris", "Audiveris", "Audiveris.exe"):
        path = shutil.which(command)
        if path:
            return path, "command"

    candidates = [
        (Path("/Applications/Audiveris.app/Contents/MacOS/Audiveris"), "macos_app_bundle"),
        (Path.home() / "Applications/Audiveris.app/Contents/MacOS/Audiveris", "macos_app_bundle"),
    ]
    for variable in ("ProgramFiles", "ProgramW6432", "ProgramFiles(x86)"):
        root = os.environ.get(variable)
        if root:
            candidates.append((Path(root) / "Audiveris" / "Audiveris.exe", "windows_msi"))

    seen: set[Path] = set()
    for path, kind in candidates:
        if path in seen:
            continue
        seen.add(path)
        if path.is_file():
            return str(path), kind
    return None, None


def find_oemer() -> tuple[str | None, str | None]:
    """Return an already-installed Oemer CLI without installing Python packages."""
    for command in ("oemer", "oemer.exe"):
        path = shutil.which(command)
        if path:
            return path, "command"
    return None, None
