#!/usr/bin/env python3
"""
共享工具模块
"""

import json
import os
from pathlib import Path


def load_api_config() -> dict:
    """从环境变量或配置文件加载大模型配置"""
    api_key = os.environ.get("API_KEY", "")
    api_base = os.environ.get("API_BASE", "")
    model_name = os.environ.get("MODEL_NAME", "")
    
    if api_key and api_base and model_name:
        return {
            "api_key": api_key,
            "api_base": api_base,
            "model": model_name
        }
    
    config_path = Path(__file__).parent / "config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        api_key = config.get("API_KEY", "")
        api_base = config.get("API_BASE", "")
        model_name = config.get("MODEL_NAME", "")
        
        if api_key and api_base and model_name:
            return {
                "api_key": api_key,
                "api_base": api_base,
                "model": model_name
            }
    
    raise ValueError("未配置 API Key，请在环境变量或 scripts/config.json 中配置")
