"""
配置管理模块
"""
import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

_config_cache: Optional[Dict[str, Any]] = None

CONFIG_FILE_NAME = "config.json"


def get_config_dir() -> Path:
    return Path(__file__).parent.parent


def load_config() -> Dict[str, Any]:
    global _config_cache
    
    if _config_cache is not None:
        return _config_cache
    
    config_path = get_config_dir() / CONFIG_FILE_NAME
    
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            _config_cache = json.load(f)
    else:
        _config_cache = {}
    
    return _config_cache


def save_config(config: Dict[str, Any]) -> None:
    global _config_cache
    
    config_path = get_config_dir() / CONFIG_FILE_NAME
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    _config_cache = config


def get_gui_agent_config() -> Dict[str, Any]:
    config = load_config()
    return config.get("gui_agent", {})


def get_api_key() -> Optional[str]:
    gui_config = get_gui_agent_config()
    api_key = gui_config.get("api_key")
    
    if not api_key:
        api_key = os.environ.get("DASHSCOPE_API_KEY")
    
    return api_key


def set_api_key(api_key: str, provider: str = "aliyun") -> None:
    config = load_config()
    
    if "gui_agent" not in config:
        config["gui_agent"] = {}
    
    config["gui_agent"]["api_key"] = api_key
    config["gui_agent"]["provider"] = provider
    
    save_config(config)


def get_game_config(game_name: str) -> Dict[str, Any]:
    config = load_config()
    games = config.get("games", {})
    return games.get(game_name, {})


def get_screenshot_config() -> Dict[str, Any]:
    config = load_config()
    return config.get("screenshot", {
        "save_dir": "screenshots",
        "format": "png"
    })
