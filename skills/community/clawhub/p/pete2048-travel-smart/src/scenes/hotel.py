# -*- coding: utf-8 -*-
"""
场景二：途中临时找住宿

评分逻辑（按 PRD）：
  Score = 距离得分×0.20 + 评分得分×0.20 + 价格得分×0.30 + 次日顺路得分×0.30
"""
from loguru import logger
from ..clients.amap import AmapClient
from ..scoring.engine import ScoreEngine


class HotelScene:
    """
    住宿推荐场景

    核心价值：告诉用户「哪个酒店有停车场+价格合适+第二天行程顺路」
    """

    # 酒店类型关键词（非连锁）
    HOTEL_KEYWORDS = ["酒店", "宾馆", "旅馆", "民宿", "招待所", "公寓"]

    def __init__(self, amap_client: AmapClient):
        self.amap = amap_client
        self.engine = ScoreEngine(scene="hotel")

    def _is_hotel(self, poi: dict) -> bool:
        """判断 POI 是否为住宿类型"""
        name = poi.get("name", "")
        poi_type = poi.get("type", "")
        combined = name + poi_type
        return any(kw in combined for kw in self.HOTEL_KEYWORDS)

    def _estimate_price(self, poi: dict) -> float:
        """
        从酒店名称/类型估算价格区间（元）
        返回估算的每晚价格
        """
        name = poi.get("name", "")
        t = poi.get("type", "")

        # 已知连锁品牌价格分段
        chain_prices = {
            "7天": 120, "如家": 150, "汉庭": 180, "格林豪泰": 140,
            "全季": 300, "亚朵": 350, "麗枫": 280,
            "锦江之星": 130, "速8": 130, "尚客优": 120,
            "布丁": 90, "99旅馆": 80,
            "万豪": 600, "喜来登": 700, "希尔顿": 650, "洲际": 550,
            "凯悦": 500, "香格里拉": 700,
            "维也纳": 200, "城市便捷": 150,
            "榻榻米": 200, "民宿": 250,
        }
        for brand, price in chain_prices.items():
            if brand in name:
                return price

        # 五星级估算
        if any(k in t for k in ["五星级", "豪华"]):
            return 600
        if any(k in t for k in ["四星级", "高档"]):
            return 350
        if any(k in t for k in ["三星级", "舒适"]):
            return 180
        return 220  # 默认中档

    def _estimate_rating(self, poi: dict) -> float:
        """
        估算酒店评分（1-5）
        """
        name = poi.get("name", "")
        t = poi.get("type", "")
        # 知名连锁品牌有稳定的评分
        high_rated = ["全季", "亚朵", "麗枫", "希尔顿", "万豪", "喜来登",
                       "洲际", "凯悦", "香格里拉", "维也纳", "汉庭", "如家"]
        for brand in high_rated:
            if brand in name:
                return 4.3
        # 五星级
        if any(k in t for k in ["五星级", "豪华"]):
            return 4.5
        if any(k in t for k in ["四星级", "高档"]):
            return 4.0
        if any(k in t for k in ["三星级", "舒适"]):
            return 3.5
        return 3.8  # 默认

    def score_hotel(
        self,
        hotel_poi: dict,
        user_lng: float,
        user_lat: float,
        budget: float = 300,
        next_day_lng: float = None,
        next_day_lat: float = None,
    ) -> dict:
        """对单个酒店计算完整评分"""
        if not hotel_poi.get("location"):
            return {**hotel_poi, "distance": 999_999, "rating": 3.5, "price": 300, "next_day_distance": 999_999, "score": 0}

        h_lng, h_lat = self.amap.parse_location(hotel_poi["location"])
        if h_lng is None:
            return {**hotel_poi, "distance": 999_999, "rating": 3.5, "price": 300, "next_day_distance": 999_999, "score": 0}

        dist = self.amap.haversine_meters(user_lng, user_lat, h_lng, h_lat)
        price = self._estimate_price(hotel_poi)
        rating = self._estimate_rating(hotel_poi)

        # 次日目的地顺路程度
        next_day_dist = 999_999
        if next_day_lng and next_day_lat:
            next_day_dist = self.amap.haversine_meters(h_lng, h_lat, next_day_lng, next_day_lat)

        scored = self.engine.score({
            "distance": dist,
            "rating": rating,
            "price": price,
            "budget": budget,
            "next_day_distance": next_day_dist,
        })

        return {
            **hotel_poi,
            "lng": h_lng,
            "lat": h_lat,
            "distance": round(dist),
            "rating": rating,
            "price": price,
            "next_day_distance": round(next_day_dist),
            "score": scored,
        }

    def recommend(
        self,
        user_lng: float,
        user_lat: float,
        budget: int = 300,
        people: int = 2,
        next_day_lng: float = None,
        next_day_lat: float = None,
        top: int = 3,
    ) -> dict:
        """
        核心推荐入口
        """
        logger.info(f"住宿推荐: ({user_lng},{user_lat}) 预算{budget}元 {people}人")

        # 搜索附近所有 POI，用关键词过滤出酒店
        pois = self.amap.around_search(
            lng=user_lng, lat=user_lat,
            keywords="酒店",
            radius=10_000,
            count=50,
        )
        logger.info(f"高德返回 {len(pois)} 个 POI")

        # 过滤真实酒店
        hotels = [p for p in pois if self._is_hotel(p)]
        logger.info(f"过滤后 {len(hotels)} 家酒店")

        if not hotels:
            return {
                "scene": "hotel",
                "user_location": {"lng": user_lng, "lat": user_lat},
                "budget": budget,
                "hotels": [],
                "total_found": 0,
            }

        # 逐个评分
        scored_hotels = []
        for h in hotels:
            scored = self.score_hotel(h, user_lng, user_lat, budget, next_day_lng, next_day_lat)
            scored_hotels.append(scored)

        ranked = self.engine.rank(scored_hotels, top=top)
        logger.info(f"评分完成，Top {len(ranked)}")

        return {
            "scene": "hotel",
            "user_location": {"lng": user_lng, "lat": user_lat},
            "budget": budget,
            "next_day": {"lng": next_day_lng, "lat": next_day_lat} if next_day_lng else None,
            "hotels": ranked,
            "total_found": len(hotels),
        }

    def format_result(self, result: dict) -> str:
        """格式化输出"""
        hotels = result.get("hotels", [])
        if not hotels:
            return "未找到合适的住宿，请尝试扩大范围或调整预算"

        lines = ["🏨 **推荐住宿**\n"]
        for i, h in enumerate(hotels, 1):
            medal = ["🥇", "🥈", "🥉"][i - 1] if i <= 3 else f"{i}️⃣"
            nd = h.get("next_day_distance", 999_999)
            nd_str = f"距次日目的 {nd/1000:.1f}km" if nd < 200_000 else "距次日目的较远"
            lines.append(
                f"{medal} **{h['name']}**（综合得分 {h['score']}）\n"
                f"   └ 距你 {h['distance']/1000:.1f}km"
                f"   · 价格 ¥{h['price']}/晚"
                f"   · ⭐{h['rating']:.1f}分\n"
                f"   └ {nd_str}\n"
                f"   └ {h.get('address', '地址未知')}"
            )
        lines.append(f"\n💡 推荐【{hotels[0]['name']}】（综合得分最高）")
        return "\n".join(lines)
