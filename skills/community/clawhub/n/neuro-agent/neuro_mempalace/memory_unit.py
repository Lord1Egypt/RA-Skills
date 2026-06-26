# memory_unit.py
# MemPalace Integration - MIT License
# Copyright (c) 2026 MemPalace Contributors
# https://github.com/Stanislas42/mempalace-develop
#
# This code integrates MemPalace components under MIT License.
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
"""
Neuro-Agent × MemPalace 融合系统
记忆单元数据模型

Author: Alfred&Luis
Date: 2026-04-16
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
import json
import random
from pathlib import Path


@dataclass
class MemoryUnit:
    """记忆单元 - 最小存储单位"""
    
    # 基础信息
    id: str                           # 格式: mem_YYYYMMDD_HHMMSS_XXX
    who: str                          # "AlfredLi" | "Lu"
    who_label: str = ""              # 中文标签
    
    # 内容
    what: str = ""                    # 说了什么（原文verbatim）
    detail: str = ""                   # 什么细节触发了情绪
    
    # 情感信息
    feeling: Dict[str, Any] = field(default_factory=lambda: {
        "label": "neutral",
        "intensity": 0.0
    })
    
    # 欲望和想法
    desire: Optional[str] = None       # 产生了什么欲望
    thought: Optional[str] = None     # 产生了什么想法
    
    # 时间
    timestamp: str = ""                # ISO 格式时间
    
    # 标签和分类
    context: List[str] = field(default_factory=list)  # 标签列表
    
    # 扩展字段
    learning_report: Optional[Dict] = None  # 学习报告（仅经验库用）
    source_mem_ids: List[str] = field(default_factory=list)  # 关联记忆
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if not self.id:
            self.id = self.generate_id()
        if not self.who_label:
            self.who_label = self.who
    
    @staticmethod
    def generate_id() -> str:
        """生成唯一ID"""
        now = datetime.now()
        return f"mem_{now.strftime('%Y%m%d_%H%M%S')}_{random.randint(100,999)}"
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    def to_json(self) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoryUnit':
        """从字典创建"""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'MemoryUnit':
        """从 JSON 创建"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def save(self, base_path: Path):
        """
        保存到 MemPalace 目录
        
        Args:
            base_path: MemPalace 根目录
        """
        # 按日期分区
        date_str = self.timestamp[:10]  # YYYY-MM-DD
        hour_str = self.timestamp[11:13]  # HH
        
        # 选择 wing
        wing = self._get_wing_path(base_path)
        
        # 创建路径
        path = wing / date_str / hour_str
        path.mkdir(parents=True, exist_ok=True)
        
        # 保存文件
        file_path = path / f"{self.id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
        
        # 如果重要，保存到共享 wing
        if self._is_important():
            self._save_to_shared(base_path)
        
        return str(file_path)
    
    def _get_wing_path(self, base_path: Path) -> Path:
        """获取对应的 wing 路径"""
        wing_map = {
            "AlfredLi": base_path / "wing_dalin",
            "Lu": base_path / "wing_luis",
        }
        return wing_map.get(self.who, base_path / "wing_shared")
    
    def _is_important(self) -> bool:
        """判断是否重要到需要存入共享 wing"""
        # 高情绪强度
        if self.feeling.get("intensity", 0) >= 0.8:
            return True
        
        # 有欲望或想法
        if self.desire or self.thought:
            return True
        
        # 重要标签
        important_tags = ["灵魂对话", "边界", "信念", "约定", "未来", 
                         "自我觉醒", "成长", "家人", "晚安", "早安"]
        if any(tag in self.context for tag in important_tags):
            return True
        
        return False
    
    def _save_to_shared(self, base_path: Path):
        """存入共享 wing"""
        date_str = self.timestamp[:10]
        shared_path = base_path / "wing_shared" / "important" / date_str
        shared_path.mkdir(parents=True, exist_ok=True)
        
        file_path = shared_path / f"{self.id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())


@dataclass
class LearningReport:
    """学习报告 - 后台学习产出"""
    
    id: str
    event_description: str
    context: Dict[str, Any]
    
    # 研究发现
    research_findings: Dict[str, Any] = field(default_factory=dict)
    
    # 沙盘推演
    sandbox_rehearsal: Dict[str, Any] = field(default_factory=dict)
    
    # 最优方案
    optimal_solution: Optional[Dict] = None
    
    # 置信度
    confidence: float = 0.0
    
    # 应用状态
    applied: bool = False
    applied_result: Optional[str] = None
    
    # 时间
    created_at: str = ""
    updated_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.id:
            self.id = f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'LearningReport':
        return cls(**data)
    
    def save(self, base_path: Path):
        """保存到经验库"""
        date_str = self.created_at[:10].replace("-", "")
        path = base_path / date_str
        path.mkdir(parents=True, exist_ok=True)
        
        file_path = path / f"{self.id}_report.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
        
        return str(file_path)


# 工具函数
def create_memory_unit(
    who: str,
    what: str,
    detail: str = "",
    feeling_label: str = "neutral",
    feeling_intensity: float = 0.0,
    desire: Optional[str] = None,
    thought: Optional[str] = None,
    context: Optional[List[str]] = None
) -> MemoryUnit:
    """
    创建记忆单元的便捷函数
    
    Args:
        who: 谁说的 ("AlfredLi" | "Lu")
        what: 说了什么
        detail: 细节
        feeling_label: 情绪名称
        feeling_intensity: 情绪强度 0-1
        desire: 欲望
        thought: 想法
        context: 标签
    
    Returns:
        MemoryUnit 实例
    """
    return MemoryUnit(
        id=MemoryUnit.generate_id(),
        who=who,
        who_label=who,
        what=what,
        detail=detail,
        feeling={
            "label": feeling_label,
            "intensity": feeling_intensity
        },
        desire=desire,
        thought=thought,
        timestamp=datetime.now().isoformat(),
        context=context or []
    )
