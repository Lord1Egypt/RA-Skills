#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stability_checker.py — 长篇稳定性检查引擎

参考：网文创作的系统化工程报告 §7 + 网络小说创作全维深度研究报告_2026 §9
核心功能：
  - 人物出现频率分布检查（突然消失30章以上标记异常）
  - 情感节奏检测（连续5章以上情绪单一）
  - 伏笔关键词密度检测
  - 情绪节律分析（高潮/缓冲/日常/铺垫分布）
"""

import re
import math
import logging
from collections import Counter, defaultdict
from typing import List, Dict, Any

_log = logging.getLogger("stability_checker")

# 情绪关键词词典
EMOTION_KEYWORDS = {
    "爽": ["打脸", "碾压", "突破", "逆袭", "秒杀", "震惊", "碾压", "一鸣惊人"],
    "燃": ["热血", "战", "拼", "吼", "爆发", "冲天", "不屈"],
    "虐": ["泪", "痛", "伤", "离", "悲", "绝望", "牺牲"],
    "暖": ["笑", "抱", "安", "温馨", "守护", "陪伴", "温暖"],
    "疑": ["?", "？", "谁", "为什么", "秘密", "不对劲", "奇怪", "诡异"],
}

# 情绪节律阶段
RHYTHM_STAGES = ["高潮", "缓冲", "日常", "铺垫"]


class StabilityChecker:
    """长篇稳定性检查引擎 — 纯规则驱动，不依赖 LLM"""

    def __init__(self):
        self._chapter_texts: Dict[int, str] = {}
        self._character_history: Dict[str, List[int]] = defaultdict(list)

    # ========== 数据录入 ==========

    def feed_chapter(self, chapter: int, text: str):
        """录入一章正文"""
        self._chapter_texts[chapter] = text

    def feed_character(self, name: str, chapter: int):
        """记录角色在指定章节出现"""
        self._character_history[name].append(chapter)

    # ========== 检查方法 ==========

    def check_character_consistency(self, character_list: List[str] = None) -> List[str]:
        """检查角色出现频率分布

        如果一个角色在某个章节密集出现后突然消失30章以上，标记为异常。
        """
        issues = []
        chars = character_list or list(self._character_history.keys())
        max_chapter = max(self._chapter_texts.keys()) if self._chapter_texts else 0

        for name in chars:
            chapters = sorted(self._character_history.get(name, []))
            if len(chapters) < 2:
                continue

            # 检查最后出现的章节与当前最大章节的间隔
            last_chapter = chapters[-1]
            if max_chapter - last_chapter > 30:
                issues.append(
                    f"[稳定性] {name} 最后出现在第{last_chapter}章，已消失{max_chapter - last_chapter}章以上"
                )

            # 检查章节间最大间隔
            for i in range(1, len(chapters)):
                gap = chapters[i] - chapters[i - 1]
                if gap > 30:
                    issues.append(
                        f"[稳定性] {name} 在第{chapters[i-1]}章到第{chapters[i]}章间消失{gap}章"
                    )

        return issues

    def check_emotional_rhythm(self) -> List[str]:
        """统计每章结尾的情绪词，检测连续5章以上情绪单一"""
        issues = []
        emotion_chain = []

        for ch in sorted(self._chapter_texts.keys()):
            text = self._chapter_texts[ch]
            # 取末段150字
            ending = text[-150:]
            detections = {}
            for emo, keywords in EMOTION_KEYWORDS.items():
                count = sum(1 for kw in keywords if kw in ending)
                if count > 0:
                    detections[emo] = count

            dominant = max(detections, key=detections.get) if detections else "中性"
            emotion_chain.append((ch, dominant))

        # 检查连续5章以上情绪单一
        for emo_type in ["爽", "燃", "虐", "暖", "疑"]:
            chain = [c for c in emotion_chain if c[1] == emo_type]
            # 找连续序列
            streak = 0
            for i, (ch, emo) in enumerate(emotion_chain):
                if emo == emo_type:
                    streak += 1
                else:
                    if streak >= 5:
                        start_ch = emotion_chain[i - streak][0]
                        issues.append(
                            f"[节奏] 第{start_ch}-{emotion_chain[i-1][0]}章连续{streak}章{emo_type}情绪，建议插入其他情绪调节"
                        )
                    streak = 0

        return issues

    def check_foreshadow_density(self) -> List[str]:
        """检测伏笔关键词密度，标记需要重点关注的章节"""
        issues = []
        import math

        for ch in sorted(self._chapter_texts.keys()):
            text = self._chapter_texts[ch]
            # 伏笔关键词
            foreshadow_words = [
                "似乎", "好像", "隐约", "隐隐", "不对劲", "奇怪",
                "难道", "秘密", "谜", "预感", "不详", "诡异",
            ]
            count = sum(1 for w in foreshadow_words if w in text)

            # 密度计算
            total_chars = len(text)
            if total_chars > 0:
                density = count * 1000 / total_chars  # 每千字出现次数
                if density > 8:
                    issues.append(
                        f"[伏笔] 第{ch}章伏笔关键词密度偏高 ({density:.1f}/千字)，"
                        "检查是否有过度堆砌伏笔的倾向"
                    )
                elif density < 0.5 and total_chars > 1500:
                    issues.append(
                        f"[伏笔] 第{ch}章伏笔关键词密度偏低 ({density:.1f}/千字)，"
                        "建议在铺垫章节适当埋点"
                    )

        return issues

    def check_rhythm_distribution(self) -> Dict[str, Any]:
        """分析情绪节律分布（高潮/缓冲/日常/铺垫）"""
        if not self._chapter_texts:
            return {}

        total = len(self._chapter_texts)
        rhythm_counts = Counter()

        for ch, text in sorted(self._chapter_texts.items()):
            # 根据段落数量和内容判断节律
            paras = [p for p in text.split("\n") if p.strip()]
            avg_para = sum(len(p) for p in paras) / max(len(paras), 1) if paras else 0

            # 简单判断逻辑
            if avg_para > 150:  # 段落长 → 高潮/铺垫
                # 检测是否包含冲突词
                if any(w in text for w in ["战", "杀", "爆发", "撞", "轰"]):
                    rhythm = "高潮"
                else:
                    rhythm = "铺垫"
            elif avg_para < 80:  # 段落短 → 日常/缓冲
                if any(w in text for w in ["笑", "聊", "吃", "走", "日常"]):
                    rhythm = "日常"
                else:
                    rhythm = "缓冲"
            else:
                # 中等段落长 → 根据关键词
                if any(w in text for w in ["?", "？", "突然", "秘密"]):
                    rhythm = "铺垫"
                elif any(w in text for w in ["终", "完", "啊", "呼"]):
                    rhythm = "缓冲"
                else:
                    rhythm = "日常"

            rhythm_counts[rhythm] += 1

        return {
            "total_chapters": total,
            "distribution": dict(rhythm_counts),
            "analysis": {
                rh: f"{rhythm_counts.get(rh, 0)/total*100:.0f}%" for rh in RHYTHM_STAGES
            },
        }

    def run_all(self) -> Dict[str, Any]:
        """运行全部检查，返回综合报告"""
        char_issues = self.check_character_consistency()
        emotion_issues = self.check_emotional_rhythm()
        foreshadow_issues = self.check_foreshadow_density()
        rhythm = self.check_rhythm_distribution()

        return {
            "character_consistency": char_issues,
            "emotional_rhythm": emotion_issues,
            "foreshadow_density": foreshadow_issues,
            "rhythm_distribution": rhythm,
            "total_issues": len(char_issues) + len(emotion_issues) + len(foreshadow_issues),
        }

    def reset(self):
        self._chapter_texts.clear()
        self._character_history.clear()
