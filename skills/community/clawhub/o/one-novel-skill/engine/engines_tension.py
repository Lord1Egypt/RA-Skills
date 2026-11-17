#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .engine_base import EngineBase


class TensionEngine(EngineBase):

    engine_name = "tension"
    engine_tags = ["节奏", "张力"]

    def analyze(self, text, **kwargs):
        issues = []
        r = self.check_push_pull(text)
        if r: issues.extend(r if isinstance(r, list) else [str(r)])
        return issues

    @staticmethod
    def calibrate(high_points, total, baseline=3, peak=8, peak_radius=2):
        if baseline < 0 or peak < 0:
            raise ValueError("baseline 和 peak 必须 >= 0")
        if peak_radius < 0:
            raise ValueError("peak_radius 必须 >= 0")
        curve = [baseline] * total
        for ch in high_points:
            if 0 <= ch < total:
                start = max(0, ch - (peak_radius - 1))
                end = min(total, ch + peak_radius)
                for i in range(start, end):
                    curve[i] = max(curve[i], peak)
        return curve

    @staticmethod
    def detect_drop(values, threshold=0.3):
        drops = []
        for i in range(1, len(values)):
            if values[i] < values[i-1] * threshold:
                drops.append(i)
        return drops

    @staticmethod
    def check_cycle(chapter, total):
        pos = (chapter - 1) % 5
        labels = ["钩子建立", "期待积累", "期待积累", "兑现释放", "新周期"]
        return {"阶段": labels[pos], "位置": pos}
    # === 推拉张力检测 (源自03-romance-arc.md) ===
    @staticmethod
    def check_push_pull(text):
        """推拉张力: 爱情题材中推(冲突)拉(亲近)比例"""
        if not text:
            return {"ratio": 0, "verdict": "无数据"}
        push_words = ["拒绝", "争吵", "误解", "冷", "离开", "推", "生气", "不理"]
        pull_words = ["靠近", "温柔", "理解", "拥抱", "温暖", "原谅", "陪伴", "等"]
        push_count = sum(text.count(w) for w in push_words)
        pull_count = sum(text.count(w) for w in pull_words)
        total = push_count + pull_count
        if total == 0:
            return {"ratio": 0, "verdict": "无推拉信号"}
        ratio = round(push_count / total, 2)
        return {
            "push": push_count, "pull": pull_count,
            "push_ratio": ratio,
            "verdict": "推拉平衡(推:拉=6:4理想)" if 0.5 <= ratio <= 0.7
                       else "推>拉过多" if ratio > 0.7
                       else "拉>推过多, 缺乏张力"}

    @staticmethod
    def analyze_full(text: str, **kwargs) -> dict:
        """全维度张力分析接口"""
        return {
            "push_pull": TensionEngine.check_push_pull(text),
            "cycle": TensionEngine.check_cycle(kwargs.get("ch", 1), kwargs.get("total", 100)),
            "verdict": "张力分析完成"
        }