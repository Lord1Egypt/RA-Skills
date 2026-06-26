"""
平台适配器模块

提供OpenClaw和LobsterAI双平台的适配支持。
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod


@dataclass
class PlatformConfig:
    """平台配置"""
    platform: str  # "openclaw" 或 "lobsterai"
    working_dir: Path
    config_dir: Path
    data_dir: Path


class BasePlatformAdapter(ABC):
    """平台适配器基类"""
    
    def __init__(self, config: PlatformConfig):
        self.config = config
    
    @abstractmethod
    def get_memory_storage(self) -> Dict[str, Any]:
        """获取记忆存储"""
        pass
    
    @abstractmethod
    def save_memory(self, key: str, value: Any):
        """保存记忆"""
        pass
    
    @abstractmethod
    def get_memory(self, key: str) -> Optional[Any]:
        """获取记忆"""
        pass
    
    @abstractmethod
    def create_scheduled_task(self, name: str, cron: str, command: str) -> bool:
        """创建定时任务"""
        pass


class OpenClawAdapter(BasePlatformAdapter):
    """OpenClaw平台适配器"""
    
    def __init__(self, config: PlatformConfig):
        super().__init__(config)
        self.memory_file = config.config_dir / "MEMORY.md"
    
    def get_memory_storage(self) -> Dict[str, Any]:
        """获取OpenClaw的记忆存储（MEMORY.md）"""
        memory = {}
        
        if not self.memory_file.exists():
            return memory
        
        try:
            content = self.memory_file.read_text(encoding='utf-8')
            
            # 解析TTS配置
            import re
            provider_match = re.search(r'Provider:\s*(\S+)', content)
            if provider_match:
                memory['tts_provider'] = provider_match.group(1)
            
            model_match = re.search(r'Model:\s*(\S+)', content)
            if model_match:
                memory['tts_model'] = model_match.group(1)
            
            voice_match = re.search(r'Voice:\s*(\S+)', content)
            if voice_match:
                memory['tts_voice'] = voice_match.group(1)
            
            emotion_match = re.search(r'Emotion:\s*(\S+)', content)
            if emotion_match:
                memory['tts_emotion'] = emotion_match.group(1)
            
            speed_match = re.search(r'Speed:\s*([\d.]+)', content)
            if speed_match:
                memory['tts_speed'] = float(speed_match.group(1))
            
            pitch_match = re.search(r'Pitch:\s*([\d.]+)', content)
            if pitch_match:
                memory['tts_pitch'] = float(pitch_match.group(1))
            
            # 解析用户偏好
            tags_match = re.search(r'Subscribed Tags:\s*(.+)', content)
            if tags_match:
                memory['subscribed_tags'] = [
                    tag.strip() for tag in tags_match.group(1).split(',') if tag.strip()
                ]
            
            topics_match = re.search(r'Default Topics:\s*(.+)', content)
            if topics_match:
                memory['default_topics'] = [
                    topic.strip() for topic in topics_match.group(1).split(',') if topic.strip()
                ]
                
        except Exception as e:
            print(f"读取MEMORY.md失败: {e}")
        
        return memory
    
    def save_memory(self, key: str, value: Any):
        """保存记忆到MEMORY.md"""
        # 使用config_manager.py中的逻辑
        from .config_manager import ConfigManager
        config_manager = ConfigManager(self.memory_file)
        
        if key.startswith('tts_'):
            config = config_manager.get_tts_config()
            if key == 'tts_voice':
                config.voice = value
            elif key == 'tts_emotion':
                config.emotion = value
            elif key == 'tts_speed':
                config.speed = value
            elif key == 'tts_pitch':
                config.pitch = value
            elif key == 'tts_model':
                config.model = value
            config_manager.save_tts_config(config)
    
    def get_memory(self, key: str) -> Optional[Any]:
        """从MEMORY.md获取记忆"""
        memory = self.get_memory_storage()
        return memory.get(key)
    
    def create_scheduled_task(self, name: str, cron: str, command: str) -> bool:
        """使用OpenClaw的cron系统创建定时任务"""
        import subprocess
        
        try:
            cmd = [
                "openclaw", "cron", "add",
                "--name", name,
                "--cron", cron,
                "--session", "isolated",
                "--message", command,
                "--announce"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            print(f"创建定时任务失败: {e}")
            return False


class LobsterAIAdapter(BasePlatformAdapter):
    """LobsterAI平台适配器"""
    
    def __init__(self, config: PlatformConfig):
        super().__init__(config)
        self.db_path = config.data_dir / "lobsterai.sqlite"
    
    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        return sqlite3.connect(str(self.db_path))
    
    def get_memory_storage(self) -> Dict[str, Any]:
        """获取LobsterAI的记忆存储（SQLite）"""
        memory = {}
        
        if not self.db_path.exists():
            return memory
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # 从kv表读取配置
            cursor.execute("SELECT key, value FROM kv WHERE key LIKE 'lobster_radio_%'")
            rows = cursor.fetchall()
            
            for key, value in rows:
                memory_key = key.replace('lobster_radio_', '')
                try:
                    memory[memory_key] = json.loads(value)
                except:
                    memory[memory_key] = value
            
            conn.close()
            
        except Exception as e:
            print(f"读取SQLite失败: {e}")
        
        return memory
    
    def save_memory(self, key: str, value: Any):
        """保存记忆到SQLite"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # 确保kv表存在
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS kv (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            
            # 插入或更新
            db_key = f"lobster_radio_{key}"
            db_value = json.dumps(value) if not isinstance(value, str) else value
            
            cursor.execute(
                "INSERT OR REPLACE INTO kv (key, value) VALUES (?, ?)",
                (db_key, db_value)
            )
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"保存到SQLite失败: {e}")
    
    def get_memory(self, key: str) -> Optional[Any]:
        """从SQLite获取记忆"""
        memory = self.get_memory_storage()
        return memory.get(key)
    
    def create_scheduled_task(self, name: str, cron: str, command: str) -> bool:
        """使用LobsterAI的scheduled-task skill创建定时任务"""
        # LobsterAI通过对话或GUI创建定时任务
        # 这里返回True，实际任务由Agent通过Cowork模式创建
        print(f"请在LobsterAI中创建定时任务: {name}")
        print(f"Cron表达式: {cron}")
        print(f"命令: {command}")
        return True


