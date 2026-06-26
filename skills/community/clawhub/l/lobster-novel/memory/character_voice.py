#!/usr/bin/env python3
"""
lobster-novel: 人物声线卡管理

每个角色有固定的说话习惯、口头禅、语气特征。
用于：
  1) 写作时注入声线描述
  2) 评审时校验角色对话一致性
"""
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional


@dataclass
class SpeechPattern:
    """一种说话模式"""
    pattern: str           # 正则模式
    description: str       # 描述
    frequency: str = "有时"  # 总是/经常/有时/偶尔


@dataclass
class CharacterVoice:
    """人物声线卡"""
    name: str
    # 基本嗓音特征
    tone: str = ""              # 低沉/清亮/沙哑/尖锐/温和
    speed: str = ""             # 语速快/中/慢
    volume: str = ""            # 声音大/中/小
    # 说话习惯
    catchphrases: List[str] = field(default_factory=list)       # 口头禅
    speech_patterns: List[SpeechPattern] = field(default_factory=list)  # 句式习惯
    opening_habit: str = ""     # 开口习惯（如"嗯…"、"那个…"）
    ending_habit: str = ""      # 结束习惯（如"……是吧？"）
    # 情绪表达特征
    angry_style: str = ""       # 生气时说话特点
    happy_style: str = ""       # 开心时说话特点
    sad_style: str = ""         # 难过时说话特点
    nervous_style: str = ""     # 紧张时说话特点
    # 词汇偏好
    common_words: List[str] = field(default_factory=list)       # 高频词汇
    avoid_words: List[str] = field(default_factory=list)        # 从不说的词
    # 文化/背景特征（基于角色背景推断）
    education_level: str = ""   # 高/中/低
    dialect_hints: List[str] = field(default_factory=list)      # 方言特征
    # 参考样本
    sample_dialogs: List[str] = field(default_factory=list)     # 该角色典型对话样本

    def to_prompt_block(self) -> str:
        """转为写作注入用文本块"""
        parts = [f"【{self.name}声线】"]
        if self.tone or self.speed or self.volume:
            parts.append(f"嗓音: {'/'.join(filter(None, [self.tone, self.speed, self.volume]))}")
        if self.catchphrases:
            parts.append(f"口头禅: {'、'.join(self.catchphrases)}")
        if self.opening_habit:
            parts.append(f"开口习惯: {self.opening_habit}")
        if self.ending_habit:
            parts.append(f"结束习惯: {self.ending_habit}")
        if self.common_words:
            parts.append(f"高频词汇: {'、'.join(self.common_words)}")
        return "\n".join(parts)


class VoiceLibrary:
    """声线库管理器"""

    FILE = "voice_library.json"

    def __init__(self, project_dir: Path):
        self.dir = Path(project_dir) / "continuity"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.file = self.dir / self.FILE
        self.voices: Dict[str, CharacterVoice] = self._load()

    def _load(self) -> Dict[str, CharacterVoice]:
        if not self.file.exists():
            return {}
        try:
            data = json.loads(self.file.read_text(encoding="utf-8"))
            return {k: CharacterVoice(**v) for k, v in data.items()}
        except Exception:
            return {}

    def save(self):
        self.file.write_text(
            json.dumps({k: asdict(v) for k, v in self.voices.items()},
                       ensure_ascii=False, indent=2),
            encoding="utf-8")

    def register(self, name: str, voice: CharacterVoice):
        """注册/更新角色声线"""
        self.voices[name] = voice
        self.save()

    def get(self, name: str) -> Optional[CharacterVoice]:
        return self.voices.get(name)

    def list_names(self) -> List[str]:
        return list(self.voices.keys())

    def get_all_prompts(self) -> str:
        """获取所有声线卡，用于写作注入"""
        parts = []
        for name, voice in sorted(self.voices.items()):
            block = voice.to_prompt_block()
            if block:
                parts.append(block)
        return "\n\n".join(parts)

    def check_dialog_consistency(self, name: str, dialog_line: str) -> List[str]:
        """检查一句台词是否符合角色声线（返回违规项列表）"""
        voice = self.voices.get(name)
        if not voice:
            return []
        issues = []
        for w in voice.avoid_words:
            if w in dialog_line:
                issues.append(f"{name}不应该说'{w}'")
        for cp in voice.catchphrases:
            # TODO: 跨对话分析时检查口头禅出现频率
            # 单句检测无法判断"没出现"口头禅
            if cp in dialog_line:
                issues.append(f"检测到{name}口头禅'{cp}'")
                break
        return issues

    def dump(self) -> str:
        """全部声线可读输出"""
        lines = [f"声线库共{len(self.voices)}个角色\n"]
        for name, v in sorted(self.voices.items()):
            lines.append(v.to_prompt_block())
            lines.append("")
        return "\n".join(lines)
