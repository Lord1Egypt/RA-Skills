"""
双轨并行架构 - 因果链提取器

从文本中提取因果关系，生成 ExtractedCausalChain 对象。
"""

from typing import List, Optional
from ..causal_chain import (
    ExtractedCausalChain,
    ProblemNode,
    CauseNode,
    CausalRelation,
    SolutionNode,
)
from .base_extractor import BaseExtractor


class CausalExtractor(BaseExtractor):
    """
    因果链提取器
    
    通过因果关系词匹配和因果对提取，从文本中识别：
    - 问题描述
    - 原因分析
    - 解决方案
    """
    
    extractor_name = "causal"
    
    # 因果关系词（中文）
    CAUSE_KEYWORDS_CN = [
        "因为", "由于", "源于", "起因于", "之所以", "归因于",
        "是由", "来自", "出于", "基于", "鉴于",
    ]
    
    EFFECT_KEYWORDS_CN = [
        "所以", "因此", "因而", "于是", "从而", "以致",
        "导致", "引起", "造成", "使得", "引发", "触发",
        "带来", "产生", "带来", "促使", "推动",
    ]
    
    # 因果关系词（英文）
    CAUSE_KEYWORDS_EN = [
        "because", "because of", "due to", "owing to", "since",
        "as a result of", "caused by", "stem from", "originate from",
        "attributed to", "arise from",
    ]
    
    EFFECT_KEYWORDS_EN = [
        "therefore", "thus", "hence", "consequently", "as a result",
        "lead to", "result in", "bring about", "give rise to",
        "contribute to", "trigger", "cause", "generate",
    ]
    
    # 问题关键词
    PROBLEM_KEYWORDS = [
        "问题", "挑战", "困难", "障碍", "瓶颈", "风险",
        "issue", "problem", "challenge", "difficulty", "risk",
        "bug", "error", "failure", "defect",
    ]
    
    # 解决方案关键词
    SOLUTION_KEYWORDS = [
        "解决方案", "对策", "措施", "建议", "方案", "办法",
        "解决", "修复", "优化", "改进", "改善",
        "solution", "fix", "resolve", "improve", "optimize",
        "recommend", "suggestion", "approach",
    ]
    
    # 所有因果关键词
    ALL_CAUSAL_KEYWORDS = (
        CAUSE_KEYWORDS_CN + EFFECT_KEYWORDS_CN +
        CAUSE_KEYWORDS_EN + EFFECT_KEYWORDS_EN
    )
    
    def extract(self, text: str, **kwargs) -> List[ExtractedCausalChain]:
        """
        从文本中提取因果链
        
        Args:
            text: 输入文本
            **kwargs: 支持参数
                - source_id: 来源标识
        
        Returns:
            因果链列表
        """
        if not text or not text.strip():
            return []
        
        source_id = kwargs.get("source_id", "")
        sentences = self.split_sentences(text)
        paragraphs = self.split_paragraphs(text)
        
        # 提取因果信息
        problems = self._extract_problems(text, sentences)
        causes = self._extract_causes(text, sentences)
        solutions = self._extract_solutions(text, sentences)
        relations = self._extract_relations(text, sentences)
        
        # 计算置信度
        causal_matches = len(self.find_keywords(text, self.ALL_CAUSAL_KEYWORDS))
        sentence_count = len(sentences)
        confidence = self.calculate_confidence(causal_matches, max(sentence_count, 1), 0.15)
        
        if confidence < self.min_confidence and not (problems and causes):
            return []
        
        # 构建链
        problem_node = None
        if problems:
            problem_node = ProblemNode(
                content=problems[0],
                severity=self._assess_severity(problems[0]),
                category="extracted",
            )
        else:
            problem_node = ProblemNode(
                content=text[:200] if len(text) > 200 else text,
                severity="medium",
                category="extracted",
            )
        
        cause_nodes = [
            CauseNode(
                content=cause,
                is_root_cause=self._is_root_cause(cause),
                cause_type="root" if self._is_root_cause(cause) else "direct",
                confidence=0.7,
            )
            for cause in causes[:5]
        ]
        
        solution_nodes = [
            SolutionNode(
                content=solution,
                effectiveness="unknown",
                effort="unknown",
            )
            for solution in solutions[:5]
        ]
        
        causal_relations = relations or [
            CausalRelation(
                from_cause=f"cause_{i}",
                to_effect="effect_0",
                relation_type="causes",
                strength=0.6,
            )
            for i in range(len(cause_nodes))
        ]
        
        chain = ExtractedCausalChain(
            chain_id=f"causal_{datetime.now().strftime('%Y%m%d%H%M%S')}_{id(text) % 10000}",
            content=text[:self.max_chain_length],
            problem=problem_node,
            causes=cause_nodes,
            causal_relations=causal_relations,
            solutions=solution_nodes,
            source_text=text[:500],
            extraction_confidence=confidence,
        )
        
        return [chain]
    
    def _extract_problems(self, text: str, sentences: List[str]) -> List[str]:
        """提取问题描述"""
        problems = []
        
        # 从包含问题关键词的句子中提取
        for kw in self.PROBLEM_KEYWORDS:
            for match in re.finditer(
                r'[^。！？\.!?]*' + re.escape(kw) + r'[^。！？\.!?]*',
                text,
                re.IGNORECASE
            ):
                content = match.group().strip()
                if content and len(content) > 2:
                    problems.append(content)
        
        # 如果没找到，尝试从段落中提取
        if not problems:
            paragraphs = self.split_paragraphs(text)
            for p in paragraphs[:2]:
                if len(p) > 10:
                    problems.append(p[:200])
        
        return problems[:3]
    
    def _extract_causes(self, text: str, sentences: List[str]) -> List[str]:
        """提取原因"""
        causes = []
        
        # 匹配原因关键词后的内容
        all_cause_kw = self.CAUSE_KEYWORDS_CN + self.CAUSE_KEYWORDS_EN
        for kw in all_cause_kw:
            pattern = re.escape(kw) + r'[^。！？\.!?]*'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                content = match.group().strip()
                # 去除关键词前缀
                content = re.sub(r'^' + re.escape(kw), '', content).strip()
                if content and len(content) > 2:
                    causes.append(content)
        
        return causes[:5]
    
    def _extract_solutions(self, text: str, sentences: List[str]) -> List[str]:
        """提取解决方案"""
        solutions = []
        
        for kw in self.SOLUTION_KEYWORDS:
            pattern = r'[^。！？\.!?]*' + re.escape(kw) + r'[^。！？\.!?]*'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                content = match.group().strip()
                if content and len(content) > 4:
                    solutions.append(content)
        
        return solutions[:5]
    
    def _extract_relations(
        self, text: str, sentences: List[str]
    ) -> List[CausalRelation]:
        """提取因果关系对"""
        relations = []
        relation_id = 0
        
        # 查找"因为...所以..."模式
        for i, sent in enumerate(sentences):
            has_cause = any(kw in sent for kw in self.CAUSE_KEYWORDS_CN + self.CAUSE_KEYWORDS_EN)
            has_effect = any(kw in sent for kw in self.EFFECT_KEYWORDS_CN + self.EFFECT_KEYWORDS_EN)
            
            if has_cause and has_effect:
                relations.append(CausalRelation(
                    from_cause=f"cause_{relation_id}",
                    to_effect=f"effect_{relation_id}",
                    relation_type="causes",
                    strength=0.8,
                ))
                relation_id += 1
        
        # 查找相邻句子间的因果对
        for i in range(len(sentences) - 1):
            has_cause = any(
                kw in sentences[i]
                for kw in self.CAUSE_KEYWORDS_CN + self.CAUSE_KEYWORDS_EN
            )
            has_effect = any(
                kw in sentences[i + 1]
                for kw in self.EFFECT_KEYWORDS_CN + self.EFFECT_KEYWORDS_EN
            )
            
            if has_cause or has_effect:
                relations.append(CausalRelation(
                    from_cause=f"cause_{relation_id}",
                    to_effect=f"effect_{relation_id}",
                    relation_type="causes",
                    strength=0.5,
                ))
                relation_id += 1
        
        return relations[:5]
    
    @staticmethod
    def _is_root_cause(cause: str) -> bool:
        """判断是否为根本原因"""
        root_keywords = [
            "根本", "本质", "根源", "深层", "核心", "基础",
            "root", "fundamental", "underlying", "core",
        ]
        return any(kw in cause.lower() for kw in root_keywords)
    
    @staticmethod
    def _assess_severity(problem: str) -> str:
        """评估问题严重程度"""
        high_keywords = [
            "严重", "关键", "致命", "紧急", "重大", "危机",
            "critical", "severe", "fatal", "urgent", "major",
        ]
        low_keywords = [
            "轻微", "次要", "小问题", "一般", "简单",
            "minor", "trivial", "simple", "cosmetic",
        ]
        
        if any(kw in problem.lower() for kw in high_keywords):
            return "high"
        if any(kw in problem.lower() for kw in low_keywords):
            return "low"
        return "medium"


import re
from datetime import datetime