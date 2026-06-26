#!/usr/bin/env python3
"""
用户设置管理 - 管理更新模式和频率设置
"""

import os
import json
from typing import Dict, Any, Optional

class UserSettings:
    """用户设置管理器"""
    
    def __init__(self, data_path: str = None):
        if data_path is None:
            data_path = '/root/.openclaw/workspace/skills/memory-auto-update/data'
        self.data_path = data_path
        self.settings_file = os.path.join(data_path, 'user_settings.json')
        self.default_file = os.path.join(data_path, 'default_settings.json')
        
        # 加载默认设置
        self.default_settings = self._load_default_settings()
        self.settings = self._load_settings()
    
    def _load_default_settings(self) -> Dict[str, Any]:
        """加载默认设置"""
        if os.path.exists(self.default_file):
            with open(self.default_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _load_settings(self) -> Dict[str, Any]:
        """加载用户设置，如果不存在则使用默认"""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.default_settings.copy()
    
    def save_settings(self) -> bool:
        """保存用户设置"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存设置失败: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取设置"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """设置值"""
        self.settings[key] = value
        return self.save_settings()
    
    def reset_to_default(self) -> bool:
        """重置为默认设置"""
        self.settings = self.default_settings.copy()
        return self.save_settings()
    
    def get_update_mode(self) -> str:
        """获取更新模式"""
        return self.get('update_mode', 'smart_hybrid')
    
    def set_update_mode(self, mode: str) -> bool:
        """设置更新模式"""
        valid_modes = ['active', 'passive', 'smart_hybrid']
        if mode in valid_modes:
            return self.set('update_mode', mode)
        return False
    
    def get_update_frequency(self) -> str:
        """获取更新频率"""
        return self.get('update_frequency', 'end_of_conversation')
    
    def set_update_frequency(self, frequency: str) -> bool:
        """设置更新频率"""
        valid_frequencies = ['realtime', '30min', '1hour', 'manual', 'end_of_conversation']
        if frequency in valid_frequencies:
            return self.set('update_frequency', frequency)
        return False
    
    def get_reminder_style(self) -> str:
        """获取提醒方式"""
        return self.get('reminder_style', 'important_immediate_others_wait')
    
    def set_reminder_style(self, style: str) -> bool:
        """设置提醒方式"""
        valid_styles = ['immediate', 'end_of_conversation', 'important_immediate_others_wait']
        if style in valid_styles:
            return self.set('reminder_style', style)
        return False
    
    def get_current_settings_display(self) -> str:
        """获取当前设置的显示文本"""
        mode = self.get_update_mode()
        frequency = self.get_update_frequency()
        
        mode_names = {
            'active': '主动模式（自动提示）',
            'passive': '被动模式（手动触发）',
            'smart_hybrid': '智能混合模式（推荐）'
        }
        
        frequency_names = {
            'realtime': '实时',
            '30min': '每30分钟',
            '1hour': '每1小时',
            'manual': '手动',
            'end_of_conversation': '对话结束时（推荐）'
        }
        
        return f"""当前设置：
- 更新模式：{mode_names.get(mode, mode)}
- 更新频率：{frequency_names.get(frequency, frequency)}"""
    
    def get_settings_menu(self) -> str:
        """获取设置菜单"""
        return """设置选项：

1. 更新模式：
   [1] 主动模式 - 对话结束自动提示
   [2] 被动模式 - 完全手动触发
   [3] 智能混合模式 - 重要内容立即提醒（推荐）

2. 更新频率：
   [1] 实时 - 重要内容立即保存
   [2] 每30分钟 - 半实时，不太打扰
   [3] 每1小时 - 低频率，高效
   [4] 手动 - 完全用户控制
   [5] 对话结束时 - 最自然的方式（推荐）

输入选项编号或直接说"设置更新模式为主动""""

if __name__ == "__main__":
    settings = UserSettings()
    
    print("当前设置：")
    print(settings.get_current_settings_display())
    print()
    
    print("设置菜单：")
    print(settings.get_settings_menu())
