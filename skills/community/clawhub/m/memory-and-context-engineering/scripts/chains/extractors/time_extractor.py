"""
双轨并行架构 - 时间链提取器

从文本中提取时间线信息，生成 ExtractedTimeChain 对象。
"""

from typing import List, Dict, Any
from ..time_chain import ExtractedTimeChain
from .base_extractor import BaseExtractor
import re
from datetime import datetime


class TimeExtractor(BaseExtractor):
    """
    时间链提取器
    
    通过时间表达式识别和时序关系分析，从文本中提取：
    - 时间线列表
    - 总时长
    """
    
    extractor_name = "time"
    
    # 时间格式模式
    TIME_PATTERNS = [
        # 标准日期
        r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?',
        # 短日期
        r'\d{1,2}[-/月]\d{1,2}[日]?',
        # 时间
        r'\d{1,2}:\d{2}(?::\d{2})?',
        # 中文日期
        r'\d{4}年\d{1,2}月\d{1,2}日',
        r'\d{1,2}月\d{1,2}日',
        # 星期
        r'星期[一二三四五六日]|周[一二三四五六日]',
        r'[上下]午\d{1,2}:\d{2}',
    ]
    
    # 时间顺序词
    TIME_ORDER_WORDS = [
        "首先", "第一", "最初", "起初",
        "然后", "接着", "随后", "之后",
        "最后", "最终", "终于",
        "first", "initially", "then", "next",
        "after", "subsequently", "finally", "eventually",
    ]
    
    # 时间关系词
    BEFORE_WORDS = ["之前", "以前", "此前", "先前", "before", "prior", "earlier"]
    AFTER_WORDS = ["之后", "以后", "此后", "随后", "after", "later", "subsequently"]
    DURING_WORDS = ["期间", "同时", "过程中", "during", "while", "meanwhile"]
    
    def extract(self, text: str, **kwargs) -> List[ExtractedTimeChain]:
        """
        从文本中提取时间链
        
        Args:
            text: 输入文本
            **kwargs: 支持参数
                - source_id: 来源标识
        
        Returns:
            时间链列表
        """
        if not text or not text.strip():
            return []
        
        # 提取时间线
        timeline = self._build_timeline(text)
        duration = self._extract_duration(text)
        
        # 计算置信度
        time_exprs = self.extract_time_expressions(text)
        order_matches = len(self.find_keywords(text, self.TIME_ORDER_WORDS))
        total_clues = len(time_exprs) + order_matches
        confidence = self.calculate_confidence(total_clues, max(len(timeline), 1), 0.1)
        
        if confidence < self.min_confidence and not timeline:
            return []
        
        chain = ExtractedTimeChain(
            chain_id=f"time_{datetime.now().strftime('%Y%m%d%H%M%S')}_{id(text) % 10000}",
            content=text[:self.max_chain_length],
            timeline=timeline[:15],
            duration=duration,
            extraction_confidence=confidence,
        )
        
        return [chain]
    
    def _build_timeline(self, text: str) -> List[Dict[str, Any]]:
        """构建时间线"""
        timeline = []
        sentences = self.split_sentences(text)
        
        # 方式1：从带时间表达式的句子中提取
        for sent in sentences:
            time_exprs = self.extract_time_expressions(sent)
            if time_exprs:
                for te in time_exprs:
                    timeline.append({
                        "time": te,
                        "event": sent,
                        "source": "time_expression",
                    })
                break  # 一个句子只取一个时间点
        
        # 方式2：从带顺序词的句子中提取
        for sent in sentences:
            for word in self.TIME_ORDER_WORDS:
                if word in sent:
                    # 检查是否已存在
                    existing = [t for t in timeline if t.get("event") == sent]
                    if not existing:
                        timeline.append({
                            "time": word,
                            "event": sent,
                            "source": "order_word",
                        })
                    break
        
        # 方式3：如果时间线太短，取所有带时间信息的句子
        if len(timeline) < 2:
            for sent in sentences:
                has_time = bool(self.extract_time_expressions(sent))
                if has_time:
                    existing = [t for t in timeline if t.get("event") == sent]
                    if not existing:
                        timeline.append({
                            "time": "unknown",
                            "event": sent,
                            "source": "time_inferred",
                        })
        
        # 按时间顺序排序（简单处理：顺序词在前，时间表达式在后）
        ordered = []
        seq_events = [t for t in timeline if t.get("source") == "order_word"]
        time_events = [t for t in timeline if t.get("source") != "order_word"]
        
        # 合并并按出现顺序排列
        all_events = timeline
        
        return all_events[:15]
    
    def _extract_duration(self, text: str) -> str:
        """提取总时长"""
        # 匹配时间段模式
        patterns = [
            r'(?:持续|历时|共计|总计)[了]?[\s]*[\d.]+[\s]*[分时天周月年]',
            r'[\d.]+[\s]*[分时天周月年][\s]*(?:之久|左右|以上|以内)',
            r'(?:从|自).*?(?:到|至|止).*?(?:共|历时)[\s]*[\d.]+[\s]*[分时天周月年]',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group()
        
        # 简单匹配时间范围
        range_pattern = r'(?:从|自)\s*([\d:/\-年月中日]+)\s*(?:到|至)\s*([\d:/\-年月中日]+)'
        match = re.search(range_pattern, text)
        if match:
            return f"{match.group(1)} 到 {match.group(2)}"
        
        return ""
    
    @staticmethod
    def extract_time_expressions(text: str) -> List[str]:
        """
        提取时间表达式（增强版）
        
        Args:
            text: 输入文本
        
        Returns:
            时间表达式列表
        """
        expressions = set()
        
        for pattern in TimeExtractor.TIME_PATTERNS:
            for match in re.finditer(pattern, text):
                expressions.add(match.group())
        
        # 中文时间词
        cn_time_words = [
            "今天", "明天", "昨天", "后天", "前天",
            "早上", "上午", "中午", "下午", "晚上", "深夜",
            "刚才", "刚刚", "不久", "立刻", "马上",
            "最近", "近期", "长期以来", "当前",
        ]
        for word in cn_time_words:
            if word in text:
                expressions.add(word)
        
        # 相对时间
        rel_patterns = [
            r'\d+[天日时月年][前前后后]',
            r'[前后昨今明][天日年]',
        ]
        for pattern in rel_patterns:
            for match in re.finditer(pattern, text):
                expressions.add(match.group())
        
        return list(expressions)