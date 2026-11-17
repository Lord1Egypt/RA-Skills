"""
双轨并行架构 - 提取器基类

所有链提取器的抽象基类，定义公共接口和工具方法。
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
import re
from datetime import datetime


class ExtractionResult:
    """
    提取结果
    
    Attributes:
        success: 是否成功
        chains: 提取的链列表
        confidence: 整体置信度
        message: 结果信息
    """
    
    def __init__(
        self,
        success: bool,
        chains: list,
        confidence: float = 0.0,
        message: str = "",
    ):
        self.success = success
        self.chains = chains
        self.confidence = confidence
        self.message = message
    
    def __repr__(self) -> str:
        return (
            f"ExtractionResult(success={self.success}, "
            f"chains={len(self.chains)}, "
            f"confidence={self.confidence:.2f})"
        )


class BaseExtractor(ABC):
    """
    链提取器基类
    
    所有链类型提取器的公共基类，提供：
    - 文本分句
    - 关键词匹配
    - 置信度计算
    - 批量提取
    """
    
    # 提取器名称（子类覆盖）
    extractor_name: str = "base"
    
    def __init__(self, config: Optional[dict] = None):
        """
        初始化提取器
        
        Args:
            config: 配置字典，支持以下键：
                - min_confidence: 最小置信度阈值（默认0.3）
                - max_chain_length: 最大链长度（默认100）
        """
        self.config = config or {}
        self.min_confidence = self.config.get("min_confidence", 0.3)
        self.max_chain_length = self.config.get("max_chain_length", 100)
    
    @abstractmethod
    def extract(self, text: str, **kwargs) -> list:
        """
        从文本中提取链
        
        Args:
            text: 输入文本
            **kwargs: 额外参数
        
        Returns:
            提取的链列表
        """
        pass
    
    def extract_batch(self, texts: List[str], **kwargs) -> List[ExtractionResult]:
        """
        批量提取
        
        Args:
            texts: 文本列表
            **kwargs: 额外参数
        
        Returns:
            提取结果列表
        """
        return [self._wrap_extract(text, **kwargs) for text in texts]
    
    def _wrap_extract(self, text: str, **kwargs) -> ExtractionResult:
        """
        包装提取过程，统一处理异常
        
        Args:
            text: 输入文本
            **kwargs: 额外参数
        
        Returns:
            提取结果
        """
        try:
            chains = self.extract(text, **kwargs)
            if chains:
                avg_conf = sum(
                    getattr(c, "extraction_confidence", 0.0)
                    for c in chains
                ) / len(chains)
                return ExtractionResult(
                    success=True,
                    chains=chains,
                    confidence=avg_conf,
                    message=f"成功提取 {len(chains)} 个链",
                )
            return ExtractionResult(
                success=True,
                chains=[],
                confidence=0.0,
                message="未提取到链",
            )
        except Exception as e:
            return ExtractionResult(
                success=False,
                chains=[],
                confidence=0.0,
                message=f"提取失败: {str(e)}",
            )
    
    # ========== 工具方法 ==========
    
    @staticmethod
    def split_sentences(text: str) -> List[str]:
        """
        将文本分句
        
        Args:
            text: 输入文本
        
        Returns:
            句子列表
        """
        # 支持中英文标点
        pattern = r'[。！？\.!?]\s*'
        sentences = re.split(pattern, text)
        return [s.strip() for s in sentences if s.strip()]
    
    @staticmethod
    def split_paragraphs(text: str) -> List[str]:
        """
        将文本分段
        
        Args:
            text: 输入文本
        
        Returns:
            段落列表
        """
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    @staticmethod
    def find_keywords(text: str, keywords: List[str]) -> List[Tuple[str, int]]:
        """
        查找关键词及其位置
        
        Args:
            text: 输入文本
            keywords: 关键词列表
        
        Returns:
            (关键词, 位置) 列表
        """
        results = []
        for kw in keywords:
            for match in re.finditer(re.escape(kw), text, re.IGNORECASE):
                results.append((kw, match.start()))
        return sorted(results, key=lambda x: x[1])
    
    @staticmethod
    def find_patterns(text: str, patterns: List[str]) -> List[Tuple[str, int, int]]:
        """
        查找正则模式及其位置
        
        Args:
            text: 输入文本
            patterns: 正则模式列表
        
        Returns:
            (匹配文本, 起始位置, 结束位置) 列表
        """
        results = []
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
                results.append((match.group(), match.start(), match.end()))
        return sorted(results, key=lambda x: x[1])
    
    @staticmethod
    def calculate_confidence(
        positive_matches: int,
        total_clues: int,
        min_ratio: float = 0.2
    ) -> float:
        """
        计算置信度
        
        Args:
            positive_matches: 正向匹配数
            total_clues: 总线索数
            min_ratio: 最小比率
        
        Returns:
            置信度 (0.0 - 1.0)
        """
        if total_clues == 0:
            return 0.0
        ratio = positive_matches / total_clues
        if ratio < min_ratio:
            return 0.0
        return min(1.0, ratio * 1.5)
    
    @staticmethod
    def extract_list_items(text: str) -> List[str]:
        """
        提取列表项（编号列表或项目符号列表）
        
        Args:
            text: 输入文本
        
        Returns:
            列表项列表
        """
        items = []
        
        # 匹配编号列表：1. 2. 3. 或 1) 2) 3)
        numbered = re.findall(
            r'(?:^|\n)\s*(?:\d+[\.\)]\s*)(.*?)(?=\n\s*(?:\d+[\.\)]|$)|\Z)',
            text,
            re.MULTILINE
        )
        items.extend([item.strip() for item in numbered if item.strip()])
        
        # 匹配项目符号列表：- * + 
        bulleted = re.findall(
            r'(?:^|\n)\s*[-*+]\s+(.*?)(?=\n\s*[-*+]|\Z)',
            text,
            re.MULTILINE
        )
        items.extend([item.strip() for item in bulleted if item.strip()])
        
        return items
    
    @staticmethod
    def extract_time_expressions(text: str) -> List[str]:
        """
        提取时间表达式
        
        Args:
            text: 输入文本
        
        Returns:
            时间表达式列表
        """
        time_patterns = [
            # 日期格式：YYYY-MM-DD, YYYY/MM/DD
            r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?',
            # 时间格式：HH:MM, HH:MM:SS
            r'\d{1,2}:\d{2}(?::\d{2})?',
            # 中文时间词
            r'(?:今天|明天|昨天|后天|前天|早上|上午|中午|下午|晚上|深夜)',
            # 相对时间
            r'(?:刚才|刚刚|不久|之前|之后|随后|立即|马上)',
            # 时间段
            r'(?:最近|近期|长期|短期|长期以来|多年来|近年来)',
        ]
        
        expressions = []
        for pattern in time_patterns:
            for match in re.finditer(pattern, text):
                expressions.append(match.group())
        
        return expressions