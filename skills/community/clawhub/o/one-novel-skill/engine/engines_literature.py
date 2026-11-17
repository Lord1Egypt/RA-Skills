#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文学引擎 - 文学手法/叙事视角/美学评分"""

import re

from .engine_base import EngineBase

class LiteratureEngine(EngineBase):
    """文学质量评估"""

    engine_name = "literature"
    engine_tags = ["文学", "审美"]

    def analyze(self, text, **kwargs):
        issues = []
        ascore = self.aesthetic_score(text)
        if ascore < 0.5: issues.append(f"审美评分 {ascore:.2f}")
        return issues

    DEVICES = [
        "象征", "隐喻", "反讽", "对比", "排比", "设问", "反问",
        "夸张", "拟人", "借代", "对偶", "层递", "反复",
    ]

    NARRATIVE_VIEWS = {
        "都市": ("第三人称有限", "快"), "仙侠": ("第三人称全知", "中"),
        "悬疑": ("第一人称", "慢快交替"), "言情": ("双视角交替", "中"),
        "科幻": ("第三人称有限", "中"), "历史": ("第三人称全知", "中"),
    }

    @staticmethod
    def literary_devices(text):
        found = []
        if re.search(r'["\u201c].*?["\u201d]', text):
            found.append("对话")
        if re.search(r'[。！？]难道[^。！？]*[？?]', text):
            found.append("反问")
        if re.search(r'似乎|仿佛|犹如|像', text):
            found.append("比喻")
        if re.search(r'却|但|然而', text):
            found.append("转折")
        for d in LiteratureEngine.DEVICES:
            if d in text and d not in found:
                found.append(d)
        return found

    @staticmethod
    def narrative_technique(genre):
        result = LiteratureEngine.NARRATIVE_VIEWS.get(genre, ("第三人称有限", "中"))
        return {"genre": genre, "view": result[0], "pace": result[1]}

    @staticmethod
    def aesthetic_score(text):
        score = 0.3
        devices = LiteratureEngine.literary_devices(text)
        score += len(devices) * 0.04
        words = re.findall(r"[\u4e00-\u9fff]{2,4}", text)
        if words:
            score += (len(set(words)) / len(words)) * 0.15
        sents = [s for s in re.split(r"[。！？\n]", text) if s.strip()]
        if len(sents) >= 3:
            lens = [len(s) for s in sents if s.strip()]
            if lens:
                variance = sum((l - sum(lens)/len(lens))**2 for l in lens) / len(lens)
                score += min(0.1, variance / 500)
        return min(1.0, score)

    # === 体裁一致性检查 (源自04-creative-writing) ===
    @staticmethod
    def check_genre_consistency(text, genre):
        """体裁一致性: 叙事模式是否符合宣称的题材"""
        genre_expect = {
            "悬疑": ["谜", "线索", "真相", "秘密", "推理"],
            "言情": ["爱", "喜欢", "心", "温柔", "甜蜜"],
            "玄幻": ["修炼", "突破", "境界", "灵气", "法宝"],
            "都市": ["公司", "上班", "钱", "手机", "车"],
        }
        expected = genre_expect.get(genre, [])
        if not expected:
            return []
        score = sum(text.count(w) for w in expected)
        min_score = len(expected)
        if score < min_score * 0.3:
            cn = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
            if cn > 200:
                return [f"体裁'{genre}'一致性偏低(命中{score}/{min_score}期望词) - 建议加入类型标志性元素"]
        return []
    # === 复调叙事检测 (源自10-the-art-of-the-novel.md 昆德拉) ===
    @staticmethod
    def check_polyphony(chapters):
        """多线叙事复调性: 各线索是否独立且有主题呼应"""
        if not chapters or len(chapters) < 5:
            return {"verdict": "章节过少"}
        # 检测是否有多个视角/线索

# 预编译正则
        pov_markers = set()
        for ch in chapters[:20]:
            if isinstance(ch, str):
                names = re.findall(r"[\u4e00-\u9fff]{2,3}(?=[:：])", ch[:500])
                for n in names[:2]:
                    pov_markers.add(n)
        if len(pov_markers) >= 2:
            return {"pov_count": len(pov_markers), "verdict": f"多视角({len(pov_markers)}个)"}
        return {"pov_count": 1, "verdict": "单视角"}

    @staticmethod
    def check_existential_code(character_data):
        """存在编码检测: 角色行为是否围绕核心关键词"""
        if not isinstance(character_data, dict):
            return []
        issues = []
        code = character_data.get("existential_code", [])
        if not code or len(code) < 3:
            issues.append("存在编码不足3个 - 昆德拉: 角色本质由3-5个存在编码定义")
        return issues