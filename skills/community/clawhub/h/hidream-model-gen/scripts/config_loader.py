#!/usr/bin/env python3
"""
配置加载器 - 支持分体式配置文件
自动检测并使用 config/ 目录或回退到 api_ports.json
"""
import json
import os
from typing import Dict, Any, Optional


class ConfigLoader:
    """配置加载器 - 支持模块化配置"""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        初始化配置加载器
        
        Args:
            config_dir: 配置目录路径，默认使用 scripts/config/
        """
        if config_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_dir = os.path.join(base_dir, 'config')
        
        self.config_dir = config_dir
        self._config: Optional[Dict[str, Any]] = None
    
    def load(self) -> Dict[str, Any]:
        """
        加载配置
        
        优先尝试加载分体式配置(config/)，如果不存在则回退到api_ports.json
        """
        if self._config is not None:
            return self._config
        
        # 尝试分体式配置
        if os.path.exists(self.config_dir):
            config = self._load_split_config()
            if config:
                self._config = config
                return config
        
        # 回退到单一文件
        self._config = self._load_legacy_config()
        return self._config
    
    def _load_split_config(self) -> Optional[Dict[str, Any]]:
        """加载分体式配置"""
        base_file = os.path.join(self.config_dir, 'base.json')
        if not os.path.exists(base_file):
            return None
        
        # 加载基础配置
        with open(base_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        config['categories'] = {}
        
        # 加载各个分类配置
        category_files = [
            'text_to_image.json',
            'image_to_video.json',
            'text_to_video.json',
            'keyframe_to_video.json',
            'image_to_image.json',
            'template_to_video.json'
        ]
        
        for filename in category_files:
            filepath = os.path.join(self.config_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    cat_config = json.load(f)
                    if 'categories' in cat_config:
                        config['categories'].update(cat_config['categories'])
        
        return config
    
    def _load_legacy_config(self) -> Dict[str, Any]:
        """加载旧版单一配置文件"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        legacy_file = os.path.join(base_dir, 'api_ports.json')
        
        with open(legacy_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def reload(self) -> Dict[str, Any]:
        """重新加载配置"""
        self._config = None
        return self.load()


# 全局配置加载器实例
_config_loader: Optional[ConfigLoader] = None


def get_config_loader(config_dir: Optional[str] = None) -> ConfigLoader:
    """获取全局配置加载器实例"""
    global _config_loader
    if _config_loader is None or config_dir is not None:
        _config_loader = ConfigLoader(config_dir)
    return _config_loader


def load_ports_config(config_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    加载端口配置的便捷函数
    
    Args:
        config_dir: 可选的配置目录路径
        
    Returns:
        完整的端口配置字典
    """
    loader = get_config_loader(config_dir)
    return loader.load()
