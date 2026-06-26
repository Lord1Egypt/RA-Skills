#!/usr/bin/env python3
"""
配置管理模块
"""

import json
import os
from pathlib import Path

class Config:
    def __init__(self, data=None, config_path=None):
        self.data = data or {}
        self.config_path = config_path

    @staticmethod
    def load(path):
        """从文件加载配置"""
        with open(path, 'r', encoding='utf-8') as f:
            return Config(json.load(f), path)

    def save(self):
        """保存配置到文件"""
        if self.config_path:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get(self, key, default=None):
        """获取配置项（支持点号分隔的嵌套键）"""
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key, value):
        """设置配置项（支持点号分隔的嵌套键）"""
        keys = key.split('.')
        current = self.data
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value

    def to_dict(self):
        return self.data.copy()
