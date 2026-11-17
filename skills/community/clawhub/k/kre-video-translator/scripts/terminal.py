"""Launch a visible, user-owned terminal for hidden API-key input."""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys


def input_available() -> bool:
    if sys.stdin.isatty():
        return True
    device = "CONIN$" if os.name == "nt" else "/dev/tty"
    try:
        descriptor = os.open(device, os.O_RDONLY)
    except OSError:
        return False
    os.close(descriptor)
    return True


def command_text(argv: list[str], *, windows: bool | None = None) -> str:
    use_windows = os.name == "nt" if windows is None else windows
    if use_windows:
        return "& " + " ".join("'" + argument.replace("'", "''") + "'" for argument in argv)
    return shlex.join(argv)


def launch(argv: list[str]) -> bool:
    if os.environ.get("SSH_CONNECTION") or os.environ.get("SSH_TTY"):
        return False
    try:
        if os.name == "nt":
            subprocess.Popen(argv, creationflags=subprocess.CREATE_NEW_CONSOLE)
            return True
        if sys.platform == "darwin":
            command = command_text(argv).replace("\\", "\\\\").replace('"', '\\"')
            subprocess.run(
                ["osascript", "-e", f'tell application "Terminal"\nactivate\ndo script "{command}"\nend tell'],
                check=True, capture_output=True, timeout=15,
            )
            return True
        if not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
            return False
        for name, separator in (("gnome-terminal", "--"), ("konsole", "-e"), ("xfce4-terminal", "-x"), ("x-terminal-emulator", "-e"), ("xterm", "-e")):
            if executable := shutil.which(name):
                subprocess.Popen([executable, separator, *argv])
                return True
    except (OSError, subprocess.SubprocessError):
        return False
    return False
