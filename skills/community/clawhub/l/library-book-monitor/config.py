import yaml
import os
from pathlib import Path


class Config:
    """配置管理类"""

    def __init__(self, config_file: str = "config.yaml"):
        self.config_file = Path(config_file)
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """加载配置文件"""
        if not self.config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_file}")

        with open(self.config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get(self, key: str, default=None):
        """获取配置项"""
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    @property
    def library(self) -> dict:
        """图书馆配置"""
        return self.get("library", {})

    @property
    def scheduler(self) -> dict:
        """定时任务配置"""
        return self.get("scheduler", {})

    @property
    def notification(self) -> dict:
        """提醒配置"""
        return self.get("notification", {})

    @property
    def storage(self) -> dict:
        """存储配置"""
        return self.get("storage", {})
