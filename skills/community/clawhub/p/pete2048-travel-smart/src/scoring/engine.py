# -*- coding: utf-8 -*-
"""
推荐评分引擎
根据 PRD 定义的权重体系，对高速出口/住宿/打车点进行多因子加权评分
"""
import math
from typing import List
from ..config.settings import SCORING_WEIGHTS


class ScoreEngine:
    """
    多因子加权评分引擎

    评分范围：0-100 分，越高越好
    各因子得分均归一化到 0-100，再用权重加权求和
    """

    # 各场景的有效因子（避免用不存在的 key 导致 fallback 到默认值）
    SCENE_FACTORS = {
        "highway": ["distance", "rating", "detour"],
        "hotel": ["distance", "rating", "price", "next_day"],
        "taxi": ["distance", "rating", "detour"],
    }

    def __init__(self, scene: str = "highway"):
        self.scene = scene
        self.weights = SCORING_WEIGHTS.get(scene, SCORING_WEIGHTS["highway"])
        self.factors = self.SCENE_FACTORS.get(scene, ["distance", "rating"])

    # ---- 单因子得分计算 ----

    def _dist_score(self, meters: float) -> float:
        """
        距离得分：越近越高，指数衰减
        基准：30km 处得分约 37，10km 处得分约 72
        """
        if meters >= 100_000:
            return 0.0
        return 100 * math.exp(-meters / 30_000)

    def _rating_score(self, rating: float) -> float:
        """评分得分：直接映射到 0-100（高德评分 1-5）"""
        return (rating / 5.0) * 100

    def _price_score(self, price: float, budget: float = 300) -> float:
        """
        价格得分：越接近预算中值越高
        budget = 用户预算（默认 300）
        100 元以下：80分（便宜但可能质量差，适度惩罚）
        300 元：95分（最接近预算）
        500 元以上：60分
        """
        if price <= 0:
            return 50.0
        # 价格偏离度：偏离越多分越低
        ratio = budget / max(price, 1)
        # ratio > 1 说明比预算便宜，越便宜分越低（惩罚太便宜的）
        # ratio < 1 说明超预算，越超分越低
        deviation = abs(1 - ratio)
        return max(0, 100 * (1 - deviation * 0.5))

    def _detour_score(self, meters: float) -> float:
        """
        绕行得分：绕行越少越好，指数衰减
        基准：1km 处得分约 93，5km 处得分约 71
        """
        if meters >= 50_000:
            return 0.0
        return 100 * math.exp(-meters / 15_000)

    def _next_day_score(self, meters: float) -> float:
        """
        次日顺路得分：距次日目的地越近越好
        基准：20km 处得分约 67，50km 处得分约 36
        """
        if meters >= 200_000:
            return 0.0
        return 100 * math.exp(-meters / 50_000)

    # ---- 主评分函数 ----

    def score(self, item: dict) -> float:
        """
        对单个候选项计算综合评分

        Args:
            item: {
                "distance": float,           # 距当前位置（米）
                "rating": float,             # 高德评分（1-5）
                "price": float,              # 价格（元）
                "detour": float,             # 绕行距离（米）
                "next_day_distance": float,  # 距次日目的地距离（米）
            }

        Returns:
            0-100 分
        """
        w = self.weights
        total = 0.0

        if "distance" in self.factors:
            total += w.get("distance", 0) * self._dist_score(item.get("distance", 999999))

        if "rating" in self.factors:
            total += w.get("rating", 0) * self._rating_score(item.get("rating", 3.0))

        if "price" in self.factors:
            total += w.get("price", 0) * self._price_score(
                item.get("price", 0), item.get("budget", 300)
            )

        if "detour" in self.factors:
            total += w.get("detour", 0) * self._detour_score(item.get("detour", 0))

        if "next_day" in self.factors:
            total += w.get("next_day", 0) * self._next_day_score(
                item.get("next_day_distance", 999999)
            )

        return round(total, 1)

    def rank(self, items: List[dict], top: int = 3) -> List[dict]:
        """
        对候选项列表打分并排序

        Returns: 排序后的列表（每项包含 score 字段）
        """
        scored = []
        for item in items:
            s = self.score(item)
            scored.append({**item, "score": s})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top]
