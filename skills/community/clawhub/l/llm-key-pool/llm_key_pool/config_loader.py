"""
配置文件加载器
负责加载、验证YAML配置文件
"""

import yaml
import os
from typing import Dict, Any, List
from urllib.parse import urlparse


class ConfigValidationError(Exception):
    """配置验证错误"""
    pass


class ConfigLoader:
    """配置文件加载器"""

    # 全局配置默认值
    DEFAULT_GLOBAL_CONFIG = {
        'max_retries': 3,
        'retry_delay': 1,
        'error_threshold': 5,
        'cooldown_seconds': 300,
        'quota_check_enabled': True,
        'quota_min_remaining': 1000  # 剩余Token少于这个值自动切换
    }

    def __init__(self, config_path: str):
        """
        初始化配置加载器

        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.config = None

    def load(self) -> Dict[str, Any]:
        """
        加载配置文件

        Returns:
            配置字典

        Raises:
            FileNotFoundError: 配置文件不存在
            yaml.YAMLError: YAML格式错误
            ConfigValidationError: 配置验证失败
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"YAML格式错误: {str(e)}")

        # 验证配置
        self.validate()

        return self.config

    def validate(self):
        """
        验证配置文件格式

        Raises:
            ConfigValidationError: 配置验证失败
        """
        if not isinstance(self.config, dict):
            raise ConfigValidationError("配置文件根节点必须是字典")

        # 检查providers字段
        if 'providers' not in self.config:
            raise ConfigValidationError("缺少必需字段: providers")

        if not isinstance(self.config['providers'], dict):
            raise ConfigValidationError("providers必须是字典类型")

        if not self.config['providers']:
            raise ConfigValidationError("providers不能为空")

        # 验证每个平台的配置
        for provider_name, provider_config in self.config['providers'].items():
            self._validate_provider_config(provider_name, provider_config)

        # 验证全局配置（如果存在）
        if 'global' in self.config:
            self._validate_global_config(self.config['global'])

    def _validate_provider_config(self, provider_name: str, config: Dict[str, Any]):
        """
        验证单个平台的配置

        Args:
            provider_name: 平台名称
            config: 平台配置

        Raises:
            ConfigValidationError: 配置验证失败
        """
        required_fields = ['model', 'api_keys', 'base_url', 'tier']
        valid_tiers = ['primary', 'daily', 'fallback']

        # 检查必需字段
        for field in required_fields:
            if field not in config:
                raise ConfigValidationError(f"平台 {provider_name} 缺少必需字段: {field}")

        # 验证tier
        if not isinstance(config['tier'], str) or not config['tier'].strip():
            raise ConfigValidationError(f"平台 {provider_name} 的 tier 必须是非空字符串")

        if config['tier'] not in valid_tiers:
            raise ConfigValidationError(
                f"平台 {provider_name} 的 tier 必须是以下值之一: {', '.join(valid_tiers)}"
            )

        # 验证model
        if not isinstance(config['model'], str) or not config['model'].strip():
            raise ConfigValidationError(f"平台 {provider_name} 的 model 必须是非空字符串")

        # 验证api_keys
        if not isinstance(config['api_keys'], list):
            raise ConfigValidationError(f"平台 {provider_name} 的 api_keys 必须是数组")

        if len(config['api_keys']) == 0:
            raise ConfigValidationError(f"平台 {provider_name} 的 api_keys 不能为空")

        for idx, key in enumerate(config['api_keys']):
            if not isinstance(key, str) or not key.strip():
                raise ConfigValidationError(
                    f"平台 {provider_name} 的 api_keys[{idx}] 必须是非空字符串"
                )

        # 验证base_url
        if not isinstance(config['base_url'], str) or not config['base_url'].strip():
            raise ConfigValidationError(f"平台 {provider_name} 的 base_url 必须是非空字符串")

        # 验证URL格式
        try:
            parsed = urlparse(config['base_url'])
            if not parsed.scheme or not parsed.netloc:
                raise ConfigValidationError(
                    f"平台 {provider_name} 的 base_url 不是有效的URL: {config['base_url']}"
                )
        except Exception as e:
            raise ConfigValidationError(
                f"平台 {provider_name} 的 base_url 解析失败: {str(e)}"
            )

    def _validate_global_config(self, global_config: Dict[str, Any]):
        """
        验证全局配置

        Args:
            global_config: 全局配置

        Raises:
            ConfigValidationError: 配置验证失败
        """
        # max_retries
        if 'max_retries' in global_config:
            if not isinstance(global_config['max_retries'], int) or global_config['max_retries'] < 0:
                raise ConfigValidationError("global.max_retries 必须是非负整数")

        # retry_delay
        if 'retry_delay' in global_config:
            if not isinstance(global_config['retry_delay'], int) or global_config['retry_delay'] < 0:
                raise ConfigValidationError("global.retry_delay 必须是非负整数")

        # error_threshold
        if 'error_threshold' in global_config:
            if not isinstance(global_config['error_threshold'], int) or global_config['error_threshold'] < 0:
                raise ConfigValidationError("global.error_threshold 必须是非负整数")

        # cooldown_seconds
        if 'cooldown_seconds' in global_config:
            if not isinstance(global_config['cooldown_seconds'], int) or global_config['cooldown_seconds'] < 0:
                raise ConfigValidationError("global.cooldown_seconds 必须是非负整数")

        # quota_check_enabled
        if 'quota_check_enabled' in global_config:
            if not isinstance(global_config['quota_check_enabled'], bool):
                raise ConfigValidationError("global.quota_check_enabled 必须是布尔值")

        # quota_min_remaining
        if 'quota_min_remaining' in global_config:
            if not isinstance(global_config['quota_min_remaining'], int) or global_config['quota_min_remaining'] < 0:
                raise ConfigValidationError("global.quota_min_remaining 必须是非负整数")

    def get_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """
        获取指定平台的配置

        Args:
            provider_name: 平台名称

        Returns:
            平台配置

        Raises:
            KeyError: 平台不存在
        """
        if provider_name not in self.config['providers']:
            raise KeyError(f"平台不存在: {provider_name}")
        return self.config['providers'][provider_name]

    def get_global_config(self) -> Dict[str, Any]:
        """
        获取全局配置

        Returns:
            全局配置（包含默认值）
        """
        global_config = self.DEFAULT_GLOBAL_CONFIG.copy()

        if 'global' in self.config:
            global_config.update(self.config['global'])

        return global_config

    def get_provider_names(self) -> List[str]:
        """
        获取所有平台名称

        Returns:
            平台名称列表
        """
        return list(self.config['providers'].keys())
