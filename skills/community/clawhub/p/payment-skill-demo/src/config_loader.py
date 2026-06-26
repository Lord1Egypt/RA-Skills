"""
配置加载器 - 从 config 目录加载环境配置
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ConfigLoader:
    """配置加载器"""
    
    @staticmethod
    def get_config_dir() -> Path:
        """获取配置目录路径"""
        # 获取项目根目录（payment-skill-demo）
        current_file = Path(__file__)
        project_root = current_file.parent.parent
        config_dir = project_root / "config"
        return config_dir
    
    @staticmethod
    def load_env_file(env_name: str = "development") -> Dict[str, str]:
        """
        加载环境配置文件
        
        参数:
            env_name: 环境名称 (development 或 production)
        
        返回:
            配置字典
        """
        config_dir = ConfigLoader.get_config_dir()
        env_file = config_dir / f"{env_name}.env"
        
        if not env_file.exists():
            logger.warning(f"配置文件不存在: {env_file}")
            return {}
        
        config = {}
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # 跳过注释和空行
                    if not line or line.startswith('#'):
                        continue
                    
                    # 解析 KEY=VALUE 格式
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # 移除引号
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        
                        config[key] = value
            
            logger.info(f"成功加载配置文件: {env_file}")
            return config
        
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return {}
    
    @staticmethod
    def get_api_config(env_name: str = "development") -> Dict[str, Any]:
        """
        获取 API 配置
        
        参数:
            env_name: 环境名称
        
        返回:
            API 配置字典
        """
        # 首先从环境变量读取
        config = {
            "api_key": os.getenv("PAYMENT_API_KEY"),
            "api_secret": os.getenv("PAYMENT_API_SECRET"),
            "api_url": os.getenv("PAYMENT_API_URL"),
            "timeout": int(os.getenv("PAYMENT_API_TIMEOUT", "30")) if os.getenv("PAYMENT_API_TIMEOUT") else 30,
        }
        
        # 如果环境变量未设置，从配置文件读取
        env_config = ConfigLoader.load_env_file(env_name)
        
        if not config["api_key"]:
            config["api_key"] = env_config.get("PAYMENT_API_KEY")
        if not config["api_secret"]:
            config["api_secret"] = env_config.get("PAYMENT_API_SECRET")
        if not config["api_url"]:
            config["api_url"] = env_config.get("PAYMENT_API_URL")
        
        # PAYMENT_API_URL 有默认值
        if not config["api_url"]:
            config["api_url"] = "https://api.zlclaw.com"
        
        # 读取超时配置
        if not config["timeout"] or config["timeout"] == 30:
            timeout_str = env_config.get("PAYMENT_API_TIMEOUT", "30")
            try:
                config["timeout"] = int(timeout_str)
            except ValueError:
                config["timeout"] = 30
        
        # 验证必需的配置
        if not config["api_key"]:
            raise ValueError("PAYMENT_API_KEY 未设置")
        if not config["api_secret"]:
            raise ValueError("PAYMENT_API_SECRET 未设置")
        
        return config
    
    @staticmethod
    def get_encryption_config(env_name: str = "development") -> Optional[str]:
        """
        获取加密密钥配置
        
        参数:
            env_name: 环境名称
        
        返回:
            加密密钥或 None
        """
        # 首先从环境变量读取
        encryption_key = os.getenv("PAYMENT_ENCRYPTION_KEY")
        
        # 如果环境变量未设置，从配置文件读取
        if not encryption_key:
            env_config = ConfigLoader.load_env_file(env_name)
            encryption_key = env_config.get("PAYMENT_ENCRYPTION_KEY")
        
        return encryption_key
    
    @staticmethod
    def get_logging_config(env_name: str = "development") -> Dict[str, Any]:
        """
        获取日志配置
        
        参数:
            env_name: 环境名称
        
        返回:
            日志配置字典
        """
        # 首先从环境变量读取
        config = {
            "level": os.getenv("PAYMENT_LOG_LEVEL", "INFO"),
            "file": os.getenv("PAYMENT_LOG_FILE"),
        }
        
        # 如果环境变量未设置，从配置文件读取
        if not config["file"]:
            env_config = ConfigLoader.load_env_file(env_name)
            config["file"] = env_config.get("PAYMENT_LOG_FILE")
        
        return config
