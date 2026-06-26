"""
配置管理器 - 管理用户配置和平台参数
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """管理快导Skill的所有配置"""
    
    CONFIG_FILE = "config/platforms.json"
    
    def __init__(self, skill_path: str = None):
        """
        初始化配置管理器
        
        Args:
            skill_path: Skill根目录路径，默认从环境变量或推断
        """
        if skill_path is None:
            # 推断Skill路径
            current_file = Path(__file__).resolve()
            self.skill_path = current_file.parent.parent
        else:
            self.skill_path = Path(skill_path)
        
        self.config_path = self.skill_path / self.CONFIG_FILE
        self._config_cache = None
    
    def load_config(self) -> Dict[str, Any]:
        """加载完整配置"""
        if self._config_cache is None:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config_cache = json.load(f)
        return self._config_cache
    
    def get_platform_config(self, platform: str) -> Dict[str, Any]:
        """
        获取指定平台的配置
        
        Args:
            platform: 平台标识（xiaohongshu/douyin/shipinhao）
            
        Returns:
            平台配置字典
        """
        config = self.load_config()
        platform_config = config.get("platforms", {}).get(platform, {})
        
        if not platform_config:
            raise ValueError(f"未找到平台配置: {platform}")
        
        # 合并全局设置
        global_settings = config.get("global_settings", {})
        platform_config["_global"] = global_settings
        
        return platform_config
    
    def get_config(self) -> Dict[str, Any]:
        """
        获取完整配置
        
        Returns:
            完整配置字典
        """
        return self.load_config()
    
    def get_user_config(self, key: str) -> Any:
        """
        获取用户配置项
        
        Args:
            key: 配置项名称
            
        Returns:
            配置值
        """
        config = self.load_config()
        global_settings = config.get("global_settings", {})
        
        value = global_settings.get(key)
        
        # 检查必须配置项
        required_keys = [
            "copy_library_path",
            "report_space_id", 
            "rules_path"
        ]
        
        if key in required_keys and not value:
            raise ConfigNotSetError(
                f"配置项 '{key}' 未设置。\n"
                f"请运行: kd config set {key} '你的路径'"
            )
        
        return value
    
    def set_user_config(self, key: str, value: Any) -> bool:
        """
        设置用户配置项
        
        Args:
            key: 配置项名称
            value: 配置值
            
        Returns:
            是否设置成功
        """
        config = self.load_config()
        
        if key not in config.get("global_settings", {}):
            raise ValueError(f"未知的配置项: {key}")
        
        config["global_settings"][key] = value
        
        # 保存配置
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            self._config_cache = config
            return True
        except Exception as e:
            raise ConfigSaveError(f"保存配置失败: {e}")
    
    def validate_config(self) -> Dict[str, bool]:
        """
        验证所有必需配置是否已设置
        
        Returns:
            配置项验证结果字典
        """
        required_configs = [
            "copy_library_path",
            "report_space_id",
            "rules_path"
        ]
        
        results = {}
        for key in required_configs:
            try:
                value = self.get_user_config(key)
                results[key] = bool(value)
            except ConfigNotSetError:
                results[key] = False
        
        return results
    
    def get_excel_path(self, platform: str) -> str:
        """
        获取指定平台的文案库Excel路径
        
        Args:
            platform: 平台标识
            
        Returns:
            Excel文件完整路径
        """
        library_path = self.get_user_config("copy_library_path")
        config = self.load_config()
        file_naming = config.get("global_settings", {}).get(
            "file_naming", 
            "{platform}文案库.xlsx"
        )
        
        platform_name = config.get("platforms", {}).get(platform, {}).get("name", platform)
        filename = file_naming.format(platform=platform_name)
        
        return os.path.join(library_path, filename)
    
    def calculate_segments(self, platform: str, total_duration: str) -> int:
        """
        根据总时长计算分镜数量
        
        Args:
            platform: 平台标识
            total_duration: 总时长描述（如"2-3min"）
            
        Returns:
            分镜数量
        """
        platform_config = self.get_platform_config(platform)
        duration_config = platform_config.get("duration", {})
        
        segment_range = duration_config.get("segment_seconds", {})
        min_seg = segment_range.get("min", 3)
        max_seg = segment_range.get("max", 12)
        avg_seg = (min_seg + max_seg) / 2
        
        # 解析总时长
        total_config = duration_config.get("total_seconds", {})
        min_total = total_config.get("min", 120)
        max_total = total_config.get("max", 180)
        avg_total = (min_total + max_total) / 2
        
        # 计算分镜数量
        segments_count = int(avg_total / avg_seg)
        
        return segments_count


class ConfigNotSetError(Exception):
    """配置项未设置错误"""
    pass


class ConfigSaveError(Exception):
    """配置保存错误"""
    pass


# 便捷函数
def get_config_manager(skill_path: str = None) -> ConfigManager:
    """获取配置管理器实例"""
    return ConfigManager(skill_path)


def validate_platform_keywords(platform: str) -> bool:
    """
    验证平台关键词是否已配置
    
    Args:
        platform: 平台标识
        
    Returns:
        是否已配置关键词
    """
    config_mgr = get_config_manager()
    platform_config = config_mgr.get_platform_config(platform)
    keywords = platform_config.get("keywords", [])
    return len(keywords) > 0
