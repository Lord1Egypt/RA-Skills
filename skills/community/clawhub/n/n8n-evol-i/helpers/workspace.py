import sys
from pathlib import Path

_DEFAULT_WS_NAME = "n8n-evol-I-workspace"
_announced = False


def workspace_root(override=None) -> Path:
    """Resolve the workspace root.

    Resolution order:
      1. ``--workspace`` override (explicit; honored as-is).
      2. ``cwd`` if its basename is ``n8n-evol-I-workspace`` — you're already inside.
      3. ``cwd/n8n-evol-I-workspace`` if it exists as a child directory.
      4. ``cwd/n8n-evol-I-workspace`` (default; ``init.py`` will create it here).

    Prints the resolved path to stderr once per process.
    """
    global _announced
    if override:
        path = Path(override).resolve()
    else:
        cwd = Path.cwd()
        if cwd.name == _DEFAULT_WS_NAME:
            path = cwd
        else:
            path = cwd / _DEFAULT_WS_NAME
        path = path.resolve()
    if not _announced:
        print(f"[n8n-evol-I] workspace: {path}", file=sys.stderr)
        _announced = True
    return path


def harness_root() -> Path:
    """Return the harness package root (parent of helpers/)."""
    return Path(__file__).parent.parent.resolve()


def ensure_workspace(path: Path) -> None:
    """Assert required workspace subdirs exist; raise SystemExit with actionable message otherwise."""
    required = [
        path / "n8n-config",
        path / "n8n-workflows-template",
    ]
    missing = [str(d) for d in required if not d.is_dir()]
    if missing:
        raise SystemExit(
            f"Workspace at {path} is incomplete or missing.\n"
            f"Missing: {', '.join(missing)}\n"
            "Run `python3 <harness>/helpers/init.py` first."
        )


def assert_not_in_harness(out_path: Path) -> None:
    """Raise RuntimeError if out_path would land inside the harness directory."""
    harness = harness_root()
    try:
        Path(out_path).resolve().relative_to(harness)
        raise RuntimeError(
            f"Refusing to write inside the harness directory: {out_path}\n"
            "Helpers must only write to workspace paths."
        )
    except ValueError:
        pass  # Not inside harness — good
