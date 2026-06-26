from __future__ import annotations

import os
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
SKILL_DATA_DIR = SKILL_ROOT / 'skill-data'
DEFAULT_STATE_BASE_DIR = SKILL_DATA_DIR
ENV_STATE_BASE = os.environ.get('OPENAI_AUTH_SWITCHER_PUBLIC_STATE_DIR')
STATE_BASE_DIR = Path(os.path.expanduser(ENV_STATE_BASE)).resolve() if ENV_STATE_BASE else DEFAULT_STATE_BASE_DIR
STATE_DIR = STATE_BASE_DIR / 'state'
RUNTIME_DIR = STATE_BASE_DIR / 'runtime'
PROFILES_DIR = STATE_BASE_DIR / 'profiles'
BACKUP_DIR = STATE_DIR / 'backups'


def _expand(path: str | Path | None) -> Path | None:
    if path is None:
        return None
    return Path(os.path.expanduser(str(path))).resolve()


def discover_openclaw_root() -> Path | None:
    candidates: list[Path] = []
    env_root = os.environ.get('OPENCLAW_ROOT')
    if env_root:
        p = _expand(env_root)
        if p:
            candidates.append(p)

    home_default = _expand('~/.openclaw')
    env_home = os.environ.get('HOME')
    root_default = Path('/root/.openclaw') if env_home == '/root' else None
    if home_default:
        candidates.append(home_default)
    if root_default is not None:
        candidates.append(root_default)

    seen = set()
    for candidate in candidates:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        if candidate.exists() and candidate.is_dir():
            return candidate
    return None


def discover_workspace(openclaw_root: Path | None = None) -> Path | None:
    env_workspace = os.environ.get('OPENCLAW_WORKSPACE')
    if env_workspace:
        p = _expand(env_workspace)
        if p and p.exists():
            return p

    if openclaw_root is not None:
        p = openclaw_root / 'workspace'
        if p.exists():
            return p

    cwd = Path.cwd()
    if (cwd / 'AGENTS.md').exists() or (cwd / 'MEMORY.md').exists():
        return cwd
    return None


def discover_agent_root(openclaw_root: Path | None = None) -> Path | None:
    env_agent_root = os.environ.get('OPENCLAW_AGENT_ROOT')
    if env_agent_root:
        p = _expand(env_agent_root)
        if p and p.exists():
            return p
    if openclaw_root is None:
        return None
    p = openclaw_root / 'agents' / 'main' / 'agent'
    return p if p.exists() else None


def discover_session_root(openclaw_root: Path | None = None) -> Path | None:
    env_session_root = os.environ.get('OPENCLAW_SESSION_ROOT')
    if env_session_root:
        p = _expand(env_session_root)
        if p and p.exists():
            return p
    if openclaw_root is None:
        return None
    p = openclaw_root / 'agents' / 'main' / 'sessions'
    return p if p.exists() else None


def get_auth_profiles_path(agent_root: Path | None) -> Path | None:
    if agent_root is None:
        return None
    p = agent_root / 'auth-profiles.json'
    return p if p.exists() else p


def get_models_path(agent_root: Path | None) -> Path | None:
    if agent_root is None:
        return None
    p = agent_root / 'models.json'
    return p if p.exists() else p


def get_skill_root() -> Path:
    return SKILL_ROOT


def get_state_base_dir() -> Path:
    return STATE_BASE_DIR


def get_state_dir() -> Path:
    return STATE_DIR


def get_runtime_dir() -> Path:
    return RUNTIME_DIR


def get_profiles_dir() -> Path:
    return PROFILES_DIR


def get_backup_dir() -> Path:
    return BACKUP_DIR


def ensure_skill_dirs() -> None:
    for path in (STATE_DIR, RUNTIME_DIR, PROFILES_DIR, BACKUP_DIR):
        path.mkdir(parents=True, exist_ok=True)


def get_sessions_dir() -> Path | None:
    runtime = detect_runtime()
    path = runtime.get('session_root')
    return Path(path) if path else None


def detect_runtime() -> dict:
    openclaw_root = discover_openclaw_root()
    workspace = discover_workspace(openclaw_root)
    agent_root = discover_agent_root(openclaw_root)
    session_root = discover_session_root(openclaw_root)
    auth_profiles = get_auth_profiles_path(agent_root)
    models_path = get_models_path(agent_root)
    return {
        'openclaw_root': str(openclaw_root) if openclaw_root else None,
        'workspace': str(workspace) if workspace else None,
        'agent_root': str(agent_root) if agent_root else None,
        'session_root': str(session_root) if session_root else None,
        'auth_profiles_path': str(auth_profiles) if auth_profiles else None,
        'auth_profiles_exists': bool(auth_profiles and auth_profiles.exists()),
        'models_path': str(models_path) if models_path else None,
        'models_exists': bool(models_path and models_path.exists()),
    }
