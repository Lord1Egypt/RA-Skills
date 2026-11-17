#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
心理引擎 — 读者心理/角色心理/续读动机分析

驱动数据: 10-reader-psychology.md (蔡格尼克效应/峰终定律/五驱力)
        06-satisfaction-psychology.md (爽点类型/节奏公式)
"""

import re

from .engine_base import EngineBase


class PsychologyEngine(EngineBase):
    """读者与角色心理分析引擎"""

    engine_name = "psychology"
    engine_tags = ["阅读体验", "读者心理"]

    def analyze(self, text, **kwargs):
        issues = []
        issues.extend(self.check_zeigarnik(text))
        issues.extend(self.check_peak_end(text))
        issues.extend(self.check_witness_effect(text))
        issues.extend(self.check_motivation_diversity(text))
        return issues

    EMOTIONAL_ARCS = {
        "V形": {"谷底": "60-70%", "特点": "虐完翻盘，治愈急速回升"},
        "倒V形": {"高点": "40-50%", "特点": "甜完刀死，坠落比上升快"},
        "W形": {"起伏": 3, "特点": "多反转猜不到，每峰比前高"},
        "递进形": {"特点": "层层打脸升级，无回落"},
        "延迟满足": {"铺垫": "70-80%", "特点": "隐忍后大爆发"},
        "急转形": {"转折": "70-80%", "特点": "结尾颠覆，前面线索能回看"},
    }

    @staticmethod
    def check_zeigarnik(text: str) -> list:
        """蔡格尼克效应: 章末是否留下认知未完成状态"""
        last_300 = text[-300:]
        has_question = '?' in last_300 or '？' in last_300
        has_hook_words = any(w in last_300 for w in ['突然', '就在这时', '没想到', '可是', '但是', '却'])
        if not has_question and not has_hook_words:
            return ["章末缺认知未完成状态 — 建议留开放式问题或悬念"]
        return []

    @staticmethod
    def check_peak_end(text: str) -> list:
        """峰终定律: 最后200字质量分析"""
        ending = text[-200:]
        # 检查结尾是否有力（非句号平淡结束）
        if ending.rstrip().endswith(('。', '.', '，', ',')):
            return ["章末以平淡标点结束 — 建议用更有力的结尾提升终末体验"]
        return []



    # === 爽点心理学 (源自06-satisfaction-psychology.md) ===

    @staticmethod
    def check_satisfaction_diversity(chapters: list) -> list:
        """检查连续3章是否同类型爽点, 建议交替"""
        issues = []
        if len(chapters) < 3:
            return []
        recent_types = [c.get("satisfaction_type", "") for c in chapters[-3:]]
        if len(set(recent_types)) == 1 and recent_types[0]:
            issues.append(f"连续3章同一爽点类型[{recent_types[0]}] - 建议交替不同类型(打脸/升级/收集/攻略/守护/战略)")
        return issues

    @staticmethod
    def check_witness_effect(text: str) -> list:
        """见证者效应检测: 关键打脸场景是否有群众见证"""
        witness_words = ["众人", "围观", "看着", "目睹", "见证", "目光", "注视", "惊呼"]
        has_witness = any(w in text for w in witness_words)
        # 检测打脸/逆袭关键词
        face_slapping = any(w in text for w in ["打脸", "碾压", "击败", "秒杀", "反杀"])
        if face_slapping and not has_witness:
            return ["打脸场景缺少见证者 - 按照社会比较理论, 有见证者的爽度提升2-3倍"]
        return []

    @staticmethod
    def estimate_satisfaction(text: str, previous_repression: int = 2, chapter_num: int = 0) -> dict:
        """爽点强度预计算"""
        score = 5  # baseline
        factors = []
        # 压抑时长加成
        repression_bonus = min(3, previous_repression * 0.5)
        if previous_repression >= 3:
            factors.append(f"压抑{previous_repression}章 +{repression_bonus:.1f}")
            score += repression_bonus
        # 冲突强度
        conflict_words = ["爆", "杀", "震", "碎", "轰", "死", "败"]
        conflict_count = sum(text.count(w) for w in conflict_words)
        if conflict_count > 10:
            factors.append(f"冲突密集 +2")
            score += 2
        elif conflict_count > 5:
            factors.append(f"中等冲突 +1")
            score += 1
        # 见证者
        witness_count = text.count("众人") + text.count("目光") + text.count("围观")
        if witness_count > 0:
            factors.append(f"有见证者 +1.5")
            score += 1.5
        return {"score": round(min(10, score), 1), "factors": factors}

    @staticmethod
    def check_satisfaction_type(text: str) -> dict:
        """检测爽点类型"""
        types = {
            "打脸爽": len(re.findall(r'碾压|吊打|踩|秒杀|虐|横扫', text)),
            "升级爽": len(re.findall(r'突破|晋级|升级|进阶|蜕变', text)),
            "收集爽": len(re.findall(r'获得|得到|获取|收获|收集', text)),
            "守护爽": len(re.findall(r'保护|守护|拯救|捍卫', text)),
            "战略爽": len(re.findall(r'算计|布局|谋划|智斗', text)),
        }
        return types

    @staticmethod
    def check_motivation_diversity(text: str) -> list:
        """续读动机多样性检测：认知型/情感型/成就型"""
        cognitive = len(re.findall(r'秘密|真相|答案|为什么|怎么回事', text))
        emotional = len(re.findall(r'爱|恨|哭|笑|温柔|心疼|在乎', text))
        achievement = len(re.findall(r'目标|任务|挑战|胜利|成功', text))
        active = sum(1 for v in [cognitive, emotional, achievement] if v > 3)
        if active < 2:
            return [f"续读动机仅{active}种 (需至少2种: 认知{cognitive}/情感{emotional}/成就{achievement})"]
        return []

    @staticmethod
    def full_eval(text: str) -> dict:
        return {
            "zeigarnik": PsychologyEngine.check_zeigarnik(text),
            "peak_end": PsychologyEngine.check_peak_end(text),
            "satisfaction": PsychologyEngine.check_satisfaction_type(text),
            "motivation": PsychologyEngine.check_motivation_diversity(text),
        }

    # === 欲望编码检测 (源自01-web-novel-creation-principles) ===
    @staticmethod
    def check_desire_coding(text):
        """欲望编码扫描: 检测每章激活的欲望类型"""
        desires = {
            "权力欲": ["掌控", "命令", "统领", "征服", "统治", "碾压"],
            "征服欲": ["击败", "打败", "压制", "压制", "推倒"],
            "占有欲": ["获得", "夺取", "拥有", "归我", "得到"],
            "求知欲": ["秘密", "真相", "发现", "探索", "弄清楚"],
            "拯救欲": ["救", "保护", "守护", "拯救", "救助"],
        }
        activated = {}
        for name, markers in desires.items():
            cnt = sum(text.count(w) for w in markers if w in text)
            if cnt > 0:
                activated[name] = cnt
        return {
            "types": list(activated.keys()),
            "count": len(activated),
            "pass": len(activated) >= 1,
            "warning": "未激活任何欲望编码" if not activated else "",
        }
    # === 峰终定律检测 (源自10-reader-psychology.md) ===
    @staticmethod
    def peak_end_check(chapter_scores):
        """最后3章质量不得低于全书平均"""
        if not chapter_scores or len(chapter_scores) < 4:
            return {"verdict": "数据不足"}
        overall_avg = sum(chapter_scores) / len(chapter_scores)
        end_avg = sum(chapter_scores[-3:]) / 3
        return {
            "overall_avg": round(overall_avg, 1),
            "end_avg": round(end_avg, 1),
            "verdict": "结尾质量达标" if end_avg >= overall_avg else "结尾质量低于全篇平均 - 峰终定律: 结尾权重极高",
            "suggestion": "强化最后3章" if end_avg < overall_avg else "",
        }