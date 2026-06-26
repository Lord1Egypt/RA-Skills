from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from paths import detect_runtime, ensure_skill_dirs, get_backup_dir

OPENAI_PROFILE_KEY = 'openai-codex:default'
JsonDict = Dict[str, Any]


class AuthFileError(RuntimeError):
    pass


def _auth_profiles_path() -> Path:
    runtime = detect_runtime()
    path = runtime.get('auth_profiles_path')
    if not path:
        raise AuthFileError('auth_profiles_path not discovered; set OPENCLAW_ROOT or OPENCLAW_AGENT_ROOT')
    return Path(path)


def load_json_file(path: Path) -> JsonDict:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except FileNotFoundError as e:
        raise AuthFileError(f'file not found: {path}') from e
    except json.JSONDecodeError as e:
        raise AuthFileError(f'invalid json: {path}: {e}') from e


def save_json_atomic(path: Path, data: JsonDict) -> None:
    tmp_path = path.with_suffix(path.suffix + '.tmp')
    tmp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    tmp_path.replace(path)


def load_auth_profiles_file() -> JsonDict:
    return load_json_file(_auth_profiles_path())


def save_auth_profiles_file(data: JsonDict) -> None:
    save_json_atomic(_auth_profiles_path(), data)


def get_openai_default_profile(data: JsonDict) -> JsonDict:
    profiles = data.get('profiles') or {}
    profile = profiles.get(OPENAI_PROFILE_KEY)
    if not isinstance(profile, dict):
        raise AuthFileError(f'missing profile: {OPENAI_PROFILE_KEY}')
    return profile


def replace_openai_default_profile(data: JsonDict, new_profile: JsonDict) -> JsonDict:
    cloned = json.loads(json.dumps(data))
    cloned.setdefault('profiles', {})[OPENAI_PROFILE_KEY] = new_profile
    return cloned


def backup_auth_profiles_file() -> Path:
    ensure_skill_dirs()
    src = _auth_profiles_path()
    if not src.exists():
        raise AuthFileError(f'auth file not found: {src}')
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
    dest = get_backup_dir() / f'auth-profiles.json.bak.{ts}'
    shutil.copy2(src, dest)
    return dest


def restore_auth_profiles_file(backup_file: Path) -> None:
    if not backup_file.exists():
        raise AuthFileError(f'backup not found: {backup_file}')
    shutil.copy2(backup_file, _auth_profiles_path())
