#!/usr/bin/env python3
"""
Configuration loader for Paper Management System

Supports multiple config sources (in order of precedence):
1. config.yaml in project directory
2. Environment variables with PAPERMGR_ prefix
3. Default values (relative to project directory)

Usage:
    from config import get_config
    cfg = get_config()
    db_path = cfg.db_path
"""

import os
import yaml
from pathlib import Path
from typing import Any, Optional

# Detect project directory (parent of scripts/)
_PROJECT_DIR = Path(__file__).parent.parent.resolve()

# Default configuration values (relative to project directory)
DEFAULTS = {
    "database.path": str(_PROJECT_DIR / "data" / "index.db"),
    "papers.dir": str(_PROJECT_DIR / "papers"),
    "papers.extensions": [".pdf"],
    "downloads.dir": str(_PROJECT_DIR / "downloads"),
    "downloads.keywords": ["科研通", "ablesci"],
    "logging.path": str(_PROJECT_DIR / "logs" / "auto_index.log"),
    "logging.level": "INFO",
    "ai.enabled": False,
    "ai.provider": "openai",
    "ai.model": "gpt-3.5-turbo",
    "ai.api_key": "",
    "ai.max_text_length": 50000,
    "notification.enabled": False,
    "notification.cmd": "",
}


class Config:
    """Configuration manager with environment variable override support"""
    
    _instance: Optional['Config'] = None
    _config: dict = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance
    
    def _load(self):
        self._config = DEFAULTS.copy()
        
        config_paths = [
            Path(__file__).parent / "config.yaml",
            Path(__file__).parent.parent / "config.yaml",
        ]
        
        for path in config_paths:
            if path.exists():
                with open(path, 'r') as f:
                    file_config = yaml.safe_load(f)
                    if file_config:
                        self._merge_config(self._config, file_config)
                break
        
        for key in list(self._config.keys()):
            env_key = f"PAPERMGR_{key.upper().replace('.', '_')}"
            if env_key in os.environ:
                value = os.environ[env_key]
                default_value = self._config.get(key)
                if isinstance(default_value, bool):
                    value = value.lower() in ('true', '1', 'yes')
                elif isinstance(default_value, list):
                    value = value.split(',')
                self._config[key] = value
    
    def _merge_config(self, base: dict, override: dict):
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)
    
    @property
    def db_path(self) -> str:
        return self.get("database.path")
    
    @property
    def papers_dir(self) -> str:
        return self.get("papers.dir")
    
    @property
    def downloads_dir(self) -> str:
        return self.get("downloads.dir")
    
    @property
    def notification_cmd(self) -> str:
        return self.get("notification.cmd")
    
    @property
    def notification_enabled(self) -> bool:
        return self.get("notification.enabled")
    
    @property
    def ai_enabled(self) -> bool:
        return self.get("ai.enabled")
    
    @property
    def ai_api_key(self) -> str:
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            api_key = self.get("ai.api_key", "")
        return api_key


def get_config() -> Config:
    return Config()
