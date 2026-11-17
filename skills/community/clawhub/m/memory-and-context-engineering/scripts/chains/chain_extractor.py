"""
双轨并行架构 - 统一的链提取器入口

提供统一的链提取接口，支持自动选择提取器或指定链类型。
"""

from typing import List, Optional, Type, Dict, Any
from .base_chain import BaseExtractedChain, ChainType
from .extractors import (
    BaseExtractor,
    CausalExtractor,
    LogicExtractor,
    OperationExtractor,
    NarrativeExtractor,
    TimeExtractor,
    ExtractionResult,
)
from .chain_buffer import ChainBuffer


# 提取器注册表
_EXTRACTOR_REGISTRY: Dict[ChainType, Type[BaseExtractor]] = {
    ChainType.CAUSAL: CausalExtractor,
    ChainType.LOGIC: LogicExtractor,
    ChainType.OPERATION: OperationExtractor,
    ChainType.NARRATIVE: NarrativeExtractor,
    ChainType.TIME: TimeExtractor,
}


class ChainExtractor:
    """
    链提取器（统一入口）
    
    支持自动识别链类型或指定类型提取。
    
    Attributes:
        config: 全局配置
        extractors: 已初始化的提取器实例
    """
    
    def __init__(self, config: Optional[dict] = None):
        """
        初始化链提取器
        
        Args:
            config: 全局配置字典，传递给所有提取器
        """
        self.config = config or {}
        self.extractors: Dict[ChainType, BaseExtractor] = {}
        
        # 初始化所有提取器
        for chain_type, extractor_cls in _EXTRACTOR_REGISTRY.items():
            self.extractors[chain_type] = extractor_cls(config)
    
    def extract(
        self,
        text: str,
        chain_type: Optional[ChainType] = None,
        **kwargs
    ) -> ExtractionResult:
        """
        从文本中提取链
        
        Args:
            text: 输入文本
            chain_type: 指定链类型（None=自动检测所有类型）
            **kwargs: 额外参数
        
        Returns:
            提取结果
        """
        if not text or not text.strip():
            return ExtractionResult(False, [], 0.0, "输入文本为空")
        
        if chain_type:
            # 指定类型提取
            extractor = self.extractors.get(chain_type)
            if not extractor:
                return ExtractionResult(
                    False, [], 0.0, f"不支持的链类型: {chain_type}"
                )
            return extractor._wrap_extract(text, **kwargs)
        
        # 自动检测：尝试所有提取器，合并结果
        all_chains = []
        total_confidence = 0.0
        extractor_count = 0
        
        for extractor in self.extractors.values():
            result = extractor._wrap_extract(text, **kwargs)
            if result.success and result.chains:
                all_chains.extend(result.chains)
                total_confidence += result.confidence
                extractor_count += 1
        
        if not all_chains:
            return ExtractionResult(
                True, [], 0.0, "未提取到任何链"
            )
        
        avg_confidence = total_confidence / max(extractor_count, 1)
        return ExtractionResult(
            success=True,
            chains=all_chains,
            confidence=avg_confidence,
            message=f"提取到 {len(all_chains)} 个链（{extractor_count} 种类型）",
        )
    
    def extract_all(self, text: str, **kwargs) -> Dict[str, ExtractionResult]:
        """
        从文本中提取所有类型的链
        
        Args:
            text: 输入文本
            **kwargs: 额外参数
        
        Returns:
            链类型到提取结果的映射
        """
        results = {}
        for chain_type, extractor in self.extractors.items():
            results[chain_type.value] = extractor._wrap_extract(text, **kwargs)
        return results
    
    def extract_batch(
        self,
        texts: List[str],
        chain_type: Optional[ChainType] = None,
        **kwargs
    ) -> List[ExtractionResult]:
        """
        批量提取
        
        Args:
            texts: 文本列表
            chain_type: 指定链类型
            **kwargs: 额外参数
        
        Returns:
            提取结果列表
        """
        return [
            self.extract(text, chain_type, **kwargs)
            for text in texts
        ]
    
    def get_available_types(self) -> List[ChainType]:
        """获取支持的链类型列表"""
        return list(_EXTRACTOR_REGISTRY.keys())
    
    def get_stats(self) -> Dict[str, Any]:
        """获取提取器统计信息"""
        stats = {
            "total_extractors": len(self.extractors),
            "available_types": [t.value for t in self.get_available_types()],
        }
        return stats