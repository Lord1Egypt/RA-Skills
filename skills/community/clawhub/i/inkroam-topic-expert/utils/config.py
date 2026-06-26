#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置加载模块
统一管理配置文件
"""

import json
from pathlib import Path


class Config:
    """配置管理器"""
    
    def __init__(self, config_file=None):
        """
        Args:
            config_file: 配置文件路径
        """
        if config_file is None:
            config_file = Path(__file__).parent.parent / "config.json"
        
        self.config_file = Path(config_file)
        self.config = self._load()
    
    def _load(self):
        """加载配置文件"""
        if not self.config_file.exists():
            return self._default_config()
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _default_config(self):
        """默认配置"""
        import os
        return {
            "account_type": "AI资讯",
            "account_style": "专业实操",
            "target_platform": "公众号",
            "min_score": 70,
            "max_daily_push": 5,
            "push_immediately_score": 80,
            "bijian_space_id": None,
            "data_sources": {
                "trendradar": {
                    "enabled": True,
                    "url": "http://localhost:8000"
                },
                "hot_search": {
                    "enabled": False
                }
            },
            "telegram": {
                "chat_id": os.environ.get("TELEGRAM_CHAT_ID", "")
            }
        }
    
    def get(self, key, default=None):
        """获取配置项"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def save(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)


# 使用示例
if __name__ == '__main__':
    config = Config()
    print(f"账号类型：{config.get('account_type')}")
    print(f"最低分数：{config.get('min_score')}")
    print(f"TrendRadar URL：{config.get('data_sources.trendradar.url')}")
