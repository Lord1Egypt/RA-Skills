# -*- coding: utf-8 -*-
"""
场景一：高速堵车 → 推荐最佳下高速出口

评分逻辑（按 PRD）：
  Score = 距离得分×0.35 + 评分得分×0.35 + 绕行得分×0.30
  餐饮评分根据出口附近 POI 情况综合估算（连锁品牌多=高评分）
"""
import math
from typing import Optional
from loguru import logger
from ..clients.amap import AmapClient
from ..scoring.engine import ScoreEngine

# 已知连锁餐饮品牌（国内高速出口常见）
CHAIN_BRANDS = {
    "肯德基", "麦当劳", "汉堡王", "必胜客", "永和大王",
    "老乡鸡", "真功夫", "吉野家", "味千拉面", "海底捞",
    "绿茶", "外婆家", "西贝", "云海肴", "南锣肥猫",
    "德克士", "华莱士", "正新鸡排", "绝味鸭脖", "周黑鸭",
    "便利蜂", "711", "全家", "罗森",
}


class HighwayScene:
    """
    高速出口推荐场景

    核心价值：告诉用户「哪个出口下去有好吃的，绕行不远，值得停」
    """

    def __init__(self, amap_client: AmapClient):
        self.amap = amap_client
        self.engine = ScoreEngine(scene="highway")

    def _estimate_dining_rating(self, lng: float, lat: float) -> tuple:
        """
        估算出口附近餐饮评分（0-5分）+ 返回 Top3 餐饮名称

        Returns: (rating: float, dining_pois: list[dict])  # dict包含 name/distance/type
        """
        pois = self.amap.around_search(
            lng=lng, lat=lat,
            keywords="餐饮",
            radius=3000,
            count=20,
        )
        if not pois:
            return 2.5, []

        # 记录知名连锁
        chain_count = 0
        has_chain = False
        chain_names = []
        for poi in pois:
            name = poi.get("name", "")
            for brand in CHAIN_BRANDS:
                if brand in name:
                    chain_count += 1
                    has_chain = True
                    chain_names.append(name)
                    break

        # 提取 Top3 餐饮名称
        dining_pois = [
            {"name": p.get("name", ""), "distance": p.get("distance", 0), "type": p.get("type", "")}
            for p in pois[:3]
        ]

        # 评分计算
        count_score = min(5, len(pois)) / 5.0 * 2.0
        chain_score = 0.5 if has_chain else 0.0
        rating = 3.0 + chain_score + count_score
        return min(5.0, round(rating, 1)), dining_pois

    def score_exit(
        self,
        exit_poi: dict,
        user_lng: float,
        user_lat: float,
        destination: str = "",
    ) -> dict:
        """
        对单个出口计算完整评分数据

        Returns: 包含 distance / detour / rating / score 的 dict
        """
        # 1. 计算距用户距离
        if not exit_poi.get("location"):
            return {**exit_poi, "distance": 999_999, "rating": 2.5, "detour": 0, "score": 0}

        exit_lng, exit_lat = self.amap.parse_location(exit_poi["location"])
        if exit_lng is None:
            return {**exit_poi, "distance": 999_999, "rating": 2.5, "detour": 0, "score": 0}

        dist = self.amap.haversine_meters(user_lng, user_lat, exit_lng, exit_lat)

        # 2. 查询餐饮评分和 Top3 餐饮
        rating, dining_pois = self._estimate_dining_rating(exit_lng, exit_lat)

        # 3. 计算绕行代价
        #    绕行 = 出口下高速后折返到主路的额外距离
        #    估算：绕行 ≈ 出口距主路距离 × 2（上下各一次）
        detour = int(dist * 0.25)  # 约 1/4 的距离作为绕行代价

        # 4. 送入评分引擎
        scored = self.engine.score({
            "distance": dist,
            "rating": rating,
            "detour": detour,
        })

        return {
            **exit_poi,
            "distance": round(dist),
            "rating": rating,
            "detour": detour,
            "dining_pois": dining_pois,
            "score": scored,
            "exit_lng": exit_lng,
            "exit_lat": exit_lat,
        }

    def recommend(
        self,
        highway_name: str,
        user_lng: float,
        user_lat: float,
        destination: str = "",
        top: int = 3,
    ) -> dict:
        """
        核心推荐入口

        Args:
            highway_name: 高速名，如 "G4"
            user_lng, user_lat: 用户当前位置
            destination: 目的地（可选，用于判断回程顺路）
            top: 返回前几名

        Returns:
            {
                "scene": "highway",
                "highway": highway_name,
                "user_location": {"lng": ..., "lat": ...},
                "exits": [exit1, exit2, exit3],  # 已按 score 排序
                "total_found": N,
            }
        """
        logger.info(f"高速出口推荐: {highway_name} 附近({user_lng},{user_lat})")

        # 1. 搜索附近高速出口（50km 半径）
        pois = self.amap.around_search(
            lng=user_lng,
            lat=user_lat,
            keywords="高速公路出口",
            radius=50_000,
            count=30,
        )

        logger.info(f"高德返回 {len(pois)} 个 POI 出口")

        if not pois:
            return {"scene": "highway", "highway": highway_name,
                    "user_location": {"lng": user_lng, "lat": user_lat},
                    "exits": [], "total_found": 0}

        # 2. 过滤有效出口（有坐标）
        pois = [p for p in pois if p.get("location")]
        logger.info(f"有效出口 {len(pois)} 个")

        # 3. 逐个出口评分
        scored_exits = []
        for poi in pois:
            scored = self.score_exit(poi, user_lng, user_lat, destination)
            scored_exits.append(scored)

        # 4. 排序取 Top
        ranked = self.engine.rank(scored_exits, top=top)

        logger.info(f"评分完成，Top {len(ranked)}")

        return {
            "scene": "highway",
            "highway": highway_name,
            "user_location": {"lng": user_lng, "lat": user_lat},
            "destination": destination,
            "exits": ranked,
            "total_found": len(pois),
        }

    def format_result(self, result: dict) -> str:
        """格式化为友好文字输出（用于 CLI）"""
        exits = result.get("exits", [])
        if not exits:
            return "未找到合适的下高速出口，请尝试扩大范围"

        lines = [f"🚗 **高速出口推荐**（{result.get('highway', '')}）\n"]
        for i, e in enumerate(exits, 1):
            medal = ["🥇", "🥈", "🥉"][i - 1] if i <= 3 else f"{i}️⃣"
            lines.append(
                f"{medal} **{e['name']}**（综合得分 {e['score']}）\n"
                f"   └ 距你 {e['distance'] / 1000:.1f}km"
                f"   · 绕行约 {e['detour'] / 1000:.1f}km"
                f"   · 餐饮评分 ⭐{e['rating']:.1f}\n"
            )

        lines.append(f"\n💡 推荐【{exits[0]['name']}】，绕行短且餐饮评分高")
        return "\n".join(lines)
