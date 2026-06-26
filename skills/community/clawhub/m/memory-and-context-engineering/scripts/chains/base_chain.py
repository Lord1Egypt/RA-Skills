"""
双轨并行架构 - 链基类模块

本模块定义所有链类型的基类和通用接口。
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field
import uuid
from enum import Enum


class ChainType(str, Enum):
    """链类型枚举"""
    CAUSAL = "causal"
    LOGIC = "logic"
    OPERATION = "operation"
    NARRATIVE = "narrative"
    TIME = "time"


class BaseExtractedChain(BaseModel, ABC):
    """
    提取链的基类
    
    所有链类型必须继承此类，实现统一的接口。
    
    Attributes:
        chain_id: 链唯一标识符
        chain_type: 链类型
        content: 原始文本内容
        extraction_confidence: 提取置信度（0-1）
        created_at: 创建时间
        metadata: 扩展元数据
    """
    
    # 基础字段
    chain_id: str = Field(
        default_factory=lambda: f"chain_{uuid.uuid4().hex[:8]}",
        description="链唯一标识符"
    )
    chain_type: ChainType = Field(description="链类型")
    content: str = Field(description="原始文本内容")
    extraction_confidence: float = Field(
        ge=0.0,
        le=1.0,
        default=0.5,
        description="提取置信度"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="创建时间"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="扩展元数据"
    )
    
    @abstractmethod
    def to_summary(self) -> str:
        """
        生成摘要（子类必须实现）
        
        Returns:
            摘要文本
        """
        raise NotImplementedError
    
    def to_dict(self) -> dict[str, Any]:
        """
        转换为字典（用于序列化）
        
        Returns:
            字典表示
        """
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BaseExtractedChain":
        """
        从字典创建实例
        
        Args:
            data: 字典数据
        
        Returns:
            链实例
        """
        return cls(**data)
    
    def is_valid(self) -> bool:
        """
        检查链是否有效
        
        Returns:
            是否有效
        """
        return (
            len(self.content.strip()) > 0 and
            0.0 <= self.extraction_confidence <= 1.0
        )
