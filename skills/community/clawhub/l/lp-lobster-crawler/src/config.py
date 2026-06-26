"""YAML 配置加载系统。

全局配置从 config/settings.yaml 加载，站点配置从 config/sites/*.yaml 加载。
环境变量优先级高于 YAML 文件。
"""

import os
from pathlib import Path
from typing import Any

import yaml


_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_SETTINGS_PATH = _PROJECT_ROOT / "config" / "settings.yaml"
_DEFAULT_SITES_DIR = _PROJECT_ROOT / "config" / "sites"

_config_cache: dict[str, Any] | None = None
_sites_cache: dict[str, dict[str, Any]] | None = None


def load_yaml(path: str | Path) -> dict[str, Any]:
    """加载单个 YAML 文件。

    Args:
        path: YAML 文件路径。

    Returns:
        解析后的字典。

    Raises:
        FileNotFoundError: 文件不存在。
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_settings(path: str | Path | None = None, force_reload: bool = False) -> dict[str, Any]:
    """加载全局配置。

    Args:
        path: settings.yaml 路径，为 None 时使用默认路径。
        force_reload: 强制重新加载，忽略缓存。

    Returns:
        全局配置字典。
    """
    global _config_cache
    if _config_cache is not None and not force_reload:
        return _config_cache

    settings_path = Path(path) if path else _DEFAULT_SETTINGS_PATH
    config = load_yaml(settings_path)

    # 环境变量覆盖
    if os.environ.get("DB_PATH"):
        config.setdefault("database", {})["path"] = os.environ["DB_PATH"]
    if os.environ.get("LOG_LEVEL"):
        config.setdefault("scrapy", {})["log_level"] = os.environ["LOG_LEVEL"]

    _config_cache = config
    return config


def load_site_config(site_name: str, sites_dir: str | Path | None = None) -> dict[str, Any]:
    """加载单个站点配置。

    Args:
        site_name: 站点名称（不含 .yaml 后缀）。
        sites_dir: 站点配置目录路径。

    Returns:
        站点配置字典。
    """
    directory = Path(sites_dir) if sites_dir else _DEFAULT_SITES_DIR
    path = directory / f"{site_name}.yaml"
    return load_yaml(path)


def load_all_sites(sites_dir: str | Path | None = None, force_reload: bool = False) -> dict[str, dict[str, Any]]:
    """加载所有站点配置。

    Args:
        sites_dir: 站点配置目录路径。
        force_reload: 强制重新加载。

    Returns:
        {站点名: 站点配置字典} 映射。
    """
    global _sites_cache
    if _sites_cache is not None and not force_reload:
        return _sites_cache

    directory = Path(sites_dir) if sites_dir else _DEFAULT_SITES_DIR
    sites = {}
    if directory.exists():
        for yaml_file in sorted(directory.glob("*.yaml")):
            name = yaml_file.stem
            sites[name] = load_yaml(yaml_file)

    _sites_cache = sites
    return sites


def get_setting(*keys: str, default: Any = None) -> Any:
    """按路径获取全局配置值。

    Args:
        *keys: 配置路径键序列，如 get_setting("database", "path")。
        default: 键不存在时的默认值。

    Returns:
        配置值或默认值。
    """
    config = load_settings()
    current = config
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def clear_cache() -> None:
    """清除配置缓存。"""
    global _config_cache, _sites_cache
    _config_cache = None
    _sites_cache = None
