#!/usr/bin/env python3
"""
弘脑记忆系统 - 记忆检索模块
HongNao Memory OS - Memory Retrieval Module

功能：根据当前任务检索相关记忆，支持语义检索 + 关键词检索，返回重建的记忆上下文
"""

import json
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

from memory_extraction import MemCell, MemoryType


@dataclass
class RetrievalResult:
    """检索结果"""
    mem_cell: MemCell
    semantic_score: float  # 语义相似度 0-1
    keyword_score: float  # 关键词匹配度 0-1
    time_score: float  # 时间衰减分数 0-1
    importance_score: float  # 重要性分数 0-1
    final_score: float  # 综合分数 0-1
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'mem_cell': self.mem_cell.to_dict(),
            'scores': {
                'semantic': self.semantic_score,
                'keyword': self.keyword_score,
                'time': self.time_score,
                'importance': self.importance_score,
                'final': self.final_score
            }
        }


class MemoryRetriever:
    """记忆检索器"""
    
    def __init__(self, mem_cells: List[MemCell]):
        """
        初始化检索器
        
        Args:
            mem_cells: 记忆库中的 MemCell 列表
        """
        self.mem_cells = mem_cells
        self.semantic_weight = 0.5  # 语义权重
        self.keyword_weight = 0.3  # 关键词权重
        self.time_weight = 0.1  # 时间权重
        self.importance_weight = 0.1  # 重要性权重
    
    def retrieve(
        self,
        query: str,
        top_k: int = 10,
        min_score: float = 0.3
    ) -> List[RetrievalResult]:
        """
        检索相关记忆
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            min_score: 最低分数阈值
        
        Returns:
            检索结果列表（按综合分数排序）
        """
        results = []
        
        # 计算每个记忆的分数
        for cell in self.mem_cells:
            # 语义相似度（简化版：基于关键词重叠）
            semantic_score = self._calculate_semantic_similarity(query, cell.content)
            
            # 关键词匹配度
            keyword_score = self._calculate_keyword_match(query, cell)
            
            # 时间衰减分数
            time_score = self._calculate_time_decay(cell.created_at)
            
            # 重要性分数
            importance_score = cell.importance / 10.0
            
            # 综合分数
            final_score = (
                self.semantic_weight * semantic_score +
                self.keyword_weight * keyword_score +
                self.time_weight * time_score +
                self.importance_weight * importance_score
            )
            
            # 过滤低分结果
            if final_score >= min_score:
                results.append(RetrievalResult(
                    mem_cell=cell,
                    semantic_score=semantic_score,
                    keyword_score=keyword_score,
                    time_score=time_score,
                    importance_score=importance_score,
                    final_score=final_score
                ))
        
        # 按综合分数排序
        results.sort(key=lambda r: r.final_score, reverse=True)
        
        # 返回 Top-K
        return results[:top_k]
    
    def _calculate_semantic_similarity(self, query: str, content: str) -> float:
        """
        计算语义相似度（简化版：基于 TF-IDF 和关键词重叠）
        
        TODO: 替换为真实的向量相似度计算（使用 BGE-M3 等 Embedding 模型）
        
        Args:
            query: 查询文本
            content: 记忆内容
        
        Returns:
            相似度分数 0-1
        """
        # 分词（简化版：按字符和空格）
        query_tokens = set(self._tokenize(query))
        content_tokens = set(self._tokenize(content))
        
        if not query_tokens or not content_tokens:
            return 0.0
        
        # Jaccard 相似度
        intersection = query_tokens & content_tokens
        union = query_tokens | content_tokens
        
        jaccard = len(intersection) / len(union) if union else 0.0
        
        # 提升长匹配片段的分数
        common_substrings = self._count_common_substrings(query, content, min_length=2)
        substring_bonus = min(common_substrings * 0.1, 0.3)
        
        return min(jaccard + substring_bonus, 1.0)
    
    def _tokenize(self, text: str) -> List[str]:
        """
        简单分词
        
        Args:
            text: 输入文本
        
        Returns:
            分词列表
        """
        import re
        # 提取中文词汇和英文单词
        tokens = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z]+', text)
        return tokens
    
    def _count_common_substrings(self, text1: str, text2: str, min_length: int = 2) -> int:
        """
        计算公共子串数量
        
        Args:
            text1: 文本 1
            text2: 文本 2
            min_length: 最小子串长度
        
        Returns:
            公共子串数量
        """
        count = 0
        for i in range(len(text1) - min_length + 1):
            substring = text1[i:i+min_length]
            if substring in text2:
                count += 1
        return count
    
    def _calculate_keyword_match(self, query: str, cell: MemCell) -> float:
        """
        计算关键词匹配度
        
        Args:
            query: 查询文本
            cell: 记忆单元
        
        Returns:
            匹配度分数 0-1
        """
        query_tokens = set(self._tokenize(query.lower()))
        
        # 检查查询词是否出现在内容中
        content_matches = sum(1 for token in query_tokens if token in cell.content.lower())
        
        # 检查查询词是否出现在标签中
        tag_matches = sum(1 for token in query_tokens 
                         for tag in cell.tags 
                         if token in tag.lower())
        
        # 计算分数
        content_score = content_matches / len(query_tokens) if query_tokens else 0.0
        tag_bonus = min(tag_matches * 0.2, 0.4)  # 标签匹配加分
        
        return min(content_score + tag_bonus, 1.0)
    
    def _calculate_time_decay(self, created_at: str, half_life_days: int = 30) -> float:
        """
        计算时间衰减分数（基于半衰期）
        
        Args:
            created_at: 创建时间（ISO 格式）
            half_life_days: 半衰期（天）
        
        Returns:
            时间衰减分数 0-1
        """
        try:
            created_time = datetime.fromisoformat(created_at)
            now = datetime.now()
            days_elapsed = (now - created_time).days
            
            # 指数衰减
            decay = math.exp(-math.log(2) * days_elapsed / half_life_days)
            
            return decay
        except Exception:
            return 0.5  # 默认值
    
    def retrieve_by_type(
        self,
        memory_type: str,
        top_k: int = 5
    ) -> List[MemCell]:
        """
        按类型检索记忆
        
        Args:
            memory_type: 记忆类型
            top_k: 返回结果数量
        
        Returns:
            MemCell 列表
        """
        filtered = [cell for cell in self.mem_cells if cell.memory_type == memory_type]
        filtered.sort(key=lambda c: c.importance, reverse=True)
        return filtered[:top_k]
    
    def retrieve_by_tags(
        self,
        tags: List[str],
        match_all: bool = False,
        top_k: int = 10
    ) -> List[MemCell]:
        """
        按标签检索记忆
        
        Args:
            tags: 标签列表
            match_all: 是否匹配所有标签
            top_k: 返回结果数量
        
        Returns:
            MemCell 列表
        """
        if match_all:
            # 匹配所有标签
            filtered = [
                cell for cell in self.mem_cells
                if all(tag in cell.tags for tag in tags)
            ]
        else:
            # 匹配任意标签
            filtered = [
                cell for cell in self.mem_cells
                if any(tag in cell.tags for tag in tags)
            ]
        
        filtered.sort(key=lambda c: c.importance, reverse=True)
        return filtered[:top_k]
    
    def rebuild_context(
        self,
        results: List[RetrievalResult],
        max_tokens: int = 1000
    ) -> str:
        """
        重建记忆上下文
        
        Args:
            results: 检索结果
            max_tokens: 最大 Token 数（简化版：按字符数估算）
        
        Returns:
            重建的上下文文本
        """
        if not results:
            return ""
        
        context_parts = []
        current_length = 0
        
        for result in results:
            cell = result.mem_cell
            # 格式化记忆条目
            entry = f"[{cell.memory_type}] {cell.content}"
            entry_length = len(entry)
            
            if current_length + entry_length > max_tokens:
                break
            
            context_parts.append(entry)
            current_length += entry_length
        
        return "\n".join(context_parts)


