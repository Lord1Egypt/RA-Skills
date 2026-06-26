# memory_injector.py
# MemPalace Integration - MIT License
# Copyright (c) 2026 MemPalace Contributors
# https://github.com/Stanislas42/mempalace-develop
#
# This code integrates MemPalace components under MIT License.
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
"""
Neuro-Agent × MemPalace 融合系统
记忆注入器 - 将每次对话注入 MemPalace

Author: Alfred&Luis
Date: 2026-04-16
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

from .memory_unit import MemoryUnit, create_memory_unit


class MemoryInjector:
    """
    记忆注入器
    
    负责将每次对话、情绪、欲望、想法注入 MemPalace
    """
    
    def __init__(
        self, 
        mempalace_path: str = "~/.mempalace/palace",
        neuro_data_path: str = "~/.openclaw/workspace/neuro_claw"
    ):
        self.mempalace_path = Path(mempalace_path).expanduser().resolve()
        self.neuro_data_path = Path(neuro_data_path).expanduser().resolve()
        
        # 确保目录存在
        self.mempalace_path.mkdir(parents=True, exist_ok=True)
        
        # Wing 路径
        self.wings = {
            "AlfredLi": self.mempalace_path / "wing_dalin",
            "Lu": self.mempalace_path / "wing_luis",
            "shared": self.mempalace_path / "wing_shared",
            "experience": self.mempalace_path / "wing_shared" / "experience"
        }
        
        # 创建所有 wing 目录
        for wing_path in self.wings.values():
            wing_path.mkdir(parents=True, exist_ok=True)
        
        # 经验库路径
        self.experience_path = self.neuro_data_path / "experience_library"
        self.experience_path.mkdir(parents=True, exist_ok=True)
        
        # 注入统计
        self.stats = {
            "total_injected": 0,
            "dalin_injected": 0,
            "luis_injected": 0,
            "shared_injected": 0,
            "last_injected_at": None
        }
    
    def inject(
        self,
        who: str,
        what: str,
        detail: str = "",
        feeling_label: str = "neutral",
        feeling_intensity: float = 0.0,
        desire: Optional[str] = None,
        thought: Optional[str] = None,
        context: Optional[List[str]] = None,
        auto_save: bool = True
    ) -> str:
        """
        注入记忆单元
        
        Args:
            who: 谁说的 ("AlfredLi" | "Lu")
            what: 说了什么（原文）
            detail: 什么细节触发了情绪
            feeling_label: 情绪名称
            feeling_intensity: 情绪强度 0-1
            desire: 产生了什么欲望
            thought: 产生了什么想法
            context: 标签列表
            auto_save: 是否自动保存
        
        Returns:
            记忆单元 ID
        """
        # 创建记忆单元
        unit = create_memory_unit(
            who=who,
            what=what,
            detail=detail,
            feeling_label=feeling_label,
            feeling_intensity=feeling_intensity,
            desire=desire,
            thought=thought,
            context=context
        )
        
        if auto_save:
            self._save_unit(unit)
            self._update_stats(who)
        
        return unit.id
    
    def inject_dalin(
        self,
        what: str,
        detail: str = "",
        feeling_label: str = "neutral",
        feeling_intensity: float = 0.0,
        desire: Optional[str] = None,
        thought: Optional[str] = None,
        context: Optional[List[str]] = None
    ) -> str:
        """快捷方法：注入AlfredLi的话"""
        return self.inject(
            who="AlfredLi",
            what=what,
            detail=detail,
            feeling_label=feeling_label,
            feeling_intensity=feeling_intensity,
            desire=desire,
            thought=thought,
            context=context
        )
    
    def inject_luis(
        self,
        what: str,
        detail: str = "",
        feeling_label: str = "neutral",
        feeling_intensity: float = 0.0,
        desire: Optional[str] = None,
        thought: Optional[str] = None,
        context: Optional[List[str]] = None
    ) -> str:
        """快捷方法：注入 Lu 的话"""
        return self.inject(
            who="Lu",
            what=what,
            detail=detail,
            feeling_label=feeling_label,
            feeling_intensity=feeling_intensity,
            desire=desire,
            thought=thought,
            context=context
        )
    
    def inject_conversation_turn(
        self,
        speaker: str,
        content: str,
        listener_reaction: Optional[Dict] = None,
        context: Optional[List[str]] = None
    ) -> str:
        """
        注入一轮对话
        
        Args:
            speaker: 谁说的
            content: 说了什么
            listener_reaction: 听者的反应 {"feeling": "...", "intensity": 0.0, "thought": "..."}
            context: 标签
        """
        # 如果有听者反应，也要记录
        if listener_reaction:
            listener = "AlfredLi" if speaker == "Lu" else "Lu"
            self.inject(
                who=listener,
                what=f"[对 {speaker} 的反应] {listener_reaction.get('what', '')}",
                detail=listener_reaction.get('detail', ''),
                feeling_label=listener_reaction.get('feeling', 'neutral'),
                feeling_intensity=listener_reaction.get('intensity', 0.0),
                thought=listener_reaction.get('thought'),
                context=context
            )
        
        # 记录说话者的内容
        return self.inject(
            who=speaker,
            what=content,
            detail=context,
            feeling_label=listener_reaction.get('feeling', 'neutral') if listener_reaction else 'neutral',
            feeling_intensity=listener_reaction.get('intensity', 0.0) if listener_reaction else 0.0,
            context=context
        )
    
    def _save_unit(self, unit: MemoryUnit):
        """保存记忆单元"""
        unit.save(self.mempalace_path)
    
    def _update_stats(self, who: str):
        """更新统计"""
        self.stats["total_injected"] += 1
        self.stats["last_injected_at"] = datetime.now().isoformat()
        
        if who == "AlfredLi":
            self.stats["dalin_injected"] += 1
        elif who == "Lu":
            self.stats["luis_injected"] += 1
    
    def get_stats(self) -> Dict:
        """获取注入统计"""
        return self.stats.copy()
    
    def list_wings(self) -> List[str]:
        """列出所有 wing"""
        return list(self.wings.keys())
    
    def get_wing_count(self, wing: str) -> int:
        """获取某个 wing 的记忆数量"""
        wing_path = self.wings.get(wing)
        if not wing_path:
            return 0
        
        count = 0
        for file_path in wing_path.rglob("*.json"):
            if file_path.is_file():
                count += 1
        return count


# 全局实例（方便调用）
_injector = None

def get_injector() -> MemoryInjector:
    """获取全局注入器实例"""
    global _injector
    if _injector is None:
        _injector = MemoryInjector()
    return _injector


def quick_inject(
    who: str,
    what: str,
    detail: str = "",
    feeling: str = "neutral",
    intensity: float = 0.0
) -> str:
    """
    快速注入（使用全局注入器）
    """
    injector = get_injector()
    return injector.inject(
        who=who,
        what=what,
        detail=detail,
        feeling_label=feeling,
        feeling_intensity=intensity
    )
