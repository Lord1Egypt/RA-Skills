"""
双轨并行架构 - 逻辑链提取器

从文本中提取逻辑推理结构，生成 ExtractedLogicChain 对象。
"""

from typing import List
from ..logic_chain import ExtractedLogicChain
from .base_extractor import BaseExtractor
import re
from datetime import datetime


class LogicExtractor(BaseExtractor):
    """
    逻辑链提取器
    
    通过逻辑结构词匹配和推理模式识别，从文本中提取：
    - 前提条件
    - 推理步骤
    - 结论
    """
    
    extractor_name = "logic"
    
    # 前提关键词（中文）
    PREMISE_KEYWORDS_CN = [
        "假设", "如果", "若", "假定", "设", "假如",
        "当", "只要", "一旦", "既然", "鉴于",
        "已知", "事实是", "数据显示", "研究表明",
    ]
    
    # 前提关键词（英文）
    PREMISE_KEYWORDS_EN = [
        "if", "assuming", "given that", "provided that",
        "suppose", "when", "whenever", "whereas",
        "given", "let", "assume",
    ]
    
    # 推理关键词（中文）
    INFERENCE_KEYWORDS_CN = [
        "那么", "则", "因此", "所以", "由此", "据此",
        "可以推出", "可得", "可推断", "意味着",
        "表明", "说明", "显示", "暗示",
    ]
    
    # 推理关键词（英文）
    INFERENCE_KEYWORDS_EN = [
        "then", "therefore", "thus", "hence", "so",
        "consequently", "it follows that", "implies",
        "suggests", "indicates", "means that",
    ]
    
    # 结论关键词（中文）
    CONCLUSION_KEYWORDS_CN = [
        "结论", "综上所述", "总之", "归根结底",
        "最终结果", "总结", "概括",
    ]
    
    # 结论关键词（英文）
    CONCLUSION_KEYWORDS_EN = [
        "conclusion", "in conclusion", "to summarize",
        "in summary", "overall", "ultimately",
        "finally", "in short",
    ]
    
    # 逻辑类型关键词
    DEDUCTIVE_KEYWORDS = [
        "所有", "凡是", "必然", "一定", "必须",
        "all", "always", "must", "never", "every",
    ]
    INDUCTIVE_KEYWORDS = [
        "通常", "一般", "大多数", "往往", "倾向",
        "usually", "generally", "most", "tend", "often",
    ]
    ABDUCTIVE_KEYWORDS = [
        "可能", "推测", "大概", "或许", "最佳解释",
        "maybe", "probably", "likely", "best explanation",
    ]
    
    @staticmethod
    def _get_all_keywords() -> List[str]:
        """获取所有逻辑关键词"""
        return (
            LogicExtractor.PREMISE_KEYWORDS_CN +
            LogicExtractor.PREMISE_KEYWORDS_EN +
            LogicExtractor.INFERENCE_KEYWORDS_CN +
            LogicExtractor.INFERENCE_KEYWORDS_EN +
            LogicExtractor.CONCLUSION_KEYWORDS_CN +
            LogicExtractor.CONCLUSION_KEYWORDS_EN
        )
    
    def extract(self, text: str, **kwargs) -> List[ExtractedLogicChain]:
        """
        从文本中提取逻辑链
        
        Args:
            text: 输入文本
            **kwargs: 支持参数
                - source_id: 来源标识
        
        Returns:
            逻辑链列表
        """
        if not text or not text.strip():
            return []
        
        sentences = self.split_sentences(text)
        
        # 提取逻辑结构
        premises = self._extract_premises(text, sentences)
        inference_steps = self._extract_inferences(text, sentences)
        conclusion = self._extract_conclusion(text, sentences)
        logic_type = self._identify_logic_type(text)
        
        # 计算置信度
        keyword_matches = len(self.find_keywords(text, self._get_all_keywords()))
        sentence_count = len(sentences)
        confidence = self.calculate_confidence(keyword_matches, max(sentence_count, 1), 0.1)
        
        if confidence < self.min_confidence and not premises:
            return []
        
        # 构建推理步骤
        if not inference_steps and premises and conclusion:
            inference_steps = [f"基于前提推导出结论"]
        elif not inference_steps:
            inference_steps = ["提取推理过程"]
        
        chain = ExtractedLogicChain(
            chain_id=f"logic_{datetime.now().strftime('%Y%m%d%H%M%S')}_{id(text) % 10000}",
            content=text[:self.max_chain_length],
            premises=premises[:5],
            inference_steps=inference_steps[:5],
            conclusion=conclusion or text[:200] if len(text) > 200 else text,
            logic_type=logic_type,
            extraction_confidence=confidence,
        )
        
        return [chain]
    
    def _extract_premises(self, text: str, sentences: List[str]) -> List[str]:
        """提取前提"""
        premises = []
        
        all_premise_kw = self.PREMISE_KEYWORDS_CN + self.PREMISE_KEYWORDS_EN
        
        # 从包含前提关键词的句子中提取
        for kw in all_premise_kw:
            pattern = r'[^。！？\.!?]*' + re.escape(kw) + r'[^。！？\.!?]*'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                content = match.group().strip()
                if content and len(content) > 3 and content not in premises:
                    premises.append(content)
        
        # 如果没找到，取前几个句子作为前提
        if not premises and len(sentences) >= 2:
            for sent in sentences[:2]:
                if len(sent) > 5:
                    premises.append(sent)
        
        return premises[:5]
    
    def _extract_inferences(self, text: str, sentences: List[str]) -> List[str]:
        """提取推理步骤"""
        steps = []
        
        all_infer_kw = self.INFERENCE_KEYWORDS_CN + self.INFERENCE_KEYWORDS_EN
        
        # 从包含推理关键词的句子中提取
        for kw in all_infer_kw:
            pattern = r'[^。！？\.!?]*' + re.escape(kw) + r'[^。！？\.!?]*'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                content = match.group().strip()
                if content and len(content) > 3 and content not in steps:
                    steps.append(content)
        
        # 如果没找到，取中间句子作为推理步骤
        if not steps and len(sentences) >= 3:
            mid = len(sentences) // 2
            for sent in sentences[mid-1:mid+1]:
                if len(sent) > 5:
                    steps.append(sent)
        
        return steps[:5]
    
    def _extract_conclusion(self, text: str, sentences: List[str]) -> str:
        """提取结论"""
        all_conc_kw = self.CONCLUSION_KEYWORDS_CN + self.CONCLUSION_KEYWORDS_EN
        
        for kw in all_conc_kw:
            pattern = r'[^。！？\.!?]*' + re.escape(kw) + r'[^。！？\.!?]*'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                content = match.group().strip()
                if content and len(content) > 3:
                    return content
        
        # 取最后一个句子作为结论
        if sentences:
            last = sentences[-1]
            if len(last) > 5:
                return last
        
        return ""
    
    def _identify_logic_type(self, text: str) -> str:
        """识别逻辑类型"""
        text_lower = text.lower()
        
        # 统计各类型关键词
        deductive_score = sum(1 for kw in self.DEDUCTIVE_KEYWORDS if kw in text_lower)
        inductive_score = sum(1 for kw in self.INDUCTIVE_KEYWORDS if kw in text_lower)
        abductive_score = sum(1 for kw in self.ABDUCTIVE_KEYWORDS if kw in text_lower)
        
        if deductive_score > inductive_score and deductive_score > abductive_score:
            return "deductive"
        elif inductive_score > deductive_score and inductive_score > abductive_score:
            return "inductive"
        elif abductive_score > deductive_score and abductive_score > inductive_score:
            return "abductive"
        
        # 默认：如果包含推理词则归为演绎
        if any(kw in text_lower for kw in self.INFERENCE_KEYWORDS_CN + self.INFERENCE_KEYWORDS_EN):
            return "deductive"
        
        return "deductive"