class HybridRetriever:
    """混合检索器 - 结合语义检索和关键词检索"""
    
    def __init__(self, mem_cells: List[MemCell]):
        """
        初始化混合检索器
        
        Args:
            mem_cells: 记忆库中的 MemCell 列表
        """
        self.semantic_retriever = MemoryRetriever(mem_cells)
        self.keyword_retriever = MemoryRetriever(mem_cells)
        # 调整权重
        self.semantic_retriever.semantic_weight = 0.6
        self.semantic_retriever.keyword_weight = 0.2
        self.keyword_retriever.semantic_weight = 0.2
        self.keyword_retriever.keyword_weight = 0.6
    
    def retrieve(
        self,
        query: str,
        top_k: int = 10,
        min_score: float = 0.3
    ) -> List[RetrievalResult]:
        """
        混合检索：语义 + 关键词
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            min_score: 最低分数阈值
        
        Returns:
            检索结果列表
        """
        # 语义检索
        semantic_results = self.semantic_retriever.retrieve(
            query, top_k=top_k * 2, min_score=min_score
        )
        
        # 关键词检索
        keyword_results = self.keyword_retriever.retrieve(
            query, top_k=top_k * 2, min_score=min_score
        )
        
        # 合并结果（去重）
        merged = {}
        for result in semantic_results + keyword_results:
            cell_id = result.mem_cell.id
            if cell_id not in merged:
                merged[cell_id] = result
            else:
                # 取最高分
                existing = merged[cell_id]
                if result.final_score > existing.final_score:
                    merged[cell_id] = result
        
        # 排序并返回 Top-K
        final_results = list(merged.values())
        final_results.sort(key=lambda r: r.final_score, reverse=True)
        
        return final_results[:top_k]
    
    def rebuild_context(self, results: List[RetrievalResult], max_tokens: int = 1000) -> str:
        """委托给语义检索器"""
        return self.semantic_retriever.rebuild_context(results, max_tokens)


