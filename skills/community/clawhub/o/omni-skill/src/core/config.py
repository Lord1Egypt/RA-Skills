import os
import yaml
import json
import logging
from typing import Dict, Any, Optional

class ConfigManager:
    def __init__(self, default_config_path: str = "config.yaml"):
        self.default_config_path = default_config_path
        self.config: Dict[str, Any] = {}
        self._backup_config: Dict[str, Any] = {}

    def load_config(self, path: Optional[str] = None) -> None:
        """Load configuration from YAML/JSON and override with env variables."""
        target_path = path or self.default_config_path
        
        try:
            if os.path.exists(target_path):
                with open(target_path, 'r', encoding='utf-8') as f:
                    if target_path.endswith('.yaml') or target_path.endswith('.yml'):
                        self.config = yaml.safe_load(f) or {}
                    elif target_path.endswith('.json'):
                        self.config = json.load(f) or {}
            else:
                logging.warning(f"Config file {target_path} not found. Using empty config.")
                self.config = {}

            self._apply_env_overrides()
            self._validate_config()
            self._backup_config = dict(self.config)  # Save for rollback
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            self.rollback()
            raise

    def _apply_env_overrides(self):
        """Override configuration with environment variables (Prefix: OMNI_)."""
        prefix = "OMNI_"
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                self.config[config_key] = value

    def _validate_config(self):
        """Basic configuration validation."""
        # e.g., Ensure required fields exist
        pass

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def rollback(self):
        """Rollback to the last known good configuration."""
        logging.info("Rolling back configuration.")
        self.config = dict(self._backup_config)
