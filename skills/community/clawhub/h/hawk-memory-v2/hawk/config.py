"""
config.py — hawk 配置管理

功能：
- 从环境变量 / openclaw.json 读取配置
- 提供配置热重载
"""

import os
import json
import path


class Config:
    """hawk 配置"""

    DEFAULTS = {
        "db_path": "~/.hawk/lancedb",
        "memories_path": "~/.hawk/memories.json",
        "governance_path": "~/.hawk/governance.log",
        "openai_api_key": "",
        "embedding_model": "text-embedding-3-small",
        "embedding_dimensions": 1536,
        "recall_top_k": 5,
        "recall_min_score": 0.6,
        "capture_max_chunks": 3,
        "capture_importance_threshold": 0.5,
        "decay_rate": 0.95,
        "working_ttl_days": 1,
        "short_ttl_days": 7,
        "long_ttl_days": 90,
        "archive_ttl_days": 180,
    }

    def __init__(self, config_path: str = None):
        self._config = {**self.DEFAULTS}
        self.config_path = config_path or os.path.expanduser("~/.hawk/config.json")
        self._load()

    def _load(self):
        # 环境变量覆盖
        for key in ["OPENAI_API_KEY", "HAWK_DB_PATH", "HAWK_EMBEDDING_MODEL"]:
            if key in os.environ:
                self._config[key.lower()] = os.environ[key]

        # 配置文件
        if os.path.exists(self.config_path):
            with open(self.config_path) as f:
                user_config = json.load(f)
                self._config.update(user_config)

    def get(self, key: str, default=None):
        return self._config.get(key, default)

    def set(self, key: str, value):
        self._config[key] = value

    def save(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)

    def reload(self):
        self._load()
