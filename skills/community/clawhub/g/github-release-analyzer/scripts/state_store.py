from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from models import RepoSpec, StateData


def _resolve_state_root() -> Path:
    """Resolve state storage directory.

    Priority:
    1. GITHUB_RELEASE_ANALYZER_STATE_ROOT env var
    2. Legacy workspace path (if existing state found, for backward compat)
    3. Persistent global path (survives skill upgrades)
    """
    env = os.environ.get("GITHUB_RELEASE_ANALYZER_STATE_ROOT")
    if env:
        return Path(env)

    home = Path.home()
    legacy = home / ".openclaw" / "workspace" / "state" / "github-release-analyzer"
    persistent = home / ".openclaw" / "state" / "github-release-analyzer"

    # If legacy path has existing state files, keep using it
    if legacy.exists() and any(legacy.iterdir()):
        return legacy

    return persistent


DEFAULT_STATE_ROOT = _resolve_state_root()


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def state_path(repo: RepoSpec, state_key: str | None = None) -> Path:
    key = state_key or repo.state_key
    return DEFAULT_STATE_ROOT / f"{key}.json"


def load_state(repo: RepoSpec, state_key: str | None = None) -> tuple[StateData, Path, bool]:
    path = state_path(repo, state_key)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        return StateData(repo=repo.slug), path, True

    data = json.loads(path.read_text(encoding="utf-8"))
    state = StateData(
        repo=data.get("repo", repo.slug),
        processed_tags=list(data.get("processed_tags", [])),
        latest_processed_release_id=data.get("latest_processed_release_id"),
        latest_processed_published_at=data.get("latest_processed_published_at"),
        last_checked_at=data.get("last_checked_at"),
        last_success_at=data.get("last_success_at"),
        initialized_at=data.get("initialized_at"),
    )
    is_first_run = not bool(state.initialized_at)
    return state, path, is_first_run


def save_state(path: Path, state: StateData) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
