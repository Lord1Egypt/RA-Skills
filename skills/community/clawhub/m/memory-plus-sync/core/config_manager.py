"""
Memory-Plus 配置管理器
统一管理模型配置、系统设置和运行参数
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self.config_dir = Path(__file__).parent.parent
        self.settings_file = self.config_dir / "model_settings.json"
        self.default_file = self.config_dir / "configs" / "default_model_settings.json"
        
        # 确保配置文件存在
        self._ensure_config_files()
    
    def _ensure_config_files(self):
        """确保配置文件存在"""
        if not self.settings_file.exists():
            self._create_default_settings()
        
        if not self.default_file.exists():
            self._create_default_file()
    
    def _create_default_settings(self):
        """创建默认设置文件"""
        default_settings = {
            "provider": "bailian",
            "model": "qwen3.5-plus",
            "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "apiKey": "",
            "timeout": 120,
            "temperature": 0.7,
            "maxTokens": 2000,
            "enableLogging": True,
            "lastUpdated": datetime.now().isoformat()
        }
        
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(default_settings, f, indent=2, ensure_ascii=False)
            logger.info(f"创建默认设置文件: {self.settings_file}")
        except Exception as e:
            logger.error(f"创建默认设置文件失败: {e}")
    
    def _create_default_file(self):
        """创建默认配置文件"""
        os.makedirs(self.default_file.parent, exist_ok=True)
        default_config = {
            "provider": "bailian",
            "model": "qwen3.5-plus",
            "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "apiKey": "",
            "timeout": 120,
            "temperature": 0.7,
            "maxTokens": 2000,
            "enableLogging": True,
            "lastUpdated": "2026-04-06T00:00:00"
        }
        
        try:
            with open(self.default_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            logger.info(f"创建默认配置文件: {self.default_file}")
        except Exception as e:
            logger.error(f"创建默认配置文件失败: {e}")
    
    def load_settings(self) -> Dict[str, Any]:
        """加载当前设置"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    logger.info(f"从设置页面加载配置: {settings.get('model', 'unknown')}")
                    return settings
            else:
                logger.warning("设置文件不存在，使用默认配置")
                return self.load_default_settings()
        except Exception as e:
            logger.error(f"加载设置失败: {e}")
            return self.load_default_settings()
    
    def load_default_settings(self) -> Dict[str, Any]:
        """加载默认设置"""
        try:
            if self.default_file.exists():
                with open(self.default_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    logger.info(f"加载默认配置: {settings.get('model', 'unknown')}")
                    return settings
            else:
                logger.error("默认配置文件也不存在，使用硬编码默认值")
                return {
                    "provider": "bailian",
                    "model": "qwen3.5-plus",
                    "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
                    "apiKey": os.getenv("BAILIAN_API_KEY", ""),
                    "timeout": 120,
                    "temperature": 0.7,
                    "maxTokens": 2000,
                    "enableLogging": True
                }
        except Exception as e:
            logger.error(f"加载默认设置失败: {e}")
            return {}
    
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """保存设置"""
        try:
            settings['lastUpdated'] = datetime.now().isoformat()
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            
            logger.info(f"设置已保存到: {self.settings_file}")
            return True
        except Exception as e:
            logger.error(f"保存设置失败: {e}")
            return False
    
    def get_model_config(self) -> Dict[str, Any]:
        """获取模型配置（用于三代理验证）"""
        settings = self.load_settings()
        
        # 根据提供商构建模型配置
        provider = settings.get('provider', 'bailian')
        model = settings.get('model', 'qwen3.5-plus')
        api_key = settings.get('apiKey', '')
        base_url = settings.get('baseUrl', '')
        
        # 如果 API Key 为空，尝试从环境变量获取
        if not api_key:
            if provider == 'bailian':
                api_key = os.getenv("BAILIAN_API_KEY", "")
            elif provider == 'kimi':
                api_key = os.getenv("KIMI_API_KEY", "")
            elif provider == 'deepseek':
                api_key = os.getenv("DEEPSEEK_API_KEY", "")
            elif provider == 'glm':
                api_key = os.getenv("ZHIPUAI_API_KEY", "")
        
        config = {
            "provider": provider,
            "model": model,
            "api_key": api_key,
            "base_url": base_url,
            "timeout": settings.get('timeout', 120),
            "temperature": settings.get('temperature', 0.7),
            "max_tokens": settings.get('maxTokens', 2000),
            "enable_logging": settings.get('enableLogging', True)
        }
        
        return config
    
    def test_connection(self) -> Dict[str, Any]:
        """测试模型连接"""
        import requests
        
        config = self.get_model_config()
        api_key = config.get('api_key', '')
        base_url = config.get('base_url', '')
        model = config.get('model', '')
        
        if not api_key:
            return {"success": False, "message": "API Key 为空"}
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        test_data = {
            "model": model,
            "messages": [{"role": "user", "content": "Connection test, please respond with 'OK'."}],
            "max_tokens": 10
        }
        
        try:
            url = f"{base_url}/chat/completions"
            response = requests.post(url, headers=headers, json=test_data, timeout=10)
            
            if response.status_code == 200:
                return {"success": True, "message": "模型连接测试成功"}
            else:
                return {"success": False, "message": f"连接失败: {response.status_code}"}
        except Exception as e:
            return {"success": False, "message": f"测试异常: {str(e)}"}

# 全局配置管理器实例
config_manager = ConfigManager()

if __name__ == "__main__":
    # 测试配置管理器
    settings = config_manager.load_settings()
    print("当前配置:")
    for key, value in settings.items():
        if key == "apiKey" and value:
            print(f"  {key}: {'*' * 8}{value[-4:]}")
        else:
            print(f"  {key}: {value}")
    
    # 测试连接
    print("\n测试模型连接...")
    result = config_manager.test_connection()
    print(f"连接测试: {result['success']} - {result['message']}")
