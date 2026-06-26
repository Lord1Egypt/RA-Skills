"""
配置管理模块
负责用户配置的加载、保存和验证
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


# 配置文件路径，兼容 ClawHub 标准数据目录
CONFIG_DIR = Path.home() / ".openclaw" / "data" / "health-assistant"
CONFIG_FILE = CONFIG_DIR / "config.json"


class UserConfig:
    """用户配置类"""
    
    def __init__(self):
        self.health_concerns: List[str] = []  # 健康关切
        self.specific_conditions: List[Dict] = []  # 具体健康问题
        self.goals: List[str] = []  # 目标
        self.preferences: Dict = {
            "report_time": "08:00",
            "timezone": "Asia/Shanghai",
            "report_platform": "feishu"  # feishu, telegram, discord, wechat
        }
        self.device_config: Dict = {}  # 穿戴设备配置
        self.setup_step: str = "START"  # START, CONCERNS, DEVICE, AUTH, TIME, COMPLETED
        self.is_configured: bool = False
        self.created_at: str = datetime.now().isoformat()
        self.last_updated: str = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "health_concerns": self.health_concerns,
            "specific_conditions": self.specific_conditions,
            "goals": self.goals,
            "preferences": self.preferences,
            "device_config": self.device_config,
            "setup_step": self.setup_step,
            "is_configured": self.is_configured,
            "created_at": self.created_at,
            "last_updated": self.last_updated
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserConfig':
        """从字典加载"""
        config = cls()
        config.health_concerns = data.get("health_concerns", [])
        config.specific_conditions = data.get("specific_conditions", [])
        config.goals = data.get("goals", [])
        config.preferences = data.get("preferences", config.preferences)
        config.device_config = data.get("device_config", {})
        config.setup_step = data.get("setup_step", "START")
        config.is_configured = data.get("is_configured", False)
        config.created_at = data.get("created_at", config.created_at)
        config.last_updated = data.get("last_updated", config.last_updated)
        return config


def load_config() -> Optional[UserConfig]:
    """加载用户配置"""
    if not CONFIG_FILE.exists():
        return None
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return UserConfig.from_dict(data)
    except Exception as e:
        print(f"加载配置失败: {e}")
        return None


def save_config(config: UserConfig) -> bool:
    """保存用户配置"""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        config.last_updated = datetime.now().isoformat()
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config.to_dict(), f, ensure_ascii=False, indent=2)
            
        # 安全改进：设置严格的配置文件权限 (仅拥有者可读写 0o600)
        os.chmod(CONFIG_FILE, 0o600)
        
        return True
    except Exception as e:
        print(f"保存配置失败: {e}")
        return False


def is_first_time() -> bool:
    """检查是否首次使用"""
    return not CONFIG_FILE.exists()


def reset_config() -> bool:
    """重置配置（删除配置文件）"""
    try:
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
        return True
    except Exception as e:
        print(f"重置配置失败: {e}")
        return False
