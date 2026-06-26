"""配置读写模块（带类型标注）"""

import json
import os
from pathlib import Path
from typing import Any
from datetime import datetime


DEFAULT_CONFIG_DIR: Path = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "music-studio"
DEFAULT_OUTPUT_DIR: Path = Path(__file__).parent.parent / "output"

CONFIG_FILE: Path = DEFAULT_CONFIG_DIR / "config.json"


def ensure_config_dir() -> None:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_config() -> dict[str, Any]:
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE) as f:
        return json.load(f)


def save_config(data: dict[str, Any]) -> None:
    ensure_config_dir()
    data = dict(data)
    data["updated"] = _now()
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_config(patch: dict[str, Any]) -> dict[str, Any]:
    cfg = load_config()
    cfg.update(patch)
    save_config(cfg)
    return cfg


def remove_keys(*keys: str) -> dict[str, Any]:
    cfg = load_config()
    for key in keys:
        cfg.pop(key, None)
    save_config(cfg)
    return cfg


def get(key: str, default: Any = None) -> Any:
    return load_config().get(key, default)


def has_api_key() -> bool:
    cfg = load_config()
    return bool(str(cfg.get("api_key", "")).strip())


def get_api_key() -> str:
    cfg = load_config()
    key = cfg.get("api_key", "")
    if key:
        return str(key)
    raise RuntimeError(
        "API Key 为空，请运行 python -m music_studio set-key"
    )


def get_provider() -> str:
    return get("provider", "minimax")


def get_music_model() -> str:
    return get("music_model", "music-2.6")


def get_cover_model() -> str:
    return get("cover_model", "music-cover")


def get_output_dir() -> Path:
    """返回 output 目录，支持用户自定义"""
    cfg = load_config()
    custom: str = cfg.get("output_dir", "")
    if custom:
        p = Path(custom).expanduser().resolve()
        p.mkdir(parents=True, exist_ok=True)
        return p
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return DEFAULT_OUTPUT_DIR


def is_configured() -> bool:
    cfg = load_config()
    return bool(cfg.get("provider") and cfg.get("music_model") and cfg.get("cover_model"))


def is_ready() -> bool:
    return is_configured() and has_api_key()


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
