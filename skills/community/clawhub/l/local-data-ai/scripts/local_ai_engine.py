#!/usr/bin/env python3
"""
本地 AI 处理引擎
提供离线问答、摘要、提取等 AI 能力
"""

import os
import yaml
import torch
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Document:
    """文档对象"""
    id: str
    title: str
    content: str
    metadata: Dict
    chunks: List[Dict]
    page_count: int = 1


@dataclass
class SearchResult:
    """搜索结果"""
    doc_id: str
    chunk_id: str
    content: str
    score: float
    page: int = 1


class LocalAIEngine:
    """
    本地 AI 处理引擎
    纯离线运行，支持问答、摘要、提取、检索
    """
    
    def __init__(self, config_path: str = None):
        """
        初始化引擎
        
        Args:
            config_path: 配置文件路径，默认使用 config/model_config.yaml
        """
        self.config = self._load_config(config_path)
        self.llm = None
        self.embedding_model = None
        self.vector_store = None
        self.conversation_history = []
        
        self._init_models()
    
    def _load_config(self, config_path: str = None) -> Dict:
        """加载配置"""
        if config_path is None:
            base_dir = Path(__file__).parent.parent
            config_path = base_dir / "config" / "model_config.yaml"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _init_models(self):
        """初始化模型"""
        # 检测设备内存
        memory_gb = self._get_available_memory()
        
        if memory_gb <= 8:
            config_key = "low_memory"
        elif memory_gb <= 16:
            config_key = "medium_memory"
        else:
            config_key = "high_memory"
        
        device_config = self.config.get("device_adaptation", {}).get(config_key, {})
        
        # 这里简化实现，实际应该加载真实模型
        print(f"[LocalAIEngine] 设备内存: {memory_gb}GB, 使用配置: {config_key}")
        print(f"[LocalAIEngine] 引擎初始化完成 (模拟模式)")
    
    def _get_available_memory(self) -> int:
        """获取可用内存(GB)"""
        try:
            import psutil
            return int(psutil.virtual_memory().total / (1024 ** 3))
        except:
            return 8  # 默认值
    
    def ask(self, document: Document, question: str, 
            context_rounds: int = 3) -> str:
        """
        基于文档内容回答问题
        
        Args:
            document: 解析后的文档对象
            question: 用户问题
            context_rounds: 保留的上下文轮数
            
        Returns:
            回答文本
        """
        # 检索相关上下文
        context = self._retrieve_context(document, question)
        
        # 构建提示词
        prompt = self._build_qa_prompt(context, question)
        
        # 调用本地 LLM 生成回答
        answer = self._generate(prompt)
        
        # 保存对话历史
        self.conversation_history.append({
            "question": question,
            "answer": answer,
            "document_id": document.id
        })
        
        # 限制历史长度
        if len(self.conversation_history) > context_rounds * 2:
            self.conversation_history = self.conversation_history[-context_rounds * 2:]
        
        return answer
    
    def summarize(self, document: Document, mode: str = "core") -> str:
        """
        生成文档摘要
        
        Args:
            document: 解析后的文档对象
            mode: 摘要模式 (brief/core/detailed)
                - brief: 100字以内
                - core: 200-300字  
                - detailed: 500字以上
                
        Returns:
            摘要文本
        """
        # 根据模式选择长度
        length_limits = {
            "brief": 100,
            "core": 300,
            "detailed": 800
        }
        max_length = length_limits.get(mode, 300)
        
        # 构建摘要提示词
        prompt = f"""请为以下文档生成摘要，控制在{max_length}字以内：

文档标题: {document.title}
文档内容: {document.content[:5000]}...

请提取核心要点，生成简洁的摘要："""
        
        summary = self._generate(prompt, max_tokens=max_length * 2)
        return summary
    
    def extract(self, document: Document, types: List[str]) -> Dict[str, List]:
        """
        提取文档中的关键信息
        
        Args:
            document: 解析后的文档对象
            types: 提取类型列表，如 ["人名", "金额", "日期"]
            
        Returns:
            按类型分类的提取结果
        """
        results = {t: [] for t in types}
        
        # 构建提取提示词
        types_str = ", ".join(types)
        prompt = f"""请从以下文档中提取指定的信息类型：{types_str}

文档内容: {document.content[:8000]}...

请以 JSON 格式返回提取结果："""
        
        # 调用 LLM 提取
        extraction_result = self._generate(prompt)
        
        # 解析结果（简化实现）
        # 实际应该解析 LLM 返回的 JSON
        for t in types:
            results[t] = [f"示例{t}1", f"示例{t}2"]
        
        return results
    
    def search(self, documents: List[Document], keywords: str,
               match_mode: str = "exact") -> List[SearchResult]:
        """
        多文件检索
        
        Args:
            documents: 文档列表
            keywords: 检索关键词
            match_mode: 匹配模式 (exact/fuzzy)
            
        Returns:
            检索结果列表
        """
        results = []
        
        for doc in documents:
            for chunk in doc.chunks:
                content = chunk.get("content", "")
                
                # 简单匹配逻辑（实际应该用向量检索）
                if match_mode == "exact":
                    score = 1.0 if keywords in content else 0.0
                else:
                    # 模糊匹配
                    score = self._fuzzy_match(keywords, content)
                
                if score > 0.5:
                    results.append(SearchResult(
                        doc_id=doc.id,
                        chunk_id=chunk.get("id", ""),
                        content=content[:200],
                        score=score,
                        page=chunk.get("page", 1)
                    ))
        
        # 按分数排序
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:10]  # 返回前10个
    
    def ask_multi(self, documents: List[Document], question: str) -> str:
        """
        跨文件问答
        
        Args:
            documents: 多个相关文档
            question: 用户问题
            
        Returns:
            回答文本
        """
        # 合并所有文档的上下文
        all_context = []
        for doc in documents:
            context = self._retrieve_context(doc, question)
            all_context.append(f"【{doc.title}】\n{context}")
        
        combined_context = "\n\n".join(all_context)
        
        prompt = f"""基于以下多个文档内容回答问题：

{combined_context}

问题: {question}

请综合分析多个文档的内容给出回答："""
        
        return self._generate(prompt)
    
    def _retrieve_context(self, document: Document, query: str) -> str:
        """检索相关上下文"""
        # 简化实现：返回文档前3000字符
        return document.content[:3000]
    
    def _build_qa_prompt(self, context: str, question: str) -> str:
        """构建问答提示词"""
        return f"""基于以下文档内容回答问题。如果文档中没有相关信息，请明确说明。

文档内容:
{context}

问题: {question}

回答:"""
    
    def _generate(self, prompt: str, max_tokens: int = 1024) -> str:
        """
        调用本地 LLM 生成文本
        
        注意：这是模拟实现，实际应该调用真实的本地模型
        """
        # 模拟生成延迟
        import time
        time.sleep(0.1)
        
        # 返回模拟回答
        return f"[模拟回答] 基于本地模型生成的回答。提示词长度: {len(prompt)} 字符"
    
    def _fuzzy_match(self, keywords: str, content: str) -> float:
        """模糊匹配计算相似度"""
        # 简化实现
        keywords_lower = keywords.lower()
        content_lower = content.lower()
        
        if keywords_lower in content_lower:
            return 0.8
        
        # 关键词拆分匹配
        keyword_parts = keywords_lower.split()
        matches = sum(1 for part in keyword_parts if part in content_lower)
        
        return matches / len(keyword_parts) if keyword_parts else 0.0


# 单例模式
_engine_instance = None


def get_engine() -> LocalAIEngine:
    """获取引擎单例"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = LocalAIEngine()
    return _engine_instance
