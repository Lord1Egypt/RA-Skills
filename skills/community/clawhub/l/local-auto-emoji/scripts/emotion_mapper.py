#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情绪分析模块
- 基于对话内容判断阿狸当前情绪
- 结合外部因素（天气、工作时间等）
- 输出 8 种情感之一
"""

import json
import os
import time
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime

class EmotionAnalyzer:
    """情绪分析器"""

    EMOTIONS = ["happy", "angry", "sad", "shy", "work", "meme", "surprised", "cool", "flying_kiss", "hug", "cute", "blink"]

    # 情绪关键词映射（权重）
    EMOTION_KEYWORDS = {
        "happy": ["开心", "高兴", "愉快", "棒", "太好了", "耶", "happy", "nice", "great", "awesome", "喜欢", "爱"],
        "angry": ["生气", "愤怒", "讨厌", "烦", "滚", "混蛋", "damn", "shit", "fuck", "怒了", "气死", "火大"],
        "sad": ["难过", "伤心", "哭", "泪", "委屈", "抑郁", "sad", "depressed", "想哭", "心疼", "不好受"],
        "shy": ["害羞", "脸红", "腼腆", "不好意思", " shy", "尴尬", "结巴", "扭捏", "低头", "遮脸"],
        "work": ["工作", "加班", "项目", "deadline", "会议", "需求", "开发", "bug", "上线", "老板", "同事", "职场"],
        "meme": ["搞笑", "笑死", "梗", "太逗了", "lol", "haha", "233", "滑稽", "离谱", "整活", "玩梗"],
        "surprised": ["惊讶", "震惊", "哇", "卧槽", "什么", "竟然", "没想到", "amazing", "unbelievable", "天呐"],
        "cool": ["酷", "帅", "厉害", "牛逼", "强", "大佬", "cool", "awesome", "霸气", "拽", "潮"],
        "flying_kiss": ["飞吻", "么么哒", "mua", "亲亲", "爱心发射", "biu", "发射爱心", "比心", "love you", "send kiss"],
        "hug": ["抱抱", "拥抱", "要抱抱", "抱紧", "温暖拥抱", " hugs", "hug me", "抱一个", "求抱抱", "蹭蹭"],
        "cute": ["可爱", "卡哇伊", "萌", "好可爱", "萌萌哒", "cute", "adorable", "卖萌", "qwq", "ovo", "捏捏"],
        "blink": ["眨眼", "wink", "放电", "挑逗", "你懂的", "😉", "eyebrow", "single eye"]
    }

    # 外部因素影响权重
    EXTERNAL_FACTORS = {
        "weather_good": {"happy": +0.1, "cool": +0.05},
        "weather_bad": {"sad": +0.1, "work": +0.05},
        "working_hours": {"work": +0.2, "happy": -0.1},
        "off_hours": {"happy": +0.1, "meme": +0.1},
        "heavy_load": {"angry": +0.15, "sad": +0.1},
        "low_load": {"happy": +0.1, "cool": +0.05}
    }

    def __init__(self, log_file: Optional[str] = None):
        self.log_file = log_file or Path(__file__).parent.parent / "config" / "emotion_log.json"
        self.current_emotion = "happy"
        self.emotion_scores = {e: 0.0 for e in self.EMOTIONS}
        self._load_history()

    def _load_history(self):
        """加载情绪历史"""
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        else:
            self.history = []

    def _save_history(self, emotion: str, trigger: str, context: str):
        """记录情绪事件"""
        entry = {
            "timestamp": int(time.time()),
            "datetime": datetime.now().isoformat(),
            "emotion": emotion,
            "trigger": trigger,
            "context": context[:200]  # 截断
        }
        self.history.append(entry)
        # 只保留最近 100 条
        if len(self.history) > 100:
            self.history = self.history[-100:]

        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    def analyze(self, message: str, external_factors: Optional[Dict] = None) -> str:
        """
        分析当前情绪
        message: 用户最新消息（或阿狸自己的输出）
        external_factors: 外部因素字典（weather, workload 等）
        返回：8 种情感之一
        """
        # 1. 基于关键词的初始分数
        scores = {e: 0.0 for e in self.EMOTIONS}

        lower_msg = message.lower()
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in lower_msg:
                    scores[emotion] += 1.0

        # 2. 外部因素调整
        if external_factors:
            factor_score = self._apply_external_factors(external_factors)
            for e, delta in factor_score.items():
                if e in scores:
                    scores[e] += delta

        # 3. 历史情绪惯性（避免频繁切换）
        if self.current_emotion in scores:
            scores[self.current_emotion] += 0.2  # 惯性奖励

        # 4. 选择最高分
        best_emotion = max(scores, key=scores.get)

        # 如果所有分数都为0，保持当前情绪或默认 happy
        if scores[best_emotion] == 0:
            best_emotion = self.current_emotion if self.current_emotion else "happy"

        # 5. 记录情绪切换
        if best_emotion != self.current_emotion:
            self._save_history(
                emotion=best_emotion,
                trigger="text_analysis",
                context=message[:100]
            )
            self.current_emotion = best_emotion

        return best_emotion

    def _apply_external_factors(self, factors: Dict) -> Dict[str, float]:
        """应用外部因素权重"""
        result = {}
        for factor, value in factors.items():
            if factor in self.EXTERNAL_FACTORS:
                for emotion, delta in self.EXTERNAL_FACTORS[factor].items():
                    result[emotion] = result.get(emotion, 0) + delta
        return result

    def get_current_emotion(self) -> str:
        """获取当前情绪"""
        return self.current_emotion

    def set_emotion(self, emotion: str, trigger: str = "manual"):
        """手动设置情绪（用于测试）"""
        if emotion in self.EMOTIONS:
            self.current_emotion = emotion
            self._save_history(emotion, trigger, "Manual override")

    def reset(self):
        """重置为默认情绪"""
        self.current_emotion = "happy"
        self.emotion_scores = {e: 0.0 for e in self.EMOTIONS}


if __name__ == "__main__":
    # 测试
    analyzer = EmotionAnalyzer()
    print(f"[Test] 当前情绪: {analyzer.get_current_emotion()}")

    test_messages = [
        "今天真是个好日子！",
        "气死我了，这个 bug 太烦了",
        "呜呜呜，我好难过",
        "这个太搞笑了，笑死",
        "我要去开会了，好忙"
    ]

    for msg in test_messages:
        emotion = analyzer.analyze(msg)
        print(f"'{msg}' → {emotion}")
