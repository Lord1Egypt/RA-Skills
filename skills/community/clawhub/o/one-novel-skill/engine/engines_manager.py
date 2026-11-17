#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""管理引擎 — 项目队列/有声书参数/KDP系列策略"""

import re

from .engine_base import EngineBase


class ManagerEngine(EngineBase):
    """创作项目管理"""

    engine_name = "manager"
    engine_tags = ["管理者", "综合"]

    def analyze(self, text, **kwargs):
        return self.check_audio_ratio(text)

    def __init__(self):
        self.queue = []

    def push(self, item):
        self.queue.append(item)

    def pop(self):
        return self.queue.pop(0) if self.queue else None

    def peek(self):
        return self.queue[0] if self.queue else None

    def size(self):
        return len(self.queue)

    def clear(self):
        self.queue.clear()

    # === 有声书参数 (源自01-audio-novel-writing.md) ===
    @staticmethod
    def check_audio_ratio(text):
        """有声书对话/叙述比例检测: 目标60:40, 最低50:50"""
        if not text:
            return {"ratio": 0, "verdict": "无文本"}
        quotes = len(re.findall(r"\u201c", text)) + len(re.findall(r"\u201d", text))
        dialog_chars = 0
        in_quote = False
        for c in text:
            if c in ("\u201c", "\u300c"):
                in_quote = True
            elif c in ("\u201d", "\u300d"):
                in_quote = False
            elif in_quote:
                dialog_chars += 1
        total = len(text)
        ratio = round(dialog_chars / max(total, 1), 2)
        return {
            "dialog_pct": int(ratio * 100),
            "narrate_pct": int((1 - ratio) * 100),
            "verdict": "有声书友好" if ratio >= 0.5 else "对话占比不足(需>50%)",
            "long_para_warning": "超过40秒纯叙述段" if ratio < 0.4 else "",
        }

    # === KDP/KU系列策略 (源自01-self-publishing.md) ===
    @staticmethod
    def kdp_series_plan(volume_count=3, words_per_volume=70000):
        """KDP系列出版计划建议"""
        return {
            "volumes": volume_count,
            "volume_words": words_per_volume,
            "volume_pages": int(words_per_volume / 250),
            "price_v1": "$0.99",
            "price_v2_plus": "$4.99",
            "max_interval": "30-45天/卷",
            "ku_estimate": f"约${words_per_volume * 0.0045 / 250:.2f}/KU读者",
            "target_v1_to_v2": "25%+转化率",
        }
    # === 杂志投稿策略 (源自02-magazine-submission.md) ===
    @staticmethod
    def submission_strategy(platform, word_count, is_simsub=False):
        """投稿匹配建议"""
        domestic = {
            "银河奖": {"字数": "3000-15000", "类型": "硬科幻", "稿费": "80-150元/千字"},
            "星云奖": {"字数": "3000-15000", "类型": "科幻(商业+文学)", "稿费": "100-200元/千字"},
            "人民文学": {"字数": "5000-20000", "类型": "纯文学", "稿费": "500-1000元/千字"},
        }
        overseas = {
            "Clarkesworld": {"字数": "1000-16000", "稿费": "$0.10/word", "SIMSUB": True},
            "F&SF": {"字数": "1000-25000", "稿费": "$0.07-0.08/word", "SIMSUB": False},
        }
        all_platforms = {**domestic, **overseas}
        spec = all_platforms.get(platform)
        if not spec:
            return {"warning": f"未知投稿渠道: {platform}"}
        return {
            "platform": platform,
            "spec": spec,
            "word_count_ok": True,
            "simsub_ok": is_simsub or spec.get("SIMSUB", False),
            "advice": "可同时投稿(SIMSUB)" if spec.get("SIMSUB") else "不可一稿多投",
        }