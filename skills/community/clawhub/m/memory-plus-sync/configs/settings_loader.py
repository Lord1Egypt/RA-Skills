"""
Memory-Plus 设置加载模块
从设置页面读取模型配置
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

def load_model_settings() -> Dict[str, Any]:
    """
    加载模型设置
    
    优先级:
    1. 设置页面保存的配置 (model_settings.json)
    2. 默认配置 (default_model_settings.json)
    3. 环境变量
    """
    config_dir = Path(__file__).parent.parent
    settings_file = config_dir / "model_settings.json"
    default_file = config_dir / "configs" / "default_model_settings.json"
    
    # 尝试加载设置页面配置
    if settings_file.exists():
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                print(f"✅ 从设置页面加载配置: {settings.get('model', 'unknown')}")
                return settings
        except Exception as e:
            print(f"⚠️  加载设置页面配置失败: {e}")
    
    # 加载默认配置
    if default_file.exists():
        try:
            with open(default_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                print(f"✅ 加载默认配置: {settings.get('model', 'unknown')}")
                return settings
        except Exception as e:
            print(f"⚠️  加载默认配置失败: {e}")
    
    # 使用环境变量
    print("ℹ️  使用环境变量配置")
    return {
        "provider": os.getenv("MEMORY_PLUS_PROVIDER", "bailian"),
        "model": os.getenv("MEMORY_PLUS_MODEL", "qwen3.5-plus"),
        "baseUrl": os.getenv("MEMORY_PLUS_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        "apiKey": os.getenv("MEMORY_PLUS_API_KEY", ""),
        "timeout": int(os.getenv("MEMORY_PLUS_TIMEOUT", "120")),
        "temperature": float(os.getenv("MEMORY_PLUS_TEMPERATURE", "0.7"))
    }

def update_memory_plus_config():
    """更新 Memory-Plus 配置以使用设置页面的配置"""
    settings = load_model_settings()
    
    # 更新 cloud_models_config.py
    cloud_config_file = Path(__file__).parent / "cloud_models_config.py"
    if cloud_config_file.exists():
        try:
            with open(cloud_config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 更新配置（简化示例）
            new_content = content.replace(
                "kimi_api_key: str = \"\"",
                f"kimi_api_key: str = \"{settings.get('apiKey', '')}\""
            )
            
            with open(cloud_config_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Memory-Plus 配置已更新")
        except Exception as e:
            print(f"⚠️  更新 Memory-Plus 配置失败: {e}")

if __name__ == "__main__":
    settings = load_model_settings()
    print("当前配置:")
    for key, value in settings.items():
        if key == "apiKey" and value:
            print(f"  {key}: {'*' * 8}{value[-4:]}")
        else:
            print(f"  {key}: {value}")
