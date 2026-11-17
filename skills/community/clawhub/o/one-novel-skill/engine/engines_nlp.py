#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自然语言引擎 — 描写质量/句式/感官检测

驱动数据: literature/chinese/11-description-practice.md (五感法则/动词优先/句式变化)
"""

import re

from .engine_base import EngineBase

# 预编译正则
class NLPEngine(EngineBase):
    """自然语言质量检测引擎"""

    engine_name = "nlp"
    engine_tags = ["NLP", "语言"]

    def analyze(self, text, **kwargs):
        return self.full_check(text)

    @staticmethod
    def analyze_senses(text: str) -> dict:
        senses = {
            "视觉": len(re.findall(r'看见|看到|见到|映入|呈现|展现', text)),
            "听觉": len(re.findall(r'听见|听到|声响|声音|悄|静|吵', text)),
            "触觉": len(re.findall(r'冰凉|温暖|炙热|刺痛|柔软|坚硬', text)),
            "嗅觉": len(re.findall(r'闻到|香气|味|芬芳|恶臭|腥', text)),
            "味觉": len(re.findall(r'尝到|苦|甜|酸|辣|咸|涩', text)),
        }
        return senses

    @staticmethod
    def check_sensory(text: str, threshold: int = 2) -> list:
        issues = []
        paras = [p for p in text.split('\n') if len(p) > 30]
        for i, p in enumerate(paras[:20]):
            senses = NLPEngine.analyze_senses(p)
            active = sum(1 for v in senses.values() if v > 0)
            if active < threshold:
                issues.append(f"段落{i+1}: 仅{active}种感官 (需{threshold}+)")
                break
        return issues

    @staticmethod
    def check_weak_verbs(text: str) -> list:
        patterns = [
            (r'慢慢地\w+', '慢慢地'),
            (r'轻轻地\w+', '轻轻地'),
            (r'缓缓地\w+', '缓缓地'),
            (r'静静地\w+', '静静地'),
            (r'用力地\w+', '用力地'),
        ]
        issues = []
        for pat, desc in patterns:
            matches = re.findall(pat, text)
            if matches:
                issues.append(f"弱动词'{desc}'x{len(matches)} — 替换为强动词")
        return issues

    @staticmethod
    def check_sentence_length(text: str) -> list:
        sents = [s.strip() for s in re.split(r'[。！？\n]', text) if len(s.strip()) >= 2]
        if not sents:
            return []
        avg = sum(len(s) for s in sents) / len(sents)
        has_excite = any(c in text for c in ['!', '！', '?', '？', '怒', '杀', '冲'])
        if has_excite and avg > 20:
            return [f"情感场景句长{avg:.0f}字 — 建议短句化至15字内"]
        return []



    # === 描写实务增强 (源自11-description-practice.md) ===

    @staticmethod
    def analyze_sentence_texture(text: str) -> dict:
        """句法纹理分析: 短句/长句/断裂句分布"""

# 预编译正则
        sents = [s.strip() for s in re.split(r"[。！？\n]", text) if s.strip()]
        if not sents:
            return {"short_pct": 0, "medium_pct": 0, "long_pct": 0}
        total = max(len(sents), 1)
        short = sum(1 for s in sents if len(s) <= 8)
        medium = sum(1 for s in sents if 9 <= len(s) <= 25)
        long_ = sum(1 for s in sents if len(s) > 25)
        return {"short_pct": round(short/total, 3), "medium_pct": round(medium/total, 3),
                "long_pct": round(long_/total, 3), "total": total}

    @staticmethod
    def check_sensory_diversity(text: str) -> list:
        """检查段落感官调用多样性: 连续3句仅视觉则标记"""

# 预编译正则
        issues = []
        paras = [p for p in text.split("\n") if len(p) > 40]
        for i, p in enumerate(paras[:10]):
            senses = NLPEngine.analyze_senses(p)
            active = sum(1 for v in senses.values() if v > 0)
            if active <= 1 and senses.get("视觉", 0) > 0:
                issues.append(f"段落{i+1}: 仅{active}种感官(视觉) - 建议叠加听觉/触觉/嗅觉")
                break
        return issues

    @staticmethod
    def check_emotion_environment_match(text: str) -> list:
        """检测情绪-环境一致性"""

# 预编译正则
        issues = []
        # 暴力/冲突语境下的正面环境描写
        conflict_words = ["杀", "战", "死", "斗", "挣", "暴", "怒"]
        sunny_words = ["阳光", "晴朗", "灿烂", "明媚", "温暖"]
        sad_words = ["悲伤", "痛哭", "哀", "绝望"]
        beautiful_env = ["美丽", "芬芳", "鸟语", "花香", "彩虹"]

        if any(w in text for w in conflict_words):
            if any(w in text for w in sunny_words):
                issues.append("战斗/冲突场景中阳光明媚 - 环境与情绪不匹配")
        if any(w in text for w in sad_words):
            if any(w in text for w in beautiful_env):
                issues.append("悲伤场景中美丽环境 - 建议用阴雨/凋零衬托")
        return issues

    @staticmethod
    def full_check(text: str) -> dict:
        return {
            "sensory": NLPEngine.check_sensory(text),
            "weak_verbs": NLPEngine.check_weak_verbs(text),
            "sentence_length": NLPEngine.check_sentence_length(text),
        }

    # === 句式节奏检测 (源自11-on-writing-well.md 津瑟) ===
    @staticmethod
    def check_sentence_rhythm(text):
        """句子长度标准差检测: 连续5句以上偏差<20%标记单调"""

# 预编译正则
        sents = [s for s in re.split(r"[。！？]", text) if s.strip()]
        if len(sents) < 5:
            return {"verdict": "句子数不足5"}
        lengths = [len(s) for s in sents[:20]]
        avg = sum(lengths) / len(lengths)
        variance = sum((l - avg)**2 for l in lengths) / len(lengths)
        std = variance ** 0.5
        cv = std / max(avg, 1)  # 变异系数
        return {
            "avg_len": round(avg, 1),
            "std": round(std, 1),
            "cv": round(cv, 2),
            "verdict": "节奏多变" if cv > 0.3 else "节奏略单调" if cv > 0.2 else "节奏单调 - 需交替短/中/长句",
        }