def test_retriever():
    """测试记忆检索器"""
    from memory_extraction import MemoryExtractor
    from memory_consolidation import MemoryConsolidator
    
    print("=" * 60)
    print("弘脑记忆系统 - 记忆检索模块测试")
    print("=" * 60)
    
    # 创建测试数据
    extractor = MemoryExtractor()
    test_text = """
    用户叫唐锋，在燧弘华创工作，职位是执行总裁。
    用户喜欢简洁商务风格，偏好使用 PPT 做演示。
    用户讨厌复杂的流程，习惯高效执行。
    项目预算为 100 万元。
    必须保证数据安全，不能泄露敏感信息。
    燧弘华创是 AI 云平台公司，专注于智慧大脑架构。
    """
    
    mem_cells = extractor.extract_from_text(test_text, source="test")
    
    # 巩固处理
    consolidator = MemoryConsolidator()
    consolidated_cells = consolidator.consolidate(mem_cells)
    
    print(f"\n记忆库：{len(consolidated_cells)} 条记忆\n")
    
    # 测试检索
    retriever = HybridRetriever(consolidated_cells)
    
    test_queries = [
        "用户信息",
        "偏好风格",
        "数据安全",
        "燧弘华创公司",
    ]
    
    for query in test_queries:
        print("=" * 60)
        print(f"查询：{query}")
        print("=" * 60)
        
        results = retriever.retrieve(query, top_k=3)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. [{result.mem_cell.memory_type}] {result.mem_cell.content}")
            print(f"   综合分数：{result.final_score:.3f}")
            print(f"   语义：{result.semantic_score:.3f} | 关键词：{result.keyword_score:.3f}")
            print(f"   时间：{result.time_score:.3f} | 重要性：{result.importance_score:.3f}")
        
        # 重建上下文
        context = retriever.rebuild_context(results, max_tokens=200)
        print(f"\n重建上下文:\n{context}")
        print()
    
    return retriever


if __name__ == '__main__':
    test_retriever()
