# -*- coding: utf-8 -*-
"""
配置加载器
自动读取 private/ 目录配置，优先级：环境变量 > private/ > 默认值
"""

import os
import re
from pathlib import Path
from typing import Optional, Dict, Any


class ConfigLoader:
    """配置加载器 - 统一管理 API Keys 和 TTS 配置"""

    # 配置文件的预期映射
    CONFIG_FILES = {
        "doubao": ["research Agent.txt", "content Agent.txt"],
        "tts": ["TTS.txt"],
    }

    def __init__(self, private_dir: Optional[Path] = None):
        """
        初始化配置加载器

        Args:
            private_dir: private 目录路径，默认使用 ../private
        """
        if private_dir is None:
            self.private_dir = Path(__file__).parent.parent / "private"
        else:
            self.private_dir = private_dir

        self._config: Dict[str, Any] = {}
        self._loaded = False

    def load(self) -> Dict[str, Any]:
        """
        加载所有配置

        Returns:
            配置字典，包含 doubao_api_key, tts_app_id, tts_access_token 等
        """
        if self._loaded:
            return self._config

        self._config = {
            "doubao_api_key": self._load_doubao_key(),
            "tts_app_id": self._load_tts_app_id(),
            "tts_access_token": self._load_tts_access_token(),
            "tts_secret_key": self._load_tts_secret_key(),
        }

        self._loaded = True
        return self._config

    def _load_doubao_key(self) -> Optional[str]:
        """加载 Doubao API Key"""
        # 1. 检查环境变量
        if key := os.getenv("DOUBAO_API_KEY"):
            return key

        # 2. 尝试从 private/ 目录读取
        for filename in self.CONFIG_FILES["doubao"]:
            filepath = self.private_dir / filename
            if filepath.exists():
                key = self._extract_api_key(filepath)
                if key:
                    # 设置环境变量供其他模块使用
                    os.environ["DOUBAO_API_KEY"] = key
                    return key

        return None

    def _load_tts_app_id(self) -> Optional[str]:
        """加载 TTS App ID"""
        if key := os.getenv("VOLCANO_TTS_APP_ID"):
            return key

        filepath = self.private_dir / "TTS.txt"
        if filepath.exists():
            app_id = self._extract_field(filepath, r"APP\s*ID[：:]\s*(\d+)")
            if app_id:
                os.environ["VOLCANO_TTS_APP_ID"] = app_id
                return app_id

        return None

    def _load_tts_access_token(self) -> Optional[str]:
        """加载 TTS Access Token"""
        if key := os.getenv("VOLCANO_TTS_ACCESS_TOKEN"):
            return key

        filepath = self.private_dir / "TTS.txt"
        if filepath.exists():
            token = self._extract_field(filepath, r"Access\s*Token[：:]\s*([a-zA-Z0-9_-]+)")
            if token:
                os.environ["VOLCANO_TTS_ACCESS_TOKEN"] = token
                return token

        return None

    def _load_tts_secret_key(self) -> Optional[str]:
        """加载 TTS Secret Key"""
        if key := os.getenv("VOLCANO_TTS_SECRET_KEY"):
            return key

        filepath = self.private_dir / "TTS.txt"
        if filepath.exists():
            key = self._extract_field(filepath, r"secret\s*key[：:]\s*([a-zA-Z0-9_-]+)")
            if key:
                os.environ["VOLCANO_TTS_SECRET_KEY"] = key
                return key

        return None

    def _extract_api_key(self, filepath: Path) -> Optional[str]:
        """从文件中提取 API Key（通用格式）"""
        try:
            content = filepath.read_text(encoding="utf-8")

            # 尝试多种格式
            patterns = [
                r"API\s*[Kk]ey[：:]\s*([a-zA-Z0-9_-]+)",
                r"api[_\-]?key[：:]\s*([a-zA-Z0-9_-]+)",
                r"[Kk]ey[：:]\s*([a-zA-Z0-9_-]{20,})",
                r"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})",  # UUID格式
            ]

            for pattern in patterns:
                match = re.search(pattern, content)
                if match:
                    return match.group(1)

            # 如果没匹配到，返回第一行看起来像 key 的内容
            for line in content.strip().split("\n"):
                line = line.strip()
                if len(line) > 20 and not line.startswith("#"):
                    # 可能是 key
                    return line

        except Exception:
            pass

        return None

    def _extract_field(self, filepath: Path, pattern: str) -> Optional[str]:
        """使用正则从文件中提取字段"""
        try:
            content = filepath.read_text(encoding="utf-8")
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        except Exception:
            pass
        return None

    def save_config(self, config_type: str, **kwargs) -> bool:
        """
        保存配置到 private/ 目录

        Args:
            config_type: 配置类型 ("doubao", "tts", "web_search")
            **kwargs: 配置键值对

        Returns:
            是否保存成功
        """
        try:
            self.private_dir.mkdir(parents=True, exist_ok=True)

            if config_type == "doubao":
                filepath = self.private_dir / "research Agent.txt"
                api_key = kwargs.get("api_key", "")
                content = f"""ID：{kwargs.get("endpoint_id", "ep-xxx")}
API key：{api_key}
{kwargs.get("model", "Doubao-Seed-2.0-lite")}
"""
                filepath.write_text(content, encoding="utf-8")
                return True

            elif config_type == "tts":
                filepath = self.private_dir / "TTS.txt"
                content = f"""APP ID：{kwargs.get("app_id", "")}
Access Token：{kwargs.get("access_token", "")}
secret key：{kwargs.get("secret_key", "")}
api接入：https://www.volcengine.com/docs/6561/1329505?lang=zh
"""
                filepath.write_text(content, encoding="utf-8")
                return True

        except Exception as e:
            print(f"保存配置失败: {e}")
            return False

        return False

    def check_missing_configs(self) -> Dict[str, bool]:
        """
        检查缺失的配置

        Returns:
            {"doubao_api_key": True/False, "tts_app_id": True/False, ...}
        """
        config = self.load()
        return {
            "doubao_api_key": config.get("doubao_api_key") is not None,
            "tts_app_id": config.get("tts_app_id") is not None,
            "tts_access_token": config.get("tts_access_token") is not None,
        }

    def is_fully_configured(self) -> bool:
        """检查是否配置了最小运行所需的配置"""
        missing = self.check_missing_configs()
        # 最小配置：只需要 Doubao API key
        return missing.get("doubao_api_key", False)


def load_config() -> Dict[str, Any]:
    """便捷函数：加载所有配置"""
    loader = ConfigLoader()
    return loader.load()


def check_first_time() -> bool:
    """检查是否首次使用（无任何配置）"""
    loader = ConfigLoader()
    return not loader.is_fully_configured()
