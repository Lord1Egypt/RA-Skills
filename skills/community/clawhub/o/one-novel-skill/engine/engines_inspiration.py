#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""创意灵感引擎 - 题材组合/爆款趋势"""

from datetime import datetime
from collections import defaultdict


class InspirationEngine:
    """创意生成与评估"""

    GENRE_MATRIX = [
        ("修仙+科技", "修仙科技流"), ("都市+修仙", "都市修仙"),
        ("悬疑+恋爱", "悬疑恋爱"), ("历史+穿越", "历史穿越"),
        ("游戏+现实", "游戏现实"), ("末世+建造", "末世建造"),
        ("科幻+修仙", "科幻修仙"), ("直播+修仙", "直播修仙"),
        ("鉴宝+悬疑", "鉴宝悬疑"), ("美食+治愈", "美食治愈"),
        ("系统+修仙", "系统修仙"), ("校园+异能", "校园异能"),
    ]

    HOT_TRENDS = [
        ("系统流", "飞卢/番茄", "高"), ("都市异能", "起点/番茄", "高"),
        ("年代文", "番茄/七猫", "中"), ("规则怪谈", "番茄/起点", "高"),
        ("无限流", "起点/番茄", "中"), ("第四天灾", "起点/飞卢", "中"),
    ]


    def analyze(self, text, **kwargs):
        """创意灵感分析"""
        issues = []
        genre = kwargs.get("genre", "")
        if genre:
            hot = self.hot_now()
            if hot:
                issues.append(f"[创意] 当前热门趋势: {hot[0]["name"]}（热度{hot[0]["heat"]}）")
        return issues

    @staticmethod
    def suggest(genre, constraints=None):
        suggestions = []
        for combo, name in InspirationEngine.GENRE_MATRIX:
            if genre in combo:
                suggestions.append(name)
        if not suggestions:
            for combo, name in InspirationEngine.GENRE_MATRIX:
                parts = combo.split("+")
                if any(genre in p for p in parts):
                    suggestions.append(name)
        return suggestions[:5] or [genre+"+热门元素"]

    @staticmethod
    def combine(a, b):
        for combo, name in InspirationEngine.GENRE_MATRIX:
            key = a+"+"+b
            key2 = b+"+"+a
            if combo == key or combo == key2:
                return name
        return a+" x "+b+" (跨类型融合)"

    @staticmethod
    def hot_now(platform="番茄"):
        results = []
        for name, plat, heat in InspirationEngine.HOT_TRENDS:
            if platform in plat:
                results.append({"name": name, "heat": heat, "platforms": plat})
        return results or [{"name": t[0], "heat": t[2], "platforms": t[1]} for t in InspirationEngine.HOT_TRENDS[:3]]

    # === 创新矩阵定位 (源自15-cross-genre-creation) ===
    @staticmethod
    def innovation_matrix(familiarity=5, novelty=5):
        """创新矩阵: 题材熟悉度×手法创新度 -> 四个象限"""
        f = max(1, min(10, familiarity))
        n = max(1, min(10, novelty))
        if f >= 6 and n >= 6:
            return {"quadrant": "创新先驱", "risk": "中", "advice": "熟悉题材+新手法 = 最佳创新"}
        if f >= 6 and n < 6:
            return {"quadrant": "稳定输出", "risk": "低", "advice": "熟悉题材+稳手法 = 安全策略"}
        if f < 6 and n >= 6:
            return {"quadrant": "试验先锋", "risk": "偏高", "advice": "新题材+新手法 = 高风险高回报"}
        return {"quadrant": "蓝海探索", "risk": "中高", "advice": "新题材+稳手法 = 需优质补充"}
    # === 跨作品融合技法 (源自03-crossover-techniques.md) ===
    @staticmethod
    def crossover_fusion(world_a, world_b):
        """评估两个世界观融合的可行性"""
        issues = []
        # 等级平衡
        tiers = {"日常系": 1, "校园系": 2, "都市系": 3, "冒险系": 4, "战斗系": 5, "奇幻系": 6, "龙傲天": 7}
        ta = tiers.get(world_a, 3)
        tb = tiers.get(world_b, 3)
        if abs(ta - tb) > 3:
            issues.append(f"世界观等级差{abs(ta-tb)} - 平衡性差, 建议弱势方获得同级别加成")
        return {"compatible": len(issues) == 0, "issues": issues,
                "suggestion": "跨界融合: " + world_a + " x " + world_b} if not issues else ""

    @staticmethod
    def suggest_crossover(genre_a, genre_b):
        """建议混搭类型"""
        known = [
            ("都市", "修仙", "都市修仙"), ("悬疑", "恋爱", "悬疑恋爱"),
            ("奇幻", "科幻", "奇幻科幻"), ("修仙", "游戏", "修仙游戏"),
        ]
        for a, b, result in known:
            if (genre_a == a and genre_b == b) or (genre_a == b and genre_b == a):
                return {"mix": result, "recommend": "双强并立, 各50%占比"}
        return {"mix": genre_a + "+" + genre_b, "recommend": "主类型70%+辅类型30%"}