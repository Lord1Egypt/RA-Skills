"""Location and permissions of the skill's local state.

Everything the skill persists (key, config, journal, kill switch) lives under a
single 0700 directory owned by the user. Nothing is written into the skill
directory, which is replaced on every `openclaw skills update`.
"""
from __future__ import annotations

import os
import stat
from pathlib import Path

APP_DIR_ENV = "POLYMARKET_AGENT_HOME"


def app_dir() -> Path:
    """State directory (0700). Created on demand."""
    override = os.environ.get(APP_DIR_ENV)
    if override:
        base = Path(override).expanduser()
    else:
        base = Path.home() / ".openclaw" / "polymarket-agent"
    base.mkdir(parents=True, exist_ok=True)
    harden_dir(base)
    return base


def keystore_path() -> Path:
    return app_dir() / "keystore.json"


def config_path() -> Path:
    return app_dir() / "config.json"


def journal_path() -> Path:
    return app_dir() / "journal.jsonl"


def halt_path() -> Path:
    """Kill switch: if it exists, NO order is ever sent."""
    return app_dir() / "HALT"


def harden_dir(path: Path) -> None:
    """0700 — owner-only read/enter. Best-effort (no-op on Windows)."""
    try:
        os.chmod(path, stat.S_IRWXU)
    except (OSError, NotImplementedError):
        pass


def harden_file(path: Path) -> None:
    """0600 — owner-only read/write. Best-effort (no-op on Windows)."""
    try:
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except (OSError, NotImplementedError):
        pass


def write_private(path: Path, data: str) -> None:
    """Write with 0600 from CREATION onwards — no window in which the file
    exists with default permissions (prevents another user reading it between
    the open() and the chmod())."""
    path.parent.mkdir(parents=True, exist_ok=True)
    harden_dir(path.parent)
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    fd = os.open(str(path), flags, stat.S_IRUSR | stat.S_IWUSR)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(data)
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass
        raise
    harden_file(path)


class trade_lock:
    """Mutual exclusion across processes while evaluating-and-sending an order.

    BUG FIX (found in review): the spend caps are computed by reading the
    journal, and only afterwards is the order written. Two concurrent
    `poly buy` runs (or the agent and the user at the same time) read the same
    consumed balance and both passed — busting the daily cap without either one
    violating the rule on its own.

    `flock` is released by the kernel if the process dies, so a crash does not
    leave the skill wedged. On platforms without `fcntl` it degrades to a no-op:
    the guarantee is lost, but usage is not blocked.
    """

    def __init__(self, timeout: float = 10.0) -> None:
        self._timeout = timeout
        self._handle = None

    def __enter__(self) -> "trade_lock":
        try:
            import fcntl
        except ImportError:  # pragma: no cover - Windows
            return self

        import time

        path = app_dir() / "trade.lock"
        self._handle = open(path, "w", encoding="utf-8")
        harden_file(path)
        deadline = time.monotonic() + self._timeout
        while True:
            try:
                fcntl.flock(self._handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except OSError:
                if time.monotonic() >= deadline:
                    self._handle.close()
                    self._handle = None
                    raise TimeoutError(
                        "another order operation is in progress; try again"
                    )
                time.sleep(0.1)

    def __exit__(self, *exc_info: object) -> None:
        if self._handle is None:
            return
        try:
            import fcntl

            fcntl.flock(self._handle.fileno(), fcntl.LOCK_UN)
        except (ImportError, OSError):
            pass
        finally:
            self._handle.close()
            self._handle = None


def check_permissions(path: Path) -> str | None:
    """Return a warning if the file is readable by group/others."""
    try:
        mode = path.stat().st_mode
    except OSError:
        return None
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        return (
            f"{path} is accessible to other users "
            f"(mode {stat.filemode(mode)}). Fix it with: chmod 600 {path}"
        )
    return None
