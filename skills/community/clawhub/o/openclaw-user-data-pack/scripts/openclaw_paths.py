"""Shared path resolution for pack/apply scripts."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def openclaw_home() -> Path:
    env = os.environ.get("OPENCLAW_HOME", "")
    return Path(env).expanduser() if env else Path.home() / ".openclaw"


def load_openclaw_config(path: Path) -> dict | None:
    if not path.is_file():
        return None
    raw = path.read_text(encoding="utf-8", errors="replace")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        try:
            import json5  # type: ignore

            return json5.loads(raw)
        except ImportError:
            print(
                "error: openclaw.json is not strict JSON (likely JSON5). "
                "Install deps: pip install -r requirements.txt",
                file=sys.stderr,
            )
            return None
        except Exception as e:  # noqa: BLE001
            print(f"error: failed to parse {path}: {e}", file=sys.stderr)
            return None


def workspace_from_config(data: dict) -> str | None:
    agent = data.get("agent")
    if isinstance(agent, dict):
        w = agent.get("workspace")
        if isinstance(w, str) and w.strip():
            return w
    agents = data.get("agents")
    if isinstance(agents, dict):
        defaults = agents.get("defaults")
        if isinstance(defaults, dict):
            w = defaults.get("workspace")
            if isinstance(w, str) and w.strip():
                return w
    return None


def resolve_workspace(
    *,
    workspace: Path | None,
    openclaw_home_dir: Path,
    config_path: Path | None,
) -> Path:
    if workspace is not None:
        p = workspace.expanduser().resolve()
        if not p.is_dir():
            raise SystemExit(f"workspace is not a directory: {p}")
        return p

    cfg_file = config_path if config_path is not None else openclaw_home_dir / "openclaw.json"
    data = load_openclaw_config(cfg_file)
    if data:
        ws = workspace_from_config(data)
        if ws:
            p = Path(ws).expanduser().resolve()
            if p.is_dir():
                return p

    profile = os.environ.get("OPENCLAW_PROFILE", "default")
    if profile and profile != "default":
        candidate = (openclaw_home_dir / f"workspace-{profile}").resolve()
        if candidate.is_dir():
            return candidate

    default_ws = (openclaw_home_dir / "workspace").resolve()
    if default_ws.is_dir():
        return default_ws

    raise SystemExit(
        "Could not resolve workspace. Pass --workspace PATH or fix openclaw.json / install json5 for JSON5 configs."
    )
