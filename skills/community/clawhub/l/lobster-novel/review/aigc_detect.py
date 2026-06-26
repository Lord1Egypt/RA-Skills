#!/usr/bin/env python3
"""
lobster-novel: AIGC / AI-tell detection (standalone module)
Separated from quality_check.py for clearer responsibility.
"""
import re
from typing import List, Dict, Tuple

AIGC_PATTERNS: Dict[str, List[str]] = {
    # ── 通用AI味 ──────────────────────────────────────────────
    "tell_not_show": [
        r"他明白[了]?", r"她明白[了]?", r"他懂[了]?", r"她懂[了]?",
        r"他意识到", r"她意识到",
        r"他感到", r"她感到",
        r"内心充满", r"心中涌起",
        r"他仿佛", r"她仿佛",
    ],
    "empty_emotion": [
        r"感到.*(悲伤|高兴|愤怒|开心|难过|孤独|恐惧)",
        r"内心.*(平静|波澜|挣扎|复杂)",
        r"一种.*的.*感[觉受]",
    ],
    "god_view": [
        r"所有人[都]?没想到",
        r"就在这时",
        r"只见",
        r"突然",
        r"原来如此",
        r"就这样",
    ],
    "template_phrase": [
        r"众所周知",
        r"不言而喻",
        r"不得不承认",
        r"真是太",
        r"多么.*啊",
        r"真是.*啊",
    ],
    "over_explain": [
        r"这.*意味着",
        r"换句话说",
        r"也就是[说]?",
        r"其实[就]?是",
    ],
    "perception_filler": [
        r"他[看听]到", r"她[看听]到",
        r"他[看][见到]", r"她[看][见到]",
        r"只见他", r"只见她",
    ],
    # ── 中文网文特有AI味 ──────────────────────────────────────
    "cliched_expression": [
        # 套路化表情/动作描写
        r"眼中闪过一丝",
        r"嘴角扬起一抹",
        r"心中一凛",
        r"眉头微皱",
        r"瞳孔一缩",
        r"脸色一变",
        r"冷笑一声",
        r"轻哼一声",
        r"冷哼一声",
        r"嘴角勾起一抹",
        r"眼中寒光一闪",
        r"心中暗道",
        r"心中大喜",
        r"心中一喜",
        r"心中一沉",
        r"心中一震",
        r"心头一紧",
        r"心底泛起",
    ],
    "dialogue_ai_tell": [
        # 对话AI味：过于工整、缺少口语化
        r"说道\"[^\"]*\"",
        r"淡淡道",
        r"冷冷道",
        r"淡淡一笑",
        r"微微一笑",
        r"冷笑道",
        r"轻声道",
        r"沉声道",
        r"厉声道",
        r"语气中带着",
        r"声音中带着一丝",
        r"语气冰冷",
        r"语气平淡",
        r"语气中透着",
    ],
    "pacing_issues": [
        # 节奏感问题：平铺直叙、缺少张力
        r"接下来[，,]",
        r"然后[，,]",
        r"随后[，,]",
        r"就这样[，,]",
        r"过了[一二三四五六七八九十]+[天日]",
        r"转眼间[，,]",
        r"不知不觉[，,]",
    ],
    "no_memorable_moment": [
        # 金句/名场面检测：识别过度平淡叙述
        r"(没有|并无|并无什么|没什么)[特别不同]"
    ],
    "character_voice_inconsistency": [
        # 人物声线标记：对话过于"标准"，缺少角色个性
        r"[他她]\s*说[道着]\s*[:：]",
        r"说[完罢]后\s*[,，]",
    ],
    "shuangdian_density": [
        # 爽点密度检测：网文每章应有1-2个爽点/转折
        # 标记爽点相关词汇
        r"打脸",
        r"碾压",
        r"秒杀",
        r"震惊",
        r"目瞪口呆",
        r"不可思议",
        r"难以置信",
        r"全场哗然",
        r"一片哗然",
        r"众人皆惊",
    ],
}


class AIGCDetector:
    """Detect AI-typical writing patterns."""

    @staticmethod
    def scan(text: str) -> List[dict]:
        """Scan text and return list of (category, pattern, match_text, line_num)."""
        results = []
        lines = text.split("\n")
        for cat, patterns in AIGC_PATTERNS.items():
            for pat in patterns:
                for m in re.finditer(pat, text):
                    ln = text[:m.start()].count("\n") + 1
                    results.append({
                        "category": f"AI-tell: {cat}",
                        "pattern": pat,
                        "match": m.group()[:40],
                        "line": ln,
                        "severity": "P1",
                        "suggestion": "Show, don't tell — use actions, expressions, or sensory details",
                    })
        return results

    @staticmethod
    def score(text: str) -> float:
        """Compute an AIGC score: 0 (clean) to 100 (heavy AI-tell)."""
        hits = AIGCDetector.scan(text)
        total_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
        if total_chars < 100:
            return 0.0
        # Penalty: each hit reduces score
        base = 100.0
        for h in hits:
            base -= 5.0
        return max(0.0, base)

    @staticmethod
    def get_problematic_paragraphs(text: str, threshold: int = 3) -> List[Tuple[int, str, int]]:
        """Return (para_index, paragraph_text, issue_count) for paragraphs with threshold+ issues."""
        paragraphs = [p for p in text.split("\n\n") if p.strip()]
        results = []
        for i, para in enumerate(paragraphs):
            hits = AIGCDetector.scan(para)
            if len(hits) >= threshold:
                results.append((i, para[:100], len(hits)))
        return results
