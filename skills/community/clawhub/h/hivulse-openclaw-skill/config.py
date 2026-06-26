#!/usr/bin/env python3
"""
配置文件管理模块
"""

import os
import json
from pathlib import Path

class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config_dir = Path.home() / ".hivulseai"
        self.config_path = self.config_dir / config_file
        
        # 确保配置目录存在
        self.config_dir.mkdir(exist_ok=True)
        
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # 配置文件损坏，创建新的
                return self._create_default_config()
        else:
            return self._create_default_config()
    
    def _create_default_config(self) -> dict:
        """创建默认配置"""
        return {
            "api_key": "",
            "last_used_directory": ""
        }
    
    def save_config(self) -> bool:
        """保存配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def get_api_key(self) -> str:
        """获取API密钥"""
        return self.config.get("api_key", "")
    
    def set_api_key(self, api_key: str):
        """设置API密钥"""
        self.config["api_key"] = api_key
        self.save_config()
    

    
    def get_last_directory(self) -> str:
        """获取上次使用的目录"""
        return self.config.get("last_used_directory", "")
    
    def set_last_directory(self, directory: str):
        """设置上次使用的目录"""
        self.config["last_used_directory"] = directory
        self.save_config()
    
    def has_valid_config(self) -> bool:
        """检查是否有有效的配置"""
        return bool(self.get_api_key())
    
    def show_config(self):
        """显示当前配置"""
        print("\n📋 当前配置:")
        print(f"   API密钥: {'*' * min(len(self.get_api_key()), 20)}..." if self.get_api_key() else "未设置")
        print(f"   API地址: http://localhost:8001 (固定)")
        print(f"   上次目录: {self.get_last_directory() or '无'}")

def setup_config():
    """配置向导"""
    config = ConfigManager()
    
    print("🔧 hivulseAI 配置向导")
    print("=" * 40)
    
    # 显示当前配置
    config.show_config()
    
    # 询问是否修改配置
    if config.has_valid_config():
        choice = input("\n是否修改配置? (y/n): ").strip().lower()
        if choice not in ['y', 'yes', '是']:
            return config
    
    # 设置API密钥
    while True:
        api_key = input("\n🔑 请输入API密钥: ").strip()
        if api_key:
            config.set_api_key(api_key)
            break
        else:
            print("❌ API密钥不能为空")
    
    # API地址固定为 http://localhost:8001
    print("🌐 API地址已固定为: http://localhost:8001")
    
    print("\n✅ 配置完成!")
    config.show_config()
    
    return config

if __name__ == "__main__":
    setup_config()