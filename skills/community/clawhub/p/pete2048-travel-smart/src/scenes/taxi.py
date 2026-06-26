# -*- coding: utf-8 -*-
"""
场景三：景点拥堵 → 推荐最佳打车点

评分逻辑（按 PRD）：
  Score = 距离得分×0.40 + 评分得分×0.20 + 绕行得分×0.30 + 价格得分×0.10
  核心：步行近 + 好停车 + 离景点近
"""
from loguru import logger
from ..clients.amap import AmapClient
from ..scoring.engine import ScoreEngine


class TaxiScene:
    """
    打车点推荐场景

    核心价值：告诉用户「在哪里停车等车去景点最省事」
    """

    def __init__(self, amap_client: AmapClient):
        self.amap = amap_client
        self.engine = ScoreEngine(scene="taxi")

    def _estimate_parking_rating(self, poi: dict) -> float:
        """估算停车场评分（1-5分）"""
        name = poi.get("name", "")
        poi_type = poi.get("type", "")
        combined = name + poi_type
        # 大型商业停车场（管理好）
        if any(k in combined for k in ["万豪", "希尔顿", "洲际", "凯悦", "商业中心", "万达", "银泰", "万象城"]):
            return 4.3
        # 公共设施配套停车场
        if any(k in combined for k in ["医院", "学校", "政府", "体育馆", "会展中心", "博物馆", "图书馆"]):
            return 4.0
        # 路边/占道停车场（管理差）
        if any(k in combined for k in ["路边", "占道", "道路"]):
            return 2.8
        return 3.5

    def find_pickup_points(self, lng: float, lat: float, radius_m: int = 3000) -> list:
        """
        查找适合作为打车点的位置
        优先搜索「停车场」类型 POIOI
        """
        pois = self.amap.around_search(
            lng=lng,
            lat=lat,
            keywords="停车场",
            radius=radius_m,
            count=30,
        )
        return pois

    def score_pickup_point(
        self,
        poi: dict,
        user_lng: float,
        user_lat: float,
        dest_lng: float,
        dest_lat: float,
    ) -> dict:
        """对单个打车点计算完整评分"""
        if not poi.get("location"):
            return {**poi, "distance": 999_999, "dest_distance": 0, "rating": 3.5, "score": 0}

        p_lng, p_lat = self.amap.parse_location(poi["location"])
        if p_lng is None:
            return {**poi, "distance": 999_999, "dest_distance": 0, "rating": 3.5, "score": 0}

        # 用户到打车点的距离
        dist_from_user = self.amap.haversine_meters(user_lng, user_lat, p_lng, p_lat)
        # 打车点到目的地的距离
        dist_to_dest = self.amap.haversine_meters(p_lng, p_lat, dest_lng, dest_lat)
        rating = self._estimate_parking_rating(poi)

        scored = self.engine.score({
            "distance": dist_from_user,
            "rating": rating,
            "detour": dist_to_dest,
        })

        return {
            **poi,
            "lng": p_lng,
            "lat": p_lat,
            "distance": round(dist_from_user),
            "dest_distance": round(dist_to_dest),
            "rating": rating,
            "score": scored,
        }

    def recommend(
        self,
        user_lng: float,
        user_lat: float,
        destination_lng: float,
        destination_lat: float,
        top: int = 3,
    ) -> dict:
        """
        核心推荐入口
        """
        logger.info(f"打车点推荐: ({user_lng},{user_lat}) → ({destination_lng},{destination_lat})")

        pois = self.find_pickup_points(user_lng, user_lat, radius_m=3000)
        logger.info(f"高德返回 {len(pois)} 个 POI")

        if not pois:
            return {
                "scene": "taxi",
                "user_location": {"lng": user_lng, "lat": user_lat},
                "destination": {"lng": destination_lng, "lat": destination_lat},
                "points": [],
                "total_found": 0,
            }

        scored = []
        for p in pois:
            scored.append(
                self.score_pickup_point(p, user_lng, user_lat, destination_lng, destination_lat)
            )

        ranked = self.engine.rank(scored, top=top)
        logger.info(f"评分完成，Top {len(ranked)}")

        return {
            "scene": "taxi",
            "user_location": {"lng": user_lng, "lat": user_lat},
            "destination": {"lng": destination_lng, "lat": destination_lat},
            "points": ranked,
            "total_found": len(pois),
        }

    def format_result(self, result: dict) -> str:
        """格式化输出"""
        points = result.get("points", [])
        if not points:
            return "未找到合适的打车点，请尝试扩大范围"

        lines = ["🚕 **推荐打车点**\n"]
        for i, p in enumerate(points, 1):
            medal = ["🥇", "🥈", "🥉"][i - 1] if i <= 3 else f"{i}️⃣"
            lines.append(
                f"{medal} **{p['name']}**（综合得分 {p['score']}）\n"
                f"   └ 距你 {p['distance']/1000:.1f}km（步行）\n"
                f"   └ 距目的地 {p['dest_distance']/1000:.1f}km（打车）\n"
                f"   └ 评分 ⭐{p['rating']:.1f}分"
            )

        lines.append(f"\n💡 推荐【{points[0]['name']}】，步行距离最短且停车场评分高")
        return "\n".join(lines)
