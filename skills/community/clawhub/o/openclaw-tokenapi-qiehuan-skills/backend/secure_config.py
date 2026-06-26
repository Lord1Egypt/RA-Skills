import json
import os
from typing import Dict, Optional
from cryptography.fernet import Fernet


class SecureConfig:
    _instance = None
    _cipher = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if SecureConfig._cipher is not None:
            return
        key_file = self._get_key_file()
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            os.makedirs(os.path.dirname(key_file), exist_ok=True)
            with open(key_file, "wb") as f:
                f.write(key)
        SecureConfig._cipher = Fernet(key)
        self.config_path = os.path.join(
            os.path.expanduser("~"), ".openclaw", "secure_config.json"
        )
        self.config = self._load_config()

    def _get_key_file(self) -> str:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        venv_root = os.path.dirname(script_dir)
        return os.path.join(venv_root, ".secure_key")

    def _load_config(self) -> Dict:
        if not os.path.exists(self.config_path):
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            default_config = {"providers": {}}
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            return default_config
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_config(self) -> bool:
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[SecureConfig] 保存失败: {e}")
            return False

    def save_provider(self, provider_id: str, config: Dict) -> bool:
        try:
            if "providers" not in self.config:
                self.config["providers"] = {}
            encrypted_apikey = SecureConfig._cipher.encrypt(
                config.get("apiKey", "").encode()
            ).decode()
            self.config["providers"][provider_id] = {
                "baseUrl": config.get("baseUrl", ""),
                "apiKey": encrypted_apikey,
                "contextWindow": config.get("contextWindow", 64000),
                "maxTokens": config.get("maxTokens", 8000),
            }
            return self._save_config()
        except Exception as e:
            print(f"[SecureConfig] 保存提供商配置失败: {e}")
            return False

    def get_provider(self, provider_id: str) -> Optional[Dict]:
        try:
            if provider_id not in self.config.get("providers", {}):
                return None
            provider = self.config["providers"][provider_id]
            decrypted_apikey = SecureConfig._cipher.decrypt(
                provider["apiKey"].encode()
            ).decode()
            return {
                "baseUrl": provider["baseUrl"],
                "apiKey": decrypted_apikey,
                "contextWindow": provider.get("contextWindow", 64000),
                "maxTokens": provider.get("maxTokens", 8000),
            }
        except Exception as e:
            print(f"[SecureConfig] 获取提供商配置失败: {e}")
            return None

    def get_all_providers(self) -> Dict:
        providers = {}
        for provider_id, provider in self.config.get("providers", {}).items():
            providers[provider_id] = {
                "baseUrl": provider["baseUrl"],
                "contextWindow": provider.get("contextWindow", 64000),
                "maxTokens": provider.get("maxTokens", 8000),
            }
        return providers

    def delete_provider(self, provider_id: str) -> bool:
        try:
            if "providers" in self.config and provider_id in self.config["providers"]:
                del self.config["providers"][provider_id]
                return self._save_config()
            return False
        except Exception as e:
            print(f"[SecureConfig] 删除提供商配置失败: {e}")
            return False
