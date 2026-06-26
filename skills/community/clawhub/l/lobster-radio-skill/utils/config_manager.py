"""
配置管理模块

负责读取和保存用户配置到MEMORY.md。
"""

import re
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class TTSConfig:
    """TTS配置"""
    provider: str = "qwen3-tts"
    model: str = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"
    voice: str = "xiaoxiao"  # 默认使用晓晓音色（女声，适合新闻播报）
    emotion: str = "neutral"
    speed: float = 1.0
    pitch: float = 1.0
    use_gpu: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


@dataclass
class UserPreferences:
    """用户偏好"""
    subscribed_tags: list = None
    default_topics: list = None
    language: str = "zh-CN"
    
    def __post_init__(self):
        if self.subscribed_tags is None:
            self.subscribed_tags = []
        if self.default_topics is None:
            self.default_topics = []
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


class ConfigManager:
    """
    配置管理器
    
    负责读取和保存用户配置到OpenClaw的MEMORY.md。
    """
    
    def __init__(self, memory_file: Optional[Path] = None):
        """
        初始化配置管理器
        
        Args:
            memory_file: MEMORY.md文件路径
        """
        if memory_file is None:
            memory_file = Path.home() / ".openclaw" / "MEMORY.md"
        
        self.memory_file = Path(memory_file)
        self._ensure_memory_file()
    
    def _ensure_memory_file(self):
        """确保MEMORY.md文件存在"""
        if not self.memory_file.exists():
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            self.memory_file.write_text("# User Memory\n\n", encoding='utf-8')
    
    def _read_memory(self) -> str:
        """读取MEMORY.md内容"""
        try:
            return self.memory_file.read_text(encoding='utf-8')
        except Exception:
            return "# User Memory\n\n"
    
    def _write_memory(self, content: str):
        """写入MEMORY.md内容"""
        try:
            self.memory_file.write_text(content, encoding='utf-8')
        except Exception as e:
            raise RuntimeError(f"Failed to write MEMORY.md: {e}")
    
    def get_tts_config(self) -> TTSConfig:
        """
        获取TTS配置
        
        Returns:
            TTSConfig: TTS配置
        """
        content = self._read_memory()
        
        config = TTSConfig()
        
        provider_match = re.search(r'Provider:\s*(\S+)', content)
        if provider_match:
            config.provider = provider_match.group(1)
        
        model_match = re.search(r'Model:\s*(\S+)', content)
        if model_match:
            config.model = model_match.group(1)
        
        voice_match = re.search(r'Voice:\s*(\S+)', content)
        if voice_match:
            config.voice = voice_match.group(1)
        
        emotion_match = re.search(r'Emotion:\s*(\S+)', content)
        if emotion_match:
            config.emotion = emotion_match.group(1)
        
        speed_match = re.search(r'Speed:\s*([\d.]+)', content)
        if speed_match:
            config.speed = float(speed_match.group(1))
        
        pitch_match = re.search(r'Pitch:\s*([\d.]+)', content)
        if pitch_match:
            config.pitch = float(pitch_match.group(1))
        
        return config
    
    def save_tts_config(self, config: TTSConfig):
        """
        保存TTS配置
        
        Args:
            config: TTS配置
        """
        content = self._read_memory()
        
        tts_section = f"""
## TTS Configuration
- Provider: {config.provider}
- Model: {config.model}
- Voice: {config.voice}
- Emotion: {config.emotion}
- Speed: {config.speed}
- Pitch: {config.pitch}
"""
        
        if "## TTS Configuration" in content:
            content = re.sub(
                r'## TTS Configuration.*?(?=\n##|\Z)',
                tts_section.strip(),
                content,
                flags=re.DOTALL
            )
        else:
            content += "\n" + tts_section
        
        self._write_memory(content)
    
    def get_user_preferences(self) -> UserPreferences:
        """
        获取用户偏好
        
        Returns:
            UserPreferences: 用户偏好
        """
        content = self._read_memory()
        
        preferences = UserPreferences()
        
        tags_match = re.search(r'Subscribed Tags:\s*(.+)', content)
        if tags_match:
            tags_str = tags_match.group(1)
            preferences.subscribed_tags = [
                tag.strip() for tag in tags_str.split(',') if tag.strip()
            ]
        
        topics_match = re.search(r'Default Topics:\s*(.+)', content)
        if topics_match:
            topics_str = topics_match.group(1)
            preferences.default_topics = [
                topic.strip() for topic in topics_str.split(',') if topic.strip()
            ]
        
        language_match = re.search(r'Language:\s*(\S+)', content)
        if language_match:
            preferences.language = language_match.group(1)
        
        return preferences
    
    def save_user_preferences(self, preferences: UserPreferences):
        """
        保存用户偏好
        
        Args:
            preferences: 用户偏好
        """
        content = self._read_memory()
        
        prefs_section = f"""
## Radio Preferences
- Subscribed Tags: {', '.join(preferences.subscribed_tags)}
- Default Topics: {', '.join(preferences.default_topics)}
- Language: {preferences.language}
"""
        
        if "## Radio Preferences" in content:
            content = re.sub(
                r'## Radio Preferences.*?(?=\n##|\Z)',
                prefs_section.strip(),
                content,
                flags=re.DOTALL
            )
        else:
            content += "\n" + prefs_section
        
        self._write_memory(content)
