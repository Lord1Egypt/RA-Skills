#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""算法引擎 - 文本模式匹配/N元词频/重复度检测"""

import re
from collections import Counter

from .engine_base import EngineBase

# 预编译正则常量
_RE_CJK_2_4 = re.compile(r"[一-鿿]{2,4}")
_RE_CJK = re.compile(r"[一-鿿]")



class AlgorithmEngine(EngineBase):
    """文本模式匹配与优化"""

    engine_name = "algorithm"
    engine_tags = ["统计分析"]

    def analyze(self, text, **kwargs):
        return self.repetition_rate(text)

    @staticmethod
    def match(text, pattern):
        matches = re.findall(pattern, text)
        return list(set(matches))

    @staticmethod
    def optimize(items, score_fn):
        scored = [(score_fn(i), i) for i in items]
        scored.sort(key=lambda x: -x[0])
        return [i for _, i in scored[:5]]

    @staticmethod
    def find_patterns(texts, min_freq=3):
        words = []
        for t in texts:
            words.extend(re.findall(r"[\u4e00-\u9fff]{2,4}", t))
        freq = Counter(words)
        return {w: c for w, c in freq.items() if c >= min_freq}

    @staticmethod
    def repetition_rate(text):
        """检测用词重复度"""
        words = re.findall(r"[\u4e00-\u9fff]{2,4}", text)
        if not words:
            return {"rate": 0, "verdict": "无文本"}
        total = len(words)
        unique = len(set(words))
        rate = round(1 - unique / total, 3)
        freq = Counter(words)
        top_3 = [w for w, _ in freq.most_common(3)]
        return {"rate": rate, "unique": unique, "total": total,
                "top_3": top_3, "verdict": "用词丰富" if rate < 0.3
                else "重复偏高" if rate < 0.5 else "严重重复"}

    @staticmethod
    def ngram_freq(text, n=2):
        chars = [c for c in text if "\u4e00" <= c <= "\u9fff"]
        if len(chars) < n:
            return []
        ngrams = ["".join(chars[i:i+n]) for i in range(len(chars)-n+1)]
        freq = Counter(ngrams).most_common(10)
        return [{"ngram": g, "count": c} for g, c in freq]

    # === 场景复用检测 (源自scene-usage.md) ===
    @staticmethod
    def detect_scene_reuse(chapters):
        """检测跨章节的场景/情节模式复用"""
        if not chapters or len(chapters) < 3:
            return []
        issues = []
        # 检测结构复用: 每章开头句式是否雷同
        openings = []
        for i, ch in enumerate(chapters[:10]):
            if isinstance(ch, str) and len(ch) > 50:
                first_30 = ch[:30]
                openings.append(first_30)
        if len(openings) >= 3:
            # 检查开头前10字相似度
            similar = 0
            for i in range(len(openings)):
                for j in range(i+1, len(openings)):
                    a = openings[i][:10]
                    b = openings[j][:10]
                    if a == b:
                        similar += 1
            if similar > 2:
                issues.append(f"章节开头{similar}处雷同 - 建议多样化开头句式")
        # 检测描写复用: 相同情绪词汇
        emotion_counts = {}
        for ch in chapters:
            for word in ["愤怒", "悲伤", "高兴", "紧张", "害怕"]:
                if word in str(ch):
                    emotion_counts[word] = emotion_counts.get(word, 0) + 1
        for word, cnt in emotion_counts.items():
            if cnt > len(chapters) * 0.5 and cnt > 3:
                issues.append(f"'{word}'出现{cnt}章 - 情绪表达方式需多样化")
        return issues

    @staticmethod
    def analyze_full(text: str, **kwargs) -> dict:
        """全维度算法分析接口"""
        return {
            "repetition": AlgorithmEngine.repetition_rate(text),
            "ngram": AlgorithmEngine.ngram_freq(text, kwargs.get("n", 2)),
            "verdict": "算法分析完成"
        }