"""
双轨并行架构 - 叙事链提取器

从文本中提取叙事事件序列，生成 ExtractedNarrativeChain 对象。
"""

from typing import List, Dict, Any
from ..narrative_chain import ExtractedNarrativeChain
from .base_extractor import BaseExtractor
import re
from datetime import datetime


class NarrativeExtractor(BaseExtractor):
    """
    叙事链提取器
    
    通过事件词和时间词匹配，从文本中提取：
    - 事件序列
    - 叙事弧类型
    - 主角
    """
    
    extractor_name = "narrative"
    
    # 事件关键词（中文）
    EVENT_KEYWORDS_CN = [
        "发生了", "开始了", "结束了", "出现了", "产生了",
        "然后", "接着", "随后", "突然", "忽然",
        "最终", "最后", "终于", "起初", "最初",
        "之后", "此前", "此前", "不久", "刹那间",
    ]
    
    # 事件关键词（英文）
    EVENT_KEYWORDS_EN = [
        "happened", "occurred", "started", "began", "ended",
        "then", "next", "after", "suddenly", "unexpectedly",
        "finally", "eventually", "initially", "originally",
        "subsequently", "meanwhile", "simultaneously",
    ]
    
    # 叙事弧关键词
    NARRATIVE_ARC_KEYWORDS = {
        "intro": ["开始", "起初", "最初", "从前", "引入", "begin", "start", "intro"],
        "rising": ["然后", "接着", "逐渐", "越来越", "加剧", "then", "rising", "build"],
        "climax": ["突然", "关键", "转折", "高潮", "关键时刻", "climax", "peak", "turning"],
        "falling": ["之后", "随后", "逐渐平静", "缓解", "falling", "resolve", "ease"],
        "resolution": ["最终", "最后", "终于", "结局", "result", "finally", "resolution"],
    }
    
    @staticmethod
    def _get_all_event_keywords() -> List[str]:
        """获取所有事件关键词"""
        return (
            NarrativeExtractor.EVENT_KEYWORDS_CN +
            NarrativeExtractor.EVENT_KEYWORDS_EN
        )
    
    def extract(self, text: str, **kwargs) -> List[ExtractedNarrativeChain]:
        """
        从文本中提取叙事链
        
        Args:
            text: 输入文本
            **kwargs: 支持参数
                - source_id: 来源标识
        
        Returns:
            叙事链列表
        """
        if not text or not text.strip():
            return []
        
        sentences = self.split_sentences(text)
        
        # 提取事件
        events = self._extract_events(text, sentences)
        arc = self._identify_narrative_arc(text)
        protagonist = self._extract_protagonist(text)
        
        # 计算置信度
        event_matches = len(self.find_keywords(text, self._get_all_event_keywords()))
        sentence_count = len(sentences)
        confidence = self.calculate_confidence(event_matches, max(sentence_count, 1), 0.1)
        
        if confidence < self.min_confidence and not events:
            return []
        
        chain = ExtractedNarrativeChain(
            chain_id=f"narrative_{datetime.now().strftime('%Y%m%d%H%M%S')}_{id(text) % 10000}",
            content=text[:self.max_chain_length],
            events=events[:10],
            narrative_arc=arc,
            protagonist=protagonist,
            extraction_confidence=confidence,
        )
        
        return [chain]
    
    def _extract_events(
        self, text: str, sentences: List[str]
    ) -> List[Dict[str, Any]]:
        """提取事件序列"""
        events = []
        all_event_kw = self.EVENT_KEYWORDS_CN + self.EVENT_KEYWORDS_EN
        
        # 方式1：通过事件关键词提取
        for kw in all_event_kw:
            pattern = r'[^。！？\.!?]*' + re.escape(kw) + r'[^。！？\.!?]*'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                content = match.group().strip()
                if content and len(content) > 3:
                    # 检查是否已存在
                    existing = [e for e in events if e.get("description") == content]
                    if not existing:
                        events.append({
                            "description": content,
                            "is_key": self._is_key_event(content),
                            "keywords_found": [kw],
                        })
        
        # 方式2：基于时间词分段
        time_expressions = self.extract_time_expressions(text)
        if time_expressions:
            for te in time_expressions:
                pattern = re.escape(te) + r'[^。！？\.!?]*'
                for match in re.finditer(pattern, text):
                    content = match.group().strip()
                    if content and len(content) > 5:
                        existing = [e for e in events if e.get("description") == content]
                        if not existing:
                            events.append({
                                "description": content,
                                "is_key": True,
                                "time": te,
                                "keywords_found": [te],
                            })
        
        # 方式3：如果事件太少，使用句子作为事件
        if len(events) < 2 and len(sentences) >= 2:
            for i, sent in enumerate(sentences):
                if len(sent) > 5:
                    events.append({
                        "description": sent,
                        "is_key": i == 0 or i == len(sentences) - 1,
                        "order": i,
                    })
        
        return events[:10]
    
    def _identify_narrative_arc(self, text: str) -> str:
        """识别叙事弧类型"""
        text_lower = text.lower()
        scores = {}
        
        for arc_type, keywords in self.NARRATIVE_ARC_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[arc_type] = score
        
        if not scores or all(s == 0 for s in scores.values()):
            return ""
        
        best_arc = max(scores, key=scores.get)
        return best_arc
    
    def _extract_protagonist(self, text: str) -> str:
        """提取主角"""
        # 常见的人称代词和称呼
        protagonist_patterns = [
            r'(?:用户|客户|系统|管理员|开发者)[：:]\s*(\S+)',
            r'(?:我叫|我是|I am|my name is)\s+(\S+)',
            r'(?:关于|对于|用户)\s+(\S+)\s*(?:的|,)',
        ]
        
        for pattern in protagonist_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        # 提取第一个大写词（英文）
        eng_match = re.search(r'[A-Z][a-z]+', text)
        if eng_match:
            return eng_match.group()
        
        return ""
    
    @staticmethod
    def _is_key_event(description: str) -> bool:
        """判断是否为关键事件"""
        key_words = [
            "关键", "重要", "转折", "决定", "核心",
            "key", "critical", "important", "crucial", "vital",
        ]
        return any(kw in description.lower() for kw in key_words)