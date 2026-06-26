"""
加载 JSON 配置，支持默认供应商与各供应商参数。
配置路径（优先级从高到低）：
  - 指定路径（函数参数 force_path / CLI --config）
  - 当前目录 package_tracker.json
"""

import json
from pathlib import Path
from typing import Any

_CONFIG_CACHE: dict[str, Any] | None = None


def _find_config_path() -> Path | None:
    cwd = Path.cwd()
    candidate = cwd / "package_tracker.json"
    if candidate.is_file():
        return candidate
    return None


def _load_json(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def load_config(force_path: str | Path | None = None, use_cache: bool = True) -> dict[str, Any]:
    """
    加载配置。返回结构：
      default: str   # 默认供应商名称
      providers: dict[str, dict]  # 供应商名 -> 该供应商的选项（如 ebusiness_id, api_key, sandbox）
    """
    global _CONFIG_CACHE
    if use_cache and _CONFIG_CACHE is not None and force_path is None:
        return _CONFIG_CACHE

    path: Path | None = None
    if force_path is not None:
        path = Path(force_path)
        if not path.is_file():
            raise FileNotFoundError(f"Config file not found: {path}")
    else:
        path = _find_config_path()

    if path is None:
        out = {"default": "kdniao", "providers": {}}
        if use_cache:
            _CONFIG_CACHE = out
        return out

    raw = _load_json(path)
    default = (raw.get("default") or "kdniao")
    if isinstance(default, str):
        default = default.strip().lower() or "kdniao"
    else:
        default = "kdniao"

    providers = raw.get("providers")
    if not isinstance(providers, dict):
        providers = {}

    out = {"default": default, "providers": {k.lower(): v if isinstance(v, dict) else {} for k, v in providers.items()}}
    if use_cache:
        _CONFIG_CACHE = out
    return out


def get_provider_options(provider_name: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
    """返回某供应商的选项字典（用于传给该 provider 的构造函数）。"""
    if config is None:
        config = load_config()
    name = provider_name.strip().lower()
    return dict(config.get("providers", {}).get(name, {}))