class PlatformAdapterFactory:
    """平台适配器工厂"""
    
    @staticmethod
    def detect_platform() -> str:
        """检测当前平台"""
        # 检查OpenClaw环境变量
        if os.environ.get('OPENCLAW_HOME') or os.environ.get('OPENCLAW_WORKSPACE'):
            return 'openclaw'
        
        # 检查LobsterAI环境变量
        if os.environ.get('LOBSTERAI_HOME') or os.environ.get('LOBSTERAI_WORKSPACE'):
            return 'lobsterai'
        
        # 检查配置文件
        home = Path.home()
        
        if (home / '.openclaw').exists():
            return 'openclaw'
        
        if (home / 'LobsterAI').exists() or (home / '.lobsterai').exists():
            return 'lobsterai'
        
        # 默认返回openclaw
        return 'openclaw'
    
    @staticmethod
    def create_adapter(platform: Optional[str] = None) -> BasePlatformAdapter:
        """创建平台适配器"""
        if platform is None:
            platform = PlatformAdapterFactory.detect_platform()
        
        home = Path.home()
        
        if platform == 'openclaw':
            config = PlatformConfig(
                platform='openclaw',
                working_dir=home / '.openclaw' / 'workspace',
                config_dir=home / '.openclaw',
                data_dir=home / '.openclaw' / 'data'
            )
            return OpenClawAdapter(config)
        
        elif platform == 'lobsterai':
            # LobsterAI使用Electron，数据存储在用户数据目录
            config = PlatformConfig(
                platform='lobsterai',
                working_dir=home / 'LobsterAI' / 'workspace',
                config_dir=home / 'LobsterAI',
                data_dir=home / 'LobsterAI'
            )
            return LobsterAIAdapter(config)
        
        else:
            raise ValueError(f"不支持的平台: {platform}")


# 便捷函数
def get_platform_adapter() -> BasePlatformAdapter:
    """获取当前平台的适配器"""
    return PlatformAdapterFactory.create_adapter()


def get_current_platform() -> str:
    """获取当前平台名称"""
    return PlatformAdapterFactory.detect_platform()
