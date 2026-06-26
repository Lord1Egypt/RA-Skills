#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BM25知识库 - 纯Python实现，零依赖
集成到现有的gitcode-issue-reply skill中，替换原有的简单相似Issue匹配
"""

import json
import math
import re
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class Document:
    """文档结构"""
    doc_id: str
    title: str
    content: str
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class SearchResult:
    """搜索结果"""
    doc_id: str
    score: float
    document: Document


class BM25KnowledgeBase:
    """
    BM25算法实现的知识库
    
    特点：
    - 纯Python实现，零外部依赖
    - 支持增量添加文档
    - 支持持久化和加载
    - 毫秒级查询响应
    - 内存占用低，支持10万级文档
    """
    
    # BM25算法参数
    DEFAULT_K1 = 1.5  # 词频饱和参数，通常1.2-2.0
    DEFAULT_B = 0.75   # 文档长度归一化参数，通常0.75
    DEFAULT_TOP_K = 3  # 默认返回前3个结果
    
    def __init__(self, k1: float = None, b: float = None):
        """初始化BM25知识库"""
        self.k1 = k1 or self.DEFAULT_K1
        self.b = b or self.DEFAULT_B
        
        # 文档存储
        self.documents: Dict[str, Document] = {}
        
        # 倒排索引: term -> {doc_id: frequency}
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        
        # 文档频率: term -> number of documents containing term
        self.doc_freq: Dict[str, int] = {}
        
        # 文档长度
        self.doc_length: Dict[str, int] = {}
        
        # 统计信息
        self.total_docs = 0
        self.avg_doc_len = 0.0
        self.total_doc_len = 0
        
        # 停用词
        self.stop_words = self._get_default_stop_words()
    
    def add_document(self, doc_id: str, content: str, title: str = "", metadata: Dict = None) -> bool:
        """
        添加单个文档
        
        Args:
            doc_id: 文档唯一ID，通常是Issue编号
            content: 文档内容（Issue的标题+正文+解决方案）
            title: 文档标题（可选）
            metadata: 元数据（可选，保存标签、创建时间等）
        
        Returns:
            bool: 是否添加成功
        """
        if doc_id in self.documents:
            return False  # 已存在，不重复添加
        
        # 分词
        tokens = self._tokenize(content)
        if not tokens:
            return False
        
        # 存储文档
        doc = Document(
            doc_id=doc_id,
            title=title,
            content=content,
            metadata=metadata
        )
        self.documents[doc_id] = doc
        
        # 更新文档长度
        doc_len = len(tokens)
        self.doc_length[doc_id] = doc_len
        self.total_doc_len += doc_len
        self.total_docs += 1
        self.avg_doc_len = self.total_doc_len / self.total_docs
        
        # 更新倒排索引和文档频率
        token_counts = self._count_tokens(tokens)
        for token, count in token_counts.items():
            # 更新倒排索引
            self.inverted_index[token][doc_id] = count
            
            # 更新文档频率（如果是第一次出现这个词）
            if len(self.inverted_index[token]) == 1:
                self.doc_freq[token] = self.doc_freq.get(token, 0) + 1
        
        return True
    
    def add_batch_documents(self, documents: List[Tuple[str, str, str, Dict]]) -> int:
        """
        批量添加文档
        
        Args:
            documents: 文档列表，每个元素为 (doc_id, content, title, metadata)
        
        Returns:
            int: 成功添加的文档数量
        """
        success_count = 0
        for doc_id, content, title, metadata in documents:
            if self.add_document(doc_id, content, title, metadata):
                success_count += 1
        return success_count
    
    def search(self, query: str, top_k: int = None) -> List[SearchResult]:
        """
        搜索相似文档
        
        Args:
            query: 查询文本
            top_k: 返回前K个结果，默认3个
        
        Returns:
            List[SearchResult]: 搜索结果列表，按得分降序排列
        """
        if not self.documents or not query:
            return []
        
        top_k = top_k or self.DEFAULT_TOP_K
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        
        scores = defaultdict(float)
        
        for token in query_tokens:
            if token not in self.inverted_index:
                continue
            
            # IDF计算
            df = self.doc_freq.get(token, 0)
            if df == 0:
                continue
            idf = math.log((self.total_docs - df + 0.5) / (df + 0.5) + 1.0)
            
            # 对每个包含该词的文档计算得分
            for doc_id, tf in self.inverted_index[token].items():
                doc_len = self.doc_length[doc_id]
                # BM25公式
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len)
                score = idf * (numerator / denominator)
                scores[doc_id] += score
        
        # 排序并返回前K个
        sorted_doc_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        results = []
        for doc_id, score in sorted_doc_ids:
            results.append(SearchResult(
                doc_id=doc_id,
                score=score,
                document=self.documents[doc_id]
            ))
        
        return results
    
    def get_document(self, doc_id: str) -> Optional[Document]:
        """根据ID获取文档"""
        return self.documents.get(doc_id)
    
    def save_to_disk(self, save_dir: str) -> bool:
        """
        持久化知识库到磁盘
        
        Args:
            save_dir: 保存目录路径
        
        Returns:
            bool: 是否保存成功
        """
        try:
            save_path = Path(save_dir)
            save_path.mkdir(parents=True, exist_ok=True)
            
            # 保存文档
            docs_data = {
                doc_id: asdict(doc)
                for doc_id, doc in self.documents.items()
            }
            with open(save_path / "documents.json", "w", encoding="utf-8") as f:
                json.dump(docs_data, f, ensure_ascii=False, indent=2)
            
            # 保存索引和统计信息
            index_data = {
                "k1": self.k1,
                "b": self.b,
                "total_docs": self.total_docs,
                "avg_doc_len": self.avg_doc_len,
                "total_doc_len": self.total_doc_len,
                "doc_length": self.doc_length,
                "doc_freq": self.doc_freq,
                "inverted_index": self.inverted_index,
            }
            with open(save_path / "index.json", "w", encoding="utf-8") as f:
                json.dump(index_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            import sys
            sys.stderr.write(f"Warning: 保存知识库失败: {e}\n")
            return False
    
    @classmethod
    def load_from_disk(cls, load_dir: str) -> Optional['BM25KnowledgeBase']:
        """
        从磁盘加载知识库
        
        Args:
            load_dir: 加载目录路径
        
        Returns:
            Optional[BM25KnowledgeBase]: 加载成功返回知识库实例，失败返回None
        """
        try:
            load_path = Path(load_dir)
            if not load_path.exists():
                return None
            
            # 加载索引和统计信息
            with open(load_path / "index.json", "r", encoding="utf-8") as f:
                index_data = json.load(f)
            
            # 创建实例
            kb = cls(
                k1=index_data.get("k1", cls.DEFAULT_K1),
                b=index_data.get("b", cls.DEFAULT_B)
            )
            
            # 恢复统计信息
            kb.total_docs = index_data.get("total_docs", 0)
            kb.avg_doc_len = index_data.get("avg_doc_len", 0.0)
            kb.total_doc_len = index_data.get("total_doc_len", 0)
            kb.doc_length = index_data.get("doc_length", {})
            kb.doc_freq = index_data.get("doc_freq", {})
            kb.inverted_index = defaultdict(dict, index_data.get("inverted_index", {}))
            
            # 加载文档
            with open(load_path / "documents.json", "r", encoding="utf-8") as f:
                docs_data = json.load(f)
            
            kb.documents = {}
            for doc_id, doc_dict in docs_data.items():
                kb.documents[doc_id] = Document(**doc_dict)
            
            return kb
            
        except Exception as e:
            import sys
            sys.stderr.write(f"Warning: 加载知识库失败: {e}\n")
            return None
    
    def _tokenize(self, text: str) -> List[str]:
        """
        分词器 - 简单单字分词方案
        - 中文：单字
        - 英文/数字：按空格和标点拆分
        """
        if not text:
            return []
        
        # 标准化文本
        text = text.lower()
        
        # 移除特殊字符，保留中英文和数字
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', ' ', text)
        
        tokens = []
        current_word = []
        
        for c in text:
            if ord(c) >= 0x4e00 and ord(c) <= 0x9fa5:  # 中文字符
                # 先处理之前收集的英文词
                if current_word:
                    word = ''.join(current_word)
                    if word not in self.stop_words and len(word) > 1:
                        tokens.append(word)
                    current_word = []
                # 添加单字
                if c not in self.stop_words:
                    tokens.append(c)
            elif c.isalnum():  # 英文或数字
                current_word.append(c)
            else:  # 其他字符（空格等）
                if current_word:
                    word = ''.join(current_word)
                    if word not in self.stop_words and len(word) > 1:
                        tokens.append(word)
                    current_word = []
        
        # 处理最后剩余的英文词
        if current_word:
            word = ''.join(current_word)
            if word not in self.stop_words and len(word) > 1:
                tokens.append(word)
        
        return tokens
    
    def _count_tokens(self, tokens: List[str]) -> Dict[str, int]:
        """统计词频"""
        counts = defaultdict(int)
        for token in tokens:
            counts[token] += 1
        return counts
    
    def _get_default_stop_words(self) -> Set[str]:
        """获取默认停用词"""
        return {
            # 中文停用词
            '的', '是', '在', '和', '了', '有', '我', '都', '个', '与', '也', '对', '为', '能',
            '上', '他', '而', '及', '或', '但是', '该', '就', '等', '可以', '会', '将', '并',
            '让', '但', '因为', '所以', '如果', '虽然', '于', '中', '到', '从', '这', '那',
            '一个', '一些', '什么', '怎么', '如何', '为什么', '是否', '可以', '需要', '能够',
            '可能', '应该', '必须', '非常', '很', '非常', '极其', '比较', '相当', '稍微',
            # 英文停用词
            'the', 'is', 'in', 'and', 'to', 'a', 'of', 'for', 'it', 'that', 'with', 'as', 'on',
            'this', 'by', 'from', 'they', 'we', 'you', 'are', 'was', 'were', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
            'an', 'be', 'been', 'being', 'can', 'cannot', 'could', 'did', 'do', 'does', 'doing',
            'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having',
            'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if',
            'in', 'into', 'is', 'it', 'its', 'itself', 'just', 'me', 'more', 'most', 'my',
            'myself', 'no', 'nor', 'not', 'now', 'of', 'off', 'on', 'once', 'only', 'or',
            'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'she', 'should',
            'so', 'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves',
            'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under',
            'until', 'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while',
            'who', 'whom', 'why', 'will', 'with', 'would', 'you', 'your', 'yours', 'yourself', 'yourselves'
        }
    
    def get_statistics(self) -> Dict:
        """获取知识库统计信息"""
        return {
            "total_documents": self.total_docs,
            "average_document_length": round(self.avg_doc_len, 2),
            "total_terms": len(self.inverted_index),
            "top_terms": sorted(
                self.doc_freq.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }
