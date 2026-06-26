"""
Configuration Loader
"""
import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
import os


class Config:
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        
        self.config_path = Path(config_path)
        self._data: Dict[str, Any] = {}
        self._load()
    
    def _load(self):
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._data = yaml.safe_load(f) or {}
        else:
            # Default config
            self._data = self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        return {
            'STORAGE_BACKEND': 'local',
            'USE_EMBEDDING': False,
            'EMBEDDING_MODEL': 'sentence-transformers/all-MiniLM-L6-v2',
            'EMBEDDING_DIM': 384,
            'storage': {
                'local': {'base_path': './memory_data'},
                'github': {
                    'repo': '',
                    'branch': 'main',
                    'token_env': 'GITHUB_TOKEN',
                    'base_path': 'memory/'
                },
                'gitee': {
                    'repo': '',
                    'branch': 'master',
                    'token_env': 'GITEE_TOKEN',
                    'base_path': 'memory/'
                }
            },
            'DEFAULT_TOP_K': 5,
            'SIMILARITY_THRESHOLD': 0.7
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)
    
    def get_storage_config(self, backend: str = None) -> Dict[str, Any]:
        if backend is None:
            backend = self.get('STORAGE_BACKEND', 'local')
        return self.get('storage', {}).get(backend, {})
    
    def save(self):
        """Save current config to file"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self._data, f, allow_unicode=True, default_flow_style=False)
    
    def update(self, key: str, value: Any):
        self._data[key] = value
    
    def update_storage(self, backend: str, config: Dict[str, Any]):
        if 'storage' not in self._data:
            self._data['storage'] = {}
        self._data['storage'][backend] = config
        self._data['STORAGE_BACKEND'] = backend


# Global config instance
config = Config()
